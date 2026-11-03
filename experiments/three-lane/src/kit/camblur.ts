// Camera motion blur (our own code; visual track round 3, smoothness: "motion blur that matches how fast the camera is
// actually moving"). A post effect that smears each pixel along the camera's own screen motion for this frame:
// v(uv) = T + Z * (uv - 0.5), T the translation and Z the zoom of the view between this frame and the next (Stage
// measures them from the camera path at the focus depth), times a 180-degree shutter. Under 1 px of smear it is off.
import { Effect, EffectAttribute, BlendFunction } from "postprocessing";
import { Uniform, Vector2 } from "three";
import * as THREE from "three";

const frag = /* glsl */ `
uniform vec2 uT;      // translation, uv per frame (y up)
uniform float uZ;     // zoom per frame (scale - 1)
uniform float uShutter;
void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
  vec2 v = (uT + uZ * (uv - 0.5)) * uShutter;
  if (length(v * resolution) < 1.0) { outputColor = inputColor; return; }
  vec4 acc = vec4(0.0);
  for (int i = 0; i < 12; i++) { float k = float(i) / 11.0 - 0.5; acc += texture2D(inputBuffer, uv - v * k); }
  outputColor = acc / 12.0;
}`;

export class CamBlurEffect extends Effect {
  constructor(shutter = 0.5) {
    super("CamBlurEffect", frag, { blendFunction: BlendFunction.NORMAL, attributes: EffectAttribute.CONVOLUTION, uniforms: new Map<string, Uniform>([["uT", new Uniform(new Vector2())], ["uZ", new Uniform(0)], ["uShutter", new Uniform(shutter)]]) });
  }
  /** set from two camera poses (this frame, next frame) and the focus distance */
  setFrom(a: THREE.PerspectiveCamera, b: THREE.PerspectiveCamera, focus: number) {
    const fwd = new THREE.Vector3(); a.getWorldDirection(fwd);
    const right = new THREE.Vector3().setFromMatrixColumn(a.matrixWorld, 0);
    const c = a.position.clone().addScaledVector(fwd, focus), r = c.clone().addScaledVector(right, focus * 0.3);
    const pa = c.clone().project(a), pb = c.clone().project(b), ra = r.clone().project(a), rb = r.clone().project(b);
    const T = new Vector2(pb.x - pa.x, pb.y - pa.y).multiplyScalar(0.5);                 // NDC -> uv
    const z = Math.abs(ra.x - pa.x) > 1e-6 ? (rb.x - pb.x) / (ra.x - pa.x) - 1 : 0;
    const ok = isFinite(T.x) && isFinite(T.y) && pa.z < 1 && pb.z < 1;
    (this.uniforms.get("uT")!.value as Vector2).copy(ok ? T.clampLength(0, 0.2) : new Vector2());
    this.uniforms.get("uZ")!.value = ok ? Math.max(-0.2, Math.min(0.2, z)) : 0;
  }
}
