/**
 * Sperm whale in house style A (docs/HOUSE_STYLE.md): the hero of explainer-sperm-whale (lane B, 2026-11-02).
 *
 * Look: a few big rounded shapes in flat colour (no gradients, outlines or texture), ONE flat shadow shape on the body
 * (the lower flank, away from the top light), a slate-violet body that reads against both the royal open water and
 * the cyan/violet boards, bone lip line and teeth, a small dark eye with one glint, four long sparse wrinkle shapes.
 * Anatomy (NOAA; art direction experiments/asset-gen/gen/sperm_side_A.png): blunt box head = 1/3 of the body, narrow
 * underslung lower jaw, eye low near the mouth corner, blowhole at the front-left of the head top, a low dorsal hump
 * two thirds back and a row of knuckles to the tail, short paddle flippers, broad horizontal flukes (two lobes seen
 * in slight perspective, like the orca hero).
 *
 * Rig (every point warps; the head never moves, so nothing can tear):
 *   swim   whale-style vertical travelling wave, zero on the head, growing to the flukes
 *   fluke  pitch lags the wave
 *   jaw    0..1 opens the lower jaw about its hinge (22 deg); mouth interior + teeth show in the gap
 *   click  0..1 swells the head front a few px (the "sound machine" beat), drawn by the caller's rings
 *   organ  0..1 shows the spermaceti organ cutaway (amber oil tank inside the head) for the anatomy beat
 *   blink  seeded auto blinks
 *
 * Local space: snout front at x ~ 1632, fluke tips at x ~ 8; 16 m along x (kit Figure contract, facing right).
 */
import React from 'react';
import type {Figure} from '../figure';
import {track} from '../util';
import {useTint} from './light';
import {blinkAt} from './motion';

type P = [number, number];

export const SW_PAL = {
	lit: '#6b6fc4', // slate violet (board indigo + bone, desaturated): reads on royal blue and on cyan
	dark: '#4b4c9e', // its one shadow tone
	wrinkle: '#5a5cb1',
	lip: '#e9f4fc', // bone white
	lipShade: '#bfd3ee',
	mouth: '#5e003f', // board magenta, darkened (as the orca's)
	tongue: '#c62292',
	eye: '#14045c',
	glint: '#ffffff',
	oil: '#fddf35', // sun yellow: the spermaceti organ
	oilDark: '#fc6e0e',
	glow: '#e9f4fc',
};

// ------------------------------------------------------------------ geometry (facing right)
const BODY: P[] = [
	[212, -34], [262, -44], [314, -62], [345, -54], [382, -80], [420, -72], [484, -102], [520, -95], [585, -124],
	[640, -132], [760, -152], [925, -170], [1083, -178], [1300, -182], [1536, -184], [1600, -174], [1630, -142],
	[1640, -60], [1636, 20], [1618, 64], [1582, 96], [1450, 104], [1300, 110], [1140, 138], [970, 172], [800, 168],
	[630, 138], [404, 92], [290, 58], [212, 34],
];
// terminator: the flat shadow is the belly band below this line (clipped to the body)
const TERM: P[] = [[150, 12], [300, 42], [450, 72], [630, 100], [800, 126], [970, 132], [1140, 108], [1300, 92], [1700, 84]];
const UPPER_LOBE: P[] = [[216, -22], [150, -48], [92, -98], [36, -136], [8, -142], [18, -112], [48, -62], [84, -10], [150, -4]];
const LOWER_LOBE: P[] = [[216, 22], [150, 44], [92, 98], [40, 146], [18, 158], [28, 122], [54, 62], [84, 10], [150, 4]];
const FLIPPER: P[] = [[1124, 96], [1156, 112], [1120, 162], [1066, 202], [1018, 210], [1004, 192], [1030, 150], [1080, 106]];
// lower jaw (closed): a narrow rod under the head, hinge at the back
const HINGE: P = [1140, 140];
const JAW: P[] = [[1140, 124], [1300, 108], [1450, 98], [1566, 92], [1580, 106], [1568, 118], [1450, 124], [1300, 132], [1140, 154]];
const JAW_LIP: P[] = [[1150, 128], [1300, 113], [1450, 103], [1566, 96], [1572, 107], [1450, 115], [1300, 124], [1150, 140]];
const WRINKLES: P[][] = [
	[[420, -34], [560, -54], [700, -42], [860, -54]],
	[[520, 8], [660, -6], [800, 4], [940, -2]],
	[[660, 54], [760, 46], [860, 54]],
];
const EYE: P = [1276, 62];
const BLOWHOLE: P[] = [[1570, -168], [1588, -175], [1606, -166]];
const GLINT: P[] = [[1250, -166], [1400, -170], [1520, -168]];
// spermaceti organ (cutaway): the upper part of the head, the oil tank; the junk below it
const ORGAN: P[] = [[1250, -150], [1420, -160], [1570, -150], [1612, -100], [1608, -40], [1540, -20], [1380, -30], [1270, -60], [1240, -110]];
const JUNK: P[] = [[1260, -6], [1420, 0], [1570, 10], [1608, 40], [1570, 72], [1420, 80], [1280, 70], [1250, 32]];
const TEETH = [1330, 1370, 1410, 1450, 1490, 1530];

const smooth = (pts: P[], closed = true): string => {
	// Catmull-Rom -> cubic Bezier (tension 0.5), rounded flat shapes with no corners
	const n = pts.length;
	const at = (i: number) => pts[closed ? (i + n) % n : Math.max(0, Math.min(n - 1, i))];
	let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
	const last = closed ? n : n - 1;
	for (let i = 0; i < last; i++) {
		const p0 = at(i - 1), p1 = at(i), p2 = at(i + 1), p3 = at(i + 2);
		const c1: P = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
		const c2: P = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
		d += ` C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
	}
	return closed ? d + ' Z' : d;
};

const rotAbout = (p: P, c: P, deg: number): P => {
	const a = (deg * Math.PI) / 180;
	const dx = p[0] - c[0], dy = p[1] - c[1];
	return [c[0] + dx * Math.cos(a) - dy * Math.sin(a), c[1] + dx * Math.sin(a) + dy * Math.cos(a)];
};

export type SpermWhaleAProps = {
	id: string;
	t: number;
	amp?: number;
	freq?: number;
	jaw?: number;
	organ?: number;
	click?: number;
	blink?: number;
	silColor?: string;
	pal?: typeof SW_PAL;
};

export const SpermWhaleA: React.FC<SpermWhaleAProps> = ({id, t, amp = 1, freq = 0.4, jaw = 0, organ = 0, click = 0, blink, silColor, pal = SW_PAL}) => {
	const tint = useTint();
	const C = (k: keyof typeof SW_PAL) => (silColor ? silColor : tint(pal[k]));
	const ph = 2 * Math.PI * freq * t;
	const A = 30 * amp;
	// vertical travelling wave: 0 on the head (x >= 1250), growing to the flukes
	const wave = (x: number) => {
		const w = Math.max(0, Math.min(1, (1250 - x) / 1070));
		return A * Math.pow(w, 1.6) * Math.sin(ph - ((1250 - x) / 1070) * 2.4);
	};
	const swell = 6 * Math.max(0, Math.min(1, click));
	const W = ([x, y]: P): P => [x + (x > 1560 ? swell * ((x - 1560) / 80) : 0), y + wave(x)];
	const root: P = [216, 0];
	const slope = (wave(200) - wave(240)) / 40;
	const pitch = (Math.atan(slope) * 180) / Math.PI * 1.4;
	const fluke = (pts: P[]) => pts.map((p) => W(rotAbout(p, root, pitch)) as P).map(([x, y]) => [x, y - wave(x) + wave(216)] as P);
	const body = smooth(BODY.map(W));
	const jawDeg = 22 * Math.max(0, Math.min(1.1, jaw));
	const jawPts = (pts: P[]) => pts.map((p) => rotAbout(p, HINGE, jawDeg));
	const b = blink ?? blinkAt(t, id);
	const clip = `swc-${id}`;
	const term = TERM.map(W);
	const shadow = `${smooth(term, false)} L 1700 400 L 100 400 Z`;
	const sil = !!silColor;
	return (
		<g>
			<defs>
				<clipPath id={clip}>
					<path d={body} />
				</clipPath>
			</defs>
			{/* far lobe, flipper behind the body never shows from this side: lobes, body, shadow, details, jaw, flipper */}
			<path d={smooth(fluke(LOWER_LOBE))} fill={C('dark')} />
			<path d={smooth(fluke(UPPER_LOBE))} fill={C('lit')} />
			{jawDeg > 0.5 && !sil ? (
				<path
					d={smooth([...JAW.slice(0, 4).map(W), ...jawPts(JAW.slice(0, 4)).reverse()])}
					fill={C('mouth')}
				/>
			) : null}
			<path d={body} fill={C('lit')} />
			{!sil ? (
				<g clipPath={`url(#${clip})`}>
					<path d={shadow} fill={C('dark')} />
					{WRINKLES.map((w, i) => (
						<path key={i} d={smooth(w.map(W), false)} stroke={C('wrinkle')} strokeWidth={9} strokeLinecap="round" fill="none" />
					))}
					<path d={smooth(GLINT.map(W), false)} stroke={C('lip')} strokeWidth={7} strokeLinecap="round" fill="none" opacity={0.55} />
					{organ > 0.01 ? (
						<g opacity={Math.min(1, organ * 1.4)}>
							<path d={smooth(ORGAN.map(W))} fill={C('oil')} />
							<path d={smooth(ORGAN.slice(4, 9).concat([[1540, -40]]).map(W))} fill={C('oilDark')} opacity={0.55} />
							<path d={smooth(JUNK.map(W))} fill={C('oilDark')} opacity={0.9} />
						</g>
					) : null}
				</g>
			) : null}
			{!sil ? <path d={smooth(BLOWHOLE.map(W), false)} stroke={C('dark')} strokeWidth={8} strokeLinecap="round" fill="none" /> : null}
			{/* lower jaw: body colour with a bone lip; teeth show only when open */}
			<path d={smooth(jawPts(JAW))} fill={C('lit')} />
			{!sil ? <path d={smooth(jawPts(JAW_LIP))} fill={C('lip')} /> : null}
			{!sil
				? TEETH.map((x, i) => {
						const y = 120 - (x - 1140) * 0.072;
						const h = jawDeg > 2 ? 22 : 13;
						const tri = jawPts([[x - 8, y], [x, y - h], [x + 8, y]]);
						return <path key={i} d={`M ${tri.map((p) => p.map((v) => v.toFixed(1)).join(' ')).join(' L ')} Z`} fill={C('lip')} />;
					})
				: null}
			<path d={smooth(FLIPPER.map(W))} fill={C('lit')} />
			{!sil ? (
				<g>
					<ellipse cx={EYE[0]} cy={EYE[1]} rx={11} ry={11 * (1 - 0.9 * b)} fill={C('eye')} />
					{b < 0.5 ? <circle cx={EYE[0] + 3.5} cy={EYE[1] - 3.5} r={3.4} fill={C('glint')} /> : null}
				</g>
			) : null}
		</g>
	);
};

/** kit Figure: replaces the old grey drawing (creature.tsx FIGURES.spermWhale); the old one stays as pose "flat" */
export const SW_BOX: [number, number, number, number] = [8, -190, 1634, 404];

export const houseSpermWhaleA = (flat: Figure): Figure => ({
	label: 'SPERM WHALE',
	box: SW_BOX,
	size: 16,
	axis: 'w',
	selfShaded: true,
	poses: {...(flat.poses ?? {}), flat: {box: flat.box, size: flat.size, axis: flat.axis, draw: flat.draw}},
	draw: (c) => (
		<SpermWhaleA
			id={c.id}
			t={c.idle ? c.t : 0}
			amp={c.idle ? c.amp : 0}
			freq={0.4 * c.speed}
			jaw={track(c.p.jawOpen, c.t, 0)}
			organ={track(c.p.organ, c.t, 0)}
			click={track(c.p.click, c.t, 0)}
			silColor={c.sil}
		/>
	),
});
