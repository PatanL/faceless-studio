// Pure-logic checks of studio/src/core (findings F17-F21), no node_modules and no render needed.
// Run: node --test tests/          (Node >= 23.2: uses module.stripTypeScriptTypes on slices of the source)
// The JSX-free functions are sliced out of the .ts/.tsx source, type-stripped and evaluated, so the tests
// always exercise the current code. xfail(): the test must FAIL today; if it passes, the bug was fixed and
// the wrapper reports XPASS so the marker gets removed (strict xfail).
import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const src = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8');

function xfail(name, id, fn) {
	test(`${name} [xfail ${id}]`, () => {
		let failed = false;
		try {
			fn();
		} catch (e) {
			failed = true;
			if (process.env.XFAIL_VERBOSE) console.log(`  ${id} fails as expected: ${String(e.message).split('\n')[0].slice(0, 200)}`);
		}
		if (!failed) throw new Error(`XPASS ${id}: the bug looks fixed, remove xfail`);
	});
}

function slice(text, from, to) {
	const a = text.indexOf(from);
	const b = to ? text.indexOf(to, a) : text.length;
	assert.ok(a >= 0 && b > a, `slice markers not found: ${from} .. ${to}`);
	return text.slice(a, b);
}

function evalTs(code, names) {
	const js = stripTypeScriptTypes(code.replace(/^export /gm, ''), {mode: 'strip'});
	return new Function(`${js}\n;return {${names.join(',')}};`)();
}

const {paginate} = evalTs(slice(src('studio/src/core/captions.tsx'), 'const PUNCT_END', 'export type CaptionCue'), ['paginate']);
// end of a top-level function: its closing brace sits at column 0
const fnEnd = (text, start) => text.indexOf('\n}', start) + 2;
const schema = src('studio/src/core/schema.ts');
const stStart = schema.indexOf('export const secToFrames');
const {sceneTimings} = evalTs(schema.slice(stStart, fnEnd(schema, schema.indexOf('export function sceneTimings'))), ['sceneTimings']);

const DEF = {maxWords: 3, maxChars: 18, gapBreak: 0.45, linger: 0.35};
const loadSb = (slug, file = 'storyboard.json') => {
	const p = path.join(ROOT, 'episodes', slug, file);
	return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : null;
};
const words = (spec) => {
	// "word word ..." -> evenly timed words 0.3 s apart
	return spec.split(' ').map((t, i) => ({text: t, start: +(i * 0.3).toFixed(3), end: +(i * 0.3 + 0.25).toFixed(3)}));
};
const texts = (pages) => pages.map((p) => p.words.map((w) => w.text).join(' '));

test('paginate loads and keeps every word (regression guard)', () => {
	const ws = words('The ocean is deep and the water is cold here.');
	const pages = paginate(ws, {...DEF});
	assert.equal(pages.flatMap((p) => p.words).length, ws.length);
});

xfail('F18 abbreviation "Mr." does not end a caption segment', 'F18', () => {
	const ws = words('I opened the chat. Mr. Okafor in Two-A was typing.');
	const pages = paginate(ws, {...DEF, maxWords: 5, maxChars: 18, gapBreak: 0.25});
	assert.ok(!texts(pages).includes('Mr.'), texts(pages).join(' | '));
});

const realPages = (slug) => {
	const sb = loadSb(slug);
	if (!sb?.captions?.words) return null;
	const {timings} = sceneTimings({fps: sb.fps, scenes: sb.scenes.map((s) => ({transitionIn: {type: 'cut'}, ...s}))});
	const cuts = timings.slice(1).map((x) => x.start / sb.fps);
	return {pages: paginate(sb.captions.words, {...DEF, ...sb.captions}, cuts), cuts};
};

xfail('F19 no page ends on an open conjunction (horror-elevator-maintenance: "... then" | "hold ...")', 'F19', () => {
	const r = realPages('horror-elevator-maintenance');
	assert.ok(r, 'storyboard missing');
	const t = texts(r.pages);
	const bad = t.filter((x, i) => i < t.length - 1 && /\b(then|so|when|that|what)$/i.test(x));
	assert.deepEqual(bad, [], bad.join(' | '));
});

xfail('F21 a page is never displayed past the next scene cut', 'F21', () => {
	const ws = [
		{text: 'They', start: 0.0, end: 0.2}, {text: 'never', start: 0.2, end: 0.45}, {text: 'have.', start: 0.45, end: 0.8},
		{text: 'Next', start: 0.95, end: 1.2}, {text: 'scene.', start: 1.2, end: 1.5},
	];
	const cut = 0.9;
	const pages = paginate(ws, {...DEF}, [cut]);
	for (const p of pages) if (p.start < cut) assert.ok(p.end <= cut + 1e-6, `page "${p.words.map((w) => w.text).join(' ')}" ends ${p.end} > cut ${cut}`);
});

test('F21 on the real orca storyboard (informational: counts pages past a cut)', (t) => {
	const sb = loadSb('explainer-orca');
	if (!sb?.captions?.words) return t.skip('no episodes/explainer-orca/storyboard.json');
	const {timings} = sceneTimings({fps: sb.fps, scenes: sb.scenes.map((s) => ({transitionIn: {type: 'cut'}, ...s}))});
	const cuts = timings.slice(1).map((x) => x.start / sb.fps);
	const pages = paginate(sb.captions.words, {...DEF, ...sb.captions}, cuts);
	const over = pages.filter((p) => cuts.some((c) => p.start < c - 1e-3 && p.end > c + 1e-3));
	t.diagnostic(`orca: ${over.length} of ${pages.length} pages stay up past a cut`);
});

xfail('F20 scene starts follow the cumulative audio time (no rounding drift)', 'F20', () => {
	const fps = 30;
	const scenes = Array.from({length: 30}, () => ({duration: 1.017, transitionIn: {type: 'cut'}}));
	const {timings, totalFrames} = sceneTimings({fps, scenes});
	let cum = 0;
	scenes.forEach((s, i) => {
		assert.ok(Math.abs(timings[i].start - Math.round(cum * fps)) <= 1, `scene ${i} starts at ${timings[i].start}, audio at ${Math.round(cum * fps)}`);
		cum += s.duration;
	});
	assert.ok(Math.abs(totalFrames - Math.round(cum * fps)) <= 1);
});

// SvgMarkup: evaluate the exact replace expression used by layers.tsx
const layers = src('studio/src/core/layers.tsx');
const svgBlock = slice(layers, 'export const SvgMarkup', 'return <div');
const svgExpr = svgBlock.match(/const html = (markup[\s\S]*?);\s*$/m)?.[1];
const svgInject = svgExpr ? new Function('markup', `return ${stripTypeScriptTypes(svgExpr, {mode: 'strip'})};`) : null;

test('SvgMarkup injects sizing into plain markup (regression guard)', () => {
	assert.ok(svgInject, 'could not find the SvgMarkup replace expression');
	assert.match(svgInject('<svg viewBox="0 0 10 10"></svg>'), /width="100%"/);
});

xfail('F17 an author preserveAspectRatio="none" survives (no duplicate attribute)', 'F17', () => {
	const out = svgInject('<svg viewBox="0 0 10 100" preserveAspectRatio="none"><line/></svg>');
	const attrs = out.match(/preserveAspectRatio="[^"]*"/g) ?? [];
	assert.equal(attrs.length, 1, out);
	assert.equal(attrs[0], 'preserveAspectRatio="none"');
});
