// Real text measurement once the bundled fonts are loaded (falls back to the em table).
import {continueRender, delayRender} from 'remotion';
import '@fontsource/montserrat/900.css';

let ctx: CanvasRenderingContext2D | null = null;
let ready = false;
let promise: Promise<void> | null = null;

export function fontsReady(): Promise<void> {
	if (promise) return promise;
	if (typeof document === 'undefined') return Promise.resolve();
	const h = delayRender('thumb fonts');
	promise = document.fonts
		.load('900 100px "Montserrat"')
		.then(() => document.fonts.ready)
		.then(() => {
			const c = document.createElement('canvas');
			ctx = c.getContext('2d');
			if (ctx) ctx.font = '900 100px "Montserrat"';
			ready = true;
		})
		.catch((e) => console.warn('thumb font load failed', e))
		.finally(() => continueRender(h));
	return promise;
}

/** Width in em of `s` set in Montserrat 900, or null before fonts are ready. */
export function measureEm(s: string): number | null {
	if (!ready || !ctx) return null;
	return ctx.measureText(s).width / 100;
}
