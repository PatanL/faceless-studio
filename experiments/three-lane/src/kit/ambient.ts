// Kit-wide life and readability the Stage adds to every set (our own code; Vasa panel round 4: "flat sparse water
// and sky", "HEAVY/LIGHT labels small"):
//   skyLife    inked painted clouds round any sky dome (sets.skyDome marks it), drifting slowly; tinted by the light
//   waterLife  a transparent layer of wave strokes and foam over a set's `extra.water` plane, scrolling against the
//              water's own texture, so open water always carries moving painted detail
//   minLabel   world labels (tagSprite marks them with userData.minPx) never read smaller than their minimum
//              on-screen height: a far label grows instead of shrinking to a smudge
// A group opts out with `clouds: false` / `waves: false`.
import * as THREE from "three";
import { NOINK } from "../ink";
import { rng } from "../paint";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
let cloudTx: THREE.Texture[] | null = null;
function cloudTextures() {
  if (cloudTx) return cloudTx;
  cloudTx = [0, 1, 2].map((k) => {
    const [c, g] = canvas(512, 256), r = rng(31 + k);
    const blobs = Array.from({ length: 7 }, (_, i) => [90 + i * 55 + (r() - 0.5) * 30, 150 - Math.sin((i / 6) * Math.PI) * 50 - r() * 20, 50 + r() * 40] as const);
    g.fillStyle = "#1b1240"; for (const [x, y, rr] of blobs) { g.beginPath(); g.arc(x, y, rr + 6, 0, 7); g.fill(); }
    g.fillRect(84, 150, 344, 56);
    g.fillStyle = "#f6f1ea"; for (const [x, y, rr] of blobs) { g.beginPath(); g.arc(x, y, rr, 0, 7); g.fill(); }
    g.fillRect(90, 150, 332, 50);
    g.fillStyle = "rgba(170, 160, 210, 0.55)"; g.fillRect(90, 182, 332, 18);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  });
  return cloudTx;
}

export type Life = (t: number, bg: THREE.Color) => void;

/** clouds round the first sky dome found under root (radius from its geometry), between 4 and 22 degrees up */
export function skyLife(root: THREE.Object3D, seed = 7): Life | null {
  let dome: THREE.Mesh | null = null;
  root.traverse((o: THREE.Object3D) => { if (!dome && (o as THREE.Mesh).isMesh && o.userData.skyDome) dome = o as THREE.Mesh; });
  if (!dome) return null;
  // inside the camera far plane (Stage: 400 m), well in front of the dome
  const R = Math.min((dome as THREE.Mesh).userData.skyDome.r * 0.55, 320), r = rng(seed), tx = cloudTextures();
  const g = new THREE.Group(); (dome as THREE.Mesh).parent!.add(g);
  const mats: THREE.SpriteMaterial[] = [];
  for (let i = 0; i < 14; i++) {
    const a = (i / 14) * Math.PI * 2 + r() * 0.3, el = ((4 + r() * 18) * Math.PI) / 180, w = R * (0.16 + r() * 0.14);
    const m = new THREE.SpriteMaterial({ map: tx[i % 3], fog: false, transparent: true, depthWrite: false });
    const s = new THREE.Sprite(m); s.scale.set(w, w / 2, 1);
    s.position.set(Math.sin(a) * Math.cos(el) * R, Math.sin(el) * R, Math.cos(a) * Math.cos(el) * R);
    s.layers.set(NOINK); s.renderOrder = -9; g.add(s); mats.push(m);
  }
  return (t, bg) => {
    g.rotation.y = t * 0.006;                                       // a slow drift across the sky
    const k = new THREE.Color(1, 1, 1).lerp(bg, 0.35);              // clouds take the sky's colour at night
    for (const m of mats) m.color.copy(k);
  };
}

let waveTx: THREE.Texture | null = null;
function waveTexture() {
  if (waveTx) return waveTx;
  const [c, g] = canvas(512, 512), r = rng(11);
  for (let i = 0; i < 60; i++) {
    const x = r() * 512, y = r() * 512, w = 20 + r() * 60;
    g.strokeStyle = `rgba(235, 250, 255, ${0.35 + r() * 0.35})`; g.lineWidth = 2 + r() * 3; g.lineCap = "round";
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y - 6, x + w, y); g.stroke();
  }
  for (let i = 0; i < 140; i++) { g.fillStyle = `rgba(245, 252, 255, ${0.4 + r() * 0.4})`; g.fillRect(r() * 512, r() * 512, 2 + r() * 3, 1.5); }
  waveTx = new THREE.CanvasTexture(c); waveTx.colorSpace = THREE.SRGBColorSpace; waveTx.wrapS = waveTx.wrapT = THREE.RepeatWrapping;
  return waveTx;
}
/** wave detail over a water plane: a copy of its geometry 2 cm up, transparent strokes scrolling diagonally */
export function waterLife(water: THREE.Object3D | undefined): Life | null {
  const w = water as THREE.Mesh | undefined;
  if (!w || !w.isMesh || w.userData.noWaves) return null;
  const tx = waveTexture().clone(); tx.needsUpdate = true;
  const base = (w.material as THREE.MeshLambertMaterial).map;
  tx.repeat.copy(base ? base.repeat : new THREE.Vector2(40, 40)).multiplyScalar(1.3);
  const m = new THREE.Mesh(w.geometry, new THREE.MeshBasicMaterial({ map: tx, transparent: true, depthWrite: false, fog: true, opacity: 0.8 }));
  m.position.copy(w.position); m.rotation.copy(w.rotation); m.scale.copy(w.scale); m.position.y += 0.02;
  m.layers.set(NOINK); m.renderOrder = 1; w.parent!.add(m);
  return (t) => { tx.offset.set(-t * 0.012, t * 0.007); };
}

/** keep labelled sprites (userData.minPx) at least minPx tall on a 1920-high frame */
export function minLabel(root: THREE.Object3D, cam: THREE.PerspectiveCamera, H = 1920) {
  const v = new THREE.Vector3();
  root.traverse((o: THREE.Object3D) => {
    const min = o.userData.minPx as number | undefined;
    if (!min || !o.visible) return;
    // the scale a rig set this frame is the base; our own enlargement from last frame is not
    if (!o.userData.labelBase || !o.scale.equals(o.userData.labelSet)) o.userData.labelBase = o.scale.clone();
    const base = o.userData.labelBase as THREE.Vector3;
    o.getWorldPosition(v);
    const d = v.distanceTo(cam.position);
    const px = (base.y / (2 * d * Math.tan((cam.fov * Math.PI) / 360))) * H;
    o.scale.copy(base).multiplyScalar(px > 0 && px < min ? min / px : 1);
    o.userData.labelSet = o.scale.clone();
  });
}
