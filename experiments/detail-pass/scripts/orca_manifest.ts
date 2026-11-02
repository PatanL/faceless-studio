/**
 * Counts what the orca-opening frames hold, from the same layout data the scene renders: named objects in
 * frame per sampled time (each fish, sponge, boulder, kelp strand, ...), distinct kinds, and the hero's
 * surface marks (asset-gen path B marks, all drawn; lit-side ones get the lit tone). Run by orca_render.sh.
 */
import geom from '../../asset-gen/orca-b/orca_geom.json';
import {schoolPoses} from '../src/detail/schools';
import {BACK_KELP, CALM, CALM_SHARE, camAt, DUR, FAR_KELP, FAR_MOUNDS, FAR_REEF, FH, FORE_KELP, FRONT_REEF, FW, KIND_LABEL, MID_REEF, orcaPt, SCHOOLS_FAR, SCHOOLS_MID, SINGLES} from '../src/scenes/orcaLayout';

const DEPTH: Record<string, number> = {dist: 0.2, far: 0.3, back: 0.45, mid: 0.6, subject: 1, fore: 1.45};
const toScreen = (t: number, plane: string, x: number, y: number): [number, number] => {
	const cam = camAt(t);
	const d = DEPTH[plane];
	const z = 1 + (cam.zoom - 1) * d;
	const a = (cam.roll * d * Math.PI) / 180;
	const px = (x - FW / 2) * z;
	const py = (y - FH / 2) * z;
	return [FW / 2 - cam.x * d + px * Math.cos(a) - py * Math.sin(a), FH / 2 - cam.y * d + px * Math.sin(a) + py * Math.cos(a)];
};
const onScreen = ([x, y]: [number, number], m = 0) => x > -m && x < FW + m && y > -m && y < FH + m;
type Obj = {kind: string; plane: string; pts: [number, number][]};
const FISH = ['scad', 'grunt', 'lancer', 'wrasse'];

const objectsAt = (t: number): Obj[] => {
	const out: Obj[] = [];
	for (const m of FAR_MOUNDS) out.push({kind: 'mound', plane: 'far', pts: [[m.x, m.y - m.h * 0.5]]});
	for (const [list, plane] of [
		[FAR_REEF, 'far'],
		[MID_REEF, 'mid'],
		[FRONT_REEF, 'subject'],
	] as const)
		for (const p of list) out.push({kind: p.kind, plane, pts: [[p.x, p.y - Math.min(p.size, 200) * 0.4]]});
	for (const [list, plane] of [
		[FAR_KELP, 'dist'],
		[BACK_KELP, 'back'],
		[FORE_KELP, 'fore'],
	] as const)
		for (const k of list) out.push({kind: 'kelp', plane, pts: [0.2, 0.5, 0.85].map((f) => [k.x, k.y - k.h * f] as [number, number])});
	for (const [list, plane] of [
		[SCHOOLS_FAR, 'far'],
		[SCHOOLS_MID, 'mid'],
		[SINGLES, 'subject'],
	] as const)
		for (const s of list) for (const p of schoolPoses(s, t)) out.push({kind: s.species, plane, pts: [[p.x, p.y]]});
	out.push({kind: 'orca', plane: 'subject', pts: [orcaPt(t, 770, 515)]});
	if (t < 5.6) out.push({kind: 'diver', plane: 'subject', pts: [[930 - 10 * t, 1040]]});
	if (t > 6.55 && t < 8.2) for (let i = 0; i < 4; i++) out.push({kind: 'car', plane: 'subject', pts: [[545 + (i - 1.5) * 198, 1150]]});
	if (t >= 7.95) out.push({kind: 'you', plane: 'subject', pts: [orcaPt(t, 560, 381)]});
	return out;
};

const samples: Record<string, unknown>[] = [];
for (let t = 0; t <= DUR - 0.2; t += 0.5) {
	const vis = objectsAt(t).filter((o) => o.pts.some((p) => onScreen(toScreen(t, o.plane, p[0], p[1]), 10)));
	const kinds = new Set(vis.map((o) => KIND_LABEL[o.kind] ?? o.kind));
	const fish = vis.filter((o) => FISH.includes(o.kind)).length;
	samples.push({t, named_objects: vis.length, kinds: kinds.size, fish, set_dressing: vis.length - fish, kind_list: [...kinds].sort()});
}
const med = (xs: number[]) => xs.slice().sort((a, b) => a - b)[Math.floor(xs.length / 2)];
const marks = (geom as {marks: {kind: string; part: string}[]}).marks;
const by = (k: 'kind' | 'part') => marks.reduce<Record<string, number>>((a, m) => ((a[m[k]] = (a[m[k]] ?? 0) + 1), a), {});
console.log(
	JSON.stringify(
		{
			named_objects_median: med(samples.map((s) => s.named_objects as number)),
			named_objects_min: Math.min(...samples.map((s) => s.named_objects as number)),
			kinds_median: med(samples.map((s) => s.kinds as number)),
			hero_marks: {total: marks.length, by_kind: by('kind'), by_part: by('part'), source: 'asset-gen orca_geom.json (measured off the Codex reference)'},
			calm: {ellipse: CALM, share_of_frame: Number(CALM_SHARE.toFixed(3))},
			samples,
		},
		null,
		1,
	),
);
