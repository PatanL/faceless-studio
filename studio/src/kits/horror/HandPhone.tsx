// "Hand holding the phone" framing: a big cartoon hand grips the phone from below,
// thumb over the screen, fingertips wrapping the far edge. Full-frame layer.
import React from 'react';
import type {KitComponentProps} from '../../core/registry';
import {glitchAt, GlitchWrap} from './fx';
import {PHONE_H, PHONE_W, PhoneDevice} from './Phone';
import {arr, clamp01, cueLevel, ease, jitter, num, obj, P, str} from './util';

/**
 * props:
 *   phone: {...}        everything horror/Phone accepts (mode/screens, chat, lock, call, banners, vibrate...)
 *   phoneWidth (0.7)    phone width as a fraction of the box width
 *   cx, cy (0.5, 0.47)  phone centre as fractions of the box
 *   tilt (-3)           degrees
 *   side ('right')      which hand: 'right' (thumb on the right) or 'left'
 *   thumbReach (0.12), thumbY (0.93)  resting thumb tip (default rests over the input bar, clear of the newest bubble): reach in from the near edge (phone widths) and height (phone heights)
 *   taps [{at, x, y}]   thumb taps; x/y = target on the screen as fractions (default 0.5, 0.85)
 *   tremble (0)         px of hand shake (fear); trembleCues [{at, duration, amount}] multiplies it
 *   skin, outline       colours
 *   glitch              cue list, RGB-splits the whole hand + phone
 */
export const HandPhone: React.FC<KitComponentProps> = ({props, time: t, width: W, height: H}) => {
	const phone = obj(props.phone);
	const pw = W * num(props.phoneWidth, 0.7);
	const ph = (pw * PHONE_H) / PHONE_W;
	const cx = W * num(props.cx, 0.5);
	const cy = H * num(props.cy, 0.47);
	const L = cx - pw / 2;
	const R = cx + pw / 2;
	const T = cy - ph / 2;
	const B = cy + ph / 2;
	const u = pw;
	// Nora's skin (horror/Protagonist) so the hand reads as hers, with the characters' outline weight
	const skin = str(props.skin, '#e8d9c4');
	const nail = str(props.nail, '#f3eadc');
	const outline = str(props.outline, P.line);
	const ow = Math.max(4, u * 0.012);
	const right = str(props.side, 'right') !== 'left';
	const tilt = num(props.tilt, -3) * (right ? 1 : -1);

	const tremAmt = num(props.tremble, 0) * (props.trembleCues ? cueLevel(props.trembleCues, t, 1, 0.1) : 1);
	const tx = tremAmt ? jitter('hp-x', t, 1 / 20) * tremAmt : 0;
	const ty = tremAmt ? jitter('hp-y', t, 1 / 20) * tremAmt * 0.6 : 0;
	// idle breathing sway
	const sway = Math.sin(t * 1.3) * u * 0.006;

	// thumb tip, moving to tap targets
	let tipX = R - num(props.thumbReach, 0.12) * u;
	let tipY = T + ph * num(props.thumbY, 0.93);
	let press = 0;
	for (const tap of arr<{at?: number; x?: number; y?: number}>(props.taps)) {
		const at = num(tap.at, 0);
		const k = t < at - 0.25 || t > at + 0.35 ? 0 : t < at ? ease('inOut', (t - (at - 0.25)) / 0.25) : 1 - ease('inOut', (t - at) / 0.35);
		if (k > 0) {
			const gx = L + num(tap.x, 0.5) * pw;
			const gy = T + num(tap.y, 0.85) * ph;
			tipX += (gx - tipX) * k;
			tipY += (gy - tipY) * k;
			press = Math.max(press, clamp01(1 - Math.abs(t - at) / 0.08));
		}
	}
	// thumb: one tapered filled shape from the heel of the hand (off the bottom-right corner) to the tip
	const baseX = R + 0.13 * u;
	const baseY = B + 0.1 * u;
	const ctrlX = (baseX + tipX) / 2 + 0.1 * u;
	const ctrlY = (baseY + tipY) / 2 + 0.07 * u;
	const thumbW = 0.15 * u * (1 - press * 0.06);
	const qp = (k: number): [number, number] => {
		const a = 1 - k;
		return [a * a * baseX + 2 * a * k * ctrlX + k * k * tipX, a * a * baseY + 2 * a * k * ctrlY + k * k * tipY];
	};
	const qd = (k: number): [number, number] => {
		const dx = 2 * (1 - k) * (ctrlX - baseX) + 2 * k * (tipX - ctrlX);
		const dy = 2 * (1 - k) * (ctrlY - baseY) + 2 * k * (tipY - ctrlY);
		const l = Math.hypot(dx, dy) || 1;
		return [dx / l, dy / l];
	};
	const halfW = (k: number) => (thumbW * (1.3 - 0.38 * k)) / 2;
	const sideA: string[] = [];
	const sideB: string[] = [];
	const NS = 14;
	for (let i = 0; i <= NS; i++) {
		const k = i / NS;
		const [x, y] = qp(k);
		const [dx, dy] = qd(k);
		const w = halfW(k);
		sideA.push(`${x - dy * w} ${y + dx * w}`);
		sideB.unshift(`${x + dy * w} ${y - dx * w}`);
	}
	const [tdx, tdy] = qd(1);
	const wTip = halfW(1);
	const capA = sideA[NS].split(' ').map(Number);
	const capB = sideB[0].split(' ').map(Number);
	const thumbPath =
		`M ${sideA.join(' L ')} C ${capA[0] + tdx * wTip * 1.35} ${capA[1] + tdy * wTip * 1.35} ${capB[0] + tdx * wTip * 1.35} ${capB[1] + tdy * wTip * 1.35} ` +
		`${capB[0]} ${capB[1]} L ${sideB.join(' L ')} Z`;
	const ang = Math.atan2(tdy, tdx);
	const nailX = tipX + tdx * wTip * 0.15;
	const nailY = tipY + tdy * wTip * 0.15;

	const mirror = right ? undefined : `translate(${2 * cx} 0) scale(-1 1)`;
	// one silhouette: outline pass (fat stroke) under a fill pass, so overlapping parts merge into one hand
	const solid = (ds: string[], key: string) => (
		<g key={key}>
			{ds.map((d, i) => <path key={`o${i}`} d={d} fill={outline} stroke={outline} strokeWidth={ow * 2} strokeLinejoin="round" />)}
			{ds.map((d, i) => <path key={`f${i}`} d={d} fill={skin} />)}
		</g>
	);
	// back of the hand: the palm cups the phone's lower edge and wraps round the far (left) side
	const backHand =
		`M ${L + 0.12 * u} ${T + ph * 0.5} C ${L - 0.15 * u} ${T + ph * 0.52} ${L - 0.19 * u} ${B - 0.08 * u} ${L + 0.02 * u} ${B + 0.1 * u} ` +
		`C ${L + 0.25 * u} ${B + 0.28 * u} ${R - 0.1 * u} ${B + 0.3 * u} ${R + 0.12 * u} ${B + 0.08 * u} L ${R + 0.5 * u} ${H + 0.6 * u} L ${L + 0.3 * u} ${H + 0.6 * u} Z`;
	const thenar = `M ${R - 0.12 * u} ${B + 0.02 * u} C ${R - 0.08 * u} ${B - 0.14 * u} ${R + 0.12 * u} ${B - 0.2 * u} ${R + 0.22 * u} ${B - 0.02 * u} L ${R + 0.3 * u} ${H + 0.5 * u} L ${R - 0.1 * u} ${H + 0.5 * u} Z`;
	// four rounded finger lobes curl round the far edge onto the bezel (cartoon capsules, no knuckle ridges)
	const tips = [
		{fy: 0.555, w: 0.112, x1: 0.05},
		{fy: 0.65, w: 0.118, x1: 0.06},
		{fy: 0.745, w: 0.114, x1: 0.055},
		{fy: 0.835, w: 0.104, x1: 0.04},
	];
	const fingerPaths = tips.map(({fy, w, x1: reach}, i) => {
		const y = T + ph * fy + Math.sin(t * 1.1 + i) * 1.5;
		const hw = (w * u) / 2;
		const x0 = L - 0.16 * u;
		const x1 = L + reach * u;
		return {y, hw, d: `M ${x0} ${y - hw} L ${x1 - hw} ${y - hw} A ${hw} ${hw} 0 0 1 ${x1 - hw} ${y + hw} L ${x0} ${y + hw} Z`};
	});

	const body = (
		<div style={{position: 'absolute', inset: 0, transform: `translate(${tx}px, ${ty + sway}px) rotate(${tilt}deg)`, transformOrigin: `${cx}px ${B}px`}}>
			{/* back: palm wrapping the lower edge and the far side */}
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<g transform={mirror}>
					{solid([backHand], 'back')}
				</g>
			</svg>
			{/* phone */}
			<div style={{position: 'absolute', left: L, top: T, width: pw, height: ph}}>
				<div style={{transform: `scale(${pw / PHONE_W})`, transformOrigin: '0 0'}}>
					<PhoneDevice p={phone} t={t} />
				</div>
			</div>
			{/* front: fingertips over the far edge, heel + thumb over the screen */}
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<g transform={mirror}>
					{fingerPaths.map((f, i) => (
						<path key={`ft${i}`} d={f.d} fill={skin} stroke={outline} strokeWidth={ow * 1.4} strokeLinejoin="round" />
					))}
					{solid([thenar, thumbPath], 'thumb')}
					<ellipse
						cx={nailX}
						cy={nailY}
						rx={wTip * 0.72}
						ry={wTip * 0.6}
						transform={`rotate(${(ang * 180) / Math.PI} ${nailX} ${nailY})`}
						fill={nail}
						stroke={outline}
						strokeWidth={ow * 0.6}
					/>
				</g>
			</svg>
		</div>
	);

	return (
		<div style={{width: W, height: H, position: 'relative'}}>
			<GlitchWrap amount={glitchAt(props, t)} t={t} seed="handphone">
				{body}
			</GlitchWrap>
		</div>
	);
};
