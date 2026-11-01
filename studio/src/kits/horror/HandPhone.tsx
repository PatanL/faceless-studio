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
	const skin = str(props.skin, P.handSkin);
	const shade = str(props.shade, '#a8988a');
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
	let tipX = R - num(props.thumbReach, 0.2) * u;
	let tipY = T + ph * 0.72;
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
	const baseX = R + 0.05 * u;
	const baseY = B - 0.04 * u;
	const ctrlX = (baseX + tipX) / 2 + 0.1 * u;
	const ctrlY = (baseY + tipY) / 2 + 0.06 * u;
	const thumbW = 0.17 * u * (1 - press * 0.06);

	// thumb direction for the nail
	const ang = Math.atan2(tipY - ctrlY, tipX - ctrlX);
	const nailX = tipX - Math.cos(ang) * thumbW * 0.28;
	const nailY = tipY - Math.sin(ang) * thumbW * 0.28;

	const mirror = right ? undefined : `translate(${2 * cx} 0) scale(-1 1)`;
	const limb = (d: string, w: number, key: string, fill = skin) => (
		<g key={key}>
			<path d={d} stroke={outline} strokeWidth={w + ow * 2} fill="none" strokeLinecap="round" strokeLinejoin="round" />
			<path d={d} stroke={fill} strokeWidth={w} fill="none" strokeLinecap="round" strokeLinejoin="round" />
		</g>
	);
	const fingerYs = [0.46, 0.58, 0.7, 0.82];
	const fingerW = 0.13 * u;

	const body = (
		<div style={{position: 'absolute', inset: 0, transform: `translate(${tx}px, ${ty + sway}px) rotate(${tilt}deg)`, transformOrigin: `${cx}px ${B}px`}}>
			{/* back: forearm + palm */}
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<g transform={mirror}>
					{limb(`M ${R - 0.12 * u} ${B} Q ${R + 0.12 * u} ${B + 0.35 * u} ${R + 0.3 * u} ${H + 0.4 * u}`, 0.5 * u, 'arm')}
					<ellipse cx={L + 0.6 * u} cy={B - 0.02 * u} rx={0.52 * u} ry={0.34 * u} fill={skin} stroke={outline} strokeWidth={ow} />
					<path d={`M ${L + 0.2 * u} ${B + 0.18 * u} Q ${L + 0.55 * u} ${B + 0.34 * u} ${R - 0.05 * u} ${B + 0.2 * u}`} stroke={shade} strokeWidth={u * 0.03} fill="none" strokeLinecap="round" opacity={0.7} />
					{/* back of the fingers, wrapped behind the phone's far edge */}
					<rect x={L - 0.13 * u} y={T + ph * 0.4} width={0.5 * u} height={ph * 0.62} rx={0.12 * u} fill={skin} stroke={outline} strokeWidth={ow} />
				</g>
			</svg>
			{/* phone */}
			<div style={{position: 'absolute', left: L, top: T, width: pw, height: ph}}>
				<div style={{transform: `scale(${pw / PHONE_W})`, transformOrigin: '0 0'}}>
					<PhoneDevice p={phone} t={t} />
				</div>
			</div>
			{/* front: fingertips over the far edge, thumb over the screen */}
			<svg width={W} height={H} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
				<g transform={mirror}>
					{fingerYs.map((fy, i) => {
						const y = T + ph * fy + Math.sin(t * 1.1 + i) * 1.5;
						const fw2 = fingerW * (i === 3 ? 0.85 : 1);
						// finger reaches round the far edge: knuckle outside the phone, tip resting on the bezel
						const x0 = L - 0.16 * u;
						const x1 = L + 0.045 * u;
						return (
							<g key={`ft${i}`} transform={`rotate(${6 + i * 3} ${x1} ${y})`}>
								<rect x={x0} y={y - fw2 / 2} width={x1 - x0} height={fw2} rx={fw2 / 2} fill={skin} stroke={outline} strokeWidth={ow} />
								<path d={`M ${x1 - 0.05 * u} ${y - fw2 * 0.3} q ${0.025 * u} ${fw2 * 0.3} 0 ${fw2 * 0.6}`} stroke={shade} strokeWidth={ow * 0.8} fill="none" strokeLinecap="round" />
								<path d={`M ${x0 + 0.05 * u} ${y - fw2 * 0.32} l 0 ${fw2 * 0.64}`} stroke={shade} strokeWidth={ow * 0.7} strokeLinecap="round" />
							</g>
						);
					})}
					{limb(`M ${baseX} ${baseY} Q ${ctrlX} ${ctrlY} ${tipX} ${tipY}`, thumbW, 'thumb')}
					<ellipse
						cx={nailX}
						cy={nailY}
						rx={thumbW * 0.26}
						ry={thumbW * 0.2}
						transform={`rotate(${(ang * 180) / Math.PI} ${nailX} ${nailY})`}
						fill="#ddd2c6"
						stroke={shade}
						strokeWidth={ow * 0.6}
					/>
					<path d={`M ${baseX - 0.02 * u} ${baseY - 0.08 * u} q ${-0.05 * u} ${0.02 * u} ${-0.07 * u} ${0.07 * u}`} stroke={shade} strokeWidth={ow} fill="none" strokeLinecap="round" />
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
