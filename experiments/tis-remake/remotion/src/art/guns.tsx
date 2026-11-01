import React from 'react';
import {P} from './defs';

// Rifles drawn as layered flat shapes on a 5-step grey ramp (v2): darkest for holes and slots, a dark
// furniture grey, a mid receiver grey, a lit-plane grey and a specular top-edge highlight, plus small
// tan/gold accents (selector tip, rivets). Local frame: origin at the receiver centre, barrel along +x,
// ~420 units long. `lod` scales the micro-detail with camera distance (0 = far, 1 = normal, 2 = hero).

export type GunKind = 'ak47' | 'ak12' | 'ak12acc' | 'm4';
export type GunPose = {kind: GunKind; x: number; y: number; rot: number; s?: number; lod?: 0 | 1 | 2};

export const G = {
	g0: '#1E2125', // holes, slots, deepest shadow
	g1: '#30343A', // furniture (stock, grip, magazine)
	g2: '#43484F', // receiver / handguard base
	g3: '#596069', // lit upper planes
	g4: '#7E8691', // specular top edges
	g5: '#A4ACB6', // tiny glints (hero only)
	tan: '#B99A62',
	gold: '#D9B24A',
};

export const ANCH: Record<GunKind, {grip: [number, number]; fore: [number, number]; muzzle: [number, number]; stock: [number, number]; sel: [number, number]}> = {
	ak47: {grip: [-42, 46], fore: [100, 8], muzzle: [204, -2], stock: [-190, 14], sel: [-34, -6]},
	ak12: {grip: [-42, 46], fore: [108, 8], muzzle: [222, -2], stock: [-190, 14], sel: [-34, -6]},
	ak12acc: {grip: [-42, 46], fore: [119, 44], muzzle: [280, -2], stock: [-190, 14], sel: [-34, -6]},
	m4: {grip: [-40, 44], fore: [96, 6], muzzle: [212, -4], stock: [-190, 10], sel: [-30, -2]},
};

/** World position of a gun anchor after the gun's transform (translate, rotate, scale). */
export function gunPt(g: GunPose, name: 'grip' | 'fore' | 'muzzle' | 'stock' | 'sel'): [number, number] {
	const [lx, ly] = ANCH[g.kind][name];
	const s = g.s ?? 1;
	const a = (g.rot * Math.PI) / 180;
	return [g.x + s * (lx * Math.cos(a) - ly * Math.sin(a)), g.y + s * (lx * Math.sin(a) + ly * Math.cos(a))];
}

/** Picatinny rail: base bar, square teeth with lit tops, a specular top edge. */
const Rail: React.FC<{x0: number; x1: number; y: number; lod: number; base?: string}> = ({x0, x1, y, lod, base = G.g1}) => {
	const teeth: React.ReactNode[] = [];
	if (lod > 0)
		for (let x = x0 + 4; x < x1 - 6; x += 9) {
			teeth.push(<rect key={x} x={x} y={y - 9} width={5.5} height={6} rx={1} fill={G.g2} />);
			teeth.push(<rect key={`h${x}`} x={x} y={y - 9} width={5.5} height={1.8} fill={G.g4} />);
		}
	return (
		<g>
			<rect x={x0} y={y - 5} width={x1 - x0} height={8} rx={2} fill={base} />
			{teeth}
			{lod === 0 && <rect x={x0} y={y - 8} width={x1 - x0} height={3} fill={G.g3} />}
		</g>
	);
};

/** Row of rounded vent holes with a lit lower bevel. */
const Vents: React.FC<{x0: number; x1: number; y: number; n: number; h?: number; lod: number}> = ({x0, x1, y, n, h = 9, lod}) => {
	const out: React.ReactNode[] = [];
	const step = (x1 - x0) / n;
	for (let i = 0; i < n; i++) {
		const x = x0 + i * step + 2;
		out.push(<rect key={i} x={x} y={y} width={step - 6} height={h} rx={h / 2} fill={G.g0} />);
		if (lod > 0) out.push(<rect key={`b${i}`} x={x + 2} y={y + h - 1} width={step - 10} height={2} rx={1} fill={G.g3} />);
	}
	return <g>{out}</g>;
};

/** Ribbed curved magazine (polymer or steel). */
const Mag: React.FC<{lod: number; fill?: string; edge?: string; bend?: number}> = ({lod, fill = G.g1, edge = G.g2, bend = 1}) => {
	const b = bend;
	return (
		<g>
			<path d={`M2,12 L44,12 Q${54 + 4 * b},60 ${82 + 4 * b},102 L${52 + 2 * b},118 Q${30 - 2 * b},68 2,12 Z`} fill={fill} />
			<path d={`M34,12 L44,12 Q${54 + 4 * b},60 ${82 + 4 * b},102 L${74 + 4 * b},106 Q${48 + 2 * b},62 34,12 Z`} fill={edge} />
			<path d={`M2,12 L12,12 Q${34 - b},62 ${58 + 2 * b},114 L${52 + 2 * b},118 Q${30 - 2 * b},68 2,12 Z`} fill={G.g0} opacity={0.55} />
			{lod > 0 &&
				[0, 1, 2, 3].map((i) => {
					const u = 0.22 + i * 0.18;
					const xa = 8 + u * 46;
					const ya = 12 + u * 100;
					return (
						<g key={i}>
							<path d={`M${xa},${ya} L${xa + 34},${ya - 7}`} stroke={G.g0} strokeWidth={4.5} strokeLinecap="round" />
							<path d={`M${xa + 1},${ya + 4} L${xa + 33},${ya - 3}`} stroke={G.g3} strokeWidth={1.6} strokeLinecap="round" opacity={0.8} />
						</g>
					);
				})}
			<path d={`M${50 + 2 * b},116 L${84 + 4 * b},100 L${88 + 4 * b},108 L${55 + 2 * b},124 Z`} fill={G.g0} />
		</g>
	);
};

/** Ribbed pistol grip, angled back. */
const Grip: React.FC<{fill: string; lod: number; hi?: string}> = ({fill, lod, hi = G.g3}) => (
	<g>
		<path d="M-48,10 L-22,10 L-28,64 Q-30,72 -39,72 L-53,69 Q-60,66 -58,57 Z" fill={fill} />
		<path d="M-48,10 L-40,10 L-52,66 Q-57,64 -58,57 Z" fill="#000" opacity={0.22} />
		<path d="M-24,12 L-22,10 L-28,64 L-31,64 Z" fill={hi} opacity={0.9} />
		{lod > 0 && <path d="M-46,30 L-31,30 M-48,42 L-33,42 M-50,54 L-35,54" stroke={G.g0} strokeWidth={2.6} strokeLinecap="round" opacity={0.8} />}
	</g>
);

const TriggerGuard: React.FC<{c?: string}> = ({c = G.g2}) => (
	<g>
		<path d="M-24,13 Q-21,36 -2,36 Q8,35 8,13" fill="none" stroke={c} strokeWidth={5} />
		<path d="M-12,14 Q-10,24 -14,30" fill="none" stroke={G.g0} strokeWidth={4} strokeLinecap="round" />
	</g>
);

/** AK selector lever: long flat lever on the right side of the receiver, tan tip. */
const Selector: React.FC<{lod: number}> = ({lod}) => (
	<g>
		<path d="M-66,-9 L4,-6 L6,1 L-64,-1 Z" fill={G.g1} />
		<path d="M-66,-9 L4,-6 L4,-4 L-66,-7 Z" fill={G.g4} opacity={0.85} />
		<path d="M2,-7 L14,-2 L12,8 L2,4 Z" fill={G.g1} />
		{lod > 0 && <rect x={6} y={-3} width={6} height={6} rx={1.5} fill={G.tan} />}
	</g>
);

const Rivets: React.FC<{pts: [number, number][]; c?: string; lod: number}> = ({pts, c = G.g0, lod}) =>
	lod > 0 ? (
		<g>
			{pts.map(([x, y], i) => (
				<g key={i}>
					<circle cx={x} cy={y} r={3.2} fill={c} />
					{lod > 1 && <circle cx={x - 0.8} cy={y - 0.9} r={1.1} fill={G.g4} />}
				</g>
			))}
		</g>
	) : null;

const AK47: React.FC<{lod: number}> = ({lod}) => (
	<g>
		{/* stock */}
		<path d="M-96,-15 L-188,-6 Q-196,-5 -197,4 L-198,38 Q-197,46 -188,46 L-170,46 L-96,13 Z" fill={P.wood} />
		<path d="M-188,40 L-170,40 L-96,8 L-96,13 L-170,46 L-188,46 Z" fill={P.woodDark} />
		<path d="M-188,-6 L-96,-15 L-96,-10 L-186,-1 Z" fill={P.woodHi} />
		{lod > 0 && <path d="M-180,8 Q-150,4 -110,-4 M-176,22 Q-140,14 -112,6 M-160,32 Q-140,26 -120,16" stroke={P.woodDark} strokeWidth={2.2} fill="none" strokeLinecap="round" opacity={0.7} />}
		<rect x={-203} y={-8} width={9} height={56} rx={3} fill={G.g1} />
		<rect x={-203} y={-8} width={9} height={3} rx={1.5} fill={G.g3} />
		{/* pistol grip */}
		<path d="M-46,10 L-22,10 L-30,62 Q-32,70 -40,69 L-52,66 Q-58,63 -56,56 Z" fill={P.wood} />
		<path d="M-30,62 Q-32,70 -40,69 L-52,66 L-49,58 L-30,58 Z" fill={P.woodDark} />
		<path d="M-24,12 L-22,10 L-30,62 L-33,62 Z" fill={P.woodHi} />
		<TriggerGuard />
		{/* receiver: stamped steel, three values */}
		<path d="M-100,-18 Q-30,-26 60,-19 L60,14 L-100,14 Z" fill={G.g2} />
		<path d="M-100,4 L60,4 L60,14 L-100,14 Z" fill={G.g1} />
		<path d="M-100,-18 Q-30,-26 60,-19 L60,-12 Q-30,-19 -100,-11 Z" fill={G.g3} />
		<path d="M-100,-18 Q-30,-26 60,-19 L60,-17 Q-30,-24 -100,-16 Z" fill={G.g4} />
		<rect x={-4} y={-10} width={36} height={9} rx={2} fill={G.g0} />
		<rect x={30} y={-6} width={14} height={6} rx={2} fill={G.g1} />
		<Selector lod={lod} />
		<Rivets pts={[[-86, 8], [42, 8], [-20, 8]]} lod={lod} />
		{/* rear sight block */}
		<path d="M52,-21 L66,-21 L68,-28 L56,-29 Z" fill={G.g2} />
		{/* upper handguard (gas tube) */}
		<rect x={60} y={-26} width={72} height={13} rx={6} fill={P.wood} />
		<rect x={60} y={-26} width={72} height={4} rx={2} fill={P.woodHi} />
		<rect x={130} y={-23} width={30} height={8} rx={3} fill={G.g2} />
		<rect x={130} y={-23} width={30} height={2.4} rx={1} fill={G.g4} />
		{/* lower handguard */}
		<path d="M60,-12 L142,-10 Q148,-9 147,-2 L144,12 Q142,16 136,16 L60,16 Z" fill={P.wood} />
		<path d="M60,9 L144,9 L143,12 Q142,16 136,16 L60,16 Z" fill={P.woodDark} />
		<path d="M60,-12 L142,-10 L142,-7 L60,-9 Z" fill={P.woodHi} />
		<rect x={76} y={-3} width={52} height={3.5} rx={1.7} fill={P.woodDark} />
		<rect x={76} y={4} width={52} height={3.5} rx={1.7} fill={P.woodDark} />
		{/* barrel, front sight, muzzle */}
		<rect x={142} y={-5} width={54} height={8} rx={2} fill={G.g2} />
		<rect x={142} y={-5} width={54} height={2.4} fill={G.g4} />
		<path d="M170,-5 L172,-28 L179,-28 L183,-5 Z" fill={G.g2} />
		<rect x={172} y={-28} width={7} height={3} fill={G.g4} />
		<path d="M192,-7 L208,-8 L208,5 L192,5 Z" fill={G.g1} />
		{/* steel magazine */}
		<Mag lod={lod} fill={G.g1} edge={G.g2} />
	</g>
);

const AK12Body: React.FC<{acc?: boolean; lod: number}> = ({acc, lod}) => (
	<g>
		{/* adjustable skeleton stock */}
		<path
			fillRule="evenodd"
			d="M-96,-16 L-186,-14 Q-196,-14 -196,-4 L-196,38 Q-196,48 -186,48 L-168,48 Q-150,46 -128,26 L-96,12 Z M-178,0 L-128,0 L-156,30 L-178,30 Z"
			fill={G.g1}
		/>
		<path d="M-186,-14 L-96,-16 L-96,-10 L-186,-8 Z" fill={G.g3} />
		<path d="M-186,-14 L-96,-16 L-96,-14 L-186,-12 Z" fill={G.g4} />
		<path d="M-168,48 Q-150,46 -128,26 L-124,30 Q-148,52 -168,52 Z" fill={G.g0} opacity={0.5} />
		<rect x={-204} y={-16} width={12} height={66} rx={5} fill={G.g0} />
		{lod > 0 && <path d="M-200,-8 L-200,42" stroke={G.g2} strokeWidth={2.4} strokeLinecap="round" />}
		<rect x={-112} y={-8} width={20} height={14} rx={3} fill={G.g0} />
		{/* pistol grip */}
		<Grip fill={G.g1} lod={lod} />
		<TriggerGuard />
		{/* receiver: mid grey body, lit upper plane, dark lower */}
		<path d="M-100,-18 L64,-18 L64,14 L-100,14 Z" fill={G.g2} />
		<path d="M-100,-18 L64,-18 L64,-10 L-100,-10 Z" fill={G.g3} />
		<path d="M-100,4 L64,4 L64,14 L-100,14 Z" fill={G.g1} />
		<rect x={-2} y={-9} width={36} height={9} rx={2} fill={G.g0} />
		{lod > 0 && <rect x={0} y={-2} width={32} height={1.6} fill={G.g3} />}
		<rect x={36} y={-6} width={16} height={6} rx={2} fill={G.g1} />
		<circle cx={52} cy={-3} r={3} fill={G.g4} />
		<Selector lod={lod} />
		<Rivets pts={[[-88, 9], [-60, 9], [50, 9]]} lod={lod} />
		{lod > 1 && <rect x={-90} y={-2} width={24} height={4} rx={2} fill={G.gold} opacity={0.85} />}
		{/* vented handguard: base, lit top, dark belly, two vent rows */}
		<rect x={62} y={-20} width={96} height={34} rx={8} fill={G.g2} />
		<rect x={62} y={-20} width={96} height={9} rx={4} fill={G.g3} />
		<rect x={62} y={6} width={96} height={8} rx={4} fill={G.g1} />
		<Vents x0={70} x1={152} y={-8} n={6} lod={lod} />
		{lod > 0 && <Vents x0={76} x1={146} y={3} n={5} h={5} lod={0} />}
		<rect x={62} y={-20} width={96} height={2.2} rx={1} fill={G.g4} />
		{/* bottom rail stub */}
		<Rail x0={80} x1={150} y={20} lod={lod > 1 ? 1 : 0} base={G.g1} />
		{/* full-length top rail */}
		<Rail x0={-94} x1={156} y={-20} lod={lod} />
		{/* folding sights */}
		<path d="M-88,-28 L-74,-28 L-72,-40 L-86,-40 Z" fill={G.g2} />
		<rect x={-86} y={-40} width={12} height={3} fill={G.g4} />
		<path d="M140,-28 L154,-28 L152,-42 L142,-42 Z" fill={G.g2} />
		<rect x={142} y={-42} width={10} height={3} fill={G.g4} />
		{/* gas block, barrel, front post, muzzle brake */}
		<rect x={156} y={-7} width={52} height={9} rx={2} fill={G.g2} />
		<rect x={156} y={-7} width={52} height={2.4} fill={G.g4} />
		<rect x={160} y={-12} width={18} height={20} rx={3} fill={G.g1} />
		<rect x={160} y={-12} width={18} height={3} rx={1.5} fill={G.g3} />
		<path d="M188,-6 L191,-34 L197,-34 L200,-6 Z" fill={G.g1} />
		<rect x={190} y={-36} width={8} height={4} rx={1} fill={G.g3} />
		<rect x={204} y={-10} width={22} height={17} rx={3} fill={G.g1} />
		<rect x={204} y={-10} width={22} height={3} rx={1.5} fill={G.g4} />
		<rect x={209} y={-6} width={3.5} height={10} rx={1.7} fill={G.g0} />
		<rect x={216} y={-6} width={3.5} height={10} rx={1.7} fill={G.g0} />
		{/* polymer magazine */}
		<Mag lod={lod} />
		{acc && (
			<g>
				{/* suppressor */}
				<rect x={206} y={-13} width={80} height={22} rx={8} fill={G.g1} />
				<rect x={206} y={-13} width={80} height={6} rx={3} fill={G.g3} />
				<rect x={206} y={-13} width={80} height={2} rx={1} fill={G.g4} />
				<rect x={236} y={-13} width={4} height={22} fill={G.g0} />
				<rect x={262} y={-13} width={4} height={22} fill={G.g0} />
				{/* vertical foregrip */}
				<path d="M108,14 L132,14 L130,64 Q130,72 120,72 Q110,72 110,64 Z" fill={G.g1} />
				<path d="M128,14 L132,14 L130,64 L127,64 Z" fill={G.g3} />
				<rect x={113} y={32} width={14} height={3} rx={1.5} fill={G.g0} />
				<rect x={113} y={44} width={14} height={3} rx={1.5} fill={G.g0} />
				{/* red-dot optic */}
				<rect x={-40} y={-36} width={30} height={10} rx={3} fill={G.g0} />
				<rect x={-60} y={-62} width={68} height={30} rx={10} fill={G.g1} />
				<rect x={-60} y={-62} width={68} height={8} rx={4} fill={G.g3} />
				<rect x={-56} y={-62} width={60} height={2.4} rx={1} fill={G.g4} />
				<circle cx={8} cy={-47} r={11} fill="#152028" />
				<circle cx={9} cy={-47} r={7} fill="#3D8FC9" />
				<circle cx={11} cy={-50} r={2.5} fill="#CDEBFF" />
				<rect x={-50} y={-44} width={12} height={4} rx={2} fill={G.tan} />
				{/* side light */}
				<rect x={84} y={-6} width={30} height={12} rx={6} fill={G.g0} />
				<rect x={84} y={-6} width={30} height={3} rx={1.5} fill={G.g3} />
				<circle cx={114} cy={0} r={5} fill="#E8E4C8" />
			</g>
		)}
	</g>
);

const M4: React.FC<{lod: number}> = ({lod}) => (
	<g>
		{/* collapsible stock + buffer tube */}
		<rect x={-150} y={-8} width={56} height={14} rx={4} fill={G.g1} />
		<rect x={-150} y={-8} width={56} height={3} rx={1.5} fill={G.g3} />
		<path d="M-186,-16 L-140,-12 Q-134,-11 -134,-4 L-136,28 Q-137,36 -146,37 L-188,40 Q-194,40 -194,32 L-194,-8 Q-194,-16 -186,-16 Z" fill={G.g2} />
		<path d="M-186,-16 L-140,-12 L-140,-6 L-188,-10 Z" fill={G.g3} />
		<path d="M-186,-16 L-140,-12 L-140,-10 L-188,-14 Z" fill={G.g4} />
		<path d="M-136,28 Q-137,36 -146,37 L-188,40 L-188,33 L-138,30 Z" fill={G.g1} />
		<rect x={-200} y={-16} width={10} height={58} rx={4} fill={G.g0} />
		{/* pistol grip */}
		<Grip fill={G.g1} lod={lod} />
		<TriggerGuard />
		{/* lower + upper receiver */}
		<path d="M-96,-16 L52,-16 L52,12 L-6,12 L-14,24 L-60,24 L-96,10 Z" fill={G.g2} />
		<path d="M-96,-16 L52,-16 L52,-8 L-96,-8 Z" fill={G.g3} />
		<path d="M-96,2 L52,2 L52,12 L-6,12 L-14,24 L-60,24 L-96,10 Z" fill={G.g1} />
		<rect x={-30} y={-6} width={40} height={10} rx={2} fill={G.g0} />
		<circle cx={-70} cy={-2} r={5} fill={G.g1} />
		<circle cx={-71} cy={-3} r={2} fill={G.tan} />
		<Rivets pts={[[-50, 6], [30, 6]]} lod={lod} />
		{/* carry handle */}
		<path fillRule="evenodd" d="M-62,-16 L-56,-46 L28,-46 L34,-16 Z M-46,-22 L-42,-36 L16,-36 L20,-22 Z" fill={G.g2} />
		<rect x={-58} y={-48} width={88} height={5} rx={2} fill={G.g4} />
		<rect x={18} y={-56} width={10} height={10} rx={2} fill={G.g1} />
		{/* ribbed rail handguard */}
		<rect x={52} y={-16} width={92} height={30} rx={9} fill={G.g2} />
		<rect x={52} y={-16} width={92} height={7} rx={3.5} fill={G.g3} />
		<rect x={52} y={8} width={92} height={6} rx={3} fill={G.g1} />
		{[62, 74, 86, 98, 110, 122].map((x) => (
			<g key={x}>
				<rect x={x} y={-7} width={6} height={16} rx={3} fill={G.g0} />
				{lod > 0 && <rect x={x + 6} y={-6} width={2} height={14} rx={1} fill={G.g3} />}
			</g>
		))}
		<Rail x0={54} x1={142} y={-16} lod={lod} />
		{/* front sight post */}
		<path d="M128,-14 L134,-48 L142,-48 L146,-14 Z" fill={G.g2} />
		<path d="M134,-48 L142,-48 L141,-44 L135,-44 Z" fill={G.g4} />
		{/* barrel + flash hider */}
		<rect x={144} y={-4} width={56} height={8} rx={2} fill={G.g1} />
		<rect x={144} y={-4} width={56} height={2.2} fill={G.g4} />
		<rect x={196} y={-8} width={20} height={14} rx={3} fill={G.g1} />
		<rect x={196} y={-8} width={20} height={3} rx={1.5} fill={G.g3} />
		{/* straight-ish magazine with ribs */}
		<path d="M0,12 L34,12 Q40,50 48,88 L18,94 Q12,50 0,12 Z" fill={G.g1} />
		<path d="M26,12 L34,12 Q40,50 48,88 L41,90 Q34,50 26,12 Z" fill={G.g2} />
		{lod > 0 &&
			[30, 50, 70].map((y) => (
				<g key={y}>
					<path d={`M${6 + y * 0.18},${y} L${34 + y * 0.16},${y - 2}`} stroke={G.g0} strokeWidth={3.5} strokeLinecap="round" />
					<path d={`M${7 + y * 0.18},${y + 3} L${34 + y * 0.16},${y + 1}`} stroke={G.g3} strokeWidth={1.4} strokeLinecap="round" />
				</g>
			))}
		<path d="M16,92 L50,86 L51,94 L17,100 Z" fill={G.g0} />
	</g>
);

const Body: React.FC<{kind: GunKind; lod: number}> = ({kind, lod}) =>
	kind === 'ak47' ? <AK47 lod={lod} /> : kind === 'm4' ? <M4 lod={lod} /> : <AK12Body acc={kind === 'ak12acc'} lod={lod} />;

export const Gun: React.FC<{g: GunPose}> = ({g}) => (
	<g transform={`translate(${g.x} ${g.y}) rotate(${g.rot}) scale(${g.s ?? 1})`}>
		<Body kind={g.kind} lod={g.lod ?? 1} />
	</g>
);

/** A gun drawn standalone (no transform helper). */
export const GunArt: React.FC<{kind: GunKind; lod?: 0 | 1 | 2}> = ({kind, lod = 1}) => <Body kind={kind} lod={lod} />;
