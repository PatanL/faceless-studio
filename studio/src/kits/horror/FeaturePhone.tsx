// Old candybar feature phone with a small monochrome LCD (burner phone / found phone beats).
import React from 'react';
import type {KitComponentProps} from '../../core/registry';
import {glitchAt, GlitchWrap} from './fx';
import {clamp01, cueLevel, num, obj, str} from './util';

const FW = 360;
const FH = 780;
const MONO = '"Courier New", Courier, monospace';

/**
 * props: sms {from, text, at, cps}  (message typed out on the LCD after `at`)
 *        header ('1 NEW MESSAGE'), clock ('02:16'), lcd ('#9db59a' green) | lcdOff, backlight (0..1, 1)
 *        body ('#2c2f35'), vibrate [{at, duration}], glitch
 */
export const FeaturePhone: React.FC<KitComponentProps> = ({props, time: t, width, height}) => {
	const s = Math.min(width / FW, height / FH);
	const sms = obj(props.sms);
	const at = num(sms.at, 0);
	const cps = num(sms.cps, 18);
	const full = str(sms.text, 'WHY IS YOUR DOOR UNLOCKED');
	const shown = t < at ? '' : full.slice(0, Math.floor((t - at) * cps));
	const cursor = Math.floor(t * 2.5) % 2 === 0 && t >= at;
	const lcd = str(props.lcd, '#9db59a');
	const back = num(props.backlight, 1);
	const body = str(props.body, '#2c2f35');
	const vib = cueLevel(props.vibrate, t, 0.6, 0.03);
	const dx = vib ? Math.sin(t * 100) * 5 * vib : 0;
	const rot = vib ? Math.sin(t * 80) * 1.5 * vib : 0;
	const keys = ['1', '2 abc', '3 def', '4 ghi', '5 jkl', '6 mno', '7 pqrs', '8 tuv', '9 wxyz', '*', '0 +', '#'];
	const device = (
		<div style={{position: 'relative', width: FW, height: FH, transform: `translateX(${dx}px) rotate(${rot}deg)`}}>
			<div
				style={{
					position: 'absolute',
					inset: 0,
					borderRadius: '70px 70px 90px 90px',
					background: `linear-gradient(90deg, #17191d, ${body} 18%, ${body} 82%, #17191d)`,
					boxShadow: '0 24px 50px rgba(0,0,0,0.6), inset 0 0 0 3px #4b4f57',
				}}
			/>
			{/* earpiece + brand plate (blank, no brand) */}
			<div style={{position: 'absolute', left: FW / 2 - 50, top: 34, width: 100, height: 12, borderRadius: 6, background: '#111316'}} />
			{/* LCD */}
			<div
				style={{
					position: 'absolute',
					left: 46,
					top: 74,
					width: FW - 92,
					height: 236,
					borderRadius: 14,
					background: '#0f1112',
					padding: 10,
					boxSizing: 'border-box',
				}}
			>
				<div
					style={{
						width: '100%',
						height: '100%',
						borderRadius: 6,
						background: lcd,
						filter: `brightness(${0.45 + 0.55 * back})`,
						boxShadow: back > 0.5 ? `0 0 30px ${lcd}` : undefined,
						fontFamily: MONO,
						fontWeight: 700,
						color: '#17221a',
						padding: '8px 12px',
						boxSizing: 'border-box',
						position: 'relative',
						overflow: 'hidden',
					}}
				>
					<div style={{display: 'flex', justifyContent: 'space-between', fontSize: 17}}>
						<span>{'▮▮▮▯'}</span>
						<span>{str(props.clock, '02:16')}</span>
						<span>{'▭'}</span>
					</div>
					<div style={{fontSize: 18, marginTop: 6, borderBottom: '2px solid #17221a', paddingBottom: 4}}>
						{t >= at ? str(sms.from, 'UNKNOWN') : str(props.header, '1 NEW MESSAGE')}
					</div>
					<div style={{fontSize: 22, lineHeight: 1.18, marginTop: 8, textTransform: 'uppercase', wordBreak: 'break-word'}}>
						{shown}
						{cursor ? '█' : ''}
					</div>
					{/* pixel grid */}
					<div style={{position: 'absolute', inset: 0, background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.06) 0 1px, transparent 1px 3px), repeating-linear-gradient(90deg, rgba(0,0,0,0.05) 0 1px, transparent 1px 3px)'}} />
				</div>
			</div>
			{/* nav cluster */}
			<div style={{position: 'absolute', left: 40, right: 40, top: 334, height: 110, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
				<div style={{width: 74, height: 40, borderRadius: 20, background: '#3aa865', opacity: 0.85}} />
				<div style={{width: 104, height: 104, borderRadius: 52, background: '#3a3e46', boxShadow: 'inset 0 0 0 4px #4c515b', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
					<div style={{width: 40, height: 40, borderRadius: 20, background: '#24272c'}} />
				</div>
				<div style={{width: 74, height: 40, borderRadius: 20, background: '#c4393e', opacity: 0.85}} />
			</div>
			{/* keypad */}
			<div style={{position: 'absolute', left: 40, right: 40, top: 466, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px 16px'}}>
				{keys.map((k) => {
					const [n, l] = k.split(' ');
					return (
						<div
							key={k}
							style={{
								height: 58,
								borderRadius: 18,
								background: 'linear-gradient(180deg, #4a4f58, #33363d)',
								boxShadow: 'inset 0 -3px 0 rgba(0,0,0,0.35)',
								display: 'flex',
								alignItems: 'baseline',
								justifyContent: 'center',
								gap: 6,
								paddingTop: 10,
								boxSizing: 'border-box',
								fontFamily: '"Montserrat", sans-serif',
								color: '#d9dde3',
							}}
						>
							<span style={{fontWeight: 800, fontSize: 28}}>{n}</span>
							{l ? <span style={{fontWeight: 700, fontSize: 13, color: '#9aa1ab'}}>{l}</span> : null}
						</div>
					);
				})}
			</div>
		</div>
	);
	return (
		<div style={{width, height, position: 'relative'}}>
			<div style={{position: 'absolute', left: (width - FW * s) / 2, top: (height - FH * s) / 2, transform: `scale(${s})`, transformOrigin: '0 0', width: FW, height: FH}}>
				<GlitchWrap amount={glitchAt(props, t)} t={t} seed="feature">
					{device}
				</GlitchWrap>
			</div>
			{back > 0.5 ? (
				<div
					style={{
						position: 'absolute',
						left: width / 2 - 200 * s,
						top: (height - FH * s) / 2 - 60 * s,
						width: 400 * s,
						height: 420 * s,
						background: `radial-gradient(circle, rgba(157,181,154,${0.18 * clamp01(back)}) 0%, rgba(0,0,0,0) 70%)`,
						pointerEvents: 'none',
					}}
				/>
			) : null}
		</div>
	);
};
