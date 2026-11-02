// DressLab (our own code): an A/B of dressing.ts. The same four KitLab sets with the same cameras and no actors,
// rendered bare (flat colour, no props or clouds: the look before) and dressed, for look_density.py.
import React from "react";
import { EpisodeNext, type NextGroup } from "../EpisodeNext";
import { setBare } from "../dressing";
import { roomSet, gearRoomSet, seaSet, deckSet } from "./sets";
import { castKey } from "../castframe";
import type { V3 } from "../../kit/Stage";

const CREW: V3[] = [[0, 0, -1.6], [-0.9, 0, -1.85], [0.9, 0, -1.85]];
const groups = (): NextGroup[] => {
  const room = { t: 1, pos: [3.0, 1.9, 1.4] as V3, look: [-0.6, 0.9, -4.6] as V3, fov: 52 };
  return [
    { id: "deck", t0: 0, t1: 1, xfade: 0, set: deckSet, light: "day", cam: [castKey(0, CREW, "wide", 12, 8, 40)], people: [] },
    { id: "room", t0: 1, t1: 2, xfade: 0, set: () => roomSet(), light: "day", cam: [room], people: [] },
    { id: "gears", t0: 2, t1: 3, xfade: 0, set: gearRoomSet, light: "night", cam: [castKey(2, [[-0.95, 0.2, -3.05]], "wide", -18, 8, 44)], people: [] },
    { id: "sea", t0: 3, t1: 4, xfade: 0, set: seaSet, light: "night", cam: [{ t: 3, pos: [0, 16, 24], look: [6, 2, -50], fov: 34 }], people: [] },
  ];
};
export const DressLab: React.FC<{ bare?: boolean }> = ({ bare = false }) => {
  setBare(bare);
  return <EpisodeNext words={[]} durations={[4]} build={() => ({ groups: groups() })} captions="none" />;
};
