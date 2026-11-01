/**
 * Type + the "lantern tag" label (STYLE_BIBLE §11): ink text on a bone pill, soft plane-gap shadow, a 3 px bone
 * leader that ends in a 2-tone ring on the object. Pops in with the POP spring (10-25 % overshoot).
 */
import React from 'react';
import {continueRender, delayRender} from 'remotion';
import '@fontsource/montserrat/700.css';
import '@fontsource/montserrat/800.css';
import '@fontsource/anton/400.css';
import {c, rgba} from './color';
import {popIn, springAt, SETTLE} from '../motion/motion';

let fontsPromise: Promise<unknown> | null = null;
export function waitForFonts() {
	if (fontsPromise || typeof document === 'undefined') return;
	const h = delayRender('fonts');
	fontsPromise = Promise.all([document.fonts.load('800 40px "Montserrat"'), document.fonts.load('700 40px "Montserrat"'), document.fonts.load('400 40px "Anton"')])
		.catch(() => undefined)
		.finally(() => continueRender(h));
}

export const FONT = '"Montserrat", "Arial Black", sans-serif';
export const DISPLAY = '"Anton", "Arial Narrow", sans-serif';

/** SVG lantern tag. (x, y) = pill centre; (ax, ay) = the ring on the object. */
export const LanternTag: React.FC<{
	t: number;
	at: number;
	x: number;
	y: number;
	ax: number;
	ay: number;
	text: string;
	sub?: string;
	size?: number;
	ring?: string;
}> = ({t, at, x, y, ax, ay, text, sub, size = 36, ring = 'tide-4'}) => {
	if (t < at) return null;
	const s = popIn(t, at);
	const lead = springAt(t, at + 0.12, SETTLE);
	const w = text.length * size * 0.74 + size * 1.3 + (sub ? sub.length * size * 0.36 + size * 0.5 : 0);
	const h = size * 1.6;
	const ex = x + (ax - x) * lead;
	const ey = y + h / 2 + (ay - y - h / 2) * lead;
	return (
		<g>
			<line x1={x} y1={y + h / 2} x2={ex} y2={ey} stroke={c('bone-2')} strokeWidth={3} strokeLinecap="round" opacity={Math.min(1, lead * 1.5)} />
			<g transform={`translate(${ex} ${ey}) scale(${Math.max(0, lead)})`}>
				<circle r={11} fill="none" stroke={c('bone-2')} strokeWidth={3.5} />
				<circle r={5} fill={c(ring)} />
			</g>
			<g transform={`translate(${x} ${y}) scale(${Math.max(0, s)})`}>
				<rect x={-w / 2} y={-h / 2 + 6} width={w} height={h} rx={h / 2} fill={rgba(c('ink-0'), 0.35)} />
				<rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2} fill={c('bone-2')} />
				<text
					x={sub ? -w / 2 + size * 0.65 : 0}
					y={size * 0.36}
					textAnchor={sub ? 'start' : 'middle'}
					fontFamily={FONT}
					fontWeight={800}
					fontSize={size}
					fill={c('ink-1')}
				>
					{text}
					{sub ? (
						<tspan dx={size * 0.4} fontWeight={700} fontSize={size * 0.6} fill={c('tide-0')}>
							{sub}
						</tspan>
					) : null}
				</text>
			</g>
		</g>
	);
};
