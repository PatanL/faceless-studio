/**
 * The showcase set as DATA (pure): every placement, school, kelp grove, the calm field, the camera, the light
 * and the hero pose. The React scene maps this to generators; scripts/manifest.ts imports the same module to
 * count what each sampled frame actually holds (named objects in frame, kinds, fish, hero marks, calm share).
 */
import {calmShare, grove, scatterGround, type Calm, type KindSpec} from '../detail/scatter';
import type {SchoolSpec} from '../detail/schools';
import {cameraAt, ease} from '../../../kurz-style/engine/src/motion/motion';
import {dirDeg, type SceneLight} from '../../../kurz-style/engine/src/lib/light';

export const FW = 1080;
export const FH = 1920;
export const DUR = 4;

export const CALM: Calm = {cx: 540, cy: 800, rx: 420, ry: 545, feather: 0.22};
export const CALM_SHARE = calmShare(CALM, FW, FH);

export const lightAt = (t: number): SceneLight => {
	const keyAng = -122 + 8 * ease.drift(t / DUR);
	return {key: dirDeg(keyAng), keyColor: 'amber-5', rim: dirDeg(40), rimColor: 'tide-4', ambient: 'ink-2', ground: 'ochre-3', haze: 'tide-1'};
};

export const camAt = (t: number) =>
	cameraAt(t, {x: -30, y: 18, zoom: 1, roll: 0}, [{at: 0.2, dur: 3.6, to: {x: 32, y: -14, zoom: 1.05}, ease: ease.drift}], {zoomPerS: 0.004, xPerS: 4, hand: 3, seed: 'detail'});

export const turtlePose = (t: number) => ({x: 236 - 16 * t, y: 560 + 9 * Math.sin(t * 1.2), rot: -7 + 1.5 * Math.sin(t * 1.2 + 0.6), s: 0.95});

const edge = (x: number) => Math.min(1, Math.abs((2 * x) / FW - 1));

const ANCH_MID: KindSpec[] = [
	{kind: 'rock', w: 0.7, size: [100, 160], tall: 0.6},
	{kind: 'brain', w: 2, size: [60, 105], tall: 1},
	{kind: 'vase', w: 1.4, size: [140, 230], tall: 1},
	{kind: 'table', w: 1.4, size: [80, 135], tall: 0.6},
	{kind: 'branch', w: 1.1, size: [150, 250], tall: 1},
];
const SAT_MID: KindSpec[] = [
	{kind: 'tubes', w: 1.4, size: [80, 160], tall: 1},
	{kind: 'ball', w: 1.2, size: [18, 36], tall: 2},
	{kind: 'soft', w: 1.3, size: [60, 120], tall: 1},
	{kind: 'grass', w: 1, size: [40, 85], tall: 1},
	{kind: 'urchin', w: 0.8, size: [11, 18], tall: 2},
	{kind: 'star', w: 0.7, size: [15, 24], tall: 1},
	{kind: 'shell', w: 0.7, size: [0.9, 1.4], tall: 1},
	{kind: 'rock', w: 0.3, size: [40, 70], tall: 0.6},
];

/** back reef rows (mid plane) */
export const MID_REEF = scatterGround({
	seed: 'midreef',
	plane: 'mid',
	x0: -140,
	x1: FW + 140,
	groundY: (x) => 1500 - 120 * edge(x) ** 2,
	depth: 200,
	anchors: 8,
	satellites: [2, 3],
	singles: 6,
	anchorKinds: ANCH_MID,
	satKinds: SAT_MID,
	edgeBias: 0.65,
	calm: CALM,
});

/** front reef row (subject plane, full contrast, larger) */
export const FRONT_REEF = scatterGround({
	seed: 'frontreef',
	plane: 'subject',
	x0: -160,
	x1: FW + 160,
	groundY: (x) => 1790 - 90 * edge(x) ** 2,
	depth: 200,
	anchors: 6,
	satellites: [1, 2],
	singles: 6,
	anchorKinds: ANCH_MID.map((k) => ({...k, w: k.kind === 'branch' ? 0.3 : k.w, size: [k.size[0] * 1.35, k.size[1] * 1.35] as [number, number]})),
	satKinds: SAT_MID.map((k) => ({...k, size: (k.kind === 'shell' ? [1.2, 1.8] : [k.size[0] * 1.3, k.size[1] * 1.3]) as [number, number]})),
	edgeBias: 0.55,
	calm: CALM,
	gap: 0.7,
});

/** far reef silhouettes (far plane) */
export const FAR_MOUNDS = [
	{seed: 'm1', x: 120, y: 1400, w: 620, h: 210, base: 'tide-1'},
	{seed: 'm2', x: 760, y: 1420, w: 720, h: 170, base: 'tide-1'},
	{seed: 'm3', x: 1160, y: 1380, w: 420, h: 260, base: 'tide-1'},
];
export const FAR_REEF = scatterGround({
	seed: 'farreef',
	plane: 'far',
	x0: -140,
	x1: FW + 140,
	groundY: (x) => 1330 - 70 * edge(x),
	depth: 60,
	anchors: 9,
	satellites: [1, 3],
	singles: 6,
	anchorKinds: [
		{kind: 'branch', w: 2, size: [110, 190]},
		{kind: 'vase', w: 1, size: [90, 150]},
		{kind: 'table', w: 1, size: [60, 100], tall: 0.6},
		{kind: 'brain', w: 1, size: [40, 70]},
	],
	satKinds: [
		{kind: 'tubes', w: 1, size: [60, 110]},
		{kind: 'soft', w: 1, size: [50, 90]},
		{kind: 'grass', w: 1, size: [30, 60]},
	],
	edgeBias: 0.4,
	calm: {...CALM, ry: CALM.ry * 0.9},
	gap: 0.6,
});

export const MID_KELP = [...grove('kl', -10, 1440, 3, [560, 1000], 120, 7), ...grove('kr', 1100, 1440, 3, [480, 900], 120, -9)];
export const FAR_KELP = [...grove('fkl', 250, 1360, 3, [260, 460], 90, 4), ...grove('fkr', 900, 1370, 3, [300, 520], 120, -5)];
export const FORE_KELP = [...grove('gl', -110, 2150, 2, [560, 760], 60, 8), ...grove('gr', 1200, 2150, 2, [480, 680], 50, -10)];

export const SCHOOLS_MID: SchoolSpec[] = [
	{id: 'scadA', species: 'scad', n: 26, x: 930, y: 230, heading: 196, speed: 24, rx: 170, ry: 70, len: 44},
	{id: 'anthB', species: 'anthias', n: 24, x: 150, y: 1330, heading: 12, speed: 16, rx: 150, ry: 62, len: 30},
	{id: 'gruntC', species: 'grunt', n: 9, x: 930, y: 1360, heading: 176, speed: 14, rx: 120, ry: 50, len: 60},
	{id: 'lancD', species: 'lancer', n: 10, x: 110, y: 420, heading: -8, speed: 20, rx: 110, ry: 46, len: 84},
];
export const SCHOOLS_FAR: SchoolSpec[] = [
	{id: 'farA', species: 'scad', n: 36, x: 140, y: 1000, heading: 4, speed: 10, rx: 120, ry: 60, len: 22, flat: 'tide-0'},
	{id: 'farB', species: 'anthias', n: 22, x: 1000, y: 900, heading: 186, speed: 9, rx: 90, ry: 50, len: 18, flat: 'tide-0'},
];
/** single fish on the subject plane: species, x, y, heading, len */
export const SINGLES: SchoolSpec[] = [
	{id: 'tang1', species: 'tang', n: 2, x: 990, y: 1170, heading: 170, speed: 12, rx: 60, ry: 40, len: 88},
	{id: 'trunk1', species: 'trunk', n: 1, x: 110, y: 1190, heading: 8, speed: 8, rx: 1, ry: 1, len: 62},
	{id: 'wrasse1', species: 'wrasse', n: 3, x: 560, y: 1600, heading: -170, speed: 20, rx: 110, ry: 30, len: 58},
];
export const RAYS = [{seed: 'ray1', x: 150, y: 240, s: 0.9, ang: 8}];

export const KIND_LABEL: Record<string, string> = {
	rock: 'rock',
	brain: 'brain coral',
	vase: 'vase sponge',
	table: 'table coral',
	branch: 'antler coral',
	tubes: 'tube sponges',
	ball: 'ball sponge',
	soft: 'finger coral',
	grass: 'sea grass',
	urchin: 'urchin',
	star: 'sea star',
	shell: 'shell',
	kelp: 'kelp',
	mound: 'far reef',
	ray: 'eagle ray',
	scad: 'scad',
	anthias: 'anthias',
	grunt: 'grunt',
	lancer: 'lancer',
	tang: 'tang',
	trunk: 'trunkfish',
	wrasse: 'wrasse',
	turtle: 'sea turtle',
};
