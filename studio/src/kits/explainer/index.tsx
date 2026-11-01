/**
 * Explainer kit ("you vs. X" ocean/animal style). Registers:
 *
 * backgrounds   explainer/Ocean            depth-lit ocean, rays, marine snow, optional surface
 * figures       explainer/Creature         any figure by `species` (+ fixed-name wrappers below)
 *               explainer/SpermWhale ColossalSquid Orca GreatWhite BlueWhale Anglerfish Octopus
 *               explainer/Crocodile Hippo Grizzly Diver You Bus Car Elephant
 *               explainer/GolfCart WhaleHeart WhaleTongue WhaleThroat Sauropod Jet Krill (anatomy.tsx)
 *               explainer/Seal Liver Sailboat, Orca pose "top" | "head" (orca_kit.tsx)
 * infographics  explainer/DepthMeter ScaleBar HeightChart Stat Map Timer Options SpeedBars Headline Tag
 *               explainer/Balance ECG (balance.tsx)
 *
 * See README.md in this folder for props.
 */
import {registerComponent} from '../../core/registry';
import {Creature, fixed} from './creature';
import {DepthMeter, Ocean} from './ocean';
import {Headline, HeightChart, MapView, Options, ScaleBar, SpeedBars, Stat, Tag, Timer} from './ui';
import {Balance, ECG} from './balance';
import {Sailboat} from './orca_kit';

registerComponent('explainer/Ocean', Ocean);
registerComponent('explainer/DepthMeter', DepthMeter);
registerComponent('explainer/Creature', Creature);

const FIXED: Record<string, string> = {
	SpermWhale: 'spermWhale',
	ColossalSquid: 'colossalSquid',
	Orca: 'orca',
	GreatWhite: 'greatWhite',
	BlueWhale: 'blueWhale',
	Anglerfish: 'anglerfish',
	Octopus: 'octopus',
	Crocodile: 'crocodile',
	Hippo: 'hippo',
	Grizzly: 'grizzly',
	Diver: 'diver',
	You: 'you',
	Bus: 'bus',
	Car: 'car',
	Elephant: 'elephant',
	GolfCart: 'golfCart',
	WhaleHeart: 'whaleHeart',
	WhaleTongue: 'whaleTongue',
	WhaleThroat: 'whaleThroat',
	Sauropod: 'sauropod',
	Jet: 'jet',
	Krill: 'krill',
	Seal: 'seal',
	Liver: 'liver',
};
for (const [name, species] of Object.entries(FIXED)) registerComponent(`explainer/${name}`, fixed(species));

registerComponent('explainer/ScaleBar', ScaleBar);
registerComponent('explainer/HeightChart', HeightChart);
registerComponent('explainer/Stat', Stat);
registerComponent('explainer/Map', MapView);
registerComponent('explainer/Timer', Timer);
registerComponent('explainer/Options', Options);
registerComponent('explainer/SpeedBars', SpeedBars);
registerComponent('explainer/Headline', Headline);
registerComponent('explainer/Tag', Tag);
registerComponent('explainer/Balance', Balance);
registerComponent('explainer/ECG', ECG);
registerComponent('explainer/Sailboat', Sailboat);
