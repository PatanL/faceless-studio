/**
 * Hero scuba diver (ported from experiments/kurz-style/engine/src/assets/Diver.tsx, the orca_open_v3 diver) ("YOU" in the orca shot), swimming horizontally, head to the RIGHT in local space
 * (mirror with flip). Drawn fresh: dusk wetsuit with a coral side stripe and BCD, amber tank, coral fins with
 * ink foot pockets, tide mask glass. Proportions: torso 0.6 m : legs 0.9 m : fins 0.55 m.
 *
 * Motion: alternating flutter kick from the hip (knee and ankle lag the thigh, fin lags the ankle = follow-
 * through), body bob, a wave gesture with anticipation + overshoot (motion.anticipate), hand lagging the forearm.
 */
import React from 'react';
import {c, mixOk, shadowOf} from './color';
import {taper} from './geom';
import {useLight, useTint} from './light';
import {Shaded, type Layers} from './Shaded';
import {anticipate, clamp, lerp} from './motion';

type P = [number, number];

const limb = (a: P, b: P, cpt: P, w0: number, w1: number): string => {
	const pts: P[] = [];
	for (let i = 0; i <= 6; i++) {
		const s = i / 6;
		pts.push([
			(1 - s) * (1 - s) * a[0] + 2 * (1 - s) * s * cpt[0] + s * s * b[0],
			(1 - s) * (1 - s) * a[1] + 2 * (1 - s) * s * cpt[1] + s * s * b[1],
		]);
	}
	return taper(pts, w0, w1);
};

/** fin blade + foot pocket, pointing back along angle `ang` (deg) from the ankle */
const fin = (ankle: P, ang: number, len = 124, w = 30): {blade: string; pocket: string; rail: string} => {
	const r = (ang * Math.PI) / 180;
	const ux = Math.cos(r);
	const uy = Math.sin(r);
	const p = (s: number, o: number): string => `${(ankle[0] + ux * s - uy * o).toFixed(1)} ${(ankle[1] + uy * s + ux * o).toFixed(1)}`;
	return {
		blade: `M ${p(-14, -12)} C ${p(10, -14)} ${p(30, -14)} ${p(40, -15)} L ${p(len, -w)} C ${p(len - 12, -w * 0.3)} ${p(len - 12, w * 0.3)} ${p(len, w)} L ${p(40, 15)} C ${p(30, 14)} ${p(10, 14)} ${p(-14, 12)} Z`,
		pocket: `M ${p(-16, -13)} C ${p(4, -16)} ${p(30, -16)} ${p(44, -15)} L ${p(44, 15)} C ${p(30, 16)} ${p(4, 16)} ${p(-16, 13)} Z`,
		rail: `M ${p(46, -12)} L ${p(len - 4, -w + 4)} M ${p(46, 12)} L ${p(len - 4, w - 4)}`,
	};
};

const TORSO = 'M 236 98 C 236 74 258 64 288 64 L 404 66 C 432 68 448 82 448 100 C 448 121 432 132 404 132 L 286 130 C 256 128 236 120 236 98 Z';
const TANK = 'M 268 50 C 268 38 278 32 292 32 L 404 32 C 416 32 424 40 424 50 C 424 60 416 68 404 68 L 292 68 C 278 68 268 62 268 50 Z';
const BCD = 'M 330 60 L 444 70 L 452 126 L 336 132 C 344 110 344 84 330 60 Z';
const STRIPE = 'M 230 106 C 300 110 380 112 456 110 L 458 120 C 380 123 300 122 230 118 Z';
const BELT = 'M 262 56 L 278 56 L 282 138 L 266 138 Z';
const STRAP1 = 'M 304 28 L 316 28 L 316 72 L 304 72 Z';
const STRAP2 = 'M 382 28 L 394 28 L 394 72 L 382 72 Z';
const HOOD = 'M 436 88 C 436 64 454 55 474 55 C 497 55 512 70 512 88 C 512 110 497 121 474 121 C 454 121 436 108 436 88 Z';
const MASK = 'M 490 69 C 507 67 521 76 523 88 C 525 101 516 109 502 109 L 490 109 C 481 102 481 76 490 69 Z';

export const Diver: React.FC<{id: string; t: number; waveAt?: number; flip?: boolean; layers?: Partial<Layers>}> = ({id, t, waveAt = 1.4, flip = false, layers}) => {
	const tint = useTint();
	const L = useLight();
	const sx = flip ? -1 : 1;

	// flutter kick 1.0 Hz from the hip; knee lags 0.06 s, ankle 0.12 s, fin 0.2 s (follow-through)
	const k = (ph: number, lag = 0) => Math.sin(2 * Math.PI * 1.0 * (t - lag) + ph);
	const nearKnee: P = [150, 132 + 7 * k(0, 0.06)];
	const nearAnkle: P = [46, 124 + 20 * k(0, 0.12)];
	const farKnee: P = [148, 80 + 7 * k(Math.PI, 0.06)];
	const farAnkle: P = [50, 68 + 20 * k(Math.PI, 0.12)];
	const nearFin = fin(nearAnkle, 178 + 18 * k(0, 0.2));
	const farFin = fin(farAnkle, 182 + 18 * k(Math.PI, 0.2), 112, 27);

	// wave: anticipation dip, spring overshoot, then a small oscillation; hand lags the forearm by 0.1 s
	const w = anticipate(t, waveAt, {antic: 0.2, dip: 0.12});
	const on = (d: number) => clamp((t - waveAt - d) * 3);
	const wig = Math.sin(2 * Math.PI * 1.6 * (t - waveAt - 0.6)) * on(0.6);
	const wigLag = Math.sin(2 * Math.PI * 1.6 * (t - waveAt - 0.7)) * on(0.7);
	const shoulder: P = [428, 116];
	const elbow: P = [lerp(462, 486, w), lerp(146, 140, w) + wig * 3];
	const hand: P = [lerp(500, 540 + wig * 9, w), lerp(152, 114, w) + wigLag * 6];

	const suit = 'dusk-2';
	const farSuit = shadowOf(tint(suit), tint(L.ambient), 0.32);
	const farFinCol = shadowOf(tint('coral-3'), tint(L.ambient), 0.32);
	const farPocket = shadowOf(tint('ink-2'), tint(L.ambient), 0.2);
	const seam = tint(shadowOf(c(suit), c(L.ambient), 0.5));

	return (
		<g transform={flip ? 'scale(-1 1)' : undefined}>
			{/* far side: leg + fin + arm, darker, support LOD */}
			<Shaded
				id={`${id}-far`}
				R={24}
				lod="support"
				xf={{sx}}
				layers={layers}
				parts={[
					{d: farFin.blade, base: farFinCol},
					{d: farFin.pocket, base: farPocket},
					{d: limb([262, 84], farAnkle, farKnee, 30, 17), base: farSuit},
					{d: limb([414, 104], [482, 148], [444, 142], 22, 15), base: farSuit},
				]}
			/>
			<Shaded
				id={`${id}-body`}
				box={[40, 30, 480, 110]}
				maskBox={[-110, 10, 650, 170]}
				R={52}
				core={0.42}
				hi={0.22}
				rimW={5}
				stippleBand={13}
				dot={0.85}
				xf={{sx}}
				layers={layers}
				parts={[
					{d: nearFin.blade, base: 'coral-3', marks: [{kind: 'dash', n: 2, size: 9, angle: 180, dL: -0.08, opacity: 0.6}]},
					{d: nearFin.pocket, base: 'ink-2'},
					{d: limb([268, 114], nearAnkle, nearKnee, 34, 18), base: suit, marks: [{kind: 'dash', n: 3, size: 8, angle: 0, dL: 0.07}]},
					{d: TORSO, base: suit, marks: [{kind: 'dash', n: 4, size: 8, angle: 5, dL: 0.07, area: [250, 70, 90, 50]}]},
					{d: TANK, base: 'amber-3', hi: 0.3, marks: [{kind: 'pore', n: 5, size: 8, dL: -0.08, area: [320, 36, 60, 20]}]},
					{
						el: (f) => <path d="M 430 48 C 450 92 470 122 512 120" stroke={f} strokeWidth={7} fill="none" strokeLinecap="round" />,
						base: 'ink-3',
						stipple: false,
					},
					{d: HOOD, base: suit},
					{d: BCD, base: 'ink-3', clip: true, shade: 0.3},
					{d: STRIPE, base: 'coral-3', clip: true, stipple: false},
					{d: BELT, base: 'ochre-1', clip: true},
					{d: STRAP1, base: 'ink-2', clip: true, stipple: false},
					{d: STRAP2, base: 'ink-2', clip: true, stipple: false},
				]}
				glints={[
					{cx: 346, cy: 38, rx: 36, ry: 3.4, rot: 0, o: 0.7},
					{cx: 470, cy: 62, rx: 12, ry: 3, rot: 10, o: 0.45},
				]}
				over={
					<g>
						<path d="M 290 70 C 320 74 360 76 410 74" stroke={seam} strokeWidth={2.4} fill="none" strokeLinecap="round" />
						<path d="M 210 124 C 180 128 160 130 140 130" stroke={seam} strokeWidth={2.2} fill="none" strokeLinecap="round" opacity={0.7} />
						{/* BCD D-rings and inflator: ring motif */}
						<circle cx={392} cy={98} r={6.5} fill="none" stroke={tint('bone-0')} strokeWidth={3} />
					</g>
				}
			/>
			{/* knife on the near calf */}
			<g transform={`translate(${(nearKnee[0] + nearAnkle[0]) / 2} ${(nearKnee[1] + nearAnkle[1]) / 2}) rotate(${(Math.atan2(nearAnkle[1] - nearKnee[1], nearAnkle[0] - nearKnee[0]) * 180) / Math.PI})`}>
				<rect x={-16} y={-4} width={30} height={8} rx={3} fill={tint('ink-1')} />
				<rect x={-18} y={-6} width={7} height={12} rx={2} fill={tint('ochre-3')} />
			</g>
			{/* tank valve + first stage, gauge hose and console */}
			<g>
				<path d="M 404 68 C 396 112 372 150 352 158" stroke={tint('ink-3')} strokeWidth={5} fill="none" strokeLinecap="round" />
				<rect x={420} y={36} width={16} height={20} rx={4} fill={tint('bone-0')} />
				<rect x={420} y={46} width={16} height={10} rx={3} fill={tint(shadowOf(c('bone-0'), c(L.ambient), 0.38))} />
				<circle cx={350} cy={160} r={12} fill={tint('ink-2')} />
				<circle cx={350} cy={160} r={8} fill={tint('bone-1')} />
				<path d="M 350 160 L 355 154" stroke={tint('signal-1')} strokeWidth={2.2} strokeLinecap="round" />
			</g>
			{/* mask: glass (glossy) + frame, regulator */}
			<Shaded
				id={`${id}-mask`}
				R={18}
				core={0.3}
				hi={0.35}
				rimW={3}
				lod="support"
				xf={{sx}}
				layers={layers}
				parts={[{d: MASK, base: 'tide-3'}]}
				glints={[
					{cx: 508, cy: 80, rx: 7, ry: 3, rot: 20, o: 0.95},
					{cx: 516, cy: 96, rx: 2.5, ry: 2.5, o: 0.8},
				]}
				top={<path d={MASK} fill="none" stroke={tint('ink-1')} strokeWidth={4.5} strokeLinejoin="round" />}
			/>
			<circle cx={514} cy={118} r={9.5} fill={tint('ink-2')} />
			<circle cx={517} cy={117} r={4} fill={tint(mixOk(c('ink-2'), c('tide-4'), 0.35))} />
			{/* near arm: the wave */}
			<Shaded
				id={`${id}-arm`}
				R={14}
				core={0.4}
				rimW={4}
				lod="support"
				xf={{sx}}
				layers={layers}
				parts={[
					{d: limb(shoulder, hand, elbow, 23, 15), base: suit},
					{
						d: `M ${hand[0] - 14} ${hand[1]} C ${hand[0] - 14} ${hand[1] - 14} ${hand[0] + 14} ${hand[1] - 14} ${hand[0] + 14} ${hand[1]} C ${hand[0] + 14} ${hand[1] + 13} ${hand[0] - 14} ${hand[1] + 13} ${hand[0] - 14} ${hand[1]} Z`,
						base: 'ink-3',
					},
					{d: `M ${hand[0] + 4} ${hand[1] - 10} C ${hand[0] + 4} ${hand[1] - 26} ${hand[0] + 14} ${hand[1] - 26} ${hand[0] + 14} ${hand[1] - 10} Z`, base: 'ink-3'},
				]}
			/>
		</g>
	);
};

/** regulator exhaust point in local (unflipped) coordinates, for the bubble stream */
export const DIVER_REG: [number, number] = [514, 118];
