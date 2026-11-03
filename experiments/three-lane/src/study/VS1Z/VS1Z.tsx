// REPLICATION STUDY (internal, never published): the VS1Z first-20-s replica on Episode3D.
// Captions: the reference look (RicksCaptions) with the reference's own page breaks and page-start frames (measured
// from the burnt-in captions by tools/caption_pages.py), so caption timing is not one of the variables under study.
import React from "react";
import { Episode3D } from "../../kit/Episode3D";
import type { CapWord } from "../../kit/captions";
import { buildStudy } from "./story";
import { SpeedLines } from "../../kit/speedlines";

// [page start frame, page text]
const PAGES: [number, string][] = [[0, "He"], [4, "put a"], [10, "bronze"], [23, "ball in"], [37, "a dragon's"], [53, "mouth"], [65, "and"], [72, "told"],
  [79, "the emperor,"], [96, "if"], [101, "this ever"], [117, "falls"], [126, "out,"], [136, "run."], [154, "The whole court"], [180, "burst"], [193, "out"],
  [198, "laughing."], [214, "You"], [218, "see,"], [227, "there"], [234, "were"], [239, "eight"], [248, "dragons"], [264, "coiled"], [276, "around"],
  [285, "a giant"], [301, "bronze"], [312, "jar,"], [325, "each"], [334, "holding"], [342, "a ball"], [356, "over"], [363, "a frog's"], [378, "open"],
  [387, "mouth."], [398, "But"], [404, "the emperor"], [420, "had the"], [427, "biggest"], [442, "army"], [450, "in the world,"], [469, "and"],
  [475, "he wasn't"], [487, "about"], [496, "to run"], [505, "from"], [512, "a jar."], [529, "Weeks"], [539, "later,"], [552, "a ball"], [566, "fell,"],
  [576, "but"], [582, "nothing"], [594, "happened."]];
export const STUDY_WORDS: (CapWord & { br: boolean })[] = PAGES.map(([f, text], i) => ({ text, start: f / 30, end: (PAGES[i + 1]?.[0] ?? 600) / 30, br: true }));

export const VS1Z: React.FC = () => (
  <Episode3D words={STUDY_WORDS} durations={[20]} build={buildStudy} captions="ricks-phrase" gates="warn"
    overlays={() => <SpeedLines f0={142} f1={160} cx={600} cy={1050} />} />
);
