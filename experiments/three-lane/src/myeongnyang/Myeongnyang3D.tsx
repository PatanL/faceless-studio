// story-myeongnyang v3 on the 3D story kit (our own code): props are episodes/story-myeongnyang/storyboard.json.
// story3.ts is the v3 build (the anonymous admiral and the cork; its opening shot is the hook lab's MyeongHook);
// story.ts keeps the v1 build. Captions: "ricks-phrase". Gates stay failing ("fail"); joins gated against the RicksClips mix.
import React from "react";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Episode3D } from "../kit/Episode3D";
import { buildStory } from "./story3";

export const Myeongnyang3D: React.FC<StoryboardInput> = (props) => (
  <Episode3D storyboard={props} build={buildStory} captions="ricks-phrase" gates="fail" joins="ricks" />
);
