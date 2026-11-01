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

export const Explosion: React.FC<{size: number; rot?: number; core?: number}> = ({size, rot = 0, core = 0}) => {
	const R = size / 2;
	return (
		<g transform={`rotate(${rot})`}>
			<circle r={R * 0.8} fill="url(#glowOrange)" opacity={0.8} />
			{core > 0 && <circle r={R * 0.68} fill="#EF6A26" opacity={core} />}
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

/** Target board in 3/4 view: a squashed face ellipse, a visible dark rim thickness on the left,
 *  and bullet holes with crack stars (holes appear at their t0). */
export const Target: React.FC<{holes: [number, number, number][]; t: number}> = ({holes, t}) => {
	const R = 262;
	const sq = 0.8; // 3/4 squash of the face
	const th = 34; // rim thickness seen on the left side
	return (
		<g>
			{/* tripod */}
			<path d="M-40,150 L-150,560" stroke="#6E4B3A" strokeWidth={22} strokeLinecap="round" />
			<path d="M40,150 L150,560" stroke="#6E4B3A" strokeWidth={22} strokeLinecap="round" />
			<path d="M0,160 L10,600" stroke="#5A3B2C" strokeWidth={20} strokeLinecap="round" />
			<path d="M-40,150 L-150,560" stroke="#8A6450" strokeWidth={6} strokeLinecap="round" transform="translate(-6 0)" />
			<path d="M-96,360 L96,360" stroke="#5A3B2C" strokeWidth={12} strokeLinecap="round" />
			{/* rim thickness: back face + the band joining it to the front face */}
			<ellipse cx={-th} cy={0} rx={R * sq} ry={R} fill="#141B21" />
			<rect x={-th} y={-R} width={th} height={2 * R} fill="#1A232A" />
			<path d={`M${-th},${-R} A${R * sq},${R} 0 0 0 ${-th},${R} L0,${R} A${R * sq},${R} 0 0 1 0,${-R} Z`} fill="#1E2830" />
			<path d={`M${-th + 4},${-R + 40} A${R * sq - 10},${R - 40} 0 0 0 ${-th + 4},${R - 40}`} stroke="#3A4852" strokeWidth={4} fill="none" opacity={0.7} />
			<g transform={`scale(${sq} 1)`}>
				<circle r={R} fill="#2F3B45" />
				<circle r={R - 6} fill="#26313A" />
				<circle r={214} fill="#FFFFFF" />
				<circle r={164} fill="#5DADE2" />
				<circle r={116} fill="#E74C3C" />
				<circle r={66} fill="#F7C548" />
				<circle r={24} fill="#E8A52E" />
				{/* light falloff to the right + a lit upper-left rim */}
				<path d={`M0,-${R - 6} A${R - 6},${R - 6} 0 0 1 ${R - 6},0 L214,0 A214,214 0 0 0 0,-214 Z`} fill="#000" opacity={0.07} />
				<path d={`M${-R + 14},-40 A${R - 14},${R - 14} 0 0 1 -40,${-R + 14}`} stroke="#4B5B67" strokeWidth={6} fill="none" strokeLinecap="round" />
				{holes.map(([hx, hy, t0], i) => {
					if (t < t0) return null;
					const pop = t0 > 0 ? E.outBack(clamp((t - t0) / 0.12)) : 1;
					return (
						<g key={i} transform={`translate(${hx / sq} ${hy}) scale(${pop})`}>
							<path d={starHole(i)} fill="#C9CED3" opacity={0.75} />
							{[0, 1, 2, 3, 4].map((k) => {
								const a = k * 1.3 + i;
								const L = 26 + hash(i * 7 + k) * 22;
								return <path key={k} d={`M0,0 L${Math.cos(a) * L},${Math.sin(a) * L}`} stroke="#222" strokeWidth={2.4} strokeLinecap="round" opacity={0.75} />;
							})}
							<circle r={10} fill="#151515" />
							<circle cx={-2} cy={-2} r={3} fill="#4A4A4A" />
						</g>
					);
				})}
			</g>
		</g>
	);
};
function starHole(i: number) {
	const pts: string[] = [];
	for (let k = 0; k < 10; k++) {
		const a = (k * Math.PI) / 5 + i;
		const r = k % 2 ? 7 : 16 + hash(i * 10 + k) * 6;
		pts.push(`${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}`);
	}
	return `M${pts.join(' L')} Z`;
}

/** v3 Czech hedgehog: three chunky shaded beams (two crossed in the picture plane, one receding),
 *  each with a lit top face, a dark underside, rounded ends showing a lighter cut face, and bolts. */
export const Hedgehog: React.FC<{x: number; y: number; s?: number; flip?: boolean}> = ({x, y, s = 1, flip}) => {
	const beam = (a: number, L: number, w: number, c: string, key: string, back?: boolean) => (
		<g key={key} transform={`rotate(${a})`}>
			<rect x={-L / 2} y={-w / 2} width={L} height={w} rx={w * 0.22} fill={c} />
			{/* lit top face */}
			<rect x={-L / 2 + 6} y={-w / 2} width={L - 12} height={w * 0.3} rx={w * 0.14} fill="#9C928A" opacity={back ? 0.5 : 0.9} />
			<rect x={-L / 2 + 10} y={-w / 2 + 3} width={L * 0.55} height={w * 0.08} rx={3} fill="#C9C0B6" opacity={back ? 0.3 : 0.8} />
			{/* dark underside */}
			<rect x={-L / 2} y={w * 0.18} width={L} height={w * 0.32} rx={w * 0.14} fill="#000" opacity={0.22} />
			{/* cut faces at the ends */}
			<rect x={-L / 2} y={-w / 2} width={w * 0.34} height={w} rx={w * 0.17} fill="#8A8079" />
			<rect x={L / 2 - w * 0.34} y={-w / 2} width={w * 0.34} height={w} rx={w * 0.17} fill="#8A8079" />
			<circle cx={-L / 2 + w * 0.17} cy={0} r={w * 0.09} fill="#4A423C" />
		</g>
	);
	return (
		<g transform={`translate(${x} ${y}) scale(${(flip ? -1 : 1) * s} ${s})`}>
			<ellipse cx={0} cy={112} rx={210} ry={20} fill="url(#softShadow)" />
			{/* receding beam (behind) */}
			<g transform="translate(10 18) scale(0.62 1)">{beam(-82, 250, 62, '#4E4640', 'r', true)}</g>
			{beam(-40, 330, 70, '#625850', 'a')}
			{beam(40, 330, 70, '#7A7068', 'b')}
			{/* gusset plate + bolts at the crossing */}
			<path d="M-30,-6 L0,-34 L30,-6 L0,22 Z" fill="#544B44" />
			<circle cx={-8} cy={-6} r={5} fill="#2E2925" />
			<circle cx={10} cy={-4} r={5} fill="#2E2925" />
		</g>
	);
};

/** v3 explosion: a layered cloud burst. Tapered flame petals in three tones, overlapping fire-cloud
 *  circles, dark smoke puffs and flying debris. `k` 0..1 is its life (grow, hold, break up). */
export const Burst: React.FC<{size: number; k: number; seed?: number; rot?: number}> = ({size, k, seed = 3, rot = 0}) => {
	const R = size / 2;
	const grow = E.outBack(clamp(k / 0.3));
	const fade = 1 - clamp((k - 0.65) / 0.35);
	const petals = (n: number, r: number, w: number, c: string, off: number) => {
		let d = '';
		for (let i = 0; i < n; i++) {
			const a = off + (i / n) * Math.PI * 2;
			const rr = r * (0.78 + 0.32 * hash(seed + i * 3.7 + n));
			const c1 = [Math.cos(a - w) * rr * 0.45, Math.sin(a - w) * rr * 0.45];
			const c2 = [Math.cos(a + w) * rr * 0.45, Math.sin(a + w) * rr * 0.45];
			const tip = [Math.cos(a) * rr, Math.sin(a) * rr];
			d += `M0,0 Q${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${tip[0].toFixed(1)},${tip[1].toFixed(1)} Q${c2[0].toFixed(1)},${c2[1].toFixed(1)} 0,0 Z `;
		}
		return <path d={d} fill={c} />;
	};
	const puffs = Array.from({length: 9}, (_, i) => {
		const a = (i / 9) * Math.PI * 2 + hash(seed + i) * 0.5;
		const d = R * (0.28 + hash(seed + i * 2) * 0.16) * (0.8 + 0.4 * k);
		return [Math.cos(a) * d, Math.sin(a) * d * 0.85, R * (0.2 + hash(seed + i * 5) * 0.12)] as const;
	});
	const smoke = Array.from({length: 7}, (_, i) => {
		const a = -Math.PI / 2 + (hash(seed + i * 11) - 0.5) * 2.6;
		const d = R * (0.35 + 0.55 * clamp((k - 0.15) / 0.85)) * (0.7 + hash(seed + i) * 0.5);
		return [Math.cos(a) * d, Math.sin(a) * d - R * 0.15 * k, R * (0.16 + hash(seed + i * 7) * 0.1) * (0.6 + k)] as const;
	});
	const debris = Array.from({length: 10}, (_, i) => {
		const a = (i / 10) * Math.PI * 2 + hash(seed + i * 13);
		const d = R * (0.3 + 1.1 * clamp(k / 0.8)) * (0.7 + hash(seed + i * 17) * 0.6);
		return [Math.cos(a) * d, Math.sin(a) * d + R * 0.5 * k * k, hash(seed + i) * 360 + k * 500, 8 + hash(seed + i * 19) * 12] as const;
	});
	return (
		<g transform={`rotate(${rot})`}>
			<circle r={R * 1.05 * grow} fill="url(#glowOrange)" opacity={0.7 * fade} />
			{/* smoke behind */}
			<g opacity={0.85 * clamp(k / 0.2)}>
				{smoke.map(([x, y, r], i) => (
					<g key={i}>
						<circle cx={x} cy={y} r={r} fill="#6E4A4E" />
						<circle cx={x - r * 0.2} cy={y - r * 0.25} r={r * 0.6} fill="#8A6266" />
					</g>
				))}
			</g>
			<g transform={`scale(${grow})`} opacity={fade}>
				{petals(11, R, 0.2, '#E8542A', 0.1)}
				{petals(9, R * 0.78, 0.24, '#F7931E', 0.45)}
				{puffs.map(([x, y, r], i) => (
					<circle key={`p${i}`} cx={x} cy={y} r={r} fill={i % 3 === 0 ? '#F7931E' : '#F9A93A'} />
				))}
				{puffs.map(([x, y, r], i) => (
					<circle key={`q${i}`} cx={x * 0.7 - r * 0.15} cy={y * 0.7 - r * 0.2} r={r * 0.62} fill="#FFD34D" />
				))}
				{petals(7, R * 0.42, 0.3, '#FFE58A', 0.2)}
				<circle r={R * 0.16} fill="#FFF6D6" />
			</g>
			{debris.map(([x, y, r, w], i) => (
				<rect key={`d${i}`} x={x - w / 2} y={y - w / 3} width={w} height={w * 0.66} rx={2} fill={i % 3 ? '#3A2522' : '#5A3532'} transform={`rotate(${r} ${x} ${y})`} opacity={clamp((1 - k) * 3)} />
			))}
		</g>
	);
};

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

/** Ammo/equipment crate: lid seam, inset panel with bevels, corner protectors, latches with lit edges,
 *  a handle and a stencil strip. */
export const Crate: React.FC<{x: number; y: number; w: number; h: number; c?: string; dk?: string; hi?: string}> = ({x, y, w, h, c = '#6D7142', dk = '#4E5338', hi = '#7F8452'}) => {
	const latch = (lx: number) => (
		<g transform={`translate(${lx} ${h * 0.13})`}>
			<rect x={-10} y={-4} width={20} height={34} rx={4} fill="#3A3D2C" />
			<rect x={-10} y={-4} width={20} height={5} rx={2} fill="#9A9C86" />
			<rect x={-6} y={8} width={12} height={16} rx={3} fill="#2A2C20" />
			<circle cx={0} cy={26} r={3} fill="#B8B9A6" />
		</g>
	);
	const corner = (cx: number, cy: number, sx: number, sy: number) => (
		<path key={`${cx}${cy}`} transform={`translate(${cx} ${cy}) scale(${sx} ${sy})`} d="M0,0 L34,0 L34,10 L10,10 L10,34 L0,34 Z" fill={dk} />
	);
	return (
		<g transform={`translate(${x} ${y})`}>
			<rect x={0} y={0} width={w} height={h} rx={12} fill={c} />
			<rect x={0} y={0} width={w} height={10} rx={5} fill={hi} />
			{/* lid seam */}
			<rect x={0} y={h * 0.22} width={w} height={8} fill={dk} />
			<rect x={0} y={h * 0.22 + 8} width={w} height={3} fill={hi} opacity={0.6} />
			{/* inset panel: dark top/left bevel, lit bottom/right bevel */}
			<rect x={w * 0.08} y={h * 0.34} width={w * 0.84} height={h * 0.56} rx={8} fill={dk} opacity={0.45} />
			<rect x={w * 0.08 + 6} y={h * 0.34 + 6} width={w * 0.84 - 6} height={h * 0.56 - 6} rx={6} fill={c} />
			<rect x={w * 0.08 + 6} y={h * 0.9 - 4} width={w * 0.84 - 6} height={4} rx={2} fill={hi} opacity={0.7} />
			{/* stencil strip */}
			<rect x={w * 0.16} y={h * 0.42} width={w * 0.28} height={9} rx={2} fill="#C9C59A" opacity={0.55} />
			<rect x={w * 0.16} y={h * 0.42 + 14} width={w * 0.18} height={7} rx={2} fill="#C9C59A" opacity={0.45} />
			{/* handle */}
			<path d={`M${w * 0.4},${h * 0.56} L${w * 0.4},${h * 0.68} Q${w * 0.4},${h * 0.75} ${w * 0.47},${h * 0.75} L${w * 0.6},${h * 0.75} Q${w * 0.67},${h * 0.75} ${w * 0.67},${h * 0.68} L${w * 0.67},${h * 0.56}`} fill="none" stroke={dk} strokeWidth={10} strokeLinecap="round" />
			{/* corners */}
			{corner(0, 0, 1, 1)}
			{corner(w, 0, -1, 1)}
			{corner(0, h, 1, -1)}
			{corner(w, h, -1, -1)}
			{latch(w * 0.18)}
			{latch(w * 0.82)}
			<rect x={w - 18} y={0} width={18} height={h} rx={9} fill="#000" opacity={0.12} />
		</g>
	);
};
