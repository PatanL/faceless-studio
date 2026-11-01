/**
 * Depth system (STYLE_BIBLE §6): N parallax planes driven by one camera.
 *
 *   <CameraProvider cam={cameraAt(...)}>
 *     <Plane preset="far"> ...svg content in frame coordinates... </Plane>
 *   </CameraProvider>
 *
 * Each plane is a full-frame div with an overscanned SVG. Per plane:
 *   depth   parallax factor (camera x/y/zoom/roll are multiplied by it)
 *   haze    0..1 mix of every engine colour toward the haze colour (done in colour math, free)
 *   desat   0..1 chroma pull (colour math, free)
 *   blur    CSS blur on the whole plane div (cheap path; never per element)
 *   fade    plane opacity
 *   gap     plane-gap drop shadow onto the plane behind (one CSS drop-shadow per plane)
 */
import React, {createContext, useContext} from 'react';
import {AbsoluteFill} from 'remotion';
import {rgba} from '../lib/color';
import {PlaneTintProvider} from '../lib/light';
import type {Cam} from '../motion/motion';
import {isOff} from '../lib/flags';

export const W = 1080;
export const H = 1920;
export const OVER = 160; // overscan px on every side (covers ±60 px moves and 10 % zoom on the fore plane)

const CamCtx = createContext<Cam>({x: 0, y: 0, zoom: 1, roll: 0});
export const CameraProvider: React.FC<{cam: Cam; children: React.ReactNode}> = ({cam, children}) => (
	<CamCtx.Provider value={cam}>{children}</CamCtx.Provider>
);
export const useCam = () => useContext(CamCtx);

export type PlaneSpec = {depth: number; haze: number; desat?: number; blur?: number; fade?: number; gap?: boolean; hazeColor?: string};

/** bible §6 presets */
export const PLANES: Record<'field' | 'far' | 'mid' | 'subject' | 'fore', PlaneSpec> = {
	field: {depth: 0.05, haze: 0},
	far: {depth: 0.3, haze: 0.62, desat: 0.15},
	mid: {depth: 0.6, haze: 0.32, desat: 0.05},
	subject: {depth: 1, haze: 0, gap: true},
	fore: {depth: 1.45, haze: 0.8, blur: 9, hazeColor: 'ink-0'},
};

export const planeTransform = (cam: Cam, d: number) => {
	const z = 1 + (cam.zoom - 1) * d;
	return `translate(${W / 2 - cam.x * d}px, ${H / 2 - cam.y * d}px) rotate(${cam.roll * d}deg) scale(${z}) translate(${-W / 2}px, ${-H / 2}px)`;
};

export const Plane: React.FC<{
	preset?: keyof typeof PLANES;
	spec?: Partial<PlaneSpec>;
	haze?: string;
	children: React.ReactNode;
	style?: React.CSSProperties;
}> = ({preset = 'subject', spec, haze = 'tide-1', children, style}) => {
	const cam = useCam();
	const s: PlaneSpec = {...PLANES[preset], ...spec};
	const filters: string[] = [];
	if (s.blur && !isOff('blur')) filters.push(`blur(${s.blur}px)`);
	if (s.gap && !isOff('gap')) filters.push(`drop-shadow(0px 8px 20px ${rgba('ink-0', 0.34)})`);
	return (
		<AbsoluteFill
			style={{
				transform: planeTransform(cam, s.depth),
				transformOrigin: '0 0',
				filter: filters.length ? filters.join(' ') : undefined,
				opacity: s.fade ?? 1,
				...style,
			}}
		>
			<PlaneTintProvider tint={{haze: s.hazeColor ?? haze, amount: s.haze, desat: s.desat ?? 0, depth: s.depth}}>
				<svg
					width={W + 2 * OVER}
					height={H + 2 * OVER}
					viewBox={`${-OVER} ${-OVER} ${W + 2 * OVER} ${H + 2 * OVER}`}
					style={{position: 'absolute', left: -OVER, top: -OVER, overflow: 'visible'}}
				>
					{children}
				</svg>
			</PlaneTintProvider>
		</AbsoluteFill>
	);
};
