import React, {useId} from 'react';
import type {KitComponent} from '../../core/registry';
import {mPerUnit, type DrawCtx, type Figure} from './figure';
import {LAND} from './land';
import {MARINE} from './marine';
import {PEOPLE} from './people';
import {ANATOMY} from './anatomy';
import {ORCA_KIT_FIGURES} from './orca_kit';
import {bool, num, safeId, str} from './util';

export const FIGURES: Record<string, Figure> = {...MARINE, ...LAND, ...PEOPLE, ...ANATOMY, ...ORCA_KIT_FIGURES};

const norm = (s: string) => s.toLowerCase().replace(/[^a-z]/g, '');
const ALIASES: Record<string, string> = {
	spermwhale: 'spermWhale',
	colossalsquid: 'colossalSquid',
	squid: 'colossalSquid',
	orca: 'orca',
	killerwhale: 'orca',
	greatwhite: 'greatWhite',
	greatwhiteshark: 'greatWhite',
	shark: 'greatWhite',
	bluewhale: 'blueWhale',
	anglerfish: 'anglerfish',
	angler: 'anglerfish',
	octopus: 'octopus',
	giantoctopus: 'octopus',
	giantpacificoctopus: 'octopus',
	crocodile: 'crocodile',
	saltwatercrocodile: 'crocodile',
	croc: 'crocodile',
	hippo: 'hippo',
	hippopotamus: 'hippo',
	grizzly: 'grizzly',
	grizzlybear: 'grizzly',
	bear: 'grizzly',
	diver: 'diver',
	scubadiver: 'diver',
	you: 'you',
	stickfigure: 'you',
	person: 'you',
	bus: 'bus',
	citybus: 'bus',
	car: 'car',
	elephant: 'elephant',
	golfcart: 'golfCart',
	whaleheart: 'whaleHeart',
	whaletongue: 'whaleTongue',
	whalethroat: 'whaleThroat',
	dinosaur: 'sauropod',
	seal: 'seal',
	harbourseal: 'seal',
	harborseal: 'seal',
	liver: 'liver',
};

/** Resolve a species/object name (any case / spacing) and optional pose. */
export function getFigure(name: string, pose?: string): Figure | undefined {
	const key = ALIASES[norm(name)] ?? name;
	const f = FIGURES[key];
	if (!f) return undefined;
	if (pose && f.poses?.[pose]) return {...f, ...f.poses[pose]};
	return f;
}

/** Real-world size (m) of a figure's bounding box. */
export function realSize(f: Figure): {w: number; h: number} {
	const m = mPerUnit(f);
	return {w: f.box[2] * m, h: f.box[3] * m};
}

export function makeCtx(props: Record<string, unknown>, time: number, id: string): DrawCtx {
	return {
		t: time + num(props.timeOffset, 0),
		p: props,
		id,
		sil: typeof props.silhouette === 'string' ? props.silhouette : props.silhouette === true ? '#06141b' : undefined,
		idle: bool(props.idle, true),
		speed: num(props.speed, 1),
		amp: num(props.amp, 1),
	};
}

/** Draw a figure into a box (x, y, w, h) of an enclosing SVG, keeping its aspect. */
export const FigureSVG: React.FC<{f: Figure; ctx: DrawCtx; x: number; y: number; w: number; h: number; align?: string}> = ({f, ctx, x, y, w, h, align = 'xMidYMax'}) => {
	const [bx, by, bw, bh] = f.box;
	return (
		<svg x={x} y={y} width={w} height={h} viewBox={`${bx} ${by} ${bw} ${bh}`} preserveAspectRatio={`${align} meet`} overflow="visible">
			{f.draw(ctx)}
		</svg>
	);
};

/**
 * explainer/Creature: any figure by name.
 * props: species, pose, pxPerM (true scale; otherwise fit the layer box), align ("center"|"bottom"),
 * silhouette (true | colour), idle, speed, amp, plus figure-specific props
 * (jaw, teeth, hooks, yawn, torch, arms, kick, fins, suit, pose, text, color).
 */
export const Creature: KitComponent = ({props, time, width, height}) => {
	const id = safeId(useId());
	const f = getFigure(str(props.species, 'spermWhale'), typeof props.pose === 'string' ? props.pose : undefined);
	if (!f) return <div style={{color: '#f0f', fontSize: 30}}>unknown species {String(props.species)}</div>;
	const ctx = makeCtx(props, time, id);
	const [bx, by, bw, bh] = f.box;
	const ppm = typeof props.pxPerM === 'number' ? props.pxPerM : null;
	const bottom = str(props.align, 'center') === 'bottom';
	if (ppm) {
		const {w, h} = realSize(f);
		const W = w * ppm;
		const H = h * ppm;
		return (
			<svg
				viewBox={`${bx} ${by} ${bw} ${bh}`}
				width={W}
				height={H}
				style={{position: 'absolute', left: (width - W) / 2, top: bottom ? height - H : (height - H) / 2, overflow: 'visible'}}
			>
				{f.draw(ctx)}
			</svg>
		);
	}
	return (
		<svg viewBox={`${bx} ${by} ${bw} ${bh}`} width="100%" height="100%" preserveAspectRatio={bottom ? 'xMidYMax meet' : 'xMidYMid meet'} style={{overflow: 'visible', display: 'block'}}>
			{f.draw(ctx)}
		</svg>
	);
};

/** Fixed-species wrapper so storyboards can say "explainer/SpermWhale". */
export const fixed =
	(species: string): KitComponent =>
	(p) => <Creature {...p} props={{...p.props, species: p.props.species ?? species}} />;
