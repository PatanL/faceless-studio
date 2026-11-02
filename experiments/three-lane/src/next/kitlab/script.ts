// KitLab's narration (our own text, written for the lab): a lighthouse keeper's clock. There is no voice track; the
// word timings are synthesised at the references' pace (3.7 words/s, short pauses at commas and full stops, rule P5)
// so every word-anchored piece (faces, marks, effects, light events, captions) can be proven against real-looking
// timings. Deterministic.
import type { Word } from "../../kit/acting";

export const SENTENCES = [
  "Every night for forty years, Ada climbed the lighthouse to wind its giant clock by hand.",
  "The brass key was older than the town itself.",
  "Inside the tower, a stone weight dropped one inch every hour, and that fall turned every gear.",
  "Her grandfather had drawn the whole mechanism on a single sheet of blue paper.",
  "Ships trusted its bell from forty miles out.",
  "Then, one stormy night, the clock stopped.",
  "Ada was terrified.",
  "Under the casing, a gear tooth had snapped clean off.",
  "So she climbed inside the clock and hammered it back into place.",
  "Through the window, she saw a ship turning straight for the rocks.",
  "She rang the bell by hand until dawn.",
  "The captain mailed her a photograph of his crew, safe in the harbour.",
  "It still hangs beside the clock.",
];

/** word timings at `wps` words per second (syllable-weighted), comma 0.10 s, sentence end 0.22 s */
export function synthWords(sentences = SENTENCES, wps = 3.7, t0 = 0.0): { words: Word[]; sentenceStarts: number[]; end: number } {
  const all = sentences.map((s) => s.split(/\s+/));
  const n = all.reduce((a, b) => a + b.length, 0);
  const syl = (w: string) => Math.max(1, (w.toLowerCase().replace(/[^a-z]/g, "").match(/[aeiouy]+/g) ?? []).length);
  const weights = all.flat().map((w) => 0.55 + 0.45 * syl(w));
  const pauses = all.reduce((a, s, i) => a + s.filter((w) => /,$/.test(w)).length * 0.1 + (i < all.length - 1 ? 0.22 : 0), 0);
  const speak = n / wps - pauses;
  const k = speak / weights.reduce((a, b) => a + b, 0);
  const words: Word[] = [], starts: number[] = [];
  let t = t0, wi = 0;
  all.forEach((s, si) => {
    starts.push(t);
    s.forEach((w) => {
      const d = weights[wi++] * k;
      words.push({ text: w, start: +t.toFixed(3), end: +(t + d * 0.92).toFixed(3) });
      t += d + (/,$/.test(w) ? 0.1 : 0);
    });
    if (si < all.length - 1) t += 0.22;
  });
  return { words, sentenceStarts: starts, end: t };
}
