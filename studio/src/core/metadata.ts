import type {CalculateMetadataFunction} from 'remotion';
import {asset} from './registry';
import {FORMATS, parseStoryboard, sceneTimings, type StoryboardInput, type Word} from './schema';

/**
 * Size / fps / duration come from the storyboard itself, so one composition renders any
 * storyboard: `npx remotion render src/index.ts Storyboard out.mp4 --props=storyboard.json`.
 * If captions.src is set, its words are fetched (from studio/public) and merged in.
 */
export const calculateStoryboardMetadata: CalculateMetadataFunction<StoryboardInput> = async ({props}) => {
	const sb = parseStoryboard(props);
	if (sb.captions?.src) {
		const res = await fetch(asset(sb.captions.src));
		if (!res.ok) throw new Error(`captions.src ${sb.captions.src}: HTTP ${res.status}`);
		const data = (await res.json()) as {words?: Word[]} | Word[];
		const words = Array.isArray(data) ? data : (data.words ?? []);
		sb.captions = {...sb.captions, words: [...sb.captions.words, ...words], src: undefined};
	}
	const {width, height} = FORMATS[sb.format];
	const {totalFrames} = sceneTimings(sb);
	return {
		width,
		height,
		fps: sb.fps,
		durationInFrames: totalFrames,
		props: sb as StoryboardInput,
		defaultOutName: sb.id,
	};
};
