/**
 * Sound made visible, house style A (flat bone arcs and dots, no blur): explainer-sperm-whale (lane B, 2026-11-02).
 *
 *   explainer/ClickRings  a click train as flat arcs leaving an emitter. The emitter sits at the middle of the box's
 *                         left edge (dir 1, rings travel right) or right edge (dir -1). Each click is one arc that grows
 *                         across the box in `life` s, thinning and fading as it goes.
 *                         props at, out (s: emission window), rate (clicks/s, number or [{t, v}] track: a rising rate
 *                         is the echolocation "buzz"), life (0.9 s), arc (half-angle deg, 38 = a beam; 90 = all round),
 *                         width (stroke px, 12), color (#e9f4fc), r0 (start radius px, 20), opacity (1)
 *   explainer/Coda        a coda (a social click pattern) as a row of dots appearing in rhythm, then the row clears and
 *                         repeats. props at, out, gaps ([s between clicks], e.g. [0.2, 0.2, 0.2, 0.4] = 1+1+1+2),
 *                         hold (s the full row stays, 0.6), r (dot px, 16), color, accent (last dot colour)
 */
import React from 'react';
import type {KitComponent} from '../../../core/registry';
import {registerComponent} from '../../../core/registry';
import {track} from '../util';

const num = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const str = (v: unknown, d: string) => (typeof v === 'string' ? v : d);

/** emission times in [at, min(t, out)] for a click rate (number or track), integrated at 120 Hz */
const emissions = (rate: unknown, at: number, out: number, t: number, life: number): number[] => {
	const res: number[] = [];
	const end = Math.min(t, out);
	if (end < at) return res;
	let ph = 0.999; // first click right at `at`
	const dt = 1 / 120;
	for (let s = at; s <= end + 1e-9; s += dt) {
		ph += Math.max(0, track(rate, s, 3)) * dt;
		if (ph >= 1) {
			ph -= 1;
			if (t - s < life) res.push(s);
		}
	}
	return res;
};

export const ClickRings: KitComponent = ({props: p, time, width, height}) => {
	const at = num(p.at, 0);
	const out = num(p.out, 1e6);
	const life = Math.max(0.1, num(p.life, 0.9));
	const dir = num(p.dir, 1) < 0 ? -1 : 1;
	const arc = (Math.max(5, Math.min(179, num(p.arc, 38))) * Math.PI) / 180;
	const w0 = num(p.width, 12);
	const r0 = num(p.r0, 20);
	const color = str(p.color, '#e9f4fc');
	const op = num(p.opacity, 1);
	const ox = dir > 0 ? 0 : width;
	const oy = height / 2;
	const rmax = Math.max(40, width - r0);
	const rings = emissions(p.rate, at, out, time, life).map((s, i) => {
		const u = (time - s) / life;
		const r = r0 + rmax * (1 - Math.pow(1 - u, 1.6));
		const a0 = dir > 0 ? -arc : Math.PI - arc;
		const a1 = dir > 0 ? arc : Math.PI + arc;
		const x0 = ox + r * Math.cos(a0), y0 = oy + r * Math.sin(a0);
		const x1 = ox + r * Math.cos(a1), y1 = oy + r * Math.sin(a1);
		const sweep = dir > 0 ? 1 : 1;
		return (
			<path
				key={i}
				d={`M ${x0.toFixed(1)} ${y0.toFixed(1)} A ${r.toFixed(1)} ${r.toFixed(1)} 0 0 ${sweep} ${x1.toFixed(1)} ${y1.toFixed(1)}`}
				stroke={color}
				strokeWidth={Math.max(2, w0 * (1 - 0.6 * u))}
				strokeLinecap="round"
				fill="none"
				opacity={op * Math.max(0, 1 - u) * Math.min(1, u * 8)}
			/>
		);
	});
	return (
		<svg width={width} height={height} style={{display: 'block', overflow: 'visible'}}>
			{rings}
		</svg>
	);
};

export const Coda: KitComponent = ({props: p, time, width, height}) => {
	const at = num(p.at, 0);
	const out = num(p.out, 1e6);
	const gaps = Array.isArray(p.gaps) ? (p.gaps as unknown[]).map((g) => num(g, 0.2)) : [0.2, 0.2, 0.2, 0.4];
	const hold = num(p.hold, 0.6);
	const r = num(p.r, 16);
	const color = str(p.color, '#e9f4fc');
	const accent = str(p.accent, color);
	if (time < at || time > out + 0.3) return null;
	const outFade = Math.max(0, Math.min(1, (out + 0.3 - time) / 0.3));
	const n = gaps.length + 1;
	const times = [0];
	for (const g of gaps) times.push(times[times.length - 1] + g);
	const cycle = times[n - 1] + hold + 0.25;
	const local = (time - at) % cycle;
	// dot x spacing follows the rhythm (a long gap is a wide space), the row centred in the box
	const span = Math.max(1e-6, times[n - 1]);
	const usable = Math.max(0, width - 2 * r - 8);
	const xs = times.map((s) => r + 4 + (usable * s) / span);
	return (
		<svg width={width} height={height} style={{display: 'block', overflow: 'visible'}} opacity={outFade}>
			{xs.map((x, i) => {
				const d = local - times[i];
				if (d < 0 || local > times[n - 1] + hold) return null;
				const k = d < 0.12 ? 0.6 + (0.4 * d) / 0.12 + 0.25 * Math.sin((d / 0.12) * Math.PI) : 1;
				// the finished row drifts up and fades over its last 0.3 s (never snaps off)
				const left = times[n - 1] + hold - local;
				const f = Math.max(0, Math.min(1, left / 0.3));
				return <circle key={i} cx={x} cy={height / 2 - (1 - f) * 18} r={r * k} fill={i === n - 1 ? accent : color} opacity={f} />;
			})}
		</svg>
	);
};

registerComponent('explainer/ClickRings', ClickRings);
registerComponent('explainer/Coda', Coda);
