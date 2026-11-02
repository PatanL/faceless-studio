/**
 * House-style figures that replace kit drawings by default (the "Lantern & Ink" look). Each keeps the kit Figure
 * contract (box, real size, draw(ctx) facing right), so storyboards, pxPerM scale shots and the staging checker work
 * unchanged. They shade themselves through <Shaded> (selfShaded), so the generic stack (shadeFigure.tsx) skips them.
 *
 *   orca   engine hero orca (experiments/kurz-style/engine): 15+ parts, jaw rig, house eye, rake scars, follow-through
 *          flippers. Props: jaw (0..1 open), detail (secondary forms, default true), lid, look [x, y], finScale, speed,
 *          amp, idle, silhouette. The previous flat kit orca stays available as pose "flat".
 */
import React from 'react';
import type {Figure} from '../figure';
import {num, bool} from '../util';
import {Orca, ORCA_BOX} from './orca';

const arr2 = (v: unknown, d: [number, number]): [number, number] =>
	Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number') ? (v as [number, number]) : d;

export const houseOrca = (flat: Figure): Figure => ({
	label: 'ORCA',
	box: ORCA_BOX,
	size: 8,
	axis: 'w',
	selfShaded: true,
	poses: {...(flat.poses ?? {}), flat: {box: flat.box, size: flat.size, axis: flat.axis, draw: flat.draw}},
	draw: (c) => (
		<Orca
			id={c.id}
			t={c.idle ? c.t : 0}
			amp={c.idle ? c.amp : 0}
			freq={0.55 * c.speed}
			lod={c.sil ? 'far' : 'hero'}
			silColor={c.sil}
			jaw={Math.max(0, Math.min(1.1, num(c.p.jaw, 0)))}
			detail={bool(c.p.detail, true)}
			lid={num(c.p.lid, 0.28)}
			look={arr2(c.p.look, [0.4, 0.1])}
			finScale={num(c.p.finScale, 1)}
		/>
	),
});
