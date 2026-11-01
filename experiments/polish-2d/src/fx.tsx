/**
 * Scene FX planes for the polish pass. Each is a plain kit component, placed by storyboard layers
 * (see polish.ts), so the kit's own camera/parallax (layer.depth) moves them.
 *
 * NOTE on blending: every storyboard layer sits in its own transformed plane div (SceneView), and a
 * transform makes a stacking context, which isolates mix-blend-mode. A layer's `blend` therefore
 * composites against transparency, i.e. it behaves like normal alpha. These FX are designed for normal
 * alpha (light colours at low alpha read as additive light), which is also the cheapest path.
 */
import React from 'react';
import {random} from 'remotion';
import type {KitComponent} from '../../../studio/src/core/registry';
import {FigureSVG, getFigure, makeCtx} from '../../../studio/src/kits/explainer/creature';

const n = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const s = (v: unknown, d: string) => (typeof v === 'string' ? v : d);

/**
 * polish/Light: surface glow + soft god rays in one SVG [POLISH_IDEAS 1d]. Rays lean with the light
 * direction, breathe on independent phases, and are faded to 0 above the caption band (`fadeAt`, frac of H).
 * props: rays, strength, color, angle (deg the light travels, 90 = down), fadeAt, seed
 */
export const Light: KitComponent = ({props, time, width: W, height: H}) => {
	const nR = n(props.rays, 5);
	const k = n(props.strength, 1);
	const col = s(props.color, '#dff8ff');
	const fadeAt = n(props.fadeAt, 0.6) * H;
	const ang = (n(props.angle, 80) * Math.PI) / 180;
	const lean = Math.cos(ang) / Math.sin(ang); // dx per dy
	const seed = n(props.seed, 3);
	const id = `lt${seed}`;
	const rays: React.ReactNode[] = [];
	for (let i = 0; i < nR; i++) {
		const r = (q: string) => random(`${id}-${i}-${q}`);
		const x0 = W * (-0.15 + (1.1 * (i + 0.2 + r('x') * 0.6)) / nR);
		const w0 = 60 + r('w') * 120;
		const w1 = w0 * (2.2 + r('s') * 1.6);
		const sway = Math.sin(time * (0.18 + r('f') * 0.12) + i * 1.9) * 26;
		const x1 = x0 + lean * fadeAt + sway;
		const a = (0.5 + 0.5 * Math.sin(time * (0.35 + r('g') * 0.3) + i * 1.7)) * k;
		rays.push(
			<polygon
				key={i}
				points={`${x0 - w0 / 2},${-20} ${x0 + w0 / 2},${-20} ${x1 + w1 / 2},${fadeAt} ${x1 - w1 / 2},${fadeAt}`}
				fill={`url(#${id}-ray)`}
				opacity={a}
			/>,
		);
	}
	return (
		<svg width={W} height={H} style={{display: 'block'}}>
			<defs>
				<linearGradient id={`${id}-ray`} gradientUnits="userSpaceOnUse" x1={0} y1={0} x2={0} y2={fadeAt}>
					<stop offset={0} stopColor={col} stopOpacity={0.16} />
					<stop offset={0.55} stopColor={col} stopOpacity={0.06} />
					<stop offset={1} stopColor={col} stopOpacity={0} />
				</linearGradient>
				<radialGradient id={`${id}-glow`} cx={0.42} cy={0} r={0.7}>
					<stop offset={0} stopColor={col} stopOpacity={0.2 * k} />
					<stop offset={1} stopColor={col} stopOpacity={0} />
				</radialGradient>
			</defs>
			<rect x={0} y={0} width={W} height={H * 0.55} fill={`url(#${id}-glow)`} />
			{rays}
		</svg>
	);
};

/**
 * polish/FarPod: a few distant silhouettes of a kit figure in the water colour (atmospheric fade,
 * POLISH_IDEAS 2c): smaller, hazier, slower than the subject. Put it on a far plane (depth ~0.35)
 * with a whole-layer CSS blur (2b).
 * props: species, color, items [{x, y, w (px), flip, speed (px/s), t0}]
 */
export const FarPod: KitComponent = ({props, time, width: W, height: H}) => {
	const f = getFigure(s(props.species, 'orca'));
	if (!f) return null;
	const color = s(props.color, '#0f3a48');
	const items = (Array.isArray(props.items) ? props.items : []) as {x: number; y: number; w: number; flip?: boolean; speed?: number; t0?: number}[];
	const [, , bw, bh] = f.box;
	return (
		<svg width={W} height={H} style={{display: 'block', overflow: 'visible'}}>
			{items.map((it, i) => {
				const w = it.w;
				const h = (w * bh) / bw;
				const dir = it.flip ? -1 : 1;
				const x = it.x * W + dir * (it.speed ?? 14) * time - w / 2;
				const y = it.y * H - h / 2;
				const ctx = {...makeCtx({speed: 0.8, timeOffset: it.t0 ?? i * 0.7}, time, `pod${i}`), sil: color};
				return (
					<g key={i} transform={it.flip ? `translate(${2 * x + w} 0) scale(-1 1)` : undefined}>
						<FigureSVG f={f} ctx={ctx} x={x} y={y} w={w} h={h} align="xMidYMid" />
					</g>
				);
			})}
		</svg>
	);
};

/** polish/Haze: depth haze sheet, transparent at the top to the deep-water colour at the bottom. props: color, top, bottom (alpha) */
export const Haze: KitComponent = ({props}) => {
	const c = s(props.color, '3,16,24');
	return (
		<div
			style={{
				width: '100%',
				height: '100%',
				background: `linear-gradient(180deg, rgba(${c},${n(props.top, 0)}) 0%, rgba(${c},${n(props.mid, 0.12)}) 55%, rgba(${c},${n(props.bottom, 0.42)}) 100%)`,
			}}
		/>
	);
};

/**
 * polish/Bokeh: large out-of-focus specks for a foreground plane (depth ~1.5), radial-gradient fills
 * only (POLISH_IDEAS 6a: never a CSS blur per speck). Kept out of the caption band.
 * props: count, color, seed, band [from, to] (fractions of H to keep clear)
 */
export const Bokeh: KitComponent = ({props, time, width: W, height: H}) => {
	const count = n(props.count, 12);
	const seed = n(props.seed, 7);
	const col = s(props.color, '#d9f5ff');
	const band = (Array.isArray(props.band) ? props.band : [0.6, 0.84]) as [number, number];
	const dots: React.ReactNode[] = [];
	for (let i = 0; i < count; i++) {
		const r = (q: string) => random(`bk${seed}-${i}-${q}`);
		const rad = 22 + r('r') * 70;
		let yf = r('y');
		// remap into the free zones (above and below the caption band)
		const free = 1 - (band[1] - band[0]);
		yf = yf * free;
		if (yf > band[0]) yf += band[1] - band[0];
		// specks stay in the outer 22% on each side: over the subject they read as smudges on it
		const side = r('side') < 0.5 ? 0 : 1;
		const xf = side === 0 ? r('x') * 0.22 : 0.78 + r('x') * 0.22;
		const x = xf * W + Math.sin(time * (0.2 + r('v') * 0.2) + r('q') * 6.28) * 18;
		const y = yf * H - time * (6 + r('w') * 10) + Math.sin(time * (0.3 + r('w') * 0.4) + r('p') * 6.28) * 14;
		const a = 0.16 + 0.24 * r('a');
		dots.push(<circle key={i} cx={x} cy={y} r={rad} fill={`url(#bk${seed}-g)`} opacity={a} />);
	}
	return (
		<svg width={W} height={H} style={{display: 'block', overflow: 'visible'}}>
			<defs>
				<radialGradient id={`bk${seed}-g`}>
					<stop offset={0} stopColor={col} stopOpacity={0.5} />
					<stop offset={0.62} stopColor={col} stopOpacity={0.32} />
					<stop offset={0.8} stopColor={col} stopOpacity={0.12} />
					<stop offset={1} stopColor={col} stopOpacity={0} />
				</radialGradient>
			</defs>
			{dots}
		</svg>
	);
};

/** polish/Halo: soft light scatter behind a subject (1b, gradient version). props: color (r,g,b), alpha, pulse (Hz, 0 = steady) */
export const Halo: KitComponent = ({props, time}) => {
	const c = s(props.color, '160,225,245');
	const pulse = n(props.pulse, 0);
	const a = n(props.alpha, 0.22) * (pulse > 0 ? 0.85 + 0.15 * Math.sin(time * Math.PI * 2 * pulse) : 1);
	return (
		<div
			style={{
				width: '100%',
				height: '100%',
				background: `radial-gradient(closest-side, rgba(${c},${a}) 0%, rgba(${c},${a * 0.45}) 45%, rgba(${c},0) 100%)`,
			}}
		/>
	);
};
