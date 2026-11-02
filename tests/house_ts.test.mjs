// House-style motion guards (studio/src/core/anim.ts), no node_modules: the pure functions are sliced out of the
// source, type-stripped and evaluated with a stand-in for remotion's spring() (a damped spring with the same config).
// Run: node --test tests/
import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {stripTypeScriptTypes} from 'node:module';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const anim = fs.readFileSync(path.join(ROOT, 'studio/src/core/anim.ts'), 'utf8');

// damped harmonic oscillator from rest at 0 to 1 (remotion spring semantics: mass, stiffness, damping)
function spring({frame, fps, config}) {
	const {mass, stiffness, damping} = config;
	const t = Math.max(0, frame / fps);
	const w0 = Math.sqrt(stiffness / mass);
	const zeta = damping / (2 * Math.sqrt(stiffness * mass));
	if (zeta >= 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
	const wd = w0 * Math.sqrt(1 - zeta * zeta);
	return 1 - Math.exp(-zeta * w0 * t) * (Math.cos(wd * t) + ((zeta * w0) / wd) * Math.sin(wd * t));
}

const a = anim.indexOf('// house-style springs');
const b = anim.indexOf('/** p = 0 means hidden');
assert.ok(a > 0 && b > a, 'house motion block not found in anim.ts');
const js = stripTypeScriptTypes(anim.slice(a, b).replace(/^export /gm, ''), {mode: 'strip'});
const {popSpringScale, dropSquashAt, POP_MIN_WIDTH} = new Function('spring', `${js}\n;return {popSpringScale, dropSquashAt, POP_MIN_WIDTH};`)(spring);

test('YOU pop: never thinner than 60 % of rest width, settles at 1, overshoots like a pop', () => {
	assert.equal(POP_MIN_WIDTH, 0.6);
	let peak = 0;
	for (let f = 0; f <= 60; f++) {
		const s = popSpringScale(f / 30);
		assert.ok(s >= 0.6 - 1e-9, `frame ${f}: scale ${s} < 0.6`);
		peak = Math.max(peak, s);
	}
	assert.ok(Math.abs(popSpringScale(2) - 1) < 0.01, 'settles at 1');
	assert.ok(peak > 1.05 && peak < 1.3, `overshoot ${peak}`);
});

test('popSpring scales both axes together (anim.ts uses one value for sx and sy)', () => {
	const block = anim.slice(anim.indexOf("case 'popSpring'"), anim.indexOf("case 'dropSquash'"));
	assert.match(block, /sx: k, sy: k/);
});

test('dropSquash: falls from above, lands, squashes with volume kept, settles flat', () => {
	const fall = 0.22;
	assert.ok(dropSquashAt(0, 90, fall).dy <= -89);
	assert.equal(dropSquashAt(fall + 0.001, 90, fall).dy, 0);
	const land = dropSquashAt(fall + 0.02, 90, fall);
	assert.ok(land.sy < 0.95, `squash on landing ${land.sy}`);
	assert.ok(Math.abs(land.sx * Math.sqrt(land.sy) - 1) < 1e-9, 'volume-keeping: sx = 1/sqrt(sy)');
	const end = dropSquashAt(2, 90, fall);
	assert.ok(Math.abs(end.sy - 1) < 0.01 && Math.abs(end.sx - 1) < 0.01, 'settles at rest');
});
