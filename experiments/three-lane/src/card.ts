// Flat character card (our own code): a canvas-drawn round-head stick figure on a camera-facing plane, on the
// NOINK layer (the world ink never outlines it), tinted by the scene light (warm where the key light reaches it,
// violet-blue where a cast shadow falls on it), casting a cut-out shadow, with a multiplied contact blob under it.
// The sun-visibility capture (LFB) comes from shade.ts.
import * as THREE from "three";
import { LFB } from "./shade";
import { NOINK } from "./ink";
import { blob } from "./paint";

const W = 512, H = 1024; // design canvas; the plane is 0.8 x 1.6 m

/** Round-head stick figure: white head with a dark rim and dot eyes, dark line limbs (~3.5 heads tall). */
export function drawStick(g: CanvasRenderingContext2D, t: number) {
  const ink = "#1c1a22";
  g.clearRect(0, 0, W, H);
  g.lineCap = "round"; g.lineJoin = "round";
  const bob = Math.sin(t * 0.25) * 4; // breathing bob, px
  const neck = 318 + bob, hip = 640 + bob * 0.5;
  g.strokeStyle = ink; g.lineWidth = 18;
  g.beginPath();
  g.moveTo(256, neck); g.lineTo(256, hip);                        // spine
  g.moveTo(256, neck + 50); g.lineTo(168, 520 + bob); g.lineTo(150, 640 + bob); // left arm
  g.moveTo(256, neck + 50); g.lineTo(346, 500 + bob); g.lineTo(392, 410 + bob); // right arm, raised a little
  g.moveTo(256, hip); g.lineTo(206, 820); g.lineTo(196, 1000);    // left leg
  g.moveTo(256, hip); g.lineTo(306, 820); g.lineTo(326, 1000);    // right leg
  g.stroke();
  // head
  const hy = 178 + bob;
  g.fillStyle = "#fbfaf6"; g.beginPath(); g.arc(256, hy, 138, 0, Math.PI * 2); g.fill();
  g.lineWidth = 14; g.stroke();
  g.fillStyle = ink;
  for (const ex of [212, 300]) { g.beginPath(); g.arc(ex, hy - 6, 13, 0, Math.PI * 2); g.fill(); }
}

export type Card = { group: THREE.Group; plane: THREE.Mesh; update: (frame: number, cam: THREE.Camera) => void };

export function makeCard(pos: THREE.Vector3, lit: THREE.Vector3, shade: THREE.Vector3): Card {
  const c = document.createElement("canvas"); c.width = W; c.height = H;
  const g = c.getContext("2d")!;
  drawStick(g, 0);
  const map = new THREE.CanvasTexture(c);
  map.colorSpace = THREE.SRGBColorSpace;

  const mat = new THREE.MeshLambertMaterial({ map, alphaTest: 0.5, side: THREE.DoubleSide });
  const uni = { uLitTint: { value: lit }, uShadeTint: { value: shade } };
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, uni);
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", "#include <common>\nuniform vec3 uLitTint; uniform vec3 uShadeTint;")
      .replace("#include <lights_fragment_begin>", "float sunVis = 1.0;\n" + LFB)
      .replace("vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;",
        // flat card: no N.L form shading (the references show none), only the light colour and cast shadows
        "vec3 outgoingLight = diffuseColor.rgb * mix( uShadeTint, uLitTint, sunVis );");
  };
  mat.customProgramCacheKey = () => "stickCard1";

  const plane = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 1.6), mat);
  plane.position.y = 0.8;
  plane.castShadow = true; plane.receiveShadow = true;
  plane.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map, alphaTest: 0.5 });
  plane.layers.set(NOINK);

  // contact shadow: multiplies the floor, drawn after it, never writes depth
  const blobMat = new THREE.MeshBasicMaterial({
    map: blob(), depthWrite: false, fog: false, toneMapped: false, transparent: false,
    blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.ZeroFactor, blendDst: THREE.SrcColorFactor,
    polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2,
  });
  const contact = new THREE.Mesh(new THREE.PlaneGeometry(0.75, 0.42), blobMat);
  contact.rotation.x = -Math.PI / 2; contact.position.y = 0.003; contact.renderOrder = 1;
  contact.layers.set(NOINK);

  const group = new THREE.Group();
  group.position.copy(pos);
  group.add(plane, contact);

  let lastT = -1;
  const update = (frame: number, cam: THREE.Camera) => {
    // yaw-only billboard: the card turns to the camera, stays upright
    group.rotation.y = Math.atan2(cam.position.x - group.position.x, cam.position.z - group.position.z);
    if (frame !== lastT) { drawStick(g, frame); map.needsUpdate = true; lastT = frame; }
  };
  return { group, plane, update };
}
