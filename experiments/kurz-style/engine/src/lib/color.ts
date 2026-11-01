/**
 * Palette tokens + OKLab colour math (STYLE_BIBLE §2). Every derived colour in the engine is an OKLab mix
 * of house tokens, never a free pick.
 *
 *   c('tide-3')                 -> '#35cbd0'   (a raw '#rrggbb' passes through)
 *   mixOk(a, b, t)              -> OKLab lerp, gamut-clipped to sRGB
 *   shadowOf(base, ambient, t)  -> mix toward the ambient that is guaranteed to get darker (dark bases too)
 *   shiftL(c, dL)               -> lighter/darker in OKLab L, same hue (micro-marks)
 *   desat(c, s)                 -> pull chroma toward 0 by s (0..1)
 */
import palette from '../../../house/palette.json';

type Ramp = {token: string; hex: string}[];
const TOKENS: Record<string, string> = {};
for (const ramp of Object.values((palette as unknown as {ramps: Record<string, Ramp>}).ramps)) {
	for (const t of ramp) TOKENS[t.token] = t.hex;
}

export const c = (tok: string): string => {
	if (tok.startsWith('#')) return tok;
	const v = TOKENS[tok];
	if (!v) throw new Error(`unknown palette token ${tok}`);
	return v;
};

type Lab = [number, number, number];

const toLin = (v: number) => (v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
const toSrgb = (v: number) => (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055);

const cache = new Map<string, Lab>();
export function hexToLab(hex: string): Lab {
	const h = c(hex);
	const hit = cache.get(h);
	if (hit) return hit;
	const n = parseInt(h.slice(1, 7), 16);
	const r = toLin(((n >> 16) & 255) / 255);
	const g = toLin(((n >> 8) & 255) / 255);
	const b = toLin((n & 255) / 255);
	const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
	const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
	const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
	const lab: Lab = [
		0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
		1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
		0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s,
	];
	cache.set(h, lab);
	return lab;
}

export function labToHex([L, A, B]: Lab): string {
	const l = Math.pow(L + 0.3963377774 * A + 0.2158037573 * B, 3);
	const m = Math.pow(L - 0.1055613458 * A - 0.0638541728 * B, 3);
	const s = Math.pow(L - 0.0894841775 * A - 1.291485548 * B, 3);
	const rgb = [
		4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
		-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
		-0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s,
	];
	return (
		'#' +
		rgb
			.map((v) => Math.round(Math.max(0, Math.min(1, toSrgb(Math.max(0, v)))) * 255))
			.map((v) => v.toString(16).padStart(2, '0'))
			.join('')
	);
}

export const mixOk = (a: string, b: string, t: number): string => {
	if (t <= 0) return c(a);
	if (t >= 1) return c(b);
	const x = hexToLab(a);
	const y = hexToLab(b);
	return labToHex([x[0] + (y[0] - x[0]) * t, x[1] + (y[1] - x[1]) * t, x[2] + (y[2] - x[2]) * t]);
};

export const lum = (a: string) => hexToLab(a)[0];

/** L shift in OKLab units (0.06-0.10 = the bible's micro-mark range). */
export const shiftL = (a: string, dL: number): string => {
	const [L, A, B] = hexToLab(a);
	return labToHex([Math.max(0.12, Math.min(0.98, L + dL)), A, B]);
};

export const desat = (a: string, s: number): string => {
	if (s <= 0) return c(a);
	const [L, A, B] = hexToLab(a);
	return labToHex([L, A * (1 - s), B * (1 - s)]);
};

/**
 * Shadow colour = mix(base, ambient, t) (bible §2.3), but always darker than the base: for a base that is
 * already darker than the ambient (an orca's black skin under ink-2) the mix would lighten it, so L is
 * forced down by ~0.45·t while keeping the ambient's hue pull. Floor L 0.13 (no black: ink-0 is L 0.17).
 */
export const shadowOf = (base: string, ambient: string, t: number): string => {
	const m = mixOk(base, ambient, t);
	const Lb = lum(base);
	const want = Lb - 0.45 * t;
	const [L, A, B] = hexToLab(m);
	if (L <= Lb - 0.3 * t) return m;
	return labToHex([Math.max(0.13, Math.min(L, want)), A, B]);
};

/** rgba() string of a token/hex with alpha. */
export const rgba = (a: string, alpha: number): string => {
	const n = parseInt(c(a).slice(1, 7), 16);
	return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${alpha})`;
};
