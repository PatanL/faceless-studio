#!/usr/bin/env python3
"""Shadow, light and timing model for whatif-earth-had-rings (pure Python, no deps).

Premise: Saturn's main rings (B, Cassini Division, A) scaled to Earth by planet radius and placed in
Earth's equatorial plane. Everything the script's HUD shows comes from this file:

    python3 rings.py            # prints every number used in script.md
    python3 rings.py --json F   # also writes the per-screen-second HUD track (date, days, km) to F

Model
- Sun declination and equation of time: NOAA fractional-year series, evaluated at local solar noon.
- Noon shadow: a point at latitude phi (winter hemisphere) looks up at the Sun through the ring plane
  at radius rho = cos(phi) + sin(phi) / tan|d| Earth radii (d = declination).
- Any time of day: exact ray/plane intersection (observer -> Sun ray crosses z = 0 at radius r).
- Light through a ring: direct beam exp(-tau / |sin d|), tau = normal optical depth (B 1.5, Cassini
  0.1, A 0.5; Saturn values, B ranges 0.5-5). Diffuse forward-scattered light is ignored, so the
  shaded numbers are lower bounds on light: all are labelled EST. on screen.
- Insolation: top of atmosphere (no air, no clouds), daily mean, S0 = 1361 W/m2.
Screen clock: 0:07.0 = JUN 21 2026, 3 days per screen second (0.1 day per frame at 30 fps).
"""
import json
import math
import sys
from datetime import date, timedelta

R_SAT = 60268.0
R_EARTH = 6371.0
KM_PER_DEG = 111.19
B_IN, B_OUT, A_IN, A_OUT = 92000 / R_SAT, 117580 / R_SAT, 122170 / R_SAT, 136775 / R_SAT
TAU = {'B': 1.5, 'CD': 0.1, 'A': 0.5}
S0 = 1361.0

MIAMI = (25.79, -80.13)   # Ocean Drive, Miami Beach
CITIES = {
    'Quito': (-0.18, -78.47), 'Bogota': (4.71, -74.07), 'Panama City': (8.98, -79.52),
    'Caracas': (10.49, -66.88), 'Havana': (23.11, -82.37), 'Miami Beach': MIAMI,
    'Rio de Janeiro': (-22.91, -43.17), 'Johannesburg': (-26.20, 28.05), 'Brisbane': (-27.47, 153.03),
    'Sydney': (-33.87, 151.21), 'Lima': (-12.05, -77.04), 'Fortaleza': (-3.73, -38.52),
    'Recife': (-8.05, -34.88), 'Manaus': (-3.12, -60.02), 'Salvador': (-12.97, -38.50),
    'Brasilia': (-15.79, -47.88), 'London': (51.51, -0.13), 'New York': (40.71, -74.01),
}
FLIP = date(2026, 6, 21)
FLIP_T = 7.0
DAYS_PER_SEC = 3.0


def zone(r):
    if B_IN <= r < B_OUT:
        return 'B'
    if B_OUT <= r < A_IN:
        return 'CD'
    if A_IN <= r <= A_OUT:
        return 'A'
    return None


def gamma(d, hour_utc):
    doy = d.timetuple().tm_yday
    ndays = 366 if (d.year % 4 == 0) else 365
    return 2 * math.pi / ndays * (doy - 1 + (hour_utc - 12) / 24)


def decl_rad(g):
    return (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))


def eqtime_min(g):
    return 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                     - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))


def noon_decl(d, lon):
    """Declination (rad) at local solar noon of date d at longitude lon (deg east)."""
    h = 12 - lon / 15
    g = gamma(d, h)
    h = 12 - lon / 15 - eqtime_min(g) / 60
    return decl_rad(gamma(d, h))


def noon_rho(lat, dec):
    """Ring-plane radius (Earth radii) the noon Sun is seen through, or None if not through the plane."""
    phi = math.radians(lat)
    if lat == 0 or dec == 0 or (lat > 0) == (dec > 0):
        return None
    return math.cos(phi) + abs(math.sin(phi)) / math.tan(abs(dec))


def ray_radius(lat, dec, h):
    """Observer at latitude lat, Sun at declination dec and hour angle h (rad). Returns (r, cos_zenith)."""
    phi = math.radians(lat)
    px, pz = math.cos(phi), math.sin(phi)
    sx, sy, sz = math.cos(dec) * math.cos(h), -math.cos(dec) * math.sin(h), math.sin(dec)
    cz = px * sx + pz * sz
    if cz <= 0:
        return None, cz
    if sz == 0 or (pz > 0) == (sz > 0):
        return None, cz
    t = -pz / sz
    x, y = px + t * sx, t * sy
    return math.hypot(x, y), cz


def transmission(r, dec):
    z = zone(r) if r is not None else None
    if z is None:
        return 1.0
    return math.exp(-TAU[z] / abs(math.sin(dec)))


def daily_insolation(lat, d, lon=0.0, rings=True, n=720):
    """Daily-mean TOA insolation (W/m2) at latitude lat on date d, with or without the ring shadow."""
    dec = noon_decl(d, lon)
    tot = 0.0
    for i in range(n):
        h = -math.pi + (i + 0.5) * 2 * math.pi / n
        r, cz = ray_radius(lat, dec, h)
        if cz <= 0:
            continue
        tr = transmission(r, dec) if rings else 1.0
        tot += S0 * cz * tr
    return tot / n


def shaded_hours(lat, d, lon, zones=('B',)):
    dec = noon_decl(d, lon)
    n, day, sh = 1440, 0, 0
    for i in range(n):
        h = -math.pi + (i + 0.5) * 2 * math.pi / n
        r, cz = ray_radius(lat, dec, h)
        if cz <= 0:
            continue
        day += 1
        if r is not None and zone(r) in zones:
            sh += 1
    return day * 24 / n, sh * 24 / n


def band_edges(dec):
    """Noon shadow band on the winter side: (equatorward edge lat, poleward edge lat), positive degrees."""
    def solve(target):
        lo, hi = 1e-6, 90 - math.degrees(abs(dec)) - 1e-6
        for _ in range(80):
            mid = (lo + hi) / 2
            if math.cos(math.radians(mid)) + math.sin(math.radians(mid)) / math.tan(abs(dec)) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    return solve(B_IN), solve(A_OUT)


def miami_distance_km(d):
    dec = noon_decl(d, MIAMI[1])
    if abs(dec) < 1e-4:
        return MIAMI[0] * KM_PER_DEG
    eq, pole = band_edges(dec)
    if dec > 0:   # band in the south: nearest edge is its equatorward edge
        return (MIAMI[0] + eq) * KM_PER_DEG
    if eq <= MIAMI[0] <= pole:
        return 0.0
    return (MIAMI[0] - pole) * KM_PER_DEG if MIAMI[0] > pole else (eq - MIAMI[0]) * KM_PER_DEG


def crossing(lat, lon, start, days, target, below=True):
    """First date (fractional) from start when the noon rho drops below (or rises above) target."""
    prev = None
    for k in range(days + 1):
        d = start + timedelta(days=k)
        rho = noon_rho(lat, noon_decl(d, lon))
        if rho is not None and prev is not None:
            ok = rho <= target if below else rho >= target
            if ok:
                frac = (target - prev[1]) / (rho - prev[1])
                return prev[0] + timedelta(days=frac), d
        prev = (d, rho if rho is not None else (99.0 if below else -99.0))
    return None, None


def screen_t(d):
    return FLIP_T + (d - FLIP).days / DAYS_PER_SEC


def fmt(d):
    return d.strftime('%b %d').upper()


def main():
    out = {}
    print('Ring radii (Earth radii): B %.3f-%.3f, Cassini to %.3f, A to %.3f' % (B_IN, B_OUT, A_IN, A_OUT))
    print('  altitude %.0f-%.0f km; main rings %.0f km wide' % ((B_IN - 1) * R_EARTH, (A_OUT - 1) * R_EARTH, (A_OUT - B_IN) * R_EARTH))
    lat = math.radians(MIAMI[0])

    # elevation: observer O = (cos lat, sin lat) in the meridian plane; ring point Q = (rr, 0) is due south
    def el(rr):
        ox, oz = math.cos(lat), math.sin(lat)
        # point of the ring plane (z = 0) due south of the observer, distance rr from Earth's centre
        qx, qz = rr, 0.0
        vx, vz = qx - ox, qz - oz
        # local up = (ox, oz); local south (horizontal, towards the equator) = (sin lat, -cos lat)
        up = vx * ox + vz * oz
        south = vx * math.sin(lat) - vz * math.cos(lat)
        return math.degrees(math.atan2(up, south))
    e1, e2 = el(B_IN), el(A_OUT)
    print('Sky from Miami Beach, due south: B inner %.1f deg, A outer %.1f deg, band %.1f deg = %.0f Moons' % (e1, e2, e2 - e1, (e2 - e1) / 0.52))
    out['sky'] = {'b_inner_deg': round(e1, 1), 'a_outer_deg': round(e2, 1), 'moons': round((e2 - e1) / 0.52)}

    # Miami transitions
    sep_eq = date(2026, 9, 23)
    a_in, _ = crossing(*MIAMI, sep_eq, 120, A_OUT, below=True)
    cd_in, _ = crossing(*MIAMI, sep_eq, 120, A_IN, below=True)
    b_in, _ = crossing(*MIAMI, sep_eq, 120, B_OUT, below=True)
    sol = date(2026, 12, 21)
    b_out, _ = crossing(*MIAMI, sol, 60, B_OUT, below=False)
    cd_out, _ = crossing(*MIAMI, sol, 60, A_IN, below=False)
    last, _ = crossing(*MIAMI, sol, 80, A_OUT, below=False)
    print('\nMiami Beach (noon): A edge arrives %s | Cassini %s | B %s | solstice rho %.3f | B ends %s | A again %s | last shadow %s'
          % (a_in, cd_in, b_in, noon_rho(MIAMI[0], noon_decl(sol, MIAMI[1])), b_out, cd_out, last))
    # next year's arrival
    a_in27, _ = crossing(*MIAMI, date(2027, 9, 23), 120, A_OUT, below=True)
    last_day = date(last.year, last.month, last.day)
    arr_day = date(a_in.year, a_in.month, a_in.day)
    arr27 = date(a_in27.year, a_in27.month, a_in27.day)
    print('  2027 arrival %s -> days from last shadow %s to next arrival: %d' % (a_in27, last_day, (arr27 - last_day).days))
    print('  days JUN 21 -> arrival %s: %d (screen %.2f s)' % (arr_day, (arr_day - FLIP).days, screen_t(arr_day)))
    out['miami'] = {k: fmt(date(v.year, v.month, v.day)) for k, v in
                    dict(a_in=a_in, cd_in=cd_in, b_in=b_in, b_out=b_out, cd_out=cd_out, last=last).items()}
    out['miami']['days_to_contact'] = (arr_day - FLIP).days
    out['miami']['return_days'] = (arr27 - last_day).days

    # transmission at noon on the transition beats
    for label, d in (('contact', arr_day), ('cassini', date(cd_in.year, cd_in.month, cd_in.day) + timedelta(days=1)),
                     ('b', date(b_in.year, b_in.month, b_in.day) + timedelta(days=1)), ('solstice', sol)):
        dec = noon_decl(d, MIAMI[1])
        rho = noon_rho(MIAMI[0], dec)
        print('  %-8s %s noon rho %.3f zone %s light %.0f%%' % (label, fmt(d), rho, zone(rho), 100 * transmission(rho, dec)))
    day_h, b_h = shaded_hours(MIAMI[0], sol, MIAMI[1], ('B',))
    _, any_h = shaded_hours(MIAMI[0], sol, MIAMI[1], ('B', 'CD', 'A'))
    print('  DEC 21: daylight %.1f h, in B shadow %.1f h, under any ring %.1f h' % (day_h, b_h, any_h))
    out['miami']['solstice_daylight_h'] = round(day_h, 1)
    out['miami']['solstice_b_hours'] = round(b_h, 1)

    # December insolation, with and without rings, and the latitude that normally gets that much
    dec_days = [date(2026, 12, k) for k in range(1, 32)]
    ring = sum(daily_insolation(MIAMI[0], d, MIAMI[1], True) for d in dec_days) / 31
    norm = sum(daily_insolation(MIAMI[0], d, MIAMI[1], False) for d in dec_days) / 31
    print('\nMiami December TOA insolation: %.0f W/m2 with rings vs %.0f normal = %.0f%%' % (ring, norm, 100 * ring / norm))
    eq_lat = None
    for la10 in range(260, 700):
        la = la10 / 10
        v = sum(daily_insolation(la, d, 0, False) for d in dec_days[::5]) / len(dec_days[::5])
        if v <= ring:
            eq_lat = la
            break
    print('  same December sunlight as latitude %.1f N normally gets (London 51.5, Amsterdam 52.4, Paris 48.9)' % eq_lat)
    lon_v = sum(daily_insolation(51.51, d, 0, False) for d in dec_days) / 31
    print('  London December TOA: %.0f W/m2 (%.0f%% of Miami normal)' % (lon_v, 100 * lon_v / norm))
    out['december'] = {'miami_ring_wm2': round(ring), 'miami_normal_wm2': round(norm), 'pct': round(100 * ring / norm),
                       'equivalent_lat': eq_lat, 'london_wm2': round(lon_v)}

    # band position at key dates
    print('\nNoon shadow band (Miami meridian):')
    for d in (FLIP, date(2026, 7, 1), date(2026, 7, 8), date(2026, 7, 24), date(2026, 8, 11), date(2026, 8, 23),
              date(2026, 9, 5), date(2026, 9, 10), date(2026, 10, 15), arr_day, sol):
        dec = noon_decl(d, MIAMI[1])
        eq, pole = band_edges(dec)
        side = 'S' if dec > 0 else 'N'
        print('  %s (t=%5.2f) decl %+5.1f  band %4.1f-%4.1f %s  Miami distance %5.0f km' % (fmt(d), screen_t(d), math.degrees(dec), eq, pole, side, miami_distance_km(d)))

    # cities: arrival of the A edge after the September equinox (north) or zone at given dates (south)
    print('\nNorthern arrivals (A edge reaches the city at noon):')
    stamps = {}
    for name in ('Bogota', 'Panama City', 'Caracas', 'Havana', 'Miami Beach'):
        la, lo = CITIES[name]
        c, _ = crossing(la, lo, sep_eq, 120, A_OUT, below=True)
        cd = date(c.year, c.month, c.day)
        print('  %-12s %5.2f N  %s  -> stamp %s at t=%.2f' % (name, la, c, fmt(cd), screen_t(cd)))
        stamps[name] = {'date': fmt(cd), 't': round(screen_t(cd), 2)}
    out['stamps'] = stamps

    print('\nSouthern cities under the band (noon zone / light):')
    for d in (FLIP, date(2026, 7, 8), date(2026, 7, 24), date(2026, 8, 23), date(2026, 9, 2), date(2026, 9, 5), date(2026, 9, 8)):
        row = []
        for name in ('Rio de Janeiro', 'Johannesburg', 'Brisbane', 'Sydney', 'Lima', 'Brasilia', 'Salvador', 'Recife', 'Fortaleza', 'Manaus'):
            la, lo = CITIES[name]
            dec = noon_decl(d, lo)
            rho = noon_rho(la, dec)
            z = zone(rho) if rho else None
            if z:
                row.append('%s %s %.1f%%' % (name, z, 100 * transmission(rho, dec)))
        print('  %s t=%5.2f: %s' % (fmt(d), screen_t(d), ', '.join(row) or '-'))

    # per-screen-second HUD track
    track = []
    t = FLIP_T
    while t <= 68.0 + 1e-9:
        dd = FLIP + timedelta(days=(t - FLIP_T) * DAYS_PER_SEC)
        dday = date(dd.year, dd.month, dd.day)
        track.append({'t': round(t, 2), 'date': fmt(dday), 'days_left': round(max(0.0, out['miami']['days_to_contact'] - (t - FLIP_T) * DAYS_PER_SEC), 1),
                      'km': int(round(miami_distance_km(dday) / 10) * 10)})
        t += 1.0
    out['track'] = track
    print('\nHUD track (t, date, days left, km):')
    print('  ' + ' | '.join('%g %s %.0f %d' % (r['t'], r['date'], r['days_left'], r['km']) for r in track))

    if '--json' in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w'), indent=1)


if __name__ == '__main__':
    main()
