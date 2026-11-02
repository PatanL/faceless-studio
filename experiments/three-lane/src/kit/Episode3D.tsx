// A 3D story-lane episode (our own code). Props are the episode's storyboard JSON (built by the pipeline; it supplies
// the scene durations, the Kokoro word timings and the caption style). The episode's story file turns those timings
// into shot groups; each group is one ThreeCanvas Sequence. Different places join with the group's xfade (the
// references' 6-8 frame scene changes, done as whip pans; 0 = hard cut); angle changes inside a place are camera moves. Captions are the
// studio CaptionTrack, placed per page off the shot's subject boxes; tags, titles and props are DOM overlays given by
// the episode. Video only: the narration mix is muxed afterwards.
import React, { useEffect, useMemo, useState } from "react";
import * as THREE from "three";
import { AbsoluteFill, Sequence, continueRender, delayRender, useCurrentFrame, useVideoConfig } from "remotion";
import { parseStoryboard, sceneTimings, type StoryboardInput } from "../../../../studio/src/core/schema";
import { CaptionTrack, paginate, type CaptionCue } from "../../../../studio/src/core/captions";
import { waitForFonts } from "../../../../studio/src/core/fonts";
import { Stage, type GroupSpec } from "./Stage";
import { CamPath } from "./campath";
import { Timing } from "./timing";
import { personBox } from "./framing";

const W = 1080, H = 1920;
// phrase pages run to two lines (caption_rule "phrase"), so 3D episodes use a slightly smaller caption than the house 84
export const CAP_SIZE = 74, CAP_W = 880;

/** caption y per page: keep the caption band off the subject boxes of the shot (projected from the story's cameras) */
export function captionCues(groups: GroupSpec[], pages: { start: number; end: number; words: { text: string }[] }[], fps: number, y0: number): CaptionCue[] {
  const paths = new Map<GroupSpec, CamPath>();
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.05, 400);
  const rects = (t: number) => {
    const g = [...groups].reverse().find((q) => t >= q.t0 - 1e-6 && t < q.t1) ?? groups[groups.length - 1];
    // the shot's subject boxes plus every visible figure (captions never sit on a face)
    const boxes = [...(g.avoid ? g.avoid(t) : []),
      ...g.people.filter((p) => !p.visible || p.visible(t)).map((p) => personBox(p.at(t), (p.props(t) as { seated?: boolean }).seated === true))];
    if (!boxes.length) return [];
    if (!paths.has(g)) paths.set(g, new CamPath(g.cam, g.t0, g.t1));
    const c = paths.get(g)!.at(t);
    cam.fov = c.fov; cam.position.copy(c.pos); cam.lookAt(c.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    return boxes.map((b) => {
      let x0 = Infinity, x1 = -Infinity, yA = Infinity, yB = -Infinity, front = false;
      for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) {
        const q = new THREE.Vector3(x, y, z);
        if (q.clone().applyMatrix4(cam.matrixWorldInverse).z > -0.05) { front = true; continue; }
        q.project(cam);
        const sx = (q.x * 0.5 + 0.5) * W, sy = (0.5 - q.y * 0.5) * H;
        x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); yA = Math.min(yA, sy); yB = Math.max(yB, sy);
      }
      return front ? { x0: 0, x1: W, y0: 0, y1: H } : { x0, x1, y0: yA, y1: yB };
    });
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
        for (const b of rects(t)) cost += Math.max(0, Math.min(cx + half, b.x1) - Math.max(cx - half, b.x0)) * Math.max(0, Math.min(bot, b.y1) - Math.max(top, b.y0));
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

export type Story = { groups: GroupSpec[] };

export function Episode3D<S extends Story>({ storyboard, build, overlays }: {
  storyboard: StoryboardInput; build: (T: Timing) => S; overlays?: (s: S) => React.ReactNode;
}) {
  waitForFonts();
  const { fps } = useVideoConfig();
  const sb = useMemo(() => {
    const s = parseStoryboard(storyboard);
    if (s.captions) {
      const words = s.captions.words.map((w, i) => (i === 0 && w.start < 0.4 ? { ...w, start: 0 } : w));   // frame 0 is the cover: it carries the first words
      s.captions = { ...s.captions, words, style: { ...s.captions.style, fontSize: CAP_SIZE, maxWidth: CAP_W } };
    }
    return s;
  }, [storyboard]);
  const { timings } = useMemo(() => sceneTimings(sb), [sb]);
  const story = useMemo(() => build(new Timing(sb.scenes.map((s) => s.duration), sb.captions?.words ?? [])), [sb, build]);
  const cuts = useMemo(() => timings.slice(1).map((tm) => tm.start / fps), [timings, fps]);
  const placement = useMemo(() => (sb.captions ? captionCues(story.groups, paginate(sb.captions.words, sb.captions, cuts), fps, sb.captions.style.y ?? 0.72) : []),
    [sb, story, cuts, fps]);
  // the 3D worlds draw text into canvases (labels, tags): build them only once the fonts are in
  const [fontsReady, setReady] = useState(false);
  const [handle] = useState(() => delayRender("three-lane fonts"));
  useEffect(() => {
    Promise.all([document.fonts.load('400 64px "Anton"'), document.fonts.load('900 64px "Montserrat"')])
      .catch(() => null).finally(() => { setReady(true); continueRender(handle); });
  }, [handle]);
  const groups = story.groups;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {fontsReady && groups.map((g, i) => {
        const nx = groups[i + 1]?.xfade ?? 0;
        const from = Math.round((g.t0 - g.xfade / 2) * fps);
        const to = Math.round((g.t1 + nx / 2) * fps);
        return (
          <Sequence key={g.id} from={from} durationInFrames={Math.max(1, to - from)} name={g.id} layout="none">
            <Fade g={g} from={from} total={Math.max(1, to - from)} nOut={Math.round(nx * fps)} />
          </Sequence>
        );
      })}
      {overlays ? overlays(story) : null}
      {sb.captions ? <CaptionTrack captions={sb.captions} format={sb.format} theme={sb.theme} placement={placement} cuts={cuts} /> : null}
    </AbsoluteFill>
  );
}

/** place changes are whip pans, never dissolves (v1/v4 review: any opacity blend ghosted one place over the other):
 * the outgoing shot smears out (blur rising, a slight push) up to the cut point, the incoming shot starts there fully
 * smeared and sharpens. The two are never drawn at once, so no frame mixes two places. */
const Fade: React.FC<{ g: GroupSpec; from: number; total: number; nOut: number }> = ({ g, from, total, nOut }) => {
  const frame = useCurrentFrame();
  const n = Math.round(g.xfade * 30);
  // a whip is n frames centred on the cut: blur and sideways travel rise to the cut and fall after it; the two shots
  // overlap only in the OV most-smeared frames at the cut (v8 review: a 6-frame overlap still read as a dissolve)
  const OV = 2;
  const half = Math.floor(n / 2), outHalf = nOut - Math.floor(nOut / 2);
  if (n > 0 && frame < half - OV / 2) return null;
  if (nOut > 0 && frame >= total - outHalf + OV / 2) return null;
  const din = n > 0 ? Math.abs(frame - half) / Math.max(1, half) : 1;                 // 0 at the cut .. 1 at the whip's edge
  const dout = nOut > 0 ? Math.abs(frame - (total - outHalf)) / Math.max(1, outHalf) : 1;
  const inWhip = n > 0 && frame < n, outWhip = nOut > 0 && frame >= total - nOut;
  const k = Math.max(inWhip ? 1 - Math.min(1, din) : 0, outWhip ? 1 - Math.min(1, dout) : 0);   // 0..1 smear
  // directional travel: the outgoing shot whips off to the left, the incoming one arrives from the right
  const dir = inWhip && frame >= half - OV / 2 && (!outWhip || frame < total - nOut) ? 1 : -1;
  const blur = 13 * Math.sqrt(k), sc = 1 + 0.18 * k, tx = dir * 0.16 * k * 1080;
  const op = n > 0 && frame < half + OV / 2 ? (frame - (half - OV / 2) + 1) / (OV + 1) : 1;  // the incoming shot fades in under the smear
  const style: React.CSSProperties = { ...(blur > 0.3 ? { filter: `blur(${blur.toFixed(1)}px)`, transform: `translateX(${tx.toFixed(1)}px) scale(${sc.toFixed(3)})` } : {}), opacity: Math.max(0, Math.min(1, op)) };
  return (
    <AbsoluteFill style={style}>
      <Stage g={g} fromFrame={from} />
    </AbsoluteFill>
  );
};

/** the overlay clock (global seconds) for episode overlays */
export const useStoryTime = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return f / fps; };
