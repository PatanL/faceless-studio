/**
 * Orca opening (detail pass) as DATA (pure): the cold-water kelp-forest set, schools, camera, light, orca pose
 * and the hero's anchor points. The React scene (OrcaOpenDetail.tsx) maps this to generators; the manifest
 * script (scripts/orca_manifest.ts) imports the same module to count what each sampled frame holds.
 *
 * Timing, beats, camera moves and captions are the approved v3 opening's (kurz-style/engine/src/scenes/
 * OrcaOpen.tsx), so the two clips are a fair A/B: same narration mix, same beats, same framing.
 *
 * Setting (FEEDBACK 2026-11-01, logical consistency): orcas hunt in cold, temperate water, so the set is a
 * kelp forest over a rocky reef, not a tropical coral reef: giant kelp columns to the surface, boulders with
 * coralline-algae crusts, sponges, cold-water soft corals and red gorgonians, plumose anemones, urchins, sea
 * stars, shells and surfgrass; herring (their prey), surfperch, kelp wrasse and sand lance; a distant pod. No
 * jellies, no tropical stony corals.
 */
import {calmShare, grove, scatterGround, type Calm, type KindSpec} from '../detail/scatter';
import type {SchoolSpec} from '../detail/schools';
import {cameraAt, clamp, ease, prog, springAt, SETTLE, type Cam} from '../../../kurz-style/engine/src/motion/motion';
import {dirDeg, type SceneLight} from '../../../kurz-style/engine/src/lib/light';

export const FW = 1080;
export const FH = 1920;
export const FPS = 30;
export const FRAMES = 292; // 9.733 s, identical to ORCA_OPEN_FRAMES (v3)
export const DUR = FRAMES / FPS;

// ------------------------------------------------------------------ light and camera (v3 values)
export const keyAngAt = (t: number) => -118 + 8 * ease.drift(t / 9.7);
export const lightAt = (t: number): SceneLight => ({key: dirDeg(keyAngAt(t)), keyColor: 'amber-5', rim: dirDeg(42), rimColor: 'tide-4', ambient: 'ink-2', ground: 'ochre-2', haze: 'tide-1'});

export const focus = (X: number, Y: number, z: number): Cam => ({x: z * (X - 540), y: z * (Y - 960), zoom: z, roll: 0});
export const camAt = (t: number) =>
	cameraAt(
		t,
		focus(790, 1000, 1.62),
		[
			{at: 0.3, dur: 2.3, to: focus(540, 905, 1.0), ease: ease.drift}, // A: pull-back reveal
			{at: 3.1, dur: 0.9, to: focus(880, 965, 2.0), ease: ease.travel}, // B: push-in on the head
			{at: 4.42, dur: 1.15, to: focus(548, 1000, 1.1), ease: ease.travel}, // C: scale board
			{at: 7.7, dur: 1.15, to: focus(560, 760, 1.5), ease: ease.travel}, // D: up to the fin
		],
		{zoomPerS: 0.005, xPerS: 3, hand: 2.5, seed: 'oo', steady: 0.4},
	);
export const toScreen = (cam: Cam, x: number, y: number): [number, number] => [540 - cam.x + cam.zoom * (x - 540), 960 - cam.y + cam.zoom * (y - 960)];

// ------------------------------------------------------------------ the hero orca (asset-gen path B geometry)
/** OrcaB local space is the 1536x1024 reference; snout (1512, 515), fluke tip (23, 578), dorsal tip (780, 48) */
export const SB = 0.53;
export const PIV: [number, number] = [770, 515];
/** v3 placement, re-solved so OrcaB covers the same screen span as the engine orca (152..932 px, midline 860) */
export const orcaPose = (t: number) => {
	const jaw = springAt(t, 3.45, SETTLE) * (1 - ease.drift(prog(t, 4.3, 0.45)));
	const antic = t > 3.22 && t < 3.45 ? Math.sin(Math.PI * prog(t, 3.22, 0.23)) : 0;
	const ox = 140 + 6 * t;
	const oy = 586 + 8 * Math.sin(t * 1.1) + 6 * antic;
	const pitch = -2 + 1.5 * Math.cos(t * 1.1) - 5 * jaw + 1.8 * antic;
	const menace = clamp(prog(t, 3.25, 0.25)) * (1 - prog(t, 4.5, 0.4));
	return {jaw, antic, ox, oy, pitch, menace, amp: 22, freq: 0.55};
};
/** OrcaB's swim wave (same formula as asset-gen/orca-b/OrcaB.tsx makeBend), for anchor points */
const HX = 1505;
const TX = 23;
export const orcaPt = (t: number, lx: number, ly: number): [number, number] => {
	const p = orcaPose(t);
	const s = Math.min(1, Math.max(0, (HX - lx) / (HX - TX)));
	const by = ly + p.amp * (s * s + 0.04) * Math.sin(2 * Math.PI * p.freq * t - 2.4 * s);
	const pcx = p.ox + PIV[0] * SB;
	const pcy = p.oy + PIV[1] * SB;
	const x = p.ox + lx * SB - pcx;
	const y = p.oy + by * SB - pcy;
	const pv = (p.pitch * Math.PI) / 180;
	return [pcx + x * Math.cos(pv) - y * Math.sin(pv), pcy + x * Math.sin(pv) + y * Math.cos(pv)];
};
export const ORCA_ANCHORS = {flukeTip: [23, 578], snout: [1512, 515], finTip: [780, 50], finMid: [835, 200], foot: [560, 381], head: [1300, 470]} as const;

// ------------------------------------------------------------------ set
const edge = (x: number) => Math.min(1, Math.abs((2 * x) / FW - 1));
/** the hero swims through open water: nothing tall may poke into this ellipse (subject-plane coordinates) */
export const CALM: Calm = {cx: 545, cy: 840, rx: 470, ry: 560, feather: 0.2};
export const CALM_SHARE = calmShare(CALM, FW, FH);

const ANCH: KindSpec[] = [
	{kind: 'rock', w: 2.6, size: [110, 175], tall: 0.6},
	{kind: 'vase', w: 1.0, size: [130, 210], tall: 1},
	{kind: 'soft', w: 1.1, size: [110, 170], tall: 1},
	{kind: 'branch', w: 0.6, size: [150, 230], tall: 1},
];
const SAT: KindSpec[] = [
	{kind: 'tubes', w: 0.8, size: [70, 130], tall: 1},
	{kind: 'ball', w: 0.9, size: [18, 32], tall: 2},
	{kind: 'soft', w: 0.9, size: [50, 90], tall: 1},
	{kind: 'anemone', w: 1.2, size: [34, 56], tall: 1},
	{kind: 'grass', w: 1.1, size: [40, 85], tall: 1},
	{kind: 'urchin', w: 1.3, size: [11, 17], tall: 2},
	{kind: 'star', w: 1.0, size: [15, 24], tall: 1},
	{kind: 'shell', w: 0.5, size: [0.9, 1.3], tall: 1},
	{kind: 'rock', w: 0.9, size: [40, 75], tall: 0.6},
];

/** back reef (mid plane, depth 0.6) */
export const MID_REEF = scatterGround({
	seed: 'oo-mid',
	plane: 'mid',
	x0: -150,
	x1: FW + 150,
	groundY: (x) => 1560 - 110 * edge(x) ** 2,
	depth: 190,
	anchors: 6,
	satellites: [1, 3],
	singles: 4,
	anchorKinds: ANCH,
	satKinds: SAT,
	edgeBias: 0.6,
	calm: {...CALM, cy: CALM.cy - 60},
});

/** front reef row (subject plane, full contrast, larger) */
export const FRONT_REEF = scatterGround({
	seed: 'oo-front',
	plane: 'subject',
	x0: -170,
	x1: FW + 170,
	groundY: (x) => 1810 - 80 * edge(x) ** 2,
	depth: 170,
	anchors: 6,
	satellites: [1, 2],
	singles: 5,
	anchorKinds: ANCH.map((k) => ({...k, w: k.kind === 'branch' ? 0.25 : k.kind === 'rock' ? 1.6 : k.w, size: (k.kind === 'rock' ? [90, 135] : [k.size[0] * 1.3, k.size[1] * 1.3]) as [number, number]})),
	satKinds: SAT.map((k) => ({...k, size: (k.kind === 'shell' ? [1.2, 1.7] : [k.size[0] * 1.25, k.size[1] * 1.25]) as [number, number]})),
	edgeBias: 0.55,
	calm: CALM,
	gap: 0.75,
});

/** far ridge silhouettes and far rocky outcrops (far plane, depth 0.3) */
export const FAR_MOUNDS = [
	{seed: 'om1', x: 140, y: 1440, w: 680, h: 230, base: 'tide-1'},
	{seed: 'om2', x: 780, y: 1460, w: 760, h: 180, base: 'tide-1'},
	{seed: 'om3', x: 1180, y: 1420, w: 460, h: 280, base: 'tide-1'},
];
export const FAR_REEF = scatterGround({
	seed: 'oo-far',
	plane: 'far',
	x0: -150,
	x1: FW + 150,
	groundY: (x) => 1370 - 70 * edge(x),
	depth: 60,
	anchors: 8,
	satellites: [1, 2],
	singles: 5,
	anchorKinds: [
		{kind: 'rock', w: 2, size: [70, 120], tall: 0.6},
		{kind: 'vase', w: 1, size: [80, 130]},
		{kind: 'soft', w: 1, size: [70, 110]},
	],
	satKinds: [
		{kind: 'grass', w: 1, size: [30, 60]},
		{kind: 'soft', w: 1, size: [40, 70]},
		{kind: 'tubes', w: 0.6, size: [50, 90]},
	],
	edgeBias: 0.45,
	calm: {...CALM, ry: CALM.ry * 0.85},
	gap: 0.6,
});

/** giant kelp: columns that reach the surface on the far and back planes, frame-edge groves on mid/fore */
export const FAR_KELP = [...grove('ofk1', 150, 1400, 2, [1150, 1400], 110, 2), ...grove('ofk2', 950, 1410, 2, [1150, 1450], 110, -3)];
export const BACK_KELP = [...grove('obk1', -60, 1500, 2, [1300, 1600], 80, 3), ...grove('obk2', 1140, 1500, 2, [1250, 1550], 80, -4)];
export const FORE_KELP = [...grove('ofg1', -110, 2160, 2, [900, 1200], 60, 7), ...grove('ofg2', 1200, 2160, 2, [700, 1000], 50, -9)];

/** herring (prey), surfperch, kelp wrasse, sand lance */
export const SCHOOLS_MID: SchoolSpec[] = [
	{id: 'herA', species: 'scad', n: 24, x: 930, y: 300, heading: 192, speed: 26, rx: 210, ry: 82, len: 40},
	{id: 'perchB', species: 'grunt', n: 8, x: 140, y: 1330, heading: 8, speed: 14, rx: 120, ry: 48, len: 56},
	{id: 'lanceC', species: 'lancer', n: 10, x: 120, y: 560, heading: -6, speed: 22, rx: 120, ry: 52, len: 70},
];
export const SCHOOLS_FAR: SchoolSpec[] = [
	{id: 'oFarA', species: 'scad', n: 30, x: 260, y: 1040, heading: 4, speed: 10, rx: 160, ry: 70, len: 20, flat: 'tide-0'},
	{id: 'oFarB', species: 'scad', n: 20, x: 980, y: 860, heading: 186, speed: 9, rx: 100, ry: 46, len: 17, flat: 'tide-0'},
];
export const SINGLES: SchoolSpec[] = [
	{id: 'wrasse1', species: 'wrasse', n: 3, x: 900, y: 1640, heading: -172, speed: 18, rx: 100, ry: 34, len: 62},
	{id: 'perch2', species: 'grunt', n: 2, x: 120, y: 1560, heading: 10, speed: 10, rx: 50, ry: 30, len: 70},
];
/** the distant pod (far plane), as in v3 */
export const POD = [0, 1, 2].map((i) => ({i, x: 560 + i * 150, y: 470 + i * 50 + (i === 1 ? 26 : 0), s: 0.16 - i * 0.02, dt: i * 0.7}));

export const KIND_LABEL: Record<string, string> = {
	rock: 'boulder',
	vase: 'vase sponge',
	soft: 'soft coral',
	branch: 'red gorgonian',
	tubes: 'tube sponges',
	ball: 'ball sponge',
	anemone: 'plumose anemone',
	grass: 'surfgrass',
	urchin: 'urchin',
	star: 'sea star',
	shell: 'shell',
	kelp: 'giant kelp',
	mound: 'far ridge',
	scad: 'herring',
	grunt: 'surfperch',
	lancer: 'sand lance',
	wrasse: 'kelp wrasse',
	pod: 'far orca',
	orca: 'orca',
	diver: 'diver',
	car: 'car',
	you: 'YOU figure',
};
