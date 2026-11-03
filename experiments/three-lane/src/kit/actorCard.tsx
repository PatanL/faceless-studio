// The Actor on a lit 3D card (our own code). Same card as the kit's personCard (Stage.tsx) - a rasterised SVG on a
// camera-facing plane, NOINK layer, tinted by the scene light, casting a cut-out shadow - but drawing next/Actor and
// with 120 units of headroom above the head so a popped hat never leaves the texture.
// Two ways in:
//   actorCard(props, opts)  -> CardRec, the drop-in replacement for personCard (see INTEGRATION.md: one line in Stage)
//   actorRig(spec)          -> a Rig, usable TODAY in any GroupSpec.rigs without touching the kit
import * as THREE from "three";
import { SvgTex, svgMarkup } from "./svgtex";
import { Card3D } from "./card3d";
import { PERSON_K, type CardRec, type PersonSpec, type Rig } from "./Stage";
import { Actor, headPose } from "./actor";

export const ACTOR_VB = { w: 600, h: 700, padT: 120, padL: 0, padR: 0, padB: 0 };
const VB_H = 700 + 120;

export function actorCard(props: (t: number) => Record<string, unknown> | null, o: { flip?: boolean; scale?: number; contact?: number; billboard?: boolean; px?: [number, number] } = {}): CardRec {
  const [pw, ph] = o.px ?? [480, Math.round((480 * VB_H) / 600)];
  const tex = new SvgTex(pw, ph, !!o.flip);
  const sc = (o.scale ?? 1) * PERSON_K;
  const card = new Card3D(tex.tex, { w: 600 * sc, h: VB_H * sc, contact: o.contact ?? 0.9 * (o.scale ?? 1), billboard: o.billboard });
  return {
    tex, card,
    markup: (t) => {
      const p = props(t);
      if (!p) return null;
      // the head circle in texture uv (flipY: v = 1 at the top of the svg), for the sphere shading in card3d.ts
      const hp = headPose(p, t);
      card.head(hp.x / 600, 1 - (hp.y + 120) / VB_H, hp.r / 600, hp.r / VB_H);
      return svgMarkup(<Actor props={{ ink: 6, ...p }} time={t} />, ACTOR_VB, pw, ph);
    },
  };
}

/** an Actor placed exactly as Stage places its people (visible, at, faceTo mirroring, char) */
export function actorRig(p: PersonSpec): Rig & { spec: PersonSpec } {
  const rig: Rig = (ctx) => {
    const rec = actorCard((t) => (p.visible && !p.visible(t) ? null : p.props(t)), { flip: p.flip, scale: p.scale, billboard: p.billboard, contact: p.billboard === false ? 0 : undefined });
    ctx.root.add(rec.card.group); ctx.addCard(rec);
    const right = new THREE.Vector3();
    return (t, cam) => {
      rec.card.visible = p.visible ? p.visible(t) : true;
      const [x, y, z] = p.at(t);
      rec.card.place(x, y, z, cam, p.yaw ?? 0);
      if (p.faceTo) {
        const [tx, , tz] = p.faceTo(t);
        right.setFromMatrixColumn(cam.matrixWorld, 0);
        const side = (tx - x) * right.x + (tz - z) * right.z;
        rec.card.group.scale.x = (side >= 0 ? 1 : -1) * (p.flip ? -1 : 1);
      }
      rec.card.char = p.char ? p.char(t) : 0;
    };
  };
  return Object.assign(rig, { spec: p });
}

/** move actor rigs into each group's people (Stage draws people as Actors), so captions, gates and the framing
 * replay see them */
export function actorsToPeople<G extends { people: PersonSpec[]; rigs?: Rig[] }>(groups: G[]): G[] {
  for (const g of groups) {
    const rigs = g.rigs ?? [];
    const specs = rigs.filter((r) => (r as Rig & { spec?: PersonSpec }).spec).map((r) => (r as Rig & { spec: PersonSpec }).spec);
    g.people = [...g.people, ...specs];
    g.rigs = rigs.filter((r) => !(r as Rig & { spec?: PersonSpec }).spec);
  }
  return groups;
}
