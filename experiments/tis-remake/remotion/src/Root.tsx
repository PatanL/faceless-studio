import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';

// INTERNAL BENCHMARK ONLY (never published): shot-for-shot remake of a TIS Short, 56 s @ 30 fps.
export const RemotionRoot: React.FC = () => (
	<Composition id="TisRemake" component={Main} durationInFrames={1680} fps={30} width={1080} height={1920} />
);
