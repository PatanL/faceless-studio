/**
 * Pure path geometry for the detail generators: flatten engine-style paths (absolute M L C Q Z only) to
 * polygons, test points against them (even-odd) and measure them. Pure JS, so the same code runs inside the
 * Remotion render and in the node manifest script (scripts/manifest.ts) that counts what the frame holds.
 */
export type Pt = [number, number];
export type Poly = Pt[];

const TOK = /[MLCQZ]|-?\d*\.?\d+(?:e-?\d+)?/gi;

/** Absolute M/L/C/Q/Z path -> list of closed polygons (curves sampled). */
export const flatten = (d: string, steps = 8): Poly[] => {
	const toks = d.match(TOK) ?? [];
	const polys: Poly[] = [];
	let cur: Poly = [];
	let i = 0;
	let cmd = 'M';
	let p: Pt = [0, 0];
	const num = () => +toks[i++];
	while (i < toks.length) {
		const tk = toks[i];
		if (/[MLCQZ]/i.test(tk)) {
			cmd = tk.toUpperCase();
			i++;
			if (cmd === 'Z') {
				if (cur.length > 2) polys.push(cur);
				cur = [];
				continue;
			}
		}
		if (cmd === 'M') {
			if (cur.length > 2) polys.push(cur);
			p = [num(), num()];
			cur = [p];
			cmd = 'L';
		} else if (cmd === 'L') {
			p = [num(), num()];
			cur.push(p);
		} else if (cmd === 'C') {
			const a: Pt = [num(), num()];
			const b: Pt = [num(), num()];
			const e: Pt = [num(), num()];
			for (let s = 1; s <= steps; s++) {
				const t = s / steps;
				const u = 1 - t;
				cur.push([
					u * u * u * p[0] + 3 * u * u * t * a[0] + 3 * u * t * t * b[0] + t * t * t * e[0],
					u * u * u * p[1] + 3 * u * u * t * a[1] + 3 * u * t * t * b[1] + t * t * t * e[1],
				]);
			}
			p = e;
		} else if (cmd === 'Q') {
			const a: Pt = [num(), num()];
			const e: Pt = [num(), num()];
			for (let s = 1; s <= steps; s++) {
				const t = s / steps;
				const u = 1 - t;
				cur.push([u * u * p[0] + 2 * u * t * a[0] + t * t * e[0], u * u * p[1] + 2 * u * t * a[1] + t * t * e[1]]);
			}
			p = e;
		} else {
			i++; // unknown token: skip
		}
	}
	if (cur.length > 2) polys.push(cur);
	return polys;
};

/** even-odd point-in-polygons */
export const inside = (polys: Poly[], x: number, y: number): boolean => {
	let c = false;
	for (const poly of polys) {
		for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
			const [xi, yi] = poly[i];
			const [xj, yj] = poly[j];
			if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c;
		}
	}
	return c;
};

export const polysBox = (polys: Poly[]): [number, number, number, number] => {
	let x0 = Infinity;
	let y0 = Infinity;
	let x1 = -Infinity;
	let y1 = -Infinity;
	for (const p of polys)
		for (const [x, y] of p) {
			x0 = Math.min(x0, x);
			y0 = Math.min(y0, y);
			x1 = Math.max(x1, x);
			y1 = Math.max(y1, y);
		}
	return [x0, y0, x1 - x0, y1 - y0];
};

/** polygon -> absolute path string */
export const polyPath = (poly: Pt[], close = true): string =>
	`M ${poly.map(([x, y]) => `${x.toFixed(1)} ${y.toFixed(1)}`).join(' L ')}${close ? ' Z' : ''}`;

/** shrink a polygon toward its centroid by a fixed distance (approx., for convex-ish cells) */
export const inset = (poly: Pt[], d: number): Pt[] => {
	const cx = poly.reduce((a, p) => a + p[0], 0) / poly.length;
	const cy = poly.reduce((a, p) => a + p[1], 0) / poly.length;
	return poly.map(([x, y]) => {
		const l = Math.hypot(x - cx, y - cy) || 1;
		const k = Math.max(0, (l - d) / l);
		return [cx + (x - cx) * k, cy + (y - cy) * k];
	});
};

export const centroid = (poly: Pt[]): Pt => [poly.reduce((a, p) => a + p[0], 0) / poly.length, poly.reduce((a, p) => a + p[1], 0) / poly.length];

/** scale a polygon about its centroid */
export const scalePoly = (poly: Pt[], k: number, o?: Pt): Pt[] => {
	const [cx, cy] = o ?? centroid(poly);
	return poly.map(([x, y]) => [cx + (x - cx) * k, cy + (y - cy) * k]);
};

/** rotate a point about a pivot, degrees */
export const rotAbout = (px: number, py: number, deg: number) => {
	const a = (deg * Math.PI) / 180;
	const ca = Math.cos(a);
	const sa = Math.sin(a);
	return (x: number, y: number): Pt => [px + (x - px) * ca - (y - py) * sa, py + (x - px) * sa + (y - py) * ca];
};
