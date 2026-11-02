// Stills for the three-lane compositions (our own code): one browser, many frames.
// node scripts/stills.mjs <bundleDir> <props.json> <outDir> <compositionId> <gl: angle|swangle> frame...
// Run it from experiments/three-lane (it resolves @remotion/renderer from this project). Mac: angle (GPU);
// Spark: swangle (CPU only).
import fs from "fs";
import { createRequire } from "module";
const require = createRequire(new URL("../package.json", import.meta.url).pathname);
const { renderStill, selectComposition, openBrowser } = require("@remotion/renderer");
const [serve, propsPath, outDir, comp, gl, ...raw] = process.argv.slice(2);
const frames = raw.filter((f) => f.trim() !== "").map(Number);
const inputProps = JSON.parse(fs.readFileSync(propsPath, "utf8"));
const chromiumOptions = { gl };
const browser = await openBrowser("chrome", { chromiumOptions, chromeMode: "chrome-for-testing" });
const composition = await selectComposition({ serveUrl: serve, id: comp, inputProps, puppeteerInstance: browser, chromiumOptions });
fs.mkdirSync(outDir, { recursive: true });
for (const f of frames) {
  await renderStill({ composition, serveUrl: serve, frame: f, output: `${outDir}/f${String(f).padStart(5, "0")}.png`, imageFormat: "png",
    inputProps, puppeteerInstance: browser, chromiumOptions, timeoutInMilliseconds: 120000, chromeMode: "chrome-for-testing" });
}
await browser.close({ silent: true });
console.log("stills", frames.length);
