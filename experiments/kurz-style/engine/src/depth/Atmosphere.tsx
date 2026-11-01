/**
 * Atmosphere (STYLE_BIBLE §5, §6, §8): gradient fields, particles, light rays, caustics, emitters and bloom.
 * Glows are radialGradient fills with screen blend, never filters. Rays + caustics + glow share ONE screen
 * layer per scene (<LightLayer>), because each full-frame blended layer costs about +28 % under load.
 */
import React from 'react';
import {c, mixOk, rgba} from '../lib/color';
import {useTint} from '../lib/light';
import {fbm1, noise1, rand} from '../lib/rng';
import {closedSpline} from '../lib/geom';
import {isOff} from '../lib/flags';
import {twinkle} from '../motion/motion';
import {H, OVER, W} from './Planes';

const X0 = -OVER;
const Y0 = -OVER;
const FW = W + 2 * OVER;
const FH = H + 2 * OVER;

// ---------------------------------------------------------------- fields

/** Gradient field: ≥ 3 stops with a hue shift, plus a soft radial lift where the light comes from. */
export const GradientField: React.FC<{id: string; stops: [number, string][]; glow?: {x: number; y: number; r: number; color: string; a: number}}> = ({
	id,
	stops,
	glow,
}) => {
	const tint = useTint();
	return (
		<g>
			<defs>
				<linearGradient id={`${id}-lin`} x1="0" y1="0" x2="0" y2="1">
					{stops.map(([o, col], i) => (
						<stop key={i} offset={o} stopColor={tint(col)} />
					))}
				</linearGradient>
				{glow ? (
					<radialGradient id={`${id}-glow`}>
						<stop offset="0" stopColor={rgba(tint(glow.color), glow.a)} />
						<stop offset="0.45" stopColor={rgba(tint(glow.color), glow.a * 0.35)} />
						<stop offset="1" stopColor={rgba(tint(glow.color), 0)} />
					</radialGradient>
				) : null}
			</defs>
			<rect x={X0} y={Y0} width={FW} height={FH} fill={`url(#${id}-lin)`} />
			{glow ? <circle cx={glow.x} cy={glow.y} r={glow.r} fill={`url(#${id}-glow)`} /> : null}
		</g>
	);
};

/** Water seen from below: a bright undulating surface band with a Snell's-window glow. */
export const SurfaceBand: React.FC<{t: number; y: number; color?: string; seed?: string}> = ({t, y, color = 'tide-4', seed = 'surf'}) => {
	const tint = useTint();
	const pts: string[] = [];
	for (let i = 0; i <= 36; i++) {
		const x = X0 + (FW * i) / 36;
		const yy = y + 10 * Math.sin(x * 0.012 + t * 1.3) + 6 * fbm1(seed, x * 0.004 + t * 0.4);
		pts.push(`${x.toFixed(1)} ${yy.toFixed(1)}`);
	}
	return (
		<g>
			<path d={`M ${X0} ${Y0} L ${pts.join(' L ')} L ${X0 + FW} ${Y0} Z`} fill={tint(color)} opacity={0.55} />
			<path d={`M ${pts.join(' L ')}`} fill="none" stroke={tint('tide-5')} strokeWidth={4} opacity={0.5} strokeLinejoin="round" />
		</g>
	);
};

// ---------------------------------------------------------------- particles

/**
 * Marine snow / dust / motes: bean-shaped specks in 2-3 field tints, drifting with per-particle noise and
 * wrapping inside the area. Deterministic per frame.
 */
export const Specks: React.FC<{
	t: number;
	seed: string;
	n: number;
	area?: [number, number, number, number];
	size?: [number, number];
	tints?: string[];
	drift?: [number, number];
	opacity?: [number, number];
	twinkleAmt?: number;
}> = ({t, seed, n, area = [X0, Y0, FW, FH], size = [3, 8], tints = ['tide-4', 'tide-5', 'bone-1'], drift = [4, -6], opacity = [0.35, 0.8], twinkleAmt = 0.3}) => {
	const tint = useTint();
	const [ax, ay, aw, ah] = area;
	const cols = tints.map((x) => tint(x));
	const out: React.ReactNode[] = [];
	for (let i = 0; i < n; i++) {
		const sp = 0.6 + rand(seed, i * 7) * 0.8;
		let x = ax + rand(seed, i * 7 + 1) * aw + drift[0] * sp * t + 14 * noise1(`${seed}${i}x`, t * 0.3);
		let y = ay + rand(seed, i * 7 + 2) * ah + drift[1] * sp * t + 10 * noise1(`${seed}${i}y`, t * 0.3);
		x = ax + ((((x - ax) % aw) + aw) % aw);
		y = ay + ((((y - ay) % ah) + ah) % ah);
		const s = size[0] + rand(seed, i * 7 + 3) * (size[1] - size[0]);
		const o = (opacity[0] + rand(seed, i * 7 + 4) * (opacity[1] - opacity[0])) * (1 - twinkleAmt + twinkleAmt * twinkle(t, seed, i));
		const rot = rand(seed, i * 7 + 5) * 180 + t * 20 * (rand(seed, i * 7 + 6) - 0.5);
		out.push(<ellipse key={i} cx={x} cy={y} rx={s * 0.5} ry={s * 0.36} transform={`rotate(${rot.toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})`} fill={cols[i % cols.length]} opacity={o} />);
	}
	return <g>{out}</g>;
};

/** Big soft out-of-focus particles for the foreground plane (gradient discs, no blur filters). */
export const Bokeh: React.FC<{t: number; seed: string; n: number; color?: string; r?: [number, number]; area?: [number, number, number, number]}> = ({
	t,
	seed,
	n,
	color = 'tide-5',
	r = [14, 40],
	area = [X0, Y0, FW, FH],
}) => {
	const tint = (x: string) => c(x); // bokeh are light: never hazed toward the plane's ink
	const id = `bokeh-${seed}`;
	const [ax, ay, aw, ah] = area;
	return (
		<g>
			<defs>
				<radialGradient id={id}>
					<stop offset="0" stopColor={rgba(tint(color), 0.5)} />
					<stop offset="0.7" stopColor={rgba(tint(color), 0.32)} />
					<stop offset="1" stopColor={rgba(tint(color), 0)} />
				</radialGradient>
			</defs>
			{Array.from({length: n}, (_, i) => {
				const rr = r[0] + rand(seed, i * 5) * (r[1] - r[0]);
				let y = ay + rand(seed, i * 5 + 1) * ah - (8 + rand(seed, i * 5 + 2) * 10) * t;
				y = ay + ((((y - ay) % ah) + ah) % ah);
				const x = ax + rand(seed, i * 5 + 3) * aw + 18 * noise1(`${seed}b${i}`, t * 0.25);
				return <circle key={i} cx={x} cy={y} r={rr} fill={`url(#${id})`} opacity={0.5 + 0.5 * twinkle(t, seed, i)} />;
			})}
		</g>
	);
};

/** Rising bubbles with a sideways wobble (40-120 px/s), from a source point; each is a ring + highlight. */
export const Bubbles: React.FC<{t: number; seed: string; x: number; y: number; n?: number; rate?: number; rise?: number; size?: [number, number]; top?: number}> = ({
	t,
	seed,
	x,
	y,
	n = 14,
	rate = 3.2,
	rise = 90,
	size = [3, 10],
	top = -200,
}) => {
	const tint = useTint();
	const out: React.ReactNode[] = [];
	for (let i = 0; i < n; i++) {
		const born = i / rate - 2.5 + rand(seed, i) * 0.25;
		const age = t - born;
		if (age < 0) continue;
		const r = size[0] + rand(seed, i + 50) * (size[1] - size[0]);
		const by = y - age * rise * (0.8 + r / 20);
		if (by < top) continue;
		const bx = x + Math.sin(age * 5 + rand(seed, i + 9) * 6) * (3 + age * 4) + age * 6;
		const grow = Math.min(1, age * 6);
		out.push(
			<g key={i} transform={`translate(${bx.toFixed(1)} ${by.toFixed(1)}) scale(${grow.toFixed(3)})`}>
				<circle r={r} fill={rgba(tint('tide-5'), 0.18)} stroke={tint('tide-5')} strokeWidth={Math.max(1.4, r * 0.22)} opacity={0.85} />
				<path d={`M ${-r * 0.55} ${-r * 0.1} A ${r * 0.6} ${r * 0.6} 0 0 1 ${-r * 0.05} ${-r * 0.6}`} stroke={c('bone-2')} strokeWidth={Math.max(1.2, r * 0.2)} strokeLinecap="round" fill="none" />
			</g>,
		);
	}
	return <g>{out}</g>;
};

// ---------------------------------------------------------------- light: rays, caustics, emitters, bloom

/** One screen-blended layer for all scene light (rays, caustics, halos): +28 % only once. */
export const LightLayer: React.FC<{children: React.ReactNode; opacity?: number}> = ({children, opacity = 1}) => (
	<g style={isOff('screen') ? undefined : {mixBlendMode: 'screen'}} opacity={opacity}>
		{children}
	</g>
);

/**
 * God rays from a point (the sun through the surface): soft wedges whose opacity follows independent noise,
 * swaying ±2-4° with 6-12 s periods (bible §5.4).
 */
export const Rays: React.FC<{t: number; seed: string; x: number; y: number; n?: number; len?: number; spread?: number; angle?: number; color?: string; alpha?: number}> = ({
	t,
	seed,
	x,
	y,
	n = 7,
	len = 2200,
	spread = 44,
	angle = 72,
	color = 'tide-5',
	alpha = 0.11,
}) => {
	const tint = useTint();
	const id = `rays-${seed}`;
	return (
		<g>
			<defs>
				<linearGradient id={id} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor={rgba(tint(color), 1)} />
					<stop offset="0.55" stopColor={rgba(tint(color), 0.45)} />
					<stop offset="1" stopColor={rgba(tint(color), 0)} />
				</linearGradient>
			</defs>
			{Array.from({length: n}, (_, i) => {
				const base = angle - spread / 2 + (spread * (i + 0.5)) / n + (rand(seed, i) - 0.5) * 5;
				const a = base + 3 * Math.sin((2 * Math.PI * t) / (6 + rand(seed, i + 10) * 6) + rand(seed, i + 20) * 6);
				const w = 2.2 + rand(seed, i + 30) * 3.5;
				const o = alpha * (0.55 + 0.45 * (0.5 + 0.5 * noise1(`${seed}o${i}`, t * 0.5 + i)));
				return (
					<path
						key={i}
						d={`M 0 0 L ${len} ${-len * Math.tan((w * Math.PI) / 360)} L ${len} ${len * Math.tan((w * Math.PI) / 360)} Z`}
						transform={`translate(${x} ${y}) rotate(${a.toFixed(2)})`}
						fill={`url(#${id})`}
						opacity={o}
					/>
				);
			})}
		</g>
	);
};

/**
 * Caustic net: packed rounded cells on a jittered hex grid. Each cell is a smooth closed spline whose six
 * vertices breathe on noise (period ≥ 4 s); cells sit a few px apart, so their strokes merge into the bright,
 * slowly morphing light net with dark rounded cells inside. Stroke width varies per cell (thick/thin lines).
 */
export const Caustics: React.FC<{t: number; seed: string; area: [number, number, number, number]; cell?: number; color?: string; alpha?: number; width?: number; fadeDown?: boolean}> = ({
	t,
	seed,
	area,
	cell = 90,
	color = 'tide-4',
	alpha = 0.22,
	width = 5,
	fadeDown = true,
}) => {
	const tint = useTint();
	const [ax, ay, aw, ah] = area;
	const dy = cell * 0.866;
	if (isOff('caustics')) return null;
	const cols = Math.ceil(aw / cell) + 2;
	const rows = Math.ceil(ah / dy) + 2;
	const id = `caus-${seed}`;
	const thick: string[] = [];
	const thin: string[] = [];
	for (let j = 0; j < rows; j++) {
		for (let i = 0; i < cols; i++) {
			const k = j * 131 + i;
			const cx = ax + (i - 0.5 + (j % 2) * 0.5) * cell + cell * 0.12 * noise1(`${seed}${k}x`, t * 0.2 + rand(seed, k) * 9);
			const cy = ay + (j - 0.5) * dy + cell * 0.12 * noise1(`${seed}${k}y`, t * 0.19 + rand(seed, k + 1) * 9);
			const pts: [number, number][] = [];
			const sc = 0.78 + rand(seed, k + 3) * 0.34;
			for (let v = 0; v < 6; v++) {
				const a = ((v * 60 + 30 + 14 * noise1(`${seed}${k}a${v}`, t * 0.15)) * Math.PI) / 180;
				const r = cell * 0.47 * sc * (1 + 0.24 * noise1(`${seed}${k}r${v}`, t * 0.22 + v));
				pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.92]);
			}
			(rand(seed, k + 7) > 0.45 ? thick : thin).push(closedSpline(pts, 1.15));
		}
	}
	return (
		<g>
			<defs>
				<linearGradient id={`${id}-fade`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="white" stopOpacity={1} />
					<stop offset="1" stopColor="white" stopOpacity={fadeDown ? 0 : 1} />
				</linearGradient>
				<mask id={`${id}-m`} maskUnits="userSpaceOnUse" x={ax} y={ay} width={aw} height={ah}>
					<rect x={ax} y={ay} width={aw} height={ah} fill={`url(#${id}-fade)`} />
				</mask>
			</defs>
			<g mask={`url(#${id}-m)`} opacity={alpha}>
				<path d={thick.join(' ')} fill="none" stroke={tint(color)} strokeWidth={width} strokeLinejoin="round" />
				<path d={thin.join(' ')} fill="none" stroke={tint(color)} strokeWidth={width * 0.55} strokeLinejoin="round" />
			</g>
		</g>
	);
};

/**
 * Emitter (bible §4.5): hue-shifted body (V stays high), tight halo (half at R+0.08R) + faint tail (to R+0.35R),
 * optional slowly turning rays and 4-point sparkles. Draw it inside a LightLayer for the screen blend.
 */
export const Emitter: React.FC<{
	id: string;
	x: number;
	y: number;
	r: number;
	t: number;
	ramp?: [string, string, string];
	halo?: string;
	haloScale?: number;
	rays?: number;
	sparkles?: number;
	pulseAmt?: number;
}> = ({id, x, y, r, t, ramp = ['amber-5', 'amber-4', 'amber-3'], halo = 'amber-4', haloScale = 1, rays = 0, sparkles = 0, pulseAmt = 1}) => {
	const tint = useTint();
	const H1 = r * (1 + 0.35 * 4 * haloScale);
	const hc = tint(halo);
	return (
		<g>
			<defs>
				<radialGradient id={`${id}-body`} cx="0.42" cy="0.4" r="0.62">
					<stop offset="0" stopColor={tint(ramp[0])} />
					<stop offset="0.6" stopColor={tint(ramp[1])} />
					<stop offset="1" stopColor={tint(ramp[2])} />
				</radialGradient>
				<radialGradient id={`${id}-halo`} gradientUnits="userSpaceOnUse" cx={x} cy={y} r={H1}>
					<stop offset={r / H1} stopColor={rgba(hc, 0.85)} />
					<stop offset={(r * 1.08) / H1} stopColor={rgba(hc, 0.42)} />
					<stop offset={(r * 1.6) / H1} stopColor={rgba(mixOk(hc, tint('coral-3'), 0.4), 0.14)} />
					<stop offset="1" stopColor={rgba(tint('ink-2'), 0)} />
				</radialGradient>
			</defs>
			<circle cx={x} cy={y} r={H1 * pulseAmt} fill={`url(#${id}-halo)`} />
			{rays
				? Array.from({length: rays}, (_, i) => {
						const a = (i / rays) * 360 + t * 2.5 + rand(id, i) * 8;
						const L = r * (1.3 + rand(id, i + 40) * 0.4);
						const w = r * 0.12;
						return (
							<path
								key={i}
								d={`M 0 ${-w} L ${L} 0 L 0 ${w} Z`}
								transform={`translate(${x} ${y}) rotate(${a.toFixed(2)})`}
								fill={hc}
								opacity={0.08 + 0.06 * rand(id, i + 80)}
							/>
						);
					})
				: null}
			<circle cx={x} cy={y} r={r} fill={`url(#${id}-body)`} />
			<path
				d={`M ${x - r * 0.84} ${y - r * 0.4} A ${r * 0.93} ${r * 0.93} 0 0 1 ${x + r * 0.3} ${y - r * 0.88}`}
				stroke={tint(ramp[0])}
				strokeWidth={Math.max(3, r * 0.08)}
				strokeLinecap="round"
				fill="none"
				opacity={0.8}
			/>
			{sparkles
				? Array.from({length: sparkles}, (_, i) => {
						const a = rand(id, i + 100) * 6.28;
						const d = r * (1.2 + rand(id, i + 120) * 2.2);
						const sx = x + Math.cos(a) * d;
						const sy = y + Math.sin(a) * d;
						const s = (10 + rand(id, i + 140) * 26) * (0.4 + 0.6 * twinkle(t, id, i));
						return (
							<g key={i} transform={`translate(${sx.toFixed(1)} ${sy.toFixed(1)})`} opacity={0.75}>
								<path d={`M ${-s} 0 L 0 -1.4 L ${s} 0 L 0 1.4 Z M 0 ${-s} L 1.4 0 L 0 ${s} L -1.4 0 Z`} fill={c('bone-2')} />
								<circle r={2.4} fill={c('bone-2')} />
							</g>
						);
					})
				: null}
		</g>
	);
};

/** Bloom behind a bright shape: a soft radial gradient in the light colour (put it inside a LightLayer). */
export const Bloom: React.FC<{id: string; x: number; y: number; rx: number; ry?: number; color?: string; a?: number}> = ({id, x, y, rx, ry, color = 'tide-5', a = 0.35}) => {
	const tint = useTint();
	return (
		<g>
			<defs>
				<radialGradient id={id}>
					<stop offset="0" stopColor={rgba(tint(color), a)} />
					<stop offset="0.4" stopColor={rgba(tint(color), a * 0.45)} />
					<stop offset="1" stopColor={rgba(tint(color), 0)} />
				</radialGradient>
			</defs>
			<ellipse cx={x} cy={y} rx={rx} ry={ry ?? rx} fill={`url(#${id})`} />
		</g>
	);
};

/** Vignette toward ink-0 (normal blend, free). */
export const Vignette: React.FC<{a?: number}> = ({a = 0.55}) => (
	<g>
		<defs>
			<radialGradient id="vig" cx="0.5" cy="0.48" r="0.75">
				<stop offset="0.55" stopColor={rgba(c('ink-0'), 0)} />
				<stop offset="1" stopColor={rgba(c('ink-0'), a)} />
			</radialGradient>
		</defs>
		<rect x={X0} y={Y0} width={FW} height={FH} fill="url(#vig)" />
	</g>
);
