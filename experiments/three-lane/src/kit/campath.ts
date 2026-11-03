// Camera path for one continuous shot group (our own code; the 3D twin of pipeline/episodes/story_camera.py's
// "toward" grammar). Keys are checked framings {t, pos, look}. The camera glides between them with sine-eased moves
// of ~0.9 s that land just after the key time, and never stops: on every hold it pushes in a little and drifts
// toward the next framing (saturating, so it never overshoots a checked framing). Velocity is continuous.
import * as THREE from "three";

// drift: scales this hold's push-in and orbit (1 = default); a tight group shot uses less so its edge figures stay whole
export type CamKey = { t: number; pos: [number, number, number]; look: [number, number, number]; fov?: number; glide?: number; drift?: number;
  /** exact mode (replication study, 2026-11-02): when any key of a path sets `ease`, the path goes through every key at
   * its time with no automatic glide, drift, push or orbit; `ease` shapes the segment that ENDS at this key and
   * `curve` runs that segment on a Catmull-Rom spline through the neighbouring keys (orbits, crane arcs) */
  ease?: Ease; curve?: boolean };
export type Ease = "lin" | "io" | "in" | "out" | "io5" | "snap";
const EASE: Record<Ease, (u: number) => number> = {
  lin: (u) => u, io: (u) => u * u * (3 - 2 * u), in: (u) => u * u, out: (u) => 1 - (1 - u) * (1 - u),
  io5: (u) => u * u * u * (u * (u * 6 - 15) + 10),
  // a snap: most of the travel in the first third, a long settle (the references' punch-ins)
  snap: (u) => 1 - Math.pow(1 - u, 4),
};
const cr = (a: THREE.Vector3, b: THREE.Vector3, c: THREE.Vector3, d: THREE.Vector3, u: number) => {
  const u2 = u * u, u3 = u2 * u;
  return new THREE.Vector3().addScaledVector(a, -0.5 * u3 + u2 - 0.5 * u).addScaledVector(b, 1.5 * u3 - 2.5 * u2 + 1)
    .addScaledVector(c, -1.5 * u3 + 2 * u2 + 0.5 * u).addScaledVector(d, 0.5 * u3 - 0.5 * u2);
};
type S = { pos: THREE.Vector3; look: THREE.Vector3; fov: number };

// every hold travels steadily FRAC of the way to the next framing and pushes in PUSH of the distance
// ORBIT: each hold also swings the camera a few degrees around its subject (parallax: v7 still measured 4.6 px/f)
const GLIDE = 0.9, LAND = 0.3, FRAC = 0.85, PUSH = 0.25, ORBIT = (9 * Math.PI) / 180;

export class CamPath {
  private keys: CamKey[];
  private glides: { s: number; e: number }[] = [];
  private exact: boolean;
  constructor(keys: CamKey[], private t0: number, private t1: number) {
    this.keys = [...keys].sort((a, b) => a.t - b.t);
    this.exact = this.keys.some((k) => k.ease !== undefined);
    if (this.exact) return;
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
    const d = k.drift ?? 1;
    pos.addScaledVector(toLook, PUSH * d * sat);
    // swing around the subject (alternate direction per key so consecutive holds don't drift one way)
    const off = pos.clone().sub(look).applyAxisAngle(new THREE.Vector3(0, 1, 0), ORBIT * d * sat * (i % 2 ? -1 : 1));
    pos.copy(look).add(off);
    return { pos, look, fov: k.fov ?? 40 };
  }
  private holdLen(i: number) {
    const start = i === 0 ? this.t0 : this.glides[i - 1].e;
    const end = i < this.glides.length ? this.glides[i].s : this.t1;
    return end - start;
  }
  private exactAt(t: number): S {
    const K = this.keys, n = K.length;
    const v = (i: number, f: "pos" | "look") => new THREE.Vector3(...K[Math.max(0, Math.min(n - 1, i))][f]);
    if (t <= K[0].t || n === 1) return { pos: v(0, "pos"), look: v(0, "look"), fov: K[0].fov ?? 40 };
    if (t >= K[n - 1].t) return { pos: v(n - 1, "pos"), look: v(n - 1, "look"), fov: K[n - 1].fov ?? 40 };
    let i = 0; while (t >= K[i + 1].t) i++;
    const b = K[i + 1], u = EASE[b.ease ?? "io"]((t - K[i].t) / (b.t - K[i].t));
    const seg = (f: "pos" | "look") => (b.curve ? cr(v(i - 1, f), v(i, f), v(i + 1, f), v(i + 2, f), u) : v(i, f).lerp(v(i + 1, f), u));
    return { pos: seg("pos"), look: seg("look"), fov: (K[i].fov ?? 40) + ((b.fov ?? 40) - (K[i].fov ?? 40)) * u };
  }
  at(t: number): S {
    if (this.exact) return this.exactAt(t);
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
