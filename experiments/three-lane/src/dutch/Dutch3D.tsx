// story-dutch-waterline v1 on the 3D story kit (our own code): props are episodes/story-dutch-waterline/storyboard.json.
// story.ts is the build (the anonymous farmer, his knee and the floodgate; the laughing general; the 1672 water line).
// Captions: "ricks-phrase". Gates stay failing ("fail"); joins gated against the RicksClips mix.
import React from "react";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Episode3D } from "../kit/Episode3D";
import { buildStory } from "./story";

export const Dutch3D: React.FC<StoryboardInput> = (props) => (
  <Episode3D storyboard={props} build={buildStory} captions="ricks-phrase" gates="fail" joins="ricks" />
);
