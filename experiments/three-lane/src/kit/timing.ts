// Word-anchored story time (our own code): scene starts from the storyboard's scene durations, word times from its
// caption words (Kokoro timings). w(scene, "word", n) = global seconds of the n-th "word" spoken in that scene.
export type Word = { text: string; start: number; end: number };

const norm = (s: string) => s.toLowerCase().replace(/[’]/g, "'").replace(/[^a-z0-9'-]/g, "");

export class Timing {
  readonly starts: number[] = [];
  readonly total: number;
  constructor(readonly durations: number[], readonly words: Word[]) {
    let t = 0;
    for (const d of durations) { this.starts.push(t); t += d; }
    this.total = t;
  }
  S(i: number) { return i >= this.starts.length ? this.total : this.starts[i]; }
  /** global time of the n-th occurrence of word in scene si (start, or end with end=true), plus off */
  w(si: number, word: string, n = 1, off = 0, end = false): number {
    const a = this.S(si) - 0.05, b = this.S(si + 1);
    const want = norm(word);
    const hits = this.words.filter((x) => x.start >= a && x.start < b && norm(x.text) === want);
    const h = hits[n - 1];
    if (!h) throw new Error(`timing: no "${word}" #${n} in scene ${si + 1}`);
    return (end ? h.end : h.start) + off;
  }
}
