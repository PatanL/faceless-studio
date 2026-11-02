/**
 * Lane C what-if worlds (house style A): a side-on world drawn in METRES around a growing YOU, so every shot is
 * honest scale (episodes/whatif-grow-1cm). Registered from index.tsx:
 *
 *   explainer/GrowWorld   full-frame world (use as the scene background, overscan ~1.05, depth 0)
 *   explainer/GrowHud     the clock + height plate (a full-frame layer, depth 1)
 *
 * Time model. `clock` is story time in seconds (a track; interpolated in log space so a minute -> an hour reads as a
 * steady count-up). YOU's height is 1.75 m + 1 cm x clock unless `youH` (track, m) overrides it.
 *
 * View. x = metres from YOU's centre line, alt = metres above the ground. Screen: X = cx*W + x*ppm,
 * Y = gy - alt*ppm. ppm comes from `lppm` (track of log10 px-per-metre: linear in log = an exponential zoom) or
 * `fit` (track: YOU's height as a fraction of the frame height). Ground: `gy` (track, fraction of H), or `focusAlt`
 * (track, fraction of YOU's height) + `focusY` (track, fraction of H): that point of YOU stays at that screen y.
 *
 * Props: ground 'room' | 'street' | 'land' (auto: below ~0.047 px/m the ground becomes the curved Earth), pose
 * [{at, pose}] (kit poses stand | wave | panic | point | shrug), face [{at, face}] (calm | smile | worried | strain |
 * gasp | shock | wow), sy (track: vertical squash of YOU, knees giving), puffs [{at}] breath puffs, items [...]:
 *   room {ceiling 2.4, crackAt}        house {x, w, h, color}        block {x, w, floors, color}
 *   tree {x, h}   car {x, color}   lamp {x}   crack {x, at, w}   eiffel {x}   paris {x0, x1, seed}
 *   mountain {x, h, w, seed, far}   cloud {x, alt, w, seed, front, drift}   plane {x, alt, v, at, dir, trail}
 *   karman {}   moon {x, alt}   sun {sx, sy, r} (screen fractions)   skyline {x0, x1, seed}
 * Every shape is one flat colour with one flat shadow shape (docs/HOUSE_STYLE.md); no gradients, blur or outlines.
 */
import React from 'react';
import type {KitComponent} from '../../core/registry';
import type {DrawCtx} from './figure';
import {PEOPLE} from './people';
import {arr, C, clamp, num, obj, str, track} from './util';
import {c} from './house/color';

const R_EARTH = 6371000;
const MOON_D = 3474800;

// ------------------------------------------------------------------ tracks

/** a track interpolated in log10 space (clock seconds: a minute -> an hour counts up evenly) */
const logTrack = (v: unknown, t: number, d: number): number => {
	if (typeof v === 'number') return v;
	const kfs = arr<{t: number; v: number; ease?: string}>(v).filter((k) => typeof k.t === 'number' && typeof k.v === 'number');
	if (!kfs.length) return d;
	const lk = kfs.map((k) => ({...k, v: Math.log10(Math.max(1e-3, k.v))}));
	return Math.pow(10, track(lk, t, Math.log10(Math.max(1e-3, d))));
};

/** the last {at, <key>} entry at or before t */
const sched = (v: unknown, t: number, key: string, d: string): string => {
	let out = d;
	for (const e of arr<Record<string, unknown>>(v)) if (typeof e.at === 'number' && t >= e.at && typeof e[key] === 'string') out = e[key] as string;
	return out;
};

export const clockText = (s: number): string => {
	const plural = (n: number, u: string) => `${n} ${u}${n === 1 ? '' : 'S'}`;
	if (s < 60) return plural(Math.floor(s), 'SECOND');
	if (s < 3600) return plural(Math.floor(s / 60), 'MINUTE');
	if (s < 86400 * 2) return plural(Math.floor(s / 3600), 'HOUR');
	if (s < 86400 * 61) return plural(Math.floor(s / 86400), 'DAY');
	if (s < 86400 * 365) return plural(Math.floor(s / (86400 * 30.44)), 'MONTH');
	return plural(Math.floor(s / (86400 * 365.25)), 'YEAR');
};

export const heightText = (m: number): string => {
	if (m < 10) return `${m.toFixed(2)} M`;
	if (m < 1000) return `${Math.round(m).toLocaleString('en-US')} M`;
	if (m < 100000) return `${(m / 1000).toFixed(1)} KM`;
	return `${Math.round(m / 1000).toLocaleString('en-US')} KM`;
};

type View = {W: number; H: number; ppm: number; gy: number; ox: number; youH: number; t: number};

/** story seconds: log interpolation by default, `clockScale: 'lin'` for linear (the first minute) */
export const clockAt = (p: Record<string, unknown>, t: number) => (p.clockScale === 'lin' ? track(p.clock, t, 0) : logTrack(p.clock, t, 0));

const view = (p: Record<string, unknown>, t: number, W: number, H: number): View => {
	const clock = clockAt(p, t);
	const youH = p.youH !== undefined ? track(p.youH, t, 1.75) : 1.75 + 0.01 * clock;
	const ppm = p.lppm !== undefined ? Math.pow(10, track(p.lppm, t, 2)) : (track(p.fit, t, 0.45) * H) / youH;
	// x: `cx` (screen fraction of YOU's centre line), or `focusXH` (world x as a fraction of YOU's height) held at `focusSX`
	const ox = p.focusXH !== undefined ? track(p.focusSX, t, 0.5) * W - track(p.focusXH, t, 0) * youH * ppm : track(p.cx, t, 0.5) * W;
	let gy = track(p.gy, t, 0.66) * H;
	if (p.focusAlt !== undefined) gy = track(p.focusY, t, 0.45) * H + track(p.focusAlt, t, 0.5) * youH * ppm;
	return {W, H, ppm, gy, ox, youH, t};
};

const X = (v: View, x: number) => v.ox + x * v.ppm;
const Y = (v: View, alt: number) => v.gy - alt * v.ppm;
const f1 = (n: number) => (Math.abs(n) > 1e7 ? (n > 0 ? 1e7 : -1e7) : n).toFixed(1);

/** deterministic 0..1 noise */
const hash = (s: string, i: number) => {
	let h = 2166136261 ^ i;
	for (let k = 0; k < s.length; k++) h = Math.imul(h ^ s.charCodeAt(k), 16777619);
	h = Math.imul(h ^ (h >>> 13), 1274126177);
	return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
};

// ------------------------------------------------------------------ sky + ground

// flat atmosphere bands (alt from, to, colour): far = paler, up = deeper (house style: flat colour bands, no gradients)
const BANDS: [number, number, string][] = [
	[0, 2000, 'sky-2'],
	[2000, 7000, 'sky-1'],
	[7000, 15000, 'sky-0'],
	[15000, 35000, 'tide-0'],
	[35000, 70000, 'dusk-1'],
	[70000, 100000, 'ink-1'],
];

const Stars: React.FC<{v: View; seed: string}> = ({v, seed}) => (
	<g>
		{Array.from({length: 90}, (_, i) => {
			const x = hash(seed, i * 3) * v.W;
			const y = hash(seed, i * 3 + 1) * v.H;
			const r = 1.6 + hash(seed, i * 3 + 2) * 3.2;
			const tw = 0.55 + 0.45 * Math.sin(v.t * (1.5 + (i % 5) * 0.4) + i);
			return <circle key={i} cx={x} cy={y} r={r} fill={c(i % 7 === 0 ? 'amber-5' : 'bone-2')} opacity={tw} />;
		})}
	</g>
);

const sphereMode = (v: View) => R_EARTH * v.ppm < 3e5;

const Sky: React.FC<{v: View; seed: string}> = ({v, seed}) => {
	const sphere = sphereMode(v);
	const topAlt = (v.gy - 0) / v.ppm; // altitude at the top edge (flat)
	const showSpace = sphere || topAlt > 90000;
	if (sphere) {
		const ex = X(v, 0);
		const ey = v.gy + R_EARTH * v.ppm;
		return (
			<g>
				<rect width={v.W} height={v.H} fill={c('ink-0')} />
				<Stars v={v} seed={seed} />
				{[...BANDS].reverse().map(([, a1, col], i) => (
					<circle key={i} cx={ex} cy={ey} r={(R_EARTH + a1) * v.ppm} fill={c(col)} />
				))}
			</g>
		);
	}
	return (
		<g>
			<rect width={v.W} height={v.H} fill={c(showSpace ? 'ink-0' : 'sky-2')} />
			{showSpace ? <Stars v={v} seed={seed} /> : null}
			{BANDS.map(([a0, a1, col], i) => {
				const y0 = Y(v, a1);
				const y1 = Y(v, a0);
				if (y1 < -10 || y0 > v.H + 10) return null;
				return <rect key={i} x={0} y={Math.max(-10, y0)} width={v.W} height={Math.min(v.H + 10, y1) - Math.max(-10, y0)} fill={c(col)} />;
			})}
		</g>
	);
};

/** street-side ground: kerb, pavement, road with dashes, verge, soil; in metres so it collapses to a soil band far out */
const Ground: React.FC<{v: View; kind: string}> = ({v, kind}) => {
	if (sphereMode(v)) {
		const ex = X(v, 0);
		const r = R_EARTH * v.ppm;
		const ey = v.gy + r;
		// continents as a few flat blobs; the cap under YOU is land so the dive from space lands on green
		const blobs: [number, number, number][] = [
			[0, -0.98, 0.34],
			[-0.62, -0.55, 0.26],
			[0.55, -0.35, 0.3],
			[-0.2, 0.2, 0.22],
			[0.35, 0.55, 0.18],
		];
		return (
			<g>
				<circle cx={ex} cy={ey} r={r} fill={c('tide-0')} />
				<clipPath id="growEarth">
					<circle cx={ex} cy={ey} r={r} />
				</clipPath>
				<g clipPath="url(#growEarth)">
					{blobs.map(([bx, by, br], i) => (
						<ellipse key={i} cx={ex + bx * r} cy={ey + by * r} rx={br * r * 1.25} ry={br * r * 0.8} fill={c('kelp-1')} />
					))}
					{[[-0.4, -0.75, 0.3], [0.3, -0.1, 0.36], [-0.5, 0.35, 0.28]].map(([bx, by, w], i) => (
						<rect key={`c${i}`} x={ex + bx * r} y={ey + by * r} width={w * r} height={0.05 * r} rx={0.025 * r} fill={c('bone-2')} opacity={0.9} />
					))}
					{/* one flat shadow shape: the night side, away from the light (upper left) */}
					<circle cx={ex + r * 0.42} cy={ey + r * 0.28} r={r * 1.02} fill={c('ink-1')} opacity={0.42} />
				</g>
			</g>
		);
	}
	const y0 = v.gy;
	if (kind === 'room') {
		return (
			<g>
				<rect x={0} y={y0} width={v.W} height={Math.max(0, v.H - y0)} fill={c('ochre-1')} />
				<rect x={0} y={y0} width={v.W} height={Math.max(2, 0.06 * v.ppm)} fill={c('ochre-0')} />
				{Array.from({length: 14}, (_, i) => {
					const x = X(v, -6 + i * 0.9);
					return <rect key={i} x={x} y={y0 + 0.06 * v.ppm} width={Math.max(1, 0.025 * v.ppm)} height={Math.max(0, v.H - y0)} fill={c('ochre-0')} opacity={0.35} />;
				})}
			</g>
		);
	}
	const m = (a: number) => Math.max(0, a * v.ppm);
	const street = kind !== 'land';
	const bands: [number, number, string][] = street
		? [
				[0, 0.25, 'violet-1'], // kerb face
				[0.25, 2.2, 'bone-0'], // pavement
				[2.2, 2.45, 'violet-2'], // kerb
				[2.45, 10.5, 'violet-0'], // road
				[10.5, 12.5, 'kelp-1'], // verge
			]
		: [[0, 2.0, 'kelp-2']];
	let y = y0;
	const out: React.ReactNode[] = [<rect key="soil" x={0} y={y0} width={v.W} height={Math.max(0, v.H - y0)} fill={c('kelp-0')} />];
	for (const [a, b, col] of bands) {
		const h = m(b - a);
		out.push(<rect key={col + a} x={0} y={y0 + m(a)} width={v.W} height={h} fill={c(col)} />);
		y = y0 + m(b);
	}
	if (street && v.ppm > 1.2) {
		// lane dashes, pavement joints
		const dashY = y0 + m(6.3);
		const step = 9;
		const first = Math.floor(-v.ox / v.ppm / step) - 1;
		const n = Math.min(400, Math.ceil(v.W / v.ppm / step) + 3);
		for (let i = 0; i < n; i++) {
			const x = (first + i) * step;
			out.push(<rect key={`d${i}`} x={X(v, x)} y={dashY} width={4.5 * v.ppm} height={Math.max(2, 0.35 * v.ppm)} fill={c('amber-4')} />);
		}
		if (v.ppm > 6) {
			const js = 1.6;
			const f2 = Math.floor(-v.ox / v.ppm / js) - 1;
			const n2 = Math.min(400, Math.ceil(v.W / v.ppm / js) + 3);
			for (let i = 0; i < n2; i++)
				out.push(<rect key={`j${i}`} x={X(v, (f2 + i) * js)} y={y0 + m(0.25)} width={Math.max(1.5, 0.05 * v.ppm)} height={m(1.95)} fill={c('sky-3')} opacity={0.5} />);
		}
	}
	return <g>{out}</g>;
};

// ------------------------------------------------------------------ props (all in metres)

type Item = Record<string, unknown>;

const shade = (base: string) => {
	// the one flat shadow tone of each base colour (a darker step of the same ramp)
	const m = /^(\w+)-(\d)$/.exec(base);
	if (!m) return base;
	const n = Number(m[2]);
	return n > 0 ? `${m[1]}-${n - 1}` : base;
};

const Room: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const ceil = num(it.ceiling, 2.4);
	const crackAt = num(it.at, num(it.crackAt, 1e9));
	const k = clamp((v.t - crackAt) / 0.35);
	const wall = c('violet-2');
	const wallSh = c('violet-1');
	const R = (x0: number, a0: number, w: number, h: number, fill: string, extra?: Record<string, unknown>) => (
		<rect x={X(v, x0)} y={Y(v, a0 + h)} width={w * v.ppm} height={h * v.ppm} fill={c(fill)} {...extra} />
	);
	const flakes = k > 0
		? Array.from({length: 9}, (_, i) => {
				const dt = v.t - crackAt;
				const x = (hash('flk', i) - 0.5) * 0.9;
				const vx = (hash('flk', i + 20) - 0.5) * 0.6;
				const fall = 4.9 * dt * dt * 0.35;
				const alt = ceil - 0.03 - fall;
				if (alt < 0.02) return null;
				const s = (0.04 + 0.05 * hash('flk', i + 40)) * v.ppm;
				return <rect key={i} x={X(v, x + vx * dt) - s / 2} y={Y(v, alt) - s / 2} width={s} height={s * 0.7} fill={c('bone-1')} transform={`rotate(${(dt * 200 + i * 40) % 360} ${X(v, x + vx * dt)} ${Y(v, alt)})`} />;
			})
		: null;
	return (
		<g>
			{/* wall, a flat shadow band in the corner, skirting */}
			<rect x={0} y={Y(v, ceil)} width={v.W} height={ceil * v.ppm + 2} fill={wall} />
			<rect x={X(v, 2.9)} y={Y(v, ceil)} width={v.W} height={ceil * v.ppm + 2} fill={wallSh} />
			{R(-9, 0, 18, 0.1, 'violet-0')}
			{/* window with sky and a cloud */}
			{R(-2.75, 0.95, 1.35, 1.15, 'bone-1')}
			{R(-2.68, 1.02, 1.21, 1.01, 'sky-2')}
			<circle cx={X(v, -2.2)} cy={Y(v, 1.62)} r={0.13 * v.ppm} fill={c('bone-2')} />
			<circle cx={X(v, -2.02)} cy={Y(v, 1.66)} r={0.17 * v.ppm} fill={c('bone-2')} />
			{R(-2.38, 1.5, 0.55, 0.12, 'bone-2')}
			{R(-2.1, 1.02, 0.07, 1.01, 'bone-1')}
			{R(-2.75, 0.92, 1.35, 0.06, 'bone-0')}
			{/* poster */}
			{R(1.0, 1.25, 0.55, 0.75, 'magenta-1')}
			<circle cx={X(v, 1.275)} cy={Y(v, 1.72)} r={0.14 * v.ppm} fill={c('amber-4')} />
			{R(1.08, 1.33, 0.39, 0.14, 'magenta-3')}
			{/* bed */}
			{R(1.25, 0, 2.3, 0.45, 'ochre-0')}
			{R(1.3, 0.42, 2.2, 0.16, 'bone-1')}
			{R(1.75, 0.55, 1.75, 0.2, 'magenta-2')}
			{R(1.75, 0.55, 1.75, 0.06, 'magenta-1')}
			{R(1.32, 0.56, 0.42, 0.16, 'bone-2')}
			{R(3.45, 0, 0.12, 1.0, 'ochre-0')}
			{/* lamp + side table */}
			{R(-1.25, 0, 0.5, 0.55, 'amber-1')}
			{R(-1.25, 0.5, 0.5, 0.05, 'amber-0')}
			{R(-1.03, 0.55, 0.05, 0.38, 'ink-2')}
			<path d={`M ${f1(X(v, -1.18))} ${f1(Y(v, 0.93))} L ${f1(X(v, -0.82))} ${f1(Y(v, 0.93))} L ${f1(X(v, -0.9))} ${f1(Y(v, 1.18))} L ${f1(X(v, -1.1))} ${f1(Y(v, 1.18))} Z`} fill={c('amber-4')} />
			{/* ceiling slab, the flat above it, a hanging light */}
			<rect x={0} y={0} width={v.W} height={Math.max(0, Y(v, ceil + 0.28))} fill={c('ink-1')} />
			{R(-9, ceil, 18, 0.28, 'bone-0')}
			{R(-9, ceil, 18, 0.05, 'sky-3')}
			{R(-0.62, ceil - 0.3, 0.02, 0.3, 'ink-2')}
			<circle cx={X(v, -0.61)} cy={Y(v, ceil - 0.33)} r={0.06 * v.ppm} fill={c('amber-4')} />
			{/* the crack where the head meets the ceiling */}
			{k > 0 ? (
				<g>
					{Array.from({length: 7}, (_, i) => {
						const a = -0.4 + i * 0.13 + (hash('crk', i) - 0.5) * 0.08;
						const L = (0.25 + 0.4 * hash('crk', i + 9)) * k;
						const pts: string[] = [];
						for (let s = 0; s <= 4; s++) {
							const u = (s / 4) * L;
							const jag = s === 0 ? 0 : (hash('crk', i * 10 + s) - 0.5) * 0.06;
							pts.push(`${f1(X(v, a * 0.15 + (a > 0 ? u : -u) * Math.abs(Math.cos(a * 3)) + jag))} ${f1(Y(v, ceil + 0.02 + (s % 2) * 0.03 + jag * 0.5))}`);
						}
						return <polyline key={i} points={pts.join(' ')} fill="none" stroke={c('ink-1')} strokeWidth={Math.max(2, 0.018 * v.ppm)} strokeLinejoin="round" strokeLinecap="round" />;
					})}
					<path
						d={`M ${f1(X(v, -0.22))} ${f1(Y(v, ceil))} L ${f1(X(v, -0.12))} ${f1(Y(v, ceil + 0.09 * k))} L ${f1(X(v, 0.0))} ${f1(Y(v, ceil + 0.05 * k))} L ${f1(X(v, 0.1))} ${f1(Y(v, ceil + 0.11 * k))} L ${f1(X(v, 0.22))} ${f1(Y(v, ceil))} Z`}
						fill={c('violet-0')}
					/>
					{flakes}
				</g>
			) : null}
		</g>
	);
};

const House: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	const w = num(it.w, 9);
	const h = num(it.h, 5.5);
	const col = str(it.color, 'coral-2');
	const roof = str(it.roof, 'violet-1');
	const L = X(v, x - w / 2);
	const Rr = X(v, x + w / 2);
	return (
		<g>
			<rect x={L} y={Y(v, h)} width={w * v.ppm} height={h * v.ppm} fill={c(col)} />
			<rect x={X(v, x + w * 0.22)} y={Y(v, h)} width={w * 0.28 * v.ppm} height={h * v.ppm} fill={c(shade(col))} />
			<path d={`M ${f1(L - 0.5 * v.ppm)} ${f1(Y(v, h))} L ${f1(X(v, x))} ${f1(Y(v, h + w * 0.42))} L ${f1(Rr + 0.5 * v.ppm)} ${f1(Y(v, h))} Z`} fill={c(roof)} />
			<path d={`M ${f1(X(v, x))} ${f1(Y(v, h + w * 0.42))} L ${f1(Rr + 0.5 * v.ppm)} ${f1(Y(v, h))} L ${f1(X(v, x + w * 0.1))} ${f1(Y(v, h))} Z`} fill={c(shade(roof))} />
			<rect x={X(v, x - w * 0.32)} y={Y(v, h * 0.75)} width={w * 0.2 * v.ppm} height={h * 0.28 * v.ppm} fill={c('sky-3')} />
			<rect x={X(v, x + w * 0.08)} y={Y(v, h * 0.48)} width={w * 0.16 * v.ppm} height={h * 0.48 * v.ppm} fill={c('ink-2')} />
		</g>
	);
};

const Block: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	const w = num(it.w, 18);
	const floors = Math.round(num(it.floors, 10));
	const fh = 3.3;
	const h = floors * fh;
	const col = str(it.color, 'magenta-1');
	const win = str(it.window, 'sky-3');
	const cols = Math.max(2, Math.round(w / 4));
	const wins: React.ReactNode[] = [];
	if (v.ppm * fh > 6)
		for (let f = 0; f < floors; f++)
			for (let k = 0; k < cols; k++) {
				const lit = hash(String(it.seed ?? 'blk'), f * 31 + k) > 0.8;
				wins.push(
					<rect key={`${f}-${k}`} x={X(v, x - w / 2 + (k + 0.25) * (w / cols))} y={Y(v, f * fh + fh * 0.75)} width={(w / cols) * 0.5 * v.ppm} height={fh * 0.42 * v.ppm} fill={c(lit ? 'amber-4' : win)} />,
				);
			}
	return (
		<g>
			<rect x={X(v, x - w / 2)} y={Y(v, h)} width={w * v.ppm} height={h * v.ppm} fill={c(col)} />
			{wins}
			<rect x={X(v, x + w * 0.2)} y={Y(v, h)} width={w * 0.3 * v.ppm} height={h * v.ppm} fill={c(shade(col))} opacity={0.75} />
			<rect x={X(v, x - w / 2 - 0.4)} y={Y(v, h + 0.8)} width={(w + 0.8) * v.ppm} height={0.8 * v.ppm} fill={c(shade(col))} />
		</g>
	);
};

const Tree: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	const h = num(it.h, 8);
	const r = h * 0.3;
	return (
		<g>
			<rect x={X(v, x - h * 0.04)} y={Y(v, h * 0.55)} width={h * 0.08 * v.ppm} height={h * 0.55 * v.ppm} fill={c('ochre-0')} />
			<circle cx={X(v, x)} cy={Y(v, h - r)} r={r * v.ppm} fill={c('kelp-1')} />
			<circle cx={X(v, x + r * 0.3)} cy={Y(v, h - r * 1.05)} r={r * 0.75 * v.ppm} fill={c('kelp-0')} opacity={0.0} />
			<path d={`M ${f1(X(v, x))} ${f1(Y(v, h))} A ${f1(r * v.ppm)} ${f1(r * v.ppm)} 0 0 1 ${f1(X(v, x))} ${f1(Y(v, h - 2 * r))} Z`} fill={c('kelp-0')} />
		</g>
	);
};

const Car: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	const col = str(it.color, 'coral-2');
	const L = 4.5;
	const p = (dx: number, a: number) => `${f1(X(v, x - L / 2 + dx))} ${f1(Y(v, a))}`;
	const wheel = (dx: number) => (
		<g key={dx}>
			<circle cx={X(v, x - L / 2 + dx)} cy={Y(v, 0.33)} r={0.33 * v.ppm} fill={c('ink-0')} />
			<circle cx={X(v, x - L / 2 + dx)} cy={Y(v, 0.33)} r={0.14 * v.ppm} fill={c('bone-0')} />
		</g>
	);
	return (
		<g>
			<path d={`M ${p(0, 0.25)} L ${p(0, 0.85)} L ${p(0.9, 0.95)} L ${p(1.4, 1.45)} L ${p(3.3, 1.45)} L ${p(3.9, 0.95)} L ${p(4.5, 0.85)} L ${p(4.5, 0.25)} Z`} fill={c(col)} />
			<path d={`M ${p(0, 0.25)} L ${p(4.5, 0.25)} L ${p(4.5, 0.55)} L ${p(0, 0.55)} Z`} fill={c(shade(col))} />
			<path d={`M ${p(1.55, 1.0)} L ${p(1.75, 1.33)} L ${p(2.3, 1.33)} L ${p(2.3, 1.0)} Z`} fill={c('sky-3')} />
			<path d={`M ${p(2.45, 1.0)} L ${p(2.45, 1.33)} L ${p(3.15, 1.33)} L ${p(3.6, 1.0)} Z`} fill={c('sky-3')} />
			{wheel(1.0)}
			{wheel(3.6)}
		</g>
	);
};

const Lamp: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	return (
		<g>
			<rect x={X(v, x - 0.08)} y={Y(v, 6)} width={0.16 * v.ppm} height={6 * v.ppm} fill={c('ink-2')} />
			<rect x={X(v, x - 0.08)} y={Y(v, 6)} width={1.1 * v.ppm} height={0.16 * v.ppm} fill={c('ink-2')} />
			<rect x={X(v, x + 0.7)} y={Y(v, 5.9)} width={0.5 * v.ppm} height={0.18 * v.ppm} fill={c('amber-4')} />
		</g>
	);
};

const Crack: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const at = num(it.at, 0);
	const k = clamp((v.t - at) / 0.3);
	if (k <= 0) return null;
	const x = num(it.x, 0);
	const w = num(it.w, 8);
	const pts = (side: number, i: number) => {
		const out: string[] = [];
		for (let s = 0; s <= 5; s++) {
			const u = (s / 5) * (w / 2) * k * (0.6 + 0.4 * hash('rd', i));
			const depth = 0.3 + (hash('rd', i * 7 + s) * 7.5) * (s / 5);
			out.push(`${f1(X(v, x + side * u))} ${f1(Y(v, -Math.min(10, depth * k)))}`);
		}
		return out.join(' ');
	};
	const dt = v.t - at;
	return (
		<g>
			<path d={`M ${f1(X(v, x - w * 0.32 * k))} ${f1(Y(v, -0.1))} L ${f1(X(v, x - w * 0.12 * k))} ${f1(Y(v, -1.4 * k))} L ${f1(X(v, x - w * 0.02))} ${f1(Y(v, -0.5 * k))} L ${f1(X(v, x + w * 0.1 * k))} ${f1(Y(v, -1.9 * k))} L ${f1(X(v, x + w * 0.3 * k))} ${f1(Y(v, -0.1))} Z`} fill={c('ink-0')} />
			{[-1, 1, -1, 1, 1, -1].map((s, i) => (
				<polyline key={i} points={pts(s, i)} fill="none" stroke={c('ink-0')} strokeWidth={Math.max(4, 0.35 * v.ppm)} strokeLinecap="round" strokeLinejoin="round" />
			))}
			{dt < 1.2
				? Array.from({length: 7}, (_, i) => {
						const vx = (hash('chk', i) - 0.5) * 16;
						const vy = 6 + hash('chk', i + 9) * 7;
						const ax = x + vx * dt;
						const ay = vy * dt - 9.8 * dt * dt;
						if (ay < -0.5) return null;
						const sz = (0.4 + 0.5 * hash('chk', i + 3)) * v.ppm;
						return <rect key={`k${i}`} x={X(v, ax) - sz / 2} y={Y(v, ay) - sz / 2} width={sz} height={sz * 0.8} fill={c(i % 2 ? 'violet-0' : 'bone-0')} transform={`rotate(${(i * 47 + dt * 300) % 360} ${X(v, ax)} ${Y(v, ay)})`} />;
					})
				: null}
			{/* dust puffs: flat bone discs that swell and fade (dust, not an animal) */}
			{dt < 1.4
				? Array.from({length: 6}, (_, i) => {
						const side = i % 2 ? 1 : -1;
						const u = clamp(dt / 1.4);
						const px = x + side * (w * 0.3 + i * 0.6) * (0.4 + u);
						const r = (0.9 + 0.4 * i) * (0.5 + u);
						return <circle key={`p${i}`} cx={X(v, px)} cy={Y(v, r * 0.6 + u * 1.5)} r={r * v.ppm} fill={c('bone-1')} opacity={0.85 * (1 - u)} />;
					})
				: null}
		</g>
	);
};

const Eiffel: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	const col = str(it.color, 'ochre-1');
	const P = (pts: [number, number][]) => 'M ' + pts.map(([a, b]) => `${f1(X(v, x + a))} ${f1(Y(v, b))}`).join(' L ') + ' Z';
	// a flat silhouette: four splayed legs, arch, two platforms, the tapering shaft, the tip
	const body: [number, number][] = [
		[-62, 0], [-44, 0], [-30, 40], [30, 40], [44, 0], [62, 0], [40, 57], [33, 62], [22, 115], [17, 122], [6, 260], [4, 276],
		[1.5, 300], [0.6, 330], [-0.6, 330], [-1.5, 300], [-4, 276], [-6, 260], [-17, 122], [-22, 115], [-33, 62], [-40, 57],
	];
	const arch = `M ${f1(X(v, x - 33))} ${f1(Y(v, 0))} Q ${f1(X(v, x))} ${f1(Y(v, 62))} ${f1(X(v, x + 33))} ${f1(Y(v, 0))} Z`;
	const sh: [number, number][] = [[8, 40], [30, 40], [44, 0], [62, 0], [40, 57], [33, 62], [22, 115], [17, 122], [6, 260], [4, 276], [1.5, 300], [0.6, 330], [0, 330], [0, 40]];
	const lattice: React.ReactNode[] = [];
	if (v.ppm > 0.6)
		for (let i = 0; i < 9; i++) {
			const a0 = 62 + i * 22;
			const a1 = a0 + 22;
			const w0 = a0 < 115 ? 33 - ((a0 - 62) / 53) * 11 : 17 - ((a0 - 122) / 138) * 11;
			const w1 = a1 < 115 ? 33 - ((a1 - 62) / 53) * 11 : 17 - ((a1 - 122) / 138) * 11;
			if (a1 > 262) break;
			lattice.push(<path key={i} d={`M ${f1(X(v, x - w0 * 0.8))} ${f1(Y(v, a0))} L ${f1(X(v, x + w1 * 0.8))} ${f1(Y(v, a1))} M ${f1(X(v, x + w0 * 0.8))} ${f1(Y(v, a0))} L ${f1(X(v, x - w1 * 0.8))} ${f1(Y(v, a1))}`} stroke={c(shade(col))} strokeWidth={Math.max(1.5, 1.4 * v.ppm)} />);
		}
	return (
		<g>
			<path d={P(body)} fill={c(col)} />
			<path d={P(sh)} fill={c(shade(col))} />
			{lattice}
			<path d={arch} fill={c('sky-2')} />
			<rect x={X(v, x - 45)} y={Y(v, 62)} width={90 * v.ppm} height={5 * v.ppm} fill={c('ochre-0')} />
			<rect x={X(v, x - 26)} y={Y(v, 120)} width={52 * v.ppm} height={4 * v.ppm} fill={c('ochre-0')} />
			<rect x={X(v, x - 7)} y={Y(v, 278)} width={14 * v.ppm} height={5 * v.ppm} fill={c('ochre-0')} />
		</g>
	);
};

const Row: React.FC<{v: View; it: Item; far?: boolean}> = ({v, it, far}) => {
	const x0 = num(it.x0, -800);
	const x1 = num(it.x1, 800);
	const seed = String(it.seed ?? 'row');
	const out: React.ReactNode[] = [];
	let x = x0;
	let i = 0;
	while (x < x1 && i < 200) {
		const w = (far ? 30 : 16) + hash(seed, i) * (far ? 40 : 14);
		const h = far ? 30 + hash(seed, i + 99) * 55 : 16 + hash(seed, i + 99) * 9;
		const wall = far ? (i % 2 ? 'dusk-4' : 'sky-3') : i % 3 === 0 ? 'bone-1' : i % 3 === 1 ? 'ochre-4' : 'bone-0';
		out.push(<rect key={i} x={X(v, x)} y={Y(v, h)} width={(w - (far ? 3 : 1)) * v.ppm} height={h * v.ppm} fill={c(wall)} />);
		if (!far) {
			out.push(<rect key={`r${i}`} x={X(v, x - 0.5)} y={Y(v, h + 3.5)} width={(w + 0) * v.ppm} height={3.5 * v.ppm} fill={c('dusk-3')} />);
			if (v.ppm > 1.5)
				for (let f = 0; f < 4; f++)
					for (let k = 0; k < Math.floor(w / 4); k++)
						out.push(<rect key={`w${i}-${f}-${k}`} x={X(v, x + 1 + k * 4)} y={Y(v, 3 + f * 3.4 + 2.2)} width={1.6 * v.ppm} height={2 * v.ppm} fill={c('dusk-2')} />);
		}
		x += w;
		i++;
	}
	return <g>{out}</g>;
};

const Mountain: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.x, 0);
	const h = num(it.h, 8849);
	const w = num(it.w, h * 2.4);
	const far = it.far === true;
	const seed = String(it.seed ?? 'mt');
	const lit = far ? 'violet-3' : 'violet-2';
	const dark = far ? 'violet-2' : 'violet-1';
	const n = 7;
	const left: [number, number][] = [];
	const right: [number, number][] = [];
	for (let i = 0; i <= n; i++) {
		const u = i / n;
		const j = i === n ? 0 : (hash(seed, i) - 0.5) * 0.08;
		left.push([x - (w / 2) * (1 - u) + j * w * 0.3, h * u + (i > 0 && i < n ? j * h * 0.6 : 0)]);
		const j2 = i === n ? 0 : (hash(seed, i + 50) - 0.5) * 0.08;
		right.push([x + (w / 2) * (1 - u) + j2 * w * 0.3, h * u + (i > 0 && i < n ? j2 * h * 0.6 : 0)]);
	}
	const pts = [...left, ...right.slice(0, -1).reverse()];
	const P = (ps: [number, number][]) => 'M ' + ps.map(([a, b]) => `${f1(X(v, a))} ${f1(Y(v, b))}`).join(' L ') + ' Z';
	const shadowSide: [number, number][] = [[x + (hash(seed, 77) - 0.5) * w * 0.06, 0], ...right.slice().reverse().filter((p) => p[1] > 0).reverse()];
	// snow cap above 70 % with a jagged lower edge
	const snowY = h * 0.7;
	const capL = left.filter((p) => p[1] >= snowY);
	const capR = right.filter((p) => p[1] >= snowY);
	const edge: [number, number][] = [];
	const xl = x - (w / 2) * 0.3;
	const xr = x + (w / 2) * 0.3;
	for (let i = 0; i <= 6; i++) {
		const u = i / 6;
		edge.push([xr - (xr - xl) * u, snowY - (i % 2 ? h * 0.05 : 0)]);
	}
	const snow = [...capL, ...capR.slice(0, -1).reverse(), ...edge.slice(1, -1)];
	return (
		<g>
			<path d={P(pts)} fill={c(lit)} />
			<path d={P([...shadowSide, [x, h]])} fill={c(dark)} />
			<path d={P(snow.length > 3 ? snow : pts)} fill={c(far ? 'bone-0' : 'bone-1')} />
			<path d={P([[x, h], ...capR.slice(0, -1).reverse(), [x + (w / 2) * 0.3, snowY], [x + w * 0.02, snowY - h * 0.05]])} fill={c('sky-3')} />
		</g>
	);
};

const Cloud: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const w = num(it.w, 1500);
	const x = num(it.x, 0) + num(it.drift, 0) * v.t;
	const alt = num(it.alt, 1200);
	const seed = String(it.seed ?? 'cl');
	const puffs = [0.18, 0.36, 0.55, 0.74].map((u, i) => ({u, r: w * (0.13 + hash(seed, i) * 0.1)}));
	return (
		<g>
			{puffs.map((p, i) => (
				<circle key={i} cx={X(v, x - w / 2 + p.u * w)} cy={Y(v, alt + p.r * 0.55)} r={p.r * v.ppm} fill={c('bone-2')} />
			))}
			<rect x={X(v, x - w / 2)} y={Y(v, alt + w * 0.09)} width={w * v.ppm} height={w * 0.09 * v.ppm} rx={w * 0.045 * v.ppm} fill={c('bone-2')} />
			<rect x={X(v, x - w / 2 + w * 0.04)} y={Y(v, alt + w * 0.035)} width={w * 0.92 * v.ppm} height={w * 0.035 * v.ppm} rx={w * 0.017 * v.ppm} fill={c('bone-0')} />
		</g>
	);
};

const Plane: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const at = num(it.at, 0);
	const dir = num(it.dir, 1);
	const L = num(it.len, 60) * num(it.scale, 1);
	const x = num(it.x, 0) + dir * num(it.v, 1500) * (v.t - at);
	const alt = num(it.alt, 10500);
	const trail = num(it.trail, 4000) * clamp((v.t - at + 2) / 2.5);
	const s = (dx: number, da: number) => `${f1(X(v, x + dir * dx * L))} ${f1(Y(v, alt + da * L))}`;
	const px = Math.max(1, L * v.ppm);
	return (
		<g>
			<rect x={Math.min(X(v, x - dir * (trail + L * 0.5)), X(v, x - dir * L * 0.5))} y={Y(v, alt + 0.05 * L)} width={trail * v.ppm} height={Math.max(3, 0.1 * px)} fill={c('bone-2')} opacity={0.85} />
			<path d={`M ${s(0.5, 0)} L ${s(0.42, 0.08)} L ${s(-0.4, 0.08)} L ${s(-0.5, 0.32)} L ${s(-0.56, 0.32)} L ${s(-0.5, 0)} Z`} fill={c('bone-1')} />
			<path d={`M ${s(0.1, 0.02)} L ${s(-0.18, -0.2)} L ${s(-0.28, -0.2)} L ${s(-0.12, 0.02)} Z`} fill={c('dusk-3')} />
			<path d={`M ${s(-0.5, 0.32)} L ${s(-0.56, 0.32)} L ${s(-0.52, 0.14)} Z`} fill={c('coral-2')} />
			<rect x={Math.min(X(v, x + dir * 0.32 * L), X(v, x - dir * 0.3 * L))} y={Y(v, alt + 0.055 * L)} width={0.62 * px} height={Math.max(1, 0.02 * px)} fill={c('sky-0')} />
		</g>
	);
};

const Karman: React.FC<{v: View}> = ({v}) => {
	if (sphereMode(v)) {
		const ex = X(v, 0);
		const ey = v.gy + R_EARTH * v.ppm;
		return <circle cx={ex} cy={ey} r={(R_EARTH + 100000) * v.ppm} fill="none" stroke={c('amber-4')} strokeWidth={5} strokeDasharray="22 16" />;
	}
	const y = Y(v, 100000);
	return <line x1={0} x2={v.W} y1={y} y2={y} stroke={c('amber-4')} strokeWidth={5} strokeDasharray="22 16" />;
};

const Moon: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const r = (MOON_D / 2) * v.ppm;
	const cx = X(v, num(it.x, 2600000));
	const cy = Y(v, num(it.alt, MOON_D / 2));
	const craters: [number, number, number][] = [[-0.35, -0.3, 0.16], [0.25, -0.45, 0.1], [0.1, 0.2, 0.22], [-0.45, 0.35, 0.12], [0.5, 0.15, 0.09]];
	return (
		<g>
			<circle cx={cx} cy={cy} r={r * 1.1} fill="none" stroke={c('bone-2')} strokeOpacity={0.18} strokeWidth={r * 0.08} />
			<circle cx={cx} cy={cy} r={r} fill={c('bone-0')} />
			{craters.map(([a, b, cr], i) => (
				<circle key={i} cx={cx + a * r} cy={cy + b * r} r={cr * r} fill={c('sky-3')} />
			))}
			<path d={`M ${f1(cx + r * 0.2)} ${f1(cy - r * 0.98)} A ${f1(r)} ${f1(r)} 0 0 1 ${f1(cx + r * 0.2)} ${f1(cy + r * 0.98)} A ${f1(r * 0.82)} ${f1(r)} 0 0 0 ${f1(cx + r * 0.2)} ${f1(cy - r * 0.98)} Z`} fill={c('dusk-4')} opacity={0.75} />
		</g>
	);
};

const Sun: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x = num(it.sx, 0.8) * v.W;
	const y = num(it.sy, 0.2) * v.H;
	const r = num(it.r, 0.07) * v.W;
	return (
		<g>
			<circle cx={x} cy={y} r={r * 1.45} fill={c('amber-5')} opacity={0.45} />
			<circle cx={x} cy={y} r={r} fill={c('amber-4')} />
		</g>
	);
};

/** far rolling hills along the ground line (pale: far layers are paler), heights in metres */
const Hills: React.FC<{v: View; it: Item}> = ({v, it}) => {
	const x0 = num(it.x0, -5000);
	const x1 = num(it.x1, 5000);
	const h = num(it.h, 250);
	const seed = String(it.seed ?? 'hl');
	const out: React.ReactNode[] = [];
	let x = x0;
	let i = 0;
	while (x < x1 && i < 120) {
		const w = h * (3 + hash(seed, i) * 4);
		const hh = h * (0.5 + hash(seed, i + 50) * 0.7);
		out.push(<ellipse key={i} cx={X(v, x + w / 2)} cy={v.gy} rx={(w / 2) * v.ppm} ry={hh * v.ppm} fill={c(i % 2 ? 'kelp-3' : 'kelp-2')} />);
		x += w * 0.7;
		i++;
	}
	return <g>{out}</g>;
};

const ITEM: Record<string, React.FC<{v: View; it: Item}>> = {
	hills: Hills,
	room: Room,
	house: House,
	block: Block,
	tree: Tree,
	car: Car,
	lamp: Lamp,
	crack: Crack,
	eiffel: Eiffel,
	paris: (p) => <Row {...p} />,
	skyline: (p) => <Row {...p} far />,
	mountain: Mountain,
	cloud: Cloud,
	plane: Plane,
	karman: ({v}) => <Karman v={v} />,
	moon: Moon,
	sun: Sun,
};

// ------------------------------------------------------------------ YOU (the kit's figure, people.tsx)

const YOU_FIG = PEOPLE.you;

/** the kit YOU (people.tsx) in a flat style-A dress: orange top, indigo trousers, a face; one flat shadow shape each */
const You: React.FC<{v: View; p: Record<string, unknown>}> = ({v, p}) => {
	const [bx, by, bw, bh] = YOU_FIG.box;
	const H = v.youH * v.ppm;
	if (H < 0.5) return null;
	const sy = track(p.sy, v.t, 1);
	const W = (bw / bh) * H;
	const pose = sched(p.pose, v.t, 'pose', 'stand');
	const face = sched(p.face, v.t, 'face', 'calm');
	const top = str(p.color, c('amber-1'));
	const ctx: DrawCtx = {t: v.t, p: {pose, color: top, outline: top, style: 'filled'}, id: 'growYou', idle: true, speed: 1, amp: 1};
	const ctxSh: DrawCtx = {...ctx, sil: c('amber-0')};
	const x0 = X(v, 0) - W / 2;
	const y0 = v.gy - H * sy;
	const breathe = Math.sin(v.t * 2) * 1.5;
	const hy = 52 + breathe;
	const legs = (
		<g>
			{['M 88 206 L 72 274 L 68 336', 'M 112 206 L 128 274 L 132 336'].map((d, i) => (
				<path key={i} d={d} stroke={c(i ? 'dusk-0' : 'dusk-1')} strokeWidth={36} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			))}
			<path d="M 78 166 L 122 166 L 121 214 C 112 222 88 222 79 214 Z" fill={c('dusk-1')} />
			<path d="M 108 166 L 122 166 L 121 214 C 117 218 112 220 108 221 Z" fill={c('dusk-0')} />
			<rect x={78} y={166} width={44} height={6} fill={c('ink-1')} />
			<ellipse cx={60} cy={346} rx={24} ry={10} fill={c('coral-2')} />
			<ellipse cx={140} cy={346} rx={24} ry={10} fill={c('coral-1')} />
			<rect x={36} y={350} width={48} height={6} rx={3} fill={c('bone-1')} />
			<rect x={116} y={350} width={48} height={6} rx={3} fill={c('bone-1')} />
		</g>
	);
	const eyes = (dy: number, r: number) => (
		<g>
			<circle cx={88} cy={hy + dy} r={r} fill={c('ink-0')} />
			<circle cx={112} cy={hy + dy} r={r} fill={c('ink-0')} />
			<circle cx={89.4} cy={hy + dy - 1.4} r={r * 0.32} fill={c('bone-2')} />
			<circle cx={113.4} cy={hy + dy - 1.4} r={r * 0.32} fill={c('bone-2')} />
		</g>
	);
	const ink = c('ink-0');
	let mouth: React.ReactNode;
	let brows: React.ReactNode = null;
	let eyesN: React.ReactNode = eyes(-2, 4.2);
	switch (face) {
		case 'smile':
			mouth = <path d={`M 90 ${hy + 10} Q 100 ${hy + 19} 110 ${hy + 10}`} stroke={ink} strokeWidth={3.4} strokeLinecap="round" fill="none" />;
			break;
		case 'worried':
			mouth = <path d={`M 92 ${hy + 15} Q 100 ${hy + 10} 108 ${hy + 15}`} stroke={ink} strokeWidth={3.4} strokeLinecap="round" fill="none" />;
			brows = <path d={`M 81 ${hy - 11} L 92 ${hy - 14} M 119 ${hy - 11} L 108 ${hy - 14}`} stroke={ink} strokeWidth={3} strokeLinecap="round" />;
			break;
		case 'strain':
			mouth = <rect x={89} y={hy + 9} width={22} height={7} rx={2} fill={c('bone-2')} stroke={ink} strokeWidth={2.4} />;
			brows = <path d={`M 81 ${hy - 14} L 93 ${hy - 9} M 119 ${hy - 14} L 107 ${hy - 9}`} stroke={ink} strokeWidth={3.2} strokeLinecap="round" />;
			eyesN = <path d={`M 83 ${hy - 2} L 93 ${hy - 2} M 107 ${hy - 2} L 117 ${hy - 2}`} stroke={ink} strokeWidth={3.4} strokeLinecap="round" />;
			break;
		case 'gasp':
			mouth = <ellipse cx={100} cy={hy + 13} rx={4.6} ry={6} fill={ink} />;
			brows = <path d={`M 81 ${hy - 12} L 92 ${hy - 15} M 119 ${hy - 12} L 108 ${hy - 15}`} stroke={ink} strokeWidth={3} strokeLinecap="round" />;
			eyesN = eyes(-2, 3.4);
			break;
		case 'shock':
		case 'wow':
			mouth = <ellipse cx={100} cy={hy + 13} rx={6.5} ry={8} fill={ink} />;
			brows = <path d={`M 81 ${hy - 15} Q 87 ${hy - 19} 93 ${hy - 15} M 107 ${hy - 15} Q 113 ${hy - 19} 119 ${hy - 15}`} stroke={ink} strokeWidth={3} strokeLinecap="round" fill="none" />;
			eyesN = eyes(-2, 5.2);
			break;
		default:
			mouth = <path d={`M 93 ${hy + 12} Q 100 ${hy + 16} 107 ${hy + 12}`} stroke={ink} strokeWidth={3.2} strokeLinecap="round" fill="none" />;
	}
	const puffs = arr<Record<string, unknown>>(p.puffs).map((e, i) => {
		const dt = v.t - num(e.at, 0);
		if (dt < 0 || dt > 1.1) return null;
		const u = dt / 1.1;
		return <circle key={i} cx={112 + u * 40} cy={hy + 12 - u * 10} r={5 + u * 10} fill={c('bone-2')} opacity={0.9 * (1 - u)} />;
	});
	return (
		// a group transform, not a nested <svg>: a nested viewport a million px tall (the dive to the feet) never paints
		<g transform={`translate(${x0.toFixed(3)} ${y0.toFixed(3)}) scale(${(W / bw).toPrecision(9)} ${((H * sy) / bh).toPrecision(9)}) translate(${-bx} ${-by})`}>
			{YOU_FIG.draw(ctx)}
			<rect x={80} y={145} width={40} height={10} fill={top} />
			{legs}
			{/* one flat shadow shape: the body's right side, away from the upper-left light */}
			<clipPath id="growYouR">
				<rect x={104} y={86} width={80} height={80} />
			</clipPath>
			<g clipPath="url(#growYouR)" opacity={0.55}>
				{YOU_FIG.draw(ctxSh)}
			</g>
			{/* head: skin, hair, a flat shadow crescent, the face */}
			<circle cx={100} cy={hy} r={40} fill={c('coral-4')} />
			<path d={`M 114 ${hy - 37.4} A 40 40 0 0 1 114 ${hy + 37.4} A 30 40 0 0 0 114 ${hy - 37.4} Z`} fill={c('coral-3')} opacity={0.7} />
			<path d={`M 60 ${hy - 2} C 58 ${hy - 48} 142 ${hy - 48} 140 ${hy - 2} C 133 ${hy - 22} 110 ${hy - 28} 92 ${hy - 22} C 80 ${hy - 19} 68 ${hy - 13} 60 ${hy - 2} Z`} fill={c('ink-1')} />
			{eyesN}
			{brows}
			{mouth}
			{puffs}
		</g>
	);
};

// ------------------------------------------------------------------ components

export const GrowWorld: KitComponent = ({props: p, time, width: W, height: H}) => {
	const v = view(p, time, W, H);
	const items = arr<Item>(p.items);
	const kind = str(p.ground, 'street');
	const seed = str(p.seed, 'grow');
	const draw = (it: Item, i: number) => {
		const C2 = ITEM[str(it.kind, '')];
		if (!C2) return null;
		if (typeof it.from === 'number' && time < it.from) return null;
		if (typeof it.until === 'number' && time > it.until) return null;
		return <C2 key={i} v={v} it={it} />;
	};
	const back = items.filter((it) => it.front !== true && it.kind !== 'room' && it.kind !== 'crack');
	const front = items.filter((it) => it.front === true);
	const room = items.find((it) => it.kind === 'room');
	const cracks = items.filter((it) => it.kind === 'crack');
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block', overflow: 'hidden'}}>
			{room ? <Room v={v} it={room} /> : <Sky v={v} seed={seed} />}
			{back.map(draw)}
			<Ground v={v} kind={room ? 'room' : kind} />
			{cracks.map(draw)}
			<You v={v} p={p} />
			{front.map(draw)}
		</svg>
	);
};

/** the clock + height plate: story time and YOU's height (1.75 m + 1 cm x clock) */
export const GrowHud: KitComponent = ({props: p, time, width: W, height: H}) => {
	const clock = clockAt(p, time);
	const youH = p.youH !== undefined ? track(p.youH, time, 1.75) : 1.75 + 0.01 * clock;
	const title = typeof p.title === 'string' && time < num(p.titleUntil, 1e9) ? p.title : null;
	const y = num(p.y, 0.075) * H;
	const op = clamp(track(p.opacity, time, 1));
	if (op <= 0.01) return null;
	const pw = 760;
	const ph = 118;
	const x = (W - pw) / 2;
	const style = obj(p.style);
	const font = C.condensed;
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block', opacity: op}}>
			<rect x={x} y={y} width={pw} height={ph} rx={26} fill={str(style.plate, C.panel)} />
			{title ? (
				<text x={x + pw / 2 + 40} y={y + ph / 2 + 19} fontFamily={font} fontSize={54} fill={c('bone-2')} letterSpacing={1} textAnchor="middle">
					{title}
				</text>
			) : (
				<g>
			<rect x={x + pw / 2 - 2} y={y + 22} width={4} height={ph - 44} fill={c('dusk-3')} />
			{/* clock icon */}
			<circle cx={x + 62} cy={y + ph / 2} r={26} fill="none" stroke={c('amber-4')} strokeWidth={6} />
			<path d={`M ${x + 62} ${y + ph / 2 - 15} L ${x + 62} ${y + ph / 2} L ${x + 73} ${y + ph / 2 + 7}`} stroke={c('amber-4')} strokeWidth={6} strokeLinecap="round" fill="none" />
			<text x={x + 104} y={y + ph / 2 + 22} fontFamily={font} fontSize={62} fill={c('bone-2')} letterSpacing={1}>
				{clockText(clock)}
			</text>
			{/* height icon: an up-down arrow */}
			<path d={`M ${x + pw / 2 + 52} ${y + 28} L ${x + pw / 2 + 52} ${y + ph - 28} M ${x + pw / 2 + 40} ${y + 40} L ${x + pw / 2 + 52} ${y + 26} L ${x + pw / 2 + 64} ${y + 40} M ${x + pw / 2 + 40} ${y + ph - 40} L ${x + pw / 2 + 52} ${y + ph - 26} L ${x + pw / 2 + 64} ${y + ph - 40}`} stroke={c('tide-3')} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			<text x={x + pw / 2 + 88} y={y + ph / 2 + 22} fontFamily={font} fontSize={62} fill={c('bone-2')} letterSpacing={1}>
				{heightText(youH)}
			</text>
						</g>
			)}
			{title ? (
				<g>
					<circle cx={x + 62} cy={y + ph / 2} r={26} fill="none" stroke={c('amber-4')} strokeWidth={6} />
					<path d={`M ${x + 62} ${y + ph / 2 - 15} L ${x + 62} ${y + ph / 2} L ${x + 73} ${y + ph / 2 + 7}`} stroke={c('amber-4')} strokeWidth={6} strokeLinecap="round" fill="none" />
				</g>
			) : null}
</svg>
	);
};

// ------------------------------------------------------------------ the square-cube board

const ease3 = (x: number) => 1 - Math.pow(1 - clamp(x), 3);

/**
 * explainer/CubeLaw: the square-cube law on a board, one row per spoken number. itemAt [taller, heavier, stronger]
 * (s): row 1 a YOU and a 20x YOU (x20 TALLER), row 2 a cube and a 20x cube (x8,000 HEAVIER, red), row 3 a square and a
 * 20x square (x400 STRONGER, aqua). Rows 2-3 carry bars at one scale, so the gap between weight and strength shows.
 * props: k (20), itemAt, top (fraction of H, 0.15), rowH (fraction, 0.16)
 */
export const CubeLaw: KitComponent = ({props: p, time, width: W, height: H}) => {
	const k = num(p.k, 20);
	const at = arr<number>(p.itemAt);
	const top = num(p.top, 0.15) * H;
	const rowH = num(p.rowH, 0.16) * H;
	const font = C.condensed;
	const rows = [
		{n: k, label: 'TALLER', col: 'bone-2', bar: null as null | string},
		{n: k * k * k, label: 'HEAVIER', col: 'coral-2', bar: 'coral-2'},
		{n: k * k, label: 'STRONGER', col: 'tide-3', bar: 'tide-3'},
	];
	const iconW = 340;
	const big = rowH * 0.78;
	const small = big / k;
	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block', overflow: 'visible'}}>
			{rows.map((r, i) => {
				const t0 = typeof at[i] === 'number' ? at[i] : i * 1.5;
				const u = ease3((time - t0) / 0.45);
				if (u <= 0) return null;
				const y = top + i * (rowH + 28);
				const cnt = Math.round(r.n * ease3((time - t0) / 0.9));
				const base = y + rowH * 0.9;
				const ix = 70;
				let icon: React.ReactNode;
				if (i === 0) {
					const [bx, by, bw, bh] = YOU_FIG.box;
					const fig = (h: number, x: number, sil: string) => (
						<svg x={x} y={base - h} width={(bw / bh) * h} height={h} viewBox={`${bx} ${by} ${bw} ${bh}`} overflow="visible">
							{YOU_FIG.draw({t: time, p: {pose: 'stand'}, id: 'cl', sil, idle: false, speed: 1, amp: 1})}
						</svg>
					);
					icon = (
						<g>
							{fig(big * u, ix + 80, c('amber-1'))}
							{fig(Math.max(4, small * 1.0), ix + 30, c('amber-1'))}
						</g>
					);
				} else if (i === 1) {
					const s = big * 0.72 * u;
					const cube = (x: number, b: number, side: number) => {
						const dd = side * 0.4;
						return (
							<g>
								<path d={`M ${x} ${b} L ${x} ${b - side} L ${x + side} ${b - side} L ${x + side} ${b} Z`} fill={c('coral-2')} />
								<path d={`M ${x} ${b - side} L ${x + dd} ${b - side - dd} L ${x + side + dd} ${b - side - dd} L ${x + side} ${b - side} Z`} fill={c('coral-3')} />
								<path d={`M ${x + side} ${b} L ${x + side} ${b - side} L ${x + side + dd} ${b - side - dd} L ${x + side + dd} ${b - dd} Z`} fill={c('coral-1')} />
							</g>
						);
					};
					icon = (
						<g>
							{cube(ix + 30, base, Math.max(5, small * 0.72))}
							{cube(ix + 80, base, s)}

						</g>
					);
				} else {
					const s = big * 0.72 * u;
					icon = (
						<g>
							<rect x={ix + 30} y={base - Math.max(5, small * 0.72)} width={Math.max(5, small * 0.72)} height={Math.max(5, small * 0.72)} fill={c('tide-3')} />
							<rect x={ix + 80} y={base - s} width={s} height={s} fill={c('tide-3')} />
							<rect x={ix + 80 + s * 0.62} y={base - s} width={s * 0.38} height={s} fill={c('tide-2')} />
						</g>
					);
				}
				const tx = ix + iconW;
				const barMax = W - tx - 70;
				return (
					<g key={i} opacity={clamp((time - t0) / 0.2)}>
						{icon}
						<text x={tx} y={y + rowH * 0.42} fontFamily={font} fontSize={rowH * 0.42} fill={c(r.col)} letterSpacing={1}>
							{`×${cnt.toLocaleString('en-US')}`}
						</text>
						<text x={tx} y={y + rowH * 0.66} fontFamily={C.font} fontWeight={800} fontSize={40} fill={c('bone-1')} letterSpacing={4}>
							{r.label}
						</text>
						{r.bar ? (
							<g>
								<rect x={tx} y={y + rowH * 0.76} width={barMax} height={26} rx={13} fill={c('ink-1')} />
								<rect x={tx} y={y + rowH * 0.76} width={Math.max(26, (barMax * cnt) / (k * k * k))} height={26} rx={13} fill={c(r.bar)} />
							</g>
						) : null}
					</g>
				);
			})}
		</svg>
	);
};
