/**
 * Counts what the showcase frames hold, from the same layout data the scene renders (no guessing by eye):
 * named objects in frame per sampled time (each fish, coral, sponge, rock, kelp strand, ...), distinct kinds,
 * hero surface marks by kind, and the calm-field share. Bundled with esbuild and run by scripts/render.sh.
 */
import {norm, type Vec} from '../../kurz-style/engine/src/lib/light';
import {countByKind} from '../src/detail/marks';
import {schoolPoses} from '../src/detail/schools';
import {heroMarks} from '../src/assets/turtleGeom';
import {CALM, CALM_SHARE, camAt, DUR, FAR_KELP, FAR_MOUNDS, FAR_REEF, FH, FORE_KELP, FRONT_REEF, FW, KIND_LABEL, lightAt, MID_KELP, MID_REEF, RAYS, SCHOOLS_FAR, SCHOOLS_MID, SINGLES, turtlePose} from '../src/scenes/layout';

const DEPTH: Record<string, number> = {field: 0.05, far: 0.3, mid: 0.6, subject: 1, fore: 1.45};

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
		[FAR_KELP, 'far'],
		[MID_KELP, 'mid'],
		[FORE_KELP, 'fore'],
	] as const)
		for (const k of list) out.push({kind: 'kelp', plane, pts: [0.2, 0.5, 0.85].map((f) => [k.x, k.y - k.h * f] as [number, number])});
	for (const [list, plane] of [
		[SCHOOLS_FAR, 'far'],
		[SCHOOLS_MID, 'mid'],
		[SINGLES, 'subject'],
	] as const)
		for (const s of list) for (const p of schoolPoses(s, t)) out.push({kind: s.species, plane, pts: [[p.x, p.y]]});
	for (const r of RAYS) out.push({kind: 'ray', plane: 'far', pts: [[r.x + 8 * t, r.y]]});
	const tp = turtlePose(t);
	out.push({kind: 'turtle', plane: 'subject', pts: [[tp.x + 300 * tp.s, tp.y + 200 * tp.s]]});
	return out;
};

const rotV = (v: Vec, deg: number): Vec => {
	const a = (-deg * Math.PI) / 180;
	return norm([v[0] * Math.cos(a) - v[1] * Math.sin(a), v[0] * Math.sin(a) + v[1] * Math.cos(a)]);
};

const samples: Record<string, unknown>[] = [];
for (let t = 0; t <= DUR - 0.25; t += 0.5) {
	const vis = objectsAt(t).filter((o) => o.pts.some((p) => onScreen(toScreen(t, o.plane, p[0], p[1]), 10)));
	const kinds = new Set(vis.map((o) => KIND_LABEL[o.kind] ?? o.kind));
	const byPlane = vis.reduce<Record<string, number>>((a, o) => ((a[o.plane] = (a[o.plane] ?? 0) + 1), a), {});
	const fish = vis.filter((o) => ['scad', 'anthias', 'grunt', 'lancer', 'tang', 'trunk', 'wrasse'].includes(o.kind)).length;
	samples.push({t, named_objects: vis.length, kinds: kinds.size, fish, set_dressing: vis.length - fish, by_plane: byPlane, kind_list: [...kinds].sort()});
}
const L0 = lightAt(0);
const tp0 = turtlePose(0);
const hm = heroMarks(rotV(L0.key, tp0.rot), rotV(L0.rim, tp0.rot));
const all = [...hm.shell, ...hm.head, ...hm.nearFront, ...hm.nearRear];
const med = (xs: number[]) => xs.slice().sort((a, b) => a - b)[Math.floor(xs.length / 2)];
console.log(
	JSON.stringify(
		{
			named_objects_median: med(samples.map((s) => s.named_objects as number)),
			kinds_median: med(samples.map((s) => s.kinds as number)),
			hero_marks: {total: all.length, clusters: [hm.shell, hm.head, hm.nearFront, hm.nearRear].reduce((a, ms) => a + new Set(ms.map((m) => m.cluster)).size, 0), by_part: {shell: hm.shell.length, head: hm.head.length, near_front_flipper: hm.nearFront.length, near_rear_flipper: hm.nearRear.length}, by_kind: countByKind(all), all_lit: true},
			calm: {ellipse: CALM, share_of_frame: Number(CALM_SHARE.toFixed(3))},
			samples,
		},
		null,
		1,
	),
);
