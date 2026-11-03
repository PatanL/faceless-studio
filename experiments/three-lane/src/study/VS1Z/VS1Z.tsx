// REPLICATION STUDY (internal, never published): the VS1Z first-20-s replica on Episode3D.
// Captions: the reference look (RicksCaptions) with the reference's own page breaks and page-start frames (measured
// from the burnt-in captions by tools/caption_pages.py), so caption timing is not one of the variables under study.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Episode3D } from "../../kit/Episode3D";
import type { CapWord } from "../../kit/captions";
import { buildStudy } from "./story";

// [page start frame, page text]
const PAGES: [number, string][] = [[0, "He"], [4, "put a"], [10, "bronze"], [23, "ball in"], [37, "a dragon's"], [53, "mouth"], [65, "and"], [72, "told"],
  [79, "the emperor,"], [96, "if"], [101, "this ever"], [117, "falls"], [126, "out,"], [136, "run."], [154, "The whole court"], [180, "burst"], [193, "out"],
  [198, "laughing."], [214, "You"], [218, "see,"], [227, "there"], [234, "were"], [239, "eight"], [248, "dragons"], [264, "coiled"], [276, "around"],
  [285, "a giant"], [301, "bronze"], [312, "jar,"], [325, "each"], [334, "holding"], [342, "a ball"], [356, "over"], [363, "a frog's"], [378, "open"],
  [387, "mouth."], [398, "But"], [404, "the emperor"], [420, "had the"], [427, "biggest"], [442, "army"], [450, "in the world,"], [469, "and"],
  [475, "he wasn't"], [487, "about"], [496, "to run"], [505, "from"], [512, "a jar."], [529, "Weeks"], [539, "later,"], [552, "a ball"], [566, "fell,"],
  [576, "but"], [582, "nothing"], [594, "happened."]];
export const STUDY_WORDS: (CapWord & { br: boolean })[] = PAGES.map(([f, text], i) => ({ text, start: f / 30, end: (PAGES[i + 1]?.[0] ?? 600) / 30, br: true }));

/** the snap punch-in's speed lines (reference F142-F160): white wedges from the frame edge toward the face, redrawn every 2 f */
const SpeedLines: React.FC<{ f0: number; f1: number; cx: number; cy: number }> = ({ f0, f1, cx, cy }) => {
  const f = useCurrentFrame();
  if (f < f0 || f >= f1) return null;
  const k = Math.floor((f - f0) / 2), fade = Math.min(1, (f1 - f) / 4);
  const r = (n: number) => { const x = Math.sin(n * 12.9898 + k * 78.233) * 43758.5453; return x - Math.floor(x); };
  const lines = Array.from({ length: 22 }, (_, i) => {
    const a = (i / 22) * Math.PI * 2 + r(i) * 0.25, r0 = 520 + r(i + 40) * 380, r1 = 1500;
    const w = 3 + r(i + 80) * 7;
    const p = (rad: number, da: number) => `${cx + Math.cos(a + da) * rad},${cy + Math.sin(a + da) * rad}`;
    return <polygon key={i} points={`${p(r0, 0)} ${p(r1, w / r1)} ${p(r1, -w / r1)}`} fill="#ffffff" opacity={0.85 * fade} />;
  });
  return <AbsoluteFill><svg width="100%" height="100%" viewBox="0 0 1080 1920">{lines}</svg></AbsoluteFill>;
};

export const VS1Z: React.FC = () => (
  <Episode3D words={STUDY_WORDS} durations={[20]} build={buildStudy} captions="ricks-phrase" gates="warn"
    overlays={() => <SpeedLines f0={142} f1={160} cx={600} cy={1050} />} />
);
