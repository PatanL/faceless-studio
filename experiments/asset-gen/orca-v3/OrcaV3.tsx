/**
 * OrcaV3: the hero orca rebuilt as animatable code from the flat, bold v3 reference (gen/a_orca_side_v3.png), recoloured to house style A
 * (gen/style_board_A.png panel 6).
 *
 * Look: a few big rounded shapes, flat colour, one flat shadow shape per part (no gradients, no outlines, no marks
 * except the eye glint), house style A palette (docs/HOUSE_STYLE.md: indigo-ink body, bone-white patches; the v3 navy is PALETTE_V3). Geometry is measured off the reference by
 * orca-v3/extract_v3.py (geom_v3.json); cut lines, pivots and hidden overlaps are placed by hand.
 *
 * Rig (every motion is a point warp of the part's paths, weighted to zero at the part's root, so the root never
 * moves and no gap can open at any pose):
 *   swim     whale-style vertical travelling wave over the whole body (head stable, amplitude grows to the tail)
 *   fluke    two lobes; pitch lags the body wave, and the lobes scissor a little (the fluke plane turning)
 *   dorsal   sways as a shear that is zero along its base line (finScale stretches it about the base)
 *   flipper  near flipper (the reference shows no far one), follow-through behind the body wave plus the `pec` angle; rotation grows from the root
 *   jaw      lower jaw rotates about the hinge with a weight that ramps in front of the gape (no blocky seam);
 *            mouth interior, tongue and simple teeth appear in the gap
 *   eye      blink (seeded auto blink, or the `blink` prop), lid droop, look
 *   light    `light.key` slides every flat shadow shape (the terminator) inside its part; still flat fills
 *
 * Views: 'side' (hero), 'front' (head-on, approaching) and 'below' (from underneath, rising). Same palette and rules.
 *
 * Pure React SVG, no Remotion and no kit imports: the kit adapter (orca-v3/port/orcaV3Kit.tsx) feeds it the
 * scene light and plane tint. Local space = reference pixels (1536 x 1024 per view).
 */
import React from 'react';
import geom from './geom_v3.json';

type Pt = [number, number];
type F = (x: number, y: number) => Pt;
export type Box = [number, number, number, number];

// ---------------------------------------------------------------- palettes
/**
 * House style A (docs/HOUSE_STYLE.md, gen/style_board_A.png panel 6): indigo-ink body, ONE darker tone of it for
 * the flat shadow shapes, a lighter indigo saddle, cool bone-white patches with one darker tone, a small dark eye
 * with one glint. Mouth colours are darker/lighter tones of the board's magenta.
 */
export const PALETTE_A = {
	water: '#008ffd', // board panel 6 water (only used by the render sheets)
	lit: '#250192', // indigo-ink
	dark: '#18006e', // indigo-ink, darker tone (OKLab L -22%)
	white: '#e9f4fc', // bone white (cool, as on the board)
	whiteShade: '#bfd3ee',
	saddle: '#4a2fb4', // indigo-ink, lighter tint
	eye: '#0d004a',
	glint: '#ffffff',
	mouth: '#5e003f',
	tongue: '#c62292',
	tooth: '#e9f4fc',
	toothShade: '#bfd3ee',
};
export type Palette = typeof PALETTE_A;
/** the navy palette sampled from gen/a_orca_side_v3.png (kept for comparison with that reference) */
export const PALETTE_V3: Palette = {
	water: '#17187c',
	lit: '#19134d',
	dark: '#120d3c',
	white: '#f3f1ee',
	whiteShade: '#e2e1e0',
	saddle: '#9998b0',
	eye: '#05040f',
	glint: '#ffffff',
	mouth: '#2a0d3e',
	tongue: '#a3376f',
	tooth: '#f3f1ee',
	toothShade: '#d6d3dc',
};

export type V3Light = {
	/** unit vector toward the key light (screen space, y down). The reference is lit from straight above: [0, -1] */
	key: Pt;
};
export const TOP_LIGHT: V3Light = {key: [0, -1]};

export type OrcaV3Props = {
	id?: string;
	/** seconds */
	t?: number;
	/** tail-beat amplitude multiplier (1 = default beat, 0 = still) */
	amp?: number;
	/** tail beats per second */
	freq?: number;
	/** 0 closed .. 1 open (24 deg); may overshoot to 1.1 */
	jaw?: number;
	/** extra flipper angle in degrees, added to the follow-through */
	pec?: number;
	/** 0 open .. 1 shut; undefined = seeded automatic blinks */
	blink?: number;
	/** upper lid droop 0..1 (kit `lid`) */
	lid?: number;
	/** pupil direction -1..1 (moves the eye glint) */
	look?: Pt;
	light?: V3Light;
	view?: 'side' | 'front' | 'below';
	/** 'far' = flat parts, no shadow shapes (distant orca); silColor = one flat colour silhouette */
	lod?: 'hero' | 'far';
	silColor?: string;
	/** dorsal fin height multiplier about its base (adult male 1.3-1.5) */
	finScale?: number;
	/** object rotation (deg) and mirror applied by the caller: used only to keep the light in screen space */
	rot?: number;
	flip?: boolean;
	/** colour set; default house style A */
	palette?: Palette;
	/** colour -> colour on the current plane (kit useTint); identity by default */
	tint?: (hex: string) => string;
	/** flat contact/cast shadow on a floor at local y */
	cast?: {y: number; lift?: number};
};

// ---------------------------------------------------------------- geometry helpers
const PAIR = /(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g;
const warp = (d: string, f?: F) =>
	f
		? d.replace(PAIR, (_, xs, ys) => {
				const [x, y] = f(+xs, +ys);
				return `${x.toFixed(1)} ${y.toFixed(1)}`;
			})
		: d;
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const smooth = (e0: number, e1: number, x: number) => {
	const u = clamp((x - e0) / (e1 - e0));
	return u * u * (3 - 2 * u);
};
const rotAbout = (o: Pt, deg: number, x: number, y: number): Pt => {
	const a = (deg * Math.PI) / 180;
	const ca = Math.cos(a);
	const sa = Math.sin(a);
	return [o[0] + (x - o[0]) * ca - (y - o[1]) * sa, o[1] + (x - o[0]) * sa + (y - o[1]) * ca];
};
/** rotation about o whose angle is scaled by a per-point weight (0 at the root -> the root never moves) */
const rotW = (o: Pt, deg: number, w: (x: number, y: number) => number): F => (x, y) => rotAbout(o, deg * w(x, y), x, y);
const chain = (...fs: (F | undefined)[]): F => (x, y) => fs.reduce<Pt>((p, f) => (f ? f(p[0], p[1]) : p), [x, y]);
const ptsPath = (pts: Pt[]) => `M ${pts.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L ')}`;

const hash = (s: string, i: number) => {
	let h = 2166136261 ^ i;
	for (let k = 0; k < s.length; k++) h = Math.imul(h ^ s.charCodeAt(k), 16777619);
	return ((h >>> 0) % 10000) / 10000;
};
/** seeded blinks: every 2-5 s, 0.18 s long (same rhythm as the kit's blinkAt) */
export const autoBlink = (t: number, seed: string) => {
	let at = 0.4 + hash(seed, 0) * 2.2;
	for (let i = 1; i < 64 && at < t + 1; i++) {
		const d = t - at;
		if (d >= 0 && d < 0.18) return Math.sin((d / 0.18) * Math.PI);
		at += 2 + hash(seed, i) * 3;
	}
	return 0;
};

/** screen-space key -> local key (undo the caller's rotation / mirror) */
const localKey = (L: V3Light, rot = 0, flip = false): Pt => {
	const a = (-rot * Math.PI) / 180;
	let [x, y] = L.key;
	[x, y] = [x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)];
	if (flip) x = -x;
	const l = Math.hypot(x, y) || 1;
	return [x / l, y / l];
};
/** how far a flat shadow shape slides when the key moves away from the reference's top light */
const slide = (k: Pt, r: number, k0: Pt = TOP_LIGHT.key): string => {
	const dx = (k0[0] - k[0]) * r;
	const dy = (k0[1] - k[1]) * r;
	return `translate(${dx.toFixed(1)} ${dy.toFixed(1)})`;
};

type Paint = (hex: string) => string;

/**
 * One flat part: base colour + its flat shadow shape(s) + decals, composited as ONE isolated group and cut by a
 * <mask> of the part's outline. A mask (not a clipPath) because renderers apply a clip to every draw call inside the
 * group: each decal that reaches the outline would then leave an a(1-a) fringe of the base colour (a thin dark
 * outline on the white belly), and a part that overlaps an identical one (the jaw over the body behind the hinge)
 * would show a seam line. A mask composites the finished group once, so neither happens.
 */
const FlatPart: React.FC<{
	id: string;
	d: string;
	base: string;
	shadows?: {d: string; fill: string; slide?: string}[];
	children?: React.ReactNode;
	flat?: boolean;
}> = ({id, d, base, shadows = [], children, flat}) =>
	flat && !children ? (
		<path d={d} fill={base} />
	) : (
		<g>
			<defs>
				<mask id={`${id}-m`} maskUnits="userSpaceOnUse" x={-2000} y={-2000} width={6000} height={5000}>
					<path d={d} fill="#fff" />
				</mask>
			</defs>
			<g mask={`url(#${id}-m)`}>
				<rect x={-2000} y={-2000} width={6000} height={5000} fill={base} />
				{flat ? null : shadows.map((s, i) => <path key={i} d={s.d} fill={s.fill} fillRule="evenodd" transform={s.slide} />)}
				{children}
			</g>
		</g>
	);

// ================================================================================== SIDE
const SG = geom.side as unknown as {
	parts: Record<string, string>;
	mouth: Pt[];
	pivots: Record<'dorsalBase' | 'flukeRoot' | 'pecNear' | 'jaw' | 'head' | 'tail', Pt>;
	cutY: Pt[];
	eye: {cx: number; cy: number; r: number};
	box: Box;
};
const SP = SG.parts;
/** tight drawing box of the side view (snout tip to fluke tip, dorsal tip to flipper tip) in local px */
export const ORCA_V3_BOX: Box = SG.box;
const JAW_MAX = 24;
const EYE: Pt = [1315.5, 509.5];

const cutYAt = (x: number) => {
	const c = SG.cutY;
	if (x <= c[0][0]) return c[0][1];
	for (let i = 1; i < c.length; i++)
		if (x <= c[i][0]) return c[i - 1][1] + ((c[i][1] - c[i - 1][1]) * (x - c[i - 1][0])) / (c[i][0] - c[i - 1][0]);
	return c[c.length - 1][1];
};

const Side: React.FC<Required<Pick<OrcaV3Props, 'id' | 't' | 'amp' | 'freq' | 'jaw' | 'pec' | 'lid' | 'look' | 'finScale'>> & {
	blink: number;
	k: Pt;
	paint: Paint;
	far: boolean;
	sil?: string;
	V: Palette;
}> = ({id, t, amp, freq, jaw, pec, blink, lid, look, finScale, k, paint, far, sil, V}) => {
	const col = (h: string) => sil ?? paint(h);
	const flat = far || !!sil;
	const ph = 2 * Math.PI * freq * t;
	const P = SG.pivots;
	const [hx] = P.head;
	const [tx] = P.tail;
	// body wave (vertical, whale style)
	const ampPx = 34 * amp;
	const bend: F = (x, y) => {
		const s = clamp((hx - x) / (hx - tx));
		return [x, y + ampPx * (s * s + 0.04) * Math.sin(ph - 2.4 * s)];
	};
	const motion = amp > 0 ? 1 : 0;
	// secondary motion, phase-lagged off the body wave
	const pitch = motion * 11 * Math.sin(ph - 2.9) * Math.min(1.4, amp);
	const scissor = motion * 3.5 * Math.cos(ph - 2.9) * Math.min(1.4, amp);
	const sway = motion * 9 * Math.sin(ph - 1.3) * Math.min(1.4, amp);
	const pecRot = motion * 6 * Math.sin(ph - 0.9) * Math.min(1.4, amp) + pec;
	const jawDeg = JAW_MAX * clamp(jaw, 0, 1.15);
	const open = jawDeg > 0.3;

	// local rigs (rest frame), then the body wave on top
	const [rx, ry] = P.flukeRoot;
	const wFluke = (x: number) => smooth(0, 95, rx + 4 - x);
	const lobe = (sgn: -1 | 1) => chain(rotW([rx, ry], pitch + sgn * scissor, (x) => wFluke(x)), bend);
	const dorsalF = chain((x, y) => {
		const cy = cutYAt(x);
		if (y >= cy) return [x, y];
		const yy = cy - (cy - y) * finScale;
		const h = clamp((cy - yy) / (190 * finScale));
		return [x + sway * Math.pow(h, 1.5), yy];
	}, bend);
	const pecW = (x: number, y: number) => smooth(24, 130, Math.hypot(x - P.pecNear[0], y - P.pecNear[1]));
	const pecF = chain(rotW(P.pecNear, pecRot, pecW), bend);
	// weight = how far a point lies in front of a line from the gape down-forward to the throat (n = its normal):
	// the lip line ramps in over ~60 px, the throat under the hinge stays with the body (no sag, no blocky seam)
	const jawW = (x: number, y: number) => smooth(-30, 90, (x - P.jaw[0]) * 0.795 - (y - P.jaw[1]) * 0.606);
	const jawF = chain(rotW(P.jaw, jawDeg, jawW), bend);

	const sl = (r: number) => (flat ? undefined : slide(k, r));
	// the body's flat layers, drawn through any point warp f (used for the body and again for the jaw)
	const bodyLayers = (f: F, pre: string) => (
		<>
			{flat ? null : <path d={warp(SP.bodyDark, f)} fill={col(V.dark)} fillRule="evenodd" transform={sl(34)} />}
			{sil ? null : (
				<>
					<path d={warp(SP.saddle, f)} fill={paint(V.saddle)} />
					<clipPath id={`${pre}-bl`}>
						<path d={warp(SP.belly, f)} />
					</clipPath>
					<path d={warp(SP.belly, f)} fill={paint(V.white)} />
					{flat ? null : <path d={warp(SP.bellyShadow, f)} fill={paint(V.whiteShade)} fillRule="evenodd" transform={sl(14)} clipPath={`url(#${pre}-bl)`} />}
					<path d={warp(SP.eyePatch, f)} fill={paint(V.white)} />
				</>
			)}
		</>
	);

	// mouth: interior + tongue + simple teeth in the gap (drawn over the body, under the jaw)
	const up: Pt[] = SG.mouth.map(([x, y]) => bend(x, y));
	const lo: Pt[] = SG.mouth.map(([x, y]) => jawF(x, y));
	const along = (pts: Pt[], s: number): [Pt, Pt] => {
		const f = s * (pts.length - 1);
		const j = Math.min(pts.length - 2, Math.floor(f));
		const u = f - j;
		const a = pts[j];
		const b = pts[j + 1];
		const l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
		return [[a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u], [(b[0] - a[0]) / l, (b[1] - a[1]) / l]];
	};
	const teeth = (pts: Pt[], dir: 1 | -1, key: string) => {
		const n = 7;
		const grow = clamp(jaw * 2.4);
		return Array.from({length: n}, (_, i) => {
			const [[x, y], [ux, uy]] = along(pts, 0.2 + (i * 0.72) / (n - 1));
			const nx = -uy * dir;
			const ny = ux * dir;
			const h = (13 - i * 0.6) * grow;
			const w = 6.2 - i * 0.25;
			const tip: Pt = [x + nx * h - ux * 1.5, y + ny * h - uy * 1.5];
			const a: Pt = [x - ux * w, y - uy * w];
			const b: Pt = [x + ux * w, y + uy * w];
			return (
				<g key={key + i}>
					<path d={`M ${a[0]} ${a[1]} Q ${tip[0] - ux * 2} ${tip[1] - uy * 2} ${tip[0]} ${tip[1]} Q ${tip[0] + ux * 3} ${tip[1] + uy * 3} ${b[0]} ${b[1]} Z`} fill={paint(V.tooth)} />
					<path d={`M ${x} ${y} L ${tip[0]} ${tip[1]} Q ${tip[0] + ux * 3} ${tip[1] + uy * 3} ${b[0]} ${b[1]} Z`} fill={paint(V.toothShade)} />
				</g>
			);
		});
	};
	const uT = up[up.length - 1];
	const lT = lo[lo.length - 1];
	const back: Pt = [(uT[0] + lT[0]) / 2 - 0.3 * Math.hypot(lT[0] - uT[0], lT[1] - uT[1]), (uT[1] + lT[1]) / 2];
	const gap = `${ptsPath(up)} Q ${back[0].toFixed(1)} ${back[1].toFixed(1)} ${lo
		.slice()
		.reverse()
		.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`)
		.join(' L ')} Z`;
	const tongueAt = along(lo, 0.32)[0];
	const mouth =
		open && !sil ? (
			<g>
				<clipPath id={`${id}-gap`}>
					<path d={gap} />
				</clipPath>
				<path d={gap} fill={paint(V.mouth)} />
				<ellipse cx={tongueAt[0] + 6} cy={tongueAt[1] - 2} rx={70} ry={8 + 10 * clamp(jaw)} fill={paint(V.tongue)} transform={`rotate(${(jawDeg * 0.75).toFixed(1)} ${tongueAt[0]} ${tongueAt[1]})`} clipPath={`url(#${id}-gap)`} />
				{teeth(up, 1, 'u')}
				{teeth(lo, -1, 'l')}
			</g>
		) : null;

	// eye: small dark eye, one glint; blink squashes it, lid droop covers the top
	const [ex, ey] = bend(EYE[0], EYE[1]);
	const shut = clamp(Math.max(blink, lid * 0.6));
	const eyeEl = sil ? null : (
		<g>
			<ellipse cx={ex} cy={ey} rx={8.5} ry={Math.max(0.8, 8.5 * (1 - shut))} fill={paint(V.eye)} />
			{shut < 0.55 && !far ? <circle cx={ex + 1 + look[0] * 2.5} cy={ey - 2.5 + look[1] * 2.5} r={2.8} fill={paint(V.glint)} /> : null}
			{shut > 0.05 ? <path d={`M ${ex - 9} ${ey - 1 + 7 * shut * 0.2} Q ${ex} ${ey + 3.5 - 6 * (1 - shut)} ${ex + 9} ${ey - 1 + 7 * shut * 0.2}`} stroke={paint(V.lit)} strokeWidth={2.4} fill="none" strokeLinecap="round" opacity={shut > 0.6 ? 1 : 0} /> : null}
		</g>
	);

	const bodyD = warp(SP.body, bend);
	return (
		<g>
			{/* flukes: lower lobe behind the upper one */}
			<FlatPart id={`${id}-fl`} d={warp(SP.lobeL, lobe(1))} base={col(V.lit)} flat={flat} shadows={[{d: warp(SP.lobeLDark, lobe(1)), fill: col(V.dark), slide: sl(16)}]} />
			<FlatPart id={`${id}-fu`} d={warp(SP.lobeU, lobe(-1))} base={col(V.lit)} flat={flat} shadows={[{d: warp(SP.lobeUDark, lobe(-1)), fill: col(V.dark), slide: sl(16)}]} />
			{/* dorsal: behind the body, its base stub hidden under the back line */}
			<FlatPart id={`${id}-do`} d={warp(SP.dorsal, dorsalF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(SP.dorsalDark, dorsalF), fill: col(V.dark), slide: sl(30)}]} />
			{/* body */}
			<FlatPart id={`${id}-bd`} d={bodyD} base={col(V.lit)}>
				{bodyLayers(bend, `${id}-bd`)}
			</FlatPart>
			{mouth}
			{/* lower jaw: the same body layers through the jaw warp; it overlaps the body behind the hinge (weight 0 there) */}
			{open ? (
				<FlatPart id={`${id}-jw`} d={warp(SP.jaw, jawF)} base={col(V.lit)}>
					{bodyLayers(jawF, `${id}-jw`)}
				</FlatPart>
			) : null}
			{eyeEl}
			{/* near flipper (in front of the body); its rounded root cap never moves */}
			<FlatPart id={`${id}-pn`} d={warp(SP.pecNear, pecF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(SP.pecNearDark, pecF), fill: col(V.dark), slide: sl(22)}]} />
		</g>
	);
};

// ================================================================================== public component
export const OrcaV3: React.FC<OrcaV3Props> = ({
	id = 'orca3',
	t = 0,
	amp = 1,
	freq = 0.55,
	jaw = 0,
	pec = 0,
	blink,
	lid = 0,
	look = [0, 0],
	light = TOP_LIGHT,
	view = 'side',
	lod = 'hero',
	silColor,
	finScale = 1,
	rot = 0,
	flip = false,
	tint,
	cast,
	palette = PALETTE_A,
}) => {
	const paint: Paint = tint ?? ((h) => h);
	const k = localKey(light, rot, flip);
	const bl = blink ?? autoBlink(t, id);
	const common = {id, t, amp, freq, jaw, pec, blink: bl, lid, look, finScale, k, paint, far: lod === 'far', sil: silColor, V: palette};
	const body = view === 'front' ? <Front {...common} /> : view === 'below' ? <Below {...common} /> : <Side {...common} />;
	if (!cast) return body;
	const box = VIEW_BOX[view];
	const cx = box[0] + box[2] / 2;
	const lift = clamp(cast.lift ?? 0.6);
	return (
		<g>
			<ellipse cx={cx} cy={cast.y} rx={box[2] * (0.42 + 0.2 * lift)} ry={18 + 30 * lift} fill={paint(palette.dark)} opacity={0.45 * (1 - 0.5 * lift)} />
			{body}
		</g>
	);
};

type ViewProps = React.ComponentProps<typeof Side>;

/** small dark eye + one glint; blink squashes it to a lid line */
const SmallEye: React.FC<{x: number; y: number; r: number; shut: number; look: Pt; paint: Paint; V: Palette; far: boolean; lidColor: string}> = ({x, y, r, shut, look, paint, V, far, lidColor}) => (
	<g>
		<ellipse cx={x} cy={y} rx={r} ry={Math.max(0.8, r * (1 - shut))} fill={paint(V.eye)} />
		{shut < 0.55 && !far ? <circle cx={x + 0.12 * r + look[0] * 0.3 * r} cy={y - 0.3 * r + look[1] * 0.3 * r} r={r * 0.33} fill={paint(V.glint)} /> : null}
		{shut > 0.6 ? <path d={`M ${x - r} ${y} Q ${x} ${y + r * 0.45} ${x + r} ${y}`} stroke={paint(lidColor)} strokeWidth={r * 0.28} fill="none" strokeLinecap="round" /> : null}
	</g>
);

const simpleTeeth = (pts: Pt[], n: number, h: number, w: number, inward: (p: Pt) => Pt, paint: Paint, V: Palette, key: string) =>
	Array.from({length: n}, (_, i) => {
		const f = ((i + 0.5) / n) * (pts.length - 1);
		const j = Math.min(pts.length - 2, Math.floor(f));
		const u = f - j;
		const x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * u;
		const y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * u;
		const [nx, ny] = inward([x, y]);
		const tx = -ny;
		const ty = nx;
		return (
			<g key={key + i}>
				<path d={`M ${x - tx * w} ${y - ty * w} L ${x + nx * h} ${y + ny * h} L ${x + tx * w} ${y + ty * w} Z`} fill={paint(V.tooth)} />
				<path d={`M ${x} ${y} L ${x + nx * h} ${y + ny * h} L ${x + tx * w} ${y + ty * w} Z`} fill={paint(V.toothShade)} />
			</g>
		);
	});

// ================================================================================== FRONT (head-on, approaching)
const FG = geom.front as unknown as {
	parts: Record<string, string>;
	smile: Pt[];
	eyes: Pt[];
	pivots: Record<'flipL' | 'flipR' | 'dorsalBase', Pt>;
	cx: number;
	box: Box;
};
const FRONT_BASE_Y = 330;

const Front: React.FC<ViewProps> = ({id, t, amp, freq, jaw, pec, blink, lid, look, finScale, k, paint, far, sil, V}) => {
	const FP = FG.parts;
	const col = (h: string) => sil ?? paint(h);
	const flat = far || !!sil;
	const ph = 2 * Math.PI * freq * t;
	const m = amp > 0 ? Math.min(1.4, amp) : 0;
	// the tail beat is hidden behind the head: it shows as a bob, a lateral fin sway and flipper follow-through
	const bob = 7 * m * Math.sin(ph);
	const sway = 10 * m * Math.sin(ph - 1.3);
	const flap = 6 * m * Math.sin(ph - 0.9) + pec;
	const cx = FG.cx;
	const dorsalF: F = (x, y) => {
		if (y >= FRONT_BASE_Y) return [x, y];
		const yy = FRONT_BASE_Y - (FRONT_BASE_Y - y) * finScale;
		const h = clamp((FRONT_BASE_Y - yy) / (240 * finScale));
		return [x + sway * Math.pow(h, 1.5), yy];
	};
	const flipW = (o: Pt) => (x: number, y: number) => smooth(20, 130, Math.hypot(x - o[0], y - o[1]));
	const flipLF = rotW(FG.pivots.flipL, flap, flipW(FG.pivots.flipL)); // + = tips up
	const flipRF = rotW(FG.pivots.flipR, -flap, flipW(FG.pivots.flipR));
	// jaw: the head below the smile drops, full in the middle, zero at the mouth corners
	const drop = 70 * clamp(jaw, 0, 1.15);
	const open = drop > 0.5;
	const sx = FG.smile.map((p) => p[0]);
	const half = (sx[sx.length - 1] - sx[0]) / 2;
	const jw = (x: number) => smooth(half, half * 0.55, Math.abs(x - cx));
	const jawF: F = (x, y) => [x, y + drop * jw(x)];
	const sl = (r: number) => (flat ? undefined : slide(k, r));
	const headLayers = (f?: F, pre = `${id}-h`) =>
		sil ? null : (
			<>
				{flat ? null : <path d={warp(FP.band, f)} fill={paint(V.dark)} fillRule="evenodd" transform={sl(24)} />}
				<path d={warp(FP.saddle, f)} fill={paint(V.saddle)} />
				<path d={warp(FP.eyePatch, f)} fill={paint(V.white)} />
				<clipPath id={`${pre}-cc`}>
					<path d={warp(FP.chin, f)} />
				</clipPath>
				<path d={warp(FP.chin, f)} fill={paint(V.white)} />
				{flat ? null : <path d={warp(FP.chinShadow, f)} fill={paint(V.whiteShade)} fillRule="evenodd" transform={sl(18)} clipPath={`url(#${pre}-cc)`} />}
			</>
		);
	const up = FG.smile;
	const lo = FG.smile.map(([x, y]) => jawF(x, y));
	const gap = `${ptsPath(up)} L ${lo
		.slice()
		.reverse()
		.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`)
		.join(' L ')} Z`;
	const mouth =
		open && !sil ? (
			<g>
				<clipPath id={`${id}-gap`}>
					<path d={gap} />
				</clipPath>
				<path d={gap} fill={paint(V.mouth)} />
				<ellipse cx={cx} cy={lo[Math.floor(lo.length / 2)][1] + 4} rx={half * 0.55} ry={drop * 0.45} fill={paint(V.tongue)} clipPath={`url(#${id}-gap)`} />
				{simpleTeeth(up.slice(3, -3), 10, 15 * clamp(jaw * 2.2), 6, () => [0, 1], paint, V, 'u')}
				{simpleTeeth(lo.slice(3, -3), 10, 13 * clamp(jaw * 2.2), 5.5, () => [0, -1], paint, V, 'l')}
			</g>
		) : null;
	const shut = clamp(Math.max(blink, lid * 0.6));
	return (
		<g transform={`translate(0 ${bob.toFixed(2)})`}>
			<FlatPart id={`${id}-do`} d={warp(FP.dorsal, dorsalF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(FP.dorsalDark, dorsalF), fill: col(V.dark), slide: sl(20)}]} />
			<FlatPart id={`${id}-hd`} d={FP.head} base={col(V.lit)}>
				{headLayers()}
			</FlatPart>
			{mouth}
			{open ? (
				<FlatPart id={`${id}-jw`} d={warp(FP.jaw, jawF)} base={col(V.lit)}>
					{headLayers(jawF, `${id}-jw`)}
				</FlatPart>
			) : null}
			{sil ? null : FG.eyes.map(([x, y], i) => <SmallEye key={i} x={x} y={y} r={8.5} shut={shut} look={look} paint={paint} V={V} far={far} lidColor={V.lit} />)}
			<FlatPart id={`${id}-fL`} d={warp(FP.flipL, flipLF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(FP.flipLDark, flipLF), fill: col(V.dark), slide: sl(20)}]} />
			<FlatPart id={`${id}-fR`} d={warp(FP.flipR, flipRF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(FP.flipRDark, flipRF), fill: col(V.dark), slide: sl(20)}]} />
		</g>
	);
};

// ================================================================================== BELOW (from underneath, rising)
const BG_ = geom.below as unknown as {
	parts: Record<string, string>;
	eyes: Pt[];
	jawRim: Pt[];
	pivots: {flipL: Pt; flipR: Pt; flukeRoot: Pt; hingeY: number; head: Pt; tail: Pt};
	cx: number;
	box: Box;
};

const Below: React.FC<ViewProps> = ({id, t, amp, freq, jaw, pec, blink, lid, look, k, paint, far, sil, V}) => {
	const BP = BG_.parts;
	const col = (h: string) => sil ?? paint(h);
	const flat = far || !!sil;
	const ph = 2 * Math.PI * freq * t;
	const m = amp > 0 ? Math.min(1.4, amp) : 0;
	const cx = BG_.cx;
	const [, headY] = BG_.pivots.head;
	const [, tailY] = BG_.pivots.tail;
	// seen from below the vertical tail beat runs along the view axis: a travelling widen/narrow (nearer = wider)
	// down the tail, and the flukes foreshorten as they pitch
	const body: F = (x, y) => {
		const s = clamp((y - (headY + 0.42 * (tailY - headY))) / (0.58 * (tailY - headY)));
		const w = 1 + 0.07 * m * s * s * Math.sin(ph - 2.4 * s);
		return [cx + (x - cx) * w, y];
	};
	const [fx, fy] = BG_.pivots.flukeRoot;
	const pitch = Math.sin(ph - 2.9);
	const flukeF = chain((x, y) => {
		const wgt = smooth(0, 40, y - fy);
		const sy = 1 - wgt * 0.3 * m * (0.5 + 0.5 * pitch);
		const sx = 1 + wgt * 0.05 * m * pitch;
		return [fx + (x - fx) * sx, fy + (y - fy) * sy];
	}, body);
	const flap = 6 * m * Math.sin(ph - 0.9) + pec;
	const fw = (o: Pt) => (x: number, y: number) => smooth(20, 120, Math.hypot(x - o[0], y - o[1]));
	const flipLF = chain(rotW(BG_.pivots.flipL, -flap, fw(BG_.pivots.flipL)), body); // + = tips forward (toward the head)
	const flipRF = chain(rotW(BG_.pivots.flipR, flap, fw(BG_.pivots.flipR)), body);
	// jaw: from below, an opening lower jaw swings toward the camera, so it shortens toward the hinge and the palate
	// (mouth colour + upper tooth row) shows beyond its tip
	const hy = BG_.pivots.hingeY;
	const jawK = 0.38 * clamp(jaw, 0, 1.15);
	const open = jawK > 0.004;
	const jawF: F = (x, y) => (y >= hy ? [x, y] : [x, y + (hy - y) * jawK * smooth(0, 45, hy - y)]);
	const sl = (r: number) => (flat ? undefined : slide(k, r));
	const shut = clamp(Math.max(blink, lid * 0.6));
	const rim = BG_.jawRim;
	const inward = ([x, y]: Pt): Pt => {
		const dx = cx - x;
		const dy = hy - 40 - y;
		const l = Math.hypot(dx, dy) || 1;
		return [dx / l, dy / l];
	};
	return (
		<g transform={`translate(0 ${(-5 * m * Math.sin(ph)).toFixed(2)})`}>
			<FlatPart id={`${id}-fL`} d={warp(BP.flipL, flipLF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(BP.flipLDark, flipLF), fill: col(V.dark), slide: sl(20)}]} />
			<FlatPart id={`${id}-fR`} d={warp(BP.flipR, flipRF)} base={col(V.lit)} flat={flat} shadows={[{d: warp(BP.flipRDark, flipRF), fill: col(V.dark), slide: sl(20)}]} />
			<FlatPart id={`${id}-fk`} d={warp(BP.fluke, flukeF)} base={col(V.dark)} flat={flat}>
				{sil ? null : <path d={warp(BP.flukePale, flukeF)} fill={paint(V.whiteShade)} fillRule="evenodd" />}
			</FlatPart>
			{/* the underside faces away from the light: dark base; the lit head rim is its one other tone */}
			<FlatPart id={`${id}-bd`} d={warp(BP.body, body)} base={col(V.dark)}>
				{flat ? null : <path d={warp(BP.rim, body)} fill={paint(V.lit)} fillRule="evenodd" transform={sl(-14)} />}
				{sil ? null : <path d={warp(BP.white, body)} fill={paint(V.white)} />}
			</FlatPart>
			{open && !sil ? (
				<g>
					<clipPath id={`${id}-pal`}>
						<rect x={0} y={0} width={2000} height={hy - 4} />
					</clipPath>
					{/* palate only above the hinge row: below it the jaw never moves, so nothing may peek out at its edge */}
					<path d={BP.jaw} fill={paint(V.mouth)} clipPath={`url(#${id}-pal)`} />
					{simpleTeeth(rim.slice(2, -2), 16, 12 * clamp(jaw * 2.5), 5, inward, paint, V, 'u')}
					<FlatPart id={`${id}-jw`} d={warp(BP.jaw, jawF)} base={paint(V.white)} />
				</g>
			) : null}
			{sil ? null : BG_.eyes.map(([x, y], i) => <SmallEye key={i} x={x} y={y} r={6.5} shut={shut} look={look} paint={paint} V={V} far={far} lidColor={V.lit} />)}
		</g>
	);
};

export const VIEW_BOX: Record<'side' | 'front' | 'below', Box> = {side: ORCA_V3_BOX, front: FG.box, below: BG_.box};
