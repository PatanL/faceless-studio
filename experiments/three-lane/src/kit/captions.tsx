// The reference caption style as an OPT-IN option (our own code; RICKSCLIPS_RULEBOOK G1-G6, gap 5).
// NOT the default: FEEDBACK.md principle 5 asks for whole-phrase captions, and the owner has to choose this style.
// EpisodeNext uses it only with `captions: "ricks"`; the house CaptionTrack stays the default.
//   - white, heavy geometric sans (Montserrat 800), mixed case with the punctuation kept, thin dark stroke and a soft
//     drop shadow, no box, no highlight colour
//   - 1-3 words per page on one line (mostly 1-2): function words ride with the next word ("with a", "on top,"),
//     a page never ends on an article / preposition / auxiliary / conjunction, punctuation closes a page
//   - a fixed centre at 71 % of the frame height (refs 68-77 %), cap height ~3.3 % of the frame height
//   - hard swaps on the word (no pop, scale or fade), from frame 0 to the last frame with no gaps
import React, { useMemo } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

export type CapWord = { text: string; start: number; end: number };
export type RicksPage = { text: string; words: CapWord[]; start: number; end: number };
export const RICKS_Y = 0.71;

const FUNC = new Set(("a an the of to in on at by for from with into onto over under about as than and or but nor so " +
  "is are was were be been am do does did has have had will would can could shall should may might must not no " +
  "his her its their our my your this that these those it he she they we i you").split(" "));
const bare = (w: string) => w.toLowerCase().replace(/[^a-z']/g, "");
const closes = (w: string) => /[,.;:!?—…]["')\]]*$/.test(w);
const isFunc = (w: string) => FUNC.has(bare(w));

/** paginate words into 1-3 word pages (least cost per punctuation-delimited segment) */
export function ricksPages(words: CapWord[], endT: number, maxWords = 3, maxChars = 16): RicksPage[] {
  const ws = words.filter((w) => w.text.trim());
  const segs: CapWord[][] = [];
  ws.forEach((w, i) => { if (i === 0 || closes(ws[i - 1].text)) segs.push([]); segs[segs.length - 1].push(w); });
  const pages: CapWord[][] = [];
  for (const s of segs) {
    const n = s.length, best: number[] = Array(n + 1).fill(Infinity), from: number[] = Array(n + 1).fill(0);
    best[0] = 0;
    for (let j = 1; j <= n; j++) for (let k = 1; k <= Math.min(maxWords, j); k++) {
      const pg = s.slice(j - k, j), last = pg[pg.length - 1];
      const chars = pg.reduce((a, w) => a + w.text.length, 0) + k - 1;
      let c = [0, 0, 0.35, 1.1][k];
      if (j < n && isFunc(last.text)) c += 6;                       // never end a page on a function word
      if (chars > maxChars) c += 4;                                  // one line
      const dur = (j < n ? s[j].start : last.end) - pg[0].start;
      if (dur < 0.2) c += 0.9;                                       // a page shorter than 6 f is unreadable
      if (k === 1 && j < n && !isFunc(last.text) && s[j] && isFunc(s[j].text) === false && last.text.length <= 3) c += 0.4;
      if (best[j - k] + c < best[j]) { best[j] = best[j - k] + c; from[j] = j - k; }
    }
    const cut: number[] = [];
    for (let j = n; j > 0; j = from[j]) cut.unshift(j);
    let a = 0;
    for (const b of cut) { pages.push(s.slice(a, b)); a = b; }
  }
  return pages.map((p, i) => ({
    text: p.map((w) => w.text).join(" "), words: p,
    start: i === 0 ? 0 : p[0].start,                                 // captions run from frame 0 ...
    end: i + 1 < pages.length ? pages[i + 1][0].start : endT,        // ... to the last frame, no gaps
  }));
}

/** pages from the pipeline's phrase breaks (Word.br, caption_rule "phrase1": whole phrases, one line), with the
 * reference timing: from frame 0 to the last frame, hard swaps, no gaps */
export function brPages(words: (CapWord & { br?: boolean })[], endT: number): RicksPage[] {
  const ws = words.filter((w) => w.text.trim());
  const groups: CapWord[][] = [];
  ws.forEach((w, i) => { if (i === 0 || w.br) groups.push([]); groups[groups.length - 1].push(w); });
  return groups.map((p, i) => ({ text: p.map((w) => w.text).join(" "), words: p, start: i === 0 ? 0 : p[0].start,
    end: i + 1 < groups.length ? groups[i + 1][0].start : endT }));
}

/** breaks: "ricks" (1-3 word pages, the reference paging) or "phrase" (the pipeline's phrase breaks, Word.br; the
 * story-lane hybrid: the reference look with whole-phrase pages) */
export const RicksCaptions: React.FC<{ words: CapWord[]; y?: number; size?: number; maxWidth?: number; breaks?: "ricks" | "phrase" }> = ({ words, y = RICKS_Y, size = 92, maxWidth = 940, breaks = "ricks" }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const pages = useMemo(() => (breaks === "phrase" ? brPages(words, durationInFrames / fps) : ricksPages(words, durationInFrames / fps)), [words, fps, durationInFrames, breaks]);
  const t = frame / fps;
  const page = pages.find((p) => t >= p.start - 1e-6 && t < p.end - 1e-6) ?? (t >= (pages[pages.length - 1]?.start ?? 0) ? pages[pages.length - 1] : undefined);
  if (!page) return null;
  const sc = height / 1920;
  // one line: shrink long pages to fit (est. 0.62 em per glyph in Montserrat 800 mixed case)
  const est = page.text.length * 0.62 * size;
  const fs = size * Math.min(1, maxWidth / Math.max(1, est)) * sc;
  return (
    <div style={{ position: "absolute", left: 0, width, top: y * height, transform: "translateY(-50%)", display: "flex", justifyContent: "center", pointerEvents: "none" }}>
      <div style={{
        fontFamily: '"Montserrat", "Arial Black", sans-serif', fontWeight: 800, fontSize: fs, lineHeight: 1, whiteSpace: "nowrap", color: "#ffffff",
        WebkitTextStroke: `${(7 * sc).toFixed(1)}px #17112e`, paintOrder: "stroke fill",
        textShadow: `0 ${(5 * sc).toFixed(1)}px ${(12 * sc).toFixed(1)}px rgba(10, 6, 30, 0.55)`, letterSpacing: -0.5 * sc,
      }}>{page.text}</div>
    </div>
  );
};

/** caption checks (rule book section 4): share of pages <= 3 words, y spread (0 = fixed), case */
export function ricksCaptionStats(pages: RicksPage[], fps = 30) {
  const n = pages.length;
  const words = pages.map((p) => p.words.length);
  const lens = pages.map((p) => Math.round((p.end - p.start) * fps)).sort((a, b) => a - b);
  return {
    pages: n, shareLe3: +(words.filter((k) => k <= 3).length / n).toFixed(3),
    wordsPerPage: { mean: +(words.reduce((a, b) => a + b, 0) / n).toFixed(2), one: words.filter((k) => k === 1).length, two: words.filter((k) => k === 2).length, three: words.filter((k) => k === 3).length },
    pageF: { min: lens[0], median: lens[Math.floor(n / 2)], max: lens[n - 1] },
    endsOnFunctionWord: pages.slice(0, -1).filter((p) => isFunc(p.words[p.words.length - 1].text) && !closes(p.words[p.words.length - 1].text)).length,
    ySpread: 0, case: "mixed",
  };
}
