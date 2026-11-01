import React from 'react';
import {staticFile} from 'remotion';

/**
 * Kit component registry. Kits call registerComponent('explainer/Whale', Whale) at import
 * time (see src/kits/index.ts); storyboards reference them with
 * {"type": "component", "name": "explainer/Whale", "props": {...}} as a layer or background.
 */
export type KitComponentProps = {
	/** Free-form props from the storyboard JSON. */
	props: Record<string, unknown>;
	/** Scene-local time in seconds (negative during an incoming transition). */
	time: number;
	/** Scene-local frame. */
	frame: number;
	fps: number;
	/** Layer box size in px (frame size for backgrounds). */
	width: number;
	height: number;
	sceneDuration: number;
};

export type KitComponent = React.FC<KitComponentProps>;

const registry = new Map<string, KitComponent>();

export function registerComponent(name: string, component: KitComponent) {
	registry.set(name, component);
}

export function getComponent(name: string): KitComponent | undefined {
	return registry.get(name);
}

export function listComponents(): string[] {
	return [...registry.keys()].sort();
}

export const MissingComponent: React.FC<{name: string}> = ({name}) => (
	<div
		style={{
			width: '100%',
			height: '100%',
			minWidth: 200,
			minHeight: 120,
			border: '6px dashed #ff00ff',
			color: '#ff00ff',
			fontFamily: 'monospace',
			fontSize: 28,
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'center',
			background: 'rgba(255,0,255,0.12)',
		}}
	>
		missing: {name}
	</div>
);

/** Paths are relative to studio/public unless they are absolute URLs. */
export const asset = (src: string) =>
	/^(https?:|data:|blob:)/.test(src) ? src : staticFile(src.replace(/^\/+/, ''));
