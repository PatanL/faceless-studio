import React from 'react';
import {clamp} from './lib/anim';

// Caption pages exactly as the reference shows them (4-line pages, hard swaps ~0.2 s ahead of the voice).
export const PAGES: [number, string[]][] = [
	[2.75, ['Moscow, mired in its war', 'in Ukraine, announced it', 'would be switching from', 'the famed AK-47']],
	[7.2, ['to a more versatile model', 'in 2023, and testing was', 'ongoing on the new model.']],
	[11.5, ['On the surface, this new', 'gun has some great', 'features. With a 16 -', 'inch barrel, it can fire']],
	[15.5, ['700 rounds per minute and', 'has a two-round burst', "function. It's also well"]],
	[19.25, ['suited for accessories,', 'and has a lower recoil.', 'But much like with most']],
	[22.6, ['things for Russia lately,', 'things aren’t turning', 'out like hoped.']],
	[26.1, ['The mode selector on the', 'new rifle was designed', 'in a poor and uncomfortable', 'way, making it far too']],
	[30.5, ['easy to switch between', 'modes. The gun was also', 'proving unreliable, with', 'many guns quickly being']],
	[35.2, ['adapted to disable the', 'two - round burst fire', 'mode. So while the', 'AK - 12 is likely to']],
	[40.0, ['continue being Russia’s', 'weapon of choice, as', 'opposed to the Cold War', '- era AK-47, Russia has']],
	[44.75, ['increasingly been going', 'back to the earlier', 'models of the rifle that', 'don’t include some of']],
	[48.4, ['the newest features.', 'All the while, modern', 'weaponry keeps pouring']],
	[51.75, ['into Ukraine - making', 'Russia’s new rifles look', 'outdated from moment one.']],
];

const Box: React.FC<{lines: string[]; opacity?: number}> = ({lines, opacity = 1}) => (
	<div style={{position: 'absolute', left: 0, right: 0, top: 1500, display: 'flex', justifyContent: 'center', opacity}}>
		<div
			style={{
				transform: 'translateY(-50%)',
				background: 'rgba(0,0,0,0.70)',
				borderRadius: 36,
				padding: "17px 40px 18px",
				fontFamily: 'K2D, sans-serif',
				fontWeight: 500,
				fontSize: 75,
				lineHeight: '100px',
				color: '#FFFFFD',
				textAlign: 'center',
				whiteSpace: 'pre',
				maxWidth: 1040,
			}}
		>
			{lines.join('\n')}
		</div>
	</div>
);

export const Captions: React.FC<{t: number}> = ({t}) => {
	let idx = -1;
	for (let i = 0; i < PAGES.length; i++) if (t >= PAGES[i][0]) idx = i;
	if (idx < 0) return null;
	// 26.0: the only cross-dissolve (2 frames, under the iris)
	if (idx === 6 && t < 26.1 + 2 / 30) {
		const u = clamp((t - 26.1) / (2 / 30));
		return (
			<>
				<Box lines={PAGES[5][1]} opacity={1 - u} />
				<Box lines={PAGES[6][1]} opacity={u} />
			</>
		);
	}
	return <Box lines={PAGES[idx][1]} />;
};
