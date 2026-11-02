// The test shot: the palace-hall corner with a ~3 s dolly (push-in + truck left) so parallax shows.
// Post chain (postprocessing, driven by hand from a priority-1 useFrame so R3F does not render on its own):
//   RenderPass (MSAA) -> InkPass (world ink, own pass) -> lens blur pre -> lens blur main
//   -> [Neutral tone mapping + mild grade] (one merged EffectPass).
// Ink runs before the DOF so the lines blur with what they belong to.
import React, { useEffect, useLayoutEffect, useMemo, useState } from "react";
import * as THREE from "three";
import { AbsoluteFill, continueRender, delayRender, useCurrentFrame, useVideoConfig } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useFrame, useThree } from "@react-three/fiber";
import { EffectComposer, EffectPass, RenderPass, ToneMappingEffect, ToneMappingMode } from "postprocessing";
import { InkPass } from "./ink";
import { LensBlur } from "./lensblur";
import { GradeEffect, GradeParams } from "./grade";
import { buildSet, HORIZON, Kit, loadKit } from "./set";

export type HallProps = { msaa: number; ink: boolean; lens: boolean; grade: boolean; cInf: number; inkDebug: number };
export const HALL_DEFAULTS: HallProps = { msaa: 4, ink: true, lens: true, grade: true, cInf: 10, inkDebug: 0 };

// mild grade: gentle S-curve, a hint of violet in the shadows, warm highlights, light vignette
const GRADE_MILD: GradeParams = {
  ky: [0, 0.092, 0.262, 0.55, 0.812, 0.94, 1],
  sat: [0.96, 1.0, 0.98],
  tintS: [0.014, 0.006], tintM: [0, 0], tintH: [-0.008, 0.004],
  vig: [0.14, 0.45],
};

const ss = (t: number) => { t = Math.min(1, Math.max(0, t)); return t * t * t * (t * (t * 6 - 15) + 10); }; // smootherstep
const lerp3 = (a: number[], b: number[], t: number) => new THREE.Vector3(...a.map((v, i) => v + (b[i] - v) * t));
const DOLLY_FRAMES = 90;
const CAM_A = [2.1, 1.7, 4.9], CAM_B = [1.25, 1.55, 3.55];   // push in ~1.6 m, truck left ~0.85 m
const LOOK_A = [-0.45, 1.25, -0.4], LOOK_B = [-0.25, 1.15, -0.1];

const useKit = () => {
  const [kit, setKit] = useState<Kit | null>(null);
  const [handle] = useState(() => delayRender("loading glTF kit", { timeoutInMilliseconds: 120000 }));
  useEffect(() => { loadKit().then((k) => { setKit(k); continueRender(handle); }); }, [handle]);
  return kit;
};

const fwd = new THREE.Vector3(), tmp = new THREE.Vector3();

const Inner: React.FC<{ kit: Kit; p: HallProps }> = ({ kit, p }) => {
  const frame = useCurrentFrame();
  const { gl, scene, camera } = useThree();
  const cam = camera as THREE.PerspectiveCamera;
  const world = useMemo(() => buildSet(kit), [kit]);

  const fx = useMemo(() => {
    const composer = new EffectComposer(gl, { multisampling: p.msaa, frameBufferType: THREE.HalfFloatType });
    composer.addPass(new RenderPass(scene, cam));
    const ink = new InkPass(scene, cam, { color: "#0b0a0c", fadeNear: 40, fadeFar: 120 });
    ink.debug = p.inkDebug;
    if (p.ink) composer.addPass(ink);
    const lens = new LensBlur({ maxCoC: 24, nearScale: 1.2 });
    if (p.lens) { composer.addPass(new EffectPass(cam, lens.pre)); composer.addPass(new EffectPass(cam, lens.main)); }
    const tone = new ToneMappingEffect({ mode: ToneMappingMode.NEUTRAL });
    const grade = new GradeEffect(GRADE_MILD, 1);
    composer.addPass(p.grade ? new EffectPass(cam, tone, grade) : new EffectPass(cam, tone));
    composer.setSize();
    return { composer, ink, lens };
  }, [gl, scene, cam, p]);
  useEffect(() => () => fx.composer.dispose(), [fx]);

  useLayoutEffect(() => {
    scene.fog = world.fog;
    scene.background = new THREE.Color(HORIZON);
  }, [scene, world]);

  // pose everything for this frame during render (before ThreeCanvas advances the frame)
  const t = ss(frame / (DOLLY_FRAMES - 1));
  cam.position.copy(lerp3(CAM_A, CAM_B, t));
  cam.lookAt(lerp3(LOOK_A, LOOK_B, t));
  cam.updateMatrixWorld();
  world.card.update(frame, cam);
  cam.getWorldDirection(fwd);
  fx.lens.focus = Math.max(0.3, tmp.copy(world.focus).sub(cam.position).dot(fwd));
  fx.lens.cInf = p.cInf;

  useFrame(() => { fx.composer.render(); }, 1);
  return <primitive object={world.root} dispose={null} />;
};

export const Hall: React.FC<Partial<HallProps>> = (props) => {
  const key = JSON.stringify(props);
  const p = useMemo(() => ({ ...HALL_DEFAULTS, ...props }), [key]); // eslint-disable-line react-hooks/exhaustive-deps
  const { width, height } = useVideoConfig();
  const kit = useKit();
  if (!kit) return null;
  return (
    <AbsoluteFill style={{ background: HORIZON }}>
      <ThreeCanvas width={width} height={height} dpr={1} shadows flat
        gl={{ antialias: false, stencil: false, depth: true, powerPreference: "high-performance" }}
        camera={{ fov: 50, near: 0.1, far: 60 }}>
        <Inner kit={kit} p={p} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
