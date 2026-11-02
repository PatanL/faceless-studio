/**
 * One light model per scene (STYLE_BIBLE §4.1) and the plane tint (§6). Components read both from context,
 * so moving the light re-shades every object in the shot, and putting an object on a far plane hazes and
 * desaturates all of its derived colours with no per-object work.
 *
 * The scene light comes from the storyboard (`scene.light`, provided by core SceneView through core/light.tsx) and
 * defaults to the Lantern setup; a <LightProvider> inside a component overrides it (engine API).
 * Ported from experiments/kurz-style/engine/src/lib/light.tsx.
 */
import React, {createContext, useContext, useMemo} from 'react';
import {useSceneLight} from '../../../core/light';
import type {SceneLight as SceneLightSpec} from '../../../core/schema';
import {c, desat, mixOk} from './color';

export type Vec = [number, number];

export type SceneLight = {
	/** unit vector TOWARD the key light, screen space (y down) */
	key: Vec;
	keyColor: string;
	/** unit vector toward the back (rim) light */
	rim: Vec;
	rimColor: string;
	ambient: string;
	/** colour bounced up from the ground/water below */
	ground: string;
	haze: string;
};

export const norm = ([x, y]: Vec): Vec => {
	const l = Math.hypot(x, y) || 1;
	return [x / l, y / l];
};

/** direction from an angle in degrees (0 = right, -90 = up) */
export const dirDeg = (deg: number): Vec => [Math.cos((deg * Math.PI) / 180), Math.sin((deg * Math.PI) / 180)];

export const LANTERN: SceneLight = {
	key: norm([-0.6, -0.8]),
	keyColor: 'amber-4',
	rim: norm([0.7, 0.7]),
	rimColor: 'tide-4',
	ambient: 'ink-2',
	ground: 'ochre-2',
	haze: 'tide-1',
};

/** bible §5.1 setups: [key angle (deg toward the key), key colour, rim angle, rim colour, ambient, ground, haze] */
const SETUPS: Record<SceneLightSpec['setup'], [number, string, number, string, string, string, string]> = {
	lantern: [-127, 'amber-4', 45, 'tide-4', 'ink-2', 'ochre-2', 'tide-1'],
	daylight: [-100, 'bone-2', 60, 'sky-3', 'dusk-2', 'ochre-2', 'sky-2'],
	cold: [-60, 'tide-4', 120, 'amber-4', 'ink-1', 'ink-3', 'ink-2'],
	stellar: [-150, 'amber-4', 30, 'tide-4', 'dusk-1', 'dusk-2', 'dusk-1'],
};

/** storyboard light spec at scene time t -> light vectors (the key sweeps `sweep` degrees across the scene) */
export const resolveLight = (spec: Partial<SceneLightSpec> | null | undefined, t = 0, duration = 1): SceneLight => {
	const [ka, kc, ra, rc, amb, gr, hz] = SETUPS[spec?.setup ?? 'lantern'];
	const sweep = spec?.sweep ?? 0;
	const u = duration > 0 ? Math.max(0, Math.min(1, t / duration)) : 0;
	const keyA = (spec?.angle ?? ka) + sweep * (u - 0.5);
	return {
		key: dirDeg(keyA),
		keyColor: spec?.keyColor ?? kc,
		rim: dirDeg(spec?.rimAngle ?? ra),
		rimColor: spec?.rimColor ?? rc,
		ambient: spec?.ambient ?? amb,
		ground: spec?.ground ?? gr,
		haze: spec?.haze ?? hz,
	};
};

const LightCtx = createContext<SceneLight | null>(null);
export const LightProvider: React.FC<{light: SceneLight; children: React.ReactNode}> = ({light, children}) => (
	<LightCtx.Provider value={light}>{children}</LightCtx.Provider>
);
export const useLight = (): SceneLight => {
	const own = useContext(LightCtx);
	const scene = useSceneLight();
	return own ?? resolveLight(scene.spec, scene.t, scene.duration);
};

// ---------------------------------------------------------------- plane tint (haze / desaturation / fade)

export type PlaneTint = {haze: string; amount: number; desat: number; depth: number};
const PlaneCtx = createContext<PlaneTint>({haze: 'tide-1', amount: 0, desat: 0, depth: 1});
export const PlaneTintProvider: React.FC<{tint: PlaneTint; children: React.ReactNode}> = ({tint, children}) => (
	<PlaneCtx.Provider value={tint}>{children}</PlaneCtx.Provider>
);
export const usePlane = () => useContext(PlaneCtx);

/** colour -> colour as it appears on the current plane (desaturate, then mix toward the haze) */
export const useTint = () => {
	const p = usePlane();
	return useMemo(() => {
		const memo = new Map<string, string>();
		return (col: string) => {
			if (p.amount <= 0 && p.desat <= 0) return c(col);
			const hit = memo.get(col);
			if (hit) return hit;
			const v = mixOk(desat(col, p.desat), p.haze, p.amount);
			memo.set(col, v);
			return v;
		};
	}, [p.amount, p.desat, p.haze]);
};
