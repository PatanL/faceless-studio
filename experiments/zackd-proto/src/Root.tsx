import React from 'react';
import {Composition} from 'remotion';
import {Proto, ProtoProps} from './Proto';
import {DURATION_FRAMES, FPS} from './timeline';

export const Root: React.FC = () => (
	<Composition
		id="ZackdProto"
		component={Proto}
		width={1080}
		height={1920}
		fps={FPS}
		durationInFrames={DURATION_FRAMES}
		defaultProps={{highlight: false, audio: true} satisfies ProtoProps}
	/>
);
