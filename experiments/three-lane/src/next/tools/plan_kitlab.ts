// KitLab plan checks without rendering (our own code). Bundled with esbuild and run in node:
//   cd experiments/three-lane && node_modules/.bin/esbuild src/next/tools/plan_kitlab.ts --bundle --platform=node \
//     --outfile=<scratch>/plan_kitlab.cjs --log-level=warning \
//     --loader:.woff=empty --loader:.woff2=empty --loader:.css=empty && node <scratch>/plan_kitlab.cjs > <scratch>/kitlab_plan.json
// Prints JSON: the shot plan (holds, flags, place changes), the lead's face track stats, caption page stats, the
// caption-over-face gate, the light arc, the join checks (match anchor drift, push coverage) and the fx cue count.
import { Timing } from "../../kit/timing";
import { synthWords } from "../kitlab/script";
import { buildLab } from "../kitlab/story";
import { planReport, planText } from "../planner";
import { ricksPages, ricksCaptionStats, RICKS_Y } from "../captions";
import { boxRect, covers, W, H } from "../match";
import { layersOf, type NextGroup } from "../EpisodeNext";

const lab = synthWords();
const words = lab.words;
const END = words[words.length - 1].end + 0.4;
const story = buildLab(new Timing([END], words));
const groups = story.groups as NextGroup[];
const plan = planReport(groups, words, 4);

// caption band gate: the lead's head box projected every frame; frames where it meets the caption's box
const pages = ricksPages(words, END);
const fps = 30;
let faceFrames = 0, hitFrames = 0;
const headTruth: [number, number, number][] = [];     // [frame, visible head height / H, full head height / H]
const hitsAt: number[] = [];
for (let f = 0; f < Math.round(END * fps); f++) {
  const t = f / fps;
  const hb = story.adaHead(t);
  const g = [...groups].reverse().find((q) => t >= q.t0 - 1e-6);
  if (!hb || !g) continue;
  const r = boxRect(g, t, hb);
  if (r.x1 < 0 || r.x0 > W || r.y1 < 0 || r.y0 > H) continue;
  faceFrames++;
  headTruth.push([f, +((Math.min(H, r.y1) - Math.max(0, r.y0)) / H).toFixed(4), +(r.h / H).toFixed(4)]);
  const page = pages.find((p) => t >= p.start && t < p.end);
  const half = page ? Math.min(940, page.text.length * 0.62 * 92) / 2 + 10 : 0;
  const top = RICKS_Y * H - 50, bot = RICKS_Y * H + 50;
  if (page && r.y1 > top && r.y0 < bot && r.x1 > W / 2 - half && r.x0 < W / 2 + half) { hitFrames++; hitsAt.push(+t.toFixed(2)); }
}
// on-screen time of the lead (for swaps per 10 s)
let leadOn = 0;
for (let f = 0; f < Math.round(END * fps); f++) if (story.adaHead(f / fps)) leadOn += 1 / fps;

// joins: match anchor drift across the transition, push openings covering the frame at the switch
const joins = groups.map((g, i) => {
  const j = g.join; if (!j || i === 0) return null;
  const prev = groups[i - 1];
  if (j.kind === "match") {
    const a = j.anchor(g.t0);
    return { group: g.id, kind: j.kind, anchorAt: a.map((x) => Math.round(x)) };
  }
  if (j.kind === "push") { const sh = j.portal(g.t0 - 1 / fps); return { group: g.id, kind: j.kind, coversAtSwitch: covers(sh), shape: sh.kind }; }
  return { group: g.id, kind: j.kind, from: prev.id };
});
// transition windows (absolute frames) for ghost_check.py: where two shots share the screen
const layers = layersOf(groups, fps);
const windows = groups.slice(1).map((g, k) => {
  const i = k + 1, kind = g.join?.kind ?? (g.xfade > 0 ? "whip" : "cut");
  const inc = layers.find((l) => l.kind === "main" && l.g === g)!, out = layers.find((l) => l.kind === "main" && l.g === groups[i - 1])!;
  const ins = layers.filter((l) => l.key === `o-${g.id}` || l.key === `i-${groups[i - 1].id}`);
  const a = Math.min(inc.from, ...ins.map((l) => l.from)), b = Math.max(out.to, Math.round(g.t0 * fps));
  return { group: g.id, kind, from: a, to: kind === "into" ? Math.round(g.t0 * fps) + ((g.join as { frames: number }).frames ?? 12) : b, t0f: Math.round(g.t0 * fps) };
});
const fxCues = groups.reduce((n, g) => n + (g.rigs?.length ?? 0), 0);

console.log(JSON.stringify({
  duration: +END.toFixed(2), words: words.length, wps: +(words.length / (words[words.length - 1].end)).toFixed(2),
  plan: { ...plan, changes: plan.changes.map((c) => `${c.t.toFixed(2)} ${c.kind} ${c.group}: ${c.why}`), holds: plan.holds.map((h) => `${h.t0}-${h.t1} (${h.len}) ${h.group}${h.flag ? " FLAG" : ""}`) },
  planText: planText(plan),
  acting: { ...story.faceReport, leadOnScreenS: +leadOn.toFixed(2), heldSwapsPer10sOnScreen: +(story.faceReport.heldSwaps / (leadOn / 10)).toFixed(2) },
  captions: { ...ricksCaptionStats(pages), sample: pages.slice(0, 14).map((p) => p.text) },
  captionOnFace: { leadFrames: faceFrames, framesUnderCaption: hitFrames, at: hitsAt.slice(0, 40) },
  joins: joins.filter(Boolean), rigCount: fxCues, windows, headTruth,
}, null, 1));
