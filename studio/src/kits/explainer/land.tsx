/**
 * Land / river animals: saltwater crocodile, hippo, grizzly (on all fours or standing).
 * Flat 2D vector style, facing RIGHT.
 */
import React from 'react';
import {paint, type DrawCtx, type Figure} from './figure';
import {num, rnd, swimWarp, warp} from './util';

const Grad: React.FC<{id: string; top: string; bottom: string}> = ({id, top, bottom}) => (
	<linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
		<stop offset="0" stopColor={top} />
		<stop offset="1" stopColor={bottom} />
	</linearGradient>
);

// ================================================================ saltwater crocodile

const CR_BODY =
	'M 20 150 C 120 140 250 118 380 110 C 470 104 560 104 640 112 C 700 118 740 122 780 124 L 958 136 C 984 138 996 146 990 154 C 980 160 950 162 920 162 L 780 164 C 740 170 700 178 640 182 C 540 190 440 188 360 178 C 250 168 120 158 20 152 Z';
const topY = (x: number) => 150 - 46 * Math.pow(Math.max(0, (x - 20) / 620), 0.6);

const leg = (x: number, y: number, back: boolean) =>
	back
		? `M ${x - 30} ${y} C ${x - 40} ${y + 24} ${x - 52} ${y + 44} ${x - 70} ${y + 56} L ${x - 20} ${y + 60} C ${x - 6} ${y + 40} ${x + 6} ${y + 20} ${x + 20} ${y} Z`
		: `M ${x - 20} ${y} C ${x - 18} ${y + 22} ${x - 16} ${y + 40} ${x - 12} ${y + 56} L ${x + 34} ${y + 60} C ${x + 22} ${y + 44} ${x + 18} ${y + 24} ${x + 20} ${y} Z`;

const crocodile: Figure = {
	label: 'SALTWATER CROC',
	box: [20, 96, 976, 150],
	size: 6,
	axis: 'w',
	draw: (c) => {
		const f = c.idle ? swimWarp({head: 700, tail: 20, amp: 9 * c.amp, t: c.t, freq: 0.35 * c.speed, k: 2.4, pow: 1.6}) : undefined;
		const jaw = num(c.p.jaw, 0) + (c.idle ? Math.max(0, Math.sin(c.t * 0.7 * c.speed) - 0.7) * 20 : 0);
		const body = warp(CR_BODY, f);
		const scutes: React.ReactNode[] = [];
		if (!c.sil) {
			for (let x = 40; x < 660; x += 22) {
				const y = topY(x) + 5;
				const h = 6 + 8 * Math.min(1, (x - 20) / 300);
				scutes.push(<path key={x} d={warp(`M ${x - 8} ${y} L ${x} ${y - h} L ${x + 8} ${y} Z`, f)} fill="#454e2b" />);
			}
		}
		const teeth = c.sil
			? null
			: Array.from({length: 13}, (_, i) => {
					const x = 800 + i * 14;
					return <path key={i} d={i % 2 ? `M ${x} 150 L ${x + 4} 160 L ${x + 8} 150 Z` : `M ${x} 152 L ${x + 4} 142 L ${x + 8} 152 Z`} fill="#efe9d6" />;
			  });
		return (
			<g>
				<defs>
					<Grad id={`${c.id}-g`} top={paint(c, '#4c5733')} bottom={paint(c, '#6e7849')} />
					<clipPath id={`${c.id}-clip`}>
						<path d={body} />
					</clipPath>
				</defs>
				<path d={leg(420, 170, true)} fill={paint(c, '#3b4426')} />
				<path d={leg(690, 168, false)} fill={paint(c, '#3b4426')} transform="translate(-30 0)" />
				<g transform={`rotate(${jaw} 780 152)`}>
					<path d="M 780 150 L 960 150 C 980 152 988 158 980 162 C 950 166 860 168 780 168 Z" fill={paint(c, '#6a7446')} />
				</g>
				<path d={body} fill={`url(#${c.id}-g)`} />
				<g clipPath={`url(#${c.id}-clip)`}>
					{c.sil ? null : <path d={warp('M 20 156 C 200 170 420 186 640 180 C 760 176 900 164 1000 156 L 1000 200 L 20 200 Z', f)} fill="#b0a771" opacity={0.75} />}
					{c.sil
						? null
						: Array.from({length: 9}, (_, i) => {
								const x = 70 + i * 34;
								return <path key={i} d={warp(`M ${x} 100 L ${x + 12} 100 L ${x + 12} 200 L ${x} 200 Z`, f)} fill="#2f3720" opacity={0.35} />;
						  })}
				</g>
				{teeth}
				{scutes}
				<path d={leg(400, 172, true)} fill={paint(c, '#55603a')} />
				<path d={leg(680, 168, false)} fill={paint(c, '#55603a')} />
				<circle cx={792} cy={124} r={13} fill={paint(c, '#57623b')} />
				<circle cx={972} cy={138} r={6} fill={paint(c, '#57623b')} />
				{c.sil ? null : (
					<g>
						<ellipse cx={794} cy={121} rx={7} ry={5.5} fill="#d4c85a" />
						<rect x={792.6} y={116} width={2.8} height={10} rx={1.4} fill="#111" />
						<path d="M 780 150 C 840 151 900 151 960 150" stroke="#2b3219" strokeWidth={2.5} fill="none" />
					</g>
				)}
			</g>
		);
	},
};

// ================================================================ hippo

const hippo: Figure = {
	label: 'HIPPO',
	box: [100, 100, 690, 304],
	size: 4.5,
	axis: 'w',
	draw: (c) => {
		const t = c.t * c.speed;
		const yawn = num(c.p.yawn, 0); // 0..1 mouth open
		const breathe = c.idle ? 1 + 0.015 * Math.sin(t * 1.6) : 1;
		const ear = c.idle ? Math.max(0, Math.sin(t * 2.3) - 0.85) * 160 : 0;
		const blink = c.idle && (t % 3.7) < 0.12;
		const jawA = yawn * 38;
		const body =
			'M 120 240 C 115 160 220 110 360 108 C 450 106 520 118 568 134 C 610 118 660 116 700 128 C 740 140 772 174 782 212 C 786 240 772 262 748 268 L 640 262 C 600 290 570 316 520 330 L 220 330 C 160 320 125 290 120 240 Z';
		const leg = (x: number) =>
			`M ${x} 290 L ${x + 72} 290 L ${x + 74} 384 C ${x + 74} 396 ${x + 66} 402 ${x + 56} 402 L ${x + 16} 402 C ${x + 6} 402 ${x - 2} 396 ${x - 2} 384 Z`;
		const legs = (dx: number, col: string, nails: boolean) => (
			<g transform={`translate(${dx} 0)`}>
				<path d={leg(180)} fill={col} />
				<path d={leg(480)} fill={col} />
				{nails && !c.sil
					? [180, 480].map((x) => [0, 1, 2].map((k) => <ellipse key={`${x}${k}`} cx={x + 16 + k * 20} cy={398} rx={7} ry={5} fill="#d8c9cf" />))
					: null}
			</g>
		);
		return (
			<g>
				<defs>
					<Grad id={`${c.id}-g`} top={paint(c, '#77667a')} bottom={paint(c, '#937f8d')} />
				</defs>
				{legs(30, paint(c, '#5f5163'), false)}
				{/* open mouth */}
				{yawn > 0 && !c.sil ? (
					<g>
						<path d="M 640 236 C 700 236 760 230 784 214 C 790 250 770 290 720 300 C 680 300 650 280 640 250 Z" fill="#c76d7a" />
						<path d="M 742 226 L 748 256 L 756 224 Z M 700 236 L 706 262 L 714 236 Z" fill="#f4efe4" />
					</g>
				) : null}
				<g transform={`translate(360 330) scale(1 ${breathe}) translate(-360 -330)`}>
					<path d={body} fill={`url(#${c.id}-g)`} />
					{c.sil ? null : <path d="M 160 300 C 260 326 420 330 560 312 C 540 324 520 330 500 330 L 220 330 C 190 324 172 314 160 300 Z" fill="#c29aa1" opacity={0.6} />}
				</g>
				<g transform={`rotate(${jawA} 640 250)`}>
					<path d="M 640 246 C 690 258 744 260 782 238 C 786 262 770 282 740 288 C 700 294 660 284 640 268 Z" fill={paint(c, '#8a7684')} />
					{c.sil ? null : <path d="M 650 270 C 690 282 740 282 774 262" stroke="#c99aa2" strokeWidth={6} fill="none" opacity={0.6} />}
				</g>
				{legs(0, paint(c, '#7a6878'), true)}
				{c.sil ? null : <path d="M 650 238 C 700 244 750 238 782 222" stroke="#4d3f4c" strokeWidth={4} fill="none" strokeLinecap="round" />}
				<g transform={`rotate(${-ear} 628 120)`}>
					<ellipse cx={620} cy={112} rx={14} ry={20} fill={paint(c, '#6a5969')} transform="rotate(-25 620 112)" />
				</g>
				<circle cx={670} cy={130} r={16} fill={paint(c, '#7d6b7d')} />
				<ellipse cx={756} cy={162} rx={20} ry={13} fill={paint(c, '#7d6b7d')} />
				{c.sil ? null : (
					<g>
						<ellipse cx={754} cy={160} rx={5} ry={3} fill="#3a2d38" />
						{blink ? <path d="M 662 128 L 680 128" stroke="#222" strokeWidth={3} /> : <circle cx={671} cy={128} r={6} fill="#141012" />}
						{!blink ? <circle cx={673} cy={126} r={2} fill="#fff" /> : null}
						<path d="M 120 230 C 108 226 100 236 104 246" stroke="#5f5163" strokeWidth={8} fill="none" strokeLinecap="round" />
					</g>
				)}
			</g>
		);
	},
};

// ================================================================ grizzly

const furStrokes = (c: DrawCtx, n: number, x0: number, y0: number, w: number, h: number, key: string) =>
	c.sil
		? null
		: Array.from({length: n}, (_, i) => {
				const x = x0 + rnd(`${key}x${i}`) * w;
				const y = y0 + rnd(`${key}y${i}`) * h;
				return <path key={i} d={`M ${x} ${y} l -6 14`} stroke="#3e2818" strokeWidth={3} strokeLinecap="round" opacity={0.4} />;
		  });

const grizzlyFours = (c: DrawCtx) => {
	const t = c.t * c.speed;
	const head = c.idle ? Math.sin(t * 1.2) * 2.5 : 0;
	const breathe = c.idle ? 1 + 0.012 * Math.sin(t * 1.7) : 1;
	const body =
		'M 130 240 C 125 175 190 135 290 130 C 370 126 420 92 490 96 C 545 100 585 125 610 156 L 610 400 C 610 410 600 415 585 415 L 545 415 C 540 400 545 380 540 300 C 480 310 360 312 262 300 L 256 400 C 256 410 246 415 232 415 L 192 415 C 186 395 180 360 160 320 C 140 300 132 270 130 240 Z';
	const headP =
		'M 580 150 C 600 130 640 128 670 140 C 700 150 730 164 762 188 C 780 200 784 216 772 226 C 756 236 726 238 700 244 C 670 252 630 252 604 236 C 584 222 572 176 580 150 Z';
	return (
		<g>
			<defs>
				<Grad id={`${c.id}-g`} top={paint(c, '#5c3c24')} bottom={paint(c, '#7a5235')} />
			</defs>
			<g fill={paint(c, '#432c1b')}>
				<path d="M 300 290 L 350 290 L 352 404 C 352 410 346 414 340 414 L 296 414 C 290 400 296 360 300 290 Z" />
				<path d="M 560 280 L 640 280 L 650 404 C 650 410 644 414 638 414 L 590 414 C 586 380 576 330 560 280 Z" />
			</g>
			<g transform={`translate(380 415) scale(1 ${breathe}) translate(-380 -415)`}>
				<path d={body} fill={`url(#${c.id}-g)`} />
				{furStrokes(c, 26, 160, 140, 420, 140, 'gf')}
			</g>
			<g transform={`rotate(${head} 600 190)`}>
				<path d={headP} fill={paint(c, '#6a4529')} />
				<circle cx={622} cy={140} r={16} fill={paint(c, '#5a3a22')} />
				{c.sil ? null : <circle cx={622} cy={142} r={7} fill="#3a2414" />}
				{c.sil ? null : <path d="M 690 214 C 720 206 750 200 772 206 C 780 220 760 234 730 236 C 710 236 696 228 690 214 Z" fill="#9b7452" />}
				{c.sil ? null : <ellipse cx={772} cy={204} rx={10} ry={8} fill="#1b120c" />}
				{c.sil ? null : <circle cx={690} cy={172} r={5.5} fill="#0f0a07" />}
			</g>
			{c.sil
				? null
				: [232, 585].map((x) =>
						[0, 1, 2].map((k) => <path key={`${x}${k}`} d={`M ${x + 6 + k * 9} 412 l 8 6`} stroke="#e7dccb" strokeWidth={3.5} strokeLinecap="round" />),
				  )}
		</g>
	);
};

const grizzlyStanding = (c: DrawCtx) => {
	const t = c.t * c.speed;
	const sway = c.idle ? Math.sin(t * 1.1) * 1.6 : 0;
	const paw = c.idle ? Math.sin(t * 2.2) * 5 : 0;
	const body =
		'M 150 200 C 100 260 90 400 100 520 C 105 620 120 700 140 760 L 130 870 C 130 880 140 885 160 885 L 210 885 C 215 860 215 820 220 770 L 250 770 L 255 870 C 255 880 265 885 285 885 L 320 885 C 320 840 305 780 295 740 C 320 640 320 500 300 380 C 290 300 270 230 240 190 Z';
	const head =
		'M 170 150 C 165 90 210 55 255 60 C 285 63 300 85 305 105 C 330 112 350 125 352 140 C 352 152 340 160 320 160 C 300 175 270 190 230 190 C 195 190 172 175 170 150 Z';
	return (
		<g transform={`rotate(${sway} 220 885)`}>
			<defs>
				<Grad id={`${c.id}-g`} top={paint(c, '#6b472c')} bottom={paint(c, '#553722')} />
			</defs>
			<g transform={`rotate(${-paw} 230 300)`}>
				<path d="M 220 290 C 270 300 310 300 350 290 C 368 288 376 302 366 314 C 330 336 280 350 236 350 Z" fill={paint(c, '#432c1b')} />
			</g>
			<path d={body} fill={`url(#${c.id}-g)`} />
			{furStrokes(c, 30, 120, 220, 170, 480, 'gs')}
			{c.sil ? null : <path d="M 160 300 C 200 280 260 290 290 320 C 300 420 290 560 270 650 C 220 660 170 640 150 610 C 140 520 140 400 160 300 Z" fill="#8a6342" opacity={0.35} />}
			<path d={head} fill={paint(c, '#6a4529')} />
			<circle cx={210} cy={72} r={17} fill={paint(c, '#5a3a22')} />
			{c.sil ? null : (
				<g>
					<circle cx={210} cy={74} r={8} fill="#3a2414" />
					<path d="M 300 128 C 320 120 340 124 352 136 C 352 150 340 158 320 160 C 306 156 298 146 300 128 Z" fill="#9b7452" />
					<ellipse cx={348} cy={136} rx={8} ry={7} fill="#1b120c" />
					<circle cx={268} cy={106} r={5.5} fill="#0f0a07" />
				</g>
			)}
			<g transform={`rotate(${paw} 250 240)`}>
				<path d="M 236 222 C 290 214 330 196 368 184 C 388 180 398 196 388 210 C 352 236 300 262 256 280 Z" fill={paint(c, '#5e3d25')} />
				{c.sil ? null : [0, 1, 2].map((k) => <path key={k} d={`M ${384 + k * 3} ${186 + k * 9} l 14 -2`} stroke="#e7dccb" strokeWidth={3.5} strokeLinecap="round" />)}
			</g>
		</g>
	);
};

const grizzly: Figure = {
	label: 'GRIZZLY',
	box: [125, 96, 659, 322],
	size: 2.4,
	axis: 'w',
	draw: (c) => (c.p.pose === 'standing' ? grizzlyStanding(c) : grizzlyFours(c)),
	poses: {
		standing: {box: [90, 55, 310, 830], size: 2.7, axis: 'h', draw: grizzlyStanding},
	},
};

export const LAND: Record<string, Figure> = {crocodile, hippo, grizzly};
