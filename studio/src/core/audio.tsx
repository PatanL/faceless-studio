import React from 'react';
import {Html5Audio, Sequence, useVideoConfig} from 'remotion';
import {clamp01} from './anim';
import {asset} from './registry';
import type {SceneTiming, Storyboard} from './schema';

type Interval = [number, number];

/** Speech intervals (seconds) used to duck the music. */
export function speechIntervals(sb: Storyboard): Interval[] {
	const mode = sb.audio.duckOn;
	if (mode === 'none') return [];
	const fromVoice: Interval[] = sb.audio.voice
		.filter((v) => v.duration !== undefined)
		.map((v) => [v.start, v.start + (v.duration as number)]);
	if (mode === 'voice' || (mode === 'auto' && fromVoice.length)) return merge(fromVoice, 0.3);
	const words = sb.captions?.words ?? [];
	return merge(
		words.map((w) => [w.start, w.end] as Interval),
		0.6,
	);
}

function merge(list: Interval[], gap: number): Interval[] {
	const s = [...list].sort((a, b) => a[0] - b[0]);
	const out: Interval[] = [];
	for (const iv of s) {
		const last = out[out.length - 1];
		if (last && iv[0] - last[1] <= gap) last[1] = Math.max(last[1], iv[1]);
		else out.push([iv[0], iv[1]]);
	}
	return out;
}

/** 0 = no speech nearby, 1 = fully ducked. */
function duckAmount(t: number, ivs: Interval[], attack: number, release: number): number {
	let d = 0;
	for (const [a, b] of ivs) {
		if (t >= a && t <= b) return 1;
		if (t < a && a - t < attack) d = Math.max(d, 1 - (a - t) / attack);
		if (t > b && t - b < release) d = Math.max(d, 1 - (t - b) / release);
	}
	return d;
}

export const AudioTrack: React.FC<{sb: Storyboard; timings: SceneTiming[]; totalFrames: number}> = ({
	sb,
	timings,
	totalFrames,
}) => {
	const {fps} = useVideoConfig();
	const total = totalFrames / fps;
	const ivs = speechIntervals(sb);
	const sfxPath = (c: {cue?: string; src?: string}) => c.src ?? `${sb.audio.sfxDir}/${c.cue}.wav`;

	const sfx = [
		...sb.audio.sfx,
		...sb.scenes.flatMap((s, i) => s.sfx.map((c) => ({...c, at: c.at + timings[i].start / fps}))),
	].filter((c) => c.src || c.cue);

	return (
		<>
			{sb.audio.music.map((m, i) => {
				const from = Math.round(m.start * fps);
				const endS = Math.min(m.end ?? total, total);
				const len = Math.max(1, Math.round(endS * fps) - from);
				return (
					<Sequence key={`m${i}`} from={from} durationInFrames={len} layout="none">
						<Html5Audio
							src={asset(m.src)}
							loop={m.loop}
							volume={(f) => {
								const t = m.start + f / fps;
								const fadeIn = m.fadeIn > 0 ? clamp01((t - m.start) / m.fadeIn) : 1;
								const fadeOut = m.fadeOut > 0 ? clamp01((endS - t) / m.fadeOut) : 1;
								const dk = duckAmount(t, ivs, m.attack, m.release);
								const v = m.volume + (m.duckTo - m.volume) * dk;
								return Math.max(0, v * fadeIn * fadeOut);
							}}
						/>
					</Sequence>
				);
			})}
			{sb.audio.voice.map((v, i) => (
				<Sequence key={`v${i}`} from={Math.round(v.start * fps)} layout="none">
					<Html5Audio src={asset(v.src)} volume={v.volume} />
				</Sequence>
			))}
			{sfx.map((c, i) => (
				<Sequence key={`s${i}`} from={Math.round(c.at * fps)} layout="none">
					<Html5Audio src={asset(sfxPath(c))} volume={c.volume} />
				</Sequence>
			))}
		</>
	);
};
