// story-barca-shield on the 3D story kit (our own code): props are episodes/story-barca-shield/storyboard.json.
// Captions: the story-lane hybrid ("ricks-phrase": the reference look, the pipeline's one-line phrase pages).
// Gates stay failing ("fail"): a hold over 4 s, specks, edge cuts or a backwards readout stop the render.
import React from "react";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Episode3D } from "../kit/Episode3D";
import { buildStory } from "./story";

export const Barca3D: React.FC<StoryboardInput> = (props) => (
  <Episode3D storyboard={props} build={buildStory} captions="ricks-phrase" gates="fail" />
);
