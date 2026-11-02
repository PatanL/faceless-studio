// node sperm-a/build.js  -> sperm-a/out/sheet.png (look-dev of the kit sperm whale, Mac-light)
const path = require('path');
const nm = path.resolve('node_modules');
require('esbuild').build({entryPoints: ['sperm-a/render.tsx'], bundle: true, platform: 'node', format: 'cjs',
  outfile: 'build/render_sw.cjs', logLevel: 'warning', nodePaths: [nm], jsx: 'automatic',
  plugins: [{name: 'stub', setup(b) {
    b.onResolve({filter: /^\.\/light$|^\.\/motion$|^\.\.\/util$|^\.\.\/figure$/}, () => ({path: path.resolve('sperm-a/stub.tsx')}));
    b.onResolve({filter: /^react(\/.*)?$|^react-dom(\/.*)?$/}, (a) => ({path: require.resolve(a.path, {paths: [nm]})}));
  }}]}).then(() => console.log('built'));
