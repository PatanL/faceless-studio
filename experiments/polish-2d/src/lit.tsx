/**
 * polish/Lit: any kit figure (same props as explainer/Creature) plus one scene light.
 *
 * - Rim light [POLISH_IDEAS 1a]: body minus a copy of the body shifted AWAY from the light leaves a
 *   band on the lit edge; it is filled with the light colour through an SVG mask.
 * - Form shading [POLISH_IDEAS 3c]: a gradient along the light direction, masked to the body:
 *   a cool highlight on the lit side, deep-water blue (not black or grey) on the far side.
 *
 * Extra props: light {angle (deg, direction the light TRAVELS in screen space, 90 = straight down),
 * rim (px), rimColor, rimOpacity, hi (0..1), lo (0..1), loColor}, flip (the layer's flipX, so the
 * light stays on the same screen side for mirrored figures).
 * The figure is drawn 4 times per frame (body, 2 mask silhouettes, 1 shade mask); figures are plain
 * SVG paths, so this costs little next to filters.
 */
import React, {useId} from 'react';
import type {KitComponent} from '../../../studio/src/core/registry';
import {getFigure, makeCtx, realSize} from '../../../studio/src/kits/explainer/creature';

type Light = {angle: number; rim: number; rimColor: string; rimOpacity: number; hi: number; lo: number; loColor: string};

const DEFAULT_LIGHT: Light = {angle: 80, rim: 7, rimColor: '#c9f3ff', rimOpacity: 0.75, hi: 0.16, lo: 0.42, loColor: '#03141d'};

export const Lit: KitComponent = ({props, time, width, height}) => {
	const id = 'L' + useId().replace(/[^a-zA-Z0-9_-]/g, '');
	const f = getFigure(String(props.species ?? 'orca'), typeof props.pose === 'string' ? props.pose : undefined);
	if (!f) return null;
	const light: Light = {...DEFAULT_LIGHT, ...(props.light as Partial<Light> | undefined)};
	const [bx, by, bw, bh] = f.box;

	// figure-unit size of one screen px (same sizing rules as explainer/Creature)
	const ppm = typeof props.pxPerM === 'number' ? props.pxPerM : null;
	let svgW: number;
	let svgH: number;
	let style: React.CSSProperties;
	const bottom = props.align === 'bottom';
	if (ppm) {
		const rs = realSize(f);
		svgW = rs.w * ppm;
		svgH = rs.h * ppm;
		style = {position: 'absolute', left: (width - svgW) / 2, top: bottom ? height - svgH : (height - svgH) / 2, overflow: 'visible'};
	} else {
		svgW = width;
		svgH = height;
		style = {overflow: 'visible', display: 'block'};
	}
	const upp = ppm ? bw / svgW : 1 / Math.min(width / bw, height / bh);

	// light travel direction in figure space (a flipped layer mirrors x)
	const a = (light.angle * Math.PI) / 180;
	const lx = Math.cos(a) * (props.flip ? -1 : 1);
	const ly = Math.sin(a);
	const dx = lx * light.rim * upp;
	const dy = ly * light.rim * upp;

	const body = makeCtx(props, time, `${id}b`);
	const white = {...makeCtx(props, time, `${id}w`), sil: '#ffffff'};
	const black = {...makeCtx(props, time, `${id}k`), sil: '#000000'};
	const white2 = {...makeCtx(props, time, `${id}v`), sil: '#ffffff'};
	const box = {x: bx - bw * 0.5, y: by - bh * 0.5, width: bw * 2, height: bh * 2};

	return (
		<svg
			viewBox={`${bx} ${by} ${bw} ${bh}`}
			width={svgW}
			height={svgH}
			preserveAspectRatio={bottom ? 'xMidYMax meet' : 'xMidYMid meet'}
			style={style}
		>
			<defs>
				<mask id={`${id}-rim`} maskUnits="userSpaceOnUse" {...box}>
					<g>{f.draw(white)}</g>
					<g transform={`translate(${dx} ${dy})`}>{f.draw(black)}</g>
				</mask>
				<mask id={`${id}-body`} maskUnits="userSpaceOnUse" {...box}>
					<g>{f.draw(white2)}</g>
				</mask>
				<linearGradient id={`${id}-shade`} x1={0.5 - 0.5 * lx} y1={0.5 - 0.5 * ly} x2={0.5 + 0.5 * lx} y2={0.5 + 0.5 * ly}>
					<stop offset={0} stopColor={light.rimColor} stopOpacity={light.hi} />
					<stop offset={0.42} stopColor={light.rimColor} stopOpacity={0} />
					<stop offset={0.6} stopColor={light.loColor} stopOpacity={0} />
					<stop offset={1} stopColor={light.loColor} stopOpacity={light.lo} />
				</linearGradient>
			</defs>
			{f.draw(body)}
			<rect x={bx} y={by} width={bw} height={bh} fill={`url(#${id}-shade)`} mask={`url(#${id}-body)`} />
			<rect {...box} fill={light.rimColor} opacity={light.rimOpacity} mask={`url(#${id}-rim)`} />
		</svg>
	);
};
