import React from 'react';
import {Composition, Still} from 'remotion';
import {Showcase} from './scenes/Showcase';
import {Assets, ShadingLadder} from './scenes/Stills';
import {OrcaOpen, ORCA_OPEN_FRAMES} from './scenes/OrcaOpen';

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="Showcase" component={Showcase} width={1080} height={1920} fps={30} durationInFrames={120} />
		<Composition id="OrcaOpen" component={OrcaOpen} width={1080} height={1920} fps={30} durationInFrames={ORCA_OPEN_FRAMES} />
		<Still id="ShadingLadder" component={ShadingLadder} width={1080} height={1920} />
		<Still id="Assets" component={Assets} width={1080} height={1920} />
	</>
);
