import React from 'react';
import {P, Cap} from './defs';
import {Flag} from './soldier';
import {E, clamp, hash, rng} from '../lib/anim';

// ------------------------------------------------------------------ sky & clouds
export const Cloud: React.FC<{x: number; y: number; s?: number; seed?: number; c?: string; sh?: string}> = ({x, y, s = 1, seed = 1, c = P.cloud, sh = P.cloudShade}) => {
	const R = rng(seed);
	const n = 6 + Math.floor(R() * 4);
	const circles: [number, number, number][] = [];
	for (let i = 0; i < n; i++) {
		const t = i / (n - 1);
		const cx = (t - 0.5) * 260 + (R() - 0.5) * 30;
		const r = 34 + Math.sin(t * Math.PI) * 34 + R() * 14;
		circles.push([cx, -r * 0.55 + (R() - 0.5) * 12, r]);
	}
	return (
		<g transform={`translate(${x} ${y}) scale(${s})`}>
			{circles.map(([cx, cy, r], i) => (
				<circle key={`s${i}`} cx={cx} cy={cy + 6} r={r} fill={sh} />
			))}
			{circles.map(([cx, cy, r], i) => (
				<circle key={`w${i}`} cx={cx - 4} cy={cy - 6} r={r * 0.9} fill={c} />
			))}
			{circles.slice(1, -1).map(([cx, cy, r], i) => (
				<circle key={`h${i}`} cx={cx - r * 0.25} cy={cy - r * 0.35} r={r * 0.35} fill="#FFFFFF" opacity={0.55} />
			))}
		</g>
	);
};

/** Cloud band that drifts left at ~10 px/s, wrapping across width w. */
export const CloudBand: React.FC<{t: number; items: [number, number, number][]; w: number; x0?: number; speed?: number; c?: string; sh?: string}> = ({t, items, w, x0 = 0, speed = 10, c, sh}) => (
	<g>
		{items.map(([x, y, s], i) => {
			const xx = x0 + ((((x - t * speed - x0) % w) + w) % w);
			return <Cloud key={i} x={xx} y={y} s={s} seed={i * 7 + 3} c={c} sh={sh} />;
		})}
	</g>
);

// ------------------------------------------------------------------ flags on poles
export const PoleFlag: React.FC<{x: number; y: number; h: number; fw: number; kind: 'ru' | 'ua'; t: number; seed?: number}> = ({x, y, h, fw, kind, t, seed = 0}) => {
	const fh = fw * 0.6;
	const sk = Math.sin(t * 2.4 + seed) * 3;
	const sy = 1 + Math.sin(t * 3.1 + seed) * 0.02;
	return (
		<g>
			<rect x={x - 5} y={y - h} width={10} height={h} rx={4} fill="#3A3933" />
			<rect x={x - 5} y={y - h} width={3} height={h} fill="#57564F" />
			<circle cx={x} cy={y - h - 6} r={9} fill="#3A3933" />
			<circle cx={x - 3} cy={y - h - 9} r={3} fill="#77766E" />
			<g transform={`translate(${x + 8} ${y - h + 6}) skewY(${sk}) scale(1 ${sy})`}>
				<Flag kind={kind} x={0} y={0} w={fw} h={fh} r={10} />
				<rect x={4} y={fh - 6} width={fw - 8} height={6} rx={3} fill="#000" opacity={0.08} />
			</g>
		</g>
	);
};

// ------------------------------------------------------------------ FX
export const SPARK_PATH = 'M0,-1 Q0.13,-0.13 1,0 Q0.13,0.13 0,1 Q-0.13,0.13 -1,0 Q-0.13,-0.13 0,-1 Z';

/** 4-point concave sparkle: 0 -> size -> 0 over dur seconds with a spin. */
export const Sparkle: React.FC<{t: number; t0: number; x: number; y: number; size: number; dur?: number; spin?: number}> = ({t, t0, x, y, size, dur = 0.5, spin = 30}) => {
	const u = (t - t0) / dur;
	if (u < 0 || u > 1) return null;
	const k = u < 0.45 ? E.outCubic(u / 0.45) : 1 - E.inCubic((u - 0.45) / 0.55);
	const r = (size / 2) * k;
	return (
		<g transform={`translate(${x} ${y}) rotate(${spin * u - spin / 2}) scale(${r})`}>
			<path d={SPARK_PATH} fill="#FFFFFF" />
		</g>
	);
};

function starPath(n: number, rOut: number, rIn: number, jitter = 0, seed = 0, rot = 0): string {
	const pts: string[] = [];
	for (let i = 0; i < n * 2; i++) {
		const a = rot + (i * Math.PI) / n;
		const r = i % 2 === 0 ? rOut * (1 - jitter * hash(seed + i)) : rIn;
		pts.push(`${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}`);
	}
	return `M${pts.join(' L')} Z`;
}

/** Star-burst muzzle flash, flickering between two shapes every 2-3 frames. */
export const MuzzleFlash: React.FC<{frame: number; size?: number; seed?: number; on?: boolean}> = ({frame, size = 110, seed = 0, on = true}) => {
	if (!on) return null;
	const k = Math.floor((frame + seed) / 2.5);
	if (k % 4 === 3) return null; // brief gaps between bursts
	const v = k % 2;
	const sc = 0.8 + hash(k * 3.1 + seed) * 0.4;
	const R = (size / 2) * sc;
	const rot = v ? 0.2 : 0;
	return (
		<g>
			<circle r={R * 1.1} fill="url(#glowOrange)" opacity={0.6} />
			<path d={starPath(v ? 8 : 7, R, R * 0.38, 0.35, k, rot)} fill="#E8542A" opacity={0.85} />
			<path d={starPath(v ? 8 : 7, R * 0.78, R * 0.3, 0.3, k + 5, rot)} fill="#F7931E" />
			<path d={starPath(v ? 8 : 7, R * 0.45, R * 0.18, 0.2, k + 9, rot + 0.2)} fill="#FFD34D" />
		</g>
	);
};

export const Explosion: React.FC<{size: number; rot?: number}> = ({size, rot = 0}) => {
	const R = size / 2;
	return (
		<g transform={`rotate(${rot})`}>
			<circle r={R * 0.8} fill="url(#glowOrange)" opacity={0.8} />
			<path d={starPath(8, R, R * 0.28, 0.12, 4)} fill="#E8542A" />
			<path d={starPath(8, R * 0.82, R * 0.24, 0.12, 6)} fill="#F7931E" />
			<path d={starPath(8, R * 0.52, R * 0.17, 0.1, 8)} fill="#FFD34D" />
			<circle r={R * 0.12} fill="#FFF3C4" />
		</g>
	);
};

// ------------------------------------------------------------------ UI icons
export const Calendar: React.FC<{text: string}> = ({text}) => (
	<g>
		<g filter="url(#dropSoft)">
			<rect x={0} y={0} width={220} height={196} rx={34} fill="#FDFDFD" />
		</g>
		<rect x={0} y={150} width={220} height={46} rx={30} fill="#EAEAE8" />
		<rect x={0} y={140} width={220} height={30} fill="#FDFDFD" />
		<path d="M0,34 Q0,0 34,0 L186,0 Q220,0 220,34 L220,58 L0,58 Z" fill="#C12B29" />
		<rect x={0} y={50} width={220} height={8} fill="#A82422" />
		{[38, 82, 126, 170].map((x) => (
			<g key={x}>
				<rect x={x - 6} y={-18} width={12} height={40} rx={6} fill="#3B3B3B" />
				<rect x={x - 6} y={-18} width={5} height={40} rx={2.5} fill="#6A6A6A" />
			</g>
		))}
		<text x={110} y={128} textAnchor="middle" fontFamily="MontserratXB, K2D, sans-serif" fontWeight={800} fontSize={60} fill="#C12B29">
			{text}
		</text>
	</g>
);

export const Clipboard: React.FC<{t: number; checks: number[]}> = ({t, checks}) => (
	<g>
		<g filter="url(#dropSoft)">
			<rect x={0} y={0} width={340} height={470} rx={22} fill="#2F3E55" />
		</g>
		<rect x={0} y={0} width={340} height={10} rx={5} fill="#46597A" />
		<rect x={318} y={0} width={22} height={470} rx={11} fill="#000" opacity={0.15} />
		<rect x={26} y={44} width={288} height={400} rx={14} fill="#FDFDFD" />
		<rect x={26} y={420} width={288} height={24} rx={12} fill="#EAEAE8" />
		{/* hand behind the clip */}
		<circle cx={170} cy={34} r={44} fill={P.hand} />
		<path d="M110,30 L230,30 Q236,30 236,38 L232,74 L108,74 L104,38 Q104,30 110,30 Z" fill="#E0A82E" />
		<path d="M118,14 L222,14 Q230,14 230,22 L228,58 L112,58 L110,22 Q110,14 118,14 Z" fill="#F2C94C" />
		<circle cx={170} cy={10} r={22} fill="#F2C94C" />
		<circle cx={170} cy={10} r={9} fill="#2F3E55" />
		{[0, 1, 2].map((i) => {
			const y = 110 + i * 112;
			const tc = checks[i];
			const u = clamp((t - tc) / 0.2);
			const sc = u <= 0 ? 0 : u < 0.6 ? E.outCubic(u / 0.6) * 1.15 : 1.15 - 0.15 * E.inOutCubic((u - 0.6) / 0.4);
			return (
				<g key={i}>
					<rect x={50} y={y} width={76} height={76} rx={16} fill="none" stroke="#D0D0D0" strokeWidth={8} />
					{[0, 1, 2].map((j) => (
						<rect key={j} x={146 + (j === 0 ? 0 : 0)} y={y + 6 + j * 26} width={j === 0 ? 70 : 140} height={10} rx={5} fill="#CFCFCF" />
					))}
					{sc > 0 && (
						<g transform={`translate(88 ${y + 38}) scale(${sc})`}>
							<rect x={-38} y={-38} width={76} height={76} rx={16} fill="#2DB34A" />
							<path d="M-20,0 L-6,15 L22,-16" fill="none" stroke="#FFFFFF" strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" />
						</g>
					)}
				</g>
			);
		})}
	</g>
);

// ------------------------------------------------------------------ set pieces
export const Quonset: React.FC<{x: number; y: number; w: number; h: number; c: string; rim: string; dark: string; door: string; strut: string; doorW?: number; doorHi?: string}> = ({x, y, w, h, c, rim, dark, door, strut, doorW, doorHi}) => {
	const dw = doorW ?? w * 0.34;
	const dh = h * 0.62;
	return (
		<g transform={`translate(${x} ${y})`}>
			<path d={`M${-w / 2},0 L${-w / 2},${-h * 0.35} Q${-w / 2},${-h} 0,${-h} Q${w / 2},${-h} ${w / 2},${-h * 0.35} L${w / 2},0 Z`} fill={rim} />
			<path d={`M${-w / 2 + 22},0 L${-w / 2 + 22},${-h * 0.35} Q${-w / 2 + 22},${-h + 22} 0,${-h + 22} Q${w / 2 - 22},${-h + 22} ${w / 2 - 22},${-h * 0.35} L${w / 2 - 22},0 Z`} fill={c} />
			<path d={`M${w / 2 - 22},0 L${w / 2 - 22},${-h * 0.35} Q${w / 2 - 22},${-h + 40} ${w * 0.18},${-h + 26} Q${w * 0.36},${-h * 0.7} ${w * 0.36},0 Z`} fill={dark} opacity={0.35} />
			{/* struts */}
			<rect x={-w * 0.42} y={-h * 0.62} width={w * 0.84} height={14} rx={7} fill={strut} />
			<rect x={-dw / 2 - 26} y={-h * 0.78} width={14} height={h * 0.78} rx={7} fill={strut} />
			<rect x={dw / 2 + 12} y={-h * 0.78} width={14} height={h * 0.78} rx={7} fill={strut} />
			<rect x={-w * 0.36} y={-h * 0.6} width={12} height={h * 0.6} rx={6} fill={strut} opacity={0.8} />
			<rect x={w * 0.36 - 12} y={-h * 0.6} width={12} height={h * 0.6} rx={6} fill={strut} opacity={0.8} />
			{/* door */}
			<rect x={-dw / 2} y={-dh} width={dw} height={dh} fill={door} />
			{doorHi && <rect x={dw / 2 - 26} y={-dh + 24} width={12} height={dh * 0.7} rx={6} fill={doorHi} />}
			<rect x={-dw / 2} y={-dh} width={dw} height={12} fill="#000" opacity={0.25} />
		</g>
	);
};

export const LatticeTower: React.FC<{x: number; y: number; w: number; h: number; c?: string; levels?: number}> = ({x, y, w, h, c = '#2B2B2B', levels = 4}) => {
	const lv = h / levels;
	const parts: React.ReactNode[] = [];
	for (let i = 0; i < levels; i++) {
		const y0 = -i * lv;
		const y1 = y0 - lv;
		parts.push(<line key={`a${i}`} x1={-w / 2} y1={y0} x2={w / 2} y2={y1} stroke={c} strokeWidth={9} />);
		parts.push(<line key={`b${i}`} x1={w / 2} y1={y0} x2={-w / 2} y2={y1} stroke={c} strokeWidth={9} />);
		parts.push(<rect key={`c${i}`} x={-w / 2} y={y1 - 5} width={w} height={10} fill={c} />);
	}
	return (
		<g transform={`translate(${x} ${y})`}>
			{parts}
			<rect x={-w / 2 - 6} y={-h} width={14} height={h} fill={c} />
			<rect x={w / 2 - 8} y={-h} width={14} height={h} fill={c} />
			<rect x={-w / 2 - 30} y={-h - 26} width={w + 60} height={30} rx={4} fill={c} />
			<rect x={-w / 2 - 30} y={-h - 26} width={w + 60} height={6} rx={3} fill="#4A4A4A" />
		</g>
	);
};

export const Streaks: React.FC<{items: [number, number, number, number?][]; c: string; o?: number}> = ({items, c, o = 1}) => (
	<g opacity={o}>
		{items.map(([x, y, w, h], i) => (
			<Cap key={i} x={x} y={y} w={w} h={h ?? 26} fill={c} />
		))}
	</g>
);

export function streakSet(seed: number, n: number, x0: number, x1: number, y0: number, y1: number, wMin = 80, wMax = 320, h = 26): [number, number, number, number][] {
	const R = rng(seed);
	const out: [number, number, number, number][] = [];
	for (let i = 0; i < n; i++) out.push([x0 + R() * (x1 - x0), y0 + R() * (y1 - y0), wMin + R() * (wMax - wMin), h * (0.7 + R() * 0.6)]);
	return out;
}

export const Target: React.FC<{holes: [number, number, number][]; t: number}> = ({holes, t}) => (
	<g>
		{/* tripod */}
		<path d="M-40,150 L-150,560" stroke="#6E4B3A" strokeWidth={22} strokeLinecap="round" />
		<path d="M40,150 L150,560" stroke="#6E4B3A" strokeWidth={22} strokeLinecap="round" />
		<path d="M0,160 L10,600" stroke="#5A3B2C" strokeWidth={20} strokeLinecap="round" />
		<path d="M-40,150 L-150,560" stroke="#8A6450" strokeWidth={6} strokeLinecap="round" transform="translate(-6 0)" />
		{/* face */}
		<circle r={262} fill="#1F2830" />
		<circle cx={-8} r={252} fill="#2F3B45" />
		<circle cx={-8} r={214} fill="#FFFFFF" />
		<circle cx={-8} r={164} fill="#5DADE2" />
		<circle cx={-8} r={116} fill="#E74C3C" />
		<circle cx={-8} r={66} fill="#F7C548" />
		<path d="M-8,-252 A252,252 0 0 1 244,0 L206,0 A214,214 0 0 0 -8,-214 Z" fill="#000" opacity={0.07} />
		<circle cx={-8} r={24} fill="#E8A52E" />
		{holes.map(([hx, hy, t0], i) =>
			t >= t0 ? (
				<g key={i} transform={`translate(${hx} ${hy})`}>
					<path d={starHole(i)} fill="#9AA0A6" opacity={0.7} />
					<circle r={9} fill="#151515" />
				</g>
			) : null,
		)}
	</g>
);
function starHole(i: number) {
	const pts: string[] = [];
	for (let k = 0; k < 10; k++) {
		const a = (k * Math.PI) / 5 + i;
		const r = k % 2 ? 7 : 16 + hash(i * 10 + k) * 6;
		pts.push(`${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}`);
	}
	return `M${pts.join(' L')} Z`;
}

export const Hedgehog: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<g transform={`translate(${x} ${y}) scale(${s})`}>
		<ellipse cx={0} cy={86} rx={150} ry={14} fill="url(#softShadow)" />
		{[
			[-45, '#625850'],
			[45, '#7A7068'],
		].map(([a, c], i) => (
			<g key={i} transform={`rotate(${a as number})`}>
				<rect x={-150} y={-24} width={300} height={48} rx={24} fill={c as string} />
				<rect x={-130} y={-15} width={200} height={12} rx={6} fill="#A39A90" opacity={0.75} />
				<rect x={-150} y={10} width={300} height={14} rx={7} fill="#000" opacity={0.15} />
			</g>
		))}
	</g>
);

export const Wire: React.FC<{x0: number; x1: number; y: number; sag?: number; seed?: number}> = ({x0, x1, y, sag = 10, seed = 0}) => {
	const barbs = [];
	const n = Math.floor((x1 - x0) / 70);
	for (let i = 0; i <= n; i++) {
		const xx = x0 + (i / n) * (x1 - x0) + (hash(seed + i) - 0.5) * 20;
		const u = (xx - x0) / (x1 - x0);
		const yy = y + Math.sin(u * Math.PI) * sag;
		barbs.push(
			<g key={i} transform={`translate(${xx} ${yy}) rotate(${hash(i + seed) * 30})`}>
				<rect x={-14} y={-4} width={28} height={8} rx={4} fill="#251716" transform="rotate(45)" />
				<rect x={-14} y={-4} width={28} height={8} rx={4} fill="#251716" transform="rotate(-45)" />
			</g>,
		);
	}
	return (
		<g>
			<path d={`M${x0},${y} Q${(x0 + x1) / 2},${y + sag * 2} ${x1},${y}`} fill="none" stroke="#251716" strokeWidth={5} />
			{barbs}
		</g>
	);
};

export const Crate: React.FC<{x: number; y: number; w: number; h: number; c?: string; dk?: string; hi?: string}> = ({x, y, w, h, c = '#6D7142', dk = '#4E5338', hi = '#7F8452'}) => (
	<g transform={`translate(${x} ${y})`}>
		<rect x={0} y={0} width={w} height={h} rx={14} fill={c} />
		<rect x={0} y={0} width={w} height={10} rx={5} fill={hi} />
		<rect x={0} y={h * 0.22} width={w} height={8} fill={dk} />
		<rect x={w * 0.08} y={h * 0.34} width={w * 0.84} height={h * 0.56} rx={10} fill={dk} opacity={0.55} />
		<rect x={w - 18} y={0} width={18} height={h} rx={9} fill="#000" opacity={0.12} />
		{/* handle */}
		<path d={`M${w * 0.38},${h * 0.48} L${w * 0.38},${h * 0.62} Q${w * 0.38},${h * 0.7} ${w * 0.46},${h * 0.7} L${w * 0.54},${h * 0.7} Q${w * 0.62},${h * 0.7} ${w * 0.62},${h * 0.62} L${w * 0.62},${h * 0.48}`} fill="none" stroke={dk} strokeWidth={10} strokeLinecap="round" />
		{/* latches */}
		<rect x={w * 0.14} y={h * 0.12} width={16} height={26} rx={4} fill={dk} />
		<rect x={w * 0.82} y={h * 0.12} width={16} height={26} rx={4} fill={dk} />
	</g>
);
