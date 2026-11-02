// POV views (our own code; RICKSCLIPS_RULEBOOK S8 "POV", T7 iris transitions). A POV is any set shot from a
// character's eye with a lens mask over it: a spyglass circle, a keyhole or binoculars. The mask irises open over
// 3-10 frames at t0 and shut at t1 (on 1s), the hole drifts a little with the hand, and the mask colour is a deep
// violet, never pure black (L6). Use it as an EpisodeNext / Episode3D overlay for the POV group's time range, and
// povKey() for the camera.
import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import type { CamKey } from "./campath";
import type { V3 } from "./Stage";

export type PovKind = "spyglass" | "keyhole" | "binoculars";
const sm = (u: number) => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };

/** enter / exit: "shut" irises from / to a closed lens (T7), "open" closes in from / opens out to the full frame (the
 * mask arrives over a shot already playing, as after a push through a window) */
export const PovMask: React.FC<{ kind?: PovKind; t0: number; t1: number; irisF?: number; color?: string; r?: number; cy?: number; enter?: "shut" | "open"; exit?: "shut" | "open" }> = ({ kind = "spyglass", t0, t1, irisF = 7, color = "#160f2c", r = 0.44, cy = 0.42, enter = "shut", exit = "shut" }) => {
  const frame = useCurrentFrame();
  const { fps, width: W, height: H } = useVideoConfig();
  const t = frame / fps;
  if (t < t0 || t >= t1) return null;
  const fIn = Math.floor((t - t0) * fps + 1e-6), fOut = Math.floor((t1 - t) * fps + 1e-6);
  const diag = Math.hypot(W, H) / W;                                  // radius (in widths) that clears every corner
  const kIn = sm((fIn + 1) / irisF), kOut = sm((fOut + 1) / irisF);
  const rIn = enter === "shut" ? r * kIn : diag + (r - diag) * kIn;
  const rOut = exit === "shut" ? r * kOut : diag + (r - diag) * kOut;
  const R = (fIn < irisF ? rIn : fOut < irisF ? rOut : r) * W;
  const cx = W / 2 + Math.sin(t * 1.3) * 10, y = cy * H + Math.cos(t * 1.1) * 8;    // the hand drifts the lens
  let hole = "";
  if (kind === "spyglass") hole = `M ${cx - R} ${y} a ${R} ${R} 0 1 0 ${2 * R} 0 a ${R} ${R} 0 1 0 ${-2 * R} 0 Z`;
  else if (kind === "binoculars") { const rr = R * 0.72, dx = rr * 0.86; hole = [-dx, dx].map((o) => `M ${cx + o - rr} ${y} a ${rr} ${rr} 0 1 0 ${2 * rr} 0 a ${rr} ${rr} 0 1 0 ${-2 * rr} 0 Z`).join(" "); }
  else { const k = R * 0.62; hole = `M ${cx - k} ${y} a ${k} ${k} 0 1 1 ${2 * k} 0 L ${cx + k * 0.55} ${y + R * 1.5} L ${cx - k * 0.55} ${y + R * 1.5} Z`; }
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", left: 0, top: 0, pointerEvents: "none" }}>
      <path d={`M 0 0 H ${W} V ${H} H 0 Z ${hole}`} fill={color} fillRule="evenodd" />
      {kind === "spyglass" && R > 4 && <g fill="none">
        <circle cx={cx} cy={y} r={R + 10} stroke="#c9963a" strokeWidth={22} />
        <circle cx={cx} cy={y} r={R + 10} stroke="#1b1240" strokeWidth={6} />
        <circle cx={cx} cy={y} r={R + 22} stroke="#1b1240" strokeWidth={6} />
        <path d={`M ${cx - R * 0.25} ${y} H ${cx + R * 0.25} M ${cx} ${y - R * 0.25} V ${y + R * 0.25}`} stroke="rgba(255,255,255,0.35)" strokeWidth={3} />
      </g>}
    </svg>
  );
};

/** a POV camera key: from a character's eye (feet at `feet`, eye 1.55 m up for an adult) toward `look` */
export const povKey = (t: number, feet: V3, look: V3, fov = 30, eye = 1.55): CamKey => ({ t, pos: [feet[0], feet[1] + eye, feet[2]], look, fov, drift: 0.3 });
