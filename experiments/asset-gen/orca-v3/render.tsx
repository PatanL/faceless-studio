/**
 * Render OrcaV3 stills to SVG (react-dom/server) and PNG (rsvg-convert): no browser, no Remotion.
 *   orca-v3/render.sh   ->  orca-v3/out/{hero,hero_v3pal,poses,stress,light,closeups,front,below}.svg|png
 *                           + sbs.png / sbs_views.png (ffmpeg side-by-sides with the references)
 */
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {execFileSync} from 'node:child_process';
import {mkdirSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {OrcaV3, PALETTE_A, PALETTE_V3, type OrcaV3Props} from './OrcaV3';

const ROOT = join(__dirname, '..');
const OUT = join(ROOT, 'orca-v3', 'out');
mkdirSync(OUT, {recursive: true});

const save = (name: string, el: React.ReactElement, w: number, h: number, vb: string, water = PALETTE_A.water) => {
	const svg =
		`<?xml version="1.0" encoding="UTF-8"?>\n` +
		renderToStaticMarkup(
			<svg xmlns="http://www.w3.org/2000/svg" width={w} height={h} viewBox={vb}>
				<rect x="-4000" y="-4000" width="12000" height="12000" fill={water} />
				{el}
			</svg>,
		);
	const f = join(OUT, `${name}.svg`);
	writeFileSync(f, svg);
	execFileSync('rsvg-convert', ['-w', String(w), '-h', String(h), f, '-o', join(OUT, `${name}.png`)]);
	console.log(name, (svg.length / 1024).toFixed(0) + ' KB', (svg.match(/<(path|circle|ellipse|rect)/g) || []).length, 'elements');
};

const Label: React.FC<{s: string}> = ({s}) => (
	<text x={40} y={70} fontSize={44} fontFamily="Helvetica" fill="#cfcde6">
		{s}
	</text>
);
const sheet = (name: string, cells: {label: string; p: OrcaV3Props}[], cols = 2) => {
	const rows = Math.ceil(cells.length / cols);
	save(
		name,
		<g>
			{cells.map((q, i) => (
				<g key={i} transform={`translate(${(i % cols) * 1536} ${Math.floor(i / cols) * 1024})`}>
					<OrcaV3 id={`${name}${i}`} blink={0} {...q.p} />
					<Label s={q.label} />
				</g>
			))}
		</g>,
		768 * cols,
		512 * rows,
		`0 0 ${1536 * cols} ${1024 * rows}`,
	);
};

// hero: rest pose, same framing as the reference (for the side-by-side)
save('hero', <OrcaV3 id="hero" t={0} amp={0} blink={0} />, 1536, 1024, '0 0 1536 1024');
// the same rest pose in the v3 reference's navy palette, for a like-for-like check against a_orca_side_v3.png
save('hero_v3pal', <OrcaV3 id="hv3" t={0} amp={0} blink={0} palette={PALETTE_V3} />, 1536, 1024, '0 0 1536 1024', PALETTE_V3.water);
save('front_rest', <OrcaV3 id="fr" view="front" t={0} amp={0} blink={0} palette={PALETTE_V3} />, 1536, 1024, '0 0 1536 1024', PALETTE_V3.water);
save('below_rest', <OrcaV3 id="br" view="below" t={0} amp={0} blink={0} palette={PALETTE_V3} />, 1536, 1024, '0 0 1536 1024', PALETTE_V3.water);

const T = 1 / 0.55; // one tail-beat period
sheet('poses', [
	{label: 'swim t=0', p: {t: 0}},
	{label: 'swim t=0.5 period', p: {t: 0.5 * T}},
	{label: 'swim t=1 period (= t=0)', p: {t: 1 * T}},
	{label: 'swim t=0.25, amp 1.4', p: {t: 0.25 * T, amp: 1.4}},
	{label: 'jaw open', p: {t: 0, amp: 0, jaw: 1}},
	{label: 'flipper +25, blink', p: {t: 0, amp: 0, pec: 25, blink: 1}},
], 2);

// stress: extreme poses for seams (big amp, jaw overshoot, flipper both ways, fin scale)
sheet('stress', [
	{label: 'amp 1.6 t=0.25', p: {t: 0.25 * T, amp: 1.6, jaw: 1.1}},
	{label: 'amp 1.6 t=0.75', p: {t: 0.75 * T, amp: 1.6, pec: -20}},
	{label: 'finScale 1.4, pec +35', p: {t: 0.1 * T, finScale: 1.4, pec: 35}},
	{label: 'far lod', p: {t: 0.3 * T, lod: 'far'}},
	{label: 'silhouette (silColor)', p: {t: 0.3 * T, silColor: '#1b0a6b'}},
	{label: 'cast shadow, look + lid', p: {t: 0.6 * T, cast: {y: 960, lift: 0.4}, look: [1, -0.5], lid: 0.5}},
], 2);

sheet('light', [
	{label: 'key from above (reference)', p: {amp: 0}},
	{label: 'key upper-left (kit lantern)', p: {amp: 0, light: {key: [-0.6, -0.8]}}},
	{label: 'key from the right', p: {amp: 0, light: {key: [0.8, -0.6]}}},
	{label: 'key from below', p: {amp: 0, light: {key: [0, 1]}}},
], 2);

// the two extra views, same parts and rules
sheet('front', [
	{label: 'front rest', p: {view: 'front', amp: 0}},
	{label: 'front swim t=0.5 (bob, fin sway, flippers)', p: {view: 'front', t: 0.5 * T, amp: 1.4}},
	{label: 'front jaw open', p: {view: 'front', amp: 0, jaw: 1}},
	{label: 'front flippers +25, blink', p: {view: 'front', amp: 0, pec: 25, blink: 1}},
], 2);
sheet('below', [
	{label: 'below rest', p: {view: 'below', amp: 0}},
	{label: 'below swim t=0.5 (fluke pitch, tail)', p: {view: 'below', t: 0.5 * T, amp: 1.4}},
	{label: 'below jaw open', p: {view: 'below', amp: 0, jaw: 1}},
	{label: 'below flippers +25, blink', p: {view: 'below', amp: 0, pec: 25, blink: 1}},
], 2);

// close-ups of every joint at extreme poses (seam check): [label, props, viewBox x y w h]
const closeups: [string, OrcaV3Props, [number, number, number, number]][] = [
	['jaw 0.5', {amp: 0, jaw: 0.5}, [1150, 400, 360, 240]],
	['jaw 1.0', {amp: 0, jaw: 1}, [1150, 400, 360, 240]],
	['jaw 1.1, t=0.25 amp 1.6', {t: 0.25 * T, amp: 1.6, jaw: 1.1}, [1150, 400, 360, 240]],
	['fluke root t=0.25 amp 1.6', {t: 0.25 * T, amp: 1.6}, [120, 470, 210, 140]],
	['fluke root t=0.75 amp 1.6', {t: 0.75 * T, amp: 1.6}, [120, 470, 210, 140]],
	['dorsal root, sway max, fin 1.4', {t: (0.25 + 1.3 / (2 * Math.PI)) * T, amp: 1.6, finScale: 1.4}, [640, 140, 400, 267]],
	['flipper root pec +35', {amp: 0, pec: 35}, [900, 520, 360, 240]],
	['flipper root pec -30', {amp: 0, pec: -30}, [900, 520, 360, 240]],
	['eye blink 0.5 / lid', {amp: 0, blink: 0.5}, [1240, 460, 150, 100]],
	['front jaw 1 + flippers -20', {view: 'front', amp: 0, jaw: 1, pec: -20}, [380, 480, 480, 320]],
	['front dorsal root, sway', {view: 'front', t: 0.75 * T, amp: 1.4, finScale: 1.3}, [600, 60, 330, 220]],
	['below jaw 1', {view: 'below', amp: 0, jaw: 1}, [600, 20, 330, 220]],
];
save(
	'closeups',
	<g>
		{closeups.map(([label, p, [x, y, w, h]], i) => (
			<g key={i} transform={`translate(${(i % 3) * 600} ${Math.floor(i / 3) * 400}) scale(${600 / w}) translate(${-x} ${-y})`}>
				<clipPath id={`cuc${i}`}>
					<rect x={x} y={y} width={w} height={h} />
				</clipPath>
				<g clipPath={`url(#cuc${i})`}>
					<rect x={x} y={y} width={w} height={h} fill={PALETTE_A.water} />
					<OrcaV3 id={`cu${i}`} blink={0} {...p} />
				</g>
				<text x={x + 6 * (w / 600)} y={y + 22 * (w / 600)} fontSize={18 * (w / 600)} fontFamily="Helvetica" fill="#cfcde6">
					{label}
				</text>
			</g>
		))}
		<path d="M 600 0 V 1600 M 1200 0 V 1600 M 0 400 H 1800 M 0 800 H 1800 M 0 1200 H 1800" stroke="#000" strokeWidth={3} />
	</g>,
	1800,
	1600,
	'0 0 1800 1600',
);

// side by sides (ffmpeg, no browser)
const G = join(ROOT, 'gen');
const ff = (args: string[]) => execFileSync('ffmpeg', ['-loglevel', 'error', '-y', ...args]);
// row 1: style board A panel 6 (the locked house style) | ours in style A.  row 2: a_orca_side_v3 | ours in its palette
ff(['-i', join(G, 'style_board_A.png'), '-i', join(OUT, 'hero.png'), '-i', join(G, 'a_orca_side_v3.png'), '-i', join(OUT, 'hero_v3pal.png'), '-filter_complex',
	'[0]crop=530:262:1122:318,scale=1536:-2,pad=1536:1024:0:(oh-ih)/2:color=0x008ffd[a];[a][1]hstack[r1];[2][3]hstack[r2];[r1][r2]vstack,scale=1536:-2', join(OUT, 'sbs.png')]);
ff(['-i', join(G, 'a_orca_side_v3.png'), '-i', join(OUT, 'hero_v3pal.png'), '-filter_complex', '[0][1]blend=all_mode=difference,eq=brightness=0.1:contrast=3', join(OUT, 'diff.png')]);
// extra views: Codex reference | ours (reference palette) | ours (style A)
ff(['-i', join(ROOT, 'orca-v3', 'refs', 'orca_v3_front_v1.png'), '-i', join(OUT, 'front_rest.png'), '-i', join(ROOT, 'orca-v3', 'refs', 'orca_v3_below_v1.png'), '-i', join(OUT, 'below_rest.png'), '-filter_complex',
	'[0][1]hstack[r1];[2][3]hstack[r2];[r1][r2]vstack,scale=1536:-2', join(OUT, 'sbs_views.png')]);
console.log('sbs.png, diff.png, sbs_views.png');
