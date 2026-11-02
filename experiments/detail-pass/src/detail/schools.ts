/** School formation (pure): sunflower-spiral formation + seeded jitter, heading noise and drift. */
import {noise1, rand} from '../../../kurz-style/engine/src/lib/rng';

export type FishPose = {x: number; y: number; ang: number; len: number; t: number; phase: number; beat?: number};

export type SchoolSpec = {
	id: string;
	species: string;
	n: number;
	/** school centre at t = 0, screen/plane coordinates */
	x: number;
	y: number;
	/** heading in degrees (0 = right) */
	heading: number;
	speed: number;
	/** formation radii along / across the heading */
	rx: number;
	ry: number;
	/** mean fish length px */
	len: number;
	flat?: string;
};

/** fish positions of a school at time t (pure; the manifest uses it to count fish in frame) */
export const schoolPoses = (s: SchoolSpec, t: number): FishPose[] => {
	const h = (s.heading * Math.PI) / 180;
	const ux = Math.cos(h);
	const uy = Math.sin(h);
	const cx = s.x + ux * s.speed * t + 20 * noise1(`${s.id}cx`, t * 0.2);
	const cy = s.y + uy * s.speed * t + 14 * noise1(`${s.id}cy`, t * 0.25);
	const out: FishPose[] = [];
	for (let i = 0; i < s.n; i++) {
		// formation: sunflower spiral (even, organic) + seeded jitter
		const f = Math.sqrt((i + 0.5) / s.n);
		const a = i * 2.39996 + rand(s.id, i) * 0.6;
		const lx = Math.cos(a) * f * s.rx + (rand(s.id, i + 500) - 0.5) * s.len * 0.6 + 10 * noise1(`${s.id}${i}`, t * 0.5);
		const ly = Math.sin(a) * f * s.ry + (rand(s.id, i + 900) - 0.5) * s.len * 0.3 + 6 * noise1(`${s.id}y${i}`, t * 0.45);
		const x = cx + ux * lx - uy * ly;
		const y = cy + uy * lx + ux * ly;
		const ang = s.heading + 9 * noise1(`${s.id}a${i}`, t * 0.4);
		out.push({x, y, ang, len: s.len * (0.78 + rand(s.id, i + 300) * 0.44), t, phase: rand(s.id, i + 700) * 6.28, beat: 7 + rand(s.id, i + 800) * 4});
	}
	return out;
};

