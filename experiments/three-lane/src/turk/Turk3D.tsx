// story-chess-turk v7 (our own code): the 3D story lane composition. Props are the episode storyboard JSON (built by
// the pipeline with caption_rule "phrase"); it supplies the scene durations, the Kokoro word timings and the caption
// style. Each shot group (story.ts) is one ThreeCanvas Sequence; different places join with a 7-frame crossfade (the
// references' 6-8 frame scene dissolves), the fire and the reveal are hard cuts, and every angle change inside a
// place is a camera move. Captions, tags, the title and the newspaper are DOM overlays. Video only: the narration
// mix is muxed afterwards.
import React, { useEffect, useMemo, useState } from "react";
import * as THREE from "three";
import { AbsoluteFill, Sequence, continueRender, delayRender, useCurrentFrame, useVideoConfig } from "remotion";
import { parseStoryboard, sceneTimings, type StoryboardInput } from "../../../../studio/src/core/schema";
import { CaptionTrack, paginate, type CaptionCue } from "../../../../studio/src/core/captions";
import { waitForFonts } from "../../../../studio/src/core/fonts";
import { Headline, Tag } from "../../../../studio/src/kits/explainer/ui";
import { Stage, type GroupSpec } from "./Stage";
import { CamPath } from "./campath";
import { Timing } from "./timing";
import { buildStory, type Tag as TagSpec } from "./story";
import { Newspaper } from "./Newspaper";

const W = 1080, H = 1920;
// phrase pages run to two lines (caption_rule "phrase"), so this episode's captions are a little smaller than the house 84
const CAP_SIZE = 74, CAP_W = 880;

/** caption y per page: keep the caption band off the cabinet + automaton (projected from the story's own cameras) */
function captionCues(groups: GroupSpec[], pages: { start: number; end: number; words: { text: string }[] }[], fps: number, y0: number): CaptionCue[] {
  const paths = new Map<GroupSpec, CamPath>();
  const cam = new THREE.PerspectiveCamera(40, W / H, 0.05, 200);
  const corners: THREE.Vector3[] = [];
  for (const x of [-0.66, 0.66]) for (const y of [0, 1.0, 1.9]) for (const z of [-0.42, 0.42]) corners.push(new THREE.Vector3(x, y, z));
  const box = (t: number) => {
    const g = [...groups].reverse().find((q) => t >= q.t0 - 1e-6 && t < q.t1) ?? groups[groups.length - 1];
    if (!g.cabinet) return null;
    if (!paths.has(g)) paths.set(g, new CamPath(g.cam, g.t0, g.t1));
    const c = paths.get(g)!.at(t);
    cam.fov = c.fov; cam.position.copy(c.pos); cam.lookAt(c.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const [cx, cy, cz] = g.cabinet.at(t);
    const rot = g.cabinet.rotY ?? 0;
    let x0 = Infinity, x1 = -Infinity, yA = Infinity, yB = -Infinity, front = false;
    for (const p of corners) {
      const q = p.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), rot).add(new THREE.Vector3(cx, cy, cz));
      const v = q.clone().applyMatrix4(cam.matrixWorldInverse);
      if (v.z > -0.05) { front = true; continue; }
      q.project(cam);
      const sx = (q.x * 0.5 + 0.5) * W, sy = (0.5 - q.y * 0.5) * H;
      x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); yA = Math.min(yA, sy); yB = Math.max(yB, sy);
    }
    if (front) return { x0: 0, x1: W, y0: 0, y1: H };
    return { x0, x1, y0: yA, y1: yB };
  };
  const cands = [y0, 0.79, 0.3, 0.24];
  const cues: CaptionCue[] = [];
  for (const p of pages) {
    const glyphs = p.words.reduce((n, w) => n + w.text.length, 0) * 0.76 + (p.words.length - 1) * 0.36;
    const lines = Math.ceil((glyphs * CAP_SIZE) / CAP_W);
    const half = Math.min(CAP_W, glyphs * CAP_SIZE) / 2 + 20, bandH = lines * CAP_SIZE * 0.55 + 24;
    const cx = W / 2 - 20;
    let best = cands[0], bestCost = Infinity;
    for (const y of cands) {
      const top = y * H - bandH, bot = y * H + bandH;
      let cost = 0;
      for (let t = p.start; t < p.end; t += 1 / fps * 3) {
        const b = box(t);
        if (!b) continue;
        const ox = Math.max(0, Math.min(cx + half, b.x1) - Math.max(cx - half, b.x0));
        const oy = Math.max(0, Math.min(bot, b.y1) - Math.max(top, b.y0));
        cost += ox * oy;
      }
      cost += (y === cands[0] ? 0 : 400);        // stay at the house position unless it actually overlaps
      if (cost < bestCost - 1) { best = y; bestCost = cost; }
    }
    cues.push({ at: p.start - 0.001, y: best });
  }
  return cues;
}

const Overlays: React.FC<{ tags: TagSpec[]; headlineOut: number; paperAt: number; paperOut: number }> = ({ tags, headlineOut, paperAt, paperOut }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const box = (x: number, y: number, w: number, h: number, el: React.ReactNode) => (
    <div style={{ position: "absolute", left: x * W - w / 2, top: y * H - h / 2, width: w, height: h }}>{el}</div>
  );
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {t < headlineOut + 0.5 && box(0.5, 0.1, 960, 240,
        <Headline props={{ text: "UNBEATABLE ROBOT", red: "ROBOT", at: -0.6, size: 88, out: headlineOut }} time={t} frame={frame} fps={fps} width={960} height={240} sceneDuration={60} />)}
      {tags.map((g, i) => (t >= g.at - 0.1 && t < g.out + 0.5 ? (
        <React.Fragment key={i}>
          {box(0.5, 0.14, 1000, 130, <Tag props={{ text: g.text, at: g.at, size: 46, out: g.out, align: "center" }} time={t} frame={frame} fps={fps} width={1000} height={130} sceneDuration={60} />)}
        </React.Fragment>) : null))}
      {t >= paperAt && t < paperOut && <Newspaper t={t - paperAt} />}
    </AbsoluteFill>
  );
};

export const Turk3D: React.FC<StoryboardInput> = (props) => {
  waitForFonts();
  const { fps } = useVideoConfig();
  const sb = useMemo(() => {
    const s = parseStoryboard(props);
    if (s.captions) s.captions = { ...s.captions, style: { ...s.captions.style, fontSize: CAP_SIZE, maxWidth: CAP_W } };
    return s;
  }, [props]);
  const { timings } = useMemo(() => sceneTimings(sb), [sb]);
  const story = useMemo(() => {
    const T = new Timing(sb.scenes.map((s) => s.duration), sb.captions?.words ?? []);
    return buildStory(T);
  }, [sb]);
  const cuts = useMemo(() => timings.slice(1).map((tm) => tm.start / fps), [timings, fps]);
  const placement = useMemo(() => {
    if (!sb.captions) return [];
    const pages = paginate(sb.captions.words, sb.captions, cuts);
    return captionCues(story.groups, pages, fps, sb.captions.style.y ?? 0.72);
  }, [sb, story, cuts, fps]);
  // the 3D worlds draw text into canvases (map labels, 3D tags): build them only once the fonts are in
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
            <Fade g={g} from={from} />
          </Sequence>
        );
      })}
      <Overlays tags={story.tags} headlineOut={story.headlineOut} paperAt={story.paperAt} paperOut={story.paperOut} />
      {sb.captions ? <CaptionTrack captions={sb.captions} format={sb.format} theme={sb.theme} placement={placement} cuts={cuts} /> : null}
    </AbsoluteFill>
  );
};

const Fade: React.FC<{ g: GroupSpec; from: number }> = ({ g, from }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = Math.round(g.xfade * fps);
  const o = n > 0 ? Math.min(1, (frame + 1) / (n + 1)) : 1;
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <Stage g={g} fromFrame={from} />
    </AbsoluteFill>
  );
};
