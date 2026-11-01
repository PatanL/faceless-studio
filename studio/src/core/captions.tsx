import React, {useMemo} from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp01} from './anim';
import {fontFamily} from './fonts';
import {SAFE_AREA, type Captions, type Format, type Theme, type Word} from './schema';

export type CaptionPage = {words: Word[]; start: number; end: number};

const PUNCT_END = /[.!?…,;:]["')\]]?$/;

/**
 * Group words into short pages (1-3 words): break on maxWords, maxChars, a pause longer
 * than gapBreak, or after punctuation. A page shows from its first word until the next
 * page starts (or `linger` after its last word).
 */
export function paginate(words: Word[], c: Pick<Captions, 'maxWords' | 'maxChars' | 'gapBreak' | 'linger'>): CaptionPage[] {
	const sorted = [...words].filter((w) => w.text.trim()).sort((a, b) => a.start - b.start);
	const pages: {words: Word[]}[] = [];
	let cur: Word[] = [];
	const flush = () => {
		if (cur.length) pages.push({words: cur});
		cur = [];
	};
	sorted.forEach((w, i) => {
		const prev = sorted[i - 1];
		const chars = cur.reduce((n, x) => n + x.text.length + 1, 0) + w.text.length;
		if (cur.length && (cur.length >= c.maxWords || chars > c.maxChars || (prev && w.start - prev.end > c.gapBreak))) {
			flush();
		}
		cur.push(w);
		if (PUNCT_END.test(w.text.trim())) flush();
	});
	flush();
	return pages.map((p, i) => {
		const start = p.words[0].start;
		const last = p.words[p.words.length - 1].end;
		const next = pages[i + 1]?.words[0].start;
		const end = next !== undefined && next - last <= c.linger ? next : last + c.linger;
		return {words: p.words, start, end};
	});
}

export const CaptionTrack: React.FC<{captions: Captions; format: Format; theme: Theme}> = ({captions, format, theme}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const pages = useMemo(() => paginate(captions.words, captions), [captions]);
	if (!captions.enabled) return null;
	const t = frame / fps;
	const page = pages.find((p) => t >= p.start && t < p.end);
	if (!page) return null;

	const st = captions.style;
	const vertical = format === '9:16';
	const safe = SAFE_AREA[format];
	const fontSize = st.fontSize ?? (vertical ? 104 : 84);
	const maxWidth = st.maxWidth ?? Math.min(width * 0.82, width - safe.left - safe.right);
	// keep the caption block inside the safe band
	const yFrac = st.y ?? (vertical ? 0.64 : 0.82);
	const yMin = safe.top + fontSize;
	const yMax = height - safe.bottom - fontSize * 0.6;
	const cy = Math.max(yMin, Math.min(yMax, yFrac * height));
	// shift a little left on 9:16 so the right-hand action buttons never cover text
	const cx = vertical ? width / 2 - (safe.right - safe.left) / 4 : width / 2;

	const popF = Math.round((t - page.start) * fps);
	const pop = st.pop ? spring({frame: popF, fps, config: {damping: 14, stiffness: 260, mass: 0.6}}) : 1;
	const scale = 0.82 + 0.18 * pop;
	const lift = (1 - pop) * 26;

	return (
		<div
			style={{
				position: 'absolute',
				left: cx,
				top: cy,
				width: maxWidth,
				transform: `translate(-50%, -50%) translateY(${lift}px) scale(${scale})`,
				display: 'flex',
				flexWrap: 'wrap',
				justifyContent: 'center',
				alignItems: 'center',
				columnGap: fontSize * 0.36,
				rowGap: fontSize * 0.04,
				textAlign: 'center',
				fontFamily: fontFamily(st.font, theme),
				fontWeight: st.weight,
				fontSize,
				lineHeight: 1.08,
				letterSpacing: '-0.01em',
			}}
		>
			{page.words.map((w, i) => {
				const next = page.words[i + 1];
				const active = t >= w.start && (next ? t < next.start : t < page.end);
				const spoken = t >= w.start;
				const wf = Math.round((t - w.start) * fps);
				const wPop = active ? spring({frame: wf, fps, config: {damping: 12, stiffness: 300, mass: 0.5}}) : 1;
				const hl = active && st.highlightMode !== 'none';
				const color = hl && st.highlightMode === 'color' ? st.highlight : st.color;
				const text = st.uppercase ? w.text.toUpperCase() : w.text;
				return (
					<span
						key={i}
						style={{
							position: 'relative',
							display: 'inline-block',
							isolation: 'isolate',
							color,
							opacity: spoken ? 1 : 0.92,
							transform: `scale(${hl ? 1 + 0.06 * clamp01(wPop) : 1})`,
							WebkitTextStroke: `${st.strokeWidth}px ${st.strokeColor}`,
							paintOrder: 'stroke fill',
							textShadow: st.shadow ? `0 ${fontSize * 0.07}px 0 rgba(0,0,0,0.55), 0 0 ${fontSize * 0.3}px rgba(0,0,0,0.35)` : undefined,
							padding: st.highlightMode === 'box' ? `0 ${fontSize * 0.12}px` : undefined,
						}}
					>
						{hl && st.highlightMode === 'box' ? (
							<span
								style={{
									position: 'absolute',
									inset: `${fontSize * 0.02}px 0`,
									background: st.boxColor,
									borderRadius: fontSize * 0.14,
									transform: `scale(${0.7 + 0.3 * clamp01(wPop)})`,
									zIndex: -1,
								}}
							/>
						) : null}
						{text}
					</span>
				);
			})}
		</div>
	);
};
