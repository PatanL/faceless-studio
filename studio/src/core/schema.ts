/**
 * Storyboard JSON schema (zod v4). Pure module: no React / Remotion imports, so the
 * pipeline (node) can import it to validate or to emit a JSON Schema.
 *
 * Units
 * - Time is in SECONDS. Scene-level times (keyframes, enter/exit, callouts, scene sfx)
 *   are relative to the scene's nominal start. Global times (captions, audio) are
 *   relative to the start of the video.
 * - Positions are pixels in composition space (1080x1920 for 9:16, 1920x1080 for 16:9)
 *   or percentage strings ("50%") of the frame width (x) / height (y).
 *   (x, y) is where the layer's anchor point sits; the anchor defaults to its centre.
 * - Scenes are laid end to end: scene N starts at the sum of the previous durations.
 *   A transition is centred on the boundary and never changes the total length.
 */
import {z} from 'zod';

// ---------------------------------------------------------------- primitives

export const Coord = z
	.union([z.number(), z.string().regex(/^-?\d+(\.\d+)?%$/, 'use a number (px) or "NN%"')])
	.describe('Pixels, or a percentage string of frame width (x) / height (y)');
export type Coord = z.infer<typeof Coord>;

export const EaseName = z.enum([
	'linear',
	'in',
	'out',
	'inOut',
	'backIn',
	'backOut',
	'elastic',
	'bounce',
	'step',
]);
export type EaseName = z.infer<typeof EaseName>;

const Color = z.string().describe('Any CSS color');
const Seconds = z.number().min(0);

/** A keyframe on a layer. Properties left out are interpolated from neighbouring keyframes. */
export const Keyframe = z.object({
	t: Seconds.describe('Scene-local time in seconds'),
	x: Coord.optional(),
	y: Coord.optional(),
	scale: z.number().optional(),
	scaleX: z.number().optional(),
	scaleY: z.number().optional(),
	rotate: z.number().optional().describe('Degrees'),
	opacity: z.number().min(0).max(1).optional(),
	ease: EaseName.optional().describe('Easing used to arrive at this keyframe (default inOut)'),
});
export type Keyframe = z.infer<typeof Keyframe>;

export const AnimType = z.enum([
	'fade',
	'pop',
	'slideUp',
	'slideDown',
	'slideLeft',
	'slideRight',
	'zoomIn',
	'zoomOut',
	'wipeRight',
	'wipeDown',
	'drop',
	// house-style motion (STYLE_BIBLE §9.2): a uniform spring pop that never draws thinner than 60 % of rest width
	// (fixes the polish-2d YOU glitch), and a gravity drop with a volume-keeping landing squash about the layer bottom
	'popSpring',
	'dropSquash',
]);
export const Anim = z.object({
	type: AnimType.default('fade'),
	at: Seconds.optional().describe('Start time (enter: default = layer start; exit: default = end - duration)'),
	duration: z.number().positive().default(0.4),
	distance: z.number().default(160).describe('px for slide/drop'),
});
export type Anim = z.infer<typeof Anim>;

export const Idle = z.object({
	type: z.enum(['bob', 'breathe', 'sway', 'float', 'pulse', 'spin', 'jitter']),
	amount: z.number().optional().describe('px for bob/float/jitter, fraction for breathe/pulse, degrees for sway'),
	speed: z.number().default(0.5).describe('Cycles per second (spin: turns per second)'),
	phase: z.number().default(0),
});
export type Idle = z.infer<typeof Idle>;

// ---------------------------------------------------------------- layers

const layerBase = {
	id: z.string().optional(),
	x: Coord.default('50%'),
	y: Coord.default('50%'),
	width: Coord.optional(),
	height: Coord.optional(),
	anchorX: z.number().default(0.5),
	anchorY: z.number().default(0.5),
	scale: z.number().default(1),
	rotate: z.number().default(0),
	opacity: z.number().min(0).max(1).default(1),
	flipX: z.boolean().default(false),
	depth: z
		.number()
		.default(1)
		.describe('Parallax factor: 0 = fixed to screen, 1 = moves with the camera, >1 = foreground'),
	z: z.number().default(0).describe('Stacking order; ties keep array order'),
	start: Seconds.optional().describe('Scene-local appear time'),
	end: Seconds.optional().describe('Scene-local disappear time'),
	keyframes: z.array(Keyframe).default([]),
	enter: Anim.optional(),
	exit: Anim.optional(),
	idle: z.array(Idle).default([]),
	blur: z.number().min(0).optional().describe('px'),
	shadow: z.string().optional().describe('CSS drop-shadow() arguments, e.g. "0 20px 30px rgba(0,0,0,.5)"'),
	blend: z.string().optional().describe('CSS mix-blend-mode'),
	role: z
		.enum(['hero', 'prop', 'label', 'dressing', 'fx'])
		.optional()
		.describe('Staging role for the build checker (pipeline/episodes/staging.py); ignored by the renderer. Default: inferred'),
	allowOverlap: z.boolean().optional().describe('Staging checker: this layer may touch the hero on purpose (contact beats)'),
};

export const RectLayer = z.object({
	...layerBase,
	type: z.literal('rect'),
	fill: Color.default('#ffffff'),
	stroke: Color.optional(),
	strokeWidth: z.number().default(0),
	radius: z.number().default(0),
});

export const CircleLayer = z.object({
	...layerBase,
	type: z.literal('circle'),
	fill: Color.default('#ffffff'),
	stroke: Color.optional(),
	strokeWidth: z.number().default(0),
});

export const TextLayer = z.object({
	...layerBase,
	type: z.literal('text'),
	text: z.string(),
	fontSize: z.number().default(96),
	font: z.string().default('display').describe('"display", "body", "condensed" or a CSS font-family'),
	weight: z.number().default(900),
	color: Color.default('#ffffff'),
	strokeColor: Color.optional(),
	strokeWidth: z.number().default(0),
	align: z.enum(['left', 'center', 'right']).default('center'),
	uppercase: z.boolean().default(false),
	lineHeight: z.number().default(1.05),
	letterSpacing: z.number().default(0).describe('em'),
	maxWidth: z.number().optional().describe('px; text wraps inside'),
	background: Color.optional(),
	padding: z.number().default(0),
	radius: z.number().default(0),
	typewriter: z
		.object({at: Seconds.default(0), cps: z.number().positive().default(30)})
		.optional()
		.describe('Reveal characters over time'),
});

export const ImageLayer = z.object({
	...layerBase,
	type: z.literal('image'),
	src: z.string().describe('Path under studio/public, or an http(s)/data: URL'),
	fit: z.enum(['contain', 'cover', 'fill']).default('contain'),
});

export const SvgLayer = z.object({
	...layerBase,
	type: z.literal('svg'),
	markup: z.string().optional().describe('Inline <svg>...</svg> markup; it is scaled to the layer box'),
	src: z.string().optional().describe('Or an .svg file under studio/public'),
});

export const ParticlesLayer = z.object({
	...layerBase,
	type: z.literal('particles'),
	preset: z.enum(['bubbles', 'dust', 'snow', 'embers', 'rain', 'stars']).default('dust'),
	count: z.number().int().min(1).max(600).default(60),
	color: Color.optional(),
	size: z.tuple([z.number(), z.number()]).optional().describe('[min, max] px'),
	speed: z.number().default(1).describe('Multiplier on the preset speed'),
	seed: z.number().default(1),
});

export const ComponentLayer = z.object({
	...layerBase,
	type: z.literal('component'),
	name: z.string().describe('Name registered by a kit with registerComponent()'),
	props: z.record(z.string(), z.unknown()).default({}),
});

export const Layer = z.discriminatedUnion('type', [
	RectLayer,
	CircleLayer,
	TextLayer,
	ImageLayer,
	SvgLayer,
	ParticlesLayer,
	ComponentLayer,
]);
export type Layer = z.infer<typeof Layer>;

// ---------------------------------------------------------------- background

const bgBase = {
	depth: z.number().default(0.15).describe('Parallax factor for the background plane'),
	overscan: z.number().min(1).default(1.25).describe('Background is drawn this much larger than the frame'),
};

export const Background = z.discriminatedUnion('type', [
	z.object({type: z.literal('color'), color: Color.default('#000000'), ...bgBase}),
	z.object({
		type: z.literal('gradient'),
		kind: z.enum(['linear', 'radial']).default('linear'),
		angle: z.number().default(180).describe('Degrees, linear only (180 = top to bottom)'),
		colors: z.array(Color).min(2),
		...bgBase,
	}),
	z.object({
		type: z.literal('image'),
		src: z.string(),
		fit: z.enum(['cover', 'contain']).default('cover'),
		...bgBase,
	}),
	z.object({
		type: z.literal('component'),
		name: z.string(),
		props: z.record(z.string(), z.unknown()).default({}),
		...bgBase,
	}),
]);
export type Background = z.infer<typeof Background>;

// ---------------------------------------------------------------- camera

export const CameraKeyframe = z.object({
	t: Seconds,
	x: Coord.optional().describe('World point at the centre of the screen'),
	y: Coord.optional(),
	zoom: z.number().positive().optional(),
	rotate: z.number().optional(),
	ease: EaseName.optional(),
});

export const Shake = z.object({
	at: Seconds.describe('Scene-local start'),
	duration: z.number().positive().default(0.4),
	amplitude: z.number().default(18).describe('px'),
	frequency: z.number().default(14).describe('Hz'),
	rotate: z.number().default(0.6).describe('Max degrees'),
	decay: z.boolean().default(true),
});

export const CameraDrift = z.object({
	zoom: z.number().default(0).describe('Zoom change per second (0.008 = +0.8 %/s)'),
	x: z.number().default(0).describe('World px per second'),
	y: z.number().default(0).describe('World px per second'),
});

export const Camera = z.object({
	preset: z
		.enum(['none', 'pushIn', 'pullOut', 'panLeft', 'panRight', 'panUp', 'panDown', 'drift'])
		.default('none')
		.describe('Used only when keyframes is empty; spans the whole scene'),
	amount: z.number().default(1).describe('Preset strength multiplier'),
	keyframes: z.array(CameraKeyframe).default([]),
	shake: z.array(Shake).default([]),
	drift: CameraDrift.optional().describe('Never-still drift added on top of keyframes (STYLE_BIBLE §9.4)'),
	preroll: z
		.number()
		.min(0)
		.optional()
		.describe('Seconds: the first keyframe move is already under way at its first key (eased as if it began this much earlier)'),
});
export type Camera = z.infer<typeof Camera>;

// ---------------------------------------------------------------- callouts

export const Callout = z.object({
	style: z.enum(['label', 'stat', 'banner', 'lowerThird', 'title']).default('label'),
	text: z.string(),
	sub: z.string().optional().describe('Secondary line (stat label, lower-third subtitle)'),
	at: Seconds.default(0),
	duration: z.number().positive().optional().describe('Default: until the scene ends'),
	x: Coord.optional(),
	y: Coord.optional(),
	color: Color.optional(),
	background: Color.optional(),
	accent: Color.optional(),
	fontSize: z.number().optional(),
	rotate: z.number().default(0),
	enter: AnimType.default('pop'),
});
export type Callout = z.infer<typeof Callout>;

// ---------------------------------------------------------------- transitions / grade

export const Transition = z.object({
	type: z.enum(['cut', 'fade', 'dipBlack', 'whip', 'glitch']).default('cut'),
	duration: z.number().min(0).default(0.4),
	direction: z.enum(['left', 'right', 'up', 'down']).default('left').describe('whip only'),
});
export type Transition = z.infer<typeof Transition>;

export const Grade = z.object({
	brightness: z.number().default(1),
	contrast: z.number().default(1),
	saturate: z.number().default(1),
	hue: z.number().default(0).describe('Degrees'),
	tint: Color.optional(),
	tintOpacity: z.number().min(0).max(1).default(0.25),
	vignette: z.number().min(0).max(1).default(0),
	flicker: z.number().min(0).max(1).default(0).describe('Random brightness flicker strength'),
});
export type Grade = z.infer<typeof Grade>;

// ---------------------------------------------------------------- audio

export const SfxCue = z.object({
	cue: z.string().optional().describe('Name in the SFX folder: <sfxDir>/<cue>.wav'),
	src: z.string().optional().describe('Or an explicit file under studio/public'),
	at: Seconds,
	volume: z.number().min(0).default(0.8),
});
export type SfxCue = z.infer<typeof SfxCue>;

export const Audio = z.object({
	voice: z
		.array(
			z.object({
				src: z.string(),
				start: Seconds.default(0),
				volume: z.number().min(0).default(1),
				duration: z.number().positive().optional().describe('Seconds; used for music ducking'),
			}),
		)
		.default([]),
	music: z
		.array(
			z.object({
				src: z.string(),
				start: Seconds.default(0),
				end: Seconds.optional().describe('Default: end of video'),
				volume: z.number().min(0).default(0.35),
				duckTo: z.number().min(0).default(0.12).describe('Volume while speech plays'),
				attack: z.number().min(0).default(0.15),
				release: z.number().min(0).default(0.45),
				fadeIn: z.number().min(0).default(0.6),
				fadeOut: z.number().min(0).default(1),
				loop: z.boolean().default(true),
			}),
		)
		.default([]),
	sfx: z.array(SfxCue).default([]),
	sfxDir: z.string().default('sfx'),
	duckOn: z
		.enum(['auto', 'voice', 'captions', 'none'])
		.default('auto')
		.describe('auto = voice clips with durations, else caption word timings'),
});

// ---------------------------------------------------------------- captions

export const Word = z.object({
	text: z.string(),
	start: Seconds,
	end: Seconds,
	emph: z.boolean().optional().describe('Draw this word in style.highlight (explicit emphasis, any highlightMode)'),
	br: z.boolean().optional().describe('A caption page starts at this word. If any word has br, pages break only at br words (phrase pages from pipeline/episodes/phrases.py)'),
});
export type Word = z.infer<typeof Word>;

export const CaptionStyle = z.object({
	font: z.string().default('display'),
	weight: z.number().default(900),
	fontSize: z.number().optional().describe('Default 104 (9:16) / 84 (16:9)'),
	color: Color.default('#ffffff'),
	highlight: Color.default('#ffe14d'),
	highlightMode: z.enum(['color', 'box', 'content', 'none']).default('color').describe("'content' = like 'color' but never on stopwords ('and', 'the', 'to'...); 'none' = only Word.emph words"),
	boxColor: Color.default('#ff3b5c'),
	strokeColor: Color.default('#000000'),
	strokeWidth: z.number().default(14),
	shadow: z.boolean().default(true),
	uppercase: z.boolean().default(true),
	y: z.number().min(0).max(1).optional().describe('Vertical centre as a fraction of height (default 0.64 / 0.82)'),
	maxWidth: z.number().optional().describe('px (default 82% of width)'),
	pop: z.boolean().default(true),
	backing: z.number().min(0).max(1).default(0).describe('Opacity of a dark rounded pill behind the caption block (0 = none); keeps it legible over busy UI'),
	backingColor: z.string().default('0,0,0').describe('r,g,b of the backing pill'),
});

export const Captions = z.object({
	enabled: z.boolean().default(true),
	src: z.string().optional().describe('JSON file under studio/public with {words:[...]} or [...] (merged at render time)'),
	words: z.array(Word).default([]),
	maxWords: z.number().int().min(1).max(6).default(3),
	maxChars: z.number().int().min(4).default(18),
	gapBreak: z.number().default(0.45).describe('A pause longer than this starts a new caption page'),
	linger: z.number().default(0.35).describe('Seconds a page stays after its last word if nothing follows'),
	glue: z.array(z.string()).default([]).describe('Phrases a caption page never splits ("golf cart", "beach ball")'),
	style: CaptionStyle.default(CaptionStyle.parse({})),
});
export type Captions = z.infer<typeof Captions>;

// ---------------------------------------------------------------- light (explainer house style, STYLE_BIBLE §4.1 / §5.1)

const Token = z.string().describe('House palette token ("amber-4") or #hex');
export const SceneLight = z.object({
	setup: z.enum(['lantern', 'daylight', 'cold', 'stellar']).default('lantern'),
	angle: z.number().optional().describe('Degrees of the direction TOWARD the key, screen space (0 = right, -90 = up). Default by setup'),
	sweep: z.number().default(0).describe('Degrees the key turns over the scene (light as an actor, <= 15)'),
	rimAngle: z.number().optional().describe('Direction toward the back (rim) light; default opposite-ish to the key'),
	keyColor: Token.optional(),
	rimColor: Token.optional(),
	ambient: Token.optional(),
	ground: Token.optional(),
	haze: Token.optional(),
});
export type SceneLight = z.infer<typeof SceneLight>;

// ---------------------------------------------------------------- scene / storyboard

export const Scene = z.object({
	id: z.string(),
	duration: z.number().positive().describe('Seconds'),
	background: Background.default({type: 'color', color: '#000000', depth: 0.15, overscan: 1.25}),
	layers: z.array(Layer).default([]),
	camera: Camera.optional(),
	callouts: z.array(Callout).default([]),
	transitionIn: Transition.default({type: 'cut', duration: 0.4, direction: 'left'}),
	grade: Grade.optional(),
	sfx: z.array(SfxCue).default([]).describe('Scene-local sound cues'),
	notes: z.string().optional().describe('Narration / intent, ignored by the renderer'),
	light: SceneLight.optional().describe('One light model for every shaded object in the scene (explainer house style)'),
	captionY: z.number().min(0).max(1).optional().describe('Caption centre (fraction of height) while this scene plays; overrides captions.style.y'),
	captionYAt: z
		.array(z.object({at: z.number().describe('Scene-local seconds'), y: z.number().min(0).max(1)}))
		.optional()
		.describe('Caption y changes inside the scene (e.g. low while a punch-in fills the top with phone text)'),
});
export type Scene = z.infer<typeof Scene>;

export const Format = z.enum(['9:16', '16:9']);
export type Format = z.infer<typeof Format>;

export const FORMATS: Record<Format, {width: number; height: number}> = {
	'9:16': {width: 1080, height: 1920},
	'16:9': {width: 1920, height: 1080},
};

/** Areas covered by platform UI. Keep text inside the frame minus these insets. */
export const SAFE_AREA: Record<Format, {top: number; bottom: number; left: number; right: number}> = {
	'9:16': {top: 230, bottom: 440, left: 70, right: 150}, // Shorts / TikTok / Reels overlays
	'16:9': {top: 60, bottom: 90, left: 96, right: 96}, // 5% title-safe
};

export const Theme = z.object({
	fontDisplay: z.string().default('Montserrat'),
	fontBody: z.string().default('Montserrat'),
	fontCondensed: z.string().default('Anton'),
	accent: Color.default('#ffe14d'),
	ink: Color.default('#0b0f14'),
	paper: Color.default('#ffffff'),
});
export type Theme = z.infer<typeof Theme>;

export const StoryboardSchema = z.object({
	version: z.literal(1).default(1),
	id: z.string(),
	title: z.string().optional(),
	format: Format.default('9:16'),
	fps: z.number().int().min(12).max(60).default(30),
	theme: Theme.default(Theme.parse({})),
	scenes: z.array(Scene).min(1),
	captions: Captions.optional(),
	audio: Audio.default(Audio.parse({})),
	overlays: z
		.object({
			grain: z.number().min(0).max(1).default(0),
			vignette: z.number().min(0).max(1).default(0),
			fadeIn: z.number().min(0).default(0).describe('Seconds from black at the start'),
			fadeOut: z.number().min(0).default(0).describe('Seconds to black at the end'),
		})
		.default({grain: 0, vignette: 0, fadeIn: 0, fadeOut: 0}),
});
export type Storyboard = z.infer<typeof StoryboardSchema>;
export type StoryboardInput = z.input<typeof StoryboardSchema>;

// ---------------------------------------------------------------- timing helpers

export type SceneTiming = {
	index: number;
	start: number; // frame of nominal start
	frames: number; // nominal length in frames
	pre: number; // frames rendered before nominal start (incoming transition)
	post: number; // frames rendered after nominal end (outgoing transition)
	inT: Transition;
	inFrames: number;
	outT: Transition | null;
	outFrames: number;
};

export const secToFrames = (s: number, fps: number) => Math.round(s * fps);

export function sceneTimings(sb: Storyboard): {timings: SceneTiming[]; totalFrames: number} {
	const fps = sb.fps;
	let cursor = 0;
	const starts = sb.scenes.map((s) => {
		const start = cursor;
		cursor += secToFrames(s.duration, fps);
		return start;
	});
	const totalFrames = Math.max(1, cursor);
	const transFrames = sb.scenes.map((s, i) => {
		if (i === 0 || s.transitionIn.type === 'cut') return 0;
		const f = secToFrames(s.transitionIn.duration, fps);
		// never longer than either neighbouring scene
		const prevLen = secToFrames(sb.scenes[i - 1].duration, fps);
		const len = secToFrames(s.duration, fps);
		return Math.max(0, Math.min(f, prevLen, len));
	});
	const timings = sb.scenes.map((s, i): SceneTiming => {
		const inFrames = transFrames[i];
		const outFrames = i + 1 < sb.scenes.length ? transFrames[i + 1] : 0;
		return {
			index: i,
			start: starts[i],
			frames: secToFrames(s.duration, fps),
			pre: Math.floor(inFrames / 2),
			post: outFrames - Math.floor(outFrames / 2),
			inT: s.transitionIn,
			inFrames,
			outT: i + 1 < sb.scenes.length ? sb.scenes[i + 1].transitionIn : null,
			outFrames,
		};
	});
	return {timings, totalFrames};
}

export function parseStoryboard(input: unknown): Storyboard {
	return StoryboardSchema.parse(input);
}
