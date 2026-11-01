/**
 * Same as studio/src/core/Episode.tsx (imported pieces are the live kit), with one change:
 * the per-frame feTurbulence grain is replaced by a STATIC noise tile that is locked to the world
 * (it follows the active scene's camera at depth `grainDepth`) [POLISH_IDEAS 3a, proposal 2].
 * The encoder sees texture that moves with the picture instead of fresh noise every 2 frames.
 */
import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {AudioTrack} from '../../../studio/src/core/audio';
import {cameraAt, planeTransform} from '../../../studio/src/core/camera';
import {CaptionTrack, captionPlacement} from '../../../studio/src/core/captions';
import {waitForFonts} from '../../../studio/src/core/fonts';
import {SceneView, Vignette} from '../../../studio/src/core/SceneView';
import {parseStoryboard, sceneTimings, type Storyboard, type StoryboardInput, type SceneTiming} from '../../../studio/src/core/schema';

export type PolishProps = StoryboardInput & {grainTile?: number; grainDepth?: number};

export const PolishedEpisode: React.FC<PolishProps> = (props) => {
	waitForFonts();
	const sb = useMemo(() => parseStoryboard(props), [props]);
	const {timings, totalFrames} = useMemo(() => sceneTimings(sb), [sb]);
	const placement = useMemo(() => captionPlacement(sb.scenes, timings, sb.fps), [sb, timings]);
	const cuts = useMemo(() => timings.slice(1).map((t) => t.start / sb.fps), [timings, sb.fps]);

	return (
		<AbsoluteFill style={{background: '#000'}}>
			{sb.scenes.map((scene, i) => {
				const tm = timings[i];
				return (
					<Sequence key={`${scene.id}-${i}`} from={tm.start - tm.pre} durationInFrames={tm.frames + tm.pre + tm.post} name={scene.id}>
						<SceneView scene={scene} timing={tm} format={sb.format} theme={sb.theme} />
					</Sequence>
				);
			})}
			{sb.overlays.vignette > 0 ? <Vignette amount={sb.overlays.vignette} /> : null}
			{(props.grainTile ?? 0) > 0 ? <GrainTile sb={sb} timings={timings} amount={props.grainTile as number} depth={props.grainDepth ?? 0.6} /> : null}
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

/** Static 512 px noise tile, overlay-blended, transformed with the active scene's camera. */
const GrainTile: React.FC<{sb: Storyboard; timings: SceneTiming[]; amount: number; depth: number}> = ({sb, timings, amount, depth}) => {
	const f = useCurrentFrame();
	const {fps, width: W, height: H} = useVideoConfig();
	let i = timings.findIndex((t) => f >= t.start && f < t.start + t.frames);
	if (i < 0) i = timings.length - 1;
	const sc = sb.scenes[i];
	const t = (f - timings[i].start) / fps;
	const cam = cameraAt(sc.camera, t, W, H, sc.duration);
	const os = 0.35; // overscan so camera drift never shows an edge
	return (
		<AbsoluteFill style={{opacity: amount, mixBlendMode: 'overlay', pointerEvents: 'none', overflow: 'hidden'}}>
			<div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0', transform: planeTransform(cam, depth, W, H)}}>
				<div
					style={{
						position: 'absolute',
						left: -W * os,
						top: -H * os,
						width: W * (1 + 2 * os),
						height: H * (1 + 2 * os),
						backgroundImage: `url(${staticFile('grain512.png')})`,
						backgroundSize: '512px 512px',
						backgroundRepeat: 'repeat',
						// a different tile offset per scene, so a cut also changes the texture
						backgroundPosition: `${(i * 173) % 512}px ${(i * 311) % 512}px`,
					}}
				/>
			</div>
		</AbsoluteFill>
	);
};
