// Horror chat-story kit. Every component is registered as "horror/<Name>".
// See README.md in this folder for props and storyboards/horror-showcase.json for a full example.
import {registerComponent} from '../../core/registry';
import {Bedroom, ElevatorPanel, FrontDoor, Hallway, LivingRoom, Peephole, Stairwell} from './backgrounds';
import {Neighbour, Protagonist} from './characters';
import {FeaturePhone} from './FeaturePhone';
import {EndCard} from './EndCard';
import {Darkness, Flicker, GlitchOverlay, Heartbeat, RedText, VignetteFx, withGlitch} from './fx';
import {HandPhone} from './HandPhone';
import {LightSwitch, TopFade} from './LightSwitch';
import {Phone} from './Phone';

// devices
registerComponent('horror/Phone', Phone);
registerComponent('horror/HandPhone', HandPhone);
registerComponent('horror/FeaturePhone', FeaturePhone);
// characters
registerComponent('horror/Protagonist', Protagonist);
registerComponent('horror/Neighbour', Neighbour);
registerComponent('horror/Stranger', Neighbour); // alias
// backgrounds
registerComponent('horror/FrontDoor', withGlitch(FrontDoor, 'door'));
registerComponent('horror/Peephole', withGlitch(Peephole, 'peep'));
registerComponent('horror/Hallway', Hallway);
registerComponent('horror/ElevatorPanel', withGlitch(ElevatorPanel, 'elev'));
registerComponent('horror/Bedroom', withGlitch(Bedroom, 'bed'));
registerComponent('horror/LivingRoom', withGlitch(LivingRoom, 'living'));
registerComponent('horror/Stairwell', withGlitch(Stairwell, 'stair'));
// effects (full-frame overlays: depth 0, high z)
registerComponent('horror/Flicker', Flicker);
registerComponent('horror/Vignette', VignetteFx);
registerComponent('horror/Heartbeat', Heartbeat);
registerComponent('horror/Glitch', GlitchOverlay);
registerComponent('horror/RedText', RedText);
registerComponent('horror/Darkness', Darkness);
registerComponent('horror/EndCard', EndCard);
registerComponent('horror/TopFade', TopFade);
// inserts
registerComponent('horror/LightSwitch', LightSwitch);
