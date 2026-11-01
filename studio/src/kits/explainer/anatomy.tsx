/**
 * Body-part and everyday-object figures for "X is the size of Y" rungs, plus two small
 * infographics built on them. Same flat-vector style as marine.tsx (muted fills, soft
 * gradients, light texture); everything faces RIGHT and has a true real-world size.
 *
 * figures      whaleHeart (1.5 m) whaleTongue (3 m slab) whaleThroat (3 m close-up of the back
 *              of the mouth, throat ring ~0.34 m) golfCart (2.4 m) sauropod (30 m) jet (38 m) krill (6 cm)
 * components   explainer/Balance, explainer/ECG live in balance.tsx
 */
import React from 'react';
import {paint, type DrawCtx, type Figure} from './figure';
import {num, rnd, str} from './util';

const Lin: React.FC<{id: string; a: string; b: string; h?: boolean}> = ({id, a, b, h}) => (
	<linearGradient id={id} x1="0" y1="0" x2={h ? '1' : '0'} y2={h ? '0' : '1'}>
		<stop offset="0" stopColor={a} />
		<stop offset="1" stopColor={b} />
	</linearGradient>
);

const speckle = (c: DrawCtx, key: string, n: number, x0: number, y0: number, w: number, h: number, color: string, op = 0.22) =>
	c.sil
		? null
		: Array.from({length: n}, (_, i) => (
				<ellipse
					key={`${key}${i}`}
					cx={x0 + rnd(`${key}x${i}`) * w}
					cy={y0 + rnd(`${key}y${i}`) * h}
					rx={3 + rnd(`${key}r${i}`) * 7}
					ry={2 + rnd(`${key}q${i}`) * 4}
					fill={color}
					opacity={op}
				/>
		  ));

// ================================================================ whale heart (~1.5 m, ~180 kg)

const whaleHeart: Figure = {
	label: 'WHALE HEART',
	box: [40, 20, 520, 560],
	size: 1.5,
	axis: 'h',
	draw: (c) => {
		const beat = num(c.p.beat, 0); // 0..1 squeeze, driven by the storyboard
		const s = 1 - 0.05 * beat;
		return (
			<g transform={`translate(300 330) scale(${s}) translate(-300 -330)`}>
				<defs>
					<Lin id={`${c.id}-h`} a={paint(c, '#8a4652')} b={paint(c, '#5b2a35')} />
					<clipPath id={`${c.id}-hc`}>
						<path d="M 120 250 C 100 170 170 130 250 150 C 300 120 400 120 450 180 C 520 260 500 380 420 470 C 370 525 320 575 290 575 C 250 570 180 500 140 420 C 110 360 125 300 120 250 Z" />
					</clipPath>
				</defs>
				{/* great vessels: aorta arch + pulmonary trunk, grey-pink */}
				<path d="M 300 160 C 290 100 300 50 350 36 C 410 22 470 50 480 110 L 440 118 C 432 84 405 68 372 74 C 342 80 336 120 340 165 Z" fill={paint(c, '#b98a8f')} />
				<path d="M 372 74 L 366 24 L 392 22 L 398 72 Z M 410 76 L 420 30 L 444 36 L 432 84 Z" fill={paint(c, '#a77b80')} />
				<path d="M 220 170 C 200 120 180 92 150 80 L 160 56 C 204 70 240 110 262 160 Z" fill={paint(c, '#9c7a86')} />
				<path d="M 120 250 C 100 170 170 130 250 150 C 300 120 400 120 450 180 C 520 260 500 380 420 470 C 370 525 320 575 290 575 C 250 570 180 500 140 420 C 110 360 125 300 120 250 Z" fill={`url(#${c.id}-h)`} />
				<g clipPath={`url(#${c.id}-hc)`}>
					{speckle(c, 'hrt', 26, 140, 170, 340, 380, '#c78690', 0.25)}
					{c.sil ? null : <path d="M 120 210 C 220 200 330 196 470 230 L 470 190 C 330 160 220 170 120 180 Z" fill="#e8d6c8" opacity={0.55} />}
					{c.sil ? null : <path d="M 300 200 C 280 300 290 420 300 575" stroke="#41202a" strokeWidth={9} fill="none" opacity={0.6} />}
					{c.sil ? null : <path d="M 300 230 C 330 300 380 360 440 400" stroke="#7a3b47" strokeWidth={6} fill="none" opacity={0.5} />}
				</g>
			</g>
		);
	},
};

// ================================================================ whale tongue (~2.7 t slab)

const whaleTongue: Figure = {
	label: 'TONGUE',
	box: [10, 40, 980, 300],
	size: 3,
	axis: 'w',
	draw: (c) => (
		<g>
			<defs>
				<Lin id={`${c.id}-t`} a={paint(c, '#d28c93')} b={paint(c, '#9c5a64')} />
			</defs>
			<path d="M 20 300 C 10 200 60 120 200 90 C 380 50 640 40 840 70 C 930 84 990 140 984 220 C 980 280 940 330 860 336 L 60 336 C 34 336 22 320 20 300 Z" fill={`url(#${c.id}-t)`} />
			{c.sil ? null : <path d="M 120 120 C 360 76 640 70 900 110" stroke="#e7aab0" strokeWidth={10} fill="none" opacity={0.6} strokeLinecap="round" />}
			{c.sil ? null : <path d="M 500 70 C 500 160 498 240 500 330" stroke="#8a4b55" strokeWidth={5} fill="none" opacity={0.45} />}
			{speckle(c, 'tng', 40, 60, 90, 880, 230, '#f0c0c4', 0.3)}
		</g>
	),
};

// ================================================================ whale throat close-up (back of the mouth, 3 m across)

/** Ring centre in drawing units (for placing a diver against it): x 230, y 470, diameter 0.34 m = 113 units. */
const TH_RING = {x: 230, y: 470, rx: 40, ry: 57};

const whaleThroat: Figure = {
	label: 'THROAT',
	box: [0, 0, 1000, 1000],
	size: 3,
	axis: 'w',
	draw: (c) => {
		const glow = num(c.p.glow, 0); // 0..1 rim highlight
		// bleed (figure units, default 0): walls, baleen row and tongue floor continue this far past every edge, so a
		// landscape cut can run the set edge to edge (QA 16:9: a 1014 px panel with hard seams in a 1920 frame)
		const B = Math.max(0, num(c.p.bleed, 0));
		const {x, y, rx, ry} = TH_RING;
		return (
			<g>
				<defs>
					<radialGradient id={`${c.id}-cv`} gradientUnits="userSpaceOnUse" cx="250" cy="470" r="900">
						<stop offset="0" stopColor={paint(c, '#140709')} />
						<stop offset="0.25" stopColor={paint(c, '#3a1822')} />
						<stop offset="1" stopColor={paint(c, '#5a2a36')} />
					</radialGradient>
					{/* daylight from the open mouth: peaks inside the art and fades out at the edge (no seam on a full-bleed set) */}
					<linearGradient id={`${c.id}-mo`} x1="0" y1="0" x2="1" y2="0">
						<stop offset="0" stopColor="rgba(80,150,180,0)" />
						<stop offset="0.6" stopColor="rgba(80,150,180,0.16)" />
						<stop offset="1" stopColor="rgba(80,150,180,0)" />
					</linearGradient>
					<Lin id={`${c.id}-tg`} a={paint(c, '#c47f88')} b={paint(c, '#93525d')} />
				</defs>
				<rect x={-B} y={-B} width={1000 + 2 * B} height={1000 + 2 * B} fill={`url(#${c.id}-cv)`} />
				{/* perspective folds converging on the throat */}
				{c.sil
					? null
					: [
							[0, 120],
							[1000, 160],
							[1000, 840],
							[0, 900],
							[560, 0],
							[600, 1000],
					  ].map(([ex, ey], i) => <path key={i} d={`M ${x} ${y} Q ${(x + ex) / 2 + 40} ${(y + ey) / 2} ${ex} ${ey}`} stroke="#6e3542" strokeWidth={14} fill="none" opacity={0.35} />)}
				{/* palate + baleen fringe across the top */}
				<path d={`M ${-B} ${-B} L ${1000 + B} ${-B} L ${1000 + B} 170 L 1000 170 C 760 150 420 170 0 210 L ${-B} ${210 + B * 0.04} Z`} fill={paint(c, '#4a2430')} />
				{c.sil
					? null
					: Array.from({length: 46 + 2 * Math.ceil(B / 22)}, (_, i) => {
							const bx = 10 + (i - Math.ceil(B / 22)) * 22;
							const top = 210 - (bx / 1000) * 40;
							const len = 70 + 40 * Math.sin((i / 45) * Math.PI) + rnd(`bl${i}`) * 20;
							return <path key={i} d={`M ${bx} ${top - 6} L ${bx - 6} ${top + len}`} stroke={i % 3 ? '#1b1d21' : '#4a4038'} strokeWidth={9} strokeLinecap="round" opacity={0.95} />;
					  })}
				{/* tongue floor */}
				<path d={`M ${-B} 760 L 0 760 C 200 700 420 690 640 700 C 820 708 940 730 1000 760 L ${1000 + B} 760 L ${1000 + B} ${1000 + B} L ${-B} ${1000 + B} Z`} fill={`url(#${c.id}-tg)`} />
				{speckle(c, 'thf', 30, 20, 730, 960, 250, '#e9b2b8', 0.28)}
				{/* daylight from the open mouth on the right (prop daylight: 0..1, default 0; a band reads as a seam full-bleed) */}
				{num(c.p.daylight, 0) > 0 ? <rect x={440} y={0} width={560} height={1000} fill={`url(#${c.id}-mo)`} opacity={num(c.p.daylight, 0)} /> : null}
				{/* the throat opening */}
				<ellipse cx={x} cy={y} rx={rx + 26} ry={ry + 30} fill={paint(c, '#7b3d4a')} opacity={0.9} />
				<ellipse cx={x} cy={y} rx={rx} ry={ry} fill={paint(c, '#050203')} />
				{c.sil ? null : <ellipse cx={x} cy={y} rx={rx + 8} ry={ry + 8} fill="none" stroke="#e6a4ac" strokeWidth={10 + 6 * glow} opacity={0.75 + 0.25 * glow} />}
			</g>
		);
	},
};

// ================================================================ golf cart (~2.4 m)

const golfCart: Figure = {
	label: 'GOLF CART',
	box: [0, 0, 960, 760],
	size: 2.4,
	axis: 'w',
	draw: (c) => {
		const body = paint(c, str(c.p.color, '#e9ece6'));
		const dk = paint(c, '#2a3036');
		const wheel = (cx: number) => (
			<g key={cx}>
				<circle cx={cx} cy={660} r={100} fill={paint(c, '#15191d')} />
				{c.sil ? null : <circle cx={cx} cy={660} r={48} fill="#a6aeb3" />}
				{c.sil ? null : <circle cx={cx} cy={660} r={16} fill="#4b545a" />}
			</g>
		);
		return (
			<g>
				{/* canopy roof on two posts */}
				<rect x={120} y={10} width={680} height={46} rx={20} fill={body} />
				<rect x={170} y={50} width={22} height={360} fill={dk} />
				<rect x={690} y={50} width={22} height={300} fill={dk} transform="rotate(8 700 50)" />
				{/* seat */}
				<rect x={150} y={340} width={300} height={70} rx={24} fill={paint(c, '#3c4650')} />
				<rect x={150} y={250} width={70} height={140} rx={24} fill={paint(c, '#3c4650')} />
				{/* steering wheel */}
				<path d="M 560 320 L 640 470" stroke={dk} strokeWidth={18} strokeLinecap="round" />
				<ellipse cx={560} cy={316} rx={48} ry={16} fill="none" stroke={dk} strokeWidth={14} transform="rotate(-25 560 316)" />
				{/* body tub + front cowl */}
				<path d="M 40 420 L 620 420 C 700 420 760 380 830 380 C 900 380 940 420 940 480 L 940 600 C 940 620 925 630 905 630 L 60 630 C 40 630 30 616 30 596 L 30 440 C 30 428 34 420 40 420 Z" fill={body} />
				{c.sil ? null : <path d="M 30 560 L 940 560 L 940 600 C 940 620 925 630 905 630 L 60 630 C 40 630 30 616 30 596 Z" fill="#c7ccc4" />}
				{c.sil ? null : <rect x={900} y={450} width={28} height={30} rx={8} fill="#fff6c9" />}
				{c.sil ? null : <rect x={36} y={470} width={180} height={70} rx={10} fill="#d5d9d2" />}
				{wheel(200)}
				{wheel(770)}
			</g>
		);
	},
};

// ================================================================ sauropod silhouette (~30 m)

const sauropod: Figure = {
	label: 'SAUROPOD',
	box: [0, 0, 1000, 400],
	size: 30,
	axis: 'w',
	draw: (c) => {
		const g = paint(c, str(c.p.color, '#56626c'));
		return (
			<g>
				<path
					d="M 0 250 C 120 240 230 220 320 200 C 380 150 470 140 560 160 C 620 120 700 40 800 20 C 860 8 900 14 935 30 C 960 42 990 52 996 66 C 970 76 930 70 900 64 C 840 70 760 130 700 210 C 690 240 680 262 660 280 L 660 396 L 610 396 L 600 300 L 470 300 L 460 396 L 410 396 L 400 290 C 330 285 260 268 200 262 C 130 258 60 258 0 256 Z"
					fill={g}
				/>
				{c.sil ? null : <circle cx={950} cy={42} r={5} fill="#141618" />}
			</g>
		);
	},
};

// ================================================================ airliner (~38 m), side view

const jet: Figure = {
	label: 'JET',
	box: [0, 40, 1000, 260],
	size: 38,
	axis: 'w',
	draw: (c) => {
		const g = paint(c, str(c.p.color, '#d3dbe0'));
		return (
			<g>
				<path d="M 60 170 L 30 60 L 90 60 L 190 150 Z" fill={paint(c, '#aab6be')} />
				<path d="M 40 150 C 200 140 600 132 860 136 C 930 138 985 152 995 172 C 985 192 930 202 860 204 L 120 206 C 80 206 50 190 40 150 Z" fill={g} />
				<path d="M 420 190 L 600 190 L 520 300 L 470 300 Z" fill={paint(c, '#aab6be')} />
				<rect x={470} y={210} width={110} height={44} rx={22} fill={paint(c, '#8c99a2')} />
				{c.sil ? null : Array.from({length: 22}, (_, i) => <rect key={i} x={240 + i * 26} y={152} width={12} height={14} rx={4} fill="#3a4a56" />)}
				{c.sil ? null : <path d="M 900 150 C 930 152 960 160 975 168 L 905 168 Z" fill="#2c3a44" />}
			</g>
		);
	},
};

// ================================================================ krill (~6 cm)

const krill: Figure = {
	label: 'KRILL',
	box: [0, 20, 600, 260],
	size: 0.06,
	axis: 'w',
	draw: (c) => {
		const o = paint(c, '#f08a6a');
		const leg = c.idle ? Math.sin(c.t * 9 * c.speed) * 6 : 0;
		return (
			<g>
				<path d="M 20 140 C 80 100 200 80 330 86 C 450 92 540 110 590 140 C 540 170 450 186 330 190 C 200 192 90 176 20 140 Z" fill={o} opacity={0.92} />
				<path d="M 20 140 L 0 110 L 8 140 L 0 170 Z" fill={o} />
				{c.sil ? null : [0, 1, 2, 3, 4, 5, 6].map((i) => <path key={i} d={`M ${200 + i * 50} 186 l ${-10 + (i % 2 ? leg : -leg)} 60`} stroke="#e37356" strokeWidth={10} strokeLinecap="round" />)}
				{c.sil ? null : <path d="M 560 120 C 600 80 640 50 700 30" stroke="#e37356" strokeWidth={6} fill="none" />}
				{c.sil ? null : <circle cx={540} cy={124} r={16} fill="#111" />}
				{c.sil ? null : [0, 1, 2, 3, 4].map((i) => <path key={i} d={`M ${180 + i * 70} 92 C ${195 + i * 70} 130 ${195 + i * 70} 160 ${180 + i * 70} 188`} stroke="#d0664c" strokeWidth={5} fill="none" opacity={0.6} />)}
			</g>
		);
	},
};

export const ANATOMY: Record<string, Figure> = {whaleHeart, whaleTongue, whaleThroat, golfCart, sauropod, jet, krill};

