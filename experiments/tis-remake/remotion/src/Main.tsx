import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {E, FPS, clamp, hash, lerp, noise} from './lib/anim';
import {Defs} from './art/defs';
import {LOOKS, Soldier} from './art/soldier';
import {Captions} from './Captions';
import {Hook} from './scenes/Hook';
import {Base} from './scenes/Base';
import {Range, SHOOTER} from './scenes/Range';
import {Office} from './scenes/Office';
import {Ruins} from './scenes/Ruins';
import {Pink} from './scenes/Pink';
import {Armoury} from './scenes/Armoury';
import {Ball} from './scenes/Ball';
import {Camp} from './scenes/Camp';
import {loadFonts} from './fonts';

type SceneFC = React.FC<{t: number}>;
const SCENES: {id: string; C: SceneFC; t0: number; t1: number}[] = [
	{id: 'hook', C: Hook, t0: 0, t1: 3.27},
	{id: 'base', C: Base, t0: 3.27, t1: 14.25},
	{id: 'range', C: Range, t0: 14.25, t1: 22.3},
	{id: 'office', C: Office, t0: 22.3, t1: 26.33},
	{id: 'ruins', C: Ruins, t0: 26.33, t1: 32.8},
	{id: 'pink', C: Pink, t0: 32.8, t1: 38.93},
	{id: 'armoury', C: Armoury, t0: 38.93, t1: 44.8},
	{id: 'ball', C: Ball, t0: 44.8, t1: 50.1},
	{id: 'camp', C: Camp, t0: 50.1, t1: 999},
];

type Kind = 'sil1' | 'sil2' | 'slash' | 'iris' | 'blob' | 'blob2' | 'splat';
const TRANS: {t0: number; t1: number; from: string; to: string; kind: Kind}[] = [
	{t0: 2.97, t1: 3.27, from: 'hook', to: 'base', kind: 'sil1'},
	{t0: 13.95, t1: 14.25, from: 'base', to: 'range', kind: 'sil2'},
	{t0: 21.97, t1: 22.3, from: 'range', to: 'office', kind: 'slash'},
	{t0: 25.97, t1: 26.33, from: 'office', to: 'ruins', kind: 'iris'},
	{t0: 32.43, t1: 32.8, from: 'ruins', to: 'pink', kind: 'blob'},
	{t0: 38.55, t1: 38.93, from: 'pink', to: 'armoury', kind: 'blob2'},
	{t0: 44.43, t1: 44.8, from: 'armoury', to: 'ball', kind: 'slash'},
	{t0: 49.7, t1: 50.1, from: 'ball', to: 'camp', kind: 'splat'},
];

const byId = (id: string) => SCENES.find((s) => s.id === id)!;

function blobPath(cx: number, cy: number, R: number, seed: number, t: number, lobes = 7, amp = 0.16, spiky = 0): string {
	const pts: string[] = [];
	const n = 72;
	for (let i = 0; i < n; i++) {
		const a = (i / n) * Math.PI * 2;
		let k = 1 + amp * Math.sin(lobes * a + seed + t * 3) + amp * 0.6 * Math.sin((lobes + 4) * a + seed * 2 - t * 4) + amp * 0.5 * noise(a * 3 + seed, seed);
		if (spiky) k += spiky * Math.pow(Math.max(0, Math.sin(11 * a + seed * 3)), 8) + spiky * 0.6 * Math.pow(Math.max(0, Math.sin(17 * a + seed)), 10);
		pts.push(`${(cx + Math.cos(a) * R * k).toFixed(1)},${(cy + Math.sin(a) * R * k).toFixed(1)}`);
	}
	// smooth with quadratic midpoints
	const P = pts.map((p) => p.split(',').map(Number));
	let d = '';
	for (let i = 0; i < n; i++) {
		const p0 = P[i];
		const p1 = P[(i + 1) % n];
		const m = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2];
		d += i === 0 ? `M${m[0].toFixed(1)},${m[1].toFixed(1)}` : '';
		const p2 = P[(i + 2) % n];
		const m2 = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2];
		d += ` Q${p1[0].toFixed(1)},${p1[1].toFixed(1)} ${m2[0].toFixed(1)},${m2[1].toFixed(1)}`;
	}
	return d + ' Z';
}

function slashStreaks(u: number): React.ReactNode[] {
	const out: React.ReactNode[] = [];
	for (let i = 0; i < 18; i++) {
		const y = -1500 + i * 190 + (hash(i) - 0.5) * 80;
		const delay = hash(i + 7) * 0.35;
		const v = clamp((u - delay) / (1 - delay * 0.6));
		if (v <= 0) continue;
		const th = lerp(20 + hash(i + 3) * 100, 260, E.inQuad(v));
		const len = 3600 * E.outCubic(Math.min(1, v * 1.4));
		const x0 = -1800 + (hash(i + 11) - 0.5) * 600;
		const x1 = x0 + len;
		out.push(<path key={i} d={`M${x0},${y} Q${(x0 + x1) / 2},${y - th / 2} ${x1},${y} Q${(x0 + x1) / 2},${y + th / 2} ${x0},${y} Z`} fill="#fff" />);
	}
	return out;
}

const Matte: React.FC<{kind: Kind; u: number; t: number}> = ({kind, u, t}) => {
	switch (kind) {
		case 'sil1': {
			// soldier A's own silhouette (helmet first) flies in from the top-right and scales up over the frame
			const e = E.inOutCubic(u);
			const hx = lerp(1250, 690, e);
			const hy = lerp(-260, 560, e);
			const k = lerp(2.2, 9, E.inCubic(u));
			return (
				<g transform={`translate(${hx} ${hy}) rotate(${lerp(-20, 8, e)}) scale(${k}) translate(0 540)`}>
					<Soldier look={LOOKS.A} x={0} y={0} shadow={false} pose={{facing: -1, handN: [-40, -300], handF: [60, -310]}} />
				</g>
			);
		}
		case 'sil2': {
			// the kneeling shooter's silhouette flies in from the bottom-right, growing over the frame
			const e = E.inCubic(u);
			const x = lerp(1180, 380, E.outCubic(u));
			const y = lerp(1650, 1500, e);
			const k = lerp(0.9, 6.5, e);
			return (
				<g transform={`translate(${x} ${y}) scale(${k})`}>
					<SHOOTER t={t} silhouette />
				</g>
			);
		}
		case 'slash':
			return <g transform="rotate(-30 540 960)">{slashStreaks(u)}</g>;
		case 'iris':
			return <circle cx={540} cy={900} r={E.inQuad(u) * 1180 + 1} fill="#fff" />;
		case 'blob':
			return <path d={blobPath(600, 800, E.inCubic(u) * 1500 + 20, 2, t, 6, 0.2)} fill="#fff" />;
		case 'blob2':
			return <path d={blobPath(-60, 300, E.inCubic(u) * 2300 + 40, 5, t, 5, 0.22)} fill="#fff" />;
		case 'splat':
			return <path d={blobPath(640, 700, E.inCubic(u) * 1400 + 15, 9, t, 9, 0.12, 0.5)} fill="#fff" />;
	}
};

const Overlay: React.FC<{kind: Kind; u: number; t: number}> = ({kind, u, t}) => {
	if (kind === 'iris') {
		const r = E.inQuad(u) * 1180 + 1;
		return (
			<g>
				<circle cx={540} cy={900} r={r} fill="none" stroke="rgba(255,255,255,0.32)" strokeWidth={40} />
				<circle cx={540} cy={900} r={r - 26} fill="none" stroke="rgba(255,255,255,0.18)" strokeWidth={14} />
			</g>
		);
	}
	if (kind === 'blob2') {
		return (
			<g>
				{[0, 1, 2, 3, 4].map((i) => {
					const a = 0.2 + i * 0.28;
					const R = E.inCubic(u) * 2300 + 120 + 140 * u;
					const x = -60 + Math.cos(a) * R + i * 30;
					const y = 300 + Math.sin(a) * R * 0.7;
					return <path key={i} d={blobPath(x, y, 26 + hash(i) * 22, i, t, 4, 0.25)} fill={i % 2 ? '#E27E8C' : '#C9707C'} opacity={1 - u * 0.6} />;
				})}
			</g>
		);
	}
	if (kind === 'splat' && u > 0.3) {
		const v = (u - 0.3) / 0.7;
		return (
			<g opacity={1 - v}>
				{[0, 1, 2].map((i) => (
					<path key={i} d={`M${-40 + i * 60},${1500 + i * 120} Q${200 + i * 40},${1300 - i * 60} ${420 + i * 50},${1180 + i * 40}`} fill="none" stroke="#5836D2" strokeWidth={26 - i * 6} strokeLinecap="round" />
				))}
			</g>
		);
	}
	return null;
};

export const Main: React.FC = () => {
	loadFonts();
	const frame = useCurrentFrame();
	const t = frame / FPS;
	const tr = TRANS.find((x) => t >= x.t0 && t < x.t1);
	let body: React.ReactNode;
	if (tr) {
		const u = clamp((t - tr.t0) / (tr.t1 - tr.t0));
		const From = byId(tr.from).C;
		const To = byId(tr.to).C;
		body = (
			<>
				<From t={t} />
				{tr.kind === 'slash' && (
					<g opacity={clamp(u * 1.6)}>
						<g transform="rotate(-30 540 960)">
							<g filter="url(#smearX)">
								<g transform="rotate(30 540 960)">
									<From t={t} />
								</g>
							</g>
						</g>
					</g>
				)}
				<mask id="tmask" maskUnits="userSpaceOnUse" x={-200} y={-200} width={1480} height={2320} style={{maskType: 'alpha'}}>
					<Matte kind={tr.kind} u={u} t={t} />
				</mask>
				<g mask="url(#tmask)">
					<To t={t} />
				</g>
				<Overlay kind={tr.kind} u={u} t={t} />
			</>
		);
	} else {
		const s = [...SCENES].reverse().find((x) => t >= x.t0)!;
		body = <s.C t={t} />;
	}
	return (
		<AbsoluteFill style={{backgroundColor: '#000'}}>
			<svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
				<Defs />
				{body}
			</svg>
			<Captions t={t} />
		</AbsoluteFill>
	);
};
