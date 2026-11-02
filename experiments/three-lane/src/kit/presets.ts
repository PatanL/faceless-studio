// Story lighting (our own code): the palette and light follow the story - warm daylight while the inventor sets up
// his show, golden in Paris, cool night in Vienna 1809, fire orange in Philadelphia and deep night blue (with one
// warm candle) once the explanation starts.
// Black point: v7 measured non-ink p5 0.045 against the references' 0.09-0.23 (crushed night/fire darks), so every curve
// starts above zero (day 0.05, night/fire/explain 0.08) and the second knot is lifted with it. Each preset sets the two-tone world light (shade.ts TONE), the card
// light, the key light, fog, background, the strength of the additive light pools and the grade.
import * as THREE from "three";
import type { GradeParams } from "../grade";

export type Preset = {
  lit: [number, number, number]; shade: [number, number, number];
  cardLit: [number, number, number]; cardShade: [number, number, number];
  key: string; keyI: number; fog: string; fogNear: number; fogFar: number; bg: string; glow: number;
  sat: number; grade: GradeParams;
};

const G = (ky: number[], sat: [number, number, number], tintS: [number, number], tintH: [number, number], vig = 0.2): GradeParams =>
  ({ ky, sat, tintS, tintM: [0, 0], tintH, vig: [vig, 0.42] });

export const PRESETS: Record<string, Preset> = {
  day: {
    lit: [1.38, 1.26, 1.06], shade: [0.56, 0.54, 0.84], cardLit: [1.04, 0.98, 0.9], cardShade: [0.7, 0.68, 0.9],
    key: "#ffe2b8", keyI: 2.0, fog: "#efdcbc", fogNear: 14, fogFar: 70, bg: "#efdcbc", glow: 0.45, sat: 0.82,
    grade: G([0.05, 0.13, 0.27, 0.55, 0.8, 0.93, 1], [0.86, 0.9, 0.86], [0.014, 0.006], [-0.008, 0.006], 0.16),
  },
  golden: {
    lit: [1.42, 1.18, 0.9], shade: [0.54, 0.48, 0.8], cardLit: [1.06, 0.94, 0.8], cardShade: [0.68, 0.62, 0.86],
    key: "#ffcf96", keyI: 2.0, fog: "#e9c79a", fogNear: 10, fogFar: 50, bg: "#e9c79a", glow: 0.7, sat: 0.84,
    grade: G([0.05, 0.13, 0.26, 0.54, 0.8, 0.93, 1], [0.86, 0.9, 0.88], [0.016, 0.008], [-0.012, 0.01], 0.2),
  },
  night: {
    lit: [0.72, 0.78, 1.12], shade: [0.3, 0.31, 0.6], cardLit: [0.86, 0.88, 1.06], cardShade: [0.5, 0.5, 0.76],
    key: "#b4c4ff", keyI: 1.6, fog: "#1c2150", fogNear: 10, fogFar: 46, bg: "#161a44", glow: 1.0, sat: 0.84,
    grade: G([0.08, 0.17, 0.28, 0.55, 0.79, 0.92, 1], [0.84, 0.88, 0.84], [0.02, 0.0], [-0.01, 0.01], 0.24),
  },
  fire: {
    lit: [1.5, 0.86, 0.5], shade: [0.3, 0.26, 0.54], cardLit: [1.1, 0.8, 0.6], cardShade: [0.46, 0.42, 0.66],
    key: "#ff9a5a", keyI: 2.0, fog: "#2b1a3a", fogNear: 8, fogFar: 40, bg: "#1d1430", glow: 1.0, sat: 0.84,
    grade: G([0.08, 0.17, 0.27, 0.54, 0.79, 0.92, 1], [0.84, 0.88, 0.84], [0.02, 0.0], [-0.016, 0.014], 0.24),
  },
  explain: {
    lit: [0.62, 0.7, 1.1], shade: [0.27, 0.28, 0.58], cardLit: [0.86, 0.88, 1.04], cardShade: [0.5, 0.5, 0.74],
    key: "#a9b8ff", keyI: 1.6, fog: "#141a48", fogNear: 6, fogFar: 26, bg: "#121640", glow: 1.0, sat: 0.84,
    grade: G([0.08, 0.17, 0.28, 0.55, 0.79, 0.92, 1], [0.84, 0.88, 0.84], [0.024, -0.004], [-0.008, 0.012], 0.26),
  },
  // story-vasa: under the harbour in 1961 (green-blue murk) and the museum hall (dark, warm pools of light)
  underwater: {
    lit: [0.62, 0.86, 0.9], shade: [0.26, 0.36, 0.5], cardLit: [0.8, 0.92, 0.94], cardShade: [0.46, 0.54, 0.7],
    key: "#b8e0d8", keyI: 1.4, fog: "#1f4a52", fogNear: 6, fogFar: 70, bg: "#1b4048", glow: 0.8, sat: 0.84,
    grade: G([0.08, 0.17, 0.28, 0.55, 0.79, 0.92, 1], [0.84, 0.88, 0.84], [0.0, 0.02], [0.0, 0.008], 0.26),
  },
  museum: {
    lit: [1.2, 1.0, 0.82], shade: [0.34, 0.33, 0.6], cardLit: [0.98, 0.9, 0.82], cardShade: [0.56, 0.54, 0.78],
    key: "#ffd6a0", keyI: 1.8, fog: "#23263a", fogNear: 30, fogFar: 140, bg: "#1d2034", glow: 0.9, sat: 0.84,
    grade: G([0.07, 0.16, 0.28, 0.55, 0.8, 0.93, 1], [0.84, 0.88, 0.84], [0.018, 0.0], [-0.008, 0.01], 0.24),
  },
};

export const v3 = (a: [number, number, number]) => new THREE.Vector3(...a);
