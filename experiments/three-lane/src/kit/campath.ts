// Camera path for one continuous shot group (our own code; the 3D twin of pipeline/episodes/story_camera.py's
// "toward" grammar). Keys are checked framings {t, pos, look}. The camera glides between them with sine-eased moves
// of ~0.9 s that land just after the key time, and never stops: on every hold it pushes in a little and drifts
// toward the next framing (saturating, so it never overshoots a checked framing). Velocity is continuous.
import * as THREE from "three";

export type CamKey = { t: number; pos: [number, number, number]; look: [number, number, number]; fov?: number; glide?: number };
type S = { pos: THREE.Vector3; look: THREE.Vector3; fov: number };

// every hold travels steadily FRAC of the way to the next framing and pushes in PUSH of the distance
const GLIDE = 0.9, LAND = 0.3, FRAC = 0.85, PUSH = 0.2;

export class CamPath {
  private keys: CamKey[];
  private glides: { s: number; e: number }[] = [];
  constructor(keys: CamKey[], private t0: number, private t1: number) {
    this.keys = [...keys].sort((a, b) => a.t - b.t);
    let prevEnd = t0;
    for (let i = 1; i < this.keys.length; i++) {
      const G = this.keys[i].glide ?? GLIDE;                       // a long move (a big swing) can take longer than GLIDE
      let s = Math.max(this.keys[i].t - (1 - LAND) * G, prevEnd + 1 / 30);
      let e = s + G;
      if (e > t1 + 0.1) { e = t1 + 0.1; s = Math.max(prevEnd + 1 / 30, e - GLIDE); }
      if (e - s < 0.5) e = s + 0.5;
      this.glides.push({ s, e }); prevEnd = e;
    }
  }
  private hold(i: number, tau: number): S {
    const k = this.keys[i], n = this.keys[i + 1];
    const pos = new THREE.Vector3(...k.pos), look = new THREE.Vector3(...k.look);
    // before the group starts (inside an incoming transition) the camera holds its first framing: extrapolating back
    // toward a far next key made the transition frames lurch (v1 review: jumps in every dissolve)
    // steady travel toward the next framing across the whole hold (eased in over 0.4 s) instead of a saturating drift:
    // story-vasa v2/v3 measured 3.8-4.5 px/f median motion against the refs' 5.8-11
    const len = Math.max(0.6, this.holdLen(i));
    const sat = tau >= 0 ? Math.min(1, (tau < 0.4 ? (tau * tau) / 0.8 : tau - 0.2) / len) : 0;
    if (n) {
      pos.addScaledVector(new THREE.Vector3(...n.pos).sub(pos), FRAC * sat);
      look.addScaledVector(new THREE.Vector3(...n.look).sub(look), FRAC * sat);
    }
    // push in along the view direction (slow, saturating at PUSH of the distance)
    const toLook = look.clone().sub(pos);
    pos.addScaledVector(toLook, PUSH * sat);
    return { pos, look, fov: k.fov ?? 40 };
  }
  private holdLen(i: number) {
    const start = i === 0 ? this.t0 : this.glides[i - 1].e;
    const end = i < this.glides.length ? this.glides[i].s : this.t1;
    return end - start;
  }
  at(t: number): S {
    const holdStart = (i: number) => (i === 0 ? this.t0 : this.glides[i - 1].e);
    for (let i = 0; i < this.glides.length; i++) {
      const g = this.glides[i];
      if (t < g.s) return this.hold(i, t - holdStart(i));
      if (t < g.e) {
        const a = this.hold(i, t - holdStart(i)), b = this.hold(i + 1, t - g.e);
        const u = 0.5 - 0.5 * Math.cos(Math.PI * (t - g.s) / (g.e - g.s));
        return { pos: a.pos.lerp(b.pos, u), look: a.look.lerp(b.look, u), fov: a.fov + (b.fov - a.fov) * u };
      }
    }
    const last = this.keys.length - 1;
    return this.hold(last, t - holdStart(last));
  }
}
