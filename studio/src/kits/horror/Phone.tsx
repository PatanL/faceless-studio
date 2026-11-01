// Smartphone with a group-chat app (chat.theme dark|light, chat.scale, chat.pinned), lock screen and incoming-call screen.
// The device is drawn at a native 600x1240 and scaled to fit its layer box.
// Original UI (generic dark messenger), not a copy of any real app.
import React from 'react';
import type {KitComponentProps} from '../../core/registry';
import {glitchAt, GlitchWrap} from './fx';
import {arr, atTime, clamp01, cueLevel, ease, num, obj, popIn, random, str} from './util';

export const PHONE_W = 600;
export const PHONE_H = 1240;
const BEZEL = 16;
const SW = PHONE_W - BEZEL * 2; // screen width
const SH = PHONE_H - BEZEL * 2;
const FONT = '"Montserrat", "Helvetica Neue", Arial, sans-serif';

type Member = {color?: string; initials?: string};
type Msg = {from?: string; text?: string; at?: number; me?: boolean; kind?: string};
type Typing = {from?: string; at?: number; until?: number};
type Banner = {at?: number; duration?: number; app?: string; title?: string; text?: string};

const AVATAR_COLORS = ['#7a5c8f', '#4f7a73', '#8f6a4a', '#4a628f', '#8f4a55', '#6b7a4a', '#5a5a7a'];
const colorFor = (name: string, members: Record<string, Member>) =>
	members[name]?.color ?? AVATAR_COLORS[Math.floor(random(`av-${name}`) * AVATAR_COLORS.length)];
const initialsFor = (name: string, members: Record<string, Member>) =>
	members[name]?.initials ??
	name
		.replace(/[^A-Za-z0-9 ]/g, '')
		.split(' ')
		.filter(Boolean)
		.map((w) => w[0])
		.join('')
		.slice(0, 2)
		.toUpperCase();

export const Avatar: React.FC<{name: string; members: Record<string, Member>; size: number}> = ({name, members, size}) => (
	<div
		style={{
			width: size,
			height: size,
			borderRadius: '50%',
			background: colorFor(name, members),
			color: 'rgba(255,255,255,0.92)',
			fontFamily: FONT,
			fontWeight: 800,
			fontSize: size * 0.38,
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
			flex: 'none',
			boxShadow: 'inset 0 -4px 0 rgba(0,0,0,0.18)',
		}}
	>
		{initialsFor(name, members)}
	</div>
);

// ---------------------------------------------------------------- status bar

const StatusBar: React.FC<{clock: string; battery: number; light?: boolean}> = ({clock, battery, light = true}) => {
	const c = light ? '#e8eaee' : '#111';
	return (
		<div style={{height: 54, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 40px 0 44px', fontFamily: FONT, fontWeight: 800, fontSize: 22, color: c}}>
			<span>{clock}</span>
			<svg width={110} height={24} viewBox="0 0 110 24">
				{[0, 1, 2, 3].map((i) => (
					<rect key={i} x={i * 9} y={18 - i * 5} width={6} height={6 + i * 5} rx={1.5} fill={c} opacity={i < 2 ? 1 : 0.35} />
				))}
				<path d="M48 9 a14 14 0 0 1 20 0 M51 13 a9 9 0 0 1 14 0" stroke={c} strokeWidth={2.6} fill="none" strokeLinecap="round" />
				<circle cx={58} cy={18} r={2.6} fill={c} />
				<rect x={76} y={5} width={28} height={15} rx={4} stroke={c} strokeWidth={2} fill="none" opacity={0.8} />
				<rect x={78.5} y={7.5} width={23 * clamp01(battery / 100)} height={10} rx={2} fill={battery < 20 ? '#e0313a' : c} />
				<rect x={105} y={9.5} width={2.5} height={6} rx={1} fill={c} opacity={0.8} />
			</svg>
		</div>
	);
};

// ---------------------------------------------------------------- chat

const MSG_FS = 30;
const BUBBLE_MAX = 380;

/** Chat colour themes. 'light' is a bright grey messenger (reads at a glance, glows in a dark room). */
type Theme = {
	bg: string; header: string; headerBorder: string; title: string; sub: string; back: string; status: boolean;
	bubble: string; text: string; alertBg: string; alertText: string; alertBorder: string; nameBright: number;
	dayBg: string; dayText: string; inputBg: string; inputText: string; icon: string; dots: string;
	pinBg: string; pinText: string; pinLabel: string; meText: string;
};
const THEMES: Record<string, Theme> = {
	dark: {
		bg: '#14171d', header: '#1b1f27', headerBorder: '#232833', title: '#eef0f3', sub: '#8a93a2', back: '#8fb0d8', status: true,
		bubble: '#262b34', text: '#eef0f3', alertBg: '#5a1d24', alertText: '#ffd9db', alertBorder: '#e0313a', nameBright: 1.6,
		dayBg: '#1e232c', dayText: '#7c8594', inputBg: '#262b34', inputText: '#6c7586', icon: '#5d6778', dots: '#9aa3b0',
		pinBg: '#20252e', pinText: '#dfe3ea', pinLabel: '#e0313a', meText: '#eef0f3',
	},
	light: {
		bg: '#dfe0e4', header: '#f4f4f6', headerBorder: '#c9cad0', title: '#14161b', sub: '#666c78', back: '#2f5b94', status: false,
		bubble: '#ffffff', text: '#15171c', alertBg: '#ffe3e5', alertText: '#7d0c16', alertBorder: '#d8232f', nameBright: 0.8,
		dayBg: '#c8c9cf', dayText: '#4c525e', inputBg: '#ffffff', inputText: '#9aa0aa', icon: '#7d838e', dots: '#80868f',
		pinBg: '#fbf3d9', pinText: '#2a2410', pinLabel: '#c0202b', meText: '#ffffff',
	},
};
const themeOf = (c: Record<string, unknown>) => THEMES[str(c.theme, 'dark')] ?? THEMES.dark;

/** Size of the chat at a given text scale (chat.scale): bigger text, fewer bubbles on screen. */
function dims(s: number) {
	const fs = MSG_FS * s;
	const avatar = Math.round(58 * Math.min(s, 1.25));
	return {fs, avatar, name: 21 * Math.min(s, 1.3), max: Math.min(BUBBLE_MAX * s, SW - 44 - avatar - 14 - 8)};
}

function estimateHeight(m: Msg, s = 1): number {
	const d = dims(s);
	if (m.kind === 'system') return d.fs * 0.7 * 1.3 + 20 + 18;
	const text = str(m.text, '');
	const charsPerLine = Math.max(8, Math.floor((d.max - 44) / (d.fs * 0.56)));
	const lines = text.split('\n').reduce((n, l) => n + Math.max(1, Math.ceil(l.length / charsPerLine)), 0);
	return lines * d.fs * 1.3 + 32 + (m.me ? 0 : d.name + 11) + 18;
}

const TypingDots: React.FC<{t: number; th?: Theme}> = ({t, th = THEMES.dark}) => (
	<div style={{display: 'flex', gap: 9, padding: '20px 26px', background: th.bubble, borderRadius: 30, borderTopLeftRadius: 8}}>
		{[0, 1, 2].map((i) => {
			const ph = (t * 2.4 - i * 0.18) % 1;
			const up = ph < 0.4 ? Math.sin((ph / 0.4) * Math.PI) : 0;
			return <div key={i} style={{width: 14, height: 14, borderRadius: 7, background: th.dots, opacity: 0.45 + 0.55 * up, transform: `translateY(${-up * 8}px)`}} />;
		})}
	</div>
);

/** A centred grey line inside the chat ("Management pinned a message", "Ben (5A) left the group"). */
const SystemLine: React.FC<{m: Msg; t: number; th: Theme; s: number}> = ({m, t, th, s}) => {
	const p = popIn(t, num(m.at, 0), 0.3);
	return (
		<div style={{alignSelf: 'center', marginTop: 18, opacity: clamp01(p * 2.5), maxWidth: SW - 80, textAlign: 'center', fontFamily: FONT, fontWeight: 700, fontSize: MSG_FS * 0.7 * s, lineHeight: 1.3, color: th.dayText, background: th.dayBg, padding: '8px 18px', borderRadius: 16}}>
			{str(m.text, '')}
		</div>
	);
};

/**
 * Pinned-message bar under the chat header. pinned: {text, at, label ('Pinned'), from,
 * editAt, editText}: at editAt the text is replaced by editText with a red flash and an "edited" tag.
 */
const PinnedBar: React.FC<{p: Record<string, unknown>; t: number; th: Theme; s: number}> = ({p, t, th, s}) => {
	const at = num(p.at, 0);
	if (t < at) return null;
	const editAt = num(p.editAt, 1e9);
	const edited = t >= editAt && p.editText !== undefined;
	const text = edited ? str(p.editText, '') : str(p.text, '');
	const flash = edited ? clamp01(1 - (t - editAt) / 0.9) : 0;
	const e = ease('out', popIn(t, at, 0.3));
	const fs = 24 * Math.min(s, 1.3);
	return (
		<div style={{display: 'flex', alignItems: 'center', gap: 14, padding: '12px 22px', background: th.pinBg, borderBottom: `2px solid ${th.headerBorder}`, boxShadow: flash ? `inset 0 0 0 ${4 * flash}px ${th.alertBorder}` : undefined, opacity: e, position: 'relative'}}>
			{flash > 0 ? <div style={{position: 'absolute', inset: 0, background: th.alertBorder, opacity: 0.35 * flash}} /> : null}
			<svg width={fs * 1.2} height={fs * 1.2} viewBox="0 0 24 24" style={{flex: 'none'}}>
				<path d="M15 3 l6 6 -2 1 -4 4 1 5 -2 1 -4 -4 -5 5 -1 -1 5 -5 -4 -4 1 -2 5 1 4 -4z" fill={th.pinLabel} />
			</svg>
			<div style={{minWidth: 0, flex: 1, position: 'relative'}}>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: fs * 0.8, color: th.pinLabel, letterSpacing: '0.04em'}}>
					{str(p.label, 'PINNED')}{str(p.from, '') ? ` · ${str(p.from, '')}` : ''}{edited ? ' · edited' : ''}
				</div>
				<div style={{fontFamily: FONT, fontWeight: 800, fontSize: fs, lineHeight: 1.25, color: th.pinText, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden'}}>{text}</div>
			</div>
		</div>
	);
};

const Bubble: React.FC<{m: Msg; members: Record<string, Member>; t: number; accent: string; th?: Theme; s?: number}> = ({m, members, t, accent, th = THEMES.dark, s = 1}) => {
	const p = popIn(t, num(m.at, 0), 0.3);
	const e = ease('backOut', p);
	const me = Boolean(m.me);
	const from = str(m.from, 'Unknown');
	const card = m.kind === 'card'; // solid red warning card (reads as a red block in a thumbnail)
	const red = m.kind === 'alert' || card;
	const d = dims(s);
	return (
		<div
			style={{
				display: 'flex',
				flexDirection: me ? 'row-reverse' : 'row',
				alignItems: 'flex-start',
				gap: 14,
				padding: '0 22px',
				marginTop: 18,
				opacity: clamp01(p * 2.5),
				transform: `scale(${0.55 + 0.45 * e})`,
				transformOrigin: me ? '100% 100%' : '0% 100%',
			}}
		>
			{me ? null : <Avatar name={from} members={members} size={d.avatar} />}
			<div style={{display: 'flex', flexDirection: 'column', alignItems: me ? 'flex-end' : 'flex-start', maxWidth: d.max}}>
				{me ? null : (
					<div style={{fontFamily: FONT, fontWeight: 800, fontSize: d.name, color: colorFor(from, members), filter: `brightness(${th.nameBright})`, margin: '2px 0 6px 6px'}}>{from}</div>
				)}
				<div
					style={{
						fontFamily: FONT,
						fontWeight: card ? 900 : 700,
						fontSize: d.fs,
						lineHeight: 1.3,
						color: me ? th.meText : card ? '#ffffff' : red ? th.alertText : th.text,
						background: me ? accent : card ? th.alertBorder : red ? th.alertBg : th.bubble,
						border: red ? `${Math.round(2 * s)}px solid ${th.alertBorder}` : undefined,
						boxShadow: th === THEMES.light && !me ? '0 2px 0 rgba(0,0,0,0.08)' : undefined,
						padding: '16px 22px',
						borderRadius: 28,
						borderTopLeftRadius: me ? 28 : 8,
						borderTopRightRadius: me ? 8 : 28,
						whiteSpace: 'pre-wrap',
						wordBreak: 'break-word',
					}}
				>
					{str(m.text, '')}
				</div>
			</div>
		</div>
	);
};

const ChatScreen: React.FC<{c: Record<string, unknown>; t: number}> = ({c, t}) => {
	const members = obj(c.members) as Record<string, Member>;
	const th = themeOf(c);
	const sc = num(c.scale, 1);
	const d = dims(sc);
	const msgs = arr<Msg>(c.messages).filter((m) => num(m.at, 0) <= t);
	const typing = arr<Typing>(c.typing).filter((y) => t >= num(y.at, 0) && t < num(y.until, num(y.at, 0) + 1.2));
	const accent = str(c.accent, '#3d5a80');
	const last = msgs[msgs.length - 1];
	// shove the list up smoothly as the newest bubble arrives
	const shove = last ? (1 - ease('out', popIn(t, num(last.at, 0), 0.25))) * estimateHeight(last, sc) : 0;
	const unread = Math.round(num(c.unread, 0) + msgs.filter((m) => !m.me && m.kind !== 'system' && num(m.at, 0) > num(c.unreadFrom, 1e9)).length);
	const typingName = typing.length ? str(typing[0].from, '') : '';
	const subtitle = typingName ? `${typingName} is typing…` : str(c.subtitle, `${num(c.count, 48)} members`);
	const title = str(c.title, 'Building 7 Residents');
	const groupNames = Object.keys(members).slice(0, 3);
	const pinned = c.pinned ? obj(c.pinned) : null;
	return (
		<div style={{position: 'absolute', inset: 0, background: th.bg, display: 'flex', flexDirection: 'column'}}>
			<div style={{background: th.header, borderBottom: `2px solid ${th.headerBorder}`, position: 'relative', zIndex: 2}}>
				<StatusBar clock={str(c.clock, '2:14')} battery={num(c.battery, 23)} light={th.status} />
				<div style={{height: 104, display: 'flex', alignItems: 'center', padding: '0 20px', gap: 14}}>
					<svg width={26} height={40} viewBox="0 0 26 40">
						<path d="M20 4 L6 20 L20 36" stroke={th.back} strokeWidth={5} fill="none" strokeLinecap="round" strokeLinejoin="round" />
					</svg>
					{unread > 0 ? (
						<div style={{minWidth: 42, height: 42, borderRadius: 21, background: '#e0313a', color: '#fff', fontFamily: FONT, fontWeight: 900, fontSize: 22, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 10px'}}>
							{unread > 99 ? '99+' : unread}
						</div>
					) : null}
					<div style={{position: 'relative', width: 70, height: 64, flex: 'none'}}>
						{(groupNames.length ? groupNames : ['A', 'B']).slice(0, 2).map((n, i) => (
							<div key={n} style={{position: 'absolute', left: i * 22, top: i * 12, border: `3px solid ${th.header}`, borderRadius: '50%'}}>
								<Avatar name={n} members={members} size={44} />
							</div>
						))}
					</div>
					<div style={{display: 'flex', flexDirection: 'column', minWidth: 0}}>
						<div style={{fontFamily: FONT, fontWeight: 800, fontSize: 28, color: th.title, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 360}}>{title}</div>
						<div style={{fontFamily: FONT, fontWeight: 700, fontSize: 20, color: typingName ? '#2e9d5c' : th.sub, marginTop: 4}}>{subtitle}</div>
					</div>
				</div>
				{pinned ? <PinnedBar p={pinned} t={t} th={th} s={sc} /> : null}
			</div>
			<div style={{flex: 1, position: 'relative', overflow: 'hidden'}}>
				<div style={{position: 'absolute', left: 0, right: 0, bottom: 16, display: 'flex', flexDirection: 'column', transform: `translateY(${shove}px)`}}>
					{str(c.dayLabel, '') ? (
						<div style={{alignSelf: 'center', fontFamily: FONT, fontWeight: 700, fontSize: 19 * Math.min(sc, 1.3), color: th.dayText, background: th.dayBg, padding: '6px 16px', borderRadius: 14, marginBottom: 6}}>{str(c.dayLabel, '')}</div>
					) : null}
					{msgs.map((m, i) =>
						m.kind === 'system' ? <SystemLine key={i} m={m} t={t} th={th} s={sc} /> : <Bubble key={i} m={m} members={members} t={t} accent={accent} th={th} s={sc} />,
					)}
					{typing.map((y, i) => (
						<div key={`ty${i}`} style={{display: 'flex', gap: 14, padding: '0 22px', marginTop: 18, alignItems: 'flex-end'}}>
							<Avatar name={str(y.from, '?')} members={members} size={d.avatar} />
							<TypingDots t={t} th={th} />
						</div>
					))}
				</div>
			</div>
			<div style={{height: 108, background: th.header, borderTop: `2px solid ${th.headerBorder}`, display: 'flex', alignItems: 'center', gap: 16, padding: '0 22px 14px'}}>
				<div style={{width: 46, height: 46, borderRadius: 23, border: `3px solid ${th.icon}`, color: th.icon, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 30}}>+</div>
				<div style={{flex: 1, height: 58, borderRadius: 29, background: th.inputBg, fontFamily: FONT, fontWeight: 700, fontSize: 24, color: th.inputText, display: 'flex', alignItems: 'center', padding: '0 24px'}}>
					{str(c.draft, 'Message')}
				</div>
				<svg width={40} height={40} viewBox="0 0 40 40">
					<rect x={13} y={4} width={14} height={22} rx={7} fill={th.icon} />
					<path d="M8 20 a12 12 0 0 0 24 0 M20 32 v6" stroke={th.icon} strokeWidth={3.5} fill="none" strokeLinecap="round" />
				</svg>
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- lock screen

const NotifCard: React.FC<{n: Banner; t: number; floating?: boolean}> = ({n, t, floating}) => {
	const p = popIn(t, num(n.at, 0), 0.32);
	const e = ease('backOut', p);
	return (
		<div
			style={{
				margin: floating ? 0 : '0 22px 14px',
				padding: '18px 20px',
				borderRadius: 30,
				background: floating ? 'rgba(38,43,53,0.97)' : 'rgba(40,46,58,0.78)',
				boxShadow: floating ? '0 18px 40px rgba(0,0,0,0.55)' : undefined,
				display: 'flex',
				gap: 16,
				alignItems: 'flex-start',
				opacity: clamp01(p * 3),
				transform: `translateY(${(1 - e) * -40}px) scale(${0.9 + 0.1 * e})`,
			}}
		>
			<div style={{width: 54, height: 54, borderRadius: 14, background: '#3d5a80', flex: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
				<svg width={34} height={30} viewBox="0 0 34 30">
					<path d="M4 4 h26 a3 3 0 0 1 3 3 v13 a3 3 0 0 1 -3 3 h-15 l-7 6 v-6 h-4 a3 3 0 0 1 -3 -3 v-13 a3 3 0 0 1 3 -3z" fill="#e8eaee" />
				</svg>
			</div>
			<div style={{flex: 1, minWidth: 0}}>
				<div style={{display: 'flex', justifyContent: 'space-between', fontFamily: FONT, fontWeight: 700, fontSize: 19, color: '#aab2bf'}}>
					<span>{str(n.app, 'Messages').toUpperCase()}</span>
					<span>now</span>
				</div>
				<div style={{fontFamily: FONT, fontWeight: 800, fontSize: 25, color: '#f1f3f6', marginTop: 4}}>{str(n.title, '')}</div>
				<div style={{fontFamily: FONT, fontWeight: 700, fontSize: 23, lineHeight: 1.3, color: '#d5dae2', marginTop: 2}}>{str(n.text, '')}</div>
			</div>
		</div>
	);
};

const LockScreen: React.FC<{c: Record<string, unknown>; t: number}> = ({c, t}) => {
	const notes = arr<Banner>(c.notifications).filter((n) => num(n.at, 0) <= t);
	return (
		<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, #121826 0%, #1c2233 45%, #2a2236 100%)'}}>
			<svg width={SW} height={SH} style={{position: 'absolute', inset: 0}}>
				<circle cx={SW * 0.72} cy={SH * 0.6} r={70} fill="#2f3850" opacity={0.6} />
				<path d={`M0 ${SH * 0.78} Q ${SW * 0.3} ${SH * 0.7} ${SW * 0.55} ${SH * 0.76} T ${SW} ${SH * 0.72} V ${SH} H 0 Z`} fill="#161a26" />
				<path d={`M0 ${SH * 0.86} Q ${SW * 0.4} ${SH * 0.8} ${SW} ${SH * 0.85} V ${SH} H 0 Z`} fill="#0f121b" />
			</svg>
			<div style={{position: 'relative'}}>
				<StatusBar clock="" battery={num(c.battery, 23)} />
				<div style={{textAlign: 'center', marginTop: 30, fontFamily: FONT, color: '#e9ecf2'}}>
					<svg width={30} height={36} viewBox="0 0 30 36">
						<rect x={3} y={15} width={24} height={19} rx={4} fill="#e9ecf2" />
						<path d="M8 15 v-5 a7 7 0 0 1 14 0 v5" stroke="#e9ecf2" strokeWidth={3.5} fill="none" />
					</svg>
					<div style={{fontWeight: 700, fontSize: 26, marginTop: 6, opacity: 0.85}}>{str(c.date, 'Tuesday, March 3')}</div>
					<div style={{fontWeight: 800, fontSize: 150, lineHeight: 1, letterSpacing: '-0.03em'}}>{str(c.time, '2:14')}</div>
				</div>
				<div style={{marginTop: 50, display: 'flex', flexDirection: 'column-reverse'}}>
					{notes.map((n, i) => (
						<NotifCard key={i} n={n} t={t} />
					))}
				</div>
			</div>
			<div style={{position: 'absolute', bottom: 60, left: 50, right: 50, display: 'flex', justifyContent: 'space-between'}}>
				{[0, 1].map((i) => (
					<div key={i} style={{width: 76, height: 76, borderRadius: 38, background: 'rgba(255,255,255,0.12)'}} />
				))}
			</div>
			<div style={{position: 'absolute', bottom: 22, left: SW / 2 - 90, width: 180, height: 8, borderRadius: 4, background: 'rgba(255,255,255,0.7)'}} />
		</div>
	);
};

// ---------------------------------------------------------------- call screen

const Handset: React.FC<{rot: number}> = ({rot}) => (
	<svg width={56} height={56} viewBox="0 0 56 56" style={{transform: `rotate(${rot}deg)`}}>
		<path
			d="M14 8 c4 -2 8 0 9 4 l3 8 c1 3 0 5 -2 7 l-3 2 c2 6 7 11 13 13 l2 -3 c2 -2 4 -3 7 -2 l8 3 c4 1 6 5 4 9 c-2 5 -7 8 -12 7 C 26 52 4 30 3 18 c-1 -5 3 -9 11 -10z"
			fill="#fff"
		/>
	</svg>
);

const CallScreen: React.FC<{c: Record<string, unknown>; t: number}> = ({c, t}) => {
	const name = str(c.name, 'Unknown');
	const members = obj(c.members) as Record<string, Member>;
	const at = num(c.at, 0);
	const connectedAt = num(c.connectedAt, 1e9);
	const connected = t >= connectedAt;
	const ring = (t - at) * 1.2;
	const secs = Math.max(0, Math.floor(t - connectedAt));
	const label = connected ? `${String(Math.floor(secs / 60)).padStart(2, '0')}:${String(secs % 60).padStart(2, '0')}` : str(c.label, 'incoming call…');
	const shakeBtn = connected ? 0 : Math.sin(t * 30) * (((t - at) % 1.2) < 0.4 ? 6 : 0);
	return (
		<div style={{position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at 50% 30%, #2b2433 0%, #15131b 70%)', fontFamily: FONT, color: '#eef0f3'}}>
			<StatusBar clock={str(c.clock, '2:16')} battery={num(c.battery, 21)} />
			<div style={{textAlign: 'center', marginTop: 40}}>
				<div style={{fontWeight: 700, fontSize: 26, color: '#aab0bb'}}>{str(c.sub, 'mobile')}</div>
				<div style={{fontWeight: 800, fontSize: 52, marginTop: 12, padding: '0 30px'}}>{name}</div>
				<div style={{fontWeight: 700, fontSize: 26, color: connected ? '#7fd1a0' : '#aab0bb', marginTop: 10}}>{label}</div>
			</div>
			<div style={{position: 'absolute', left: SW / 2 - 110, top: 400, width: 220, height: 220}}>
				{connected
					? null
					: [0, 1, 2].map((i) => {
							const ph = (ring + i / 3) % 1;
							return (
								<div
									key={i}
									style={{
										position: 'absolute',
										inset: 0,
										borderRadius: '50%',
										border: '4px solid rgba(220,200,255,0.5)',
										transform: `scale(${1 + ph * 0.9})`,
										opacity: 1 - ph,
									}}
								/>
							);
						})}
				<Avatar name={name} members={members} size={220} />
			</div>
			<div style={{position: 'absolute', bottom: 120, left: 0, right: 0, display: 'flex', justifyContent: connected ? 'center' : 'space-around'}}>
				<div style={{textAlign: 'center'}}>
					<div style={{width: 120, height: 120, borderRadius: 60, background: '#d23a3f', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
						<Handset rot={135} />
					</div>
					<div style={{fontWeight: 700, fontSize: 22, marginTop: 12, color: '#c9ced6'}}>{connected ? 'End' : 'Decline'}</div>
				</div>
				{connected ? null : (
					<div style={{textAlign: 'center', transform: `translateX(${shakeBtn}px)`}}>
						<div style={{width: 120, height: 120, borderRadius: 60, background: '#3aa865', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
							<Handset rot={0} />
						</div>
						<div style={{fontWeight: 700, fontSize: 22, marginTop: 12, color: '#c9ced6'}}>Accept</div>
					</div>
				)}
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- device

/**
 * The phone at native 600x1240 px.
 * p: mode ('chat'|'lock'|'call'|'off') or screens [{t, mode}], chat {...}, lock {...}, call {...},
 *    banners [{at, duration, app, title, text}], vibrate [{at, duration}], dim (0..1), glitch
 */
export const PhoneDevice: React.FC<{p: Record<string, unknown>; t: number}> = ({p, t}) => {
	const screens = arr<{t?: number; mode?: string}>(p.screens);
	const mode = screens.length ? str(atTime(screens, t).item?.mode, 'chat') : str(p.mode, 'chat');
	const chat = {members: p.members, ...obj(p.chat)};
	const lock = obj(p.lock);
	const call = {members: p.members, ...obj(p.call)};
	const vib = cueLevel(p.vibrate, t, 0.6, 0.03);
	const rot = vib > 0 ? Math.sin(t * 90) * 1.6 * vib : 0;
	const dx = vib > 0 ? Math.sin(t * 110) * 5 * vib : 0;
	const banners = arr<Banner>(p.banners);
	const dim = num(p.dim, 0);
	let screen: React.ReactNode;
	switch (mode) {
		case 'lock':
			screen = <LockScreen c={lock} t={t} />;
			break;
		case 'call':
			screen = <CallScreen c={call} t={t} />;
			break;
		case 'off':
			screen = <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(160deg, #15171c, #08090b)'}} />;
			break;
		default:
			screen = <ChatScreen c={chat} t={t} />;
	}
	return (
		<div style={{width: PHONE_W, height: PHONE_H, position: 'relative', transform: `translateX(${dx}px) rotate(${rot}deg)`}}>
			<div
				style={{
					position: 'absolute',
					inset: 0,
					borderRadius: 86,
					background: 'linear-gradient(135deg, #3a3e47, #0d0e12 30%, #0d0e12 70%, #2b2e35)',
					boxShadow: '0 30px 60px rgba(0,0,0,0.55), inset 0 0 0 3px #4a4f5a',
				}}
			/>
			<div style={{position: 'absolute', left: BEZEL, top: BEZEL, width: SW, height: SH, borderRadius: 72, overflow: 'hidden', background: '#000'}}>
				<GlitchWrap amount={glitchAt(p, t)} t={t} seed="phone">
					<div style={{position: 'absolute', inset: 0}}>{screen}</div>
				</GlitchWrap>
				{/* dynamic-island style camera pill */}
				<div style={{position: 'absolute', left: SW / 2 - 70, top: 14, width: 140, height: 38, borderRadius: 19, background: '#000'}} />
				{banners.map((b, i) => {
					const at = num(b.at, 0);
					const d = num(b.duration, 2.2);
					if (t < at || t > at + d + 0.3) return null;
					const inE = ease('backOut', clamp01((t - at) / 0.35));
					const outE = ease('in', clamp01((t - (at + d)) / 0.3));
					const y = -220 + 280 * inE - 280 * outE;
					return (
						<div key={i} style={{position: 'absolute', left: 14, right: 14, top: y}}>
							<NotifCard n={{...b, at}} t={t} floating />
						</div>
					);
				})}
				{dim > 0 ? <div style={{position: 'absolute', inset: 0, background: '#000', opacity: dim}} /> : null}
				{/* glass sheen */}
				<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0) 35%)'}} />
			</div>
		</div>
	);
};

/** horror/Phone: the device scaled to fit its layer box (no hand). Same props as PhoneDevice. */
export const Phone: React.FC<KitComponentProps> = ({props, time, width, height}) => {
	const s = Math.min(width / PHONE_W, height / PHONE_H);
	return (
		<div style={{width, height, position: 'relative'}}>
			<div style={{position: 'absolute', left: (width - PHONE_W * s) / 2, top: (height - PHONE_H * s) / 2, transform: `scale(${s})`, transformOrigin: '0 0'}}>
				<PhoneDevice p={props} t={time} />
			</div>
		</div>
	);
};
