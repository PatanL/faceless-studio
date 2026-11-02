/**
 * Reef set dressing, all seeded and varied (no two instances alike), shaded WITHOUT outlines and without
 * per-object masks: the "stack" recipe draws the same silhouette 3-4 times (rim tone, core-shadow tone, base
 * shrunk + nudged toward the key, highlight plane further toward the key), which gives a hard crescent
 * shadow, a lit plane and a rim from the scene light for the cost of a few paths. Internal texture (grooves,
 * strata, ribs, polyps) is clipped to the silhouette and stays within ±10 % of the local value.
 *
 * lod 'far' = silhouette + one shadow step (bible §6: far planes keep L0/L1 only).
 */
import React from 'react';
import {c, mixOk, shadowOf, shiftL, lum} from '../../../kurz-style/engine/src/lib/color';
import {blob, closedSpline, openSpline, taper} from '../../../kurz-style/engine/src/lib/geom';
import {useLight, useTint} from '../../../kurz-style/engine/src/lib/light';
import {rand, rng} from '../../../kurz-style/engine/src/lib/rng';
import {chain} from '../../../kurz-style/engine/src/motion/motion';
import {placeMarks} from './marks';
import {SurfaceMarks} from './SurfaceMarks';
import type {Pt} from './pathgeo';

type Lod = 'mid' | 'far';
const vs = (base: string, f: number) => shiftL(base, lum(base) * f);

/** the mask-free shading stack for a closed silhouette */
export const Stack: React.FC<{d: string; cx: number; cy: number; R: number; base: string; lod?: Lod; hi?: number; core?: number; rim?: boolean}> = ({
	d,
	cx,
	cy,
	R,
	base,
	lod = 'mid',
	hi = 0.2,
	core = 0.36,
	rim = true,
}) => {
	const tint = useTint();
	const L = useLight();
	const b = tint(base);
	const sh = shadowOf(b, tint(L.ambient), core);
	const k = L.key;
	const r = L.rim;
	const at = (s: number, dx: number, dy: number) => `translate(${(cx + dx).toFixed(1)} ${(cy + dy).toFixed(1)}) scale(${s}) translate(${(-cx).toFixed(1)} ${(-cy).toFixed(1)})`;
	if (lod === 'far')
		return (
			<g>
				<path d={d} fill={sh} />
				<path d={d} fill={b} transform={at(0.9, k[0] * 0.09 * R, k[1] * 0.09 * R)} />
			</g>
		);
	return (
		<g>
			<path d={d} fill={rim && R > 40 ? mixOk(sh, tint(L.rimColor), 0.7) : sh} />
			{rim && R > 40 ? <path d={d} fill={sh} transform={at(0.975, -r[0] * 0.022 * R, -r[1] * 0.022 * R)} /> : null}
			<path d={d} fill={b} transform={at(0.86, k[0] * 0.12 * R, k[1] * 0.12 * R)} />
			<path d={d} fill={mixOk(b, tint(L.keyColor), hi)} transform={at(0.52, k[0] * 0.36 * R, k[1] * 0.36 * R)} />
		</g>
	);
};

const clipId = (seed: string) => `clip-${seed.replace(/[^a-z0-9]/gi, '')}`;

// ---------------------------------------------------------------- rocks

export const Rock: React.FC<{seed: string; x: number; y: number; rx: number; ry: number; base?: string; lod?: Lod; algae?: boolean}> = ({
	seed,
	x,
	y,
	rx,
	ry,
	base = mixOk(c('ochre-2'), c('coral-1'), 0.3),
	lod = 'mid',
	algae = true,
}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`rock:${seed}`);
	const d = blob(`rk${seed}`, x, y - ry * 0.45, rx, ry, {n: 9 + Math.floor(r() * 4), jag: 0.22 + r() * 0.12, flatBottom: true});
	const R = Math.min(rx, ry);
	if (lod === 'far') return <Stack d={d} cx={x} cy={y - ry * 0.45} R={R} base={base} lod="far" />;
	const id = clipId(`rock${seed}`);
	const b = tint(base);
	const strata: React.ReactNode[] = [];
	const ns = 2 + Math.floor(r() * 3);
	for (let i = 0; i < ns; i++) {
		const yy = y - ry * (0.2 + 0.9 * (i + r() * 0.5) / ns);
		const pts: Pt[] = [];
		for (let j = 0; j <= 5; j++) pts.push([x - rx * 1.1 + (2.2 * rx * j) / 5, yy + (r() - 0.5) * ry * 0.14]);
		strata.push(<path key={i} d={openSpline(pts)} stroke={vs(b, -0.09)} strokeWidth={Math.max(2.5, ry * 0.035)} fill="none" strokeLinecap="round" opacity={0.85} />);
	}
	const marks = placeMarks({seed: `rock${seed}`, d, key: L.key, rim: L.rim, R, clusters: 3 + Math.floor(rx / 60), kinds: {pores: 3, dash: 2, spots: 1}, size: Math.max(4, R * 0.09)});
	const patches: React.ReactNode[] = [];
	if (algae) {
		const np = 1 + Math.floor(r() * 3);
		for (let i = 0; i < np; i++) {
			const px = x + (r() - 0.5) * rx * 1.3;
			const py = y - ry * (0.7 + r() * 0.8);
			patches.push(<path key={i} d={blob(`alg${seed}${i}`, px, py, rx * (0.2 + r() * 0.25), ry * (0.12 + r() * 0.12), {n: 8, jag: 0.5})} fill={tint(i % 2 ? 'coral-4' : 'kelp-3')} opacity={0.9} />);
		}
	}
	return (
		<g>
			<defs>
				<clipPath id={id}>
					<path d={d} />
				</clipPath>
			</defs>
			<Stack d={d} cx={x} cy={y - ry * 0.45} R={R} base={base} />
			<g clipPath={`url(#${id})`}>
				{strata}
				{patches}
			</g>
			<SurfaceMarks marks={marks} base={base} />
		</g>
	);
};

// ---------------------------------------------------------------- corals

/** brain coral: dome with meandering ridge-and-groove lines */
export const Brain: React.FC<{seed: string; x: number; y: number; r: number; base?: string; lod?: Lod}> = ({seed, x, y, r: rad, base = 'kelp-3', lod = 'mid'}) => {
	const tint = useTint();
	const L = useLight();
	const rr = rng(`brain:${seed}`);
	const cy = y - rad * 0.5;
	const d = blob(`br${seed}`, x, cy, rad, rad * 0.62, {n: 11, jag: 0.1, flatBottom: true});
	if (lod === 'far') return <Stack d={d} cx={x} cy={cy} R={rad * 0.6} base={base} lod="far" />;
	const id = clipId(`brain${seed}`);
	const b = tint(base);
	const grooves: React.ReactNode[] = [];
	const ng = 5 + Math.floor(rad / 18);
	for (let i = 0; i < ng; i++) {
		let gx = x + (rr() - 0.5) * rad * 1.6;
		let gy = cy + (rr() - 0.5) * rad;
		let a = rr() * Math.PI * 2;
		const pts: Pt[] = [[gx, gy]];
		for (let j = 0; j < 7; j++) {
			a += (rr() - 0.5) * 1.6;
			gx += Math.cos(a) * rad * 0.16;
			gy += Math.sin(a) * rad * 0.1;
			pts.push([gx, gy]);
		}
		const sp = openSpline(pts);
		grooves.push(
			<g key={i}>
				<path d={sp} stroke={vs(b, -0.1)} strokeWidth={Math.max(3, rad * 0.05)} fill="none" strokeLinecap="round" />
				<path d={sp} stroke={vs(b, 0.08)} strokeWidth={Math.max(1.6, rad * 0.022)} fill="none" strokeLinecap="round" transform={`translate(${L.key[0] * 3} ${L.key[1] * 3})`} />
			</g>,
		);
	}
	return (
		<g>
			<defs>
				<clipPath id={id}>
					<path d={d} />
				</clipPath>
			</defs>
			<Stack d={d} cx={x} cy={cy} R={rad * 0.6} base={base} />
			<g clipPath={`url(#${id})`}>{grooves}</g>
		</g>
	);
};

/** branching (antler) coral: recursive round-capped branches, cylinder-shaded by three offset passes */
export const Branch: React.FC<{seed: string; x: number; y: number; h: number; t: number; base?: string; lod?: Lod; spread?: number}> = ({
	seed,
	x,
	y,
	h,
	t,
	base = 'coral-3',
	lod = 'mid',
	spread = 1,
}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`branch:${seed}`);
	const segs: {a: Pt; b: Pt; w: number; tip: boolean}[] = [];
	const grow = (p: Pt, ang: number, len: number, w: number, depth: number) => {
		const sway = 1.6 * Math.sin(t * 0.8 + depth + rand(seed, depth) * 6) * (4 - depth) * 0.3;
		const a2 = ang + sway;
		const q: Pt = [p[0] + Math.cos((a2 * Math.PI) / 180) * len, p[1] + Math.sin((a2 * Math.PI) / 180) * len];
		const leaf = depth >= 3 || len < 14;
		segs.push({a: p, b: q, w, tip: leaf});
		if (leaf) return;
		const n = 2 + (r() < 0.35 ? 1 : 0);
		for (let i = 0; i < n; i++) {
			const da = (n === 2 ? (i ? 1 : -1) : i - 1) * (18 + r() * 22) * spread;
			grow(q, a2 + da + (r() - 0.5) * 10, len * (0.62 + r() * 0.18), w * 0.72, depth + 1);
		}
	};
	const trunks = 1 + Math.floor(r() * 3);
	for (let i = 0; i < trunks; i++) grow([x + (i - (trunks - 1) / 2) * h * 0.12, y], -90 + (i - (trunks - 1) / 2) * 18 + (r() - 0.5) * 12, h * 0.36, Math.max(6, h * 0.1), 0);
	const b = tint(base);
	const sh = shadowOf(b, tint(L.ambient), 0.36);
	const k = L.key;
	if (lod === 'far')
		return (
			<g>
				{segs.map((s, i) => (
					<line key={i} x1={s.a[0]} y1={s.a[1]} x2={s.b[0]} y2={s.b[1]} stroke={b} strokeWidth={s.w} strokeLinecap="round" />
				))}
			</g>
		);
	const hiC = mixOk(b, tint(L.keyColor), 0.14);
	const tipC = tint('coral-4');
	return (
		<g>
			{segs.map((s, i) => (
				<line key={`s${i}`} x1={s.a[0]} y1={s.a[1]} x2={s.b[0]} y2={s.b[1]} stroke={sh} strokeWidth={s.w} strokeLinecap="round" />
			))}
			{segs.map((s, i) => (
				<line key={`b${i}`} x1={s.a[0] + k[0] * s.w * 0.14} y1={s.a[1] + k[1] * s.w * 0.14} x2={s.b[0] + k[0] * s.w * 0.14} y2={s.b[1] + k[1] * s.w * 0.14} stroke={b} strokeWidth={s.w * 0.68} strokeLinecap="round" />
			))}
			{segs.map((s, i) => (
				<line key={`h${i}`} x1={s.a[0] + k[0] * s.w * 0.28} y1={s.a[1] + k[1] * s.w * 0.28} x2={s.b[0] + k[0] * s.w * 0.28} y2={s.b[1] + k[1] * s.w * 0.28} stroke={hiC} strokeWidth={s.w * 0.24} strokeLinecap="round" />
			))}
			{segs
				.filter((s, i) => s.tip && i % 3 !== 1)
				.map((s, i) => (
					<circle key={`t${i}`} cx={s.b[0]} cy={s.b[1]} r={Math.max(2, s.w * 0.36)} fill={tipC} />
				))}
		</g>
	);
};

/** table coral: a plate on a short stalk, polyp dots along the front edge, radial ridges on top */
export const Table: React.FC<{seed: string; x: number; y: number; w: number; base?: string; lod?: Lod}> = ({seed, x, y, w, base = 'amber-3', lod = 'mid'}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`table:${seed}`);
	const h = w * (0.35 + r() * 0.2);
	const py = y - h;
	const tilt = (r() - 0.5) * 8;
	const plate = blob(`tb${seed}`, x, py, w, w * 0.17, {n: 12, jag: 0.12});
	const b = tint(base);
	const sh = shadowOf(b, tint(L.ambient), 0.4);
	const stalk = taper(
		[
			[x, y],
			[x + w * 0.04, y - h * 0.5],
			[x - w * 0.02, py],
		],
		w * 0.24,
		w * 0.12,
	);
	if (lod === 'far')
		return (
			<g transform={`rotate(${tilt} ${x} ${py})`}>
				<path d={stalk} fill={sh} />
				<path d={plate} fill={b} />
			</g>
		);
	const dots: React.ReactNode[] = [];
	const nd = 8 + Math.floor(w / 14);
	for (let i = 0; i < nd; i++) {
		const a = Math.PI * (0.05 + (0.9 * i) / (nd - 1));
		const dx = x + Math.cos(Math.PI - a) * w * 0.92;
		const dy = py + Math.sin(a) * w * 0.14;
		dots.push(<circle key={i} cx={dx} cy={dy} r={Math.max(2, w * 0.022)} fill={vs(mixOk(b, tint(L.keyColor), 0.25), 0.08)} />);
	}
	const ridges: React.ReactNode[] = [];
	for (let i = 0; i < 7; i++) {
		const a = -Math.PI * (0.15 + (0.7 * i) / 6);
		ridges.push(<line key={i} x1={x} y1={py} x2={x + Math.cos(a) * w * 0.8} y2={py + Math.sin(a) * w * 0.12} stroke={vs(b, 0.08)} strokeWidth={2.4} strokeLinecap="round" />);
	}
	return (
		<g transform={`rotate(${tilt} ${x} ${py})`}>
			<path d={stalk} fill={sh} />
			<path d={plate} fill={sh} />
			<path d={plate} fill={b} transform={`translate(${x} ${py - w * 0.04}) scale(0.97 0.78) translate(${-x} ${-py})`} />
			<path d={plate} fill={mixOk(b, tint(L.keyColor), 0.2)} transform={`translate(${x + L.key[0] * w * 0.12} ${py - w * 0.07}) scale(0.62 0.42) translate(${-x} ${-py})`} />
			{ridges}
			{dots}
		</g>
	);
};

/** tube sponges: 2-5 capsules of varied height and lean, each with a deep-toned opening */
export const Tubes: React.FC<{seed: string; x: number; y: number; h: number; t: number; base?: string; lod?: Lod}> = ({seed, x, y, h, t, base = 'coral-2', lod = 'mid'}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`tubes:${seed}`);
	const n = 2 + Math.floor(r() * 4);
	const b0 = tint(base);
	const out: React.ReactNode[] = [];
	const order = Array.from({length: n}, (_, i) => i).sort(() => r() - 0.5);
	for (const i of order) {
		const hh = h * (0.45 + r() * 0.6);
		const w = h * (0.13 + r() * 0.07);
		const bx = x + (i - (n - 1) / 2) * w * 1.15;
		const lean = (i - (n - 1) / 2) * 7 + (r() - 0.5) * 8 + 1.5 * Math.sin(t * 0.7 + i);
		const b = mixOk(b0, tint('amber-3'), r() * 0.25);
		const sh = shadowOf(b, tint(L.ambient), 0.36);
		const k = L.key;
		const tx = `rotate(${lean.toFixed(1)} ${bx} ${y})`;
		const body = `M ${bx - w / 2} ${y} L ${bx - w / 2} ${y - hh} L ${bx + w / 2} ${y - hh} L ${bx + w / 2} ${y} Z`;
		out.push(
			<g key={i} transform={tx}>
				<path d={body} fill={sh} />
				{lod === 'far' ? null : (
					<>
						<rect x={k[0] < 0 ? bx - w / 2 : bx - w * 0.1} y={y - hh} width={w * 0.6} height={hh} fill={b} />
						<rect x={k[0] < 0 ? bx - w * 0.34 : bx + w * 0.16} y={y - hh} width={w * 0.18} height={hh} fill={mixOk(b, tint(L.keyColor), 0.22)} />
						{[0.3, 0.55, 0.78].map((f, j) => (
							<line key={j} x1={bx - w / 2 + 2} y1={y - hh * f} x2={bx + w / 2 - 2} y2={y - hh * f + 3} stroke={vs(b, -0.07)} strokeWidth={2.4} strokeLinecap="round" />
						))}
					</>
				)}
				<ellipse cx={bx} cy={y - hh} rx={w / 2} ry={w * 0.2} fill={lod === 'far' ? sh : mixOk(b, tint(L.keyColor), 0.12)} />
				{lod === 'far' ? null : <ellipse cx={bx} cy={y - hh + w * 0.02} rx={w * 0.36} ry={w * 0.12} fill={shadowOf(b, tint(L.ambient), 0.55)} />}
			</g>,
		);
	}
	return <g>{out}</g>;
};

/** vase / barrel sponge with vertical ribs */
export const Vase: React.FC<{seed: string; x: number; y: number; h: number; base?: string; lod?: Lod}> = ({seed, x, y, h, base = 'ochre-2', lod = 'mid'}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`vase:${seed}`);
	const wTop = h * (0.42 + r() * 0.2);
	const wBot = h * (0.22 + r() * 0.1);
	const pts: Pt[] = [
		[x - wBot / 2, y],
		[x - wBot * 0.62, y - h * 0.35],
		[x - wTop / 2, y - h * 0.85],
		[x - wTop * 0.47, y - h],
		[x + wTop * 0.47, y - h],
		[x + wTop / 2, y - h * 0.85],
		[x + wBot * 0.62, y - h * 0.35],
		[x + wBot / 2, y],
	];
	const d = closedSpline(pts, 0.8);
	const b = tint(base);
	const id = clipId(`vase${seed}`);
	const ribs: React.ReactNode[] = [];
	if (lod !== 'far')
		for (let i = 1; i < 7; i++) {
			const f = i / 7 - 0.5;
			ribs.push(<path key={i} d={`M ${x + f * wBot} ${y} Q ${x + f * wBot * 1.3} ${y - h * 0.5} ${x + f * wTop} ${y - h}`} stroke={vs(b, i % 2 ? -0.08 : 0.07)} strokeWidth={3} fill="none" />);
		}
	return (
		<g>
			<defs>
				<clipPath id={id}>
					<path d={d} />
				</clipPath>
			</defs>
			<Stack d={d} cx={x} cy={y - h * 0.5} R={wTop * 0.45} base={base} lod={lod} />
			<g clipPath={`url(#${id})`}>{ribs}</g>
			<ellipse cx={x} cy={y - h} rx={wTop * 0.47} ry={wTop * 0.12} fill={mixOk(b, tint(L.keyColor), 0.1)} />
			<ellipse cx={x} cy={y - h + 2} rx={wTop * 0.36} ry={wTop * 0.075} fill={shadowOf(b, tint(L.ambient), 0.55)} />
		</g>
	);
};

/** ball sponge: a pored sphere */
export const Ball: React.FC<{seed: string; x: number; y: number; r: number; base?: string; lod?: Lod}> = ({seed, x, y, r: rad, base = 'amber-4', lod = 'mid'}) => {
	const L = useLight();
	const d = blob(`ball${seed}`, x, y - rad * 0.85, rad, rad * 0.88, {n: 9, jag: 0.1, flatBottom: true});
	if (lod === 'far') return <Stack d={d} cx={x} cy={y - rad * 0.85} R={rad} base={base} lod="far" />;
	const marks = placeMarks({seed: `ball${seed}`, d, key: L.key, rim: L.rim, R: rad, clusters: 3, kinds: {pores: 3, spots: 1}, size: Math.max(3, rad * 0.12), tone: 'dark'});
	return (
		<g>
			<Stack d={d} cx={x} cy={y - rad * 0.85} R={rad} base={base} />
			<SurfaceMarks marks={marks} base={base} />
		</g>
	);
};

/** soft (finger) coral: a cluster of thick swaying lobes with polyp dots */
export const Soft: React.FC<{seed: string; x: number; y: number; h: number; t: number; base?: string; lod?: Lod}> = ({seed, x, y, h, t, base = 'coral-4', lod = 'mid'}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`soft:${seed}`);
	const n = 4 + Math.floor(r() * 5);
	const b = tint(base);
	const sh = shadowOf(b, tint(L.ambient), 0.34);
	const k = L.key;
	const lobes: {pts: Pt[]; w: number}[] = [];
	for (let i = 0; i < n; i++) {
		const a0 = -90 + (i - (n - 1) / 2) * (60 / n) * 2 + (r() - 0.5) * 14;
		const len = h * (0.5 + r() * 0.55);
		const w = h * (0.13 + r() * 0.08);
		const pts: Pt[] = [[x + (i - (n - 1) / 2) * w * 0.4, y]];
		let ang = a0;
		for (let j = 0; j < 3; j++) {
			ang += chain(t, j, 3, {amp: 5, freq: 0.3, phase: rand(seed, i) * 6, lagPerSeg: 0.6});
			const [px, py] = pts[pts.length - 1];
			pts.push([px + Math.cos((ang * Math.PI) / 180) * (len / 3), py + Math.sin((ang * Math.PI) / 180) * (len / 3)]);
		}
		lobes.push({pts, w});
	}
	if (lod === 'far') return <g>{lobes.map((l, i) => <path key={i} d={openSpline(l.pts)} stroke={b} strokeWidth={l.w} strokeLinecap="round" fill="none" />)}</g>;
	return (
		<g>
			{lobes.map((l, i) => (
				<path key={`s${i}`} d={openSpline(l.pts)} stroke={sh} strokeWidth={l.w} strokeLinecap="round" fill="none" />
			))}
			{lobes.map((l, i) => (
				<path key={`b${i}`} d={openSpline(l.pts.map(([px, py]) => [px + k[0] * l.w * 0.14, py + k[1] * l.w * 0.14]))} stroke={b} strokeWidth={l.w * 0.7} strokeLinecap="round" fill="none" />
			))}
			{lobes.map((l, i) => (
				<path key={`h${i}`} d={openSpline(l.pts.slice(1).map(([px, py]) => [px + k[0] * l.w * 0.26, py + k[1] * l.w * 0.26]))} stroke={mixOk(b, tint(L.keyColor), 0.24)} strokeWidth={l.w * 0.22} strokeLinecap="round" fill="none" />
			))}
			{lobes.flatMap((l, i) =>
				[0.55, 0.88].map((f, j) => {
					const a = l.pts[Math.floor(f * (l.pts.length - 1))];
					const bb = l.pts[Math.min(l.pts.length - 1, Math.floor(f * (l.pts.length - 1)) + 1)];
					const px = a[0] + (bb[0] - a[0]) * 0.5 + (rand(seed, i * 9 + j) - 0.5) * l.w * 0.4;
					const py = a[1] + (bb[1] - a[1]) * 0.5;
					return <circle key={`p${i}-${j}`} cx={px} cy={py} r={Math.max(1.8, l.w * 0.09)} fill={vs(b, 0.09)} />;
				}),
			)}
		</g>
	);
};

// ---------------------------------------------------------------- kelp, grass, small life

/** kelp with seeded height, curvature, blade style and bladder frequency */
export const VarKelp: React.FC<{seed: string; x: number; y: number; h: number; t: number; lean?: number; bend?: number; style?: 'lance' | 'broad' | 'frond'; silhouette?: boolean; lod?: Lod; blade?: string}> = ({
	seed,
	x,
	y,
	h,
	t,
	lean = 0,
	bend = 0,
	style = 'lance',
	silhouette = false,
	lod = 'mid',
	blade,
}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`kelp:${seed}`);
	const segs = Math.max(5, Math.round(h / 90));
	const pts: Pt[] = [[x, y]];
	let ang = -90 + lean;
	let px = x;
	let py = y;
	const segL = h / segs;
	for (let i = 0; i < segs; i++) {
		ang += bend / segs + chain(t, i, segs, {amp: 6, freq: 1 / (5 + rand(seed, 0) * 3), phase: rand(seed, 1) * 6.28, lagPerSeg: 0.5, seed});
		px += Math.cos((ang * Math.PI) / 180) * segL;
		py += Math.sin((ang * Math.PI) / 180) * segL;
		pts.push([px, py]);
	}
	const flat = silhouette || lod === 'far';
	const stipe = tint(flat ? (silhouette ? 'ink-1' : 'kelp-1') : 'kelp-1');
	const bladeBase = tint(silhouette ? 'ink-1' : mixOk(blade ? c(blade) : c('kelp-3'), c('ochre-3'), r() * 0.35));
	const bladeSh = shadowOf(bladeBase, tint(L.ambient), 0.24);
	const bladeHi = mixOk(bladeBase, tint(L.keyColor), 0.2);
	const W = style === 'broad' ? 1.5 : style === 'frond' ? 0.7 : 1;
	const Lm = style === 'frond' ? 0.75 : style === 'broad' ? 1.15 : 1;
	const out: React.ReactNode[] = [];
	for (let i = 1; i < pts.length; i++) {
		if (r() < 0.3) continue; // gaps: not every node has a blade
		const [ax, ay] = pts[i - 1];
		const [bx, by] = pts[i];
		const a = Math.atan2(by - ay, bx - ax);
		const side = (i + (r() < 0.2 ? 1 : 0)) % 2 ? 1 : -1;
		const ba = a + side * (0.7 + r() * 0.4 + 0.2 * Math.sin(t * 0.9 + i + rand(seed, i) * 3));
		const len = (60 + r() * 70) * Lm * Math.min(1.3, h / 600 + 0.5);
		const wid = (14 + r() * 12) * W * Math.min(1.3, h / 600 + 0.5);
		const ux = Math.cos(ba);
		const uy = Math.sin(ba);
		const nx = -uy;
		const ny = ux;
		const tip: Pt = [ax + ux * len, ay + uy * len];
		const crv = (r() - 0.5) * 0.6;
		const leaf = `M ${ax} ${ay} C ${ax + ux * len * 0.3 + nx * wid * (1 + crv)} ${ay + uy * len * 0.3 + ny * wid * (1 + crv)} ${tip[0] + nx * wid * 0.35} ${tip[1] + ny * wid * 0.35} ${tip[0]} ${tip[1]} C ${tip[0] - nx * wid * 0.35} ${tip[1] - ny * wid * 0.35} ${ax + ux * len * 0.3 - nx * wid * (1 - crv)} ${ay + uy * len * 0.3 - ny * wid * (1 - crv)} ${ax} ${ay} Z`;
		const away = nx * L.key[0] + ny * L.key[1] < 0 ? 1 : -1;
		const half = `M ${ax} ${ay} C ${ax + ux * len * 0.3 + away * nx * wid * (1 + away * crv)} ${ay + uy * len * 0.3 + away * ny * wid * (1 + away * crv)} ${tip[0] + away * nx * wid * 0.35} ${tip[1] + away * ny * wid * 0.35} ${tip[0]} ${tip[1]} L ${ax} ${ay} Z`;
		out.push(
			<g key={i}>
				<path d={leaf} fill={bladeBase} />
				{flat ? null : (
					<>
						<path d={half} fill={bladeSh} />
						{r() < 0.35 ? <circle cx={ax + ux * 8} cy={ay + uy * 8} r={5 * W} fill={tint('ochre-3')} /> : null}
						<path d={`M ${ax + ux * len * 0.25 - away * nx * wid * 0.45} ${ay + uy * len * 0.25 - away * ny * wid * 0.45} Q ${ax + ux * len * 0.5 - away * nx * wid * 0.6} ${ay + uy * len * 0.5 - away * ny * wid * 0.6} ${ax + ux * len * 0.8 - away * nx * wid * 0.15} ${ay + uy * len * 0.8 - away * ny * wid * 0.15}`} stroke={bladeHi} strokeWidth={2.6} fill="none" strokeLinecap="round" />
					</>
				)}
			</g>,
		);
	}
	return (
		<g>
			<path d={taper(pts, 12 * Math.min(1.4, h / 700 + 0.4), 5)} fill={stipe} />
			{out}
		</g>
	);
};

export const Grass: React.FC<{seed: string; x: number; y: number; h: number; t: number; n?: number; lod?: Lod}> = ({seed, x, y, h, t, n = 8, lod = 'mid'}) => {
	const tint = useTint();
	return (
		<g>
			{Array.from({length: n}, (_, i) => {
				const bx = x + (i - n / 2) * 6 + (rand(seed, i + 40) - 0.5) * 6;
				const hh = h * (0.5 + rand(seed, i) * 0.6);
				const a = 8 * Math.sin(t * (1.2 + rand(seed, i + 9) * 0.6) + rand(seed, i + 3) * 6) + (i - n / 2) * 4;
				const pts: Pt[] = [];
				for (let j = 0; j <= 4; j++) {
					const s = j / 4;
					const rr = ((-90 + a * s * s) * Math.PI) / 180;
					pts.push([bx + Math.cos(rr) * hh * s, y + Math.sin(rr) * hh * s]);
				}
				return <path key={i} d={taper(pts, 6, 1.4)} fill={tint(lod === 'far' ? 'kelp-2' : i % 3 ? 'kelp-3' : 'kelp-4')} />;
			})}
		</g>
	);
};

export const Urchin: React.FC<{seed: string; x: number; y: number; r: number; t: number}> = ({seed, x, y, r: rad, t}) => {
	const tint = useTint();
	const L = useLight();
	const base = tint('coral-1');
	const lit = mixOk(base, tint(L.keyColor), 0.3);
	return (
		<g>
			{Array.from({length: 22}, (_, i) => {
				const a = Math.PI + (i / 21) * Math.PI + 0.05 * Math.sin(t * 1.3 + i);
				const len = rad * (1.4 + rand(seed, i) * 0.6);
				const isLit = Math.cos(a) * L.key[0] + Math.sin(a) * L.key[1] > 0.1;
				return <line key={i} x1={x} y1={y - rad * 0.3} x2={x + Math.cos(a) * len} y2={y - rad * 0.3 + Math.sin(a) * len} stroke={isLit ? lit : base} strokeWidth={2.2} strokeLinecap="round" />;
			})}
			<ellipse cx={x} cy={y - rad * 0.3} rx={rad} ry={rad * 0.72} fill={base} />
			<ellipse cx={x + L.key[0] * rad * 0.3} cy={y - rad * 0.3 + L.key[1] * rad * 0.25} rx={rad * 0.5} ry={rad * 0.3} fill={lit} />
		</g>
	);
};

export const Star: React.FC<{seed: string; x: number; y: number; s: number; base?: string}> = ({seed, x, y, s, base = 'coral-3'}) => {
	const tint = useTint();
	const L = useLight();
	const r = rng(`star:${seed}`);
	const rot = r() * 72;
	const b = tint(base);
	const arms = Array.from({length: 5}, (_, i) => {
		const a = ((rot + i * 72 - 90) * Math.PI) / 180;
		const len = s * (0.85 + r() * 0.3);
		const pts: Pt[] = [
			[x, y],
			[x + Math.cos(a) * len * 0.5 + Math.cos(a + 1.4) * s * 0.06, y + Math.sin(a) * len * 0.3],
			[x + Math.cos(a) * len, y + Math.sin(a) * len * 0.55],
		];
		return taper(pts, s * 0.42, s * 0.08);
	});
	return (
		<g>
			{arms.map((d, i) => (
				<path key={i} d={d} fill={shadowOf(b, tint(L.ambient), 0.3)} transform={`translate(1.5 1.5)`} />
			))}
			{arms.map((d, i) => (
				<path key={`b${i}`} d={d} fill={b} />
			))}
			{arms.map((_, i) => {
				const a = ((rot + i * 72 - 90) * Math.PI) / 180;
				return [0.3, 0.55, 0.78].map((f, j) => <circle key={`${i}-${j}`} cx={x + Math.cos(a) * s * f} cy={y + Math.sin(a) * s * f * 0.55} r={Math.max(1.5, s * 0.05)} fill={vs(b, 0.09)} />);
			})}
		</g>
	);
};

export const Shell: React.FC<{seed: string; x: number; y: number; s: number}> = ({seed, x, y, s}) => {
	const tint = useTint();
	const rot = (rand(seed, 1) - 0.5) * 40;
	const b = tint(rand(seed, 2) > 0.5 ? 'bone-0' : 'coral-4');
	return (
		<g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
			<path d="M -14 4 C -14 -10 -4 -16 6 -12 C 14 -8 16 2 10 6 Z" fill={b} />
			<path d="M -10 2 C -8 -6 -2 -10 4 -8 M -4 4 C -3 -4 2 -7 7 -4" stroke={vs(b, -0.09)} strokeWidth={1.8} fill="none" strokeLinecap="round" />
		</g>
	);
};

/** distant reef mound silhouette with knobs (far plane) */
export const FarMound: React.FC<{seed: string; x: number; y: number; w: number; h: number; base?: string}> = ({seed, x, y, w, h, base = 'tide-0'}) => {
	const r = rng(`mound:${seed}`);
	const pts: Pt[] = [[x - w / 2, y + 40]];
	const n = 9;
	for (let i = 0; i <= n; i++) {
		const f = i / n;
		const env = Math.sin(Math.PI * f);
		pts.push([x - w / 2 + w * f, y - h * env * (0.7 + r() * 0.5) + (r() - 0.5) * h * 0.15]);
	}
	pts.push([x + w / 2, y + 40]);
	return <Stack d={closedSpline(pts, 0.8)} cx={x} cy={y - h * 0.4} R={h * 0.6} base={base} lod="far" />;
};

