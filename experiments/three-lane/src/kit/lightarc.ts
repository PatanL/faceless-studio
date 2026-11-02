// Light that follows the story (our own code; RICKSCLIPS_RULEBOOK L2-L5, T8, gap 6).
// The kit's Stage reads `PRESETS[g.light(t)]`, so a mid-shot change of preset pops. This module blends presets and
// registers each blend under a generated key in the same PRESETS table, which lets any GroupSpec.light function
// return a tweened preset TODAY without touching Stage:
//   light: lightArc([[t0, "day"], [t1, "golden", 0.8], [t2, "night", 1.2]], events)
// - an arc is a list of [time, preset, blendSeconds?]: each new state blends in over blendSeconds (default 0.6 s =
//   18 f; refs relight inside a held shot over 6-40 f, T8)
// - events are keyword light events (L4) laid over the arc: flicker-on (dark until the word, then on/off/on in 3 f),
//   flash (1-4 f pop), alarm wash
//   (red pulses every 6 f), glow ramp (6-25 f), each anchored to a caption word by the story file
// Blends are quantised to 1/48 steps so the table stays small (a whole Short registers well under 200 keys).
import { PRESETS, type Preset } from "./presets";
import type { GradeParams } from "../grade";

const lerp = (a: number, b: number, u: number) => a + (b - a) * u;
const l3 = (a: [number, number, number], b: [number, number, number], u: number): [number, number, number] => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];
const hex = (h: string) => { const n = parseInt(h.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const lhex = (a: string, b: string, u: number) => "#" + hex(a).map((x, i) => Math.round(lerp(x, hex(b)[i], u)).toString(16).padStart(2, "0")).join("");
const sm = (u: number) => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

function blendGrade(a: GradeParams, b: GradeParams, u: number): GradeParams {
  return {
    ky: a.ky.map((k, i) => lerp(k, b.ky[i], u)),
    sat: l3(a.sat, b.sat, u),
    tintS: [lerp(a.tintS[0], b.tintS[0], u), lerp(a.tintS[1], b.tintS[1], u)],
    tintM: [lerp(a.tintM[0], b.tintM[0], u), lerp(a.tintM[1], b.tintM[1], u)],
    tintH: [lerp(a.tintH[0], b.tintH[0], u), lerp(a.tintH[1], b.tintH[1], u)],
    vig: [lerp(a.vig[0], b.vig[0], u), lerp(a.vig[1], b.vig[1], u)],
  } as GradeParams;
}
export function blendPreset(a: Preset, b: Preset, u: number): Preset {
  return {
    lit: l3(a.lit, b.lit, u), shade: l3(a.shade, b.shade, u), cardLit: l3(a.cardLit, b.cardLit, u), cardShade: l3(a.cardShade, b.cardShade, u),
    key: lhex(a.key, b.key, u), keyI: lerp(a.keyI, b.keyI, u), fog: lhex(a.fog, b.fog, u), fogNear: lerp(a.fogNear, b.fogNear, u), fogFar: lerp(a.fogFar, b.fogFar, u),
    bg: lhex(a.bg, b.bg, u), glow: lerp(a.glow, b.glow, u), sat: lerp(a.sat, b.sat, u), grade: blendGrade(a.grade, b.grade, u),
  };
}

// extra moods for events and arcs (added once to PRESETS; the kit's own names are untouched)
const EXTRA: Record<string, (base: Preset) => Preset> = {
  // a dawn: cool shade, pink-gold key (in-shot sunrise, GM9U-style)
  dawn: () => blendPreset(PRESETS.night, PRESETS.golden, 0.62),
  // everything off but the glows (the moment before a flicker-on)
  dark: () => ({ ...blendPreset(PRESETS.night, PRESETS.night, 0), keyI: 0.35, lit: [0.42, 0.44, 0.7], cardLit: [0.55, 0.56, 0.74], glow: 0.15 }),
  alarm: () => ({ ...PRESETS.fire, lit: [1.6, 0.5, 0.42], key: "#ff4a3a", cardLit: [1.15, 0.62, 0.6], fog: "#4a1420", bg: "#3a0f1a", glow: 1.0 }),
  flash: () => ({ ...PRESETS.day, lit: [1.75, 1.7, 1.6], cardLit: [1.25, 1.22, 1.18], keyI: 2.6, glow: 1.0 }),
};
export function ensureExtras() {
  for (const [k, f] of Object.entries(EXTRA)) if (!PRESETS[k]) PRESETS[k] = f(PRESETS.day);
}

/** register a blend of two named presets (u quantised) and return its key */
export function mixKey(a: string, b: string, u: number): string {
  ensureExtras();
  const uq = Math.round(Math.min(1, Math.max(0, u)) * 48) / 48;
  if (uq <= 0) return a;
  if (uq >= 1) return b;
  const key = `~${a}>${b}@${uq.toFixed(4)}`;
  if (!PRESETS[key]) PRESETS[key] = blendPreset(PRESETS[a], PRESETS[b], uq);
  return key;
}
export type ArcState = [number, string, number?];       // [time, preset, blend seconds]
export type LightEvent =
  | { kind: "flicker"; t: number; to?: string; from?: string }                 // dark -> on in 3 f (off, on, off, on)
  | { kind: "flash"; t: number; frames?: number }                              // 1-4 f pop toward white
  | { kind: "alarm"; t: number; dur: number; every?: number }                  // red wash pulsing every `every` frames
  | { kind: "ramp"; t: number; dur: number; to: string };                      // glow ramp to another state (6-25 f)

/** the arc's base preset key at t (eased blends between consecutive states) */
function arcAt(arc: ArcState[], t: number): string {
  let cur = arc[0][1];
  for (let i = 1; i < arc.length; i++) {
    const [ti, pi, bi = 0.6] = arc[i];
    if (t < ti) break;
    const u = sm((t - ti) / Math.max(1e-3, bi));
    cur = u >= 1 ? pi : mixKey(arc[i - 1][1], pi, u);
  }
  return cur;
}

/** a light function for GroupSpec.light: the arc, with keyword events laid on top */
export function lightArc(arc: ArcState[], events: LightEvent[] = []): (t: number) => string {
  ensureExtras();
  const sorted = [...arc].sort((a, b) => a[0] - b[0]);
  return (t: number) => {
    let key = arcAt(sorted, t);
    for (const e of events) {
      const fr = Math.round((t - e.t) * 30);
      if (e.kind === "flicker") {
        // before the word: dark; on the word: on, off, on (1 f each), then held on
        const to = e.to ?? key, from = e.from ?? "dark";
        if (fr < 0) key = from; else if (fr === 1) key = from; else key = to;
      } else if (e.kind === "flash" && fr >= 0 && fr < (e.frames ?? 2)) {
        key = mixKey(key, "flash", fr === 0 ? 0.9 : 0.45);
      } else if (e.kind === "alarm" && fr >= 0 && t < e.t + e.dur) {
        const on = Math.floor(fr / (e.every ?? 6)) % 2 === 0;
        const fade = sm((e.t + e.dur - t) / 0.3);
        key = mixKey(key, "alarm", (on ? 0.85 : 0.35) * fade);
      } else if (e.kind === "ramp" && fr >= 0) {
        key = mixKey(key, e.to, sm((t - e.t) / Math.max(0.2, e.dur)));
      }
    }
    return key;
  };
}

/** count the distinct base states an arc visits and how many in-shot relights (blends of 6-40 f) it has */
export function arcStats(arc: ArcState[]) {
  const states = new Set(arc.map((a) => a[1]));
  const relights = arc.slice(1).filter(([, , b = 0.6]) => b * 30 >= 6 && b * 30 <= 40).length;
  return { states: states.size, relights };
}
