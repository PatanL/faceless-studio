/**
 * The hero orca for the detail-pass opening: asset-gen's path B (`./OrcaB.tsx` is a small fork of
 * `experiments/asset-gen/orca-b/OrcaB.tsx`; the geometry JSON is imported read-only from asset-gen). Geometry, parts and the 187 surface marks were extracted from the Codex reference
 * image and rigged by hand there; every part is re-shaded from ONE light vector.
 *
 * This wrapper only adapts it to the scene: the scene light (screen space) is rotated into the orca's pitched
 * frame so the key stays put while the body pitches, plus seeded blinks and the "menace" lid.
 */
import React from 'react';
import {norm, useLight, type Vec} from '../../../kurz-style/engine/src/lib/light';
import {blinkAt} from '../../../kurz-style/engine/src/motion/motion';
import {OrcaB, markCount, type Light} from './OrcaB';

const rotV = ([x, y]: Vec, deg: number): [number, number] => {
	const a = (deg * Math.PI) / 180;
	return norm([x * Math.cos(a) - y * Math.sin(a), x * Math.sin(a) + y * Math.cos(a)]) as [number, number];
};

export const OrcaHero: React.FC<{id: string; t: number; pitch: number; jaw: number; menace: number; amp: number; freq: number}> = ({id, t, pitch, jaw, menace, amp, freq}) => {
	const S = useLight();
	const L: Light = {key: rotV(S.key, -pitch), rim: rotV(S.rim, -pitch), keyColor: 'amber-4', rimColor: S.rimColor, ambient: S.ambient, bounce: 'tide-1'};
	const blink = Math.max(blinkAt(t, id), 0.28 * menace);
	return <OrcaB id={id} t={t} amp={amp} freq={freq} jaw={jaw} blink={blink} light={L} pec={-6 * jaw} />;
};

export const orcaMarkCount = markCount;
