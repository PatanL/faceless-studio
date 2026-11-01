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

// a page never ends on one of these unless punctuation closes it there: the phrase is still open
// ("Rule four said if", "So who'd been answering our", "Management may", "His little green")
const DANGLING = new Set(
	(
		'a an the this these those my your his her our their its no every each some any ' +
		'and or but nor if as than because though while where who whose which ' +
		'will would can could may might must shall should do does did is are was were be been being am has have had ' +
		"i i'm i'd i'll i've we we're they he she he'd she'd they'd you're who'd " +
		'little big small old new last first same other red green grey gray black white dark cold calm only very really just not'
	).split(' '),
);
// ... nor on an open verb / preposition unless a new phrase starts right after it: "Rule four said | if someone",
// "need | to come", "I looked | through the peephole", "come in | for a minute" are fine; "A calm voice said | my name",
// "I looked through | the peephole", "We just need to come | in for a minute" are not
const OPEN_VERB = new Set('said says say come came go get got sat looked turned switched need needs want wants'.split(' '));
const PREP = new Set(
	'of to in into onto on at by for from with without through about over under after before behind against between until'.split(' '),
);
const CLAUSE = new Set('and but or so because then when while if that who which to what'.split(' '));
// a break right before one of these lands on a phrase boundary
const STARTERS = new Set([...CLAUSE, ...PREP]);
const isParticle = (w: Word, after?: Word) => PREP.has(bare(w)) && (PUNCT_END.test(w.text.trim()) || !after || STARTERS.has(bare(after)));
// cost of a page ending on `last` (followed by nx, nx2) that leaves the phrase open: determiners / pronouns /
// auxiliaries 4, a preposition before its object 3.5, an open verb 3 ("I looked | through" beats "I looked through |")
const dangles = (last: Word, nx: Word, nx2?: Word) => {
	if (PUNCT_END.test(last.text.trim())) return 0;
	const b = bare(last);
	if (DANGLING.has(b)) return 4;
	if (PREP.has(b)) return STARTERS.has(bare(nx)) ? 0 : 3.5; // "come in | for", "light on | and" (particles) are fine
	if (OPEN_VERB.has(b)) return CLAUSE.has(bare(nx)) || (PREP.has(bare(nx)) && !isParticle(nx, nx2)) ? 0 : 3;
	return 0;
};

/**
 * Group words into short one-line pages (up to maxWords+1 words / maxChars+6 chars). Pages never cross a
 * sentence end or a scene cut; inside a sentence the breaks are picked by least cost (see DANGLING / STARTERS).
 * Words with `br` (pipeline phrase pages) override this: break only there. A page shows from its first word
 * until the next page starts (or `linger` after its last word).
 */
export function paginate(
	words: Word[],
	c: Pick<Captions, 'maxWords' | 'maxChars' | 'gapBreak' | 'linger'> & {glue?: string[]; style?: {backing?: number}},
	cuts?: number[],
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
	// Hard segments: a page never runs across a sentence end or a scene cut (`cuts`, global seconds). Inside a
	// segment the breaks are chosen together (least cost): whole short lines first, never a page ending on a dangling
	// function word ("Rule four said if", "I looked through"), never splitting glued pairs ("Six | C", "only | one"),
	// breaks preferred at commas / pauses / before a phrase starter, no flashes under 0.6 s or lone words.
	const cutList = [...(cuts ?? [])].sort((x, y) => x - y);
	const crossesCut = (a: Word, b: Word) => cutList.some((t) => a.start < t - 1e-3 && b.start >= t - 1e-3);
	const segs: Word[][] = [];
	sorted.forEach((w, i) => {
		const prev = sorted[i - 1];
		if (!prev || SENTENCE_END.test(prev.text.trim()) || crossesCut(prev, w)) segs.push([]);
		segs[segs.length - 1].push(w);
	});
	const hardWords = c.maxWords + 1;
	// a backed (pill) caption shrinks its type to stay on one line, so it can take a whole short sentence
	const hardChars = c.maxChars + ((c.style?.backing ?? 0) > 0 ? 8 : 6);
	segs.forEach((seg, si) => {
		const n = seg.length;
		// the segment's last page is cut short by the next segment's first word (see the timing below)
		const after = segs[si + 1]?.[0].start ?? Infinity;
		const cost = (i: number, j: number) => {
			// page = seg[i..j)
			const ws = seg.slice(i, j);
			const chars = ws.reduce((k, x) => k + x.text.length + 1, -1);
			if (ws.length > 1 && (ws.length > hardWords || chars > hardChars)) return Infinity;
			let k = 1;
			k += Math.max(0, chars - c.maxChars) * 0.15 + (ws.length > c.maxWords ? 0.6 : 0);
			const last = ws[ws.length - 1];
			const end = j < n ? seg[j].start : Math.min(last.end + c.linger, Math.max(after, last.end));
			if (end - ws[0].start < 0.6) k += 2.5;
			if (end - ws[0].start > 3.2) k += 1;
			if (ws.length === 1 && n > 1) k += 1;
			if (j < n) {
				const nx = seg[j];
				const lt = last.text.trim();
				k += dangles(last, nx, seg[j + 1]);
				if (glues(nx, last) || binds(nx, last, pairs)) k += 4;
				if (PUNCT_END.test(lt)) k -= 0.8;
				if (nx.start - last.end > c.gapBreak) k -= 1.5;
				if (STARTERS.has(bare(nx))) k -= 0.2;
			}
			return k;
		};
		const best: number[] = new Array(n + 1).fill(Infinity);
		const nxt: number[] = new Array(n + 1).fill(n);
		best[n] = 0;
		for (let i = n - 1; i >= 0; i--) {
			// longest page first: on a tie the earlier page keeps more words
			for (let j = n; j > i; j--) {
				const v = cost(i, j) + best[j];
				if (v < best[i] - 1e-9) {
					best[i] = v;
					nxt[i] = j;
				}
			}
		}
		for (let i = 0; i < n; i = nxt[i]) pages.push({words: seg.slice(i, nxt[i])});
	});
	return pages.map((p, i) => {
		const start = p.words[0].start;
		const last = p.words[p.words.length - 1].end;
		const next = pages[i + 1]?.words[0].start;
		const end = next !== undefined && next - last <= c.linger ? next : last + c.linger;
		return {words: p.words, start, end};
	});
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

export const CaptionTrack: React.FC<{captions: Captions; format: Format; theme: Theme; placement?: CaptionCue[]; cuts?: number[]}> = ({
	captions,
	format,
	theme,
	placement,
	cuts,
}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const pages = useMemo(() => paginate(captions.words, captions, cuts), [captions, cuts]);
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
