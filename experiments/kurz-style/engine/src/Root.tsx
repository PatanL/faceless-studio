import React from 'react';
import {Composition, Still} from 'remotion';
import {Showcase} from './scenes/Showcase';
import {Assets, ShadingLadder} from './scenes/Stills';

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="Showcase" component={Showcase} width={1080} height={1920} fps={30} durationInFrames={120} />
		<Still id="ShadingLadder" component={ShadingLadder} width={1080} height={1920} />
		<Still id="Assets" component={Assets} width={1080} height={1920} />
	</>
);
