/**
 * Kit adapter for OrcaV3 (house style A). Copy to studio/src/kits/explainer/house/orcaV3Kit.tsx together with
 * OrcaV3.tsx and geom_v3.json (same folder). It is a drop-in for house/orca.tsx:
 *
 *   - `Orca` takes the same props as house/orca.tsx's Orca (id, t, amp, freq, lod, layers, rot, flip, cast, jaw, look,
 *     lid, detail, silColor, finScale) plus pec, blink, view ('side' | 'front' | 'below') and palette.
 *   - `ORCA_BOX` is the side view's drawing box (local px of the reference, snout tip to fluke tip = 8 m).
 *   - `houseOrcaV3(flat)` is the Figure, like houseOrca in house/figures.tsx, with poses front, head (= front),
 *     below, plus the flat kit drawing as pose "flat" (and its "top").
 *
 * The scene light (useLight) slides the flat shadow shapes; the layer transform (useLayerXf) keeps that light in screen
 * space; the plane tint (useTint) hazes every colour on far planes. Blinks are seeded like the kit's blinkAt.
 */
import React from 'react';
import type {Figure} from '../figure';
import {useLayerXf} from '../../../core/light';
import {useLight, useTint} from './light';
import {blinkAt} from './motion';
import {OrcaV3, ORCA_V3_BOX, VIEW_BOX, type OrcaV3Props, type Palette} from './OrcaV3';

export const ORCA_BOX = ORCA_V3_BOX;

export type KitOrcaProps = {
	id: string;
	t: number;
	amp?: number;
	freq?: number;
	lod?: 'hero' | 'far';
	/** accepted for compatibility with house/orca.tsx (the flat style has no layer stack) */
	layers?: unknown;
	rot?: number;
	flip?: boolean;
	cast?: {y: number; lift?: number};
	jaw?: number;
	look?: [number, number];
	lid?: number;
	/** accepted for compatibility (v3 is deliberately sparse: no secondary marks) */
	detail?: boolean;
	silColor?: string;
	finScale?: number;
	pec?: number;
	blink?: number;
	view?: OrcaV3Props['view'];
	palette?: Palette;
};

export const Orca: React.FC<KitOrcaProps> = ({id, t, rot = 0, flip = false, blink, layers: _l, detail: _d, ...rest}) => {
	const L = useLight();
	const tint = useTint();
	const layer = useLayerXf();
	return (
		<OrcaV3
			{...rest}
			id={id}
			t={t}
			light={{key: L.key}}
			rot={rot + layer.rotate}
			flip={flip !== layer.flipX}
			blink={blink ?? blinkAt(t, id)}
			tint={tint}
		/>
	);
};

const n = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const arr2 = (v: unknown, d: [number, number]): [number, number] =>
	Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number') ? (v as [number, number]) : d;

const drawView = (view: 'side' | 'front' | 'below'): Figure['draw'] => (c) => (
	<Orca
		id={c.id}
		view={view}
		t={c.idle ? c.t : 0}
		amp={c.idle ? c.amp : 0}
		freq={0.55 * c.speed}
		lod={c.sil ? 'far' : 'hero'}
		silColor={c.sil}
		jaw={Math.max(0, Math.min(1.1, n(c.p.jaw, 0)))}
		pec={n(c.p.pec, 0)}
		blink={typeof c.p.blink === 'number' ? c.p.blink : undefined}
		lid={n(c.p.lid, 0)}
		look={arr2(c.p.look, [0, 0])}
		finScale={n(c.p.finScale, 1)}
	/>
);

const pose = (view: 'front' | 'below', size: number, axis: 'w' | 'h') => ({box: VIEW_BOX[view], size, axis, selfShaded: true, draw: drawView(view)});

/** Figure for the kit registry (creature.tsx FIGURES.orca). Real size: 8 m snout to fluke. */
export const houseOrcaV3 = (flat: Figure): Figure => ({
	label: 'ORCA',
	box: ORCA_V3_BOX,
	size: 8,
	axis: 'w',
	selfShaded: true,
	poses: {
		...(flat.poses ?? {}),
		flat: {box: flat.box, size: flat.size, axis: flat.axis, draw: flat.draw},
		// head-on: flipper tip to flipper tip ~ 3.4 m (same as the kit's flat "head" pose); from below: 8 m long
		front: pose('front', 3.4, 'w'),
		head: pose('front', 3.4, 'w'),
		below: pose('below', 8, 'h'),
	},
	draw: drawView('side'),
});
