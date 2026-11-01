// Shared drawing helpers for thumbnails: tapered strokes, scratchboard "engraving" fill,
// film grain, vignette, sonar rings, the red hand-drawn pointer and the headline.
import React from 'react';
import {RED} from './spec';
import {measureEm} from './measure';

export type Pt = [number, number];

/** Seeded PRNG so stills are deterministic. */
export function rng(seed: number) {
	let s = seed >>> 0 || 1;
	return () => {
		s = (s * 1664525 + 1013904223) >>> 0;
		return s / 4294967296;
	};
}

/** Closed path around a centreline whose width tapers from w0 to w1 (with optional bulge). */
export function taper(points: Pt[], w0: number, w1: number, bulge = 0): string {
	const n = points.length;
	const left: Pt[] = [];
	const right: Pt[] = [];
	for (let i = 0; i < n; i++) {
		const [x, y] = points[i];
		const [ax, ay] = points[Math.max(0, i - 1)];
		const [bx, by] = points[Math.min(n - 1, i + 1)];
		let dx = bx - ax;
		let dy = by - ay;
		const len = Math.hypot(dx, dy) || 1;
		dx /= len;
		dy /= len;
		const u = i / (n - 1);
		const w = (w0 + (w1 - w0) * u + bulge * Math.sin(Math.PI * u)) / 2;
		left.push([x - dy * w, y + dx * w]);
		right.push([x + dy * w, y - dx * w]);
	}
	const f = (p: Pt) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`;
	return `M${left.map(f).join(' L')} L${right.reverse().map(f).join(' L')} Z`;
}

/** Sample a cubic bezier into points. */
export function bezier(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n = 40): Pt[] {
	const out: Pt[] = [];
	for (let i = 0; i <= n; i++) {
		const t = i / n;
		const m = 1 - t;
		out.push([
			m * m * m * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t * t * t * p3[0],
			m * m * m * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t * t * t * p3[1],
		]);
	}
	return out;
}

/** Shared <defs>: grain + speckle filters, hatch patterns. Put once per thumbnail SVG. */
export const FxDefs: React.FC<{id: string}> = ({id}) => (
	<defs>
		<filter id={`${id}-grain`} x="0" y="0" width="100%" height="100%">
			<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={7} result="n" />
			<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.05" />
		</filter>
		{/* white specks, for scratchboard texture inside shapes */}
		<filter id={`${id}-speckle`} x="0" y="0" width="100%" height="100%">
			<feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves={3} seed={3} result="n" />
			<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 9 -5.2" />
		</filter>
		<pattern id={`${id}-hatch`} width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-28)">
			<line x1="0" y1="1" x2="7" y2="1" stroke="#fff" strokeWidth="2.2" />
		</pattern>
		<pattern id={`${id}-hatch2`} width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
			<line x1="0" y1="1" x2="9" y2="1" stroke="#fff" strokeWidth="1.6" />
		</pattern>
		<pattern id={`${id}-dots`} width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(15)">
			<circle cx="3" cy="3" r="1.1" fill="#fff" />
		</pattern>
	</defs>
);

/**
 * Scratchboard / engraving fill for a shape: black body, white hatching that is dense where
 * the light hits (`light` = gradient direction, 0..1 box units), speckle texture, white rim.
 */
export const Engraved: React.FC<{
	id: string;
	fx: string;
	d: string;
	light?: {x1: number; y1: number; x2: number; y2: number};
	strength?: number;
	rim?: number;
	base?: string;
	cross?: boolean;
}> = ({id, fx, d, light = {x1: 0.5, y1: 0, x2: 0.5, y2: 1}, strength = 1, rim = 3, base = '#070707', cross = true}) => (
	<g>
		<defs>
			<clipPath id={`${id}-clip`}>
				<path d={d} />
			</clipPath>
			<linearGradient id={`${id}-lg`} x1={light.x1} y1={light.y1} x2={light.x2} y2={light.y2}>
				<stop offset="0" stopColor="#fff" stopOpacity={0.95 * strength} />
				<stop offset="0.45" stopColor="#fff" stopOpacity={0.55 * strength} />
				<stop offset="1" stopColor="#fff" stopOpacity={0.04} />
			</linearGradient>
			<linearGradient id={`${id}-lg2`} x1={light.x1} y1={light.y1} x2={light.x2} y2={light.y2}>
				<stop offset="0" stopColor="#fff" stopOpacity={0.8 * strength} />
				<stop offset="0.35" stopColor="#fff" stopOpacity={0.15} />
				<stop offset="1" stopColor="#fff" stopOpacity={0} />
			</linearGradient>
			<mask id={`${id}-m`} maskContentUnits="userSpaceOnUse">
				<path d={d} fill={`url(#${id}-lg)`} />
			</mask>
			<mask id={`${id}-m2`} maskContentUnits="userSpaceOnUse">
				<path d={d} fill={`url(#${id}-lg2)`} />
			</mask>
		</defs>
		<path d={d} fill={base} />
		<g clipPath={`url(#${id}-clip)`}>
			<g mask={`url(#${id}-m)`}>
				<rect x="-400" y="-400" width="1900" height="1900" fill={`url(#${fx}-hatch)`} />
			</g>
			{cross && (
				<g mask={`url(#${id}-m2)`}>
					<rect x="-400" y="-400" width="1900" height="1900" fill={`url(#${fx}-hatch2)`} />
					<rect x="-400" y="-400" width="1900" height="1900" fill="#fff" opacity={0.18} />
				</g>
			)}
			<g mask={`url(#${id}-m)`} opacity={0.7}>
				<rect x="-400" y="-400" width="1900" height="1900" filter={`url(#${fx}-speckle)`} />
			</g>
		</g>
		{rim > 0 && <path d={d} fill="none" stroke="#f4f4f4" strokeWidth={rim} strokeLinejoin="round" opacity={0.9} />}
	</g>
);

export const Grain: React.FC<{fx: string; w: number; h: number; opacity?: number}> = ({fx, w, h, opacity = 0.09}) => (
	<rect width={w} height={h} filter={`url(#${fx}-grain)`} opacity={opacity} style={{mixBlendMode: 'screen'}} />
);

export const Vignette: React.FC<{id: string; w: number; h: number; strength?: number; color?: string}> = ({
	id,
	w,
	h,
	strength = 0.85,
	color = '#000',
}) => (
	<>
		<defs>
			<radialGradient id={`${id}-vig`} cx="0.5" cy="0.5" r="0.75">
				<stop offset="0.45" stopColor={color} stopOpacity={0} />
				<stop offset="1" stopColor={color} stopOpacity={strength} />
			</radialGradient>
		</defs>
		<rect width={w} height={h} fill={`url(#${id}-vig)`} />
	</>
);

/** Concentric sonar arcs around (cx, cy). */
export const Sonar: React.FC<{cx: number; cy: number; r0: number; step: number; n?: number; from?: number; to?: number}> = ({
	cx,
	cy,
	r0,
	step,
	n = 5,
	from = 120,
	to = 240,
}) => {
	const arc = (r: number) => {
		const a0 = (from * Math.PI) / 180;
		const a1 = (to * Math.PI) / 180;
		return `M${cx + r * Math.cos(a0)} ${cy + r * Math.sin(a0)} A${r} ${r} 0 0 1 ${cx + r * Math.cos(a1)} ${cy + r * Math.sin(a1)}`;
	};
	return (
		<g fill="none" stroke="#fff" strokeLinecap="round">
			{Array.from({length: n}, (_, i) => (
				<path key={i} d={arc(r0 + i * step)} strokeWidth={Math.max(2, 7 - i)} opacity={0.75 - i * 0.12} />
			))}
		</g>
	);
};

/** Hand-drawn red pointer from a to b with a slight bend. */
export const RedArrow: React.FC<{a: Pt; b: Pt; bend?: number; width?: number}> = ({a, b, bend = 0.25, width = 16}) => {
	const [ax, ay] = a;
	const [bx, by] = b;
	const dx = bx - ax;
	const dy = by - ay;
	const len = Math.hypot(dx, dy);
	const nx = -dy / len;
	const ny = dx / len;
	const c1: Pt = [ax + dx * 0.3 + nx * len * bend, ay + dy * 0.3 + ny * len * bend];
	const c2: Pt = [ax + dx * 0.75 + nx * len * bend * 0.6, ay + dy * 0.75 + ny * len * bend * 0.6];
	const head = width * 3.4;
	// stop the shaft a little before the tip so the head covers it
	const pts = bezier(a, c1, c2, b, 50);
	const tip = pts[pts.length - 1];
	const prev = pts[pts.length - 6];
	const ang = Math.atan2(tip[1] - prev[1], tip[0] - prev[0]);
	const shaft = pts.slice(0, pts.length - 4);
	const h1: Pt = [tip[0] - head * Math.cos(ang - 0.5), tip[1] - head * Math.sin(ang - 0.5)];
	const h2: Pt = [tip[0] - head * Math.cos(ang + 0.5), tip[1] - head * Math.sin(ang + 0.5)];
	return (
		<g fill={RED} stroke="none">
			<path d={taper(shaft, width * 0.55, width, width * 0.25)} />
			<path d={taper([h1, tip], width * 0.7, width * 0.9)} />
			<path d={taper([h2, tip], width * 0.7, width * 0.9)} />
			<circle cx={tip[0]} cy={tip[1]} r={width * 0.45} />
		</g>
	);
};

// ------------------------------------------------------------------- headline

/** Rough advance widths (em) for Montserrat 900 uppercase. Good enough to fit 2-4 words. */
const WIDE = new Set(['M', 'W']);
const NARROW = new Set(['I', '!', "'", '.', ',', ':', '1']);
export function textWidthEm(s: string): number {
	const m = measureEm(s);
	if (m !== null) return m;
	let w = 0;
	for (const ch of s) {
		if (ch === ' ') w += 0.28;
		else if (WIDE.has(ch)) w += 0.98;
		else if (NARROW.has(ch)) w += 0.36;
		else if (ch === '?') w += 0.62;
		else w += 0.74;
	}
	return w;
}

/** Split into at most `maxLines` balanced lines (explicit "\n" wins). */
export function splitLines(text: string, maxLines: number): string[] {
	if (text.includes('\n')) return text.split('\n').map((s) => s.trim());
	const words = text.trim().split(/\s+/);
	if (maxLines <= 1 || words.length <= 1) return [words.join(' ')];
	let best: string[] = [words.join(' ')];
	let bestScore = textWidthEm(best[0]);
	const tryLines = (n: number) => {
		// brute-force break positions (<= 4 words, so tiny)
		const combos = (start: number, left: number): string[][] => {
			if (left === 1) return [[words.slice(start).join(' ')]];
			const out: string[][] = [];
			for (let i = start + 1; i <= words.length - left + 1; i++) {
				for (const rest of combos(i, left - 1)) out.push([words.slice(start, i).join(' '), ...rest]);
			}
			return out;
		};
		for (const c of combos(0, n)) {
			const score = Math.max(...c.map(textWidthEm)) * Math.pow(1.18, n - 1);
			if (score < bestScore) {
				best = c;
				bestScore = score;
			}
		}
	};
	for (let n = 2; n <= Math.min(maxLines, words.length); n++) tryLines(n);
	return best;
}

export type HeadlineBox = {x: number; y: number; w: number; h: number; align?: 'left' | 'center' | 'right'; maxLines?: number};

/**
 * 2-4 word headline in Montserrat 900, white with a heavy black outline + shadow, the accent
 * word in red. Sized to fill the box. Returns <g>; also reports the accent word's box via
 * `onAccent` so a pointer can start from it.
 */
export function layoutHeadline(text: string, accent: string | undefined, box: HeadlineBox) {
	const lines = splitLines(text.toUpperCase(), box.maxLines ?? 2);
	const lh = 1.0;
	const widest = Math.max(...lines.map(textWidthEm));
	const size = Math.min(box.w / widest, box.h / (lines.length * lh));
	const acc = (accent ?? text.trim().split(/\s+/).slice(-1)[0]).toUpperCase().split(/\s+/);
	const blockH = lines.length * size * lh;
	const top = box.y + (box.h - blockH) / 2;
	const align = box.align ?? 'left';
	let accentBox: {x: number; y: number; w: number; h: number} | null = null;
	const rows = lines.map((line, li) => {
		const lw = textWidthEm(line) * size;
		const x0 = align === 'left' ? box.x : align === 'right' ? box.x + box.w - lw : box.x + (box.w - lw) / 2;
		const baseline = top + (li + 0.82) * size * lh;
		const words = line.split(' ');
		let cx = x0;
		const spans = words.map((wd, wi) => {
			const ww = textWidthEm(wd) * size;
			const isAcc = acc.includes(wd.replace(/[^A-Z0-9']/g, '')) || acc.includes(wd);
			if (isAcc && !accentBox) accentBox = {x: cx, y: baseline - size * 0.74, w: ww, h: size * 0.74};
			const span = {text: wd + (wi < words.length - 1 ? ' ' : ''), red: isAcc};
			cx += ww + textWidthEm(' ') * size;
			return span;
		});
		return {x: x0, baseline, spans};
	});
	return {size, rows, accentBox: accentBox as {x: number; y: number; w: number; h: number} | null, top, bottom: top + blockH};
}

export const Headline: React.FC<{layout: ReturnType<typeof layoutHeadline>; stroke?: number}> = ({layout, stroke}) => {
	const sw = stroke ?? layout.size * 0.11;
	const font: React.CSSProperties = {
		fontFamily: '"Montserrat", "Arial Black", sans-serif',
		fontWeight: 900,
		fontSize: layout.size,
			};
	const row = (r: (typeof layout.rows)[number], i: number, mode: 'shadow' | 'stroke' | 'fill') => (
		<text
			key={`${mode}${i}`}
			x={r.x + (mode === 'shadow' ? layout.size * 0.04 : 0)}
			y={r.baseline + (mode === 'shadow' ? layout.size * 0.06 : 0)}
			style={font}
			xmlSpace="preserve"
			fill={mode === 'fill' ? '#fff' : '#000'}
			stroke={mode === 'fill' ? 'none' : '#000'}
			strokeWidth={mode === 'stroke' ? sw : mode === 'shadow' ? sw : 0}
			strokeLinejoin="round"
			opacity={mode === 'shadow' ? 0.55 : 1}
		>
			{r.spans.map((s, j) => (
				<tspan key={j} fill={mode === 'fill' ? (s.red ? RED : '#ffffff') : '#000'}>
					{s.text}
				</tspan>
			))}
		</text>
	);
	return (
		<g>
			{layout.rows.map((r, i) => row(r, i, 'shadow'))}
			{layout.rows.map((r, i) => row(r, i, 'stroke'))}
			{layout.rows.map((r, i) => row(r, i, 'fill'))}
		</g>
	);
};
