/**
 * House ocean background (STYLE_BIBLE §2.5 colour script, §5.4 rays and caustics, §8 micro layer). The default look of
 * explainer/Ocean; `look: "legacy"` draws the previous flat-teal kit background.
 *
 *   key       field ramp: "tide" (sunlit shallows), "mid" (open water), "deep" (ink, night), "kelp", "dusk", "sky",
 *             "warm" (a lantern-lit proof/scale beat), "danger" (coral sinking to ink: threat beats), "royal" (open ocean: royal
 *             blue), "polar" (clear
 *             cold sea: blue under the surface sinking to indigo). Default from depth: < 30 m tide, < 200 m mid, else deep.
 *   shiftTo   the colour shift (mandatory at the scale/turn beat): the field blends to this key in OKLab over
 *   shiftAt   `shiftDur` s (default 0.8) starting at `shiftAt` (scene s). Consecutive scenes should also change key.
 *   depth     m (number or track): darkens the field toward ink and fades the rays, as before.
 *   rays      count (default 7), rayStrength; rays sway ±3° on 6-12 s periods, aim away from the scene key and fade
 *             out by `fadeAt` (0.62 of the height) so they never cross the caption band.
 *   caustics  light net under the surface (default on when shallow or `surface`)
 *   specks    marine snow count (default 170; the legacy `snow` prop is ignored here)
 *   surface   true or 0..1 y: sky + waterline;  sky (SKIES key, e.g. "polar-dusk") or skyTop / skyBottom, vignette
 *             (0.5, toward ink-0, never black), glow
 *   topColor / midColor / bottomColor   explicit overrides of the first / middle / last stops
 * Everything is gradients and flat shapes, normal alpha (one SVG): no filters, no blend layers.
 */
import React, {useId} from 'react';
import type {KitComponent} from '../../../core/registry';
import {c, mixOk, rgba} from './color';
import {useLight} from './light';
import {Bokeh, Caustics, Rays, Specks} from './atmosphere';
import {ease, prog} from './motion';
import {num, str, track} from '../util';
import {FLAT} from './style';
import {rand} from './rng';

export const KEYS: Record<string, string[]> = {
	tide: ['tide-4', 'tide-3', 'tide-2', 'tide-1', 'tide-0', 'ink-4'],
	mid: ['tide-2', 'tide-1', 'tide-0', 'ink-4', 'ink-3', 'ink-2'],
	deep: ['ink-4', 'ink-3', 'ink-2', 'ink-1', 'ink-0', 'ink-0'],
	kelp: ['kelp-4', 'kelp-3', 'kelp-2', 'kelp-1', 'kelp-0', 'ink-1'],
	dusk: ['dusk-4', 'dusk-3', 'dusk-2', 'dusk-1', 'dusk-0', 'ink-0'],
	sky: ['sky-4', 'sky-3', 'sky-2', 'tide-3', 'tide-1', 'tide-0'],
	// proof / scale beat: a lantern-warm sunlit top that still reads as water lower down (a value + temperature lift)
	warm: ['amber-5', '#e8b45a', 'tide-3', 'tide-1', 'tide-0', 'ink-4'],
};
KEYS.ink = KEYS.deep;
// open ocean (art direction experiments/asset-gen/gen/orca_set_01/04/05: flat bold royal blue, owner's pick): cyan under
// the surface sinking to deep navy
KEYS.royal = FLAT ? ['sky-1', 'tide-1', 'tide-0', 'dusk-1', 'ink-2', 'ink-1'] : ['#38b6f4', '#1f78e6', '#1652d4', '#1240b4', '#0c2c8a', '#071a5c'];
// polar sea (settings biome polar_ice; art direction experiments/asset-gen/gen/f_antarctic_v3.png): clear cold water,
// bright blue under the surface sinking to deep indigo, no seabed, no warm stops
KEYS.polar = FLAT
	? ['dusk-3', 'dusk-2', 'dusk-1', 'ink-2', 'ink-1', 'ink-0'] // style A (f_antarctic_A): deep indigo water, no seabed
	: [mixOk('sky-1', 'dusk-4', 0.4), 'dusk-4', mixOk('dusk-3', 'dusk-2', 0.4), 'dusk-2', 'dusk-1', 'dusk-0'];
// danger re-key (shark / kill beats, colour script carries meaning): coral water sinking to ink; every stop is a
// coral -> dusk/ink mix, so it stays inside the palette (P1)
KEYS.danger = [mixOk('coral-3', 'dusk-2', 0.5), mixOk('coral-2', 'dusk-1', 0.55), mixOk('coral-1', 'dusk-1', 0.62), mixOk('coral-0', 'ink-1', 0.62), mixOk('coral-0', 'ink-0', 0.8), 'ink-0'];
const OFFS = [0, 0.12, 0.32, 0.55, 0.8, 1];
// sky by place + light (house.py names it from the scene's setting: `sky` = "<temperate|polar>-<day|overcast|dusk|night>");
// explicit skyTop / skyBottom props still win. Polar dusk: art direction experiments/asset-gen/gen/f_antarctic_v3.png
export const SKIES: Record<string, string[]> = FLAT
	? {
			// style A: flat sky bands (top -> horizon), e.g. orca_set_05_calf_A dusk = violet, magenta, orange
			'temperate-day': ['sky-1', 'sky-2', 'sky-3'],
			'temperate-overcast': ['sky-3', 'sky-4', 'bone-1'],
			'temperate-dusk': ['violet-1', 'magenta-2', 'amber-1'],
			'temperate-night': ['ink-0', 'ink-1', 'ink-2'],
			'polar-day': ['sky-1', 'sky-3', 'sky-4'],
			'polar-overcast': ['sky-3', 'sky-4', 'bone-1'],
			'polar-dusk': ['ink-1', 'violet-0', 'violet-1'],
			'polar-night': ['ink-0', 'ink-1', 'ink-2'],
		}
	: {
	'temperate-day': ['sky-2', 'sky-4'],
	'temperate-overcast': ['#b9cdd8', '#dfe8ec'],
	'temperate-dusk': ['dusk-2', 'coral-4'],
	'temperate-night': ['dusk-0', 'dusk-1'],
	'polar-day': ['sky-1', 'sky-4'],
	'polar-overcast': ['#9fb4c6', '#d4e0e8'],
	'polar-dusk': ['#160c5c', '#3a3cb0'],
	'polar-night': ['dusk-0', 'dusk-2'],
		};

/** light level 0..1 at a depth (m); same curve as the legacy ocean */
const lightAt = (depth: number, falloff: number) => Math.exp(-Math.max(0, depth) / falloff);

export const autoKey = (depth: number) => (depth < 30 ? 'tide' : depth < 200 ? 'mid' : 'deep');

export const HouseOcean: KitComponent = ({props, time, width: W, height: H}) => {
	const id = 'o' + useId().replace(/[^a-zA-Z0-9_-]/g, '');
	const L = useLight();
	const depth = track(props.depth, time, 40);
	const lit = lightAt(depth, num(props.falloff, 260)) * num(props.brightness, 1);
	const key = str(props.key, autoKey(depth));
	const base = KEYS[key] ?? KEYS.tide;
	const to = typeof props.shiftTo === 'string' ? KEYS[props.shiftTo] : undefined;
	const sh = to ? ease.drift(prog(time, num(props.shiftAt, 0), num(props.shiftDur, 0.8))) : 0;
	const dark = (1 - lit) * (key === 'deep' || key === 'ink' ? 0.4 : 0.75);
	const stops = base.map((tok, i) => {
		let col = to && sh > 0 ? mixOk(tok, to[i], sh) : c(tok);
		if (i === 0 && typeof props.topColor === 'string') col = props.topColor;
		if (i === 2 && typeof props.midColor === 'string') col = props.midColor;
		if (i === 5 && typeof props.bottomColor === 'string') col = props.bottomColor;
		return mixOk(col, 'ink-0', dark);
	});

	const surface = props.surface === true ? 0.28 : typeof props.surface === 'number' ? props.surface : null;
	const sy = surface !== null ? surface * H : 0;
	const rayA = Math.pow(lit, 0.7) * num(props.rayStrength, 1);
	const travel = (Math.atan2(-L.key[1], -L.key[0]) * 180) / Math.PI; // light travels away from the key
	const trav = Math.max(40, Math.min(140, travel < 0 ? travel + 180 : travel));
	const sunX = W / 2 + L.key[0] * W * 0.55;
	const fadeY = num(props.fadeAt, 0.62) * H;
	const rayLen = Math.max(200, (fadeY - sy) / Math.max(0.3, Math.sin((trav * Math.PI) / 180)));
	const nRays = Math.round(num(props.rays, 7));
	const shallow = depth < 40 || surface !== null;
	const caustics = props.caustics === undefined ? shallow : props.caustics === true;
	const seed = String(props.seed ?? 1);
	const nSpecks = Math.round(num(props.specks, 170));
	const t = time + 30;

	const waveY = (x: number) => sy + Math.sin(x / 90 + t * 1.2) * 4 + Math.sin(x / 37 - t * 1.7) * 2;
	let wave = '';
	if (surface !== null) {
		const pts: string[] = [];
		for (let x = -20; x <= W + 20; x += 20) pts.push(`${x},${waveY(x).toFixed(1)}`);
		wave = pts.join(' ');
	}
	const glowA = Math.pow(lit, 0.8) * num(props.glow, 1);

	if (FLAT) {
		// style A: flat colour bands, a few hard-edged translucent rays, flat ripple pills under the surface, flat sky
		// bands with rounded clouds. No gradients, glow, bokeh or vignette.
		const sky = (typeof props.sky === 'string' && SKIES[props.sky]) || ['sky-1', 'sky-2', 'sky-3'];
		const skyCols = typeof props.skyTop === 'string' ? [props.skyTop, mixOk(props.skyTop, str(props.skyBottom, props.skyTop), 0.5), str(props.skyBottom, props.skyTop)] : sky.map((x) => c(x));
		const bandTop = surface !== null ? sy : 0;
		const span = H - bandTop;
		const nR = Math.min(5, nRays);
		const rays: React.ReactNode[] = [];
		if (nR > 0 && rayA > 0.01) {
			const dx = Math.cos((trav * Math.PI) / 180);
			const dy = Math.sin((trav * Math.PI) / 180);
			for (let i = 0; i < nR; i++) {
				const x0 = sunX + (i - (nR - 1) / 2) * W * 0.17 + 18 * Math.sin(time * 0.25 + i * 1.9);
				const w0 = 40 + 50 * rand(`${seed}rw`, i);
				const w1 = w0 * 2.2;
				const len = rayLen * (0.75 + 0.25 * rand(`${seed}rl`, i));
				const ex = x0 + dx * len;
				const ey = bandTop + dy * len;
				rays.push(<polygon key={i} points={`${x0 - w0 / 2},${bandTop} ${x0 + w0 / 2},${bandTop} ${ex + w1 / 2},${ey} ${ex - w1 / 2},${ey}`} fill={c('bone-2')} opacity={0.075 * Math.min(1, rayA * 1.4)} />);
			}
		}
		const ripples: React.ReactNode[] = [];
		if (shallow) {
			for (let i = 0; i < 14; i++) {
				const w = 60 + 110 * rand(`${seed}pw`, i);
				const x = ((rand(`${seed}px`, i) * (W + 200) + time * 14 * (0.5 + rand(`${seed}pv`, i))) % (W + 200)) - 100;
				const y = bandTop + 14 + 150 * rand(`${seed}py`, i) * rand(`${seed}pq`, i);
				ripples.push(<rect key={i} x={x - w / 2} y={y} width={w} height={11 + 6 * rand(`${seed}ph`, i)} rx={8} fill={c(i % 3 ? 'tide-4' : 'bone-2')} opacity={(0.35 + 0.25 * rand(`${seed}po`, i)) * lit} />);
			}
		}
		const clouds: React.ReactNode[] = [];
		if (surface !== null && props.clouds !== false && (str(props.sky, '').endsWith('-day'))) {
			for (let i = 0; i < 3; i++) {
				const cw = 150 + 110 * rand(`${seed}cw`, i);
				const cx = ((rand(`${seed}cx`, i) * W + time * 6) % (W + cw)) - cw / 2;
				const cy = Math.max(30, sy * (0.25 + 0.4 * rand(`${seed}cy`, i)));
				clouds.push(
					<g key={i}>
						<rect x={cx - cw / 2} y={cy - cw * 0.12} width={cw} height={cw * 0.24} rx={cw * 0.12} fill={c('bone-2')} />
						<circle cx={cx - cw * 0.12} cy={cy - cw * 0.12} r={cw * 0.2} fill={c('bone-2')} />
						<circle cx={cx + cw * 0.14} cy={cy - cw * 0.16} r={cw * 0.25} fill={c('bone-2')} />
						<rect x={cx - cw / 2} y={cy + cw * 0.04} width={cw} height={cw * 0.08} rx={cw * 0.04} fill={c('sky-4')} />
					</g>,
				);
			}
		}
		const bounds = [0, 0.14, 0.32, 0.52, 0.74, 1];
		return (
			<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block'}}>
				{stops.slice(0, 5).map((col, i) => (
					<rect key={i} x={0} y={bandTop + bounds[i] * span - 1} width={W} height={(bounds[i + 1] - bounds[i]) * span + 2} fill={i === 4 ? stops[5] : col} />
				))}
				{rays}
				{ripples}
				{nSpecks > 0 ? <Specks t={time} seed={`${seed}s`} n={Math.round(nSpecks * 0.35)} area={[0, bandTop, W, span]} size={[3, 6]} tints={['tide-4', 'bone-1']} opacity={[0.35, 0.6]} twinkleAmt={0} /> : null}
				{surface !== null ? (
					<g>
						{[0, 1, 2].map((i) => (
							<rect key={i} x={0} y={(sy * i) / 3 - 1} width={W} height={sy / 3 + 2} fill={skyCols[i] ?? skyCols[skyCols.length - 1]} />
						))}
						{clouds}
						<polygon points={`-20,${sy - 2} ${wave.split(' ').reverse().join(' ')} ${W + 20},${sy - 2}`} fill={skyCols[2] ?? skyCols[0]} />
						<rect x={0} y={sy} width={W} height={10} fill={c('tide-4')} opacity={0.75} />
						<polyline points={wave} fill="none" stroke={c('bone-2')} strokeWidth={4} />
					</g>
				) : null}
			</svg>
		);
	}

	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block'}}>
			<defs>
				<linearGradient id={`${id}-bg`} x1="0" y1="0" x2="0" y2="1">
					{stops.map((col, i) => (
						<stop key={i} offset={OFFS[i]} stopColor={col} />
					))}
				</linearGradient>
				<radialGradient id={`${id}-glow`} gradientUnits="userSpaceOnUse" cx={sunX} cy={sy} r={H * 0.62}>
					<stop offset="0" stopColor={rgba(c('tide-5'), 0.42)} />
					<stop offset="0.35" stopColor={rgba(mixOk('tide-5', 'amber-5', 0.25), 0.16)} />
					<stop offset="1" stopColor={rgba(c('tide-5'), 0)} />
				</radialGradient>
				<radialGradient id={`${id}-vig`} cx="0.5" cy="0.48" r="0.75">
					<stop offset="0.55" stopColor={rgba(c('ink-0'), 0)} />
					<stop offset="1" stopColor={rgba(c('ink-0'), num(props.vignette, 0.5))} />
				</radialGradient>
				<linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={c(str(props.skyTop, (SKIES[str(props.sky, '')] ?? ['dusk-1', 'dusk-3'])[0]))} />
					<stop offset="1" stopColor={c(str(props.skyBottom, (SKIES[str(props.sky, '')] ?? ['dusk-1', 'dusk-3'])[1]))} />
				</linearGradient>
			</defs>
			<rect x={0} y={sy} width={W} height={H - sy} fill={`url(#${id}-bg)`} />
			<rect x={0} y={sy} width={W} height={H - sy} fill={`url(#${id}-glow)`} opacity={glowA} />
			{caustics ? <Caustics t={time} seed={`${seed}c`} area={[-40, sy - 20, W + 80, H * 0.24]} cell={84} color="tide-5" alpha={0.14 * lit} width={3.4} /> : null}
			{nRays > 0 && rayA > 0.01 ? (
				<g opacity={rayA}>
					<Rays t={time} seed={`${id}r`} x={sunX} y={sy - 40} n={nRays} angle={trav} spread={46} len={rayLen} alpha={0.12} color="tide-5" />
				</g>
			) : null}
			<Bokeh t={time} seed={`${id}b`} n={8} r={[12, 34]} area={[0, sy, W, H - sy]} />
			{nSpecks > 0 ? <Specks t={time} seed={`${seed}s`} n={nSpecks} area={[0, sy, W, H - sy]} size={[2.5, 6.5]} opacity={[0.25 + 0.3 * lit, 0.55 + 0.3 * lit]} /> : null}
			{surface !== null ? (
				<g>
					<rect x={0} y={0} width={W} height={sy + 2} fill={`url(#${id}-sky)`} />
					<polygon points={`-20,-20 ${W + 20},-20 ${wave.split(' ').reverse().join(' ')}`} fill={`url(#${id}-sky)`} />
					<polyline points={wave} fill="none" stroke={c('tide-5')} strokeOpacity={0.55} strokeWidth={3} />
					<rect x={0} y={sy} width={W} height={18} fill={c('tide-4')} opacity={0.14} />
				</g>
			) : null}
			<rect x={0} y={0} width={W} height={H} fill={`url(#${id}-vig)`} />
		</svg>
	);
};
