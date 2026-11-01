/**
 * Infographic pieces for the explainer kit: headline, tag, stat callout, scale bar,
 * timer, options list, speed bars, height-chart wall and map. Each one fills its layer
 * box and animates from its own `at` (scene-local seconds); `out` fades it away.
 */
import React, {useId} from 'react';
import type {KitComponent} from '../../core/registry';
import {FigureSVG, getFigure, makeCtx, realSize} from './creature';
import {LAND as MAP_LAND, PLACES} from './mapdata';
import {arr, backOut, bool, C, clamp, easeInOut, easeOut, fmtNum, num, prog, safeId, smooth, str, track, type Pt} from './util';

const fadeOut = (props: Record<string, unknown>, time: number) =>
	typeof props.out === 'number' ? 1 - prog(time, props.out, num(props.outDur, 0.3)) : 1;

const colorOf = (v: unknown, d: string) => (v === 'red' ? C.red : v === 'yellow' ? C.yellow : v === 'green' ? C.green : str(v, d));
const flexAlign = (a: string) => (a === 'left' ? 'flex-start' : a === 'right' ? 'flex-end' : 'center');

// ---------------------------------------------------------------- headline

/** Big uppercase title, optional red underline that draws on. props: text, sub, color, size, underline, align, at, out */
export const Headline: KitComponent = ({props, time}) => {
	const at = num(props.at, 0);
	// at <= 0: already in place on the first frame (frame 0 is the Shorts cover), no entrance
	const p = at <= 0 ? 1 : easeOut(prog(time, at, 0.35));
	const u = at <= 0 ? 1 : easeOut(prog(time, at + 0.15, 0.45));
	const size = num(props.size, 56);
	const color = colorOf(props.color, C.white);
	const align = str(props.align, 'center');
	const o = p * fadeOut(props, time);
	if (o <= 0) return null;
	return (
		<div style={{width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: flexAlign(align), justifyContent: 'center', opacity: o, transform: `translateY(${(1 - p) * 18}px)`}}>
			<div
				style={{
					position: 'relative',
					fontFamily: C.font,
					fontWeight: 900,
					fontSize: size,
					color,
					letterSpacing: '0.03em',
					textTransform: 'uppercase',
					textAlign: align as 'left',
					lineHeight: 1.1,
					textShadow: '0 4px 18px rgba(0,0,0,0.55)',
					whiteSpace: 'pre-line',
				}}
			>
				{str(props.text, '')}
				{bool(props.underline, false) ? (
					<div style={{position: 'absolute', left: 0, bottom: -size * 0.16, height: Math.max(3, size * 0.07), width: `${u * 100}%`, background: color, borderRadius: 2}} />
				) : null}
			</div>
			{typeof props.sub === 'string' ? (
				<div style={{marginTop: size * 0.4, fontFamily: C.font, fontWeight: 700, fontSize: size * 0.42, color: C.muted, letterSpacing: '0.14em', textTransform: 'uppercase'}}>{props.sub}</div>
			) : null}
		</div>
	);
};

// ---------------------------------------------------------------- tag

/** Dark fact tag that slides in (at <= 0: in place on frame 0). props: text, size, color, bg, at, out, align */
export const Tag: KitComponent = ({props, time}) => {
	const at = num(props.at, 0);
	const p = at <= 0 ? 1 : easeOut(prog(time, at, 0.3));
	const o = p * fadeOut(props, time);
	if (o <= 0) return null;
	const size = num(props.size, 28);
	const accent = colorOf(props.accent, C.red);
	return (
		<div style={{width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: flexAlign(str(props.align, 'left'))}}>
			<div
				style={{
					opacity: o,
					transform: `translateX(${(1 - p) * -28}px)`,
					background: str(props.bg, C.panel),
					border: `1.5px solid ${C.panelLine}`,
					borderLeft: `${Math.max(4, size * 0.2)}px solid ${accent}`,
					borderRadius: 6,
					padding: `${size * 0.42}px ${size * 0.8}px`,
					fontFamily: C.font,
					fontWeight: 900,
					fontSize: size,
					letterSpacing: '0.06em',
					color: colorOf(props.color, C.white),
					textTransform: 'uppercase',
					whiteSpace: 'nowrap',
					boxShadow: '0 10px 30px rgba(0,0,0,0.35)',
				}}
			>
				{str(props.text, '')}
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- stat

/**
 * Counting stat callout: "~6,500 / CODAS ANALYSED". props: value, from, prefix, suffix, decimals, label, labelSize,
 * size, color (value; default white), rule (red underline under the value, default true), pulse (seconds between
 * slow red ring pulses, off by default), box, at, duration, align
 */
export const Stat: KitComponent = ({props, time}) => {
	const at = num(props.at, 0);
	const dur = num(props.duration, 1.2);
	const p = easeOut(prog(time, at, 0.3));
	const o = p * fadeOut(props, time);
	if (o <= 0) return null;
	const v = num(props.from, 0) + (num(props.value, 0) - num(props.from, 0)) * easeOut(prog(time, at, dur));
	const size = num(props.size, 96);
	const box = bool(props.box, true);
	const color = colorOf(props.color, C.white);
	const align = str(props.align, 'center');
	const rule = bool(props.rule, true);
	const pulse = num(props.pulse, 0);
	const ph = pulse > 0 && time >= at ? ((time - at) % pulse) / pulse : -1;
	return (
		<div style={{width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: flexAlign(align)}}>
			<div
				style={{
					position: 'relative',
					opacity: o,
					transform: `scale(${0.85 + 0.15 * backOut(prog(time, at, 0.4))})`,
					background: box ? C.panel : undefined,
					border: box ? `1.5px solid ${C.panelLine}` : undefined,
					borderRadius: 12,
					padding: box ? `${size * 0.22}px ${size * 0.45}px ${size * 0.26}px` : 0,
					textAlign: 'center',
					boxShadow: box ? '0 14px 40px rgba(0,0,0,0.4)' : undefined,
				}}
			>
				<div style={{fontFamily: C.font, fontWeight: 900, fontSize: size, color, lineHeight: 1, fontVariantNumeric: 'tabular-nums', textShadow: box ? undefined : '0 4px 18px rgba(0,0,0,0.5)'}}>
					{str(props.prefix, '')}
					{fmtNum(v, num(props.decimals, 0))}
					{str(props.suffix, '')}
				</div>
				{rule ? <div style={{height: Math.max(4, size * 0.06), width: `${easeOut(prog(time, at + 0.1, 0.45)) * 70}%`, margin: `${size * 0.1}px auto 0`, background: C.red, borderRadius: 3}} /> : null}
				{typeof props.label === 'string' ? (
					<div style={{marginTop: size * 0.16, fontFamily: C.font, fontWeight: 800, fontSize: num(props.labelSize, Math.max(16, size * 0.24)), color: C.white, letterSpacing: '0.14em', textTransform: 'uppercase'}}>{props.label}</div>
				) : null}
				{ph >= 0 ? (
					<div style={{position: 'absolute', inset: -size * 0.12, border: `${Math.max(4, size * 0.05)}px solid ${C.red}`, borderRadius: 18, opacity: 0.8 * (1 - ph), transform: `scale(${1 + 0.18 * easeOut(ph)})`}} />
				) : null}
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- scale bar

/** Measuring bar with end ticks and a label ("~16 M"). Box width = bar length. props: label, at, duration, from ("center"|"left"), color, labelSize, thickness */
export const ScaleBar: KitComponent = ({props, time, width: W, height: H}) => {
	const at = num(props.at, 0);
	const p = easeInOut(prog(time, at, num(props.duration, 0.6)));
	const o = fadeOut(props, time);
	if (time < at || o <= 0) return null;
	const color = colorOf(props.color, C.white);
	const th = num(props.thickness, 4);
	const y = num(props.barY, H * 0.3);
	const fromLeft = str(props.from, 'center') === 'left';
	const x0 = fromLeft ? 0 : (W / 2) * (1 - p);
	const x1 = fromLeft ? W * p : W / 2 + (W / 2) * p;
	const ls = num(props.labelSize, 40);
	const lp = easeOut(prog(time, at + num(props.duration, 0.6) * 0.6, 0.3));
	return (
		<svg width={W} height={H} style={{overflow: 'visible', display: 'block', opacity: o}}>
			<line x1={x0} x2={x1} y1={y} y2={y} stroke={color} strokeWidth={th} strokeLinecap="round" />
			{bool(props.ticks, true) ? (
				<>
					<line x1={x0} x2={x0} y1={y - 14} y2={y + 14} stroke={color} strokeWidth={th} strokeLinecap="round" opacity={p} />
					<line x1={x1} x2={x1} y1={y - 14} y2={y + 14} stroke={color} strokeWidth={th} strokeLinecap="round" opacity={p} />
				</>
			) : null}
			<text x={W / 2} y={y + ls * 1.45} textAnchor="middle" fill={color} fontFamily={C.font} fontWeight={900} fontSize={ls} letterSpacing={ls * 0.06} opacity={lp} style={{filter: 'drop-shadow(0 3px 8px rgba(0,0,0,0.6))'}}>
				{str(props.label, '')}
			</text>
		</svg>
	);
};

// ---------------------------------------------------------------- timer

const fmtClock = (s: number, mode: string) => {
	if (mode === 's') return String(Math.ceil(s));
	const c = Math.ceil(s);
	return `${Math.floor(c / 60)}:${String(c % 60).padStart(2, '0')}`;
};

/** Countdown. props: from, to, at, rate (x realtime), label, style ("box"|"ring"), format ("mm:ss"|"s"), warnBelow, size */
export const Timer: KitComponent = ({props, time, width: W, height: H}) => {
	const at = num(props.at, 0);
	const appear = easeOut(prog(time, at - 0.3, 0.3));
	const o = appear * fadeOut(props, time);
	if (o <= 0) return null;
	const from = num(props.from, 10);
	const to = num(props.to, 0);
	const rem = Math.max(to, from - Math.max(0, time - at) * num(props.rate, 1));
	const warn = rem <= num(props.warnBelow, -1);
	const frac = rem - Math.floor(rem);
	const pulse = warn ? 1 + 0.08 * Math.pow(frac, 6) : 1;
	const color = warn ? C.red : C.white;
	const size = num(props.size, 120);
	const label = str(props.label, '');
	const mode = str(props.format, 'mm:ss');
	if (str(props.style, 'box') === 'ring') {
		const r = Math.min(W, H) * 0.36;
		const cx = W / 2;
		const cy = H / 2 - (label ? 18 : 0);
		const f = clamp((rem - to) / Math.max(0.001, from - to));
		const circ = 2 * Math.PI * r;
		return (
			<svg width={W} height={H} style={{opacity: o, overflow: 'visible', display: 'block'}}>
				<circle cx={cx} cy={cy} r={r + 22} fill={C.panel} />
				<circle cx={cx} cy={cy} r={r} fill="none" stroke="rgba(255,255,255,0.12)" strokeWidth={10} />
				<circle cx={cx} cy={cy} r={r} fill="none" stroke={C.red} strokeWidth={10} strokeLinecap="round" strokeDasharray={`${circ * f} ${circ}`} transform={`rotate(-90 ${cx} ${cy})`} />
				<text x={cx} y={cy + size * 0.35} textAnchor="middle" fill={color} fontFamily={C.font} fontWeight={900} fontSize={size} style={{fontVariantNumeric: 'tabular-nums'}} transform={`translate(${cx} ${cy}) scale(${pulse}) translate(${-cx} ${-cy})`}>
					{fmtClock(rem, mode)}
				</text>
				{label ? (
					<text x={cx} y={cy + r + 64} textAnchor="middle" fill={C.muted} fontFamily={C.font} fontWeight={800} fontSize={size * 0.2} letterSpacing={size * 0.03}>
						{label.toUpperCase()}
					</text>
				) : null}
			</svg>
		);
	}
	return (
		<div style={{width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: o}}>
			<div
				style={{
					background: C.panel,
					border: `2px solid ${warn ? C.red : C.panelLine}`,
					borderRadius: 14,
					padding: `${size * 0.16}px ${size * 0.38}px ${size * 0.2}px`,
					textAlign: 'center',
					boxShadow: warn ? `0 0 ${40 * Math.pow(frac, 4)}px rgba(229,72,61,0.6)` : '0 14px 40px rgba(0,0,0,0.4)',
				}}
			>
				{label ? <div style={{fontFamily: C.font, fontWeight: 800, fontSize: size * 0.2, color: C.muted, letterSpacing: '0.16em'}}>{label.toUpperCase()}</div> : null}
				<div style={{fontFamily: C.font, fontWeight: 900, fontSize: size, color, lineHeight: 1.05, fontVariantNumeric: 'tabular-nums', transform: `scale(${pulse})`}}>{fmtClock(rem, mode)}</div>
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- options list

/** "YOUR OPTIONS" list. props: title, items[], at, stagger, strikes [{index, at}], select {index, at} | [..], size */
export const Options: KitComponent = ({props, time}) => {
	const at = num(props.at, 0);
	const stagger = num(props.stagger, 0.18);
	const size = num(props.size, 44);
	const items = arr<string>(props.items);
	const strikes = arr<{index: number; at: number}>(props.strikes);
	const selects = Array.isArray(props.select) ? arr<{index: number; at: number}>(props.select) : props.select ? [props.select as {index: number; at: number}] : [];
	const o = easeOut(prog(time, at, 0.3)) * fadeOut(props, time);
	if (o <= 0) return null;
	return (
		<div style={{width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', opacity: o}}>
			<div style={{fontFamily: C.font, fontWeight: 900, fontSize: size * 1.15, color: C.white, letterSpacing: '0.06em', marginBottom: size * 0.7, textTransform: 'uppercase'}}>
				{str(props.title, 'Your options')}
			</div>
			<div style={{display: 'flex', flexDirection: 'column', gap: size * 0.42, alignItems: 'stretch'}}>
				{items.map((it, i) => {
					const ip = easeOut(prog(time, at + 0.15 + i * stagger, 0.3));
					const st = strikes.find((s) => s.index === i);
					const sp = st ? easeInOut(prog(time, st.at, 0.35)) : 0;
					const se = selects.find((s) => s.index === i);
					const sel = se ? backOut(prog(time, se.at, 0.35)) : 0;
					return (
						<div
							key={i}
							style={{
								position: 'relative',
								opacity: ip * (1 - 0.55 * sp),
								transform: `translateX(${(1 - ip) * -30}px)`,
								fontFamily: C.font,
								fontWeight: 900,
								fontSize: size,
								color: sp > 0.5 ? '#c9a5a2' : C.white,
								letterSpacing: '0.04em',
								textTransform: 'uppercase',
								padding: `${size * 0.22}px ${size * 0.5}px`,
								whiteSpace: 'nowrap',
							}}
						>
							{sel > 0 ? (
								<div
									style={{
										position: 'absolute',
										inset: 0,
										border: `3px solid ${C.red}`,
										background: 'rgba(229,72,61,0.18)',
										borderRadius: 8,
										transform: `scale(${0.9 + 0.1 * sel})`,
										opacity: clamp(sel),
									}}
								/>
							) : null}
							<span style={{position: 'relative'}}>
								{i + 1}. {it}
								{sp > 0 ? <span style={{position: 'absolute', left: -6, top: '52%', height: Math.max(4, size * 0.1), width: `calc(${sp * 100}% + 12px)`, background: C.red, borderRadius: 3}} /> : null}
							</span>
						</div>
					);
				})}
			</div>
		</div>
	);
};

// ---------------------------------------------------------------- speed bars

/** Horizontal bar comparison. props: title, rows [{label, value, unit, color, text}], max, at, duration, stagger, size */
export const SpeedBars: KitComponent = ({props, time, width: W}) => {
	const at = num(props.at, 0);
	const dur = num(props.duration, 0.9);
	const stagger = num(props.stagger, 0.25);
	const size = num(props.size, 30);
	const rows = arr<{label: string; value: number; unit?: string; color?: string; text?: string}>(props.rows);
	const max = num(props.max, Math.max(1, ...rows.map((r) => r.value)));
	const o = easeOut(prog(time, at, 0.3)) * fadeOut(props, time);
	if (o <= 0) return null;
	const labelW = num(props.labelWidth, W * 0.3);
	const valueW = size * 6;
	const barMax = W - labelW - valueW - size;
	return (
		<div style={{width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', opacity: o, fontFamily: C.font}}>
			{typeof props.title === 'string' ? (
				<div style={{fontWeight: 900, fontSize: size * 1.3, color: C.white, letterSpacing: '0.06em', marginBottom: size * 0.9, textTransform: 'uppercase'}}>{props.title}</div>
			) : null}
			{rows.map((r, i) => {
				const p = easeOut(prog(time, at + 0.2 + i * stagger, dur));
				const v = r.value * p;
				const w = Math.max(size * 0.4, (r.value / max) * barMax * p);
				const col = colorOf(r.color, i === 0 ? C.white : C.cyan);
				return (
					<div key={i} style={{display: 'flex', alignItems: 'center', marginBottom: size * 0.7, opacity: easeOut(prog(time, at + i * stagger, 0.25))}}>
						<div style={{width: labelW, fontWeight: 800, fontSize: size * 0.8, color: C.muted, letterSpacing: '0.1em', textTransform: 'uppercase', paddingRight: size * 0.6, boxSizing: 'border-box', textAlign: 'right'}}>{r.label}</div>
						<div style={{position: 'relative', width: barMax, height: size * 0.9, background: 'rgba(255,255,255,0.07)', borderRadius: size}}>
							<div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: w, background: col, borderRadius: size, boxShadow: `0 0 18px ${col}55`}} />
							<div style={{position: 'absolute', left: w + size * 0.5, top: '50%', transform: 'translateY(-50%)', fontWeight: 900, fontSize: size, color: C.white, whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums'}}>
								{r.text ?? `~${fmtNum(v)} ${r.unit ?? 'km/h'}`}
							</div>
						</div>
					</div>
				);
			})}
		</div>
	);
};

// ---------------------------------------------------------------- height chart wall

/**
 * Lineup wall with metre lines; figures stand on the floor at true relative height.
 * props: maxM, stepM, entries [{kind, label, heightM?, pose?, at, color?, silhouette?}], at, title, size
 */
export const HeightChart: KitComponent = ({props, time, width: W, height: H}) => {
	const id = safeId(useId());
	const at = num(props.at, 0);
	const wall = easeOut(prog(time, at, 0.4)) * fadeOut(props, time);
	if (wall <= 0) return null;
	const maxM = num(props.maxM, 4);
	const step = num(props.stepM, 0.5);
	const size = num(props.size, 26);
	const axisW = size * 3.4;
	const floor = H - size * 2.8;
	const entries = arr<{kind: string; label?: string; heightM?: number; pose?: string; at?: number; color?: string; silhouette?: string | boolean}>(props.entries);
	// Size each figure by its real height, then pick one px-per-metre that fits both the wall
	// height and the summed figure widths, so wide animals never overlap.
	const laid = entries.map((e) => {
		const f = getFigure(e.kind, e.pose);
		if (!f) return null;
		const hM = e.heightM ?? realSize(f).h;
		return {e, f, hM, aspect: f.box[2] / f.box[3]};
	});
	const gap = num(props.gap, size * 2.2);
	const avail = W - axisW - size * 1.5 - gap * Math.max(0, entries.length - 1);
	const sumW = laid.reduce((a, l) => a + (l ? l.hM * l.aspect : 0), 0);
	const ppmH = (floor - size * 3.2) / maxM;
	const ppm = Math.min(ppmH, sumW > 0 ? avail / sumW : ppmH);
	const top = floor - maxM * ppm;
	const used = laid.reduce((a, l) => a + (l ? l.hM * l.aspect * ppm : 0), 0) + gap * Math.max(0, entries.length - 1);
	let cursor = axisW + size * 0.75 + (W - axisW - size * 1.5 - used) / 2;
	const centers = laid.map((l) => {
		const w = l ? l.hM * l.aspect * ppm : 0;
		const c = cursor + w / 2;
		cursor += w + gap;
		return c;
	});
	const lines: React.ReactNode[] = [];
	for (let m = 0; m <= maxM + 1e-6; m += step) {
		const y = floor - m * ppm;
		const major = Math.abs(m - Math.round(m)) < 1e-6;
		const lp = easeOut(prog(time, at + 0.1 + m * 0.05, 0.4));
		lines.push(
			<g key={m} opacity={lp}>
				<line x1={axisW} x2={axisW + (W - axisW) * lp} y1={y} y2={y} stroke={major ? 'rgba(220,240,245,0.32)' : 'rgba(220,240,245,0.12)'} strokeWidth={major ? 2.5 : 1.5} />
				{major ? (
					<text x={axisW - size * 0.5} y={y + size * 0.35} textAnchor="end" fill={C.muted} fontFamily={C.font} fontWeight={800} fontSize={size}>
						{m} m
					</text>
				) : null}
			</g>,
		);
	}
	return (
		<svg width={W} height={H} style={{display: 'block', overflow: 'visible', opacity: wall}}>
			<defs>
				<linearGradient id={`${id}-wall`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#0b2a36" stopOpacity={0.55} />
					<stop offset="1" stopColor="#041219" stopOpacity={0.85} />
				</linearGradient>
			</defs>
			<rect x={axisW} y={top - size} width={W - axisW} height={floor - top + size} fill={`url(#${id}-wall)`} rx={6} />
			{lines}
			<line x1={axisW - 10} x2={W} y1={floor} y2={floor} stroke="rgba(235,248,250,0.8)" strokeWidth={4} />
			{laid.map((l, i) => {
				if (!l) return null;
				const {e, f} = l;
				const eAt = e.at ?? at + 0.4 + i * 0.35;
				const p = prog(time, eAt, 0.45);
				if (p <= 0) return null;
				const hM = l.hM;
				const hPx = hM * ppm;
				const wPx = hPx * l.aspect;
				const cx = centers[i];
				const grow = backOut(p);
				const ctx = makeCtx({...(e as Record<string, unknown>), silhouette: e.silhouette, color: e.color}, time, `${id}-e${i}`);
				const yTop = floor - hPx;
				const tagO = easeOut(prog(time, eAt + 0.3, 0.3));
				return (
					<g key={i}>
						<line x1={axisW} x2={cx + wPx / 2} y1={yTop} y2={yTop} stroke={C.red} strokeWidth={2.5} strokeDasharray="10 8" opacity={tagO * 0.8} />
						<g transform={`translate(${cx} ${floor}) scale(${grow}) translate(${-cx} ${-floor})`}>
							<FigureSVG f={f} ctx={ctx} x={cx - wPx / 2} y={yTop} w={wPx} h={hPx} />
						</g>
						<g opacity={tagO}>
							<rect x={cx - size * 2} y={yTop - size * 1.9} width={size * 4} height={size * 1.4} rx={size * 0.3} fill={C.red} />
							<text x={cx} y={yTop - size * 0.85} textAnchor="middle" fill="#fff" fontFamily={C.font} fontWeight={900} fontSize={size * 0.8}>
								{hM.toFixed(hM < 10 ? 1 : 0)} M
							</text>
						</g>
						<text x={cx} y={floor + size * 1.6} textAnchor="middle" fill={C.white} fontFamily={C.font} fontWeight={900} fontSize={size} letterSpacing={size * 0.08} opacity={easeOut(p)}>
							{(e.label ?? f.label).toUpperCase()}
						</text>
					</g>
				);
			})}
		</svg>
	);
};

// ---------------------------------------------------------------- map

type View = {lon: number; lat: number; zoom: number};

/**
 * Stylised world map with camera moves, pins and highlight rings.
 * props: view {lon,lat,zoom} or views [{t, lon, lat, zoom}], pins [{place|lon,lat, label, at, color}],
 * rings [{place|lon,lat, r (deg), at, label}], highlight [continent names], landColor, oceanColor, grid
 */
export const MapView: KitComponent = ({props, time, width: W, height: H}) => {
	const id = safeId(useId());
	const o = easeOut(prog(time, num(props.at, 0), 0.4)) * fadeOut(props, time);
	if (o <= 0) return null;
	const views = arr<{t: number; lon?: number; lat?: number; zoom?: number; place?: string}>(props.views).map((v) => {
		const pl = v.place ? PLACES[v.place] : undefined;
		return {t: v.t, v: {lon: pl ? pl[0] : v.lon ?? 0, lat: pl ? pl[1] : v.lat ?? 0, zoom: v.zoom ?? 1}};
	});
	const sv = (props.view as Partial<View>) ?? {};
	let view: View = {lon: sv.lon ?? 0, lat: sv.lat ?? 10, zoom: sv.zoom ?? 1};
	if (views.length) {
		// zoom interpolates in log space so a 1 -> 40 zoom feels even
		const tr = (k: 'lon' | 'lat') => track(views.map((v) => ({t: v.t, v: v.v[k]})), time, 0);
		const z = Math.exp(track(views.map((v) => ({t: v.t, v: Math.log(v.v.zoom)})), time, 0));
		view = {lon: tr('lon'), lat: tr('lat'), zoom: z};
	}
	const base = W / 360; // px per degree at zoom 1
	const k = base * view.zoom;
	const proj = (lon: number, lat: number): Pt => [W / 2 + (lon - view.lon) * k, H / 2 - (lat - view.lat) * k];
	const land = str(props.landColor, '#2d5a55');
	const hl = arr<string>(props.highlight);
	const paths: React.ReactNode[] = [];
	for (const [name, rings] of Object.entries(MAP_LAND)) {
		rings.forEach((ring, j) => {
			const pts = ring.map(([lo, la]) => proj(lo, la));
			const xs = pts.map((p) => p[0]);
			const ys = pts.map((p) => p[1]);
			if (Math.max(...xs) < -50 || Math.min(...xs) > W + 50 || Math.max(...ys) < -50 || Math.min(...ys) > H + 50) return;
			const isHl = hl.includes(name);
			paths.push(
				<path key={`${name}${j}`} d={smooth(pts, true, 0.7)} fill={isHl ? C.red : land} stroke={isHl ? '#ff8a7f' : '#4f8a80'} strokeWidth={2} strokeLinejoin="round" />,
			);
		});
	}
	const grid: React.ReactNode[] = [];
	if (bool(props.grid, true)) {
		const stepDeg = view.zoom > 8 ? 5 : view.zoom > 3 ? 10 : 30;
		for (let lon = -180; lon <= 180; lon += stepDeg) {
			const [x] = proj(lon, 0);
			if (x > -10 && x < W + 10) grid.push(<line key={`a${lon}`} x1={x} x2={x} y1={0} y2={H} stroke="rgba(160,220,235,0.07)" strokeWidth={1.5} />);
		}
		for (let lat = -90; lat <= 90; lat += stepDeg) {
			const [, y] = proj(0, lat);
			if (y > -10 && y < H + 10) grid.push(<line key={`b${lat}`} x1={0} x2={W} y1={y} y2={y} stroke="rgba(160,220,235,0.07)" strokeWidth={1.5} />);
		}
	}
	const where = (e: {place?: string; lon?: number; lat?: number}): Pt => {
		const pl = e.place ? PLACES[e.place] : undefined;
		return proj(pl ? pl[0] : e.lon ?? 0, pl ? pl[1] : e.lat ?? 0);
	};
	const rings = arr<{place?: string; lon?: number; lat?: number; r?: number; at?: number; label?: string; color?: string}>(props.rings).map((r, i) => {
		const p = prog(time, r.at ?? 0, 0.5);
		if (p <= 0) return null;
		const [x, y] = where(r);
		const rad = Math.max(18, (r.r ?? 3) * k) * easeOut(p);
		const pulse = (time * 0.8 + i * 0.3) % 1;
		const col = colorOf(r.color, C.red);
		return (
			<g key={`r${i}`}>
				<circle cx={x} cy={y} r={rad} fill={col} fillOpacity={0.14} stroke={col} strokeWidth={4} />
				<circle cx={x} cy={y} r={rad * (1 + pulse * 0.6)} fill="none" stroke={col} strokeWidth={3} opacity={(1 - pulse) * 0.6 * p} />
				{r.label ? (
					<text x={x + rad + 22} y={y + 16} fill={C.white} fontFamily={C.font} fontWeight={900} fontSize={num(props.labelSize, 46)} letterSpacing={2} opacity={easeOut(prog(time, (r.at ?? 0) + 0.3, 0.3))} style={{filter: 'drop-shadow(0 3px 8px rgba(0,0,0,0.7))'}}>
						{r.label.toUpperCase()}
					</text>
				) : null}
			</g>
		);
	});
	const pins = arr<{place?: string; lon?: number; lat?: number; at?: number; label?: string; color?: string}>(props.pins).map((pn, i) => {
		const p = prog(time, pn.at ?? 0, 0.45);
		if (p <= 0) return null;
		const [x, y] = where(pn);
		const drop = (1 - backOut(p)) * -60;
		const col = colorOf(pn.color, C.red);
		const s = num(props.pinSize, 1);
		return (
			<g key={`p${i}`} transform={`translate(${x} ${y + drop}) scale(${s})`} opacity={clamp(p * 3)}>
				<ellipse cx={0} cy={2} rx={12} ry={5} fill="#000" opacity={0.35} />
				<path d="M 0 0 C -6 -14 -22 -26 -22 -44 C -22 -58 -12 -68 0 -68 C 12 -68 22 -58 22 -44 C 22 -26 6 -14 0 0 Z" fill={col} stroke="#fff" strokeWidth={3} />
				<circle cx={0} cy={-44} r={8} fill="#fff" />
				{pn.label ? (
					<text x={30} y={-36} fill={C.white} fontFamily={C.font} fontWeight={900} fontSize={num(props.labelSize, 40)} letterSpacing={2} style={{filter: 'drop-shadow(0 3px 8px rgba(0,0,0,0.7))'}}>
						{pn.label.toUpperCase()}
					</text>
				) : null}
			</g>
		);
	});
	return (
		<svg width={W} height={H} style={{display: 'block', opacity: o}}>
			<defs>
				<radialGradient id={`${id}-sea`} cx="0.5" cy="0.45" r="0.8">
					<stop offset="0" stopColor={str(props.oceanColor, '#0f3a4a')} />
					<stop offset="1" stopColor="#04121a" />
				</radialGradient>
			</defs>
			<rect width={W} height={H} fill={`url(#${id}-sea)`} />
			{grid}
			{paths}
			{rings}
			{pins}
		</svg>
	);
};
