/**
 * Renders placeMarks() output. Tone = the local surface tone (base, or the highlight colour inside the
 * highlight plane) with OKLab L scaled by (1 + dv): ±6-10 % of the base value, never a dark line. Glints are
 * bone-2. A `xf` point transform lets marks ride on an animated part (flipper stroke) computed in rest pose.
 */
import React from 'react';
import {c, mixOk, lum, shiftL} from '../../../kurz-style/engine/src/lib/color';
import {useLight, useTint} from '../../../kurz-style/engine/src/lib/light';
import type {MarkEl} from './marks';
import type {Pt} from './pathgeo';

export const SurfaceMarks: React.FC<{marks: MarkEl[]; base: string; hi?: number; xf?: (x: number, y: number) => Pt; rot?: number; opacity?: number}> = ({
	marks,
	base,
	hi = 0.22,
	xf,
	rot = 0,
	opacity = 0.95,
}) => {
	const tint = useTint();
	const L = useLight();
	const b = tint(base);
	const h = mixOk(b, tint(L.keyColor), hi);
	const memo = new Map<string, string>();
	const tone = (e: MarkEl) => {
		if (e.kind === 'glint') return c('bone-2');
		const src = e.hi ? h : b;
		const k = `${e.hi}:${e.dv.toFixed(3)}`;
		let v = memo.get(k);
		if (!v) {
			v = shiftL(src, lum(src) * e.dv);
			memo.set(k, v);
		}
		return v;
	};
	return (
		<g opacity={opacity}>
			{marks.map((e, i) => {
				const [x, y] = xf ? xf(e.x, e.y) : [e.x, e.y];
				const col = tone(e);
				const a = ((e.ang + rot) * Math.PI) / 180;
				const ux = Math.cos(a);
				const uy = Math.sin(a);
				switch (e.prim) {
					case 'dot':
						return <circle key={i} cx={x} cy={y} r={e.s} fill={col} />;
					case 'ring':
						return (
							<g key={i}>
								<circle cx={x} cy={y} r={e.s} fill="none" stroke={col} strokeWidth={e.w} />
								<circle cx={x} cy={y} r={e.s * 0.38} fill={col} />
							</g>
						);
					case 'line':
						return <line key={i} x1={x} y1={y} x2={x + ux * e.s} y2={y + uy * e.s} stroke={col} strokeWidth={e.w} strokeLinecap="round" />;
					case 'curve': {
						const mx = x + (ux * e.s) / 2 - uy * e.s * 0.08;
						const my = y + (uy * e.s) / 2 + ux * e.s * 0.08;
						return <path key={i} d={`M ${x - (ux * e.s) / 2} ${y - (uy * e.s) / 2} Q ${mx} ${my} ${x + (ux * e.s) / 2} ${y + (uy * e.s) / 2}`} stroke={col} strokeWidth={e.w} strokeLinecap="round" fill="none" />;
					}
					case 'arc':
						return (
							<path
								key={i}
								d={`M ${x - ux * e.s} ${y - uy * e.s} Q ${x - uy * e.s * 0.9} ${y + ux * e.s * 0.9} ${x + ux * e.s} ${y + uy * e.s}`}
								stroke={col}
								strokeWidth={e.w}
								strokeLinecap="round"
								fill="none"
							/>
						);
					case 'bean':
						return <ellipse key={i} cx={x} cy={y} rx={e.s} ry={e.s * 0.42} transform={`rotate(${(e.ang + rot).toFixed(1)} ${x.toFixed(1)} ${y.toFixed(1)})`} fill={col} opacity={0.85} />;
				}
				return null;
			})}
		</g>
	);
};

/** quick helper: the base L shift used by marks, exported for other generators' internal detail (±% of base) */
export const valueShift = (base: string, frac: number) => shiftL(base, lum(base) * frac);
