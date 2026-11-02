// Acting tied to words (our own code; RICKSCLIPS_RULEBOOK A2/A3/A5/A12, M2, gap 2). Story files say WHICH caption word
// changes a face; this turns that into a hard-swap face track (the Actor's `face` prop) from the Kokoro word timings,
// with optional 1-4 frame reaction runs in front of the held face, and checks the result against the reference ranges
// (holds 6-40 f typical, reaction runs 1-4 f, swaps 3-10 per 10 s on the speaking lead).
export type Word = { text: string; start: number; end: number };
const FPS = 30;
const norm = (s: string) => s.toLowerCase().replace(/[’]/g, "'").replace(/[^a-z0-9'-]/g, "");
const q = (t: number) => Math.round(t * FPS) / FPS;      // every swap lands on a frame

/** start (or end) time of the n-th `word` at or after `after` seconds; throws when the script has no such word */
export function wordT(words: Word[], word: string, n = 1, after = -1, end = false): number {
  const want = norm(word);
  const hits = words.filter((w) => w.start >= after - 1e-6 && norm(w.text) === want);
  const h = hits[n - 1];
  if (!h) throw new Error(`acting: no "${word}" #${n} after ${after.toFixed(2)} s`);
  return end ? h.end : h.start;
}

export type FaceCue = {
  /** the caption word the swap lands on (n-th occurrence after `after`) */
  word: string; n?: number; after?: number;
  face: string;
  /** frames before (+) or after (-) the word start; default 0 = on the word */
  lead?: number;
  /** reaction drawings shown first, 1-4 frames each (e.g. a 2-frame smirk before the scream) */
  react?: { face: string; frames: number }[];
};
export type FaceKey = { t: number; v: string };

/** a hard-swap face track: [{t, v}] for the Actor's `face` prop */
export function faceTrack(words: Word[], start: string, cues: FaceCue[], t0 = 0): FaceKey[] {
  const keys: FaceKey[] = [{ t: t0, v: start }];
  for (const c of cues) {
    const at = q(wordT(words, c.word, c.n ?? 1, c.after ?? -1) - (c.lead ?? 0) / FPS);
    let t = at;
    const runs = c.react ?? [];
    const total = runs.reduce((n, r) => n + Math.max(1, Math.min(4, r.frames)), 0);
    t = q(at - total / FPS);
    for (const r of runs) { keys.push({ t, v: r.face }); t = q(t + Math.max(1, Math.min(4, r.frames)) / FPS); }
    keys.push({ t: at, v: c.face });
  }
  keys.sort((a, b) => a.t - b.t);
  // a later cue overrides an earlier one at the same frame
  return keys.filter((k, i) => i === keys.length - 1 || Math.round(keys[i + 1].t * FPS) !== Math.round(k.t * FPS));
}

/** emotion mark or colour fill that pops on at a word (and off after `dur` s, or at another word) */
export const markAt = (words: Word[], word: string, kind: string, dur?: number, n = 1, after = -1) => {
  const t0 = q(wordT(words, word, n, after));
  return { t0, t1: dur === undefined ? undefined : t0 + dur, kind };
};
export const fillAt = (words: Word[], word: string, color: string, dur?: number, n = 1, after = -1, rise = 0.2) => {
  const t0 = q(wordT(words, word, n, after));
  return { t0, t1: dur === undefined ? undefined : t0 + dur, color, rise };
};
/** a pose track that snaps on words: [[word, pose], ...] -> [{t, v}] (the Actor snaps in snapF frames) */
export function poseTrack(words: Word[], start: string, cues: [string, string, number?][], t0 = 0, leadF = 2) {
  const keys = [{ t: t0, v: start }];
  for (const [w, pose, n] of cues) keys.push({ t: q(wordT(words, w, n ?? 1) - leadF / FPS), v: pose });
  return keys.sort((a, b) => a.t - b.t);
}

export type TrackReport = {
  swaps: number; perTenS: number; heldSwaps: number;
  holdsF: { median: number; min: number; max: number };
  reactionRuns: number; shortHolds: { t: number; frames: number; face: string }[];
};
/** check a face track over [t0, t1]: swaps per 10 s (reaction runs excluded), hold lengths, stray short holds */
export function checkFaceTrack(track: FaceKey[], t0: number, t1: number): TrackReport {
  const ks = track.filter((k) => k.t < t1).map((k) => ({ ...k, t: Math.max(k.t, t0) }));
  const holds: { t: number; frames: number; face: string }[] = [];
  for (let i = 0; i < ks.length; i++) {
    const end = i + 1 < ks.length ? ks[i + 1].t : t1;
    holds.push({ t: ks[i].t, frames: Math.round((end - ks[i].t) * FPS), face: ks[i].v });
  }
  const changes = holds.slice(1).filter((h, i) => h.face !== holds[i].face);
  const reaction = holds.slice(1).filter((h) => h.frames <= 4);
  const held = changes.filter((h) => h.frames > 4);
  const hf = holds.slice(1, -1).map((h) => h.frames).filter((n) => n > 4).sort((a, b) => a - b);
  return {
    swaps: changes.length, perTenS: +(held.length / ((t1 - t0) / 10)).toFixed(2), heldSwaps: held.length,
    holdsF: { median: hf.length ? hf[Math.floor(hf.length / 2)] : 0, min: hf[0] ?? 0, max: hf[hf.length - 1] ?? 0 },
    reactionRuns: reaction.length,
    // a 5-frame hold is neither a reaction run (1-4) nor a readable hold (6+): flag it
    shortHolds: holds.slice(1, -1).filter((h) => h.frames === 5),
  };
}
