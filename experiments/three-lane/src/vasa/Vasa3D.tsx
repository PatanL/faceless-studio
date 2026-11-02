// story-vasa v1 (our own code) on the 3D story kit: the shot groups from story.ts, the place tags, and two progress
// instruments drawn in the DOM - a roll gauge (how far she heels, with the danger zone where the lower ports go under)
// and the distance she sails before she sinks. Props are the episode storyboard JSON.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Tag } from "../../../../studio/src/kits/explainer/ui";
import { Episode3D, type ScreenRect } from "../kit/Episode3D";
import { buildStory, type VasaStory } from "./story";

const W = 1080, H = 1920;
const ink = "#1b1240", cream = "#fff2c0", red = "#e0442e";
const font = '"Anton", Impact, sans-serif';

/** a ship's clinometer on its own plate (it must read over masts and heads): a half dial with red danger zones on both
 * sides from 14 degrees (the lower gun ports reach the water), a swinging needle and a large readout */
const RollGauge: React.FC<{ heel: number; o: number }> = ({ heel, o }) => {
  const deg = (heel * 180) / Math.PI;
  const R = 112, cx = 150, cy = 136;
  const pt = (a: number, r: number) => [cx + r * Math.sin((a * Math.PI) / 180), cy - r * Math.cos((a * Math.PI) / 180)];
  const arc = (a0: number, a1: number, r: number) => { const [x0, y0] = pt(a0, r), [x1, y1] = pt(a1, r); return `M ${x0} ${y0} A ${r} ${r} 0 0 1 ${x1} ${y1}`; };
  const [nx, ny] = pt(Math.max(-60, Math.min(60, deg)), R - 12);
  const danger = Math.abs(deg) >= 14;
  return (
    <svg width={345} height={300} viewBox="0 -40 300 270" style={{ position: "absolute", left: W - 385, top: 330, opacity: o, overflow: "visible" }}>
      <rect x={10} y={-36} width={280} height={262} rx={34} fill="rgba(27, 18, 64, 0.92)" stroke={cream} strokeWidth={5} />
      <text x={cx} y={-2} textAnchor="middle" fontFamily={font} fontSize={34} fill={cream} letterSpacing={4}>HEEL</text>
      <path d={arc(14, 60, R - 8)} stroke={red} strokeWidth={16} fill="none" />
      <path d={arc(-60, -14, R - 8)} stroke={red} strokeWidth={16} fill="none" />
      {[-45, -30, -15, 0, 15, 30, 45].map((a) => { const [x0, y0] = pt(a, R - 26), [x1, y1] = pt(a, R - 2); return <line key={a} x1={x0} y1={y0} x2={x1} y2={y1} stroke={cream} strokeWidth={a === 0 ? 5 : 3} />; })}
      <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={danger ? red : cream} strokeWidth={9} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={12} fill={cream} />
      <text x={cx} y={cy + 72} textAnchor="middle" fontFamily={font} fontSize={68} fill={danger ? red : cream} letterSpacing={2}>{`${Math.abs(deg).toFixed(0)}°`}</text>
    </svg>
  );
};

/** distance sailed: a ship marker running along a track that ends where she sank (1,300 m) */
const Distance: React.FC<{ m: number; o: number }> = ({ m, o }) => {
  const k = m / 1300;
  return (
    <div style={{ position: "absolute", left: 40, top: 340, width: 590, height: 170, opacity: o, background: "rgba(27, 18, 64, 0.88)", borderRadius: 30, border: `4px solid ${cream}` }}>
      <div style={{ position: "absolute", left: 24, top: 8, fontFamily: font, fontSize: 42, color: cream, letterSpacing: 3 }}>DISTANCE</div>
      <div style={{ position: "absolute", right: 24, top: 6, fontFamily: font, fontSize: 60, color: k >= 1 ? red : cream, letterSpacing: 2 }}>{`${Math.round(m).toLocaleString("en-US")} m`}</div>
      <div style={{ position: "absolute", left: 24, top: 118, width: 500, height: 12, borderRadius: 5, background: "rgba(255, 242, 192, 0.25)" }} />
      <div style={{ position: "absolute", left: 24, top: 118, width: 500 * k, height: 12, borderRadius: 5, background: cream }} />
      <div style={{ position: "absolute", left: 24 + 500 * k - 15, top: 109, width: 30, height: 30, borderRadius: 15, background: k >= 1 ? red : cream, border: `4px solid ${ink}` }} />
      <div style={{ position: "absolute", left: 24 + 500 - 4, top: 103, width: 8, height: 42, background: red, borderRadius: 4 }} />
    </div>
  );
};

const Overlays: React.FC<{ s: VasaStory }> = ({ s }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const fadeOf = (f: (t: number) => number | null) => {
    let o = 0;
    for (const d of [-0.25, 0, 0.25]) if (f(t + d) !== null) o += 1 / 3;
    return o;
  };
  const heel = s.heel(t), dist = s.dist(t);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {s.tags.map((g, i) => (t >= g.at - 0.1 && t < g.out + 0.5 ? (
        <div key={i} style={{ position: "absolute", left: 0.5 * W - 500, top: 0.14 * H - 65, width: 1000, height: 130 }}>
          <Tag props={{ text: g.text, at: g.at, size: 46, out: g.out, align: "center" }} time={t} frame={frame} fps={fps} width={1000} height={130} sceneDuration={60} />
        </div>) : null))}
      {heel !== null || fadeOf(s.heel) > 0 ? <RollGauge heel={heel ?? s.heel(t - 0.25) ?? s.heel(t + 0.25) ?? 0} o={fadeOf(s.heel)} /> : null}
      {dist !== null || fadeOf(s.dist) > 0 ? <Distance m={dist ?? s.dist(t - 0.25) ?? 0} o={fadeOf(s.dist)} /> : null}
    </AbsoluteFill>
  );
};

/** where the gauge and the distance panel sit (captions keep off them; also used by the caption gate) */
export const hudRects = (s: VasaStory, t: number): ScreenRect[] => [
  ...(s.heel(t) !== null ? [{ x0: W - 385, x1: W - 40, y0: 290, y1: 630 }] : []),
  ...(s.dist(t) !== null ? [{ x0: 40, x1: 630, y0: 340, y1: 510 }] : []),
];

export const Vasa3D: React.FC<StoryboardInput> = (props) => (
  // gates "warn": Vasa was finished before the kit gates existed (its gate report is in docs/RND_LOG.md)
  <Episode3D storyboard={props} build={buildStory} overlays={(s) => <Overlays s={s} />} screenAvoid={hudRects} gates="warn" />
);
