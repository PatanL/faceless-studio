// story-myeongnyang on the 3D story kit (our own code): props are episodes/story-myeongnyang/storyboard.json.
// Captions: the story-lane hybrid ("ricks-phrase": the reference look, the pipeline's one-line phrase pages).
// Gates stay failing ("fail"): a hold over 4 s, specks, edge cuts or a backwards readout stop the render.
import React from "react";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Episode3D } from "../kit/Episode3D";
import { buildStory, setHook } from "./story";

export const Myeongnyang3D: React.FC<StoryboardInput> = (props) => {
  // the hook still check passes {"hookVariant": "A" | "B" | "C"} alongside the storyboard
  // (stills only: the candidates are judged as frames; the chosen one is the default and renders with gates failing)
  const v = (props as unknown as { hookVariant?: string }).hookVariant;
  if (v) setHook(v);
  return <Episode3D storyboard={props} build={buildStory} captions="ricks-phrase" gates={v ? "warn" : "fail"} joins="ricks" />;
};
