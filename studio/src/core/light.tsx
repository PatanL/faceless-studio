/**
 * Scene light + layer transform contexts (kit-agnostic plumbing; the explainer house style reads them).
 *
 * - SceneLightCtx: the scene's `light` spec (schema.ts SceneLight) plus scene-local time, provided by SceneView. Kits
 *   turn it into light vectors (kits/explainer/house/light.tsx), so every object in a shot is lit from one key that can
 *   sweep over the scene (STYLE_BIBLE §4.1, §9.5). Scenes without `light` provide null: kits use their default.
 * - LayerXfCtx: the layer's own mirror/rotation, provided by LayerView, so a shader can keep the light in SCREEN space
 *   (a flipX diver and a rotated orca are lit from the same side; rubric J3).
 * Horror and demo kits never read either context.
 */
import React, {createContext, useContext} from 'react';
import type {SceneLight} from './schema';

export type SceneLightState = {spec: SceneLight | null; t: number; duration: number};
const SceneLightCtx = createContext<SceneLightState>({spec: null, t: 0, duration: 1});
export const SceneLightProvider: React.FC<{value: SceneLightState; children: React.ReactNode}> = ({value, children}) => (
	<SceneLightCtx.Provider value={value}>{children}</SceneLightCtx.Provider>
);
export const useSceneLight = () => useContext(SceneLightCtx);

export type LayerXf = {flipX: boolean; rotate: number};
const LayerXfCtx = createContext<LayerXf>({flipX: false, rotate: 0});
export const LayerXfProvider: React.FC<{value: LayerXf; children: React.ReactNode}> = ({value, children}) => (
	<LayerXfCtx.Provider value={value}>{children}</LayerXfCtx.Provider>
);
export const useLayerXf = () => useContext(LayerXfCtx);
