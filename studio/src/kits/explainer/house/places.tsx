/**
 * Place rigs for the per-scene settings (pipeline/episodes/settings.py; research/frame-analysis/REFERENCES_ANALYSIS.md
 * §4). house.py picks them from a scene's declared setting; a builder can also place them by hand.
 *
 *   explainer/Board     abstract-fact board (rule 13): a flat field in one house colour, a soft lantern glow from the
 *                       key side, slow dust motes, an optional floor line for scale comparisons. Works as a background
 *                       or a full-frame layer. props field (blue | navy | ink | dusk | kelp | amber | coral | sky),
 *                       floor (0..1 y or false), motes (count), seed, surface (0..1 y of a flat water-surface band at
 *                       the top: a water board), rays (count of soft light shafts from it), lanes (count of swim-lane
 *                       ropes: the speed board). Art direction: experiments/asset-gen/gen/orca_set_01/02/07.
 *   explainer/IceField  polar pack ice along the waterline: tabular icebergs on the horizon (aerial-perspective haze),
 *                       brash ice and small floes bobbing on the surface with their pale submerged parts. Draw it at the
 *                       background's depth and box (depth 0.12, 1.2x overscan) so it stays locked to the waterline.
 *                       props waterline (0..1 of the box, the Ocean `surface` value), seed, bergs, brash, sun (x 0..1 of
 *                       a low sun on the horizon with its glitter path: dusk light; omit for none)
 *   explainer/IceFloe   a hero floe drawn across the waterline: snow top, icy front face with cracks, foam line and a
 *                       pale submerged keel. Tilt it with layer `rotate` keyframes (riders follow in the builder).
 *                       props waterline (0..1 of the layer box, default 0.42), seed, snow
 *   explainer/Coast     a coastline on the horizon: hazed ranges, a headland with a surf line, whitecaps on the near
 *                       water. Same box/depth rule as IceField. props waterline, seed, kind ('cliffs': rocky headland,
 *                       `lighthouse` true adds one | 'hills': low far ranges only | 'rock': one tall limestone rock
 *                       with a white town along the shore, Gibraltar-like), sun (x 0..1: a low sun + glitter path)
 * Everything is flat shapes + gradients in the house palette (no filters).
 */
import React, {useId} from 'react';
import type {KitComponent} from '../../../core/registry';
import {c, mixOk, rgba} from './color';
import {closedSpline, openSpline} from './geom';
import {noise1, rand, rng} from './rng';
import {Specks as SpeckField} from './atmosphere';

const num = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const str = (v: unknown, d: string) => (typeof v === 'string' ? v : d);
const uid = (s: string) => 'p' + s.replace(/[^a-zA-Z0-9_-]/g, '');

// board fields: [top, middle, bottom, glow, mote tints]
const FIELDS: Record<string, [string, string, string, string, string[]]> = {
	blue: ['#2a8ff0', '#1650d2', '#0a2a8c', 'tide-5', ['tide-5', 'sky-4']],
	navy: ['#13328e', '#0b1f66', '#050f3c', 'sky-3', ['sky-4', 'tide-5']],
	ink: [mixOk('ink-3', 'ink-2', 0.5), 'ink-2', 'ink-0', 'tide-4', ['bone-1', 'tide-5']],
	dusk: ['dusk-3', 'dusk-2', 'dusk-0', 'sky-3', ['bone-1', 'sky-4']],
	kelp: [mixOk('kelp-2', 'kelp-1', 0.4), 'kelp-1', 'kelp-0', 'kelp-4', ['bone-1', 'amber-5']],
	amber: [mixOk('amber-2', 'ochre-2', 0.4), mixOk('ochre-1', 'amber-1', 0.5), 'ochre-0', 'amber-5', ['amber-5', 'bone-2']],
	coral: [mixOk('coral-2', 'coral-1', 0.5), mixOk('coral-1', 'coral-0', 0.5), mixOk('coral-0', 'ink-0', 0.55), 'coral-4', ['amber-5', 'coral-4']],
	sky: ['sky-2', 'sky-1', 'dusk-2', 'sky-4', ['bone-2', 'sky-4']],
};

export const Board: KitComponent = ({props: p, time, width: W, height: H}) => {
	const id = uid(useId());
	const f = FIELDS[str(p.field, 'ink')] ?? FIELDS.ink;
	const floor = typeof p.floor === 'number' ? p.floor * H : null;
	const seed = String(p.seed ?? 'board');
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block'}}>
			<defs>
				<linearGradient id={`${id}f`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={c(f[0])} />
					<stop offset="0.5" stopColor={c(f[1])} />
					<stop offset="1" stopColor={c(f[2])} />
				</linearGradient>
				<radialGradient id={`${id}g`} gradientUnits="userSpaceOnUse" cx={W * 0.3} cy={H * 0.24} r={H * 0.62}>
					<stop offset="0" stopColor={rgba(f[3], 0.26)} />
					<stop offset="0.45" stopColor={rgba(f[3], 0.08)} />
					<stop offset="1" stopColor={rgba(f[3], 0)} />
				</radialGradient>
				<radialGradient id={`${id}v`} cx="0.5" cy="0.46" r="0.78">
					<stop offset="0.55" stopColor={rgba('ink-0', 0)} />
					<stop offset="1" stopColor={rgba('ink-0', 0.45)} />
				</radialGradient>
			</defs>
			<rect width={W} height={H} fill={`url(#${id}f)`} />
			<rect width={W} height={H} fill={`url(#${id}g)`} />
			{typeof p.surface === 'number' ? (
				<g>
					{Array.from({length: Math.round(num(p.rays, 0))}, (_, i) => {
						const x = W * (0.12 + (0.76 * (i + 0.5)) / Math.max(1, num(p.rays, 1))) + 30 * Math.sin(time * 0.3 + i * 1.7);
						const w = 50 + 40 * rand(`${seed}r`, i);
						return <path key={i} d={`M ${x - w / 2} ${(p.surface as number) * H} L ${x + w / 2} ${(p.surface as number) * H} L ${x + w * 1.6 + 120} ${H * 0.62} L ${x + w * 0.4 + 120} ${H * 0.62} Z`} fill={rgba('tide-5', 0.07 + 0.04 * Math.sin(time * 0.7 + i))} />;
					})}
					<rect x={0} y={0} width={W} height={(p.surface as number) * H} fill={c('tide-4')} />
					<rect x={0} y={(p.surface as number) * H - 4} width={W} height={8} fill={c('tide-5')} opacity={0.85} />
				</g>
			) : null}
			{Array.from({length: Math.round(num(p.lanes, 0))}, (_, i) => {
				const y = H * (0.4 + (0.32 * (i + 0.5)) / Math.max(1, num(p.lanes, 1)));   // under the speed bars
				return (
					<g key={`l${i}`}>
						<rect x={0} y={y - 9} width={W} height={18} rx={9} fill={rgba('tide-4', 0.55)} />
						{Array.from({length: 14}, (_, k) => (
							<rect key={k} x={((k * 90 - time * 40) % (W + 90)) - 45} y={y - 9} width={44} height={18} rx={6} fill={rgba('tide-5', 0.55)} />
						))}
						<rect x={W * 0.03} y={y - 34} width={12} height={68} rx={6} fill={c('bone-2')} opacity={0.9} />
					</g>
				);
			})}
			{floor !== null ? (
				<g>
					<rect x={0} y={floor} width={W} height={H - floor} fill={rgba(f[2], 0.35)} />
					<line x1={W * 0.06} y1={floor} x2={W * 0.94} y2={floor} stroke={rgba('bone-1', 0.28)} strokeWidth={4} strokeLinecap="round" />
				</g>
			) : null}
			<SpeckField t={time} seed={`${seed}m`} n={Math.round(num(p.motes, 70))} area={[0, 0, W, H]} size={[2.5, 6]} tints={f[4]} drift={[3, -4]} opacity={[0.1, 0.32]} />
			<rect width={W} height={H} fill={`url(#${id}v)`} />
		</svg>
	);
};

/** a tabular berg / floe outline: flat top, steep irregular sides (y = waterline, h above, w wide) */
const tabular = (seed: string, x: number, y: number, w: number, h: number) => {
	const r = rng(seed);
	const top = y - h;
	const pts: [number, number][] = [
		[x - w / 2, y + 2],
		[x - w / 2 + w * (0.04 + r() * 0.05), top + h * (0.25 + r() * 0.2)],
		[x - w / 2 + w * (0.12 + r() * 0.06), top + h * r() * 0.08],
		[x - w * 0.1 + w * r() * 0.2, top - h * r() * 0.06],
		[x + w / 2 - w * (0.12 + r() * 0.06), top + h * r() * 0.1],
		[x + w / 2 - w * (0.03 + r() * 0.04), top + h * (0.3 + r() * 0.2)],
		[x + w / 2, y + 2],
	];
	return `M ${pts.map((q) => `${q[0].toFixed(1)} ${q[1].toFixed(1)}`).join(' L ')} Z`;
};

export const IceField: KitComponent = ({props: p, time: t, width: W, height: H}) => {
	const id = uid(useId());
	const wl = num(p.waterline, 0.36) * H;
	const seed = String(p.seed ?? 'ice');
	const r = rng(`${seed}-bergs`);
	const nB = Math.round(num(p.bergs, 3));
	const nBrash = Math.round(num(p.brash, 12));
	// cyan-white ice (art direction f_antarctic_v3): lit faces near white, shaded faces saturated cyan
	const far = mixOk('tide-5', 'bone-2', 0.35);
	const farSide = mixOk('tide-3', 'sky-2', 0.4);
	const sun = typeof p.sun === 'number' ? p.sun * W : null;
	const bergs = Array.from({length: nB}, (_, i) => {
		const w = W * (0.16 + r() * 0.22);
		const x = W * ((i + 0.5) / nB) + (r() - 0.5) * W * 0.18;
		const h = 22 + r() * 46;
		return {x, w, h, k: `${seed}b${i}`};
	});
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block', overflow: 'visible'}}>
			<defs>
				<linearGradient id={`${id}k`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={rgba('tide-5', 0.32)} />
					<stop offset="1" stopColor={rgba('tide-5', 0)} />
				</linearGradient>
				<radialGradient id={`${id}h`}>
					<stop offset="0.3" stopColor={rgba('amber-5', 0.5)} />
					<stop offset="0.6" stopColor={rgba('dusk-4', 0.25)} />
					<stop offset="1" stopColor={rgba('dusk-4', 0)} />
				</radialGradient>
			</defs>
			{sun !== null ? (
				<g>
					<circle cx={sun} cy={wl - 70} r={150} fill={`url(#${id}h)`} />
					<circle cx={sun} cy={wl - 70} r={52} fill={c('amber-5')} />
					{[0, 1, 2, 3, 4].map((i) => {
						const w = 150 - i * 24 + 10 * Math.sin(t * 1.3 + i);
						return <rect key={i} x={sun - w / 2} y={wl + 8 + i * 13} width={w} height={4} rx={2} fill={c('amber-4')} opacity={0.7 - i * 0.11} />;
					})}
				</g>
			) : null}
			{/* far tabular icebergs on the horizon: lit face + a cyan shaded face */}
			{bergs.map((b) => (
				<g key={b.k}>
					<path d={tabular(b.k, b.x, wl, b.w, b.h)} fill={far} />
					<path d={tabular(b.k, b.x + b.w * 0.18, wl, b.w * 0.64, b.h * 0.72)} fill={farSide} opacity={0.75} />
					<rect x={b.x - b.w * 0.45} y={wl + 3} width={b.w * 0.9} height={b.h * 2.4} fill={`url(#${id}k)`} />
				</g>
			))}
			{/* brash ice and pancake floes on the surface, each with its pale underwater part, bobbing */}
			{Array.from({length: nBrash}, (_, i) => {
				const q = rng(`${seed}-br${i}`);
				const x = W * ((i + q()) / nBrash) + 10 * noise1(`${seed}d${i}`, t * 0.15);
				const w = 26 + q() * 70;
				const h = 5 + q() * 9;
				const bob = 3 * Math.sin(t * (0.9 + q() * 0.6) + i * 1.7);
				const y = wl + bob;
				const tilt = 4 * Math.sin(t * 0.7 + i);
				return (
					<g key={i} transform={`rotate(${tilt.toFixed(2)} ${x.toFixed(1)} ${y.toFixed(1)})`}>
						<ellipse cx={x} cy={y + h * 1.4} rx={w * 0.46} ry={h * 1.9} fill={rgba('tide-5', 0.22)} />
						<path d={closedSpline([[x - w / 2, y + 2], [x - w * 0.3, y - h], [x + w * 0.25, y - h * 0.85], [x + w / 2, y + 2], [x, y + h * 0.5]])} fill={c('bone-2')} />
						<path d={`M ${(x - w * 0.42).toFixed(1)} ${(y + 1).toFixed(1)} L ${(x + w * 0.44).toFixed(1)} ${(y + 1).toFixed(1)}`} stroke={c('sky-3')} strokeWidth={3} opacity={0.7} />
					</g>
				);
			})}
		</svg>
	);
};

export const IceFloe: KitComponent = ({props: p, width: W, height: H}) => {
	const id = uid(useId());
	const seed = String(p.seed ?? 'floe');
	const wl = num(p.waterline, 0.42) * H;
	const r = rng(seed);
	const x0 = W * 0.04;
	const x1 = W * 0.96;
	const topY = wl - H * 0.17;
	const lip = H * 0.06;
	// top surface (seen slightly from above) + the front face down to the waterline
	const topPts: [number, number][] = [];
	for (let i = 0; i <= 10; i++) {
		const x = x0 + ((x1 - x0) * i) / 10;
		topPts.push([x, topY - lip * (0.4 + 0.6 * Math.sin((Math.PI * i) / 10)) + (r() - 0.5) * 6]);
	}
	const top = openSpline(topPts);
	const front = `M ${x0} ${topY} ${topPts.map((q) => `L ${q[0].toFixed(1)} ${(q[1] + lip * 0.9).toFixed(1)}`).join(' ')} L ${x1} ${wl} L ${x0} ${wl} Z`;
	const keel = closedSpline([[x0 + W * 0.02, wl], [x0 + W * 0.1, wl + H * 0.32], [W * 0.5, wl + H * 0.46], [x1 - W * 0.12, wl + H * 0.3], [x1 - W * 0.02, wl]]);
	const cracks = Array.from({length: 4}, (_, i) => {
		const cx = x0 + (x1 - x0) * (0.15 + 0.22 * i + r() * 0.08);
		return `M ${cx.toFixed(1)} ${(topY + lip).toFixed(1)} L ${(cx + (r() - 0.5) * 20).toFixed(1)} ${(topY + lip + (wl - topY - lip) * (0.4 + r() * 0.5)).toFixed(1)}`;
	});
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block', overflow: 'visible'}}>
			<defs>
				<linearGradient id={`${id}f`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={mixOk('tide-5', 'sky-4', 0.4)} />
					<stop offset="1" stopColor={mixOk('tide-3', 'sky-2', 0.35)} />
				</linearGradient>
				<linearGradient id={`${id}k`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={rgba('tide-5', 0.55)} />
					<stop offset="1" stopColor={rgba('tide-4', 0.08)} />
				</linearGradient>
			</defs>
			<path d={keel} fill={`url(#${id}k)`} />
			<path d={front} fill={`url(#${id}f)`} />
			{cracks.map((d, i) => (
				<path key={i} d={d} stroke={c('sky-2')} strokeWidth={3} opacity={0.55} fill="none" strokeLinecap="round" />
			))}
			<path d={`${top} L ${x1} ${(topY + lip * 0.9).toFixed(1)} ${topPts.slice().reverse().map((q) => `L ${q[0].toFixed(1)} ${(q[1] + lip * 0.9).toFixed(1)}`).join(' ')} Z`} fill={str(p.snow, mixOk('bone-2', 'tide-5', 0.5))} />
			<path d={top} stroke={c('bone-2')} strokeWidth={4} fill="none" />
			<path d={`M ${x0} ${wl} L ${x1} ${wl}`} stroke={c('bone-2')} strokeWidth={5} strokeLinecap="round" opacity={0.8} />
		</svg>
	);
};

export const Coast: KitComponent = ({props: p, time: t, width: W, height: H}) => {
	const wl = num(p.waterline, 0.3) * H;
	const seed = String(p.seed ?? 'coast');
	const cliffs = str(p.kind, 'cliffs') === 'cliffs';
	const lighthouse = p.lighthouse === true;
	const range = (s: string, x0: number, x1: number, h: number, rough: number) => {
		const pts: [number, number][] = [];
		for (let i = 0; i <= 14; i++) {
			const x = x0 + ((x1 - x0) * i) / 14;
			const env = Math.sin((Math.PI * i) / 14);
			pts.push([x, wl - h * env * (0.55 + rough * Math.abs(noise1(s, i * 0.6)))]);
		}
		return `${openSpline(pts)} L ${x1} ${wl + 2} L ${x0} ${wl + 2} Z`;
	};
	const far = mixOk('sky-3', 'dusk-3', 0.25);
	const mid = mixOk('kelp-1', 'dusk-2', 0.55);
	const head = mixOk('ochre-1', 'kelp-0', 0.45);
	const kind = str(p.kind, 'cliffs');
	const sun = typeof p.sun === 'number' ? p.sun * W : null;
	const hx = cliffs ? W * 0.08 : W * 0.02;
	const hw = W * 0.34;
	const hh = H * 0.05;
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block', overflow: 'visible'}}>
			<defs>
				<radialGradient id={`${seed.replace(/[^a-zA-Z0-9]/g, '')}sh`}>
					<stop offset="0.3" stopColor={rgba('amber-5', 0.55)} />
					<stop offset="0.65" stopColor={rgba('coral-4', 0.2)} />
					<stop offset="1" stopColor={rgba('coral-4', 0)} />
				</radialGradient>
			</defs>
			{sun !== null ? (
				<g>
					<circle cx={sun} cy={wl - 10} r={170} fill={`url(#${seed.replace(/[^a-zA-Z0-9]/g, '')}sh)`} />
					<circle cx={sun} cy={wl - 10} r={58} fill={c('amber-4')} />
				</g>
			) : null}
			<path d={range(`${seed}f`, W * 0.25, W * 1.1, H * 0.035, 0.6)} fill={far} />
			{kind === 'rock' ? (
				<g>
					{/* one tall limestone rock on the right, a white town strip along the shore under it */}
					<path d={`M ${W * 0.62} ${wl + 2} C ${W * 0.66} ${wl - H * 0.03} ${W * 0.7} ${wl - H * 0.075} ${W * 0.76} ${wl - H * 0.09} C ${W * 0.79} ${wl - H * 0.095} ${W * 0.81} ${wl - H * 0.06} ${W * 0.86} ${wl - H * 0.035} C ${W * 0.9} ${wl - H * 0.02} ${W * 0.95} ${wl - H * 0.01} ${W * 0.99} ${wl + 2} Z`} fill={mixOk('ochre-2', 'sky-2', 0.45)} />
					<path d={`M ${W * 0.76} ${wl - H * 0.09} C ${W * 0.79} ${wl - H * 0.095} ${W * 0.81} ${wl - H * 0.06} ${W * 0.86} ${wl - H * 0.035} L ${W * 0.84} ${wl + 2} L ${W * 0.74} ${wl + 2} Z`} fill={mixOk('ochre-1', 'sky-1', 0.5)} />
					{Array.from({length: 26}, (_, i) => {
						const x = W * (0.04 + 0.6 * rand(`${seed}t`, i));
						const h = 8 + 14 * rand(`${seed}th`, i);
						const tone = ['bone-2', 'ochre-4', 'amber-5', 'coral-4'][i % 4];
						return <rect key={i} x={x} y={wl - h} width={14 + 10 * rand(`${seed}tw`, i)} height={h + 2} fill={c(tone)} opacity={0.9} />;
					})}
				</g>
			) : (
				<path d={range(`${seed}m`, -W * 0.05, W * 0.62, H * 0.03, 0.5)} fill={mid} />
			)}
			{cliffs ? (
				<g>
					<path d={`M ${hx - 40} ${wl + 2} L ${hx - 40} ${wl - hh * 0.7} C ${hx + hw * 0.2} ${wl - hh * 1.05} ${hx + hw * 0.6} ${wl - hh} ${hx + hw * 0.82} ${wl - hh * 0.82} L ${hx + hw * 0.9} ${wl - hh * 0.2} L ${hx + hw} ${wl + 2} Z`} fill={head} />
					<path d={`M ${hx + hw * 0.82} ${wl - hh * 0.82} L ${hx + hw * 0.9} ${wl - hh * 0.2} L ${hx + hw} ${wl + 2} L ${hx + hw * 0.86} ${wl + 2} Z`} fill={mixOk(head, 'ink-1', 0.35)} />
					<path d={`M ${hx - 40} ${wl - hh * 0.7} C ${hx + hw * 0.2} ${wl - hh * 1.05} ${hx + hw * 0.6} ${wl - hh} ${hx + hw * 0.82} ${wl - hh * 0.82}`} stroke={mixOk('kelp-2', 'ochre-2', 0.5)} strokeWidth={6} fill="none" />
					{lighthouse ? (
						<g>
							<rect x={hx + hw * 0.3} y={wl - hh * 1.0 - 46} width={14} height={46} fill={c('bone-2')} />
							<rect x={hx + hw * 0.3} y={wl - hh * 1.0 - 34} width={14} height={8} fill={c('signal-1')} />
							<rect x={hx + hw * 0.3 - 3} y={wl - hh * 1.0 - 54} width={20} height={9} fill={c('ink-2')} />
						</g>
					) : null}
				</g>
			) : null}
			{/* surf line at the coast foot and whitecaps on the open water */}
			<path d={`M ${hx - 40} ${wl} L ${hx + hw + 30} ${wl}`} stroke={c('bone-2')} strokeWidth={4} opacity={0.75} />
			{Array.from({length: 9}, (_, i) => {
				const x = ((rand(`${seed}w`, i) * W + t * 6 * (0.5 + rand(`${seed}v`, i))) % (W + 80)) - 40;
				const y = wl + 14 + rand(`${seed}y`, i) * H * 0.012;
				const a = 0.3 + 0.35 * Math.max(0, Math.sin(t * 1.1 + i * 2.1));
				return <path key={i} d={`M ${x.toFixed(1)} ${y.toFixed(1)} q 9 -4 18 0`} stroke={c('bone-2')} strokeWidth={3} opacity={a} fill="none" />;
			})}
		</svg>
	);
};
