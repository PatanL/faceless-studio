#!/usr/bin/env python3
"""Single source for whatif-everyone-born-same-day.

Holds the VO, on-screen text and shot list as data, computes every timestamp from word
counts and per-section TTS rates, measures pacing, and writes:
  script.md        (front matter metrics, VO with timestamps, shot list, fact sheet)
  storyboard.json  (studio/src/core/schema.ts, 16:9 30 fps)
Run: python3 gen_storyboard.py   (pure Python, no deps; small, fine on the Mac)
"""
import json
import math
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
FPS = 30
GAP = 0.12          # silence after each VO line
SECTION_GAP = 0.3  # extra silence at a section end
TITLE_CARD = 5.0    # music-only title card after the hook
END_SCREEN = 10.0

# ------------------------------------------------------------------ VO data
# (section label, TTS rate wpm, [(line id, VO text, [on-screen events])])
# on-screen events are (offset_s, text); offset is from the line start.
SECTIONS = [
 ("L1 COLD OPEN", 158, [
  ("h1", "Every second, about four babies are born somewhere on Earth.",
        [(0.0, "counter `BIRTHS THIS SECOND: 4` ticking in the corner over the crib field; PILL `~132 MILLION A YEAR`")]),
  ("h2", "Now imagine you, and everyone alive, born on the same morning.",
        [(0.6, "60 rows of 365 dots (`60 YEARS OF BIRTHS`) slam into one block; TAG `ONE MORNING`")]),
  ("h3", "Same day as you. Same year as you.",
        [(0.3, "every crib fills at once; the YOU crib gets its ringed baby; HUD in: `YEAR 0 · EVERYONE IS 0`")]),
  ("h4", "Eight billion newborns crying at once. The planet smells of warm milk.",
        [(0.2, "HUD `BABIES 8,000,000,000`"), (2.6, "warm milk-steam drifts over the field")]),
  ("h5", "Not quite everyone, though: two billion borrowed adults are here to hold you.",
        [(1.5, "HUD adds `ADULTS 2,000,000,000`")]),
  ("h6", "On day one, each adult gets four of you.",
        [(0.3, "scrubber draws in; tick `DAY 1` with bottle icon")]),
  ("h7", "At six, your class has ninety kids.",
        [(0.2, "scrubber tick `6` with desk icon")]),
  ("h8", "At sixty-five, you and the whole human race retire on one Monday.",
        [(0.3, "scrubber tick `65` with rocking-chair icon")]),
  ("h9", "And one of you will get a birthday none of the other eight billion ever had.",
        [(0.5, "scrubber end tick `?` with unlit candle; HUD line `YOUR ODDS OF BEING THE LAST: 1 IN 8,000,000,000`")]),
 ]),
 ("L2 TITLE CARD + RULES", 158, [
  ("r1", "The rules. No clones. No time machine. Same planet, same cities.",
        [(0.6, "TAGs `NO CLONES` `NO TIME MACHINE` struck through; `SAME PLANET · SAME CITIES`")]),
  ("r2", "One change: everyone alive shares your birthday, right down to the year.",
        [(0.4, "PYRAMID: the real 2024 world pyramid drains into one amber bar at age 0 (overflow chevron `×12`)")]),
  ("r3", "To keep you alive, two billion adults are on loan from the old world: one per four babies.",
        [(1.0, "grey bands `THE OLD WORLD · 2,000,000,000 ON LOAN`; inset `1 ADULT : 4 BABIES`")]),
  ("r4", "They raise you. Then, on your thirtieth birthday, they hand everything over and step out of the story.",
        [(1.8, "new scrubber tick `30` with key icon; chip `HANDOVER IN 30 YEARS`")]),
  ("r5", "Keep that date in mind.",
        [(0.0, "pin drops on the grey bands; TAG `KEEP THIS DATE`")]),
  ("r6", "Happy birthday, everyone.",
        [(0.2, "HUD switches to `TOTAL ALIVE 10,000,000,000` / `YOUR AGE GROUP 8,000,000,000`; scrubber dot starts")]),
 ]),
 ("L3 DAY 1", 164, [
  ("d1", "Day one.", [(0.0, "STAMP `DAY 1` / `EIGHT BILLION BIRTHDAYS`")]),
  ("d2", "Normally, the world handles about three hundred and sixty thousand births a day.",
        [(1.2, "bars `NORMAL DAY ~360,000`")]),
  ("d3", "Today, you're sixty years' worth before lunch.",
        [(0.2, "bar `TODAY 8,000,000,000` overflows; PILL `~60 YEARS OF BIRTHS`")]),
  ("d4", "That's the first promise: every adult on Earth has four newborns, and newborns feed every few hours, all night.",
        [(0.0, "the `DAY 1` bottle tick lights (promise 1 paid)")]),
  ("d5", "That's around forty feeds and forty diaper changes, per adult, per day.",
        [(0.3, "stat `40 FEEDS + 40 DIAPERS / ADULT / DAY (EST.)`")]),
  ("d6", "Here's the problem: who's running the power stations? The farms? The hospitals?",
        [(0.0, "three panels light: power station, farm, hospital, each tagged `UNSTAFFED?`")]),
  ("d7", "Yesterday, three and a half billion people had jobs. Today, there are two billion adults, all of them up at night with you.",
        [(0.4, "bars `JOBS YESTERDAY ~3.5 BN` vs `ADULTS TODAY 2 BN · ALL ON NIGHT FEEDS`")]),
  ("d8", "Fine. We'll be kind: the lights stay on, and nobody goes hungry.",
        [(0.6, "tags flip to ticks; TAG `RULE 2: LIGHTS ON · NOBODY HUNGRY`")]),
  ("d9", "But nobody on Earth sleeps for about a year.",
        [(0.6, "TAG `SLEEP: 0`")]),
 ]),
 ("L4 YEARS 1-5", 160, [
  ("y1a", "Then it gets lovely.", [(0.0, "corner STAMP `YEAR 1`")]),
  ("y1b", "Over a few months, the whole species learns to walk, clinging to somebody's hand.",
        [(0.5, "TAG `FIRST STEPS: EVERYONE`")]),
  ("y1c", "Your birthday is a planet-wide holiday. Somewhere, a bakery gets an order for eight billion cakes.",
        [(2.4, "receipt rolls off-frame `ORDER: 8,000,000,000 CAKES`")]),
  ("y1d", "Nobody is the baby of the family. Nobody is ever too old for the swings.",
        [(0.4, "TAG `OLDEST KID ON THE SWINGS: 1`")]),
  ("y1e", "It's the fairest world there's ever been. Until you turn six.",
        [(2.0, "the desk tick blinks")]),
 ]),
 ("L5 YEAR 6", 164, [
  ("y6a", "Year six.", [(0.0, "STAMP `YEAR 6` / `FIRST DAY OF SCHOOL`")]),
  ("y6b", "The first day of school is one Monday, for everybody.", []),
  ("y6c", "Here's the problem: Earth has fewer than a hundred million teachers, so your class has about ninety kids in it. Today's average is twenty-three.",
        [(1.8, "stat `~90 KIDS PER TEACHER` / grey `TODAY ~23`; desk tick lights (promise 2 paid)")]),
  ("y6d", "Sound impossible? One country already ran a small version.",
        [(1.0, "map pin + ring on Romania; chip `1966`")]),
  ("y6e", "In nineteen sixty-six, Romania banned abortion almost overnight, and the next year, births nearly doubled.",
        [(1.0, "bars `1966 ~274,000` -> `1967 ~528,000`")]),
  ("y6f", "That one bulge jammed maternity wards, then classrooms, then university entrance, for twenty years.",
        [(0.3, "gates `MATERNITY` -> `SCHOOL` -> `UNIVERSITY` flash red")]),
  ("y6g", "Romania doubled one year. You're sixty years in a single morning.",
        [(0.3, "bars `ROMANIA ×2` vs `YOU ×22,000`")]),
  ("y6h", "Your year-group photo has to be taken from orbit.",
        [(0.4, "camera flash; TAG `YEAR-GROUP PHOTO: 7,700,000,000`")]),
 ]),
 ("L6 YEAR 18", 166, [
  ("y18a", "Year eighteen.", [(0.0, "STAMP `YEAR 18` / `EVERYONE GRADUATES`")]),
  ("y18b", "Everyone on Earth finishes school on the same day.", []),
  ("y18c", "The world has a quarter of a billion university places, about one per thirty-two of you, and three and a half billion jobs, with the old world sitting in most of them.",
        [(0.6, "32 chairs, one lit; PILL `~250 M UNIVERSITY PLACES`"), (6.2, "stat `~3.5 BN JOBS / 8 BN APPLICANTS`")]),
  ("y18e", "In twenty thirteen, more than half of young Spaniards looking for work couldn't find any. They called it a crisis.",
        [(0.5, "map pin + ring on Spain; chip `2013`; PILL `SPAIN, UNDER-25 UNEMPLOYMENT ~56%`")]),
  ("y18f", "For you, it's the whole planet.",
        [(1.2, "every continent fills amber on 'planet'")]),
  ("y18g", "Dating is easy, though. Everyone is exactly your age.",
        [(1.4, "TAG `AGE GAP: 0`")]),
  ("y18h", "Which is why, a few years later, you all have kids. At once.",
        [(2.4, "strollers pop in across the park")]),
 ]),
 ("L6b YEAR 24, THE ECHO", 164, [
  ("e1", "Year twenty-four.", [(0.0, "corner STAMP `YEAR 24`")]),
  ("e2", "At a bit over two children per woman, a second wave rolls in: about eight billion babies, most of them inside twenty years.",
        [(0.5, "PILL `~2.2 CHILDREN PER WOMAN`; teal bands grow under the amber bar; HUD `TOTAL ALIVE` 9.9 -> 11.8 BN")]),
  ("e3", "Demographers would call your kids an echo.", [(0.3, "TAG `THE ECHO`")]),
  ("e4", "Japan has one: a boom after the Second World War, then a smaller one in the early seventies, when those babies had babies.",
        [(1.0, "mini Japan pyramid, chips `1947-49` and `1971-74`, arrow parent bulge -> child bulge")]),
  ("e5", "Yours is the loudest echo in history.", []),
 ]),
 ("L7 YEAR 30, MIDPOINT RUG PULL", 156, [
  ("m1", "But exams and jobs turn out to be the easy part.",
        [(0.0, "music cuts; the `KEEP THIS DATE` pin glows; scrubber key tick `30` flashes; chip `HANDOVER IN 0 YEARS`")]),
  ("m2", "Year thirty. The date from the rules.", [(0.0, "corner STAMP `YEAR 30`")]),
  ("m3", "On your thirtieth birthday, two billion adults hand over the keys and step out. All at once.",
        [(2.2, "every grey band lifts off the pyramid together; HUD `TOTAL ALIVE` 14.7 -> 13.0 BN")]),
  ("m4", "Look at the chart. Nobody on Earth is older than you.",
        [(1.0, "TAG `OLDEST PERSON ALIVE: 30`")]),
  ("m5", "At eighteen, there weren't enough jobs. But at thirty, every senior job on the planet is suddenly yours.",
        [(2.4, "TAG `OPEN TODAY: EVERY SENIOR JOB`")]),
  ("m6", "The most experienced surgeon alive is still finishing their training.",
        [(0.3, "panel `SURGEON · STILL IN TRAINING`")]),
  ("m7", "Every judge, every pilot, every power-station engineer: thirty. Same as you.",
        [(0.0, "panels `JUDGE 30` `PILOT 30` `POWER STATION 30`")]),
  ("m8", "Your kids will never meet a grandparent. And nobody is left to ask how anything used to work.",
        [(0.6, "TAG `GRANDPARENTS: 0`")]),
 ]),
 ("L8 YEAR 65, TRAILER PAID", 164, [
  ("r65a", "Year sixty-five. The retirement promise comes due.",
        [(0.0, "STAMP `YEAR 65` / `ONE MONDAY`; rocking-chair tick lights (promise 3 paid)")]),
  ("r65b", "On one Monday, over six billion of you stop working, and every pension on Earth starts paying at once.",
        [(0.6, "stat `~6.3 BN RETIREES (EST.)`; HUD odds `1 IN 6,300,000,000`")]),
  ("r65c", "Here's the catch: who does the work? Your kids, the echo, now twenty to forty-five.", []),
  ("r65d", "Japan, the oldest big country today, has about one retiree for every two working-age adults. You have three for every four.",
        [(0.6, "icon rows `JAPAN TODAY 1 : 2`"), (5.6, "icon rows `YOUR WORLD 3 : 4`")]),
  ("r65e", "Every golf course on Earth is booked solid.", [(0.4, "TAG `TEE TIMES: SOLD OUT`")]),
 ]),
 ("L8b YEAR 80, LOW POINT", 148, [
  ("r80a", "Then come the hard years.", []),
  ("r80b", "Year eighty. Half of you are gone.",
        [(0.0, "corner STAMP `YEAR 80`; HUD `YOUR AGE GROUP 3,800,000,000`; odds `1 IN 3,800,000,000`")]),
  ("r80c", "The world holds four times today's funerals, and nearly every one is for someone your age.",
        [(0.6, "PILL `~4× TODAY'S YEARLY DEATHS (EST.)`")]),
  ("r80d", "Your friends. Your partner. Half of that ninety-kid classroom.",
        [(1.4, "the class photo from YEAR 6 loses half its faces")]),
  ("r80e", "Was sharing every birthday worth it? Or did it just mean losing everyone together?", []),
 ]),
 ("L8c REVERSAL", 160, [
  ("rv1", "But look at the chart again.", []),
  ("rv2", "Under your shrinking bar sits the echo, and under that, the echo's echo, lower and wider.",
        [(2.4, "TAG `ECHO OF THE ECHO`")]),
  ("rv3", "Japan already showed you how this ends.", []),
  ("rv4", "Its first boom peaked at two point seven million babies in nineteen forty-nine.",
        [(0.6, "chip `1949 · 2.7 M BIRTHS`")]),
  ("rv5", "The echo, in nineteen seventy-three, peaked at two point one million, spread across more years.",
        [(0.6, "chip `1973 · 2.1 M BIRTHS`")]),
  ("rv6", "But the third wave everyone expected around two thousand? It never really showed up.",
        [(0.6, "dotted bump `EXPECTED ~2000`; TAG `NEVER CAME`")]),
  ("rv8", "Your birthday put eight billion babies into one day. The echo's busiest day has about one and a half million.",
        [(0.4, "bars `YOUR BIRTHDAY 8,000,000,000` vs `ECHO'S BUSIEST DAY ~1,500,000 (EST.)` vs `TODAY ~360,000`; TAG `EACH WAVE: LOWER AND WIDER`")]),
  ("rv9", "By the time you're a hundred, your family has birthdays in every month.",
        [(0.6, "12-month calendar inset fills with family birthdays")]),
 ]),
 ("L9 YEARS 100-110, CLIMB", 160, [
  ("c1", "Year one hundred.", [(0.0, "STAMP `YEAR 100` / `THE CENTURY`; HUD switches to survivors mode")]),
  ("c2", "Roughly forty million of you are still here, more than fifty times today's centenarians.",
        [(0.3, "stat `~40,000,000 AGED 100 (EST.)` / grey `TODAY ~0.72 M`; HUD odds `1 IN 40,000,000`")]),
  ("c3", "But past a hundred and five, each birthday is a coin toss.", []),
  ("c4", "A twenty eighteen study of Italy's oldest people found about half die before their next birthday, every year.",
        [(0.4, "PILL `105+: ~50% EACH YEAR` / source `Barbi et al., Science, 2018`")]),
  ("c5", "From here on, this is less a forecast and more a dice roll.",
        [(1.0, "`ESTIMATE` stamp lands on the HUD")]),
 ]),
 ("L9c YEAR 110, HALVING LADDER", 154, [
  ("c6", "At a hundred and ten, forty thousand of you.",
        [(0.0, "corner STAMP `YEAR 110`; HUD survivors `40,000`; odds `1 IN 40,000`")]),
  ("c7", "Twenty thousand at a hundred and eleven. Then ten thousand. Five thousand.",
        [(0.0, "HUD `20,000` (YEAR 111)"), (2.6, "HUD `10,000` (YEAR 112)"), (3.6, "HUD `5,000` (YEAR 113)")]),
  ("c8", "By a hundred and twenty, a few dozen of you.",
        [(0.6, "HUD `YEAR 120 · ~40`; odds `1 IN 40`")]),
  ("c9", "The longest life on record is Jeanne Calment's: a hundred and twenty-two years and five months.",
        [(0.6, "PILL `RECORD: 122 YEARS, 164 DAYS (1875-1997)`; `122` marker on the scrubber")]),
  ("c10", "With that many people rolling the same dice, one of you very likely beats her.",
        [(1.5, "the scrubber dot creeps past 122")]),
 ]),
 ("L9d YEAR 125, MASTER PAYOFF + SECOND STAGE", 148, [
  ("p1", "Year one hundred and twenty-five. One of you is left.",
        [(0.0, "STAMP `YEAR 125` / `ALIVE: 1`; HUD odds `1 IN 1`")]),
  ("p2", "And here's the birthday none of the others ever had.", []),
  ("p3", "For the first time in their life, nobody else on Earth is turning the same age.",
        [(0.6, "one lit candle")]),
  ("p4", "Eight billion birthdays, down to one.", []),
  ("p5", "But that isn't the strangest part. Look who's at the table.",
        [(1.8, "pull out: family of every age around the table")]),
  ("p6", "Grandkids. Great-great-grandkids. Every one of them born on a different day.",
        [(1.0, "date tags pop over the family: `MAR 3` `JUL 19` `FEB 29` `NOV 1` ...")]),
  ("p7", "And outside, the counter from the very first second is back to normal: about four babies a second.",
        [(1.2, "corner counter `BIRTHS THIS SECOND: 4` returns from 0:00; candle tick lights; HUD and scrubber fade out")]),
 ]),
 ("L10 BOOKEND + RECAP + THESIS", 152, [
  ("b1", "Go back to that first morning.", []),
  ("b2", "Sixty years of births before lunch. Ninety kids to a class. Every job handed over in a day. One last candle.",
        [(0.3, "recap icons `DAY 1 · 60 YEARS OF BIRTHS` `YEAR 6 · 90 PER CLASS` `YEAR 30 · THE HANDOVER` `YEAR 65 · ONE MONDAY` `YEAR 125 · ONE CANDLE`")]),
  ("b3", "All of it came from removing one thing: the gaps between us.", [(1.6, "TAG `THE GAPS`")]),
  ("b4", "But in the real world, somebody is always a few steps ahead of you.", []),
  ("b5", "Someone holding your hand while you learned to walk. Someone teaching ninety kids. Someone handing over the keys.", []),
  ("b6", "A population pyramid isn't really a chart. It's a relay race, and it only works if somebody is right behind you.",
        [(2.6, "TAG `IT'S A RELAY`")]),
 ]),
 ("L11 CTA", 156, [
  ("cta1", "So, would you rather be one of the eight billion, sharing your birthday with the whole planet?",
        [(0.6, "card 1 `THE COHORT · ONE BIRTHDAY WITH 8 BN`")]),
  ("cta2", "Or one of their kids, born into a world where every grown-up is exactly the same age? Tell me below.",
        [(0.6, "card 2 `THE ECHO · EVERY GROWN-UP THE SAME AGE`")]),
 ]),
]

EXTRA_PAUSE_BEFORE = {"m1": 0.8, "p1": 0.6, "b1": 0.4, "rv1": 0.4}

# ------------------------------------------------------------------ timing


def wc(s):
    return len(s.split())


LINES = {}
order = []
t = 0.0
sec_bounds = []
for si, (label, rate, lines) in enumerate(SECTIONS):
    sec_start = None
    for li, (lid, text, os_) in enumerate(lines):
        t += EXTRA_PAUSE_BEFORE.get(lid, 0.0)
        if sec_start is None:
            sec_start = t
        dur = wc(text) * 60.0 / rate
        LINES[lid] = dict(id=lid, text=text, os=os_, start=round(t, 2), dur=round(dur, 2),
                          end=round(t + dur, 2), section=label, rate=rate)
        order.append(lid)
        t += dur + GAP
    t += SECTION_GAP
    if label.startswith("L1 "):
        hook_end = t
        t += TITLE_CARD  # silent title card
    sec_bounds.append((label, sec_start, LINES[lines[-1][0]]["end"], rate))
NARRATION_END = LINES["cta2"]["end"]
RUNTIME = round(NARRATION_END + 0.6 + END_SCREEN, 1)
TITLE_START = round(hook_end, 2)


def mmss(x):
    x = max(0.0, x)
    return f"{int(x // 60)}:{int(x % 60):02d}"


def mmss1(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"

# ------------------------------------------------------------------ metrics

ALL_TEXT = [LINES[i]["text"] for i in order]
SENTS = []
for s in ALL_TEXT:
    SENTS += [p.strip() for p in re.split(r"(?<=[.?!])\s+", s) if p.strip()]
YOU = re.compile(r"\b(you|your|you're|yourself|yours)\b", re.I)
PIV = re.compile(r"\b(but|except|until|here's|problem|catch|though|instead)\b", re.I)
NUMW = re.compile(r"\b(\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|half|twenty-\w+|thirty-\w+|forty-\w+|sixty-\w+|seventy-\w+|eighty-\w+|ninety-\w+)\b", re.I)
total_words = sum(wc(s) for s in ALL_TEXT)
narr_min = NARRATION_END / 60
M = dict(
    words=total_words,
    sentences=len(SENTS),
    mean_sentence=round(total_words / len(SENTS), 1),
    punch_pct=round(100 * sum(1 for s in SENTS if wc(s) <= 3) / len(SENTS), 1),
    second_person_pct=round(100 * sum(1 for s in SENTS if YOU.search(s)) / len(SENTS), 1),
    you_words=sum(len(YOU.findall(s)) for s in ALL_TEXT),
    pivots_per_min=round(sum(len(PIV.findall(s)) for s in ALL_TEXT) / narr_min, 2),
    questions=sum(s.count("?") for s in ALL_TEXT),
    numbers_per_min=round(sum(len(NUMW.findall(s)) for s in ALL_TEXT) / narr_min, 1),
    wpm_overall=round(total_words / narr_min, 1),
    narration_end=NARRATION_END,
    runtime=RUNTIME,
)
hook_ids = [lid for lid, _, _ in SECTIONS[0][2]]
M["hook_words"] = sum(wc(LINES[i]["text"]) for i in hook_ids)
M["hook_end"] = LINES["h9"]["end"]
M["you_first_30s"] = sum(len(YOU.findall(LINES[i]["text"])) for i in order if LINES[i]["start"] < 30)
spoken = sum(LINES[i]["dur"] for i in order)
M["wpm_spoken"] = round(total_words / (spoken / 60), 1)

# ------------------------------------------------------------------ storyboard helpers
NAVY = "#13213A"; AMBER = "#F2B33D"; GREY = "#9AA3AE"; TEAL = "#3FB8AF"; CREAM = "#F4EEDF"; RED = "#E2554B"

# approx UN WPP 2024 world population by 5-year band, millions (both sexes) and male share.
# Replace with the exact WPP 2024 CSV values before render (fact sheet).
WPP2024 = [[0, 660, .515], [5, 680, .515], [10, 680, .515], [15, 640, .514], [20, 615, .512],
           [25, 610, .510], [30, 620, .508], [35, 580, .505], [40, 525, .502], [45, 480, .498],
           [50, 455, .494], [55, 400, .488], [60, 340, .478], [65, 290, .466], [70, 220, .452],
           [75, 145, .435], [80, 90, .41], [85, 50, .37], [90, 20, .32], [95, 5, .26], [100, 0.6, .2]]
PYR_SCALE = {"refValueM": 700, "refHalfWidthPct": 40, "overflow": "clip+chevron"}


def comp(name, props=None, **kw):
    d = {"type": "component", "name": name, "props": props or {}}
    d.update(kw)
    return d


def board():
    return {"type": "color", "color": NAVY}


def setbg(name, **props):
    p = {"name": name}
    p.update(props)
    return {"type": "component", "name": "whatif/Set", "props": p}


def tag(text, at=0.3, x="50%", y="22%"):
    return comp("explainer/Tag", {"text": text, "at": at, "align": "center"}, x=x, y=y, width=1100, height=90, depth=0, z=70)


def stat(value, label, at=0.3, x="50%", y="45%", sub=None):
    p = {"value": value, "label": label, "at": at}
    if sub:
        p["sub"] = sub
    return comp("explainer/Stat", p, x=x, y=y, width=1100, height=320, depth=0, z=60)


def pill(text, source=None, at=0.3):
    p = {"text": text, "at": at}
    if source:
        p["source"] = source
    # zone: pills top-centre under the HUD row; source line top-right (whatif/Pill draws both)
    return comp("whatif/Pill", p, x="50%", y=150, width=1000, height=70, depth=0, z=85)


LAYER_KEYS = {"start", "end", "idle", "enter", "exit", "keyframes", "z", "depth", "opacity", "blur", "rotate"}


def person(age="adult", pose="stand", color=AMBER, hat=None, you=False, x="50%", y="70%", h=300, **kw):
    p = {"age": age, "pose": pose, "color": color}
    if hat:
        p["hat"] = hat
    if you:
        p["you"] = True
    lk = {k: v for k, v in kw.items() if k in LAYER_KEYS}
    p.update({k: v for k, v in kw.items() if k not in LAYER_KEYS})
    return comp("whatif/Person", p, x=x, y=y, width=int(h * 0.6), height=h, **lk)


def crowd(age, count, color=AMBER, rows=None, you_index=None, x="50%", y="62%", w=1700, h=560, **props):
    p = {"age": age, "count": min(count, 500), "color": color, "pattern": "staticFadeBeyondRow4"}
    if rows:
        p["rows"] = rows
    if you_index is not None:
        p["youIndex"] = you_index
    p.update(props)
    return comp("whatif/Crowd", p, x=x, y=y, width=w, height=h)


def icon(name, x, y, size=120, **kw):
    return comp("whatif/Icon", {"name": name}, x=x, y=y, width=size, height=size, **kw)


def pyramid(bands, **props):
    p = {"bands": bands, "scale": PYR_SCALE}
    p.update(props)
    return comp("whatif/Pyramid", p, x="50%", y="52%", width=1500, height=760, z=10)


def stamp(year, sub=None, corner=False):
    p = {"year": year, "corner": corner}
    if sub:
        p["sub"] = sub
    if corner:
        return comp("whatif/YearStamp", p, x=1640, y=230, width=360, height=150, depth=0, z=88)
    return comp("whatif/YearStamp", p, x="50%", y="50%", width=1920, height=1080, depth=0, z=95)


def bars(rows, title=None, at=0.3, y="50%", max=None):
    p = {"rows": rows, "at": at, "stagger": 0.8}
    if max is not None:
        p["max"] = max
    if title:
        p["title"] = title
    return comp("explainer/SpeedBars", p, x="50%", y=y, width=1500, height=420, depth=0, z=50)


def mapview(views, pins=None, highlight=None, at=0):
    p = {"views": views, "pins": pins or [], "at": at}
    if highlight:
        p["highlight"] = highlight
    return comp("explainer/Map", p, x="50%", y="50%", width=1920, height=1080, depth=0.2)


CONTINENTS = ["northAmerica", "southAmerica", "eurasia", "africa", "australia", "antarctica"]

# HUD states (TOTAL ALIVE = cohort + echoes + borrowed adults; YOUR AGE GROUP = cohort only). EST. from fact sheet model.
HUD = {
 "y0hook":  {"mode": "hook", "year": "YEAR 0", "sub": "EVERYONE IS 0", "babies": "8,000,000,000", "adults": "2,000,000,000"},
 "y0":   {"mode": "year", "year": "YEAR 0", "sub": "EVERYONE IS 0", "total": "10,000,000,000", "cohort": "8,000,000,000"},
 "d1":   {"mode": "year", "year": "DAY 1", "sub": "EVERYONE IS 1 DAY OLD", "total": "10,000,000,000", "cohort": "8,000,000,000"},
 "y1":   {"mode": "year", "year": "YEAR 1", "sub": "EVERYONE IS 1", "total": "9,800,000,000", "cohort": "7,800,000,000"},
 "y6":   {"mode": "year", "year": "YEAR 6", "sub": "EVERYONE IS 6", "total": "9,700,000,000", "cohort": "7,700,000,000"},
 "y18":  {"mode": "year", "year": "YEAR 18", "sub": "EVERYONE IS 18", "total": "9,900,000,000", "cohort": "7,600,000,000"},
 "y24":  {"mode": "year", "year": "YEAR 24", "sub": "EVERYONE IS 24", "total": "11,800,000,000", "cohort": "7,600,000,000"},
 "y30a": {"mode": "year", "year": "YEAR 30", "sub": "EVERYONE IS 30", "total": "14,700,000,000", "cohort": "7,500,000,000", "odds": "1 IN 7,500,000,000"},
 "y30b": {"mode": "year", "year": "YEAR 30", "sub": "NOBODY IS OLDER", "total": "13,000,000,000", "cohort": "7,500,000,000", "odds": "1 IN 7,500,000,000"},
 "y65":  {"mode": "year", "year": "YEAR 65", "sub": "EVERYONE IS 65", "total": "21,200,000,000", "cohort": "6,300,000,000", "odds": "1 IN 6,300,000,000"},
 "y80":  {"mode": "year", "year": "YEAR 80", "sub": "EVERYONE IS 80", "total": "22,200,000,000", "cohort": "3,800,000,000", "odds": "1 IN 3,800,000,000"},
 "y100": {"mode": "survivors", "year": "YEAR 100", "cohort": "~40,000,000", "odds": "1 IN 40,000,000", "estimate": True},
 "y110": {"mode": "survivors", "year": "YEAR 110", "cohort": "40,000", "odds": "1 IN 40,000", "estimate": True,
          "ladder": [{"t": 0, "year": "YEAR 110", "cohort": "40,000"}, {"t": "c7+0.0", "year": "YEAR 111", "cohort": "20,000"},
                     {"t": "c7+2.6", "year": "YEAR 112", "cohort": "10,000"}, {"t": "c7+3.6", "year": "YEAR 113", "cohort": "5,000"},
                     {"t": "c8+0.6", "year": "YEAR 120", "cohort": "~40", "odds": "1 IN 40"}]},
 "y120": {"mode": "survivors", "year": "YEAR 120", "cohort": "~40", "odds": "1 IN 40", "estimate": True},
 "y122": {"mode": "survivors", "year": "YEAR 122", "cohort": "~7", "odds": "1 IN 7", "estimate": True},
 "y125": {"mode": "survivors", "year": "YEAR 125", "cohort": "1", "odds": "1 IN 1", "estimate": True},
}

TICKS_ALL = [
    {"year": 0, "icon": "bottle", "label": "DAY 1"},
    {"year": 6, "icon": "desk", "label": "6"},
    {"year": 30, "icon": "key", "label": "30"},
    {"year": 65, "icon": "rockingChair", "label": "65"},
    {"year": 125, "icon": "candle", "label": "?"},
]


def scrub(dot, lit=(), show=("DAY 1", "6", "65", "?", "30"), marker=None):
    ticks = [dict(tk, lit=tk["label"] in lit) for tk in TICKS_ALL if tk["label"] in show]
    p = {"dot": dot, "ticks": ticks, "max": 125}
    if marker:
        p["marker"] = marker
    # zone: scrubber y 94-98% of 1080
    return comp("whatif/Scrubber", p, x="50%", y=1037, width=1728, height=40, depth=0, z=90)


def hud(state):
    p = dict(HUD[state])
    return comp("whatif/Hud", p, x=96, y=60, anchorX=0, anchorY=0, width=640, height=170, depth=0, z=92)

# ------------------------------------------------------------------ shot list
# Each shot: anchor (line id, offset) or absolute time; type; description; camera; sfx; storyboard spec.
# Camera: preset names from core (pushIn/pullOut/pan*/drift) or explicit keyframes; no 'zoom' preset exists.


def cam(preset=None, amount=1.0, keys=None, shake=None):
    c = {"preset": preset or "none", "amount": amount}
    if keys:
        c["keyframes"] = keys
    if shake:
        c["shake"] = shake
    return c


SHOTS = [
 # ---------------- L1
 dict(id="s01-crib-field", at=("h1", 0), type="STORY extreme wide (impossible frame 0)",
      desc="`whatif/Set` `ward` = the crib field: side-on rows of cribs to the horizon at dawn (per-row scale for depth, `whatif/Crowd` age baby capped at 480 near cribs + static pattern fade beyond row 4). Cribs are empty; 4 light up amber each second. Corner `explainer/Stat` counter `BIRTHS THIS SECOND: 4`. One front crib carries the cream YOU ring, still empty. `whatif/Pill` `~132 MILLION A YEAR`.",
      camera=cam("pullOut", 0.3), cam_txt="slow `pullOut` 0.3", sfx=[("pop", 0.4, 0.3), ("pop", 1.4, 0.3), ("pop", 2.4, 0.3)], sfx_txt="`documentary_pulse` bed in low; soft `pop` per lit crib",
      bg=setbg("ward", light="dawn"),
      layers=lambda: [crowd("baby", 480, fill=0.0, litPerSecond=4, you_index=7), stat(4, "BIRTHS THIS SECOND", x=1700, y=180), pill("~132 MILLION A YEAR", "UN WPP 2024", at=0.8)]),
 dict(id="s02-sixty-years", at=("h2", 0), type="BOARD graphic",
      desc="Navy board: 60 rows x 365 columns of amber dots labelled `60 YEARS OF BIRTHS` slide together from both sides into one bright block; `explainer/Tag` `ONE MORNING`.",
      camera=cam("pullOut", 0.15), cam_txt="`pullOut` 0.15 as the strip compresses", sfx=[("whoosh_long", 0.4, 0.7), ("impact", 2.6, 0.8)], sfx_txt="`whoosh_long`, `impact` when the block lands",
      bg=board(), layers=lambda: [comp("whatif/DotStrip", {"rows": 60, "cols": 365, "label": "60 YEARS OF BIRTHS", "collapseAt": 0.6, "collapseDur": 2.0}, x="50%", y="48%", width=1600, height=600), tag("ONE MORNING", at=2.7, y="82%")]),
 dict(id="s03-every-crib", at=("h3", 0), type="STORY wide",
      desc="Back on the crib field: every crib fills at once with an amber baby (`whatif/Crowd` fill 0 -> 1 in 0.5 s); the YOU crib's baby gets its cream ring. `whatif/Hud` fades in top-left `YEAR 0 · EVERYONE IS 0`.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 2.4, "zoom": 1.25, "x": "42%", "y": "60%"}]), cam_txt="keyframed push to the YOU crib (zoom 1 -> 1.25)",
      sfx=[("stinger", 0.2, 0.7)], sfx_txt="`stinger` + music swell (no layered-breath crowd)",
      bg=setbg("ward", light="dawn"), hud="y0hook", layers=lambda: [crowd("baby", 480, fill=1.0, fillAt=0.2, you_index=7)]),
 dict(id="s04-crying", at=("h4", 0), type="STORY extreme wide",
      desc="The full field, tiny `waa` glyphs popping above cribs; cream milk-steam `particles` (dust preset, rising) drift across. HUD `BABIES 8,000,000,000`.",
      camera=cam("pullOut", 0.5), cam_txt="`pullOut` 0.5 (ease out)", sfx=[("pop", 0.3, 0.4)], sfx_txt="music swell holds; soft `pop`s",
      bg=setbg("ward", light="dawn"), hud="y0hook",
      layers=lambda: [crowd("baby", 480, fill=1.0, crying=True, you_index=7), {"type": "particles", "preset": "dust", "count": 120, "color": CREAM, "speed": 0.4, "start": 2.6, "depth": 0.6}]),
 dict(id="s05-borrowed-adults", at=("h5", 0), type="STORY medium",
      desc="Grey adult `whatif/Person` (pose hold) figures stand up between the cribs, one per four cribs; one holds the YOU baby. HUD adds `ADULTS 2,000,000,000`.",
      camera=cam("drift"), cam_txt="`drift`", sfx=[], sfx_txt="music drops to bass only",
      bg=setbg("ward", light="dawn"), hud="y0hook",
      layers=lambda: [crowd("baby", 120, rows=3, you_index=5, y="72%"), person("adult", "hold", GREY, x="38%", y="62%"), person("adult", "hold", GREY, x="62%", y="62%"), person("adult", "stand", GREY, x="84%", y="60%", h=240)]),
 dict(id="s06-trailer", at=("h6", 0), type="BOARD trailer",
      desc="Navy board; `whatif/Scrubber` draws in along the bottom (DAY 1 -> 125). Ticks pop with the VO: bottle `DAY 1`, desk `6`, rocking chair `65`, each with a small vignette above it (one grey adult + 4 cribs; a 9x10 grid of kids; one calendar page `MONDAY`).",
      camera=cam(keys=[{"t": 0, "x": "30%"}, {"t": 7.5, "x": "70%", "ease": "linear"}]), cam_txt="keyframed pan right along the ticks",
      sfx=[("tick", 0.3, 0.6), ("pop", 0.4, 0.5), ("tick", 2.8, 0.6), ("pop", 2.9, 0.5), ("tick", 5.4, 0.6), ("pop", 5.5, 0.5)], sfx_txt="`tick` + `pop` per milestone",
      bg=board(), hud="y0hook", scrub=dict(dot=0, show=("DAY 1", "6", "65")),
      layers=lambda: [icon("cribQuad", "22%", "40%", 220, start=0.3), icon("classGrid", "50%", "40%", 220, start=2.9), icon("calendarMonday", "78%", "40%", 220, start=5.5)]),
 dict(id="s07-master-loop", at=("h9", 0), type="STORY close-up",
      desc="`whatif/Set` `kitchen` at night: `whatif/Cake` with a forest of ~120 unlit candles, one candle in front; scrubber end tick `?` with candle icon; HUD line `YOUR ODDS OF BEING THE LAST: 1 IN 8,000,000,000`; amber light falls off at the edges (`grade` vignette 0.45).",
      camera=cam("pushIn", 0.6), cam_txt="slow `pushIn` toward the front candle", sfx=[("riser", 0.5, 0.6)], sfx_txt="`riser` into the title card",
      bg=setbg("kitchen", light="night"), hud="y0hook", hud_extra={"odds": "1 IN 8,000,000,000"}, scrub=dict(dot=0), grade={"vignette": 0.45},
      layers=lambda: [comp("whatif/Cake", {"candles": 120, "lit": 0, "front": 1}, x="50%", y="60%", width=900, height=620)]),
 # ---------------- L2
 dict(id="s08-title", at=("TITLE", 0), type="TITLE card (5 s, music only)",
      desc="`explainer/Headline` in Anton, centred on navy: What If Everyone On Earth Was Born On _The Same Day_? (keyword amber); behind it a single amber bar (`whatif/Pyramid`, one band at age 0).",
      camera=cam(), cam_txt="static", sfx=[("impact", 0.0, 0.6)], sfx_txt="music hit on the cut; no VO",
      bg=board(), layers=lambda: [pyramid([{"age": 0, "value": 8000, "kind": "cohort"}], opacity=0.35), comp("explainer/Headline", {"text": "WHAT IF EVERYONE ON EARTH WAS BORN ON THE SAME DAY?", "red": ["THE", "SAME", "DAY?"], "size": 78, "at": 0.2}, x="50%", y="46%", width=1600, height=300, depth=0, z=60)]),
 dict(id="s09-rules", at=("r1", 0), type="BOARD",
      desc="`explainer/Tag` `NO CLONES` then `NO TIME MACHINE`, each crossed by an animated red strike-through `rect` (no clone-vat or time-machine drawings); then `SAME PLANET · SAME CITIES`.",
      camera=cam("drift"), cam_txt="`drift`", sfx=[("click", 0.9, 0.7), ("click", 1.9, 0.7)], sfx_txt="`click` x2 on the strikes",
      bg=board(), layers=lambda: [tag("NO CLONES", 0.6, y="34%"), {"type": "rect", "fill": RED, "x": "50%", "y": "34%", "width": 420, "height": 8, "start": 1.0, "enter": {"type": "wipeRight", "duration": 0.25}, "depth": 0, "z": 75},
                                  tag("NO TIME MACHINE", 1.5, y="48%"), {"type": "rect", "fill": RED, "x": "50%", "y": "48%", "width": 560, "height": 8, "start": 1.9, "enter": {"type": "wipeRight", "duration": 0.25}, "depth": 0, "z": 75},
                                  tag("SAME PLANET · SAME CITIES", 2.6, y="64%")]),
 dict(id="s10-pyramid-collapse", at=("r2", 0), type="BOARD signature shot (GATE SHOT, part 1)",
      desc="`whatif/Pyramid` starts as the real 2024 world pyramid (21 bands, male left / female right, data in storyboard), then `morph` over 3 s: every band drains sideways into one amber bar at age 0. Fixed x-scale: 0.7 BN = 40% of half-width; the 8 BN bar (x12) clips at the board edge with an overflow chevron and a `×12` label; camera eases out (zoom 1 -> 0.85) as the bar lands.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 2.0, "zoom": 1}, {"t": 4.0, "zoom": 0.85}]), cam_txt="hold, then keyframed ease-out zoom 1 -> 0.85",
      sfx=[("whoosh_long", 0.5, 0.7), ("underwater_rumble", 0.6, 0.4)], sfx_txt="`whoosh_long` + `underwater_rumble` as the drain",
      bg=board(), layers=lambda: [pyramid([{"age": a, "value": v, "male": m, "kind": "world2024"} for a, v, m in WPP2024], morphTo=[{"age": 0, "value": 8000, "kind": "cohort"}], morphAt=0.6, morphDur=3.0, source="UN WPP 2024")]),
 dict(id="s11-old-world", at=("r3", 0), type="BOARD (GATE SHOT, part 2)",
      desc="Pyramid adds grey bands at ages 20-45 labelled `THE OLD WORLD · 2,000,000,000 ON LOAN`; `whatif/IconRows` `1 ADULT : 4 BABIES` inset bottom-right; `whatif/Pill` source `infant-care ratio guidance`.",
      camera=cam(), cam_txt="static", sfx=[("pop", 1.0, 0.6), ("pop", 2.4, 0.5)], sfx_txt="`pop` on bands and inset",
      bg=board(), layers=lambda: [pyramid([{"age": 0, "value": 8000, "kind": "cohort"}] + [{"age": a, "value": 400, "kind": "old"} for a in (20, 25, 30, 35, 40)], label={"kind": "old", "text": "THE OLD WORLD · 2,000,000,000 ON LOAN"}),
                                  comp("whatif/IconRows", {"rows": [{"label": "1 ADULT : 4 BABIES", "a": 1, "b": 4}], "at": 2.2}, x=1560, y=760, width=520, height=160, depth=0, z=60), pill("1 ADULT : 4 BABIES", "infant-care ratio guidance (AAP/APHA)", at=2.2)]),
 dict(id="s12-keep-date", at=("r4", 1.6), type="BOARD detail",
      desc="`whatif/Scrubber` returns with a new tick at 30 (key icon); chip `HANDOVER IN 30 YEARS`; on r5 a red pin drops onto the grey bands; `explainer/Tag` `KEEP THIS DATE`.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 2.5, "zoom": 1.15, "x": "50%", "y": "40%"}]), cam_txt="keyframed zoom 1 -> 1.15 on the pin",
      sfx=[("tick", 0.2, 0.6), ("ding", "r5", 0.7)], sfx_txt="`tick` on the new tick; `ding` on the pin",
      bg=board(), scrub=dict(dot=0, show=("DAY 1", "6", "30", "65", "?")),
      layers=lambda: [pyramid([{"age": 0, "value": 8000, "kind": "cohort"}] + [{"age": a, "value": 400, "kind": "old"} for a in (20, 25, 30, 35, 40)], pin={"age": 30, "at": "r5"}),
                      comp("explainer/Tag", {"text": "HANDOVER IN 30 YEARS", "at": 0.3}, x=1480, y=880, width=600, height=80, depth=0, z=70), tag("KEEP THIS DATE", at="r5", y="20%")]),
 dict(id="s13-happy-birthday", at=("r6", 0), type="STORY wide",
      desc="Back to the crib field; paper bunting and one balloon per front-row crib pop up; HUD switches to `TOTAL ALIVE 10,000,000,000` / `YOUR AGE GROUP 8,000,000,000`; the scrubber dot starts moving.",
      camera=cam("pullOut", 0.1), cam_txt="`pullOut` 0.1", sfx=[("pop", 0.2, 0.6), ("pop", 0.5, 0.5), ("pop", 0.8, 0.5)], sfx_txt="`pop` cascade; music returns full",
      bg=setbg("ward", light="day", bunting=True), hud="y0", scrub=dict(dot=0),
      layers=lambda: [crowd("baby", 480, fill=1.0, balloons=True, you_index=7)]),
 # ---------------- L3
 dict(id="s14-stamp-day1", at=("d1", 0), type="STAMP",
      desc="`whatif/YearStamp` full width `DAY 1` / `EIGHT BILLION BIRTHDAYS` (Anton).", camera=cam(), cam_txt="flip-in (`whip` up)",
      sfx=[("whoosh", 0.0, 0.7)], sfx_txt="`whoosh`", trans={"type": "whip", "duration": 0.4, "direction": "up"},
      bg=board(), hud="d1", layers=lambda: [stamp("DAY 1", "EIGHT BILLION BIRTHDAYS")], min=1.8),
 dict(id="s15-births-bars", at=("d2", 1.0), type="BOARD",
      desc="`explainer/SpeedBars`: `NORMAL DAY ~360,000` (thin) vs `TODAY 8,000,000,000` (runs off the right edge); `whatif/Pill` `~60 YEARS OF BIRTHS`.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 5.5, "zoom": 0.7}]), cam_txt="keyframed pull out to fit the long bar",
      sfx=[("tick", 0.8, 0.6), ("whoosh_long", "d3", 0.7)], sfx_txt="`tick` on bar 1; `whoosh_long` as bar 2 overflows",
      bg=board(), hud="d1", scrub=dict(dot=0),
      layers=lambda: [bars([{"label": "NORMAL DAY", "value": 360000, "text": "~360,000"}, {"label": "TODAY", "value": 8e9, "text": "8,000,000,000", "color": AMBER}], max=4e8), pill("~60 YEARS OF BIRTHS", "UN WPP 2024 (EST.)", at="d3")]),
 dict(id="s16-one-adult", at=("d4", 0), type="STORY close-up (one-person rung)",
      desc="`whatif/Set` `ward` at night, close: one grey adult `whatif/Person` (pose hold) between four cribs, the YOU baby in one; a wall `explainer/Timer` (ring) spinning fast; the `DAY 1` bottle tick lights (promise 1 paid). On d5: `explainer/Stat` `40 FEEDS + 40 DIAPERS` / `PER ADULT, PER DAY (EST.)` and a pile of instanced diaper icons grows beside the adult, with `explainer/Bus` for scale.",
      camera=cam("pushIn", 0.4), cam_txt="`pushIn` 0.4", sfx=[("ding", 0.0, 0.6), ("clock_ticking", 0.4, 0.4), ("pop", "d5", 0.6)], sfx_txt="`ding` on the tick; `clock_ticking`; `pop` per diaper",
      bg=setbg("ward", light="night"), hud="d1", scrub=dict(dot=0, lit=("DAY 1",)),
      layers=lambda: [person("adult", "hold", GREY, x="44%", y="66%", h=380), crowd("baby", 4, rows=1, you_index=1, x="58%", y="80%", w=520, h=160),
                      comp("explainer/Timer", {"from": 0, "to": 86400, "rate": 3600, "style": "ring", "format": "mm:ss"}, x=1600, y=320, width=220, height=220),
                      stat(40, "FEEDS + 40 DIAPERS / ADULT / DAY (EST.)", at="d5", x="50%", y="30%"),
                      comp("whatif/IconPile", {"icon": "diaper", "count": 80, "at": "d5"}, x=380, y=820, width=300, height=300), comp("explainer/Bus", {}, x=150, y=860, width=260, height=120)]),
 dict(id="s17-who-runs-it", at=("d6", 0), type="BOARD consequence chain",
      desc="Three navy panels light in sequence: power station, farm, hospital icons, each with a red `UNSTAFFED?` tag. On d7: `explainer/SpeedBars` `JOBS YESTERDAY ~3.5 BN` vs `ADULTS TODAY 2 BN · ALL ON NIGHT FEEDS`; source ILO.",
      camera=cam("drift"), cam_txt="`drift`", sfx=[("click", 0.3, 0.6), ("click", 1.4, 0.6), ("click", 2.4, 0.6), ("tick", "d7", 0.6)], sfx_txt="`click` per panel; `tick` on the bars",
      bg=board(), hud="d1", scrub=dict(dot=0, lit=("DAY 1",)),
      layers=lambda: [icon("powerStation", "25%", "32%", 200, start=0.2), icon("farm", "50%", "32%", 200, start=1.3), icon("hospital", "75%", "32%", 200, start=2.3),
                      bars([{"label": "JOBS YESTERDAY", "value": 3.5, "text": "~3.5 BN"}, {"label": "ADULTS TODAY", "value": 2.0, "text": "2 BN · ALL ON NIGHT FEEDS", "color": GREY}], at="d7", y="70%"),
                      pill("~3.5 BN PEOPLE EMPLOYED", "ILO WESO 2024", at="d7")]),
 dict(id="s18-be-kind", at=("d8", 0), type="BOARD",
      desc="The three `UNSTAFFED?` tags flip to green ticks; `explainer/Tag` `RULE 2: LIGHTS ON · NOBODY HUNGRY`.",
      camera=cam(), cam_txt="static", sfx=[("ding", 0.7, 0.6)], sfx_txt="`ding`",
      bg=board(), hud="d1", scrub=dict(dot=0, lit=("DAY 1",)),
      layers=lambda: [icon("powerStation", "25%", "32%", 200), icon("farm", "50%", "32%", 200), icon("hospital", "75%", "32%", 200), tag("RULE 2: LIGHTS ON · NOBODY HUNGRY", 0.6, y="62%")]),
 dict(id="s19-no-sleep", at=("d9", 0), type="STORY button",
      desc="The adult from s16 asleep standing up; all four babies wide awake; `explainer/Tag` `SLEEP: 0`.",
      camera=cam("pushIn", 0.2), cam_txt="`pushIn` micro", sfx=[("click", 1.4, 0.6)], sfx_txt="silence beat, then one `click`",
      bg=setbg("ward", light="night"), hud="d1", scrub=dict(dot=0, lit=("DAY 1",)),
      layers=lambda: [person("adult", "stand", GREY, x="44%", y="66%", h=380, idle=[{"type": "sway", "amount": 3, "speed": 0.3}]), crowd("baby", 4, rows=1, you_index=1, x="58%", y="80%", w=520, h=160), tag("SLEEP: 0", 0.6, y="24%")]),
 # ---------------- L4
 dict(id="s20-first-steps", at=("y1a", 0), type="STORY wide, warm",
      desc="`whatif/Set` `park`: a wave of amber toddlers (`whatif/Crowd` age kid, pose walk) take first steps left to right, each holding a grey adult's hand; the YOU toddler mid-frame; corner `whatif/YearStamp` `YEAR 1`; Tag `FIRST STEPS: EVERYONE`.",
      camera=cam("panRight", 0.6), cam_txt="slow `panRight` with the wave", sfx=[("footsteps", 0.6, 0.4)], sfx_txt="soft `footsteps`; music lifts",
      bg=setbg("park"), hud="y1", scrub=dict(dot=1, lit=("DAY 1",)),
      layers=lambda: [stamp("YEAR 1", corner=True), crowd("kid", 60, rows=2, pose="walk", holdAdults=True, you_index=31, y="70%"), tag("FIRST STEPS: EVERYONE", "y1b", y="22%")]),
 dict(id="s21-cakes", at=("y1c", 0), type="STORY gag",
      desc="Split: left, `explainer/Map` at global zoom, every continent highlighted amber, plain amber pins (no cake glyphs); right, `whatif/Set` `kitchen` counter where a receipt `rect` rolls off the bottom of frame: `ORDER: 8,000,000,000 CAKES`.",
      camera=cam("drift"), cam_txt="`drift`", sfx=[("pop", 0.3, 0.5), ("pop", 0.6, 0.5), ("typing", 2.5, 0.5)], sfx_txt="`pop` per pin; `typing` as the receipt prints",
      bg=setbg("kitchen", light="day"), hud="y1", scrub=dict(dot=2, lit=("DAY 1",)),
      layers=lambda: [comp("explainer/Map", {"view": {"lon": 10, "lat": 15, "zoom": 1}, "highlight": CONTINENTS, "pins": [{"lon": -74, "lat": 40.7}, {"lon": 2.3, "lat": 48.9}, {"lon": 77.2, "lat": 28.6}, {"lon": 139.7, "lat": 35.7}, {"lon": 3.4, "lat": 6.5}, {"lon": -46.6, "lat": -23.5}], "at": 0.2}, x="27%", y="50%", width=960, height=1080, depth=0),
                      {"type": "rect", "fill": "#FFFFFF", "x": "74%", "y": "60%", "width": 300, "height": 700, "start": 2.4, "keyframes": [{"t": 2.4, "y": "20%"}, {"t": 5.0, "y": "75%", "ease": "linear"}]},
                      {"type": "text", "text": "ORDER: 8,000,000,000 CAKES", "x": "74%", "y": "40%", "fontSize": 34, "color": "#13213A", "font": "condensed", "start": 2.6, "maxWidth": 280}]),
 dict(id="s22-swings", at=("y1d", 0), type="STORY",
      desc="`whatif/Set` `park` playground: a swing set full of same-size amber toddlers, no older kids anywhere; Tag `OLDEST KID ON THE SWINGS: 1`.",
      camera=cam("drift"), cam_txt="`drift`", sfx=[], sfx_txt="music only",
      bg=setbg("park", props="swings"), hud="y1", scrub=dict(dot=3, lit=("DAY 1",)),
      layers=lambda: [crowd("kid", 12, rows=1, pose="sit", y="66%", w=1200, h=220), tag("OLDEST KID ON THE SWINGS: 1", 0.4, y="22%")]),
 dict(id="s23-until-six", at=("y1e", 0), type="STORY transition",
      desc="The park freezes (all idles stop); the desk tick on `whatif/Scrubber` blinks.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 3.6, "zoom": 1.4, "y": "90%"}]), cam_txt="keyframed push toward the scrubber tick",
      sfx=[("tick", 2.0, 0.6), ("tick", 2.5, 0.6), ("stinger", 2.9, 0.5)], sfx_txt="`tick` x2, low `stinger`",
      bg=setbg("park", props="swings"), hud="y1", scrub=dict(dot=5, lit=("DAY 1",)),
      layers=lambda: [crowd("kid", 12, rows=1, pose="sit", y="66%", w=1200, h=220, frozen=True)]),
 # ---------------- L5
 dict(id="s24-stamp-y6", at=("y6a", 0), type="STAMP", desc="`whatif/YearStamp` `YEAR 6` / `FIRST DAY OF SCHOOL`.",
      camera=cam(), cam_txt="`whip` up", sfx=[("whoosh", 0, 0.7)], sfx_txt="`whoosh`", trans={"type": "whip", "duration": 0.4, "direction": "up"},
      bg=board(), hud="y6", layers=lambda: [stamp("YEAR 6", "FIRST DAY OF SCHOOL")], min=1.8),
 dict(id="s25-queue", at=("y6b", 1.0), type="STORY wide",
      desc="`whatif/Set` `classroom` (door view): a queue of amber kids with backpack icons wraps out of the door and off-frame.",
      camera=cam("panLeft", 0.6), cam_txt="`panLeft` along the queue", sfx=[("ding", 0.2, 0.5), ("ding", 0.45, 0.5), ("ding", 0.7, 0.5)], sfx_txt="school bell = `ding` x3 fast",
      bg=setbg("classroom", view="door"), hud="y6", scrub=dict(dot=6, lit=("DAY 1",)),
      layers=lambda: [crowd("kid", 40, rows=1, backpack=True, y="72%", w=2400, h=260)]),
 dict(id="s26-ninety", at=("y6c", 0), type="STORY interior",
      desc="`whatif/Set` `classroom`: one grey teacher `whatif/Person` (pose point) at the chalkboard facing a 9 x 10 grid of amber kids on the floor; the YOU kid ringed in the back row; `explainer/Stat` `~90` / small grey `TODAY ~23`; the desk tick lights (promise 2 paid).",
      camera=cam("pullOut", 0.4), cam_txt="`pullOut` 0.4 to reveal the whole class", sfx=[("boom", 1.8, 0.4), ("ding", 2.0, 0.5)], sfx_txt="soft `boom` on the 90; `ding` on the tick",
      bg=setbg("classroom", view="interior"), hud="y6", scrub=dict(dot=6, lit=("DAY 1", "6")),
      layers=lambda: [person("adult", "point", GREY, x="18%", y="56%", h=360), crowd("kid", 90, rows=9, pose="sit", you_index=84, x="60%", y="64%", w=1100, h=520), stat(90, "KIDS PER TEACHER", at=1.8, x="22%", y="22%", sub="TODAY ~23")]),
 dict(id="s27-romania-map", at=("y6d", 0), type="BOARD",
      desc="`explainer/Map` flies from global to Romania via `views` (lon 25, lat 46, zoom 5); a pin + pulsing ring at (25, 46) labelled `ROMANIA` (no country polygon); chip `1966`.",
      camera=cam(), cam_txt="map `views` keyframes (no camera zoom preset)", sfx=[("whoosh", 0.4, 0.6)], sfx_txt="`whoosh`",
      bg=board(), hud="y6", scrub=dict(dot=6, lit=("DAY 1", "6")),
      layers=lambda: [mapview([{"t": 0, "lon": 10, "lat": 20, "zoom": 1}, {"t": 2.0, "lon": 25, "lat": 46, "zoom": 5}], pins=[{"lon": 25, "lat": 46, "label": "ROMANIA", "at": 1.6, "ring": True}]), tag("1966", 1.0, x=1600, y=200)]),
 dict(id="s28-romania-bars", at=("y6e", 0.8), type="BOARD",
      desc="Two bars grow side by side: `1966 ~274,000` -> `1967 ~528,000`; source line `INS Romania (verify)`.",
      camera=cam(), cam_txt="static", sfx=[("tick", 0.4, 0.6), ("ding", 2.4, 0.6)], sfx_txt="`tick` + `ding`",
      bg=board(), hud="y6", scrub=dict(dot=6, lit=("DAY 1", "6")),
      layers=lambda: [bars([{"label": "1966", "value": 274, "text": "~274,000"}, {"label": "1967", "value": 528, "text": "~528,000", "color": AMBER}], title="LIVE BIRTHS, ROMANIA"), pill("BIRTHS NEARLY DOUBLED", "INS Romania (verify before render)", at=1.2)]),
 dict(id="s29-romania-gates", at=("y6f", 0), type="BOARD cascade",
      desc="The 1967 bulge as one amber block on a mini Romania pyramid slides upward through three labelled gates `MATERNITY` -> `SCHOOL` -> `UNIVERSITY`, each flashing red as it squeezes through.",
      camera=cam("panUp", 0.6), cam_txt="`panUp` following the block", sfx=[("whoosh", 0.3, 0.5), ("whoosh", 1.9, 0.5), ("whoosh", 3.4, 0.5)], sfx_txt="`whoosh` per gate",
      bg=board(), hud="y6", scrub=dict(dot=6, lit=("DAY 1", "6")),
      layers=lambda: [comp("whatif/GateCascade", {"gates": ["MATERNITY", "SCHOOL", "UNIVERSITY"], "at": 0.3, "step": 1.6}, x="50%", y="50%", width=900, height=900)]),
 dict(id="s30-x22000", at=("y6g", 0), type="BOARD comparison",
      desc="`explainer/SpeedBars` `ROMANIA ×2` (short) vs `YOU ×22,000` (runs off-frame).",
      camera=cam("pullOut", 0.4), cam_txt="`pullOut`", sfx=[("whoosh_long", 1.6, 0.6)], sfx_txt="`whoosh_long`",
      bg=board(), hud="y6", scrub=dict(dot=6, lit=("DAY 1", "6")),
      layers=lambda: [bars([{"label": "ROMANIA", "value": 2, "text": "×2"}, {"label": "YOU", "value": 22000, "text": "×22,000", "color": AMBER}], max=60)]),
 dict(id="s31-orbit-photo", at=("y6h", 0), type="STORY button",
      desc="`whatif/Set` `park` from very high: rows of amber kids filling every field to the horizon (static pattern); a white camera-flash `rect` pulse; Tag `YEAR-GROUP PHOTO: 7,700,000,000`.",
      camera=cam("pullOut", 0.6), cam_txt="`pullOut` 0.6", sfx=[("click", 0.4, 0.8)], sfx_txt="`click` as shutter",
      bg=setbg("park", view="aerial"), hud="y6", scrub=dict(dot=6, lit=("DAY 1", "6")),
      layers=lambda: [crowd("kid", 500, rows=20, y="60%", h=800), {"type": "rect", "fill": "#FFFFFF", "x": "50%", "y": "50%", "width": 1920, "height": 1080, "opacity": 0, "keyframes": [{"t": 0.35, "opacity": 0}, {"t": 0.45, "opacity": 0.9}, {"t": 0.9, "opacity": 0}], "depth": 0, "z": 80}, tag("YEAR-GROUP PHOTO: 7,700,000,000", 0.6, y="22%")]),
 # ---------------- L6
 dict(id="s32-stamp-y18", at=("y18a", 0), type="STAMP", desc="`whatif/YearStamp` `YEAR 18` / `EVERYONE GRADUATES`.",
      camera=cam(), cam_txt="`whip` up", sfx=[("whoosh", 0, 0.7)], sfx_txt="`whoosh`", trans={"type": "whip", "duration": 0.4, "direction": "up"},
      bg=board(), hud="y18", layers=lambda: [stamp("YEAR 18", "EVERYONE GRADUATES")], min=1.8),
 dict(id="s33-graduation", at=("y18b", 1.0), type="STORY wide",
      desc="`whatif/Set` `classroom` (hall): rows of amber teens toss mortarboard icons at the same instant; the YOU teen front-left.",
      camera=cam("pullOut", 0.3), cam_txt="`pullOut` 0.3", sfx=[("pop", 1.2, 0.6), ("pop", 1.35, 0.5), ("pop", 1.5, 0.5)], sfx_txt="`pop` cascade",
      bg=setbg("classroom", view="hall"), hud="y18", scrub=dict(dot=18, lit=("DAY 1", "6")),
      layers=lambda: [crowd("teen", 60, rows=3, you_index=2, tossCaps=1.2, y="68%")]),
 dict(id="s34-chairs", at=("y18c", 0), type="STORY",
      desc="32 chair icons in a row, one lit amber with a mortarboard; 31 amber teens look at it; `whatif/Pill` `~250 M UNIVERSITY PLACES`.",
      camera=cam("panRight", 0.5), cam_txt="`panRight` along the row", sfx=[("pop", 1.0, 0.6)], sfx_txt="`pop` on the lit chair",
      bg=setbg("classroom", view="hall"), hud="y18", scrub=dict(dot=18, lit=("DAY 1", "6")),
      layers=lambda: [comp("whatif/IconRow", {"icon": "chair", "count": 32, "lit": [16], "litIcon": "mortarboard"}, x="50%", y="60%", width=1800, height=200), pill("~250 M UNIVERSITY PLACES · 1 PER 32", "UNESCO UIS", at=0.6)]),
 dict(id="s35-office-queue", at=("y18c", 6.0), type="STORY wide",
      desc="`whatif/Set` `office`: grey old-world `whatif/Person` figures (pose sit) at desks behind glass; an amber queue (the YOU teen near the front) runs out of the door and off-frame as an amber path; `explainer/Stat` `~3.5 BN JOBS` / `8 BN APPLICANTS`.",
      camera=cam("pullOut", 0.4), cam_txt="`pullOut` from the door", sfx=[("footsteps", 0.2, 0.4), ("notify", 1.5, 0.4)], sfx_txt="`footsteps` shuffle; `notify` pings",
      bg=setbg("office"), hud="y18", scrub=dict(dot=18, lit=("DAY 1", "6")),
      layers=lambda: [person("adult", "sit", GREY, x="20%", y="52%", h=260), person("adult", "sit", GREY, x="34%", y="52%", h=260), crowd("teen", 30, rows=1, you_index=1, x="70%", y="74%", w=1100, h=240), stat("~3.5 BN", "JOBS · 8 BN APPLICANTS", at=0.4, y="24%")]),
 dict(id="s36-spain", at=("y18e", 0), type="BOARD",
      desc="`explainer/Map` to Spain via `views` (lon -3.7, lat 40.4, zoom 5) with a pin + ring `SPAIN`; chip `2013`; `whatif/Pill` `SPAIN, UNDER-25 UNEMPLOYMENT ~56%`. On 'planet' the view pulls to global and all six continent keys highlight amber. Shot holds 0.8 s past 'planet'.",
      camera=cam(), cam_txt="map `views` keyframes in, then out to global", sfx=[("whoosh", 0.3, 0.5), ("whoosh_long", "y18f+1.0", 0.6)], sfx_txt="`whoosh`; `whoosh_long` on the flood",
      bg=board(), hud="y18", scrub=dict(dot=18, lit=("DAY 1", "6")),
      layers=lambda: [mapview([{"t": 0, "lon": 10, "lat": 30, "zoom": 1.5}, {"t": 1.6, "lon": -3.7, "lat": 40.4, "zoom": 5}, {"t": "y18f+0.6", "lon": -3.7, "lat": 40.4, "zoom": 5}, {"t": "y18f+1.6", "lon": 10, "lat": 15, "zoom": 1}], pins=[{"lon": -3.7, "lat": 40.4, "label": "SPAIN", "at": 1.4, "ring": True}], highlight={"keys": CONTINENTS, "at": "y18f+1.2"}),
                      tag("2013", 0.8, x=1600, y=200), pill("SPAIN, UNDER-25 UNEMPLOYMENT ~56%", "Eurostat, 2013", at=1.0)]),
 dict(id="s37-dating", at=("y18g", 0), type="STORY button",
      desc="`whatif/Set` `park` bench: two amber 18-year-old `whatif/Person`s (pose sit), identical height; Tag `AGE GAP: 0`.",
      camera=cam(), cam_txt="static", sfx=[("ding", 1.4, 0.6)], sfx_txt="`ding`",
      bg=setbg("park", props="bench"), hud="y18", scrub=dict(dot=18, lit=("DAY 1", "6")),
      layers=lambda: [person("teen", "sit", AMBER, you=True, x="44%", y="66%", h=300), person("teen", "sit", AMBER, x="56%", y="66%", h=300), tag("AGE GAP: 0", 1.4, y="22%")]),
 dict(id="s38-strollers", at=("y18h", 0), type="STORY",
      desc="Same bench, now with a stroller icon beside it; across the park a whole row of strollers pops in at once.",
      camera=cam("pullOut", 0.5), cam_txt="`pullOut` 0.5", sfx=[("pop", 2.4, 0.5), ("pop", 2.55, 0.5), ("pop", 2.7, 0.5)], sfx_txt="`pop` cascade",
      bg=setbg("park", props="bench"), hud="y18", scrub=dict(dot=22, lit=("DAY 1", "6")),
      layers=lambda: [person("adult", "sit", AMBER, you=True, x="44%", y="66%", h=300), person("adult", "sit", AMBER, x="56%", y="66%", h=300), icon("stroller", "64%", "74%", 140), comp("whatif/IconRow", {"icon": "stroller", "count": 14, "at": 2.4, "stagger": 0.05}, x="50%", y="88%", width=1800, height=120)]),
 # ---------------- L6b
 dict(id="s39-echo-bands", at=("e1", 0), type="BOARD",
      desc="Corner `whatif/YearStamp` `YEAR 24` over `whatif/Pyramid`: amber bar at 24, grey bands at 44-69, teal echo bands growing at ages 0-5; `whatif/Pill` `~2.2 CHILDREN PER WOMAN`; HUD `TOTAL ALIVE` counts 9.9 -> 11.8 BN.",
      camera=cam("pullOut", 0.2), cam_txt="`pullOut` 0.2", sfx=[("pop", 1.2, 0.5), ("pop", 2.2, 0.5), ("pop", 3.2, 0.5)], sfx_txt="music returns; `pop` per teal band",
      bg=board(), hud="y24", scrub=dict(dot=24, lit=("DAY 1", "6")),
      layers=lambda: [stamp("YEAR 24", corner=True), pyramid([{"age": 20, "value": 7600, "kind": "cohort"}] + [{"age": a, "value": 360, "kind": "old"} for a in (40, 45, 50, 55, 60, 65)] + [{"age": 0, "value": 2400, "kind": "echo", "growFrom": 0, "growAt": 1.0, "growDur": 4.0}]), pill("~2.2 CHILDREN PER WOMAN", "UN WPP 2024", at=0.6)]),
 dict(id="s40-japan-echo", at=("e3", 0), type="BOARD",
      desc="Tag `THE ECHO`; inset mini Japan pyramid with two bulges, chips `1947-49` and `1971-74`, an arrow from parent bulge to child bulge. (Planted here; paid in the reversal.)",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 3, "zoom": 1.2, "x": "62%"}]), cam_txt="keyframed push to the inset", sfx=[("sonar_ping", 0.4, 0.5), ("sonar_ping", 3.0, 0.4)], sfx_txt="`sonar_ping` x2 (echo)",
      bg=board(), hud="y24", scrub=dict(dot=24, lit=("DAY 1", "6")),
      layers=lambda: [tag("THE ECHO", 0.3, y="18%"), comp("whatif/MiniPyramid", {"country": "japan", "bulges": [{"label": "1947-49"}, {"label": "1971-74"}], "arrow": True, "at": 1.4}, x="62%", y="56%", width=700, height=600)]),
 dict(id="s41-crowded-park", at=("e5", 0), type="STORY wide",
      desc="`whatif/Set` `park`, now crowded with teal toddlers and amber parents (the YOU parent with a teal kid).",
      camera=cam("pullOut", 0.3), cam_txt="`pullOut`", sfx=[], sfx_txt="music swell (no breath murmur)",
      bg=setbg("park"), hud="y24", scrub=dict(dot=26, lit=("DAY 1", "6")),
      layers=lambda: [crowd("adult", 30, rows=2, you_index=4, y="62%", h=400), crowd("kid", 40, color=TEAL, rows=2, y="80%", h=220)]),
 # ---------------- L7
 dict(id="s42-interrupt", at=("m1", -0.8), type="BOARD interrupt",
      desc="Music cuts; the navy board goes dark except the `KEEP THIS DATE` pin from s12 glowing on the grey bands; the key tick `30` flashes; chip `HANDOVER IN 0 YEARS`.",
      camera=cam("pushIn", 0.3), cam_txt="slow `pushIn`", sfx=[("heartbeat_slow", 0.9, 0.8)], sfx_txt="silence, then `heartbeat_slow` once",
      bg=board(), hud="y30a", scrub=dict(dot=30, lit=("DAY 1", "6")), grade={"brightness": 0.6},
      layers=lambda: [pyramid([{"age": 30, "value": 7500, "kind": "cohort"}] + [{"age": a, "value": 340, "kind": "old"} for a in (50, 55, 60, 65, 70)] + [{"age": a, "value": v, "kind": "echo"} for a, v in ((0, 2200), (5, 2100), (10, 1100))], pin={"age": 60, "glow": True}, dim=0.7),
                      comp("explainer/Tag", {"text": "HANDOVER IN 0 YEARS", "at": 0.6}, x=1480, y=880, width=600, height=80, depth=0, z=70)]),
 dict(id="s43-handover", at=("m2", 0), type="BOARD signature shot",
      desc="Corner `whatif/YearStamp` `YEAR 30`; `whatif/Pyramid` at YEAR 30: amber bar at 30, teal echo bands at 0-12 below it, grey bands at 50-75 above. On m3 every grey band lifts off the top together (they step out; nobody dies) and a key icon drops from the grey into the amber bar; HUD `TOTAL ALIVE` 14.7 -> 13.0 BN.",
      camera=cam(), cam_txt="static", sfx=[("whoosh_long", "m3+2.2", 0.6), ("ding", "m3+2.8", 0.5)], sfx_txt="`whoosh_long` as the grey lifts; `ding` on the key",
      bg=board(), hud="y30a", hud_at={"m3+2.2": "y30b"}, scrub=dict(dot=30, lit=("DAY 1", "6", "30")),
      layers=lambda: [stamp("YEAR 30", corner=True), pyramid([{"age": 30, "value": 7500, "kind": "cohort"}] + [{"age": a, "value": 340, "kind": "old", "liftAt": "m3+2.2"} for a in (50, 55, 60, 65, 70)] + [{"age": a, "value": v, "kind": "echo"} for a, v in ((0, 2200), (5, 2100), (10, 1100))]), icon("key", "50%", "30%", 110, start=2.6)]),
 dict(id="s44-oldest-30", at=("m4", 0), type="BOARD",
      desc="Same pyramid, nothing above the amber bar; Tag `OLDEST PERSON ALIVE: 30`.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 3.2, "zoom": 1.25, "y": "30%"}]), cam_txt="keyframed push on the empty space above the bar", sfx=[("static", 0.5, 0.3)], sfx_txt="faint `static`",
      bg=board(), hud="y30b", scrub=dict(dot=30, lit=("DAY 1", "6", "30")),
      layers=lambda: [pyramid([{"age": 30, "value": 7500, "kind": "cohort"}] + [{"age": a, "value": v, "kind": "echo"} for a, v in ((0, 2200), (5, 2100), (10, 1100))]), tag("OLDEST PERSON ALIVE: 30", 1.0, y="20%")]),
 dict(id="s45-empty-desks", at=("m5", 0), type="STORY wide (callback to s35)",
      desc="`whatif/Set` `office` from s35, now with empty desks; the amber queue walks in and sits (YOU at the corner office); Tag `OPEN TODAY: EVERY SENIOR JOB`.",
      camera=cam("panRight", 0.4), cam_txt="`panRight`", sfx=[("footsteps", 0.5, 0.4)], sfx_txt="`footsteps`",
      bg=setbg("office"), hud="y30b", scrub=dict(dot=30, lit=("DAY 1", "6", "30")),
      layers=lambda: [crowd("adult", 20, rows=1, you_index=0, pose="walk", y="70%", w=1400, h=300), tag("OPEN TODAY: EVERY SENIOR JOB", 2.4, y="20%")]),
 dict(id="s46-roles", at=("m6", 0), type="BOARD role panels",
      desc="Four navy panels, each an amber 30-year-old `whatif/Person` with a hat: scrubcap `SURGEON · STILL IN TRAINING`, then wig `JUDGE 30`, cap `PILOT 30`, hardhat `POWER STATION 30` (no cockpit/OR/court sets).",
      camera=cam("drift"), cam_txt="`drift`", sfx=[("click", 0.3, 0.6), ("click", "m7+0.0", 0.6), ("click", "m7+1.0", 0.6), ("click", "m7+2.0", 0.6)], sfx_txt="`click` per panel",
      bg=board(), hud="y30b", scrub=dict(dot=30, lit=("DAY 1", "6", "30")),
      layers=lambda: [person("adult", "stand", AMBER, hat="scrubcap", x="14%", y="56%", h=340, start=0.2), person("adult", "stand", AMBER, hat="wig", x="38%", y="56%", h=340, start="m7+0.0"),
                      person("adult", "stand", AMBER, hat="cap", x="62%", y="56%", h=340, start="m7+1.0"), person("adult", "stand", AMBER, hat="hardhat", x="86%", y="56%", h=340, start="m7+2.0"),
                      tag("SURGEON · STILL IN TRAINING", 0.4, x="14%", y="84%"), tag("JUDGE 30", "m7+0.0", x="38%", y="84%"), tag("PILOT 30", "m7+1.0", x="62%", y="84%"), tag("POWER STATION 30", "m7+2.0", x="86%", y="84%")]),
 dict(id="s47-recipe", at=("m8", 0), type="STORY quiet",
      desc="`whatif/Set` `kitchen`: the amber YOU adult holds an old recipe card in grey handwriting nobody can ask about; a teal kid at the table; an empty chair; Tag `GRANDPARENTS: 0`.",
      camera=cam("drift", 0.6), cam_txt="slow `drift`", sfx=[], sfx_txt="room tone only (music still out)",
      bg=setbg("kitchen", light="day"), hud="y30b", scrub=dict(dot=31, lit=("DAY 1", "6", "30")),
      layers=lambda: [person("adult", "hold", AMBER, you=True, x="38%", y="62%", h=380, props_extra="recipeCard"), person("kid", "sit", TEAL, x="58%", y="70%", h=220), icon("chair", "74%", "70%", 200), tag("GRANDPARENTS: 0", 0.6, y="20%")]),
 # ---------------- L8
 dict(id="s48-stamp-y65", at=("r65a", 0), type="STAMP",
      desc="`whatif/YearStamp` `YEAR 65` / `ONE MONDAY`; the rocking-chair tick on `whatif/Scrubber` lights.",
      camera=cam(), cam_txt="`whip` up", sfx=[("whoosh", 0, 0.7), ("ding", 1.2, 0.6)], sfx_txt="`whoosh`; `ding` on the tick", trans={"type": "whip", "duration": 0.4, "direction": "up"},
      bg=board(), hud="y65", scrub=dict(dot=65, lit=("DAY 1", "6", "30", "65")), layers=lambda: [stamp("YEAR 65", "ONE MONDAY")], min=1.8),
 dict(id="s49-retire", at=("r65b", 0), type="STORY wide",
      desc="`whatif/Set` `office` street side at 9:00: every door opens and amber elders (`whatif/Person` age elder, pose walk, holding a box) walk out at once; YOU among them; `explainer/Stat` `~6.3 BN RETIREES (EST.)`; HUD odds `1 IN 6,300,000,000`.",
      camera=cam("panRight", 0.5), cam_txt="`panRight` along the street", sfx=[("whoosh", 0.3, 0.4), ("footsteps", 0.6, 0.5)], sfx_txt="`whoosh` as doors swing; `footsteps`",
      bg=setbg("office", view="street"), hud="y65", scrub=dict(dot=65, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [crowd("elder", 40, rows=2, pose="hold", carry="box", you_index=6, y="68%", w=2200, h=420), stat("~6.3 BN", "RETIREES (EST.)", at=0.6, y="22%")]),
 dict(id="s50-one-worker", at=("r65c", 0), type="STORY",
      desc="`whatif/Set` `office`: a single teal worker at a desk behind a tower of paperwork (stacked `rect`s).",
      camera=cam("pushIn", 0.3), cam_txt="`pushIn`", sfx=[("typing", 0.4, 0.5)], sfx_txt="`typing`",
      bg=setbg("office"), hud="y65", scrub=dict(dot=65, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [person("adult", "sit", TEAL, x="50%", y="66%", h=300), comp("whatif/IconPile", {"icon": "paper", "count": 40}, x="62%", y="52%", width=200, height=520)]),
 dict(id="s51-ratio", at=("r65d", 0), type="BOARD",
      desc="`whatif/IconRows`: `JAPAN TODAY 1 : 2`, then `YOUR WORLD 3 : 4` stacks beneath; source `Japan Statistics Bureau 2023`.",
      camera=cam(), cam_txt="static", sfx=[("tick", 0.6, 0.6), ("tick", 5.6, 0.6)], sfx_txt="`tick` per row",
      bg=board(), hud="y65", scrub=dict(dot=65, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [comp("whatif/IconRows", {"rows": [{"label": "JAPAN TODAY", "a": 1, "b": 2, "at": 0.6}, {"label": "YOUR WORLD", "a": 3, "b": 4, "at": 5.6}]}, x="50%", y="50%", width=1400, height=520)]),
 dict(id="s52-golf", at=("r65e", 0), type="STORY button",
      desc="`whatif/Set` `park`: a long queue of amber elders with a single flag icon at the far end; Tag `TEE TIMES: SOLD OUT`.",
      camera=cam("panRight", 0.3), cam_txt="`panRight`", sfx=[("ding", 0.5, 0.5)], sfx_txt="`ding`",
      bg=setbg("park"), hud="y65", scrub=dict(dot=66, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [crowd("elder", 30, rows=1, y="72%", w=2000, h=260), icon("flag", "90%", "60%", 160), tag("TEE TIMES: SOLD OUT", 0.4, y="22%")]),
 # ---------------- L8b
 dict(id="s53-porch", at=("r80a", 0), type="STORY dusk",
      desc="`whatif/Set` `porch` at sunset: two amber elders in rocking-chair icons, one is YOU; corner `whatif/YearStamp` `YEAR 80` on r80b; HUD `YOUR AGE GROUP 3,800,000,000`.",
      camera=cam("pullOut", 0.3), cam_txt="slow `pullOut`", sfx=[], sfx_txt="music thins (`documentary_pulse` at 0.12)",
      bg=setbg("porch", light="sunset"), hud="y80", scrub=dict(dot=80, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [stamp("YEAR 80", corner=True), person("elder", "sit", AMBER, you=True, x="42%", y="64%", h=300), person("elder", "sit", AMBER, x="58%", y="64%", h=300)]),
 dict(id="s54-photo", at=("r80c", 0), type="STORY quiet",
      desc="The 90-kid class grid from s26 returns as a framed photo on the porch wall; figures fade out of it to half (`whatif/Crowd` fadeOut 0 -> 0.5); `whatif/Pill` `~4× TODAY'S YEARLY DEATHS (EST.)`.",
      camera=cam("pushIn", 0.5), cam_txt="slow `pushIn` on the photo", sfx=[("heartbeat_slow", 2.0, 0.5)], sfx_txt="`heartbeat_slow` under",
      bg=setbg("porch", light="sunset"), hud="y80", scrub=dict(dot=80, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [{"type": "rect", "fill": CREAM, "stroke": "#5A4632", "strokeWidth": 14, "x": "50%", "y": "46%", "width": 900, "height": 560}, crowd("kid", 90, rows=9, pose="sit", you_index=84, x="50%", y="46%", w=820, h=480, fadeOut=0.5, fadeAt="r80d+1.4", fadeDur=3.0), pill("~4× TODAY'S YEARLY DEATHS (EST.)", "UN WPP 2024 + model", at=0.6)]),
 dict(id="s55-empty-chair", at=("r80e", 0), type="STORY quiet",
      desc="The porch again: the YOU elder alone; the second rocking chair still rocking, empty.",
      camera=cam(), cam_txt="static", sfx=[], sfx_txt="silence",
      bg=setbg("porch", light="dusk"), hud="y80", scrub=dict(dot=80, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [person("elder", "sit", AMBER, you=True, x="42%", y="64%", h=300), icon("rockingChair", "58%", "66%", 260, idle=[{"type": "sway", "amount": 6, "speed": 0.4}])]),
 # ---------------- L8c
 dict(id="s56-echo-echo", at=("rv1", -0.4), type="BOARD signature shot",
      desc="`whatif/Pyramid` YEAR 80: shrinking amber bar at 80, teal echo bands at 35-62, a softer second-echo band below; bands widen and blur (smoothed `bands` track); Tag `ECHO OF THE ECHO`.",
      camera=cam("pullOut", 0.3), cam_txt="`pullOut` 0.3", sfx=[("sonar_ping", 0.6, 0.4), ("sonar_ping", 2.6, 0.3)], sfx_txt="`sonar_ping` soft x2; music returns",
      bg=board(), hud="y80", scrub=dict(dot=80, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [pyramid([{"age": 80, "value": 3800, "kind": "cohort"}] + [{"age": a, "value": v, "kind": "echo"} for a, v in ((35, 900), (40, 1500), (45, 1900), (50, 1700), (55, 1000))] + [{"age": a, "value": v, "kind": "echo2"} for a, v in ((0, 500), (5, 700), (10, 900), (15, 1100), (20, 1200), (25, 1100), (30, 900))], smooth={"at": 1.0, "dur": 4.0}), tag("ECHO OF THE ECHO", "rv2+2.4", y="18%")]),
 dict(id="s57-japan-births", at=("rv3", 0), type="BOARD (plant from s40 paid)",
      desc="Japan births line chart (`svg` path, 1945-2010): chip `1949 · 2.7 M`, chip `1973 · 2.1 M`, then a dotted bump outline `EXPECTED ~2000` with nothing under it; Tag `NEVER CAME`. Source `MHLW vital statistics`.",
      camera=cam("panRight", 0.4), cam_txt="`panRight` along the line", sfx=[("tick", "rv4+0.6", 0.6), ("tick", "rv5+0.6", 0.6), ("knock", "rv6+2.0", 0.5)], sfx_txt="`tick` per chip; `knock` on NEVER CAME",
      bg=board(), hud="y80", scrub=dict(dot=80, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [comp("whatif/LineChart", {"series": "japanBirths", "chips": [{"x": 1949, "text": "1949 · 2.7 M", "at": "rv4+0.6"}, {"x": 1973, "text": "1973 · 2.1 M", "at": "rv5+0.6"}], "ghost": {"x": 2000, "text": "EXPECTED ~2000", "at": "rv6+0.6"}}, x="50%", y="52%", width=1600, height=700), tag("NEVER CAME", "rv6+2.0", x="78%", y="24%"), pill("JAPAN LIVE BIRTHS", "MHLW vital statistics", at=0.3)]),
 dict(id="s58-busiest-day", at=("rv8", 0), type="BOARD",
      desc="`explainer/SpeedBars`: `YOUR BIRTHDAY 8,000,000,000` (off-frame) vs `ECHO'S BUSIEST DAY ~1,500,000 (EST.)` vs `TODAY ~360,000`; Tag `EACH WAVE: LOWER AND WIDER`.",
      camera=cam("pullOut", 0.3), cam_txt="`pullOut`", sfx=[("tick", 0.4, 0.6), ("tick", 3.2, 0.6)], sfx_txt="`tick` per bar",
      bg=board(), hud="y80", scrub=dict(dot=80, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [bars([{"label": "YOUR BIRTHDAY", "value": 8e9, "text": "8,000,000,000", "color": AMBER}, {"label": "ECHO'S BUSIEST DAY", "value": 1.5e6, "text": "~1,500,000 (EST.)", "color": TEAL}, {"label": "TODAY", "value": 3.6e5, "text": "~360,000", "color": CREAM}], max=3e6), tag("EACH WAVE: LOWER AND WIDER", 3.8, y="18%")]),
 dict(id="s59-every-month", at=("rv9", 0), type="BOARD",
      desc="The chart outline morphs toward a pyramid; a thin cream outline of the 2024 pyramid from s10 overlays; inset: a 12-month calendar grid where each month lights with a family figure (`BIRTHDAYS IN YOUR FAMILY: 12 MONTHS`).",
      camera=cam(), cam_txt="static", sfx=[("riser", 0.4, 0.4)], sfx_txt="soft `riser`",
      bg=board(), hud="y80", scrub=dict(dot=82, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [pyramid([{"age": a, "value": v, "male": m, "kind": "world2024", "outline": True} for a, v, m in WPP2024], opacity=0.5), comp("whatif/MonthGrid", {"lit": list(range(12)), "at": 0.6, "stagger": 0.2, "label": "BIRTHDAYS IN YOUR FAMILY: 12 MONTHS"}, x=1560, y=520, width=520, height=420)]),
 # ---------------- L9
 dict(id="s60-century", at=("c1", 0), type="STAMP + BOARD",
      desc="`whatif/YearStamp` `YEAR 100` / `THE CENTURY` (held 1.8 s), then the board: HUD switches to survivors mode; `explainer/Stat` `~40,000,000 AGED 100 (EST.)` with grey `TODAY ~0.72 M`; odds `1 IN 40,000,000`.",
      camera=cam(), cam_txt="`whip` up into the board", sfx=[("whoosh", 0, 0.7), ("ding", 1.9, 0.5)], sfx_txt="`whoosh`; `ding`", trans={"type": "whip", "duration": 0.4, "direction": "up"},
      bg=board(), hud="y100", scrub=dict(dot=100, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [stamp("YEAR 100", "THE CENTURY") | {"end": 1.8}, stat("~40,000,000", "AGED 100 (EST.)", at=1.9, sub="TODAY ~0.72 M")], min=4.0),
 dict(id="s61-coin", at=("c3", 0), type="BOARD",
      desc="A coin icon flips every 1.5 s above a row of 10 elder icons; half grey out each flip; `whatif/Pill` `105+: ~50% EACH YEAR` with source `Barbi et al., Science, 2018`.",
      camera=cam(), cam_txt="static", sfx=[("click", 0.5, 0.6), ("click", 2.0, 0.6), ("click", 3.5, 0.6), ("click", 5.0, 0.6)], sfx_txt="`click` per flip",
      bg=board(), hud="y100", scrub=dict(dot=105, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [icon("coin", "50%", "30%", 160, idle=[{"type": "spin", "speed": 0.66}]), comp("whatif/IconRow", {"icon": "elder", "count": 10, "halveEvery": 1.5, "at": 0.5}, x="50%", y="62%", width=1300, height=220), pill("105+: ~50% EACH YEAR", "Barbi et al., Science, 2018", at="c4+0.4")]),
 dict(id="s62-estimate", at=("c5", 0), type="BOARD",
      desc="A red `ESTIMATE` stamp lands across the HUD; a dice icon tumbles in.",
      camera=cam(shake=[{"at": 1.0, "duration": 0.15, "amplitude": 10}]), cam_txt="`shake` 0.15 s", sfx=[("knock", 1.2, 0.6), ("knock", 1.5, 0.5)], sfx_txt="`knock` (dice clack) x2",
      bg=board(), hud="y100", scrub=dict(dot=105, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [icon("dice", "50%", "50%", 220, start=1.1, enter={"type": "drop", "duration": 0.4}), comp("explainer/Tag", {"text": "ESTIMATE", "at": 1.0, "accent": RED}, x=340, y=250, width=360, height=80, rotate=-6, depth=0, z=95)]),
 dict(id="s63-halving", at=("c6", 0), type="BOARD countdown",
      desc="Corner `whatif/YearStamp` `YEAR 110`; HUD survivors `40,000` -> `20,000` (111) -> `10,000` (112) -> `5,000` (113) -> `~40` (120) on the VO beats while a `whatif/Crowd` elder grid halves each beat; odds line follows (`1 IN 40,000` ... `1 IN 40`).",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": "c7+0.0", "zoom": 1.08}, {"t": "c7+2.6", "zoom": 1.16}, {"t": "c7+3.6", "zoom": 1.24}, {"t": "c8+0.6", "zoom": 1.4}]), cam_txt="keyframed push, one step per halving",
      sfx=[("tick", 0.0, 0.7), ("tick", "c7+0.0", 0.6), ("tick", "c7+2.6", 0.5), ("tick", "c7+3.6", 0.4), ("tick", "c8+0.6", 0.3)], sfx_txt="`tick` per halving, getting quieter",
      bg=board(), hud="y110", scrub=dict(dot=110, lit=("DAY 1", "6", "30", "65")),
      layers=lambda: [stamp("YEAR 110", corner=True), crowd("elder", 320, rows=16, halvings=["c7+0.0", "c7+2.6", "c7+3.6", "c8+0.6"], y="56%", h=700)]),
 dict(id="s64-calment", at=("c9", 0), type="BOARD",
      desc="`whatif/Pill` `RECORD: 122 YEARS, 164 DAYS (1875-1997)` beside a generic cream elder silhouette (no likeness); a `122` marker drops onto the scrubber.",
      camera=cam(keys=[{"t": 0, "x": "45%"}, {"t": 4, "x": "60%"}]), cam_txt="keyframed pan right to the 122 marker", sfx=[("ding", 0.6, 0.6)], sfx_txt="`ding`",
      bg=board(), hud="y120", scrub=dict(dot=120, lit=("DAY 1", "6", "30", "65"), marker={"year": 122.45, "label": "122"}),
      layers=lambda: [person("elder", "stand", CREAM, x="34%", y="58%", h=420), pill("RECORD: 122 YEARS, 164 DAYS (1875-1997)", "Gerontology Research Group", at=0.6)]),
 dict(id="s65-dice", at=("c10", 0), type="BOARD",
      desc="The dice roll again; the scrubber dot creeps past the 122 marker; HUD `~7`.",
      camera=cam("pushIn", 0.3), cam_txt="slow `pushIn`", sfx=[("knock", 0.4, 0.5), ("knock", 0.7, 0.5), ("riser", 1.5, 0.5)], sfx_txt="`knock` x2; `riser`",
      bg=board(), hud="y122", scrub=dict(dot=123, lit=("DAY 1", "6", "30", "65"), marker={"year": 122.45, "label": "122"}),
      layers=lambda: [icon("dice", "50%", "48%", 220, idle=[{"type": "jitter", "amount": 6, "speed": 6}])]),
 dict(id="s66-stamp-125", at=("p1", -0.6), type="STAMP",
      desc="`whatif/YearStamp` `YEAR 125` / `ALIVE: 1`; HUD survivors `1`, odds `1 IN 1`.",
      camera=cam(), cam_txt="`dipBlack` in, stamp fades up", sfx=[("heartbeat_slow", 0.8, 0.7)], sfx_txt="music out; one `heartbeat_slow`", trans={"type": "dipBlack", "duration": 0.8},
      bg=board(), hud="y125", scrub=dict(dot=125, lit=("DAY 1", "6", "30", "65"), marker={"year": 122.45, "label": "122"}), layers=lambda: [stamp("YEAR 125", "ALIVE: 1")], min=1.8),
 dict(id="s67-one-candle", at=("p2", 0), type="STORY close",
      desc="`whatif/Set` `kitchen`, morning: one amber elder at the table wearing the YOU ring with a small `?` (maybe it's you); `whatif/Cake` with one lit candle.",
      camera=cam("pushIn", 0.4), cam_txt="slow `pushIn` on the elder", sfx=[], sfx_txt="room tone; music returns very soft",
      bg=setbg("kitchen", light="morning"), hud="y125", scrub=dict(dot=125, lit=("DAY 1", "6", "30", "65"), marker={"year": 122.45, "label": "122"}),
      layers=lambda: [person("elder", "sit", AMBER, you=True, x="44%", y="62%", h=380, youQuestion=True), comp("whatif/Cake", {"candles": 1, "lit": 1}, x="60%", y="74%", width=300, height=240)]),
 dict(id="s68-family", at=("p5", 0), type="STORY wide (second-stage reveal)",
      desc="Pull out from the elder to reveal the whole table: teal, cream and new-colour `whatif/Person`s of every age (kid to adult), each with a small date tag (`MAR 3`, `JUL 19`, `FEB 29`, `NOV 1` ...).",
      camera=cam(keys=[{"t": 0, "zoom": 1.3, "x": "44%"}, {"t": 2.4, "zoom": 1.0, "x": "50%"}]), cam_txt="keyframed pull out (zoom 1.3 -> 1.0)",
      sfx=[("pop", "p6+1.0", 0.4), ("pop", "p6+1.3", 0.4), ("pop", "p6+1.6", 0.4), ("pop", "p6+1.9", 0.4)], sfx_txt="soft `pop` per date tag",
      bg=setbg("kitchen", light="morning"), hud="y125", scrub=dict(dot=125, lit=("DAY 1", "6", "30", "65"), marker={"year": 122.45, "label": "122"}),
      layers=lambda: [person("elder", "sit", AMBER, you=True, x="44%", y="62%", h=380), comp("whatif/Cake", {"candles": 1, "lit": 1}, x="50%", y="76%", width=260, height=200),
                      person("kid", "stand", TEAL, x="20%", y="66%", h=240), person("adult", "stand", CREAM, x="30%", y="60%", h=360), person("teen", "stand", "#C77DFF", x="62%", y="62%", h=320), person("adult", "stand", TEAL, x="74%", y="60%", h=360), person("baby", "stand", "#7FB2FF", x="84%", y="72%", h=140),
                      comp("whatif/DateTags", {"tags": ["MAR 3", "JUL 19", "FEB 29", "NOV 1", "AUG 8"], "at": "p6+1.0", "stagger": 0.3}, x="50%", y="40%", width=1500, height=200)]),
 dict(id="s69-four-a-second", at=("p7", 0), type="STORY extreme close",
      desc="Corner counter `BIRTHS THIS SECOND: 4` from s01 returns and flicks, through the kitchen window; then the single candle flame; the scrubber candle tick lights; HUD and scrubber fade out together.",
      camera=cam(keys=[{"t": 0, "zoom": 1}, {"t": 5.5, "zoom": 1.8, "x": "50%", "y": "70%"}]), cam_txt="keyframed push to the flame, then hold", sfx=[("pop", 1.4, 0.3), ("pop", 2.4, 0.3), ("breath", 5.2, 0.4)], sfx_txt="soft `pop` x4/s under the counter; a `breath` out, flame stays lit",
      bg=setbg("kitchen", light="morning"), hud="y125", hud_out=5.0, scrub=dict(dot=125, lit=("DAY 1", "6", "30", "65", "?"), marker={"year": 122.45, "label": "122"}),
      layers=lambda: [comp("whatif/Cake", {"candles": 1, "lit": 1}, x="50%", y="76%", width=260, height=200), stat(4, "BIRTHS THIS SECOND", at=1.2, x=1700, y=180)]),
 # ---------------- L10
 dict(id="s70-recap", at=("b1", -0.2), type="STORY bookend + recap",
      desc="`glitch` 0.2 s back to the s01 crib-field framing; the cribs dissolve into a horizontal recap icon timeline: bottle `DAY 1`, desk `YEAR 6`, key `YEAR 30`, rocking chair `YEAR 65`, candle `YEAR 125` (the same icons as the scrubber ticks).",
      camera=cam(keys=[{"t": 0, "x": "50%"}, {"t": 2.0, "x": "50%"}, {"t": 8.5, "x": "62%"}]), cam_txt="locked on the 0:00 composition, then pan right along the icons",
      sfx=[("pop", 2.2, 0.5), ("pop", 3.4, 0.5), ("pop", 4.6, 0.5), ("pop", 5.8, 0.5), ("pop", 7.0, 0.5)], sfx_txt="`pop` per icon", trans={"type": "glitch", "duration": 0.2},
      bg=setbg("ward", light="dawn"),
      layers=lambda: [crowd("baby", 480, fill=0.0, dissolveAt=1.8), comp("whatif/RecapRow", {"items": [{"icon": "bottle", "text": "DAY 1 · 60 YEARS OF BIRTHS"}, {"icon": "desk", "text": "YEAR 6 · 90 PER CLASS"}, {"icon": "key", "text": "YEAR 30 · THE HANDOVER"}, {"icon": "rockingChair", "text": "YEAR 65 · ONE MONDAY"}, {"icon": "candle", "text": "YEAR 125 · ONE CANDLE"}], "at": 2.2, "stagger": 1.2}, x="50%", y="50%", width=2400, height=300)]),
 dict(id="s71-gaps", at=("b3", 0), type="BOARD",
      desc="`whatif/Pyramid` 2024 real shape again; the gaps between bands glow; Tag `THE GAPS`.",
      camera=cam("pushIn", 0.1), cam_txt="`pushIn` 0.1", sfx=[], sfx_txt="music swells gently",
      bg=board(), layers=lambda: [pyramid([{"age": a, "value": v, "male": m, "kind": "world2024"} for a, v, m in WPP2024], glowGaps=True), tag("THE GAPS", 1.6, y="18%")]),
 dict(id="s72-street", at=("b4", 0), type="STORY (three callbacks)",
      desc="`whatif/Set` `park` path, side-on: a toddler holding an adult's hand (callback 1:3x first steps), a teacher with a few kids (callback YEAR 6), an older figure handing a key to a younger one (callback YEAR 30); every figure a different shirt colour.",
      camera=cam("panRight", 0.6), cam_txt="slow `panRight` along the path", sfx=[("footsteps", 0.4, 0.3)], sfx_txt="soft `footsteps`",
      bg=setbg("park", view="path"),
      layers=lambda: [person("kid", "walk", "#7FB2FF", x="14%", y="72%", h=200), person("adult", "hold", CREAM, x="20%", y="64%", h=360), person("adult", "point", TEAL, x="44%", y="64%", h=360), person("kid", "stand", "#C77DFF", x="52%", y="72%", h=200), person("kid", "stand", AMBER, x="58%", y="72%", h=200),
                      person("elder", "hold", GREY, x="78%", y="64%", h=360), person("adult", "stand", "#F28C6B", x="86%", y="64%", h=360), icon("key", "82%", "52%", 80)]),
 dict(id="s73-relay", at=("b6", 0), type="STORY",
      desc="The same figures in one line, `point` poses; a glowing cream `circle` (the baton) travels along a path from elder to adult to teen to child; Tag `IT'S A RELAY`.",
      camera=cam("panLeft", 0.5), cam_txt="`panLeft` following the baton back to the child", sfx=[("whoosh", 1.0, 0.3), ("whoosh", 2.6, 0.3), ("whoosh", 4.2, 0.3)], sfx_txt="soft `whoosh` per hand-off",
      bg=setbg("park", view="path"),
      layers=lambda: [person("elder", "point", GREY, x="80%", y="64%", h=360), person("adult", "point", TEAL, x="60%", y="64%", h=360), person("teen", "point", "#C77DFF", x="40%", y="66%", h=320), person("kid", "point", AMBER, x="20%", y="72%", h=200),
                      {"type": "circle", "fill": "#FFF4C2", "width": 46, "height": 46, "x": "80%", "y": "52%", "shadow": "0 0 24px #FFE08A", "keyframes": [{"t": 0.6, "x": "80%"}, {"t": 2.2, "x": "60%"}, {"t": 3.8, "x": "40%", "y": "55%"}, {"t": 5.4, "x": "20%", "y": "62%"}]},
                      tag("IT'S A RELAY", "b6+2.6", y="18%")]),
 # ---------------- L11
 dict(id="s74-cta", at=("cta1", 0), type="CTA board",
      desc="`explainer/Options` (text-only list, title `PICK ONE`): `THE COHORT · ONE BIRTHDAY WITH 8 BN` / `THE ECHO · EVERY GROWN-UP THE SAME AGE`, staggered in with the VO.",
      camera=cam(), cam_txt="static", sfx=[("pop", 0.6, 0.6), ("pop", "cta2+0.6", 0.6)], sfx_txt="`pop` per item",
      bg=board(), layers=lambda: [comp("explainer/Options", {"title": "PICK ONE", "items": ["THE COHORT · ONE BIRTHDAY WITH 8 BN", "THE ECHO · EVERY GROWN-UP THE SAME AGE"], "at": 0.6, "stagger": 5.6}, x="50%", y="46%", width=1500, height=520)]),
 dict(id="s75-end", at=("END", 0), type="END SCREEN",
      desc="The one-candle kitchen set with `blur` 12 on the background layer (core `grade` has no blur); two end-card placeholder `rect`s.",
      camera=cam(), cam_txt="static", sfx=[], sfx_txt="music out by the end",
      bg=board(), layers=lambda: [comp("whatif/Set", {"name": "kitchen", "light": "morning"}, x="50%", y="50%", width=1920, height=1080, blur=12, depth=0), comp("whatif/Cake", {"candles": 1, "lit": 1}, x="50%", y="76%", width=260, height=200, blur=12, depth=0),
                                  {"type": "rect", "fill": "rgba(0,0,0,0.35)", "stroke": "#FFFFFF", "strokeWidth": 4, "radius": 16, "x": "30%", "y": "48%", "width": 640, "height": 360, "depth": 0}, {"type": "rect", "fill": "rgba(0,0,0,0.35)", "stroke": "#FFFFFF", "strokeWidth": 4, "radius": 16, "x": "70%", "y": "48%", "width": 640, "height": 360, "depth": 0}]),
]

# ------------------------------------------------------------------ resolve shot times


def resolve_anchor(a):
    lid, off = a
    if lid == "TITLE":
        return TITLE_START
    if lid == "END":
        return round(NARRATION_END + 0.6, 2)
    return LINES[lid]["start"] + off


for s in SHOTS:
    s["start"] = round(resolve_anchor(s["at"]), 2)
SHOTS.sort(key=lambda s: s["start"])
for i, s in enumerate(SHOTS):
    s["end"] = SHOTS[i + 1]["start"] if i + 1 < len(SHOTS) else RUNTIME
    s["dur"] = round(s["end"] - s["start"], 2)

problems = []
for s in SHOTS:
    if s["dur"] < s.get("min", 1.5):
        problems.append(f"{s['id']} only {s['dur']} s")
# VO line that must land inside a specific shot (on-screen word sync)
for lid, sid, off in (("y18f", "s36-spain", 1.4), ("m3", "s43-handover", 2.8)):
    sh = next(x for x in SHOTS if x["id"] == sid)
    if not (sh["start"] <= LINES[lid]["start"] + off <= sh["end"]):
        problems.append(f"{lid} sync point outside {sid}")


def scene_rel(val, s):
    """Turn 'lineid+off' strings into scene-local seconds."""
    if isinstance(val, str) and re.match(r"^[a-z0-9]+(\+[\d.]+)?$", val) and val.split("+")[0] in LINES:
        lid, _, off = val.partition("+")
        return round(LINES[lid]["start"] + float(off or 0) - s["start"], 2)
    return val


def fix_times(obj, s):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("t", "at", "start", "end", "fadeAt", "growAt", "liftAt", "morphAt", "fillAt", "dissolveAt", "tossCaps"):
                out[k] = scene_rel(v, s) if not isinstance(v, (dict, list)) else fix_times(v, s)
            elif k == "halvings":
                out[k] = [scene_rel(x, s) for x in v]
            else:
                out[k] = fix_times(v, s)
        return out
    if isinstance(obj, list):
        return [fix_times(x, s) for x in obj]
    return obj

# ------------------------------------------------------------------ storyboard


def build_storyboard():
    scenes = []
    hud_state = None
    for s in SHOTS:
        layers = s["layers"]()
        if s.get("hud"):
            h = hud(s["hud"])
            if s.get("hud_extra"):
                h["props"].update(s["hud_extra"])
            if s.get("hud_at"):
                h["props"]["changes"] = [{"at": k, "state": HUD[v]} for k, v in s["hud_at"].items()]
            if s.get("hud_out") is not None:
                h["exit"] = {"type": "fade", "at": s["hud_out"], "duration": 0.8}
            if "ladder" in h["props"]:
                h["props"]["ladder"] = [dict(x, t=x["t"]) for x in h["props"]["ladder"]]
            layers.append(h)
        if s.get("scrub"):
            sc = scrub(**s["scrub"])
            if s.get("hud_out") is not None:
                sc["exit"] = {"type": "fade", "at": s["hud_out"], "duration": 0.8}
            layers.append(sc)
        scene = {
            "id": s["id"],
            "duration": round(s["dur"], 2),
            "background": s["bg"],
            "layers": layers,
            "camera": s["camera"],
            "transitionIn": s.get("trans", {"type": "cut"}),
            "sfx": [{"cue": c, "at": a, "volume": v} for c, a, v in s["sfx"]],
            "notes": s["type"] + ": " + s["desc"],
        }
        if s.get("grade"):
            scene["grade"] = s["grade"]
        scenes.append(fix_times(scene, s))
    # clamp negative / overflowing scene-local times
    for sc, s in zip(scenes, SHOTS):
        for cue in sc["sfx"]:
            cue["at"] = max(0.0, min(cue["at"], s["dur"] - 0.05))
    words = []
    for lid in order:
        L = LINES[lid]
        toks = L["text"].split()
        weights = [len(w) + 2 for w in toks]
        tot = sum(weights)
        t0 = L["start"]
        for w, wt in zip(toks, weights):
            d = L["dur"] * wt / tot
            words.append({"text": w, "start": round(t0, 3), "end": round(t0 + d * 0.92, 3)})
            t0 += d
    music = [
        {"src": "music/documentary_pulse.m4a", "start": 0, "end": round(LINES["m1"]["start"] - 0.8, 2), "volume": 0.3, "duckTo": 0.1, "fadeOut": 0.4},
        {"src": "music/documentary_pulse.m4a", "start": round(LINES["e1"]["start"] - 60 if False else LINES["r65a"]["start"], 2), "end": round(LINES["r80a"]["start"], 2), "volume": 0.3, "duckTo": 0.1},
        {"src": "music/documentary_pulse.m4a", "start": round(LINES["r80a"]["start"], 2), "end": round(LINES["rv1"]["start"], 2), "volume": 0.12, "duckTo": 0.06},
        {"src": "music/documentary_pulse.m4a", "start": round(LINES["rv1"]["start"], 2), "end": round(LINES["p1"]["start"] - 0.6, 2), "volume": 0.3, "duckTo": 0.1},
        {"src": "music/documentary_pulse.m4a", "start": round(LINES["p2"]["start"], 2), "end": RUNTIME, "volume": 0.16, "duckTo": 0.07, "fadeIn": 2.0, "fadeOut": 2.0},
    ]
    sb = {
        "version": 1,
        "id": "whatif-everyone-born-same-day",
        "title": "What If Everyone On Earth Was Born On The Same Day?",
        "format": "16:9",
        "fps": FPS,
        "theme": {"fontDisplay": "Montserrat", "fontBody": "Montserrat", "fontCondensed": "Anton", "accent": AMBER, "ink": NAVY, "paper": CREAM},
        "scenes": scenes,
        "captions": {
            "enabled": True, "words": words, "maxWords": 4, "maxChars": 26, "gapBreak": 0.3,
            "style": {"font": "display", "weight": 900, "fontSize": 60, "color": "#FFFFFF", "highlight": AMBER, "highlightMode": "content", "strokeWidth": 10, "uppercase": True, "y": 0.82, "backing": 0.0},
        },
        "audio": {"voice": [], "music": music, "sfx": [], "sfxDir": "sfx", "duckOn": "captions"},
        "overlays": {"grain": 0.04, "vignette": 0.15, "fadeIn": 0.3, "fadeOut": 1.2},
    }
    return sb

# ------------------------------------------------------------------ markdown


def vo_markdown():
    out = []
    li = 0
    for label, rate, lines in SECTIONS:
        s0 = LINES[lines[0][0]]["start"]
        e1 = LINES[lines[-1][0]]["end"]
        if label.startswith("L2"):
            out.append(f"\n**[{label}] {mmss(TITLE_START)}-{mmss(e1)}** (TTS {rate} wpm)")
            out.append(f"- {mmss(TITLE_START)} TITLE (music only, {TITLE_CARD:.0f} s): What If Everyone On Earth Was Born On _The Same Day_?")
        else:
            out.append(f"\n**[{label}] {mmss(s0)}-{mmss(e1)}** (TTS {rate} wpm)")
        for lid, text, os_ in lines:
            L = LINES[lid]
            out.append(f"- {mmss(L['start'])} VO: {text}")
            for off, txt in os_:
                out.append(f"- {mmss(L['start'] + off)} ON-SCREEN: {txt}")
    out.append(f"\n**[END SCREEN] {mmss(NARRATION_END + 0.6)}-{mmss(RUNTIME)}**")
    out.append(f"- {mmss(NARRATION_END + 0.6)} two end-screen cards over the blurred one-candle kitchen; music out by {mmss(RUNTIME)}")
    return "\n".join(out)


def shot_markdown():
    rows = ["| # | t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX |", "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(SHOTS, 1):
        rows.append(f"| {i} | {mmss1(s['start'])} | {mmss1(s['end'])} | {s['type']} | {s['desc']} | {s['cam_txt']} | {s['sfx_txt']} |")
    return "\n".join(rows)


def chapter_list():
    stamps = [("DAY 1", "d1"), ("YEAR 1", "y1a"), ("YEAR 6", "y6a"), ("YEAR 18", "y18a"), ("YEAR 24", "e1"), ("YEAR 30", "m2"), ("YEAR 65", "r65a"), ("YEAR 80", "r80b"), ("YEAR 100", "c1"), ("YEAR 110", "c6"), ("YEAR 125", "p1")]
    ts = [LINES[l]["start"] for _, l in stamps]
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    return ", ".join(f"{n} {mmss(LINES[l]['start'])}" for n, l in stamps), round(sorted(gaps)[len(gaps) // 2]), round(max(gaps))


if __name__ == "__main__":
    sb = build_storyboard()
    (HERE / "storyboard.json").write_text(json.dumps(sb, indent=1, ensure_ascii=False) + "\n")
    timing = {"lines": [LINES[i] | {"os": None} for i in order], "shots": [{k: s[k] for k in ("id", "start", "end", "dur")} for s in SHOTS], "metrics": M}
    (HERE / "timing.json").write_text(json.dumps(timing, indent=1) + "\n")
    tmpl = (HERE / "script.template.md").read_text()
    ch, ch_med, ch_max = chapter_list()
    pct = lambda lid: round(100 * LINES[lid]["start"] / RUNTIME)
    repl = {
        "{{VO}}": vo_markdown(), "{{SHOTS}}": shot_markdown(), "{{WORDS}}": str(M["words"]), "{{WPM}}": str(M["wpm_overall"]),
        "{{WPM_SPOKEN}}": str(M["wpm_spoken"]), "{{RUNTIME}}": str(RUNTIME), "{{RUNTIME_MMSS}}": mmss(RUNTIME), "{{NARR_END}}": mmss(NARRATION_END),
        "{{HOOK_WORDS}}": str(M["hook_words"]), "{{HOOK_END}}": mmss(M["hook_end"]), "{{HOOK_END_S}}": str(round(M["hook_end"])), "{{SENT_MEAN}}": str(M["mean_sentence"]),
        "{{PUNCH}}": str(M["punch_pct"]), "{{SECOND}}": str(M["second_person_pct"]), "{{PIVOTS}}": str(M["pivots_per_min"]), "{{QUESTIONS}}": str(M["questions"]),
        "{{NUMS}}": str(M["numbers_per_min"]), "{{YOU30}}": str(M["you_first_30s"]), "{{CHAPTERS}}": ch, "{{CH_MED}}": str(ch_med), "{{CH_MAX}}": str(ch_max),
        "{{TITLE_T}}": mmss(TITLE_START), "{{TITLE_END}}": mmss(TITLE_START + TITLE_CARD), "{{SHOTCOUNT}}": str(len(SHOTS)), "{{SENTS}}": str(M["sentences"]),
    }
    for lid in order:
        repl["{{T:" + lid + "}}"] = mmss(LINES[lid]["start"])
        repl["{{P:" + lid + "}}"] = str(pct(lid))
    for s in SHOTS:
        repl["{{S:" + s["id"] + "}}"] = mmss(s["start"])
        repl["{{SE:" + s["id"] + "}}"] = mmss(s["end"])
    text = tmpl
    for k, v in repl.items():
        text = text.replace(k, v)
    left = re.findall(r"\{\{[^}]+\}\}", text)
    (HERE / "script.md").write_text(text)
    print(json.dumps(M, indent=1))
    print("shots", len(SHOTS), "runtime", RUNTIME, "title", TITLE_START)
    print("problems:", problems or "none")
    print("unresolved placeholders:", left or "none")
