/**
 * Render Path B stills to SVG (react-dom/server), then PNG with rsvg-convert (no browser, no Remotion).
 *   npm run render-b   ->  orca-b/out/{hero,poses,light}.svg|png
 */
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {execFileSync} from 'node:child_process';
import {mkdirSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {OrcaB, LANTERN, markCount, type Light} from './OrcaB';
import {c, mixOk} from '../../kurz-style/engine/src/lib/color';

const OUT = join(__dirname, '..', 'orca-b', 'out');
mkdirSync(OUT, {recursive: true});
const BG = mixOk(c('ink-3'), c('tide-0'), 0.35);

const save = (name: string, el: React.ReactElement, w: number, h: number, vb: string) => {
	const svg = `<?xml version="1.0" encoding="UTF-8"?>\n` + renderToStaticMarkup(
		<svg xmlns="http://www.w3.org/2000/svg" width={w} height={h} viewBox={vb}>
			<rect x="-4000" y="-4000" width="10000" height="10000" fill={BG} />
			{el}
		</svg>,
	);
	const f = join(OUT, `${name}.svg`);
	writeFileSync(f, svg);
	execFileSync('rsvg-convert', ['-w', String(w), '-h', String(h), f, '-o', join(OUT, `${name}.png`)]);
	console.log(name, (svg.length / 1024).toFixed(0) + ' KB', (svg.match(/<(path|circle|ellipse|rect)/g) || []).length, 'elements');
};

save('hero', <OrcaB t={0.35} />, 1536, 1024, '0 0 1536 1024');

// pose sheet: same component, only props change (proves the parts are separately animatable)
const poses: {label: string; p: React.ComponentProps<typeof OrcaB>}[] = [
	{label: 'swim t=0.0', p: {t: 0}},
	{label: 'swim t=1.0', p: {t: 1.0, amp: 34}},
	{label: 'jaw open', p: {t: 0.35, jaw: 1}},
	{label: 'flipper +25, blink', p: {t: 0.35, pec: 25, blink: 1}},
];
save(
	'poses',
	<g>
		{poses.map((q, i) => (
			<g key={i} transform={`translate(${(i % 2) * 1536} ${Math.floor(i / 2) * 1024})`}>
				<OrcaB id={`p${i}`} {...q.p} />
				<text x={40} y={70} fontSize={44} fontFamily="Helvetica" fill={c('bone-2')}>{q.label}</text>
			</g>
		))}
	</g>,
	1536,
	1024,
	'0 0 3072 2048',
);

// relight: the light vector moves, every part re-shades (nothing redrawn)
const lights: [string, Light][] = [
	['key upper-left (default)', LANTERN],
	['key from above-right', {...LANTERN, key: [0.5, -0.86], rim: [-0.6, 0.8]}],
];
save(
	'light',
	<g>
		{lights.map(([label, L], i) => (
			<g key={i} transform={`translate(${i * 1536} 0)`}>
				<OrcaB id={`l${i}`} t={0.35} light={L} />
				<text x={40} y={70} fontSize={44} fontFamily="Helvetica" fill={c('bone-2')}>{label}</text>
			</g>
		))}
	</g>,
	1536,
	512,
	'0 0 3072 1024',
);
console.log('marks from reference:', markCount());
