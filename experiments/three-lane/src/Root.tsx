import React from "react";
import { Composition } from "remotion";
import { Hall, HALL_DEFAULTS } from "./Hall";
import { GLInfo } from "./GLInfo";

// 90 frames = the ~3 s dolly; a Short would be ~1900 frames of shots like this.
export const Root: React.FC = () => (
  <>
    <Composition id="Hall1080" component={Hall} width={1080} height={1920} fps={30} durationInFrames={90} defaultProps={HALL_DEFAULTS} />
    <Composition id="Hall720" component={Hall} width={720} height={1280} fps={30} durationInFrames={90} defaultProps={HALL_DEFAULTS} />
    {/* same shot without MSAA (cheaper variant, if the full chain is too slow) */}
    <Composition id="Hall1080NoMSAA" component={Hall} width={1080} height={1920} fps={30} durationInFrames={90} defaultProps={{ ...HALL_DEFAULTS, msaa: 0 }} />
    <Composition id="GLInfo" component={GLInfo} width={1080} height={1920} fps={30} durationInFrames={1} />
  </>
);
