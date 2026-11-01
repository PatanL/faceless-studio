/**
 * Ocean scene kit for the orca shot (house style, drawn fresh). All pieces read the scene light and plane
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
import {c, mixOk, shadowOf, shiftL} from '../lib/color';
import {blob, closedSpline, openSpline, taper} from '../lib/geom';
import {useLight, useTint} from '../lib/light';
import {noise1, rand, rng} from '../lib/rng';
import {Shaded} from '../shade/Shaded';
import {chain, sway} from '../motion/motion';

type P = [number, number];

// ---------------------------------------------------------------- kelp

export const Kelp: React.FC<{seed: string; x: number; y: number; h: number; t: number; segs?: number; blade?: number; silhouette?: boolean; lean?: number}> = ({
	seed,
	x,
	y,
	h,
	t,
	segs = 10,
	blade = 1,
	silhouette = false,
	lean = 0,
}) => {
	const tint = useTint();
	const L = useLight();
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
	const stipeCol = tint(silhouette ? 'ink-1' : 'kelp-1');
	const bladeBase = tint(silhouette ? 'ink-1' : 'kelp-3');
	const bladeShadow = silhouette ? bladeBase : shadowOf(bladeBase, tint(L.ambient), 0.38);
	const bladeHi = silhouette ? bladeBase : mixOk(bladeBase, tint(L.keyColor), 0.2);
	const out: React.ReactNode[] = [];
	for (let i = 2; i < pts.length; i++) {
		const [ax, ay] = pts[i - 1];
		const [bx, by] = pts[i];
		const a = Math.atan2(by - ay, bx - ax);
		const side = i % 2 ? 1 : -1;
		const ba = a + side * (0.85 + 0.25 * Math.sin(t * 0.9 + i + rand(seed, i) * 3));
		const len = (70 + rand(seed, i + 30) * 50) * blade;
		const wid = (20 + rand(seed, i + 60) * 10) * blade;
		const ux = Math.cos(ba);
		const uy = Math.sin(ba);
		const nx = -uy;
		const ny = ux;
		const tip: P = [ax + ux * len, ay + uy * len];
		const leaf = `M ${ax} ${ay} C ${ax + ux * len * 0.3 + nx * wid} ${ay + uy * len * 0.3 + ny * wid} ${tip[0] + nx * wid * 0.4} ${tip[1] + ny * wid * 0.4} ${tip[0]} ${tip[1]} C ${tip[0] - nx * wid * 0.4} ${tip[1] - ny * wid * 0.4} ${ax + ux * len * 0.3 - nx * wid} ${ay + uy * len * 0.3 - ny * wid} ${ax} ${ay} Z`;
		// shadow half: the side of the blade facing away from the key
		const away = nx * L.key[0] + ny * L.key[1] < 0 ? 1 : -1;
		const half = `M ${ax} ${ay} C ${ax + ux * len * 0.3 + away * nx * wid} ${ay + uy * len * 0.3 + away * ny * wid} ${tip[0] + away * nx * wid * 0.4} ${tip[1] + away * ny * wid * 0.4} ${tip[0]} ${tip[1]} L ${ax} ${ay} Z`;
		const hiEdge = `M ${ax + ux * len * 0.2 - away * nx * wid * 0.55} ${ay + uy * len * 0.2 - away * ny * wid * 0.55} Q ${ax + ux * len * 0.5 - away * nx * wid * 0.75} ${ay + uy * len * 0.5 - away * ny * wid * 0.75} ${ax + ux * len * 0.85 - away * nx * wid * 0.2} ${ay + uy * len * 0.85 - away * ny * wid * 0.2}`;
		out.push(
			<g key={i}>
				<path d={leaf} fill={bladeBase} />
				{silhouette ? null : (
					<>
						<path d={half} fill={bladeShadow} />
						<path d={hiEdge} stroke={bladeHi} strokeWidth={3} fill="none" strokeLinecap="round" />
						<path d={`M ${ax} ${ay} L ${ax + ux * len * 0.9} ${ay + uy * len * 0.9}`} stroke={shadowOf(bladeBase, tint(L.ambient), 0.2)} strokeWidth={2} strokeLinecap="round" />
						<circle cx={ax + ux * 10} cy={ay + uy * 10} r={6.5 * blade} fill={tint('ochre-3')} />
						<circle cx={ax + ux * 10} cy={ay + uy * 10} r={3 * blade} fill={tint('ochre-1')} />
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

export const Seabed: React.FC<{y: number; t: number; seed?: string}> = ({y, t, seed = 'bed'}) => {
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
					<stop offset="1" stopColor={tint(mixOk(c('ochre-1'), c('ink-2'), 0.5))} />
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

const FISH = 'M 22 0 C 16 -9 -4 -10 -14 -3 L -24 -10 C -22 -4 -22 4 -24 10 L -14 3 C -4 10 16 9 22 0 Z';
const FISH_BACK = 'M 22 0 C 16 -9 -4 -10 -14 -3 L -16 -1 C -4 -3 12 -3 22 0 Z';

export const FishSchool: React.FC<{t: number; seed: string; n: number; cx: number; cy: number; rx: number; ry: number; speed?: number; scale?: number; dir?: 1 | -1}> = ({
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
}) => {
	const tint = useTint();
	const L = useLight();
	const body = tint('sky-2');
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
		const s = scale * (0.75 + rand(seed, i + 300) * 0.5);
		const tail = Math.sin(t * 9 + ph) * 0.08;
		fish.push(
			<g key={i} transform={`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${ang.toFixed(1)}) scale(${s.toFixed(3)} ${(s * flipY).toFixed(3)})`}>
				<g transform={`skewY(${(tail * 60).toFixed(2)})`}>
					<path d={FISH} fill={body} />
					<path d={FISH_BACK} fill={back} />
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

export const Jelly: React.FC<{id: string; x: number; y: number; s: number; t: number}> = ({id, x, y, s, t}) => {
	const tint = useTint();
	const pump = Math.sin(2 * Math.PI * 0.6 * t + rand(id, 0) * 6);
	const bw = s * (1 + 0.08 * pump);
	const bh = s * 0.72 * (1 - 0.08 * pump);
	const yy = y - 8 * pump;
	const bell = `M ${x - bw} ${yy} C ${x - bw} ${yy - bh * 1.3} ${x + bw} ${yy - bh * 1.3} ${x + bw} ${yy} C ${x + bw * 0.6} ${yy + bh * 0.16} ${x - bw * 0.6} ${yy + bh * 0.16} ${x - bw} ${yy} Z`;
	const tents: React.ReactNode[] = [];
	for (let i = 0; i < 7; i++) {
		const bx = x - bw * 0.75 + (i * bw * 1.5) / 6;
		const pts: P[] = [[bx, yy + 4]];
		for (let j = 1; j <= 5; j++) pts.push([bx + Math.sin(t * 1.8 - j * 0.7 + i) * j * 3.2, yy + 4 + j * s * 0.32]);
		tents.push(<path key={i} d={openSpline(pts)} stroke={tint('tide-4')} strokeWidth={i % 2 ? 2.2 : 3.2} fill="none" strokeLinecap="round" opacity={0.6} />);
	}
	return (
		<g>
			{tents}
			<path d={`M ${x - bw * 0.3} ${yy + 2} C ${x - bw * 0.35} ${yy + s * 0.6} ${x + bw * 0.1} ${yy + s * 0.9} ${x} ${yy + s * 1.3}`} stroke={tint('coral-4')} strokeWidth={6} fill="none" strokeLinecap="round" opacity={0.55} />
			<Shaded
				id={id}
				R={s * 0.6}
				core={0.3}
				lod="support"
				layers={{stipple: false, innerGlow: true}}
				parts={[{d: bell, base: 'tide-3', opacity: 0.55}]}
				innerGlow={{color: 'tide-5', width: s * 0.16, opacity: 0.9}}
				over={<path d={`M ${x - bw * 0.7} ${yy - bh * 0.55} Q ${x - bw * 0.2} ${yy - bh * 1.05} ${x + bw * 0.35} ${yy - bh * 0.85}`} stroke={c('bone-2')} strokeWidth={s * 0.08} fill="none" strokeLinecap="round" opacity={0.3} />}
			/>
			{[0.3, 0.55, 0.8].map((k, i) => (
				<circle key={i} cx={x + (k - 0.55) * bw * 1.2} cy={yy - bh * 0.35} r={s * 0.08} fill="none" stroke={tint('coral-4')} strokeWidth={2} opacity={0.7} />
			))}
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
