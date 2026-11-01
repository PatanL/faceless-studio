import React from 'react';
import {Composition, type CalculateMetadataFunction} from 'remotion';
import {Episode} from '../../../studio/src/core/Episode';
import {calculateStoryboardMetadata} from '../../../studio/src/core/metadata';
import type {StoryboardInput} from '../../../studio/src/core/schema';
import '../../../studio/src/kits';
import {registerComponent} from '../../../studio/src/core/registry';
import orca from '../../../episodes/explainer-orca/storyboard.json';
import {Bokeh, FarPod, Halo, Haze, Light} from './fx';
import {Lit} from './lit';
import {Spring} from './spring';
import {PolishedEpisode, type PolishProps} from './PolishedEpisode';
import {polishStoryboard, type PolishOpts} from './polish';

registerComponent('polish/Lit', Lit);
registerComponent('polish/Spring', Spring);
registerComponent('polish/Light', Light);
registerComponent('polish/FarPod', FarPod);
registerComponent('polish/Haze', Haze);
registerComponent('polish/Bokeh', Bokeh);
registerComponent('polish/Halo', Halo);

// calculateStoryboardMetadata returns the zod-parsed storyboard, which drops our extra props
const calc: CalculateMetadataFunction<PolishProps> = async (args) => {
	const m = await calculateStoryboardMetadata(args as never);
	return {...m, props: {...(m.props as PolishProps), grainTile: args.props.grainTile, grainDepth: args.props.grainDepth}};
};

const AUDIO = 'polish_audio.wav';
const GRAIN = 0.1;

const variant = (opts: PolishOpts, grain: number): PolishProps => ({
	...(polishStoryboard(orca, {audioSrc: AUDIO, ...opts}) as StoryboardInput),
	grainTile: grain,
	grainDepth: 0.6,
});

/** Render with --frames=0-299: the first 10 s. The full episode stays in the props so scene timing is identical. */
const VARIANTS: Record<string, PolishProps> = {
	Polish10: variant({}, GRAIN),
	// cost attribution: the full pass minus one group
	Polish10NoLight: variant({lighting: false}, GRAIN),
	Polish10NoDepth: variant({depth: false}, GRAIN),
	Polish10NoGrain: variant({}, 0),
};

// the live kit's own Episode through this entry (base_audio.wav = mix.wav cut to 10.5 s), as a same-bundle control
const kit10 = {
	...(orca as unknown as StoryboardInput),
	audio: {...(orca as any).audio, voice: (orca as any).audio.voice.map((v: object) => ({...v, src: 'base_audio.wav'}))},
} as StoryboardInput;

export const RemotionRoot: React.FC = () => (
	<>
		{Object.entries(VARIANTS).map(([id, props]) => (
			<Composition
				key={id}
				id={id}
				component={PolishedEpisode}
				defaultProps={props}
				calculateMetadata={calc}
				width={1080}
				height={1920}
				fps={30}
				durationInFrames={300}
			/>
		))}
		<Composition
			id="Kit10"
			component={Episode}
			defaultProps={kit10}
			calculateMetadata={calculateStoryboardMetadata}
			width={1080}
			height={1920}
			fps={30}
			durationInFrames={300}
		/>
		{/* the live kit with its feTurbulence grain switched off: what the current grain costs */}
		<Composition
			id="Kit10NoGrain"
			component={Episode}
			defaultProps={{...kit10, overlays: {...(kit10 as any).overlays, grain: 0}} as StoryboardInput}
			calculateMetadata={calculateStoryboardMetadata}
			width={1080}
			height={1920}
			fps={30}
			durationInFrames={300}
		/>
	</>
);
