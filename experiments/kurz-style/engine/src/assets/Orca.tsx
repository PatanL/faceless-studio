/**
 * Hero orca, side view facing right, drawn fresh for the house style (not traced from any reference).
 * Local space: snout at x≈990, fluke tips at x≈15, back at y≈131, belly at y≈300, dorsal tip at y≈-58.
 *
 * Built as FLAT coloured parts (ink-1 skin, bone eye patch / belly / flank lobe, tide-tinted saddle), handed to
 * <Shaded>, which adds the whole light stack from the scene light. Motion: travelling-wave tail beat (vertical,
 * whale-style), flipper follow-through lagging the body, breathing, seeded blinks.
 */
import React from 'react';
import {c, mixOk, shadowOf} from '../lib/color';
import {swimBend, warp} from '../lib/geom';
import {useLight, useTint} from '../lib/light';
import {Eye, Shaded, type Layers} from '../shade/Shaded';
import {blinkAt, breathe} from '../motion/motion';

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
}> = ({id, t, amp = 1, freq = 0.55, lod = 'hero', layers, rot = 0, flip = false, cast}) => {
	const tint = useTint();
	const L = useLight();
	const bend = swimBend({head: 990, tail: 15, amp: 26 * amp, t, freq, lag: 1.9});
	const w = (d: string) => warp(d, bend);
	// flipper: follow-through, lags the body wave by ~0.18 s and adds its own paddle
	const flip1 = 7 * Math.sin(2 * Math.PI * freq * (t - 0.18)) + 3 * Math.sin(2 * Math.PI * 0.21 * t);
	const pecNear = `rotate(${flip1.toFixed(2)} 812 268)`;
	const pecFar = `translate(34 -26) rotate(${(-flip1 * 0.8 - 8).toFixed(2)} 812 268) translate(812 268) scale(0.82) translate(-812 -268)`;

	if (lod === 'far') {
		const col = tint('ink-1');
		return (
			<g>
				<path d={PEC} transform={pecFar} fill={col} />
				<path d={w(FLUKE)} fill={col} />
				<path d={w(DORSAL)} fill={col} />
				<path d={w(BODY)} fill={col} />
				<path d={PEC} transform={pecNear} fill={col} />
			</g>
		);
	}

	const skin = 'ink-1';
	const br = breathe(t, id, 0.01, 3.6);
	const blink = blinkAt(t, id);
	const farPec = shadowOf(tint(skin), tint(L.ambient), 0.25);

	return (
		<g transform={`translate(700 215) scale(${br}) translate(-700 -215)`}>
			{/* far flipper, behind the body: darker (occluded), supporting-level shading */}
			<g transform={pecFar}>
				<Shaded id={`${id}-pf`} parts={[{d: PEC, base: farPec}]} R={40} lod="support" xf={{rot, sx: flip ? -1 : 1}} layers={layers} />
			</g>
			<Shaded
				id={`${id}-b`}
				box={[14, 128, 976, 180]}
				maskBox={[10, -62, 1000, 420]}
				R={96}
				core={0.4}
				hi={0.1}
				hiWidth={0.16}
				rimW={5.5}
				stippleBand={18}
				dot={1.1}
				xf={{rot, sx: flip ? -1 : 1}}
				layers={layers}
				cast={cast ? {y: cast.y, lift: cast.lift ?? 0.6, spread: 1.1, opacity: 0.55} : undefined}
				parts={[
					{d: w(FLUKE), base: skin, marks: [{kind: 'scar', n: 1, size: 7, angle: 200, dL: 0.1, opacity: 0.45}]},
					{
						d: w(DORSAL),
						base: skin,
						marks: [
							{kind: 'scar', n: 2, size: 7, angle: 250, dL: 0.12, opacity: 0.45, area: [590, -20, 70, 120]},
							{kind: 'pore', n: 5, size: 9, dL: 0.07, area: [580, 0, 90, 130]},
						],
					},
					{
						d: w(BODY),
						base: skin,
						marks: [
							{kind: 'scar', n: 4, size: 9, angle: 158, dL: 0.12, opacity: 0.5, area: [560, 150, 230, 80]},
							{kind: 'scar', n: 2, size: 7, angle: 20, dL: 0.1, opacity: 0.4, area: [300, 180, 140, 50]},
							{kind: 'pore', n: 16, size: 8, dL: 0.07, area: [820, 150, 150, 70]},
							{kind: 'dash', n: 6, size: 10, angle: 175, dL: 0.06, opacity: 0.7, area: [380, 160, 400, 80]},
						],
					},
					{d: w(SADDLE), base: mixOk(c('bone-0'), c('tide-0'), 0.55), clip: true, opacity: 0.5, stipple: false},
					{d: w(EYE_PATCH), base: 'bone-1', clip: true, hi: 0.1, shade: 0.24},
					{
						d: w(BELLY),
						base: 'bone-1',
						clip: true,
						hi: 0.1,
						shade: 0.24,
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
						<path d={w(MOUTH)} stroke={tint('ink-0')} strokeWidth={3.2} fill="none" strokeLinecap="round" opacity={0.9} />
						<path d={w(BLOWHOLE)} stroke={tint('ink-0')} strokeWidth={3} fill="none" strokeLinecap="round" />
						{/* skin crease behind the eye and above the flipper (internal detail lines, ramp tone) */}
						<path d={w('M 852 238 C 840 252 826 262 808 268')} stroke={tint('ink-0')} strokeWidth={2.4} fill="none" strokeLinecap="round" opacity={0.6} />
					</g>
				}
				top={<Eye cx={900} cy={bend(900, 206)[1]} r={9} iris="ochre-0" lid={0.28} blink={blink} look={[0.4, 0.1]} />}
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
