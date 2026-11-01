import {continueRender, delayRender} from 'remotion';
import '@fontsource/montserrat/700.css';
import '@fontsource/montserrat/800.css';
import '@fontsource/montserrat/900.css';
import '@fontsource/anton/400.css';
import type {Theme} from './schema';

const FALLBACK = ', "Arial Black", "Helvetica Neue", Arial, sans-serif';

/** "display" | "body" | "condensed" | any CSS family -> font-family string. */
export function fontFamily(name: string | undefined, theme: Theme): string {
	switch (name ?? 'display') {
		case 'display':
			return `"${theme.fontDisplay}"${FALLBACK}`;
		case 'body':
			return `"${theme.fontBody}"${FALLBACK}`;
		case 'condensed':
			return `"${theme.fontCondensed}"${FALLBACK}`;
		default:
			return `${name}${FALLBACK}`;
	}
}

let fontsPromise: Promise<unknown> | null = null;

/** Block rendering until the bundled fonts are loaded (once per tab). */
export function waitForFonts() {
	if (fontsPromise || typeof document === 'undefined') return;
	const handle = delayRender('Loading fonts');
	fontsPromise = Promise.all([
		document.fonts.load('900 64px "Montserrat"'),
		document.fonts.load('800 64px "Montserrat"'),
		document.fonts.load('700 64px "Montserrat"'),
		document.fonts.load('400 64px "Anton"'),
	])
		.catch((e) => console.warn('font load failed', e))
		.finally(() => continueRender(handle));
}
