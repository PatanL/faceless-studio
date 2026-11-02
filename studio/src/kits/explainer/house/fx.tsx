/**
 * House light and micro-layer components (STYLE_BIBLE §4.5, §5, §8).
 *
 *   explainer/Specks      marine snow / motes: bean specks in 2-3 field tints, drifting (D3 >= 150 specks per frame).
 *                         props n (160), seed, size [min,max] px, tints, drift [x,y] px/s, opacity [min,max]
 *   explainer/Glow        emitter (lantern, lure, bioluminescence): hue-shifted body, tight halo (half at R+0.08R), tail to
 *                         R+0.35R, optional rays + 4-point sparkles, lub-dub pulse. props color ("amber" | "tide" | "coral"),
 *                         r (px, default 0.25 x box), rays, sparkles, pulse (0..1). Glow only on emitters (J7).
 *   explainer/LightEvent  a light beat that reads at phone size (a real value swing, not a 12° sweep). Put it on a
 *                         screen-space layer (depth 0) above the world, below labels (z ~ 12). props:
 *                           kind  "lanternOn": the frame starts as ink and a soft lit disc opens at (x, y) to radius r
 *                                 "spot":      the world dims to ink outside a lit disc that follows (x, y) (lit/unlit pass)
 *                                 "flash":     a warm lantern bloom (0.3-1.5 s) at (x, y)
 *                                 "dim":       a dark beat: the frame sinks toward ink and recovers
 *                           at, dur (s), out (s, when it releases; default end of scene), x, y (0..1 of the box),
 *                           r (px), amount (0..1 ink veil / bloom strength), color (token)
 *                         Bible §5.3: at most one full-frame flash per 30 s; it lands on a narration beat.
 */
import React, {useId} from 'react';
import type {KitComponent} from '../../../core/registry';
import {c, mixOk, rgba} from './color';
import {Emitter, Specks as SpeckField} from './atmosphere';
import {ease, prog, pulse} from './motion';

const num = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const str = (v: unknown, d: string) => (typeof v === 'string' ? v : d);
const pair = (v: unknown, d: [number, number]): [number, number] =>
	Array.isArray(v) && v.length === 2 && typeof v[0] === 'number' && typeof v[1] === 'number' ? [v[0], v[1]] : d;
const uidOf = (id: string) => 'f' + id.replace(/[^a-zA-Z0-9_-]/g, '');

export const Specks: KitComponent = ({props: p, time, width, height}) => (
	<svg width={width} height={height} style={{display: 'block', overflow: 'visible'}}>
		<SpeckField
			t={time}
			seed={String(p.seed ?? 'sn')}
			n={Math.round(num(p.n, 160))}
			area={[0, 0, width, height]}
			size={pair(p.size, [3, 7])}
			tints={Array.isArray(p.tints) ? (p.tints as string[]) : ['tide-4', 'tide-5', 'bone-1']}
			drift={pair(p.drift, [4, -6])}
			opacity={pair(p.opacity, [0.3, 0.75])}
		/>
	</svg>
);

const RAMPS: Record<string, [[string, string, string], string]> = {
	amber: [['amber-5', 'amber-4', 'amber-3'], 'amber-4'],
	tide: [['tide-5', 'tide-4', 'tide-2'], 'tide-4'],
	coral: [['amber-5', 'coral-4', 'coral-3'], 'coral-4'],
	bone: [['bone-2', 'amber-5', 'amber-4'], 'amber-5'],
};

export const Glow: KitComponent = ({props: p, time, width, height}) => {
	const id = uidOf(useId());
	const [ramp, halo] = RAMPS[str(p.color, 'amber')] ?? RAMPS.amber;
	const r = num(p.r, Math.min(width, height) * 0.25);
	const k = 1 + (pulse(time + num(p.phase, 0), num(p.period, 1.4), 0.08) - 1) * num(p.pulse, 1);
	return (
		<svg width={width} height={height} style={{display: 'block', overflow: 'visible'}}>
			<Emitter id={id} x={width / 2} y={height / 2} r={r * k} t={time} ramp={ramp} halo={halo} haloScale={num(p.halo, 1)} rays={Math.round(num(p.rays, 0))} sparkles={Math.round(num(p.sparkles, 0))} />
		</svg>
	);
};

export const LightEvent: KitComponent = ({props: p, time, width: W, height: H, sceneDuration}) => {
	const id = uidOf(useId());
	const kind = str(p.kind, 'lanternOn');
	const at = num(p.at, 0);
	const dur = num(p.dur, kind === 'flash' ? 0.8 : 1.2);
	const out = num(p.out, sceneDuration + 1);
	const x = num(p.x, 0.5) * W;
	const y = num(p.y, 0.45) * H;
	const r = num(p.r, Math.min(W, H) * 0.55);
	const amount = num(p.amount, kind === 'flash' ? 0.55 : 0.72);
	const veil = c(str(p.color, kind === 'flash' ? 'amber-5' : 'ink-1'));
	const rel = 1 - ease.drift(prog(time, out, 0.6));
	if (kind === 'flash') {
		// fast rise (0.12 s), slower fall: a lantern bloom with a warm core and a coral/ink tail
		const u = (time - at) / dur;
		if (u < 0 || u > 1) return null;
		const a = amount * (u < 0.15 ? u / 0.15 : Math.pow(1 - (u - 0.15) / 0.85, 1.6));
		return (
			<svg width={W} height={H} style={{display: 'block'}}>
				<defs>
					<radialGradient id={`${id}-b`} gradientUnits="userSpaceOnUse" cx={x} cy={y} r={Math.max(W, H) * 0.9}>
						<stop offset="0" stopColor={rgba(c('bone-2'), Math.min(1, a * 1.1))} />
						<stop offset="0.12" stopColor={rgba(veil, a)} />
						<stop offset="0.45" stopColor={rgba(mixOk(veil, c('coral-3'), 0.4), a * 0.45)} />
						<stop offset="1" stopColor={rgba(c('coral-1'), a * 0.12)} />
					</radialGradient>
				</defs>
				<rect width={W} height={H} fill={`url(#${id}-b)`} />
			</svg>
		);
	}
	if (kind === 'dim') {
		const u = prog(time, at, dur);
		if (time < at) return null;
		const a = amount * Math.sin(Math.PI * Math.min(1, u)) ** 0.7 * rel;
		return <div style={{position: 'absolute', inset: 0, background: rgba(veil, a)}} />;
	}
	// lanternOn / spot: an ink veil with a soft lit disc (the lit/unlit pass, bible §5.2, done as one screen-space veil)
	const open = kind === 'lanternOn' ? ease.travel(prog(time, at, dur)) : 1;
	const veilA = kind === 'lanternOn' ? amount * rel : amount * ease.drift(prog(time, at, dur)) * rel;
	if (veilA <= 0.002) return null;
	const R = Math.max(1, r * (kind === 'lanternOn' ? 0.15 + 0.85 * open : 1));
	const soft = num(p.soft, 0.45);
	return (
		<svg width={W} height={H} style={{display: 'block'}}>
			<defs>
				<radialGradient id={`${id}-v`} gradientUnits="userSpaceOnUse" cx={x} cy={y} r={R}>
					<stop offset={Math.max(0, 1 - soft)} stopColor={rgba(veil, 0)} />
					<stop offset="1" stopColor={rgba(veil, veilA)} />
				</radialGradient>
				{/* the lit interior is lifted toward the lantern (a cone that reads as light, not just a hole) */}
				<radialGradient id={`${id}-l`} gradientUnits="userSpaceOnUse" cx={x} cy={y} r={R}>
					<stop offset="0" stopColor={rgba(c('amber-5'), 0.1 * open * rel)} />
					<stop offset="1" stopColor={rgba(c('amber-5'), 0)} />
				</radialGradient>
			</defs>
			<rect width={W} height={H} fill={`url(#${id}-v)`} />
			<circle cx={x} cy={y} r={R} fill={`url(#${id}-l)`} />
		</svg>
	);
};
