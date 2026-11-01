import React from 'react';
import {P} from './defs';

// Rifles drawn as layered flat shapes: base fill, a darker underside, a lighter top-edge strip.
// Local frame: origin at the receiver centre, barrel along +x, ~400 units long.

export type GunKind = 'ak47' | 'ak12' | 'ak12acc' | 'm4';
export type GunPose = {kind: GunKind; x: number; y: number; rot: number; s?: number};

const ANCH: Record<GunKind, {grip: [number, number]; fore: [number, number]; muzzle: [number, number]; stock: [number, number]}> = {
	ak47: {grip: [-38, 34], fore: [98, 2], muzzle: [200, -2], stock: [-190, 14]},
	ak12: {grip: [-38, 34], fore: [104, 2], muzzle: [214, -2], stock: [-186, 14]},
	ak12acc: {grip: [-38, 34], fore: [118, 40], muzzle: [272, -2], stock: [-186, 14]},
	m4: {grip: [-36, 34], fore: [92, 2], muzzle: [206, -4], stock: [-186, 10]},
};

/** World position of a gun anchor after the gun's transform (translate, rotate, scale). */
export function gunPt(g: GunPose, name: 'grip' | 'fore' | 'muzzle' | 'stock'): [number, number] {
	const [lx, ly] = ANCH[g.kind][name];
	const s = g.s ?? 1;
	const a = (g.rot * Math.PI) / 180;
	return [g.x + s * (lx * Math.cos(a) - ly * Math.sin(a)), g.y + s * (lx * Math.sin(a) + ly * Math.cos(a))];
}

const Rail: React.FC<{x0: number; x1: number; y: number}> = ({x0, x1, y}) => {
	const teeth = [];
	for (let x = x0 + 4; x < x1 - 6; x += 10) teeth.push(<rect key={x} x={x} y={y - 7} width={6} height={5} rx={1} fill="#1A1C1B" />);
	return (
		<g>
			<rect x={x0} y={y - 8} width={x1 - x0} height={10} rx={2} fill="#2A2D2B" />
			{teeth}
			<rect x={x0} y={y - 9} width={x1 - x0} height={2.5} rx={1} fill={P.metalHi} opacity={0.8} />
		</g>
	);
};

const Slots: React.FC<{x0: number; x1: number; y: number; n: number}> = ({x0, x1, y, n}) => {
	const out = [];
	const step = (x1 - x0) / n;
	for (let i = 0; i < n; i++) out.push(<rect key={i} x={x0 + i * step + 2} y={y} width={step - 6} height={8} rx={4} fill="#1C1E1D" />);
	return <g>{out}</g>;
};

const AK47: React.FC = () => (
	<g>
		{/* stock */}
		<path d="M-96,-15 L-188,-6 Q-196,-5 -197,4 L-198,38 Q-197,46 -188,46 L-170,46 L-96,13 Z" fill={P.wood} />
		<path d="M-188,40 L-170,40 L-96,8 L-96,13 L-170,46 L-188,46 Z" fill={P.woodDark} />
		<path d="M-188,-6 L-96,-15 L-96,-10 L-186,-1 Z" fill={P.woodHi} opacity={0.7} />
		<rect x={-201} y={-7} width={8} height={54} rx={3} fill="#3A2A20" />
		{/* pistol grip */}
		<path d="M-44,10 L-22,10 L-30,62 Q-32,70 -40,69 L-52,66 Q-58,63 -56,56 Z" fill={P.wood} />
		<path d="M-30,62 Q-32,70 -40,69 L-52,66 L-49,58 L-30,58 Z" fill={P.woodDark} />
		{/* trigger guard */}
		<path d="M-26,13 Q-22,34 -4,34 Q6,33 6,13" fill="none" stroke={P.metal} strokeWidth={4.5} />
		<rect x={-16} y={14} width={4} height={14} rx={2} fill={P.metal} />
		{/* receiver */}
		<path d="M-100,-18 Q-30,-27 58,-19 L58,14 L-100,14 Z" fill={P.metal} />
		<path d="M-100,4 L58,4 L58,14 L-100,14 Z" fill={P.metal3} />
		<path d="M-100,-18 Q-30,-27 58,-19 L58,-15 Q-30,-23 -100,-14 Z" fill={P.metalHi} />
		<rect x={-70} y={-8} width={58} height={6} rx={3} fill="#4A4C44" />
		<rect x={-8} y={-11} width={34} height={9} rx={2} fill="#1E201D" />
		<circle cx={-84} cy={6} r={3} fill="#1E201D" />
		<circle cx={40} cy={6} r={3} fill="#1E201D" />
		{/* rear sight block */}
		<path d="M50,-21 L64,-21 L66,-27 L54,-28 Z" fill={P.metal2} />
		{/* upper handguard (gas tube) */}
		<rect x={58} y={-25} width={72} height={13} rx={6} fill={P.wood} />
		<rect x={58} y={-25} width={72} height={4} rx={2} fill={P.woodHi} opacity={0.75} />
		<rect x={128} y={-22} width={30} height={8} rx={3} fill={P.metal2} />
		{/* lower handguard */}
		<path d="M58,-12 L140,-10 Q146,-9 145,-2 L142,12 Q140,16 134,16 L58,16 Z" fill={P.wood} />
		<path d="M58,9 L142,9 L141,12 Q140,16 134,16 L58,16 Z" fill={P.woodDark} />
		<rect x={74} y={-4} width={52} height={3.5} rx={1.7} fill={P.woodDark} opacity={0.8} />
		<rect x={74} y={3} width={52} height={3.5} rx={1.7} fill={P.woodDark} opacity={0.8} />
		{/* barrel, front sight, muzzle */}
		<rect x={140} y={-5} width={52} height={8} rx={2} fill={P.metal} />
		<rect x={140} y={-5} width={52} height={2.4} fill={P.metalHi} />
		<path d="M168,-5 L170,-26 L176,-26 L180,-5 Z" fill={P.metal} />
		<path d="M190,-7 L204,-8 L204,5 L190,5 Z" fill={P.metal3} />
		{/* magazine */}
		<path d="M0,12 L40,12 Q52,58 78,102 L48,116 Q26,66 0,12 Z" fill="#2E2D2A" />
		<path d="M30,12 L40,12 Q52,58 78,102 L70,106 Q46,62 30,12 Z" fill="#3E3D39" />
		<path d="M12,40 L42,36 M20,58 L52,52 M30,76 L62,70 M38,94 L70,88" stroke="#22211F" strokeWidth={3} strokeLinecap="round" />
	</g>
);

const AK12Body: React.FC<{acc?: boolean}> = ({acc}) => (
	<g>
		{/* adjustable polymer stock with cut-out */}
		<path
			fillRule="evenodd"
			d="M-96,-16 L-182,-14 Q-192,-14 -192,-4 L-194,36 Q-194,46 -184,46 L-166,46 Q-150,44 -126,24 L-96,14 Z M-156,-4 L-120,-4 Q-112,-4 -116,4 L-128,18 Q-134,24 -146,24 L-152,24 Q-158,24 -158,18 Z"
			fill={P.metal3}
		/>
		<path d="M-182,-14 L-96,-16 L-96,-11 L-180,-9 Z" fill={P.metalHi} opacity={0.75} />
		<rect x={-198} y={-14} width={9} height={60} rx={4} fill="#1C1F21" />
		<rect x={-112} y={-6} width={18} height={10} rx={3} fill="#1C1F21" />
		{/* pistol grip */}
		<path d="M-46,10 L-22,10 L-28,62 Q-30,70 -38,70 L-52,67 Q-58,64 -56,56 Z" fill={P.metal3} />
		<path d="M-44,26 L-30,26 M-46,38 L-32,38 M-48,50 L-34,50" stroke="#1A1D1F" strokeWidth={3} strokeLinecap="round" />
		<path d="M-26,13 Q-22,34 -4,34 Q6,33 6,13" fill="none" stroke={P.metal} strokeWidth={4.5} />
		{/* receiver */}
		<path d="M-100,-18 L62,-18 L62,14 L-100,14 Z" fill={P.metal} />
		<path d="M-100,4 L62,4 L62,14 L-100,14 Z" fill={P.metal3} />
		<rect x={-72} y={-8} width={60} height={6} rx={3} fill="#4A4C44" />
		<rect x={-6} y={-11} width={36} height={9} rx={2} fill="#1E201D" />
		<circle cx={46} cy={-2} r={4} fill="#1E201D" />
		{/* vented handguard */}
		<rect x={60} y={-20} width={94} height={34} rx={8} fill={P.metal2} />
		<rect x={60} y={6} width={94} height={8} rx={4} fill={P.metal3} />
		<Slots x0={68} x1={148} y={-8} n={5} />
		<rect x={60} y={-20} width={94} height={3} rx={1.5} fill={P.metalHi} opacity={0.8} />
		{/* full-length top rail */}
		<Rail x0={-92} x1={150} y={-18} />
		{/* folding sights */}
		<path d="M-86,-27 L-74,-27 L-72,-36 L-84,-36 Z" fill={P.metal3} />
		<path d="M136,-27 L148,-27 L146,-38 L138,-38 Z" fill={P.metal3} />
		{/* barrel + muzzle brake */}
		<rect x={152} y={-5} width={46} height={8} rx={2} fill={P.metal} />
		<rect x={152} y={-5} width={46} height={2.4} fill={P.metalHi} />
		<rect x={196} y={-9} width={20} height={15} rx={3} fill={P.metal3} />
		<rect x={201} y={-6} width={3} height={9} rx={1.5} fill="#121414" />
		<rect x={208} y={-6} width={3} height={9} rx={1.5} fill="#121414" />
		{/* magazine (polymer, ribbed) */}
		<path d="M2,12 L42,12 Q54,58 80,100 L50,114 Q28,66 2,12 Z" fill="#232625" />
		<path d="M32,12 L42,12 Q54,58 80,100 L72,104 Q48,62 32,12 Z" fill="#363A39" />
		<path d="M14,42 L44,37 M22,60 L54,54 M32,78 L64,71" stroke="#161818" strokeWidth={4} strokeLinecap="round" />
		{acc && (
			<g>
				{/* suppressor */}
				<rect x={200} y={-12} width={78} height={20} rx={7} fill="#2A2C2D" />
				<rect x={200} y={-12} width={78} height={5} rx={2.5} fill={P.metalHi} opacity={0.85} />
				<rect x={230} y={-12} width={4} height={20} fill="#1A1C1C" />
				{/* vertical foregrip */}
				<path d="M108,12 L130,12 L128,62 Q128,70 119,70 Q110,70 110,62 Z" fill={P.metal3} />
				<rect x={112} y={30} width={14} height={3} rx={1.5} fill="#151717" />
				<rect x={112} y={42} width={14} height={3} rx={1.5} fill="#151717" />
				{/* red-dot optic */}
				<rect x={-40} y={-34} width={30} height={10} rx={3} fill="#1A1C1C" />
				<rect x={-58} y={-60} width={66} height={30} rx={10} fill="#1E2124" />
				<rect x={-58} y={-60} width={66} height={6} rx={3} fill={P.metalHi} />
				<circle cx={8} cy={-45} r={11} fill="#152028" />
				<circle cx={9} cy={-45} r={7} fill="#3D8FC9" />
				<circle cx={11} cy={-48} r={2.5} fill="#CDEBFF" />
				{/* side light */}
				<rect x={80} y={-6} width={30} height={12} rx={6} fill="#1A1C1C" />
				<circle cx={110} cy={0} r={5} fill="#E8E4C8" />
			</g>
		)}
	</g>
);

const M4: React.FC = () => (
	<g>
		{/* collapsible stock + buffer tube */}
		<rect x={-150} y={-8} width={56} height={14} rx={4} fill="#2F3338" />
		<path d="M-186,-16 L-140,-12 Q-134,-11 -134,-4 L-136,28 Q-137,36 -146,37 L-188,40 Q-194,40 -194,32 L-194,-8 Q-194,-16 -186,-16 Z" fill="#3A3F45" />
		<path d="M-186,-16 L-140,-12 L-140,-7 L-188,-11 Z" fill="#6A717A" />
		<rect x={-198} y={-16} width={8} height={56} rx={3} fill="#24272B" />
		{/* pistol grip */}
		<path d="M-46,8 L-22,8 L-28,60 Q-30,68 -38,68 L-52,65 Q-58,62 -56,54 Z" fill="#2F3338" />
		<path d="M-26,11 Q-22,32 -4,32 Q6,31 6,11" fill="none" stroke="#3A3F45" strokeWidth={4.5} />
		{/* lower + upper receiver */}
		<path d="M-96,-16 L50,-16 L50,12 L-6,12 L-14,22 L-60,22 L-96,10 Z" fill="#3A3F45" />
		<path d="M-96,2 L50,2 L50,12 L-6,12 L-14,22 L-60,22 L-96,10 Z" fill="#30353A" />
		<rect x={-96} y={-18} width={146} height={4} rx={2} fill="#6A717A" />
		<rect x={-30} y={-8} width={40} height={10} rx={2} fill="#202327" />
		<circle cx={-70} cy={-2} r={4} fill="#555B63" />
		{/* carry handle */}
		<path fillRule="evenodd" d="M-62,-16 L-56,-44 L28,-44 L34,-16 Z M-46,-22 L-42,-36 L16,-36 L20,-22 Z" fill="#555B63" />
		<rect x={-58} y={-46} width={88} height={4} rx={2} fill="#7B838C" />
		{/* ribbed handguard */}
		<rect x={50} y={-15} width={90} height={28} rx={9} fill="#3A3F45" />
		<rect x={50} y={-15} width={90} height={5} rx={2.5} fill="#6A717A" />
		{[60, 72, 84, 96, 108, 120].map((x) => (
			<rect key={x} x={x} y={-8} width={5} height={16} rx={2.5} fill="#272B30" />
		))}
		{/* front sight post */}
		<path d="M126,-14 L132,-46 L140,-46 L144,-14 Z" fill="#3A3F45" />
		{/* barrel + flash hider */}
		<rect x={140} y={-4} width={54} height={7} rx={2} fill="#2E3237" />
		<rect x={192} y={-7} width={18} height={12} rx={3} fill="#24272B" />
		{/* magazine */}
		<path d="M0,12 L32,12 Q38,50 46,86 L18,92 Q12,50 0,12 Z" fill="#2E3237" />
		<path d="M24,12 L32,12 Q38,50 46,86 L39,88 Q32,50 24,12 Z" fill="#454B52" />
	</g>
);

export const Gun: React.FC<{g: GunPose}> = ({g}) => (
	<g transform={`translate(${g.x} ${g.y}) rotate(${g.rot}) scale(${g.s ?? 1})`}>
		{g.kind === 'ak47' ? <AK47 /> : g.kind === 'm4' ? <M4 /> : <AK12Body acc={g.kind === 'ak12acc'} />}
	</g>
);

/** A gun drawn standalone (no transform helper). */
export const GunArt: React.FC<{kind: GunKind}> = ({kind}) =>
	kind === 'ak47' ? <AK47 /> : kind === 'm4' ? <M4 /> : <AK12Body acc={kind === 'ak12acc'} />;
