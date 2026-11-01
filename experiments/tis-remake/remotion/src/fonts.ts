import {continueRender, delayRender, staticFile} from 'remotion';

let done = false;
/** Load the caption face (K2D Medium) and the pill face (Montserrat ExtraBold) once per tab. */
export function loadFonts() {
	if (done || typeof document === 'undefined') return;
	done = true;
	const h = delayRender('fonts');
	const faces = [
		new FontFace('K2D', `url(${staticFile('fonts/K2D-Medium.ttf')})`, {weight: '500'}),
		new FontFace('MontserratXB', `url(${staticFile('fonts/Montserrat-ExtraBold.woff2')})`, {weight: '800'}),
	];
	Promise.all(faces.map((f) => f.load().then((ff) => document.fonts.add(ff))))
		.catch((e) => console.warn('font load failed', e))
		.finally(() => continueRender(h));
}
