/**
 * Screen-space type for Shorts (bible §11), in house style:
 *   TitlePlate  Anton, tight tracking, on an ink-0 plate (85 %) with a soft plane-gap shadow; enters by a
 *               mask wipe (travel), exits with the exit token. Never wide-tracked thin caps.
 *   Counter     Anton big number that ticks continuously (never jumps), unit in Montserrat 700 tide-4.
 *   Captions    Montserrat 900, bone-2 with an ink-0 stroke, whole phrases, emphasis words in amber.
 *   UnlitPass   the lit/unlit pass (bible §5.2) as one ink layer with a soft elliptical hole: everything
 *               behind it outside the hole becomes mix(fill, ink-1, a).
 */
import React from 'react';
import '@fontsource/montserrat/900.css';
import {AbsoluteFill} from 'remotion';
import {c, rgba} from './color';
import {DISPLAY, FONT} from './type';
import {clamp, ease, popIn, prog, springAt, SETTLE} from '../motion/motion';

export type Span = {text: string; color?: string};

/** 0..1 visibility: wipe in over `dur` from `at`, wipe out over 60 % of it from `out` */
const vis = (t: number, at: number, out: number | undefined, dur: number) => {
	const i = ease.travel(prog(t, at, dur));
	const o = out === undefined ? 0 : ease.exit(prog(t, out, dur * 0.6));
	return {i, o};
};

export const TitlePlate: React.FC<{
	t: number;
	at: number;
	out?: number;
	lines: Span[][];
	size: number;
	y: number;
	sub?: Span;
	subSize?: number;
	pulse?: {at: number; index: [number, number]};
}> = ({t, at, out, lines, size, y, sub, subSize = 40, pulse}) => {
	if (t < at - 0.001) return null;
	const {i, o} = vis(t, at, out, 0.45);
	if (o >= 1) return null;
	const padX = size * 0.42;
	const padY = size * 0.26;
	const lh = size * 1.06;
	const h = lines.length * lh + padY * 2 + (sub ? subSize * 1.5 : 0);
	// wipe: left->right reveal of the plate and text; exit: wipe off upward + fade
	const clipR = 100 - 100 * i;
	const ty = -40 * o;
	const pScale = pulse ? 1 + 0.3 * Math.sin(Math.PI * clamp((t - pulse.at) / 0.35)) : 1;
	const ring = pulse ? clamp((t - pulse.at) / 0.6) : 0;
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div
				style={{
					position: 'absolute',
					left: 0,
					right: 0,
					top: y,
					display: 'flex',
					justifyContent: 'center',
					transform: `translateY(${ty}px)`,
					opacity: 1 - o,
				}}
			>
				<div
					style={{
						position: 'relative',
						padding: `${padY}px ${padX}px`,
						background: rgba(c('ink-0'), 0.86),
						borderRadius: 18,
						boxShadow: `0 8px 22px ${rgba(c('ink-0'), 0.38)}`,
						clipPath: i >= 1 ? undefined : `inset(-40px ${clipR}% -40px -40px round 18px)`,
						minHeight: h - padY * 2,
						textAlign: 'center',
					}}
				>
					{lines.map((ln, li) => (
						<div key={li} style={{fontFamily: DISPLAY, fontSize: size, lineHeight: `${lh}px`, letterSpacing: '-0.01em', whiteSpace: 'nowrap', color: c('bone-2')}}>
							{ln.map((s, si) => {
								const isP = pulse && pulse.index[0] === li && pulse.index[1] === si;
								return (
									<span key={si} style={{color: s.color ? c(s.color) : undefined, display: 'inline-block', position: 'relative', transform: isP ? `scale(${pScale})` : undefined}}>
										{isP && ring > 0 && ring < 1 ? (
											<span
												style={{
													position: 'absolute',
													left: '50%',
													top: '52%',
													width: size * (0.9 + 1.1 * ease.travel(ring)),
													height: size * (0.9 + 1.1 * ease.travel(ring)),
													transform: 'translate(-50%, -50%)',
													borderRadius: '50%',
													border: `${Math.max(1, 6 * (1 - ring))}px solid ${c('signal-1')}`,
													opacity: 1 - ring,
												}}
											/>
										) : null}
										{s.text}
									</span>
								);
							})}
						</div>
					))}
					{sub ? (
						<div style={{fontFamily: FONT, fontWeight: 700, fontSize: subSize, color: c(sub.color ?? 'tide-4'), marginTop: subSize * 0.2, letterSpacing: '0.02em'}}>{sub.text}</div>
					) : null}
				</div>
			</div>
		</AbsoluteFill>
	);
};

/** SVG big number (Anton) that ticks from `from` to `to` over `dur`, unit in Montserrat. Pops in. */
export const Counter: React.FC<{
	t: number;
	at: number;
	dur: number;
	from?: number;
	to: number;
	decimals?: number;
	x: number;
	y: number;
	size: number;
	unit?: string;
	prefix?: string;
	out?: number;
	color?: string;
}> = ({t, at, dur, from = 0, to, decimals = 1, x, y, size, unit, prefix, out, color = 'bone-2'}) => {
	if (t < at) return null;
	const p = ease.outQuad(prog(t, at, dur));
	const v = from + (to - from) * p;
	const done = p >= 1;
	const txt = done ? `${to}` : v.toFixed(decimals);
	const s = popIn(t, at);
	const land = done ? 1 + 0.12 * Math.max(0, Math.sin(Math.PI * clamp((t - at - dur) / 0.25))) : 1;
	const o = out === undefined ? 0 : ease.exit(prog(t, out, 0.3));
	if (o >= 1) return null;
	return (
		<g transform={`translate(${x} ${y}) scale(${(s * land * (1 - 0.4 * o)).toFixed(4)})`} opacity={1 - o}>
			<text
				textAnchor="middle"
				fontFamily={DISPLAY}
				fontSize={size}
				fill={c(color)}
				style={{fontVariantNumeric: 'tabular-nums'}}
			>
				{prefix ? (
					<tspan fontSize={size * 0.6} fill={c('tide-4')} dy={-size * 0.02}>
						{prefix}{' '}
					</tspan>
				) : null}
				<tspan>{txt}</tspan>
				{unit ? (
					<tspan fontFamily={FONT} fontWeight={700} fontSize={size * 0.45} fill={c('tide-4')} dx={size * 0.12}>
						{unit}
					</tspan>
				) : null}
			</text>
		</g>
	);
};

export type Phrase = {text: string; start: number; end: number; emph?: string[]};

export const Captions: React.FC<{t: number; phrases: Phrase[]; y: number; size?: number; width?: number}> = ({t, phrases, y, size = 64, width = 900}) => {
	const cur = phrases.find((p) => t >= p.start && t < p.end);
	if (!cur) return null;
	const s = 0.9 + 0.1 * springAt(t, cur.start, SETTLE);
	const words = cur.text.split(' ');
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top: y, left: (1080 - width) / 2, width, textAlign: 'center', transform: `scale(${s})`, transformOrigin: '50% 50%'}}>
				<span
					style={{
						fontFamily: FONT,
						fontWeight: 900,
						fontSize: size,
						lineHeight: 1.12,
						color: c('bone-2'),
						WebkitTextStroke: `${size * 0.13}px ${c('ink-0')}`,
						paintOrder: 'stroke fill',
						textTransform: 'uppercase',
						letterSpacing: '0.01em',
					}}
				>
					{words.map((w, i) => {
						const clean = w.replace(/[^a-z0-9']/gi, '').toLowerCase();
						const em = cur.emph?.includes(clean);
						return (
							<span key={i} style={{color: em ? c('amber-4') : undefined}}>
								{w}
								{i < words.length - 1 ? ' ' : ''}
							</span>
						);
					})}
				</span>
			</div>
		</AbsoluteFill>
	);
};

/** lit/unlit pass: screen-space ink layer with a soft elliptical hole at (x, y) in screen px */
export const UnlitPass: React.FC<{a: number; x: number; y: number; rx: number; ry: number; soft?: number; color?: string}> = ({a, x, y, rx, ry, soft = 0.45, color = 'ink-1'}) => {
	if (a <= 0.001) return null;
	const m = `radial-gradient(${rx.toFixed(0)}px ${ry.toFixed(0)}px at ${x.toFixed(0)}px ${y.toFixed(0)}px, transparent ${((1 - soft) * 100).toFixed(0)}%, black 100%)`;
	return <AbsoluteFill style={{background: rgba(c(color), a), WebkitMaskImage: m, maskImage: m}} />;
};
