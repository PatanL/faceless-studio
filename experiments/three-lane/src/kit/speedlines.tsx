// Speed lines (round 3, replication lesson 8, promoted from the VS1Z study): white wedges from the frame edge toward a
// screen point, redrawn every 2 frames, for the snap punch-in on a hook's loudest word (rule E7). An Episode3D overlay:
//   overlays={() => <SpeedLines f0={142} f1={160} cx={600} cy={1050} />}     (frames; cx, cy in 1080 x 1920 px)
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

export const SpeedLines: React.FC<{ f0: number; f1: number; cx: number; cy: number; n?: number; inner?: number; color?: string }> = ({ f0, f1, cx, cy, n = 22, inner = 520, color = "#ffffff" }) => {
  const f = useCurrentFrame();
  if (f < f0 || f >= f1) return null;
  const k = Math.floor((f - f0) / 2), fade = Math.min(1, (f1 - f) / 4);
  const r = (m: number) => { const x = Math.sin(m * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
  const lines = Array.from({ length: n }, (_, i) => {
    const a = (i / n) * Math.PI * 2 + r(i) * 0.25, r0 = inner + r(i + 40) * 380, r1 = 1500, w = 3 + r(i + 80) * 7;
    const p = (rad: number, da: number) => `${cx + Math.cos(a + da) * rad},${cy + Math.sin(a + da) * rad}`;
    return <polygon key={i} points={`${p(r0, 0)} ${p(r1, w / r1)} ${p(r1, -w / r1)}`} fill={color} opacity={0.85 * fade} />;
  });
  return <AbsoluteFill><svg width="100%" height="100%" viewBox="0 0 1080 1920">{lines}</svg></AbsoluteFill>;
};
