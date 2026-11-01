// Horror chat-story thumbnails: flat 2D apartment at night, a huge threat (figure / phone),
// a tiny resident for scale, 2-4 words with one red word. Cold teal grade, no other red.
import React from 'react';
import {Grain, Headline, Vignette, layoutHeadline, rng, textWidthEm} from '../fx';
import {Resident, ShadowFigure} from '../art/people';
import {KitArt, hasKit} from '../art/KitArt';
import type {TplProps} from './explainer';
import type {ThumbSpec} from '../spec';

const WALL = '#1d2a2c';
const WALL_D = '#0d1517';
const COLD = '#a9d4de';

const Figure: React.FC<{spec: ThumbSpec; x: number; y: number; w: number; h: number; id: string; lean?: number}> = ({spec, ...b}) => {
	if (spec.art && hasKit(spec.art.component)) return <KitArt name={spec.art.component} props={spec.art.props} time={spec.art.time} {...b} />;
	return <ShadowFigure {...b} />;
};

const Tiny: React.FC<{spec: ThumbSpec; x: number; y: number; h: number; id: string; glow?: boolean; flip?: boolean}> = ({spec, ...b}) => {
	const ha = spec.humanArt;
	if (ha && hasKit(ha.component)) {
		const w = b.h * 0.6;
		return <KitArt name={ha.component} props={ha.props} time={ha.time} x={b.x - w / 2} y={b.y - b.h} w={w} h={b.h} flip={b.flip} />;
	}
	return <Resident {...b} />;
};

const Plate: React.FC<{x: number; y: number; size: number; text: string}> = ({x, y, size, text}) => (
	<g>
		<rect x={x - size * 1.3} y={y - size * 0.62} width={size * 2.6} height={size * 1.24} rx={size * 0.15} fill="#c9d3cf" stroke="#000" strokeWidth={size * 0.06} />
		<text x={x} y={y + size * 0.36} textAnchor="middle" style={{fontFamily: '"Montserrat", sans-serif', fontWeight: 900, fontSize: size}} fill="#111">
			{text}
		</text>
	</g>
);

// ------------------------------------------------------------------- door: "DON'T OPEN IT"

export const DoorTemplate: React.FC<TplProps> = ({spec, W, H, fx}) => {
	const tall = H > W;
	const k = Math.min(W / 1280, H / 720);
	// door frame
	const dw = tall ? W * 0.62 : W * 0.34;
	const dh = tall ? H * 0.62 : H * 0.92;
	const dx = tall ? W * 0.3 : W * 0.53;
	const dy = tall ? H * 0.3 : H * 0.08;
	const floorY = dy + dh;
	const open = 0.62; // fraction of the doorway that is open (void)
	const lay = layoutHeadline(
		spec.text,
		spec.accent,
		tall ? {x: W * 0.06, y: H * 0.04, w: W * 0.88, h: H * 0.2, align: 'center', maxLines: 2} : {x: W * 0.04, y: H * 0.06, w: W * 0.46, h: H * 0.4, maxLines: 3},
	);
	const fig = {w: dw * 1.0, h: dh * 1.04};
	const resH = tall ? H * 0.14 : H * 0.24;
	const res = tall ? {x: W * 0.16, y: H * 0.97} : {x: W * 0.36, y: H * 0.96};
	return (
		<>
			<defs>
				<linearGradient id="d-wall" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor={WALL_D} />
					<stop offset="0.7" stopColor={spec.bg ?? WALL} />
					<stop offset="1" stopColor={WALL_D} />
				</linearGradient>
				<linearGradient id="d-void" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#000" />
					<stop offset="1" stopColor="#0a1012" />
				</linearGradient>
				<linearGradient id="d-spill" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={COLD} stopOpacity={0.22} />
					<stop offset="1" stopColor={COLD} stopOpacity={0} />
				</linearGradient>
				<linearGradient id="d-cone" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={COLD} stopOpacity={0.45} />
					<stop offset="1" stopColor={COLD} stopOpacity={0.05} />
				</linearGradient>
				<clipPath id="d-gap">
					<rect x={dx} y={dy} width={dw * open} height={dh} />
				</clipPath>
			</defs>
			<rect width={W} height={H} fill="url(#d-wall)" />
			{/* floor */}
			<rect x={0} y={floorY} width={W} height={H - floorY} fill="#0b1011" />
			{/* door frame */}
			<rect x={dx - 18 * k} y={dy - 18 * k} width={dw + 36 * k} height={dh + 18 * k} fill="#2c3a3c" />
			{/* the void and the thing in it */}
			<rect x={dx} y={dy} width={dw} height={dh} fill="url(#d-void)" />
			<g clipPath="url(#d-gap)">
				<Figure spec={spec} x={dx + dw * open * 0.5 - fig.w / 2} y={floorY - fig.h} w={fig.w} h={fig.h} id="fig" lean={18} />
			</g>
			{/* door leaf swung in (perspective trapezoid) */}
			<polygon
				points={`${dx + dw * open},${dy} ${dx + dw},${dy - 10 * k} ${dx + dw},${floorY + 10 * k} ${dx + dw * open},${floorY}`}
				fill="#3a4a4b"
				stroke="#0b1011"
				strokeWidth={4 * k}
			/>
			<polygon points={`${dx + dw * open},${dy} ${dx + dw * open + 12 * k},${dy} ${dx + dw * open + 12 * k},${floorY} ${dx + dw * open},${floorY}`} fill="#556667" />
			{/* chain lock across the gap */}
			<path
				d={`M${dx + dw * open + 6 * k} ${dy + dh * 0.42} q ${-dw * open * 0.18} ${30 * k} ${-dw * open * 0.36} ${-6 * k}`}
				fill="none"
				stroke="#c9d3cf"
				strokeWidth={5 * k}
				strokeDasharray={`${10 * k} ${5 * k}`}
			/>
			<circle cx={dx + dw * open + dw * 0.3} cy={dy + dh * 0.52} r={9 * k} fill="#c9d3cf" />
			<Plate x={dx + dw * open + dw * 0.19} y={dy + dh * 0.2} size={26 * k * (tall ? 1.4 : 1)} text={spec.room ?? '802'} />
			{/* light spilling on the floor from the void */}
			<polygon points={`${dx},${floorY} ${dx + dw * open},${floorY} ${dx + dw * open + 120 * k},${H} ${dx - 160 * k},${H}`} fill="url(#d-spill)" />
			<polygon points={`${res.x - resH * 0.12},${res.y - resH * 2.4} ${res.x + resH * 0.12},${res.y - resH * 2.4} ${res.x + resH * 0.75},${res.y + 4} ${res.x - resH * 0.75},${res.y + 4}`} fill="url(#d-cone)" />
			<ellipse cx={res.x} cy={res.y} rx={resH * 0.6} ry={resH * 0.07} fill={COLD} opacity={0.25} />
			<Tiny spec={spec} x={res.x} y={res.y} h={resH} id="res" />
			<Vignette id="v" w={W} h={H} strength={0.8} />
			<Headline layout={lay} />
			<Grain fx={fx} w={W} h={H} opacity={0.08} />
		</>
	);
};

// ------------------------------------------------------------------- chat: giant phone, tiny reader

const Bubble: React.FC<{x: number; y: number; w: number; size: number; text: string; me?: boolean; from?: string; hot?: boolean; maxChars: number}> = ({
	x,
	y,
	w,
	size,
	text,
	me,
	from,
	hot,
	maxChars,
}) => {
	// greedy wrap
	const words = text.split(/\s+/);
	const lines: string[] = [];
	let cur = '';
	for (const wd of words) {
		if ((cur + ' ' + wd).trim().length > maxChars && cur) {
			lines.push(cur);
			cur = wd;
		} else cur = (cur + ' ' + wd).trim();
	}
	if (cur) lines.push(cur);
	const lh = size * 1.25;
	const bh = lines.length * lh + size * 0.9;
	const longest = Math.max(...lines.map((l) => textWidthEm(l)));
	const bw = Math.min(w, longest * size * 0.97 + size * 1.4);
	const bx = me ? x + w - bw : x;
	const nameH = from && !me ? size * 1.05 : 0;
	return (
		<g>
			{from && !me && (
				<text x={bx + size * 0.2} y={y + size * 0.75} style={{fontFamily: '"Montserrat", sans-serif', fontWeight: 700, fontSize: size * 0.68}} fill={hot ? '#111' : '#7f9196'}>
					{from}
				</text>
			)}
			{hot && <rect x={bx - size * 0.3} y={y + nameH - size * 0.3} width={bw + size * 0.6} height={bh + size * 0.6} rx={size * 0.9} fill="#fff" opacity={0.18} />}
			<rect x={bx} y={y + nameH} width={bw} height={bh} rx={size * 0.7} fill={me ? '#5d8c6a' : hot ? '#f4f4f4' : '#e3e7e8'} />
			{lines.map((l, i) => (
				<text
					key={i}
					x={bx + size * 0.7}
					y={y + nameH + size * 0.45 + (i + 0.85) * lh}
					style={{fontFamily: '"Montserrat", sans-serif', fontWeight: hot ? 800 : 700, fontSize: size}}
					fill={me ? '#fff' : '#111'}
				>
					{l}
				</text>
			))}
		</g>
	);
};

export function bubbleHeight(text: string, size: number, maxChars: number, from?: string, me?: boolean) {
	let n = 0;
	let cur = '';
	for (const wd of text.split(/\s+/)) {
		if ((cur + ' ' + wd).trim().length > maxChars && cur) {
			n++;
			cur = wd;
		} else cur = (cur + ' ' + wd).trim();
	}
	if (cur) n++;
	return n * size * 1.25 + size * 0.9 + (from && !me ? size * 1.05 : 0);
}

const DEFAULT_CHAT = [
	{from: 'Mrs. Ortiz (5B)', text: 'Who keeps knocking on every door on 5?'},
	{from: 'Dev (5D)', text: 'Not me. I am at work until 2'},
	{me: true, text: 'Someone just knocked on mine'},
	{from: 'Unknown', text: 'I know. I can see you through it.'},
];

export const ChatTemplate: React.FC<TplProps> = ({spec, W, H, fx}) => {
	const tall = H > W;
	const k = Math.min(W / 1280, H / 720);
	const chat = spec.chat?.length ? spec.chat : DEFAULT_CHAT;
	// phone geometry (portrait), tilted
	const ph = tall ? H * 0.66 : H * 1.12;
	const pw = ph * 0.49;
	const pcx = tall ? W * 0.56 : W * 0.71;
	const pcy = tall ? H * 0.58 : H * 0.56;
	const tilt = tall ? -4 : 7;
	const px = pcx - pw / 2;
	const py = pcy - ph / 2;
	const fs = pw * 0.056;
	const maxChars = 19;
	const lay = layoutHeadline(
		spec.text,
		spec.accent,
		tall ? {x: W * 0.06, y: H * 0.035, w: W * 0.88, h: H * 0.17, align: 'center', maxLines: 2} : {x: W * 0.04, y: H * 0.06, w: W * 0.5, h: H * 0.42, maxLines: 3},
	);
	// lay out bubbles bottom-up so the last (scary) one sits low and big
	const pad = pw * 0.07;
	const inner = pw - pad * 2;
	const bottom = py + ph * 0.86;
	let yy = bottom;
	const placed = chat
		.slice()
		.reverse()
		.map((m, ri) => {
			const hot = ri === 0;
			const size = hot ? fs * 1.3 : fs;
			const h = bubbleHeight(m.text, size, hot ? 15 : maxChars, m.from, m.me);
			yy -= h + fs * 0.7;
			return {m, y: yy, size, hot};
		})
		.filter((b) => b.y > py + ph * 0.16);
	const r = rng(4);
	return (
		<>
			<defs>
				<radialGradient id="c-glow" cx={pcx / W} cy={pcy / H} r={0.6}>
					<stop offset="0" stopColor="#3d5a60" />
					<stop offset="0.5" stopColor={spec.bg ?? '#132024'} />
					<stop offset="1" stopColor="#05090a" />
				</radialGradient>
				<clipPath id="c-screen">
					<rect x={px + pw * 0.035} y={py + pw * 0.035} width={pw * 0.93} height={ph - pw * 0.07} rx={pw * 0.09} />
				</clipPath>
			</defs>
			<rect width={W} height={H} fill="url(#c-glow)" />
			{/* bedroom: window with blinds, bed + sitting reader (tiny) */}
			<g opacity={0.6}>
				<rect x={W * (tall ? 0.06 : 0.05)} y={H * (tall ? 0.24 : 0.5)} width={W * (tall ? 0.3 : 0.17)} height={H * (tall ? 0.16 : 0.26)} fill="#0b1416" stroke="#304448" strokeWidth={6 * k} />
				{Array.from({length: 7}, (_, i) => (
					<line
						key={i}
						x1={W * (tall ? 0.06 : 0.05)}
						x2={W * (tall ? 0.36 : 0.22)}
						y1={H * (tall ? 0.24 : 0.5) + (i + 1) * H * (tall ? 0.02 : 0.032)}
						y2={H * (tall ? 0.24 : 0.5) + (i + 1) * H * (tall ? 0.02 : 0.032)}
						stroke="#5b7b80"
						strokeWidth={3 * k}
						opacity={0.5 + r() * 0.3}
					/>
				))}
			</g>
			<rect x={-20} y={H * 0.86} width={W * (tall ? 0.6 : 0.42)} height={H * 0.2} rx={20 * k} fill="#0f1a1c" />
			<rect x={-20} y={H * 0.83} width={W * (tall ? 0.22 : 0.12)} height={H * 0.06} rx={18 * k} fill="#1c2b2e" />
			<Tiny spec={spec} x={W * (tall ? 0.22 : 0.16)} y={H * 0.9} h={H * (tall ? 0.12 : 0.24)} id="res" />
			{/* phone */}
			<g transform={`rotate(${tilt} ${pcx} ${pcy})`}>
				<rect x={px - 6 * k} y={py - 6 * k} width={pw + 12 * k} height={ph + 12 * k} rx={pw * 0.12} fill="#000" opacity={0.6} transform={`translate(${14 * k} ${18 * k})`} />
				<rect x={px} y={py} width={pw} height={ph} rx={pw * 0.11} fill="#0c0f10" stroke="#3a4446" strokeWidth={5 * k} />
				<g clipPath="url(#c-screen)">
					<rect x={px} y={py} width={pw} height={ph} fill="#f1f3f3" />
					<rect x={px} y={py} width={pw} height={ph * 0.12} fill="#dfe5e6" />
					<text x={pcx} y={py + ph * 0.085} textAnchor="middle" style={{fontFamily: '"Montserrat", sans-serif', fontWeight: 800, fontSize: fs * 0.95}} fill="#111">
						{spec.chatTitle ?? 'Building 7 Residents (58)'}
					</text>
					{placed.map((b, i) => (
						<Bubble key={i} x={px + pad} y={b.y} w={inner} size={b.size} text={b.m.text} me={b.m.me} from={b.m.from} hot={b.hot} maxChars={b.hot ? 15 : maxChars} />
					))}
					{/* typing dots */}
					<rect x={px + pad} y={py + ph * 0.885} width={fs * 3.6} height={fs * 1.6} rx={fs * 0.8} fill="#d5dbdc" />
					{[0, 1, 2].map((i) => (
						<circle key={i} cx={px + pad + fs * (0.95 + i * 0.85)} cy={py + ph * 0.885 + fs * 0.8} r={fs * 0.24} fill="#6f7b7d" />
					))}
				</g>
				<rect x={pcx - pw * 0.16} y={py + pw * 0.05} width={pw * 0.32} height={pw * 0.07} rx={pw * 0.035} fill="#000" />
			</g>
			<Vignette id="v" w={W} h={H} strength={0.75} />
			<Headline layout={lay} />
			<Grain fx={fx} w={W} h={H} opacity={0.08} />
		</>
	);
};

// ------------------------------------------------------------------- hallway: it's right behind you

export const HallwayTemplate: React.FC<TplProps> = ({spec, W, H, fx}) => {
	const tall = H > W;
	const k = Math.min(W / 1280, H / 720);
	// one-point perspective corridor
	const vx = tall ? W * 0.5 : W * 0.42;
	const vy = tall ? H * 0.52 : H * 0.48;
	const fw = tall ? W * 0.16 : W * 0.09; // far wall half width
	const fh = tall ? H * 0.06 : H * 0.12; // far wall half height
	const far = {l: vx - fw, r: vx + fw, t: vy - fh, b: vy + fh};
	const near = {l: -W * 0.05, r: W * 1.05, t: -H * 0.05, b: H * 1.05};
	const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
	// depth parameter d: 0 = near, 1 = far (non-linear for perspective)
	const at = (d: number) => {
		const t = 1 - 1 / (1 + d * 6) + d * 0.14; // rough foreshortening
		const u = Math.min(1, t);
		return {l: lerp(near.l, far.l, u), r: lerp(near.r, far.r, u), t: lerp(near.t, far.t, u), b: lerp(near.b, far.b, u)};
	};
	const doors = [0.12, 0.3, 0.55, 0.85];
	const lights = [0.08, 0.28, 0.6, 1.0];
	const lay = layoutHeadline(
		spec.text,
		spec.accent,
		tall ? {x: W * 0.06, y: H * 0.04, w: W * 0.88, h: H * 0.18, align: 'center', maxLines: 2} : {x: W * 0.035, y: H * 0.05, w: W * 0.42, h: H * 0.36, maxLines: 3},
	);
	const resAt = at(0.93);
	const resH = (resAt.b - resAt.t) * 0.55;
	const fig = tall ? {x: W * 0.3, y: H * 0.18, w: W * 1.0, h: H * 0.92} : {x: W * 0.54, y: -H * 0.12, w: W * 0.6, h: H * 1.25};
	return (
		<>
			<defs>
				<radialGradient id="h-light" cx={vx / W} cy={vy / H} r={0.45}>
					<stop offset="0" stopColor="#dff3f2" stopOpacity={0.55} />
					<stop offset="1" stopColor="#dff3f2" stopOpacity={0} />
				</radialGradient>
			</defs>
			<rect width={W} height={H} fill={WALL_D} />
			{/* ceiling, floor, walls */}
			<polygon points={`${near.l},${near.t} ${near.r},${near.t} ${far.r},${far.t} ${far.l},${far.t}`} fill="#0f1819" />
			<polygon points={`${near.l},${near.b} ${near.r},${near.b} ${far.r},${far.b} ${far.l},${far.b}`} fill="#162021" />
			<polygon points={`${near.l},${near.t} ${far.l},${far.t} ${far.l},${far.b} ${near.l},${near.b}`} fill={spec.bg ?? '#223234'} />
			<polygon points={`${near.r},${near.t} ${far.r},${far.t} ${far.r},${far.b} ${near.r},${near.b}`} fill="#1a2829" />
			<rect x={far.l} y={far.t} width={far.r - far.l} height={far.b - far.t} fill="#2c3d3e" />
			{/* floor lines */}
			{Array.from({length: 9}, (_, i) => {
				const d = i / 8;
				const s = at(d);
				return <line key={i} x1={s.l} x2={s.r} y1={s.b} y2={s.b} stroke="#0a1112" strokeWidth={3 * k} opacity={0.7} />;
			})}
			{/* doors on both walls */}
			{doors.map((d, i) => {
				const a = at(d);
				const b = at(d + 0.08);
				const hTop = (s: typeof a) => lerp(s.b, s.t, 0.78);
				const left = i % 2 === 0;
				const x1 = left ? a.l : a.r;
				const x2 = left ? b.l : b.r;
				return (
					<g key={i}>
						<polygon points={`${x1},${a.b} ${x1},${hTop(a)} ${x2},${hTop(b)} ${x2},${b.b}`} fill="#0b1112" stroke="#2e3f40" strokeWidth={3 * k} />
						{i === 1 && (
							<text
								x={(x1 + x2) / 2}
								y={lerp(hTop(a), hTop(b), 0.5) + (a.b - hTop(a)) * 0.18}
								textAnchor="middle"
								style={{fontFamily: '"Montserrat", sans-serif', fontWeight: 900, fontSize: Math.abs(x2 - x1) * 0.42}}
								fill="#c9d3cf"
							>
								{spec.room ?? '802'}
							</text>
						)}
					</g>
				);
			})}
			{/* ceiling lights: the far one works, the near ones are dead */}
			{lights.map((d, i) => {
				const a = at(Math.min(0.98, d));
				const cx = (a.l + a.r) / 2;
				const w = (a.r - a.l) * 0.12;
				const lit = i === lights.length - 1;
				return <rect key={i} x={cx - w / 2} y={a.t + 4 * k} width={w} height={Math.max(4, w * 0.12)} fill={lit ? '#f2fbfa' : '#3b4a4b'} />;
			})}
			<rect width={W} height={H} fill="url(#h-light)" />
			{/* tiny resident far down the hall, under the only working light */}
			<Tiny spec={spec} x={vx - fw * 0.15} y={resAt.b - (resAt.b - resAt.t) * 0.02} h={resH} id="res" />
			{/* the huge figure, foreground right, cropped by the frame */}
			<Figure spec={spec} x={fig.x} y={fig.y} w={fig.w} h={fig.h} id="fig" lean={-16} />
			<Vignette id="v" w={W} h={H} strength={0.85} />
			<Headline layout={lay} />
			<Grain fx={fx} w={W} h={H} opacity={0.08} />
		</>
	);
};
