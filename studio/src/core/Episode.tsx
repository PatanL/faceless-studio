import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {AudioTrack} from './audio';
import {CaptionTrack, captionPlacement} from './captions';
import {waitForFonts} from './fonts';
import {SceneView, Vignette} from './SceneView';
import {parseStoryboard, sceneTimings, StoryboardSchema, type StoryboardInput} from './schema';

/** Renders any storyboard. Props are the storyboard JSON itself. */
export const Episode: React.FC<StoryboardInput> = (props) => {
	waitForFonts();
	const sb = useMemo(() => parseStoryboard(props), [props]);
	const {timings, totalFrames} = useMemo(() => sceneTimings(sb), [sb]);
	// per-scene caption y (global seconds), for scenes whose framing needs the caption moved off phone text
	const placement = useMemo(() => captionPlacement(sb.scenes, timings, sb.fps), [sb, timings]);
	// scene cuts (global seconds): a caption page never runs across one
	const cuts = useMemo(() => timings.slice(1).map((t) => t.start / sb.fps), [timings, sb.fps]);

	return (
		<AbsoluteFill style={{background: '#000'}}>
			{sb.scenes.map((scene, i) => {
				const tm = timings[i];
				return (
					<Sequence
						key={`${scene.id}-${i}`}
						from={tm.start - tm.pre}
						durationInFrames={tm.frames + tm.pre + tm.post}
						name={scene.id}
					>
						<SceneView scene={scene} timing={tm} format={sb.format} theme={sb.theme} />
					</Sequence>
				);
			})}
			{sb.overlays.vignette > 0 ? <Vignette amount={sb.overlays.vignette} /> : null}
			{sb.overlays.grain > 0 ? <Grain amount={sb.overlays.grain} /> : null}
			{sb.captions ? <CaptionTrack captions={sb.captions} format={sb.format} theme={sb.theme} placement={placement} cuts={cuts} /> : null}
			<Fades fadeIn={sb.overlays.fadeIn} fadeOut={sb.overlays.fadeOut} totalFrames={totalFrames} />
			<AudioTrack sb={sb} timings={timings} totalFrames={totalFrames} />
		</AbsoluteFill>
	);
};

const Fades: React.FC<{fadeIn: number; fadeOut: number; totalFrames: number}> = ({fadeIn, fadeOut, totalFrames}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	let o = 0;
	if (fadeIn > 0) o = Math.max(o, interpolate(f, [0, fadeIn * fps], [1, 0], {extrapolateRight: 'clamp'}));
	if (fadeOut > 0)
		o = Math.max(o, interpolate(f, [totalFrames - 1 - fadeOut * fps, totalFrames - 1], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
	return o > 0 ? <AbsoluteFill style={{background: '#000', opacity: o}} /> : null;
};

const Grain: React.FC<{amount: number}> = ({amount}) => {
	const f = useCurrentFrame();
	const seed = Math.floor(random(`grain-${Math.floor(f / 2)}`) * 1000);
	return (
		<AbsoluteFill style={{opacity: 0.18 * amount, mixBlendMode: 'overlay', pointerEvents: 'none'}}>
			<svg width="100%" height="100%">
				<filter id="grain-f">
					<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} stitchTiles="stitch" />
					<feColorMatrix type="saturate" values="0" />
				</filter>
				<rect width="100%" height="100%" filter="url(#grain-f)" />
			</svg>
		</AbsoluteFill>
	);
};

export {StoryboardSchema};
