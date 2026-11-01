// Horror effects. Overlays are meant as full-frame component layers with depth 0 and a high z:
//   {"type":"component","name":"horror/Flicker","depth":0,"z":50,"props":{...}}
// Screen shake uses the core camera: "camera": {"shake": [{"at": 1.2, "amplitude": 26}]}.
// Every horror component also accepts `glitch: [{at, duration, amount}]` (real RGB split of itself).
import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import type {KitComponentProps} from '../../core/registry';
import {clamp01, cueLevel, ease, jitter, num, P, str, useUid} from './util';

const abs: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: '100%', height: '100%'};

/**
 * Chromatic RGB-split + slice displacement of its children. amount 0 renders children as is.
 */
export const GlitchWrap: React.FC<{amount: number; t: number; seed: string; children: React.ReactNode}> = ({
	amount,
	t,
	seed,
	children,
}) => {
	const uid = useUid('gw');
	if (amount <= 0.001) return <>{children}</>;
	const step = Math.floor(t * 15);
	const r = (k: string) => random(`${seed}-${k}-${step}`);
	const d = amount * (8 + 22 * r('d'));
	const slices = [0, 1, 2, 3].map((i) => ({
		y0: r(`y${i}`) * 92,
		hh: 1.5 + r(`h${i}`) * 9 * amount,
		dx: (r(`x${i}`) - 0.5) * 2 * amount * 70,
		on: r(`o${i}`) < 0.35 + amount * 0.5,
	}));
	return (
		<div style={{position: 'relative', width: '100%', height: '100%'}}>
			<svg width={0} height={0} style={{position: 'absolute'}}>
				<defs>
					<filter id={`${uid}r`} colorInterpolationFilters="sRGB">
						<feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" />
					</filter>
					<filter id={`${uid}c`} colorInterpolationFilters="sRGB">
						<feColorMatrix type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" />
					</filter>
				</defs>
			</svg>
			<div style={abs}>{children}</div>
			<div style={{...abs, transform: `translateX(${d}px)`, filter: `url(#${uid}r)`, mixBlendMode: 'lighten', opacity: 0.85}}>
				{children}
			</div>
			<div style={{...abs, transform: `translateX(${-d}px)`, filter: `url(#${uid}c)`, mixBlendMode: 'lighten', opacity: 0.85}}>
				{children}
			</div>
			{slices
				.filter((s) => s.on)
				.map((s, i) => (
					<div
						key={i}
						style={{
							...abs,
							clipPath: `inset(${s.y0}% 0 ${Math.max(0, 100 - s.y0 - s.hh)}% 0)`,
							transform: `translateX(${s.dx}px)`,
						}}
					>
						{children}
					</div>
				))}
		</div>
	);
};

/** Glitch level from a component's `glitch` prop (cue list) at time t. */
export const glitchAt = (props: Record<string, unknown>, t: number) => cueLevel(props.glitch, t, 0.35, 0.02);

/** Wrap any kit component so it honours props.glitch. */
export function withGlitch(C: React.FC<KitComponentProps>, name: string): React.FC<KitComponentProps> {
	const W: React.FC<KitComponentProps> = (p) => (
		<GlitchWrap amount={glitchAt(p.props, p.time)} t={p.time} seed={name}>
			<C {...p} />
		</GlitchWrap>
	);
	W.displayName = `Glitch(${name})`;
	return W;
}

// ---------------------------------------------------------------- overlays

/**
 * Light flicker: random dips to dark plus optional full blackouts.
 * props: strength (0..1, 0.5), color ('#000'), rate (changes per second, 15), seed,
 *        blackouts [{at, duration}], from, to (active window, scene seconds)
 */
export const Flicker: React.FC<KitComponentProps> = ({props, time}) => {
	const from = num(props.from, -1e9);
	const to = num(props.to, 1e9);
	if (time < from || time > to) return null;
	const s = num(props.strength, 0.5);
	const rate = num(props.rate, 15);
	const seed = str(props.seed, 'flk');
	const step = Math.floor(time * rate);
	const r = random(`${seed}-${step}`);
	// mostly steady, a few deep dips, occasional double-blink
	let o = r > 0.82 ? 0.55 + 0.45 * random(`${seed}-b-${step}`) : r * 0.12;
	o *= s;
	o = Math.max(o, cueLevel(props.blackouts, time, 0.2, 0.01) * 0.97);
	if (o <= 0.001) return null;
	return <AbsoluteFill style={{background: str(props.color, '#000'), opacity: clamp01(o)}} />;
};

/**
 * Vignette, optionally coloured and pulsing.
 * props: amount (0.7), color ('0,0,0' rgb triple or css color), inner (0.35 = clear radius),
 *        pulse (Hz, 0 = steady), pulseAmount (0.3)
 */
export const VignetteFx: React.FC<KitComponentProps> = ({props, time}) => {
	const amount = num(props.amount, 0.7);
	const pulse = num(props.pulse, 0);
	const pa = num(props.pulseAmount, 0.3);
	const a = amount * (pulse > 0 ? 1 - pa / 2 + (pa / 2) * Math.sin(time * Math.PI * 2 * pulse) : 1);
	const c = str(props.color, '0,0,0');
	const inner = num(props.inner, 0.35) * 100;
	const col = /^\d/.test(c) ? `rgba(${c},${a})` : c;
	return (
		<AbsoluteFill
			style={{
				background: `radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) ${inner}%, ${col} 100%)`,
				opacity: /^\d/.test(c) ? 1 : a,
			}}
		/>
	);
};

/** Heartbeat envelope (lub-dub) in 0..1 at time t for a given bpm. */
export function heartbeat(t: number, bpm: number): number {
	const period = 60 / bpm;
	const ph = ((t % period) + period) % period;
	const lub = Math.exp(-ph / 0.07) * (ph >= 0 ? 1 : 0);
	const ph2 = ph - 0.2;
	const dub = ph2 >= 0 ? 0.7 * Math.exp(-ph2 / 0.08) : 0;
	return clamp01(lub + dub);
}

/**
 * Heartbeat pulse: red edges throb lub-dub. Pair with a layer `idle: pulse` or camera zoom.
 * props: bpm (96, or bpmTo to speed up), bpmTo, color ('150,0,10'), intensity (0.85), from, to
 */
export const Heartbeat: React.FC<KitComponentProps> = ({props, time, sceneDuration}) => {
	const from = num(props.from, 0);
	const to = num(props.to, sceneDuration);
	if (time < from || time > to) return null;
	const bpm0 = num(props.bpm, 96);
	const bpm1 = num(props.bpmTo, bpm0);
	const p = clamp01((time - from) / Math.max(0.001, to - from));
	// integrate tempo so speeding up doesn't jump phase
	const avgBpm = bpm0 + (bpm1 - bpm0) * p * 0.5;
	const local = time - from;
	const e = heartbeat(local * (avgBpm / bpm0), bpm0);
	const c = str(props.color, '150,0,10');
	const k = num(props.intensity, 0.85);
	return (
		<AbsoluteFill
			style={{
				background: `radial-gradient(ellipse at 50% 50%, rgba(${c},0) ${42 - e * 10}%, rgba(${c},${0.25 + 0.6 * e * k}) 100%)`,
				boxShadow: `inset 0 0 ${80 + e * 160}px rgba(${c},${0.5 * e * k})`,
			}}
		/>
	);
};

/**
 * Screen glitch overlay: inverted / hue-shifted bands (backdrop-filter), RGB tear lines, blocks.
 * Use with the per-component `glitch` prop for a true RGB split of the art underneath.
 * props: cues [{at, duration, amount}] (or always-on `amount`), seed
 */
export const GlitchOverlay: React.FC<KitComponentProps> = ({props, time, width, height}) => {
	const lvl = props.cues ? cueLevel(props.cues, time, 0.35, 0.02) : num(props.amount, 0);
	if (lvl <= 0.001) return null;
	const seed = str(props.seed, 'gl');
	const step = Math.floor(time * 20);
	const r = (k: string) => random(`${seed}-${k}-${step}`);
	const bands = Array.from({length: 6}, (_, i) => ({
		y: r(`y${i}`) * height,
		h: (6 + r(`h${i}`) * 70) * lvl,
		kind: r(`k${i}`),
		on: r(`o${i}`) < 0.3 + 0.6 * lvl,
	}));
	const lines = Array.from({length: 10}, (_, i) => ({y: r(`l${i}`) * height, c: i % 2 ? 'rgba(0,255,240,0.55)' : 'rgba(255,0,60,0.6)', w: r(`lw${i}`) * width}));
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			{bands
				.filter((b) => b.on)
				.map((b, i) => (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: 0,
							top: b.y,
							width,
							height: b.h,
							backdropFilter:
								b.kind < 0.33 ? 'invert(1) hue-rotate(180deg)' : b.kind < 0.66 ? 'hue-rotate(110deg) saturate(4) brightness(1.4)' : 'grayscale(1) contrast(3)',
							transform: `translateX(${(r(`bx${i}`) - 0.5) * 60 * lvl}px)`,
						}}
					/>
				))}
			<svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
				{lines.map((l, i) => (
					<rect key={i} x={r(`lx${i}`) * width * 0.4} y={l.y} width={l.w} height={2 + 4 * lvl} fill={l.c} opacity={lvl} />
				))}
				{Array.from({length: 8}, (_, i) => (
					<rect
						key={`b${i}`}
						x={r(`qx${i}`) * width}
						y={r(`qy${i}`) * height}
						width={20 + r(`qw${i}`) * 120}
						height={8 + r(`qh${i}`) * 40}
						fill={i % 3 === 0 ? 'rgba(255,255,255,0.8)' : i % 3 === 1 ? 'rgba(255,20,60,0.7)' : 'rgba(10,10,14,0.9)'}
						opacity={r(`qo${i}`) < lvl ? 1 : 0}
					/>
				))}
			</svg>
			{/* scanlines */}
			<AbsoluteFill
				style={{
					opacity: 0.35 * lvl,
					background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.6) 0px, rgba(0,0,0,0.6) 2px, rgba(0,0,0,0) 2px, rgba(0,0,0,0) 6px)',
				}}
			/>
		</AbsoluteFill>
	);
};

/**
 * Red text flash, burned into the picture (not the caption track).
 * props: text, at (0), duration (until scene end), style 'flash' | 'neon' | 'scrawl',
 *        fontSize (130), color (P.red), strobe (Hz of white/red alternation, 0 = off),
 *        cps (typewriter chars/sec, 0 = all at once), shake (px jitter, 6), maxWidth (0.86 of box)
 */
export const RedText: React.FC<KitComponentProps> = ({props, time, width, height, sceneDuration}) => {
	const at = num(props.at, 0);
	const dur = num(props.duration, sceneDuration - at);
	if (time < at || time > at + dur) return null;
	const local = time - at;
	const style = str(props.style, 'flash');
	const fs = num(props.fontSize, 130);
	const color = str(props.color, P.red);
	const cps = num(props.cps, 0);
	let text = str(props.text, 'DON\'T OPEN IT');
	if (cps > 0) text = text.slice(0, Math.max(1, Math.floor(local * cps)));
	const strobe = num(props.strobe, 0);
	const white = strobe > 0 && Math.floor(local * strobe * 2) % 2 === 1 && local < 0.6;
	const shake = num(props.shake, 6);
	const jx = jitter(`rt-x-${text}`, time) * shake;
	const jy = jitter(`rt-y-${text}`, time) * shake;
	const pop = ease('backOut', clamp01(local / 0.18));
	const fade = clamp01((at + dur - time) / 0.12);
	const flashIn = clamp01(1 - local / 0.12);
	const base: React.CSSProperties = {
		fontFamily: '"Anton", "Montserrat", Impact, sans-serif',
		fontSize: fs,
		lineHeight: 1.02,
		textAlign: 'center',
		textTransform: 'uppercase',
		letterSpacing: '0.02em',
		maxWidth: width * num(props.maxWidth, 0.86),
		color: white ? '#fff' : color,
		transform: `translate(${jx}px, ${jy}px) scale(${0.6 + 0.4 * pop}) rotate(${style === 'scrawl' ? -4 : 0}deg)`,
		opacity: fade,
	};
	let body: React.ReactNode;
	if (style === 'neon') {
		body = (
			<div
				style={{
					...base,
					fontFamily: '"Montserrat", sans-serif',
					fontWeight: 900,
					fontSize: fs * 0.62,
					padding: `${fs * 0.22}px ${fs * 0.3}px`,
					background: 'rgba(8,6,12,0.82)',
					border: `${Math.max(4, fs * 0.04)}px solid ${color}`,
					borderRadius: fs * 0.12,
					boxShadow: `0 0 ${fs * 0.3}px ${P.redGlow}, inset 0 0 ${fs * 0.25}px rgba(255,40,50,0.35)`,
					textShadow: `0 0 ${fs * 0.12}px ${P.redGlow}, 0 0 ${fs * 0.3}px ${P.redGlow}`,
					color: white ? '#fff' : '#ff5a62',
				}}
			>
				{text}
			</div>
		);
	} else {
		body = (
			<div
				style={{
					...base,
					WebkitTextStroke: `${Math.max(3, fs * 0.05)}px #120406`,
					paintOrder: 'stroke fill',
					textShadow: `0 0 ${fs * 0.25}px ${P.redGlow}, 0 ${fs * 0.05}px 0 #000`,
				}}
			>
				{text}
			</div>
		);
	}
	return (
		<div style={{width, height, display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative'}}>
			{style === 'flash' && flashIn > 0 ? (
				<div style={{position: 'absolute', inset: 0, background: color, opacity: 0.35 * flashIn}} />
			) : null}
			{body}
		</div>
	);
};

/**
 * Darkness with a light hole (phone glow, torch, lamp). Full-frame overlay.
 * props: x, y (fraction of box, 0.5/0.6), radius (fraction of width, 0.35), darkness (0.85),
 *        color (glow tint, 'rgba(120,170,255,0.18)'), flicker (0..1)
 */
export const Darkness: React.FC<KitComponentProps> = ({props, time, width, height}) => {
	const x = num(props.x, 0.5) * width;
	const y = num(props.y, 0.6) * height;
	const fl = num(props.flicker, 0);
	const rr = num(props.radius, 0.35) * width * (1 + fl * 0.08 * jitter('dk', time, 1 / 12));
	const d = num(props.darkness, 0.85);
	const c = str(props.color, 'rgba(120,170,255,0.18)');
	return (
		<AbsoluteFill>
			<AbsoluteFill
				style={{
					background: `radial-gradient(circle at ${x}px ${y}px, rgba(4,6,10,0) 0px, rgba(4,6,10,${d * 0.5}) ${rr * 0.7}px, rgba(4,6,10,${d}) ${rr * 1.6}px)`,
				}}
			/>
			<AbsoluteFill style={{background: `radial-gradient(circle at ${x}px ${y}px, ${c} 0px, rgba(0,0,0,0) ${rr}px)`, mixBlendMode: 'screen'}} />
		</AbsoluteFill>
	);
};

