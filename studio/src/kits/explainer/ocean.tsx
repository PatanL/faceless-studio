/**
 * Ocean background (depth-driven gradient, light rays, marine snow, optional surface)
 * and a depth meter. Both read `depth` as a number or a keyframe track [{t, v}], so a
 * scene can sink the camera and keep the meter in sync.
 */
import React, {useId} from 'react';
import type {KitComponent} from '../../core/registry';
import {bool, C, clamp, fmtNum, num, rnd, safeId, str, arr, track} from './util';

const hex = (h: string): [number, number, number] => {
	const s = h.replace('#', '');
	return [parseInt(s.slice(0, 2), 16), parseInt(s.slice(2, 4), 16), parseInt(s.slice(4, 6), 16)];
};
export const mix = (a: string, b: string, t: number) => {
	const A = hex(a);
	const B = hex(b);
	const k = clamp(t);
	return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * k)).join(',')})`;
};

/** Light level 0..1 at a depth (m). */
export const lightAt = (depth: number, falloff: number) => Math.exp(-Math.max(0, depth) / falloff);

export const Ocean: KitComponent = ({props, time, width: W, height: H}) => {
	const id = safeId(useId());
	const depth = track(props.depth, time, 40);
	const L = lightAt(depth, num(props.falloff, 260)) * num(props.brightness, 1);
	const top = mix('#041820', str(props.topColor, '#2b8197'), L);
	const mid = mix('#03121a', str(props.midColor, '#10465a'), Math.pow(L, 0.8));
	const bottom = mix('#020a0f', str(props.bottomColor, '#071f2b'), Math.pow(L, 0.5));
	const nRays = num(props.rays, 7);
	const nSnow = num(props.snow, 70);
	const seed = num(props.seed, 1);
	const surface = props.surface === true ? 0.28 : typeof props.surface === 'number' ? props.surface : null;
	const sy = surface !== null ? surface * H : 0;
	const rayAlpha = Math.pow(L, 0.7) * num(props.rayStrength, 1);
	const t = time + 30;
	const drift = num(props.drift, 1);

	const rays: React.ReactNode[] = [];
	for (let i = 0; i < nRays; i++) {
		const r = (k: string) => rnd(`ray-${seed}-${i}-${k}`);
		const cx = W * (-0.1 + (1.2 * (i + 0.3 + r('x') * 0.5)) / nRays);
		const tilt = (cx - W / 2) * 0.22 + Math.sin(t * 0.25 + i * 1.7) * 40;
		const w0 = 30 + r('w') * 70;
		const w1 = w0 * (3 + r('s') * 2.5);
		const len = H * (0.75 + r('l') * 0.35);
		const a = (0.45 + 0.55 * Math.abs(Math.sin(t * (0.2 + r('f') * 0.3) + i))) * rayAlpha;
		rays.push(
			<polygon
				key={i}
				points={`${cx - w0 / 2},${sy} ${cx + w0 / 2},${sy} ${cx + tilt + w1 / 2},${sy + len} ${cx + tilt - w1 / 2},${sy + len}`}
				fill={`url(#${id}-ray)`}
				opacity={a}
			/>,
		);
	}

	const snow: React.ReactNode[] = [];
	const spanH = H - sy + 40;
	for (let i = 0; i < nSnow; i++) {
		const r = (k: string) => rnd(`snow-${seed}-${i}-${k}`);
		const size = 0.8 + Math.pow(r('s'), 2.2) * 3.4;
		const vy = (6 + size * 5) * drift;
		const x = (((r('x') * W + Math.sin(t * (0.2 + r('w')) + r('p') * 6) * 18 + t * 4 * drift) % W) + W) % W;
		const y = sy + ((((r('y') * spanH + t * vy) % spanH) + spanH) % spanH) - 20;
		const alpha = (0.18 + r('a') * 0.42) * (0.6 + 0.4 * L);
		snow.push(<circle key={i} cx={x} cy={y} r={size} fill="#cfeef5" opacity={alpha} />);
	}
	const bokeh: React.ReactNode[] = [];
	for (let i = 0; i < Math.round(nSnow / 7); i++) {
		const r = (k: string) => rnd(`bok-${seed}-${i}-${k}`);
		const x = (((r('x') * W + t * 6 * drift) % W) + W) % W;
		const y = sy + ((((r('y') * spanH + t * 3 * drift) % spanH) + spanH) % spanH);
		bokeh.push(<circle key={i} cx={x} cy={y} r={10 + r('r') * 26} fill={`url(#${id}-bokeh)`} opacity={0.35 + 0.4 * r('a')} />);
	}

	const waveY = (x: number) => sy + Math.sin(x / 90 + t * 1.2) * 4 + Math.sin(x / 37 - t * 1.7) * 2;
	let wave = '';
	if (surface !== null) {
		const pts: string[] = [];
		for (let x = -20; x <= W + 20; x += 20) pts.push(`${x},${waveY(x).toFixed(1)}`);
		wave = pts.join(' ');
	}

	return (
		<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{display: 'block'}}>
			<defs>
				<linearGradient id={`${id}-bg`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={top} />
					<stop offset="0.45" stopColor={mid} />
					<stop offset="1" stopColor={bottom} />
				</linearGradient>
				<linearGradient id={`${id}-ray`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#d8f6ff" stopOpacity={0.28} />
					<stop offset="0.6" stopColor="#d8f6ff" stopOpacity={0.07} />
					<stop offset="1" stopColor="#d8f6ff" stopOpacity={0} />
				</linearGradient>
				<radialGradient id={`${id}-glow`} cx="0.5" cy="0" r="0.75">
					<stop offset="0" stopColor="#bdf0ff" stopOpacity={0.42} />
					<stop offset="1" stopColor="#bdf0ff" stopOpacity={0} />
				</radialGradient>
				<radialGradient id={`${id}-bokeh`}>
					<stop offset="0" stopColor="#d6f4ff" stopOpacity={0.1} />
					<stop offset="1" stopColor="#d6f4ff" stopOpacity={0} />
				</radialGradient>
				<radialGradient id={`${id}-vig`} cx="0.5" cy="0.5" r="0.75">
					<stop offset="0.55" stopColor="#000" stopOpacity={0} />
					<stop offset="1" stopColor="#000" stopOpacity={num(props.vignette, 0.55)} />
				</radialGradient>
				<linearGradient id={`${id}-sky`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={str(props.skyTop, '#8f8a80')} />
					<stop offset="1" stopColor={str(props.skyBottom, '#e2d9c6')} />
				</linearGradient>
			</defs>
			<rect x={0} y={sy} width={W} height={H - sy} fill={`url(#${id}-bg)`} />
			<ellipse cx={W / 2} cy={sy} rx={W * 0.7} ry={H * 0.55} fill={`url(#${id}-glow)`} opacity={Math.pow(L, 0.8)} />
			{rays}
			{bokeh}
			{snow}
			{surface !== null ? (
				<g>
					<rect x={0} y={0} width={W} height={sy + 2} fill={`url(#${id}-sky)`} />
					<polygon points={`-20,-20 ${W + 20},-20 ${wave.split(' ').reverse().join(' ')}`} fill={`url(#${id}-sky)`} />
					<polyline points={wave} fill="none" stroke="#e8f6f8" strokeOpacity={0.55} strokeWidth={3} />
					<rect x={0} y={sy} width={W} height={18} fill="#9fd6e0" opacity={0.12} />
				</g>
			) : null}
			<rect x={0} y={0} width={W} height={H} fill={`url(#${id}-vig)`} />
		</svg>
	);
};

/**
 * Vertical depth ruler with a red marker and a big value label.
 * props: max, depth (number | track), step, zones [{from,to,label,color}], window (m, scrolling ruler),
 * side "right"|"left", suffix (e.g. "+"), size (value font px)
 */
export const DepthMeter: KitComponent = ({props, time, width: W, height: H}) => {
	const max = num(props.max, 1000);
	const depth = track(props.depth, time, 0);
	const win = typeof props.window === 'number' ? props.window : null;
	const lo = win ? depth - win / 2 : num(props.min, 0);
	const hi = win ? depth + win / 2 : max;
	const step = num(props.step, (hi - lo) / 5);
	const pad = 30;
	const yOf = (d: number) => pad + ((d - lo) / (hi - lo)) * (H - pad * 2);
	const right = str(props.side, 'right') === 'right';
	const lx = right ? W - 96 : 96;
	const size = num(props.size, 46);
	const accent = str(props.color, C.red);
	const ticks: React.ReactNode[] = [];
	const first = Math.ceil(lo / step) * step;
	for (let d = first; d <= hi + 0.001; d += step) {
		if (d < 0) continue;
		const y = yOf(d);
		ticks.push(
			<g key={d}>
				<line x1={lx - 16} x2={lx} y1={y} y2={y} stroke="rgba(230,245,250,0.55)" strokeWidth={3} />
				<text x={right ? lx + 12 : lx - 12} y={y + 7} fill="rgba(230,245,250,0.55)" fontSize={20} fontFamily={C.font} fontWeight={700} textAnchor={right ? 'start' : 'end'}>
					{fmtNum(d)} m
				</text>
			</g>,
		);
		for (let k = 1; k < 5; k++) {
			const dm = d + (step * k) / 5;
			if (dm > hi) break;
			const ym = yOf(dm);
			ticks.push(<line key={`${d}-${k}`} x1={lx - 8} x2={lx} y1={ym} y2={ym} stroke="rgba(230,245,250,0.3)" strokeWidth={2} />);
		}
	}
	const zones = arr<{from: number; to: number; label?: string; color?: string}>(props.zones).map((z, i) => {
		const y0 = Math.max(pad, yOf(z.from));
		const y1 = Math.min(H - pad, yOf(z.to));
		if (y1 <= y0) return null;
		return (
			<g key={i}>
				<rect x={lx - 10} y={y0} width={10} height={y1 - y0} fill={z.color ?? accent} opacity={0.55} />
				{z.label ? (
					<text x={lx - 30} y={(y0 + y1) / 2 + 8} textAnchor="end" fill={z.color ?? accent} fontSize={22} fontWeight={900} fontFamily={C.font} letterSpacing={2}>
						{z.label}
					</text>
				) : null}
			</g>
		);
	});
	const my = clamp(yOf(depth), pad, H - pad);
	const label = `${fmtNum(Math.round(depth / num(props.round, 1)) * num(props.round, 1))}${str(props.suffix, '')} m`;
	return (
		<svg width={W} height={H} style={{overflow: 'visible', display: 'block'}}>
			<line x1={lx} x2={lx} y1={pad} y2={H - pad} stroke="rgba(230,245,250,0.45)" strokeWidth={3} />
			{zones}
			{ticks}
			{bool(props.marker, true) ? (
				<g transform={`translate(${lx}, ${my})`}>
					<polygon points={right ? '-6,0 -26,-13 -26,13' : '6,0 26,-13 26,13'} fill={accent} />
					<text x={right ? -38 : 38} y={size * 0.36} textAnchor={right ? 'end' : 'start'} fill={C.white} fontSize={size} fontWeight={900} fontFamily={C.font} style={{filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.6))'}}>
						{label}
					</text>
				</g>
			) : null}
		</svg>
	);
};
