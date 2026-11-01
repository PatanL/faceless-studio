import React from 'react';
import {E, camAt, camT, hash, look} from '../lib/anim';
import {Gun} from '../art/guns';

// Scene block 8 (44.43-50.10): a worried Russia country-ball on robot legs juggling old and new rifles (S22-S23).

const DARK = '#3F3C45';
const HI = '#615E64';

const Link: React.FC<{a: [number, number]; b: [number, number]; w?: number}> = ({a, b, w = 34}) => (
	<g>
		<line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={DARK} strokeWidth={w} strokeLinecap="round" />
		<line x1={a[0] + (b[0] - a[0]) * 0.25} y1={a[1] + (b[1] - a[1]) * 0.25} x2={a[0] + (b[0] - a[0]) * 0.6} y2={a[1] + (b[1] - a[1]) * 0.6} stroke={HI} strokeWidth={w * 0.32} strokeLinecap="round" />
		<circle cx={b[0]} cy={b[1]} r={w * 0.62} fill={DARK} />
		<circle cx={b[0] - 3} cy={b[1] - 3} r={w * 0.22} fill={HI} />
	</g>
);

const Chain: React.FC<{pts: [number, number][]; w?: number}> = ({pts, w}) => (
	<g>
		{pts.slice(1).map((p, i) => (
			<Link key={i} a={pts[i]} b={p} w={w} />
		))}
	</g>
);

const Foot: React.FC<{x: number; y: number}> = ({x, y}) => (
	<g transform={`translate(${x} ${y})`}>
		<rect x={-70} y={-30} width={140} height={52} rx={26} fill={DARK} />
		{[-44, -15, 15, 44].map((cx) => (
			<g key={cx}>
				<circle cx={cx} cy={-4} r={20} fill="#55525B" />
				<circle cx={cx} cy={-4} r={8} fill={DARK} />
			</g>
		))}
		<rect x={-74} y={16} width={148} height={14} rx={7} fill="#2A2830" />
	</g>
);

export const Ball: React.FC<{t: number}> = ({t}) => {
	// S23: an aggressive push that ends with the ball overflowing the frame
	const c = camAt(t, [
		[44.43, {x: 540, y: 960, s: 1, r: 0}],
		[47.2, {x: 540, y: 960, s: 1.02, r: 0}, E.linear],
		[48.35, look([540, 760], [540, 800], 3.3, 0), E.inOutCubic],
		[50.2, look([540, 760], [540, 800], 3.55, 0), E.linear],
	]);
	// S22: a crouched, nervous side-shuffle: knees bent out, the body leaning into each step
	const sh = Math.sin(t * Math.PI * 2 * 0.9);
	const sx = sh * 38;
	const leanDeg = Math.sin(t * Math.PI * 2 * 0.9 + 0.6) * 9;
	const bounce = Math.abs(Math.sin(t * Math.PI * 2 * 1.8)) * -14;
	const cx = 540 + sx;
	const cy = 780 + bounce;
	const lift = (k: number) => Math.max(0, Math.sin(t * Math.PI * 2 * 1.8 + k * Math.PI)) * 30;
	const wave = (k: number) => Math.sin(t * Math.PI * 2 * 1.3 + k) * 10;
	const dart = t > 47.2 ? Math.sign(Math.sin(t * Math.PI * 2 * 1.2)) * 10 : Math.sin(t * 2) * 4;
	const worry = t > 47.2 ? 1 : 0.5;
	const sweatY = t > 47.2 ? Math.min(20, (t - 47.2) * 12) : 0;
	const R = 162;
	// brows act: a worried knit that twitches up on each eye dart in S23
	const browUp = t > 47.2 ? 8 + Math.abs(Math.sin(t * Math.PI * 2 * 1.2)) * 8 : Math.sin(t * 3) * 3;
	const browTw = t > 47.2 ? Math.sin(t * Math.PI * 2 * 2.4) * 4 : 0;
	const armL = (() => {
		const a = (wave(0) * Math.PI) / 180;
		const h: [number, number] = [cx - 250 + Math.sin(a) * 30, cy - 30 - Math.cos(a) * 20];
		return {pts: [[cx - 120, cy + 30], [cx - 190, cy + 70], [cx - 260, cy + 40], h] as [number, number][], h, rot: -105 + 48 * Math.sin(t * Math.PI * 2 * 0.85)};
	})();
	const armR = (() => {
		const a = (wave(2) * Math.PI) / 180;
		const h: [number, number] = [cx + 250 + Math.sin(a) * 30, cy - 30 - Math.cos(a) * 20];
		return {pts: [[cx + 120, cy + 30], [cx + 190, cy + 70], [cx + 260, cy + 40], h] as [number, number][], h, rot: -70 + 46 * Math.sin(t * Math.PI * 2 * 1.05 + 1.2)};
	})();
	return (
		<g>
			<g transform={camT(c)}>
				<rect x={-1500} y={-1500} width={4080} height={4920} fill="#5836D2" />
				<g transform={`translate(${-((t * 30) % 300)} ${(t * 30) % 300})`}>
					{/* v3: a denser field of diagonal speed streaks in two tones */}
					{Array.from({length: 64}, (_, i) => {
						const x = -800 + hash(i) * 2800;
						const y = -700 + hash(i + 50) * 3500;
						const L = 140 + hash(i + 9) * 420;
						const h = 26 + hash(i + 17) * 26;
						return <rect key={i} x={x} y={y} width={L} height={h} rx={h / 2} fill={i % 3 === 0 ? '#7150DC' : '#6541D5'} transform={`rotate(-45 ${x} ${y})`} />;
					})}
					{Array.from({length: 18}, (_, i) => (
						<circle key={`d${i}`} cx={-400 + hash(i + 200) * 2000} cy={-400 + hash(i + 300) * 2800} r={10 + hash(i + 400) * 14} fill="#6541D5" />
					))}
				</g>
				<ellipse cx={540 + sx * 0.8} cy={1170} rx={240} ry={20} fill="#000" opacity={0.18} />
				{/* legs: bent knees splayed outward (crouch) */}
				<Chain pts={[[cx - 50, cy + 110], [cx - 150 - lift(0) * 0.3, cy + 230 - lift(0) * 0.6], [cx - 96, 1120 - lift(0)]]} w={56} />
				<Chain pts={[[cx + 50, cy + 110], [cx + 150 + lift(1) * 0.3, cy + 230 - lift(1) * 0.6], [cx + 96, 1120 - lift(1)]]} w={56} />
				<Foot x={cx - 100} y={1150 - lift(0)} />
				<Foot x={cx + 100} y={1150 - lift(1)} />
				<g transform={`rotate(${leanDeg} ${cx} ${cy + 120})`}>
				{/* arms behind the guns' hands */}
				<Chain pts={armL.pts} w={32} />
				<Chain pts={armR.pts} w={32} />
				{/* the ball */}
				<circle cx={cx} cy={cy} r={R + 22} fill={DARK} />
				<path d={`M${cx - R - 14},${cy - 40} A${R + 14},${R + 14} 0 0 1 ${cx + 40},${cy - R - 14}`} stroke={HI} strokeWidth={9} fill="none" strokeLinecap="round" />
				<clipPath id="ballClip">
					<circle cx={cx} cy={cy} r={R} />
				</clipPath>
				<g clipPath="url(#ballClip)">
					<rect x={cx - R} y={cy - R} width={2 * R} height={(2 * R) / 3} fill="#FFFFFF" />
					<rect x={cx - R} y={cy - R / 3} width={2 * R} height={(2 * R) / 3} fill="#0C0B97" />
					<rect x={cx - R} y={cy + R / 3} width={2 * R} height={(2 * R) / 3} fill="#F71617" />
					<circle cx={cx + 50} cy={cy + 20} r={48} fill="#4A5BE0" opacity={0.3} />
					<circle cx={cx - 30} cy={cy + 70} r={40} fill="#FF8080" opacity={0.3} />
					<circle cx={cx + 70} cy={cy + 80} r={30} fill="#FF8080" opacity={0.3} />
					<path d={`M${cx + R},${cy - R} A${R},${R} 0 0 1 ${cx + R * 0.2},${cy + R} L${cx + R},${cy + R} Z`} fill="#000" opacity={0.1} />
					{/* v3 shading: a terminator crescent on the shadow side and a glossy top-left highlight */}
					<path d={`M${cx + R * 0.35},${cy - R} A${R},${R} 0 0 1 ${cx + R * 0.35},${cy + R} A${R * 0.8},${R} 0 0 0 ${cx + R * 0.35},${cy - R} Z`} fill="#000" opacity={0.12} />
				</g>
				<ellipse cx={cx - R * 0.5} cy={cy - R * 0.62} rx={R * 0.28} ry={R * 0.13} fill="#FFFFFF" opacity={0.55} transform={`rotate(-35 ${cx - R * 0.5} ${cy - R * 0.62})`} />
				<circle cx={cx - R * 0.78} cy={cy - R * 0.28} r={R * 0.06} fill="#FFFFFF" opacity={0.5} />
				{/* visor + brows */}
				<g transform={`translate(${cx} ${cy - 55})`}>
					<rect x={-76} y={-30} width={152} height={62} rx={26} fill="#2E2B33" />
					<rect x={-68} y={-23} width={136} height={48} rx={22} fill="#E4E2E4" />
					<circle cx={-30 + dart} cy={2} r={15} fill="#111" />
					<circle cx={30 + dart} cy={2} r={15} fill="#111" />
					<circle cx={-25 + dart} cy={-3} r={4} fill="#FFF" />
					<circle cx={35 + dart} cy={-3} r={4} fill="#FFF" />
					<rect x={-76} y={-62 - browUp} width={64} height={20} rx={10} fill="#76737C" transform={`rotate(${-16 * worry - browTw} -44 -51)`} />
					<rect x={12} y={-62 - browUp} width={64} height={20} rx={10} fill="#76737C" transform={`rotate(${16 * worry + browTw} 44 -51)`} />
				</g>
				{t > 46.0 && <path d={`M${cx},${cy + 20 + sweatY} Q${cx + 13},${cy + 42 + sweatY} ${cx},${cy + 50 + sweatY} Q${cx - 13},${cy + 42 + sweatY} ${cx},${cy + 20 + sweatY} Z`} fill="#FFFFFF" />}
				{/* rifles in the grippers */}
				<Gun g={{kind: 'ak47', x: armL.h[0] + 10, y: armL.h[1] + 30, rot: armL.rot, s: 0.95}} />
				<Gun g={{kind: 'ak12', x: armR.h[0] - 10, y: armR.h[1] + 30, rot: armR.rot, s: 0.95}} />
				<circle cx={armL.h[0]} cy={armL.h[1]} r={30} fill={DARK} />
				<circle cx={armL.h[0] - 6} cy={armL.h[1] - 6} r={9} fill={HI} />
				<circle cx={armR.h[0]} cy={armR.h[1]} r={30} fill={DARK} />
				<circle cx={armR.h[0] - 6} cy={armR.h[1] - 6} r={9} fill={HI} />
				</g>
			</g>
		</g>
	);
};
