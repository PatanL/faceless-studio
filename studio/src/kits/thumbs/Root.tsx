// Separate Remotion root for thumbnails (keeps src/Root.tsx untouched).
// `Thumb` takes a ThumbSpec as props; size comes from spec.format (16:9 -> 1280x720, 9:16 -> 1080x1920).
import React from 'react';
import {Composition, Still} from 'remotion';
import {Thumbnail} from './Thumbnail';
import {SIZES, TEMPLATES, type ThumbSpec} from './spec';
import samples from './samples/samples.json';

const sampleSpecs = samples as unknown as ThumbSpec[];

export const ThumbRoot: React.FC = () => (
	<>
		<Composition
			id="Thumb"
			component={Thumbnail as React.FC<any>}
			durationInFrames={1}
			fps={30}
			width={1280}
			height={720}
			defaultProps={sampleSpecs[0] as any}
			calculateMetadata={({props}) => {
				const s = SIZES[((props as ThumbSpec).format ?? '16:9') as keyof typeof SIZES] ?? SIZES['16:9'];
				return {width: s.width, height: s.height};
			}}
		/>
		{/* one Still per sample/template/format, for browsing in `remotion studio` */}
		{(Object.keys(TEMPLATES) as (keyof typeof TEMPLATES)[]).flatMap((niche) =>
			TEMPLATES[niche].flatMap((t) => {
				const spec = sampleSpecs.find((s) => s.niche === niche && s.template === t) ?? {niche, template: t, text: 'SAMPLE TEXT'};
				return (['16:9', '9:16'] as const).map((f) => (
					<Still
						key={`${niche}-${t}-${f}`}
						id={`thumb-${niche}-${t}-${f === '16:9' ? 'h' : 'v'}`}
						component={Thumbnail as React.FC<any>}
						width={SIZES[f].width}
						height={SIZES[f].height}
						defaultProps={{...spec, format: f} as any}
					/>
				));
			}),
		)}
	</>
);
