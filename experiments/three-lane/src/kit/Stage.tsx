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
import { BlendFunction, SelectiveBloomEffect, EffectComposer, EffectPass, NormalPass, RenderPass, SSAOEffect, ToneMappingEffect, ToneMappingMode } from "postprocessing";
import { InkPass } from "../ink";
import { LensBlur } from "../lensblur";
import { GradeEffect } from "../grade";
import { TONE } from "../shade";
import { Person } from "../../../../studio/src/kits/explainer/stick/person";
import { SvgTex, svgMarkup } from "./svgtex";
import { Card3D, CARD_TONE } from "./card3d";
import { CamKey, CamPath } from "./campath";
import { PRESETS, Preset } from "./presets";
import { actorCard } from "./actorCard";
import { skyLife, waterLife, minLabel, type Life } from "./ambient";
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
  /** draw with the old stick/Person (idle breathing, regular blinks) instead of the Actor (the default since the
   * src/next integration: whole-face swaps, still body, rare short blinks, marks, prop follow-through) */
  classic?: boolean;
};
/** an SVG card a rig draws every frame (markup null = keep the last drawing) */
export type CardRec = { tex: SvgTex; card: Card3D; markup: (t: number) => string | null };
export type Ctx = { root: THREE.Group; set: SetBuild; addCard: (c: CardRec) => void };
export type Rig = (ctx: Ctx) => (t: number, cam: THREE.PerspectiveCamera) => void;
export type GroupSpec = {
  id: string; t0: number; t1: number; xfade: number;
  set: () => SetBuild;
  /** a preset name or object, or a function of time returning either (kit/lightarc.ts blends presets) */
  light: string | Preset | ((t: number) => string | Preset);
  cam: CamKey[];
  people: PersonSpec[];
  rigs?: Rig[];
  /** world boxes the captions must stay off at time t (the subject of the shot) */
  avoid?: (t: number) => [number, number, number, number, number, number][];
  // busy bands captions must stay off (rigging, rows of ports): weighted above avoid in caption placement and checked by
  // the caption gate in scripts/framing.ts (story-vasa v15)
  busy?: (t: number, cam: [number, number, number]) => [number, number, number, number, number, number][];
  /** lens blur strength: cInf = blur radius (px at 1080x1920) at infinity; default LENS.cInf (macro shots ~22) */
  lens?: { cInf?: number; maxCoC?: number };
  /** lighting (round 2): ambient occlusion strength (default 0 = off; contact shadows come from soft shadow maps and blobs) and bloom on light sources (default 0.55) */
  ao?: number; bloom?: number;
  /** kit life: drifting clouds round a sky dome and wave detail over extra.water (default on) */
  clouds?: boolean; waves?: boolean;
  /** how the group is entered (Episode3D joins; default from xfade: whip, or cut when 0) */
  join?: import("./Episode3D").Join;
  /** gates: place name (same string for revisits), an insert (cutaway), an establishing wide (allowed small figures) */
  place?: string; insert?: boolean; establishing?: boolean;
  /** world boxes that must stay whole in frame (a banner, a mast top); figures are checked anyway */
  keepInFrame?: (t: number) => [number, number, number, number, number, number][];
  /** the key light for this group: "auto" = a warm side key 75 degrees round from the camera, 34 degrees up, aimed at the
   * group's first framing (so subjects are lit and cast shadows toward the background); or explicit from/at */
  sun?: "auto" | { from: V3; at?: V3; span?: number };
  /** windows where the group's rigs visibly animate (fire, smoke, a falling weight): the still gate counts them */
  alive?: [number, number][];
};

/** kit-wide lens default (src/next integration): cInf 10 left KitLab's soft-edge share at 2.6 % (refs 4-15 % at 720p) */
export const LENS = { cInf: 12, maxCoC: 24 };
/** a light value -> a preset */
export const presetOf = (v: string | Preset): Preset => (typeof v === "string" ? PRESETS[v] : v);

export const PERSON_VB = { w: 600, h: 700, padT: 40, padL: 0, padR: 0, padB: 0 };
export const PERSON_K = 0.0025;                     // m per Person svg unit (a standing adult ~1.75 m)

/** a stick-kit person as a card: 600 x 740 svg units, feet on the bottom edge */
export function personCard(props: (t: number) => Record<string, unknown> | null, o: { flip?: boolean; scale?: number; contact?: number; billboard?: boolean; px?: [number, number] } = {}): CardRec {
  const [pw, ph] = o.px ?? [480, 592];
  const tex = new SvgTex(pw, ph, !!o.flip);
  const sc = (o.scale ?? 1) * PERSON_K;
  const card = new Card3D(tex.tex, { w: 600 * sc, h: 740 * sc, contact: o.contact ?? 0.9 * (o.scale ?? 1), billboard: o.billboard });
  return { tex, card, markup: (t) => { const p = props(t); return p ? svgMarkup(<Person props={{ ink: 6, ...p }} time={t} frame={0} fps={30} width={600} height={700} sceneDuration={60} />, PERSON_VB, tex.pxW, tex.pxH) : null; } };
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
      const rec = (p.classic ? personCard : actorCard)((t) => (p.visible && !p.visible(t) ? null : p.props(t)), { flip: p.flip, scale: p.scale, billboard: p.billboard,
        contact: p.billboard === false ? 0 : undefined });
      root.add(rec.card.group); cards.push(rec); return rec;
    });
    const ctx: Ctx = { root, set, addCard: (c) => cards.push(c) };
    const rigs = (g.rigs ?? []).map((r) => r(ctx));
    const life = [g.clouds === false ? null : skyLife(set.root), g.waves === false ? null : waterLife(set.extra.water)].filter(Boolean) as Life[];
    const path = new CamPath(g.cam, g.t0, g.t1);
    if (g.sun) {
      const c0 = path.at(g.t0), look = c0.look.clone();
      let from: THREE.Vector3, span: number;
      if (g.sun === "auto") {
        const toCam = c0.pos.clone().sub(look); toCam.y = 0; toCam.normalize();
        from = toCam.applyAxisAngle(new THREE.Vector3(0, 1, 0), (75 * Math.PI) / 180).multiplyScalar(Math.cos(0.6)).add(new THREE.Vector3(0, Math.sin(0.6), 0)).normalize();
        span = Math.max(10, c0.pos.distanceTo(look) * 1.4);
      } else { from = new THREE.Vector3(...g.sun.from).normalize(); if (g.sun.at) look.set(...g.sun.at); span = g.sun.span ?? 30; }
      set.key.position.copy(look).addScaledVector(from, span * 2.5); set.key.target.position.copy(look); set.key.target.updateMatrixWorld();
      Object.assign(set.key.shadow.camera, { left: -span, right: span, top: span, bottom: -span, near: 0.5, far: span * 6 });
      set.key.shadow.camera.updateProjectionMatrix();
    }
    return { root, set, cards, people, rigs, life, path };
  }, [g]);

  const { width: vw, height: vh } = useVideoConfig();
  const fx = useMemo(() => {
    const composer = new EffectComposer(gl, { multisampling: 4, frameBufferType: THREE.HalfFloatType });
    composer.addPass(new RenderPass(scene, cam));
    // ambient occlusion (round-2 craft: "no contact shadows"): violet, multiplied, before the ink so the lines stay crisp
    // the normals come from a world-only camera: the character cards (NOINK) would enter the normal pass as whole
    // quads (no alpha cut-out there) and leave a rectangular AO halo round every figure
    const aoCam = cam.clone(); aoCam.layers.set(0);
    const normal = new NormalPass(scene, aoCam);
    const ao = new SSAOEffect(cam, normal.texture, {
      // half resolution, upsampled depth-aware: smooth (full-res AO left a grain on the white heads)
      blendFunction: BlendFunction.MULTIPLY, samples: 16, rings: 7, distanceScaling: true, depthAwareUpsampling: true, resolutionScale: 0.5,
      worldDistanceThreshold: 60, worldDistanceFalloff: 10, worldProximityThreshold: 0.6, worldProximityFalloff: 0.3,
      luminanceInfluence: 0.3, minRadiusScale: 0.25, radius: 0.1, intensity: 2.6 * (g.ao ?? 0), bias: 0.025, fade: 0.012, color: new THREE.Color("#3a2a5a"),
    });
    if ((g.ao ?? 0) > 0) { composer.addPass(normal); composer.addPass(new EffectPass(cam, ao)); }   // off by default: on the character cards it mixed the cards' depth with the world's normals and left grain on the white heads (round-2 face judge)
    composer.addPass(new InkPass(scene, cam, { color: "#0b0a0c", fadeNear: 140, fadeFar: 420, distFar: 160, widthNear: 5.8, widthFar: 3.9 }));
    const lens = new LensBlur({ maxCoC: g.lens?.maxCoC ?? LENS.maxCoC, nearScale: 1.2 });
    composer.addPass(new EffectPass(cam, lens.pre));
    composer.addPass(new EffectPass(cam, lens.main));
    const grade = new GradeEffect(PRESETS.day.grade, 1);
    // bloom on light sources only (glows, lamps, fire, sunlit highlights above the threshold), then the tone map
    // round 10: selective (the set's glows and anything tagged userData.bloom): the white heads are pushed far above
    // 1.0 before the tone map (card3d.ts) and a threshold bloom made them glow
    const bloom = new SelectiveBloomEffect(scene, cam, { luminanceThreshold: 0.3, luminanceSmoothing: 0.25, intensity: g.bloom ?? 0.55, mipmapBlur: true, radius: 0.7 });
    bloom.ignoreBackground = true;
    composer.addPass(new EffectPass(cam, bloom, new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL }), grade));
    composer.setSize(vw, vh);       // explicit: a first frame rendered before the canvas settled came out tiled (v1 review)
    return { composer, lens, grade, aoCam, bloom };
  }, [gl, scene, cam, vw, vh, g]);
  const mounted = React.useRef(false);
  useEffect(() => () => fx.composer.dispose(), [fx]);

  useLayoutEffect(() => { scene.add(world.root); return () => { scene.remove(world.root); }; }, [scene, world]);
  useLayoutEffect(() => {
    const sel: THREE.Object3D[] = [...world.set.glows];
    world.root.traverse((o) => { if (o.userData.bloom) sel.push(o); });
    fx.bloom.selection.set(sel);
  }, [fx, world]);

  const t = tOf(frame);
  // ---- pose everything for this frame (during render, before ThreeCanvas advances)
  const P: Preset = presetOf(typeof g.light === "function" ? g.light(t) : g.light);
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
  fx.aoCam.copy(cam); fx.aoCam.layers.set(0);
  minLabel(world.root, cam);
  TONE.uLitCol.value.set(...P.lit); TONE.uShadeCol.value.set(...P.shade); TONE.uSat.value = P.sat;
  // rim light: the key's colour, weaker at night; the hemisphere fill keeps cool above and warm below
  const kc = new THREE.Color(P.key); TONE.uRim.value.set(kc.r, kc.g, kc.b).multiplyScalar(0.28 * Math.min(1, P.keyI / 2));
  CARD_TONE.uLitTint.value.set(...P.cardLit); CARD_TONE.uShadeTint.value.set(...P.cardShade);
  world.set.key.color.set(P.key); world.set.key.intensity = P.keyI;
  const fs = world.set.fogScale ?? 1;
  scene.fog = new THREE.Fog(P.fog, P.fogNear * fs, P.fogFar * fs);
  scene.background = new THREE.Color(P.bg);
  for (const l of world.life) l(t, scene.background as THREE.Color, cam);
  for (const o of world.set.glows) o.visible = P.glow > 0.05, o.scale.setScalar((o.userData.base ??= o.scale.x) * (0.6 + 0.4 * P.glow));
  fx.grade.set(P.grade);
  const fwd = new THREE.Vector3(); cam.getWorldDirection(fwd);
  fx.lens.focus = Math.max(0.3, c.look.clone().sub(cam.position).dot(fwd));
  fx.lens.cInf = g.lens?.cInf ?? LENS.cInf;

  useFrame(() => { fx.composer.render(); }, 1);

  // ---- redraw the cards whose svg changed, then render again and release the frame
  useEffect(() => {
    const h = delayRender(`cards ${g.id} ${frame}`, { timeoutInMilliseconds: 60000 });
    // each card's raster follows its size on screen (close-ups get up to 4x, see SvgTex.fit)
    const fwd = new THREE.Vector3(), wp = new THREE.Vector3(), ws = new THREE.Vector3(); cam.getWorldDirection(fwd);
    const tanH = Math.tan((cam.fov * Math.PI) / 360);
    for (const r of world.cards) {
      if (!r.card.group.visible) continue;
      r.card.plane.getWorldPosition(wp); r.card.plane.getWorldScale(ws);
      const d = Math.max(0.05, wp.sub(cam.position).dot(fwd));
      r.tex.fit((r.card.o.h * Math.abs(ws.y)) / (2 * d * tanH) * vh);
    }
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
