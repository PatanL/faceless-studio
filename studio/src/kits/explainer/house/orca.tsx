/**
 * Hero orca, side view facing right, drawn fresh for the house style (not traced from any reference).
 * Ported from experiments/kurz-style/engine/src/assets/Orca.tsx; registered as the kit's default side orca (house/figures.tsx).
 * Local space: snout at x≈990, fluke tips at x≈15, back at y≈131, belly at y≈300, dorsal tip at y≈-58.
 *
 * Built as FLAT coloured parts (ink-1 skin, bone eye patch / belly / flank lobe, tide-tinted saddle), handed to
 * <Shaded>, which adds the whole light stack from the scene light. Motion: travelling-wave tail beat (vertical,
 * whale-style), flipper follow-through lagging the body, breathing, seeded blinks.
 */
import {FLAT} from './style';
import React from 'react';
import {c, mixOk, shadowOf} from './color';
import {swimBend, warp} from './geom';
import {useLight, useTint} from './light';
import {Eye, Shaded, type Layers} from './Shaded';
import {blinkAt, breathe} from './motion';

const BODY =
	'M 990 214 C 987 188 966 166 934 156 C 884 140 806 131 704 131 C 594 131 474 145 362 167 C 272 185 192 197 124 202 C 106 204 100 220 118 223 C 194 230 264 247 362 268 C 474 292 594 304 704 300 C 806 296 882 282 932 264 C 966 252 987 238 990 214 Z';
const FLUKE =
	'M 132 206 C 104 196 74 170 40 140 C 26 128 14 134 24 152 C 36 176 52 196 66 208 C 52 222 36 244 26 268 C 18 286 30 292 44 280 C 78 252 104 228 132 220 Z';
const DORSAL = 'M 694 136 C 670 96 640 24 608 -44 C 600 -58 586 -56 586 -42 C 584 16 572 84 546 150 Z';
const PEC = 'M 840 262 C 836 300 812 352 772 386 C 746 408 712 410 706 388 C 700 362 740 314 790 266 Z';
const EYE_PATCH = 'M 790 194 C 796 174 832 164 866 169 C 884 172 892 182 884 191 C 866 204 822 210 790 194 Z';
const BELLY =
	'M 1004 220 C 976 228 946 234 912 240 C 870 248 824 262 770 274 C 730 282 700 286 660 286 C 610 286 572 282 534 274 C 494 264 462 240 432 214 C 412 198 384 192 360 200 C 352 228 356 262 342 300 L 342 380 L 1010 380 Z';
const SADDLE = 'M 548 112 C 548 160 520 176 474 184 C 440 188 410 188 386 184 C 420 170 470 146 500 112 Z';
const MOUTH = 'M 986 224 C 966 233 936 238 902 236 C 894 235 888 232 884 228';
const BLOWHOLE = 'M 836 147 Q 846 141 856 147';

// jaw rig: the body split along the mouth line into an upper body and a lower jaw that rotates about the hinge.
// Used only while the jaw is open, so the closed orca keeps the seamless single body path.
const BODY_UPPER =
	'M 990 214 C 987 188 966 166 934 156 C 884 140 806 131 704 131 C 594 131 474 145 362 167 C 272 185 192 197 124 202 C 106 204 100 220 118 223 C 194 230 264 247 362 268 C 474 292 594 304 704 300 C 790 297 840 290 872 280 C 860 266 862 244 878 229 C 892 234 930 239 960 234 C 975 231 984 226 990 214 Z';
const JAW_TOP: [number, number][] = [
	[878, 229],
	[892, 234],
	[930, 239],
	[960, 234],
	[975, 231],
	[984, 226],
	[990, 216],
];
const JAW = 'M 870 230 C 892 234 930 239 960 234 C 975 231 984 226 990 216 C 987 238 966 252 932 264 C 912 271 892 276 868 281 C 856 268 856 244 870 230 Z';
const HINGE: [number, number] = [872, 236];
// secondary forms (bible §10: 15-40 constructed parts on a hero)
const MELON = 'M 926 158 C 956 164 980 182 987 204 C 968 196 944 188 916 182 C 904 176 910 160 926 158 Z';
const CHEEK = 'M 846 214 C 870 226 900 232 930 232 C 900 240 868 238 846 228 Z';
const PEC_ROOT = 'M 786 254 C 806 246 836 250 852 262 C 832 270 806 270 786 262 Z';
const FLUKE_RIDGE = 'M 124 210 C 98 196 70 172 40 146 M 124 216 C 98 228 68 252 40 276';
const KEEL = 'M 360 172 C 300 184 220 196 150 202';
const WRINKLES = 'M 800 278 Q 806 286 800 294 M 788 280 Q 794 288 788 296 M 812 276 Q 818 283 813 290';

const rotAbout = (o: [number, number], deg: number) => {
	const a = (deg * Math.PI) / 180;
	const ca = Math.cos(a);
	const sa = Math.sin(a);
	return (x: number, y: number): [number, number] => [o[0] + (x - o[0]) * ca - (y - o[1]) * sa, o[1] + (x - o[0]) * sa + (y - o[1]) * ca];
};
const JAW_MAX_DEG = 24;

export const ORCA_BOX: [number, number, number, number] = [14, -58, 990, 470];

export const Orca: React.FC<{
	id: string;
	t: number;
	/** tail beat amplitude multiplier */
	amp?: number;
	freq?: number;
	lod?: 'hero' | 'far';
	layers?: Partial<Layers>;
	/** object rotation in degrees (passed to the shader so the light stays in screen space) */
	rot?: number;
	flip?: boolean;
	cast?: {y: number; lift?: number};
	/** 0 closed .. 1 fully open (24°), teeth + mouth interior appear in the gap; may overshoot slightly */
	jaw?: number;
	/** pupil direction (-1..1) and lid (0 open .. 1 shut) for acting */
	look?: [number, number];
	lid?: number;
	/** secondary forms (melon, cheek, flipper root, fluke ridges, keel, wrinkles): hero only */
	detail?: boolean;
	/** flat colour for lod 'far' (kit silhouette mode); default ink-1 on the current plane */
	silColor?: string;
	/** dorsal fin height multiplier about its base (an adult male's fin: 1.3-1.5) */
	finScale?: number;
}> = ({id, t, amp = 1, freq = 0.55, lod = 'hero', layers, rot = 0, flip = false, cast, jaw = 0, look = [0.4, 0.1], lid = 0.28, detail = false, silColor, finScale = 1}) => {
	const tint = useTint();
	const L = useLight();
	const bend = swimBend({head: 990, tail: 15, amp: 26 * amp, t, freq, lag: 1.9});
	const w = (d: string) => warp(d, bend);
	const finTop = Math.min(-62, 145 - 207 * finScale);
	const dorsal = finScale === 1 ? DORSAL : warp(DORSAL, (x, y) => [x, 145 - (145 - y) * finScale]);
	// flipper: follow-through, lags the body wave by ~0.18 s and adds its own paddle
	const flip1 = 7 * Math.sin(2 * Math.PI * freq * (t - 0.18)) + 3 * Math.sin(2 * Math.PI * 0.21 * t);
	const pecNear = `rotate(${flip1.toFixed(2)} 812 268)`;
	const pecFar = `translate(34 -26) rotate(${(-flip1 * 0.8 - 8).toFixed(2)} 812 268) translate(812 268) scale(0.82) translate(-812 -268)`;

	if (lod === 'far') {
		const col = silColor ?? tint('ink-1');
		// a distant orca keeps its white eye patch, belly and grey saddle (plane-hazed, so low contrast): a flat
		// one-colour far orca read as a shark (ORCA_V2_AUDIT I2). A builder silhouette (silColor) stays flat.
		const marks = silColor === undefined;
		return (
			<g>
				<path d={PEC} transform={pecFar} fill={col} />
				<path d={w(FLUKE)} fill={col} />
				<path d={w(dorsal)} fill={col} />
				<path d={w(BODY)} fill={col} />
				{marks ? (
					<g clipPath={`url(#${id}-fc)`}>
						<clipPath id={`${id}-fc`}>
							<path d={w(BODY)} />
						</clipPath>
						<path d={w(BELLY)} fill={tint('bone-1')} />
						<path d={w(SADDLE)} fill={tint('bone-0')} opacity={0.55} />
						<path d={w(EYE_PATCH)} fill={tint('bone-2')} />
					</g>
				) : null}
				<path d={PEC} transform={pecNear} fill={col} />
			</g>
		);
	}

	// style A: near-navy skin (style_board_A orca); Lantern: ink-1
	const skin = FLAT ? 'ink-0' : 'ink-1';
	const br = breathe(t, id, 0.01, 3.6);
	const blink = blinkAt(t, id);
	const farPec = shadowOf(tint(skin), tint(L.ambient), 0.25);
	const open = jaw > 0.002;
	const jr = rotAbout(HINGE, JAW_MAX_DEG * jaw);
	const jawD = warp(warp(JAW, jr), bend);
	const bodyD = open ? w(BODY_UPPER) : w(BODY);
	// mouth interior + teeth: drawn BEHIND the body so the lips overlap the tooth roots
	const mouth = open
		? (() => {
				const up = JAW_TOP.map(([x, y]) => bend(x, y));
				const lo = JAW_TOP.map(([x, y]) => bend(...jr(x, y)));
				const poly = `M ${up.map((q) => q.join(' ')).join(' L ')} L ${lo
					.slice()
					.reverse()
					.map((q) => q.join(' '))
					.join(' L ')} Z`;
				const gum = shadowOf(tint('coral-1'), tint(L.ambient), 0.45);
				const tongue = shadowOf(tint('coral-2'), tint(L.ambient), 0.2);
				const tooth = tint('bone-1');
				const toothSh = shadowOf(tint('bone-1'), tint(L.ambient), 0.32);
				const teeth: React.ReactNode[] = [];
				const row = (pts: [number, number][], dir: 1 | -1, key: string) => {
					for (let i = 0; i < 9; i++) {
						const s0 = 0.08 + i * 0.1;
						const idx = Math.min(pts.length - 2, Math.floor(s0 * (pts.length - 1)));
						const f = s0 * (pts.length - 1) - idx;
						const [ax, ay] = pts[idx];
						const [bx, by] = pts[idx + 1];
						const x = ax + (bx - ax) * f;
						const y = ay + (by - ay) * f;
						let nx = -(by - ay);
						let ny = bx - ax;
						const l = Math.hypot(nx, ny) || 1;
						nx = (nx / l) * dir;
						ny = (ny / l) * dir;
						const tx = (bx - ax) / (Math.hypot(bx - ax, by - ay) || 1);
						const ty = (by - ay) / (Math.hypot(bx - ax, by - ay) || 1);
						const hgt = (11 + 4 * Math.sin(i * 1.7)) * Math.min(1, jaw * 2.2);
						const wd = 4.6;
						const tip: [number, number] = [x + nx * hgt + tx * 1.5, y + ny * hgt + ty * 1.5];
						teeth.push(
							<g key={`${key}${i}`}>
								<path d={`M ${x - tx * wd} ${y - ty * wd} Q ${tip[0] - tx * 2} ${tip[1] - ty * 2} ${tip[0]} ${tip[1]} Q ${x + tx * wd * 0.6} ${y + ty * wd * 0.6} ${x + tx * wd} ${y + ty * wd} Z`} fill={tooth} />
								<path d={`M ${x} ${y} Q ${tip[0] + tx * 1} ${tip[1] + ty * 1} ${tip[0]} ${tip[1]} Q ${x + tx * wd * 0.6} ${y + ty * wd * 0.6} ${x + tx * wd} ${y + ty * wd} Z`} fill={toothSh} />
							</g>,
						);
					}
				};
				row(up, 1, 'u');
				row(lo, -1, 'l');
				const tc = lo[2];
				return (
					<g>
						<path d={poly} fill={gum} />
						<ellipse cx={tc[0] + 10} cy={tc[1] - 6 * jaw} rx={44} ry={9 + 6 * jaw} fill={tongue} transform={`rotate(${(JAW_MAX_DEG * jaw * 0.7).toFixed(2)} ${tc[0]} ${tc[1]})`} />
						{teeth}
					</g>
				);
			})()
		: null;

	return (
		<g transform={`translate(700 215) scale(${br}) translate(-700 -215)`}>
			{/* far flipper, behind the body: darker (occluded), supporting-level shading */}
			<g transform={pecFar}>
				<Shaded id={`${id}-pf`} parts={[{d: PEC, base: farPec}]} R={40} lod="support" xf={{rot, sx: flip ? -1 : 1}} layers={layers} />
			</g>
			{mouth}
			<Shaded
				id={`${id}-b`}
				box={[14, 128, 976, 180]}
				maskBox={[10, finTop, 1000, (open ? 470 : 420) - 62 - finTop]}
				R={96}
				core={0.4}
				hi={0.1}
				hiWidth={0.16}
				rimW={3.4}
				rimOpacity={0.8}
				stippleBand={18}
				dot={1.1}
				xf={{rot, sx: flip ? -1 : 1}}
				layers={layers}
				cast={cast ? {y: cast.y, lift: cast.lift ?? 0.6, spread: 1.1, opacity: 0.55} : undefined}
				parts={[
					{d: w(FLUKE), base: skin, marks: [{kind: 'scar', n: 1, size: 7, angle: 200, dL: 0.1, opacity: 0.45}]},
					{
						d: w(dorsal),
						base: skin,
						marks: [
							{kind: 'scar', n: 2, size: 7, angle: 250, dL: 0.12, opacity: 0.45, area: [590, -20, 70, 120]},
							{kind: 'pore', n: 5, size: 9, dL: 0.07, area: [580, 0, 90, 130]},
						],
					},
					{
						d: bodyD,
						base: skin,
						marks: [
							{kind: 'scar', n: 4, size: 9, angle: 158, dL: 0.12, opacity: 0.5, area: [560, 150, 230, 80]},
							{kind: 'scar', n: 2, size: 7, angle: 20, dL: 0.1, opacity: 0.4, area: [300, 180, 140, 50]},
							{kind: 'pore', n: 16, size: 8, dL: 0.07, area: [820, 150, 150, 70]},
							{kind: 'dash', n: 6, size: 10, angle: 175, dL: 0.06, opacity: 0.7, area: [380, 160, 400, 80]},
						],
					},
					...(open ? [{d: jawD, base: skin, marks: [{kind: 'pore' as const, n: 4, size: 7, dL: 0.07, area: [900, 236, 70, 24] as [number, number, number, number]}]}] : []),
					{d: w(SADDLE), base: mixOk(c('bone-0'), c('tide-0'), 0.55), clip: true, opacity: 0.5, stipple: false},
					...(detail
						? [
								{d: w(MELON), base: mixOk(c('ink-1'), c('tide-1'), 0.28), clip: true, stipple: false, opacity: 0.85},
								{d: w(PEC_ROOT), base: shadowOf(c('ink-1'), c('ink-0'), 0.6), clip: true, stipple: false},
							]
						: []),
					{d: w(EYE_PATCH), base: detail ? mixOk(c('bone-1'), c('amber-4'), 0.16) : 'bone-1', clip: true, hi: 0.1, shade: 0.36, ambient: 'tide-1'},
					{
						d: w(BELLY),
						base: detail ? mixOk(c('bone-1'), c('amber-4'), 0.2) : 'bone-1',
						clip: true,
						hi: 0.1,
						shade: 0.42,
						ambient: 'tide-1',
						marks: [
							{kind: 'arc', n: 7, size: 12, dL: -0.06, opacity: 0.6, area: [800, 250, 160, 40]},
							{kind: 'scar', n: 2, size: 8, angle: 165, dL: -0.08, opacity: 0.45, area: [560, 255, 200, 40]},
						],
					},
				]}
				glints={[
					{cx: 770, cy: 146, rx: 70, ry: 4.5, rot: -2, o: 0.4},
					{cx: 900, cy: 168, rx: 26, ry: 4, rot: 22, o: 0.55},
					{cx: 640, cy: 30, rx: 34, ry: 3, rot: -66, o: 0.3},
					{cx: 420, cy: 168, rx: 40, ry: 3, rot: -9, o: 0.25},
				]}
				over={
					<g>
						{open ? null : <path d={w(MOUTH)} stroke={tint('ink-0')} strokeWidth={3.2} fill="none" strokeLinecap="round" opacity={0.9} />}
						<path d={w(BLOWHOLE)} stroke={tint('ink-0')} strokeWidth={3} fill="none" strokeLinecap="round" />
						{/* skin crease behind the eye and above the flipper (internal detail lines, ramp tone) */}
						<path d={w('M 852 238 C 840 252 826 262 808 268')} stroke={tint('ink-0')} strokeWidth={2.4} fill="none" strokeLinecap="round" opacity={0.6} />
						{detail ? (
							<g fill="none" strokeLinecap="round">
								<path d={w(CHEEK)} fill={mixOk(tint(skin), tint(L.keyColor), 0.1)} opacity={0.55} />
								<path d={w(FLUKE_RIDGE)} stroke={mixOk(tint(skin), tint('tide-3'), 0.3)} strokeWidth={2.6} opacity={0.55} />
								<path d={w(KEEL)} stroke={mixOk(tint(skin), tint(L.keyColor), 0.3)} strokeWidth={3} opacity={0.5} />
								<path d={w(WRINKLES)} stroke={tint('ink-0')} strokeWidth={2.2} opacity={0.55} />
								<path d={w('M 790 252 C 810 244 836 248 852 260')} stroke={mixOk(tint(skin), tint(L.keyColor), 0.35)} strokeWidth={2.6} opacity={0.6} />
								<path d={w('M 862 176 C 880 168 906 168 922 176')} stroke={mixOk(tint(skin), tint(L.keyColor), 0.3)} strokeWidth={2.2} opacity={0.45} />
							</g>
						) : null}
					</g>
				}
				top={<Eye cx={900} cy={bend(900, 206)[1]} r={detail ? 10.5 : 9} iris="ochre-0" lid={lid} blink={blink} look={look} />}
			/>
			{/* near flipper: shaded on its own (it's a separate solid in front of the body) */}
			<g transform={pecNear}>
				<Shaded
					id={`${id}-pn`}
					R={46}
					core={0.42}
					rimW={5}
					stippleBand={12}
					xf={{rot: rot + flip1, sx: flip ? -1 : 1}}
					layers={layers}
					parts={[{d: PEC, base: skin, marks: [{kind: 'dash', n: 3, size: 9, angle: 120, dL: 0.07}]}]}
					glints={[{cx: 790, cy: 300, rx: 22, ry: 3, rot: 120, o: 0.4}]}
				/>
			</g>
		</g>
	);
};
