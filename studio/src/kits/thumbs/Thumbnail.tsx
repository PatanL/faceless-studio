// One still = one spec. Dispatches to the niche template and waits for fonts so text
// measurement (and therefore the headline fit) is exact.
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, useVideoConfig} from 'remotion';
import '../index'; // other kits register their art; specs can reference it via art/humanArt
import {FxDefs} from './fx';
import {fontsReady} from './measure';
import type {ThumbSpec} from './spec';
import {AbyssTemplate, EyeTemplate, ScaleTemplate, type TplProps} from './templates/explainer';
import {ChatTemplate, DoorTemplate, HallwayTemplate} from './templates/horror';

const TPL: Record<string, React.FC<TplProps>> = {
	'explainer/eye': EyeTemplate,
	'explainer/scale': ScaleTemplate,
	'explainer/abyss': AbyssTemplate,
	'horror/door': DoorTemplate,
	'horror/chat': ChatTemplate,
	'horror/hallway': HallwayTemplate,
};

export const Thumbnail: React.FC<ThumbSpec> = (spec) => {
	const {width: W, height: H} = useVideoConfig();
	const [ready, setReady] = useState(false);
	const [handle] = useState(() => delayRender('thumbnail layout'));
	useEffect(() => {
		fontsReady().then(() => setReady(true));
	}, []);
	useEffect(() => {
		// release only after the measured layout has been committed
		if (ready) continueRender(handle);
	}, [ready, handle]);
	const T = TPL[`${spec.niche}/${spec.template}`];
	if (!ready) return <AbsoluteFill style={{background: '#000'}} />;
	if (!T)
		return (
			<AbsoluteFill style={{background: '#300', color: '#fff', fontSize: 48, alignItems: 'center', justifyContent: 'center'}}>
				unknown template {spec.niche}/{spec.template}
			</AbsoluteFill>
		);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} xmlns="http://www.w3.org/2000/svg" style={{display: 'block'}}>
				<FxDefs id="fx" />
				<T spec={spec} W={W} H={H} fx="fx" />
			</svg>
		</AbsoluteFill>
	);
};
