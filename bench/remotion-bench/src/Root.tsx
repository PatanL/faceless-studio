import React from 'react';
import {Composition} from 'remotion';
import {Bench} from './Bench';

export const Root: React.FC = () => (
  <>
    <Composition id="Bench" component={Bench} durationInFrames={900} fps={30} width={1080} height={1920} />
    <Composition id="Bench169" component={Bench} durationInFrames={900} fps={30} width={1920} height={1080} />
  </>
);
