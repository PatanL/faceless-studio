import React from 'react';
import {E, blinking, camAt, camT, clamp, kf} from '../lib/anim';
import {Gun} from '../art/guns';
import {ik} from '../art/soldier';
import {P} from '../art/defs';

// Scene block 4 (21.97-26.33): a generic, unnamed official at a heavy desk with the AK-12 (S13).

const Panel: React.FC<{x: number; w: number; top: number; c: string}> = ({x, w, top, c}) => (
	<g>
		<path d={`M${x},1200 L${x},${top + w / 2} Q${x},${top} ${x + w / 2},${top} Q${x + w},${top} ${x + w},${top + w / 2} L${x + w},1200 Z`} fill={c} />
		<path d={`M${x + w - 18},1200 L${x + w - 18},${top + w / 2} Q${x + w - 20},${top + 20} ${x + w / 2},${top + 4} Q${x + w},${top + 8} ${x + w},${top + w / 2} L${x + w},1200 Z`} fill="#000" opacity={0.12} />
		<rect x={x + 16} y={top + w / 2} width={10} height={1200 - top - w / 2} fill="#FFFFFF" opacity={0.06} />
	</g>
);

const Emblem: React.FC = () => (
	<g transform="translate(540 52)">
		<ellipse cx={0} cy={-30} rx={210} ry={140} fill="#3D1D10" />
		{/* generic gold crest: wings + shield (not a real coat of arms) */}
		{[-1, 1].map((s) => (
			<g key={s} transform={`scale(${s} 1)`}>
				<path d="M10,-10 Q60,-60 120,-40 Q90,-30 100,-10 Q70,-14 76,10 Q46,0 30,20 Z" fill="#F2B32A" />
				<path d="M10,-10 Q60,-60 120,-40 Q90,-34 70,-30 Q40,-30 10,-10 Z" fill="#FFD66B" />
				<circle cx={22} cy={-44} r={12} fill="#F2B32A" />
			</g>
		))}
		<path d="M-26,-20 L26,-20 L26,14 Q26,40 0,50 Q-26,40 -26,14 Z" fill="#D9921A" />
		<path d="M-16,-12 L16,-12 L16,12 Q16,28 0,36 Q-16,28 -16,12 Z" fill="#B23A2A" />
		<path d="M-30,-36 L-20,-56 L0,-44 L20,-56 L30,-36 Z" fill="#F2B32A" />
	</g>
);

const Lamp: React.FC<{x: number; flip?: boolean}> = ({x, flip}) => (
	<g transform={`translate(${x} 1330) scale(${flip ? -1 : 1} 1)`}>
		<circle cx={0} cy={60} r={170} fill="url(#lampGlow)" />
		<path d="M-90,60 Q-90,-10 0,-20 Q90,-10 90,60 Z" fill="#F7A824" />
		<path d="M-90,60 Q-90,-10 0,-20 Q-40,0 -46,60 Z" fill="#FFD066" />
		<rect x={-96} y={52} width={192} height={18} rx={9} fill="#D9861A" />
		<rect x={-10} y={70} width={20} height={240} fill="#C9711A" />
		<path d="M-50,320 L50,320 L30,290 L-30,290 Z" fill="#B85E14" />
	</g>
);

/** The seated official: navy suit, thinning grey-brown hair, worried face. */
const Official: React.FC<{t: number}> = ({t}) => {
	// scratch cycle 22.3-23.8, then the hand comes down to tap the gun
	const scratching = t > 22.25 && t < 23.9;
	const sc = Math.sin((t - 22.3) * Math.PI * 2 * 1.6);
	const handTo = kf(t, [
		[22.0, 0],
		[22.3, 1],
		[23.8, 1],
		[24.25, 0],
	]);
	const tap = t > 24.3 ? Math.max(0, Math.sin((t - 24.3) * Math.PI * 2 * 1.4)) * 12 : 0;
	const rest: [number, number] = [150, 260 - tap];
	const head: [number, number] = [110 + sc * 6 * (scratching ? 1 : 0), -150 + sc * 14 * (scratching ? 1 : 0)];
	const hR: [number, number] = [rest[0] + (head[0] - rest[0]) * handTo, rest[1] + (head[1] - rest[1]) * handTo];
	const shR: [number, number] = [150, 70];
	const eR = ik(shR, hR, 150, 140, handTo > 0.5 ? -1 : 1);
	const blink = blinking(t, 21) || blinking(t + 1.3, 22);
	const headTilt = Math.sin(t * 1.3) * 2 + (scratching ? -4 : 0);
	return (
		<g transform="translate(540 600)">
			{/* body */}
			<path d="M-230,500 L-210,120 Q-200,40 -110,30 L110,30 Q200,40 210,120 L230,500 Z" fill="#27303D" />
			<path d="M120,30 Q200,40 210,120 L230,500 L150,500 Z" fill="#171F2C" />
			<path d="M-60,30 L0,190 L60,30 Z" fill="#CFE0F5" />
			<path d="M-60,30 L0,190 L-8,30 Z" fill="#B7CBE6" />
			<path d="M-14,60 L14,60 L22,180 L0,210 L-22,180 Z" fill="#C0392B" />
			<path d="M-14,60 L14,60 L10,80 L-10,80 Z" fill="#8E2A20" />
			<path d="M-60,30 L-110,30 L-20,240 L-6,200 Z" fill="#1D2532" />
			<path d="M60,30 L110,30 L20,240 L6,200 Z" fill="#1D2532" />
			{/* neck + head */}
			<rect x={-34} y={-20} width={68} height={60} rx={14} fill={P.skinShade} />
			<g transform={`rotate(${headTilt} 0 -10)`}>
				<ellipse cx={-70} cy={-100} rx={18} ry={26} fill={P.skin} />
				<ellipse cx={70} cy={-100} rx={18} ry={26} fill={P.skinShade} />
				<rect x={-68} y={-210} width={136} height={200} rx={56} fill={P.skin} />
				<path d="M30,-205 Q68,-190 68,-120 L68,-60 Q60,-20 30,-12 Q60,-80 30,-205 Z" fill={P.skinShade} />
				{/* thinning hair: side band + a few strands on top */}
				<path d="M-72,-110 Q-80,-200 -20,-214 Q-60,-190 -56,-120 Z" fill="#A08E6F" />
				<path d="M72,-110 Q80,-200 20,-214 Q60,-190 56,-120 Z" fill="#8F7E61" />
				<path d="M-40,-206 Q0,-226 44,-206 Q20,-214 0,-212 Q-20,-212 -40,-206 Z" fill="#A08E6F" />
				<path d="M-30,-196 Q0,-205 30,-196" stroke="#B9A888" strokeWidth={5} fill="none" strokeLinecap="round" />
				{/* forehead lines (worry) */}
				<path d="M-34,-168 Q0,-176 34,-168 M-28,-156 Q0,-163 28,-156" stroke="#D99A78" strokeWidth={4} fill="none" strokeLinecap="round" />
				{/* brows raised */}
				<rect x={-50} y={-146} width={36} height={9} rx={4.5} fill="#7B6A50" transform="rotate(-12 -32 -142)" />
				<rect x={14} y={-146} width={36} height={9} rx={4.5} fill="#7B6A50" transform="rotate(12 32 -142)" />
				{/* eyes */}
				{blink ? (
					<g>
						<rect x={-42} y={-120} width={22} height={5} rx={2.5} fill="#3A2A20" />
						<rect x={20} y={-120} width={22} height={5} rx={2.5} fill="#3A2A20" />
					</g>
				) : (
					<g>
						{[-31, 31].map((x) => (
							<g key={x}>
								<ellipse cx={x} cy={-118} rx={12} ry={10} fill="#FFFFFF" />
								<circle cx={x + 1} cy={-117} r={7} fill="#2563B0" />
								<circle cx={x + 1} cy={-117} r={3.5} fill="#0F1C30" />
								<circle cx={x + 3} cy={-120} r={2} fill="#FFFFFF" />
							</g>
						))}
						<path d="M-44,-110 Q-31,-104 -18,-110 M18,-110 Q31,-104 44,-110" stroke="#D99A78" strokeWidth={3} fill="none" />
					</g>
				)}
				{/* nose, cheeks, mouth */}
				<path d="M-8,-112 Q-12,-80 -14,-74 Q0,-66 14,-74 Q10,-84 8,-112 Z" fill={P.skinDeep} opacity={0.8} />
				<ellipse cx={-42} cy={-80} rx={13} ry={9} fill={P.blush} opacity={0.55} />
				<ellipse cx={42} cy={-80} rx={13} ry={9} fill={P.blush} opacity={0.55} />
				<ellipse cx={0} cy={-46} rx={9} ry={11 + Math.sin(t * 7) * 2} fill="#5A2A20" />
				<ellipse cx={0} cy={-40} rx={5} ry={4} fill="#C0392B" />
				<path d="M-28,-26 Q0,-16 28,-26" stroke="#E3A584" strokeWidth={4} fill="none" strokeLinecap="round" />
			</g>
			{/* right arm (scratch / tap) */}
			<path d={`M${shR[0]},${shR[1]} L${eR[0]},${eR[1]} L${hR[0]},${hR[1]}`} fill="none" stroke="#1F2734" strokeWidth={78} strokeLinecap="round" strokeLinejoin="round" />
			<path d={`M${eR[0]},${eR[1]} L${hR[0]},${hR[1]}`} fill="none" stroke="#000" strokeOpacity={0.12} strokeWidth={78} strokeLinecap="round" />
			<circle cx={hR[0]} cy={hR[1]} r={44} fill={P.hand} />
			<path d={`M${hR[0] - 40},${hR[1] + 12} Q${hR[0]},${hR[1] + 52} ${hR[0] + 36},${hR[1] + 20} Q${hR[0] + 20},${hR[1] + 44} ${hR[0]},${hR[1] + 44} Z`} fill={P.handShade} opacity={0.7} />
		</g>
	);
};

export const Office: React.FC<{t: number}> = ({t}) => {
	const u = clamp((t - 22.0) / 4.33);
	const c = camAt(t, [
		[22.0, {x: 540, y: 960, s: 1, r: 0}],
		[26.4, {x: 540, y: 920, s: 1.12, r: 0}, E.linear],
	]);
	return (
		<g>
			<g transform={camT(c)}>
				<rect x={-300} y={-400} width={1680} height={2700} fill="#542A17" />
				<rect x={935} y={-400} width={445} height={520} fill="#DAB696" />
				<rect x={-300} y={160} width={1680} height={30} fill="#351815" />
				<Panel x={-60} w={170} top={300} c="#643827" />
				<Panel x={210} w={250} top={250} c="#6F3A28" />
				<Panel x={620} w={250} top={250} c="#6F3A28" />
				<Panel x={970} w={170} top={300} c="#643827" />
				<rect x={-300} y={1150} width={1680} height={60} fill="#351815" />
				<Emblem />
				<Official t={t} />
				{/* papers + folders on the left of the desk */}
				<g transform="translate(-20 760)">
					<rect x={0} y={150} width={240} height={90} rx={8} fill="#2E4A7A" />
					<rect x={0} y={150} width={240} height={14} rx={7} fill="#4467A0" />
					{[0, 1, 2, 3, 4].map((i) => (
						<rect key={i} x={10 + (i % 2) * 6} y={50 + i * 20} width={220} height={16} rx={3} fill={i % 2 ? '#F2EEE6' : '#FFFFFF'} />
					))}
					<rect x={10} y={30} width={210} height={20} rx={4} fill="#E1655A" opacity={0.85} />
				</g>
				{/* AK-12 lying across the desk, hand rests on it after the scratch */}
				<Gun g={{kind: 'ak12', x: 560, y: 880, rot: -12, s: 2.05}} />
				{/* desk */}
				<rect x={-80} y={1000} width={1240} height={70} rx={10} fill="#85402E" />
				<rect x={-80} y={1000} width={1240} height={14} rx={7} fill="#A65A44" />
				<rect x={-80} y={1060} width={1240} height={640} fill="#752E22" />
				<rect x={-80} y={1060} width={1240} height={24} fill="#29110E" opacity={0.6} />
				{[[-40, 330], [380, 320], [790, 330]].map(([x, w], i) => (
					<g key={i}>
						<rect x={x} y={1130} width={w} height={500} rx={6} fill="#6A2A1F" />
						<rect x={x + 20} y={1150} width={w - 40} height={460} rx={4} fill="none" stroke="#94644D" strokeWidth={5} />
						<path d={`M${x + w - 120},1150 L${x + w - 20},1150 L${x + w - 20},1250 Z`} fill="#FFFFFF" opacity={0.06} />
					</g>
				))}
				<rect x={-300} y={1700} width={1680} height={600} fill="#D9B48C" />
				<Lamp x={30} />
				<Lamp x={1050} flip />
			</g>
		</g>
	);
};
