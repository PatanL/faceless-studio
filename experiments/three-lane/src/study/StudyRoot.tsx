import React from "react";
import { Composition } from "remotion";
import { VS1Z, VS1Z25 } from "./VS1Z/VS1Z";
import { MyeongHook } from "./myeong/hook";

// 1080x1920 like the episodes (the ink and caption sizes are tuned for it); compared at 720x1280 against the reference
export const StudyRoot: React.FC = () => (
  <>
    <Composition id="VS1Z" component={VS1Z} width={1080} height={1920} fps={30} durationInFrames={600} />
    <Composition id="MyeongHook" component={MyeongHook} width={1080} height={1920} fps={30} durationInFrames={110} />
    <Composition id="VS1Z25" component={VS1Z25} width={1080} height={1920} fps={30} durationInFrames={600} />
  </>
);
