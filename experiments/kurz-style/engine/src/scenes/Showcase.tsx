/**
 * 4 s engine showcase: the orca shot rebuilt with every engine system (1080x1920, 30 fps).
 *
 *   P0 field    3-stop+ water gradient, surface band, sun emitter, god rays + surface caustics (ONE screen layer)
 *   P1 far      ridges with an arch, a distant pod (orca LOD 'far'), small specks         haze 0.62
 *   P2 mid      seabed + sand caustics, shaded rocks, kelp forest, anemones, urchins, fish school, jellies,
 *               the orca's cast shadow on the sand                                       haze 0.32
 *   P3 subject  hero orca + hero diver (full 9-layer shading), bubbles, marine snow, lantern tags
 *   P4 fore     ink kelp + rock silhouettes cropped by the frame, bokeh                   haze 0.8 ink, blur 9
 *
 * Light as an actor: the key sweeps 12° over the shot (sun slides with it), so every terminator crawls.
 * Camera: eased lateral move + push with drift and hand-held noise; parallax ratio fore/subject = 1.45.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {c, rgba} from '../lib/color';
import {dirDeg, LightProvider, type SceneLight} from '../lib/light';
import {CameraProvider, Plane} from '../depth/Planes';
import {Bokeh, Bubbles, Caustics, Emitter, GradientField, LightLayer, Rays, Specks, SurfaceBand, Bloom} from '../depth/Atmosphere';
import {Orca} from '../assets/Orca';
import {Diver} from '../assets/Diver';
import {Anemone, FishSchool, Jelly, Kelp, Ridge, Rock, SeaFan, SeaGrass, Seabed, Shell, Urchin} from '../assets/Ocean';
import {cameraAt, ease} from '../motion/motion';
import {LanternTag, waitForFonts} from '../lib/type';

export const Showcase: React.FC = () => {
	waitForFonts();
	const frame = useCurrentFrame();
	const {fps, durationInFrames} = useVideoConfig();
	const t = frame / fps;
	const T = durationInFrames / fps;
	const u = t / T;

	// light as an actor: key sweeps from -118° to -106° (toward the upper left), the sun slides with it
	const keyAng = -118 + 12 * ease.drift(u);
	const light: SceneLight = {
		key: dirDeg(keyAng),
		keyColor: 'amber-5',
		rim: dirDeg(42),
		rimColor: 'tide-4',
		ambient: 'ink-2',
		ground: 'ochre-2',
		haze: 'tide-1',
	};
	const sunX = 540 + Math.cos((keyAng * Math.PI) / 180) * 1000;
	const sunY = 30;

	const cam = cameraAt(t, {x: -40, y: 26, zoom: 1, roll: 0}, [{at: 0.3, dur: 3.3, to: {x: 34, y: -12, zoom: 1.065}, ease: ease.drift}], {
		zoomPerS: 0.004,
		xPerS: 5,
		hand: 3,
		seed: 'show',
	});

	// hero placement (subject plane, frame coordinates)
	const ox = 110 + 34 * t;
	const oy = 700 + 10 * Math.sin(t * 1.1);
	const S = 0.7;
	const pitch = -2 + 1.5 * Math.cos(t * 1.1);
	const dx = 1004;
	const dy = 1180 + 9 * Math.sin(t * 1.5 + 1);
	const DS = 0.44;

	return (
		<LightProvider light={light}>
			<CameraProvider cam={cam}>
				<AbsoluteFill style={{backgroundColor: c('ink-2')}}>
					{/* P0 field */}
					<Plane preset="field">
						<GradientField
							id="sea"
							stops={[
								[0, 'tide-3'],
								[0.1, 'tide-2'],
								[0.3, 'tide-0'],
								[0.55, 'ink-4'],
								[0.8, 'ink-3'],
								[1, 'ink-2'],
							]}
							glow={{x: sunX, y: sunY + 60, r: 1100, color: 'tide-5', a: 0.42}}
						/>
						<SurfaceBand t={t} y={-150} />
						<LightLayer>
							<Caustics t={t} seed="surf" area={[-260, -260, 1600, 600]} cell={76} color="tide-5" alpha={0.14} width={3.4} />
							<Rays t={t} seed="sun" x={sunX} y={sunY - 60} n={8} angle={74} spread={46} len={2600} alpha={0.13} />
							<Emitter id="sun" x={sunX} y={sunY - 140} r={60} t={t} ramp={['bone-2', 'amber-5', 'amber-4']} halo="amber-5" haloScale={1.4} sparkles={7} />
						</LightLayer>
					</Plane>

					{/* P1 far */}
					<Plane preset="far">
						<Ridge seed="r1" y={1380} h={170} color="ink-3" arch={800} />
						{[0, 1, 2].map((i) => (
							<g key={i} transform={`translate(${600 + i * 150 - 14 * t} ${430 + i * 46 + (i === 1 ? 30 : 0)}) scale(${0.17 - i * 0.02})`}>
								<Orca id={`pod${i}`} t={t + i * 0.7} lod="far" />
							</g>
						))}
						<Kelp seed="fk1" x={-40} y={1420} h={620} t={t} blade={0.7} />
						<Kelp seed="fk2" x={330} y={1400} h={460} t={t} blade={0.6} />
						<Kelp seed="fk3" x={1110} y={1420} h={700} t={t} blade={0.7} />
						<Ridge seed="r2" y={1520} h={110} color="ink-2" />
						<FishSchool t={t} seed="farfish" n={22} cx={260} cy={980} rx={200} ry={80} scale={0.45} dir={-1} />
						<Specks t={t} seed="sn-far" n={130} size={[2, 4.5]} drift={[3, -4]} opacity={[0.25, 0.6]} />
					</Plane>

					{/* P2 mid */}
					<Plane preset="mid">
						<Jelly id="j1" x={160} y={560} s={44} t={t} />
						<Jelly id="j2" x={950} y={400} s={32} t={t + 1.3} />
						<Kelp seed="k1" x={30} y={1650} h={980} t={t} blade={1.25} />
						<Kelp seed="k2" x={170} y={1680} h={720} t={t} blade={0.9} />
						<Kelp seed="k3" x={890} y={1660} h={680} t={t} blade={0.9} />
						<Kelp seed="k4" x={1050} y={1650} h={1050} t={t} blade={1.25} />
						<Seabed y={1600} t={t} />
						<g>
							<defs>
								<radialGradient id="orcaCast">
									<stop offset="0" stopColor={rgba(c('ink-2'), 0.42)} />
									<stop offset="1" stopColor={rgba(c('ink-2'), 0)} />
								</radialGradient>
							</defs>
							<ellipse cx={ox * 0.6 + 330 - light.key[0] * 160} cy={1690} rx={300} ry={38} fill="url(#orcaCast)" />
						</g>
						<Caustics t={t} seed="sand" area={[-260, 1610, 1600, 520]} cell={60} color="amber-5" alpha={0.17} width={3} fadeDown={false} />
						<SeaFan x={250} y={1640} h={330} t={t} seed="fan1" />
						<SeaFan x={1020} y={1640} h={300} t={t} seed="fan2" color="amber-3" />
						<SeaFan x={600} y={1700} h={200} t={t} seed="fan3" color="coral-2" />
						<Rock id="rk1" x={110} y={1650} rx={150} ry={92} />
						<Rock id="rk2" x={340} y={1716} rx={86} ry={52} barnacles={4} />
						<Rock id="rk3" x={910} y={1668} rx={170} ry={104} />
						<Rock id="rk4" x={650} y={1740} rx={62} ry={36} barnacles={3} moss={false} />
						<SeaGrass x={500} y={1690} h={90} t={t} seed="sg1" />
						<SeaGrass x={760} y={1672} h={120} t={t} seed="sg2" n={9} />
						<SeaGrass x={1020} y={1740} h={80} t={t} seed="sg3" />
						<Anemone x={430} y={1712} s={70} t={t} seed="an1" />
						<Anemone x={780} y={1726} s={56} t={t} seed="an2" color="amber-3" />
						<Urchin x={560} y={1744} r={18} t={t} seed="u1" />
						<Urchin x={250} y={1770} r={14} t={t} seed="u2" />
						<Shell x={700} y={1790} s={1.3} rot={-10} />
						<Shell x={190} y={1810} s={1.1} rot={14} />
						<FishSchool t={t} seed="fish" n={26} cx={790} cy={1330} rx={230} ry={110} scale={0.9} />
					</Plane>

					{/* P3 subject */}
					<Plane preset="subject">
						<g transform={`translate(${ox} ${oy}) rotate(${pitch} ${490 * S} ${215 * S}) scale(${S})`}>
							<Orca id="orca" t={t} rot={pitch} />
						</g>
						<Bubbles t={t} seed="reg" x={dx - 514 * DS} y={dy + 118 * DS} n={18} rate={4} rise={110} size={[3, 11]} />
						<g transform={`translate(${dx} ${dy}) scale(${DS})`}>
							<Diver id="diver" t={t} flip waveAt={1.5} />
						</g>
						<LightLayer opacity={0.8}>
							<Bloom id="diverBloom" x={dx - 130} y={dy + 40} rx={220} ry={120} color="tide-4" a={0.18} />
						</LightLayer>
						<Specks t={t} seed="sn" n={150} size={[3, 8]} drift={[5, -7]} />
						<LanternTag t={t} at={0.8} x={300} y={560} ax={ox + 640 * S} ay={oy + 150 * S} text="ORCA" sub="8 m" />
						<LanternTag t={t} at={2.05} x={850} y={1060} ax={dx - 350 * DS} ay={dy + 40 * DS} text="YOU" ring="signal-1" />
					</Plane>

					{/* P4 foreground */}
					<Plane preset="fore">
						<Kelp seed="fg1" x={-60} y={2120} h={1250} t={t} blade={2.3} silhouette />
						<Kelp seed="fg2" x={1150} y={2150} h={900} t={t} blade={2} silhouette lean={-6} />
						<Rock id="fgr" x={980} y={2010} rx={280} ry={170} lod="far" moss={false} barnacles={0} />
						<Bokeh t={t} seed="bk" n={12} r={[16, 46]} />
					</Plane>

					{/* screen-locked vignette (normal blend gradient: free) */}
					<AbsoluteFill style={{background: `radial-gradient(ellipse 80% 62% at 50% 46%, ${rgba(c('ink-0'), 0)} 58%, ${rgba(c('ink-0'), 0.5)} 100%)`}} />
				</AbsoluteFill>
			</CameraProvider>
		</LightProvider>
	);
};
