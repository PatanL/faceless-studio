// Light-switch insert (full-frame 9:16 close-up): a wall plate lit by the hallway lamp, Nora's hand reaching in from
// the lower right, the index finger flicking the rocker down at `at`, and the light dying (warm wall -> blue-black,
// the hand and plate go dark with it, only the cool strip of corridor light from under the door remains).
// props: at (flick time, scene seconds, default 0.6), reach (seconds the finger takes to arrive, 0.4),
//        withdraw (seconds after the flick before the hand pulls back, 0.55), on ('#e9d3a6' lamp colour).
import React from 'react';
import {AbsoluteFill} from 'remotion';
import type {KitComponentProps} from '../../core/registry';
import {clamp01, ease, num, P, str} from './util';

export const LightSwitch: React.FC<KitComponentProps> = ({props, time: t, width: W, height: H}) => {
	const at = num(props.at, 0.6);
	const reach = num(props.reach, 0.4);
	const back = num(props.withdraw, 0.55);
	const lamp = str(props.on, '#e9d3a6');
	// light level: 1 on, 0 off (a 2-frame flicker on the way down)
	const dt = t - at;
	const light = dt < 0 ? 1 : dt < 0.04 ? 0.35 : dt < 0.07 ? 0.7 : dt < 0.1 ? 0.15 : 0;
	// rocker: up (on) until the flick, snapping down over 2 frames
	const rock = clamp01(dt / 0.06);
	// finger: travels in, presses through the flick, holds, then pulls back out of frame
	const inK = ease('out', clamp01((t - (at - reach)) / reach));
	const outK = ease('in', clamp01((t - (at + back)) / 0.45));
	const press = dt < -0.05 ? 0 : dt < 0.08 ? clamp01((dt + 0.05) / 0.13) : 1 - clamp01((dt - 0.08) / 0.25) * 0.6;
	const u = W / 1080;
	// plate in art units (1080 x 1920)
	const px = 540;
	const py = 860;
	const pw = 330;
	const ph = 520;
	// fingertip target: the top half of the rocker, pushing it down
	const tipX = px + 20 + (1 - inK) * 420 + outK * 520;
	const tipY = py - 70 + press * 95 + (1 - inK) * 520 + outK * 640;
	const skin = P.skin;
	const shade = P.skinShade;
	const ow = 9;
	const wallOn = '#8a7d68';
	const wallOff = '#232a38';
	const mix = (a: string, b: string, k: number) => {
		const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
		const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
		return `rgb(${pa.map((v, i) => Math.round(v * k + pb[i] * (1 - k))).join(',')})`;
	};
	const wall = mix(wallOn, wallOff, light);
	// forearm from the lower-right corner to the knuckles; index finger extended to the tip
	const kx = tipX + 150;
	const ky = tipY + 210;
	const ang = Math.atan2(tipY - ky, tipX - kx);
	const fw = 64; // finger width
	const nx = -Math.sin(ang) * (fw / 2);
	const ny = Math.cos(ang) * (fw / 2);
	const finger = `M ${kx + nx} ${ky + ny} L ${tipX + nx} ${tipY + ny} A ${fw / 2} ${fw / 2} 0 0 1 ${tipX - nx} ${tipY - ny} L ${kx - nx} ${ky - ny} Z`;
	const palm = `M ${kx - 70} ${ky - 40} C ${kx - 40} ${ky - 120}, ${kx + 120} ${ky - 120}, ${kx + 170} ${ky - 30}
		C ${kx + 230} ${ky + 60}, ${kx + 260} ${ky + 200}, ${kx + 300} ${ky + 420} L ${kx + 520} ${ky + 900} L ${kx + 60} ${ky + 900}
		C ${kx + 20} ${ky + 600}, ${kx - 40} ${ky + 300}, ${kx - 90} ${ky + 120} C ${kx - 110} ${ky + 50}, ${kx - 100} ${ky - 10}, ${kx - 70} ${ky - 40} Z`;
	// curled middle / ring fingers: rounded knuckle bumps under the index finger
	const curls = [0, 1, 2].map((i) => ({cx: kx - 40 + i * 62, cy: ky + 40 + i * 34, r: 44 - i * 4}));
	const sleeveY = ky + 470;
	return (
		<AbsoluteFill style={{background: wall}}>
			<svg width={W} height={H} viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice" style={{display: 'block'}}>
				<defs>
					<radialGradient id="ls-lamp" cx="0.35" cy="0.18" r="0.75">
						<stop offset="0" stopColor={lamp} stopOpacity={0.55 * light} />
						<stop offset="1" stopColor={lamp} stopOpacity={0} />
					</radialGradient>
					<linearGradient id="ls-strip" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#7ea0d8" stopOpacity={0} />
						<stop offset="1" stopColor="#7ea0d8" stopOpacity={0.22 + 0.1 * (1 - light)} />
					</linearGradient>
				</defs>
				{/* wall texture: faint vertical panel seams + skirting */}
				{[160, 920].map((x) => (
					<rect key={x} x={x} y={0} width={6} height={1920} fill="#000" opacity={0.12} />
				))}
				<rect x={0} y={0} width={1080} height={1920} fill="url(#ls-lamp)" />
				{/* door frame edge on the left, corridor light under the door */}
				<rect x={0} y={0} width={70} height={1920} fill={mix('#5c4a3a', '#141820', light)} stroke={P.line} strokeWidth={ow} />
				<rect x={0} y={1640} width={1080} height={280} fill="url(#ls-strip)" />
				{/* switch plate: shadow, plate, screws, rocker */}
				<rect x={px - pw / 2 + 22} y={py - ph / 2 + 26} width={pw} height={ph} rx={34} fill="#000" opacity={0.25 + 0.2 * light} />
				<rect x={px - pw / 2} y={py - ph / 2} width={pw} height={ph} rx={34} fill={mix('#ece3cf', '#3a3f4a', light)} stroke={P.line} strokeWidth={ow} />
				<circle cx={px} cy={py - ph / 2 + 50} r={13} fill={mix('#b9ae96', '#2a2e36', light)} stroke={P.line} strokeWidth={4} />
				<circle cx={px} cy={py + ph / 2 - 50} r={13} fill={mix('#b9ae96', '#2a2e36', light)} stroke={P.line} strokeWidth={4} />
				<rect x={px - 82} y={py - 150} width={164} height={300} rx={22} fill={mix('#d8ccb2', '#2c3038', light)} stroke={P.line} strokeWidth={7} />
				{/* rocker: the pressed half is darker; up = on, down = off */}
				<rect x={px - 66} y={py - 136 + rock * 136} width={132} height={136} rx={16} fill={mix('#fbf6ea', '#3f444e', light)} stroke={P.line} strokeWidth={6} />
				<rect x={px - 66} y={py - 136 + (1 - rock) * 136} width={132} height={136} rx={16} fill={mix('#bfb39b', '#262a31', light)} stroke={P.line} strokeWidth={6} opacity={0.9} />
				{/* hand (lit by the lamp, then by nothing) */}
				<g opacity={inK > 0.001 && outK < 0.999 ? 1 : 0}>
					<path d={palm} fill={mix(skin, '#596070', light)} stroke={P.line} strokeWidth={ow} strokeLinejoin="round" />
					{/* sleeve cuff */}
					<path
						d={`M ${kx + 40} ${sleeveY} L ${kx + 330} ${sleeveY - 70} L ${kx + 560} ${sleeveY + 500} L ${kx + 80} ${sleeveY + 600} Z`}
						fill={mix('#3f5a3a', '#161b22', light)}
						stroke={P.line}
						strokeWidth={ow}
						strokeLinejoin="round"
					/>
					{curls.map((c, i) => (
						<circle key={i} cx={c.cx} cy={c.cy} r={c.r} fill={mix(shade, '#33363e', light)} stroke={P.line} strokeWidth={ow * 0.8} />
					))}
					<path d={finger} fill={mix(skin, '#596070', light)} stroke={P.line} strokeWidth={ow} strokeLinejoin="round" />
					{/* knuckle crease + nail */}
					<path d={`M ${(kx + tipX) / 2 + nx * 0.7} ${(ky + tipY) / 2 + ny * 0.7} l ${-nx * 1.4} ${-ny * 1.4}`} stroke={P.line} strokeWidth={4} opacity={0.5} />
					<ellipse
						cx={tipX - Math.cos(ang) * -6}
						cy={tipY - Math.sin(ang) * -6}
						rx={fw * 0.32}
						ry={fw * 0.4}
						transform={`rotate(${(ang * 180) / Math.PI + 90} ${tipX} ${tipY})`}
						fill={mix('#f6eee2', '#454852', light)}
						stroke={P.line}
						strokeWidth={4}
					/>
				</g>
				{/* the dark: a blue-black wash once the lamp is off (the hand and plate stay as silhouettes) */}
				<rect x={0} y={0} width={1080} height={1920} fill="#05070c" opacity={(1 - light) * 0.25} />
			</svg>
			<AbsoluteFill style={{boxShadow: `inset 0 0 ${260 * u}px rgba(0,0,0,${0.55 + 0.3 * (1 - light)})`}} />
		</AbsoluteFill>
	);
};

/**
 * Top-of-frame fade for chat punch-ins: darkens the top `height` of the screen so a text row cut by the frame edge
 * reads as falling into shadow, not as a cropping error. windows [{at, until}] (scene seconds), strength 0..1.
 */
export const TopFade: React.FC<KitComponentProps> = ({props, time: t, height: H}) => {
	let k = 0;
	for (const w of (Array.isArray(props.windows) ? props.windows : []) as {at?: number; until?: number}[]) {
		const a = num(w.at, 0);
		const b = num(w.until, 1e9);
		k = Math.max(k, Math.min(clamp01((t - a) / 0.15), clamp01((b - t) / 0.1)));
	}
	if (k <= 0) return null;
	const h = num(props.height, 0.24) * H;
	const s = num(props.strength, 1);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div
				style={{
					position: 'absolute',
					left: 0,
					top: 0,
					right: 0,
					height: h,
					opacity: k,
					background: `linear-gradient(to bottom, rgba(5,6,9,${s}) 0%, rgba(5,6,9,${s * 0.97}) 55%, rgba(5,6,9,0) 100%)`,
				}}
			/>
		</AbsoluteFill>
	);
};
