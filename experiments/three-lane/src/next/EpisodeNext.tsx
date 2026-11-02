// EpisodeNext (our own code): the kit's Episode3D with a richer join grammar and the opt-in reference captions.
// It renders the same GroupSpecs with the same Stage; only the way two groups meet changes, chosen per group by
// `join` (how the group is ENTERED; default = the kit's behaviour from xfade: a whip, or a cut when xfade is 0).
// None of the new joins ever draws two places semi-transparently over each other (RICKSCLIPS_RULEBOOK 1.2: keep the
// dissolve's function, leave its ghost):
//   whip   the kit's whip pan, ported unchanged (blur + sideways travel, the shots overlap only in the 2 most-smeared frames)
//   cut    a hard cut
//   match  a dissolve that holds one object in place: the incoming shot is framed (match.ts matchKey) so its anchor
//          sits exactly where the outgoing anchor sat, and it is revealed by a hard-edged growing disc centred on
//          that anchor over 6-8 f. Every pixel switches once, from A to B; only a thin feathered rim is ever mixed.
//   push   the camera pushes through an opening in the outgoing shot (window, eye, screen, photo): the incoming shot
//          shows through the opening's projected outline (a clip, not a blend) until the opening fills the frame.
//   into   frame-in-frame: the outgoing shot freezes and shrinks into a prop of the incoming shot (a photo, monitor,
//          fishbowl), mapped by a homography onto the prop's projected quad, and stays there (frozen = free to render)
//   outOf  the reverse: the incoming shot starts frozen inside a prop of the outgoing shot and grows out of it to
//          fill the frame, then starts moving
import React, { useEffect, useMemo, useState } from "react";
import { AbsoluteFill, Freeze, Sequence, continueRender, delayRender, useCurrentFrame, useVideoConfig } from "remotion";
import { parseStoryboard, sceneTimings, type StoryboardInput } from "../../../../studio/src/core/schema";
import { CaptionTrack, paginate } from "../../../../studio/src/core/captions";
import { waitForFonts } from "../../../../studio/src/core/fonts";
import { Stage, type GroupSpec } from "../kit/Stage";
import { Timing } from "../kit/timing";
import { captionCues, CAP_SIZE, CAP_W } from "../kit/Episode3D";
import { RicksCaptions, type CapWord } from "./captions";
import { clipCss, covers, homography, W, H, type Shape } from "./match";

export type Join =
  | { kind: "whip"; dur?: number }
  | { kind: "cut" }
  | { kind: "match"; frames?: number; anchor: (t: number) => [number, number]; feather?: number }
  | { kind: "push"; frames: number; portal: (t: number) => Shape }
  | { kind: "into"; frames: number; quad: (t: number) => [number, number][]; until?: number }
  | { kind: "outOf"; frames: number; quad: (t: number) => [number, number][]; pre?: number };
export type NextGroup = GroupSpec & { join?: Join; place?: string; insert?: boolean };
export type NextStory = { groups: NextGroup[] };

const sm = (u: number) => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
const joinOf = (g: NextGroup | undefined): Join | null => (!g ? null : g.join ?? (g.xfade > 0 ? { kind: "whip", dur: g.xfade } : { kind: "cut" }));
const whipF = (j: Join | null, fps: number) => (j && j.kind === "whip" ? Math.round((j.dur ?? 0.4) * fps) : 0);
const FULL: [number, number][] = [[0, 0], [W, 0], [W, H], [0, H]];
const lerpQuad = (a: [number, number][], b: [number, number][], u: number) => a.map(([x, y], i) => [x + (b[i][0] - x) * u, y + (b[i][1] - y) * u] as [number, number]);

type Style = (abs: number) => React.CSSProperties | null;
/** host: the style of the shot this layer lives inside (a push's opening, a prop's picture), so the host's whip
 * (blur, travel, scale, fade) carries the inner shot with it; only its transform / filter / opacity are taken */
type Layer = { key: string; g: NextGroup; from: number; to: number; kind: "main" | "inset"; freezeAt?: number; style: Style; host?: Style };
const carry = (s: React.CSSProperties | null): React.CSSProperties | null => (s ? { transform: s.transform, filter: s.filter, opacity: s.opacity } : null);

/** frame ranges and per-frame styles of every layer (main shots, then the frozen frame-in-frame insets on top) */
export function layersOf(groups: NextGroup[], fps: number, endFrame?: number): Layer[] {
  const L: Layer[] = [], insets: Layer[] = [];
  groups.forEach((g, i) => {
    const inJ = i === 0 ? null : joinOf(g), outJ = joinOf(groups[i + 1]);
    const T = Math.round(g.t0 * fps), T1 = Math.round(g.t1 * fps);
    const nIn = whipF(inJ, fps), nOut = whipF(outJ, fps);
    let from = T, to = T1;
    if (inJ?.kind === "whip") from = Math.round((g.t0 - nIn / fps / 2) * fps);
    if (inJ?.kind === "match") from = T - Math.floor((inJ.frames ?? 7) / 2);
    if (inJ?.kind === "push") from = T - inJ.frames;
    if (outJ?.kind === "whip") to = Math.round((g.t1 + nOut / fps / 2) * fps);
    if (outJ?.kind === "match") to = T1 + ((outJ.frames ?? 7) - Math.floor((outJ.frames ?? 7) / 2));
    if (i === groups.length - 1 && endFrame) to = Math.max(to, endFrame);       // the last shot runs to the last frame
    const total = Math.max(1, to - from);
    const outgoing = L[L.length - 1];
    L.push({
      host: inJ?.kind === "push" && outgoing ? (abs) => (abs < T ? carry(outgoing.style(abs)) : {}) : undefined,
      key: `m-${g.id}-${i}`, g, from, to, kind: "main",
      style: (abs) => {
        const frame = abs - from;
        // ---- the kit's whip (Episode3D Fade, unchanged numbers)
        const OV = 2, half = Math.floor(nIn / 2), outHalf = nOut - Math.floor(nOut / 2);
        if (nIn > 0 && frame < half - OV / 2) return null;
        if (nOut > 0 && frame >= total - outHalf + OV / 2) return null;
        const din = nIn > 0 ? Math.abs(frame - half) / Math.max(1, half) : 1;
        const dout = nOut > 0 ? Math.abs(frame - (total - outHalf)) / Math.max(1, outHalf) : 1;
        const inWhip = nIn > 0 && frame < nIn, outWhip = nOut > 0 && frame >= total - nOut;
        const k = Math.max(inWhip ? 1 - Math.min(1, din) : 0, outWhip ? 1 - Math.min(1, dout) : 0);
        const dir = inWhip && frame >= half - OV / 2 && (!outWhip || frame < total - nOut) ? 1 : -1;
        const blur = 13 * Math.sqrt(k), sc = 1 + 0.18 * k, tx = dir * 0.16 * k * 1080;
        const op = nIn > 0 && frame < half + OV / 2 ? (frame - (half - OV / 2) + 1) / (OV + 1) : 1;
        const st: React.CSSProperties = { ...(blur > 0.3 ? { filter: `blur(${blur.toFixed(1)}px)`, transform: `translateX(${tx.toFixed(1)}px) scale(${sc.toFixed(3)})` } : {}), opacity: Math.max(0, Math.min(1, op)) };
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
        // ---- push: clipped to the opening's outline until it covers the frame
        if (inJ?.kind === "push" && abs < T) {
          const sh = inJ.portal(t);
          const clip = covers(sh) ? undefined : clipCss(sh);
          if (clip) Object.assign(st, { clipPath: clip, WebkitClipPath: clip });
        }
        return st;
      },
    });
    // ---- frame-in-frame insets (frozen shots mapped onto a prop quad), drawn above the main layers
    if (outJ?.kind === "into") {
      const nx = groups[i + 1], until = Math.round((outJ.until ?? nx.t1) * fps);
      const self = L.length;     // the incoming main layer is pushed next; its style hosts the inset
      insets.push({ key: `i-${g.id}`, g, from: T1, to: until, kind: "inset", freezeAt: T1 - 1, host: (abs) => carry(L[self].style(abs)),
        style: (abs) => { const u = sm((abs - T1 + 1) / outJ.frames); const q = lerpQuad(FULL, outJ.quad(abs / fps), u); return { transformOrigin: "0 0", transform: homography(q) }; } });
    }
    if (inJ?.kind === "outOf") {
      const s = T - inJ.frames - Math.round((inJ.pre ?? 0.6) * fps);
      const outgoing = L[L.length - 2];
      insets.push({ key: `o-${g.id}`, g, from: s, to: T, kind: "inset", freezeAt: T, host: (abs) => carry(outgoing.style(abs)),
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

export function EpisodeNext<S extends NextStory>({ storyboard, words: wordsIn, durations, build, overlays, captions = "house" }: {
  storyboard?: StoryboardInput; words?: CapWord[]; durations?: number[];
  build: (T: Timing) => S; overlays?: (s: S) => React.ReactNode; captions?: "house" | "ricks" | "none";
}) {
  waitForFonts();
  const { fps, durationInFrames } = useVideoConfig();
  const sb = useMemo(() => {
    if (!storyboard) return null;
    const s = parseStoryboard(storyboard);
    if (s.captions) {
      const ws = s.captions.words.map((w, i) => (i === 0 && w.start < 0.4 ? { ...w, start: 0 } : w));
      s.captions = { ...s.captions, words: ws, style: { ...s.captions.style, fontSize: CAP_SIZE, maxWidth: CAP_W } };
    }
    return s;
  }, [storyboard]);
  const words: CapWord[] = useMemo(() => wordsIn ?? (sb?.captions?.words ?? []), [wordsIn, sb]);
  const durs = useMemo(() => durations ?? (sb ? sb.scenes.map((s) => s.duration) : [words.length ? words[words.length - 1].end + 0.5 : 1]), [durations, sb, words]);
  const story = useMemo(() => build(new Timing(durs, words)), [durs, words, build]);
  const layers = useMemo(() => layersOf(story.groups, fps, durationInFrames), [story, fps, durationInFrames]);
  const timings = useMemo(() => (sb ? sceneTimings(sb).timings : []), [sb]);
  const cuts = useMemo(() => timings.slice(1).map((tm) => tm.start / fps), [timings, fps]);
  const placement = useMemo(() => (sb?.captions && captions === "house" ? captionCues(story.groups, paginate(sb.captions.words, sb.captions, cuts), fps, sb.captions.style.y ?? 0.72) : []), [sb, story, cuts, fps, captions]);
  const [fontsReady, setReady] = useState(false);
  const [handle] = useState(() => delayRender("three-lane next fonts"));
  useEffect(() => {
    Promise.all([document.fonts.load('400 64px "Anton"'), document.fonts.load('900 64px "Montserrat"'), document.fonts.load('800 64px "Montserrat"'), document.fonts.load('700 64px "Montserrat"')])
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
    </AbsoluteFill>
  );
}
