/**
 * The 9-layer shading stack (STYLE_BIBLE §4.3) for ANY kit figure, with no per-figure work.
 *
 * Every kit Figure can already draw itself as a flat silhouette (`DrawCtx.sil`). That is all the stack needs: the
 * figure is drawn three times per frame (colour body, a white silhouette and a black silhouette, the latter two once
 * in <defs> and reused through <use>), and every light layer is a mask built from shifted silhouette copies:
 *
 *   L9 cast      soft ellipse below the figure, offset away from the key (opt-in: `cast`)
 *   L0 form      radial gradient toward the key, masked to the silhouette (still reads flat)
 *   L1 core      hard crescent away from the key (silhouette minus silhouette shifted toward the key), MULTIPLY with a
 *                saturated ambient tint: white bellies go teal, not grey (P4); dark skins only get darker
 *   L2 stipple   3 graded dot bands on the lit side of the terminator (seeded tile: dots never swim)
 *   L3 deep      thin darker crescent at the far edge
 *   L4 bounce    faint ground colour on the underside
 *   L5 highlight crescent toward the key, key colour at low alpha
 *   L6 glints    opt-in (`glint`): a bean pair placed toward the key
 *   L7 rim       crescent toward the back light, GATED by a gradient so it only lights the edges facing the back light
 *                (never a full-silhouette outline)
 *   L8 marks     seeded dash clusters / pores on the front 70 % of the body; shadow-side marks take the shadow tone
 *
 * The light is the scene's (scene.light via house/light.tsx) in screen space: the layer's flipX/rotation are undone
 * (core LayerXfCtx). Level of detail follows the on-screen size: >= 140 px tall gets everything (hero), 60-140 px the
 * support set (form, core, highlight, rim), smaller ones form + core only. Cost: masks + gradients + 2 extra
 * silhouette draws; no SVG filters.
 */
import React from 'react';
import {useLayerXf} from '../../../core/light';
import type {DrawCtx, Figure} from '../figure';
import {c, mixOk, rgba} from './color';
import {useLight, useTint} from './light';
import {rng} from './rng';
import {toLocal} from './Shaded';
import {FLAT} from './style';

export type ShadeOpts = {
	/** 'hero' | 'support' | 'far' (default from on-screen size) */
	lod?: 'hero' | 'support' | 'far';
	/** core-shadow depth (fraction of R the silhouette is shifted), default 0.38 */
	core?: number;
	/** highlight alpha toward the key colour, default 0.16 */
	hi?: number;
	/** rim width in screen px (3-8 at 1080p), default from size */
	rim?: number;
	rimOpacity?: number;
	/** micro-mark count on hero LOD (0 = none), default 22 */
	marks?: number;
	/** contact shadow on the ground under the figure */
	cast?: boolean;
	/** glint size as a fraction of R (wet skin, glass), default none */
	glint?: number;
	/** shadow strength 0..1 (multiplier alpha), default 1 */
	strength?: number;
};

const num = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);

/** read the shading options from a figure layer's props (`shade: false` turns the stack off) */
export const shadeOpts = (p: Record<string, unknown>): ShadeOpts | null => {
	const s = p.shade;
	if (s === false) return null;
	const o = s && typeof s === 'object' ? (s as Record<string, unknown>) : {};
	const lod = o.lod === 'hero' || o.lod === 'support' || o.lod === 'far' ? o.lod : undefined;
	return {
		lod,
		core: typeof o.core === 'number' ? o.core : undefined,
		hi: typeof o.hi === 'number' ? o.hi : undefined,
		rim: typeof o.rim === 'number' ? o.rim : undefined,
		rimOpacity: typeof o.rimOpacity === 'number' ? o.rimOpacity : undefined,
		marks: typeof o.marks === 'number' ? o.marks : undefined,
		cast: o.cast === true,
		glint: typeof o.glint === 'number' ? o.glint : undefined,
		strength: typeof o.strength === 'number' ? o.strength : undefined,
	};
};

export const ShadeStack: React.FC<{f: Figure; ctx: DrawCtx; upp: number; opts: ShadeOpts}> = ({f, ctx, upp, opts}) => {
	const L = useLight();
	const tint = useTint();
	const xf = useLayerXf();
	const id = `${ctx.id}S`;
	const [bx, by, bw, bh] = f.box;
	const R = Math.min(bw, bh) / 2;
	const cx = bx + bw / 2;
	const cy = by + bh / 2;
	const screenH = bh / Math.max(1e-6, upp);
	const lod = opts.lod ?? (screenH >= 140 ? 'hero' : screenH >= 60 ? 'support' : 'far');
	const hero = lod === 'hero';
	const support = lod !== 'far';

	const k = toLocal(L.key, undefined, xf);
	const r = toLocal(L.rim, undefined, xf);
	const g = toLocal([0, 1], undefined, xf);

	const core = (opts.core ?? 0.38) * R;
	const deep = 0.1 * R;
	const hiW = 0.2 * R;
	const rimPx = opts.rim ?? Math.max(3, Math.min(7, screenH * 0.018));
	const rimW = rimPx * upp;
	const band = Math.max(14 * upp, 0.1 * R);
	const pad = Math.max(core + band, hiW, rimW) + 24 * upp;
	const mr = {maskUnits: 'userSpaceOnUse' as const, x: bx - pad, y: by - pad, width: bw + 2 * pad, height: bh + 2 * pad};

	// colours: shadow = multiply by a saturated ambient tint (never grey on white bellies), light = key colour at low alpha
	const strength = opts.strength ?? 1;
	const shadeMul = mixOk(mixOk('bone-2', tint(L.haze), 0.5), tint(L.ambient), 0.15);
	const deepMul = mixOk(shadeMul, tint(L.ambient), 0.4);
	const key = tint(L.keyColor);
	const W = `#${id}-W`;
	const K = `#${id}-K`;
	const use = (href: string, dx = 0, dy = 0) => <use href={href} transform={dx || dy ? `translate(${dx.toFixed(2)} ${dy.toFixed(2)})` : undefined} />;
	const full = <rect x={mr.x} y={mr.y} width={mr.width} height={mr.height} />;

	// stipple dot tile (figure units; dots 1.2-3.2 screen px)
	const T = 44 * upp;
	const n = 6;
	const rr = rng(`${f.label}-dots`);
	const dots: [number, number][] = [];
	for (let a = 0; a < n; a++) for (let b = 0; b < n; b++) dots.push([(a + 0.5 + (rr() - 0.5) * 0.6) * (T / n), (b + 0.5 + (rr() - 0.5) * 0.6) * (T / n)]);
	const radii = [3.2 * upp, 2.2 * upp, 1.2 * upp];

	// micro-marks: front 70 % of the body (figures face right: the head end bends least under swim warps)
	const darkMarks: React.ReactNode[] = [];
	const lightMarks: React.ReactNode[] = [];
	const nMarks = hero ? Math.round(opts.marks ?? 22) : 0;
	if (nMarks > 0) {
		const m = rng(`${f.label}-marks`);
		const s = 9 * upp;
		for (let i = 0; i < nMarks; i++) {
			const x = bx + bw * (0.3 + 0.62 * m());
			const y = by + bh * (0.2 + 0.6 * m());
			const proj = ((x - cx) * k[0] + (y - cy) * k[1]) / R;
			const dark = proj < -0.2;
			const ang = (m() * 50 - 25 + (m() > 0.5 ? 0 : 90)) * (Math.PI / 180);
			const ux = Math.cos(ang);
			const uy = Math.sin(ang);
			if (m() < 0.55) {
				const cnt = 3 + Math.floor(m() * 3);
				for (let j = 0; j < cnt; j++) {
					const ox = x - uy * j * s * 0.55;
					const oy = y + ux * j * s * 0.55;
					const l = s * (0.6 + m() * 0.6);
					(dark ? darkMarks : lightMarks).push(
						<line key={`${i}-${j}`} x1={ox} y1={oy} x2={ox + ux * l} y2={oy + uy * l} stroke={dark ? deepMul : c('bone-2')} strokeWidth={Math.max(1.6 * upp, s * 0.24)} strokeLinecap="round" opacity={dark ? 0.7 : 0.12} />,
					);
				}
			} else {
				(dark ? darkMarks : lightMarks).push(<circle key={i} cx={x} cy={y} r={Math.max(1.4 * upp, s * 0.2)} fill={dark ? deepMul : c('bone-2')} opacity={dark ? 0.7 : 0.12} />);
			}
		}
	}

	const castY = by + bh;
	const castRx = bw * 0.5;
	return (
		<g>
			<defs>
				<g id={`${id}-W`}>{f.draw({...ctx, id: `${id}w`, sil: '#ffffff'})}</g>
				<g id={`${id}-K`}>{f.draw({...ctx, id: `${id}k`, sil: '#000000'})}</g>
				<mask id={`${id}-sil`} {...mr}>
					{use(W)}
				</mask>
				<mask id={`${id}-core`} {...mr}>
					{use(W)}
					{use(K, k[0] * core, k[1] * core)}
				</mask>
				<mask id={`${id}-hi`} {...mr}>
					{use(W)}
					{use(K, -k[0] * hiW, -k[1] * hiW)}
				</mask>
				<mask id={`${id}-rim`} {...mr}>
					{use(W)}
					{use(K, -r[0] * rimW, -r[1] * rimW)}
				</mask>
				{hero ? (
					<>
						<mask id={`${id}-deep`} {...mr}>
							{use(W)}
							{use(K, k[0] * deep, k[1] * deep)}
						</mask>
						<mask id={`${id}-bnc`} {...mr}>
							{use(W)}
							{use(K, -g[0] * 0.14 * R, -g[1] * 0.14 * R)}
							{use(K, k[0] * 0.2 * R, k[1] * 0.2 * R)}
						</mask>
						{[0, 1, 2].map((j) => (
							<mask key={j} id={`${id}-band${j}`} {...mr}>
								<g transform={`translate(${(k[0] * (core + (j * band) / 3)).toFixed(2)} ${(k[1] * (core + (j * band) / 3)).toFixed(2)})`}>{use(W)}</g>
								{use(K, k[0] * (core + ((j + 1) * band) / 3), k[1] * (core + ((j + 1) * band) / 3))}
							</mask>
						))}
						{radii.map((rad, j) => (
							<pattern key={j} id={`${id}-d${j}`} patternUnits="userSpaceOnUse" width={T} height={T}>
								{dots.map(([x, y], q) => (
									<circle key={q} cx={x} cy={y} r={rad} fill={shadeMul} />
								))}
							</pattern>
						))}
					</>
				) : null}
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
				<radialGradient id={`${id}-form`} gradientUnits="userSpaceOnUse" cx={0} cy={0} r={1.15} gradientTransform={`translate(${cx + k[0] * 0.25 * (bw / 2)} ${cy + k[1] * 0.25 * (bh / 2)}) scale(${bw / 2} ${bh / 2})`}>
					<stop offset="0" stopColor={rgba(key, 0.08)} />
					<stop offset="0.55" stopColor={rgba(key, 0)} />
					<stop offset="1" stopColor={rgba(tint(L.ambient), 0.12)} />
				</radialGradient>
				{opts.cast ? (
					<radialGradient id={`${id}-cast`}>
						<stop offset="0" stopColor={rgba(mixOk(tint(L.ground), tint(L.ambient), 0.55), 0.6)} />
						<stop offset="0.6" stopColor={rgba(mixOk(tint(L.ground), tint(L.ambient), 0.55), 0.25)} />
						<stop offset="1" stopColor={rgba(mixOk(tint(L.ground), tint(L.ambient), 0.55), 0)} />
					</radialGradient>
				) : null}
			</defs>

			{!FLAT && opts.cast ? <ellipse cx={cx - k[0] * R * 0.5} cy={castY} rx={castRx} ry={Math.max(6 * upp, castRx * 0.12)} fill={`url(#${id}-cast)`} /> : null}
			{f.draw(ctx)}
			{FLAT ? (
				// style A (house/style.ts): one flat shadow shape on the side away from the light; nothing else
				<g mask={`url(#${id}-sil)`} style={{mixBlendMode: 'multiply'}} opacity={strength}>
					<g mask={`url(#${id}-core)`}>{React.cloneElement(full, {fill: shadeMul})}</g>
				</g>
			) : null}
			{FLAT ? null : <>
			{/* L0 form (normal alpha) */}
			<g mask={`url(#${id}-sil)`}>{React.cloneElement(full, {fill: `url(#${id}-form)`})}</g>
			{/* L1 core + L2 stipple + L3 deep + shadow-side marks: one MULTIPLY group. The blend sits on the masked element
			    itself (a masked group is isolated, so a blend nested inside it would composite against transparency). */}
			<g mask={`url(#${id}-sil)`} style={{mixBlendMode: 'multiply'}} opacity={strength}>
				<g mask={`url(#${id}-core)`}>{React.cloneElement(full, {fill: shadeMul})}</g>
				{hero
					? [0, 1, 2].map((j) => (
							<g key={j} mask={`url(#${id}-band${j})`}>
								{React.cloneElement(full, {fill: `url(#${id}-d${j})`})}
							</g>
						))
					: null}
				{hero ? <g mask={`url(#${id}-deep)`}>{React.cloneElement(full, {fill: deepMul})}</g> : null}
				{darkMarks}
			</g>
			<g mask={`url(#${id}-sil)`}>
				{/* L4 bounce */}
				{hero ? <g mask={`url(#${id}-bnc)`}>{React.cloneElement(full, {fill: tint(L.ground), opacity: 0.14})}</g> : null}
				{/* L5 highlight */}
				{support ? <g mask={`url(#${id}-hi)`}>{React.cloneElement(full, {fill: key, opacity: opts.hi ?? 0.16})}</g> : null}
				{/* L8 lit-side marks */}
				{lightMarks}
				{/* L6 glints */}
				{opts.glint && support
					? (() => {
							const gx = cx + k[0] * 0.5 * (bw / 2);
							const gy = cy + k[1] * 0.5 * (bh / 2);
							const s = opts.glint * R;
							const a = (Math.atan2(k[1], k[0]) * 180) / Math.PI + 90;
							return (
								<g>
									<ellipse cx={gx} cy={gy} rx={s} ry={s * 0.42} transform={`rotate(${a.toFixed(1)} ${gx} ${gy})`} fill={c('bone-2')} opacity={0.8} />
									<circle cx={gx - k[1] * s * 1.5} cy={gy + k[0] * s * 1.5} r={s * 0.28} fill={c('bone-2')} opacity={0.75} />
								</g>
							);
						})()
					: null}
				{/* L7 rim: only the edges facing the back light */}
				{support ? (
					<g mask={`url(#${id}-rimgate)`}>
						<g mask={`url(#${id}-rim)`}>{React.cloneElement(full, {fill: tint(L.rimColor), opacity: opts.rimOpacity ?? 0.85})}</g>
					</g>
				) : null}
			</g>
			</>}
		</g>
	);
};
