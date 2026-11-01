/**
 * Reef kit (house style, drawn fresh): the warm subject masses the open-water orca shot was missing
 * (NOTES gap 2: P5 hue families) and designed silhouettes instead of noise blobs (NOTES gap 3).
 *
 *   BrainCoral   flat-bottomed dome, meandering groove lines (shadow tone), polyp pores
 *   TubeSponge   3-6 capsules with open ring mouths (our ring motif), slow sway
 *   TableCoral   stacked plates on a stalk, lit top edge, polyp dots
 *   Staghorn     thick round-capped branches (constant-width strokes, KB §2), lit tips
 *   FanCoral     gorgonian with a translucent filled web behind the branches (not a bare tree)
 *   Spire        far-plane rock pillar / arch silhouette built from stacked rounded lobes
 *
 * Every piece goes through <Shaded> (support LOD on the mid plane) so it agrees with the scene key (J3).
 */
import React from 'react';
import {c, mixOk, shadowOf, shiftL} from '../lib/color';
import {closedSpline, openSpline} from '../lib/geom';
import {useLight, useTint} from '../lib/light';
import {noise1, rand, rng} from '../lib/rng';
import {Shaded} from '../shade/Shaded';
import {sway} from '../motion/motion';

type P = [number, number];

export const BrainCoral: React.FC<{id: string; x: number; y: number; r: number; base?: string; lod?: 'hero' | 'support'}> = ({id, x, y, r, base = 'ochre-3', lod = 'support'}) => {
	const tint = useTint();
	const L = useLight();
	const h = r * 0.78;
	const d = `M ${x - r} ${y} C ${x - r * 1.02} ${y - h * 0.8} ${x - r * 0.6} ${y - h * 1.1} ${x} ${y - h * 1.08} C ${x + r * 0.6} ${y - h * 1.1} ${x + r * 1.02} ${y - h * 0.8} ${x + r} ${y} C ${x + r * 0.5} ${y + r * 0.08} ${x - r * 0.5} ${y + r * 0.08} ${x - r} ${y} Z`;
	const groove = shadowOf(tint(base), tint(L.ambient), 0.3);
	const ridge = mixOk(tint(base), tint(L.keyColor), 0.25);
	const rr = rng(`${id}g`);
	const lines: React.ReactNode[] = [];
	for (let i = 0; i < 7; i++) {
		const yy = y - h * (0.12 + i * 0.13);
		const half = Math.sqrt(Math.max(0, 1 - ((y - yy) / (h * 1.08)) ** 2)) * r * 0.92;
		const pts: P[] = [];
		for (let j = 0; j <= 8; j++) {
			const xx = x - half + (2 * half * j) / 8;
			pts.push([xx, yy + Math.sin(j * 1.9 + rr() * 2) * r * 0.045]);
		}
		lines.push(<path key={i} d={openSpline(pts)} stroke={groove} strokeWidth={Math.max(2.4, r * 0.035)} fill="none" strokeLinecap="round" />);
		lines.push(
			<path key={`h${i}`} d={openSpline(pts.map(([a, b]) => [a, b - r * 0.03] as P))} stroke={ridge} strokeWidth={Math.max(1.6, r * 0.018)} fill="none" strokeLinecap="round" opacity={0.6} />,
		);
	}
	return (
		<Shaded
			id={id}
			R={r * 0.8}
			lod={lod}
			layers={{marks: true}}
			parts={[{d, base, marks: [{kind: 'pore', n: 14, size: r * 0.09, dL: -0.09}]}]}
			over={<g>{lines}</g>}
			cast={{y: y + 4, lift: 0, spread: 1.05, opacity: 0.6}}
		/>
	);
};

export const TubeSponge: React.FC<{id: string; x: number; y: number; h: number; t: number; n?: number; base?: string}> = ({id, x, y, h, t, n = 4, base = 'coral-2'}) => {
	const tint = useTint();
	const L = useLight();
	const tubes: {d: string; mouth: [number, number, number]}[] = [];
	for (let i = 0; i < n; i++) {
		const w = h * (0.17 + rand(id, i) * 0.06);
		const hh = h * (0.55 + rand(id, i + 10) * 0.45);
		const bx = x + (i - (n - 1) / 2) * w * 1.15;
		const a = ((sway(t, `${id}${i}`, 3, 5 + i) + (i - (n - 1) / 2) * 7) * Math.PI) / 180;
		const tx = bx + Math.sin(a) * hh;
		const ty = y - Math.cos(a) * hh;
		const nx = Math.cos(a) * w * 0.5;
		const ny = Math.sin(a) * w * 0.5;
		const lip = w * 0.62;
		tubes.push({
			d: `M ${bx - w * 0.5} ${y} L ${tx - nx * 1.2} ${ty - ny * 1.2} C ${tx - lip} ${ty - w * 0.25} ${tx + lip} ${ty - w * 0.25} ${tx + nx * 1.2} ${ty + ny * 1.2} L ${bx + w * 0.5} ${y} Z`,
			mouth: [tx, ty - w * 0.06, w * 0.5],
		});
	}
	const inner = shadowOf(tint(base), tint(L.ambient), 0.55);
	const lipCol = mixOk(tint(base), tint(L.keyColor), 0.3);
	return (
		<Shaded
			id={id}
			R={h * 0.25}
			lod="support"
			layers={{marks: true}}
			parts={tubes.map((q, i) => ({d: q.d, base: i % 2 ? base : shiftL(c(base), 0.05), marks: [{kind: 'ring' as const, n: 2, size: h * 0.05, dL: -0.08}]}))}
			top={
				<g>
					{tubes.map((q, i) => (
						<g key={i}>
							<ellipse cx={q.mouth[0]} cy={q.mouth[1]} rx={q.mouth[2] * 1.16} ry={q.mouth[2] * 0.42} fill={lipCol} />
							<ellipse cx={q.mouth[0]} cy={q.mouth[1] + 1} rx={q.mouth[2] * 0.8} ry={q.mouth[2] * 0.26} fill={inner} />
						</g>
					))}
				</g>
			}
		/>
	);
};

export const TableCoral: React.FC<{id: string; x: number; y: number; w: number; base?: string}> = ({id, x, y, w, base = 'amber-3'}) => {
	const tint = useTint();
	const L = useLight();
	const stalkH = w * 0.32;
	const plates: string[] = [];
	const tiers = [
		[0, 1, 0.13],
		[-0.22, 0.62, 0.1],
	];
	for (const [dy, sc, th] of tiers) {
		const py = y - stalkH - dy * w;
		const pw = (w * sc) / 2;
		plates.push(
			`M ${x - pw} ${py} C ${x - pw * 0.9} ${py - w * th} ${x + pw * 0.9} ${py - w * th} ${x + pw} ${py} C ${x + pw * 0.7} ${py + w * 0.06} ${x - pw * 0.7} ${py + w * 0.06} ${x - pw} ${py} Z`,
		);
	}
	const stalk = `M ${x - w * 0.06} ${y} C ${x - w * 0.05} ${y - stalkH * 0.6} ${x - w * 0.09} ${y - stalkH} ${x - w * 0.16} ${y - stalkH} L ${x + w * 0.16} ${y - stalkH} C ${x + w * 0.09} ${y - stalkH} ${x + w * 0.05} ${y - stalkH * 0.6} ${x + w * 0.06} ${y} Z`;
	const lit = mixOk(tint(base), tint(L.keyColor), 0.35);
	return (
		<Shaded
			id={id}
			R={w * 0.18}
			lod="support"
			layers={{marks: true}}
			parts={[
				{d: stalk, base: shiftL(c(base), -0.1)},
				...plates.map((d) => ({d, base, marks: [{kind: 'pore' as const, n: 16, size: w * 0.035, dL: -0.1}]})),
			]}
			top={
				<g>
					{tiers.map(([dy, sc], i) => {
						const py = y - stalkH - dy * w;
						const pw = (w * sc) / 2;
						return <path key={i} d={`M ${x - pw * 0.86} ${py - w * 0.035} C ${x - pw * 0.5} ${py - w * 0.1} ${x + pw * 0.3} ${py - w * 0.1} ${x + pw * 0.6} ${py - w * 0.06}`} stroke={lit} strokeWidth={Math.max(2.5, w * 0.014)} fill="none" strokeLinecap="round" />;
					})}
				</g>
			}
		/>
	);
};

export const Staghorn: React.FC<{id: string; x: number; y: number; h: number; t: number; base?: string; depth?: number}> = ({id, x, y, h, t, base = 'coral-3', depth = 3}) => {
	const tint = useTint();
	const L = useLight();
	const segs: {a: P; b: P; w: number}[] = [];
	const tips: P[] = [];
	let k = 0;
	const grow = (px: number, py: number, ang: number, len: number, w: number, dpt: number) => {
		const a = ang + sway(t, `${id}${k}`, 1.5 + dpt, 6 + dpt);
		const r = (a * Math.PI) / 180;
		const ex = px + Math.cos(r) * len;
		const ey = py + Math.sin(r) * len;
		segs.push({a: [px, py], b: [ex, ey], w});
		const kk = k++;
		if (dpt >= depth) {
			tips.push([ex, ey]);
			return;
		}
		const sp = 24 + rand(id, kk) * 14;
		grow(ex, ey, a - sp, len * 0.78, w * 0.82, dpt + 1);
		grow(ex, ey, a + sp * 0.8, len * 0.72, w * 0.82, dpt + 1);
	};
	grow(x - h * 0.08, y, -104, h * 0.36, h * 0.14, 0);
	grow(x + h * 0.08, y, -72, h * 0.32, h * 0.13, 1);
	const tip = tint('coral-4');
	const allPts = segs.flatMap((s) => [s.a, s.b]);
	const xs = allPts.map((p) => p[0]);
	const ys = allPts.map((p) => p[1]);
	const box: [number, number, number, number] = [Math.min(...xs), Math.min(...ys), Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys)];
	return (
		<Shaded
			id={id}
			box={box}
			R={h * 0.09}
			core={0.5}
			lod="support"
			parts={[
				{
					el: (f) => (
						<g>
							{segs.map((s, i) => (
								<line key={i} x1={s.a[0]} y1={s.a[1]} x2={s.b[0]} y2={s.b[1]} stroke={f} strokeWidth={s.w} strokeLinecap="round" />
							))}
						</g>
					),
					base,
				},
			]}
			top={
				<g>
					{tips.map(([tx, ty], i) => (
						<circle key={i} cx={tx} cy={ty} r={h * 0.035} fill={tip} />
					))}
					{tips.map(([tx, ty], i) => (
						<circle key={`g${i}`} cx={tx + L.key[0] * h * 0.012} cy={ty + L.key[1] * h * 0.012} r={h * 0.012} fill={mixOk(tip, tint('bone-2'), 0.5)} />
					))}
				</g>
			}
		/>
	);
};

export const FanCoral: React.FC<{id: string; x: number; y: number; h: number; t: number; base?: string}> = ({id, x, y, h, t, base = 'coral-3'}) => {
	const tint = useTint();
	const L = useLight();
	const b = tint(base);
	const lit = mixOk(b, tint(L.keyColor), 0.25);
	const dark = shadowOf(b, tint(L.ambient), 0.3);
	const lines: React.ReactNode[] = [];
	const outline: P[] = [];
	let n = 0;
	const sw = sway(t, id, 2.5, 7);
	const grow = (px: number, py: number, ang: number, len: number, w: number, dpt: number) => {
		if (dpt > 5) {
			outline.push([px, py]);
			return;
		}
		const a = ang + sw * (dpt / 5);
		const r = (a * Math.PI) / 180;
		const ex = px + Math.cos(r) * len;
		const ey = py + Math.sin(r) * len;
		const k = n++;
		lines.push(<line key={k} x1={px} y1={py} x2={ex} y2={ey} stroke={dpt < 2 ? dark : Math.cos(r) * L.key[0] + Math.sin(r) * L.key[1] > 0 ? lit : b} strokeWidth={w} strokeLinecap="round" />);
		const spread = 13 + rand(id, k) * 10;
		const cl = (v: number) => Math.max(-168, Math.min(-12, v));
		grow(ex, ey, cl(a - spread), len * 0.8, w * 0.74, dpt + 1);
		grow(ex, ey, cl(a + spread), len * 0.8, w * 0.74, dpt + 1);
	};
	grow(x, y, -90, h * 0.22, Math.max(5, h * 0.05), 0);
	outline.sort((p, q) => Math.atan2(p[1] - y, p[0] - x) - Math.atan2(q[1] - y, q[0] - x));
	const web = outline.length > 3 ? closedSpline([[x, y - h * 0.15], ...outline], 0.8) : '';
	return (
		<g>
			{web ? <path d={web} fill={mixOk(b, tint(L.ambient), 0.2)} opacity={0.42} /> : null}
			{web ? <path d={web} fill="none" stroke={lit} strokeWidth={2.5} opacity={0.35} /> : null}
			{lines}
		</g>
	);
};

/** Far-plane pillar or arch built from stacked rounded lobes: designed silhouette, not a noise ridge. */
export const Spire: React.FC<{seed: string; x: number; y: number; w: number; h: number; color?: string; arch?: boolean}> = ({seed, x, y, w, h, color = 'ink-3', arch = false}) => {
	const tint = useTint();
	const r = rng(seed);
	const lobes: React.ReactNode[] = [];
	const n = 5;
	let cy = y;
	let cw = w;
	for (let i = 0; i < n; i++) {
		const lh = (h / n) * (0.9 + r() * 0.4);
		const cx = x + (r() - 0.5) * w * 0.25;
		const pts: P[] = [
			[cx - cw * 0.5, cy + 4],
			[cx - cw * (0.52 + r() * 0.08), cy - lh * 0.55],
			[cx - cw * (0.32 + r() * 0.08), cy - lh * 1.02],
			[cx + cw * (0.3 + r() * 0.08), cy - lh * 1.04],
			[cx + cw * (0.5 + r() * 0.08), cy - lh * 0.5],
			[cx + cw * 0.5, cy + 4],
		];
		lobes.push(<path key={i} d={closedSpline(pts, 0.9)} fill={tint(color)} />);
		cy -= lh * 0.82;
		cw *= 0.8 + r() * 0.1;
	}
	return (
		<g>
			{lobes}
			{arch ? (
				<path
					d={`M ${x + w * 0.3} ${y - h * 0.35} C ${x + w * 0.9} ${y - h * 0.75} ${x + w * 1.9} ${y - h * 0.7} ${x + w * 2.2} ${y + 4} L ${x + w * 1.75} ${y + 4} C ${x + w * 1.6} ${y - h * 0.4} ${x + w * 1.0} ${y - h * 0.45} ${x + w * 0.4} ${y - h * 0.12} Z`}
					fill={tint(color)}
				/>
			) : null}
			{/* tone-on-tone ledge marks (≤ 6 % ΔL), far plane keeps no highlights */}
			{Array.from({length: 4}, (_, i) => {
				const yy = y - h * (0.15 + i * 0.2);
				return <path key={i} d={`M ${x - w * 0.25} ${yy} Q ${x} ${yy - 6} ${x + w * 0.22} ${yy + 2}`} stroke={tint(shiftL(c(color), 0.04))} strokeWidth={4} fill="none" strokeLinecap="round" />;
			})}
		</g>
	);
};

/** A low reef shelf silhouette (mid plane backing) so corals sit on something, with a lit top lip. */
export const ReefShelf: React.FC<{seed: string; y: number; h: number; color?: string}> = ({seed, y, h, color}) => {
	const tint = useTint();
	const L = useLight();
	const base = color ?? mixOk(c('ochre-1'), c('tide-0'), 0.45);
	const pts: P[] = [];
	for (let i = 0; i <= 14; i++) {
		const xx = -320 + (1720 * i) / 14;
		pts.push([xx, y - h * (0.45 + 0.55 * Math.abs(noise1(seed, i * 0.7))) + (i % 3 === 0 ? h * 0.25 : 0)]);
	}
	const top = openSpline(pts, 0.8);
	return (
		<g>
			<path d={`${top} L 1400 ${y + 900} L -320 ${y + 900} Z`} fill={tint(base)} />
			<path d={openSpline(pts.map(([a, b]) => [a, b + 10] as P), 0.8)} stroke={mixOk(tint(base), tint(L.keyColor), 0.3)} strokeWidth={6} fill="none" strokeLinecap="round" opacity={0.7} />
			<path d={openSpline(pts.map(([a, b]) => [a, b + 60] as P), 0.8)} stroke={shadowOf(tint(base), tint(L.ambient), 0.25)} strokeWidth={26} fill="none" strokeLinecap="round" opacity={0.5} />
		</g>
	);
};
