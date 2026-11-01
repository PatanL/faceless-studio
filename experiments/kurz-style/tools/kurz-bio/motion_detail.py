import sys, numpy as np
z = np.load(sys.argv[1]); fps = float(z["fps"]); mad = z["mad"]; chg = z["chg"]; dx = z["dx"]; dy = z["dy"]; pk = z["pk"]
n = len(mad); end = float(sys.argv[2]) if len(sys.argv) > 2 else n / fps
m = int(end * fps)
spd = np.hypot(dx, dy) * fps * 7.5
st = mad[:m] < 0.25
# static runs > 1 s
runs = []; i = 0
while i < m:
    if st[i]:
        j = i
        while j < m and st[j]: j += 1
        if (j - i) / fps > 1.0: runs.append((round(i / fps, 1), round((j - i) / fps, 2), round(float(chg[i:j].max() * 100), 2)))
        i = j
    else: i += 1
print("static runs >1s (start, dur, max %pix changed):", runs)
print("static frames % (content only)", round(st.mean() * 100, 1), " truly frozen (chg==0) %", round(float((chg[:m] == 0).mean() * 100), 1))
ok = (pk[:m] > 0.08) & (mad[:m] < 6)
s = spd[:m][ok]
print("global shift px/s among non-transition frames: p25/50/75/90", np.percentile(s, [25, 50, 75, 90]).round(1))
print("share: <3 px/s", round((s < 3).mean() * 100, 1), " 3-60 drift", round(((s >= 3) & (s < 60)).mean() * 100, 1), " 60-400 pan", round(((s >= 60) & (s < 400)).mean() * 100, 1), " >400", round((s >= 400).mean() * 100, 1))
for a in sys.argv[3:]:
    t0, d = map(float, a.split(":")); i0 = int(t0 * fps); i1 = int((t0 + d) * fps)
    v = np.convolve(spd[i0:i1], np.ones(5) / 5, "same")
    k = max(1, len(v) // 16)
    print(f"profile {t0}+{d}s px/s:", [int(x) for x in v[::k]], " dir", round(float(np.degrees(np.arctan2(np.median(dy[i0:i1]), np.median(dx[i0:i1])))), 0))
