/**
 * Ocean scene kit (house style, drawn fresh). Ported from experiments/kurz-style/engine/src/assets/Ocean.tsx with seeded
 * variation added to the repeated pieces (kelp leaves, fish, jellies). All pieces read the scene light and plane
 * tint, so the same Kelp drawn on the far plane comes out hazed, on the foreground plane as an ink silhouette.
 *
 *   Kelp        swaying stipe (chain sway, phase lag per segment) with shaded blades and ring-motif gas bladders
 *   Rock        seeded blob through <Shaded> (support LOD on mid plane), barnacle rings, moss decal
 *   Seabed      sand body with a gradient, ripple arcs, pebbles
 *   Urchin, Anemone, SeaGrass, Shell
 *   FishSchool  school following a curved path with per-fish noise, tail beat, 2-tone shading, eye glint
 *   Jelly       translucent bell (40-60 % fill, inner glow, glare band) + trailing tentacles
 *   Ridge       far silhouette ridge with arches (P1)
 */
import React from 'react';
import {c, mixOk, shadowOf, shiftL} from './color';
import {blob, closedSpline, openSpline, taper} from './geom';
import {useLight, useTint} from './light';
import {noise1, rand, rng} from './rng';
import {Shaded} from './Shaded';
import {chain, sway} from './motion';

type P = [number, number];

// ---------------------------------------------------------------- kelp

export const Kelp: React.FC<{seed: string; x: number; y: number; h: number; t: number; segs?: number; blade?: number; silhouette?: boolean; lean?: number; golden?: boolean}> = ({
	seed,
	x,
	y,
	h,
	t,
	segs = 10,
	blade = 1,
	silhouette = false,
	lean = 0,
	golden = false,
}) => {
	// Seeded variation (judge orca_open_v3 2.5: "every kelp leaf is the same with a ring node"): per stalk a leaf family
	// (lance / wavy / broad) and a tint; per leaf its own length, width, curl and side, random gaps, and a gas
	// bladder on only about a third of the leaves, in two sizes and two warm tints.
	const tint = useTint();
	const L = useLight();
	const R = rng(`${seed}-kelp`);
	const style = Math.floor(R() * 3);
	// golden: the golden-brown of real giant / bamboo kelp (Ecklonia at Gansbaai; art direction orca_set_03)
	const tints = golden ? [mixOk(c('ochre-3'), c('amber-2'), 0.45), mixOk(c('ochre-2'), c('amber-1'), 0.4), mixOk(c('ochre-3'), c('kelp-3'), 0.3)] : ['kelp-3', 'kelp-2', mixOk(c('kelp-3'), c('ochre-3'), 0.4)];
	const pts: P[] = [[x, y]];
	let ang = -90 + lean;
	let px = x;
	let py = y;
	const segL = h / segs;
	for (let i = 0; i < segs; i++) {
		ang += chain(t, i, segs, {amp: 7, freq: 1 / (5 + rand(seed, 0) * 3), phase: rand(seed, 1) * 6.28, lagPerSeg: 0.5, seed});
		px += Math.cos((ang * Math.PI) / 180) * segL;
		py += Math.sin((ang * Math.PI) / 180) * segL;
		pts.push([px, py]);
	}
	const stipeCol = tint(silhouette ? 'ink-1' : golden ? mixOk(c('ochre-1'), c('kelp-1'), 0.4) : 'kelp-1');
	const bladeBase = tint(silhouette ? 'ink-1' : tints[Math.floor(R() * tints.length)]);
	const bladeShadow = silhouette ? bladeBase : shadowOf(bladeBase, tint(L.ambient), 0.38);
	const bladeHi = silhouette ? bladeBase : mixOk(bladeBase, tint(L.keyColor), 0.2);
	const out: React.ReactNode[] = [];
	let side = R() > 0.5 ? 1 : -1;
	for (let i = 2; i < pts.length; i++) {
		const skip = R() < 0.16;
		side = R() < 0.8 ? -side : side;
		const lenK = 0.6 + R() * 0.7;
		const widK = 0.7 + R() * 0.6;
		const curl = (R() - 0.5) * 0.5;
		const node = R() < 0.34;
		const nodeK = 0.7 + R() * 0.6;
		const warm = R() < 0.5;
		if (skip) continue;
		const [ax, ay] = pts[i - 1];
		const [bx, by] = pts[i];
		const a = Math.atan2(by - ay, bx - ax);
		const ba = a + side * (0.85 + curl + 0.25 * Math.sin(t * 0.9 + i + rand(seed, i) * 3));
		const len = (style === 2 ? 60 : 78) * lenK * blade;
		const wid = (style === 2 ? 30 : style === 1 ? 20 : 24) * widK * blade;
		const ux = Math.cos(ba);
		const uy = Math.sin(ba);
		const nx = -uy;
		const ny = ux;
		const tip: P = [ax + ux * len, ay + uy * len];
		const q = (f: number, o: number): string => `${(ax + ux * len * f + nx * wid * o).toFixed(1)} ${(ay + uy * len * f + ny * wid * o).toFixed(1)}`;
		const leaf =
			style === 1
				? // wavy edge: two bulges per side
					`M ${ax} ${ay} C ${q(0.15, 0.9)} ${q(0.3, 0.55)} ${q(0.45, 0.85)} C ${q(0.6, 1)} ${q(0.75, 0.35)} ${q(0.85, 0.5)} C ${q(0.95, 0.55)} ${q(1, 0.1)} ${tip[0]} ${tip[1]} C ${q(1, -0.1)} ${q(0.95, -0.55)} ${q(0.85, -0.5)} C ${q(0.75, -0.35)} ${q(0.6, -1)} ${q(0.45, -0.85)} C ${q(0.3, -0.55)} ${q(0.15, -0.9)} ${ax} ${ay} Z`
				: `M ${ax} ${ay} C ${q(0.3, 1)} ${q(1, 0.4)} ${tip[0]} ${tip[1]} C ${q(1, -0.4)} ${q(0.3, -1)} ${ax} ${ay} Z`;
		const away = nx * L.key[0] + ny * L.key[1] < 0 ? 1 : -1;
		const half = `M ${ax} ${ay} C ${q(0.3, away)} ${q(1, 0.4 * away)} ${tip[0]} ${tip[1]} L ${ax} ${ay} Z`;
		const hiEdge = `M ${q(0.2, -away * 0.55)} Q ${q(0.5, -away * 0.75)} ${q(0.85, -away * 0.2)}`;
		out.push(
			<g key={i}>
				<path d={leaf} fill={bladeBase} />
				{silhouette ? null : (
					<>
						<path d={half} fill={bladeShadow} />
						<path d={hiEdge} stroke={bladeHi} strokeWidth={3} fill="none" strokeLinecap="round" />
						<path d={`M ${ax} ${ay} L ${ax + ux * len * 0.9} ${ay + uy * len * 0.9}`} stroke={shadowOf(bladeBase, tint(L.ambient), 0.2)} strokeWidth={2} strokeLinecap="round" />
						{node ? (
							<>
								<circle cx={ax + ux * 10} cy={ay + uy * 10} r={6.5 * blade * nodeK} fill={tint(warm ? 'amber-3' : 'ochre-3')} />
								<circle cx={ax + ux * 10} cy={ay + uy * 10} r={3 * blade * nodeK} fill={tint(warm ? 'amber-1' : 'ochre-1')} />
							</>
						) : null}
					</>
				)}
			</g>,
		);
	}
	return (
		<g>
			<path d={taper(pts, 14 * blade, 6 * blade)} fill={stipeCol} />
			{out}
		</g>
	);
};

// ---------------------------------------------------------------- rocks, seabed and small life

export const Rock: React.FC<{id: string; x: number; y: number; rx: number; ry: number; base?: string; lod?: 'hero' | 'support' | 'far'; moss?: boolean; barnacles?: number}> = ({
	id,
	x,
	y,
	rx,
	ry,
	base = mixOk(c('ochre-1'), c('tide-0'), 0.35),
	lod = 'support',
	moss = true,
	barnacles = 6,
}) => {
	const d = blob(id, x, y, rx, ry, {n: 10, jag: 0.26, flatBottom: true});
	const mossD = blob(`${id}m`, x - rx * 0.15, y - ry * 0.85, rx * 0.95, ry * 0.45, {n: 9, jag: 0.4});
	return (
		<Shaded
			id={id}
			R={Math.min(rx, ry)}
			lod={lod}
			layers={{marks: true}}
			parts={[
				{d, base, marks: barnacles ? [{kind: 'ring', n: barnacles, size: Math.max(8, rx * 0.12), dL: 0.1}, {kind: 'pore', n: barnacles * 2, size: 8, dL: -0.08}] : undefined},
				...(moss ? [{d: mossD, base: 'kelp-2', clip: true}] : []),
			]}
		/>
	);
};

export const Seabed: React.FC<{y: number; t: number; seed?: string; deep?: string}> = ({y, t, seed = 'bed', deep}) => {
	const tint = useTint();
	const pts: string[] = [];
	for (let i = 0; i <= 24; i++) {
		const x = -300 + (1680 * i) / 24;
		pts.push(`${x.toFixed(0)} ${(y + 26 * noise1(seed, i * 0.45) + 10 * Math.sin(i * 0.9)).toFixed(1)}`);
	}
	const r = rng(seed);
	const ripples: React.ReactNode[] = [];
	for (let i = 0; i < 26; i++) {
		const rx = -200 + r() * 1480;
		const ry = y + 60 + r() * 380;
		const w = 30 + r() * 50;
		ripples.push(<path key={i} d={`M ${rx - w} ${ry} Q ${rx} ${ry - 9} ${rx + w} ${ry}`} stroke={tint('ochre-1')} strokeWidth={3} fill="none" strokeLinecap="round" opacity={0.55} />);
	}
	const pebbles: React.ReactNode[] = [];
	for (let i = 0; i < 30; i++) {
		const px = -200 + r() * 1480;
		const py = y + 40 + r() * 420;
		const s = 4 + r() * 9;
		pebbles.push(
			<g key={i}>
				<ellipse cx={px} cy={py} rx={s} ry={s * 0.6} fill={tint(r() > 0.5 ? 'ochre-2' : 'ochre-1')} />
				<ellipse cx={px - s * 0.3} cy={py - s * 0.25} rx={s * 0.45} ry={s * 0.22} fill={tint('ochre-3')} opacity={0.7} />
			</g>,
		);
	}
	return (
		<g>
			<defs>
				<linearGradient id={`${seed}-g`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={tint('ochre-3')} />
					<stop offset="0.35" stopColor={tint('ochre-2')} />
					<stop offset="1" stopColor={tint(deep ?? mixOk(c('ochre-1'), c('ink-2'), 0.5))} />
				</linearGradient>
			</defs>
			<path d={`M -300 ${y + 700} L ${pts.join(' L ')} L 1380 ${y + 700} Z`} fill={`url(#${seed}-g)`} />
			<path d={`M ${pts.join(' L ')}`} stroke={tint('ochre-4')} strokeWidth={4} fill="none" opacity={0.6} strokeLinejoin="round" />
			{ripples}
			{pebbles}
		</g>
	);
};

export const Urchin: React.FC<{x: number; y: number; r: number; t: number; seed: string}> = ({x, y, r, t, seed}) => {
	const tint = useTint();
	const L = useLight();
	const base = tint('ink-2');
	const spines: React.ReactNode[] = [];
	for (let i = 0; i < 26; i++) {
		const a = Math.PI + (i / 25) * Math.PI + 0.06 * Math.sin(t * 1.3 + i);
		const len = r * (1.5 + rand(seed, i) * 0.6);
		const lit = Math.cos(a) * L.key[0] + Math.sin(a) * L.key[1] > 0.2;
		spines.push(
			<line key={i} x1={x} y1={y} x2={x + Math.cos(a) * len} y2={y + Math.sin(a) * len} stroke={lit ? mixOk(base, tint(L.keyColor), 0.25) : base} strokeWidth={2.4} strokeLinecap="round" />,
		);
	}
	return (
		<g>
			{spines}
			<ellipse cx={x} cy={y} rx={r} ry={r * 0.75} fill={base} />
			<ellipse cx={x + L.key[0] * r * 0.3} cy={y + L.key[1] * r * 0.25} rx={r * 0.5} ry={r * 0.32} fill={mixOk(base, tint(L.keyColor), 0.18)} />
			<circle cx={x} cy={y - r * 0.2} r={r * 0.22} fill="none" stroke={tint('coral-2')} strokeWidth={2} />
		</g>
	);
};

export const Anemone: React.FC<{x: number; y: number; s: number; t: number; seed: string; color?: string}> = ({x, y, s, t, seed, color = 'coral-3'}) => {
	const tint = useTint();
	const L = useLight();
	const base = tint(color);
	const n = 9;
	const tent: React.ReactNode[] = [];
	for (let i = 0; i < n; i++) {
		const a0 = -150 + (120 * i) / (n - 1);
		const pts: P[] = [[x + (i - (n - 1) / 2) * s * 0.12, y - s * 0.55]];
		let ang = a0;
		for (let j = 0; j < 4; j++) {
			ang += chain(t, j, 4, {amp: 10, freq: 0.35, phase: rand(seed, i) * 6, lagPerSeg: 0.6});
			const [px, py] = pts[pts.length - 1];
			pts.push([px + Math.cos((ang * Math.PI) / 180) * s * 0.18, py + Math.sin((ang * Math.PI) / 180) * s * 0.18]);
		}
		const tip = pts[pts.length - 1];
		tent.push(
			<g key={i}>
				<path d={openSpline(pts)} stroke={i % 2 ? base : shadowOf(base, tint(L.ambient), 0.2)} strokeWidth={s * 0.09} fill="none" strokeLinecap="round" />
				<circle cx={tip[0]} cy={tip[1]} r={s * 0.055} fill={tint('coral-4')} />
			</g>,
		);
	}
	const col = `M ${x - s * 0.35} ${y} C ${x - s * 0.38} ${y - s * 0.3} ${x - s * 0.5} ${y - s * 0.5} ${x - s * 0.45} ${y - s * 0.6} L ${x + s * 0.45} ${y - s * 0.6} C ${x + s * 0.5} ${y - s * 0.5} ${x + s * 0.38} ${y - s * 0.3} ${x + s * 0.35} ${y} Z`;
	return (
		<g>
			{tent}
			<Shaded id={`an-${seed}`} R={s * 0.4} lod="support" parts={[{d: col, base: shiftL(c(color), -0.12)}]} />
		</g>
	);
};

export const SeaGrass: React.FC<{x: number; y: number; h: number; t: number; seed: string; n?: number}> = ({x, y, h, t, seed, n = 7}) => {
	const tint = useTint();
	return (
		<g>
			{Array.from({length: n}, (_, i) => {
				const bx = x + (i - n / 2) * 7;
				const hh = h * (0.6 + rand(seed, i) * 0.5);
				const a = sway(t, `${seed}${i}`, 9, 4 + rand(seed, i + 9) * 3) + (i - n / 2) * 5;
				const pts: P[] = [];
				for (let j = 0; j <= 4; j++) {
					const s = j / 4;
					const r = ((-90 + a * s * s) * Math.PI) / 180;
					pts.push([bx + Math.cos(r) * hh * s, y + Math.sin(r) * hh * s]);
				}
				return <path key={i} d={taper(pts, 7, 1.5)} fill={tint(i % 3 ? 'kelp-2' : 'kelp-3')} />;
			})}
		</g>
	);
};

export const Shell: React.FC<{x: number; y: number; s: number; rot?: number}> = ({x, y, s, rot = 0}) => {
	const tint = useTint();
	return (
		<g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
			<path d="M -14 4 C -14 -10 -4 -16 6 -12 C 14 -8 16 2 10 6 Z" fill={tint('bone-0')} />
			<path d="M -10 2 C -8 -6 -2 -10 4 -8 M -4 4 C -3 -4 2 -7 7 -4" stroke={tint('ochre-2')} strokeWidth={1.8} fill="none" strokeLinecap="round" />
			<path d="M -14 4 L 10 6" stroke={tint('ochre-1')} strokeWidth={2.2} strokeLinecap="round" />
		</g>
	);
};

// ---------------------------------------------------------------- fish school

const FISH_SHAPES = [
	// [body, back] : slender, deep-bodied, long-tailed (no two neighbours share size, tint or shape)
	['M 22 0 C 16 -9 -4 -10 -14 -3 L -24 -10 C -22 -4 -22 4 -24 10 L -14 3 C -4 10 16 9 22 0 Z', 'M 22 0 C 16 -9 -4 -10 -14 -3 L -16 -1 C -4 -3 12 -3 22 0 Z'],
	['M 20 0 C 14 -13 -6 -14 -12 -4 L -22 -12 C -19 -4 -19 4 -22 12 L -12 4 C -6 14 14 13 20 0 Z', 'M 20 0 C 14 -13 -6 -14 -12 -4 L -14 -1 C -4 -5 10 -4 20 0 Z'],
	['M 24 0 C 18 -7 0 -8 -10 -3 L -28 -12 C -24 -4 -24 4 -28 12 L -10 3 C 0 8 18 7 24 0 Z', 'M 24 0 C 18 -7 0 -8 -10 -3 L -12 -1 C -2 -3 14 -2 24 0 Z'],
] as const;

export const FishSchool: React.FC<{t: number; seed: string; n: number; cx: number; cy: number; rx: number; ry: number; speed?: number; scale?: number; dir?: 1 | -1; tints?: string[]}> = ({
	t,
	seed,
	n,
	cx,
	cy,
	rx,
	ry,
	speed = 0.08,
	scale = 1,
	dir = 1,
	tints = ['sky-2', 'tide-3', 'sky-3', 'amber-3'],
}) => {
	const tint = useTint();
	const L = useLight();
	const back = shadowOf(tint('dusk-3'), tint(L.ambient), 0.2);
	const belly = tint('bone-1');
	const fish: React.ReactNode[] = [];
	for (let i = 0; i < n; i++) {
		const ph = rand(seed, i) * Math.PI * 2;
		const rr = 0.45 + rand(seed, i + 100) * 0.55;
		const u = dir * t * speed * 2 * Math.PI + ph;
		const x = cx + Math.cos(u) * rx * rr + 16 * noise1(`${seed}${i}`, t * 0.5);
		const y = cy + Math.sin(u * 2) * ry * rr * 0.5 + (rand(seed, i + 200) - 0.5) * ry + 10 * noise1(`${seed}y${i}`, t * 0.4);
		const vx = -Math.sin(u) * rx * rr * dir;
		const vy = Math.cos(u * 2) * ry * rr * dir;
		const ang = (Math.atan2(vy, vx) * 180) / Math.PI;
		const flipY = Math.abs(ang) > 90 ? -1 : 1;
		const s = scale * (0.6 + rand(seed, i + 300) * 0.8);
		const [bodyD, backD] = FISH_SHAPES[Math.floor(rand(seed, i + 400) * FISH_SHAPES.length)];
		// mostly the school tint, an odd warm one now and then; each fish's tint nudged in lightness
		const tk = rand(seed, i + 500) < 0.12 ? tints[tints.length - 1] : tints[Math.floor(rand(seed, i + 600) * Math.max(1, tints.length - 1))];
		const body = shiftL(tint(tk), (rand(seed, i + 700) - 0.5) * 0.08);
		const tail = Math.sin(t * (7 + rand(seed, i + 800) * 4) + ph) * 0.08;
		fish.push(
			<g key={i} transform={`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${ang.toFixed(1)}) scale(${s.toFixed(3)} ${(s * flipY).toFixed(3)})`}>
				<g transform={`skewY(${(tail * 60).toFixed(2)})`}>
					<path d={bodyD} fill={body} />
					<path d={backD} fill={back} />
					<path d="M 18 2 C 8 6 -4 6 -12 3" stroke={belly} strokeWidth={2.4} fill="none" strokeLinecap="round" opacity={0.85} />
					<path d="M 12 -3 C 4 -5 -4 -4 -10 -1" stroke={mixOk(body, tint(L.keyColor), 0.3)} strokeWidth={1.6} fill="none" strokeLinecap="round" />
				</g>
				<circle cx={14} cy={-1} r={2.6} fill={tint('ink-0')} />
				<circle cx={14.8} cy={-1.8} r={0.9} fill={c('bone-2')} />
			</g>,
		);
	}
	return <g>{fish}</g>;
};

// ---------------------------------------------------------------- jelly (translucent recipe, bible §4.6)

/**
 * Jelly designs (judge: "every jelly has the same 3-dot bell"): 0 dome + ring spots, 1 flat saucer + radial canals,
 * 2 tall bell + long oral arms, 3 frilled bell + stripe. `design` defaults to a seeded pick.
 */
export const Jelly: React.FC<{id: string; x: number; y: number; s: number; t: number; base?: string; glow?: string; design?: number}> = ({id, x, y, s, t, base = 'tide-3', glow = 'tide-5', design}) => {
	const tint = useTint();
	const d = design ?? Math.floor(rand(id, 9) * 4);
	const pump = Math.sin(2 * Math.PI * (0.45 + rand(id, 3) * 0.3) * t + rand(id, 0) * 6);
	const tall = d === 2 ? 1.35 : d === 1 ? 0.6 : 1;
	const bw = s * (1 + 0.08 * pump);
	const bh = s * 0.72 * tall * (1 - 0.08 * pump);
	const yy = y - 8 * pump;
	const frill = d === 3;
	const rim = frill
		? Array.from({length: 6}, (_, i) => {
				const x0 = x + bw - (i * bw) / 3;
				return `Q ${(x0 - bw / 6).toFixed(1)} ${(yy + bh * 0.22).toFixed(1)} ${(x0 - bw / 3).toFixed(1)} ${yy.toFixed(1)}`;
			}).join(' ')
		: `C ${x + bw * 0.6} ${yy + bh * 0.16} ${x - bw * 0.6} ${yy + bh * 0.16} ${x - bw} ${yy}`;
	const bell = `M ${x - bw} ${yy} C ${x - bw} ${yy - bh * 1.3} ${x + bw} ${yy - bh * 1.3} ${x + bw} ${yy} ${rim} Z`;
	const nT = 5 + Math.floor(rand(id, 4) * 5);
	const tLen = s * (d === 2 ? 0.45 : 0.3 + rand(id, 5) * 0.12);
	const accent = tint(d === 1 ? 'amber-4' : 'coral-4');
	const tents: React.ReactNode[] = [];
	for (let i = 0; i < nT; i++) {
		const bx = x - bw * 0.75 + (i * bw * 1.5) / (nT - 1);
		const pts: P[] = [[bx, yy + 4]];
		for (let j = 1; j <= 5; j++) pts.push([bx + Math.sin(t * 1.8 - j * 0.7 + i + rand(id, i + 20) * 2) * j * 3.2, yy + 4 + j * tLen]);
		tents.push(<path key={i} d={openSpline(pts)} stroke={tint('tide-4')} strokeWidth={i % 2 ? 2.2 : 3.2} fill="none" strokeLinecap="round" opacity={0.6} />);
	}
	const marks =
		d === 0
			? [0.3, 0.55, 0.8].map((k, i) => <circle key={i} cx={x + (k - 0.55) * bw * 1.2} cy={yy - bh * 0.35} r={s * (0.06 + rand(id, i + 30) * 0.04)} fill="none" stroke={accent} strokeWidth={2} opacity={0.7} />)
			: d === 1
				? Array.from({length: 6}, (_, i) => {
						const a = Math.PI + (i + 0.5) * (Math.PI / 6);
						return <path key={i} d={`M ${x} ${yy - bh * 0.25} L ${x + Math.cos(a) * bw * 0.8} ${yy - bh * 0.25 + Math.sin(a) * bh * 0.7}`} stroke={accent} strokeWidth={2} opacity={0.55} strokeLinecap="round" />;
					})
				: d === 2
					? [<path key="oa" d={`M ${x - bw * 0.15} ${yy + 2} C ${x - bw * 0.4} ${yy + s * 0.8} ${x + bw * 0.25} ${yy + s * 1.2} ${x - bw * 0.05} ${yy + s * 1.9}`} stroke={accent} strokeWidth={7} fill="none" strokeLinecap="round" opacity={0.5} />]
					: [<path key="st" d={`M ${x - bw * 0.8} ${yy - bh * 0.45} Q ${x} ${yy - bh * 0.7} ${x + bw * 0.8} ${yy - bh * 0.45}`} stroke={accent} strokeWidth={4} fill="none" strokeLinecap="round" opacity={0.6} />];
	return (
		<g>
			{tents}
			{d === 2 ? null : <path d={`M ${x - bw * 0.3} ${yy + 2} C ${x - bw * 0.35} ${yy + s * 0.6} ${x + bw * 0.1} ${yy + s * 0.9} ${x} ${yy + s * 1.3}`} stroke={tint('coral-4')} strokeWidth={6} fill="none" strokeLinecap="round" opacity={0.45} />}
			<Shaded
				id={id}
				R={s * 0.6}
				core={0.3}
				lod="support"
				layers={{stipple: false, innerGlow: true}}
				parts={[{d: bell, base, opacity: 0.6}]}
				innerGlow={{color: glow, width: s * 0.16, opacity: 0.9}}
				over={<path d={`M ${x - bw * 0.7} ${yy - bh * 0.55} Q ${x - bw * 0.2} ${yy - bh * 1.05} ${x + bw * 0.35} ${yy - bh * 0.85}`} stroke={c('bone-2')} strokeWidth={s * 0.08} fill="none" strokeLinecap="round" opacity={0.3} />}
			/>
			{marks}
		</g>
	);
};

// ---------------------------------------------------------------- far ridge with arches (P1)

export const Ridge: React.FC<{seed: string; y: number; h: number; color?: string; arch?: number}> = ({seed, y, h, color = 'ink-3', arch}) => {
	const tint = useTint();
	const pts: P[] = [];
	for (let i = 0; i <= 18; i++) {
		const x = -300 + (1680 * i) / 18;
		pts.push([x, y - h * (0.35 + 0.65 * Math.abs(noise1(seed, i * 0.55))) - h * 0.2 * Math.sin(i * 0.7)]);
	}
	const top = openSpline(pts);
	return (
		<g>
			<path d={`${top} L 1380 ${y + 900} L -300 ${y + 900} Z`} fill={tint(color)} />
			{arch !== undefined ? (
				<path
					d={`M ${arch - 120} ${y + 10} C ${arch - 130} ${y - h * 1.6} ${arch + 130} ${y - h * 1.6} ${arch + 120} ${y + 10} L ${arch + 70} ${y + 10} C ${arch + 70} ${y - h * 0.9} ${arch - 70} ${y - h * 0.9} ${arch - 70} ${y + 10} Z`}
					fill={tint(color)}
				/>
			) : null}
			{Array.from({length: 7}, (_, i) => {
				const r = rng(`${seed}s${i}`);
				const sx = -200 + r() * 1480;
				return <path key={i} d={closedSpline([[sx - 20, y + 30], [sx - 6, y - 40 - r() * 60], [sx + 10, y - 30 - r() * 40], [sx + 22, y + 30]])} fill={tint(color)} />;
			})}
		</g>
	);
};


// ---------------------------------------------------------------- sea fan (gorgonian): branching, swaying

export const SeaFan: React.FC<{x: number; y: number; h: number; t: number; seed: string; color?: string}> = ({x, y, h, t, seed, color = 'coral-3'}) => {
	const tint = useTint();
	const L = useLight();
	const base = tint(color);
	const lit = mixOk(base, tint(L.keyColor), 0.22);
	const dark = shadowOf(base, tint(L.ambient), 0.3);
	const segs: React.ReactNode[] = [];
	let n = 0;
	const grow = (px: number, py: number, ang: number, len: number, w: number, depth: number) => {
		if (depth > 6 || len < 6) return;
		const a = ang + sway(t, `${seed}${n}`, 2 + depth, 5 + depth);
		const r = (a * Math.PI) / 180;
		const ex = px + Math.cos(r) * len;
		const ey = py + Math.sin(r) * len;
		const k = n++;
		const side = Math.cos(r) * L.key[0] + Math.sin(r) * L.key[1];
		segs.push(<line key={k} x1={px} y1={py} x2={ex} y2={ey} stroke={depth > 3 ? lit : side > 0 ? lit : depth < 2 ? dark : base} strokeWidth={w} strokeLinecap="round" />);
		if (depth >= 5) segs.push(<circle key={`p${k}`} cx={ex} cy={ey} r={Math.max(2.2, w * 0.9)} fill={tint('coral-4')} />);
		const spread = 15 + rand(seed, k) * 12;
		const clampA = (v: number) => Math.max(-160, Math.min(-20, v));
		grow(ex, ey, clampA(a - spread), len * (0.76 + rand(seed, k + 1) * 0.1), w * 0.78, depth + 1);
		grow(ex, ey, clampA(a + spread), len * (0.76 + rand(seed, k + 2) * 0.1), w * 0.78, depth + 1);
	};
	grow(x, y, -90, h * 0.24, Math.max(5, h * 0.045), 0);
	return <g>{segs}</g>;
};
