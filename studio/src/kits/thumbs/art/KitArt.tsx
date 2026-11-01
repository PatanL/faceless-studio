// Render a component registered by another kit (src/kits/explainer, src/kits/horror) inside
// an SVG box, so thumbnails reuse the episode art once it exists.
import React from 'react';
import {getComponent} from '../../../core/registry';

export function hasKit(name: string | undefined): boolean {
	return !!name && !!getComponent(name);
}

export const KitArt: React.FC<{
	name: string;
	props?: Record<string, unknown>;
	time?: number;
	x: number;
	y: number;
	w: number;
	h: number;
	flip?: boolean;
	rotate?: number;
}> = ({name, props = {}, time = 0, x, y, w, h, flip, rotate = 0}) => {
	const C = getComponent(name);
	if (!C) return null;
	return (
		<g transform={`rotate(${rotate} ${x + w / 2} ${y + h / 2})`}>
			<foreignObject x={x} y={y} width={w} height={h} style={{overflow: 'visible'}}>
				<div style={{width: w, height: h, transform: flip ? 'scaleX(-1)' : undefined}}>
					<C props={props} time={time} frame={Math.round(time * 30)} fps={30} width={w} height={h} sceneDuration={10} />
				</div>
			</foreignObject>
		</g>
	);
};
