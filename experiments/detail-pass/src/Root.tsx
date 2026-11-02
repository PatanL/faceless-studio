import React from 'react';
import {AbsoluteFill, Composition, Still} from 'remotion';
import {DetailShowcase} from './scenes/DetailShowcase';
import {OrcaOpenDetail} from './scenes/OrcaOpenDetail';
import {FRAMES as ORCA_FRAMES} from './scenes/orcaLayout';
import {c} from '../../kurz-style/engine/src/lib/color';
import {LightProvider} from '../../kurz-style/engine/src/lib/light';
import {Fish} from './detail/Fish';
import {SPECIES} from './detail/species';
import {Ball, Brain, Branch, Rock, Soft, Star, Table, Tubes, Urchin, Vase, VarKelp} from './detail/flora';
import {Turtle} from './assets/Turtle';
import {lightAt} from './scenes/layout';

/** proof sheet: every species (3 variants each), every reef generator (2 seeds each), the hero at 1:1 */
const Sheet: React.FC = () => {
	const L = lightAt(0);
	const sp = Object.keys(SPECIES);
	return (
		<LightProvider light={L}>
			<AbsoluteFill style={{backgroundColor: c('tide-2')}}>
				<svg width={1080} height={1920}>
					{sp.map((s, i) =>
						[0, 1, 2].map((j) => <Fish key={`${s}${j}`} species={s} seed={`sheet${j}`} pose={{x: 150 + j * 330, y: 90 + i * 92, ang: 0, len: 150 - j * 25, t: j * 0.3, phase: j}} />),
					)}
					{[0, 1].map((j) => (
						<g key={j} transform={`translate(${j * 540} 0)`}>
							<Rock seed={`s${j}`} x={110} y={1000} rx={95} ry={60} />
							<Brain seed={`s${j}`} x={330} y={1000} r={80} base={j ? 'ochre-3' : 'kelp-3'} />
							<Branch seed={`s${j}`} x={110} y={1260} h={210} t={0} base={j ? 'amber-3' : 'coral-3'} />
							<Vase seed={`s${j}`} x={330} y={1260} h={200} base={j ? 'coral-2' : 'ochre-2'} />
							<Table seed={`s${j}`} x={110} y={1480} w={100} />
							<Tubes seed={`s${j}`} x={330} y={1480} h={150} t={0} base={j ? 'tide-2' : 'coral-2'} />
							<Soft seed={`s${j}`} x={110} y={1680} h={120} t={0} />
							<Ball seed={`s${j}`} x={250} y={1680} r={34} />
							<Star seed={`s${j}`} x={350} y={1660} s={26} />
							<Urchin seed={`s${j}`} x={450} y={1670} r={16} t={0} />
							<VarKelp seed={`s${j}`} x={470} y={1900} h={520 + j * 200} t={0} style={j ? 'broad' : 'lance'} bend={j ? 30 : -20} />
						</g>
					))}
				</svg>
			</AbsoluteFill>
		</LightProvider>
	);
};

const Hero: React.FC = () => {
	const L = lightAt(0);
	return (
		<LightProvider light={L}>
			<AbsoluteFill style={{backgroundColor: c('tide-2')}}>
				<svg width={1080} height={1920}>
					<g transform="translate(36 720) rotate(-7 300 215) scale(1.65)">
						<Turtle t={0.6} rot={-7} refKey={L.key} refRim={L.rim} />
					</g>
				</svg>
			</AbsoluteFill>
		</LightProvider>
	);
};

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="DetailShowcase" component={DetailShowcase} width={1080} height={1920} fps={30} durationInFrames={120} />
		<Composition id="OrcaOpenDetail" component={OrcaOpenDetail} width={1080} height={1920} fps={30} durationInFrames={ORCA_FRAMES} />
		<Still id="Sheet" component={Sheet} width={1080} height={1920} />
		<Still id="Hero" component={Hero} width={1080} height={1920} />
	</>
);
