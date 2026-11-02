/**
 * The hero turtle: geometry from turtleGeom.ts, shaded by the engine's <Shaded> (two groups: skin, then the
 * carapace on top) with the hard terminator (stipple off, owner override), plus the surface-mark generator's
 * clusters on the lit side. No outlines anywhere: seams are LIGHTER than the scutes, scale gaps are pale
 * skin, and separation from the water comes from value, the warm/cool split and the tide rim.
 */
import React from 'react';
import {c, mixOk} from '../../../kurz-style/engine/src/lib/color';
import {norm, useLight, type Vec} from '../../../kurz-style/engine/src/lib/light';
import {Eye, Shaded} from '../../../kurz-style/engine/src/shade/Shaded';
import {blinkAt} from '../../../kurz-style/engine/src/motion/motion';
import {rotAbout, type Pt} from '../detail/pathgeo';
import {SurfaceMarks} from '../detail/SurfaceMarks';
import {
	cellPath,
	EYE,
	GROWTH,
	HEAD,
	HEAD_CELLS,
	HEAD_PIVOT,
	heroMarks,
	LIMB_CELLS,
	LIMBS,
	limbAngle,
	limbPath,
	limbXf,
	MARGINAL,
	MOUTH,
	PLASTRON,
	BEAK,
	BROW,
	polysD,
	RY,
	SEAMS,
	SHELL,
	STREAKS,
	TAIL,
	VERTEBRAL,
} from './turtleGeom';
import {warp} from '../../../kurz-style/engine/src/lib/geom';

export const SKIN = mixOk(c('ochre-3'), c('kelp-3'), 0.32);
export const SCALE = mixOk(SKIN, mixOk(c('ochre-1'), c('kelp-1'), 0.4), 0.34);
export const SCUTE = mixOk(c('amber-1'), c('ochre-2'), 0.2);
export const SEAM = mixOk(SCUTE, mixOk(c('amber-3'), c('ochre-4'), 0.35), 0.32);
/** warm shadow targets keep the shadow sides saturated (no muddy brown-grey, P4) */
const SHELL_AMB = mixOk(c('coral-0'), c('ink-2'), 0.45);
const SKIN_AMB = mixOk(c('kelp-0'), c('ink-2'), 0.4);

const toLocal = (v: Vec, rot: number): Vec => {
	const a = (-rot * Math.PI) / 180;
	return norm([v[0] * Math.cos(a) - v[1] * Math.sin(a), v[0] * Math.sin(a) + v[1] * Math.cos(a)]);
};

/** reference light for the marks (the scene's light at the shot's start pose), so marks never swim */
export const turtleMarks = (key: Vec, rim: Vec, rot: number) => heroMarks(toLocal(key, rot), toLocal(rim, rot));

export const Turtle: React.FC<{t: number; rot: number; refKey: Vec; refRim: Vec}> = ({t, rot, refKey, refRim}) => {
	const L = useLight();
	const pose = Object.fromEntries(LIMBS.map((lb) => [lb.name, limbXf(lb, limbAngle(lb.name, t))]));
	const limbD = Object.fromEntries(LIMBS.map((lb) => [lb.name, limbPath(lb, pose[lb.name])]));
	const headRot = 3 * Math.sin(2 * Math.PI * 0.34 * t - 0.9);
	const hx = rotAbout(HEAD_PIVOT[0], HEAD_PIVOT[1], headRot);
	const headD = warp(HEAD, hx);
	const cells = [
		...LIMBS.flatMap((lb) => LIMB_CELLS[lb.name].map((p) => cellPath(p.map(([x, y]) => pose[lb.name](x, y))))),
		...HEAD_CELLS.map((p) => cellPath(p.map(([x, y]) => hx(x, y)))),
	].join(' ');
	const marks = turtleMarks(refKey, refRim, rot);
	const [ex, ey] = hx(EYE[0], EYE[1]);
	const blink = blinkAt(t, 'turtle');

	return (
		<g>
			<Shaded
				id="tskin"
				R={46}
				xf={{rot}}
				layers={{stipple: false}}
				core={0.42}
				rimW={4}
				maskBox={[-20, -40, 660, 500]}
				parts={[
					{d: limbD.farFront, base: SKIN, ambient: SKIN_AMB},
					{d: limbD.farRear, base: SKIN, ambient: SKIN_AMB},
					{d: PLASTRON, base: mixOk(c('bone-0'), c('amber-4'), 0.35), hi: 0.12, ambient: SHELL_AMB},
					{d: limbD.nearRear, base: SKIN, ambient: SKIN_AMB},
					{d: TAIL, base: SKIN, ambient: SKIN_AMB},
					{d: headD, base: SKIN, ambient: SKIN_AMB},
					{d: limbD.nearFront, base: SKIN, ambient: SKIN_AMB},
					{el: (fill) => <path d={cells} fill={fill} />, base: SCALE, clip: true, hi: 0.26, ambient: SKIN_AMB},
					{d: warp(BEAK, hx), base: mixOk(c('amber-4'), c('ochre-3'), 0.5), clip: true, ambient: SHELL_AMB},
				]}
				over={
					<>
						<path d={warp(MOUTH, hx)} stroke={mixOk(SCALE, SKIN_AMB, 0.25)} strokeWidth={3} fill="none" strokeLinecap="round" />
						<path d={warp(BROW, hx)} stroke={mixOk(SKIN, SKIN_AMB, 0.3)} strokeWidth={5} fill="none" strokeLinecap="round" />
					</>
				}
				top={<Eye cx={ex} cy={ey} r={EYE[2]} iris="ochre-2" lid={0} look={[-0.6, 0.15]} blink={blink} />}
			/>
			<SurfaceMarks marks={marks.head} base={SCALE} xf={hx} />
			<SurfaceMarks marks={marks.nearFront} base={SCALE} xf={pose.nearFront} />
			<SurfaceMarks marks={marks.nearRear} base={SCALE} xf={pose.nearRear} />
			<Shaded
				id="tshell"
				R={RY}
				xf={{rot}}
				layers={{stipple: false}}
				core={0.4}
				hi={0.24}
				rimW={6}
				maskBox={[120, 60, 470, 280]}
				parts={[
					{d: SHELL, base: SCUTE, ambient: SHELL_AMB},
					{d: polysD(MARGINAL), base: mixOk(SCUTE, c('amber-2'), 0.5), clip: true, ambient: SHELL_AMB},
					{d: polysD(VERTEBRAL), base: mixOk(SCUTE, c('coral-1'), 0.16), clip: true, ambient: SHELL_AMB},
					{el: (fill) => <path d={STREAKS.dark.join(' ')} fill={fill} />, base: mixOk(SCUTE, c('coral-0'), 0.25), clip: true, ambient: SHELL_AMB},
					{el: (fill) => <path d={STREAKS.light.join(' ')} fill={fill} />, base: mixOk(SCUTE, c('amber-3'), 0.4), clip: true, ambient: SHELL_AMB},
					{el: (fill) => <path d={GROWTH} stroke={fill} strokeWidth={2.2} fill="none" />, base: mixOk(SCUTE, c('amber-3'), 0.22), clip: true, ambient: SHELL_AMB},
					{el: (fill) => <path d={SEAMS} stroke={fill} strokeWidth={4.2} fill="none" strokeLinejoin="round" strokeLinecap="round" />, base: SEAM, clip: true, ambient: SHELL_AMB, hi: 0.15},
				]}
			/>
			<SurfaceMarks marks={marks.shell} base={SCUTE} hi={0.24} />
		</g>
	);
};

export const markCount = (key: Vec, rim: Vec, rot: number) => {
	const m = turtleMarks(key, rim, rot);
	return {shell: m.shell.length, head: m.head.length, nearFront: m.nearFront.length, nearRear: m.nearRear.length, total: m.shell.length + m.head.length + m.nearFront.length + m.nearRear.length};
};

export type {Pt};
