import React from "react";
import { Composition } from "remotion";
import { Hall, HALL_DEFAULTS } from "./Hall";
import { GLInfo } from "./GLInfo";
import { Turk3D } from "./turk/Turk3D";
import { Vasa3D } from "./vasa/Vasa3D";
import { parseStoryboard, sceneTimings } from "../../../studio/src/core/schema";

// 90 frames = the ~3 s dolly; a Short would be ~1900 frames of shots like this.
export const Root: React.FC = () => (
  <>
    <Composition id="Hall1080" component={Hall} width={1080} height={1920} fps={30} durationInFrames={90} defaultProps={HALL_DEFAULTS} />
    <Composition id="Hall720" component={Hall} width={720} height={1280} fps={30} durationInFrames={90} defaultProps={HALL_DEFAULTS} />
    {/* same shot without MSAA (cheaper variant, if the full chain is too slow) */}
    <Composition id="Hall1080NoMSAA" component={Hall} width={1080} height={1920} fps={30} durationInFrames={90} defaultProps={{ ...HALL_DEFAULTS, msaa: 0 }} />
    {/* story-chess-turk v7: props = the episode storyboard.json (pass with --props) */}
    <Composition id="Turk3D" component={Turk3D} width={1080} height={1920} fps={30} durationInFrames={1767}
      defaultProps={{} as never}
      calculateMetadata={({ props }) => {
        try { return { durationInFrames: sceneTimings(parseStoryboard(props)).totalFrames }; } catch { return {}; }
      }} />
    {/* story-vasa v1: props = episodes/story-vasa/storyboard.json */}
    <Composition id="Vasa3D" component={Vasa3D} width={1080} height={1920} fps={30} durationInFrames={1770}
      defaultProps={{} as never}
      calculateMetadata={({ props }) => {
        try { return { durationInFrames: sceneTimings(parseStoryboard(props)).totalFrames }; } catch { return {}; }
      }} />
    <Composition id="GLInfo" component={GLInfo} width={1080} height={1920} fps={30} durationInFrames={1} />
  </>
);
