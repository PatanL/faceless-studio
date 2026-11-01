/**
 * The YOU figure (bible §10, brand/avatar): bone stick figure, round caps, 2-tone ring head, standing on a
 * signal ring pad. Shaded (core + rim at least), contact shadow, idle sway, optional wave with anticipation.
 * Local space: feet at y = 0, head top at y = -200, centred on x = 0.
 */
import React from 'react';
import {c, mixOk, rgba, shadowOf} from '../lib/color';
import {useLight, useTint} from '../lib/light';
import {Shaded} from '../shade/Shaded';
import {anticipate, clamp, lerp, sway} from '../motion/motion';

export const YouFigure: React.FC<{id: string; t: number; waveAt?: number; pad?: boolean}> = ({id, t, waveAt = 99, pad = true}) => {
	const tint = useTint();
	const L = useLight();
	const sw = sway(t, id, 2.2, 3.4);
	const w = anticipate(t, waveAt, {antic: 0.16, dip: 0.1});
	const wig = Math.sin(2 * Math.PI * 1.8 * (t - waveAt - 0.5)) * clamp((t - waveAt - 0.5) * 3);
	const hip: [number, number] = [0, -84];
	const neck: [number, number] = [0, -146];
	const handR: [number, number] = [lerp(30, 40 + wig * 8, w), lerp(-100, -196, w)];
	const elbowR: [number, number] = [lerp(20, 36, w), lerp(-122, -166, w)];
	const LW = 15;
	const strokes = (f: string) => (
		<g stroke={f} strokeWidth={LW} strokeLinecap="round" strokeLinejoin="round" fill="none">
			<path d={`M ${hip[0]} ${hip[1]} L ${neck[0]} ${neck[1]}`} />
			<path d={`M ${hip[0]} ${hip[1]} L -22 -6`} />
			<path d={`M ${hip[0]} ${hip[1]} L 22 -6`} />
			<path d={`M ${neck[0]} ${neck[1] + 8} L -24 -118 L -32 -92`} />
			<path d={`M ${neck[0]} ${neck[1] + 8} L ${elbowR[0]} ${elbowR[1]} L ${handR[0]} ${handR[1]}`} />
		</g>
	);
	const head = (f: string) => <circle cx={0} cy={-176} r={21} fill={f} />;
	const ringInner = shadowOf(tint('bone-1'), tint(L.ambient), 0.2);
	return (
		<g>
			{pad ? (
				<g>
					<ellipse cx={4} cy={6} rx={58} ry={12} fill={rgba(tint('ink-0'), 0.4)} />
					<ellipse cx={0} cy={0} rx={50} ry={11} fill={tint('signal-0')} />
					<ellipse cx={0} cy={-1} rx={42} ry={8} fill="none" stroke={tint('signal-1')} strokeWidth={5} />
					<ellipse cx={-14} cy={-4} rx={12} ry={2} fill={mixOk(tint('signal-1'), c('bone-2'), 0.5)} opacity={0.7} />
				</g>
			) : null}
			<g transform={`rotate(${sw.toFixed(2)} 0 0)`}>
				<Shaded
					id={id}
					box={[-40, -200, 80, 200]}
					maskBox={[-50, -210, 110, 220]}
					R={22}
					core={0.5}
					hi={0.18}
					rimW={4}
					stippleBand={8}
					dot={0.7}
					parts={[
						{el: strokes, base: 'bone-2'},
						{el: head, base: 'bone-2'},
					]}
					top={
						<g>
							<circle cx={0} cy={-176} r={9} fill={ringInner} />
							<circle cx={L.key[0] * 9} cy={-176 + L.key[1] * 9} r={3.2} fill={c('bone-2')} opacity={0.9} />
						</g>
					}
				/>
			</g>
		</g>
	);
};
