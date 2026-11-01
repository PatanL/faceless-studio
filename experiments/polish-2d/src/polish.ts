/**
 * Storyboard -> polished storyboard. Pure data transform over the live episode JSON; the kit is
 * untouched. Everything here is something a storyboard writer (or pipeline/episodes/build.py) could
 * emit, given the extra components registered in Root.tsx.
 *
 * Applied to the scenes that start inside `untilS` (the first ~10 s):
 *  lighting   figures -> polish/Lit (rim + form shading from one scene light), a halo behind each orca,
 *             one polish/Light plane (surface glow + rays faded above the captions)
 *  depth      far pod plane (depth .35, CSS blur 2.5), haze sheet (depth .5), foreground bokeh (depth 1.5),
 *             a lateral camera drift through the planes, hand-held drift (low-amplitude shake, no decay)
 *  motion     spring drops with squash for the cars, spring pop with follow-through for YOU, backOut on
 *             camera punch-ins, camera pre-roll so frame 1 already moves, lagged float on the YOU tag
 *             chain, a slow body pitch on orcas, small camera kicks on landings
 *  texture    feTurbulence grain off (overlays.grain = 0); PolishedEpisode draws a static world-locked tile
 *  grade      scene grade saturate 1.12, contrast 1.05
 *  audio      voice src -> polish_audio.wav (same mix.wav + designed SFX, built by audio/make_audio.sh)
 */

type J = Record<string, any>;

const FIGURES: Record<string, string> = {
	'explainer/Orca': 'orca',
	'explainer/Diver': 'diver',
	'explainer/You': 'you',
	'explainer/Car': 'car',
};

const LIGHT = {angle: 80, rim: 6, rimColor: '#c9f3ff', rimOpacity: 0.62, hi: 0.16, lo: 0.42, loColor: '#03141d'};
const SMALL_LIGHT = {...LIGHT, rim: 3.5, rimOpacity: 0.65, lo: 0.3};

const clone = <T>(v: T): T => JSON.parse(JSON.stringify(v));

function litLayer(l: J): J {
	const species = FIGURES[l.name];
	const small = typeof l.width === 'number' && l.width < 320;
	return {
		...l,
		name: 'polish/Lit',
		props: {...l.props, species, flip: !!l.flipX, light: small ? SMALL_LIGHT : LIGHT},
	};
}

function haloFor(l: J, alpha: number): J {
	const w = typeof l.width === 'number' ? l.width : 900;
	const h = typeof l.height === 'number' ? l.height : 360;
	return {
		type: 'component',
		name: 'polish/Halo',
		x: l.x,
		y: l.y,
		width: w * 1.45,
		height: h * 2.1,
		depth: l.depth ?? 1,
		z: (l.z ?? 0) - 0.5,
		start: l.start,
		end: l.end,
		keyframes: clone(l.keyframes ?? []),
		idle: clone(l.idle ?? []),
		enter: l.enter ? clone(l.enter) : undefined,
		props: {alpha, pulse: 0.25},
	};
}

/** Phase lag (radians) for a float idle so a child follows its parent `lagS` seconds late. */
const lagPhase = (speed: number, lagS: number) => -2 * Math.PI * speed * lagS;

export type PolishOpts = {untilS?: number; audioSrc?: string; lighting?: boolean; depth?: boolean; motion?: boolean; grade?: boolean};

export function polishStoryboard(input: J, opts: PolishOpts = {}): J {
	const sb = clone(input);
	const until = opts.untilS ?? 10;
	const LIT = opts.lighting ?? true;
	const DEPTH = opts.depth ?? true;
	const MOTION = opts.motion ?? true;
	const GRADE = opts.grade ?? true;
	sb.overlays = {...sb.overlays, grain: 0};
	if (opts.audioSrc) {
		sb.audio = {...sb.audio, voice: sb.audio.voice.map((v: J) => ({...v, src: opts.audioSrc}))};
	}

	let t0 = 0;
	sb.scenes = sb.scenes.map((scene: J, si: number) => {
		const start = t0;
		t0 += scene.duration;
		if (start >= until) return scene;
		const sc = clone(scene);
		const dur = sc.duration;
		const layers: J[] = [];
		const kicks: J[] = [];

		for (const l of sc.layers as J[]) {
			// --- figures: lit, cars spring-drop, YOU spring-pop
			if (l.type === 'component' && FIGURES[l.name]) {
				const lit = LIT ? litLayer(l) : {...l, props: {...l.props}};
				const innerName = LIT ? 'polish/Lit' : l.name;
				if (l.name === 'explainer/Orca') {
					if (LIT) layers.push(haloFor(l, si === 0 ? 0.2 : 0.16));
					if (MOTION) lit.idle = [...(lit.idle ?? []), {type: 'sway', amount: 0.7, speed: 0.22, phase: 0.8}];
				}
				if (MOTION && l.enter?.type === 'drop') {
					const at = l.enter.at ?? l.start ?? 0;
					const fall = 0.22;
					kicks.push({at: at + fall, duration: 0.3, amplitude: 3.5, frequency: 11, rotate: 0.12, decay: true});
					layers.push({
						...lit,
						enter: undefined,
						name: 'polish/Spring',
						props: {inner: innerName, innerProps: lit.props, kind: 'drop', at, fall, distance: 110, squash: 0.22},
					});
					continue;
				}
				if (MOTION && l.enter?.type === 'pop') {
					const at = l.enter.at ?? l.start ?? 0;
					layers.push({
						...lit,
						enter: undefined,
						name: 'polish/Spring',
						props: {inner: innerName, innerProps: lit.props, kind: 'pop', at, damping: 10, stiffness: 170, mass: 0.55, origin: '50% 78%'},
					});
					continue;
				}
				layers.push(lit);
				continue;
			}
			layers.push(l);
		}

		// --- secondary motion: the diver -> tether line -> YOU tag chain follows with a lag
		const diver = MOTION ? layers.find((l) => l.props?.species === 'diver' || l.name === 'explainer/Diver') : undefined;
		const df = diver?.idle?.find((i: J) => i.type === 'float');
		if (diver && df) {
			for (const l of layers) {
				if (l === diver) continue;
				const sameX = l.x === diver.x;
				if (!sameX) continue;
				if (l.type === 'svg') l.idle = [{...df, phase: (df.phase ?? 0) + lagPhase(df.speed, 0.07)}];
				if (l.name === 'explainer/Tag') l.idle = [{...df, phase: (df.phase ?? 0) + lagPhase(df.speed, 0.16)}];
			}
		}

		// --- depth + light planes (normal alpha; see fx.tsx)
		const podOpacity = si === 0 ? 0.55 : 0.38;
		if (DEPTH) layers.push(
			{type: 'component', name: 'polish/FarPod', depth: 0.35, z: -8, blur: 2.5, opacity: podOpacity, props: {
				color: '#0e3644',
				items: [
					{x: 0.18, y: 0.6, w: 250, speed: 16, t0: 0.2},
					{x: 0.86, y: 0.66, w: 190, flip: true, speed: 11, t0: 1.1},
					{x: 0.32, y: 0.71, w: 150, speed: 9, t0: 0.5},
				],
			}},
			{type: 'component', name: 'polish/Haze', depth: 0.5, z: -7, props: {top: 0, mid: 0.1, bottom: 0.42}},
			{type: 'component', name: 'polish/Bokeh', depth: 1.5, z: 15, props: {count: 11, seed: 7 + si, band: [0.6, 0.86]}},
		);
		if (LIT) layers.push({type: 'component', name: 'polish/Light', depth: 0.25, z: -6, props: {rays: 5, strength: si === 0 ? 1 : 0.8, fadeAt: 0.6, seed: 3 + si}});
		sc.layers = layers;

		// --- camera: pre-roll on the first scene, backOut punch-ins, lateral drift, hand-held drift, kicks
		const cam: J = sc.camera ?? {keyframes: []};
		const kfs: J[] = cam.keyframes ?? [];
		if (MOTION && si === 0 && kfs.length > 1 && kfs[0].t === 0 && kfs[1].ease === 'inOut') {
			// Camera pre-roll [ME R10]: the first move should already be under way on frame 1. The schema
			// rejects negative keyframe times (Seconds = min(0)), so the pre-rolled curve (an inOut that
			// started at t = -0.3) is baked into linear keys every 2 frames. Frame 0 keeps the cover framing.
			const k0 = kfs[0];
			const k1 = kfs[1];
			const pct = (v: unknown, d: number) => (typeof v === 'string' ? parseFloat(v) : d);
			const P = 0.3;
			const span = k1.t + P;
			const io = (p: number) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
			const p0 = io(P / span);
			// back-solve the virtual start so the curve passes through k0 at t = 0
			const v0 = (v: number, c: number) => (v - p0 * c) / (1 - p0);
			const z0 = v0(k0.zoom, k1.zoom ?? 1);
			const x0 = v0(pct(k0.x, 50), pct(k1.x, 50));
			const y0 = v0(pct(k0.y, 50), pct(k1.y, 50));
			const at = (t: number, a: number, b: number) => a + (b - a) * io((t + P) / span);
			const baked: J[] = [];
			for (let f = 0; f < Math.round(k1.t * 30); f += 2) {
				const t = f / 30;
				baked.push({
					t,
					zoom: +at(t, z0, k1.zoom ?? 1).toFixed(4),
					x: `${at(t, x0, pct(k1.x, 50)).toFixed(3)}%`,
					y: `${at(t, y0, pct(k1.y, 50)).toFixed(3)}%`,
					ease: 'linear',
				});
			}
			kfs.splice(0, 1, ...baked);
			kfs[baked.length] = {...k1, ease: 'linear'};
		}
		for (let i = 1; MOTION && i < kfs.length; i++) {
			const a = kfs[i - 1];
			const b = kfs[i];
			if (b.ease === 'out' && typeof a.zoom === 'number' && typeof b.zoom === 'number' && b.zoom - a.zoom > 0.08 && b.t - a.t <= 0.3) {
				b.ease = 'backOut';
			}
		}
		if (DEPTH && si === 1) {
			const first = kfs[0];
			const last = kfs[kfs.length - 1];
			if (first?.x === '50%' && last?.x === '50%') {
				first.x = '48.6%';
				last.x = '51.4%';
			}
		}
		cam.keyframes = kfs;
		if (MOTION) {
			cam.shake = [
				...(cam.shake ?? []),
				{at: 0, duration: dur, amplitude: 4, frequency: 0.22, rotate: 0, decay: false},
				...kicks,
			];
		}
		sc.camera = cam;

		if (GRADE) sc.grade = {brightness: 1.02, contrast: 1.05, saturate: 1.12, ...(sc.grade ?? {})};
		return sc;
	});
	return sb;
}
