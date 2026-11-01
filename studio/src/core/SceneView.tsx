import React from 'react';
import {AbsoluteFill, Img, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {cameraAt, planeTransform, shakeAt} from './camera';
import {CalloutView} from './callouts';
import {LayerView, type LayerCtx} from './layers';
import {asset, getComponent, MissingComponent} from './registry';
import type {Background, Format, Scene, SceneTiming, Theme} from './schema';
import {transitionLook} from './transitions';

const plane: React.CSSProperties = {position: 'absolute', left: 0, top: 0, transformOrigin: '0 0'};

export const SceneView: React.FC<{
	scene: Scene;
	timing: SceneTiming;
	format: Format;
	theme: Theme;
}> = ({scene, timing, format, theme}) => {
	const f = useCurrentFrame();
	const {fps, width: W, height: H} = useVideoConfig();
	const localFrame = f - timing.pre;
	const t = localFrame / fps;
	const seed = `${scene.id}-${timing.index}`;

	const cam = cameraAt(scene.camera, t, W, H, scene.duration);
	const shake = shakeAt(scene.camera, t, seed);
	const look = transitionLook(timing, f, W, H, `s${timing.index}`);

	const ctx: LayerCtx = {t, fps, W, H, sceneDuration: scene.duration, theme, seed};
	const layers = scene.layers
		.map((l, i) => ({l, i}))
		.sort((a, b) => a.l.z - b.l.z || a.i - b.i);

	const g = scene.grade;
	let gradeFilter: string | undefined;
	if (g) {
		let b = g.brightness;
		if (g.flicker > 0) {
			const step = Math.floor(localFrame / 2);
			const r = random(`${seed}-flk-${step}`);
			// mostly steady, occasional dips
			b *= 1 - g.flicker * (r > 0.85 ? 0.6 * random(`${seed}-flk2-${step}`) : 0.08 * r);
		}
		gradeFilter = `brightness(${b}) contrast(${g.contrast}) saturate(${g.saturate}) hue-rotate(${g.hue}deg)`;
	}

	return (
		<AbsoluteFill style={{overflow: 'hidden', ...look.style}}>
			{look.filter ? (
				<svg width={0} height={0} style={{position: 'absolute'}}>
					<defs>{look.filter}</defs>
				</svg>
			) : null}
			{/* world: background + layers, camera + shake + grade */}
			<AbsoluteFill
				style={{
					transform: `translate(${shake.dx}px, ${shake.dy}px) rotate(${shake.rotate}deg)`,
					filter: gradeFilter,
				}}
			>
				<div style={{...plane, width: W, height: H, transform: planeTransform(cam, scene.background.depth, W, H)}}>
					<BackgroundView bg={scene.background} W={W} H={H} t={t} fps={fps} dur={scene.duration} />
				</div>
				{layers.map(({l, i}) => (
					<div key={l.id ?? i} style={{...plane, width: W, height: H, transform: planeTransform(cam, l.depth, W, H)}}>
						<LayerView layer={l} ctx={ctx} index={i} />
					</div>
				))}
			</AbsoluteFill>
			{g?.tint ? <AbsoluteFill style={{background: g.tint, opacity: g.tintOpacity, mixBlendMode: 'multiply'}} /> : null}
			{g && g.vignette > 0 ? <Vignette amount={g.vignette} /> : null}
			{/* screen space */}
			{scene.callouts.map((c, i) => (
				<CalloutView key={i} c={c} t={t} sceneDuration={scene.duration} W={W} H={H} format={format} theme={theme} />
			))}
			{look.flash > 0 ? <AbsoluteFill style={{background: '#fff', opacity: look.flash}} /> : null}
			{look.black > 0 ? <AbsoluteFill style={{background: '#000', opacity: look.black}} /> : null}
		</AbsoluteFill>
	);
};

export const Vignette: React.FC<{amount: number}> = ({amount}) => (
	<AbsoluteFill
		style={{
			background: `radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 45%, rgba(0,0,0,${0.85 * amount}) 100%)`,
		}}
	/>
);

const BackgroundView: React.FC<{bg: Background; W: number; H: number; t: number; fps: number; dur: number}> = ({
	bg,
	W,
	H,
	t,
	fps,
	dur,
}) => {
	const os = bg.overscan;
	const bw = W * os;
	const bh = H * os;
	const box: React.CSSProperties = {position: 'absolute', left: (W - bw) / 2, top: (H - bh) / 2, width: bw, height: bh};
	switch (bg.type) {
		case 'color':
			return <div style={{...box, background: bg.color}} />;
		case 'gradient': {
			const stops = bg.colors.join(', ');
			const css =
				bg.kind === 'radial'
					? `radial-gradient(ellipse at 50% 40%, ${stops})`
					: `linear-gradient(${bg.angle}deg, ${stops})`;
			return <div style={{...box, background: css}} />;
		}
		case 'image':
			return <Img src={asset(bg.src)} style={{...box, objectFit: bg.fit}} />;
		case 'component': {
			const C = getComponent(bg.name);
			return (
				<div style={box}>
					{C ? (
						<C props={bg.props} time={t} frame={Math.round(t * fps)} fps={fps} width={bw} height={bh} sceneDuration={dur} />
					) : (
						<MissingComponent name={bg.name} />
					)}
				</div>
			);
		}
	}
};
