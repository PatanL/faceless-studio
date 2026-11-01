// Tiny demo kit: proves the component registry. Real kits live in src/kits/explainer and
// src/kits/horror and register themselves the same way.
import React from 'react';
import {registerComponent, type KitComponentProps} from '../../core/registry';

const str = (v: unknown, d: string) => (typeof v === 'string' ? v : d);
const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);

/** Stick figure "YOU" with an optional waving arm. props: color, wave (bool), label */
const StickFigure: React.FC<KitComponentProps> = ({props, time}) => {
	const c = str(props.color, '#ffffff');
	const wave = props.wave !== false;
	const arm = wave ? -50 + Math.sin(time * 9) * 28 : 20;
	return (
		<svg viewBox="0 0 200 320" width="100%" height="100%" style={{overflow: 'visible'}}>
			<g stroke={c} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" fill="none">
				<circle cx={100} cy={60} r={40} fill={c} stroke="none" />
				<line x1={100} y1={100} x2={100} y2={210} />
				<line x1={100} y1={210} x2={60} y2={300} />
				<line x1={100} y1={210} x2={140} y2={300} />
				<line x1={100} y1={130} x2={45} y2={185} />
				<g transform={`rotate(${arm} 100 130)`}>
					<line x1={100} y1={130} x2={170} y2={130} />
				</g>
			</g>
			<circle cx={86} cy={56} r={6} fill="#0b0f14" />
			<circle cx={114} cy={56} r={6} fill="#0b0f14" />
		</svg>
	);
};

/** Generic whale silhouette with a tail beat. props: color, belly, tail (Hz) */
const Whale: React.FC<KitComponentProps> = ({props, time}) => {
	const c = str(props.color, '#24435a');
	const belly = str(props.belly, '#5f8aa6');
	const tail = Math.sin(time * Math.PI * 2 * num(props.tail, 0.6)) * 9;
	return (
		<svg viewBox="0 0 1000 420" width="100%" height="100%" style={{overflow: 'visible'}}>
			<g transform={`rotate(${tail} 820 210)`}>
				<path d="M800 200 C 870 170, 920 110, 990 90 C 960 160, 950 200, 985 300 C 920 270, 870 240, 800 225 Z" fill={c} />
			</g>
			{/* boxy head, long body: generic toothed-whale shape */}
			<path
				d="M40 150 C 40 90, 120 70, 260 70 C 470 70, 640 110, 820 190 C 830 205, 830 220, 815 230 C 640 300, 430 330, 240 320 C 120 314, 40 290, 40 240 Z"
				fill={c}
			/>
			<path d="M70 268 C 200 300, 420 300, 640 262 C 470 318, 220 330, 90 300 Z" fill={belly} opacity={0.75} />
			<path d="M330 270 C 360 330, 400 350, 440 352 C 420 320, 400 300, 390 280 Z" fill={c} />
			<circle cx={190} cy={175} r={11} fill="#0b0f14" />
			<circle cx={193} cy={172} r={4} fill="#ffffff" />
			<path d="M70 250 C 120 262, 180 262, 240 252" stroke="#0b0f14" strokeWidth={6} fill="none" strokeLinecap="round" opacity={0.6} />
		</svg>
	);
};

/** Light rays from the surface. props: color, count */
const LightRays: React.FC<KitComponentProps> = ({props, time, width, height}) => {
	const n = num(props.count, 6);
	const c = str(props.color, 'rgba(180,240,255,0.10)');
	const rays = Array.from({length: n}, (_, i) => {
		const x = (width / n) * (i + 0.5) + Math.sin(time * 0.4 + i) * 40;
		const w = 90 + ((i * 37) % 80);
		return <polygon key={i} points={`${x - w / 2},0 ${x + w / 2},0 ${x + w * 1.6},${height} ${x - w * 0.4},${height}`} fill={c} />;
	});
	return (
		<svg width={width} height={height} style={{display: 'block'}}>
			<defs>
				<linearGradient id="ray-fade" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#fff" stopOpacity={1} />
					<stop offset="1" stopColor="#fff" stopOpacity={0} />
				</linearGradient>
				<mask id="ray-mask">
					<rect width={width} height={height} fill="url(#ray-fade)" />
				</mask>
			</defs>
			<g mask="url(#ray-mask)">{rays}</g>
		</svg>
	);
};

/** Vertical depth gauge with a moving marker. props: max (m), value (m, animated via valueTo/at) */
const DepthGauge: React.FC<KitComponentProps> = ({props, time, width, height}) => {
	const max = num(props.max, 3000);
	const from = num(props.from, 0);
	const to = num(props.to, max);
	const t0 = num(props.at, 0);
	const dur = num(props.duration, 1.6);
	const p = Math.max(0, Math.min(1, (time - t0) / dur));
	const e = 1 - Math.pow(1 - p, 3);
	const v = from + (to - from) * e;
	const y = (v / max) * (height - 40) + 20;
	const ticks = Array.from({length: 7}, (_, i) => i);
	return (
		<svg width={width} height={height} style={{overflow: 'visible'}}>
			<rect x={width / 2 - 10} y={20} width={20} height={height - 40} rx={10} fill="rgba(255,255,255,0.18)" />
			<rect x={width / 2 - 10} y={20} width={20} height={Math.max(0, y - 20)} rx={10} fill="#ffe14d" />
			{ticks.map((i) => {
				const ty = 20 + (i / 6) * (height - 40);
				return (
					<g key={i}>
						<line x1={width / 2 - 34} x2={width / 2 - 14} y1={ty} y2={ty} stroke="rgba(255,255,255,0.6)" strokeWidth={4} />
						<text x={width / 2 - 44} y={ty + 10} textAnchor="end" fill="rgba(255,255,255,0.75)" fontSize={30} fontFamily="Montserrat" fontWeight={800}>
							{Math.round((max / 6) * i)}m
						</text>
					</g>
				);
			})}
			<g transform={`translate(${width / 2}, ${y})`}>
				<polygon points="18,0 50,-22 50,22" fill="#ffe14d" />
				<text x={62} y={14} fill="#ffffff" fontSize={44} fontFamily="Montserrat" fontWeight={900}>
					{Math.round(v).toLocaleString('en-US')} m
				</text>
			</g>
		</svg>
	);
};

registerComponent('demo/StickFigure', StickFigure);
registerComponent('demo/Whale', Whale);
registerComponent('demo/LightRays', LightRays);
registerComponent('demo/DepthGauge', DepthGauge);
