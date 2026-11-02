// One continuous shot group of the story: a 3D set rendered with @remotion/three, the post chain proven by the cost
// test (MSAA render -> world ink pass -> lens blur -> neutral tone map + grade), the cabinet and the stick-kit cards.
// The camera, the light preset and every actor are functions of the GLOBAL story time (seconds), so consecutive
// groups in the same place can join seamlessly and the story file stays declarative.
import React, { useEffect, useLayoutEffect, useMemo } from "react";
import * as THREE from "three";
import { continueRender, delayRender, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useFrame, useThree } from "@react-three/fiber";
import { EffectComposer, EffectPass, RenderPass, ToneMappingEffect, ToneMappingMode } from "postprocessing";
import { InkPass } from "../ink";
import { LensBlur } from "../lensblur";
import { GradeEffect } from "../grade";
import { TONE } from "../shade";
import { Person } from "../../../../studio/src/kits/explainer/stick/person";
import { Turk } from "../../../../studio/src/kits/explainer/stick/turk";
import { SvgTex, svgMarkup } from "./svgtex";
import { Card3D, CARD_TONE } from "./card3d";
import { Cabinet, CabState, TURK_CARD, TOP } from "./cabinet";
import { CamKey, CamPath } from "./campath";
import { PRESETS, Preset } from "./presets";
import type { SetBuild } from "./sets";
import type { ChessState } from "./chess3d";

export type V3 = [number, number, number];
export type PersonSpec = {
  id: string; flip?: boolean; scale?: number;
  at: (t: number) => V3;
  props: (t: number) => Record<string, unknown>;
  visible?: (t: number) => boolean;
  char?: (t: number) => number;
};
export type CabinetSpec = {
  at: (t: number) => V3; rotY?: number; setup?: string;
  state: (t: number) => CabState;
  chess?: (t: number) => Omit<ChessState, "t">;
  turk: (t: number) => Record<string, unknown>;
  turkChar?: (t: number) => number; turkBurn?: (t: number) => number;
  master?: (t: number) => Record<string, unknown>;
  masterDark?: (t: number) => number;
};
export type Ctx = { root: THREE.Group; set: SetBuild; cabinet: Cabinet | null };
export type GroupSpec = {
  id: string; t0: number; t1: number; xfade: number;
  set: () => SetBuild;
  light: string | ((t: number) => string);
  cam: CamKey[];
  cabinet?: CabinetSpec;
  people: PersonSpec[];
  extras?: (ctx: Ctx) => (t: number, cam: THREE.PerspectiveCamera) => void;
};

const PERSON_VB = { w: 600, h: 700, padT: 40, padL: 0, padR: 0, padB: 0 };
const PERSON_K = 0.0025;                     // m per Person svg unit (a standing adult ~1.75 m)
const TURK_VB = { w: 900, h: 1000, padT: 300 };

type CardRec = { tex: SvgTex; card: Card3D; markup: (t: number) => string | null };

const Inner: React.FC<{ g: GroupSpec; tOf: (f: number) => number }> = ({ g, tOf }) => {
  const frame = useCurrentFrame();
  const { gl, scene, camera, advance } = useThree();
  const cam = camera as THREE.PerspectiveCamera;

  const world = useMemo(() => {
    const set = g.set();
    const root = new THREE.Group();
    root.add(set.root);
    let cabinet: Cabinet | null = null;
    const cards: CardRec[] = [];
    if (g.cabinet) {
      cabinet = new Cabinet(g.cabinet.setup ?? "mid");
      root.add(cabinet.group);
      const tt = new SvgTex(640, 924);
      const tc = new Card3D(tt.tex, { w: TURK_CARD.w, h: TURK_CARD.h, billboard: false, contact: 0 });
      tc.group.position.set(0, TURK_CARD.y, TURK_CARD.z);
      cabinet.group.add(tc.group);
      const spec = g.cabinet;
      cards.push({ tex: tt, card: tc, markup: (t) => svgMarkup(<Turk props={{ ...spec.turk(t), figureOnly: true, ink: 4.5 }} time={t} frame={0} fps={30} width={900} height={1000} sceneDuration={60} />, TURK_VB, 640, 924) });
      if (spec.master) {
        const mt = new SvgTex(320, 395);
        const mw = 0.46, mh = mw * (740 / 600);
        const mc = new Card3D(mt.tex, { w: mw, h: mh, billboard: false, contact: 0, shadow: false });
        cabinet.masterAnchor.add(mc.group);
        (mc as Card3D & { size?: { w: number; h: number } }).size = { w: mw, h: mh };
        cards.push({ tex: mt, card: mc, markup: (t) => svgMarkup(<Person props={{ ...spec.master!(t), ink: 7 }} time={t} frame={0} fps={30} width={600} height={700} sceneDuration={60} />, PERSON_VB, 320, 395) });
      }
    }
    for (const p of g.people) {
      const tx = new SvgTex(480, 592, !!p.flip);
      const sc = (p.scale ?? 1) * PERSON_K;
      const c = new Card3D(tx.tex, { w: 600 * sc, h: 740 * sc, contact: 0.9 * (p.scale ?? 1) });
      root.add(c.group);
      cards.push({ tex: tx, card: c, markup: (t) => (p.visible && !p.visible(t) ? null : svgMarkup(<Person props={{ ...p.props(t), ink: 6 }} time={t} frame={0} fps={30} width={600} height={700} sceneDuration={60} />, PERSON_VB, 480, 592)) });
    }
    const ctx: Ctx = { root, set, cabinet };
    const extra = g.extras ? g.extras(ctx) : null;
    return { root, set, cabinet, cards, extra, path: new CamPath(g.cam, g.t0, g.t1) };
  }, [g]);

  const fx = useMemo(() => {
    const composer = new EffectComposer(gl, { multisampling: 4, frameBufferType: THREE.HalfFloatType });
    composer.addPass(new RenderPass(scene, cam));
    const ink = new InkPass(scene, cam, { color: "#0b0a0c", fadeNear: 40, fadeFar: 120 });
    composer.addPass(ink);
    const lens = new LensBlur({ maxCoC: 24, nearScale: 1.2 });
    composer.addPass(new EffectPass(cam, lens.pre));
    composer.addPass(new EffectPass(cam, lens.main));
    const grade = new GradeEffect(PRESETS.day.grade, 1);
    composer.addPass(new EffectPass(cam, new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL }), grade));
    composer.setSize();
    return { composer, lens, grade };
  }, [gl, scene, cam]);
  useEffect(() => () => fx.composer.dispose(), [fx]);

  useLayoutEffect(() => { scene.add(world.root); return () => { scene.remove(world.root); }; }, [scene, world]);

  const t = tOf(frame);
  // ---- pose everything for this frame (during render, before ThreeCanvas advances)
  const presetName = typeof g.light === "function" ? g.light(t) : g.light;
  const P: Preset = PRESETS[presetName];
  const c = world.path.at(t);
  cam.position.copy(c.pos); cam.lookAt(c.look); cam.fov = c.fov; cam.near = 0.05; cam.far = 200; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  if (world.cabinet && g.cabinet) {
    const [x, y, z] = g.cabinet.at(t);
    world.cabinet.group.position.set(x, y, z); world.cabinet.group.rotation.y = g.cabinet.rotY ?? 0;
    const st = g.cabinet.state(t);
    const mrec = world.cards[1] && g.cabinet.master ? (world.cards[1].card as Card3D & { size?: { w: number; h: number } }) : null;
    world.cabinet.update({ ...st, t }, mrec?.size ?? null);
    if (g.cabinet.chess) world.cabinet.chess.update({ ...g.cabinet.chess(t), t }, cam);
    world.cards[0].card.char = g.cabinet.turkChar ? g.cabinet.turkChar(t) : 0;
    world.cards[0].card.burn = g.cabinet.turkBurn ? g.cabinet.turkBurn(t) : 0;
    if (mrec) mrec.char = g.cabinet.masterDark ? g.cabinet.masterDark(t) : 0;
  }
  const off = world.cabinet && g.cabinet ? (g.cabinet.master ? 2 : 1) : 0;
  g.people.forEach((p, i) => {
    const rec = world.cards[off + i];
    const vis = p.visible ? p.visible(t) : true;
    rec.card.visible = vis;
    const [x, y, z] = p.at(t);
    rec.card.place(x, y, z, cam);
    rec.card.char = p.char ? p.char(t) : 0;
  });
  if (world.extra) world.extra(t, cam);
  // light preset
  TONE.uLitCol.value.set(...P.lit); TONE.uShadeCol.value.set(...P.shade); TONE.uSat.value = P.sat;
  CARD_TONE.uLitTint.value.set(...P.cardLit); CARD_TONE.uShadeTint.value.set(...P.cardShade);
  world.set.key.color.set(P.key); world.set.key.intensity = P.keyI;
  scene.fog = new THREE.Fog(P.fog, P.fogNear, P.fogFar);
  scene.background = new THREE.Color(P.bg);
  for (const o of world.set.glows) o.visible = P.glow > 0.05, o.scale.setScalar((o.userData.base ??= o.scale.x) * (0.6 + 0.4 * P.glow));
  fx.grade.set(P.grade);
  const fwd = new THREE.Vector3(); cam.getWorldDirection(fwd);
  fx.lens.focus = Math.max(0.3, c.look.clone().sub(cam.position).dot(fwd));
  fx.lens.cInf = 10;

  useFrame(() => { fx.composer.render(); }, 1);

  // ---- redraw the cards whose svg changed, then render again and release the frame
  useEffect(() => {
    const h = delayRender(`cards ${g.id} ${frame}`, { timeoutInMilliseconds: 60000 });
    const jobs = world.cards.map((r) => { const m = r.card.group.visible ? r.markup(t) : null; return m ? r.tex.draw(m) : Promise.resolve(false); });
    Promise.all(jobs).then(() => { advance(performance.now()); continueRender(h); })
      .catch((e) => { console.error(e); continueRender(h); });
  }, [frame]); // eslint-disable-line react-hooks/exhaustive-deps

  return null;
};

export const Stage: React.FC<{ g: GroupSpec; fromFrame: number }> = ({ g, fromFrame }) => {
  const { width, height, fps } = useVideoConfig();
  const tOf = (f: number) => (fromFrame + f) / fps;
  return (
    <ThreeCanvas width={width} height={height} dpr={1} shadows flat
      gl={{ antialias: false, stencil: false, depth: true, powerPreference: "high-performance" }}
      camera={{ fov: 40, near: 0.05, far: 200 }}>
      <Inner g={g} tOf={tOf} />
    </ThreeCanvas>
  );
};
void TOP;
