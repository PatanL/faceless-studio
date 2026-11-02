// story-vasa v1 (our own code) on the 3D story kit: the shot groups from story.ts, the place tags, and two progress
// instruments drawn in the DOM - a roll gauge (how far she heels, with the danger zone where the lower ports go under)
// and the distance she sails before she sinks. Props are the episode storyboard JSON.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Tag } from "../../../../studio/src/kits/explainer/ui";
import { Episode3D } from "../kit/Episode3D";
import { buildStory, type VasaStory } from "./story";

const W = 1080, H = 1920;
const ink = "#1b1240", cream = "#fff2c0", red = "#e0442e";
const font = '"Anton", Impact, sans-serif';

/** a ship's clinometer: a half dial, the 14 degree mark where the lower gun ports reach the water, a swinging needle */
const RollGauge: React.FC<{ heel: number; o: number }> = ({ heel, o }) => {
  const deg = (heel * 180) / Math.PI;
  const R = 120, cx = 150, cy = 140;
  const pt = (a: number, r: number) => [cx + r * Math.sin((a * Math.PI) / 180), cy - r * Math.cos((a * Math.PI) / 180)];
  const arc = (a0: number, a1: number, r: number) => { const [x0, y0] = pt(a0, r), [x1, y1] = pt(a1, r); return `M ${x0} ${y0} A ${r} ${r} 0 0 1 ${x1} ${y1}`; };
  const [nx, ny] = pt(Math.max(-60, Math.min(60, deg)), R - 12);
  const danger = deg >= 14;
  return (
    <svg width={300} height={190} viewBox="0 0 300 190" style={{ position: "absolute", left: W - 330, top: 250, opacity: o, overflow: "visible" }}>
      <path d={`${arc(-60, 60, R)} L ${cx} ${cy} Z`} fill="rgba(27, 18, 64, 0.88)" stroke={cream} strokeWidth={5} />
      <path d={arc(14, 60, R - 10)} stroke={red} strokeWidth={16} fill="none" />
      {[-45, -30, -15, 0, 15, 30, 45].map((a) => { const [x0, y0] = pt(a, R - 24), [x1, y1] = pt(a, R - 4); return <line key={a} x1={x0} y1={y0} x2={x1} y2={y1} stroke={cream} strokeWidth={a === 0 ? 5 : 3} />; })}
      <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={danger ? red : cream} strokeWidth={8} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={12} fill={cream} />
      <text x={cx} y={cy + 44} textAnchor="middle" fontFamily={font} fontSize={38} fill={danger ? red : cream} letterSpacing={2}>{`${Math.abs(deg).toFixed(0)}°`}</text>
    </svg>
  );
};

/** distance sailed: a small ship marker running along a line to the point where she sank */
const Distance: React.FC<{ m: number; o: number }> = ({ m, o }) => {
  const k = m / 1300;
  return (
    <div style={{ position: "absolute", left: 60, top: 260, width: 520, height: 120, opacity: o }}>
      <div style={{ position: "absolute", left: 0, top: 0, padding: "6px 22px", borderRadius: 40, background: "rgba(27, 18, 64, 0.88)", border: `4px solid ${cream}`,
        fontFamily: font, fontSize: 52, color: k >= 1 ? red : cream, letterSpacing: 2 }}>{`${Math.round(m).toLocaleString("en-US")} m`}</div>
      <div style={{ position: "absolute", left: 10, top: 96, width: 480, height: 8, borderRadius: 4, background: "rgba(27, 18, 64, 0.7)" }} />
      <div style={{ position: "absolute", left: 10, top: 96, width: 480 * k, height: 8, borderRadius: 4, background: cream }} />
      <div style={{ position: "absolute", left: 10 + 480 * k - 14, top: 84, width: 28, height: 28, borderRadius: 14, background: k >= 1 ? red : cream, border: `4px solid ${ink}` }} />
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

export const Vasa3D: React.FC<StoryboardInput> = (props) => (
  <Episode3D storyboard={props} build={buildStory} overlays={(s) => <Overlays s={s} />} />
);
