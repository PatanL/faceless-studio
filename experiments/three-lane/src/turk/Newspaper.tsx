// The 1854 newspaper that tells the secret (our own drawing), drawn in the DOM at full resolution so it reads on a
// phone: masthead, dateline, a two-line headline, a subhead in real words and a cutaway sketch of the cabinet with the
// man folded inside. It drops in with a small settle and sits in the upper two-thirds, clear of the captions.
import React from "react";

const ink = "#1b1240", paper = "#f3e6c4", paper2 = "#e6d3a6", red = "#b8332a";
const font = '"Anton", "Arial Narrow", sans-serif';

export const Newspaper: React.FC<{ t: number }> = ({ t }) => {
  const k = Math.min(1, Math.max(0, t / 0.45));
  const e = 1 - Math.pow(1 - k, 3);
  const settle = Math.sin(Math.min(1, t / 0.7) * Math.PI) * (1 - e) * 4;
  return (
    <div style={{ position: "absolute", left: 120, top: 190, width: 840, height: 1060,
      transform: `translateY(${(1 - e) * -1300}px) rotate(${-2.5 + (1 - e) * 12 + settle}deg)`, transformOrigin: "50% 50%" }}>
      <div style={{ position: "absolute", left: 18, top: 22, width: 840, height: 1060, background: "rgba(10, 6, 30, 0.45)" }} />
      <div style={{ position: "absolute", inset: 0, background: paper, padding: "34px 44px", boxSizing: "border-box", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ fontFamily: font, fontSize: 76, color: ink, letterSpacing: 4, lineHeight: 1 }}>THE CHESS MONTHLY</div>
        <div style={{ width: "100%", height: 7, background: ink, marginTop: 14 }} />
        <div style={{ width: "100%", display: "flex", justifyContent: "space-between", fontFamily: font, fontSize: 30, color: ink, marginTop: 8, letterSpacing: 2 }}>
          <span>NEW YORK</span><span>1857</span><span>ONE CENT</span>
        </div>
        <div style={{ width: "100%", height: 3, background: ink, marginTop: 6 }} />
        <div style={{ fontFamily: font, fontSize: 132, color: red, lineHeight: 1.0, marginTop: 26, textAlign: "center", letterSpacing: 2 }}>THE TURK'S<br />SECRET</div>
        <div style={{ fontFamily: font, fontSize: 50, color: ink, marginTop: 18, letterSpacing: 2 }}>THE AUTOMATON EXPOSED</div>
        <div style={{ display: "flex", width: "100%", marginTop: 28, gap: 30 }}>
          <svg viewBox="0 0 330 330" width={330} height={330} style={{ background: paper2, flex: "none" }}>
            {/* cutaway: the cabinet, the false gears on the left, the man folded on his sliding seat with a candle */}
            <rect x={30} y={170} width={270} height={130} fill="#c98a3e" stroke={ink} strokeWidth={6} />
            <rect x={44} y={182} width={110} height={106} fill="#7d5126" />
            {[0, 1, 2].map((i) => <circle key={i} cx={74 + (i % 2) * 44} cy={206 + i * 30} r={18} fill="none" stroke="#e0b04a" strokeWidth={7} strokeDasharray="7 5" />)}
            <rect x={162} y={182} width={126} height={106} fill={ink} />
            <circle cx={204} cy={214} r={17} fill="#f4eee1" />
            <path d="M 192 232 Q 214 270 256 262" stroke="#6f86c9" strokeWidth={16} fill="none" strokeLinecap="round" />
            <rect x={262} y={236} width={7} height={22} fill="#f4eee1" />
            <circle cx={265} cy={230} r={6} fill="#ffcf6a" />
            <rect x={30} y={154} width={270} height={18} fill="#a8692c" stroke={ink} strokeWidth={5} />
            <circle cx={165} cy={86} r={34} fill="#f4eee1" stroke={ink} strokeWidth={5} />
            <ellipse cx={165} cy={60} rx={42} ry={24} fill="#fff" stroke={ink} strokeWidth={5} />
            <path d="M 140 118 L 190 118 L 200 154 L 130 154 Z" fill="#c0392b" stroke={ink} strokeWidth={5} />
          </svg>
          <div style={{ display: "flex", flexDirection: "column", gap: 17, flex: 1, paddingTop: 6 }}>
            {Array.from({ length: 10 }, (_, i) => <div key={i} style={{ height: 13, borderRadius: 6, background: "#cdb98c", width: i % 4 === 3 ? "62%" : "100%" }} />)}
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 17, width: "100%", marginTop: 26 }}>
          {Array.from({ length: 4 }, (_, i) => <div key={i} style={{ height: 13, borderRadius: 6, background: "#cdb98c", width: i === 3 ? "48%" : "100%" }} />)}
        </div>
      </div>
    </div>
  );
};
