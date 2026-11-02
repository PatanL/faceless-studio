/**
 * Procedural shading layer (STYLE_BIBLE §4.3, the 9-layer stack). Give it a FLAT drawing - one path or a
 * group of coloured parts - and it adds, from the scene light (context) alone:
 *
 *   L9 cast shadow   soft ellipse on the ground, offset away from the key, shrinks/fades with lift
 *   L0 form          per-part radial gradient centred toward the key (ΔL ≤ 0.06, still reads flat)
 *   L1 core shadow   hard crescent on the side away from the key: silhouette minus silhouette shifted
 *                    toward the key. ONE crescent for the whole group, each part gets its own shadow mix
 *                    (a white belly patch and a black back share one terminator).
 *   L2 stipple       graded vector dots along the terminator on the lit side (3 sub-bands, 3 dot sizes,
 *                    seeded pattern so dots never swim)  -- the house signature
 *   L3 deep          thin, darker occlusion crescent at the far edge
 *   L4 bounce        faint ground-coloured crescent on the underside
 *   L5 highlight     hard crescent (or inset plane) toward the key, mix(base, keyColor, hi)
 *   L6 glints        bone-2 beans on glossy parts
 *   L7 rim           crescent toward the back light in the opposite temperature
 *   L8 micro-marks   seeded dash clusters / pores / rings / rake scars / scale arcs, shadow-aware tone
 *   +  inner glow    stepped inner strokes (no filter) for translucent/emissive or subsurface bodies
 *
 * Everything is masks + flat fills + gradients: no SVG filters (bible render-cost rules). All clipping is done
 * with luminance masks because <clipPath> may not contain <g>, and parts may be arbitrary groups.
 * The object's own transform (rotation, mirror) is passed as `xf` so the light stays in SCREEN space (J3); the storyboard
 * layer's flipX / rotation are read from core/light.tsx (LayerXfCtx) and undone too.
 *
 * Live-kit change vs the engine: the rim (L7) is gated by a gradient along the rim direction, so it lights only the
 * edges that face the back light (the far ~45 % of the object on that side) instead of reading as an outline around
 * fins and bellies (judge, orca_open_v3 2.1).
 * Ported from experiments/kurz-style/engine/src/shade/Shaded.tsx.
 */
import React from 'react';
import {c, mixOk, rgba, shadowOf, shiftL, lum} from './color';
import {pathBox, type Box} from './geom';
import {norm, useLight, useTint, type SceneLight, type Vec} from './light';
import {rng} from './rng';
import {useLayerXf, type LayerXf} from '../../../core/light';
import {FLAT} from './style';

export type Draw = (fill: string) => React.ReactNode;

export type MarkSpec = {
	kind: 'dash' | 'pore' | 'ring' | 'scar' | 'arc';
	n: number;
	seed?: string;
	/** where marks may land (default: the part's bounds, shrunk 15 %) */
	area?: Box;
	size?: number;
	/** OKLab L shift (default ±0.08 depending on base lightness) */
	dL?: number;
	opacity?: number;
	/** stroke angle in degrees for dash/scar */
	angle?: number;
};

export type Part = {
	d?: string;
	el?: Draw;
	base: string;
	/** decal: masked to the silhouette (patches, stripes, saddle) */
	clip?: boolean;
	/** highlight mix toward the key colour (default from props) */
	hi?: number;
	/** core-shadow mix for this part (default from props); lower keeps white patches reading white */
	shade?: number;
	stipple?: boolean;
	marks?: MarkSpec[];
	/** no shading at all (lights, eyes) */
	flat?: boolean;
	/** shadow target for this part (default: the scene ambient). A saturated tide shadow keeps white patches off grey (P4). */
	ambient?: string;
	opacity?: number;
};

export type Glint = {cx: number; cy: number; rx: number; ry: number; rot?: number; o?: number};

export type Layers = {
	form: boolean;
	core: boolean;
	stipple: boolean;
	deep: boolean;
	bounce: boolean;
	highlight: boolean;
	glints: boolean;
	rim: boolean;
	marks: boolean;
	cast: boolean;
	innerGlow: boolean;
};

/** style A (house/style.ts): one flat shadow shape (L1) + a few small glints; every other layer stays coded but off */
export const FLAT_LAYERS: Partial<Layers> = {form: false, stipple: false, deep: false, bounce: false, highlight: false, rim: false, marks: false, cast: false, innerGlow: false};

export const ALL_LAYERS: Layers = {
	form: true,
	core: true,
	stipple: false, // owner 2026-11-01: clean hard terminator by default (crisper, survives compression); stipple is opt-in
	deep: true,
	bounce: true,
	highlight: true,
	glints: true,
	rim: true,
	marks: true,
	cast: true,
	innerGlow: true,
};

export type ShadedProps = {
	id: string;
	parts: Part[];
	box?: Box;
	/** bounds of everything that must be shaded, if larger than `box` (fins outside the body box) */
	maskBox?: Box;
	R?: number;
	silhouette?: Draw;
	/** outline path(s) for the inner glow strokes (default: the non-decal parts' d) */
	outline?: string;
	xf?: {rot?: number; sx?: number; sy?: number};
	light?: Partial<SceneLight>;
	layers?: Partial<Layers>;
	/** level of detail: 'hero' = all layers; 'support' = form, core, highlight, rim; 'far' = form + core */
	lod?: 'hero' | 'support' | 'far';
	core?: number;
	deep?: number;
	hi?: number;
	hiWidth?: number;
	hiMode?: 'crescent' | 'inset';
	rimW?: number;
	rimOpacity?: number;
	stippleBand?: number;
	dot?: number;
	glints?: Glint[];
	/** add a glint pair that follows the light: placed at centre + key·0.55R (size = fraction of R) */
	autoGlint?: number;
	innerGlow?: {color: string; width: number; opacity?: number};
	cast?: {y: number; lift?: number; spread?: number; opacity?: number; ground?: string};
	/** drawn on top, masked to the silhouette (mouth line, eye socket) */
	over?: React.ReactNode;
	/** drawn on top, unmasked (eyes, labels) */
	top?: React.ReactNode;
};

const LOD: Record<string, Partial<Layers>> = {
	hero: {},
	support: {stipple: false, deep: false, bounce: false, glints: false, marks: false, cast: false, innerGlow: false},
	far: {stipple: false, deep: false, bounce: false, highlight: false, glints: false, rim: false, marks: false, cast: false, innerGlow: false},
};

/** screen-space direction -> object-local direction, given the object's local->screen rotate/scale */
const undo = (v: Vec, rot: number, sx: number, sy: number): Vec => {
	const a = (-rot * Math.PI) / 180;
	const x = v[0] * Math.cos(a) - v[1] * Math.sin(a);
	const y = v[0] * Math.sin(a) + v[1] * Math.cos(a);
	return [x * Math.sign(sx), y * Math.sign(sy)];
};
/** screen-space direction -> object-local: undo the storyboard layer (rotate, flipX), then the object's own xf */
export const toLocal = (v: Vec, xf?: ShadedProps['xf'], layer?: LayerXf): Vec => {
	const l = layer ? undo(v, layer.rotate, layer.flipX ? -1 : 1, 1) : v;
	return norm(undo(l, xf?.rot ?? 0, xf?.sx ?? 1, xf?.sy ?? 1));
};

export const Shaded: React.FC<ShadedProps> = (p) => {
	const scene = useLight();
	const layerXf = useLayerXf();
	const L: SceneLight = {...scene, ...p.light};
	const tint = useTint();
	const on: Layers = {...ALL_LAYERS, ...LOD[p.lod ?? 'hero'], ...p.layers, ...(FLAT ? FLAT_LAYERS : {})};

	const k = toLocal(L.key, p.xf, layerXf);
	const r = toLocal(L.rim, p.xf, layerXf);
	const g = toLocal([0, 1], p.xf, layerXf);

	const ds = p.parts.filter((q) => q.d && !q.clip).map((q) => q.d as string);
	const box: Box = p.box ?? pathBox(...(ds.length ? ds : p.parts.filter((q) => q.d).map((q) => q.d as string)));
	const [bx, by, bw, bh] = box;
	const R = p.R ?? Math.min(bw, bh) / 2;
	const cx = bx + bw / 2;
	const cy = by + bh / 2;

	const id = p.id;
	const drawPart = (q: Part, fill: string): React.ReactNode =>
		q.d ? <path d={q.d} fill={fill} /> : q.el ? q.el(fill) : null;
	const sil: Draw =
		p.silhouette ??
		((fill) => (
			<>
				{p.parts
					.filter((q) => !q.clip)
					.map((q, i) => (
						<React.Fragment key={i}>{drawPart(q, fill)}</React.Fragment>
					))}
			</>
		));
	const shifted = (dx: number, dy: number, fill: string) => <g transform={`translate(${dx.toFixed(2)} ${dy.toFixed(2)})`}>{sil(fill)}</g>;

	const core = (p.core ?? 0.38) * R;
	const deep = (p.deep ?? 0.12) * R;
	const hiW = (p.hiWidth ?? 0.22) * R;
	const rimW = p.rimW ?? Math.max(3, Math.min(9, 0.07 * R));
	const band = p.stippleBand ?? Math.max(14, 0.12 * R);

	// mask region: the object's bounds plus the largest shift any layer uses. Masks are rasterised over this
	// whole box, so a tight box is the main render-cost lever of the shading layer (profiled: scripts/profile.sh).
	const pad = Math.max(core + band, hiW, 0.2 * R, rimW) + 24;
	const [mx, my, mw, mh] = p.maskBox ?? box;
	const mr = {maskUnits: 'userSpaceOnUse' as const, x: mx - pad, y: my - pad, width: mw + 2 * pad, height: mh + 2 * pad};
	const dot = p.dot ?? 1;
	const ambient = L.ambient;

	const shaded = p.parts.map((q, i) => ({q, i, base: tint(q.base), amb: tint(q.ambient ?? ambient)}));

	// stipple dot tile (seeded jittered grid, shared positions, 3 radii)
	const T = 48;
	const n = 6;
	const rr = rng(`${id}-dots`);
	const dots: [number, number][] = [];
	for (let a = 0; a < n; a++)
		for (let b = 0; b < n; b++) dots.push([(a + 0.5 + (rr() - 0.5) * 0.6) * (T / n), (b + 0.5 + (rr() - 0.5) * 0.6) * (T / n)]);
	const radii = [3.1 * dot, 2.1 * dot, 1.15 * dot];

	const cast = p.cast && on.cast ? p.cast : null;

	return (
		<g>
			<defs>
				<mask id={`${id}-sil`} {...mr}>
					{sil('white')}
				</mask>
				{shaded.map(({q, i}) => (
					<mask key={i} id={`${id}-pm${i}`} {...mr}>
						{drawPart(q, 'white')}
					</mask>
				))}
				<mask id={`${id}-core`} {...mr}>
					{sil('white')}
					{shifted(k[0] * core, k[1] * core, 'black')}
				</mask>
				<mask id={`${id}-deep`} {...mr}>
					{sil('white')}
					{shifted(k[0] * deep, k[1] * deep, 'black')}
				</mask>
				<mask id={`${id}-bnc`} {...mr}>
					{sil('white')}
					{shifted(-g[0] * 0.14 * R, -g[1] * 0.14 * R, 'black')}
					{shifted(k[0] * 0.2 * R, k[1] * 0.2 * R, 'black')}
				</mask>
				<mask id={`${id}-hi`} {...mr}>
					{p.hiMode === 'inset' ? (
						<g transform={`translate(${cx + k[0] * 0.15 * R} ${cy + k[1] * 0.15 * R}) scale(0.64) translate(${-cx} ${-cy})`}>{sil('white')}</g>
					) : (
						<>
							{sil('white')}
							{shifted(-k[0] * hiW, -k[1] * hiW, 'black')}
						</>
					)}
				</mask>
				<mask id={`${id}-rim`} {...mr}>
					{sil('white')}
					{shifted(-r[0] * rimW, -r[1] * rimW, 'black')}
				</mask>
				{/* rim gate: black up to 10 % past the centre toward the rim light, white at the far rim-side extreme */}
				{(() => {
					const ext = Math.abs(r[0]) * (bw / 2) + Math.abs(r[1]) * (bh / 2) || 1;
					return (
						<linearGradient id={`${id}-rimg`} gradientUnits="userSpaceOnUse" x1={cx + r[0] * ext * 0.1} y1={cy + r[1] * ext * 0.1} x2={cx + r[0] * ext} y2={cy + r[1] * ext}>
							<stop offset="0" stopColor="black" />
							<stop offset="0.55" stopColor="white" />
							<stop offset="1" stopColor="white" />
						</linearGradient>
					);
				})()}
				<mask id={`${id}-rimgate`} {...mr}>
					<rect x={mr.x} y={mr.y} width={mr.width} height={mr.height} fill={`url(#${id}-rimg)`} />
				</mask>
				{[0, 1, 2].map((j) => (
					<mask key={j} id={`${id}-band${j}`} {...mr}>
						{shifted(k[0] * (core + (j * band) / 3), k[1] * (core + (j * band) / 3), 'white')}
						{shifted(k[0] * (core + ((j + 1) * band) / 3), k[1] * (core + ((j + 1) * band) / 3), 'black')}
					</mask>
				))}
				{shaded.map(({q, i, base, amb}) => (
					<React.Fragment key={i}>
						<radialGradient
							id={`${id}-f${i}`}
							gradientUnits="userSpaceOnUse"
							cx={0}
							cy={0}
							r={1.15}
							gradientTransform={`translate(${cx + k[0] * 0.25 * (bw / 2)} ${cy + k[1] * 0.25 * (bh / 2)}) scale(${bw / 2} ${bh / 2})`}
						>
							<stop offset="0" stopColor={mixOk(base, tint(L.keyColor), 0.06)} />
							<stop offset="1" stopColor={shadowOf(base, amb, 0.08)} />
						</radialGradient>
						{q.stipple === false || q.flat
							? null
							: radii.map((rad, j) => (
									<pattern key={j} id={`${id}-d${i}-${j}`} patternUnits="userSpaceOnUse" width={T} height={T}>
										{dots.map(([x, y], m) => (
											<circle key={m} cx={x} cy={y} r={rad} fill={shadowOf(base, amb, q.shade ?? p.core ?? 0.38)} />
										))}
									</pattern>
								))}
					</React.Fragment>
				))}
				{cast ? (
					<radialGradient id={`${id}-cast`}>
						<stop offset="0" stopColor={rgba(mixOk(tint(cast.ground ?? L.ground), tint(ambient), 0.55), 0.7)} />
						<stop offset="0.6" stopColor={rgba(mixOk(tint(cast.ground ?? L.ground), tint(ambient), 0.55), 0.3)} />
						<stop offset="1" stopColor={rgba(mixOk(tint(cast.ground ?? L.ground), tint(ambient), 0.55), 0)} />
					</radialGradient>
				) : null}
			</defs>

			{/* L9 cast shadow (outside the silhouette) */}
			{cast
				? (() => {
						const lift = cast.lift ?? 0;
						const s = 1 - 0.45 * lift;
						const rx = bw * 0.55 * s * (cast.spread ?? 1);
						return (
							<ellipse
								cx={cx - k[0] * (R * 0.6 + lift * R * 2.2)}
								cy={cast.y}
								rx={rx}
								ry={Math.max(6, rx * 0.13)}
								fill={`url(#${id}-cast)`}
								opacity={(cast.opacity ?? 1) * s}
							/>
						);
					})()
				: null}

			{shaded.map(({q, i, base, amb}) => {
				const hiAmt = q.hi ?? p.hi ?? 0.22;
				const body = (
					<g opacity={q.opacity}>
						{/* L0 */}
						{drawPart(q, on.form && !q.flat ? `url(#${id}-f${i})` : base)}
						{q.flat ? null : (
							<>
								{/* L1 core shadow */}
								{on.core ? <g mask={`url(#${id}-core)`}>{drawPart(q, shadowOf(base, amb, q.shade ?? p.core ?? 0.38))}</g> : null}
								{/* L2 stipple terminator */}
								{on.stipple && on.core && q.stipple !== false ? (
									<g mask={`url(#${id}-pm${i})`}>
										{[0, 1, 2].map((j) => (
											<rect key={j} x={mr.x} y={mr.y} width={mr.width} height={mr.height} fill={`url(#${id}-d${i}-${j})`} mask={`url(#${id}-band${j})`} />
										))}
									</g>
								) : null}
								{/* L3 deep occlusion */}
								{on.deep ? <g mask={`url(#${id}-deep)`}>{drawPart(q, shadowOf(base, amb, Math.min(0.6, (q.shade ?? 0.38) * 1.6)))}</g> : null}
								{/* L4 bounce */}
								{on.bounce ? (
									<g mask={`url(#${id}-bnc)`} opacity={0.16}>
										{drawPart(q, mixOk(base, tint(L.ground), 0.3))}
									</g>
								) : null}
								{/* L5 highlight */}
								{on.highlight && hiAmt > 0 ? <g mask={`url(#${id}-hi)`}>{drawPart(q, mixOk(base, tint(L.keyColor), hiAmt))}</g> : null}
								{/* L8 micro-marks */}
								{on.marks && q.marks ? (
									<g mask={`url(#${id}-pm${i})`}>
										{q.marks.map((m, mi) => (
											<Marks key={mi} spec={m} part={q} base={base} shadow={shadowOf(base, amb, p.core ?? 0.38)} k={k} cx={cx} cy={cy} R={R} seed={`${id}-${i}-${mi}`} />
										))}
									</g>
								) : null}
							</>
						)}
					</g>
				);
				return q.clip ? (
					<g key={i} mask={`url(#${id}-sil)`}>
						{body}
					</g>
				) : (
					<React.Fragment key={i}>{body}</React.Fragment>
				);
			})}

			{/* L7 rim, L6 glints, inner glow, overlays: once for the whole silhouette */}
			<g mask={`url(#${id}-sil)`}>
				{p.innerGlow && on.innerGlow
					? (() => {
							const d = p.outline ?? ds.join(' ');
							const col = tint(p.innerGlow.color);
							const o = p.innerGlow.opacity ?? 1;
							return [
								[2.0, 0.1],
								[1.2, 0.14],
								[0.5, 0.2],
							].map(([w, a], j) => <path key={j} d={d} fill="none" stroke={col} strokeWidth={p.innerGlow!.width * w} strokeLinejoin="round" opacity={a * o} />);
						})()
					: null}
				{on.rim ? (
					<g mask={`url(#${id}-rimgate)`}>
						<g mask={`url(#${id}-rim)`} opacity={p.rimOpacity ?? 0.92}>
							{sil(tint(L.rimColor))}
						</g>
					</g>
				) : null}
				{on.glints && p.autoGlint
					? (() => {
							const gx = cx + k[0] * 0.55 * R;
							const gy = cy + k[1] * 0.55 * R;
							const a = (Math.atan2(k[1], k[0]) * 180) / Math.PI + 90;
							const s = p.autoGlint * R;
							return (
								<g>
									<ellipse cx={gx} cy={gy} rx={s} ry={s * 0.45} transform={`rotate(${a} ${gx} ${gy})`} fill={c('bone-2')} opacity={0.85} />
									<circle cx={gx - k[1] * s * 1.5 + k[0] * s * 0.3} cy={gy + k[0] * s * 1.5 + k[1] * s * 0.3} r={s * 0.28} fill={c('bone-2')} opacity={0.8} />
								</g>
							);
						})()
					: null}
				{on.glints && p.glints
					? p.glints.map((gl, j) => (
							<ellipse
								key={j}
								cx={gl.cx}
								cy={gl.cy}
								rx={gl.rx}
								ry={gl.ry}
								transform={gl.rot ? `rotate(${gl.rot} ${gl.cx} ${gl.cy})` : undefined}
								fill={c('bone-2')}
								opacity={gl.o ?? 0.85}
							/>
						))
					: null}
				{p.over}
			</g>
			{p.top}
		</g>
	);
};

// ---------------------------------------------------------------- micro-marks (L8)

const Marks: React.FC<{spec: MarkSpec; part: Part; base: string; shadow: string; k: Vec; cx: number; cy: number; R: number; seed: string}> = ({
	spec,
	part,
	base,
	shadow,
	k,
	cx,
	cy,
	R,
	seed,
}) => {
	const r = rng(spec.seed ?? seed);
	const area = spec.area ?? (part.d ? pathBox(part.d) : ([cx - R, cy - R, 2 * R, 2 * R] as Box));
	const [ax, ay, aw, ah] = area;
	const sz = spec.size ?? Math.max(6, R * 0.08);
	const dL = spec.dL ?? (lum(base) < 0.5 ? 0.08 : -0.07);
	const lit = shiftL(base, dL);
	const op = spec.opacity ?? 0.9;
	const out: React.ReactNode[] = [];
	for (let i = 0; i < spec.n; i++) {
		const x = ax + aw * (0.08 + 0.84 * r());
		const y = ay + ah * (0.08 + 0.84 * r());
		const proj = ((x - cx) * k[0] + (y - cy) * k[1]) / R;
		const inShadow = proj < -0.55;
		const col = inShadow ? shiftL(shadow, dL * 0.6) : lit;
		const ang = ((spec.angle ?? r() * 180) + (r() - 0.5) * 24) * (Math.PI / 180);
		const ux = Math.cos(ang);
		const uy = Math.sin(ang);
		const s = sz * (0.7 + r() * 0.6);
		switch (spec.kind) {
			case 'dash': {
				const m = 3 + Math.floor(r() * 3);
				for (let j = 0; j < m; j++) {
					const ox = x + -uy * j * s * 0.55 + ux * (r() - 0.5) * s * 0.4;
					const oy = y + ux * j * s * 0.55 + uy * (r() - 0.5) * s * 0.4;
					const l = s * (0.5 + r() * 0.6);
					out.push(<line key={`${i}-${j}`} x1={ox} y1={oy} x2={ox + ux * l} y2={oy + uy * l} stroke={col} strokeWidth={Math.max(2, s * 0.22)} strokeLinecap="round" opacity={op} />);
				}
				break;
			}
			case 'pore':
				out.push(<circle key={i} cx={x} cy={y} r={Math.max(1.5, s * 0.22)} fill={col} opacity={op} />);
				break;
			case 'ring':
				out.push(
					<g key={i} opacity={op}>
						<circle cx={x} cy={y} r={s * 0.5} fill="none" stroke={col} strokeWidth={Math.max(2, s * 0.16)} />
						<circle cx={x} cy={y} r={s * 0.18} fill={col} />
					</g>,
				);
				break;
			case 'scar': {
				const m = 3 + Math.floor(r() * 2);
				const l = s * (2.2 + r() * 1.4);
				for (let j = 0; j < m; j++) {
					const ox = x + -uy * j * s * 0.42;
					const oy = y + ux * j * s * 0.42;
					out.push(
						<path
							key={`${i}-${j}`}
							d={`M ${ox} ${oy} Q ${ox + ux * l * 0.5 - uy * s * 0.18} ${oy + uy * l * 0.5 + ux * s * 0.18} ${ox + ux * l} ${oy + uy * l}`}
							stroke={col}
							strokeWidth={Math.max(1.6, s * 0.12)}
							strokeLinecap="round"
							fill="none"
							opacity={op * (0.6 + r() * 0.4)}
						/>,
					);
				}
				break;
			}
			case 'arc':
				out.push(
					<path
						key={i}
						d={`M ${x - s * 0.5} ${y} Q ${x} ${y + s * 0.45} ${x + s * 0.5} ${y}`}
						stroke={col}
						strokeWidth={Math.max(1.6, s * 0.14)}
						strokeLinecap="round"
						fill="none"
						opacity={op}
					/>,
				);
				break;
		}
	}
	return <>{out}</>;
};

// ---------------------------------------------------------------- the house eye (bible §10)

export const Eye: React.FC<{cx: number; cy: number; r: number; iris?: string; lid?: number; look?: Vec; blink?: number}> = ({
	cx,
	cy,
	r,
	iris = 'ochre-1',
	lid = 0,
	look = [0, 0],
	blink = 0,
}) => {
	const tint = useTint();
	const L = useLight();
	const open = Math.max(0.06, 1 - blink);
	const px = cx + look[0] * r * 0.25;
	const py = cy + look[1] * r * 0.25;
	return (
		<g transform={`translate(${cx} ${cy}) scale(1 ${open}) translate(${-cx} ${-cy})`}>
			<circle cx={cx} cy={cy} r={r} fill={tint('bone-1')} />
			<circle cx={px} cy={py} r={r * 0.7} fill={tint(iris)} />
			<circle cx={px} cy={py} r={r * 0.7} fill="none" stroke={tint(shiftL(c(iris), -0.08))} strokeWidth={r * 0.12} />
			<circle cx={px} cy={py} r={r * 0.38} fill={tint('ink-0')} />
			<circle cx={px + L.key[0] * r * 0.3} cy={py + L.key[1] * r * 0.3} r={r * 0.2} fill={c('bone-2')} />
			<circle cx={px - L.key[0] * r * 0.25} cy={py - L.key[1] * r * 0.25} r={r * 0.08} fill={c('bone-2')} opacity={0.8} />
			{lid > 0 ? <path d={`M ${cx - r * 1.1} ${cy - r * 1.1} L ${cx + r * 1.1} ${cy - r * 1.1} L ${cx + r * 1.1} ${cy - r + lid * r * 1.2} Q ${cx} ${cy - r + lid * r * 1.6} ${cx - r * 1.1} ${cy - r + lid * r * 1.2} Z`} fill={tint('ink-1')} /> : null}
		</g>
	);
};
