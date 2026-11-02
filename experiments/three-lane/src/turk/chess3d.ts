// A real chessboard and pieces on the Turk's cabinet (our own code): lathe-turned pieces, a checker board with a
// frame, moves that lift the piece in an arc, a king that topples, an illegal-move marker, and the sweep that throws
// every piece off the board to the floor. Hands (the Turk's wooden glove, a player's glove) are cards that come in
// from the player's side, carry the piece and leave with a slow start (no snaps).
import * as THREE from "three";
import { lambert } from "./sets";
import { NOINK } from "../ink";

export const SQ = 0.06;                        // square size, m
const SETUPS: Record<string, Record<string, string>> = {
  mid: { e4: "wP", d4: "wP", f3: "wN", c4: "wB", e1: "wK", a2: "wP", h2: "wR", d1: "wQ",
    e5: "bP", d6: "bP", c6: "bN", g8: "bK", f7: "bP", a7: "bP", h8: "bR", d8: "bQ", g6: "bP" },
  napoleon: { e4: "wP", c3: "wN", d1: "wQ", e1: "wK", b2: "wP", g2: "wP", f1: "wB", h1: "wR",
    e5: "bP", c5: "bP", f6: "bN", e8: "bK", d8: "bQ", a7: "bP", g7: "bP", h8: "bR" },
};

export type Move = { t: number; from: string; to: string; dur?: number; hand?: "turk" | "human"; illegal?: boolean };
export type ChessState = { t: number; moves: Move[]; topple?: { t: number; sq: string }; glow?: { t: number; sq: string }; sweepAt?: number };

const profile: Record<string, [number, number][]> = {
  P: [[0, 0], [0.016, 0], [0.016, 0.006], [0.009, 0.012], [0.006, 0.026], [0.011, 0.03], [0.009, 0.04], [0, 0.044]],
  R: [[0, 0], [0.018, 0], [0.018, 0.007], [0.012, 0.012], [0.011, 0.04], [0.016, 0.046], [0.016, 0.056], [0, 0.056]],
  N: [[0, 0], [0.018, 0], [0.018, 0.007], [0.011, 0.014], [0.01, 0.034], [0.014, 0.05], [0.008, 0.06], [0, 0.06]],
  B: [[0, 0], [0.018, 0], [0.018, 0.007], [0.01, 0.014], [0.008, 0.044], [0.012, 0.056], [0.006, 0.066], [0, 0.07]],
  Q: [[0, 0], [0.019, 0], [0.019, 0.008], [0.011, 0.016], [0.009, 0.05], [0.016, 0.064], [0.01, 0.07], [0.005, 0.078], [0, 0.08]],
  K: [[0, 0], [0.019, 0], [0.019, 0.008], [0.011, 0.016], [0.009, 0.056], [0.015, 0.068], [0.009, 0.074], [0.003, 0.082], [0.003, 0.092], [0, 0.092]],
};
const geoCache: Record<string, THREE.LatheGeometry> = {};
const pieceGeo = (k: string) => (geoCache[k] ??= new THREE.LatheGeometry(profile[k].map(([r, y]) => new THREE.Vector2(r, y)), 18));

const ease = (u: number) => { u = Math.min(1, Math.max(0, u)); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
const easeOut = (u: number) => 1 - Math.pow(1 - Math.min(1, Math.max(0, u)), 3);

function checker() {
  const c = document.createElement("canvas"); c.width = 512; c.height = 512;
  const g = c.getContext("2d")!;
  for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) { g.fillStyle = (i + j) % 2 ? "#efe6d2" : "#3a3658"; g.fillRect(i * 64, j * 64, 64, 64); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function handTex(kind: "turk" | "human") {
  const c = document.createElement("canvas"); c.width = 256; c.height = 1024;
  const g = c.getContext("2d")!;
  g.lineJoin = "round"; g.lineCap = "round";
  g.strokeStyle = "#1b1240"; g.lineWidth = 8;
  if (kind === "turk") {
    g.fillStyle = "#b8442e"; g.beginPath(); g.rect(78, 0, 100, 820); g.fill(); g.stroke();       // red sleeve
    g.fillStyle = "#e3b04b"; g.beginPath(); g.rect(64, 800, 128, 46); g.fill(); g.stroke();     // brass cuff
    g.fillStyle = "#c79a62"; g.beginPath(); g.roundRect(72, 846, 112, 120, 30); g.fill(); g.stroke(); // wooden glove
    for (const x of [86, 116, 146]) { g.beginPath(); g.roundRect(x, 940, 24, 70, 12); g.fill(); g.stroke(); }
  } else {
    g.fillStyle = "#2a3b78"; g.beginPath(); g.rect(80, 0, 96, 800); g.fill(); g.stroke();       // blue sleeve
    g.fillStyle = "#f4eee1"; g.beginPath(); g.rect(66, 780, 124, 46); g.fill(); g.stroke();     // cuff
    g.fillStyle = "#f4eee1"; g.beginPath(); g.arc(128, 900, 66, 0, Math.PI * 2); g.fill(); g.stroke(); // white glove
    for (const [x, y] of [[96, 960], [128, 975], [160, 960]]) { g.beginPath(); g.arc(x, y, 22, 0, Math.PI * 2); g.fill(); g.stroke(); }
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export class Chess3D {
  readonly group = new THREE.Group();
  private pieces: Record<string, THREE.Mesh> = {};
  private setup: Record<string, string>;
  private white = lambert({ color: "#f4eee1" });
  private black = lambert({ color: "#2a2340" });
  private hands: Record<string, THREE.Mesh> = {};
  private marker: THREE.Mesh;
  private ring: THREE.Mesh;
  private floorY: number;
  constructor(setupName: string, floorY: number) {
    this.floorY = floorY;
    this.setup = { ...SETUPS[setupName] };
    const frame = new THREE.Mesh(new THREE.BoxGeometry(SQ * 8 + 0.05, 0.02, SQ * 8 + 0.05), lambert({ color: "#7a4a24" }));
    frame.position.y = 0.0; frame.castShadow = true; frame.receiveShadow = true; this.group.add(frame);
    const board = new THREE.Mesh(new THREE.PlaneGeometry(SQ * 8, SQ * 8), lambert({ map: checker() }));
    board.rotation.x = -Math.PI / 2; board.position.y = 0.0105; board.receiveShadow = true; this.group.add(board);
    for (const [sq, p] of Object.entries(this.setup)) {
      const m = new THREE.Mesh(pieceGeo(p[1]), p[0] === "w" ? this.white : this.black);
      m.castShadow = true; m.receiveShadow = true;
      this.pieces[sq] = m; this.group.add(m);
    }
    for (const k of ["turk", "human"] as const) {
      const mat = new THREE.MeshBasicMaterial({ map: handTex(k), alphaTest: 0.5, side: THREE.DoubleSide, fog: false });
      const h = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 0.24), mat);
      h.geometry.translate(0, 0.12, 0);              // pivot at the glove tip
      h.layers.set(NOINK); h.visible = false; this.hands[k] = h; this.group.add(h);
    }
    const mk = document.createElement("canvas"); mk.width = 128; mk.height = 128;
    const g = mk.getContext("2d")!;
    g.fillStyle = "#d94a3a"; g.beginPath(); g.arc(64, 64, 58, 0, Math.PI * 2); g.fill();
    g.strokeStyle = "#fff6e6"; g.lineWidth = 16; g.lineCap = "round";
    g.beginPath(); g.moveTo(38, 38); g.lineTo(90, 90); g.moveTo(90, 38); g.lineTo(38, 90); g.stroke();
    const mt = new THREE.CanvasTexture(mk); mt.colorSpace = THREE.SRGBColorSpace;
    this.marker = new THREE.Mesh(new THREE.PlaneGeometry(0.05, 0.05), new THREE.MeshBasicMaterial({ map: mt, transparent: true, fog: false }));
    this.marker.layers.set(NOINK); this.marker.visible = false; this.group.add(this.marker);
    this.ring = new THREE.Mesh(new THREE.TorusGeometry(0.026, 0.004, 8, 32), new THREE.MeshBasicMaterial({ color: "#e0503a", fog: false }));
    this.ring.rotation.x = -Math.PI / 2; this.ring.layers.set(NOINK); this.ring.visible = false; this.group.add(this.ring);
  }
  /** square name -> local board position (white at +z, files a..h along +x) */
  sqPos(sq: string, out = new THREE.Vector3()) {
    const f = sq.charCodeAt(0) - 97, r = Number(sq[1]) - 1;
    return out.set((f - 3.5) * SQ, 0.011, (3.5 - r) * SQ);
  }
  update(s: ChessState, cam: THREE.Camera) {
    const LEAD = 0.45, OUT = 0.7;
    const pos: Record<string, string> = {};
    for (const k of Object.keys(this.setup)) pos[k] = k;       // square -> original piece id (its starting square)
    const v = new THREE.Vector3(), a = new THREE.Vector3(), b = new THREE.Vector3();
    for (const h of Object.values(this.hands)) h.visible = false;
    this.marker.visible = false;
    const placed: Record<string, THREE.Vector3> = {};
    let flying: { id: string; p: THREE.Vector3 } | null = null;
    for (const m of [...s.moves].sort((x, y) => x.t - y.t)) {
      const dur = m.dur ?? 0.45;
      if (s.t < m.t - LEAD) break;
      const id = pos[m.from];
      if (!id) continue;
      this.sqPos(m.from, a); this.sqPos(m.to, b);
      const k = Math.min(1, Math.max(0, (s.t - m.t) / dur)), e = ease(k);
      v.lerpVectors(a, b, e); v.y += Math.sin(e * Math.PI) * 0.07;
      if (s.t >= m.t + dur) { delete pos[m.from]; pos[m.to] = id; }
      else if (s.t >= m.t) { delete pos[m.from]; flying = { id, p: v.clone() }; }
      if (m.hand && s.t < m.t + dur + OUT) {
        const kin = Math.min(1, Math.max(0, (s.t - m.t + LEAD) / LEAD));
        const out = Math.min(1, Math.max(0, (s.t - m.t - dur) / OUT));
        const o = Math.max(out * out, 1 - easeOut(kin));
        const h = this.hands[m.hand];
        const dir = m.hand === "turk" ? new THREE.Vector3(0.05, 0.55, -0.6) : new THREE.Vector3(0.45, 0.4, 0.55);
        h.position.copy(v).addScaledVector(dir, o).add(new THREE.Vector3(0, 0.03, 0));
        h.lookAt(h.position.clone().add(dir));       // the sleeve trails back toward where the arm comes from
        h.rotateX(Math.PI / 2);
        h.visible = true;
      }
      if (m.illegal && s.t >= m.t + dur && s.t < m.t + dur + 1.2) {
        this.marker.visible = true;
        this.marker.position.copy(b).add(new THREE.Vector3(SQ * 0.9, 0.11, 0));
        this.marker.quaternion.copy((cam as THREE.PerspectiveCamera).quaternion);
        const age = s.t - m.t - dur; this.marker.scale.setScalar(easeOut(age / 0.25) * (age > 0.9 ? 1 - (age - 0.9) / 0.3 : 1));
      }
    }
    for (const [sq, id] of Object.entries(pos)) placed[id] = this.sqPos(sq);
    const sweeping = s.sweepAt !== undefined && s.t >= s.sweepAt;
    for (const [id, mesh] of Object.entries(this.pieces)) {
      mesh.rotation.set(0, 0, 0);
      if (flying && flying.id === id) { mesh.position.copy(flying.p); mesh.visible = true; continue; }
      const p = placed[id];
      if (!p) { mesh.visible = false; continue; }
      mesh.visible = true; mesh.position.copy(p);
      if (s.topple && s.t >= s.topple.t && Object.entries(pos).find(([, i]) => i === id)?.[0] === s.topple.sq) {
        mesh.rotation.z = -1.45 * easeOut((s.t - s.topple.t) / 0.35);
      }
      if (sweeping) {
        // thrown off the board toward +x (the player's side) and down to the floor, where they bounce and lie
        const dt = Math.max(0, s.t - s.sweepAt! - (p.x + 0.25) * 0.4);
        if (dt > 0) {
          const vx = 1.4 + (p.z + 0.3) * 0.8, vy = 1.2 + ((p.x * 37) % 0.3), vz = 0.5 + p.z;
          const floor = this.floorY - 0.0;
          let y = p.y + vy * dt - 4.9 * dt * dt;
          if (y < floor) y = floor;
          mesh.position.set(p.x + vx * Math.min(dt, 0.9), y, p.z + vz * Math.min(dt, 0.9));
          mesh.rotation.set(dt * 9, 0, dt * 7);
          if (y <= floor) mesh.rotation.set(Math.PI / 2, 0, (p.x * 13) % 3);
        }
      }
    }
    if (s.glow && s.t >= s.glow.t) {
      this.ring.visible = true; this.sqPos(s.glow.sq, this.ring.position); this.ring.position.y = 0.013;
      this.ring.scale.setScalar(easeOut((s.t - s.glow.t) / 0.3) * 1.2);
    } else this.ring.visible = false;
  }
}
