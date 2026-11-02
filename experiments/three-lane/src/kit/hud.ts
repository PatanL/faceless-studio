// HUD readouts that never read backwards for no reason (our own code; Vasa panel round 4: the heel gauge swung
// 6, 2, 10 degrees as the crew ran back and forth, which read as the reading jumping back). Wrap a raw value:
//   progress(f)               never decreases (distance sailed, money spent, days passed)
//   steadyGauge(f, tol, turns) follows the raw value only away from its last extreme; it may turn back only inside the
//                             story's `turns` windows (the beat where the narration says it comes back), and holds
//                             its extreme otherwise. Hand the same windows to gates.ts as allowBack.
// Both are pure functions of t (sampled on the frame grid from `from`), so a render, a still and the gate agree.
export type Raw = (t: number) => number | null;

export function progress(f: Raw, from = 0, fps = 30): Raw {
  const cache = new Map<number, number | null>();
  return (t) => {
    const n = Math.round(t * fps);
    let best: number | null = null;
    for (let k = Math.round(from * fps); k <= n; k++) {
      if (!cache.has(k)) cache.set(k, f(k / fps));
      const v = cache.get(k)!;
      if (v === null) { if (k === n) return null; continue; }
      best = best === null ? v : Math.max(best, v);
    }
    return best;
  };
}

export function steadyGauge(f: Raw, tol = 2, turns: [number, number][] = [], from = 0, fps = 30): Raw {
  const out = new Map<number, number | null>();
  let done = Math.round(from * fps) - 1, ext: number | null = null, dir = 0, shown: number | null = null;
  return (t) => {
    const n = Math.round(t * fps);
    for (let k = done + 1; k <= n; k++) {
      const tt = k / fps, v = f(tt);
      if (v === null) { ext = null; dir = 0; shown = null; out.set(k, null); continue; }
      const free = turns.some(([a, b]) => tt >= a && tt <= b);
      if (shown === null || free) { shown = v; ext = v; dir = 0; }
      else if (dir === 0) { shown = v; if (Math.abs(v - (ext as number)) > tol) { dir = Math.sign(v - (ext as number)); ext = v; } }
      else if ((v - (ext as number)) * dir >= 0) { shown = v; ext = v; }
      // otherwise hold the extreme: the needle does not come back until the story says so
      out.set(k, shown);
    }
    done = Math.max(done, n);
    return out.has(n) ? out.get(n)! : f(t);
  };
}
