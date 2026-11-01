import React from 'react';
import {Composition} from 'remotion';
import {Episode} from './core/Episode';
import {calculateStoryboardMetadata} from './core/metadata';
import {StoryboardSchema, type StoryboardInput} from './core/schema';
import './kits';
import test916 from '../storyboards/test-9x16.json';
import test169 from '../storyboards/test-16x9.json';

export const RemotionRoot: React.FC = () => (
	<>
		{/* Renders whatever storyboard is passed with --props=<file.json>. */}
		<Composition
			id="Storyboard"
			component={Episode}
			schema={StoryboardSchema}
			defaultProps={test916 as unknown as StoryboardInput}
			calculateMetadata={calculateStoryboardMetadata}
			width={1080}
			height={1920}
			fps={30}
			durationInFrames={300}
		/>
		<Composition
			id="Test-16x9"
			component={Episode}
			schema={StoryboardSchema}
			defaultProps={test169 as unknown as StoryboardInput}
			calculateMetadata={calculateStoryboardMetadata}
			width={1920}
			height={1080}
			fps={30}
			durationInFrames={150}
		/>
	</>
);
