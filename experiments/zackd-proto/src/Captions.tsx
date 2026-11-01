// Zack-style captions (VISUAL_GRAMMAR 9): one centred line, vertical centre at 78.3% of H, ~68 px heavy sans,
// pure white with a soft shadow, 2-3 words per card cut at phrase boundaries, locked to the Kokoro word times.
// `highlight` (off by default, as measured in 9/9 references) dims the not-yet-spoken words of the card.
import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, useCurrentFrame, useVideoConfig} from 'remotion';
import '@fontsource/montserrat/800.css';

export type Word = {text: string; start: number; end: number};

// card boundaries as word counts (phrase-level chunking of the 34 words)
const CHUNKS = [3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2];

const clean = (w: string) => w.replace(/[.,!?;:"]/g, '');

export function buildCards(words: Word[]) {
	const cards: {words: Word[]; start: number; end: number}[] = [];
	let i = 0;
	for (const n of CHUNKS) {
		const ws = words.slice(i, i + n);
		i += n;
		if (!ws.length) break;
		cards.push({words: ws, start: ws[0].start, end: ws[ws.length - 1].end});
	}
	// cards change while the voice runs: each card holds until the next starts (or +0.25 s after its last word)
	return cards.map((c, k) => ({...c, end: k + 1 < cards.length ? cards[k + 1].start : c.end + 0.25}));
}

const FONT = '"Montserrat", "Arial Black", sans-serif';
const BASE_PX = 68;

export const Captions: React.FC<{words: Word[]; highlight?: boolean}> = ({words, highlight = false}) => {
	const frame = useCurrentFrame();
	const {fps, width, height} = useVideoConfig();
	const t = frame / fps;
	const [ready] = useState(() => delayRender('caption font'));
	const [measure, setMeasure] = useState<CanvasRenderingContext2D | null>(null);
	useEffect(() => {
		document.fonts
			.load(`800 ${BASE_PX}px "Montserrat"`)
			.then(() => {
				const ctx = document.createElement('canvas').getContext('2d')!;
				setMeasure(ctx);
			})
			.finally(() => continueRender(ready));
	}, [ready]);
	const cards = buildCards(words);
	const card = cards.find((c) => t >= c.start - 0.03 && t < c.end - 0.03);
	if (!card || !measure) return null;
	const text = card.words.map((w) => clean(w.text)).join(' ');
	measure.font = `800 ${BASE_PX}px ${FONT}`;
	const w = measure.measureText(text).width;
	const px = Math.min(BASE_PX, (BASE_PX * width * 0.72) / w); // never wider than 72% of W, never wraps
	const opacity = Math.min(1, (t - card.start + 0.03) / (2 / fps)); // 2-frame fade in
	return (
		<div
			style={{
				position: 'absolute',
				left: 0,
				right: 0,
				top: height * 0.783,
				transform: 'translateY(-50%)',
				textAlign: 'center',
				fontFamily: FONT,
				fontWeight: 800,
				fontSize: px,
				lineHeight: 1,
				color: '#ffffff',
				whiteSpace: 'nowrap',
				textShadow: '0 3px 8px rgba(0,0,0,0.6), 0 0 2px rgba(0,0,0,0.35)',
				opacity,
			}}
		>
			{card.words.map((wd, i) => (
				<span key={i} style={{opacity: highlight && t < wd.start ? 0.55 : 1}}>
					{clean(wd.text)}
					{i < card.words.length - 1 ? ' ' : ''}
				</span>
			))}
		</div>
	);
};
