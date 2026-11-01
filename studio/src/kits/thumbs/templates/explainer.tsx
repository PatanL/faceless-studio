// Explainer (Depth Theory-style) thumbnails: black, scratchboard creature, tiny diver,
// 2-4 word headline with one red word that continues as a hand-drawn red pointer.
import React from 'react';
import {Grain, Headline, RedArrow, Sonar, Vignette, layoutHeadline, type Pt} from '../fx';
import {ANGLER_EYE, ANGLER_LURE, ANGLER_VB, Anglerfish, ColossalSquid, SQUID_EYE, SQUID_VB, SpermWhale, WHALE_EYE, WHALE_VB} from '../art/creatures';
import {Diver} from '../art/people';
import {KitArt, hasKit} from '../art/KitArt';
import type {ThumbSpec} from '../spec';

export type TplProps = {spec: ThumbSpec; W: number; H: number; fx: string};

type Creature = {vb: number[]; eye: Pt; C: React.FC<any>};
const CREATURES: Record<string, Creature> = {
	whale: {vb: WHALE_VB.split(' ').map(Number), eye: WHALE_EYE, C: SpermWhale},
	squid: {vb: SQUID_VB.split(' ').map(Number), eye: SQUID_EYE, C: ColossalSquid},
	angler: {vb: ANGLER_VB.split(' ').map(Number), eye: ANGLER_LURE, C: Anglerfish},
};

/**
 * Place a creature so its focus point (eye / lure) lands on `at`, `s` px per viewBox unit.
 * If spec.art names a registered kit component it is drawn in the same box instead.
 */
const Subject: React.FC<{
	spec: ThumbSpec;
	name: string;
	at: Pt;
	s: number;
	fx: string;
	id: string;
	flip?: boolean;
	rotate?: number;
	extra?: Record<string, unknown>;
}> = ({spec, name, at, s, fx, id, flip, rotate = 0, extra}) => {
	const cr = CREATURES[name] ?? CREATURES.whale;
	const [, , vw, vh] = cr.vb;
	const ex = flip ? vw - cr.eye[0] : cr.eye[0];
	const x = at[0] - ex * s;
	const y = at[1] - cr.eye[1] * s;
	const w = vw * s;
	const h = vh * s;
	if (spec.art && hasKit(spec.art.component)) {
		// placeholders face left; kit figures face right unless art.facing says otherwise
		const kitFlip = (spec.art.facing ?? 'right') === 'right' ? !flip : !!flip;
		// rotate about the focus point like the placeholder does (KitArt alone would use the box centre)
		return (
			<g transform={`rotate(${rotate} ${at[0]} ${at[1]})`}>
				<KitArt name={spec.art.component} props={spec.art.props} time={spec.art.time} x={x} y={y} w={w} h={h} flip={kitFlip} />
			</g>
		);
	}
	const C = cr.C;
	return (
		<g transform={`rotate(${rotate} ${at[0]} ${at[1]})`}>
			<C x={x} y={y} w={w} h={h} fx={fx} id={id} flip={flip} {...extra} />
		</g>
	);
};

const Human: React.FC<{spec: ThumbSpec; x: number; y: number; s: number; flip?: boolean; beam?: number; beamAngle?: number; id: string; tilt?: number}> = (p) => {
	const ha = p.spec.humanArt;
	if (ha && hasKit(ha.component)) {
		const w = 200 * p.s;
		const h = 100 * p.s;
		return <KitArt name={ha.component} props={ha.props} time={ha.time} x={p.x - w / 2} y={p.y - h / 2} w={w} h={h} flip={p.flip} />;
	}
	return <Diver {...p} />;
};

const SmallLabel: React.FC<{x: number; y: number; size: number; text: string; anchor?: 'start' | 'middle' | 'end'}> = ({x, y, size, text, anchor = 'middle'}) => (
	<text
		x={x}
		y={y}
		textAnchor={anchor}
		style={{fontFamily: '"Montserrat", sans-serif', fontWeight: 900, fontSize: size}}
		fill="#fff"
		stroke="#000"
		strokeWidth={size * 0.18}
		paintOrder="stroke"
		strokeLinejoin="round"
	>
		{text}
	</text>
);

const Backdrop: React.FC<TplProps & {glow?: Pt; glowR?: number}> = ({spec, W, H, glow, glowR}) => (
	<>
		<defs>
			<radialGradient id="ex-bg" cx={glow ? glow[0] / W : 0.6} cy={glow ? glow[1] / H : 0.5} r={glowR ?? 0.7}>
				<stop offset="0" stopColor={spec.bg ?? '#141b1e'} />
				<stop offset="1" stopColor="#000" />
			</radialGradient>
		</defs>
		<rect width={W} height={H} fill="url(#ex-bg)" />
	</>
);

const arrowFrom = (lay: ReturnType<typeof layoutHeadline>, toward: Pt): Pt => {
	const b = lay.accentBox;
	if (!b) return [lay.rows[0].x, lay.bottom];
	const onLast = b.y + b.h > lay.bottom - lay.size * 0.9;
	const onFirst = b.y < lay.top + lay.size * 0.9;
	const below = toward[1] > b.y + b.h;
	const above = toward[1] < b.y;
	// leave from the bottom/top only when no other headline line is in the way
	if (below && onLast) return [Math.max(b.x + b.w * 0.15, Math.min(b.x + b.w * 0.85, toward[0])), b.y + b.h + lay.size * 0.2];
	if (above && onFirst) return [Math.max(b.x + b.w * 0.15, Math.min(b.x + b.w * 0.85, toward[0])), b.y - lay.size * 0.15];
	// otherwise from the word's side facing the target, clear of the text block
	const leftSide = toward[0] < b.x + b.w / 2;
	return [leftSide ? b.x - lay.size * 0.15 : b.x + b.w + lay.size * 0.15, b.y + b.h * 0.5];
};

// ------------------------------------------------------------------- eye: "IT SEES YOU"

export const EyeTemplate: React.FC<TplProps> = (p) => {
	const {spec, W, H, fx} = p;
	const tall = H > W;
	const subject = spec.subject ?? 'squid';
	const eye: Pt = tall ? [W * 0.58, H * 0.54] : [W * 0.62, H * 0.5];
	const s = subject === 'whale' ? (tall ? 3.2 : 2.6) * (W / 1280) * (tall ? 0.62 : 1) : (tall ? 1.9 : 1.15) * (H / 720) * (tall ? 0.42 : 1);
	const flip = tall && subject !== 'whale';
	const diver: Pt = tall ? [W * 0.22, H * 0.8] : [W * 0.11, H * 0.66];
	const lay = layoutHeadline(
		spec.text,
		spec.accent,
		tall ? {x: W * 0.06, y: H * 0.045, w: W * 0.88, h: H * 0.2, align: 'center', maxLines: 2} : {x: W * 0.045, y: H * 0.05, w: W * 0.5, h: H * 0.32, maxLines: 2},
	);
	const ds = (tall ? 0.95 : 0.55) * (W / 1280) * (tall ? 1.2 : 1);
	const target: Pt = [diver[0] + (tall ? 0 : -10), diver[1] - 50 * ds];
	return (
		<>
			<Backdrop {...p} glow={eye} glowR={0.6} />
			<Sonar cx={eye[0] - (subject === 'whale' ? 40 : 0)} cy={eye[1] + (tall ? 30 : 0)} r0={(tall ? 260 : 170) * (W / 1280)} step={(tall ? 60 : 44) * (W / 1280)} n={4} from={140} to={220} />
			<Subject spec={spec} name={subject} at={eye} s={s} fx={fx} id="subj" flip={flip} />
			<Vignette id="v" w={W} h={H} strength={0.7} />
			<Human spec={spec} x={diver[0]} y={diver[1]} s={ds} beam={W * 0.3} beamAngle={tall ? -50 : -8} id="diver" />
			{spec.humanLabel && <SmallLabel x={diver[0]} y={diver[1] + 60 * ds} size={26 * ds * 1.6} text={spec.humanLabel} />}
			<Headline layout={lay} />
			{!spec.noArrow && <RedArrow a={arrowFrom(lay, target)} b={target} bend={tall ? 0.18 : -0.22} width={tall ? 18 : 12} />}
			<Grain fx={fx} w={W} h={H} />
		</>
	);
};

// ------------------------------------------------------------------- scale: whole animal vs you

const Ruler: React.FC<{a: Pt; b: Pt; label: string; size: number; vertical?: boolean}> = ({a, b, label, size, vertical}) => {
	const n = 10;
	const ticks = Array.from({length: n + 1}, (_, i) => {
		const t = i / n;
		const x = a[0] + (b[0] - a[0]) * t;
		const y = a[1] + (b[1] - a[1]) * t;
		const L = i % 5 === 0 ? size * 0.5 : size * 0.25;
		return vertical ? <line key={i} x1={x} y1={y} x2={x - L} y2={y} /> : <line key={i} x1={x} y1={y} x2={x} y2={y - L} />;
	});
	const mx = (a[0] + b[0]) / 2;
	const my = (a[1] + b[1]) / 2;
	return (
		<g stroke="#fff" strokeWidth={Math.max(3, size * 0.09)} strokeLinecap="round">
			<line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} />
			{ticks}
			<g stroke="none">
				{vertical ? (
					<g transform={`translate(${mx + size * 0.7} ${my}) rotate(90)`}>
						<SmallLabel x={0} y={0} size={size} text={label} />
					</g>
				) : (
					<SmallLabel x={mx} y={my + size * 1.15} size={size} text={label} />
				)}
			</g>
		</g>
	);
};

export const ScaleTemplate: React.FC<TplProps> = (p) => {
	const {spec, W, H, fx} = p;
	const tall = H > W;
	const subject = spec.subject ?? 'whale';
	const label = spec.label ?? '16 M';
	const k = W / 1280;
	if (!tall) {
		// whale side-on across the lower frame, facing left; tiny diver at its eye
		const s = subject === 'whale' ? 1.12 * k : subject === 'squid' ? 0.62 * k : 0.85 * k;
		const eye: Pt = subject === 'whale' ? [W * 0.43, H * 0.6] : [W * 0.5, H * 0.55];
		const cr = CREATURES[subject] ?? CREATURES.whale;
		const left = eye[0] - cr.eye[0] * s;
		const right = left + cr.vb[2] * s;
		const bottom = eye[1] + (cr.vb[3] - cr.eye[1]) * s;
		const diver: Pt = [left - 70 * k, eye[1] - 30 * k];
		const lay = layoutHeadline(spec.text, spec.accent, {x: W * 0.045, y: H * 0.04, w: W * 0.62, h: H * 0.27, maxLines: 2});
		const target: Pt = [diver[0] - 12 * k, diver[1] - 24 * k];
		return (
			<>
				<Backdrop {...p} glow={[W * 0.55, H * 0.55]} glowR={0.75} />
				<Subject spec={spec} name={subject} at={eye} s={s} fx={fx} id="subj" />
				<Ruler a={[Math.max(left, W * 0.03), Math.min(bottom + 28 * k, H * 0.93)]} b={[Math.min(right, W * 0.97), Math.min(bottom + 28 * k, H * 0.93)]} label={label} size={34 * k} />
				<Vignette id="v" w={W} h={H} strength={0.55} />
				<Human spec={spec} x={diver[0]} y={diver[1]} s={0.3 * k} beam={70 * k} id="diver" tilt={4} />
				{spec.humanLabel && <SmallLabel x={diver[0] - 4 * k} y={diver[1] + 40 * k} size={22 * k} text={spec.humanLabel} />}
				<Headline layout={lay} />
				{!spec.noArrow && <RedArrow a={arrowFrom(lay, target)} b={target} bend={0.2} width={11 * k} />}
				<Grain fx={fx} w={W} h={H} />
			</>
		);
	}
	// 9:16: the animal dives head-down through the whole frame
	const s = (subject === 'whale' ? 1.62 * k : 1.0 * k) * (spec.subjectScale ?? 1);
	const eye: Pt = [W * 0.47, H * 0.74];
	const diver: Pt = [W * 0.76, H * 0.74];
	const lay = layoutHeadline(spec.text, spec.accent, {x: W * 0.06, y: H * 0.04, w: W * 0.88, h: H * 0.19, align: 'center', maxLines: 2});
	const target: Pt = [diver[0] + 6 * k, diver[1] - 30 * k];
	return (
		<>
			<Backdrop {...p} glow={[W * 0.5, H * 0.55]} glowR={0.8} />
			<Subject spec={spec} name={subject} at={eye} s={s} fx={fx} id="subj" rotate={-90} />
			<Ruler a={[W * 0.13, H * 0.28]} b={[W * 0.13, H * 0.93]} label={label} size={44 * k} vertical />
			<Vignette id="v" w={W} h={H} strength={0.5} />
			<Human spec={spec} x={diver[0]} y={diver[1]} s={0.42 * k} beam={90 * k} flip id="diver" tilt={8} />
			{spec.humanLabel && <SmallLabel x={diver[0]} y={diver[1] + 60 * k} size={34 * k} text={spec.humanLabel} />}
			<Headline layout={lay} />
			{!spec.noArrow && <RedArrow a={arrowFrom(lay, target)} b={target} bend={-0.15} width={16 * k} />}
			<Grain fx={fx} w={W} h={H} />
		</>
	);
};

// ------------------------------------------------------------------- abyss: the light is a lure

export const AbyssTemplate: React.FC<TplProps> = (p) => {
	const {spec, W, H, fx} = p;
	const tall = H > W;
	const subject = spec.subject ?? 'angler';
	const k = W / 1280;
	const lure: Pt = tall ? [W * 0.36, H * 0.38] : [W * 0.4, H * 0.3];
	const s = subject === 'angler' ? (tall ? 1.5 : 0.9) * k : (tall ? 1.4 : 1.0) * k;
	const diver: Pt = tall ? [W * 0.2, H * 0.32] : [W * 0.14, H * 0.27];
	const lay = layoutHeadline(
		spec.text,
		spec.accent,
		tall ? {x: W * 0.06, y: H * 0.04, w: W * 0.88, h: H * 0.17, align: 'center', maxLines: 2} : {x: W * 0.53, y: H * 0.05, w: W * 0.43, h: H * 0.34, align: 'right', maxLines: 2},
	);
	const target: Pt = [diver[0] + 50 * k, diver[1] - 40 * k];
	return (
		<>
			<rect width={W} height={H} fill="#000" />
			<defs>
				<radialGradient id="ab-glow" cx={lure[0] / W} cy={lure[1] / H} r={0.55}>
					<stop offset="0" stopColor={spec.bg ?? '#1d2a2e'} />
					<stop offset="1" stopColor="#000" />
				</radialGradient>
				<linearGradient id="ab-dark" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#000" stopOpacity={0} />
					<stop offset="0.55" stopColor="#000" stopOpacity={0.15} />
					<stop offset="1" stopColor="#000" stopOpacity={0.9} />
				</linearGradient>
			</defs>
			<rect width={W} height={H} fill="url(#ab-glow)" />
			<Subject spec={spec} name={subject} at={lure} s={s} fx={fx} id="subj" />
			<rect width={W} height={H} fill="url(#ab-dark)" />
			<Human spec={spec} x={diver[0]} y={diver[1]} s={(tall ? 0.5 : 0.36) * k} beam={0} id="diver" tilt={12} />
			{spec.humanLabel && <SmallLabel x={diver[0]} y={diver[1] + 50 * k} size={(tall ? 34 : 22) * k} text={spec.humanLabel} />}
			<Vignette id="v" w={W} h={H} strength={0.6} />
			<Headline layout={lay} />
			{!spec.noArrow && <RedArrow a={arrowFrom(lay, target)} b={target} bend={tall ? 0.45 : -0.18} width={(tall ? 16 : 12) * k} />}
			<Grain fx={fx} w={W} h={H} />
		</>
	);
};
