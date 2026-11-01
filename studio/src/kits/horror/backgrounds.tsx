// Six apartment-horror backgrounds (plus the peephole view). Flat 2D, dark muted night palette.
// All are drawn on a 1080x1920 stage that crops ("slice") to any box, so they work as scene
// backgrounds ({"background": {"type": "component", "name": "horror/Hallway"}}) in 9:16 and 16:9.
import React from 'react';
import type {KitComponentProps} from '../../core/registry';
import {Neighbour} from './characters';
import {glitchAt, GlitchWrap} from './fx';
import {arr, clamp01, jitter, num, P, random, Stage, str, useUid} from './util';

const OL = P.line;

/** Brightness 0..1 of a flickering light at time t. */
function lightLevel(seed: string, t: number, flicker: number): number {
	if (flicker <= 0) return 1;
	const step = Math.floor(t * 14);
	const r = random(`${seed}-${step}`);
	const dip = r > 1 - 0.25 * flicker ? 0.15 + 0.4 * random(`${seed}-d-${step}`) : 1;
	return dip;
}

const knockLevel = (knocks: unknown, t: number) => {
	let k = 0;
	for (const at of arr<number>(knocks)) {
		const d = t - num(at, -9);
		if (d >= 0 && d < 0.18) k = Math.max(k, 1 - d / 0.18);
	}
	return k;
};

// ---------------------------------------------------------------- front door

/**
 * Apartment front door seen from inside.
 * props: knocks [t...] (door rattles + impact marks), chain ('on'|'off'), hallLight (0..1, light under the door),
 *        feet (bool or [from, to]: shadow of feet breaking the light strip), handle (deg, rattling lever: [{at, duration}] = jiggle cues),
 *        peepholeGlow (0..1), flicker
 */
export const FrontDoor: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const k = knockLevel(props.knocks, t);
	const dx = k ? jitter('door-k', t, 1 / 40) * 8 * k : 0;
	const hall = num(props.hallLight, 0.8) * lightLevel('door-hall', t, num(props.flicker, 0));
	const feetP = props.feet;
	const feet = Array.isArray(feetP) ? t >= num(feetP[0], 0) && t < num(feetP[1], 999) : Boolean(feetP);
	const jig = arr<{at?: number; duration?: number}>(props.handle).some((c) => t >= num(c.at, 0) && t < num(c.at, 0) + num(c.duration, 0.8));
	const handleRot = jig ? 18 + Math.sin(t * 40) * 14 : 0;
	const chain = str(props.chain, 'on') === 'on';
	const uid = useUid('door');
	return (
		<Stage width={width} height={height}>
			<defs>
				<linearGradient id={`${uid}w`} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#2c3443" />
					<stop offset="0.5" stopColor="#252c39" />
					<stop offset="1" stopColor="#1a1f29" />
				</linearGradient>
				<linearGradient id={`${uid}d`} x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor="#4d3d35" />
					<stop offset="1" stopColor="#33282396" />
				</linearGradient>
				<linearGradient id={`${uid}under`} x1="0" y1="1" x2="0" y2="0">
					<stop offset="0" stopColor="#e7b46a" stopOpacity={0.55 * hall} />
					<stop offset="1" stopColor="#e7b46a" stopOpacity={0} />
				</linearGradient>
			</defs>
			<rect width={1080} height={1920} fill={`url(#${uid}w)`} />
			{/* floor */}
			<rect y={1690} width={1080} height={230} fill="#1d1a1c" />
			{[1730, 1790, 1860].map((y) => (
				<line key={y} x1={0} x2={1080} y1={y} y2={y} stroke="#141214" strokeWidth={4} />
			))}
			<rect y={1660} width={1080} height={34} fill="#1a1e26" stroke={OL} strokeWidth={4} />
			{/* coat hook + coat */}
			<rect x={80} y={560} width={150} height={16} rx={6} fill="#4a4f59" stroke={OL} strokeWidth={4} />
			<path d="M 100 576 Q 70 760 90 1040 L 210 1040 Q 230 760 200 576 Z" fill="#2e3a37" stroke={OL} strokeWidth={6} />
			<path d="M 150 590 L 150 1030" stroke="#25302d" strokeWidth={6} />
			{/* light switch */}
			<rect x={905} y={960} width={70} height={110} rx={10} fill="#d6d1c4" stroke={OL} strokeWidth={4} opacity={0.75} />
			<rect x={928} y={990} width={24} height={46} rx={6} fill="#b9b3a5" />
			{/* frame */}
			<rect x={250} y={290} width={580} height={1390} fill="#3a404b" stroke={OL} strokeWidth={8} />
			<g transform={`translate(${dx} 0)`}>
				<rect x={290} y={330} width={500} height={1340} fill={`url(#${uid}d)`} stroke={OL} strokeWidth={7} />
				<rect x={340} y={400} width={400} height={480} fill="none" stroke="#2a211d" strokeWidth={10} opacity={0.75} />
				<rect x={340} y={960} width={400} height={620} fill="none" stroke="#2a211d" strokeWidth={10} opacity={0.75} />
				{/* peephole */}
				<circle cx={540} cy={760} r={24} fill="#b39257" stroke={OL} strokeWidth={5} />
				<circle cx={540} cy={760} r={11} fill={num(props.peepholeGlow, 0) > 0 ? `rgba(240,190,110,${0.4 + 0.6 * num(props.peepholeGlow, 0)})` : '#0b0b0e'} />
				{/* deadbolt + lever */}
				<circle cx={735} cy={900} r={26} fill="#a9a59c" stroke={OL} strokeWidth={5} />
				<rect x={727} y={880} width={16} height={40} rx={5} fill="#7f7b73" />
				<g transform={`rotate(${handleRot} 735 1010)`}>
					<circle cx={735} cy={1010} r={22} fill="#a9a59c" stroke={OL} strokeWidth={5} />
					<rect x={640} y={1000} width={100} height={22} rx={10} fill="#bdb9b0" stroke={OL} strokeWidth={5} />
				</g>
				{/* chain lock */}
				<rect x={690} y={800} width={60} height={22} rx={6} fill="#8d8a83" stroke={OL} strokeWidth={4} />
				{chain ? (
					<path d="M 720 812 Q 790 870 840 822" stroke="#b7b3aa" strokeWidth={9} fill="none" strokeDasharray="14 7" strokeLinecap="round" />
				) : (
					<path d="M 720 812 Q 724 880 716 950" stroke="#b7b3aa" strokeWidth={9} fill="none" strokeDasharray="14 7" strokeLinecap="round" />
				)}
				{k > 0 ? (
					<g stroke="#e8e2d4" strokeWidth={8} strokeLinecap="round" opacity={k}>
						<line x1={470} y1={1120} x2={410} y2={1080} />
						<line x1={460} y1={1160} x2={390} y2={1165} />
						<line x1={470} y1={1200} x2={410} y2={1240} />
						<line x1={610} y1={1120} x2={670} y2={1080} />
						<line x1={620} y1={1160} x2={690} y2={1165} />
						<line x1={610} y1={1200} x2={670} y2={1240} />
					</g>
				) : null}
			</g>
			{/* light leaking under the door from the hallway */}
			<rect x={290} y={1666} width={500} height={10} fill="#f1c37c" opacity={0.25 + 0.75 * hall} />
			<rect x={250} y={1676} width={580} height={150} fill={`url(#${uid}under)`} transform="scale(1 -1) translate(0 -3352)" />
			{feet ? (
				<g fill="#0b0b0e">
					<rect x={420} y={1664} width={80} height={14} />
					<rect x={560} y={1664} width={80} height={14} />
				</g>
			) : null}
			{/* doormat */}
			<path d="M 330 1760 L 750 1760 L 790 1860 L 290 1860 Z" fill="#3a2f2b" stroke={OL} strokeWidth={5} />
			{/* moonlight wash from the left */}
			<polygon points="0,300 260,420 260,1680 0,1900" fill="#9fb6cf" opacity={0.05} />
		</Stage>
	);
};

// ---------------------------------------------------------------- hallway (shared drawing)

type HallOpts = {t: number; flicker: number; lights: number; endDoor: boolean; runner: string; figure: number; figureDepth: number; seed: string};

const HallArt: React.FC<HallOpts & {uid: string}> = ({t, flicker, lights, endDoor, runner, figure, figureDepth, seed, uid}) => {
	const VX0 = 420;
	const VX1 = 660;
	const VY0 = 700;
	const VY1 = 1010;
	const at = (d: number) => ({
		xl: VX0 * d,
		xr: 1080 - (1080 - VX1) * d,
		yc: VY0 * d,
		yf: 1920 - (1920 - VY1) * d,
	});
	const doorD: [number, number][] = [
		[0.08, 0.3],
		[0.48, 0.62],
		[0.74, 0.82],
	];
	const lightDs = [0.22, 0.55, 0.78].slice(0, lights);
	const levels = lightDs.map((_, i) => lightLevel(`${seed}-l${i}`, t, i === 1 ? flicker : flicker * 0.4));
	const avg = levels.reduce((a, b) => a + b, 0) / Math.max(1, levels.length);
	return (
		<g>
			<defs>
				<linearGradient id={`${uid}fl`} x1="0" y1="1" x2="0" y2="0">
					<stop offset="0" stopColor="#262226" />
					<stop offset="1" stopColor="#141215" />
				</linearGradient>
				<linearGradient id={`${uid}wl`} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#3a4251" />
					<stop offset="1" stopColor="#1c212b" />
				</linearGradient>
				<linearGradient id={`${uid}wr`} x1="1" y1="0" x2="0" y2="0">
					<stop offset="0" stopColor="#343c4a" />
					<stop offset="1" stopColor="#1a1f28" />
				</linearGradient>
			</defs>
			<rect width={1080} height={1920} fill="#101318" />
			<polygon points={`0,0 1080,0 ${VX1},${VY0} ${VX0},${VY0}`} fill="#1b1f27" />
			<polygon points={`0,0 ${VX0},${VY0} ${VX0},${VY1} 0,1920`} fill={`url(#${uid}wl)`} />
			<polygon points={`1080,0 ${VX1},${VY0} ${VX1},${VY1} 1080,1920`} fill={`url(#${uid}wr)`} />
			<polygon points={`0,1920 1080,1920 ${VX1},${VY1} ${VX0},${VY1}`} fill={`url(#${uid}fl)`} />
			{/* runner carpet */}
			<polygon points={`300,1920 780,1920 ${VX1 - 70},${VY1} ${VX0 + 70},${VY1}`} fill={runner} opacity={0.85} />
			{/* end wall */}
			<rect x={VX0} y={VY0} width={VX1 - VX0} height={VY1 - VY0} fill="#0c0e12" stroke={OL} strokeWidth={4} />
			{endDoor ? <rect x={VX0 + 70} y={VY0 + 90} width={100} height={VY1 - VY0 - 90} fill="#1c1716" stroke="#2c2522" strokeWidth={4} /> : null}
			{/* baseboards */}
			<line x1={0} y1={1920} x2={VX0} y2={VY1} stroke="#0d0f13" strokeWidth={10} />
			<line x1={1080} y1={1920} x2={VX1} y2={VY1} stroke="#0d0f13" strokeWidth={10} />
			{/* side doors */}
			{doorD.map(([d0, d1], i) =>
				[0, 1].map((side) => {
					const a = at(d0);
					const b = at(d1);
					const ha = a.yf - a.yc;
					const hb = b.yf - b.yc;
					const x0 = side ? a.xr : a.xl;
					const x1 = side ? b.xr : b.xl;
					const pts = `${x0},${a.yc + ha * 0.28} ${x1},${b.yc + hb * 0.28} ${x1},${b.yf} ${x0},${a.yf}`;
					const plateX = x0 + (x1 - x0) * 0.5;
					const plateY = a.yc + ha * 0.4 + (b.yc + hb * 0.4 - (a.yc + ha * 0.4)) * 0.5;
					return (
						<g key={`${i}-${side}`}>
							<polygon points={pts} fill="#3b2f2a" stroke={OL} strokeWidth={Math.max(2, 6 * (1 - d0))} />
							<circle cx={x0 + (x1 - x0) * (side ? 0.2 : 0.8)} cy={a.yc + ha * 0.62} r={Math.max(3, 12 * (1 - d0))} fill="#a9a59c" />
							<rect x={plateX - 26 * (1 - d0)} y={plateY - 12 * (1 - d0)} width={52 * (1 - d0)} height={24 * (1 - d0)} fill="#b8ad93" opacity={0.6} />
						</g>
					);
				}),
			)}
			{/* ceiling lights + floor pools */}
			{lightDs.map((d, i) => {
				const a = at(d);
				const w = (a.xr - a.xl) * 0.28;
				const cx = (a.xl + a.xr) / 2;
				const L = levels[i];
				return (
					<g key={i}>
						<ellipse cx={cx} cy={a.yf - (a.yf - a.yc) * 0.02} rx={w * 1.4} ry={w * 0.32} fill="#e8d9a8" opacity={0.12 * L} />
						<rect x={cx - w / 2} y={a.yc + 6} width={w} height={Math.max(6, 22 * (1 - d))} rx={6} fill={L > 0.6 ? '#f3e7c0' : '#4a4a44'} />
						<polygon points={`${cx - w / 2},${a.yc + 20} ${cx + w / 2},${a.yc + 20} ${cx + w * 1.6},${a.yf} ${cx - w * 1.6},${a.yf}`} fill="#f3e7c0" opacity={0.05 * L} />
					</g>
				);
			})}
			{figure > 0
				? (() => {
						const a = at(figureDepth);
						const h = (a.yf - a.yc) * 0.62;
						const cx = (a.xl + a.xr) / 2 + 30 * (1 - figureDepth);
						const w = h * 0.28;
						return (
							<g opacity={figure}>
								<ellipse cx={cx} cy={a.yf - h * 0.86} rx={w * 0.36} ry={w * 0.46} fill="#07080a" />
								<path d={`M ${cx - w / 2} ${a.yf} L ${cx - w * 0.55} ${a.yf - h * 0.62} Q ${cx} ${a.yf - h * 0.8} ${cx + w * 0.55} ${a.yf - h * 0.62} L ${cx + w / 2} ${a.yf} Z`} fill="#07080a" />
								<circle cx={cx - w * 0.12} cy={a.yf - h * 0.87} r={Math.max(1.5, w * 0.04)} fill="#e9e6da" />
								<circle cx={cx + w * 0.12} cy={a.yf - h * 0.87} r={Math.max(1.5, w * 0.04)} fill="#e9e6da" />
							</g>
						);
					})()
				: null}
			{/* overall exposure follows the lights */}
			<rect width={1080} height={1920} fill="#000" opacity={0.45 * (1 - avg)} />
		</g>
	);
};

/**
 * Apartment corridor in one-point perspective with flickering ceiling lights.
 * props: flicker (0..1, 0.4), lights (1-3), endDoor (true), runner (carpet colour),
 *        figure (0..1 opacity of a silhouette with eye glints), figureDepth (0..1, 0.8 = far)
 */
export const Hallway: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const uid = useUid('hall');
	return (
		<GlitchWrap amount={glitchAt(props, t)} t={t} seed="hall">
			<Stage width={width} height={height}>
				<HallArt
					uid={uid}
					t={t}
					flicker={num(props.flicker, 0.4)}
					lights={num(props.lights, 3)}
					endDoor={props.endDoor !== false}
					runner={str(props.runner, '#3a2228')}
					figure={num(props.figure, 0)}
					figureDepth={num(props.figureDepth, 0.8)}
					seed="hall"
				/>
			</Stage>
		</GlitchWrap>
	);
};

// ---------------------------------------------------------------- peephole

/**
 * View through the door peephole: fisheye circle of the hallway with a visitor.
 * props: figure ('neighbour' | 'silhouette' | 'none'), expr / exprs (neighbour face), talk, lookX, lookY,
 *        lean (0..1 how close the visitor presses to the lens, 0.4), flicker (0.3), radius (fraction, 0.46)
 */
export const Peephole: React.FC<KitComponentProps> = ({props, time: t, width, height, fps, frame, sceneDuration}) => {
	const uid = useUid('peep');
	const r = Math.min(width, height * 0.6) * num(props.radius, 0.46);
	const cx = width / 2;
	const cy = height * 0.47;
	const figure = str(props.figure, 'neighbour');
	const lean = num(props.lean, 0.4);
	const fl = lightLevel('peep', t, num(props.flicker, 0.3));
	const breathe = 1 + Math.sin(t * 1.4) * 0.01;
	const fw = r * (1.25 + lean * 0.9) * breathe;
	const fh = fw * (760 / 500);
	return (
		<div style={{width, height, position: 'relative', background: '#050506', overflow: 'hidden'}}>
			<div
				style={{
					position: 'absolute',
					left: cx - r,
					top: cy - r,
					width: r * 2,
					height: r * 2,
					borderRadius: '50%',
					overflow: 'hidden',
					filter: `brightness(${0.55 + 0.45 * fl}) saturate(0.8) blur(0.6px)`,
				}}
			>
				<svg width={r * 2} height={r * 2} viewBox="190 330 700 700" preserveAspectRatio="xMidYMid slice" style={{position: 'absolute', inset: 0, transform: 'scale(1.18)'}}>
					<HallArt uid={uid} t={t} flicker={0} lights={2} endDoor runner="#3a2228" figure={figure === 'silhouette' ? 1 : 0} figureDepth={0.55} seed="peep" />
				</svg>
				{figure === 'neighbour' ? (
					<div style={{position: 'absolute', left: r - fw / 2, top: r * (1.15 - lean * 0.35) - fh * 0.42, width: fw, height: fh}}>
						<Neighbour props={{...props, glitch: undefined}} time={t} frame={frame} fps={fps} width={fw} height={fh} sceneDuration={sceneDuration} />
					</div>
				) : null}
				{/* fisheye falloff + warm hallway light */}
				<div style={{position: 'absolute', inset: 0, background: 'radial-gradient(circle at 50% 42%, rgba(240,200,140,0.12) 0%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 78%, rgba(0,0,0,0.98) 100%)'}} />
				<div style={{position: 'absolute', left: r * 0.35, top: r * 0.22, width: r * 0.5, height: r * 0.24, borderRadius: '50%', background: 'rgba(255,255,255,0.08)', transform: 'rotate(-25deg)'}} />
			</div>
			{/* lens rim */}
			<div style={{position: 'absolute', left: cx - r - 14, top: cy - r - 14, width: (r + 14) * 2, height: (r + 14) * 2, borderRadius: '50%', boxShadow: '0 0 0 18px #0c0b0d, 0 0 60px 30px rgba(0,0,0,0.9) inset'}} />
		</div>
	);
};

// ---------------------------------------------------------------- elevator panel

/**
 * Elevator button panel with a floor display that counts.
 * props: from (1), to (7), at (0.3), perFloor (0.45 s), floors (12), target (lit button, default `to`),
 *        pressed [{at, floor}] extra button lights, flicker (0)
 */
export const ElevatorPanel: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const from = num(props.from, 1);
	const to = num(props.to, 7);
	const at = num(props.at, 0.3);
	const per = num(props.perFloor, 0.45);
	const n = Math.max(1, Math.abs(to - from));
	const steps = clamp01((t - at) / (n * per)) * n;
	const dir = Math.sign(to - from) || 1;
	const floor = Math.round(from + dir * Math.floor(steps));
	const moving = t >= at && steps < n;
	const arrived = steps >= n;
	const sinceArrive = t - (at + n * per);
	const floors = num(props.floors, 12);
	const target = num(props.target, to);
	const lit = new Set<number>([target]);
	for (const p of arr<{at?: number; floor?: number}>(props.pressed)) if (t >= num(p.at, 0)) lit.add(num(p.floor, 1));
	if (arrived && sinceArrive > 0.4) lit.delete(target);
	const fl = lightLevel('elev', t, num(props.flicker, 0));
	const arrowOn = moving ? Math.floor(t * 4) % 2 === 0 : arrived && sinceArrive < 0.6;
	const ding = arrived && sinceArrive < 0.25 ? 1 - sinceArrive / 0.25 : 0;
	const uid = useUid('elev');
	const rows = Math.ceil(floors / 2);
	return (
		<Stage width={width} height={height}>
			<defs>
				<linearGradient id={`${uid}m`} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#4c535c" />
					<stop offset="0.45" stopColor="#7a828c" />
					<stop offset="1" stopColor="#4a5058" />
				</linearGradient>
				<pattern id={`${uid}br`} width={6} height={1920} patternUnits="userSpaceOnUse">
					<rect width={6} height={1920} fill="transparent" />
					<line x1={2} y1={0} x2={2} y2={1920} stroke="#ffffff" strokeOpacity={0.05} strokeWidth={1} />
				</pattern>
			</defs>
			<rect width={1080} height={1920} fill="#2a2e34" />
			<rect x={0} y={0} width={170} height={1920} fill="#1f2227" />
			<rect x={910} y={0} width={170} height={1920} fill="#23262b" />
			{/* panel */}
			<rect x={200} y={180} width={680} height={1560} rx={18} fill={`url(#${uid}m)`} stroke={OL} strokeWidth={8} />
			<rect x={200} y={180} width={680} height={1560} rx={18} fill={`url(#${uid}br)`} />
			{/* display */}
			<rect x={300} y={260} width={480} height={250} rx={14} fill="#0b0909" stroke="#2c2f35" strokeWidth={8} />
			{(() => {
				const digits = String(Math.abs(floor)).padStart(2, ' ').slice(-2).split('');
				return [0, 1].map((i) => (
					<g key={i}>
						<text x={575 + i * 125} y={455} textAnchor="middle" fontFamily="Anton, Impact, sans-serif" fontSize={210} fill="#1e0709">
							8
						</text>
						{digits[i] !== ' ' ? (
							<text x={575 + i * 125} y={455} textAnchor="middle" fontFamily="Anton, Impact, sans-serif" fontSize={210} fill="#ff3b30" style={{filter: 'drop-shadow(0 0 14px rgba(255,50,40,0.8))'}}>
								{digits[i]}
							</text>
						) : null}
					</g>
				));
			})()}
			<path
				d={dir > 0 ? 'M 390 310 L 445 400 L 335 400 Z' : 'M 390 460 L 445 370 L 335 370 Z'}
				fill={arrowOn ? '#ff3b30' : '#3a0d10'}
				style={arrowOn ? {filter: 'drop-shadow(0 0 10px rgba(255,50,40,0.8))'} : undefined}
			/>
			{/* buttons */}
			{Array.from({length: floors}, (_, i) => {
				const f = i + 1;
				const col = i % 2;
				const row = rows - 1 - Math.floor(i / 2);
				const x = 420 + col * 240;
				const y = 640 + row * 132;
				const on = lit.has(f);
				return (
					<g key={f}>
						<circle cx={x} cy={y} r={50} fill="#9aa1aa" stroke={OL} strokeWidth={5} />
						<circle cx={x} cy={y} r={40} fill={on ? '#ffb35c' : '#c9ced4'} stroke={on ? '#ff8a1e' : '#7c838c'} strokeWidth={6} style={on ? {filter: 'drop-shadow(0 0 16px rgba(255,150,40,0.9))'} : undefined} />
						<text x={x} y={y + 16} textAnchor="middle" fontFamily="Montserrat, sans-serif" fontWeight={900} fontSize={42} fill={on ? '#5a2a00' : '#3c4148'}>
							{f}
						</text>
						<g fill="#3c4148" opacity={0.7}>
							<circle cx={x - 92} cy={y - 10} r={4} />
							<circle cx={x - 92} cy={y + 4} r={4} />
							<circle cx={x - 80} cy={y - 10} r={4} />
						</g>
					</g>
				);
			})}
			{/* open / close / alarm */}
			{[
				['◀▶', 360],
				['▶◀', 540],
				['!', 720],
			].map(([s, x]) => (
				<g key={String(x)}>
					<circle cx={Number(x)} cy={1560} r={52} fill="#9aa1aa" stroke={OL} strokeWidth={5} />
					<circle cx={Number(x)} cy={1560} r={42} fill={s === '!' ? '#d0a23a' : '#c9ced4'} />
					<text x={Number(x)} y={1574} textAnchor="middle" fontFamily="Montserrat, sans-serif" fontWeight={900} fontSize={34} fill="#3c4148">
						{s}
					</text>
				</g>
			))}
			{/* handrail */}
			<rect x={0} y={1790} width={1080} height={40} rx={20} fill="#8a929c" stroke={OL} strokeWidth={6} />
			{ding > 0 ? <rect width={1080} height={1920} fill="#fff1d6" opacity={0.18 * ding} /> : null}
			<rect width={1080} height={1920} fill="#000" opacity={0.55 * (1 - fl)} />
		</Stage>
	);
};

// ---------------------------------------------------------------- bedroom at night

/**
 * Bedroom at night: moonlit window, bed, nightstand lamp, wardrobe.
 * props: lamp (0..1, 0 = off), wardrobeOpen (0..1, dark gap), rain (bool), phoneGlow (0..1 on the nightstand),
 *        flicker (lamp flicker)
 */
export const Bedroom: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const uid = useUid('bed');
	const lamp = num(props.lamp, 0) * lightLevel('bedlamp', t, num(props.flicker, 0));
	const wo = clamp01(num(props.wardrobeOpen, 0.15));
	const glow = num(props.phoneGlow, 0);
	return (
		<Stage width={width} height={height}>
			<defs>
				<linearGradient id={`${uid}w`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#1a2130" />
					<stop offset="1" stopColor="#141924" />
				</linearGradient>
				<linearGradient id={`${uid}sky`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#24364f" />
					<stop offset="1" stopColor="#3e5874" />
				</linearGradient>
				<radialGradient id={`${uid}lamp`} cx="0.5" cy="0.5" r="0.5">
					<stop offset="0" stopColor="#f0c27a" stopOpacity={0.5 * lamp} />
					<stop offset="1" stopColor="#f0c27a" stopOpacity={0} />
				</radialGradient>
			</defs>
			<rect width={1080} height={1920} fill={`url(#${uid}w)`} />
			<rect y={1500} width={1080} height={420} fill="#17141a" />
			{/* window */}
			<rect x={140} y={300} width={420} height={600} fill={`url(#${uid}sky)`} stroke={OL} strokeWidth={10} />
			<circle cx={440} cy={420} r={58} fill="#d7e2ec" opacity={0.9} />
			<circle cx={418} cy={408} r={50} fill="#2e4560" opacity={0.25} />
			<path d="M 140 800 L 220 720 L 280 760 L 360 680 L 440 740 L 560 690 L 560 900 L 140 900 Z" fill="#141c29" />
			{[0, 1, 2, 3, 4, 5].map((i) => (
				<rect key={i} x={170 + i * 62} y={760 + (i % 3) * 30} width={14} height={18} fill={i === 3 ? '#e6c27a' : '#2a3549'} />
			))}
			<line x1={350} y1={300} x2={350} y2={900} stroke={OL} strokeWidth={10} />
			<line x1={140} y1={600} x2={560} y2={600} stroke={OL} strokeWidth={10} />
			{props.rain
				? Array.from({length: 26}, (_, i) => {
						const x = 150 + random(`rx${i}`) * 400;
						const y = 300 + (((random(`ry${i}`) * 600 + t * 700) % 600) + 600) % 600;
						return <line key={i} x1={x} y1={y} x2={x - 6} y2={y + 30} stroke="#9fb6cf" strokeWidth={3} opacity={0.5} />;
					})
				: null}
			{/* curtains */}
			<path d="M 100 270 Q 140 600 110 940 L 190 940 Q 170 600 200 270 Z" fill="#2f2a3d" stroke={OL} strokeWidth={6} />
			<path d="M 600 270 Q 560 600 590 940 L 510 940 Q 530 600 500 270 Z" fill="#2f2a3d" stroke={OL} strokeWidth={6} />
			<rect x={80} y={252} width={540} height={22} rx={10} fill="#3b3f4a" stroke={OL} strokeWidth={5} />
			{/* moonlight beam on the floor / bed */}
			<polygon points="140,900 560,900 900,1700 300,1700" fill="#9fb6cf" opacity={0.07} />
			{/* wardrobe */}
			<rect x={760} y={320} width={300} height={1200} fill="#2a2326" stroke={OL} strokeWidth={8} />
			<rect x={760} y={320} width={150} height={1200} fill="#30282b" stroke={OL} strokeWidth={6} />
			<rect x={910} y={320} width={150 * (1 - wo)} height={1200} fill="#30282b" stroke={OL} strokeWidth={6} />
			{wo > 0 ? <rect x={910 + 150 * (1 - wo)} y={326} width={150 * wo} height={1188} fill="#050506" /> : null}
			<circle cx={892} cy={920} r={10} fill="#8b8379" />
			{/* nightstand + lamp */}
			<rect x={60} y={1180} width={200} height={260} fill="#3a2e2a" stroke={OL} strokeWidth={6} />
			<rect x={80} y={1240} width={160} height={70} fill="#33282396" stroke={OL} strokeWidth={4} />
			<circle cx={160} cy={1275} r={8} fill="#8b8379" />
			<path d="M 110 1180 L 210 1180 L 190 1090 L 130 1090 Z" fill={lamp > 0.1 ? '#f2d9a4' : '#5b5348'} stroke={OL} strokeWidth={5} />
			<rect x={152} y={1080} width={16} height={100} fill="#4a4540" />
			<circle cx={160} cy={1140} r={260} fill={`url(#${uid}lamp)`} />
			{glow > 0 ? (
				<g>
					<rect x={190} y={1166} width={50} height={14} rx={3} fill="#1a1b20" />
					<ellipse cx={215} cy={1150} rx={90} ry={60} fill="#a9c6ff" opacity={0.25 * glow} />
				</g>
			) : null}
			{/* bed */}
			<rect x={240} y={1150} width={60} height={420} rx={10} fill="#3a2e2a" stroke={OL} strokeWidth={6} />
			<path d="M 280 1260 L 1080 1260 L 1080 1580 L 280 1580 Z" fill="#2c3346" stroke={OL} strokeWidth={6} />
			<ellipse cx={400} cy={1260} rx={110} ry={46} fill="#cfd3dc" stroke={OL} strokeWidth={6} opacity={0.85} />
			<path d="M 470 1240 Q 640 1200 1080 1250 L 1080 1460 Q 700 1500 470 1430 Q 430 1340 470 1240 Z" fill="#3c4a6b" stroke={OL} strokeWidth={6} />
			<path d="M 560 1290 Q 760 1270 980 1300 M 540 1370 Q 760 1360 1060 1390" stroke="#2f3a55" strokeWidth={6} fill="none" />
			<rect x={240} y={1560} width={840} height={30} fill="#3a2e2a" stroke={OL} strokeWidth={5} />
		</Stage>
	);
};

// ---------------------------------------------------------------- living room

/**
 * Living room at night: sofa, coffee table, switched-off TV, floor lamp, blinds.
 * props: lamp (0..1), tv ('off' | 'static' | 'glow'), flicker
 */
export const LivingRoom: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const uid = useUid('liv');
	const lamp = num(props.lamp, 0.6) * lightLevel('livlamp', t, num(props.flicker, 0));
	const tv = str(props.tv, 'off');
	return (
		<Stage width={width} height={height}>
			<defs>
				<radialGradient id={`${uid}lamp`} cx="0.5" cy="0.5" r="0.5">
					<stop offset="0" stopColor="#efbd72" stopOpacity={0.45 * lamp} />
					<stop offset="1" stopColor="#efbd72" stopOpacity={0} />
				</radialGradient>
				<filter id={`${uid}noise`}>
					<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={1} seed={Math.floor(t * 20)} />
					<feColorMatrix type="saturate" values="0" />
				</filter>
			</defs>
			<rect width={1080} height={1920} fill="#232733" />
			<rect width={1080} height={700} fill="#1e222c" />
			<rect y={1460} width={1080} height={460} fill="#1c1a1d" />
			<line x1={0} y1={1460} x2={1080} y2={1460} stroke={OL} strokeWidth={8} />
			{/* window with blinds */}
			<rect x={120} y={360} width={360} height={520} fill="#30455e" stroke={OL} strokeWidth={10} />
			{Array.from({length: 13}, (_, i) => (
				<rect key={i} x={120} y={370 + i * 39} width={360} height={24} fill="#283041" />
			))}
			<polygon points="120,880 480,880 640,1460 120,1460" fill="#9fb6cf" opacity={0.05} />
			{/* picture frame */}
			<rect x={580} y={420} width={200} height={260} fill="#3a2e2a" stroke={OL} strokeWidth={8} />
			<rect x={604} y={444} width={152} height={212} fill="#4e5a6a" />
			<circle cx={680} cy={530} r={38} fill="#2a3240" />
			{/* TV on a low cabinet (right) */}
			<rect x={760} y={1080} width={300} height={180} fill="#2a2326" stroke={OL} strokeWidth={6} />
			<rect x={740} y={760} width={340} height={300} rx={10} fill="#0d0e11" stroke={OL} strokeWidth={8} />
			{tv === 'static' ? <rect x={756} y={776} width={308} height={268} filter={`url(#${uid}noise)`} opacity={0.75} /> : null}
			{tv === 'glow' ? <rect x={756} y={776} width={308} height={268} fill="#6f8fb8" opacity={0.5} /> : null}
			{tv === 'off' ? <path d="M 770 790 L 860 790 L 790 900 Z" fill="#ffffff" opacity={0.05} /> : null}
			{/* floor lamp */}
			<rect x={92} y={1000} width={12} height={460} fill="#4a4540" />
			<path d="M 50 1000 L 150 1000 L 130 900 L 70 900 Z" fill={lamp > 0.1 ? '#f2d9a4' : '#5b5348'} stroke={OL} strokeWidth={5} />
			<ellipse cx={98} cy={1462} rx={60} ry={12} fill="#2a2628" />
			<circle cx={100} cy={950} r={420} fill={`url(#${uid}lamp)`} />
			{/* sofa */}
			<rect x={170} y={1120} width={560} height={200} rx={40} fill="#4a3b45" stroke={OL} strokeWidth={8} />
			<rect x={140} y={1240} width={620} height={200} rx={36} fill="#55444f" stroke={OL} strokeWidth={8} />
			<rect x={120} y={1200} width={90} height={260} rx={40} fill="#4a3b45" stroke={OL} strokeWidth={8} />
			<rect x={690} y={1200} width={90} height={260} rx={40} fill="#4a3b45" stroke={OL} strokeWidth={8} />
			<line x1={450} y1={1250} x2={450} y2={1420} stroke="#3d313a" strokeWidth={6} />
			<rect x={240} y={1160} width={130} height={110} rx={24} fill="#6a5a4a" stroke={OL} strokeWidth={6} transform="rotate(-8 300 1215)" />
			{/* rug + coffee table */}
			<ellipse cx={460} cy={1700} rx={460} ry={110} fill="#2d2530" />
			<rect x={240} y={1560} width={460} height={40} rx={10} fill="#4d3d34" stroke={OL} strokeWidth={6} />
			<rect x={270} y={1600} width={20} height={120} fill="#3b2f2a" />
			<rect x={650} y={1600} width={20} height={120} fill="#3b2f2a" />
			<rect x={420} y={1530} width={70} height={34} rx={6} fill="#cfd3dc" opacity={0.8} />
			{/* plant */}
			<path d="M 980 1460 L 1000 1340 L 1060 1340 L 1080 1460 Z" fill="#3a2e2a" stroke={OL} strokeWidth={5} />
			{[-30, 0, 30].map((a) => (
				<ellipse key={a} cx={1030} cy={1280} rx={22} ry={70} fill="#2f4536" stroke={OL} strokeWidth={4} transform={`rotate(${a} 1030 1340)`} />
			))}
		</Stage>
	);
};

// ---------------------------------------------------------------- stairwell

/**
 * Concrete fire stairwell: zig-zag flights, railing, painted floor number, EXIT sign, buzzing tube light.
 * props: floor ('7'), flicker (0.5), exit (true)
 */
export const Stairwell: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const uid = useUid('stair');
	const L = lightLevel('stair', t, num(props.flicker, 0.5));
	const steps = 9;
	return (
		<Stage width={width} height={height}>
			<defs>
				<linearGradient id={`${uid}w`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#2f3833" />
					<stop offset="1" stopColor="#1e2421" />
				</linearGradient>
				<radialGradient id={`${uid}ex`} cx="0.5" cy="0.5" r="0.5">
					<stop offset="0" stopColor="#46d17a" stopOpacity={0.35} />
					<stop offset="1" stopColor="#46d17a" stopOpacity={0} />
				</radialGradient>
			</defs>
			<rect width={1080} height={1920} fill={`url(#${uid}w)`} />
			{/* painted stripe + floor number */}
			<rect y={1000} width={1080} height={50} fill="#5a6b52" opacity={0.6} />
			<text x={820} y={880} textAnchor="middle" fontFamily="Anton, Impact, sans-serif" fontSize={300} fill="#c9c2a8" opacity={0.5}>
				{str(props.floor, '7')}
			</text>
			<text x={820} y={960} textAnchor="middle" fontFamily="Montserrat, sans-serif" fontWeight={900} fontSize={60} fill="#c9c2a8" opacity={0.45}>
				FLOOR
			</text>
			{/* fire door + exit sign */}
			<rect x={90} y={520} width={330} height={640} fill="#4a3f36" stroke={OL} strokeWidth={8} />
			<rect x={130} y={580} width={90} height={160} fill="#1b1f1d" stroke={OL} strokeWidth={5} />
			<rect x={120} y={860} width={270} height={26} rx={10} fill="#8a8a80" stroke={OL} strokeWidth={4} />
			{props.exit !== false ? (
				<g>
					<circle cx={255} cy={440} r={160} fill={`url(#${uid}ex)`} />
					<rect x={170} y={400} width={170} height={80} rx={8} fill="#0f1a12" stroke={OL} strokeWidth={5} />
					<text x={255} y={458} textAnchor="middle" fontFamily="Montserrat, sans-serif" fontWeight={900} fontSize={46} fill="#5af08f" style={{filter: 'drop-shadow(0 0 8px rgba(70,209,122,0.9))'}}>
						EXIT
					</text>
				</g>
			) : null}
			{/* landing */}
			<polygon points="0,1180 1080,1180 1080,1920 0,1920" fill="#3b3f3c" />
			{/* flight going up to the right */}
			{Array.from({length: steps}, (_, i) => {
				const x = 470 + i * 64;
				const y = 1180 - i * 60;
				return (
					<g key={i}>
						<rect x={x} y={y - 60} width={1080 - x} height={60} fill={i % 2 ? '#4a4f4b' : '#555a56'} stroke={OL} strokeWidth={4} />
						<rect x={x} y={y - 60} width={1080 - x} height={10} fill="#6a706b" />
					</g>
				);
			})}
			{/* flight going down (foreground) */}
			{Array.from({length: 6}, (_, i) => {
				const y = 1420 + i * 90;
				return <rect key={`d${i}`} x={0} y={y} width={700 - i * 70} height={90} fill={i % 2 ? '#2e322f' : '#343935'} stroke={OL} strokeWidth={4} />;
			})}
			<rect x={0} y={1180} width={1080} height={240} fill="#424743" stroke={OL} strokeWidth={4} />
			{/* railings */}
			<line x1={470} y1={960} x2={1080} y2={420} stroke="#9a8a5a" strokeWidth={16} strokeLinecap="round" />
			{Array.from({length: 6}, (_, i) => {
				const x = 500 + i * 110;
				const y = 960 - (i * 110 * 540) / 610;
				return <line key={i} x1={x} y1={y} x2={x} y2={y + 220} stroke="#7d7050" strokeWidth={10} />;
			})}
			<line x1={0} y1={1300} x2={720} y2={1300} stroke="#9a8a5a" strokeWidth={16} />
			{[80, 260, 440, 620].map((x) => (
				<line key={x} x1={x} y1={1300} x2={x} y2={1420} stroke="#7d7050" strokeWidth={10} />
			))}
			{/* tube light */}
			<rect x={420} y={120} width={420} height={36} rx={18} fill={L > 0.6 ? '#eef3e0' : '#56594f'} stroke={OL} strokeWidth={5} />
			<polygon points="420,156 840,156 1080,1100 120,1100" fill="#eef3e0" opacity={0.06 * L} />
			<rect width={1080} height={1920} fill="#000" opacity={0.5 * (1 - L)} />
		</Stage>
	);
};

