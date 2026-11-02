/**
 * FORK of experiments/asset-gen/orca-b/OrcaB.tsx (read-only there), changed for the detail-pass orca opening:
 *   - eye: the lid is clipped to the eye disc and the eye sits in a skin socket, so at 2x push-in it no longer
 *     shows a square skin-coloured lid block over the eye-patch edge
 *   - L8 lit-side marks at a lower value step (+0.13 / +0.20 L instead of +0.34 / +0.5), i.e. Kurzgesagt-like
 *     low-contrast marks: same 187 marks, fewer of them read as bright specks (D3) or Canny edges (D4)
 * Geometry is still asset-gen's orca_geom.json.
 *
 * Path B: structured redraw of the Codex reference orca (gen/a_orca_side_v2.png) as a layered, rigged component.
 *
 * Geometry comes from orca_geom.json (scripts/extract_orca.py): silhouette parts cut along hand-placed lines,
 * bone patches, saddle, and every surface mark measured off the reference (position, length, angle, size).
 * Nothing about light is copied from the image: every part is re-shaded here from ONE light vector with the
 * STYLE_BIBLE §4.3 stack (L0 form gradient, L1 hard core shadow, L3 deep occlusion, L4 bounce, L5 highlight +
 * warm edge, L6 glints, L7 cool rim, L8 micro-marks), so the light can move and the parts can rotate.
 *
 * Named, separately animatable parts (back to front):
 *   pecFar  · fluke · dorsal · mouth (interior + teeth, only while open) · body (upper) · jaw · eye · pecNear
 *
 * Local space = reference image pixels (1536 × 1024), snout at x≈1505, fluke tip at x≈23. Pure SVG + React,
 * no Remotion dependency: drive it with `t` (seconds) and the pose props.
 */
import React from 'react';
import {c, mixOk, shadowOf, shiftL} from '../../../kurz-style/engine/src/lib/color';
import geom from '../../../asset-gen/orca-b/orca_geom.json';

type Pt = [number, number];
type Mark = {kind: 'scar' | 'dot'; part: string; x: number; y: number; lum: number; len?: number; w?: number; ang?: number; r?: number};
type Patch = {name: string; d: string; cx: number; cy: number; area: number};

const G = geom as unknown as {
	parts: Record<'body' | 'upper' | 'jaw' | 'dorsal' | 'fluke' | 'pecNear' | 'pecFar' | 'saddle', string>;
	pivots: Record<'dorsal' | 'fluke' | 'pecNear' | 'pecFar' | 'jaw' | 'bodyHead' | 'bodyTail', Pt>;
	patches: Patch[];
	eye: {cx: number; cy: number; r: number};
	marks: Mark[];
};

export type Light = {key: Pt; rim: Pt; keyColor: string; rimColor: string; ambient: string; bounce: string};
export const LANTERN: Light = {key: [-0.45, -0.89], rim: [0.55, 0.83], keyColor: 'amber-4', rimColor: 'tide-4', ambient: 'ink-2', bounce: 'tide-1'};

// ---------- geometry helpers ----------
const PAIR = /(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g;
const warpPath = (d: string, f: (x: number, y: number) => Pt) =>
	d.replace(PAIR, (_, xs, ys) => {
		const [x, y] = f(+xs, +ys);
		return `${x.toFixed(1)} ${y.toFixed(1)}`;
	});
const rotV = ([x, y]: Pt, deg: number): Pt => {
	const a = (deg * Math.PI) / 180;
	return [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];
};
const norm = ([x, y]: Pt): Pt => {
	const l = Math.hypot(x, y) || 1;
	return [x / l, y / l];
};

/** whale swim: vertical travelling wave, amplitude grows toward the tail (head is stable) */
const makeBend = (t: number, amp: number, freq: number) => {
	const [hx] = G.pivots.bodyHead;
	const [tx] = G.pivots.bodyTail;
	return (x: number, y: number): Pt => {
		const s = Math.min(1, Math.max(0, (hx - x) / (hx - tx)));
		const dy = amp * (s * s * 1.0 + 0.04) * Math.sin(2 * Math.PI * freq * t - 2.4 * s);
		return [x, y + dy];
	};
};

// ---------- the shading stack for one part ----------
type Decal = {d: string; base: string; opacity?: number; shadowT?: number};
type PartProps = {
	id: string;
	d: string;
	base: string;
	R: number;
	L: Light;
	/** rotation of the enclosing group, so the light stays in screen space */
	rot?: number;
	decals?: Decal[];
	marks?: Mark[];
	glints?: {cx: number; cy: number; rx: number; ry: number; rot: number; o: number}[];
	core?: number;
	rimW?: number;
	/** extra content drawn inside the clip after shading (creases, occlusion from other parts) */
	over?: React.ReactNode;
	lod?: 'hero' | 'support';
};

const tr = ([x, y]: Pt, s: number) => `translate(${(x * s).toFixed(2)} ${(y * s).toFixed(2)})`;

export const ShadedPart: React.FC<PartProps> = ({id, d, base, R, L, rot = 0, decals = [], marks = [], glints = [], core = 0.38, rimW = 5, over, lod = 'hero'}) => {
	const k = norm(rotV(L.key, -rot));
	const r = norm(rotV(L.rim, -rot));
	const amb = c(L.ambient);
	const key = c(L.keyColor);
	const sh = (b: string, t = 0.38) => shadowOf(c(b), amb, t);
	const hiC = (b: string) => mixOk(c(b), key, 0.22);
	const crescent = (mid: string, dir: Pt, dist: number) => (
		<mask id={mid} maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="6000" height="6000">
			<path d={d} fill="white" />
			<path d={d} fill="black" transform={tr(dir, -dist)} />
		</mask>
	);
	const all = [{d, base, opacity: 1, shadowT: 0.38}, ...decals];
	return (
		<g>
			<defs>
				<clipPath id={`${id}-clip`}>
					<path d={d} />
				</clipPath>
				{crescent(`${id}-core`, [-k[0], -k[1]], core * R)}
				{crescent(`${id}-occ`, [-k[0], -k[1]], 0.1 * R)}
				{crescent(`${id}-hi`, k, 0.16 * R)}
				{crescent(`${id}-edge`, k, Math.max(2.5, Math.min(6, 0.03 * R)))}
				{crescent(`${id}-rim`, r, rimW)}
				{crescent(`${id}-bnc`, [0, 1], 0.14 * R)}
				<mask id={`${id}-lit`} maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="6000" height="6000">
					<path d={d} fill="white" transform={tr(k, core * R)} />
				</mask>
				<radialGradient id={`${id}-form`} cx={0.5 + 0.25 * k[0]} cy={0.5 + 0.25 * k[1]} r="0.75">
					<stop offset="0" stopColor={mixOk(c(base), key, 0.06)} />
					<stop offset="1" stopColor={mixOk(c(base), amb, 0.08)} />
				</radialGradient>
			</defs>
			<g clipPath={`url(#${id}-clip)`}>
				{/* L0 base + form gradient, then flat decals (bone patches, saddle) */}
				<path d={d} fill={`url(#${id}-form)`} />
				{decals.map((p, i) => (
					<path key={i} d={p.d} fill={c(p.base)} opacity={p.opacity ?? 1} />
				))}
				{/* L5 highlight plane + warm lit edge (group-aware: every colour gets its own lit tone) */}
				<g mask={`url(#${id}-hi)`}>
					{all.map((p, i) => (
						<path key={i} d={p.d} fill={hiC(p.base)} opacity={(p.opacity ?? 1) * (lod === 'hero' ? 0.9 : 0.7)} />
					))}
				</g>
				<g mask={`url(#${id}-edge)`}>
					<path d={d} fill={mixOk(c(base), key, 0.78)} opacity={0.95} />
				</g>
				{/* L1 hard core shadow: one terminator for the whole group, per-colour shadow tone */}
				<g mask={`url(#${id}-core)`}>
					{all.map((p, i) => (
						<path key={i} d={p.d} fill={sh(p.base, p.shadowT ?? 0.38)} opacity={p.opacity ?? 1} />
					))}
				</g>
				{lod === 'hero' ? (
					<>
						{/* L3 deep occlusion along the far shadow edge */}
						<g mask={`url(#${id}-occ)`}>
							{all.map((p, i) => (
								<path key={i} d={p.d} fill={sh(p.base, 0.6)} opacity={p.opacity ?? 1} />
							))}
						</g>
						{/* L4 bounce from the water below */}
						<path d={d} fill={mixOk(c(base), c(L.bounce), 0.3)} opacity={0.16} mask={`url(#${id}-bnc)`} />
					</>
				) : null}
				{/* L8 micro-marks: lit-side tone, then shadow-side tone */}
				{marks.length ? <MarkSet id={`${id}-mk`} marks={marks} base={base} L={L} litMask={`${id}-lit`} /> : null}
				{over}
				{/* L6 specular glints */}
				{glints.map((g, i) => (
					<ellipse key={i} cx={g.cx} cy={g.cy} rx={g.rx} ry={g.ry} transform={`rotate(${g.rot} ${g.cx} ${g.cy})`} fill={c('bone-2')} opacity={g.o} />
				))}
				{/* L7 cool rim from behind */}
				<path d={d} fill={c(L.rimColor)} opacity={0.95} mask={`url(#${id}-rim)`} />
			</g>
		</g>
	);
};

const MarkSet: React.FC<{id: string; marks: Mark[]; base: string; L: Light; litMask: string}> = ({marks, base, L, litMask}) => {
	const lit = mixOk(shiftL(c(base), 0.13), c('tide-5'), 0.14);
	const litScar = mixOk(shiftL(c(base), 0.2), c('tide-5'), 0.18);
	const dark = shiftL(shadowOf(c(base), c(L.ambient), 0.38), 0.16);
	const draw = (scar: string, dot: string, op: number) =>
		marks.map((m, i) => {
			if (m.kind === 'scar') {
				const a = ((m.ang ?? 0) * Math.PI) / 180;
				const h = (m.len ?? 10) / 2;
				const dx = Math.cos(a) * h;
				const dy = Math.sin(a) * h;
				const w = Math.max(2.2, Math.min(4.2, (m.w ?? 2) * 1.25));
				// tapered scar: a thin lens instead of a constant stroke
				const nx = (-dy / h) * w * 0.5;
				const ny = (dx / h) * w * 0.5;
				const d = `M ${(m.x - dx).toFixed(1)} ${(m.y - dy).toFixed(1)} Q ${(m.x + nx).toFixed(1)} ${(m.y + ny).toFixed(1)} ${(m.x + dx).toFixed(1)} ${(m.y + dy).toFixed(1)} Q ${(m.x - nx).toFixed(1)} ${(m.y - ny).toFixed(1)} ${(m.x - dx).toFixed(1)} ${(m.y - dy).toFixed(1)} Z`;
				return <path key={i} d={d} fill={scar} opacity={op} />;
			}
			const rr = Math.max(1.8, Math.min(5, (m.r ?? 2) * 1.1));
			return rr > 3.2 ? (
				// our ring motif for the larger spots: outer ring + inner disc
				<g key={i} opacity={op}>
					<circle cx={m.x} cy={m.y} r={rr} fill="none" stroke={dot} strokeWidth={1.3} />
					<circle cx={m.x} cy={m.y} r={rr * 0.38} fill={dot} />
				</g>
			) : (
				<circle key={i} cx={m.x} cy={m.y} r={rr} fill={dot} opacity={op} />
			);
		});
	return (
		<g>
			<g opacity={0.95}>{draw(dark, dark, 0.9)}</g>
			<g mask={`url(#${litMask})`}>{draw(litScar, lit, 0.85)}</g>
		</g>
	);
};

// ---------- the orca ----------
export type OrcaBProps = {
	id?: string;
	t?: number;
	/** tail-beat amplitude in px at the fluke */
	amp?: number;
	freq?: number;
	/** 0 closed .. 1 open (26°) */
	jaw?: number;
	/** extra pectoral angle (deg), added to the follow-through */
	pec?: number;
	/** 0 open .. 1 shut */
	blink?: number;
	light?: Light;
	/** turn off L8 marks (for the ladder) */
	marks?: boolean;
	skin?: string;
};

const JAW_MAX = 26;
const MOUTH_UP: Pt[] = [
	[1300, 528],
	[1340, 522],
	[1380, 519],
	[1420, 518],
	[1460, 517],
	[1490, 516],
	[1506, 514],
];

const marksFor = (part: string, f: (x: number, y: number) => Pt) =>
	G.marks
		.filter((m) => m.part === part)
		.map((m) => {
			const [x, y] = f(m.x, m.y);
			return {...m, x, y};
		});

export const OrcaB: React.FC<OrcaBProps> = ({id = 'orb', t = 0, amp = 22, freq = 0.5, jaw = 0, pec = 0, blink = 0, light = LANTERN, marks = true, skin = 'ink-1'}) => {
	const L = light;
	const bend = makeBend(t, amp, freq);
	const w = (d: string) => warpPath(d, bend);
	const ph = 2 * Math.PI * freq * t;
	const P = G.pivots;
	const wp = (p: Pt) => bend(p[0], p[1]);
	// secondary motion, all phase-lagged off the body wave
	const flukePitch = 9 * Math.sin(ph - 2.9);
	const dorsalSway = 1.6 * Math.sin(ph - 1.2);
	const pecNearRot = 7 * Math.sin(ph - 0.9) + pec;
	const pecFarRot = -5 * Math.sin(ph - 1.1) + pec * 0.7;
	const jawRot = JAW_MAX * jaw;
	const mk = (part: string) => (marks ? marksFor(part, bend) : []);
	const bone = 'bone-1';
	const boneWarm = mixOk(c('bone-1'), c('amber-4'), 0.12);
	const patch = (n: string) => G.patches.filter((p) => p.name === n).map((p) => w(p.d));
	const saddle = {d: w(G.parts.saddle), base: mixOk(c('bone-0'), c('tide-1'), 0.5), opacity: 0.75, shadowT: 0.3};
	const rot = (deg: number, p: Pt) => `rotate(${deg.toFixed(2)} ${p[0].toFixed(1)} ${p[1].toFixed(1)})`;
	const open = jaw > 0.002;

	// mouth interior + teeth (behind body and jaw)
	const hinge = wp(P.jaw);
	const rj = (q: Pt): Pt => {
		const v = rotV([q[0] - hinge[0], q[1] - hinge[1]], jawRot);
		return [hinge[0] + v[0], hinge[1] + v[1]];
	};
	const up = MOUTH_UP.map((q) => bend(q[0], q[1]));
	const lo = up.map(rj);
	const teeth = (pts: Pt[], dir: 1 | -1, key: string) => {
		const out: React.ReactNode[] = [];
		for (let i = 0; i < 10; i++) {
			const s = 0.12 + i * 0.085;
			const f = s * (pts.length - 1);
			const j = Math.min(pts.length - 2, Math.floor(f));
			const u = f - j;
			const x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * u;
			const y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * u;
			const [tx, ty] = norm([pts[j + 1][0] - pts[j][0], pts[j + 1][1] - pts[j][1]]);
			const nx = -ty * dir;
			const ny = tx * dir;
			const hgt = (12 + 3 * Math.sin(i * 1.9)) * Math.min(1, jaw * 2);
			const wd = 5.5;
			const tip: Pt = [x + nx * hgt, y + ny * hgt];
			out.push(
				<g key={key + i}>
					<path d={`M ${x - tx * wd} ${y - ty * wd} Q ${tip[0] - tx * 2} ${tip[1] - ty * 2} ${tip[0]} ${tip[1]} Q ${x + tx * wd * 0.5} ${y + ty * wd * 0.5} ${x + tx * wd} ${y + ty * wd} Z`} fill={c('bone-1')} />
					<path d={`M ${x} ${y} Q ${tip[0] + tx} ${tip[1] + ty} ${tip[0]} ${tip[1]} Q ${x + tx * wd * 0.5} ${y + ty * wd * 0.5} ${x + tx * wd} ${y + ty * wd} Z`} fill={shadowOf(c('bone-1'), c(L.ambient), 0.32)} />
				</g>,
			);
		}
		return out;
	};
	const mouth = open ? (
		<g>
			<path d={`M ${up.map((q) => q.join(' ')).join(' L ')} L ${lo.slice().reverse().map((q) => q.join(' ')).join(' L ')} Z`} fill={shadowOf(c('coral-1'), c(L.ambient), 0.45)} />
			<ellipse cx={(up[2][0] + lo[3][0]) / 2 + 20} cy={lo[3][1] - 8} rx={70} ry={10 + 8 * jaw} fill={shadowOf(c('coral-2'), c(L.ambient), 0.15)} transform={rot(jawRot * 0.7, lo[3])} />
			{teeth(up, 1, 'u')}
			{teeth(lo, -1, 'l')}
		</g>
	) : null;

	const bodyD = w(open ? G.parts.upper : G.parts.body);
	const jawD = w(G.parts.jaw);
	const eye = wp([G.eye.cx, G.eye.cy]);
	const pecNearD = w(G.parts.pecNear);
	const pnPivot = wp(P.pecNear);

	// creases + blowhole + mouth line (internal detail lines in ramp tones, never black)
	const ink0 = c('ink-0');
	const creases = (
		<g fill="none" strokeLinecap="round" stroke={ink0}>
			<path d={w('M 1160 500 C 1186 520 1200 540 1204 562')} strokeWidth={2.4} opacity={0.5} />
			<path d={w('M 1176 494 C 1206 512 1226 532 1234 556')} strokeWidth={2} opacity={0.4} />
			<path d={w('M 1318 470 C 1336 462 1360 462 1378 470')} strokeWidth={2} opacity={0.5} />
			<path d={w('M 1190 590 C 1206 606 1210 626 1204 646')} strokeWidth={2.2} opacity={0.45} />
			<path d={w('M 1220 352 Q 1236 344 1252 352')} strokeWidth={3.2} opacity={0.9} />
			{/* closed mouth reads from the skin/bone boundary itself; no stroke (outline response stays low) */}
		</g>
	);
	// soft occlusion the near flipper throws onto the body (offset copy, no filter)
	const pecOcc = (
		<g transform={rot(pecNearRot, pnPivot)}>
			<path d={pecNearD} fill={ink0} opacity={0.32} transform="translate(14 16)" />
			<path d={pecNearD} fill={ink0} opacity={0.18} transform="translate(26 30)" />
		</g>
	);

	return (
		<g>
			{/* far flipper: behind the body, supporting-level shading, a step darker */}
			<g transform={rot(pecFarRot, wp(P.pecFar))}>
				<ShadedPart id={`${id}-pf`} d={w(G.parts.pecFar)} base={shadowOf(c(skin), c(L.ambient), 0.2)} R={60} L={L} rot={pecFarRot} lod="support" marks={mk('pecFar')} rimW={6} />
			</g>
			<g transform={rot(flukePitch, wp(P.fluke))}>
				<ShadedPart id={`${id}-fl`} d={w(G.parts.fluke)} base={skin} R={28} L={L} rot={flukePitch} marks={mk('fluke')} rimW={4} core={0.42}
					decals={[{d: w('M 30 584 C 90 592 170 588 250 576 L 250 600 L 30 600 Z'), base: bone, opacity: 0.85}]} />
			</g>
			<g transform={rot(dorsalSway, wp(P.dorsal))}>
				<ShadedPart id={`${id}-do`} d={w(G.parts.dorsal)} base={skin} R={95} L={L} rot={dorsalSway} marks={mk('dorsal')} core={0.4}
					glints={[{cx: 806, cy: 110, rx: 30, ry: 3, rot: 62, o: 0.35}]} />
			</g>
			{mouth}
			<ShadedPart
				id={`${id}-bd`}
				d={bodyD}
				base={skin}
				R={180}
				L={L}
				core={0.36}
				rimW={6}
				marks={mk('body')}
				decals={[
					saddle,
					...patch('eyePatch').map((d) => ({d, base: boneWarm, shadowT: 0.42})),
					...patch('throat').map((d) => ({d, base: boneWarm, shadowT: 0.42})),
					...patch('flank').map((d) => ({d, base: bone, shadowT: 0.42})),
				]}
				glints={[
					{cx: 1180, cy: 362, rx: 90, ry: 4, rot: 4, o: 0.35},
					{cx: 1420, cy: 420, rx: 34, ry: 3.5, rot: 22, o: 0.45},
					{cx: 520, cy: 420, rx: 60, ry: 3, rot: -21, o: 0.25},
				]}
				over={
					<g>
						{pecOcc}
						{creases}
					</g>
				}
			/>
			{open ? (
				<g transform={rot(jawRot, hinge)}>
					<ShadedPart id={`${id}-jw`} d={jawD} base={skin} R={60} L={L} rot={jawRot} marks={mk('jaw')} rimW={5}
						decals={patch('throat').map((d) => ({d, base: boneWarm, shadowT: 0.42}))} />
				</g>
			) : null}
			{/* eye: bone sclera ring, ochre iris ring, ink pupil, 1 large + 1 small glint toward the key; lid = skin */}
			<g>
				<defs>
					<clipPath id={`${id}-eyeclip`}>
						<circle cx={eye[0]} cy={eye[1]} r={11.5} />
					</clipPath>
				</defs>
				<ellipse cx={eye[0]} cy={eye[1]} rx={13.5} ry={13} fill={c(skin)} />
				<g clipPath={`url(#${id}-eyeclip)`}>
					<circle cx={eye[0]} cy={eye[1]} r={11.5} fill={c('bone-0')} />
					<circle cx={eye[0] + 1} cy={eye[1]} r={8.2} fill={c('ochre-0')} />
					<circle cx={eye[0] + 1.5} cy={eye[1]} r={5} fill={c('ink-0')} />
					<circle cx={eye[0] - 2} cy={eye[1] - 3} r={2.4} fill={c('bone-2')} />
					<circle cx={eye[0] + 3} cy={eye[1] + 2.5} r={1.1} fill={c('bone-2')} />
					<rect x={eye[0] - 14} y={eye[1] - 14} width={28} height={28 * (0.28 + 0.72 * blink)} fill={c(skin)} />
					<path d={`M ${eye[0] - 14} ${eye[1] - 14 + 28 * (0.28 + 0.72 * blink)} l 28 0`} stroke={mixOk(c(skin), c(L.keyColor), 0.3)} strokeWidth={1.6} />
				</g>
			</g>
			{/* near flipper: its own solid in front of the body */}
			<g transform={rot(pecNearRot, pnPivot)}>
				<ShadedPart id={`${id}-pn`} d={pecNearD} base={skin} R={80} L={L} rot={pecNearRot} marks={mk('pecNear')} core={0.42} rimW={7}
					glints={[{cx: 1000, cy: 700, rx: 40, ry: 3.5, rot: -60, o: 0.35}]} />
			</g>
		</g>
	);
};

export const markCount = () => G.marks.length;
