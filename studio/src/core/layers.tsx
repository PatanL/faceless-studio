import React from 'react';
import {Img, random} from 'remotion';
import {enterExit, idleAt, px, sample, sortByT} from './anim';
import {asset, getComponent, MissingComponent} from './registry';
import type {Layer, Theme} from './schema';
import {fontFamily} from './fonts';

export type LayerCtx = {
	t: number; // scene-local seconds
	fps: number;
	W: number;
	H: number;
	sceneDuration: number;
	theme: Theme;
	seed: string;
};

export const LayerView: React.FC<{layer: Layer; ctx: LayerCtx; index: number}> = ({layer, ctx, index}) => {
	const {t, W, H} = ctx;
	const start = layer.start ?? -Infinity;
	const end = layer.end ?? Infinity;
	if (t < start || t >= end) return null;

	const kfs = sortByT(layer.keyframes);
	const x = sample(kfs, 'x', t, px(layer.x, W, W / 2), (v) => px(v as never, W));
	const y = sample(kfs, 'y', t, px(layer.y, H, H / 2), (v) => px(v as never, H));
	const scale = sample(kfs, 'scale', t, layer.scale);
	const sx = sample(kfs, 'scaleX', t, 1);
	const sy = sample(kfs, 'scaleY', t, 1);
	const rotate = sample(kfs, 'rotate', t, layer.rotate);
	const opacity = sample(kfs, 'opacity', t, layer.opacity);

	const ee = enterExit(
		t,
		layer.enter,
		layer.exit,
		Number.isFinite(start) ? start : 0,
		Number.isFinite(end) ? end : ctx.sceneDuration,
	);
	const idle = idleAt(layer.idle, t, `${ctx.seed}-${layer.id ?? index}`);

	// Component layers without a size get the full frame so kits always receive a box.
	const w = layer.width !== undefined ? px(layer.width, W) : layer.type === 'component' ? W : undefined;
	const h = layer.height !== undefined ? px(layer.height, H) : layer.type === 'component' ? H : undefined;
	const ax = layer.anchorX;
	const ay = layer.anchorY;
	const fx = layer.flipX ? -1 : 1;
	const finalOpacity = opacity * ee.opacity;
	if (finalOpacity <= 0.001) return null;

	const filters: string[] = [];
	if (layer.blur) filters.push(`blur(${layer.blur}px)`);
	if (layer.shadow) filters.push(`drop-shadow(${layer.shadow})`);

	const style: React.CSSProperties = {
		position: 'absolute',
		left: x,
		top: y,
		width: w,
		height: h,
		opacity: finalOpacity,
		transformOrigin: `${ax * 100}% ${ay * 100}%`,
		transform: [
			`translate(${-ax * 100}%, ${-ay * 100}%)`,
			`translate(${ee.dx + idle.dx}px, ${ee.dy + idle.dy}px)`,
			`rotate(${rotate + idle.rotate}deg)`,
			`scale(${scale * ee.scale * sx * idle.sx * fx}, ${scale * ee.scale * sy * idle.sy})`,
		].join(' '),
		filter: filters.length ? filters.join(' ') : undefined,
		mixBlendMode: layer.blend as React.CSSProperties['mixBlendMode'],
		clipPath: ee.clip,
	};

	return <div style={style}>{renderBody(layer, ctx, w ?? 0, h ?? 0)}</div>;
};

function renderBody(layer: Layer, ctx: LayerCtx, w: number, h: number): React.ReactNode {
	switch (layer.type) {
		case 'rect':
			return (
				<div
					style={{
						width: '100%',
						height: '100%',
						background: layer.fill,
						borderRadius: layer.radius,
						boxSizing: 'border-box',
						border: layer.stroke ? `${layer.strokeWidth}px solid ${layer.stroke}` : undefined,
					}}
				/>
			);
		case 'circle':
			return (
				<div
					style={{
						width: '100%',
						height: '100%',
						background: layer.fill,
						borderRadius: '50%',
						boxSizing: 'border-box',
						border: layer.stroke ? `${layer.strokeWidth}px solid ${layer.stroke}` : undefined,
					}}
				/>
			);
		case 'text': {
			let text = layer.uppercase ? layer.text.toUpperCase() : layer.text;
			if (layer.typewriter) {
				const n = Math.max(0, Math.floor((ctx.t - layer.typewriter.at) * layer.typewriter.cps));
				text = text.slice(0, n);
			}
			return (
				<div
					style={{
						fontFamily: fontFamily(layer.font, ctx.theme),
						fontWeight: layer.weight,
						fontSize: layer.fontSize,
						color: layer.color,
						textAlign: layer.align,
						lineHeight: layer.lineHeight,
						letterSpacing: `${layer.letterSpacing}em`,
						maxWidth: layer.maxWidth,
						width: layer.maxWidth ? 'max-content' : undefined,
						whiteSpace: layer.maxWidth ? 'normal' : 'pre',
						WebkitTextStroke: layer.strokeWidth ? `${layer.strokeWidth}px ${layer.strokeColor ?? '#000'}` : undefined,
						paintOrder: 'stroke fill',
						background: layer.background,
						padding: layer.padding,
						borderRadius: layer.radius,
					}}
				>
					{text}
				</div>
			);
		}
		case 'image':
			return (
				<Img
					src={asset(layer.src)}
					style={{width: '100%', height: '100%', objectFit: layer.fit, display: 'block'}}
				/>
			);
		case 'svg':
			if (layer.src) {
				return <Img src={asset(layer.src)} style={{width: '100%', height: '100%', display: 'block'}} />;
			}
			return <SvgMarkup markup={layer.markup ?? ''} />;
		case 'particles':
			return <Particles layer={layer} ctx={ctx} w={w || ctx.W} h={h || ctx.H} />;
		case 'component': {
			const C = getComponent(layer.name);
			if (!C) return <MissingComponent name={layer.name} />;
			return (
				<C
					props={layer.props}
					time={ctx.t}
					frame={Math.round(ctx.t * ctx.fps)}
					fps={ctx.fps}
					width={w}
					height={h}
					sceneDuration={ctx.sceneDuration}
				/>
			);
		}
	}
}

/** Inline SVG markup scaled to fill the layer box. */
export const SvgMarkup: React.FC<{markup: string}> = ({markup}) => {
	const html = markup.replace(/<svg\b/, '<svg width="100%" height="100%" preserveAspectRatio="xMidYMid meet"');
	return <div style={{width: '100%', height: '100%'}} dangerouslySetInnerHTML={{__html: html}} />;
};

// ---------------------------------------------------------------- particles

type ParticleLayer = Extract<Layer, {type: 'particles'}>;

const PRESETS: Record<
	ParticleLayer['preset'],
	{vx: number; vy: number; size: [number, number]; color: string; wobble: number; twinkle: boolean}
> = {
	bubbles: {vx: 0, vy: -110, size: [6, 26], color: 'rgba(200,240,255,0.55)', wobble: 18, twinkle: false},
	dust: {vx: 12, vy: -8, size: [2, 6], color: 'rgba(255,255,255,0.35)', wobble: 10, twinkle: true},
	snow: {vx: 20, vy: 90, size: [3, 9], color: 'rgba(255,255,255,0.85)', wobble: 24, twinkle: false},
	embers: {vx: 10, vy: -140, size: [2, 7], color: 'rgba(255,150,60,0.9)', wobble: 20, twinkle: true},
	rain: {vx: -120, vy: 1500, size: [2, 3], color: 'rgba(190,210,255,0.45)', wobble: 0, twinkle: false},
	stars: {vx: 0, vy: 0, size: [1.5, 4], color: 'rgba(255,255,255,0.9)', wobble: 0, twinkle: true},
};

const Particles: React.FC<{layer: ParticleLayer; ctx: LayerCtx; w: number; h: number}> = ({layer, ctx, w, h}) => {
	const pr = PRESETS[layer.preset];
	const [smin, smax] = layer.size ?? pr.size;
	const color = layer.color ?? pr.color;
	const margin = 40;
	const t = ctx.t + 20; // start "mid-flight" so the frame is already populated at t=0
	const items: React.ReactNode[] = [];
	for (let i = 0; i < layer.count; i++) {
		const r = (k: string) => random(`p-${layer.seed}-${i}-${k}`);
		const size = smin + (smax - smin) * r('s');
		const speed = layer.speed * (0.5 + r('v')) * (0.6 + size / smax / 2);
		const spanW = w + margin * 2;
		const spanH = h + margin * 2;
		let x = r('x') * spanW + pr.vx * speed * t + Math.sin(t * (0.6 + r('wf')) + r('wp') * 6.28) * pr.wobble;
		let y = r('y') * spanH + pr.vy * speed * t;
		x = (((x % spanW) + spanW) % spanW) - margin;
		y = (((y % spanH) + spanH) % spanH) - margin;
		const tw = pr.twinkle ? 0.45 + 0.55 * Math.abs(Math.sin(t * (1 + r('tf') * 2) + r('tp') * 6.28)) : 1;
		if (layer.preset === 'rain') {
			items.push(
				<line key={i} x1={x} y1={y} x2={x + pr.vx * 0.02} y2={y + 46} stroke={color} strokeWidth={size} strokeLinecap="round" />,
			);
		} else if (layer.preset === 'bubbles') {
			items.push(
				<g key={i} opacity={tw}>
					<circle cx={x} cy={y} r={size / 2} fill="none" stroke={color} strokeWidth={Math.max(1.5, size / 9)} />
					<circle cx={x - size * 0.17} cy={y - size * 0.17} r={size * 0.1} fill={color} />
				</g>,
			);
		} else {
			items.push(<circle key={i} cx={x} cy={y} r={size / 2} fill={color} opacity={tw} />);
		}
	}
	return (
		<svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} style={{display: 'block', overflow: 'visible'}}>
			{items}
		</svg>
	);
};
