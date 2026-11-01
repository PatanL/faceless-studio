/**
 * Sea creatures, flat 2D vector style. All face RIGHT; head at high x.
 * Original drawings built from simple curves; idle motion bends the whole outline
 * with a travelling wave so fins and details stay attached.
 */
import React from 'react';
import {paint, type DrawCtx, type Figure} from './figure';
import {bool, clamp, curl, num, ribbon, rnd, swimWarp, track, warp, type Pt, type Warp} from './util';
import {ORCA_POSES} from './orca_kit';

const Grad: React.FC<{id: string; top: string; bottom: string; angle?: 'v' | 'h'}> = ({id, top, bottom, angle = 'v'}) => (
	<linearGradient id={id} x1="0" y1="0" x2={angle === 'h' ? '1' : '0'} y2={angle === 'h' ? '0' : '1'}>
		<stop offset="0" stopColor={top} />
		<stop offset="1" stopColor={bottom} />
	</linearGradient>
);

const Eye: React.FC<{c: DrawCtx; x: number; y: number; r: number; iris?: string; glint?: boolean}> = ({c, x, y, r, iris = '#0b0d10', glint = true}) =>
	c.sil ? null : (
		<g>
			<circle cx={x} cy={y} r={r} fill={iris} />
			{glint ? <circle cx={x + r * 0.3} cy={y - r * 0.32} r={r * 0.32} fill="#ffffff" opacity={0.85} /> : null}
		</g>
	);

/** apply warp to a point */
const wp = (f: Warp | undefined, x: number, y: number): Pt => (f ? f(x, y) : [x, y]);

// ================================================================ sperm whale

const SW_BODY =
	'M 175 150 C 260 132 360 112 470 100 C 500 96 520 84 545 86 C 565 88 580 96 600 96 C 700 84 820 74 930 76 C 968 77 990 96 992 130 L 990 196 C 988 214 972 226 945 228 C 860 232 780 236 700 236 C 560 238 430 222 330 196 C 270 182 215 170 175 166 Z';
const SW_FLUKE = 'M 192 146 C 150 134 90 104 28 90 C 55 120 72 145 84 158 C 72 172 55 198 28 228 C 92 214 150 184 192 170 Z';
const SW_KNUCKLES =
	'M 250 142 Q 262 130 274 138 Q 288 126 300 133 Q 314 121 326 128 Q 340 117 352 123 Q 366 112 380 118 Q 394 106 408 112 L 408 132 L 250 152 Z';
const SW_BELLY = 'M 360 202 C 470 226 600 232 720 230 C 820 228 900 224 962 222 C 940 232 880 238 700 240 C 560 242 440 228 360 202 Z';
const SW_TOP = 'M 610 98 C 700 86 820 76 930 78 C 966 79 986 96 990 126 C 960 104 900 96 820 98 C 740 100 670 106 610 98 Z';
const SW_FLIPPER = 'M 700 228 C 682 254 652 274 616 284 C 636 262 650 246 656 230 Z';
const SW_JAW = 'M 712 226 C 790 220 880 218 958 220 C 962 228 952 236 930 238 C 860 240 780 240 712 238 Z';

const spermWhale: Figure = {
	label: 'SPERM WHALE',
	box: [28, 76, 964, 208],
	size: 16,
	axis: 'w',
	draw: (c) => {
		const f = c.idle ? swimWarp({head: 990, tail: 30, amp: 15 * c.amp, t: c.t, freq: 0.42 * c.speed, k: 2.0}) : undefined;
		const id = c.id;
		const jaw = num(c.p.jaw, 0); // degrees open
		const teeth = bool(c.p.teeth, false) || jaw > 0;
		const body = warp(SW_BODY, f);
		const wrinkles: React.ReactNode[] = [];
		if (!c.sil) {
			for (let i = 0; i < 46; i++) {
				const x = 300 + i * 15 + rnd(`sw-w${i}`) * 8;
				const y0 = 70 + rnd(`sw-a${i}`) * 50;
				const y1 = y0 + 40 + rnd(`sw-b${i}`) * 90;
				wrinkles.push(<path key={i} d={warp(`M ${x} ${y0} L ${x - 3} ${y1}`, f)} stroke="#3c434a" strokeWidth={2.2} opacity={0.18} />);
			}
		}
		const hinge = wp(f, 712, 228);
		const teethEl = teeth && !c.sil
			? Array.from({length: 11}, (_, i) => {
					const x = 760 + i * 17;
					return <path key={i} d={warp(`M ${x} 222 L ${x + 6} 207 L ${x + 12} 222 Z`, f)} fill="#f2efe6" />;
			  })
			: null;
		return (
			<g>
				<defs>
					<Grad id={`${id}-g`} top={paint(c, '#666d74')} bottom={paint(c, '#99a0a6')} />
					<clipPath id={`${id}-clip`}>
						<path d={body} />
					</clipPath>
				</defs>
				<path d={warp(SW_FLUKE, f)} fill={paint(c, '#5f666d')} />
				{jaw > 0 && !c.sil ? <path d={warp('M 712 228 C 800 226 880 224 958 222 L 958 250 C 880 262 780 262 712 240 Z', f)} fill="#2a1718" /> : null}
				<path d={body} fill={`url(#${id}-g)`} />
				<path d={warp(SW_KNUCKLES, f)} fill={paint(c, '#6a7178')} />
				<g clipPath={`url(#${id}-clip)`}>
					{c.sil ? null : <path d={warp(SW_BELLY, f)} fill="#b3b9bd" opacity={0.55} />}
					{c.sil ? null : <path d={warp(SW_TOP, f)} fill="#555c63" opacity={0.45} />}
					{wrinkles}
				</g>
				<g transform={`rotate(${jaw} ${hinge[0]} ${hinge[1]})`}>
					{teethEl}
					<path d={warp(SW_JAW, f)} fill={paint(c, '#8c9399')} />
				</g>
				{c.sil ? null : <path d={warp('M 718 224 C 800 218 880 216 956 220', f)} stroke="#3a4046" strokeWidth={3} fill="none" opacity={0.7} />}
				<path d={warp(SW_FLIPPER, f)} fill={paint(c, '#5c636a')} />
				<Eye c={c} x={wp(f, 744, 200)[0]} y={wp(f, 744, 200)[1]} r={6.5} />
			</g>
		);
	},
};

// ================================================================ colossal squid

const SQ_MANTLE = 'M 70 180 C 70 118 160 92 300 96 C 420 99 500 120 532 150 L 532 212 C 500 242 420 262 300 264 C 160 268 70 242 70 180 Z';
const SQ_FINS = 'M 150 180 C 120 112 66 70 20 56 C 40 106 68 150 96 180 C 68 210 40 254 20 304 C 66 290 120 248 150 180 Z';
const SQ_HEAD = 'M 520 140 C 560 128 604 138 628 158 L 628 204 C 604 224 560 232 520 222 Z';

function squidArms(c: DrawCtx, front: boolean): React.ReactNode {
	const out: React.ReactNode[] = [];
	const n = 10;
	const sp = c.speed;
	for (let i = 0; i < n; i++) {
		const isTentacle = i === 3 || i === 6;
		if ((i % 2 === 0) !== front && !isTentacle) continue;
		if (isTentacle && front) continue;
		const y0 = 150 + (i / (n - 1)) * 58;
		const spread = (i - (n - 1) / 2) * (isTentacle ? 2.2 : 4.6);
		const len = isTentacle ? 390 : 230 + rnd(`sqa${i}`) * 60;
		const ph = i * 0.9;
		const amp = c.idle ? 3.4 * c.amp : 0;
		const curlDir = i < n / 2 ? -1 : 1;
		const pts = curl([614, y0], spread, len, 24, (s) => amp * Math.sin(c.t * 2.2 * sp - s * 5 + ph) + (isTentacle ? 0 : curlDir * 4.5 * s * s + spread * -0.04));
		const widths = pts.map((_, k) => {
			const s = k / (pts.length - 1);
			const base = isTentacle ? 13 : 34;
			if (isTentacle && s > 0.78) return 22 * Math.sin(((s - 0.78) / 0.22) * Math.PI) + 4; // club
			return Math.max(2.5, base * Math.pow(1 - s, 0.8) * 0.95 + 2);
		});
		out.push(<path key={i} d={ribbon(pts, widths)} fill={paint(c, front ? '#a6352c' : '#7c241f')} />);
		if (!c.sil && front && bool(c.p.hooks, true)) {
			for (let h = 3; h < pts.length - 4; h += 3) {
				const [x, y] = pts[h];
				out.push(<path key={`h${i}-${h}`} d={`M ${x - 4} ${y + 2} Q ${x} ${y - 9} ${x + 5} ${y - 4}`} stroke="#f1e6d6" strokeWidth={2.6} fill="none" strokeLinecap="round" />);
			}
		}
	}
	return out;
}

const colossalSquid: Figure = {
	label: 'COLOSSAL SQUID',
	box: [20, 56, 980, 248],
	size: 9,
	axis: 'w',
	draw: (c) => {
		const breathe = c.idle ? 1 + 0.025 * Math.sin(c.t * 2.4 * c.speed) : 1;
		const fin = c.idle ? Math.sin(c.t * 3 * c.speed) * 6 : 0;
		const spots = c.sil
			? null
			: Array.from({length: 26}, (_, i) => (
					<circle key={i} cx={110 + rnd(`sq-x${i}`) * 400} cy={115 + rnd(`sq-y${i}`) * 130} r={3 + rnd(`sq-r${i}`) * 7} fill="#661a16" opacity={0.5} />
			  ));
		return (
			<g>
				<defs>
					<Grad id={`${c.id}-g`} top={paint(c, '#8a2620')} bottom={paint(c, '#c04a3b')} />
					<clipPath id={`${c.id}-clip`}>
						<path d={SQ_MANTLE} />
					</clipPath>
				</defs>
				{squidArms(c, false)}
				<g transform={`translate(150 180) scale(1 ${1 + fin / 60}) translate(-150 -180)`}>
					<path d={SQ_FINS} fill={paint(c, '#7a221d')} />
				</g>
				<g transform={`translate(300 180) scale(1 ${breathe}) translate(-300 -180)`}>
					<path d={SQ_MANTLE} fill={`url(#${c.id}-g)`} />
					<g clipPath={`url(#${c.id}-clip)`}>
						{spots}
						{c.sil ? null : <path d="M 70 222 C 200 250 400 250 532 214 L 532 270 L 70 270 Z" fill="#d86a56" opacity={0.25} />}
					</g>
				</g>
				<path d={SQ_HEAD} fill={paint(c, '#a93a2f')} />
				{squidArms(c, true)}
				{c.sil ? null : (
					<g>
						<circle cx={575} cy={180} r={30} fill="#f0c27b" />
						<circle cx={575} cy={180} r={25} fill="#140707" />
						<circle cx={584} cy={171} r={7} fill="#ffffff" opacity={0.85} />
					</g>
				)}
			</g>
		);
	},
};

// ================================================================ orca
// Blunt rounded melon, tall straight dorsal, big paddle flippers, white chin/belly with the
// flank lobe that sweeps up behind the dorsal, eye patch above-behind the eye, grey saddle.

const OR_BODY =
	'M 150 200 C 240 180 360 150 500 140 C 640 130 780 134 878 160 C 948 178 994 202 994 224 C 994 246 962 260 904 268 C 764 286 562 286 402 266 C 292 252 212 228 150 214 Z';
const OR_FIN = 'M 648 142 C 624 104 604 52 596 2 C 570 52 532 102 500 148 Z';
const OR_FLUKE = 'M 166 200 C 124 188 74 170 20 160 C 44 182 54 197 58 207 C 54 217 44 234 20 256 C 74 244 124 226 166 214 Z';
const OR_WHITE =
	'M 1000 230 C 962 242 908 250 836 252 C 736 254 640 254 574 250 C 530 247 498 232 468 212 C 446 198 424 198 412 210 C 398 228 378 246 330 260 L 330 330 L 1000 330 Z';
const OR_PATCH = 'M 806 182 C 828 166 878 162 904 174 C 886 192 838 198 806 182 Z';
const OR_SADDLE = 'M 420 152 C 470 138 540 134 600 140 C 560 162 480 166 420 152 Z';
const OR_FLIPPER = 'M 808 258 C 800 300 772 340 732 354 C 708 360 704 338 718 312 C 732 288 752 270 770 260 Z';

/** finScale: dorsal fin height multiplier about its base (an adult male's fin is ~1.8 m: finScale 1.5) */
const orcaFin = (s: number) =>
	s === 1 ? OR_FIN : OR_FIN.replace(/(-?[\d.]+) (-?[\d.]+)/g, (_m, x, y) => `${x} ${(145 - (145 - Number(y)) * s).toFixed(1)}`);

const orca: Figure = {
	label: 'ORCA',
	box: [20, 2, 974, 356],
	size: 8,
	axis: 'w',
	poses: ORCA_POSES,
	draw: (c) => {
		const f = c.idle ? swimWarp({head: 994, tail: 20, amp: 14 * c.amp, t: c.t, freq: 0.6 * c.speed}) : undefined;
		const body = warp(OR_BODY, f);
		const [ex, ey] = wp(f, 916, 206);
		return (
			<g>
				<defs>
					<clipPath id={`${c.id}-clip`}>
						<path d={body} />
					</clipPath>
				</defs>
				<path d={warp(OR_FLUKE, f)} fill={paint(c, '#121518')} />
				<path d={warp(orcaFin(num(c.p.finScale, 1)), f)} fill={paint(c, '#15181b')} />
				<path d={body} fill={paint(c, '#191c20')} />
				<g clipPath={`url(#${c.id}-clip)`}>
					{c.sil ? null : <path d={warp(OR_WHITE, f)} fill="#eef2f3" />}
					{c.sil ? null : <path d={warp(OR_SADDLE, f)} fill="#8b9399" opacity={0.55} />}
					{c.sil ? null : <path d={warp('M 150 196 C 320 160 620 134 940 176 L 940 156 C 620 116 320 138 150 180 Z', f)} fill="#2a2f35" opacity={0.5} />}
				</g>
				{c.sil ? null : <path d={warp(OR_PATCH, f)} fill="#eef2f3" />}
				{c.sil ? null : <path d={warp('M 994 228 C 962 234 934 232 912 224', f)} stroke="#000" strokeWidth={3} fill="none" opacity={0.55} strokeLinecap="round" />}
				<path d={warp(OR_FLIPPER, f)} fill={paint(c, '#101316')} />
				<Eye c={c} x={ex} y={ey} r={5} iris="#000" />
			</g>
		);
	},
};

// ================================================================ great white

const GW_BODY =
	'M 160 190 C 260 160 400 125 560 120 C 700 116 830 140 920 175 C 960 190 990 205 994 212 C 976 228 930 240 870 245 C 760 255 600 262 460 252 C 340 244 240 222 160 205 Z';
const GW_BELLY =
	'M 994 212 L 905 224 L 860 219 L 815 233 L 775 226 L 725 240 L 675 235 L 615 248 L 540 245 L 460 250 L 380 242 L 300 232 L 300 300 L 994 300 Z';
const GW_DORSAL = 'M 660 124 C 620 82 560 42 512 22 C 525 60 520 100 500 128 Z';
const GW_TAIL = 'M 178 188 C 140 158 90 100 40 48 C 70 110 86 160 96 196 C 86 226 70 262 48 300 C 96 270 140 236 178 206 Z';
const GW_PEC = 'M 770 238 C 740 290 696 330 640 352 C 680 312 702 272 708 244 Z';

const greatWhite: Figure = {
	label: 'GREAT WHITE',
	box: [40, 22, 954, 330],
	size: 6,
	axis: 'w',
	draw: (c) => {
		const f = c.idle ? swimWarp({head: 994, tail: 40, amp: 10 * c.amp, t: c.t, freq: 0.9 * c.speed, k: 3}) : undefined;
		// lateral tail beat reads as the caudal fin narrowing/widening in side view
		const beat = c.idle ? 0.78 + 0.22 * Math.cos(c.t * Math.PI * 2 * 0.9 * c.speed) : 1;
		const tf: Warp = (x, y) => {
			const [a, b] = f ? f(x, y) : [x, y];
			return x < 180 ? [180 - (180 - a) * beat, b] : [a, b];
		};
		const body = warp(GW_BODY, f);
		return (
			<g>
				<defs>
					<Grad id={`${c.id}-g`} top={paint(c, '#55636f')} bottom={paint(c, '#7d8b95')} />
					<clipPath id={`${c.id}-clip`}>
						<path d={body} />
					</clipPath>
				</defs>
				<path d={warp(GW_TAIL, tf)} fill={paint(c, '#5a6873')} />
				<path d={warp(GW_DORSAL, f)} fill={paint(c, '#55636e')} />
				<path d={warp('M 285 165 L 252 142 L 262 170 Z', f)} fill={paint(c, '#5a6873')} />
				<path d={warp('M 300 228 L 266 250 L 268 222 Z', f)} fill={paint(c, '#5a6873')} />
				<path d={body} fill={`url(#${c.id}-g)`} />
				<g clipPath={`url(#${c.id}-clip)`}>{c.sil ? null : <path d={warp(GW_BELLY, f)} fill="#e7ebed" />}</g>
				{c.sil
					? null
					: [0, 1, 2, 3, 4].map((i) => (
							<path key={i} d={warp(`M ${712 + i * 16} ${168 + i} C ${716 + i * 16} 186 ${716 + i * 16} 204 ${712 + i * 16} ${220 - i}`, f)} stroke="#3c4750" strokeWidth={3} fill="none" opacity={0.55} />
					  ))}
				{c.sil ? null : <path d={warp('M 966 224 C 930 234 888 238 846 232', f)} stroke="#2a3138" strokeWidth={3.5} fill="none" strokeLinecap="round" />}
				<path d={warp(GW_PEC, f)} fill={paint(c, '#4f5d68')} />
				<Eye c={c} x={wp(f, 884, 184)[0]} y={wp(f, 884, 184)[1]} r={7} iris="#050607" />
			</g>
		);
	},
};

// ================================================================ blue whale

const BW_BODY =
	'M 150 110 C 260 92 420 76 600 72 C 760 70 880 76 960 92 C 985 98 995 108 993 118 C 985 132 950 140 900 146 C 760 156 600 158 440 150 C 320 142 220 126 150 120 Z';
const BW_FLUKE = 'M 162 108 C 120 98 70 74 20 60 C 45 90 55 108 60 115 C 55 124 45 142 20 170 C 70 156 120 132 162 122 Z';
const BW_FIN = 'M 322 92 C 300 80 282 72 262 68 C 268 80 274 90 284 97 Z';
const BW_FLIPPER = 'M 826 140 C 806 172 772 192 730 202 C 760 176 780 156 792 142 Z';

/**
 * Lunge-feeding mouth for the blue whale. gape 0..1 (number or [{t, v}] track): the lower jaw
 * drops ~30 deg about the mouth corner, the pleated throat pouch balloons under the body and the
 * black baleen fringe shows under the upper jaw. Drawn over the closed body, so gape 0 = no change.
 */
const bwMouth = (c: DrawCtx, f: Warp | undefined, g: number) => {
	if (g <= 0.001) return null;
	const H: Pt = [806, 127]; // mouth corner (hinge)
	const S: Pt = [993, 117]; // snout tip
	const th = (g * 30 * Math.PI) / 180;
	const rot = ([x, y]: Pt): Pt => [H[0] + (x - H[0]) * Math.cos(th) - (y - H[1]) * Math.sin(th), H[1] + (x - H[0]) * Math.sin(th) + (y - H[1]) * Math.cos(th)];
	const T = rot([988, 123]); // lower-jaw tip
	const J1 = rot([900, 131]);
	const J2 = rot([900, 141]);
	const T2 = rot([984, 131]);
	const P = (p: Pt) => wp(f, p[0], p[1]).map((v) => v.toFixed(1)).join(' ');
	const drop = 118 * g; // throat pouch depth (drawing units)
	const pouch = `M ${P(T)} C ${P([T[0] - 30, T[1] + 40 * g])} ${P([800, 156 + drop])} ${P([700, 154 + drop * 0.95])} C ${P([600, 152 + drop * 0.8])} ${P([500, 160 + drop * 0.3])} ${P([420, 148])} L ${P([600, 150])} L ${P(H)} Z`;
	const pleats = c.sil
		? null
		: Array.from({length: 9}, (_, i) => {
				const k = (i + 1) / 10;
				const a = rot([988 - k * 40, 123 + k * 18]);
				return (
					<path
						key={i}
						d={`M ${P(a)} C ${P([820 - k * 20, 150 + drop * k])} ${P([680, 152 + drop * k * 0.95])} ${P([440 + k * 60, 150 + drop * k * 0.15])}`}
						stroke="#5f7f96"
						strokeWidth={2.4}
						fill="none"
						opacity={0.55}
					/>
				);
		  });
	const baleen = c.sil
		? null
		: Array.from({length: 26}, (_, i) => {
				const x = 820 + i * 6.6;
				const y = 117 + ((993 - x) / 187) * 9;
				const len = (8 + 14 * g) * (0.6 + 0.4 * Math.sin((i / 25) * Math.PI));
				return <path key={i} d={`M ${P([x, y])} L ${P([x - 3, y + len])}`} stroke="#15171b" strokeWidth={4.2} strokeLinecap="round" />;
		  });
	const inside = `M ${P(S)} C ${P([950, 117])} ${P([870, 120])} ${P(H)} L ${P(T)} Q ${P([(S[0] + T[0]) / 2 + 14, (S[1] + T[1]) / 2])} ${P(S)} Z`;
	const tongue = `M ${P(rot([840, 128]))} Q ${P(rot([900, 112]))} ${P(rot([960, 126]))} Z`;
	return (
		<g>
			<path d={pouch} fill={paint(c, '#9fb9c9')} />
			{pleats}
			<path d={inside} fill={paint(c, '#2b1a24')} />
			{c.sil ? null : <path d={tongue} fill="#b9727c" opacity={0.9} />}
			{baleen}
			<path d={`M ${P(H)} L ${P(J1)} L ${P(T)} L ${P(T2)} L ${P(J2)} Z`} fill={paint(c, '#46698a')} />
		</g>
	);
};

const blueWhale: Figure = {
	label: 'BLUE WHALE',
	box: [20, 60, 975, 142],
	size: 28,
	axis: 'w',
	draw: (c) => {
		const f = c.idle ? swimWarp({head: 993, tail: 20, amp: 9 * c.amp, t: c.t, freq: 0.3 * c.speed, k: 1.8}) : undefined;
		const gape = clamp(track(c.p.gape, c.t, 0));
		const body = warp(BW_BODY, f);
		const mottle = c.sil
			? null
			: Array.from({length: 40}, (_, i) => {
					const x = 200 + rnd(`bw-x${i}`) * 720;
					const y = 80 + rnd(`bw-y${i}`) * 50;
					const [a, b] = wp(f, x, y);
					return <ellipse key={i} cx={a} cy={b} rx={4 + rnd(`bw-r${i}`) * 9} ry={2 + rnd(`bw-q${i}`) * 4} fill="#b8cfdc" opacity={0.28} />;
			  });
		return (
			<g>
				<defs>
					<Grad id={`${c.id}-g`} top={paint(c, '#46698a')} bottom={paint(c, '#7397b0')} />
					<clipPath id={`${c.id}-clip`}>
						<path d={body} />
					</clipPath>
				</defs>
				<path d={warp(BW_FLUKE, f)} fill={paint(c, '#46698a')} />
				<path d={warp(BW_FIN, f)} fill={paint(c, '#46698a')} />
				<path d={body} fill={`url(#${c.id}-g)`} />
				<g clipPath={`url(#${c.id}-clip)`}>
					{mottle}
					{c.sil
						? null
						: [0, 1, 2, 3, 4, 5].map((i) => (
								<path key={i} d={warp(`M 992 ${120 + i * 4} C 900 ${134 + i * 4} 780 ${142 + i * 3} 640 ${146 + i * 2}`, f)} stroke="#2f4c66" strokeWidth={2} fill="none" opacity={0.45} />
						  ))}
				</g>
				{c.sil || gape > 0.001 ? null : <path d={warp('M 993 116 C 960 114 910 112 868 109', f)} stroke="#203547" strokeWidth={2.5} fill="none" />}
				{bwMouth(c, f, gape)}
				<path d={warp(BW_FLIPPER, f)} fill={paint(c, '#3f6080')} />
				{/* eye just above and behind the mouth corner (hinge 806,127), not over the snout */}
				<Eye c={c} x={wp(f, 786, 117)[0]} y={wp(f, 786, 117)[1]} r={4.5} />
			</g>
		);
	},
};

// ================================================================ anglerfish

const AF_BODY =
	'M 120 220 C 120 130 220 72 340 70 C 450 68 530 128 548 200 L 562 248 C 540 302 470 352 360 360 C 230 366 128 310 120 220 Z';
const AF_TAIL = 'M 136 214 C 96 176 62 140 18 128 C 38 180 38 262 18 314 C 62 302 96 264 136 234 Z';

const anglerfish: Figure = {
	label: 'ANGLERFISH',
	box: [18, 0, 600, 366],
	size: 0.2,
	axis: 'w',
	draw: (c) => {
		const t = c.t * c.speed;
		const f = c.idle ? swimWarp({head: 560, tail: 18, amp: 12 * c.amp, t: c.t, freq: 0.7 * c.speed, k: 1.6, pow: 2.5}) : undefined;
		const glow = c.idle ? 0.75 + 0.25 * Math.sin(t * 3.1) : 1;
		const lx = 580 + (c.idle ? Math.sin(t * 1.3) * 10 : 0);
		const ly = 40 + (c.idle ? Math.sin(t * 1.9) * 8 : 0);
		const jaw = c.idle ? 4 + 4 * Math.sin(t * 0.9) : 4;
		const teethUp: React.ReactNode[] = [];
		const teethDn: React.ReactNode[] = [];
		if (!c.sil) {
			for (let i = 0; i < 9; i++) {
				const x = 440 + i * 14;
				const y = 214 + i * 2;
				teethUp.push(<path key={i} d={`M ${x} ${y} L ${x + 4} ${y + 22 + (i % 2) * 10} L ${x + 8} ${y} Z`} fill="#ece7da" />);
				teethDn.push(<path key={i} d={`M ${x - 6} ${262 - i} L ${x - 2} ${238 - i - (i % 2) * 10} L ${x + 2} ${262 - i} Z`} fill="#ece7da" />);
			}
		}
		const hinge: Pt = [430, 236];
		return (
			<g>
				<defs>
					<radialGradient id={`${c.id}-lure`}>
						<stop offset="0" stopColor="#d9fff4" stopOpacity={0.95} />
						<stop offset="0.25" stopColor="#7fffd9" stopOpacity={0.55} />
						<stop offset="1" stopColor="#3fe6c0" stopOpacity={0} />
					</radialGradient>
					<Grad id={`${c.id}-g`} top={paint(c, '#3d3533')} bottom={paint(c, '#2a2423')} />
				</defs>
				{c.sil ? null : <circle cx={lx} cy={ly} r={120 * glow} fill={`url(#${c.id}-lure)`} opacity={0.75} />}
				<path d={warp(AF_TAIL, f)} fill={paint(c, '#2f2827')} />
				<path d={warp('M 250 84 L 236 40 L 270 76 L 268 34 L 300 72 Z', f)} fill={paint(c, '#2f2827')} />
				<path d="M 562 248 C 520 230 470 226 430 236 L 562 236 Z" fill={paint(c, '#0a0607')} />
				<path d={warp(AF_BODY, f)} fill={`url(#${c.id}-g)`} />
				{c.sil ? null : <path d="M 440 214 C 490 206 530 206 552 214 L 562 248 C 520 250 470 250 430 240 Z" fill="#120a0b" />}
				{teethUp}
				<g transform={`rotate(${jaw} ${hinge[0]} ${hinge[1]})`}>
					{teethDn}
					<path d="M 430 252 C 480 266 540 268 576 252 C 566 300 520 330 460 330 C 440 310 432 280 430 252 Z" fill={paint(c, '#352e2c')} />
				</g>
				{c.sil
					? null
					: Array.from({length: 14}, (_, i) => (
							<circle key={i} cx={wp(f, 180 + rnd(`af-x${i}`) * 300, 0)[0]} cy={110 + rnd(`af-y${i}`) * 200} r={3 + rnd(`af-r${i}`) * 5} fill="#5a4d4a" opacity={0.6} />
					  ))}
				<path d={warp('M 300 280 C 270 310 240 330 210 336 C 236 312 256 290 266 272 Z', f)} fill={paint(c, '#27201f')} />
				<path d={`M 430 82 C 450 20 ${lx - 60} ${ly - 30} ${lx} ${ly}`} stroke={paint(c, '#3b3432')} strokeWidth={6} fill="none" strokeLinecap="round" />
				<circle cx={lx} cy={ly} r={11} fill={c.sil ? c.sil : '#e9fff8'} />
				<g>
					{c.sil ? null : <circle cx={478} cy={136} r={11} fill="#c9d3cf" />}
					<Eye c={c} x={478} y={136} r={6} glint={false} />
				</g>
			</g>
		);
	},
};

// ================================================================ giant pacific octopus

function octopusArms(c: DrawCtx, front: boolean): React.ReactNode {
	const out: React.ReactNode[] = [];
	const t = c.t * c.speed;
	for (let i = 0; i < 8; i++) {
		if ((i % 2 === 0) !== front) continue;
		const x0 = 230 + (i / 7) * 140;
		const side = i < 4 ? -1 : 1;
		const startA = 90 + side * (25 + Math.abs(i - 3.5) * 11);
		const amp = c.idle ? c.amp : 0;
		const pts = curl([x0, 300], startA, 300 + rnd(`oa${i}`) * 60, 26, (s) => {
			const wave = 5 * amp * Math.sin(t * 1.6 - s * 6 + i * 1.3);
			const coil = s > 0.6 ? -side * 18 * ((s - 0.6) / 0.4) : 0;
			return wave * 0.5 + coil;
		});
		const widths = pts.map((_, k) => Math.max(2, 46 * (1 - (k / (pts.length - 1)) * 0.94)));
		out.push(<path key={i} d={ribbon(pts, widths)} fill={paint(c, front ? '#b4523b' : '#8a3a2a')} />);
		if (front && !c.sil) {
			for (let k = 3; k < pts.length - 3; k += 2) {
				const s = k / (pts.length - 1);
				out.push(<circle key={`s${i}-${k}`} cx={pts[k][0]} cy={pts[k][1]} r={Math.max(1.6, 8 * (1 - s))} fill="#efb39c" opacity={0.85} />);
			}
		}
	}
	return out;
}

const octopus: Figure = {
	label: 'GIANT OCTOPUS',
	box: [10, 30, 580, 560],
	size: 6,
	axis: 'w',
	draw: (c) => {
		const br = c.idle ? 1 + 0.04 * Math.sin(c.t * 1.8 * c.speed) : 1;
		const mantle = 'M 300 40 C 404 36 456 118 446 200 C 438 262 396 292 344 302 L 256 302 C 204 292 162 262 154 200 C 144 118 196 44 300 40 Z';
		return (
			<g>
				<defs>
					<Grad id={`${c.id}-g`} top={paint(c, '#c4624a')} bottom={paint(c, '#943c2b')} />
				</defs>
				{octopusArms(c, false)}
				<g transform={`translate(300 300) scale(${br} ${br}) translate(-300 -300)`}>
					<path d={mantle} fill={`url(#${c.id}-g)`} />
					{c.sil
						? null
						: Array.from({length: 18}, (_, i) => (
								<circle key={i} cx={200 + rnd(`ox${i}`) * 200} cy={70 + rnd(`oy${i}`) * 180} r={4 + rnd(`or${i}`) * 8} fill="#7c2e20" opacity={0.45} />
						  ))}
				</g>
				{octopusArms(c, true)}
				{c.sil
					? null
					: [252, 348].map((x) => (
							<g key={x}>
								<ellipse cx={x} cy={268} rx={20} ry={16} fill="#d9765c" />
								<ellipse cx={x} cy={270} rx={12} ry={9} fill="#f2d48a" />
								<rect x={x - 9} y={267} width={18} height={5} rx={2.5} fill="#120807" />
							</g>
					  ))}
			</g>
		);
	},
};

export const MARINE: Record<string, Figure> = {
	spermWhale,
	colossalSquid,
	orca,
	greatWhite,
	blueWhale,
	anglerfish,
	octopus,
};

