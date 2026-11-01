#!/usr/bin/env node
// Storyboard stills for quick look-dev. Run ON THE SPARK (CPU only) from studio/:
//
//   node src/cli/stills.mjs <storyboard.json> --at 0.5,2,4.5 [--out out/stills/<id>] [--format 16:9]
//
// Bundles once, opens one browser and renders each requested second as a JPEG
// (<out>/<id>_<t>s.jpg). Much cheaper than an MP4 render, so it skips the render lock
// (like the thumbs CLI) and should be run with `nice -n 10`. --format overrides the
// storyboard's own format (layout is NOT adapted; use pipeline.episodes.reformat for that).
// From the Mac use scripts/spark_stills.sh, which syncs, renders here, tiles a sheet and pulls it back.
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

process.env.CUDA_VISIBLE_DEVICES = '';
const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (name, d) => {
	const i = args.indexOf(name);
	if (i < 0) return d;
	const v = args[i + 1];
	args.splice(i, 2);
	return v;
};
const at = opt('--at', '0.5').split(',').map(Number);
const fmt = opt('--format', '');
const sbPath = args[0];
if (!sbPath) {
	console.error('usage: stills.mjs <storyboard.json> --at 0.5,2 [--out dir] [--format 16:9]');
	process.exit(2);
}
const sb = JSON.parse(fs.readFileSync(sbPath, 'utf8'));
if (fmt) sb.format = fmt;
const outDir = path.resolve(opt('--out', `out/stills/${sb.id ?? 'sb'}`));
fs.mkdirSync(outDir, {recursive: true});

const serveUrl = await bundle({entryPoint: path.join(here, '..', 'index.ts'), publicDir: path.resolve(here, '../../public')});
const browser = await openBrowser('chrome', {chromiumOptions: {gl: 'swangle'}});
try {
	const composition = await selectComposition({serveUrl, id: 'Storyboard', inputProps: sb, puppeteerInstance: browser});
	for (const t of at) {
		const frame = Math.min(composition.durationInFrames - 1, Math.max(0, Math.round(t * composition.fps)));
		const output = path.join(outDir, `${sb.id ?? 'sb'}_${t.toFixed(2).padStart(6, '0')}s.jpg`);
		await renderStill({serveUrl, composition, inputProps: sb, frame, output, imageFormat: 'jpeg', jpegQuality: 85, puppeteerInstance: browser, overwrite: true});
		console.log(`[stills] ${path.basename(output)} frame ${frame}`);
	}
} finally {
	await browser.close({silent: true});
}
