// Render a list of frames of TisRemake as half-size JPEGs + a contact sheet (run on the Spark from remotion/).
// usage: node tools/stills.mjs <outdir> <frame> [frame...]
import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition, openBrowser} from '@remotion/renderer';
const [outDir, ...fr] = process.argv.slice(2);
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public')});
const browser = await openBrowser('chrome', {chromiumOptions: {gl: 'swangle'}});
const composition = await selectComposition({serveUrl, id: 'TisRemake', puppeteerInstance: browser});
let i = 0;
for (const f of fr.map(Number)) {
  const out = path.join(outDir, `s_${String(i++).padStart(3, '0')}.jpeg`);
  await renderStill({serveUrl, composition, frame: f, output: out, imageFormat: 'jpeg', jpegQuality: 85, scale: 0.5, puppeteerInstance: browser});
  console.log('frame', f, '->', out);
}
await browser.close({silent: true});
