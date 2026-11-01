// One composition per polish technique. Each = Base + one technique, so cost(technique) = time(comp) - time(Base).
import React from 'react';
import {AbsoluteFill, Composition, HtmlInCanvas, Solid, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {HtmlInCanvasMotionBlur} from '@remotion/motion-blur';
import {glow} from '@remotion/effects/glow';
import {noise} from '@remotion/effects/noise';
import {lightLeak} from '@remotion/effects/light-leak';
import {C, Caption, Creature, Far, Foreground, H, Mid, Near, Sky, W, creatureY, planeT, useCam} from './scene';

const full: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0'};
const Svg: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{...full, overflow: 'visible', ...style}}>
		{children}
	</svg>
);

/** The flat baseline: everything in one SVG plane under one camera transform. */
const Flat: React.FC<{rim?: boolean; extraBehind?: React.ReactNode}> = ({rim, extraBehind}) => {
	const cam = useCam();
	return (
		<div style={{...full, transform: planeT(cam, 1)}}>
			<Svg>
				<Sky />
				<Far />
				<Mid />
				<Near />
				{extraBehind}
				<Creature rim={rim} />
				<Foreground />
			</Svg>
		</div>
	);
};

/** 5 parallax planes, each its own composited DOM layer. blur: CSS blur px per plane (depth of field). */
const Planes: React.FC<{blur?: number[]; svgBlur?: boolean; rim?: boolean; behind?: React.ReactNode}> = ({blur = [0, 0, 0, 0, 0], svgBlur, rim, behind}) => {
	const cam = useCam();
	const planes: [number, React.ReactNode][] = [
		[0.3, <><Sky /><Far /></>],
		[0.55, <Mid />],
		[0.8, <Near />],
		[1, <>{behind}<Creature rim={rim} /></>],
		[1.4, <Foreground />],
	];
	return (
		<>
			{planes.map(([d, node], i) => (
				<div key={i} style={{...full, transform: planeT(cam, d), filter: !svgBlur && blur[i] ? `blur(${blur[i]}px)` : undefined}}>
					<Svg>
						{svgBlur && blur[i] ? (
							<>
								<filter id={`pb-${i}`} x="-10%" y="-10%" width="120%" height="120%">
									<feGaussianBlur stdDeviation={blur[i]} />
								</filter>
								<g filter={`url(#pb-${i})`}>{node}</g>
							</>
						) : (
							node
						)}
					</Svg>
				</div>
			))}
		</>
	);
};

const Rays: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<Svg style={{mixBlendMode: 'screen'}}>
			<defs>
				<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={C.ray} stopOpacity="0.45" />
					<stop offset="1" stopColor={C.ray} stopOpacity="0" />
				</linearGradient>
			</defs>
			{Array.from({length: 6}, (_, i) => {
				const x = 80 + i * 170 + Math.sin(f / 50 + i) * 30;
				return <polygon key={i} points={`${x},-50 ${x + 70},-50 ${x + 420},1500 ${x + 160},1500`} fill="url(#ray)" opacity={0.55 + 0.45 * Math.sin(f / 40 + i * 1.7)} />;
			})}
		</Svg>
	);
};

const GlowGradient: React.FC = () => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	return (
		<>
			<defs>
				<radialGradient id="halo">
					<stop offset="0" stopColor={C.glow} stopOpacity="0.65" />
					<stop offset="0.5" stopColor={C.glow} stopOpacity="0.18" />
					<stop offset="1" stopColor={C.glow} stopOpacity="0" />
				</radialGradient>
			</defs>
			<circle cx={540} cy={creatureY(f, fps)} r={420} fill="url(#halo)" style={{mixBlendMode: 'screen'}} />
		</>
	);
};

const ShadowGradient: React.FC<{blurFilter?: boolean}> = ({blurFilter}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	const lift = (1180 - creatureY(f, fps)) / 120; // 0 on the ground, 1 at the top of the jump
	const s = 1 - 0.45 * lift;
	return (
		<>
			<defs>
				<radialGradient id="shadow">
					<stop offset="0" stopColor="#081626" stopOpacity="0.7" />
					<stop offset="1" stopColor="#081626" stopOpacity="0" />
				</radialGradient>
				<filter id="shblur" x="-50%" y="-50%" width="200%" height="200%">
					<feGaussianBlur stdDeviation={18} />
				</filter>
			</defs>
			{blurFilter ? (
				<ellipse cx={540} cy={1365} rx={170 * s} ry={34 * s} fill="#081626" opacity={0.6 * s} filter="url(#shblur)" />
			) : (
				<ellipse cx={540} cy={1365} rx={210 * s} ry={46 * s} fill="url(#shadow)" opacity={s} />
			)}
		</>
	);
};

const GrainTurb: React.FC = () => {
	const f = useCurrentFrame();
	const seed = Math.floor(random(`g-${Math.floor(f / 2)}`) * 1000);
	return (
		<Svg style={{mixBlendMode: 'overlay', opacity: 0.12}}>
			<filter id="grain">
				<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={seed} stitchTiles="stitch" />
				<feColorMatrix type="saturate" values="0" />
			</filter>
			<rect width={W} height={H} filter="url(#grain)" />
		</Svg>
	);
};

const GrainTile: React.FC<{opacity?: number}> = ({opacity = 0.12}) => {
	const f = useCurrentFrame();
	const k = Math.floor(f / 2);
	return (
		<div
			style={{
				...full,
				backgroundImage: `url(${staticFile('noise.png')})`,
				backgroundRepeat: 'repeat',
				backgroundPosition: `${Math.floor(random(`gx${k}`) * 512)}px ${Math.floor(random(`gy${k}`) * 512)}px`,
				mixBlendMode: 'overlay',
				opacity,
			}}
		/>
	);
};

const GrainEffect: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<div style={{...full, mixBlendMode: 'overlay', opacity: 0.5}}>
			<Solid color="#808080" width={W} height={H} effects={[noise({amount: 0.5, seed: Math.floor(f / 2)})]} />
		</div>
	);
};

const DOTS = Array.from({length: 150}, (_, i) => ({x: random(`d-x${i}`) * W, y: random(`d-y${i}`) * H, r: 3 + random(`d-r${i}`) * 6, v: 0.3 + random(`d-v${i}`)}));
const Particles: React.FC<{n?: number}> = ({n = 150}) => {
	const f = useCurrentFrame();
	return (
		<Svg>
			{DOTS.slice(0, n).map((d, i) => (
				<circle key={i} cx={d.x + Math.sin(f / 40 + i) * 14} cy={(((d.y - f * d.v * 3) % H) + H) % H} r={d.r} fill="#e8f6ff" opacity={0.5} />
			))}
		</Svg>
	);
};

const BOKEH = Array.from({length: 40}, (_, i) => ({x: random(`b-x${i}`) * W, y: random(`b-y${i}`) * H, r: 20 + random(`b-r${i}`) * 50}));
const Bokeh: React.FC<{cssBlur?: boolean}> = ({cssBlur}) => {
	const f = useCurrentFrame();
	return (
		<Svg style={{mixBlendMode: 'screen'}}>
			<defs>
				<radialGradient id="bk">
					<stop offset="0" stopColor={C.glow} stopOpacity="0.35" />
					<stop offset="0.7" stopColor={C.glow} stopOpacity="0.12" />
					<stop offset="1" stopColor={C.glow} stopOpacity="0" />
				</radialGradient>
			</defs>
			{BOKEH.map((b, i) => (
				<circle
					key={i}
					cx={b.x + Math.sin(f / 70 + i) * 20}
					cy={b.y + Math.cos(f / 90 + i) * 20}
					r={b.r}
					fill={cssBlur ? C.glow : 'url(#bk)'}
					opacity={cssBlur ? 0.25 : 1}
					style={cssBlur ? {filter: 'blur(10px)'} : undefined}
				/>
			))}
		</Svg>
	);
};

const CausticsTurb: React.FC = () => {
	const f = useCurrentFrame();
	const layer = (id: string, dx: number, dy: number, seed: number) => (
		<Svg style={{mixBlendMode: 'screen', opacity: 0.4}}>
			<filter id={id} x="0" y="0" width="100%" height="100%">
				<feTurbulence type="turbulence" baseFrequency="0.012" numOctaves={2} seed={seed} />
				<feColorMatrix type="matrix" values="0 0 0 0 0.75  0 0 0 0 0.95  0 0 0 0 1  -10 0 0 0 1.4" />
			</filter>
			<rect x={-200 + dx} y={-200 + dy} width={W + 400} height={H + 400} filter={`url(#${id})`} />
		</Svg>
	);
	return (
		<>
			{layer('ca', Math.sin(f / 60) * 120, f * 0.8, 3)}
			{layer('cb', Math.cos(f / 70) * 120, -f * 0.6, 7)}
		</>
	);
};

const CausticsTile: React.FC = () => {
	const f = useCurrentFrame();
	const layer = (dx: number, dy: number) => (
		<div style={{...full, backgroundImage: `url(${staticFile('caustic.png')})`, backgroundRepeat: 'repeat', backgroundPosition: `${dx}px ${dy}px`, mixBlendMode: 'screen', opacity: 0.4}} />
	);
	return (
		<>
			{layer(Math.sin(f / 60) * 120, f * 0.8)}
			{layer(Math.cos(f / 70) * 120 + 250, -f * 0.6 + 170)}
		</>
	);
};

/** 512x512 source for caustic.png (rendered once as a still, then tiled). */
const CausticSource: React.FC = () => (
	<svg width={512} height={512}>
		<rect width={512} height={512} fill="black" />
		<filter id="cs" x="0" y="0" width="100%" height="100%">
			<feTurbulence type="turbulence" baseFrequency="0.0234375" numOctaves={2} seed={3} stitchTiles="stitch" />
			<feColorMatrix type="matrix" values="0 0 0 0 0.75  0 0 0 0 0.95  0 0 0 0 1  -10 0 0 0 1.4" />
		</filter>
		<rect width={512} height={512} filter="url(#cs)" />
	</svg>
);

const Leak: React.FC = () => {
	const f = useCurrentFrame();
	const {durationInFrames} = useVideoConfig();
	return (
		<div style={{...full, mixBlendMode: 'screen'}}>
			<Solid color="#000000" width={W} height={H} effects={[lightLeak({seed: 2, progress: f / durationInFrames})]} />
		</div>
	);
};

const Vignette: React.FC = () => <div style={{...full, background: 'radial-gradient(120% 85% at 50% 45%, transparent 55%, rgba(4,10,24,0.55) 100%)'}} />;

const CreatureOnly: React.FC<{rim?: boolean}> = ({rim}) => {
	const cam = useCam();
	return (
		<div style={{...full, transform: planeT(cam, 1)}}>
			<Svg>
				<Creature rim={rim} />
			</Svg>
		</div>
	);
};
const BgNoCreature: React.FC = () => {
	const cam = useCam();
	return (
		<div style={{...full, transform: planeT(cam, 1)}}>
			<Svg>
				<Sky />
				<Far />
				<Mid />
				<Near />
			</Svg>
		</div>
	);
};

const T: Record<string, React.FC> = {
	Base: () => <Flat />,
	Parallax5: () => <Planes />,
	DofCss: () => <Planes blur={[4, 2, 0, 0, 12]} />,
	DofSvg: () => <Planes blur={[4, 2, 0, 0, 12]} svgBlur />,
	Rays: () => (<><Flat /><Rays /></>),
	RimGlowGradient: () => <Flat rim extraBehind={<GlowGradient />} />,
	GlowSvgFilter: () => {
		// the creature plane gets one feGaussianBlur+merge glow filter
		const cam = useCam();
		return (
			<>
				<BgNoCreature />
				<div style={{...full, transform: planeT(cam, 1)}}>
					<Svg>
						<filter id="gl" x="-50%" y="-50%" width="200%" height="200%">
							<feGaussianBlur stdDeviation={28} result="b" />
							<feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
						</filter>
						<g filter="url(#gl)"><Creature /></g>
					</Svg>
				</div>
			</>
		);
	},
	GlowCssDropShadow: () => (
		<>
			<BgNoCreature />
			<div style={{...full, filter: `drop-shadow(0 0 40px ${C.glow})`}}><CreatureOnly /></div>
		</>
	),
	GlowEffectHtmlInCanvas: () => (
		<>
			<BgNoCreature />
			<HtmlInCanvas width={W} height={H} effects={[glow({radius: 40, intensity: 1.2, color: C.glow})]}>
				<CreatureOnly />
			</HtmlInCanvas>
		</>
	),
	ShadowGradient: () => <Flat extraBehind={<ShadowGradient />} />,
	ShadowBlurFilter: () => <Flat extraBehind={<ShadowGradient blurFilter />} />,
	GrainTurbulence: () => (<><Flat /><GrainTurb /></>),
	GrainTile: () => (<><Flat /><GrainTile /></>),
	GrainEffect: () => (<><Flat /><GrainEffect /></>),
	Particles150: () => (<><Flat /><Particles /></>),
	Bokeh40Gradient: () => (<><Flat /><Bokeh /></>),
	Bokeh40CssBlur: () => (<><Flat /><Bokeh cssBlur /></>),
	CausticsTurbulence: () => (<><Flat /><CausticsTurb /></>),
	CausticsTile: () => (<><Flat /><CausticsTile /></>),
	LightLeakEffect: () => (<><Flat /><Leak /></>),
	MotionBlurCreature: () => (
		<>
			<BgNoCreature />
			<HtmlInCanvasMotionBlur width={W} height={H} samples={6} shutterAngle={180}>
				<CreatureOnly />
			</HtmlInCanvasMotionBlur>
		</>
	),
	GradeCssFilter: () => (
		<div style={{...full, filter: 'brightness(1.05) contrast(1.1) saturate(1.15)'}}>
			<Flat />
		</div>
	),
	VignetteGradient: () => (<><Flat /><Vignette /></>),
	MotionBlurPlainChild: () => (
		<>
			<BgNoCreature />
			<HtmlInCanvasMotionBlur width={W} height={H} samples={6} shutterAngle={180}>
				<Svg>
					<Creature />
				</Svg>
			</HtmlInCanvasMotionBlur>
		</>
	),
	KurzStack: () => (
		<>
			<Planes blur={[3, 1.5, 0, 0, 10]} rim behind={<><GlowGradient /><ShadowGradient /></>} />
			<Rays />
			<Bokeh />
			<Particles n={80} />
			<Vignette />
			<GrainTile opacity={0.1} />
		</>
	),
	KurzStackNoGrain: () => (
		<>
			<Planes blur={[3, 1.5, 0, 0, 10]} rim behind={<><GlowGradient /><ShadowGradient /></>} />
			<Rays />
			<Bokeh />
			<Particles n={80} />
			<Vignette />
		</>
	),
};

export const Root: React.FC = () => (
	<>
		{Object.entries(T).map(([id, Body]) => (
			<Composition
				key={id}
				id={id}
				width={W}
				height={H}
				fps={30}
				durationInFrames={450}
				component={() => (
					<AbsoluteFill style={{background: C.sky0, overflow: 'hidden'}}>
						<Body />
						<Caption />
					</AbsoluteFill>
				)}
			/>
		))}
		<Composition id="CausticSource" width={512} height={512} fps={30} durationInFrames={1} component={CausticSource} />
	</>
);

