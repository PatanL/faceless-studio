/**
 * Small sharks for the explainer kit (added by the studio-make repeatability test, lane H1: the cookiecutter Short
 * had to fake its subject with inline SVG and its thumbnails could not show it at all).
 *
 *   cookiecutter   Isistius brasiliensis, ~0.5 m. Cigar body, two small rear dorsal fins, dark collar band behind
 *                  the head, glowing green belly photophores. props: glow (0..1 or [{t, v}] track, default 0.8),
 *                  collar (true), mouth ("closed" | "open": round sucker lips + saw teeth).
 *
 * Original code-drawn SVG. Faces RIGHT like the rest of the kit. Use as explainer/Cookiecutter or
 * explainer/Creature species "cookiecutter".
 */
import React from 'react';
import {paint, type DrawCtx, type Figure} from './figure';
import {str, swimWarp, track, warp} from './util';

const CC_BODY =
	'M 990 128 C 986 102 946 86 868 80 C 712 72 492 80 330 96 C 226 106 158 118 104 126 C 158 136 226 146 330 156 C 492 170 712 176 868 168 C 946 162 986 152 990 128 Z';
const CC_TAIL = 'M 126 126 C 96 100 66 72 38 54 C 48 90 56 112 64 126 C 56 140 48 162 42 188 C 66 168 98 150 126 132 Z';
const CC_DORSAL1 = 'M 372 98 C 352 76 330 66 308 64 C 314 80 320 92 326 102 Z';
const CC_DORSAL2 = 'M 278 108 C 260 88 242 80 224 78 C 230 92 236 102 242 113 Z';
const CC_PEC = 'M 770 162 C 750 188 720 198 696 200 C 712 184 726 172 734 164 Z';
const CC_PELVIC = 'M 330 154 C 312 170 296 176 280 178 C 290 168 300 160 306 154 Z';
const CC_BELLY = 'M 230 150 C 400 168 640 176 860 166';

const cookiecutter: Figure = {
	label: 'COOKIECUTTER SHARK',
	box: [38, 54, 952, 146],
	size: 0.5,
	axis: 'w',
	draw: (c: DrawCtx) => {
		const f = c.idle ? swimWarp({head: 990, tail: 40, amp: 9 * c.amp, t: c.t, freq: 1.2 * c.speed, k: 3}) : undefined;
		const glow = c.sil ? 0 : Math.max(0, Math.min(1, track(c.p.glow, c.t, 0.8)));
		const collar = c.p.collar !== false && !c.sil;
		const open = str(c.p.mouth, 'closed') === 'open';
		const body = warp(CC_BODY, f);
		const [ex, ey] = f ? f(936, 112) : [936, 112];
		const [mx, my] = f ? f(978, 140) : [978, 140];
		return (
			<g>
				<defs>
					<linearGradient id={`${c.id}-cc`} x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor={paint(c, '#3f3027')} />
						<stop offset="1" stopColor={paint(c, '#6a5242')} />
					</linearGradient>
					<clipPath id={`${c.id}-ccclip`}>
						<path d={body} />
					</clipPath>
					<filter id={`${c.id}-ccglow`} x="-20%" y="-200%" width="140%" height="500%">
						<feGaussianBlur stdDeviation="7" />
					</filter>
				</defs>
				<path d={warp(CC_TAIL, f)} fill={paint(c, '#3a2c24')} />
				<path d={warp(CC_DORSAL1, f)} fill={paint(c, '#3a2c24')} />
				<path d={warp(CC_DORSAL2, f)} fill={paint(c, '#3a2c24')} />
				<path d={warp(CC_PELVIC, f)} fill={paint(c, '#3a2c24')} />
				{glow > 0 ? (
					<path d={warp(CC_BELLY, f)} stroke="#7dffb0" strokeWidth={30} fill="none" opacity={0.55 * glow} filter={`url(#${c.id}-ccglow)`} />
				) : null}
				<path d={body} fill={`url(#${c.id}-cc)`} />
				<g clipPath={`url(#${c.id}-ccclip)`}>
					{glow > 0 ? <path d={warp(CC_BELLY, f)} stroke="#9dffc4" strokeWidth={14} fill="none" opacity={0.9 * glow} /> : null}
					{collar ? <path d={warp('M 772 60 L 812 60 L 812 200 L 772 200 Z', f)} fill="#140d09" /> : null}
				</g>
				<path d={warp(CC_PEC, f)} fill={paint(c, '#33261f')} />
				{c.sil ? null : (
					<g>
						<circle cx={ex} cy={ey} r={15} fill="#d9f7e6" />
						<circle cx={ex + 2} cy={ey} r={9} fill="#0c1a12" />
						<circle cx={ex + 5} cy={ey - 4} r={3} fill="#ffffff" />
						{open ? (
							<g>
								<ellipse cx={mx - 6} cy={my + 4} rx={22} ry={16} fill="#2a1a14" stroke="#8a5a4a" strokeWidth={5} />
								<path d={`M ${mx - 22} ${my + 10} L ${mx - 16} ${my - 2} L ${mx - 10} ${my + 10} L ${mx - 4} ${my - 2} L ${mx + 2} ${my + 10} L ${mx + 8} ${my - 2} L ${mx + 12} ${my + 10} Z`} fill="#f2efe6" />
							</g>
						) : (
							<path d={`M ${mx - 40} ${my - 2} C ${mx - 24} ${my + 6} ${mx - 10} ${my + 6} ${mx + 4} ${my}`} stroke="#1b120d" strokeWidth={4} fill="none" strokeLinecap="round" />
						)}
					</g>
				)}
			</g>
		);
	},
};

export const SMALL_SHARKS: Record<string, Figure> = {cookiecutter};
