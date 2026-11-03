// next/Actor (our own code): the story lane's round-head figure, acted the way the references act it
// (research/library/RICKSCLIPS_RULEBOOK.md 1.3, gap 2). It is a drop-in twin of studio stick/Person - same 600 x 700
// box, same costumes, poses, items and prop names, feet on the bottom edge - with the acting rules built in:
//   - faces are WHOLE DRAWINGS swapped on one frame (A2), from a 27-face library (A4): ring eyes, >< squeeze, X,
//     spiral, grid-teeth grimace, wink, ^^ bliss, half-lid deadpan, dead-dot pupils ...
//   - no idle breathing (A6): the body is frozen between poses; only a walk bobs it
//   - no lip-sync (A7): the mouth belongs to the face; `quote` (or Person's `talk`) windows get loose flaps from
//     3-4 mouth shapes, a new shape every 3 frames (A8)
//   - blinks are rare and short (A5): irregular 2-8 s apart, closed 2 frames (1-4 via blinkF), optional half-lid
//     frames around them ("half, closed, half")
//   - poses snap in 3-6 frames with a small overshoot (A9), on 1s
//   - props carry the overlap instead of hair or cloth (A11): a held lantern / tag / key swings and settles after
//     every pose snap (pendulum, ~20 f), a hat pops off and lands (hatPop)
//   - emotion marks pop on with no fade (A12): sweat, tears, steam puffs, anger vein, blush, and the head filling
//     with colour like a liquid (fill)
// Everything is a pure function of time, so the SVG markup is identical on held frames and the 3D card is not
// redrawn (SvgTex.draw skips unchanged markup).
//
// props (Person's, plus)
//   face     a FACES name, constant or [{t, v}]  - hard swap at t
//   marks    [{t0, t1?, kind: sweat | tears | steam | vein | blush}]
//   fill     [{t0, t1?, color, rise?: s (0.2), drain?: s (0.2)}]  head colour fill
//   quote    [[t0, t1], ...] mouth flaps (Person's `talk` is read as quote)
//   blinkF   frames closed (1-4, default 2); blinkHalf: true adds a half-lid frame either side; blinks: [t...] to
//            place them by hand (default: seeded irregular schedule); noBlink: true
//   snapF    pose snap length in frames (default 4)
//   hatPop   [t, ...] the hat jumps half a head and lands, tumbling, over ~20 f
//   stepF    frames per walk step (default 7)
import React from 'react';
import {num, str, track, clamp, lerp} from '../../../../studio/src/kits/explainer/util';
import {c, K, f, hash, inkG, step, stepBlend, inWin} from '../../../../studio/src/kits/explainer/stick/common';

type P2 = [number, number];
const FPS = 30;

// ------------------------------------------------------------------ costumes (same names and colours as stick/Person)
type Costume = {
	coat: string; coatShade: string; vest?: string; cravat?: string; legs: string; shoes: string;
	hat?: 'tricorn' | 'bicorne' | 'crown' | 'furcap' | 'brim' | 'cap' | 'bonnet' | 'bowler' | 'helmet' | 'tiara' | 'none';
	hair?: 'wig' | 'wigTall' | 'updo' | 'side' | 'short' | 'messy' | 'bob' | 'none'; hairColor?: string;
	gown?: string; gownShade?: string; glasses?: boolean; epaulettes?: boolean; buttons?: boolean;
};
const COSTUMES: Record<string, Costume> = {
	kempelen: {coat: c('violet-1'), coatShade: c('violet-0'), vest: c('amber-4'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'tricorn', hair: 'wig', hairColor: c('bone-0'), buttons: true},
	empress: {coat: c('magenta-2'), coatShade: c('magenta-1'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'crown', hair: 'updo', hairColor: c('bone-0'), gown: c('magenta-1'), gownShade: c('magenta-0')},
	courtier: {coat: c('tide-0'), coatShade: c('dusk-1'), vest: c('bone-1'), cravat: c('bone-2'), legs: c('bone-0'), shoes: c('ink-0'), hair: 'wig', hairColor: c('bone-0'), buttons: true},
	courtier2: {coat: c('kelp-1'), coatShade: c('kelp-0'), vest: c('magenta-3'), cravat: c('bone-2'), legs: c('bone-0'), shoes: c('ink-0'), hair: 'wigTall', hairColor: c('bone-0'), buttons: true},
	count: {coat: c('amber-1'), coatShade: c('amber-0'), vest: c('amber-4'), cravat: c('bone-2'), legs: c('bone-0'), shoes: c('ink-0'), hair: 'wig', hairColor: c('bone-0'), buttons: true},
	franklin: {coat: c('ochre-0'), coatShade: c('amber-0'), vest: c('ochre-2'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'furcap', hair: 'side', hairColor: c('bone-0'), glasses: true},
	napoleon: {coat: c('dusk-1'), coatShade: c('ink-1'), vest: c('bone-1'), cravat: c('bone-2'), legs: c('bone-1'), shoes: c('ink-0'), hat: 'bicorne', hair: 'short', hairColor: c('ink-1'), epaulettes: true, buttons: true},
	master: {coat: c('sky-1'), coatShade: c('sky-0'), legs: K.ink, shoes: c('ink-0'), hair: 'messy', hairColor: c('ink-1')},
	plain: {coat: c('coral-2'), coatShade: c('coral-0'), legs: K.ink, shoes: c('ink-0'), hair: 'short', hairColor: c('ink-1')},
	sailor: {coat: c('sky-1'), coatShade: c('sky-0'), legs: c('bone-0'), shoes: c('ink-0'), hat: 'cap', hair: 'short', hairColor: c('ochre-0')},
	sailor2: {coat: c('coral-1'), coatShade: c('coral-0'), legs: c('bone-0'), shoes: c('ink-0'), hat: 'cap', hair: 'messy', hairColor: c('ink-1')},
	admiral: {coat: c('ink-1'), coatShade: c('ink-0'), vest: c('amber-4'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'brim', hair: 'side', hairColor: c('ochre-0'), buttons: true, epaulettes: true},
	captain: {coat: c('kelp-1'), coatShade: c('kelp-0'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'none', hair: 'side', hairColor: c('ochre-0'), buttons: true},
	king: {coat: c('sky-0'), coatShade: c('dusk-1'), vest: c('amber-4'), cravat: c('bone-2'), legs: c('amber-2'), shoes: c('ink-0'), hat: 'crown', hair: 'side', hairColor: c('ochre-1'), epaulettes: true, buttons: true},
	shipwright: {coat: c('ochre-0'), coatShade: c('amber-0'), legs: K.ink, shoes: c('ink-0'), hat: 'brim', hair: 'short', hairColor: c('bone-0')},
	citizen: {coat: c('kelp-1'), coatShade: c('kelp-0'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'bonnet', hair: 'updo', hairColor: c('ochre-0'), gown: c('kelp-1'), gownShade: c('kelp-0')},
	citizen2: {coat: c('amber-1'), coatShade: c('amber-0'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'brim', hair: 'short', hairColor: c('ink-1')},
	judge: {coat: c('ink-1'), coatShade: c('ink-0'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'), hat: 'none', hair: 'side', hairColor: c('bone-0')},
	// KitLab's keeper (a lighthouse keeper in oilskins) and her apprentice
	keeper: {coat: c('amber-3'), coatShade: c('amber-1'), legs: K.ink, shoes: c('ink-0'), hat: 'none', hair: 'bob', hairColor: c('ink-1'), buttons: true},
	apprentice: {coat: c('sky-1'), coatShade: c('sky-0'), legs: K.ink, shoes: c('ink-0'), hat: 'bowler', hair: 'short', hairColor: c('ochre-0')},
	// story-barca-shield (Barca, c. 515 BC): a Greek bronze-smith in a work tunic, Greek guards (hoplites) in crested
	// bronze helmets, Persian soldiers and diggers in soft caps and trousers, and their commander
	smith: {coat: c('amber-1'), coatShade: c('amber-0'), legs: c('bone-1'), shoes: c('ochre-0'), hat: 'none', hair: 'messy', hairColor: c('ink-1')},
	hoplite: {coat: c('coral-1'), coatShade: c('coral-0'), legs: c('bone-1'), shoes: c('ochre-0'), hat: 'helmet', hair: 'none'},
	hoplite2: {coat: c('sky-1'), coatShade: c('sky-0'), legs: c('bone-1'), shoes: c('ochre-0'), hat: 'helmet', hair: 'none'},
	persian: {coat: c('magenta-1'), coatShade: c('magenta-0'), legs: c('amber-2'), shoes: c('ink-0'), hat: 'tiara', hair: 'none'},
	persian2: {coat: c('kelp-1'), coatShade: c('kelp-0'), legs: c('ochre-1'), shoes: c('ink-0'), hat: 'tiara', hair: 'none'},
	digger: {coat: c('ochre-0'), coatShade: c('amber-0'), legs: c('amber-2'), shoes: c('ink-0'), hat: 'tiara', hair: 'none'},
	persianLord: {coat: c('violet-1'), coatShade: c('violet-0'), vest: c('amber-4'), legs: c('magenta-0'), shoes: c('ink-0'), hat: 'tiara', hair: 'none', buttons: true},
};

// ------------------------------------------------------------------ geometry (Person's 600 x 700 box)
const HEAD: P2 = [300, 150];
const HR = 118;
const SH_L: P2 = [242, 292];
const SH_R: P2 = [358, 292];
const HIP_L: P2 = [268, 470];
const HIP_R: P2 = [332, 470];
const UPPER = 98, LOWER = 92, LIMB = 24;
const POSES: Record<string, [P2, P2]> = {
	stand: [[214, 478], [386, 478]], point: [[214, 478], [540, 240]], hold: [[214, 478], [440, 352]],
	holdHigh: [[214, 478], [452, 236]], armsUp: [[178, 110], [422, 110]], laugh: [[268, 418], [336, 420]],
	shrug: [[150, 286], [450, 286]], push: [[452, 372], [480, 352]], reach: [[214, 478], [520, 420]],
	handIn: [[214, 478], [312, 352]], wind: [[214, 478], [476, 404]], hips: [[226, 442], [374, 442]],
	sweep: [[214, 478], [548, 330]],
	// new: a raised strike (hammer up) and the blow (hammer down), hands to the face, a facepalm
	strikeUp: [[214, 478], [470, 120]], strike: [[214, 478], [552, 400]], cheeks: [[236, 200], [372, 214]],
	facepalm: [[214, 478], [360, 170]],
};
function ik(s: P2, t: P2, a: number, b: number, out: number): P2 {
	const dx = t[0] - s[0], dy = t[1] - s[1];
	const d = clamp(Math.hypot(dx, dy), Math.abs(a - b) + 1, a + b - 1);
	const base = Math.atan2(dy, dx);
	const A = Math.acos(clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1));
	const e1: P2 = [s[0] + a * Math.cos(base + A), s[1] + a * Math.sin(base + A)];
	const e2: P2 = [s[0] + a * Math.cos(base - A), s[1] + a * Math.sin(base - A)];
	const score = (e: P2) => out * (e[0] - 300) + 0.35 * e[1];
	return score(e1) >= score(e2) ? e1 : e2;
}
const lerp2 = (a: P2, b: P2, t: number): P2 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];
/** ease with a small overshoot that settles by the end (snap-in poses read as drawn, not tweened) */
const snapEase = (u: number) => { const x = clamp(u); const c1 = 1.2, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };

// ------------------------------------------------------------------ the face library (whole drawings)
// Features are drawn in Person's face frame (eyes at x 322 / 378, y 148; mouth at x 352, y 204), then scaled 1.32
// about (350, 168) exactly as Person does, so a face swap never moves the head.
type Eye = 'dot' | 'wide' | 'ring' | 'half' | 'squint' | 'happy' | 'closed' | 'squeeze' | 'x' | 'spiral' | 'deadDot' | 'wink' | 'side' | 'sob';
type Mouth = 'smallSmile' | 'smile' | 'grin' | 'laugh' | 'smirk' | 'o' | 'bigO' | 'wavy' | 'frown' | 'teeth' | 'grid' | 'flat' | 'tongue' | 'wobble';
export type FaceDef = {eyes: Eye; brow: [number, number] | null; browY: number; mouth: Mouth; look?: number};
export const FACES: Record<string, FaceDef> = {
	// Person's eleven (same names, so story files keep working)
	neutral: {eyes: 'dot', brow: [0, 0], browY: 0, mouth: 'smallSmile'},
	smile: {eyes: 'dot', brow: [-6, 6], browY: -6, mouth: 'smile'},
	grin: {eyes: 'dot', brow: [-8, 8], browY: -8, mouth: 'grin'},
	smug: {eyes: 'half', brow: [10, -4], browY: 4, mouth: 'smirk'},
	laugh: {eyes: 'happy', brow: [-10, 10], browY: -10, mouth: 'laugh'},
	shock: {eyes: 'wide', brow: [-12, 12], browY: -18, mouth: 'o'},
	worried: {eyes: 'dot', brow: [-16, 16], browY: -6, mouth: 'wavy'},
	frown: {eyes: 'dot', brow: [16, -16], browY: 4, mouth: 'frown'},
	angry: {eyes: 'squint', brow: [24, -24], browY: 8, mouth: 'teeth'},
	focus: {eyes: 'dot', brow: [8, -8], browY: 8, mouth: 'flat'},
	sleepy: {eyes: 'closed', brow: [0, 0], browY: 2, mouth: 'flat'},
	// the reference vocabulary beyond happy / sad (rule A4)
	terrified: {eyes: 'ring', brow: [-14, 14], browY: -20, mouth: 'grid'},
	stunned: {eyes: 'ring', brow: null, browY: 0, mouth: 'o'},
	scream: {eyes: 'ring', brow: [-18, 18], browY: -22, mouth: 'bigO'},
	grimace: {eyes: 'dot', brow: [-14, 14], browY: -4, mouth: 'grid'},
	squeeze: {eyes: 'squeeze', brow: [14, -14], browY: 2, mouth: 'grid'},
	cackle: {eyes: 'squeeze', brow: [-8, 8], browY: -10, mouth: 'laugh'},
	dizzy: {eyes: 'spiral', brow: null, browY: 0, mouth: 'wobble'},
	dead: {eyes: 'x', brow: null, browY: 0, mouth: 'tongue'},
	wink: {eyes: 'wink', brow: [-6, 10], browY: -4, mouth: 'smirk'},
	bliss: {eyes: 'happy', brow: [-6, 6], browY: -8, mouth: 'smile'},
	deadpan: {eyes: 'side', brow: [4, -2], browY: 4, mouth: 'flat', look: 1},
	sly: {eyes: 'half', brow: [14, -10], browY: 6, mouth: 'smirk', look: 1},
	blank: {eyes: 'deadDot', brow: null, browY: 0, mouth: 'flat'},
	sob: {eyes: 'sob', brow: [-18, 18], browY: -6, mouth: 'wobble'},
	furious: {eyes: 'squint', brow: [30, -30], browY: 12, mouth: 'grid'},
	puzzled: {eyes: 'dot', brow: [-18, 4], browY: -2, mouth: 'wavy', look: -1},
};
export const FACE_NAMES = Object.keys(FACES);
const OPEN_EYES: Eye[] = ['dot', 'wide', 'ring', 'half', 'side', 'deadDot'];

function Eyes({eyes, look, lid}: {eyes: Eye; look: number; lid: 0 | 1 | 2}) {
	const xs = [329, 371].map((x) => x + look * 10);
	const y = 135;
	// lid: 0 open, 1 half (blink in/out), 2 closed
	const kind: Eye = lid === 2 && OPEN_EYES.includes(eyes) ? 'closed' : eyes;
	const ink = FINK;
	return (
		<g>
			{xs.map((x, i) => {
				const key = i;
				let el: React.ReactNode = null;
				switch (kind === 'wink' ? (i === 0 ? 'happy' : 'dot') : kind) {
					// bold black oval under a heavy upper lid (the refs' resting eye)
					case 'dot': el = <g><ellipse cx={x} cy={y + 1} rx={10.5} ry={14} fill={ink} /><rect x={x - 15} y={y - 18} width={30} height={10} fill={WHITE} stroke="none" /><path d={`M ${x - 14} ${y - 7} Q ${x} ${y - 11} ${x + 14} ${y - 7}`} stroke={ink} strokeWidth={6.5} strokeLinecap="round" fill="none" /></g>; break;
					case 'wide': el = <g><circle cx={x} cy={y} r={20} fill={WHITE} stroke={ink} strokeWidth={5} /><circle cx={x + 3} cy={y} r={9} fill={ink} stroke="none" /></g>; break;
					case 'ring': el = <g><circle cx={x} cy={y} r={20} fill="#fbf8f2" stroke={ink} strokeWidth={7} /><circle cx={x} cy={y} r={6.5} fill={ink} stroke="none" /></g>; break;
					case 'deadDot': el = <circle cx={x} cy={y + 2} r={4.5} fill={ink} stroke="none" />; break;
					case 'half':
						el = <g><ellipse cx={x} cy={y + 3} rx={10} ry={10} fill={ink} /><rect x={x - 15} y={y - 13} width={30} height={12} fill={WHITE} stroke="none" /><rect x={x - 15} y={y - 4} width={30} height={7} rx={3.5} fill={ink} stroke="none" /></g>; break;
					case 'side':
						el = <g><ellipse cx={x + 5} cy={y + 4} rx={8} ry={9} fill={ink} /><rect x={x - 15} y={y - 3} width={30} height={7} rx={3.5} fill={ink} stroke="none" /></g>; break;
					case 'squint': el = <rect x={x - 13} y={y - 4} width={26} height={9} rx={4.5} fill={ink} />; break;
					case 'happy': el = <path d={`M ${x - 13} ${y + 5} Q ${x} ${y - 13} ${x + 13} ${y + 5}`} stroke={ink} strokeWidth={8.5} strokeLinecap="round" fill="none" />; break;
					case 'squeeze': {
						const s = i === 0 ? 1 : -1;     // > <
						el = <path d={`M ${x - 12 * s} ${y - 12} L ${x + 10 * s} ${y} L ${x - 12 * s} ${y + 12}`} stroke={ink} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" fill="none" />; break;
					}
					case 'x': el = <path d={`M ${x - 12} ${y - 12} L ${x + 12} ${y + 12} M ${x + 12} ${y - 12} L ${x - 12} ${y + 12}`} stroke={ink} strokeWidth={7} strokeLinecap="round" fill="none" />; break;
					case 'spiral': {
						let d = `M ${x} ${y}`;
						for (let k = 1; k <= 22; k++) { const a = k * 0.62 + i * Math.PI, r = k * 0.95; d += ` L ${f(x + Math.cos(a) * r)} ${f(y + Math.sin(a) * r)}`; }
						el = <path d={d} stroke={ink} strokeWidth={4.5} strokeLinecap="round" fill="none" />; break;
					}
					case 'sob': el = <path d={`M ${x - 13} ${y - 3} Q ${x} ${y + 9} ${x + 13} ${y - 3}`} stroke={ink} strokeWidth={7} strokeLinecap="round" fill="none" />; break;
					default: el = <path d={`M ${x - 12} ${y} Q ${x} ${y + 8} ${x + 12} ${y}`} stroke={ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
				}
				// the half-lid blink frame: a skin lid over the top half of an open eye
				return <g key={key}>{el}{lid === 1 && OPEN_EYES.includes(eyes) && <rect x={x - 24} y={y - 26} width={48} height={24} fill={WHITE} stroke="none" />}{lid === 1 && OPEN_EYES.includes(eyes) && <rect x={x - 16} y={y - 4} width={32} height={6} rx={3} fill={ink} stroke="none" />}</g>;
			})}
		</g>
	);
}

function Brows({face, look}: {face: FaceDef; look: number}) {
	if (!face.brow) return null;
	const xs = [329, 371].map((x) => x + look * 9);
	const y = 99 + face.browY;
	return <g>{xs.map((x, i) =>  <rect key={i} x={x - 16} y={y - 5.5} width={32} height={11} rx={5.5} fill={FINK} transform={`rotate(${face.brow![i]} ${x} ${y})`} />)}</g>;
}

/** the face ink (near black, as the refs) and the head white the card shader shades as a sphere */
export const FINK = '#16121c', WHITE = '#ffffff';
/** where a hat brim or hairline meets the head (svg y), for its soft shadow on the forehead; null = bare head */
function brimY(cos: {hat?: string; hair?: string}): number | null {
	const h: Record<string, number> = {tricorn: 84, bicorne: 76, crown: 44, brim: 66, bowler: 58, cap: 96, bonnet: 104, furcap: 98, tiara: 70, helmet: 84};
	if (cos.hat && cos.hat !== 'none' && h[cos.hat] !== undefined) return h[cos.hat];
	if (cos.hair && ['short', 'messy', 'bob', 'wig', 'wigTall', 'updo'].includes(cos.hair)) return 84;
	return null;
}
const FLAPS: Mouth[] = ['o', 'flat', 'bigO', 'grid'];
function MouthShape({kind}: {kind: Mouth}) {
	const x = 350, y = 188, ink = FINK;
	switch (kind) {
		case 'smile': return <path d={`M ${x - 24} ${y - 4} Q ${x} ${y + 18} ${x + 24} ${y - 6}`} stroke={ink} strokeWidth={9} strokeLinecap="round" fill="none" />;
		case 'smallSmile': return <path d={`M ${x - 15} ${y - 2} Q ${x} ${y + 9} ${x + 15} ${y - 3}`} stroke={ink} strokeWidth={8.5} strokeLinecap="round" fill="none" />;
		case 'grin': return <g><path d={`M ${x - 32} ${y - 10} Q ${x} ${y + 34} ${x + 32} ${y - 12} Z`} fill={c('ink-0')} /><path d={`M ${x - 26} ${y - 8} L ${x + 26} ${y - 10} L ${x + 22} ${y - 2} L ${x - 22} ${y} Z`} fill={c('bone-2')} stroke="none" /></g>;
		case 'laugh': return <g><path d={`M ${x - 30} ${y - 12} Q ${x} ${y + 44} ${x + 32} ${y - 12} Z`} fill={c('ink-0')} /><ellipse cx={x + 2} cy={y + 14} rx={14} ry={7} fill={c('coral-3')} stroke="none" /></g>;
		case 'smirk': return <path d={`M ${x - 20} ${y + 2} Q ${x + 6} ${y + 8} ${x + 24} ${y - 10}`} stroke={ink} strokeWidth={9} strokeLinecap="round" fill="none" />;
		case 'o': return <ellipse cx={x} cy={y + 4} rx={12} ry={17} fill={c('ink-0')} />;
		case 'bigO': return <g><ellipse cx={x} cy={y + 8} rx={19} ry={26} fill={c('ink-0')} /><ellipse cx={x} cy={y + 22} rx={11} ry={7} fill={c('coral-3')} stroke="none" /></g>;
		case 'wavy': return <path d={`M ${x - 22} ${y + 2} q 7 -8 14 0 t 14 0 t 14 0`} stroke={ink} strokeWidth={8} strokeLinecap="round" fill="none" />;
		case 'wobble': return <path d={`M ${x - 24} ${y + 6} q 6 -10 12 0 t 12 0 t 12 0 t 12 0`} stroke={ink} strokeWidth={8} strokeLinecap="round" fill="none" />;
		case 'frown': return <path d={`M ${x - 22} ${y + 8} Q ${x} ${y - 10} ${x + 22} ${y + 8}`} stroke={ink} strokeWidth={9} strokeLinecap="round" fill="none" />;
		case 'teeth':
			return <g><rect x={x - 26} y={y - 8} width={52} height={22} rx={6} fill={c('ink-0')} /><rect x={x - 22} y={y - 4} width={44} height={14} rx={3} fill={c('bone-2')} stroke="none" /><path d={`M ${x - 22} ${y + 3} H ${x + 22} M ${x - 8} ${y - 4} V ${y + 10} M ${x + 7} ${y - 4} V ${y + 10}`} stroke={c('bone-0')} strokeWidth={2.5} /></g>;
		case 'grid':     // the grid-teeth grimace: a white box with an ink grid (two rows, four columns)
			return <g><rect x={x - 28} y={y - 10} width={56} height={30} rx={7} fill="#fbf8f2" stroke={ink} strokeWidth={8} /><path d={`M ${x - 28} ${y + 5} H ${x + 28} M ${x - 14} ${y - 10} V ${y + 20} M ${x} ${y - 10} V ${y + 20} M ${x + 14} ${y - 10} V ${y + 20}`} stroke={ink} strokeWidth={4} fill="none" /></g>;
		case 'tongue': return <g><path d={`M ${x - 18} ${y} H ${x + 18}`} stroke={ink} strokeWidth={8} strokeLinecap="round" /><path d={`M ${x - 2} ${y} q 0 22 10 22 q 10 0 10 -22`} fill={c('coral-3')} /></g>;
		default: return <rect x={x - 16} y={y - 3} width={32} height={7} rx={3.5} fill={ink} />;
	}
}

// ------------------------------------------------------------------ emotion marks
type Mark = {t0: number; t1?: number; kind: string};
type Fill = {t0: number; t1?: number; color: string; rise?: number; drain?: number};
const markOn = (m: {t0: number; t1?: number}, t: number) => t >= m.t0 && (m.t1 === undefined || t < m.t1);

function Marks({marks, t}: {marks: Mark[]; t: number}) {
	const out: React.ReactNode[] = [];
	marks.forEach((m, i) => {
		if (!markOn(m, t)) return;
		const fr = Math.floor((t - m.t0) * FPS + 1e-6);          // frames since the mark popped on
		if (m.kind === 'sweat') {
			const dy = Math.min(fr, 12) * 3;                     // slides 36 units over 12 f, then sticks
			out.push(<path key={i} d={`M 206 ${84 + dy} Q 222 ${114 + dy} 206 ${128 + dy} Q 190 ${114 + dy} 206 ${84 + dy} Z`} fill="#a9d8f2" />);
		} else if (m.kind === 'tears') {
			// two streams from under the eyes; three drops per side ride each stream (a new one every 4 f)
			for (const x0 of [303, 359]) {
				out.push(<path key={`${i}s${x0}`} d={`M ${x0 - 7} 128 Q ${x0 - 10} 180 ${x0 - 4} 232 L ${x0 + 8} 232 Q ${x0 + 10} 180 ${x0 + 7} 128 Z`} fill="#a9d8f2" />);
				for (let k = 0; k < 3; k++) {
					const ph = ((fr + k * 4) % 12) / 12;
					out.push(<circle key={`${i}d${x0}${k}`} cx={x0 + 1} cy={138 + ph * 90} r={7} fill="#dff2fb" stroke="none" />);
				}
			}
		} else if (m.kind === 'steam') {
			// outlined puffs pop out of both sides of the head and rise, alternating sides (18 f cycle)
			for (const [side, off] of [[-1, 0], [1, 9]] as const) {
				for (let k = 0; k < 2; k++) {
					const ph = ((fr + off + k * 9) % 18) / 18;
					const s = 0.6 + ph * 0.7, x = 300 + side * (150 + ph * 40), y = 70 - ph * 70;
					out.push(<g key={`${i}p${side}${k}`} transform={`translate(${f(x)} ${f(y)}) scale(${s.toFixed(2)})`}>
						<circle cx={-16} cy={4} r={18} fill="#fbf8f2" /><circle cx={12} cy={-6} r={22} fill="#fbf8f2" /><circle cx={18} cy={14} r={15} fill="#fbf8f2" />
					</g>);
				}
			}
		} else if (m.kind === 'vein') {
			const s = fr % 8 < 4 ? 1 : 1.12;
			out.push(<g key={i} transform={`translate(386 66) scale(${s})`} fill="none" stroke={c('coral-1')} strokeWidth={7} strokeLinecap="round">
				<path d="M -18 -6 Q -6 -6 -6 -18" /><path d="M 6 -18 Q 6 -6 18 -6" /><path d="M 18 6 Q 6 6 6 18" /><path d="M -6 18 Q -6 6 -18 6" />
			</g>);
		} else if (m.kind === 'blush') {
			for (const x of [288, 374]) {
				out.push(<ellipse key={`${i}b${x}`} cx={x} cy={162} rx={26} ry={12} fill="#f4a3b4" stroke="none" opacity={0.9} />);
				out.push(<path key={`${i}h${x}`} d={`M ${x - 14} 168 l 6 -12 M ${x - 2} 168 l 6 -12 M ${x + 10} 168 l 6 -12`} stroke="#d0607a" strokeWidth={3.5} strokeLinecap="round" />);
			}
		}
	});
	return <g>{out}</g>;
}

/** head colour fill level 0..1 at t (rises over `rise` s, drains over `drain` s after t1) */
function fillLevel(fills: Fill[], t: number): {k: number; color: string} | null {
	for (let i = fills.length - 1; i >= 0; i--) {
		const fl = fills[i];
		if (t < fl.t0) continue;
		const rise = fl.rise ?? 0.2, drain = fl.drain ?? 0.2;
		// quantised to whole frames: the fill climbs in drawn steps, on 1s
		const up = clamp(Math.floor((t - fl.t0) * FPS + 1e-6) / Math.max(1, rise * FPS));
		const down = fl.t1 === undefined || t < fl.t1 ? 1 : 1 - clamp(Math.floor((t - fl.t1) * FPS + 1e-6) / Math.max(1, drain * FPS));
		const k = Math.min(up, down);
		if (k > 0) return {k, color: fl.color};
	}
	return null;
}

// ------------------------------------------------------------------ hats, hair, items
function Hair({kind, color, back}: {kind?: string; color: string; back: boolean}) {
	const sh = c('bone-0') === color ? c('sky-3') : c('ink-0');
	if (kind === 'wig' || kind === 'wigTall') {
		if (back) return <g><path d="M 200 120 Q 190 230 236 252 L 214 268 Q 168 220 182 140 Z" fill={color} /><rect x={182} y={178} width={18} height={70} rx={9} fill={c('ink-1')} transform="rotate(14 190 210)" /></g>;
		return (
			<g>
				{kind === 'wigTall' && <ellipse cx={292} cy={36} rx={92} ry={58} fill={color} />}
				<path d="M 186 132 Q 196 30 300 28 Q 394 30 412 104 Q 352 66 282 76 Q 222 88 212 150 Z" fill={color} />
				<circle cx={214} cy={160} r={26} fill={color} /><circle cx={214} cy={210} r={26} fill={color} />
				<path d="M 196 174 Q 214 186 236 172" stroke={sh} strokeWidth={5} fill="none" opacity={0.55} strokeLinecap="round" />
			</g>
		);
	}
	if (kind === 'updo') {
		if (back) return null;
		return <g><ellipse cx={290} cy={20} rx={70} ry={52} fill={color} /><path d="M 186 140 Q 190 40 300 34 Q 404 40 414 120 Q 352 76 290 80 Q 226 86 206 150 Z" fill={color} /></g>;
	}
	if (kind === 'side') {
		if (back) return <path d="M 196 120 Q 176 236 236 270 L 250 250 Q 214 200 222 130 Z" fill={color} />;
		return <path d="M 190 120 Q 190 200 226 236 Q 214 170 232 120 Z" fill={color} />;
	}
	if (kind === 'short') { if (back) return null; return <path d="M 188 136 Q 196 36 304 32 Q 404 38 414 112 Q 360 70 300 82 Q 270 60 240 92 Q 214 104 206 150 Z" fill={color} />; }
	if (kind === 'bob') {
		if (back) return <path d="M 186 120 Q 170 236 214 262 L 250 262 Q 214 190 230 120 Z" fill={color} />;
		return <path d="M 184 150 Q 186 34 300 30 Q 410 34 418 120 Q 380 84 330 92 Q 296 70 262 96 Q 226 104 214 170 Z" fill={color} />;
	}
	if (kind === 'messy') {
		if (back) return null;
		return <path d="M 184 140 L 178 92 L 210 104 L 214 56 L 246 82 L 270 34 L 296 72 L 328 30 L 344 74 L 384 46 L 382 92 L 420 92 L 404 120 Q 340 84 280 94 Q 226 104 206 158 Z" fill={color} />;
	}
	return null;
}
function Hat({kind}: {kind?: string}) {
	if (kind === 'tricorn') return <g><path d="M 160 78 Q 300 120 450 70 Q 420 4 300 -6 Q 186 2 160 78 Z" fill={c('ink-1')} /><path d="M 160 78 Q 300 120 450 70 L 444 84 Q 300 136 166 92 Z" fill={c('amber-3')} /></g>;
	if (kind === 'bicorne') return <g><path d="M 128 76 Q 300 120 470 74 Q 420 -36 300 -40 Q 176 -36 128 76 Z" fill={c('ink-1')} /><circle cx={384} cy={40} r={20} fill={c('tide-0')} /><circle cx={384} cy={40} r={9} fill={c('coral-2')} /></g>;
	if (kind === 'crown') return <g><path d="M 238 44 L 252 -4 L 276 26 L 300 -14 L 324 26 L 348 -4 L 362 44 Z" fill={K.gold} /><circle cx={300} cy={28} r={7} fill={c('coral-2')} /></g>;
	if (kind === 'brim') return <g><ellipse cx={300} cy={66} rx={176} ry={30} fill={c('ink-1')} /><path d="M 214 66 Q 210 -6 300 -14 Q 390 -6 386 66 Z" fill={c('ink-1')} /><path d="M 214 60 Q 300 74 386 60 L 386 46 Q 300 60 214 46 Z" fill={c('amber-3')} /></g>;
	if (kind === 'bowler') return <g><ellipse cx={300} cy={58} rx={140} ry={22} fill={c('ink-1')} /><path d="M 206 58 Q 204 -30 300 -34 Q 396 -30 394 58 Z" fill={c('ink-1')} /><path d="M 208 44 Q 300 58 392 44 L 392 30 Q 300 44 208 30 Z" fill={c('coral-0')} /></g>;
	if (kind === 'cap') return <g><path d="M 192 92 Q 186 18 300 4 Q 404 14 410 70 Q 430 40 470 58 Q 436 80 408 96 Z" fill={c('coral-1')} /><rect x={186} y={78} width={226} height={26} rx={12} fill={c('coral-0')} /></g>;
	if (kind === 'helmet') return <g><path d="M 210 34 Q 300 -76 392 34 Q 300 -18 210 34 Z" fill={c('coral-1')} /><path d="M 188 150 Q 180 18 300 8 Q 420 18 412 150 L 390 150 L 390 98 Q 300 82 210 98 L 210 150 Z" fill={c('amber-2')} /><path d="M 204 86 Q 300 70 396 86" stroke={c('amber-0')} strokeWidth={8} fill="none" /></g>;
	if (kind === 'tiara') return <g><path d="M 190 172 Q 184 12 300 -10 Q 404 4 412 88 Q 440 64 452 80 Q 430 96 412 104 L 412 172 Q 400 180 390 168 L 390 100 Q 300 84 210 100 L 210 168 Q 200 180 190 172 Z" fill={c('bone-2')} /><path d="M 200 98 Q 300 80 400 98" stroke={c('magenta-1')} strokeWidth={12} fill="none" /></g>;
	if (kind === 'bonnet') return <path d="M 186 110 Q 176 10 300 2 Q 424 10 414 110 Q 380 60 300 56 Q 220 60 186 110 Z" fill={c('bone-2')} />;
	if (kind === 'furcap') return <g><path d="M 196 96 Q 186 40 214 20 Q 226 -10 262 -6 Q 290 -24 320 -8 Q 356 -16 378 14 Q 414 34 404 96 Z" fill={c('amber-0')} />{[200, 236, 272, 308, 344, 380].map((x) => <circle key={x} cx={x + 10} cy={96} r={22} fill={c('ochre-0')} />)}</g>;
	return null;
}
/** held items; `swing` (degrees) is the pendulum / follow-through angle about the hand */
function Item({kind, at, swing, t}: {kind: string; at: P2; swing: number; t: number}) {
	const [x, y] = at;
	if (kind === 'candle') {
		return <g transform={`translate(${x} ${y}) scale(1.45) translate(${-x} ${-y})`}>
			<rect x={x - 24} y={y - 6} width={48} height={12} rx={6} fill={K.gold} /><rect x={x - 11} y={y - 56} width={22} height={52} rx={5} fill={c('bone-2')} />
			<path d={`M ${x} ${y - 98} Q ${x + 13} ${y - 70} ${x} ${y - 58} Q ${x - 13} ${y - 70} ${x} ${y - 98} Z`} fill={c('amber-3')} />
		</g>;
	}
	if (kind === 'key' || kind === 'tag' || kind === 'lantern') {
		// dangling things hang from the hand and swing about it
		const g = (body: React.ReactNode) => <g transform={`rotate(${f(swing)} ${x} ${y})`}><path d={`M ${x} ${y} V ${y + 46}`} stroke={K.ink} strokeWidth={5} />{body}</g>;
		if (kind === 'key') return g(<g><circle cx={x} cy={y + 58} r={14} fill={K.gold} /><rect x={x - 5} y={y + 66} width={10} height={44} rx={4} fill={K.gold} /><rect x={x + 3} y={y + 96} width={16} height={8} rx={3} fill={K.gold} /></g>);
		if (kind === 'tag') return g(<g><path d={`M ${x - 28} ${y + 50} H ${x + 28} V ${y + 110} H ${x - 28} Z`} fill={c('bone-2')} /><circle cx={x} cy={y + 60} r={5} fill={K.ink} /></g>);
		const fl = 1 + 0.08 * Math.sin(Math.floor(t * 12) * 1.7);
		return g(<g>
			<circle cx={x} cy={y + 96} r={64 * fl} fill={c('amber-4')} opacity={0.22} stroke="none" />
			<rect x={x - 30} y={y + 46} width={60} height={14} rx={6} fill={c('ink-1')} />
			<rect x={x - 24} y={y + 60} width={48} height={66} rx={10} fill={c('amber-4')} />
			<path d={`M ${x - 24} ${y + 78} H ${x + 24} M ${x - 24} ${y + 104} H ${x + 24}`} stroke={c('ink-1')} strokeWidth={5} />
			<rect x={x - 30} y={y + 124} width={60} height={14} rx={6} fill={c('ink-1')} />
		</g>);
	}
	if (kind === 'pick') {
		return <g transform={`rotate(${f(-30 + swing)} ${x} ${y})`}><rect x={x - 7} y={y - 120} width={14} height={140} rx={6} fill={c('ochre-1')} /><path d={`M ${x - 78} ${y - 112} Q ${x} ${y - 156} ${x + 78} ${y - 112} L ${x + 72} ${y - 100} Q ${x} ${y - 136} ${x - 72} ${y - 100} Z`} fill={c('sky-0')} /></g>;
	}
	if (kind === 'shield') {
		return <g><circle cx={x + 10} cy={y + 10} r={78} fill={c('amber-0')} /><circle cx={x + 10} cy={y + 10} r={66} fill={K.gold} /><circle cx={x + 10} cy={y + 10} r={18} fill={c('amber-2')} /></g>;
	}
	if (kind === 'spade') {
		return <g transform={`rotate(${f(-20 + swing)} ${x} ${y})`}><rect x={x - 6} y={y - 110} width={12} height={150} rx={5} fill={c('ochre-1')} /><path d={`M ${x - 30} ${y + 36} H ${x + 30} V ${y + 80} Q ${x} ${y + 104} ${x - 30} ${y + 80} Z`} fill={c('sky-0')} /></g>;
	}
	if (kind === 'hammer') {
		return <g transform={`rotate(${f(-30 + swing)} ${x} ${y})`}><rect x={x - 7} y={y - 110} width={14} height={130} rx={6} fill={c('ochre-1')} /><rect x={x - 40} y={y - 132} width={80} height={34} rx={8} fill={c('sky-0')} /></g>;
	}
	if (kind === 'letter' || kind === 'photo') {
		return <g transform={`rotate(${f(-12 + swing * 0.4)} ${x} ${y})`}><rect x={x - 34} y={y - 58} width={68} height={86} rx={4} fill={c('bone-2')} />
			{kind === 'photo' ? <rect x={x - 26} y={y - 50} width={52} height={56} fill={c('sky-1')} /> : [0, 1, 2].map((i) => <rect key={i} x={x - 24} y={y - 44 + i * 16} width={48} height={6} rx={3} fill={c('bone-0')} />)}
		</g>;
	}
	if (kind === 'piece') return <g><path d={`M ${x - 18} ${y + 4} L ${x + 18} ${y + 4} L ${x + 12} ${y - 22} Q ${x} ${y - 30} ${x - 12} ${y - 22} Z`} fill={c('bone-2')} /><circle cx={x} cy={y - 34} r={11} fill={c('bone-2')} /></g>;
	return null;
}

// ------------------------------------------------------------------ timing helpers
/** blink state at t: 0 open, 1 half, 2 closed. Seeded irregular schedule 2-8 s apart unless `blinks` is given */
export function blinkState(props: Record<string, unknown>, t: number): 0 | 1 | 2 {
	if (props.noBlink === true) return 0;
	const closedF = Math.round(clamp(num(props.blinkF, 2), 1, 4));
	const half = props.blinkHalf === true;
	const seed = num(props.seed, 1);
	const times: number[] = Array.isArray(props.blinks) ? (props.blinks as number[]) : blinkTimes(seed, t + 1);
	const fr = Math.round(t * FPS);
	for (const b of times) {
		const b0 = Math.round(b * FPS);
		const d = fr - b0;
		if (d >= 0 && d < closedF) return 2;
		if (half && (d === -1 || d === closedF)) return 1;
	}
	return 0;
}
/** the seeded schedule up to tMax: first blink 0.8-3 s in, then 2-8 s apart (irregular) */
export function blinkTimes(seed: number, tMax: number): number[] {
	const out: number[] = [];
	let b = 0.8 + 2.2 * hash(seed * 7.13);
	for (let k = 0; b < tMax && k < 200; k++) { out.push(b); b += 2 + 6 * hash(seed * 13.7 + k * 3.1); }
	return out;
}
/** degrees of follow-through swing for dangling / held items: a damped pendulum kicked by every pose snap */
function swingAt(pose: unknown, t: number): number {
	const pb = stepBlend<string>(pose, t, 'stand');
	if (pb.since > 1.2 || pb.prev === pb.cur) return 0;
	const s = Math.floor(pb.since * FPS + 1e-6) / FPS;        // on 1s
	return 22 * Math.exp(-s / 0.28) * Math.sin((2 * Math.PI * s) / 0.5);
}
/** hat pop: vertical offset (units, negative = up) and tumble (deg) for the most recent pop */
function hatPopAt(pops: unknown, t: number): {dy: number; rot: number} {
	const ts = Array.isArray(pops) ? (pops as number[]).filter((p) => t >= p) : [];
	if (!ts.length) return {dy: 0, rot: 0};
	const fr = Math.floor((t - ts[ts.length - 1]) * FPS + 1e-6);
	if (fr > 24) return {dy: 0, rot: 0};
	// up 60 units in 4 f, falls back by 12 f, one 8-unit bounce, settled by ~20 f; tumbles and rocks to rest
	const hop = fr <= 4 ? -60 * Math.sin((fr / 4) * (Math.PI / 2)) : fr <= 12 ? -60 * Math.cos(((fr - 4) / 8) * (Math.PI / 2)) : fr <= 18 ? -8 * Math.sin(((fr - 12) / 6) * Math.PI) : 0;
	const rot = fr <= 12 ? 24 * Math.sin((fr / 12) * Math.PI) : 10 * Math.exp(-(fr - 12) / 4) * Math.sin(((fr - 12) / 6) * Math.PI * 2);
	return {dy: hop, rot};
}

// ------------------------------------------------------------------ the figure
export const Actor: React.FC<{props: Record<string, unknown>; time: number}> = ({props, time}) => (
	<svg viewBox="0 0 600 700" width="100%" height="100%" preserveAspectRatio="xMidYMax meet" style={{overflow: 'visible'}}>
		<g {...(inkG(props.ink ?? 6) as Record<string, unknown>)}>
			<ActorBody props={props} t={time} />
		</g>
	</svg>
);

export const ActorBody: React.FC<{props: Record<string, unknown>; t: number}> = ({props, t}) => {
	const cos = COSTUMES[str(props.costume, 'plain')] ?? COSTUMES.plain;
	const faceName = step<string>(props.face, t, 'neutral');
	const face = FACES[faceName] ?? FACES.neutral;
	const snapF = clamp(num(props.snapF, 4), 1, 12);
	const pb = stepBlend<string>(props.pose, t, 'stand');
	const u = snapEase(Math.floor(pb.since * FPS + 1e-6) / snapF);  // on 1s, overshoots a little, settles at snapF
	const P0 = POSES[pb.prev] ?? POSES.stand, P1 = POSES[pb.cur] ?? POSES.stand;
	const hl = lerp2(P0[0], P1[0], u);
	const hr = lerp2(P0[1], P1[1], u);
	const seated = props.seated === true;
	const crouch = clamp(track(props.crouch, t, 0));
	// kneel (round 2: "kneels, listens" played standing - crouch reads as standing at phone size): 0..1, the hips drop
	// 165 units, the far knee goes down on the ground with its shin lying back, the near knee comes up in front
	const kneel = clamp(typeof props.kneel === 'boolean' ? (props.kneel ? 1 : 0) : track(props.kneel, t, 0));
	const walk = clamp(track(props.walk, t, 0));
	const look = track(props.look, t, face.look ?? 0);
	const item = step<string>(props.item, t, 'none');
	// walk: four drawn leg poses, a step every stepF frames, a bob on the passing poses. No idle bob at all.
	const stepF = clamp(num(props.stepF, 7), 3, 14);
	const wp = Math.floor((t * FPS) / stepF) % 4;
	const bob = walk > 0.5 ? (wp % 2 ? -10 : 0) : 0;
	const lean = crouch * 8;
	const lid = blinkState(props, t);
	const quoting = inWin(props.quote, t) || inWin(props.talk, t);
	const flapMouth: Mouth | null = quoting ? FLAPS[Math.floor(hash(Math.floor((t * FPS) / 3) * 3.7 + num(props.seed, 1)) * FLAPS.length)] : null;
	const isGown = !!cos.gown;
	const fill = fillLevel((props.fill as Fill[]) ?? [], t);
	const marks = (props.marks as Mark[]) ?? [];
	const swing = swingAt(props.pose, t);
	const pop = hatPopAt(props.hatPop, t);

	let legs: [P2, P2, P2][];
	if (seated) {
		legs = [[HIP_L, [392, 486], [398, 672]], [HIP_R, [430, 478], [440, 672]]];
	} else {
		const sw = walk > 0.5 ? [-0.34, 0, 0.34, 0][wp] : 0;
		const kn = (hip: P2, a: number): [P2, P2, P2] => {
			const foot: P2 = [hip[0] + Math.sin(a) * 210, hip[1] + Math.cos(a) * 210];
			return [hip, [(hip[0] + foot[0]) / 2 + Math.abs(a) * 20, (hip[1] + foot[1]) / 2], foot];
		};
		legs = [kn([HIP_L[0] - 6, HIP_L[1]], -0.08 + sw), kn([HIP_R[0] + 6, HIP_R[1]], 0.08 - sw)];
		if (kneel > 0) {
			const K2: [P2, P2, P2][] = [[[262, 470], [236, 520], [112, 522]], [[338, 470], [436, 426], [446, 522]]];   // relative to hips at 470; feet land on 686 after the drop
			legs = legs.map((l, i) => l.map((p, j) => lerp2(p, K2[i][j], kneel)) as [P2, P2, P2]);
		}
	}
	const kneelDrop = kneel * 165;
	const bodyY = bob + crouch * 120 + kneelDrop;
	const level = fill ? 268 - (268 - 26) * fill.k : 300;
	const wave = fill ? Array.from({length: 13}, (_, i) => `L ${170 + i * 22} ${f(level + Math.sin(i * 1.3 + Math.floor(t * 12)) * 5)}`).join(' ') : '';

	return (
		<g>
			{seated && props.chair !== false && (
				<g>
					<rect x={150} y={250} width={40} height={250} rx={12} fill={c('coral-0')} />
					<rect x={150} y={486} width={300} height={34} rx={10} fill={c('amber-0')} />
					<rect x={168} y={516} width={20} height={174} fill={c('amber-0')} /><rect x={412} y={516} width={20} height={174} fill={c('amber-0')} />
				</g>
			)}
			{!isGown && legs.map(([h, k, ft], i) => (
				<g key={i}>
					<path d={`M ${f(h[0])} ${f(h[1] + (bodyY - kneelDrop) * 0.4 + kneelDrop)} L ${f(k[0])} ${f(k[1] + crouch * 60 + kneelDrop)} L ${f(ft[0])} ${f(ft[1] + kneelDrop)}`} stroke={cos.legs} strokeWidth={LIMB + 4} strokeLinecap="round" strokeLinejoin="round" fill="none" />
					<ellipse cx={ft[0] + 16} cy={ft[1] + 2 + kneelDrop} rx={34} ry={16} fill={cos.shoes} />
				</g>
			))}
			<g transform={`translate(0 ${f(bodyY)}) rotate(${f(lean)} 300 470)`}>
				<Hair kind={cos.hair} color={cos.hairColor ?? K.ink} back />
				<Limb sh={SH_L} hand={hl} out={-1} sleeve={cos.coatShade} skin={K.skinShade} />
				{isGown && <path d={`M 236 404 Q 150 560 110 ${700 - bodyY} L 490 ${700 - bodyY} Q 450 560 364 404 Z`} fill={cos.gown} />}
				<path d="M 236 262 Q 300 246 364 262 L 398 470 Q 300 490 202 470 Z" fill={cos.coat} />
				<path d="M 300 254 Q 336 252 364 262 L 398 470 Q 350 482 318 484 Z" fill={cos.coatShade} />
				{cos.vest && <path d="M 284 262 L 316 262 L 322 452 L 278 452 Z" fill={cos.vest} />}
				{cos.buttons && [300, 340, 380, 420].map((y) => <circle key={y} cx={300} cy={y} r={5.5} fill={K.goldShade} />)}
				{cos.epaulettes && <g><rect x={214} y={262} width={50} height={20} rx={10} fill={K.gold} /><rect x={336} y={262} width={50} height={20} rx={10} fill={K.goldShade} /></g>}
				{cos.cravat && <path d="M 270 258 Q 300 300 330 258 Q 300 252 270 258 Z" fill={cos.cravat} />}
				{/* head: skin, then the colour fill (clipped to the head, under hair and features), hair, face, marks, hat */}
				<g>
					<defs><clipPath id="headclip"><circle cx={HEAD[0]} cy={HEAD[1]} r={HR - 3} /></clipPath><filter id="soft" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="9" /></filter></defs>
					{/* round 2 (owner): the head is a pure white disc with a thick near-black outline (refs: 5.8 % of the head
					    diameter); the card shader shades it as a sphere lit by the scene's key light (card3d.ts), so no shading
					    is painted here. No ear, no cheek dot (both read as odd marks) */}
					<circle cx={HEAD[0]} cy={HEAD[1]} r={HR} fill={WHITE} stroke={FINK} strokeWidth={14} />
					{fill && <path clipPath="url(#headclip)" d={`M 160 300 L 160 ${f(level)} ${wave} L 450 300 Z`} fill={fill.color} stroke="none" />}
					{brimY(cos) !== null && <ellipse clipPath="url(#headclip)" cx={300} cy={brimY(cos)! + 16} rx={130} ry={24} fill="rgba(58, 52, 92, 0.30)" stroke="none" filter="url(#soft)" />}
					<Hair kind={cos.hair} color={cos.hairColor ?? K.ink} back={false} />
					<g transform="translate(318 150) scale(1.32) translate(-340 -168)">
						<Brows face={face} look={look} />
						<Eyes eyes={face.eyes} look={look} lid={lid} />
						{cos.glasses && <g fill="none" stroke={c('ink-1')} strokeWidth={5}><circle cx={329 + look * 10} cy={135} r={22} /><circle cx={371 + look * 10} cy={135} r={22} /></g>}
						<MouthShape kind={flapMouth ?? face.mouth} />
					</g>
					<Marks marks={marks} t={t} />
					<g transform={`translate(0 ${f(pop.dy)}) rotate(${f(pop.rot)} 300 40)`}><Hat kind={cos.hat} /></g>
				</g>
				<Limb sh={SH_R} hand={hr} out={1} sleeve={cos.coat} skin={K.skin} />
				{item !== 'none' && <Item kind={item} at={[hr[0], hr[1] - 6]} swing={swing} t={t} />}
			</g>
		</g>
	);
};
/** an arm drawn as one inked silhouette with its hand (round 2: "the arms read as detached from the hands"): an ink
 * underlay round sleeve and hand together, the sleeve stopping just short of the hand's centre, the hand on top
 * without its own outline, so the sleeve runs into the hand like a cuff */
function Limb({sh, hand, out, sleeve, skin}: {sh: P2; hand: P2; out: number; sleeve: string; skin: string}) {
	const el = ik(sh, hand, UPPER, LOWER, out);
	const dx = hand[0] - el[0], dy = hand[1] - el[1], d = Math.hypot(dx, dy) || 1;
	const cuff: P2 = [hand[0] - (dx / d) * 9, hand[1] - (dy / d) * 9];
	const path = `M ${f(sh[0])} ${f(sh[1])} L ${f(el[0])} ${f(el[1])} L ${f(cuff[0])} ${f(cuff[1])}`;
	return (
		<g>
			<path d={`M ${f(sh[0])} ${f(sh[1])} L ${f(el[0])} ${f(el[1])} L ${f(hand[0])} ${f(hand[1])}`} stroke={K.ink} strokeWidth={LIMB + 12} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			<circle cx={hand[0]} cy={hand[1]} r={23} fill={K.ink} stroke="none" />
			<path d={path} stroke={sleeve} strokeWidth={LIMB} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			<circle cx={hand[0]} cy={hand[1]} r={17} fill={skin} stroke="none" />
			<path d={`M ${f(cuff[0] - (dy / d) * 13)} ${f(cuff[1] + (dx / d) * 13)} L ${f(cuff[0] + (dy / d) * 13)} ${f(cuff[1] - (dx / d) * 13)}`} stroke={K.ink} strokeWidth={4} strokeLinecap="round" />
		</g>
	);
}
function arm(sh: P2, hand: P2, out: number) {
	const el = ik(sh, hand, UPPER, LOWER, out);
	return `M ${f(sh[0])} ${f(sh[1])} L ${f(el[0])} ${f(el[1])} L ${f(hand[0])} ${f(hand[1])}`;
}

/** where the head's centre is (svg units, 600 x 700 box) and its radius at t, after the walk bob, crouch, lean and
 * kneel: the card shader shades the head as a sphere there */
export function headPose(props: Record<string, unknown>, t: number): {x: number; y: number; r: number} {
	const crouch = clamp(track(props.crouch, t, 0));
	const kneel = clamp(typeof props.kneel === 'boolean' ? (props.kneel ? 1 : 0) : track(props.kneel, t, 0));
	const walk = clamp(track(props.walk, t, 0));
	const stepF = clamp(num(props.stepF, 7), 3, 14);
	const wp = Math.floor((t * FPS) / stepF) % 4;
	const bob = walk > 0.5 ? (wp % 2 ? -10 : 0) : 0;
	const bodyY = bob + crouch * 120 + kneel * 165;
	const a = (crouch * 8 * Math.PI) / 180, dx = HEAD[0] - 300, dy = HEAD[1] - 470;
	return {x: 300 + dx * Math.cos(a) - dy * Math.sin(a), y: 470 + dx * Math.sin(a) + dy * Math.cos(a) + bodyY, r: HR};
}
