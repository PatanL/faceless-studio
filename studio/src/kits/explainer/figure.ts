import type React from 'react';

/** Everything a figure needs to draw one frame. */
export type DrawCtx = {
	t: number; // scene-local seconds
	p: Record<string, unknown>; // storyboard props
	id: string; // unique id prefix for gradients / clip paths
	sil?: string; // silhouette colour: draw everything flat in this colour, no details
	idle: boolean; // run the built-in idle animation (tail beat, kicks, ...)
	speed: number; // idle speed multiplier
	amp: number; // idle amplitude multiplier
};

/**
 * A drawable figure (creature, person, everyday object). Drawn in its own unit space,
 * facing RIGHT. `box` is the tight bounding box of the drawing [x, y, w, h], and
 * `size` tells how many real metres the box spans along `axis`, so figures can be
 * placed at true relative scale (see pxPerM on explainer/Creature).
 */
export type Figure = {
	label: string;
	box: [number, number, number, number];
	size: number;
	axis: 'w' | 'h';
	/** Optional alternative poses, e.g. grizzly "standing". */
	poses?: Record<string, Omit<Figure, 'poses' | 'label'>>;
	/** draws its own house shading (house/figures.tsx): the generic shade stack (house/shadeFigure.tsx) skips it */
	selfShaded?: boolean;
	draw: (c: DrawCtx) => React.ReactNode;
};

export const paint = (c: DrawCtx, color: string) => c.sil ?? color;

/** metres per drawing unit */
export const mPerUnit = (f: Pick<Figure, 'box' | 'size' | 'axis'>) => f.size / (f.axis === 'w' ? f.box[2] : f.box[3]);
