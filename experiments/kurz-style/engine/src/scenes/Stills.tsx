/**
 * Proof stills:
 *   ShadingLadder  the shading layer built up one layer at a time on a flat group (9 tiles), then the same
 *                  object under 3 other light directions (the light is a parameter, nothing redrawn)
 *   Assets         hero orca and diver large, for detail review
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {c} from '../lib/color';
import {blob} from '../lib/geom';
import {dirDeg, LightProvider, LANTERN, type SceneLight} from '../lib/light';
import {Shaded, type Layers} from '../shade/Shaded';
import {GradientField, Specks} from '../depth/Atmosphere';
import {Orca} from '../assets/Orca';
import {Diver} from '../assets/Diver';
import {Kelp, Rock, FishSchool} from '../assets/Ocean';
import {FONT, waitForFonts} from '../lib/type';

const OFF: Layers = {form: false, core: false, stipple: false, deep: false, bounce: false, highlight: false, glints: false, rim: false, marks: false, cast: false, innerGlow: false};

const STEPS: [string, Partial<Layers>][] = [
	['flat input', {}],
	['+ form gradient', {form: true}],
	['+ core shadow', {form: true, core: true}],
	['+ stipple terminator', {form: true, core: true, stipple: true}],
	['+ deep + bounce', {form: true, core: true, stipple: true, deep: true, bounce: true}],
	['+ highlight + glints', {form: true, core: true, stipple: true, deep: true, bounce: true, highlight: true, glints: true}],
	['+ rim light', {form: true, core: true, stipple: true, deep: true, bounce: true, highlight: true, glints: true, rim: true}],
	['+ micro-marks', {form: true, core: true, stipple: true, deep: true, bounce: true, highlight: true, glints: true, rim: true, marks: true}],
	['+ cast shadow = all', {...OFF, form: true, core: true, stipple: true, deep: true, bounce: true, highlight: true, glints: true, rim: true, marks: true, cast: true}],
];

const BODY = blob('ladder', 180, 230, 118, 96, {n: 9, jag: 0.12});
const FIN = 'M 250 170 C 280 120 310 100 330 96 C 322 130 300 168 276 196 Z';
const BAND = 'M 60 236 C 120 254 240 262 320 240 L 320 270 C 240 292 120 286 60 266 Z';

const Specimen: React.FC<{id: string; layers: Partial<Layers>}> = ({id, layers}) => (
	<Shaded
		id={id}
		R={100}
		layers={{...OFF, ...layers}}
		cast={{y: 352, lift: 0.15}}
		parts={[
			{d: FIN, base: 'coral-2'},
			{d: BODY, base: 'coral-3', marks: [{kind: 'ring', n: 5, size: 18, dL: 0.09}, {kind: 'dash', n: 5, size: 12}]},
			{d: BAND, base: 'bone-1', clip: true},
		]}
		autoGlint={0.16}
	/>
);

export const ShadingLadder: React.FC = () => {
	waitForFonts();
	const tiles: React.ReactNode[] = [];
	const W = 360;
	const H = 480;
	STEPS.forEach(([label, layers], i) => {
		tiles.push(
			<g key={i} transform={`translate(${(i % 3) * W} ${Math.floor(i / 3) * H})`}>
				<rect width={W} height={H} fill={c(i % 2 ? 'ink-2' : 'ink-3')} />
				<g transform="translate(0 30)">
					<Specimen id={`lad${i}`} layers={layers} />
				</g>
				<text x={18} y={H - 26} fontFamily={FONT} fontWeight={800} fontSize={26} fill={c('bone-2')}>
					{`${i + 1}. ${label}`}
				</text>
			</g>,
		);
	});
	const dirs: [string, number][] = [
		['key from left', 180],
		['key from top-right', -45],
		['key from below', 90],
	];
	dirs.forEach(([label, deg], j) => {
		const light: SceneLight = {...LANTERN, key: dirDeg(deg), rim: dirDeg(deg + 160)};
		tiles.push(
			<g key={`d${j}`} transform={`translate(${j * W} ${3 * H})`}>
				<rect width={W} height={H} fill={c(j % 2 ? 'ink-3' : 'ink-2')} />
				<LightProvider light={light}>
					<g transform="translate(0 30)">
						<Specimen id={`dir${j}`} layers={STEPS[8][1]} />
					</g>
				</LightProvider>
				<line x1={180} y1={250} x2={180 + Math.cos((deg * Math.PI) / 180) * 150} y2={250 + Math.sin((deg * Math.PI) / 180) * 150} stroke={c('amber-4')} strokeWidth={3} strokeDasharray="6 8" opacity={0.7} />
				<text x={18} y={H - 26} fontFamily={FONT} fontWeight={800} fontSize={26} fill={c('amber-4')}>
					{label}
				</text>
			</g>,
		);
	});
	return (
		<AbsoluteFill style={{backgroundColor: c('ink-1')}}>
			<svg width={1080} height={1920} viewBox="0 0 1080 1920">
				<LightProvider light={LANTERN}>{tiles}</LightProvider>
			</svg>
		</AbsoluteFill>
	);
};

export const Assets: React.FC = () => {
	waitForFonts();
	const t = useCurrentFrame() / 30 + 0.9;
	const light: SceneLight = {...LANTERN, key: dirDeg(-115), keyColor: 'amber-5'};
	return (
		<AbsoluteFill style={{backgroundColor: c('ink-2')}}>
			<svg width={1080} height={1920} viewBox="0 0 1080 1920">
				<LightProvider light={light}>
					<GradientField
						id="af"
						stops={[
							[0, 'tide-2'],
							[0.3, 'tide-0'],
							[0.7, 'ink-4'],
							[1, 'ink-2'],
						]}
						glow={{x: 200, y: 0, r: 900, color: 'tide-5', a: 0.3}}
					/>
					<Kelp seed="ak" x={980} y={1920} h={900} t={t} />
					<Rock id="ark" x={160} y={1880} rx={200} ry={120} lod="hero" />
					<FishSchool t={t} seed="af" n={10} cx={300} cy={1500} rx={160} ry={70} scale={1.4} />
					<g transform="translate(40 230) scale(1.02)">
						<Orca id="aorca" t={t} />
					</g>
					<g transform="translate(880 1000) scale(1.5)">
						<Diver id="adiver" t={t} flip waveAt={0.2} />
					</g>
					<Specks t={t} seed="asn" n={120} size={[3, 7]} />
					<text x={40} y={80} fontFamily={FONT} fontWeight={800} fontSize={34} fill={c('bone-2')}>
						Hero assets, procedural shading only
					</text>
				</LightProvider>
			</svg>
		</AbsoluteFill>
	);
};
