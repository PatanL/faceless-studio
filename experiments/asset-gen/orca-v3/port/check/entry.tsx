import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {writeFileSync} from 'node:fs';
import {houseOrcaV3, Orca} from './src/kits/explainer/house/orcaV3Kit';
import {MARINE} from './src/kits/explainer/marine';
import {LightProvider, PlaneTintProvider, resolveLight} from './src/kits/explainer/house/light';
const fig = houseOrcaV3(MARINE.orca);
let k = 0;
const ctx = (p: Record<string, unknown>, extra: object = {}) => ({t: 1.3, p, id: `k${k++}`, idle: true, speed: 1, amp: 1, ...extra});
const cell = (el: React.ReactNode, i: number, box: number[]) => {
	const s = Math.min(700 / box[2], 450 / box[3]);
	return <g key={i} transform={`translate(${(i % 3) * 760 + 30} ${Math.floor(i / 3) * 520 + 40}) scale(${s}) translate(${-box[0]} ${-box[1]})`}>{el}</g>;
};
const cells = [
	cell(fig.draw(ctx({})), 0, fig.box),
	cell(fig.draw(ctx({jaw: 0.8, pec: 15})), 1, fig.box),
	cell(fig.poses!.front.draw(ctx({jaw: 0.6})), 2, fig.poses!.front.box),
	cell(fig.poses!.below.draw(ctx({})), 3, fig.poses!.below.box),
	cell(<LightProvider light={resolveLight({setup: 'cold'} as never)}><PlaneTintProvider tint={{haze: 'tide-1', amount: 0.45, desat: 0.3, depth: 3}}><Orca id="far" t={0.4} /></PlaneTintProvider></LightProvider>, 4, fig.box),
	cell(fig.draw(ctx({}, {sil: '#06141b'})), 5, fig.box),
];
const svg = renderToStaticMarkup(<svg xmlns="http://www.w3.org/2000/svg" width={2300} height={1080} viewBox="0 0 2300 1080"><rect width="2300" height="1080" fill="#008ffd" />{cells}</svg>);
writeFileSync(process.argv[2], svg);
console.log('poses', Object.keys(fig.poses!), 'box', fig.box);
