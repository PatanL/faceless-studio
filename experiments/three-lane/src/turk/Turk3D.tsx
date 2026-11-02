// story-chess-turk v7 (our own code) on the 3D story kit (kit/Episode3D): the shot groups from story.ts, the cabinet
// rig, the title, the place tags and the 1857 newspaper as DOM overlays. Props are the episode storyboard JSON.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { StoryboardInput } from "../../../../studio/src/core/schema";
import { Headline, Tag } from "../../../../studio/src/kits/explainer/ui";
import { Episode3D } from "../kit/Episode3D";
import type { Timing } from "../kit/timing";
import { buildStory, type Tag as TagSpec } from "./story";
import { toKit } from "./rig";
import { Newspaper } from "./Newspaper";

const W = 1080, H = 1920;

const build = (T: Timing) => { const s = buildStory(T); return { ...s, groups: s.groups.map(toKit) }; };

export const PlaceTags: React.FC<{ tags: TagSpec[] }> = ({ tags }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  return (
    <>
      {tags.map((g, i) => (t >= g.at - 0.1 && t < g.out + 0.5 ? (
        <div key={i} style={{ position: "absolute", left: 0.5 * W - 500, top: 0.14 * H - 65, width: 1000, height: 130 }}>
          <Tag props={{ text: g.text, at: g.at, size: 46, out: g.out, align: "center" }} time={t} frame={frame} fps={fps} width={1000} height={130} sceneDuration={60} />
        </div>) : null))}
    </>
  );
};

const Overlays: React.FC<{ tags: TagSpec[]; headlineOut: number; paperAt: number; paperOut: number }> = ({ tags, headlineOut, paperAt, paperOut }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {t < headlineOut + 0.5 && (
        <div style={{ position: "absolute", left: 0.5 * W - 480, top: 0.1 * H - 120, width: 960, height: 240 }}>
          <Headline props={{ text: "UNBEATABLE ROBOT", red: "ROBOT", at: -0.6, size: 88, out: headlineOut }} time={t} frame={frame} fps={fps} width={960} height={240} sceneDuration={60} />
        </div>)}
      <PlaceTags tags={tags} />
      {t >= paperAt && t < paperOut && <Newspaper t={t - paperAt} />}
    </AbsoluteFill>
  );
};

export const Turk3D: React.FC<StoryboardInput> = (props) => (
  <Episode3D storyboard={props} build={build}
    overlays={(s) => <Overlays tags={s.tags} headlineOut={s.headlineOut} paperAt={s.paperAt} paperOut={s.paperOut} />} />
);
