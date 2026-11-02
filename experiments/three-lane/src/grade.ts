// three-lane experiment: display-referred colour grade (tone curve, zone saturation, split tint, vignette).
// The bridge's fitted presets are dropped; our mild preset lives in Hall.tsx.
// Ported from mromidev/claude-animated-shorts, templates/bridge/grade.ts (commit e3b817b), MIT licence:
//
// Copyright (c) 2026 Mr omi
//
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
// documentation files (the "Software"), to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
// to permit persons to whom the Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of
// the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
// THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
// CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
// IN THE SOFTWARE.
//
// Colour grade for the bridge short (post agent): references/grade/GradeEffect.ts (reports/grade.md) verbatim,
// plus GRADES / GRADE_STRENGTH / gradeFor() so the lead can re-fit the presets after the lighting merge.
// The presets were fitted to the OLD unlit stills: after the WORLD lighting lands they will over-correct; re-fit
// (grade.md 5.C) or lower GRADE_STRENGTH. Each Inner (crossfade layer) grades with its own shot's light, so the DOM
// crossfade at XFADE frames (shots 10->11, 13->14) cross-fades the presets as well.
// GradeEffect: the fitted reference-style colour grade as a postprocessing 6.37 Effect.
// Put it LAST in the EffectComposer, after ToneMappingEffect. It works on display-referred values: the input (linear,
// already tone-mapped to 0..1) is encoded to sRGB, graded exactly like scripts/grade.py (validated on our stills), and
// decoded back to linear for the composer's output encoding.
//   1. RGB tone curve: monotone cubic Hermite through 7 knots at x = 0, .1, .25, .5, .75, .9, 1
//   2. saturation around luma Y' (Rec.709 weights on the encoded values), separately for shadows / mids / highlights
//   3. 3-way tint (split tone): zero-luma RGB offsets in shadows, mids, highlights
//   4. vignette: x (1 - k * smoothstep(r0, 1, r)), r = elliptical radius, corners = 1
// `amount` blends the whole grade (0 = bypass) so it can be dialled back once lighting/albedo work brightens the render.
import { Effect, BlendFunction } from "postprocessing";
import { Uniform, Vector3, Vector2 } from "three";

const frag = /* glsl */ `
uniform float gradeKy[7];
uniform float gradeKm[7];
uniform vec3 gradeSat;      // x = shadows, y = mids, z = highlights
uniform vec3 gradeTintS;    // zero-luma RGB offsets (sRGB-encoded units)
uniform vec3 gradeTintM;
uniform vec3 gradeTintH;
uniform vec2 gradeVig;      // x = strength k, y = start radius r0
uniform float gradeAmount;

vec3 gradeEncode(vec3 c) {   // linear -> sRGB
  c = clamp(c, 0.0, 1.0);
  return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c));
}
vec3 gradeDecode(vec3 c) {   // sRGB -> linear
  return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c));
}
float gradeHermite(float v, float x0, float x1, float y0, float y1, float m0, float m1) {
  float h = x1 - x0, t = (v - x0) / h, t2 = t * t, t3 = t2 * t;
  return (2.0 * t3 - 3.0 * t2 + 1.0) * y0 + (t3 - 2.0 * t2 + t) * h * m0 + (-2.0 * t3 + 3.0 * t2) * y1 + (t3 - t2) * h * m1;
}
float gradeCurve(float v) {
  v = clamp(v, 0.0, 1.0);
  if (v < 0.1)  return gradeHermite(v, 0.0, 0.1, gradeKy[0], gradeKy[1], gradeKm[0], gradeKm[1]);
  if (v < 0.25) return gradeHermite(v, 0.1, 0.25, gradeKy[1], gradeKy[2], gradeKm[1], gradeKm[2]);
  if (v < 0.5)  return gradeHermite(v, 0.25, 0.5, gradeKy[2], gradeKy[3], gradeKm[2], gradeKm[3]);
  if (v < 0.75) return gradeHermite(v, 0.5, 0.75, gradeKy[3], gradeKy[4], gradeKm[3], gradeKm[4]);
  if (v < 0.9)  return gradeHermite(v, 0.75, 0.9, gradeKy[4], gradeKy[5], gradeKm[4], gradeKm[5]);
  return gradeHermite(v, 0.9, 1.0, gradeKy[5], gradeKy[6], gradeKm[5], gradeKm[6]);
}

void mainImage(const in vec4 inputColor, const in vec2 uv, out vec4 outputColor) {
  vec3 src = gradeEncode(inputColor.rgb);
  vec3 c = vec3(gradeCurve(src.r), gradeCurve(src.g), gradeCurve(src.b));
  const vec3 W = vec3(0.2126, 0.7152, 0.0722);
  float y = dot(c, W);
  float wS = 1.0 - smoothstep(0.0, 0.55, y);
  float wH = smoothstep(0.45, 1.0, y);
  float wM = 1.0 - wS - wH;
  float s = gradeSat.y + (gradeSat.x - gradeSat.y) * wS + (gradeSat.z - gradeSat.y) * wH;
  c = vec3(y) + s * (c - vec3(y));
  c += wS * gradeTintS + wM * gradeTintM + wH * gradeTintH;
  vec2 p = uv * 2.0 - 1.0;
  float r = length(p) * 0.70710678;
  c *= 1.0 - gradeVig.x * smoothstep(gradeVig.y, 1.0, r);
  c = clamp(c, 0.0, 1.0);
  outputColor = vec4(gradeDecode(mix(src, c, gradeAmount)), inputColor.a);
}`;

// BT.709 zero-luma chroma basis (sRGB-encoded units): unit Cb and unit Cr as RGB offsets with Y' unchanged
const E_CB: [number, number, number] = [0.0, -0.18733, 1.8556];
const E_CR: [number, number, number] = [1.5748, -0.46813, 0.0];
export const tintRGB = (cb: number, cr: number) =>
  new Vector3(cb * E_CB[0] + cr * E_CR[0], cb * E_CB[1] + cr * E_CR[1], cb * E_CB[2] + cr * E_CR[2]);

/** Fritsch-Carlson monotone tangents for the 7 fixed knots (same as scripts/grade.py `tangents`) */
export const KX = [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1];
export function monoTangents(ky: number[]): number[] {
  const n = KX.length, h: number[] = [], d: number[] = [], m = new Array(n).fill(0);
  for (let k = 0; k < n - 1; k++) { h.push(KX[k + 1] - KX[k]); d.push((ky[k + 1] - ky[k]) / h[k]); }
  m[0] = d[0]; m[n - 1] = d[n - 2];
  for (let k = 1; k < n - 1; k++) {
    if (d[k - 1] * d[k] <= 0) { m[k] = 0; continue; }
    const w1 = 2 * h[k] + h[k - 1], w2 = h[k] + 2 * h[k - 1];
    m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k]);
  }
  return m;
}

export type GradeParams = {
  ky: number[];                                  // 7 curve values at KX
  sat: [number, number, number];                 // shadows, mids, highlights
  tintS: [number, number]; tintM: [number, number]; tintH: [number, number];   // (Cb, Cr) per zone
  vig: [number, number];                         // strength, start radius
};

export class GradeEffect extends Effect {
  constructor(p: GradeParams, amount = 1) {
    super("GradeEffect", frag, {
      blendFunction: BlendFunction.NORMAL,
      uniforms: new Map<string, Uniform>([
        ["gradeKy", new Uniform(p.ky.slice())],
        ["gradeKm", new Uniform(monoTangents(p.ky))],
        ["gradeSat", new Uniform(new Vector3(...p.sat))],
        ["gradeTintS", new Uniform(tintRGB(...p.tintS))],
        ["gradeTintM", new Uniform(tintRGB(...p.tintM))],
        ["gradeTintH", new Uniform(tintRGB(...p.tintH))],
        ["gradeVig", new Uniform(new Vector2(...p.vig))],
        ["gradeAmount", new Uniform(amount)],
      ]),
    });
  }
  /** switch preset per shot (day <-> golden) or blend two presets during a crossfade/time-of-day change */
  set(p: GradeParams, q?: GradeParams, t = 0) {
    const L = (a: number, b: number) => a + (b - a) * t;
    const r: GradeParams = q ? {
      ky: p.ky.map((v, i) => L(v, q.ky[i])),
      sat: [L(p.sat[0], q.sat[0]), L(p.sat[1], q.sat[1]), L(p.sat[2], q.sat[2])],
      tintS: [L(p.tintS[0], q.tintS[0]), L(p.tintS[1], q.tintS[1])], tintM: [L(p.tintM[0], q.tintM[0]), L(p.tintM[1], q.tintM[1])],
      tintH: [L(p.tintH[0], q.tintH[0]), L(p.tintH[1], q.tintH[1])], vig: [L(p.vig[0], q.vig[0]), L(p.vig[1], q.vig[1])],
    } : p;
    const u = this.uniforms;
    u.get("gradeKy")!.value = r.ky.slice();
    u.get("gradeKm")!.value = monoTangents(r.ky);
    (u.get("gradeSat")!.value as Vector3).set(...r.sat);
    u.get("gradeTintS")!.value = tintRGB(...r.tintS);
    u.get("gradeTintM")!.value = tintRGB(...r.tintM);
    u.get("gradeTintH")!.value = tintRGB(...r.tintH);
    (u.get("gradeVig")!.value as Vector2).set(...r.vig);
  }
  get amount() { return this.uniforms.get("gradeAmount")!.value as number; }
  set amount(v: number) { this.uniforms.get("gradeAmount")!.value = v; }
}
