import React from 'react';
import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {Scene} from './Scene';
import {Captions, Word} from './Captions';
import {failure, shakeAt, whipAt, W} from './timeline';
import caps from '../public/audio/captions.json';

export type ProtoProps = {highlight: boolean; audio: boolean};

export const Proto: React.FC<ProtoProps> = ({highlight, audio}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const t = frame / fps;
	const sh = shakeAt(t);
	const whip = whipAt(t);
	const smear = 70 * whip.amount;
	const fail = failure(t);
	return (
		<AbsoluteFill style={{backgroundColor: '#6f9fc4'}}>
			<svg width={0} height={0} style={{position: 'absolute'}}>
				<filter id="smear" x="-10%" y="0" width="120%" height="100%">
					<feGaussianBlur stdDeviation={`${smear} 0`} />
				</filter>
			</svg>
			<AbsoluteFill
				style={{
					transform: `translate(${sh.x * width + whip.dir * whip.amount * 140}px, ${sh.y * height}px) scale(1.05)`,
					filter: smear > 0.5 ? 'url(#smear)' : undefined,
				}}
			>
				<ThreeCanvas width={width} height={height} shadows="percentage" flat gl={{antialias: true, preserveDrawingBuffer: true}}>
					<Scene t={t} />
				</ThreeCanvas>
			</AbsoluteFill>
			{/* mild vignette: centre ~10 luma above the corners, navy not black */}
			<AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 60% at 50% 45%, rgba(8,14,28,0) 55%, rgba(8,14,28,0.28) 100%)'}} />
			{/* failure flush: whole frame toward red */}
			<AbsoluteFill style={{backgroundColor: '#96524e', mixBlendMode: 'multiply', opacity: 0.55 * fail}} />
			<AbsoluteFill style={{backgroundColor: '#ff300a', mixBlendMode: 'soft-light', opacity: 0.25 * fail}} />
			{t < W.lastWordEnd + 0.1 && <Captions words={(caps as {words: Word[]}).words} highlight={highlight} />}
			{audio && <Html5Audio src={staticFile('audio/mix.wav')} />}
		</AbsoluteFill>
	);
};
