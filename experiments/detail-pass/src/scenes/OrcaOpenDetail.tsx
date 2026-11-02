/**
 * Orca opening, detail pass (1080x1920, 30 fps, 9.733 s). The approved v3 opening (kurz-style/engine/src/
 * scenes/OrcaOpen.tsx) re-set with the detail-pass generators and asset-gen's path-B hero orca, for an A/B at
 * the same beats, camera, captions and narration mix:
 *
 *   A 0.00-3.06  hook   cover = YOU (diver) under the orca's head; pull-back reveals the whole animal; "0" pulse
 *   B 3.06-4.45  threat push-in on the head, anticipation, jaw opens on teeth, diver flinches + bubble burst
 *   C 4.45-7.75  scale  lit/unlit light event; 8 m bar + counter; four cars on a dipping platform; ≈ 6 tonnes
 *   D 7.75-9.73  fin    push up to the dorsal fin; YOU figure on the back; equal-height guides
 *
 * Planes: field / far (ridges, kelp columns, pod, far schools, micro) / back kelp / mid (rocky reef scatter,
 * herring, surfperch, sand lance, micro) / [unlit pass] / subject (orca, diver, front reef, micro) / fore.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {c, mixOk, rgba} from '../../../kurz-style/engine/src/lib/color';
import {LightProvider} from '../../../kurz-style/engine/src/lib/light';
import {CameraProvider, Plane} from '../../../kurz-style/engine/src/depth/Planes';
import {Bokeh, Bubbles, Caustics, Emitter, GradientField, LightLayer, Rays, SurfaceBand} from '../../../kurz-style/engine/src/depth/Atmosphere';
import {Anemone, Seabed} from '../../../kurz-style/engine/src/assets/Ocean';
import {Diver} from '../../../kurz-style/engine/src/assets/Diver';
import {Car} from '../../../kurz-style/engine/src/assets/Car';
import {YouFigure} from '../../../kurz-style/engine/src/assets/YouFigure';
import {clamp, ease, lerp, popIn, prog, springAt, SETTLE} from '../../../kurz-style/engine/src/motion/motion';
import {LanternTag, waitForFonts} from '../../../kurz-style/engine/src/lib/type';
import {Captions, Counter, TitlePlate, UnlitPass, type Phrase} from '../../../kurz-style/engine/src/lib/titles';
import {rand} from '../../../kurz-style/engine/src/lib/rng';
import {isOff} from '../../../kurz-style/engine/src/lib/flags';
import {Micro} from '../detail/Micro';
import {School} from '../detail/Fish';
import {Ball, Branch, FarMound, Grass, Rock, Shell, Soft, Star, Tubes, Urchin, Vase, VarKelp} from '../detail/flora';
import type {Placement} from '../detail/scatter';
import {OrcaHero} from '../assets/OrcaHero';
import {
	BACK_KELP,
	camAt,
	FAR_KELP,
	FAR_MOUNDS,
	FAR_REEF,
	FORE_KELP,
	FRONT_REEF,
	lightAt,
	MID_REEF,
	ORCA_ANCHORS as A,
	orcaPose,
	orcaPt,
	PIV,
	SB,
	SCHOOLS_FAR,
	SCHOOLS_MID,
	SINGLES,
	toScreen,
} from './orcaLayout';

// caption phrases: identical to v3 (episode word timings)
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

const DS = 0.36; // diver scale (v3)
/** the open-water band stays in a narrow value range so it reads as ONE calm mass */
const OPEN_HI = mixOk(c('tide-2'), c('tide-3'), 0.15);
const OPEN_LO = mixOk(c('tide-1'), c('tide-2'), 0.15);
/** giant kelp is golden brown, not green: a warm amber family in every frame */
const GIANT_KELP = 'amber-2';
/** cold-water boulders: cool brown-teal stone; their pink crusts read as coralline algae */
const ROCKS = [mixOk(c('ochre-1'), c('tide-1'), 0.45), mixOk(c('coral-1'), c('ochre-2'), 0.5), mixOk(c('ochre-2'), c('tide-2'), 0.5)];

/** placement -> generator (cold-water kinds only) */
const Item: React.FC<{p: Placement; t: number; lod?: 'mid' | 'far'}> = ({p, t, lod = 'mid'}) => {
	const pick = (arr: string[]) => arr[Math.floor(p.variant * arr.length) % arr.length];
	switch (p.kind) {
		case 'rock':
			return <Rock seed={p.seed} x={p.x} y={p.y} rx={p.size} ry={p.size * (0.5 + p.variant * 0.25)} lod={lod} base={pick(ROCKS)} />;
		case 'vase':
			return <Vase seed={p.seed} x={p.x} y={p.y} h={p.size} lod={lod} base={pick(['ochre-2', 'amber-2', 'coral-2', 'ochre-3'])} />;
		case 'soft':
			return <Soft seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} base={pick(['coral-3', 'coral-4', 'amber-4', 'bone-1'])} />;
		case 'branch':
			return <Branch seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} base={pick(['coral-3', 'coral-2'])} />;
		case 'tubes':
			return <Tubes seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} base={pick(['amber-3', 'ochre-3', 'coral-2'])} />;
		case 'ball':
			return <Ball seed={p.seed} x={p.x} y={p.y} r={p.size} lod={lod} base={pick(['amber-4', 'ochre-3', 'coral-3'])} />;
		case 'grass':
			return <Grass seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} />;
		case 'urchin':
			return <Urchin seed={p.seed} x={p.x} y={p.y} r={p.size} t={t} />;
		case 'star':
			return <Star seed={p.seed} x={p.x} y={p.y} s={p.size} base={pick(['coral-3', 'amber-4', 'ochre-3'])} />;
		case 'shell':
			return <Shell seed={p.seed} x={p.x} y={p.y} s={p.size} />;
		case 'anemone':
			return <Anemone x={p.x} y={p.y} s={p.size} t={t} seed={p.seed} color={pick(['bone-1', 'amber-4', 'coral-3'])} />;
		default:
			return null;
	}
};

export const OrcaOpenDetail: React.FC = () => {
	waitForFonts();
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const light = lightAt(t);
	const cam = camAt(t);
	const sunX = 540 + Math.cos(Math.atan2(light.key[1], light.key[0])) * 900;
	const o = orcaPose(t);
	const P = (a: readonly [number, number]) => orcaPt(t, a[0], a[1]);

	// ---------------------------------------------------------------- diver ("YOU" in the hook), v3 timing
	const flinch = springAt(t, 3.62, SETTLE);
	const away = ease.travel(prog(t, 4.2, 1.3));
	const dx = 930 - 10 * t - 60 * flinch - 640 * away;
	const dy = 1040 + 6 * Math.sin(1.4 * t) + 48 * flinch + 420 * away;
	const drot = -9 * flinch * (1 - away) + 12 * away;
	const reg: [number, number] = [dx - 514 * DS, dy + 118 * DS];
	const showDiver = t < 5.6;

	// ---------------------------------------------------------------- scale board (C)
	const [fx0, fy0] = P(A.flukeTip);
	const [fx1, fy1] = P(A.snout);
	const barY = o.oy + 905 * SB; // just under the near flipper tip
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
	const [footX, footY] = P(A.foot);
	const [finTipX, finTipY] = P(A.finTip);
	const [finMidX, finMidY] = P(A.finMid);
	const figS = (footY - finTipY) / 200; // the figure is exactly as tall as the fin (200 local units)
	const figPop = popIn(t, 7.95);
	const headY = footY - 200 * figS;
	const guideP = ease.travel(prog(t, 8.62, 0.5));

	// ---------------------------------------------------------------- lit/unlit pass (C, D)
	const unlitA = 0.4 * ease.drift(prog(t, 4.45, 0.7)) - 0.1 * ease.drift(prog(t, 7.8, 0.8));
	const body = P([760, 500]);
	const fd = ease.drift(prog(t, 7.8, 0.9));
	const holeC: [number, number] = t < 7.8 ? body : [lerp(body[0], (footX + finTipX) / 2, fd), lerp(body[1], (footY + finTipY) / 2, fd)];
	const [hx, hy] = toScreen(cam, holeC[0], holeC[1] + 60);
	const holeR = lerp(680, 460, fd);

	// bubble burst when the diver flinches (v3)
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
	const TY = !isOff('type');

	return (
		<LightProvider light={light}>
			<CameraProvider cam={cam}>
				<AbsoluteFill style={{backgroundColor: c('tide-1')}}>
					{/* P0 field */}
					<Plane preset="field">
						<GradientField
							id="sea"
							stops={[
								[0, 'tide-4'],
								[0.1, 'tide-3'],
								[0.3, OPEN_HI],
								[0.55, OPEN_LO],
								[0.8, 'tide-0'],
								[1, 'ink-4'],
							]}
							glow={{x: sunX, y: 60, r: 1100, color: 'tide-5', a: 0.34}}
						/>
						<SurfaceBand t={t} y={30} />
						{isOff('light') ? null : <LightLayer>
							<Caustics t={t} seed="surf" area={[-260, -200, 1600, 520]} cell={84} color="tide-5" alpha={0.14} width={3.4} />
							<Rays t={t} seed="sun" x={sunX} y={-40} n={8} angle={70} spread={50} len={2600} alpha={0.11} />
							<Emitter id="sun" x={sunX} y={-110} r={58} t={t} ramp={['bone-2', 'amber-5', 'amber-4']} halo="amber-5" haloScale={1.4} sparkles={6} />
						</LightLayer>}
					</Plane>

					{/* P0.5 distance: kelp columns to the surface, deep in the haze */}
					<Plane preset="far" spec={{depth: 0.2, haze: 0.86, desat: 0.08}}>
						{isOff('farkelp') ? null : FAR_KELP.map((k) => <VarKelp key={k.id} seed={k.seed} x={k.x} y={k.y} h={k.h} t={t} lean={k.lean} bend={k.bend} style={k.style} lod="far" blade={GIANT_KELP} />)}
						{/* no distant pod: at this size their silhouettes read as sharks (owner: no background sharks) */}
					</Plane>

					{/* P1 far: ridges, kelp columns to the surface, the distant pod, far herring, micro */}
					<Plane preset="far">
						{FAR_MOUNDS.map((m) => (
							<FarMound key={m.seed} {...m} />
						))}
						{isOff('far') ? null : FAR_REEF.map((p) => <Item key={p.id} p={p} t={t} lod="far" />)}
						{isOff('farfish') ? null : SCHOOLS_FAR.map((s) => <School key={s.id} spec={s} t={t} />)}
						{isOff('micro') ? null : <Micro t={t} seed="ofar" preset="far" n={45} />}
					</Plane>

					{/* P1.5 back: giant kelp groves at the frame edges (haze step 0.42) */}
					<Plane preset="mid" spec={{depth: 0.45, haze: 0.42, desat: 0.06}}>
						{isOff('backkelp') ? null : BACK_KELP.map((k) => <VarKelp key={k.id} seed={k.seed} x={k.x} y={k.y} h={k.h} t={t} lean={k.lean} bend={k.bend} style={k.style} blade={GIANT_KELP} />)}
					</Plane>

					{/* P2 mid: rocky reef + schools */}
					<Plane preset="mid" spec={{haze: 0.18, desat: 0}}>
						{isOff('seabed') ? null : <Seabed y={1530} t={t} seed="obed" deep={mixOk(c('ochre-1'), c('coral-0'), 0.35)} />}
						<LightLayer opacity={0.9}>
							<Caustics t={t} seed="sand" area={[-260, 1540, 1600, 560]} cell={58} color="amber-5" alpha={0.07} width={2.6} fadeDown={false} />
						</LightLayer>
						{isOff('midreef') ? null : MID_REEF.map((p) => <Item key={p.id} p={p} t={t} />)}
						{isOff('schools') ? null : SCHOOLS_MID.map((s) => <School key={s.id} spec={s} t={t} />)}
						{isOff('micro') ? null : <Micro t={t} seed="omid" preset="mid" n={45} />}
					</Plane>

					{/* lit/unlit pass (v3) */}
					<UnlitPass a={unlitA} x={hx} y={hy} rx={holeR * cam.zoom} ry={holeR * 0.7 * cam.zoom} color="ink-2" />
					{unlitA > 0.01 ? (
						<AbsoluteFill style={{mixBlendMode: 'screen', opacity: unlitA * 1.2, background: `radial-gradient(${(holeR * 0.8 * cam.zoom).toFixed(0)}px ${(holeR * 0.5 * cam.zoom).toFixed(0)}px at ${hx.toFixed(0)}px ${hy.toFixed(0)}px, ${rgba(c('amber-4'), 0.22)} 0%, ${rgba(c('tide-3'), 0.1)} 55%, ${rgba(c('tide-3'), 0)} 100%)`}} />
					) : null}

					{/* P3 subject */}
					<Plane preset="subject">
						{isOff('front') ? null : FRONT_REEF.map((p) => <Item key={p.id} p={p} t={t} />)}
						{isOff('singles') ? null : SINGLES.map((s) => <School key={s.id} spec={s} t={t} />)}
						{showDiver ? <Bubbles t={t} seed="reg" x={reg[0]} y={reg[1]} n={16} rate={3.6} rise={100} size={[3, 10]} /> : null}
						{isOff('orca') ? null : (
							<g transform={`translate(${o.ox.toFixed(1)} ${o.oy.toFixed(1)}) rotate(${o.pitch.toFixed(2)} ${(PIV[0] * SB).toFixed(1)} ${(PIV[1] * SB).toFixed(1)}) scale(${SB})`}>
								<OrcaHero id="orca" t={t} pitch={o.pitch} jaw={o.jaw} menace={o.menace} amp={o.amp} freq={o.freq} />
							</g>
						)}
						{showDiver ? (
							<g transform={`translate(${dx} ${dy}) rotate(${drot} ${-300 * DS} ${90 * DS}) scale(${DS})`}>
								<Diver id="diver" t={t} flip waveAt={2.3} />
							</g>
						) : null}
						{burst}
						{TY && youTagFade > 0 ? (
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
						{TY && <Counter t={t} at={5.05} dur={0.95} to={8} decimals={1} x={(fx0 + fx1) / 2} y={barY + 120} size={150} unit="m" out={6.3} />}

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
						{TY && <Counter t={t} at={6.98} dur={0.45} to={6} decimals={1} x={545} y={1306} size={120} prefix="≈" unit="tonnes" out={7.7} />}

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
									const x1 = finTipX + 60;
									return <line key={i} x1={x0} y1={y0} x2={x0 + (x1 - x0) * guideP} y2={y0 + (y1 - y0) * guideP} stroke={c('bone-2')} strokeWidth={4} strokeDasharray="12 10" />;
								})}
							</g>
						) : null}
						{TY && <LanternTag t={t} at={8.15} x={finTipX + 150} y={finTipY - 70} ax={finMidX + 8} ay={finMidY} text="FIN" sub="1.8 m" size={40} />}
						{TY && <LanternTag t={t} at={9.15} x={footX - 170} y={headY - 70} ax={footX} ay={headY + 30} text="YOU" ring="signal-1" size={40} />}

						{isOff('micro') ? null : <Micro t={t} seed="onear" preset="near" n={32} />}
					</Plane>

					{/* P4 foreground: kelp + boulder silhouettes cropped by the frame, bokeh */}
					<Plane preset="fore" spec={{blur: 6}}>
						{isOff('fore') ? null : FORE_KELP.map((k) => <VarKelp key={k.id} seed={k.seed} x={k.x} y={k.y} h={k.h} t={t} lean={k.lean} bend={k.bend} style="broad" silhouette />)}
						<Rock seed="ofgr" x={1010} y={2070} rx={300} ry={170} base="ink-1" lod="far" />
						<Soft seed="ofgs" x={60} y={2090} h={300} t={t} base="ink-1" lod="far" />
						<Bokeh t={t} seed="obk" n={10} r={[14, 40]} />
					</Plane>

					<AbsoluteFill style={{background: `radial-gradient(ellipse 85% 65% at 50% 46%, ${rgba(c('ink-0'), 0)} 60%, ${rgba(c('ink-0'), 0.42)} 100%)`}} />
				</AbsoluteFill>
			</CameraProvider>

			{/* screen-space type (v3); --props '{"off":["type"]}' drops it for the scenery-only D5 diagnostic */}
			{isOff('type') ? null : <>
			<TitlePlate
				t={t}
				at={-1}
				out={3.0}
				y={116}
				size={116}
				lines={[[{text: '0', color: 'signal-1'}, {text: ' HUMAN KILLS'}]]}
				sub={{text: 'IN THE WILD', color: 'tide-4'}}
				subSize={42}
				pulse={{at: 2.25, index: [0, 0]}}
			/>
			<Captions t={t} phrases={PHRASES} y={1350} size={62} />
			</>}
		</LightProvider>
	);
};
