// KitLab (our own code): the proving ground for src/next. One ~37 s Short-shaped reel on the 3D story kit that puts
// every new piece on screen - cutaway sets, word-tied acting, the ghost-free joins, the effects, the light arc and
// the opt-in reference captions - so each can be measured with the repo's tools against the rule book's ranges.
// Composition "KitLab" lives in its own entry (src/next/index.ts) so the shared kit's Root.tsx is untouched.
import React from "react";
import { AbsoluteFill } from "remotion";
import { Episode3D } from "../kit/Episode3D";
import { PovMask } from "../kit/pov";
import { synthWords } from "./kitlab/script";
import { buildLab, type LabStory } from "./kitlab/story";

export const LAB = synthWords();
export const LAB_FRAMES = Math.ceil((LAB.words[LAB.words.length - 1].end + 0.4) * 30);

const Overlays: React.FC<{ s: LabStory }> = ({ s }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <PovMask kind="spyglass" t0={s.pov.t0} t1={s.pov.t1} enter="open" exit="open" irisF={8} />
  </AbsoluteFill>
);

export const KitLab: React.FC<{ captions?: "ricks" | "none" }> = ({ captions = "ricks" }) => (
  <Episode3D words={LAB.words} durations={[LAB_FRAMES / 30]} build={buildLab} overlays={(s) => <Overlays s={s} />} captions={captions} />
);
