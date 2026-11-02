/**
 * The house look switch (docs/HOUSE_STYLE.md). One place decides how every kit piece is drawn:
 *
 *   'A'        house style A (owner pick, 2026-11-01; reference experiments/asset-gen/gen/style_board_A.png): flat 2D,
 *              each shape one solid colour, one flat shadow shape per object, a few small glints, 3-5 flat depth
 *              layers (no haze gradients, no blur), flat water bands with hard-edged translucent rays.
 *   'lantern'  the previous Lantern & Ink stack (form gradients, rim, bounce, stipple, micro-marks, haze, bokeh). The
 *              code stays in place; set LOOK = 'lantern' (and palette.ts PALETTE = 'lantern') to switch back.
 */
export type Look = 'A' | 'lantern';
export const LOOK: Look = 'A';
/** true when the flat style-A look is on */
export const FLAT = LOOK === 'A';
