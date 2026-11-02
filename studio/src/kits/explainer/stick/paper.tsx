/**
 * stick/Paper: a period newspaper page that slides in (700 x 900 box).
 * props: masthead, headline (2 short lines max, "\n" splits), at (slide-in time), sketch: true draws the cabinet
 * with a figure folded inside.
 */
import React from 'react';
import type {KitComponentProps} from '../../../core/registry';
import {clamp, easeOut, num, str} from '../util';
import {c} from './common';

export const Paper: React.FC<KitComponentProps> = ({props, time}) => {
	const at = num(props.at, 0);
	const k = easeOut(clamp((time - at) / 0.5));
	const lines = str(props.headline, 'THE SECRET').split('\n');
	const font = '"Anton", "Arial Narrow", sans-serif';
	return (
		<svg viewBox="0 0 700 900" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style={{overflow: 'visible'}}>
			<g transform={`translate(0 ${(1 - k) * 900}) rotate(${(1 - k) * 14 - 3} 350 450)`} opacity={k > 0 ? 1 : 0}>
				<rect x={24} y={30} width={660} height={860} fill={c('ink-1')} opacity={0.3} />
				<rect x={10} y={10} width={660} height={860} fill={c('bone-1')} />
				<rect x={360} y={10} width={310} height={860} fill={c('bone-0')} opacity={0.6} />
				<text x={340} y={96} textAnchor="middle" fontFamily={font} fontSize={58} fill={c('ink-1')} letterSpacing={3}>
					{str(props.masthead, 'THE CHESS MONTHLY')}
				</text>
				<rect x={40} y={120} width={600} height={8} fill={c('ink-1')} />
				{lines.map((ln, i) => (
					<text key={i} x={340} y={214 + i * 92} textAnchor="middle" fontFamily={font} fontSize={88} fill={c('coral-1')}>
						{ln}
					</text>
				))}
				<g transform={`translate(70 ${250 + lines.length * 92})`}>
					<rect width={250} height={230} fill={c('bone-2')} />
					<rect x={30} y={120} width={190} height={90} fill={c('ochre-1')} />
					<rect x={44} y={132} width={162} height={66} fill={c('ink-1')} />
					<circle cx={110} cy={150} r={16} fill={c('bone-1')} />
					<path d="M 96 166 Q 120 200 160 186" stroke={c('sky-1')} strokeWidth={14} fill="none" strokeLinecap="round" />
					<circle cx={125} cy={70} r={34} fill={c('bone-1')} />
					<ellipse cx={125} cy={44} rx={40} ry={22} fill={c('bone-0')} />
				</g>
				{Array.from({length: 9}, (_, i) => (
					<rect key={i} x={350} y={260 + lines.length * 92 + i * 28} width={i % 3 === 2 ? 200 : 280} height={12} rx={6} fill={c('bone-0')} />
				))}
				{Array.from({length: 6}, (_, i) => (
					<rect key={`b${i}`} x={60} y={520 + lines.length * 92 + i * 28} width={i % 4 === 3 ? 340 : 560} height={12} rx={6} fill={c('bone-0')} />
				))}
			</g>
		</svg>
	);
};
