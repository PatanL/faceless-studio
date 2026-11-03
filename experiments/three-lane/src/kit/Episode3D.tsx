// A 3D story-lane episode (our own code). Props are the episode's storyboard JSON (built by the pipeline; it supplies
// the scene durations, the Kokoro word timings and the caption style). The episode's story file turns those timings
// into shot groups; each group is one ThreeCanvas Sequence. Different places join with the group's xfade (the
// references' 6-8 frame scene changes, done as whip pans; 0 = hard cut); angle changes inside a place are camera moves. Captions are the
// studio CaptionTrack, placed per page off the shot's subject boxes; tags, titles and props are DOM overlays given by
// the episode. Video only: the narration mix is muxed afterwards.
import React, { useEffect, useMemo, useState } from "react";
import * as THREE from "three";
import { AbsoluteFill, Freeze, Sequence, continueRender, delayRender, useCurrentFrame, useVideoConfig } from "remotion";
import { parseStoryboard, sceneTimings, type StoryboardInput } from "../../../../studio/src/core/schema";
import { CaptionTrack, paginate, type CaptionCue } from "../../../../studio/src/core/captions";
import { waitForFonts } from "../../../../studio/src/core/fonts";
import { Stage, type GroupSpec } from "./Stage";
import { CamPath } from "./campath";
import { Timing } from "./timing";
import { personBox } from "./framing";
import { RicksCaptions, type CapWord } from "./captions";
import { clipCss, covers, homography, type Shape } from "./match";
import { runGates, type HudTrack } from "./gates";
import { preloadModels } from "./models";
import { preloadCodeModels } from "./codemodels";
import { preloadPlate } from "./plate";

const W = 1080, H = 1920;
// phrase pages run to two lines (caption_rule "phrase"), so 3D episodes use a slightly smaller caption than the house 84
export const CAP_SIZE = 74, CAP_W = 880;

/** caption y per page: keep the caption band off the subject boxes of the shot (projected from the story's cameras) */
export type ScreenRect = { x0: number; x1: number; y0: number; y1: number };
/** screenAvoid: on-screen panels the episode draws over the shot (gauges, counters), in 1080x1920 pixels */
export function captionCues(groups: GroupSpec[], pages: { start: number; end: number; words: { text: string }[] }[], fps: number, y0: number,
  screenAvoid?: (t: number) => ScreenRect[]): CaptionCue[] {
  const paths = new Map<GroupSpec, CamPath>();
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.05, 400);
  const BUSY_W = 3, FACE_W = 8;                                     // a busy band costs 3x an avoid box, a face 8x (plus its body box)
  const rects = (t: number) => {
    const g = [...groups].reverse().find((q) => t >= q.t0 - 1e-6 && t < q.t1) ?? groups[groups.length - 1];
    // the shot's subject boxes plus every visible figure (captions never sit on a face), plus the busy bands
    if (!paths.has(g)) paths.set(g, new CamPath(g.cam, g.t0, g.t1));
    const c = paths.get(g)!.at(t);
    const busyB = g.busy ? g.busy(t, [c.pos.x, c.pos.y, c.pos.z]) : [];
    const nBusy = busyB.length;
    const figs = g.people.filter((p) => !p.visible || p.visible(t)).map((p) => personBox(p.at(t), (p.props(t) as { seated?: boolean }).seated === true));
    // faces (the top third of each figure) weigh most: a caption on a face is the worst place (v15 stills: the busy
    // weight alone pushed a caption onto the admiral's face)
    const faces = figs.map((b): typeof b => [b[0], b[4] - 0.33 * (b[4] - b[1]), b[2], b[3], b[4], b[5]]);
    const boxes = [...busyB, ...faces, ...(g.avoid ? g.avoid(t) : []), ...figs];
    const panels = (screenAvoid ? screenAvoid(t) : []).map((r) => ({ ...r, w: FACE_W }));   // never under a HUD panel
    if (!boxes.length) return panels;
    cam.fov = c.fov; cam.position.copy(c.pos); cam.lookAt(c.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    return boxes.map((b, bi) => {
      const wgt = bi < nBusy ? BUSY_W : bi < nBusy + faces.length ? FACE_W : 1;
      let x0 = Infinity, x1 = -Infinity, yA = Infinity, yB = -Infinity, front = false;
      for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) {
        const q = new THREE.Vector3(x, y, z);
        if (q.clone().applyMatrix4(cam.matrixWorldInverse).z > -0.05) { front = true; continue; }
        q.project(cam);
        const sx = (q.x * 0.5 + 0.5) * W, sy = (0.5 - q.y * 0.5) * H;
        x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); yA = Math.min(yA, sy); yB = Math.max(yB, sy);
      }
      // a busy band partly behind the lens cannot be placed on screen: skip it (a figure there still blocks everything)
      if (front && bi < nBusy) return { x0: 0, x1: 0, y0: 0, y1: 0, w: 0 };
      return front ? { x0: 0, x1: W, y0: 0, y1: H, w: wgt } : { x0, x1, y0: yA, y1: yB, w: wgt };
    }).concat(panels);
  };
  const cands = [y0, 0.79, 0.3, 0.24];
  const groupAt = (t: number) => [...groups].reverse().find((q) => t >= q.t0 - 1e-6 && t < q.t1) ?? groups[groups.length - 1];
  // one caption position per shot group (v1 review: captions hopping top/bottom page to page read as a glitch): sum the
  // overlap of every page shown in the group for each candidate height, keep the cheapest for the whole group
  const pageCost = pages.map((p) => {
    const glyphs = p.words.reduce((n, w) => n + w.text.length, 0) * 0.76 + (p.words.length - 1) * 0.36;
    const lines = Math.ceil((glyphs * CAP_SIZE) / CAP_W);
    const half = Math.min(CAP_W, glyphs * CAP_SIZE) / 2 + 20, bandH = lines * CAP_SIZE * 0.55 + 24;
    const cx = W / 2 - 20;
    return cands.map((y) => {
      const top = y * H - bandH, bot = y * H + bandH;
      let cost = 0;
      for (let t = p.start; t < p.end; t += 3 / fps)
        for (const b of rects(t)) cost += b.w * Math.max(0, Math.min(cx + half, b.x1) - Math.max(cx - half, b.x0)) * Math.max(0, Math.min(bot, b.y1) - Math.max(top, b.y0));
      return cost;
    });
  });
  const choice = new Map<GroupSpec, number>();
  for (const g of groups) {
    const tot = cands.map((_, ci) => pages.reduce((n, p, pi) => n + (groupAt((p.start + p.end) / 2) === g ? pageCost[pi][ci] : 0), 0) + (ci === 0 ? 0 : 3000));
    choice.set(g, cands[tot.indexOf(Math.min(...tot))]);
  }
  return pages.map((p) => ({ at: p.start - 0.001, y: choice.get(groupAt((p.start + p.end) / 2))! }));
}

// ------------------------------------------------------------------------------------------------ joins
// How two groups meet, chosen per group by `join` (how the group is ENTERED; default from xfade: a whip, or a cut).
// None of them ever draws two places semi-transparently over each other (rule book 1.2: keep the dissolve's
// function, leave its ghost):
//   whip   blur + sideways travel; in its overlap frames the incoming shot is revealed by a feathered wipe that
//          follows the travel, not faded in under the outgoing one (the opacity overlap left 2-3 blend frames per whip)
//   cut    a hard cut
//   match  the incoming shot (framed by match.matchKey so its anchor sits where the outgoing anchor was) is revealed
//          by a hard-edged disc growing from the anchor over 6-8 f; only a 40 px feathered rim is ever mixed
//   push   the camera pushes through an opening of the outgoing shot (window: quadPortal, eye: circlePortal); the
//          incoming shot shows through the opening's outline (a clip) until it fills the frame
//   into   the outgoing shot freezes and shrinks into a prop of the incoming shot (homography onto its projected quad)
//   outOf  the incoming shot starts frozen inside a prop of the outgoing shot and grows out of it, then moves
export type Join =
  | { kind: "whip"; dur?: number }
  | { kind: "cut" }
  | { kind: "match"; frames?: number; anchor: (t: number) => [number, number]; feather?: number }
  | { kind: "push"; frames: number; portal: (t: number) => Shape }
  | { kind: "into"; frames: number; quad: (t: number) => [number, number][]; until?: number }
  | { kind: "outOf"; frames: number; quad: (t: number) => [number, number][]; pre?: number }
  // story-myeongnyang (owner, 2026-11-02, the RicksClips join mix): a short cross-dissolve (5-8 f, centred on the
  // change; match: the incoming shot is framed so an object keeps its spot on screen), and a travel join: the camera
  // flies on through one connected world, so the change of group is a seam the viewer never sees (the gate checks that
  // the camera is continuous across it and that both groups build the same world)
  | { kind: "dissolve"; frames?: number; match?: boolean }
  | { kind: "travel"; world: string };

const sm = (u: number) => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
const joinOf = (g: GroupSpec | undefined): Join | null => (!g ? null : g.join ?? (g.xfade > 0 ? { kind: "whip", dur: g.xfade } : { kind: "cut" }));
const whipF = (j: Join | null, fps: number) => (j && j.kind === "whip" ? Math.round((j.dur ?? 0.4) * fps) : 0);
const FULL: [number, number][] = [[0, 0], [W, 0], [W, H], [0, H]];
const lerpQuad = (a: [number, number][], b: [number, number][], u: number) => a.map(([x, y], i) => [x + (b[i][0] - x) * u, y + (b[i][1] - y) * u] as [number, number]);
/** whip overlap: the frames at the cut where both shots are drawn (both under the heaviest smear) */
export const WHIP_OV = 5;

type Style = (abs: number) => React.CSSProperties | null;
/** host: the style of the shot this layer lives inside (a push's opening, a prop's picture), so the host's whip carries
 * the inner shot with it; only its transform / filter / opacity / clip are taken */
type Layer = { key: string; g: GroupSpec; from: number; to: number; kind: "main" | "inset"; freezeAt?: number; style: Style; host?: Style };
const carry = (s: React.CSSProperties | null): React.CSSProperties | null => (s ? { transform: s.transform, filter: s.filter, opacity: s.opacity, maskImage: s.maskImage, WebkitMaskImage: s.WebkitMaskImage } : null);

/** frame ranges and per-frame styles of every layer (main shots, then the frozen frame-in-frame insets on top) */
export function layersOf(groups: GroupSpec[], fps: number, endFrame?: number): Layer[] {
  const L: Layer[] = [], insets: Layer[] = [];
  groups.forEach((g, i) => {
    const inJ = i === 0 ? null : joinOf(g), outJ = joinOf(groups[i + 1]);
    const T = Math.round(g.t0 * fps), T1 = Math.round(g.t1 * fps);
    const nIn = whipF(inJ, fps), nOut = whipF(outJ, fps);
    let from = T, to = T1;
    if (inJ?.kind === "whip") from = Math.round((g.t0 - nIn / fps / 2) * fps);
    if (inJ?.kind === "match") from = T - Math.floor((inJ.frames ?? 7) / 2);
    if (inJ?.kind === "push") from = T - inJ.frames;
    if (inJ?.kind === "dissolve") from = T - Math.floor((inJ.frames ?? 6) / 2);
    if (outJ?.kind === "whip") to = Math.round((g.t1 + nOut / fps / 2) * fps);
    if (outJ?.kind === "match") to = T1 + ((outJ.frames ?? 7) - Math.floor((outJ.frames ?? 7) / 2));
    if (outJ?.kind === "dissolve") to = T1 + ((outJ.frames ?? 6) - Math.floor((outJ.frames ?? 6) / 2));
    if (i === groups.length - 1 && endFrame) to = Math.max(to, endFrame);       // the last shot runs to the last frame
    const total = Math.max(1, to - from);
    const outgoing = L[L.length - 1];
    L.push({
      key: `m-${g.id}-${i}`, g, from, to, kind: "main",
      host: inJ?.kind === "push" && outgoing ? (abs) => (abs < T ? carry(outgoing.style(abs)) : {}) : undefined,
      style: (abs) => {
        const frame = abs - from;
        // ---- whip: a frames centred on the cut; blur and travel rise to the cut and fall after it
        const OV = WHIP_OV, half = Math.floor(nIn / 2), outHalf = nOut - Math.floor(nOut / 2);
        if (nIn > 0 && frame < half - OV / 2) return null;
        if (nOut > 0 && frame >= total - outHalf + OV / 2) return null;
        const din = nIn > 0 ? Math.abs(frame - half) / Math.max(1, half) : 1;
        const dout = nOut > 0 ? Math.abs(frame - (total - outHalf)) / Math.max(1, outHalf) : 1;
        const inWhip = nIn > 0 && frame < nIn, outWhip = nOut > 0 && frame >= total - nOut;
        const k = Math.max(inWhip ? 1 - Math.min(1, din) : 0, outWhip ? 1 - Math.min(1, dout) : 0);
        const dir = inWhip && frame >= half - OV / 2 && (!outWhip || frame < total - nOut) ? 1 : -1;
        const blur = 16 * Math.sqrt(k), sc = 1 + 0.18 * k, tx = dir * 0.16 * k * 1080;
        const st: React.CSSProperties = blur > 0.3 ? { filter: `blur(${blur.toFixed(1)}px)`, transform: `translateX(${tx.toFixed(1)}px) scale(${sc.toFixed(3)})` } : {};
        // the overlap frames: the incoming shot wipes in from the right, the way the whip travels, behind a feathered
        // edge (a 60 %-wide band under the 16 px smear, over 5 frames). Only the band mixes; the rest of the frame is one shot or the
        // other, so no frame reads as a dissolve (the opacity fade-in left 2-3 blend frames per whip), and the change
        // is spread over the overlap frames (a hard edge made 3 one-frame jumps per whip)
        if (nIn > 0 && frame < half + OV / 2) {
          const u = (frame - (half - OV / 2) + 1) / (OV + 1), F = 0.6 * W;
          const edge = (W + F) * (1 - u) - F / 2;
          const mask = `linear-gradient(to right, transparent ${(edge - F / 2).toFixed(0)}px, #000 ${(edge + F / 2).toFixed(0)}px)`;
          Object.assign(st, { WebkitMaskImage: mask, maskImage: mask });
        }
        const t = abs / fps;
        // ---- match: a growing hard-edged disc from the anchor
        if (inJ?.kind === "match" && abs < T + ((inJ.frames ?? 7) - Math.floor((inJ.frames ?? 7) / 2))) {
          const m = inJ.frames ?? 7, u = (abs - from + 1) / m;
          const [ax, ay] = inJ.anchor(t), fe = inJ.feather ?? 40;
          const R = Math.max(...FULL.map(([x, y]) => Math.hypot(x - ax, y - ay))) + fe;
          const r = Math.max(0, sm(u) * R - fe);
          const mask = `radial-gradient(circle at ${ax.toFixed(1)}px ${ay.toFixed(1)}px, #000 ${r.toFixed(1)}px, transparent ${(r + fe).toFixed(1)}px)`;
          Object.assign(st, { WebkitMaskImage: mask, maskImage: mask });
        }
        // ---- dissolve: the incoming shot fades in over the outgoing one (which stays opaque under it)
        if (inJ?.kind === "dissolve" && abs < from + (inJ.frames ?? 6)) Object.assign(st, { opacity: (abs - from + 1) / ((inJ.frames ?? 6) + 1) });
        // ---- push: clipped to the opening's outline until it covers the frame
        if (inJ?.kind === "push" && abs < T) {
          const shp = inJ.portal(t);
          const clip = covers(shp) ? undefined : clipCss(shp);
          if (clip) Object.assign(st, { clipPath: clip, WebkitClipPath: clip });
        }
        return st;
      },
    });
    if (outJ?.kind === "into") {
      const nx = groups[i + 1], until = Math.round((outJ.until ?? nx.t1) * fps);
      const self = L.length;
      insets.push({ key: `i-${g.id}`, g, from: T1, to: until, kind: "inset", freezeAt: T1 - 1, host: (abs) => carry(L[self].style(abs)),
        style: (abs) => { const u = sm((abs - T1 + 1) / outJ.frames); const q = lerpQuad(FULL, outJ.quad(abs / fps), u); return { transformOrigin: "0 0", transform: homography(q) }; } });
    }
    if (inJ?.kind === "outOf") {
      const s = T - inJ.frames - Math.round((inJ.pre ?? 0.6) * fps);
      const og = L[L.length - 2];
      insets.push({ key: `o-${g.id}`, g, from: s, to: T, kind: "inset", freezeAt: T, host: (abs) => carry(og.style(abs)),
        style: (abs) => { const u = sm((abs - (T - inJ.frames) + 1) / inJ.frames); const q = lerpQuad(inJ.quad(abs / fps), FULL, abs < T - inJ.frames ? 0 : u); return { transformOrigin: "0 0", transform: homography(q) }; } });
    }
  });
  return [...L, ...insets];
}

const LayerView: React.FC<{ l: Layer }> = ({ l }) => {
  const f = useCurrentFrame();
  const st = l.style(l.from + f);
  const hs = l.host ? l.host(l.from + f) : {};
  if (!st || !hs) return null;
  return (
    <AbsoluteFill style={hs}>
      <AbsoluteFill style={st}>
        {l.kind === "inset" ? <Freeze frame={0}><Stage g={l.g} fromFrame={l.freezeAt!} /></Freeze> : <Stage g={l.g} fromFrame={l.from} />}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------------------------------------ the episode
export type Story = { groups: GroupSpec[]; hud?: HudTrack[] };

/** A 3D story episode. Props: the episode storyboard (scene durations, Kokoro word timings, the caption style), or for
 * a lab reel bare `words` + `durations`. captions: "house" (default: the studio CaptionTrack placed off faces, HUD
 * panels and busy bands), "ricks" (the reference style: opt-in, the owner has not chosen it), "none".
 * gates (kit/gates.ts: holds <= 4 s, no speck figures, nothing cut by the edge, HUD never backwards): "fail" (default)
 * stops the render with the list, "warn" logs it, "off". */
export function Episode3D<S extends Story>({ storyboard, words: wordsIn, durations, build, overlays, screenAvoid, captions = "house", gates = "fail", joins, plates }: {
  storyboard?: StoryboardInput; words?: CapWord[]; durations?: number[];
  /** "ricks": also gate the join mix against the RicksClips counts (kit/gates.ts joinMix) */
  joins?: "ricks";
  build: (T: Timing) => S; overlays?: (s: S) => React.ReactNode;
  screenAvoid?: (s: S, t: number) => ScreenRect[];
  captions?: "house" | "ricks" | "ricks-phrase" | "none"; gates?: "fail" | "warn" | "off";
  /** key-frame depth plates to preload (kit/plate.ts) */
  plates?: string[];
}) {
  waitForFonts();
  const { fps, durationInFrames } = useVideoConfig();
  const sb = useMemo(() => {
    if (!storyboard) return null;
    const s = parseStoryboard(storyboard);
    if (s.captions) {
      const words = s.captions.words.map((w, i) => (i === 0 && w.start < 0.4 ? { ...w, start: 0 } : w));   // frame 0 is the cover: it carries the first words
      s.captions = { ...s.captions, words, style: { ...s.captions.style, fontSize: CAP_SIZE, maxWidth: CAP_W } };
    }
    return s;
  }, [storyboard]);
  const words: CapWord[] = useMemo(() => wordsIn ?? (sb?.captions?.words ?? []), [wordsIn, sb]);
  const durs = useMemo(() => durations ?? (sb ? sb.scenes.map((s) => s.duration) : [words.length ? words[words.length - 1].end + 0.5 : 1]), [durations, sb, words]);
  const story = useMemo(() => build(new Timing(durs, words)), [durs, words, build]);
  useMemo(() => {
    if (gates === "off") return;
    const r = runGates(story.groups, words, { fps, hud: story.hud, joins });
    const msg = `[three-lane gates] ${r.failures.length} failure(s)\n  ${r.failures.join("\n  ")}\n  ${r.notes.join("\n  ")}`;
    if (r.failures.length && gates === "fail") throw new Error(msg + "\n(pass gates=\"warn\" to render anyway)");
    if (r.failures.length) console.warn(msg);
  }, [story, words, fps, gates]);
  const layers = useMemo(() => layersOf(story.groups, fps, durationInFrames), [story, fps, durationInFrames]);
  const timings = useMemo(() => (sb ? sceneTimings(sb).timings : []), [sb]);
  const cuts = useMemo(() => timings.slice(1).map((tm) => tm.start / fps), [timings, fps]);
  const placement = useMemo(() => (sb?.captions && captions === "house" ? captionCues(story.groups, paginate(sb.captions.words, sb.captions, cuts), fps, sb.captions.style.y ?? 0.72, screenAvoid ? (t) => screenAvoid(story, t) : undefined) : []),
    [sb, story, cuts, fps, captions]);   // eslint-disable-line react-hooks/exhaustive-deps
  // the 3D worlds draw text into canvases (labels, tags): build them only once the fonts are in
  const [fontsReady, setReady] = useState(false);
  const [handle] = useState(() => delayRender("three-lane fonts"));
  useEffect(() => {
    Promise.all([document.fonts.load('400 64px "Anton"'), document.fonts.load('900 64px "Montserrat"'), document.fonts.load('800 64px "Montserrat"'), preloadModels(), preloadCodeModels(), ...(plates ?? []).map((id) => preloadPlate(id))])
      .catch(() => null).finally(() => { setReady(true); continueRender(handle); });
  }, [handle]);
  return (
    <AbsoluteFill style={{ background: "#120d24" }}>
      {fontsReady && layers.map((l) => (
        <Sequence key={l.key} from={l.from} durationInFrames={Math.max(1, l.to - l.from)} name={l.key} layout="none">
          <LayerView l={l} />
        </Sequence>
      ))}
      {overlays ? overlays(story) : null}
      {captions === "house" && sb?.captions ? <CaptionTrack captions={sb.captions} format={sb.format} theme={sb.theme} placement={placement} cuts={cuts} /> : null}
      {captions === "ricks" ? <RicksCaptions words={words} /> : null}
      {captions === "ricks-phrase" ? <RicksCaptions words={words} breaks="phrase" /> : null}
    </AbsoluteFill>
  );
}

/** the overlay clock (global seconds) for episode overlays */
export const useStoryTime = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return f / fps; };
