// The chess Turk as a kit rig (our own code): the modelled cabinet and board, the stick-kit automaton seated behind
// it as a card, and the hidden master's card inside. story.ts describes it per shot group with a CabinetSpec; toKit()
// turns a TurkGroup into a plain kit GroupSpec (the cabinet rig first, then the group's own extras).
import React from "react";
import * as THREE from "three";
import type { Ctx, GroupSpec, Rig, V3 } from "../kit/Stage";
import { PERSON_VB } from "../kit/Stage";
import { Person } from "../../../../studio/src/kits/explainer/stick/person";
import { Turk } from "../../../../studio/src/kits/explainer/stick/turk";
import { SvgTex, svgMarkup } from "../kit/svgtex";
import { Card3D } from "../kit/card3d";
import { Cabinet, CabState, TURK_CARD } from "./cabinet";
import type { ChessState } from "./chess3d";

export type CabinetSpec = {
  at: (t: number) => V3; rotY?: number; setup?: string;
  state: (t: number) => CabState;
  chess?: (t: number) => Omit<ChessState, "t">;
  turk: (t: number) => Record<string, unknown>;
  turkChar?: (t: number) => number; turkBurn?: (t: number) => number;
  master?: (t: number) => Record<string, unknown>;
  masterDark?: (t: number) => number;
};
export type TurkCtx = Ctx & { cabinet: Cabinet | null };
export type TurkGroup = Omit<GroupSpec, "rigs"> & {
  cabinet?: CabinetSpec;
  extras?: (ctx: TurkCtx) => (t: number, cam: THREE.PerspectiveCamera) => void;
};

const TURK_VB = { w: 900, h: 1000, padT: 300 };

function cabinetRig(spec: CabinetSpec, hold: { cabinet: Cabinet | null }): Rig {
  return (ctx) => {
    const cabinet = new Cabinet(spec.setup ?? "mid");
    hold.cabinet = cabinet;
    ctx.root.add(cabinet.group);
    const tt = new SvgTex(640, 924);
    const tc = new Card3D(tt.tex, { w: TURK_CARD.w, h: TURK_CARD.h, billboard: false, contact: 0 });
    tc.group.position.set(0, TURK_CARD.y, TURK_CARD.z);
    cabinet.group.add(tc.group);
    ctx.addCard({ tex: tt, card: tc, markup: (t) => svgMarkup(React.createElement(Turk, { props: { ...spec.turk(t), figureOnly: true, ink: 4.5 }, time: t, frame: 0, fps: 30, width: 900, height: 1000, sceneDuration: 60 }), TURK_VB, 640, 924) });
    let mc: Card3D | null = null;
    const mw = 0.46, mh = mw * (740 / 600);
    if (spec.master) {
      const mt = new SvgTex(320, 395);
      mc = new Card3D(mt.tex, { w: mw, h: mh, billboard: false, contact: 0, shadow: false });
      cabinet.masterAnchor.add(mc.group);
      ctx.addCard({ tex: mt, card: mc, markup: (t) => svgMarkup(React.createElement(Person, { props: { ...spec.master!(t), ink: 7 }, time: t, frame: 0, fps: 30, width: 600, height: 700, sceneDuration: 60 }), PERSON_VB, 320, 395) });
    }
    return (t, cam) => {
      const [x, y, z] = spec.at(t);
      cabinet.group.position.set(x, y, z); cabinet.group.rotation.y = spec.rotY ?? 0;
      cabinet.update({ ...spec.state(t), t }, mc ? { w: mw, h: mh } : null);
      if (spec.chess) cabinet.chess.update({ ...spec.chess(t), t }, cam);
      tc.char = spec.turkChar ? spec.turkChar(t) : 0;
      tc.burn = spec.turkBurn ? spec.turkBurn(t) : 0;
      if (mc) mc.char = spec.masterDark ? spec.masterDark(t) : 0;
    };
  };
}

/** cabinet + automaton world box (captions stay off it) */
export const cabinetAvoid = (c: V3, rot = 0): [number, number, number, number, number, number][] => {
  void rot;
  return [[c[0] - 0.66, 0, c[2] - 0.42, c[0] + 0.66, 1.9, c[2] + 0.42]];
};

export function toKit(g: TurkGroup): GroupSpec {
  const hold: { cabinet: Cabinet | null } = { cabinet: null };
  const rigs: Rig[] = [];
  if (g.cabinet) rigs.push(cabinetRig(g.cabinet, hold));
  if (g.extras) { const ex = g.extras; rigs.push((ctx) => ex({ ...ctx, cabinet: hold.cabinet })); }
  const { cabinet, extras, ...rest } = g;
  void extras;
  return { ...rest, rigs, avoid: cabinet ? (t) => cabinetAvoid(cabinet.at(t), cabinet.rotY) : undefined };
}
