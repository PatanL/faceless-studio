/**
 * Orca pilot, first 9.73 s (p00 + p01 of episodes/explainer-orca/storyboard.json), rebuilt on the engine in the
 * "Lantern & Ink" house style. 1080x1920, 30 fps, one continuous set, no hard cuts: every new composition comes
 * from a camera move, an acting beat or a light event.
 *
 *   A 0.00-3.06  hook   "Wild killer whales could kill you easily. They never have."
 *                       cover = YOU under the orca's head; pull-back reveals the whole animal; "0" pulses + ring ping
 *   B 3.06-4.45  threat "Not because they can't."  push-in on the head, anticipation, jaw opens on teeth, diver
 *                       flinches (bubble burst) and swims off
 *   C 4.45-7.75  scale  lit/unlit light event isolates the orca; 8 m bar + ticking counter; four cars drop onto a
 *                       platform that dips under each one; "≈ 6 tonnes" counter
 *   D 7.75-9.73  fin    push up to the dorsal fin; the YOU figure pops onto the back; equal-height guides
 *
 * Planes: field / far / mid / [unlit pass] / subject / fore, then screen-space titles and captions.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {c, mixOk, rgba} from '../lib/color';
import {dirDeg, LightProvider, type SceneLight} from '../lib/light';
import {CameraProvider, Plane} from '../depth/Planes';
import {Bokeh, Bubbles, Caustics, Emitter, GradientField, LightLayer, Rays, Specks, SurfaceBand} from '../depth/Atmosphere';
import {Orca} from '../assets/Orca';
import {Diver} from '../assets/Diver';
import {Anemone, FishSchool, Jelly, Kelp, Ridge, Rock, SeaGrass, Seabed, Shell, Urchin} from '../assets/Ocean';
import {BrainCoral, FanCoral, ReefShelf, Spire, Staghorn, TableCoral, TubeSponge} from '../assets/Reef';
import {Car} from '../assets/Car';
import {YouFigure} from '../assets/YouFigure';
import {cameraAt, clamp, ease, lerp, popIn, prog, springAt, SETTLE, type Cam} from '../motion/motion';
import {LanternTag, waitForFonts} from '../lib/type';
import {Captions, Counter, TitlePlate, UnlitPass, type Phrase} from '../lib/titles';
import {swimBend} from '../lib/geom';
import {rand} from '../lib/rng';

export const ORCA_OPEN_FRAMES = 292; // 9.733 s: ends after "...as tall as you." (9.48), before "It hits" (9.78)

// caption phrases from the storyboard's word timings (kokoro captions.json)
const PHRASES: Phrase[] = [
	{text: 'Wild killer whales', start: 0.0, end: 0.97},
	{text: 'could kill you easily.', start: 0.97, end: 2.195, emph: ['kill']},
	{text: 'They never have.', start: 2.195, end: 3.21, emph: ['never']},
	{text: "Not because they can't.", start: 3.21, end: 4.495, emph: ["can't"]},
	{text: 'A big male', start: 4.495, end: 5.232},
	{text: 'is eight metres long,', start: 5.232, end: 6.345, emph: ['eight', 'metres']},
	{text: 'as heavy as four cars,', start: 6.345, end: 7.77, emph: ['four', 'cars']},
	{text: 'and its fin alone', start: 7.77, end: 8.645, emph: ['fin']},
	{text: 'is as tall as you.', start: 8.645, end: 10, emph: ['you']},
];

const S = 0.8; // orca scale on the subject plane
const DS = 0.36; // diver scale
const focus = (X: number, Y: number, z: number): Cam => ({x: z * (X - 540), y: z * (Y - 960), zoom: z, roll: 0});
const toScreen = (cam: Cam, x: number, y: number): [number, number] => [540 - cam.x + cam.zoom * (x - 540), 960 - cam.y + cam.zoom * (y - 960)];

export const OrcaOpen: React.FC = () => {
	waitForFonts();
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;

	// ---------------------------------------------------------------- light (an actor: slow 8° key sweep)
	const keyAng = -118 + 8 * ease.drift(t / 9.7);
	const light: SceneLight = {key: dirDeg(keyAng), keyColor: 'amber-5', rim: dirDeg(42), rimColor: 'tide-4', ambient: 'ink-2', ground: 'ochre-2', haze: 'tide-1'};
	const sunX = 540 + Math.cos((keyAng * Math.PI) / 180) * 900;

	// ---------------------------------------------------------------- camera: one set, moves instead of cuts
	const cam = cameraAt(
		t,
		focus(790, 1000, 1.62),
		[
			{at: 0.3, dur: 2.3, to: focus(540, 905, 1.0), ease: ease.drift}, // A: pull-back reveal
			{at: 3.1, dur: 0.9, to: focus(880, 965, 2.0), ease: ease.travel}, // B: push-in on the head (teeth readable at phone size)
			{at: 4.42, dur: 1.15, to: focus(548, 1000, 1.1), ease: ease.travel}, // C: scale board, hero fills the width
			{at: 7.7, dur: 1.15, to: focus(560, 760, 1.5), ease: ease.travel}, // D: up to the fin
		],
		{zoomPerS: 0.005, xPerS: 3, hand: 2.5, seed: 'oo', steady: 0.4},
	);

	// ---------------------------------------------------------------- orca acting
	const jawOpen = springAt(t, 3.45, SETTLE) * (1 - ease.drift(prog(t, 4.3, 0.45)));
	const antic = t > 3.22 && t < 3.45 ? Math.sin(Math.PI * prog(t, 3.22, 0.23)) : 0; // head dips before the bite
	const ox = 140 + 6 * t;
	const oy = 688 + 8 * Math.sin(t * 1.1) + 6 * antic;
	const pitch = -2 + 1.5 * Math.cos(t * 1.1) - 5 * jawOpen + 1.8 * antic;
	const pv = (pitch * Math.PI) / 180;
	const pcx = ox + 490 * S;
	const pcy = oy + 215 * S;
	const bend = swimBend({head: 990, tail: 15, amp: 26, t, freq: 0.55, lag: 1.9});
	const orcaPt = (lx: number, ly: number): [number, number] => {
		const [bx, by] = bend(lx, ly);
		const x = ox + bx * S - pcx;
		const y = oy + by * S - pcy;
		return [pcx + x * Math.cos(pv) - y * Math.sin(pv), pcy + x * Math.sin(pv) + y * Math.cos(pv)];
	};
	const menace = clamp(prog(t, 3.25, 0.25)) * (1 - prog(t, 4.5, 0.4));
	const lid = 0.26 + 0.2 * menace;
	const look: [number, number] = t < 4.5 ? [0.1 + 0.4 * menace, 0.7 - 0.3 * menace] : [0.5, 0.15];

	// ---------------------------------------------------------------- diver ("YOU" in the hook)
	const flinch = springAt(t, 3.62, SETTLE);
	const away = ease.travel(prog(t, 4.2, 1.3));
	const dx = 930 - 10 * t - 60 * flinch - 640 * away;
	const dy = 1040 + 6 * Math.sin(1.4 * t) + 48 * flinch + 420 * away;
	const drot = -9 * flinch * (1 - away) + 12 * away;
	const reg: [number, number] = [dx - 514 * DS, dy + 118 * DS];
	const showDiver = t < 5.6;

	// ---------------------------------------------------------------- scale board (C)
	const [fx0, fy0] = orcaPt(15, 230);
	const [fx1, fy1] = orcaPt(990, 214);
	const barY = oy + 430 * S;
	const barP = ease.travel(prog(t, 5.0, 0.85));
	const barOut = ease.exit(prog(t, 6.3, 0.3));
	const platY = 1182;
	const platIn = ease.travel(prog(t, 6.35, 0.35));
	const platOut = ease.exit(prog(t, 7.85, 0.3));
	const impact = (i: number) => 6.55 + 0.13 * i + 0.22;
	let platDip = 0;
	for (let i = 0; i < 4; i++) {
		const d = t - impact(i);
		if (d > 0) platDip += 7 * Math.exp(-d * 6) * Math.sin(d * 20);
	}
	const CARS = ['coral-3', 'amber-3', 'tide-2', 'bone-1'];

	// ---------------------------------------------------------------- fin beat (D)
	const [footX, footY] = orcaPt(468, 143);
	const [finTipX, finTipY] = orcaPt(598, -54);
	const [finMidX, finMidY] = orcaPt(612, 40);
	const figS = 0.76 * S / 0.8; // 200 local -> fin height (≈ 152 px)
	const figPop = popIn(t, 7.95);
	const headY = footY - 200 * figS;
	const guideP = ease.travel(prog(t, 8.62, 0.5));

	// ---------------------------------------------------------------- lit/unlit pass (C, D)
	const unlitA = 0.4 * ease.drift(prog(t, 4.45, 0.7)) - 0.1 * ease.drift(prog(t, 7.8, 0.8));
	const holeC: [number, number] = t < 7.8 ? orcaPt(520, 250) : [lerp(orcaPt(520, 250)[0], (footX + finTipX) / 2, ease.drift(prog(t, 7.8, 0.9))), lerp(orcaPt(520, 250)[1], (footY + finTipY) / 2, ease.drift(prog(t, 7.8, 0.9)))];
	const [hx, hy] = toScreen(cam, holeC[0], holeC[1] + 60);
	const holeR = lerp(680, 460, ease.drift(prog(t, 7.8, 0.9)));

	// bubble burst when the diver flinches
	const burst: React.ReactNode[] = [];
	if (t > 3.62 && t < 6) {
		for (let i = 0; i < 14; i++) {
			const age = t - 3.62 - rand('burst', i) * 0.12;
			if (age < 0) continue;
			const r = 4 + rand('burst', i + 20) * 9;
			const bx = reg[0] + (rand('burst', i + 40) - 0.5) * 50 + Math.sin(age * 6 + i) * 8;
			const by = reg[1] - age * (150 + r * 9) - rand('burst', i + 60) * 20;
			burst.push(
				<g key={i} transform={`translate(${bx.toFixed(1)} ${by.toFixed(1)}) scale(${Math.min(1, age * 8).toFixed(3)})`}>
					<circle r={r} fill={rgba(c('tide-5'), 0.16)} stroke={c('tide-5')} strokeWidth={Math.max(1.4, r * 0.22)} opacity={0.85} />
					<path d={`M ${-r * 0.55} ${-r * 0.1} A ${r * 0.6} ${r * 0.6} 0 0 1 ${-r * 0.05} ${-r * 0.6}`} stroke={c('bone-2')} strokeWidth={Math.max(1.2, r * 0.2)} strokeLinecap="round" fill="none" />
				</g>,
			);
		}
	}

	const youTagFade = 1 - ease.exit(prog(t, 2.85, 0.3));

	return (
		<LightProvider light={light}>
			<CameraProvider cam={cam}>
				<AbsoluteFill style={{backgroundColor: c('ink-2')}}>
					{/* P0 field */}
					<Plane preset="field">
						<GradientField
							id="sea"
							stops={[
								[0, 'tide-4'],
								[0.1, 'tide-3'],
								[0.3, 'tide-2'],
								[0.55, 'tide-1'],
								[0.8, 'tide-0'],
								[1, 'ink-4'],
							]}
							glow={{x: sunX, y: 60, r: 1150, color: 'tide-5', a: 0.4}}
						/>
						<SurfaceBand t={t} y={30} />
						<LightLayer>
							<Caustics t={t} seed="surf" area={[-260, -200, 1600, 520]} cell={84} color="tide-5" alpha={0.16} width={3.6} />
							<Rays t={t} seed="sun" x={sunX} y={-40} n={8} angle={70} spread={50} len={2600} alpha={0.14} />
							<Emitter id="sun" x={sunX} y={-110} r={58} t={t} ramp={['bone-2', 'amber-5', 'amber-4']} halo="amber-5" haloScale={1.4} sparkles={6} />
						</LightLayer>
					</Plane>

					{/* P1 far: designed spires + arch, distant pod, far kelp */}
					<Plane preset="far">
						{[0, 1, 2].map((i) => (
							<g key={i} transform={`translate(${560 + i * 150 - 16 * t} ${470 + i * 50 + (i === 1 ? 26 : 0)}) scale(${0.16 - i * 0.02})`}>
								<Orca id={`pod${i}`} t={t + i * 0.7} lod="far" />
							</g>
						))}
						<Spire seed="sp1" x={130} y={1620} w={170} h={560} arch />
						<Spire seed="sp2" x={900} y={1640} w={210} h={720} />
						<Spire seed="sp3" x={640} y={1640} w={110} h={300} />
						<Kelp seed="fk1" x={380} y={1640} h={560} t={t} blade={0.6} />
						<Kelp seed="fk3" x={1110} y={1640} h={760} t={t} blade={0.7} />
						<Ridge seed="r2" y={1660} h={90} color="ink-3" />
						<FishSchool t={t} seed="farfish" n={22} cx={300} cy={1060} rx={200} ry={80} scale={0.42} dir={-1} />
						<Specks t={t} seed="sn-far" n={140} size={[2, 4.5]} drift={[-6, -4]} opacity={[0.25, 0.6]} />
					</Plane>

					{/* P2 mid: reef shelf with warm subject masses, kelp, jellies, school */}
					<Plane preset="mid" spec={{haze: 0.14, desat: 0}} haze="tide-2">
						<Jelly id="j1" x={150} y={560} s={42} t={t} />
						<Jelly id="j2" x={960} y={430} s={30} t={t + 1.3} />
						<Jelly id="j3" x={880} y={250} s={46} t={t + 0.6} base="coral-3" glow="amber-4" />
						<Jelly id="j4" x={250} y={880} s={34} t={t + 2.1} base="amber-3" glow="amber-5" />
						<Jelly id="j5" x={700} y={560} s={26} t={t + 3.3} base="coral-3" glow="amber-4" />
						<g transform="translate(0 -130)">
						<Kelp seed="k1" x={30} y={1720} h={1020} t={t} blade={1.2} />
						<Kelp seed="k2" x={200} y={1740} h={700} t={t} blade={0.9} />
						<Kelp seed="k3" x={890} y={1730} h={660} t={t} blade={0.9} />
						<Kelp seed="k4" x={1060} y={1720} h={1060} t={t} blade={1.2} />
						<ReefShelf seed="shelf" y={1700} h={110} />
						<Seabed y={1790} t={t} deep={mixOk(c('ochre-2'), c('kelp-1'), 0.45)} />
						<FanCoral id="fan1" x={250} y={1690} h={340} t={t} />
						<FanCoral id="fan2" x={1000} y={1700} h={300} t={t} base="amber-3" />
						<TableCoral id="tab1" x={790} y={1712} w={250} />
						<BrainCoral id="br1" x={330} y={1760} r={104} />
						<BrainCoral id="br2" x={1010} y={1790} r={78} base="coral-2" />
						<TubeSponge id="tube1" x={560} y={1748} h={200} t={t} />
						<TubeSponge id="tube2" x={110} y={1790} h={150} t={t} n={3} base="amber-3" />
						<Staghorn id="stag1" x={665} y={1770} h={190} t={t} />
						<Rock id="rk1" x={470} y={1800} rx={110} ry={62} barnacles={4} />
						<Rock id="rk2" x={880} y={1810} rx={90} ry={50} barnacles={3} moss={false} />
						<SeaGrass x={430} y={1770} h={90} t={t} seed="sg1" />
						<SeaGrass x={740} y={1760} h={110} t={t} seed="sg2" n={9} />
						<Anemone x={210} y={1800} s={64} t={t} seed="an1" />
						<Anemone x={940} y={1790} s={52} t={t} seed="an2" color="amber-3" />
						<Urchin x={600} y={1820} r={16} t={t} seed="u1" />
						<Shell x={760} y={1850} s={1.3} rot={-10} />
						</g>
						<FishSchool t={t} seed="fish" n={24} cx={820} cy={1330} rx={220} ry={100} scale={0.85} />
					</Plane>

					{/* lit/unlit pass: everything behind the subject goes toward ink outside the light */}
					<UnlitPass a={unlitA} x={hx} y={hy} rx={holeR * cam.zoom} ry={holeR * 0.7 * cam.zoom} color="ink-2" />
					{/* the lit side of the light event: a lantern lift on the subject (one screen layer) */}
					{unlitA > 0.01 ? (
						<AbsoluteFill style={{mixBlendMode: 'screen', opacity: unlitA * 1.2, background: `radial-gradient(${(holeR * 0.8 * cam.zoom).toFixed(0)}px ${(holeR * 0.5 * cam.zoom).toFixed(0)}px at ${hx.toFixed(0)}px ${hy.toFixed(0)}px, ${rgba(c('amber-4'), 0.22)} 0%, ${rgba(c('tide-3'), 0.1)} 55%, ${rgba(c('tide-3'), 0)} 100%)`}} />
					) : null}

					{/* P3 subject */}
					<Plane preset="subject">
						{showDiver ? <Bubbles t={t} seed="reg" x={reg[0]} y={reg[1]} n={16} rate={3.6} rise={100} size={[3, 10]} /> : null}
						<g transform={`translate(${ox} ${oy}) rotate(${pitch} ${490 * S} ${215 * S}) scale(${S})`}>
							<Orca id="orca" t={t} rot={pitch} jaw={jawOpen} lid={lid} look={look} detail />
						</g>
						{showDiver ? (
							<g transform={`translate(${dx} ${dy}) rotate(${drot} ${-300 * DS} ${90 * DS}) scale(${DS})`}>
								<Diver id="diver" t={t} flip waveAt={2.3} />
							</g>
						) : null}
						{burst}
						{youTagFade > 0 ? (
							<g opacity={youTagFade}>
								<LanternTag t={t} at={-1} x={dx - 120} y={dy + 170} ax={dx - 300 * DS} ay={dy + 96 * DS} text="YOU" ring="signal-1" size={38} />
							</g>
						) : null}

						{/* C: 8 m bar with ring ends and a ticking counter */}
						{t > 5.0 && barOut < 1 ? (
							<g opacity={1 - barOut}>
								{[fx0, fx1].map((xx, i) => (
									<line key={i} x1={xx} y1={barY - 18} x2={xx} y2={(i ? fy1 : fy0) + 6} stroke={c('bone-2')} strokeWidth={3} strokeDasharray="8 9" strokeLinecap="round" opacity={0.7 * clamp((barP - (i ? 0.85 : 0)) * 6)} />
								))}
								<line x1={fx0} y1={barY} x2={fx0 + (fx1 - fx0) * barP} y2={barY} stroke={c('bone-2')} strokeWidth={6} strokeLinecap="round" />
								{Array.from({length: 9}, (_, i) => {
									const xx = fx0 + ((fx1 - fx0) * i) / 8;
									const on = clamp((barP * 8 - i) * 3 + 1);
									const big = i === 0 || i === 8;
									return on > 0 ? (
										<g key={i} opacity={on}>
											<line x1={xx} y1={barY - (big ? 24 : 12) * on} x2={xx} y2={barY + (big ? 24 : 12) * on} stroke={c('bone-2')} strokeWidth={big ? 5 : 3.5} strokeLinecap="round" />
											{big ? (
												<g>
													<circle cx={xx} cy={barY - 30} r={10} fill="none" stroke={c('bone-2')} strokeWidth={3.5} />
													<circle cx={xx} cy={barY - 30} r={4.5} fill={c('tide-4')} />
												</g>
											) : null}
										</g>
									) : null;
								})}
							</g>
						) : null}
						<Counter t={t} at={5.05} dur={0.95} to={8} decimals={1} x={(fx0 + fx1) / 2} y={barY + 150} size={150} unit="m" out={6.3} />

						{/* C: platform + four cars */}
						{platIn > 0 && platOut < 1 ? (
							<g transform={`translate(545 ${platY + platDip}) scale(${platIn * (1 - platOut)} 1)`}>
								<rect x={-440} y={6} width={880} height={26} rx={13} fill={rgba(c('ink-0'), 0.45)} />
								<rect x={-440} y={0} width={880} height={24} rx={12} fill={c('ink-3')} />
								<rect x={-436} y={1} width={872} height={5} rx={2.5} fill={c('tide-4')} opacity={0.85} />
								{[-330, -110, 110, 330].map((xx) => (
									<g key={xx}>
										<circle cx={xx} cy={13} r={6} fill="none" stroke={c('bone-0')} strokeWidth={2.5} />
										<circle cx={xx} cy={13} r={2.5} fill={c('signal-1')} />
									</g>
								))}
							</g>
						) : null}
						{CARS.map((col, i) => {
							const at = 6.55 + 0.13 * i;
							if (t < at) return null;
							const p = prog(t, at, 0.22);
							const fall = -420 * (1 - p * p);
							const d = t - impact(i);
							const sq = d > 0 ? 0.13 * Math.exp(-d * 10) * Math.cos(d * 28) : 0;
							const sink = ease.exit(prog(t, 7.72 + 0.04 * i, 0.4));
							if (sink >= 1) return null;
							const cx = 545 + (i - 1.5) * 198;
							const cs = 0.86;
							return (
								<g key={i} opacity={clamp(p * 4) * (1 - sink)} transform={`translate(${cx} ${platY + platDip + fall + sink * 520}) rotate(${sink * (i % 2 ? 14 : -12)}) scale(${cs * (1 + 0.5 * sq)} ${cs * (1 - sq)})`}>
									<ellipse cx={0} cy={2} rx={96 * (0.6 + 0.4 * p)} ry={7} fill={rgba(c('ink-0'), 0.4 * p)} />
									<g transform="translate(-105 -88)">
										<Car id={`car${i}`} base={col} spin={t * 3} />
									</g>
								</g>
							);
						})}
						<Counter t={t} at={6.98} dur={0.45} to={6} decimals={1} x={545} y={1306} size={120} prefix="≈" unit="tonnes" out={7.7} />

						{/* D: the YOU figure on the back, equal-height guides, tags */}
						{t >= 7.95 ? (
							<g transform={`translate(${footX} ${footY}) scale(${figS * figPop})`}>
								<YouFigure id="you" t={t} waveAt={9.12} />
							</g>
						) : null}
						{guideP > 0 ? (
							<g strokeLinecap="round">
								{[
									[headY, finTipY],
									[footY, footY],
								].map(([y0, y1], i) => {
									const x0 = footX - 70;
									const x1 = finTipX + 40;
									const xe = x0 + (x1 - x0) * guideP;
									const ye = y0 + (y1 - y0) * guideP;
									return (
										<g key={i}>
																						<line x1={x0} y1={y0} x2={xe} y2={ye} stroke={c('bone-2')} strokeWidth={4} strokeDasharray="12 10" />
										</g>
									);
								})}
							</g>
						) : null}
						<LanternTag t={t} at={8.15} x={finTipX + 120} y={finTipY - 70} ax={finMidX + 8} ay={finMidY} text="FIN" sub="1.8 m" size={40} />
						<LanternTag t={t} at={9.15} x={footX - 170} y={headY - 70} ax={footX} ay={headY + 30} text="YOU" ring="signal-1" size={40} />

						<Specks t={t} seed="sn" n={160} size={[3, 8]} drift={[-14, -6]} />
					</Plane>

					{/* P4 foreground: ink silhouettes cropped by the frame, bokeh */}
					<Plane preset="fore">
						<Kelp seed="fg1" x={-40} y={2160} h={1300} t={t} blade={2.3} silhouette />
						<Kelp seed="fg2" x={1160} y={2160} h={980} t={t} blade={2} silhouette lean={-6} />
						<Rock id="fgr" x={1000} y={2040} rx={300} ry={170} lod="far" moss={false} barnacles={0} />
						<Staghorn id="fgst" x={70} y={2080} h={330} t={t} base="ink-1" />
						<Bokeh t={t} seed="bk" n={12} r={[16, 46]} />
					</Plane>

					<AbsoluteFill style={{background: `radial-gradient(ellipse 80% 62% at 50% 46%, ${rgba(c('ink-0'), 0)} 58%, ${rgba(c('ink-0'), 0.48)} 100%)`}} />
				</AbsoluteFill>
			</CameraProvider>

			{/* screen-space type */}
			<TitlePlate
				t={t}
				at={-1}
				out={3.0}
				y={116}
				size={116}
				lines={[[{text: '0', color: 'signal-1'}, {text: '\u00a0HUMAN KILLS'}]]}
				sub={{text: 'IN THE WILD', color: 'tide-4'}}
				subSize={42}
				pulse={{at: 2.25, index: [0, 0]}}
			/>
			<Captions t={t} phrases={PHRASES} y={1350} size={62} />
		</LightProvider>
	);
};
