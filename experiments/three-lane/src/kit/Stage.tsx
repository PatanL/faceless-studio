// The 3D story lane's stage (our own code): one continuous shot group rendered with @remotion/three and the post chain
// proven by the cost test (MSAA render -> world ink pass -> lens blur -> neutral tone map + grade). A group is a set,
// a light preset, a camera path and actors, all functions of the GLOBAL story time (seconds), so consecutive groups in
// the same place can join seamlessly and an episode's story file stays declarative.
// Actors: stick-kit people (drawn per frame into lit, shadow-casting cards) plus "rigs" - anything else an episode
// builds into the world (a cabinet, a ship, fire). A rig may add its own SVG cards with ctx.addCard.
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
import { SvgTex, svgMarkup } from "./svgtex";
import { Card3D, CARD_TONE } from "./card3d";
import { CamKey, CamPath } from "./campath";
import { PRESETS, Preset } from "./presets";
import type { SetBuild } from "./sets";

export type V3 = [number, number, number];
export type PersonSpec = {
  id: string; flip?: boolean; scale?: number;
  /** false: a flat card facing +z turned by yaw (a portrait, a sign), no contact shadow */
  billboard?: boolean; yaw?: number;
  /** turn the drawing to face this point on screen (the card mirrors when the camera sees the scene from behind) */
  faceTo?: (t: number) => V3;
  at: (t: number) => V3;
  props: (t: number) => Record<string, unknown>;
  visible?: (t: number) => boolean;
  char?: (t: number) => number;
};
/** an SVG card a rig draws every frame (markup null = keep the last drawing) */
export type CardRec = { tex: SvgTex; card: Card3D; markup: (t: number) => string | null };
export type Ctx = { root: THREE.Group; set: SetBuild; addCard: (c: CardRec) => void };
export type Rig = (ctx: Ctx) => (t: number, cam: THREE.PerspectiveCamera) => void;
export type GroupSpec = {
  id: string; t0: number; t1: number; xfade: number;
  set: () => SetBuild;
  light: string | ((t: number) => string);
  cam: CamKey[];
  people: PersonSpec[];
  rigs?: Rig[];
  /** world boxes the captions must stay off at time t (the subject of the shot) */
  avoid?: (t: number) => [number, number, number, number, number, number][];
};

export const PERSON_VB = { w: 600, h: 700, padT: 40, padL: 0, padR: 0, padB: 0 };
export const PERSON_K = 0.0025;                     // m per Person svg unit (a standing adult ~1.75 m)

/** a stick-kit person as a card: 600 x 740 svg units, feet on the bottom edge */
export function personCard(props: (t: number) => Record<string, unknown> | null, o: { flip?: boolean; scale?: number; contact?: number; billboard?: boolean; px?: [number, number] } = {}): CardRec {
  const [pw, ph] = o.px ?? [480, 592];
  const tex = new SvgTex(pw, ph, !!o.flip);
  const sc = (o.scale ?? 1) * PERSON_K;
  const card = new Card3D(tex.tex, { w: 600 * sc, h: 740 * sc, contact: o.contact ?? 0.9 * (o.scale ?? 1), billboard: o.billboard });
  return { tex, card, markup: (t) => { const p = props(t); return p ? svgMarkup(<Person props={{ ink: 6, ...p }} time={t} frame={0} fps={30} width={600} height={700} sceneDuration={60} />, PERSON_VB, pw, ph) : null; } };
}

const Inner: React.FC<{ g: GroupSpec; tOf: (f: number) => number }> = ({ g, tOf }) => {
  const frame = useCurrentFrame();
  const { gl, scene, camera, advance } = useThree();
  const cam = camera as THREE.PerspectiveCamera;

  const world = useMemo(() => {
    const set = g.set();
    const root = new THREE.Group();
    root.add(set.root);
    const cards: CardRec[] = [];
    const people = g.people.map((p) => {
      const rec = personCard((t) => (p.visible && !p.visible(t) ? null : p.props(t)), { flip: p.flip, scale: p.scale, billboard: p.billboard,
        contact: p.billboard === false ? 0 : undefined });
      root.add(rec.card.group); cards.push(rec); return rec;
    });
    const ctx: Ctx = { root, set, addCard: (c) => cards.push(c) };
    const rigs = (g.rigs ?? []).map((r) => r(ctx));
    return { root, set, cards, people, rigs, path: new CamPath(g.cam, g.t0, g.t1) };
  }, [g]);

  const { width: vw, height: vh } = useVideoConfig();
  const fx = useMemo(() => {
    const composer = new EffectComposer(gl, { multisampling: 4, frameBufferType: THREE.HalfFloatType });
    composer.addPass(new RenderPass(scene, cam));
    composer.addPass(new InkPass(scene, cam, { color: "#0b0a0c", fadeNear: 140, fadeFar: 420, distFar: 160, widthNear: 5.8, widthFar: 3.9 }));
    const lens = new LensBlur({ maxCoC: 24, nearScale: 1.2 });
    composer.addPass(new EffectPass(cam, lens.pre));
    composer.addPass(new EffectPass(cam, lens.main));
    const grade = new GradeEffect(PRESETS.day.grade, 1);
    composer.addPass(new EffectPass(cam, new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL }), grade));
    composer.setSize(vw, vh);       // explicit: a first frame rendered before the canvas settled came out tiled (v1 review)
    return { composer, lens, grade };
  }, [gl, scene, cam, vw, vh]);
  const mounted = React.useRef(false);
  useEffect(() => () => fx.composer.dispose(), [fx]);

  useLayoutEffect(() => { scene.add(world.root); return () => { scene.remove(world.root); }; }, [scene, world]);

  const t = tOf(frame);
  // ---- pose everything for this frame (during render, before ThreeCanvas advances)
  const P: Preset = PRESETS[typeof g.light === "function" ? g.light(t) : g.light];
  const c = world.path.at(t);
  cam.position.copy(c.pos); cam.lookAt(c.look); cam.fov = c.fov; cam.near = 0.05; cam.far = 400; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  g.people.forEach((p, i) => {
    const rec = world.people[i];
    rec.card.visible = p.visible ? p.visible(t) : true;
    const [x, y, z] = p.at(t);
    rec.card.place(x, y, z, cam, p.yaw ?? 0);
    if (p.faceTo) {
      // the drawing faces right; mirror it when the target is to the figure's left on screen
      const [tx, , tz] = p.faceTo(t);
      const right = new THREE.Vector3().setFromMatrixColumn(cam.matrixWorld, 0);
      const side = (tx - x) * right.x + (tz - z) * right.z;
      const base = p.flip ? -1 : 1;                         // the texture is already mirrored when flip is set
      rec.card.group.scale.x = (side >= 0 ? 1 : -1) * base;
    }
    rec.card.char = p.char ? p.char(t) : 0;
  });
  for (const r of world.rigs) r(t, cam);
  TONE.uLitCol.value.set(...P.lit); TONE.uShadeCol.value.set(...P.shade); TONE.uSat.value = P.sat;
  CARD_TONE.uLitTint.value.set(...P.cardLit); CARD_TONE.uShadeTint.value.set(...P.cardShade);
  world.set.key.color.set(P.key); world.set.key.intensity = P.keyI;
  const fs = world.set.fogScale ?? 1;
  scene.fog = new THREE.Fog(P.fog, P.fogNear * fs, P.fogFar * fs);
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
    // the first frame after a mount renders twice (targets, shadow maps and card textures settle on the first pass)
    // release the frame two animation frames after the last draw: on the Mac GPU path a screenshot taken straight after
    // the WebGL draw sometimes came back as a tiled mosaic (story-vasa v2/v3)
    Promise.all(jobs).then(() => { if (!mounted.current) { advance(performance.now()); mounted.current = true; } advance(performance.now());
      requestAnimationFrame(() => requestAnimationFrame(() => continueRender(h))); })
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
      camera={{ fov: 40, near: 0.05, far: 400 }}>
      <Inner g={g} tOf={tOf} />
    </ThreeCanvas>
  );
};
