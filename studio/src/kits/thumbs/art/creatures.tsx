// Placeholder subjects in a scratchboard / engraving look (white on black). Each one is a
// nested <svg> placed into a box; the explainer kit's real art can replace them via spec.art.
import React from 'react';
import {Engraved, bezier, rng, taper, type Pt} from '../fx';

type BoxProps = {x: number; y: number; w: number; h: number; fx: string; id: string; flip?: boolean};

const Box: React.FC<BoxProps & {vb: string; children: React.ReactNode}> = ({x, y, w, h, vb, flip, children}) => {
	const [, , vw] = vb.split(' ').map(Number);
	return (
		<svg x={x} y={y} width={w} height={h} viewBox={vb} overflow="visible" preserveAspectRatio="xMidYMid meet">
			<g transform={flip ? `translate(${vw} 0) scale(-1 1)` : undefined}>{children}</g>
		</svg>
	);
};

// ----------------------------------------------------------------- sperm whale (side, facing left)

export const WHALE_VB = '0 0 1000 420';
/** Eye position in viewBox units (for arrows / human placement). */
export const WHALE_EYE: Pt = [262, 232];

export const SpermWhale: React.FC<BoxProps> = (p) => {
	const id = p.id;
	const body =
		'M40 128 C40 72 92 52 210 50 C390 48 560 78 700 140 C780 176 842 196 904 204 L906 228 C842 238 762 254 680 276 C520 318 340 334 205 322 C150 318 118 306 100 292 L72 302 C54 304 44 292 50 282 L78 268 C52 248 40 218 40 186 Z';
	const flukes = 'M880 206 C918 166 950 118 1000 96 C986 158 974 194 994 216 C974 238 986 274 1000 334 C950 314 918 266 880 228 Z';
	const flipper = 'M300 300 C318 350 356 384 404 392 C386 352 372 322 362 300 Z';
	const jaw = 'M86 288 C150 300 260 304 352 300 C260 318 160 318 96 306 Z';
	const r = rng(11);
	const wrinkles = Array.from({length: 14}, (_, i) => {
		const x = 380 + i * 34 + r() * 10;
		const yTop = 90 + i * 6 + r() * 10;
		const pts = bezier([x, yTop], [x + 12, yTop + 50], [x - 10, yTop + 110], [x + 6, yTop + 150 - i * 3], 16);
		return <path key={i} d={taper(pts, 1, 4, 3)} fill="#fff" opacity={0.55} />;
	});
	const teeth = Array.from({length: 9}, (_, i) => {
		const x = 110 + i * 24;
		return <path key={i} d={`M${x} 292 l6 -14 l6 14 Z`} fill="#fff" opacity={0.9} />;
	});
	return (
		<Box {...p} vb={WHALE_VB}>
			<Engraved id={`${id}-f`} fx={p.fx} d={flukes} light={{x1: 0.2, y1: 0, x2: 0.8, y2: 1}} />
			<Engraved id={`${id}-b`} fx={p.fx} d={body} light={{x1: 0.3, y1: 0, x2: 0.45, y2: 1}} strength={1.05} />
			{wrinkles}
			{teeth}
			<Engraved id={`${id}-j`} fx={p.fx} d={jaw} rim={2} strength={0.7} />
			<Engraved id={`${id}-fl`} fx={p.fx} d={flipper} light={{x1: 0, y1: 0, x2: 1, y2: 1}} rim={2.5} />
			{/* blowhole + forehead highlight */}
			<path d="M70 92 C120 64 200 58 260 60" fill="none" stroke="#fff" strokeWidth={5} strokeLinecap="round" opacity={0.85} />
			<ellipse cx={58} cy={110} rx={8} ry={4} fill="#000" stroke="#fff" strokeWidth={2} />
			{/* eye */}
			<ellipse cx={WHALE_EYE[0]} cy={WHALE_EYE[1]} rx={15} ry={11} fill="#000" stroke="#fff" strokeWidth={3} />
			<circle cx={WHALE_EYE[0] + 4} cy={WHALE_EYE[1] - 3} r={4} fill="#fff" />
			<path d={`M${WHALE_EYE[0] - 26} ${WHALE_EYE[1] - 16} C${WHALE_EYE[0]} ${WHALE_EYE[1] - 28} ${WHALE_EYE[0] + 26} ${WHALE_EYE[1] - 20} ${WHALE_EYE[0] + 34} ${WHALE_EYE[1] - 8}`} fill="none" stroke="#fff" strokeWidth={3} opacity={0.8} />
			{/* scars */}
			{Array.from({length: 6}, (_, i) => (
				<path
					key={i}
					d={`M${150 + i * 50} ${120 + (i % 3) * 30} q ${30} ${-6} ${60} ${8}`}
					fill="none"
					stroke="#fff"
					strokeWidth={2.5}
					opacity={0.6}
				/>
			))}
		</Box>
	);
};

// ----------------------------------------------------------------- colossal squid (eye close-up friendly)

export const SQUID_VB = '0 0 1000 1000';
export const SQUID_EYE: Pt = [470, 560];

export const ColossalSquid: React.FC<BoxProps> = (p) => {
	const id = p.id;
	const mantle = 'M560 520 C520 420 560 230 700 90 C760 30 830 20 860 60 C900 120 860 260 790 380 C730 480 660 560 600 600 Z';
	const fin = 'M760 70 C820 -10 960 -20 990 40 C940 60 900 110 860 170 C840 120 800 90 760 70 Z';
	const head = 'M380 520 C390 460 470 430 560 450 C640 470 660 540 640 610 C620 680 540 720 460 700 C390 680 370 590 380 520 Z';
	// arms: tapered curling strokes going down-left
	const r = rng(5);
	const arms = Array.from({length: 9}, (_, i) => {
		const sx = 420 + i * 22;
		const sy = 650 + (i % 3) * 14;
		const ex = -40 + i * 70 + r() * 40;
		const ey = 980 + r() * 60 - (i % 2) * 90;
		const pts = bezier([sx, sy], [sx - 60 - i * 10, sy + 160], [ex + 220 - i * 18, ey - 230 + r() * 80], [ex, ey], 40);
		return (
			<Engraved
				key={i}
				id={`${id}-a${i}`}
				fx={p.fx}
				d={taper(pts, 58 - i * 2, 6, 18)}
				light={{x1: 1, y1: 0, x2: 0, y2: 1}}
				rim={2}
				cross={false}
			/>
		);
	});
	// suckers along two arms
	const suckers = [2, 5].flatMap((ai) => {
		const rr = rng(ai + 40);
		return Array.from({length: 8}, (_, k) => {
			const cx = 330 - ai * 30 + k * 18 + rr() * 6;
			const cy = 760 + k * 22;
			return <circle key={`${ai}-${k}`} cx={cx} cy={cy} r={7 - k * 0.5} fill="#000" stroke="#fff" strokeWidth={2} />;
		});
	});
	const [ex, ey] = SQUID_EYE;
	return (
		<Box {...p} vb={SQUID_VB}>
			<Engraved id={`${id}-fin`} fx={p.fx} d={fin} light={{x1: 0, y1: 0, x2: 1, y2: 1}} />
			<Engraved id={`${id}-m`} fx={p.fx} d={mantle} light={{x1: 0.1, y1: 0.2, x2: 0.9, y2: 0.8}} strength={1.1} />
			{arms}
			<Engraved id={`${id}-h`} fx={p.fx} d={head} light={{x1: 0.2, y1: 0, x2: 0.8, y2: 1}} />
			{suckers}
			{/* the eye: big, glossy, staring */}
			<circle cx={ex} cy={ey} r={98} fill="#000" stroke="#fff" strokeWidth={6} />
			{Array.from({length: 36}, (_, i) => {
				const a = (i / 36) * Math.PI * 2;
				return (
					<line
						key={i}
						x1={ex + Math.cos(a) * 52}
						y1={ey + Math.sin(a) * 52}
						x2={ex + Math.cos(a) * 88}
						y2={ey + Math.sin(a) * 88}
						stroke="#fff"
						strokeWidth={2.4}
						opacity={0.75}
					/>
				);
			})}
			<circle cx={ex} cy={ey} r={50} fill="#000" />
			<circle cx={ex - 26} cy={ey - 30} r={20} fill="#fff" />
			<circle cx={ex + 28} cy={ey + 24} r={7} fill="#fff" opacity={0.8} />
			<path d={`M${ex - 120} ${ey - 40} C${ex - 80} ${ey - 140} ${ex + 80} ${ey - 150} ${ex + 130} ${ey - 50}`} fill="none" stroke="#fff" strokeWidth={5} opacity={0.8} />
		</Box>
	);
};

// ----------------------------------------------------------------- anglerfish (huge, mostly darkness + lure)

export const ANGLER_VB = '0 0 1000 800';
/** Lure bulb (glows) in viewBox units. */
export const ANGLER_LURE: Pt = [250, 70];
export const ANGLER_EYE: Pt = [420, 330];

export const Anglerfish: React.FC<BoxProps & {glow?: boolean}> = (p) => {
	const id = p.id;
	const body =
		'M180 420 C180 260 300 170 470 170 C680 170 830 260 900 380 C930 430 960 440 1000 420 C990 470 990 520 1000 580 C960 560 930 570 900 610 C820 700 650 740 470 730 C320 720 220 640 196 560 Z';
	const jaw = 'M180 470 C230 560 320 640 470 660 C560 670 620 650 650 620 C560 600 420 590 300 540 C240 515 200 490 180 470 Z';
	const r = rng(9);
	const fang = (x: number, y: number, len: number, dir: 1 | -1, lean: number, w: number, i: string) => {
		const pts = bezier([x, y], [x + lean * 0.2, y + dir * len * 0.4], [x + lean * 0.8, y + dir * len * 0.8], [x + lean, y + dir * len], 12);
		return <path key={i} d={taper(pts, w, 1.5)} fill="#f4f4f4" stroke="#000" strokeWidth={2} />;
	};
	// upper jaw edge runs (190,455) -> (560,560); lower lip (210,500) -> (620,615)
	const teethTop = Array.from({length: 10}, (_, i) => {
		const t = i / 9;
		const len = 50 + r() * 70 + (i % 3 === 1 ? 40 : 0);
		return fang(200 + t * 360, 462 + t * 96, len, 1, 14 + r() * 16, 14 + r() * 6, `t${i}`);
	});
	const teethBot = Array.from({length: 9}, (_, i) => {
		const t = i / 8;
		const len = 40 + r() * 60 + (i % 3 === 0 ? 36 : 0);
		return fang(230 + t * 380, 590 + t * 40, len, -1, -10 - r() * 14, 13 + r() * 6, `b${i}`);
	});
	const stalk = bezier([430, 190], [400, 40], [300, 10], ANGLER_LURE, 30);
	const [lx, ly] = ANGLER_LURE;
	return (
		<Box {...p} vb={ANGLER_VB}>
			<defs>
				<radialGradient id={`${id}-glow`}>
					<stop offset="0" stopColor="#fff" stopOpacity={1} />
					<stop offset="0.25" stopColor="#e9fbff" stopOpacity={0.6} />
					<stop offset="1" stopColor="#bff4ff" stopOpacity={0} />
				</radialGradient>
			</defs>
			<Engraved id={`${id}-b`} fx={p.fx} d={body} light={{x1: 0.15, y1: 0.05, x2: 0.7, y2: 1}} strength={0.75} rim={2.5} />
			<path d="M520 300 C600 250 700 280 760 340" fill="none" stroke="#fff" strokeWidth={3} opacity={0.5} />
			<path d="M190 455 C300 500 440 545 600 560 C560 600 420 610 300 560 C240 530 205 495 190 455 Z" fill="#000" />
			<Engraved id={`${id}-j`} fx={p.fx} d={jaw} light={{x1: 0, y1: 0, x2: 1, y2: 1}} strength={0.6} rim={2} />
			{teethTop}
			{teethBot}
			<path d={taper(stalk, 14, 5)} fill="#ddd" />
			<circle cx={ANGLER_EYE[0]} cy={ANGLER_EYE[1]} r={22} fill="#000" stroke="#fff" strokeWidth={4} />
			<circle cx={ANGLER_EYE[0] - 6} cy={ANGLER_EYE[1] - 6} r={6} fill="#fff" />
			{p.glow !== false && <circle cx={lx} cy={ly} r={160} fill={`url(#${id}-glow)`} />}
			<circle cx={lx} cy={ly} r={22} fill="#fff" />
		</Box>
	);
};

export const SUBJECTS = ['whale', 'squid', 'angler'] as const;
