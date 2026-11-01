// Representative explainer-style load: depth gradient, light rays, 80 particles,
// a swimming SVG creature with camera zoom, scale bar, stat callout and word captions.
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const rand = (i: number) => {
  const x = Math.sin(i * 9301 + 49297) * 233280;
  return x - Math.floor(x);
};

const WORDS = 'A colossal squid has the largest eyes of any animal on Earth each one as wide as a dinner plate and it hunts in total darkness two thousand meters below you'.split(' ');

export const Bench: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const t = frame / fps;
  const depth = interpolate(frame, [0, durationInFrames], [200, 2000]);
  const zoom = interpolate(Math.sin(t * 0.4), [-1, 1], [1, 1.15]);
  const top = interpolate(depth, [0, 2000], [40, 5]);
  const callout = spring({frame: frame - 90, fps, config: {damping: 12}});
  const wordIdx = Math.floor(t * 2.4) % WORDS.length;
  const capWords = WORDS.slice(Math.max(0, wordIdx - 2), wordIdx + 1);

  return (
    <AbsoluteFill style={{background: `linear-gradient(180deg, hsl(190,70%,${top}%) 0%, hsl(205,80%,4%) 100%)`, overflow: 'hidden', fontFamily: 'sans-serif'}}>
      <AbsoluteFill style={{transform: `scale(${zoom})`}}>
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
          <defs>
            <linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor="#bff" stopOpacity="0.35" />
              <stop offset="1" stopColor="#bff" stopOpacity="0" />
            </linearGradient>
            <radialGradient id="glow"><stop offset="0" stopColor="#9ff" stopOpacity="0.9" /><stop offset="1" stopColor="#9ff" stopOpacity="0" /></radialGradient>
          </defs>
          {new Array(7).fill(0).map((_, i) => {
            const x = (i / 7) * width + Math.sin(t * 0.7 + i) * 60;
            return <polygon key={i} points={`${x},0 ${x + 120},0 ${x + 380},${height * 0.8} ${x - 140},${height * 0.8}`} fill="url(#ray)" opacity={0.5 + 0.5 * Math.sin(t + i * 1.3)} />;
          })}
          {new Array(80).fill(0).map((_, i) => {
            const x = rand(i) * width + Math.sin(t * 0.8 + i) * 20;
            const y = ((rand(i + 100) * height - t * (30 + rand(i + 200) * 60)) % height + height) % height;
            const r = 2 + rand(i + 300) * 6;
            return <circle key={i} cx={x} cy={y} r={r} fill="url(#glow)" />;
          })}
          <g transform={`translate(${width / 2 + Math.sin(t * 0.5) * 200}, ${height * 0.45 + Math.cos(t * 0.7) * 80}) rotate(${Math.sin(t) * 8})`}>
            <ellipse cx={0} cy={0} rx={260} ry={110} fill="#c2453a" />
            <circle cx={-120} cy={-20} r={42} fill="#fff" /><circle cx={-120} cy={-20} r={22} fill="#111" />
            {new Array(8).fill(0).map((_, k) => (
              <path key={k} d={`M 220 ${-60 + k * 17} q ${120 + k * 10} ${Math.sin(t * 3 + k) * 80} ${300} ${Math.cos(t * 2 + k) * 60}`} stroke="#a8362d" strokeWidth={16 - k} fill="none" strokeLinecap="round" />
            ))}
          </g>
          <g transform={`translate(80, ${height - 520})`}>
            <rect width={width - 160} height={16} rx={8} fill="#ffffff33" />
            <rect width={(width - 160) * interpolate(frame, [0, 300], [0, 1], {extrapolateRight: 'clamp'})} height={16} rx={8} fill="#ffd34d" />
            <text x={0} y={-20} fill="#fff" fontSize={40}>14 m — longer than a city bus</text>
          </g>
        </svg>
      </AbsoluteFill>
      <div style={{position: 'absolute', top: 120, left: 60, color: '#fff', fontSize: 64, fontWeight: 800, transform: `scale(${callout})`, transformOrigin: 'left top'}}>
        DEPTH {Math.round(depth)} m
      </div>
      <div style={{position: 'absolute', bottom: 260, width: '100%', textAlign: 'center', color: '#fff', fontSize: 84, fontWeight: 900, textShadow: '0 6px 0 #000, 0 0 20px #000'}}>
        {capWords.map((w, i) => (
          <span key={i} style={{color: i === capWords.length - 1 ? '#ffd34d' : '#fff', margin: '0 12px'}}>{w.toUpperCase()}</span>
        ))}
      </div>
    </AbsoluteFill>
  );
};
