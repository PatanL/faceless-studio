import React, {useMemo} from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp01} from './anim';
import {fontFamily} from './fonts';
import {SAFE_AREA, type Captions, type Format, type Scene, type Theme, type Word} from './schema';

export type CaptionPage = {words: Word[]; start: number; end: number};

const PUNCT_END = /[.!?…,;:]["')\]]?$/;
const SENTENCE_END = /[.!?…]["')\]]?$/;
// a caption card never ends on one of these: it is carried to the next card, or the card stretches by one word
const STOPWORDS = new Set(
	"a an the and as of to into onto on in its it's that's about when than with your but or for at from by just every being is".split(' '),
);
const isStop = (w: Word) => STOPWORDS.has(w.text.toLowerCase().replace(/[’]/g, "'").replace(/[^a-z']/g, ''));
// a page never breaks right before these: a lone capital (unit letters "5 A", "6 C"), a number word / numeral,
// or the word after "only" ("only | one" reads wrong on mute)
const NUMWORDS = new Set(
	'one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty sixty seventy eighty ninety hundred hundreds thousand thousands million millions billion half'.split(' '),
);
// a number word glues to a following number or unit: "two | hundred tonnes", "seven | metres"
const UNITS = new Set(
	'metres meters metre meter tonnes tons ton kilos kg km kilometres kilometers cm mm m beats krill times percent minutes seconds hours days years feet miles degrees decibels db'.split(' '),
);
const bare = (w: Word) => w.text.toLowerCase().replace(/[’]/g, "'").replace(/[^a-z0-9']/g, '');
const isNum = (w: Word) => NUMWORDS.has(bare(w)) || /^\d/.test(bare(w));
// two-word compounds a page never splits (plus Captions.glue phrases from the storyboard)
const COMPOUNDS = ['golf cart', 'beach ball', 'jet engine', 'deep dive', 'own body', 'city buses', 'city bus', 'killer whale', 'blue whale'];
const pairsOf = (phrases: string[]) => {
	const out = new Set<string>();
	for (const ph of phrases) {
		const ws = ph.toLowerCase().split(/\s+/).filter(Boolean);
		for (let k = 1; k < ws.length; k++) out.add(`${ws[k - 1]} ${ws[k]}`);
	}
	return out;
};
const glues = (w: Word, prev?: Word) =>
	!!prev &&
	!PUNCT_END.test(prev.text.trim()) &&
	(/^[A-HJ-Z][.,!?:;]?$/.test(w.text.trim()) || isNum(w) || bare(prev) === 'only');
// number + unit and listed compounds: never split, but only up to maxWords+1 words on the page
const binds = (w: Word, prev: Word | undefined, pairs: Set<string>) =>
	!!prev &&
	!PUNCT_END.test(prev.text.trim()) &&
	((isNum(prev) && (isNum(w) || UNITS.has(bare(w)))) || pairs.has(`${bare(prev)} ${bare(w)}`));

/**
 * Group words into short pages (1-3 words): break on maxWords, maxChars, a pause longer
 * than gapBreak, or after punctuation. A page shows from its first word until the next
 * page starts (or `linger` after its last word).
 */
export function paginate(
	words: Word[],
	c: Pick<Captions, 'maxWords' | 'maxChars' | 'gapBreak' | 'linger'> & {glue?: string[]},
): CaptionPage[] {
	const sorted = [...words].filter((w) => w.text.trim()).sort((a, b) => a.start - b.start);
	const pairs = pairsOf([...COMPOUNDS, ...(c.glue ?? [])]);
	const pages: {words: Word[]}[] = [];
	let cur: Word[] = [];
	const flush = (carry = false) => {
		let keep = cur;
		const moved: Word[] = [];
		while (carry && keep.length > 1 && isStop(keep[keep.length - 1])) {
			moved.unshift(keep[keep.length - 1]);
			keep = keep.slice(0, -1);
		}
		if (keep.length) pages.push({words: keep});
		cur = moved;
	};
	if (sorted.some((w) => w.br)) {
		// explicit phrase pages (Word.br): break only where the pipeline said so
		sorted.forEach((w) => {
			if (w.br && cur.length) flush();
			cur.push(w);
		});
		flush();
		return pages.map((p, i) => {
			const last = p.words[p.words.length - 1].end;
			const next = pages[i + 1]?.words[0].start;
			return {words: p.words, start: p.words[0].start, end: next !== undefined && next - last <= c.linger ? next : last + c.linger};
		});
	}
	sorted.forEach((w, i) => {
		const prev = sorted[i - 1];
		const chars = cur.reduce((n, x) => n + x.text.length + 1, 0) + w.text.length;
		const gap = !!prev && w.start - prev.end > c.gapBreak;
		const full = cur.length >= c.maxWords || chars > c.maxChars;
		// page would end on a stopword: let it take one more word (up to maxWords+1 / maxChars+4) ...
		const stretch =
			(cur.length > 0 && isStop(cur[cur.length - 1]) && cur.length <= c.maxWords && chars <= c.maxChars + 4) ||
			(glues(w, prev) && cur.length <= c.maxWords + 1 && chars <= c.maxChars + 6) ||
			(binds(w, prev, pairs) && cur.length <= c.maxWords && chars <= c.maxChars + 6) ||
			// look-ahead: a phrase-final word ("cart.", "body.") joins this page instead of sitting alone on the next
			(PUNCT_END.test(w.text.trim()) && cur.length <= c.maxWords && chars <= c.maxChars + 6);
		if (cur.length && (gap || (full && !stretch))) {
			flush(!gap); // ... or carry the trailing stopword(s) to the next page
		}
		cur.push(w);
		// sentence ends close a page; a comma/colon only once the page has 3+ words ("Signed, Management." stays one page)
		const wt = w.text.trim();
		if (SENTENCE_END.test(wt) ? cur.length >= 2 || wt.length >= 8 : PUNCT_END.test(wt) && cur.length >= 3) flush();
	});
	flush();
	const timed = () =>
		pages.map((p, i) => {
			const start = p.words[0].start;
			const last = p.words[p.words.length - 1].end;
			const next = pages[i + 1]?.words[0].start;
			const end = next !== undefined && next - last <= c.linger ? next : last + c.linger;
			return {words: p.words, start, end};
		});
	// merge flashes: a page shorter than 0.6 s, or a lone word, joins a neighbour when the result has <= 4 words.
	// A sentence-final page joins the previous one; a sentence-initial page joins the next one.
	const MAXM = Math.max(4, c.maxWords);
	const SENT_END = /[.!?…]["')\]]?$/;
	const lastText = (p: {words: Word[]}) => p.words[p.words.length - 1].text.trim();
	for (let guard = 0; guard < 200; guard++) {
		const tp = timed();
		let done = true;
		for (let i = 0; i < tp.length; i++) {
			const p = tp[i];
			if (!(p.end - p.start < 0.6 || p.words.length === 1)) continue;
			// <= 4 words, or 5 when the merged card stays short (it wraps to two lines at most)
			const fits = (q: {words: Word[]}) => {
				const n = q.words.length + p.words.length;
				return n <= MAXM || (n <= MAXM + 1 && [...q.words, ...p.words].reduce((k, x) => k + x.text.length + 1, -1) <= c.maxChars + 8);
			};
			const prevOk = i > 0 && !SENT_END.test(lastText(pages[i - 1])) && fits(pages[i - 1]);
			const nextOk = i < pages.length - 1 && !PUNCT_END.test(lastText(pages[i])) && fits(pages[i + 1]);
			const ends = PUNCT_END.test(lastText(pages[i]));
			const j = ends ? (prevOk ? i - 1 : -1) : nextOk ? i + 1 : prevOk ? i - 1 : -1;
			if (j < 0) {
				// a lone phrase-final word after a full page: take the previous page's tail ("in the middle | of that cloud?")
				const pv = pages[i - 1];
				if (p.words.length === 1 && ends && pv && !PUNCT_END.test(lastText(pv)) && pv.words.length >= 3) {
					const moved: Word[] = [];
					while (pv.words.length > 2 && moved.length < 2 && (moved.length === 0 || isStop(pv.words[pv.words.length - 1])))
						moved.unshift(pv.words.pop() as Word);
					pages[i] = {words: [...moved, ...pages[i].words]};
					done = false;
					break;
				}
				continue;
			}
			const [a, b] = j < i ? [j, i] : [i, j];
			pages.splice(a, 2, {words: [...pages[a].words, ...pages[b].words]});
			done = false;
			break;
		}
		if (done) break;
	}
	return timed();
}

/** Global-time caption y cues from Scene.captionY / captionYAt: [{at, y}] sorted; y undefined = style.y. */
export type CaptionCue = {at: number; y: number | undefined};
export function captionPlacement(scenes: Scene[], timings: {start: number}[], fps: number): CaptionCue[] {
	const cues: CaptionCue[] = [];
	if (!scenes.some((s) => s.captionY !== undefined || s.captionYAt?.length)) return cues;
	scenes.forEach((s, i) => {
		const t0 = timings[i].start / fps;
		cues.push({at: t0, y: s.captionY});
		for (const c of [...(s.captionYAt ?? [])].sort((a, b) => a.at - b.at)) cues.push({at: t0 + c.at, y: c.y});
	});
	return cues.sort((a, b) => a.at - b.at);
}

export const CaptionTrack: React.FC<{captions: Captions; format: Format; theme: Theme; placement?: CaptionCue[]}> = ({
	captions,
	format,
	theme,
	placement,
}) => {
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
	const maxWidth = st.maxWidth ?? Math.min(width * 0.82, width - safe.left - safe.right);
	// a backed (pill) caption is ONE line: when the page's estimated width (~0.68 em per glyph in the 900 display
	// face, +0.36 em gaps) passes maxWidth, shrink the type (down to 76%) instead of wrapping to a second line
	const baseSize = st.fontSize ?? (vertical ? 104 : 84);
	const glyphs = page.words.reduce((n, w) => n + w.text.length, 0) * (st.uppercase ? 0.76 : 0.68) + (page.words.length - 1) * 0.36;
	const fontSize = st.backing > 0 ? baseSize * Math.max(0.76, Math.min(1, maxWidth / (glyphs * baseSize))) : baseSize;
	// keep the caption block inside the safe band
	let cueY: number | undefined;
	for (const c of placement ?? []) if (c.at <= t + 1e-6) cueY = c.y;
	const yFrac = cueY ?? st.y ?? (vertical ? 0.64 : 0.82);
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
				// max-content: one line until the words pass maxWidth (fit-content capped the box at frameWidth - cx ~560 px)
				width: st.backing > 0 ? 'max-content' : maxWidth,
				maxWidth,
				...(st.backing > 0
					? {background: `rgba(${st.backingColor ?? '0,0,0'},${st.backing})`, borderRadius: fontSize * 0.34, padding: `${fontSize * 0.1}px ${fontSize * 0.3}px`}
					: {}),
				transform: `translate(-50%, -50%) translateY(${lift}px) scale(${scale})`,
				display: 'flex',
				// one line for a backed pill (Chrome's max-content of a wrapping flex row ignores column-gap, so the last word wrapped)
				flexWrap: st.backing > 0 ? 'nowrap' : 'wrap',
				whiteSpace: st.backing > 0 ? 'nowrap' : undefined,
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
				const hl = active && st.highlightMode !== 'none' && !(st.highlightMode === 'content' && isStop(w));
				// explicit per-word emphasis (Word.emph) is the only highlight when highlightMode is 'none'
				const color = w.emph || (hl && (st.highlightMode === 'color' || st.highlightMode === 'content')) ? st.highlight : st.color;
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
