// Series end card (Part 1 -> Part 2 cliffhanger): a full-width chat bubble with the next rule being typed,
// and a big rubber-stamp "PART 2" across the frame. Full-frame layer; reads at phone scale on a small screen.
import React from 'react';
import type {KitComponentProps} from '../../core/registry';
import {clamp01, ease, jitter, num, P, str} from './util';

const FONT = '"Montserrat", "Helvetica Neue", Arial, sans-serif';

/**
 * props: rule ('RULE 6:'), from ('Management'), sub ('is typing…'), label ('PART 2'), at (0, bubble pops in),
 *        stampAt (at + 0.6), bg ('#07070a'), bubbleY (0.4 fraction of height), stampY (0.68)
 */
export const EndCard: React.FC<KitComponentProps> = ({props, time: t, width: W, height: H}) => {
	const at = num(props.at, 0);
	const stampAt = num(props.stampAt, at + 0.6);
	if (t < at) return null;
	const u = W / 1080;
	const pin = ease('backOut', clamp01((t - at) / 0.3));
	const st = clamp01((t - stampAt) / 0.16);
	const shake = t >= stampAt && t < stampAt + 0.25 ? jitter('end-st', t, 1 / 30) * 14 * u * (1 - (t - stampAt) / 0.25) : 0;
	const red = P.red;
	return (
		<div style={{position: 'absolute', inset: 0, width: W, height: H, background: str(props.bg, '#07070a'), overflow: 'hidden', transform: `translate(${shake}px, ${shake * 0.6}px)`}}>
			<div style={{position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at 50% 42%, rgba(120,16,24,0.35) 0%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.85) 100%)'}} />
			{/* sender line */}
			<div style={{position: 'absolute', left: 70 * u, top: H * num(props.bubbleY, 0.4) - 250 * u, display: 'flex', alignItems: 'center', gap: 22 * u, opacity: clamp01((t - at) / 0.2)}}>
				<div style={{width: 92 * u, height: 92 * u, borderRadius: '50%', background: '#3a3f4a', border: `${4 * u}px solid ${P.line}`, color: '#eef0f3', fontFamily: FONT, fontWeight: 900, fontSize: 44 * u, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					{str(props.from, 'Management').slice(0, 1)}
				</div>
				<div style={{fontFamily: FONT, fontWeight: 800, color: '#cfd3da', fontSize: 46 * u}}>
					{str(props.from, 'Management')} <span style={{color: '#7fd1a0', fontWeight: 700}}>{str(props.sub, 'is typing…')}</span>
				</div>
			</div>
			{/* the rule bubble, nearly full width */}
			<div
				style={{
					position: 'absolute',
					left: 60 * u,
					right: 60 * u,
					top: H * num(props.bubbleY, 0.4) - 130 * u,
					background: red,
					border: `${6 * u}px solid #ff6b72`,
					borderRadius: 48 * u,
					borderTopLeftRadius: 12 * u,
					padding: `${40 * u}px ${56 * u}px`,
					transform: `scale(${0.6 + 0.4 * pin})`,
					transformOrigin: '0% 0%',
					opacity: clamp01((t - at) / 0.12),
					boxShadow: `0 0 ${60 * u}px rgba(255,40,50,0.35)`,
					display: 'flex',
					alignItems: 'center',
					gap: 36 * u,
				}}
			>
				<div style={{fontFamily: '"Anton", "Montserrat", Impact, sans-serif', fontSize: 190 * u, lineHeight: 1, color: '#fff', letterSpacing: '0.02em'}}>{str(props.rule, 'RULE 6:')}</div>
				<div style={{display: 'flex', gap: 22 * u, alignItems: 'center'}}>
					{[0, 1, 2].map((i) => {
						const ph = (t * 2.4 - i * 0.18) % 1;
						const up = ph < 0.4 ? Math.sin((ph / 0.4) * Math.PI) : 0;
						return <div key={i} style={{width: 34 * u, height: 34 * u, borderRadius: '50%', background: '#fff', opacity: 0.45 + 0.55 * up, transform: `translateY(${-up * 18 * u}px)`}} />;
					})}
				</div>
			</div>
			{/* PART 2 stamp */}
			{t >= stampAt ? (
				<div style={{position: 'absolute', left: 0, right: 0, top: H * num(props.stampY, 0.68), display: 'flex', justifyContent: 'center', transform: 'translateY(-50%)'}}>
					<div
						style={{
							fontFamily: '"Anton", "Montserrat", Impact, sans-serif',
							fontSize: 260 * u,
							lineHeight: 1,
							color: red,
							letterSpacing: '0.06em',
							padding: `${18 * u}px ${70 * u}px`,
							border: `${18 * u}px solid ${red}`,
							borderRadius: 26 * u,
							background: 'rgba(10,4,6,0.85)',
							textShadow: `0 0 ${24 * u}px rgba(255,40,50,0.55)`,
							transform: `rotate(-7deg) scale(${1.8 - 0.8 * ease('out', st)})`,
							opacity: st,
						}}
					>
						{str(props.label, 'PART 2')}
					</div>
				</div>
			) : null}
		</div>
	);
};
