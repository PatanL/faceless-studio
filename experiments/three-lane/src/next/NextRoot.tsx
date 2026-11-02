import React from "react";
import { Composition } from "remotion";
import { KitLab, LAB_FRAMES } from "./KitLab";
import { DressLab } from "./kitlab/DressLab";

export const NextRoot: React.FC = () => (
  <>
    <Composition id="KitLab" component={KitLab} width={1080} height={1920} fps={30} durationInFrames={LAB_FRAMES} defaultProps={{ captions: "ricks" as const }} />
    <Composition id="DressLab" component={DressLab} width={1080} height={1920} fps={30} durationInFrames={120} defaultProps={{ bare: false }} />
  </>
);
