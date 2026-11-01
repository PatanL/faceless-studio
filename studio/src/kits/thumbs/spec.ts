/**
 * Thumbnail spec. Pure module (no React) so the CLI can import the template list.
 *
 * Formula (from R1's Depth Theory teardown + the horror chat-story refs):
 *   one BIG subject + one TINY human for scale, 2-4 words of high-contrast text,
 *   and exactly ONE red accent (the key word; explainer templates let it continue as a
 *   hand-drawn pointer). Everything else is monochrome / desaturated.
 */

export type Niche = 'explainer' | 'horror';
export type ThumbFormat = '16:9' | '9:16';

export const TEMPLATES: Record<Niche, string[]> = {
	// eye: giant creature head/eye fills 2/3, sonar rings, tiny diver + red arrow ("IT SEES YOU")
	// scale: whole creature side-on, tiny human at its eye, scale ruler ("30 M LONG")
	// abyss: diver in a light cone, a vast lure-fish below in the dark ("NOT A LIGHT")
	explainer: ['eye', 'scale', 'abyss'],
	// door: huge door ajar, towering figure in the gap, tiny resident with phone ("DON'T OPEN IT")
	// chat: giant phone with the group chat, tiny person in bed lit by it ("WHO SENT THIS?")
	// hallway: endless corridor, too-tall figure at the end, tiny resident ("ROOM 802")
	horror: ['door', 'chat', 'hallway'],
};

export const SIZES: Record<ThumbFormat, {width: number; height: number}> = {
	'16:9': {width: 1280, height: 720},
	'9:16': {width: 1080, height: 1920},
};

export type ChatLine = {from?: string; text: string; me?: boolean};

export type ThumbSpec = {
	/** Output basename (CLI appends _<template>_<16x9|9x16>.png). */
	id?: string;
	niche: Niche;
	template: string;
	format?: ThumbFormat;
	/** 2-4 words. Use "\n" to force a line break. */
	text: string;
	/** Word(s) of `text` drawn in red. Default: the last word. */
	accent?: string;
	/** Built-in placeholder subject: explainer whale | squid | angler; horror figure. */
	subject?: string;
	/**
	 * Optional kit art override: any component registered by src/kits/* (e.g.
	 * "explainer/SpermWhale"). Rendered at time `art.time` (default 0) in the subject's box.
	 * `facing` is the way the kit drawing faces (explainer kit figures face "right", the default);
	 * the templates' placeholders face left, so right-facing art is mirrored to match.
	 */
	art?: {component: string; props?: Record<string, unknown>; time?: number; facing?: 'left' | 'right'};
	/** Optional kit art override for the tiny human (e.g. "explainer/Diver", "horror/Resident"). */
	humanArt?: {component: string; props?: Record<string, unknown>; time?: number};
	/** Small label next to the human ("YOU") or on the ruler ("30 m"). */
	label?: string;
	humanLabel?: string;
	/** horror/chat: the chat lines shown on the phone (last one is the scary one). */
	chat?: ChatLine[];
	chatTitle?: string;
	/** horror/door + hallway: the room / apartment number on the door. */
	room?: string;
	/** Override the template's background tone (CSS color). */
	bg?: string;
	/** Hide the red pointer arrow (explainer). */
	noArrow?: boolean;
	/** Scale the subject about its anchor (scale 9:16: < 1 pulls the tail down, clear of the headline). Default 1. */
	subjectScale?: number;
};

export const RED = '#ff1f1f';

export function slug(s: string) {
	return s
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, '-')
		.replace(/^-|-$/g, '')
		.slice(0, 40);
}
