/**
 * Stick kit (story lane: RicksClips / Zack D.-type "clever trick from history" Shorts) in house style A colours.
 * Registers stick/Person (round-head characters), stick/Turk (the chess automaton + cabinet + cutaway),
 * stick/Chess (board close-up), stick/Set (flat backgrounds), stick/Paper (newspaper prop).
 * Our own designs; built only as far as episodes/story-chess-turk needs.
 */
import {registerComponent} from '../../../core/registry';
import {Person} from './person';
import {Turk} from './turk';
import {Chess} from './chess';
import {StickSet} from './sets';
import {Paper} from './paper';

registerComponent('stick/Person', Person);
registerComponent('stick/Turk', Turk);
registerComponent('stick/Chess', Chess);
registerComponent('stick/Set', StickSet);
registerComponent('stick/Paper', Paper);
