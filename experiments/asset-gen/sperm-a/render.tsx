// look-dev harness for studio/src/kits/explainer/house/spermWhaleA.tsx (Mac, light): out/*.png
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {writeFileSync} from 'fs';
import {SpermWhaleA, SW_BOX} from '../../../studio/src/kits/explainer/house/spermWhaleA';
const [bx, by, bw, bh] = SW_BOX;
const cell = (bg: string, props: any, i: number) => (
	<g transform={`translate(0 ${i * 560})`} key={i}>
		<rect width={1800} height={560} fill={bg} />
		<g transform={`translate(${(1800 - bw) / 2 - bx} ${280 - by - bh / 2})`}>
			<SpermWhaleA id={`w${i}`} {...props} />
		</g>
	</g>
);
const rows: [string, any][] = [
	['#0024fd', {t: 0}],
	['#01aefd', {t: 0.6}],
	['#250192', {t: 1.2, jaw: 1}],
	['#3a1fa8', {t: 0.3, organ: 1, click: 1}],
];
const svg = renderToStaticMarkup(
	<svg xmlns="http://www.w3.org/2000/svg" width={1800} height={560 * rows.length}>
		{rows.map(([bg, p], i) => cell(bg, p, i))}
	</svg>,
);
writeFileSync(process.argv[2] || 'sperm-a/out/sheet.svg', svg);
