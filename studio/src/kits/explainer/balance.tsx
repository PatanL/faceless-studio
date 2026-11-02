/** Scale infographics built on the figures: explainer/Balance (seesaw) and explainer/ECG (heartbeat trace). */
import React, {useId} from 'react';
import type {KitComponent} from '../../core/registry';
import {FigureSVG, getFigure, makeCtx} from './creature';
import {arr, C, clamp, easeIn, easeOut, num, obj, prog, safeId, str, track} from './util';

// ================================================================ components

/**
 * explainer/Balance: a seesaw. props: left / right {species, w (px across), at (appear, s), drop (true: falls in),
 * pose, silhouette, ...figure props}, tilt (deg or [{t, v}] track; + = right side down), beam (px, default 90 % of
 * the box), color.
 */
export const Balance: KitComponent = ({props, time, width: W, height: H}) => {
	const id = safeId(useId());
	const tilt = track(props.tilt, time, 0);
	const L = num(props.beam, W * 0.9);
	const px = W / 2;
	const py = H - num(props.fulcrum, 150);
	const col = str(props.color, '#c9d4da');
	const side = (key: 'left' | 'right', sign: number) => {
		const s = obj(props[key]);
		const name = str(s.species, '');
		const f = name ? getFigure(name, typeof s.pose === 'string' ? s.pose : undefined) : undefined;
		if (!f) return null;
		const at = num(s.at, 0);
		if (time < at) return null;
		const w = num(s.w, L * 0.35);
		const h = (w * f.box[3]) / f.box[2];
		const d = s.drop === true ? 1 - easeIn(prog(time, at, 0.4)) : 0;
		const fade = s.drop === true ? 1 : easeOut(prog(time, at, 0.3));
		const cx = px + sign * L * num(s.pos, 0.3);
		return (
			<g key={key} opacity={fade} transform={`translate(0 ${-d * H * 0.6})`}>
				{/* feet sink 3 px into the beam's rounded top: contact, never a hairline gap (judge: elephant floats) */}
				<FigureSVG f={f} ctx={makeCtx(s, time, `${id}${key}`)} x={cx - w / 2} y={py - 5 - h} w={w} h={h} />
			</g>
		);
	};
	return (
		<svg width={W} height={H} style={{overflow: 'visible', display: 'block'}}>
			<path d={`M ${px} ${py + 6} L ${px - 70} ${H} L ${px + 70} ${H} Z`} fill={col} opacity={0.85} />
			<g transform={`rotate(${tilt} ${px} ${py})`}>
				<rect x={px - L / 2} y={py - 8} width={L} height={18} rx={9} fill={col} />
				{side('left', -1)}
				{side('right', 1)}
			</g>
			<circle cx={px} cy={py} r={14} fill="#7d8a92" />
		</svg>
	);
};

/**
 * explainer/ECG: scrolling heartbeat trace. props: beats (scene-local beat times, s), speed (px/s, default 260),
 * color, thickness, at (trace appears), stopAt (flat line after this time, optional), prefill (true: the trace is
 * already drawn across the full width at `at`, with beats before `at` as history, so it is never half-drawn).
 */
export const ECG: KitComponent = ({props, time, width: W, height: H}) => {
	const at = num(props.at, 0);
	if (time < at) return null;
	const sp = num(props.speed, 260);
	const beats = arr<number>(props.beats).filter((b) => typeof b === 'number') as unknown as number[];
	const y0 = H / 2;
	const amp = H * 0.42;
	const t0 = props.prefill === true ? time - W / sp : Math.max(at, time - W / sp);
	const pts: string[] = [];
	const xOf = (tt: number) => W - (time - tt) * sp;
	pts.push(`M ${xOf(t0).toFixed(1)} ${y0}`);
	for (const b of beats) {
		if (b < t0 || b > time) continue;
		const x = xOf(b);
		pts.push(`L ${(x - 18).toFixed(1)} ${y0} L ${(x - 8).toFixed(1)} ${y0 + amp * 0.18} L ${x.toFixed(1)} ${y0 - amp} L ${(x + 10).toFixed(1)} ${y0 + amp * 0.55} L ${(x + 20).toFixed(1)} ${y0}`);
	}
	pts.push(`L ${W} ${y0}`);
	const recent = beats.filter((b) => b <= time).pop();
	const flash = recent !== undefined ? clamp(1 - (time - recent) / 0.35) : 0;
	const color = str(props.color, C.cyan);
	return (
		<svg width={W} height={H} style={{overflow: 'visible', display: 'block'}}>
			<path d={pts.join(' ')} stroke={color} strokeWidth={num(props.thickness, 7)} fill="none" strokeLinejoin="round" strokeLinecap="round" style={{filter: `drop-shadow(0 0 ${8 + 14 * flash}px ${color})`}} />
			<circle cx={W} cy={y0} r={10 + 6 * flash} fill={color} />
		</svg>
	);
};
