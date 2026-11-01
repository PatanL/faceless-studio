import React from 'react';
import {enterExit, px} from './anim';
import {fontFamily} from './fonts';
import {SAFE_AREA, type Callout, type Format, type Theme} from './schema';

/** Screen-space text callouts (not affected by camera or grade). */
export const CalloutView: React.FC<{
	c: Callout;
	t: number;
	sceneDuration: number;
	W: number;
	H: number;
	format: Format;
	theme: Theme;
}> = ({c, t, sceneDuration, W, H, format, theme}) => {
	const end = c.duration !== undefined ? c.at + c.duration : sceneDuration + 1;
	if (t < c.at || t >= end) return null;
	const safe = SAFE_AREA[format];
	const v = format === '9:16';
	const ee = enterExit(
		t,
		{type: c.enter, duration: 0.35, distance: 120},
		c.duration !== undefined ? {type: 'fade', duration: 0.2, distance: 0} : undefined,
		c.at,
		end,
	);
	const accent = c.accent ?? theme.accent;

	const defaults: Record<Callout['style'], {x: number; y: number; ax: number}> = {
		label: {x: W / 2, y: H * (v ? 0.3 : 0.25), ax: 0.5},
		stat: {x: W / 2, y: H * (v ? 0.3 : 0.3), ax: 0.5},
		banner: {x: W / 2, y: safe.top + (v ? 90 : 70), ax: 0.5},
		lowerThird: {x: safe.left + 20, y: v ? H - safe.bottom - 80 : H * 0.6, ax: 0}, // 16:9: above the caption band
		title: {x: W / 2, y: H * 0.42, ax: 0.5},
	};
	const d = defaults[c.style];
	const x = px(c.x, W, d.x);
	const y = px(c.y, H, d.y);

	let body: React.ReactNode;
	switch (c.style) {
		case 'label':
			body = (
				<div
					style={{
						background: c.background ?? theme.paper,
						color: c.color ?? theme.ink,
						fontFamily: fontFamily('display', theme),
						fontWeight: 900,
						fontSize: c.fontSize ?? (v ? 58 : 48),
						textTransform: 'uppercase',
						padding: '0.28em 0.7em',
						borderRadius: 999,
						whiteSpace: 'nowrap',
						boxShadow: '0 10px 0 rgba(0,0,0,0.35)',
					}}
				>
					{c.text}
				</div>
			);
			break;
		case 'stat':
			body = (
				<div style={{textAlign: 'center', lineHeight: 0.95}}>
					<div
						style={{
							fontFamily: fontFamily('condensed', theme),
							fontSize: c.fontSize ?? (v ? 220 : 180),
							color: c.color ?? accent,
							WebkitTextStroke: '14px #000',
							paintOrder: 'stroke fill',
							textShadow: '0 14px 0 rgba(0,0,0,0.45)',
							whiteSpace: 'nowrap',
						}}
					>
						{c.text}
					</div>
					{c.sub ? (
						<div
							style={{
								marginTop: 18,
								display: 'inline-block',
								fontFamily: fontFamily('display', theme),
								fontWeight: 900,
								fontSize: v ? 50 : 42,
								letterSpacing: '0.08em',
								textTransform: 'uppercase',
								color: theme.paper,
								background: c.background ?? 'rgba(0,0,0,0.65)',
								padding: '0.2em 0.6em',
								borderRadius: 14,
								whiteSpace: 'nowrap',
							}}
						>
							{c.sub}
						</div>
					) : null}
				</div>
			);
			break;
		case 'banner':
			body = (
				<div
					style={{
						width: W - safe.left - safe.right - 40,
						background: c.background ?? accent,
						color: c.color ?? theme.ink,
						fontFamily: fontFamily('display', theme),
						fontWeight: 900,
						fontSize: c.fontSize ?? (v ? 64 : 56),
						textTransform: 'uppercase',
						textAlign: 'center',
						padding: '0.32em 0.5em',
						borderRadius: 18,
						boxShadow: '0 12px 0 rgba(0,0,0,0.35)',
						lineHeight: 1.05,
					}}
				>
					{c.text}
				</div>
			);
			break;
		case 'lowerThird':
			body = (
				<div style={{display: 'flex', alignItems: 'stretch', fontFamily: fontFamily('display', theme)}}>
					<div style={{width: 16, background: accent, borderRadius: 4}} />
					<div style={{background: c.background ?? 'rgba(8,10,14,0.78)', padding: '18px 30px', borderRadius: '0 14px 14px 0'}}>
						<div style={{color: c.color ?? theme.paper, fontWeight: 900, fontSize: c.fontSize ?? (v ? 56 : 52), textTransform: 'uppercase', whiteSpace: 'nowrap'}}>
							{c.text}
						</div>
						{c.sub ? (
							<div style={{color: 'rgba(255,255,255,0.75)', fontWeight: 700, fontSize: v ? 36 : 32, marginTop: 4, whiteSpace: 'nowrap'}}>
								{c.sub}
							</div>
						) : null}
					</div>
				</div>
			);
			break;
		case 'title':
			body = (
				<div
					style={{
						fontFamily: fontFamily('condensed', theme),
						fontSize: c.fontSize ?? (v ? 240 : 220),
						color: c.color ?? theme.paper,
						WebkitTextStroke: '16px #000',
						paintOrder: 'stroke fill',
						textShadow: '0 16px 0 rgba(0,0,0,0.45)',
						textTransform: 'uppercase',
						textAlign: 'center',
						lineHeight: 0.95,
						maxWidth: W - safe.left - safe.right,
					}}
				>
					{c.text}
				</div>
			);
			break;
	}

	return (
		<div
			style={{
				position: 'absolute',
				left: x,
				top: y,
				opacity: ee.opacity,
				clipPath: ee.clip,
				transformOrigin: `${d.ax * 100}% 50%`,
				transform: `translate(${-d.ax * 100}%, -50%) translate(${ee.dx}px, ${ee.dy}px) rotate(${c.rotate}deg) scale(${ee.scale})`,
			}}
		>
			{body}
		</div>
	);
};
