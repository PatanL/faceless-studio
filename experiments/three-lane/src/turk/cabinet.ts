// The Turk's cabinet as a modelled 3D prop (our own code): body on castors, three hinged doors and a drawer, a gear
// bay and a machinery bay with real gear wheels, the chessboard on top. For the explanation it opens as a cutaway:
// the front comes away (dashed ghost doors stay), the hidden master (a stick-kit card) sits inside with a candle,
// slides behind the false gear panel, reads iron markers under the board and works a lever up to the Turk's arm.
// The automaton itself is a stick-kit card (Turk figureOnly) seated behind the board; anchors for it are below.
import * as THREE from "three";
import { lambert, glowSprite } from "./sets";
import { cabinetWood, brass } from "./paint2";
import { NOINK } from "../ink";
import { Chess3D } from "./chess3d";

export const TOP = 0.9;                         // cabinet top surface, m
export const K = 1.2 / 660;                     // stick-kit Turk svg unit -> m (its cabinet front is 660 units wide)
/** Turk figure card (svg viewBox 900 x 1000, padded 300 on top) placement relative to the cabinet */
export const TURK_CARD = { w: 900 * K, h: 1300 * K, y: TOP - (1000 - 606) * K, z: -0.23 };
export const svgToCab = (sx: number, sy: number, out = new THREE.Vector3()) =>
  out.set((sx - 450) * K, TURK_CARD.y + (1000 - sy) * K, TURK_CARD.z);

export type CabState = {
  t: number;
  doorL?: number; doorR?: number; doorR2?: number; drawer?: number;
  cut?: number;              // 1 = cutaway (front removed, ghost doors)
  seat?: number;             // master x: 1 = right bay, 0 = behind the false gear panel
  master?: boolean;          // show the hidden master
  lever?: number;            // 0..1 the rod appears
  magnets?: { t: number; i: number }[];
  spin?: number;             // gear angle, rad
  bayGlow?: number;          // candle light in the left bay (outside view)
  masterCandle?: number;     // 0..1 his candle light (cutaway)
  char?: number;             // 0..1 burnt
};

function gearGeo(r: number, teeth: number, depth: number) {
  const s = new THREE.Shape();
  for (let i = 0; i < teeth * 2; i++) {
    const a0 = (i / (teeth * 2)) * Math.PI * 2, a1 = ((i + 1) / (teeth * 2)) * Math.PI * 2;
    const rr = i % 2 === 0 ? r : r * 0.8;
    if (i === 0) s.moveTo(Math.cos(a0) * rr, Math.sin(a0) * rr); else s.lineTo(Math.cos(a0) * rr, Math.sin(a0) * rr);
    s.lineTo(Math.cos(a1) * rr, Math.sin(a1) * rr);
  }
  const hole = new THREE.Path(); hole.absarc(0, 0, r * 0.22, 0, Math.PI * 2, true); s.holes.push(hole);
  return new THREE.ExtrudeGeometry(s, { depth, bevelEnabled: false });
}

export class Cabinet {
  readonly group = new THREE.Group();
  readonly chess: Chess3D;
  readonly masterAnchor = new THREE.Group();     // the Stage parents the master card here
  private doors: { pivot: THREE.Group; solid: THREE.Mesh; ghost: THREE.LineSegments }[] = [];
  private drawer: THREE.Group;
  private front: THREE.Object3D[] = [];
  private gears: THREE.Mesh[] = [];
  private magnets: { ball: THREE.Mesh; glow: THREE.Sprite }[] = [];
  private lever: THREE.Mesh;
  private falsePanel: THREE.Mesh;
  private bayGlow: THREE.Sprite;
  private masterGlow: THREE.Sprite;
  private charMats: { m: THREE.MeshLambertMaterial; c: THREE.Color }[] = [];
  constructor(setup = "mid") {
    const wood = lambert({ map: cabinetWood([1, 1]) });
    const woodDark = lambert({ map: cabinetWood([1, 1]), color: "#8a6a4a" });
    const brassM = lambert({ map: brass() });
    const inside = lambert({ color: "#2a2340" });
    const iron = lambert({ color: "#24203a" });
    for (const m of [wood, woodDark, brassM, inside, iron]) this.charMats.push({ m, c: m.color.clone() });
    const g = this.group;
    const add = (geo: THREE.BufferGeometry, mat: THREE.Material, x: number, y: number, z: number, parent: THREE.Object3D = g) => {
      const m = new THREE.Mesh(geo, mat); m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; parent.add(m); return m;
    };
    // castors and base
    for (const x of [-0.5, 0.5]) for (const z of [-0.22, 0.22]) {
      const w = add(new THREE.CylinderGeometry(0.05, 0.05, 0.04, 16), iron, x, 0.05, z); w.rotation.z = Math.PI / 2;
    }
    add(new THREE.BoxGeometry(1.26, 0.05, 0.64), woodDark, 0, 0.115, 0);
    // body: back, sides, bottom, top, inner divider
    add(new THREE.BoxGeometry(1.2, 0.74, 0.03), wood, 0, 0.51, -0.285);
    for (const s of [-1, 1]) add(new THREE.BoxGeometry(0.03, 0.74, 0.6), wood, s * 0.585, 0.51, 0);
    add(new THREE.BoxGeometry(1.24, 0.04, 0.64), wood, 0, TOP - 0.02, 0);
    add(new THREE.BoxGeometry(1.14, 0.02, 0.56), inside, 0, 0.29, 0);
    add(new THREE.BoxGeometry(0.03, 0.56, 0.56), wood, -0.14, 0.57, 0);
    // bay interiors (dark) - left = gear bay, right = machinery bay / the master's room
    add(new THREE.BoxGeometry(1.12, 0.54, 0.01), inside, 0, 0.57, -0.265);
    // front frame (removed on the cutaway)
    this.front.push(
      add(new THREE.BoxGeometry(1.2, 0.03, 0.03), wood, 0, 0.285, 0.29),
      add(new THREE.BoxGeometry(1.2, 0.03, 0.03), wood, 0, 0.865, 0.29),
      add(new THREE.BoxGeometry(0.03, 0.6, 0.03), wood, -0.14, 0.575, 0.29),
    );
    // gears in the left bay (the false panel when he hides behind it)
    for (const [x, y, r, n] of [[-0.45, 0.66, 0.085, 10], [-0.31, 0.5, 0.07, 9], [-0.27, 0.72, 0.05, 7], [-0.48, 0.42, 0.045, 6]] as const) {
      const ge = add(gearGeo(r, n, 0.018), brassM, x, y, 0.06); this.gears.push(ge);
    }
    this.falsePanel = add(new THREE.BoxGeometry(0.42, 0.54, 0.01), new THREE.MeshLambertMaterial({ color: "#1d1838", transparent: true, opacity: 0.55 }), -0.37, 0.57, 0.035);
    this.falsePanel.castShadow = false; this.falsePanel.visible = false;
    // machinery in the right bay: a brass drum and small gears (hides nothing in the outside view)
    const drum = add(new THREE.CylinderGeometry(0.06, 0.06, 0.5, 18), brassM, 0.23, 0.42, -0.12); drum.rotation.z = Math.PI / 2;
    for (const [x, y, r, n] of [[0.05, 0.68, 0.06, 9], [0.42, 0.7, 0.05, 8], [0.3, 0.6, 0.035, 6]] as const) {
      const ge = add(gearGeo(r, n, 0.016), brassM, x, y, -0.2); this.gears.push(ge);
    }
    // doors: hinge pivots; solid panels + dashed ghost outlines (cutaway)
    const door = (hx: number, w: number, dir: 1 | -1) => {
      const pivot = new THREE.Group(); pivot.position.set(hx, 0.575, 0.3); g.add(pivot);
      const geo = new THREE.BoxGeometry(w, 0.54, 0.02);
      const solid = add(geo, wood, (dir * w) / 2, 0, 0, pivot);
      add(new THREE.SphereGeometry(0.014, 10, 8), brassM, dir * (w - 0.035), 0, 0.02, pivot);
      add(new THREE.BoxGeometry(w - 0.06, 0.46, 0.006), woodDark, (dir * w) / 2, 0, 0.012, pivot);
      const ghost = new THREE.LineSegments(new THREE.EdgesGeometry(geo), new THREE.LineDashedMaterial({ color: "#f2ead8", dashSize: 0.025, gapSize: 0.015 }));
      ghost.computeLineDistances(); ghost.position.set((dir * w) / 2, 0, 0); ghost.layers.set(NOINK); ghost.visible = false; pivot.add(ghost);
      this.doors.push({ pivot, solid, ghost });
    };
    door(-0.58, 0.42, 1); door(-0.12, 0.35, 1); door(0.58, 0.35, -1);
    // drawer
    this.drawer = new THREE.Group(); g.add(this.drawer);
    add(new THREE.BoxGeometry(1.12, 0.13, 0.02), woodDark, 0, 0.2, 0.3, this.drawer);
    add(new THREE.SphereGeometry(0.015, 10, 8), brassM, 0, 0.2, 0.32, this.drawer);
    // the board on top
    this.chess = new Chess3D(setup, -TOP);
    this.chess.group.position.set(0.16, TOP, 0.02);
    g.add(this.chess.group);
    // iron markers under the board (cutaway), the lever rod, light pools
    for (let i = 0; i < 8; i++) {
      const x = 0.16 + (i - 3.5) * 0.06;
      const thread = add(new THREE.CylinderGeometry(0.0015, 0.0015, 0.05, 4), lambert({ color: "#e8e0cc" }), x, TOP - 0.065, 0.02);
      thread.castShadow = false;
      const ball = add(new THREE.SphereGeometry(0.013, 10, 8), iron, x, TOP - 0.095, 0.02);
      const gl = glowSprite(g, [255, 110, 80], 0.09, x, TOP - 0.095, 0.05); gl.visible = false;
      this.magnets.push({ ball, glow: gl });
      thread.visible = ball.visible = false;
      ball.userData.thread = thread;
    }
    this.lever = add(new THREE.CylinderGeometry(0.008, 0.008, 1, 8), brassM, 0, 0, 0);
    this.lever.visible = false;
    this.bayGlow = glowSprite(g, [255, 190, 110], 0.55, -0.37, 0.56, 0.1); this.bayGlow.visible = false;
    this.masterGlow = glowSprite(g, [255, 190, 110], 0.5, 0.2, 0.62, 0.0); this.masterGlow.visible = false;
    this.masterAnchor.position.set(0.23, 0.3, -0.08);
    g.add(this.masterAnchor);
  }
  /** world position of the master's candle hand (holdHigh), given the master card size */
  masterHand(cardW: number, cardH: number, out = new THREE.Vector3()) {
    return out.set(this.masterAnchor.position.x + ((452 - 300) / 600) * cardW, this.masterAnchor.position.y + ((700 - 236) / 700) * cardH,
      this.masterAnchor.position.z + 0.01);
  }
  update(s: CabState, masterCard: { w: number; h: number } | null) {
    const open = [s.doorL ?? 0, s.doorR ?? 0, s.doorR2 ?? 0];
    const cut = (s.cut ?? 0) > 0.5;
    this.doors.forEach((d, i) => {
      const dir = i === 2 ? 1 : -1;
      d.pivot.rotation.y = dir * open[i] * 1.75;
      d.pivot.children.forEach((c) => { if (c !== d.ghost) c.visible = !cut; });
      d.ghost.visible = cut;
    });
    this.front.forEach((f) => (f.visible = !cut));
    this.drawer.position.z = (s.drawer ?? 0) * 0.18;
    this.falsePanel.visible = cut;
    for (const ge of this.gears) ge.rotation.z = (s.spin ?? 0) * (ge.position.x > -0.14 ? -1.3 : 1);
    const seat = s.seat ?? 1;
    this.masterAnchor.position.x = -0.37 + 0.6 * seat;
    this.masterAnchor.position.z = seat < 0.5 ? -0.16 : -0.08;
    this.masterAnchor.visible = !!s.master;
    // markers: visible on the cutaway; a hit jumps up and glows
    this.magnets.forEach((m, i) => {
      const hit = (s.magnets ?? []).filter((q) => q.i === i && s.t >= q.t).pop();
      const age = hit ? s.t - hit.t : 9;
      const up = hit ? (age < 0.18 ? age / 0.18 : Math.max(0, 1 - (age - 1.4) / 0.4)) : 0;
      m.ball.visible = cut; (m.ball.userData.thread as THREE.Mesh).visible = cut;
      m.ball.position.y = TOP - 0.095 + up * 0.03;
      m.glow.visible = cut && up > 0.05; m.glow.position.y = m.ball.position.y; m.glow.scale.setScalar(0.09 * (0.6 + up));
    });
    this.bayGlow.visible = (s.bayGlow ?? 0) > 0.01;
    this.bayGlow.scale.setScalar(0.25 + 0.5 * (s.bayGlow ?? 0));
    this.masterGlow.visible = !!s.master && (s.masterCandle ?? 0) > 0.01 && masterCard !== null;
    if (masterCard) {
      const hand = this.masterHand(masterCard.w, masterCard.h);
      this.masterGlow.position.copy(hand).add(new THREE.Vector3(0, 0.05, 0.03));
      this.masterGlow.scale.setScalar(0.45 * (s.masterCandle ?? 0));
      // the lever: from his hand (lowered, 'hold' pose) up through the top to the Turk's right shoulder
      const lv = s.lever ?? 0;
      this.lever.visible = cut && lv > 0.02;
      if (this.lever.visible) {
        const a = new THREE.Vector3(this.masterAnchor.position.x + ((440 - 300) / 600) * masterCard.w,
          this.masterAnchor.position.y + ((700 - 352) / 700) * masterCard.h, this.masterAnchor.position.z + 0.02);
        const b = svgToCab(372, 412);
        const mid = a.clone().lerp(b, 0.5), len = a.distanceTo(b) * Math.min(1, lv * 1.2);
        this.lever.position.copy(a.clone().lerp(b, Math.min(1, lv * 1.2) * 0.5));
        this.lever.scale.set(1, Math.max(0.001, len), 1);
        this.lever.lookAt(b.clone().add(this.group.position)); // orient along a->b (cylinder y axis)
        this.lever.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
        void mid;
      }
    }
    const ch = s.char ?? 0;
    for (const { m, c } of this.charMats) m.color.copy(c).lerp(new THREE.Color("#120e18"), ch * 0.9);
  }
}
