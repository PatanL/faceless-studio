// SVG React element -> canvas texture (our own code). The story lane's characters are the studio's stick-kit SVG
// components (stick/Person, stick/Turk with figureOnly); here they are rasterised every frame into a CanvasTexture
// that a flat card in the 3D world carries. Rasterising goes through an <img> decode, which is async, so the caller
// (Stage) holds the frame with delayRender until every card that changed has been redrawn.
import type React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import * as THREE from "three";

export type ViewBox = { w: number; h: number; padL?: number; padR?: number; padT?: number; padB?: number };

/** the component's own <svg viewBox="0 0 w h" width="100%" height="100%"> inside a padded outer svg of px size */
export function svgMarkup(el: React.ReactElement, vb: ViewBox, pxW: number, pxH: number): string {
  const { w, h, padL = 0, padR = 0, padT = 0, padB = 0 } = vb;
  const inner = renderToStaticMarkup(el).replace('width="100%" height="100%"', `x="0" y="0" width="${w}" height="${h}"`);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${-padL} ${-padT} ${w + padL + padR} ${h + padT + padB}" ` +
    `width="${pxW}" height="${pxH}" preserveAspectRatio="none">${inner}</svg>`;
}

export class SvgTex {
  readonly canvas: HTMLCanvasElement;
  readonly tex: THREE.CanvasTexture;
  private g: CanvasRenderingContext2D;
  private last = "";
  private baseW: number; private baseH: number; private tier = 1;
  constructor(public pxW: number, public pxH: number, readonly flip = false) {
    this.baseW = pxW; this.baseH = pxH;
    this.canvas = document.createElement("canvas");
    this.canvas.width = pxW; this.canvas.height = pxH;
    this.g = this.canvas.getContext("2d")!;
    this.tex = new THREE.CanvasTexture(this.canvas);
    this.tex.colorSpace = THREE.SRGBColorSpace;
    this.tex.anisotropy = 4;
  }
  /** face round 3: a card filling a close-up was upscaled ~3x from its 480 px raster, so every ink line went soft
   * and the grade tinted the grey edge pixels navy. Raise the raster in steps (x1..x4, never back down within a
   * mount) so a texel is no bigger than a screen pixel; the caller passes the card's height on screen in px. */
  fit(screenPxH: number) {
    const tier = Math.min(4, Math.max(1, Math.ceil(screenPxH / this.baseH - 0.15)));
    if (tier <= this.tier) return;
    this.tier = tier; this.pxW = this.baseW * tier; this.pxH = this.baseH * tier;
    this.canvas.width = this.pxW; this.canvas.height = this.pxH;
    this.g = this.canvas.getContext("2d")!;
    this.tex.dispose(); this.last = "";
  }
  /** redraw if the markup changed; resolves true when the texture was updated */
  async draw(markup: string): Promise<boolean> {
    if (markup === this.last) return false;
    this.last = markup;
    const img = new Image();
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(markup);
    await img.decode();
    const g = this.g;
    g.clearRect(0, 0, this.pxW, this.pxH);
    g.save();
    if (this.flip) { g.translate(this.pxW, 0); g.scale(-1, 1); }
    g.drawImage(img, 0, 0, this.pxW, this.pxH);
    g.restore();
    this.tex.needsUpdate = true;
    return true;
  }
}
