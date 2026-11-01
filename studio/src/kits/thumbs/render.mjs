#!/usr/bin/env node
// Thumbnail CLI. Run ON THE SPARK (CPU only) from studio/:
//
//   node src/kits/thumbs/render.mjs <spec.json>... [--out out/thumbs] [--formats 16:9,9:16] [--png] [--sheet]
//
// A spec file holds one ThumbSpec, an array of them, or a per-video object with `variants`
// (each variant is merged over the base, e.g. 3 templates for one episode). A spec with no
// `template` expands to every template of its niche. Output per still:
//   <out>/<id>_<niche>-<template>_<16x9|9x16>.jpg  (JPEG q90, under YouTube's 2 MB cap; --png for lossless)
//        (+ <out>/sheet_16x9.jpg / sheet_9x16.jpg with --sheet)
// From the Mac use scripts/thumbs_render.sh, which syncs, renders here and pulls the PNGs back.
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

process.env.CUDA_VISIBLE_DEVICES = '';
const here = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATES = {explainer: ['eye', 'scale', 'abyss'], horror: ['door', 'chat', 'hallway']};

const args = process.argv.slice(2);
const opt = (name, d) => {
	const i = args.indexOf(name);
	if (i < 0) return d;
	const v = args[i + 1];
	args.splice(i, 2);
	return v;
};
const flag = (name) => {
	const i = args.indexOf(name);
	if (i < 0) return false;
	args.splice(i, 1);
	return true;
};
const outDir = path.resolve(opt('--out', 'out/thumbs'));
const formats = opt('--formats', '16:9,9:16').split(',');
const sheet = flag('--sheet');
const png = flag('--png');
const ext = png ? 'png' : 'jpg';
if (!args.length) {
	console.error('usage: render.mjs <spec.json>... [--out dir] [--formats 16:9,9:16] [--sheet]');
	process.exit(2);
}

const specs = [];
for (const f of args) {
	const raw = JSON.parse(fs.readFileSync(f, 'utf8'));
	for (const base of Array.isArray(raw) ? raw : [raw]) {
		const {variants, ...rest} = base;
		const list = variants?.length ? variants.map((v) => ({...rest, ...v})) : rest.template ? [rest] : TEMPLATES[rest.niche].map((t) => ({...rest, template: t}));
		specs.push(...list);
	}
}
for (const s of specs) {
	const n = s.text.trim().split(/\s+/).length;
	if (n < 2 || n > 4) console.warn(`[thumbs] warning: "${s.text}" has ${n} words (formula wants 2-4)`);
	if (!TEMPLATES[s.niche]?.includes(s.template)) throw new Error(`unknown template ${s.niche}/${s.template}`);
}

fs.mkdirSync(outDir, {recursive: true});
const t0 = Date.now();
const serveUrl = await bundle({entryPoint: path.join(here, 'entry.ts'), publicDir: path.resolve(here, '../../../public')});
const browser = await openBrowser('chrome', {chromiumOptions: {gl: 'swangle'}});
const made = [];
try {
	for (const s of specs) {
		for (const format of formats) {
			const inputProps = {...s, format};
			const composition = await selectComposition({serveUrl, id: 'Thumb', inputProps, puppeteerInstance: browser});
			const name = `${s.id ?? 'thumb'}_${s.niche}-${s.template}_${format.replace(':', 'x')}.${ext}`;
			const output = path.join(outDir, name);
			await renderStill({serveUrl, composition, inputProps, output, imageFormat: png ? 'png' : 'jpeg', jpegQuality: 90, puppeteerInstance: browser, overwrite: true});
			made.push({output, format});
			const kb = Math.round(fs.statSync(output).size / 1024);
			console.log(`[thumbs] ${name} ${composition.width}x${composition.height} ${kb} KB${kb > 2000 ? '  (over 2 MB: YouTube will reject)' : ''}`);
		}
	}
} finally {
	await browser.close({silent: true});
}
console.log(`[thumbs] ${made.length} stills in ${((Date.now() - t0) / 1000).toFixed(1)} s -> ${outDir}`);

if (sheet) {
	// contact sheet per format with ffmpeg (tile), small JPG for review
	const ff = fs.existsSync(`${process.env.HOME}/studio/bin/ffmpeg`) ? `${process.env.HOME}/studio/bin/ffmpeg` : 'ffmpeg';
	for (const format of formats) {
		const files = made.filter((m) => m.format === format).map((m) => m.output);
		if (!files.length) continue;
		const cols = format === '16:9' ? Math.min(3, files.length) : Math.min(6, files.length);
		const rows = Math.ceil(files.length / cols);
		const w = format === '16:9' ? 640 : 360;
		const h = format === '16:9' ? 360 : 640;
		const inputs = files.flatMap((f) => ['-i', f]);
		const scaled = files.map((_, i) => `[${i}:v]scale=${w}:${h}[s${i}]`).join(';');
		const layout = files.map((_, i) => `${(i % cols) * w}_${Math.floor(i / cols) * h}`).join('|');
		const filter = `${scaled};${files.map((_, i) => `[s${i}]`).join('')}xstack=inputs=${files.length}:layout=${layout}:fill=black`;
		const out = path.join(outDir, `sheet_${format.replace(':', 'x')}.jpg`);
		const fc = files.length === 1 ? `[0:v]scale=${w}:${h}` : filter;
		execFileSync(ff, ['-y', '-loglevel', 'error', ...inputs, '-filter_complex', fc, '-frames:v', '1', '-q:v', '3', out]);
		console.log(`[thumbs] sheet ${out} (${cols}x${rows})`);
	}
}
