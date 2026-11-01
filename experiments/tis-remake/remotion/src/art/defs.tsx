import React from 'react';
import {rng} from '../lib/anim';

// Palette tokens (SHOTLIST section 0)
export const P = {
	skin: '#F6BE98',
	skinShade: '#E5B08C',
	skinDeep: '#D99A78',
	hand: '#EFC5A8',
	handShade: '#E2AE8E',
	blush: '#F0A090',
	eyeGreen: '#5D8A1E',
	eyeBlue: '#2563B0',
	mouth: '#2B1A15',
	tongue: '#C0392B',
	camoBase: '#6D674A',
	camoA: '#4A482F',
	camoB: '#303025',
	camoC: '#84856F',
	camoD: '#A6B27F',
	carrier: '#4A482F',
	carrierDark: '#3A3926',
	buckle: '#BEBAB7',
	boot: '#1F1D18',
	bootTop: '#3A3933',
	metal: '#2E312C',
	metal2: '#3C3F3C',
	metal3: '#272E32',
	metalHi: '#58574C',
	wood: '#B4532F',
	woodDark: '#8A3A20',
	woodHi: '#C96A42',
	strap: '#303025',
	lens: '#333332',
	lensHi: '#58574C',
	sky: '#D0E5FA',
	cloud: '#F7FBFD',
	cloudShade: '#C7E1F0',
	ruWhite: '#FFFFFF',
	ruBlue: '#0039A6',
	ruRed: '#D52B1E',
	uaBlue: '#0057B7',
	uaYellow: '#FFD700',
};

type Blob = {x: number; y: number; w: number; h: number; c: string; r: number};

function camoBlobs(seed: number, tile: number, colors: string[], n: number): Blob[] {
	// v2: smaller capsules (about 60% of v1's), no H glyphs, a few short vertical "drips" like the
	// reference's pattern, at lower contrast (see the palettes in Defs).
	const R = rng(seed);
	const out: Blob[] = [];
	for (let i = 0; i < n; i++) {
		const c = colors[Math.floor(R() * colors.length)];
		const x = R() * tile;
		const y = R() * tile;
		const kind = R();
		if (kind < 0.18) {
			out.push({x, y, w: 8 + R() * 3, h: 16 + R() * 10, c, r: 0});
		} else {
			const w = 14 + R() * 20;
			const h = 8 + R() * 5;
			out.push({x, y, w, h, c, r: R() < 0.12 ? 90 : 0});
		}
	}
	return out;
}

function CamoPattern({id, tile, base, colors, seed, n}: {id: string; tile: number; base: string; colors: string[]; seed: number; n: number}) {
	const blobs = camoBlobs(seed, tile, colors, n);
	const shapes: React.ReactNode[] = [];
	blobs.forEach((b, i) => {
		for (const ox of [-tile, 0, tile])
			for (const oy of [-tile, 0, tile]) {
				const x = b.x + ox;
				const y = b.y + oy;
				if (x > tile + 40 || y > tile + 40 || x + b.w < -40 || y + b.h < -40) continue;
				shapes.push(
					<rect
						key={`${i}_${ox}_${oy}`}
						x={x}
						y={y}
						width={b.w}
						height={b.h}
						rx={Math.min(b.w, b.h) / 2}
						fill={b.c}
						transform={b.r ? `rotate(${b.r} ${x + b.w / 2} ${y + b.h / 2})` : undefined}
					/>,
				);
			}
	});
	return (
		<pattern id={id} patternUnits="userSpaceOnUse" width={tile} height={tile}>
			<rect width={tile} height={tile} fill={base} />
			{shapes}
		</pattern>
	);
}

/** Shared <defs>: camo fabrics, textures and gradients. Mounted once per SVG. */
export const Defs: React.FC = () => (
	<defs>
		<CamoPattern id="camoRU" tile={200} base={P.camoBase} colors={['#57553B', '#4C4A33', '#7E7E62', '#8E9470', '#7E7E62']} seed={7} n={64} />
		<CamoPattern id="camoRUdk" tile={180} base={'#55523A'} colors={['#4A482F', '#45432D', '#625F47', '#4D4B33']} seed={11} n={46} />
		<CamoPattern id="camoHelm" tile={160} base={'#757052'} colors={['#5F5C40', '#66634A', '#86866A', '#8F9472']} seed={19} n={40} />
		<CamoPattern id="camoUA" tile={200} base={'#A0A06A'} colors={['#83865A', '#B9B184', '#8C7B58', '#787C50', '#B0AC7A']} seed={23} n={64} />
		<CamoPattern id="camoUAdk" tile={180} base={'#7E7F52'} colors={['#6C7046', '#918E62', '#74664A']} seed={29} n={44} />
		<CamoPattern id="camoOff" tile={200} base={'#77714F'} colors={['#615D42', '#686449', '#8A8A6C', '#969B78']} seed={31} n={56} />
		<pattern id="hatch" patternUnits="userSpaceOnUse" width={8.5} height={8.5} patternTransform="rotate(45)">
			<rect width={8.5} height={8.5} fill="rgba(0,0,0,0)" />
			<rect width={2.2} height={8.5} fill="rgba(120,20,0,0.07)" />
		</pattern>
		<radialGradient id="softShadow">
			<stop offset="0" stopColor="rgba(0,0,0,0.30)" />
			<stop offset="0.6" stopColor="rgba(0,0,0,0.16)" />
			<stop offset="1" stopColor="rgba(0,0,0,0)" />
		</radialGradient>
		<radialGradient id="glowOrange">
			<stop offset="0" stopColor="rgba(255,190,80,0.85)" />
			<stop offset="1" stopColor="rgba(255,120,40,0)" />
		</radialGradient>
		<radialGradient id="hookVignette" cx="0.5" cy="0.594" r="0.75">
			<stop offset="0.35" stopColor="rgba(245,70,2,0)" />
			<stop offset="1" stopColor="rgba(240,60,0,0.85)" />
		</radialGradient>
		<radialGradient id="lampGlow">
			<stop offset="0" stopColor="rgba(255,200,90,0.55)" />
			<stop offset="1" stopColor="rgba(255,170,60,0)" />
		</radialGradient>
		<filter id="smearX" x="-20%" y="-5%" width="140%" height="110%">
			<feGaussianBlur stdDeviation="38 0" />
		</filter>
		<filter id="dropSoft" x="-30%" y="-30%" width="160%" height="170%">
			<feDropShadow dx="0" dy="8" stdDeviation="7" floodColor="#000" floodOpacity="0.22" />
		</filter>
	</defs>
);

/** Soft elliptical cast shadow (contact shadow) on the ground. */
export const CastShadow: React.FC<{x: number; y: number; w: number; h?: number; o?: number}> = ({x, y, w, h, o = 1}) => (
	<ellipse cx={x} cy={y} rx={w / 2} ry={(h ?? w * 0.14) / 2} fill="url(#softShadow)" opacity={o} />
);

/** Rounded capsule rect helper. */
export const Cap: React.FC<{x: number; y: number; w: number; h: number; fill: string; o?: number; r?: number}> = ({x, y, w, h, fill, o, r}) => (
	<rect x={x} y={y} width={w} height={h} rx={r ?? Math.min(w, h) / 2} fill={fill} opacity={o} />
);
