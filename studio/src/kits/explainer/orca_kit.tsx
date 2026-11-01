/**
 * Extra explainer-kit pieces added for the orca pilot fix round (reusable in any episode):
 *
 *   orca poses     ORCA_POSES.top (top-down, flukes sway sideways) and .head (head-on, flippers flap),
 *                  used via explainer/Orca props.pose = "top" | "head"
 *   figures        seal (harbour seal, 1.6 m), liver (organ icon, ~0.6 m)
 *   component      explainer/Sailboat: side view across the waterline (hull, mast, sails above; keel and
 *                  rudder below). props: snapAt (rudder snaps off and sinks), hits [t] (hull jolts),
 *                  list (deg, number or track: roll toward the viewer), sink (px, number or track), bob,
 *                  waterline (0..1 of the box height, default 0.5), hullColor, bottomColor, sailColor.
 *
 * All drawings are original code-drawn SVG. Figures face RIGHT like the rest of the kit.
 */
import React from 'react';
import type {KitComponent} from '../../core/registry';
import {paint, type DrawCtx, type Figure} from './figure';
import {arr, clamp, easeIn, easeOut, num, str, swimWarp, track, warp} from './util';

// ---------------------------------------------------------------- orca, top-down

const OT_BODY =
	'M 990 200 C 990 162 934 136 862 128 C 722 116 522 122 382 142 C 282 156 202 180 142 193 L 142 207 C 202 220 282 244 382 258 C 522 278 722 284 862 272 C 934 264 990 238 990 200 Z';
const OT_FLUKE = 'M 168 200 C 126 182 84 132 32 104 C 44 142 62 176 72 200 C 62 224 44 258 32 296 C 84 268 126 218 168 200 Z';
const OT_PEC_L = 'M 770 142 C 752 96 712 58 660 46 C 648 74 668 112 708 142 Z';
const OT_PEC_R = 'M 770 258 C 752 304 712 342 660 354 C 648 326 668 288 708 258 Z';
const OT_DORSAL = 'M 650 200 C 610 192 548 192 500 200 C 548 208 610 208 650 200 Z';
const OT_SADDLE = 'M 528 172 C 474 166 424 178 404 200 C 424 222 474 234 528 228 C 506 212 506 188 528 172 Z';
const OT_PATCH_L = 'M 904 156 C 874 144 834 142 812 150 C 832 160 872 162 904 156 Z';
const OT_PATCH_R = 'M 904 244 C 874 256 834 258 812 250 C 832 240 872 238 904 244 Z';

const orcaTop: Omit<Figure, 'poses' | 'label'> = {
	box: [30, 44, 962, 312],
	size: 8,
	axis: 'w',
	draw: (c: DrawCtx) => {
		// seen from above the tail beat is a sideways sway (same travelling wave, y = lateral)
		const f = c.idle ? swimWarp({head: 990, tail: 30, amp: 16 * c.amp, t: c.t, freq: 0.6 * c.speed}) : undefined;
		const fl = c.idle ? Math.sin(c.t * Math.PI * 2 * 0.6 * c.speed) * 4 : 0;
		return (
			<g>
				<path d={warp(OT_FLUKE, f)} fill={paint(c, '#121518')} />
				<g transform={`rotate(${fl} 740 142)`}>
					<path d={warp(OT_PEC_L, f)} fill={paint(c, '#101316')} />
				</g>
				<g transform={`rotate(${-fl} 740 258)`}>
					<path d={warp(OT_PEC_R, f)} fill={paint(c, '#101316')} />
				</g>
				<path d={warp(OT_BODY, f)} fill={paint(c, '#191c20')} />
				{c.sil ? null : <path d={warp(OT_SADDLE, f)} fill="#8b9399" opacity={0.6} />}
				{c.sil ? null : <path d={warp(OT_DORSAL, f)} fill="#2c3238" />}
				{c.sil ? null : <path d={warp(OT_PATCH_L, f)} fill="#eef2f3" />}
				{c.sil ? null : <path d={warp(OT_PATCH_R, f)} fill="#eef2f3" />}
				{c.sil ? null : <path d={warp('M 960 200 C 930 196 900 196 880 200', f)} stroke="#2f353b" strokeWidth={3} fill="none" opacity={0.6} />}
			</g>
		);
	},
};

// ---------------------------------------------------------------- orca, head-on

const orcaHead: Omit<Figure, 'poses' | 'label'> = {
	box: [10, 30, 580, 520],
	size: 3.4, // flipper tip to flipper tip
	axis: 'w',
	draw: (c: DrawCtx) => {
		const fl = c.idle ? Math.sin(c.t * Math.PI * 2 * 0.45 * c.speed) * 6 * c.amp : 0;
		const br = c.idle ? 1 + Math.sin(c.t * Math.PI * 2 * 0.3 * c.speed) * 0.012 : 1;
		const id = `${c.id}-hd`;
		return (
			<g transform={`translate(300 340) scale(${br}) translate(-300 -340)`}>
				<defs>
					<clipPath id={id}>
						<ellipse cx={300} cy={340} rx={152} ry={136} />
					</clipPath>
				</defs>
				<g transform={`rotate(${-fl} 190 420)`}>
					<path d="M 196 404 C 140 432 72 474 20 534 C 82 536 150 494 204 446 Z" fill={paint(c, '#101316')} />
				</g>
				<g transform={`rotate(${fl} 410 420)`}>
					<path d="M 404 404 C 460 432 528 474 580 534 C 518 536 450 494 396 446 Z" fill={paint(c, '#101316')} />
				</g>
				<path d="M 282 222 C 290 160 296 90 300 34 C 304 90 310 160 318 222 Z" fill={paint(c, '#15181b')} />
				<ellipse cx={300} cy={340} rx={152} ry={136} fill={paint(c, '#191c20')} />
				<g clipPath={`url(#${id})`}>
					{c.sil ? null : <ellipse cx={300} cy={452} rx={118} ry={84} fill="#eef2f3" />}
					{c.sil ? null : <ellipse cx={300} cy={262} rx={70} ry={26} fill="#2a2f35" opacity={0.6} />}
				</g>
				{c.sil ? null : (
					<g fill="#eef2f3">
						<ellipse cx={214} cy={302} rx={38} ry={17} transform="rotate(-24 214 302)" />
						<ellipse cx={386} cy={302} rx={38} ry={17} transform="rotate(24 386 302)" />
					</g>
				)}
				{c.sil ? null : (
					<g>
						<circle cx={236} cy={336} r={6} fill="#000" />
						<circle cx={364} cy={336} r={6} fill="#000" />
						<path d="M 214 392 Q 300 420 386 392" stroke="#000" strokeWidth={4} fill="none" opacity={0.5} strokeLinecap="round" />
					</g>
				)}
			</g>
		);
	},
};

export const ORCA_POSES: Record<string, Omit<Figure, 'poses' | 'label'>> = {top: orcaTop, head: orcaHead};

// ---------------------------------------------------------------- harbour seal

const SE_BODY =
	'M 22 92 C 44 62 122 44 222 46 C 300 48 348 54 374 68 C 394 78 396 98 374 106 C 332 118 250 120 160 114 C 92 110 42 106 22 92 Z';

const seal: Figure = {
	label: 'SEAL',
	box: [0, 40, 400, 96],
	size: 1.6,
	axis: 'w',
	draw: (c) => {
		const f = c.idle ? swimWarp({head: 396, tail: 0, amp: 5 * c.amp, t: c.t, freq: 0.7 * c.speed}) : undefined;
		const id = `${c.id}-se`;
		return (
			<g>
				<defs>
					<clipPath id={id}>
						<path d={warp(SE_BODY, f)} />
					</clipPath>
				</defs>
				<path d={warp('M 34 90 L 0 66 L 10 92 L 0 120 Z', f)} fill={paint(c, '#5f6c72')} />
				<path d={warp(SE_BODY, f)} fill={paint(c, '#7c898f')} />
				<g clipPath={`url(#${id})`}>
					{c.sil ? null : <path d={warp('M 0 100 C 120 96 260 98 400 92 L 400 140 L 0 140 Z', f)} fill="#b8c2c6" />}
					{c.sil
						? null
						: [
								[110, 70],
								[150, 62],
								[196, 74],
								[236, 60],
								[270, 80],
								[90, 86],
							].map(([x, y], i) => <circle key={i} cx={f ? f(x, y)[0] : x} cy={f ? f(x, y)[1] : y} r={5} fill="#5a666c" opacity={0.6} />)}
				</g>
				<path d={warp('M 292 106 C 286 122 272 130 256 132 C 262 120 268 112 270 104 Z', f)} fill={paint(c, '#5f6c72')} />
				{c.sil ? null : (
					<g>
						<circle cx={f ? f(358, 72)[0] : 358} cy={f ? f(358, 72)[1] : 72} r={6} fill="#0b0d10" />
						<circle cx={f ? f(390, 86)[0] : 390} cy={f ? f(390, 86)[1] : 86} r={4} fill="#20262a" />
					</g>
				)}
			</g>
		);
	},
};

// ---------------------------------------------------------------- liver (organ icon)

const liver: Figure = {
	label: 'LIVER',
	box: [8, 4, 300, 158],
	size: 0.6,
	axis: 'w',
	draw: (c) => (
		<g>
			<path d="M 20 62 C 28 22 118 6 218 14 C 280 20 304 40 294 72 C 282 112 202 142 122 152 C 70 158 28 124 20 62 Z" fill={paint(c, '#9c2f2a')} />
			{c.sil ? null : <path d="M 160 18 C 150 60 150 100 168 146" stroke="#6e1d1a" strokeWidth={6} fill="none" opacity={0.6} strokeLinecap="round" />}
			{c.sil ? null : <path d="M 52 54 C 70 36 110 28 140 30" stroke="#e07a6f" strokeWidth={9} fill="none" opacity={0.7} strokeLinecap="round" />}
		</g>
	),
};

export const ORCA_KIT_FIGURES: Record<string, Figure> = {seal, liver};

// ---------------------------------------------------------------- sailboat across the waterline

/**
 * explainer/Sailboat. Drawn in a 600 x 900 unit box, waterline at `waterline` (default 0.5) of the height; place
 * the layer so that line sits on the Ocean surface (same layer depth as the background keeps them locked).
 */
export const Sailboat: KitComponent = ({props, time, width: W, height: H}) => {
	const wl = num(props.waterline, 0.5) * 900;
	const snapAt = typeof props.snapAt === 'number' ? props.snapAt : null;
	const list = track(props.list, time, 0);
	const sink = track(props.sink, time, 0);
	const bob = num(props.bob, 1) * Math.sin(time * Math.PI * 2 * 0.35) * 6;
	const roll = num(props.bob, 1) * Math.sin(time * Math.PI * 2 * 0.27 + 1) * 1.5;
	let jolt = 0;
	for (const h of arr<number>(props.hits)) {
		const p = time - h;
		if (p >= 0 && p < 0.5) jolt += Math.sin(p * 60) * 9 * (1 - p / 0.5);
	}
	const hull = str(props.hullColor, '#e9eef0');
	const bottom = str(props.bottomColor, '#2b3440');
	const sail = str(props.sailColor, '#f4f1ea');
	// rudder: pivot at its stock under the stern; after snapAt it swings back, then tumbles down and fades
	const rx = 112;
	const ry = wl + 34;
	let rRot = 0;
	let rDy = 0;
	let rDx = 0;
	let rOp = 1;
	if (snapAt !== null && time >= snapAt) {
		const p = time - snapAt;
		rRot = 70 * easeOut(clamp(p / 0.25)) + 40 * clamp((p - 0.25) / 1.5);
		rDy = 180 * easeIn(clamp((p - 0.15) / 1.4)) + 40 * p;
		rDx = -60 * easeOut(clamp(p / 0.6));
		rOp = 1 - clamp((p - 1.2) / 0.8);
	}
	const crack = snapAt !== null && time >= snapAt && time < snapAt + 0.18;
	return (
		<svg viewBox="0 0 600 900" width={W} height={H} style={{overflow: 'visible', display: 'block'}}>
			<g transform={`translate(${jolt} ${bob + sink}) rotate(${list + roll} 300 ${wl})`}>
				{/* mast + sails */}
				<rect x={296} y={60} width={9} height={wl - 70} fill="#c8cfd3" />
				<path d={`M 292 76 L 292 ${wl - 46} L 132 ${wl - 46} Z`} fill={sail} />
				<path d={`M 312 92 L 312 ${wl - 42} L 470 ${wl - 42} Z`} fill={sail} opacity={0.92} />
				<path d={`M 292 76 L 292 ${wl - 46} L 132 ${wl - 46} Z`} fill="none" stroke="#c9c2b4" strokeWidth={3} />
				<rect x={128} y={wl - 48} width={168} height={7} rx={3} fill="#9aa3a9" />
				{/* keel fin + bulb */}
				<path d={`M 270 ${wl + 50} L 336 ${wl + 50} L 322 ${wl + 230} L 286 ${wl + 230} Z`} fill={bottom} />
				<ellipse cx={304} cy={wl + 238} rx={46} ry={16} fill={bottom} />
				{/* rudder (snaps) */}
				<g opacity={rOp} transform={`translate(${rDx} ${rDy}) rotate(${rRot} ${rx} ${ry})`}>
					<rect x={rx - 3} y={ry - 10} width={6} height={22} fill="#59626a" />
					<path d={`M ${rx - 14} ${ry + 8} L ${rx + 16} ${ry + 8} L ${rx + 8} ${ry + 132} L ${rx - 20} ${ry + 120} Z`} fill={bottom} stroke="#465260" strokeWidth={3} />
				</g>
				{crack ? <path d={`M ${rx - 30} ${ry} L ${rx + 26} ${ry - 10} M ${rx - 22} ${ry + 18} L ${rx + 30} ${ry + 14}`} stroke="#ffffff" strokeWidth={6} strokeLinecap="round" /> : null}
				{/* hull: topsides above the waterline, antifouling below */}
				<path d={`M 60 ${wl - 40} L 540 ${wl - 40} C 520 ${wl + 10} 480 ${wl + 44} 400 ${wl + 54} L 150 ${wl + 54} C 110 ${wl + 48} 86 ${wl + 30} 74 ${wl} Z`} fill={hull} />
				<path d={`M 72 ${wl} L 528 ${wl} C 506 ${wl + 30} 470 ${wl + 48} 400 ${wl + 56} L 150 ${wl + 56} C 112 ${wl + 50} 88 ${wl + 30} 72 ${wl} Z`} fill={bottom} />
				<rect x={66} y={wl - 18} width={468} height={7} fill="#3a8fd6" opacity={0.85} />
				<rect x={210} y={wl - 64} width={130} height={24} rx={6} fill="#dfe5e8" />
			</g>
		</svg>
	);
};

