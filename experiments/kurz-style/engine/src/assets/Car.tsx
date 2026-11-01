/**
 * Car (side view, facing right) for weight comparisons. Hard-surface prop: soft-chamfer corners (bible §3),
 * full support stack from the scene light, glass with a glare band, ring-motif hubs.
 * Local box: x 0..206, y 0..88 (wheel bottoms at y = 88).
 */
import React from 'react';
import {c, mixOk, shadowOf} from '../lib/color';
import {useLight, useTint} from '../lib/light';
import {Shaded} from '../shade/Shaded';

const SHELL =
	'M 6 58 C 6 47 12 42 22 41 L 50 38 L 72 16 C 77 11 83 9 91 9 L 138 9 C 146 9 152 12 157 17 L 176 38 L 192 41 C 200 43 204 49 204 57 L 204 68 C 204 72 201 74 197 74 L 11 74 C 8 74 6 72 6 68 Z';
const WIN_R = 'M 80 18 C 83 15 86 14 91 14 L 111 14 L 111 37 L 59 37 Z';
const WIN_F = 'M 117 14 L 136 14 C 141 14 145 16 148 19 L 165 37 L 117 37 Z';
const SKIRT = 'M 6 62 L 204 62 L 204 68 C 204 72 201 74 197 74 L 11 74 C 8 74 6 72 6 68 Z';

export const Car: React.FC<{id: string; base: string; spin?: number}> = ({id, base, spin = 0}) => {
	const tint = useTint();
	const L = useLight();
	const glass = tint('tide-2');
	const wheel = (cx: number) => (
		<g key={cx}>
			<circle cx={cx} cy={72} r={16} fill={tint('ink-1')} />
			<circle cx={cx} cy={72} r={9.5} fill="none" stroke={tint('bone-0')} strokeWidth={3.4} />
			<circle cx={cx} cy={72} r={3.6} fill={tint('bone-1')} />
			<line x1={cx} y1={72} x2={cx + 9 * Math.cos(spin)} y2={72 + 9 * Math.sin(spin)} stroke={tint('bone-0')} strokeWidth={2} strokeLinecap="round" />
			<path d={`M ${cx - 13} ${66} A 14 14 0 0 1 ${cx - 2} ${58}`} stroke={mixOk(tint('ink-1'), tint(L.keyColor), 0.35)} strokeWidth={2.4} fill="none" strokeLinecap="round" />
		</g>
	);
	return (
		<g>
			{/* wheel arches read as deep occlusion behind the tyres */}
			<path d="M 30 74 C 30 54 70 54 70 74 Z M 138 74 C 138 54 178 54 178 74 Z" fill={shadowOf(tint(base), tint(L.ambient), 0.6)} />
			<Shaded
				id={id}
				R={34}
				core={0.42}
				hi={0.24}
				rimW={4}
				stippleBand={10}
				dot={0.8}
				parts={[
					{d: SHELL, base, marks: [{kind: 'pore', n: 3, size: 6, dL: -0.06, area: [20, 44, 160, 14]}]},
					{d: SKIRT, base: shadowOf(c(base), c('ink-2'), 0.3), clip: true, stipple: false},
					{d: WIN_R, base: 'tide-2', clip: true, hi: 0.3, stipple: false},
					{d: WIN_F, base: 'tide-2', clip: true, hi: 0.3, stipple: false},
				]}
				glints={[
					{cx: 96, cy: 22, rx: 16, ry: 2.6, rot: -40, o: 0.65},
					{cx: 136, cy: 24, rx: 12, ry: 2.4, rot: -40, o: 0.55},
					{cx: 120, cy: 11, rx: 22, ry: 1.8, o: 0.45},
				]}
				over={
					<g fill="none" strokeLinecap="round">
						<path d="M 114 14 L 114 62 M 58 40 L 58 62" stroke={shadowOf(tint(base), tint(L.ambient), 0.45)} strokeWidth={2.4} />
						<path d="M 74 46 L 86 46 M 126 46 L 138 46" stroke={mixOk(tint(base), tint('bone-2'), 0.35)} strokeWidth={3} />
						<path d="M 72 14 L 60 37" stroke={mixOk(glass, tint('bone-2'), 0.4)} strokeWidth={2} opacity={0.6} />
					</g>
				}
				top={
					<g>
						<rect x={194} y={46} width={10} height={7} rx={3} fill={tint('amber-5')} />
						<rect x={6} y={46} width={8} height={7} rx={3} fill={tint('coral-4')} />
					</g>
				}
			/>
			{wheel(50)}
			{wheel(158)}
		</g>
	);
};
