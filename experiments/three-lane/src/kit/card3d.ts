// A flat card in the 3D world (our own code, after src/card.ts): any texture (a rasterised stick-kit SVG) on an
// upright plane, on the NOINK layer (the world ink pass never outlines it; the SVG carries its own ink), lit flat by
// the scene's key light colour (warm where it reaches the card, the shade colour where a cast shadow falls on it,
// no form shading - the references show none), casting a cut-out shadow, with a contact blob under its feet.
import * as THREE from "three";
import { LFB } from "../shade";
import { NOINK } from "../ink";
import { blob } from "../paint";

/** shared per-scene card light (Stage sets it from the light preset): lit tint and shade tint */
export const CARD_TONE = {
  uLitTint: { value: new THREE.Vector3(1.06, 0.98, 0.88) },
  uShadeTint: { value: new THREE.Vector3(0.62, 0.62, 0.88) },
};

let blobTex: THREE.Texture | null = null;

export type CardOpts = {
  w: number; h: number;            // plane size, m
  footY?: number;                  // fraction of the plane height where the feet are (0 = bottom edge)
  billboard?: boolean;             // yaw toward the camera (default true)
  contact?: number;                // contact blob width, m (0 = none)
  shadow?: boolean;                // casts a shadow (default true)
  emissive?: number;               // 0..1 self-lit (fire, glowing paper)
  doubleSide?: boolean;
};

export class Card3D {
  readonly group = new THREE.Group();
  readonly plane: THREE.Mesh;
  readonly mat: THREE.MeshLambertMaterial;
  private contact: THREE.Mesh | null = null;
  private uni: { uEmit: { value: number }; uOpacity: { value: number }; uChar: { value: number }; uBurn: { value: number }; uHead: { value: THREE.Vector4 }; uMirror: { value: number } };
  constructor(readonly tex: THREE.Texture, readonly o: CardOpts) {
    const footY = o.footY ?? 0;
    this.mat = new THREE.MeshLambertMaterial({ map: tex, alphaTest: 0.5, side: THREE.DoubleSide, transparent: false });
    this.uni = { uEmit: { value: o.emissive ?? 0 }, uOpacity: { value: 1 }, uChar: { value: 0 }, uBurn: { value: 0 },
      uHead: { value: new THREE.Vector4(0, 0, 0, 0) }, uMirror: { value: 1 } };
    const uni = this.uni;
    this.mat.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, CARD_TONE, uni);
      sh.fragmentShader = sh.fragmentShader
        .replace("#include <common>", "#include <common>\nuniform vec3 uLitTint; uniform vec3 uShadeTint; uniform float uEmit; uniform float uChar; uniform float uBurn; uniform vec4 uHead; uniform float uMirror;")
        // burning to ash: blocks of the card drop out, from the top down, with a glowing edge
        .replace("#include <alphatest_fragment>", "#include <alphatest_fragment>\n" +
          "float nz = fract( sin( dot( floor( vMapUv * vec2( 48.0, 96.0 ) ), vec2( 12.9898, 78.233 ) ) ) * 43758.5453 );\n" +
          "float burnK = nz * 0.55 + vMapUv.y * 0.45;\n" +
          "if ( uBurn > 0.0 && burnK < uBurn * 1.05 - 0.02 ) discard;\n" +
          "float ember = uBurn > 0.0 ? smoothstep( 0.06, 0.0, burnK - uBurn ) : 0.0;")
        .replace("#include <lights_fragment_begin>", "float sunVis = 1.0;\n" + LFB)
        .replace("vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;",
          "vec3 lightK = mix( uShadeTint, uLitTint, sunVis );\n" +
          "vec3 base = mix( diffuseColor.rgb, vec3( 0.05, 0.045, 0.06 ) * (0.6 + 0.4 * diffuseColor.r), uChar );\n" +
          // the head (round 2, owner): pure-white pixels inside the head circle are shaded as a sphere lit by the key
          // light (half-Lambert, soft ramp; refs: lit 0.97, darkest ~0.87 of white, falling away from the key), with
          // a little extra fall-off toward the rim so the roundness reads
          "#if NUM_DIR_LIGHTS > 0\n" +
          "if ( uHead.z > 0.0 ) {\n" +
          "  vec2 hd = ( vMapUv - uHead.xy ) / vec2( uHead.z, uHead.w );\n" +
          "  float rr = dot( hd, hd );\n" +
          "  float white = step( 0.93, min( diffuseColor.r, min( diffuseColor.g, diffuseColor.b ) ) );\n" +
          "  if ( rr < 1.0 && white > 0.5 ) {\n" +
          "    vec3 nrm = normalize( vec3( hd.x * uMirror, hd.y, sqrt( max( 0.0, 1.0 - rr ) ) ) );\n" +
          "    vec3 Lv = normalize( directionalLights[ 0 ].direction );\n" +
          "    float hl = 0.5 + 0.5 * dot( nrm, Lv );\n" +
          "    float k = mix( 0.80, 1.0, smoothstep( 0.18, 0.92, hl ) ) * mix( 0.93, 1.0, smoothstep( 0.0, 0.55, nrm.z ) );\n" +
          "    base *= k * mix( vec3( 0.97, 0.97, 1.03 ), vec3( 1.0 ), smoothstep( 0.8, 1.0, k ) );\n" +
          "  }\n" +
          "}\n" +
          "#endif\n" +
          "vec3 outgoingLight = mix( base * lightK, base, uEmit ) + vec3( 1.6, 0.55, 0.12 ) * ember;");
    };
    this.mat.customProgramCacheKey = () => "turkCard4";
    this.plane = new THREE.Mesh(new THREE.PlaneGeometry(o.w, o.h), this.mat);
    this.plane.position.y = o.h / 2 - footY * o.h;
    this.plane.castShadow = o.shadow ?? true;
    this.plane.receiveShadow = true;
    this.plane.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: tex, alphaTest: 0.5 });
    this.plane.layers.set(NOINK);
    this.group.add(this.plane);
    if ((o.contact ?? 0) > 0) {
      blobTex = blobTex ?? blob();
      const bm = new THREE.MeshBasicMaterial({
        map: blobTex, depthWrite: false, fog: false, toneMapped: false,
        blending: THREE.CustomBlending, blendEquation: THREE.AddEquation, blendSrc: THREE.ZeroFactor, blendDst: THREE.SrcColorFactor,
        polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2,
      });
      this.contact = new THREE.Mesh(new THREE.PlaneGeometry(o.contact!, o.contact! * 0.5), bm);
      this.contact.rotation.x = -Math.PI / 2; this.contact.position.y = 0.004; this.contact.renderOrder = 1;
      this.contact.layers.set(NOINK);
      this.group.add(this.contact);
    }
  }
  set emit(v: number) { this.uni.uEmit.value = v; }
  set char(v: number) { this.uni.uChar.value = v; }
  /** the head circle in texture uv (centre u, v and radius in u, v; radius 0 = no sphere shading) */
  head(u: number, v: number, ru: number, rv: number) { this.uni.uHead.value.set(u, v, ru, rv); this.uni.uMirror.value = Math.sign(this.group.scale.x) || 1; }
  set burn(v: number) { this.uni.uBurn.value = v; }
  set visible(v: boolean) { this.group.visible = v; }
  /** place feet at (x, y, z); yaw to the camera unless billboard: false (then face +z rotated by yaw) */
  place(x: number, y: number, z: number, cam: THREE.Camera, yaw = 0) {
    this.group.position.set(x, y, z);
    this.group.rotation.y = (this.o.billboard ?? true)
      ? Math.atan2(cam.position.x - x, cam.position.z - z) : yaw;
  }
}
