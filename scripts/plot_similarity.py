#!/usr/bin/env python3
"""Plot-similarity gate for the horror track: is our story a retelling of a studied source?

Usage:
  python3 scripts/plot_similarity.py <script.md> <source.md | source_dir> [...] [--json] [-v]

<source.md> is a corpus annotation with a beat table (research/corpus/horror-cn/BV*.md).
A directory checks every annotation file in it. Exit 0 = PASS, 1 = FAIL, 2 = usage error.

originality_check.py catches copied wording. This catches copied plot: the same specific
events in the same order, even when every word and name has been changed.

How it works
- Our events: one per paragraph of the ```narration block (or, with no narration block,
  one per sentence of the prose outside front matter, tables and headings).
- Source events: one per row of the annotation's beat table (Beat column = specifics,
  Mechanic column = genre device). Source twists: the twist-inventory table.
- Each event is reduced to its *specific* terms: content words (light stemming and a
  US/UK synonym map, so "elevator" == "lift"), minus stopwords, minus a lexicon of genre
  mechanics (door, knock, rule, chat, police, neighbour ...), minus any word that shows up in
  the story text of half or more of the annotation files (data-driven "generic").
  Content-word bigrams (e.g. "fingerprint lock") are kept as extra features.
- Two events match when they share >= 2 specific terms, or one specific bigram.
  Sharing a mechanic alone (both have a knock, a fake authority, a count clue) never matches.

FAIL when any of these holds for one source:
  1. chain   >= 3 matched events in the same order, each step within 8 beat-table rows and
             4 of our events of the last one ("3+ consecutive specific events");
  2. twists  >= 3 of the source's twists matched in the same order (the twist chain);
  3. names   a source name or named role (Chen Jie, Uncle Wang, Professor Han ...) plus
             signature clues worth >= 1, or signature clues worth >= 3 on their own. Signature
             clues come from the source's SPECIFIC section: bigrams and words that occur in
             no other annotation's story text (red curtain, fingerprint lock, dinosaur ...);
             a signature bigram is worth 1, a signature word on its own 0.5.
Single overlaps are printed as notes, and so are the shared generic mechanics (allowed).

Limits: the match is lexical. A rewrite that swaps every noun but keeps the source's twist
*types* in the same order will PASS here and is still a retelling; the TRANSPOSE_RULES.md
checklist (research/corpus/horror-cn/) covers that by hand. Run this together with
originality_check.py, not instead of it.
"""
import json
import math
import pathlib
import re
import sys
import unicodedata

CHAIN_MIN = 3        # matched events in order
GAP_SRC = 8          # max source-row step between consecutive chain links (rows are ~10 s)
GAP_OURS = 4         # max our-event step between consecutive chain links
TWIST_MIN = 3        # source twists matched in order
SIG_ALONE = 3        # signature clues that fail without a name
GENERIC_DF = 0.5     # share of annotation files above which a word counts as generic
MIN_SHARED = 2       # specific unigrams two events must share to match

STOP = set("""
a about above after again against all almost alone along already also although always am an and another any anyone
anything are around as at away back be became because become been before being below between both but by can cannot
could did do does doing done down during each either else even ever every everyone everything few for from further
get gets getting give given gives go goes going gone got had has have having he her here hers herself him himself his
how however i if in into is it its itself just keep kept know knows knew last least less let lets like little made
make makes many may me might mine more most much must my myself never next no nobody none nor not nothing now of off
often on once one only onto or other others our ours ourselves out over own per put rather really right same say says
said see seen she should since so some someone something still such take takes than that the their theirs them
themselves then there these they thing things think this those though through thus till to too toward towards under
until up upon us very via was way we well were what whatever when where whether which while who whom whose why will
with within without would yet you your yours yourself yourselves s t ll re ve d m isn wasn don doesn didn won can't
don't it's i'm he's she's that's there's what's let's i've i'll you're we're they're
first second third new old another already ago tonight today tomorrow yesterday now later soon
please okay ok yes yeah oh good sent remove reach treat date forward exactly design claim believe enter
visible aside twice slowly suddenly finally maybe really even
""".split())

# Genre mechanics and stage vocabulary: shared by the whole niche, never evidence of copying.
GENERIC = set("""
door knock knocking doorbell peephole handle lock locked unlock open opens opened shut close closed
rule taboo warning warn note list law order instruction
phone call called caller calling text message chat group dm post posted reply answer screen app ring ringing
night midnight hour minute second clock time timer countdown day week
police authority admin management manager staff official expert helper guide mentor
neighbour roommate friend father mother parent son daughter brother sister family child baby boy girl man woman
people person stranger visitor guest someone everyone resident member
dead death die dying kill killer killed body corpse blood murder victim alive live life
monster ghost thing creature entity voice sound noise scream shout whisper silence quiet
see look looks watch hear listen saw heard feel felt
run hide hiding escape flee chase trap safe danger threat attack
hero narrator protagonist viewer reader audience character cast villain ally enemy suspect culprit
beat twist reveal reversal clue count proof evidence test check question plan deduction logic
real fake lie lies liar lying truth trust true false wrong right
help rescue save saved
home house room flat building floor hall corridor outside inside window wall stair
tell tells told ask asks asked says say saying think thought realise realize know wait
come comes came leave leaves left stay stays go goes went return returns back
start end ending begin final last next
grandfather grandmother husband wife uncle aunt cousin coworker colleague boss landlord tenant
supernatural survival survive survivor horror scare scary creepy unit press button hook
""".split())

# Annotation meta-vocabulary (how the studies talk about a story, not story content).
META = set("""
distinctive avoid echo exact combination generic mechanic mechanics transposition transpose transposed reuse retell
chain premise line lines quote quoted name named role roles specific author expression frame different device
token motif payoff plant planted setup type pattern template studio channel episode viewer danmaku caption
english chinese translation phrase phrasing wording
""".split())

SYN = {
    "elevator": "lift", "apartment": "flat", "neighbor": "neighbour", "neighbors": "neighbour",
    "mom": "mother", "mum": "mother", "mommy": "mother", "dad": "father", "daddy": "father",
    "cop": "police", "cops": "police", "officer": "police", "policeman": "police",
    "cellphone": "phone", "mobile": "phone", "sms": "text", "texts": "text", "texted": "text",
    "closet": "wardrobe", "couch": "sofa", "hallway": "corridor", "grandpa": "grandfather",
    "granddad": "grandfather", "grandma": "grandmother", "granny": "grandmother", "kid": "child",
    "kids": "child", "dorm": "dormitory", "dorms": "dormitory", "colour": "color",
    "favour": "favor", "realise": "realize", "realised": "realize", "trashcan": "bin",
    "garbage": "bin", "trash": "bin", "dumpster": "bin", "truck": "lorry", "trucker": "lorry",
    "spat": "spit", "dumplings": "dumpling",
    # irregular verbs, so "ate" == "eats"
    "ate": "eat", "eaten": "eat", "grew": "grow", "grown": "grow", "ran": "run", "hid": "hide",
    "hidden": "hide", "bit": "bite", "bitten": "bite", "fell": "fall", "fallen": "fall", "woke": "wake",
    "woken": "wake", "froze": "freeze", "frozen": "freeze", "stole": "steal", "stolen": "steal",
    "broke": "break", "broken": "break", "threw": "throw", "thrown": "throw", "drove": "drive",
    "driven": "drive", "rode": "ride", "swam": "swim", "dug": "dig", "buried": "bury", "burnt": "burn",
    "burned": "burn", "caught": "catch", "brought": "bring", "bought": "buy", "taught": "teach",
    "fought": "fight", "sang": "sing", "rang": "ring", "rung": "ring", "lit": "light", "slept": "sleep",
    "spoke": "speak", "spoken": "speak", "wrote": "write", "written": "write", "hung": "hang",
}
NUM = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}

# Capitalised words that are never names here.
NOT_NAMES = set("""
Bilibili TikTok YouTube Douyin WeChat English Chinese Spark Part Shorts Remotion CCTV DNA OK THE END GENERIC SPECIFIC
Mist Chenjie Internal Names Do Don't Never Keep Avoid Distinctive Exact Premise Setting Act Rule Rules Loop Twist
Source Code Reset Freud Notes Transposition Safe Takeaways Template How Specific Generic Note Lord Zone Project
""".split())

ROLE_WORDS = set("""
aunt uncle grandpa grandma grandfather grandmother sister brother officer professor doctor director
city university year mister miss lord lady
""".split())

CJK = re.compile(r"[　-鿿＀-￯]+")
BRACKETS = re.compile(r"\[[^\]\n]{0,60}\]")


def norm(text):
    text = unicodedata.normalize("NFKC", text)
    return text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')


def stem(w):
    w = SYN.get(w, w)
    w = NUM.get(w, w)
    if w.isdigit() or any(c.isdigit() for c in w):
        return w
    if w.endswith("'s"):
        w = w[:-2]
    for suf, keep in (("ies", "y"), ("sses", "ss"), ("ing", ""), ("ed", ""), ("es", ""), ("s", "")):
        if w.endswith(suf) and len(w) - len(suf) >= 3 and not (suf == "s" and w.endswith("ss")):
            w = w[: len(w) - len(suf)] + keep
            break
    return SYN.get(w, w)


GENERIC |= {stem(w) for w in GENERIC}
META |= {stem(w) for w in META}


def tokens(text):
    text = CJK.sub(" ", BRACKETS.sub(" ", norm(text)))
    raw = re.findall(r"[a-z0-9][a-z0-9']*[a-z0-9]|[a-z0-9]", text.lower())
    return [stem(w) for w in raw if w not in STOP]


def content(toks):
    return [t for t in toks if t not in STOP and len(t) > 1]


class Vocab:
    """Corpus-level generic filter: words common to many annotation files are generic."""

    def __init__(self, story_texts):
        self.n = max(1, len(story_texts))
        self.df, self.bdf = {}, {}
        for text in story_texts:
            toks = content(tokens(text))
            for t in set(toks):
                self.df[t] = self.df.get(t, 0) + 1
            for b in set(zip(toks, toks[1:])):
                self.bdf[b] = self.bdf.get(b, 0) + 1

    def generic(self, t):
        if t in GENERIC or t in META or (t.isdigit() and len(t) < 2):
            return True
        return self.n >= 4 and self.df.get(t, 0) / self.n >= GENERIC_DF

    def features(self, text):
        toks = content(tokens(text))
        uni = {t for t in toks if not self.generic(t)}
        bi = set()
        for a, b in zip(toks, toks[1:]):
            if (a in uni or b in uni) and self.bdf.get((a, b), 0) <= 1 and a != b:
                bi.add((a, b))
        return uni, bi


def match(fa, fb):
    """Shared specific evidence between two events, or None."""
    shared_u = fa[0] & fb[0]
    shared_b = fa[1] & fb[1]
    if len(shared_u) >= MIN_SHARED or shared_b:
        return sorted(shared_u) + [" ".join(b) for b in sorted(shared_b)]
    return None


# --- parsing -----------------------------------------------------------------

def split_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells


def tables(text):
    """Yield (header_cells, rows) for every markdown table."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].lstrip().startswith("|") and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            head = split_row(lines[i])
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            yield head, rows
            i = j
        else:
            i += 1


def col(head, *names):
    for n in names:
        for k, h in enumerate(head):
            if re.sub(r"[*_]", "", h).strip().lower().startswith(n):
                return k
    return None


def strip_md(s):
    return re.sub(r"[*_`]", "", s)


def section(text, start_pat, stop_pat):
    out, on = [], False
    for line in text.splitlines():
        if not on and re.search(start_pat, line, re.I):
            on = True
            continue
        if on and re.search(stop_pat, line, re.I):
            break
        if on:
            out.append(line)
    return "\n".join(out)


class Source:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.text = norm(self.path.read_text(errors="ignore"))
        self.beats, self.twists = [], []
        for head, rows in tables(self.text):
            b, m = col(head, "beat"), col(head, "mechanic", "device")
            t, ty = col(head, "twist"), col(head, "type")
            tm = col(head, "time", "t", "story clock")
            if b is not None and m is not None and not self.beats:
                for r in rows:
                    if len(r) > max(b, m):
                        self.beats.append({"time": strip_md(r[tm]) if tm is not None and tm < len(r) else "",
                                           "text": strip_md(r[b]), "mech": strip_md(r[m])})
            elif t is not None and ty is not None and not self.twists:
                for r in rows:
                    if len(r) > max(t, ty):
                        self.twists.append({"n": strip_md(r[0]), "text": strip_md(r[t]), "mech": strip_md(r[ty])})
        self.specific = section(self.text, r"^\s*(\*\*|#+\s*)specific\b",
                                r"^\s*(## |\*\*(transposition|safe transposition|takeaways|template|how to transpose)|---)")
        self.generic_text = section(self.text, r"^\s*(\*\*|#+\s*)generic\b", r"^\s*(\*\*|#+\s*)specific\b|^## ")

    def ok(self):
        return bool(self.beats)

    def story_text(self):
        return " ".join(e["text"] for e in self.beats + self.twists)

    def names(self):
        """Proper names in the SPECIFIC section: capitalised words that the file never writes in
        lower case and that occur mid-sentence at least once (so not just sentence-initial words)."""
        lower_seen = set(re.findall(r"\b[a-z][a-z'-]+\b", self.text))

        def namey(w):
            return (w not in NOT_NAMES and w.lower() not in lower_seen and w.lower() not in STOP
                    and re.search(r"[a-z0-9,;:)] +" + re.escape(w) + r"\b", self.text) is not None)

        found = set()
        for m in re.finditer(r"\b[A-Z][a-z]+(?:[ -][A-Z][a-z]+){0,2}\b", self.specific):
            words = re.split(r"[ -]", m.group(0))
            core = [w for w in words if namey(w)]
            if not core:
                continue
            if len(words) > 1:
                found.add(" ".join(words).lower())
            for w in core:
                if len(w) >= 4 and w.lower() not in ROLE_WORDS:
                    found.add(w.lower())
        return found

    def signatures(self, vocab, others):
        """Signature clues: SPECIFIC-section terms that no other annotation's story text uses."""
        spec_toks = content(tokens(self.specific))
        gen_toks = content(tokens(self.generic_text))
        gen, gen_bi = set(gen_toks), set(zip(gen_toks, gen_toks[1:]))
        story = set(content(tokens(self.story_text())))
        other_u, other_b = set(), set()
        for o in others:
            ot = content(tokens(o))
            other_u |= set(ot)
            other_b |= set(zip(ot, ot[1:]))
        name_toks = {w for n in self.names() for w in n.split()}
        uni = {t for t in spec_toks
               if not vocab.generic(t) and t not in gen and t not in other_u and t in story and len(t) >= 4
               and t not in name_toks}
        bi = {(a, b) for a, b in zip(spec_toks, spec_toks[1:])
              if a != b and (a, b) not in other_b and not (vocab.generic(a) and vocab.generic(b))
              and a in story and b in story and a not in META and b not in META
              and (a in uni or b in uni or not (vocab.generic(a) or vocab.generic(b)))
              and (a, b) not in gen_bi}
        return uni, bi


def our_events(path):
    text = norm(pathlib.Path(path).read_text(errors="ignore"))
    m = re.search(r"```narration\s*\n(.*?)```", text, re.S)
    if m:
        paras = [p.strip() for p in re.split(r"\n\s*\n", m.group(1)) if p.strip()]
        return [BRACKETS.sub(" ", p).strip() for p in paras if BRACKETS.sub(" ", p).strip()]
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    keep = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("|", "#", "```")) or s.lower().startswith(("ref", "- id:", "references")):
            continue
        keep.append(s)
    prose = " ".join(keep)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", prose) if len(s.split()) >= 3]


# --- mechanics (reported only; shared mechanics are allowed) -------------------

MECHANICS = [
    ("knock / threshold visitor", r"\bknock|doorbell|peephole|at (?:the|my|our) door"),
    ("rule or warning stated", r"\brules?\b|taboo|\bnever\b|don't|warning|warns?\b"),
    ("count / number clue", r"\bcount|exactly|\bnumber|\b\d+\b"),
    ("fake or compromised authority", r"authority|admin|management|supervisor|director|professor|expert|helper|police|cop\b"),
    ("group chat / DM", r"group chat|\bchat\b|\bdm\b|residents'? group|@"),
    ("phone text / call", r"\btexts?\b|\bsms\b|message|\bcall(?:s|ed)?\b|\bphone"),
    ("isolation / comms cut", r"no signal|jamm|cut off|snow|blocked|tunnel|no one (?:came|answer)"),
    ("ringtone exposes a lie", r"ringtone|phone rang|rings? (?:from|behind|outside|next)"),
    ("loop / reset", r"\bloop|reset|wakes? (?:up )?(?:again|at)"),
    ("frame break (dream, sim, stream)", r"dream|simulat|hypno|illusion|livestream|experiment"),
    ("test human vs not", r"\btest|prove|proof|shibboleth"),
    ("knowledge leak", r"how (?:did|does|do) (?:he|she|you|they) know|knew"),
    ("mimic voice / impostor", r"mimic|imitat|impostor|voice|copy|replaced"),
    ("narrator twist", r"narrator|it was me|i was the|unreliable"),
]


def mechanics(text):
    t = text.lower()
    return {name for name, pat in MECHANICS if re.search(pat, t)}


# --- checks ------------------------------------------------------------------

def longest_chain(pairs):
    """pairs: list of (our_i, src_j, evidence). Longest ordered chain with bounded steps."""
    pairs = sorted(pairs)
    best = [None] * len(pairs)
    for k, (i, j, _) in enumerate(pairs):
        best[k] = [k]
        for p in range(k):
            pi, pj, _ = pairs[p]
            if pi < i and pj < j and i - pi <= GAP_OURS and j - pj <= GAP_SRC:
                if len(best[p]) + 1 > len(best[k]):
                    best[k] = best[p] + [k]
    chain = max(best, key=len) if best else []
    return [pairs[k] for k in chain]


def ordered_chain(pairs):
    """Longest chain increasing in both indices (no gap limit)."""
    pairs = sorted(pairs)
    best = []
    for k, (i, j, _) in enumerate(pairs):
        cur = [k]
        for p in range(k):
            pi, pj, _ = pairs[p]
            if pi < i and pj < j and len(best[p]) + 1 > len(cur):
                cur = best[p] + [k]
        best.append(cur)
    chain = max(best, key=len) if best else []
    return [pairs[k] for k in chain]


def present(phrase_toks, our_toks, our_bigrams):
    if isinstance(phrase_toks, tuple):
        return phrase_toks in our_bigrams
    return phrase_toks in our_toks


def check(events, src, vocab, others):
    ours = [vocab.features(e) for e in events]
    beats = [vocab.features(b["text"]) for b in src.beats]
    twists = [vocab.features(t["text"]) for t in src.twists]

    pairs = []
    for i, fa in enumerate(ours):
        for j, fb in enumerate(beats):
            ev = match(fa, fb)
            if ev:
                pairs.append((i, j, ev))
    chain = longest_chain(pairs)

    tpairs = []
    for i, fa in enumerate(ours):
        for j, fb in enumerate(twists):
            ev = match(fa, fb)
            if ev:
                tpairs.append((i, j, ev))
    tchain = ordered_chain(tpairs)

    all_text = " ".join(events)
    raw_lower = all_text.lower()
    our_toks = set(content(tokens(all_text)))
    tl = content(tokens(all_text))
    our_bi = set(zip(tl, tl[1:]))
    names = sorted(n for n in src.names()
                   if re.search(r"(?<![a-z])" + re.escape(n) + r"(?![a-z])", raw_lower))
    sig_u, sig_b = src.signatures(vocab, others)
    hit_b = sorted(b for b in sig_b if b in our_bi)
    covered = {w for b in hit_b for w in b}
    hit_u = sorted(u for u in sig_u if u in our_toks and u not in covered)
    clues = [" ".join(b) for b in hit_b] + hit_u

    # A signature bigram is a full clue; a signature word on its own is half of one.
    clue_score = len(hit_b) + 0.5 * len(hit_u)
    reasons = []
    if len(chain) >= CHAIN_MIN:
        reasons.append(f"{len(chain)} specific events in the source's order")
    if len(tchain) >= TWIST_MIN:
        reasons.append(f"{len(tchain)} of the source's twists in order")
    if names and clue_score >= 1:
        reasons.append("source name(s) plus signature clue(s)")
    elif clue_score >= SIG_ALONE:
        reasons.append(f"signature clues from the source's SPECIFIC list (score {clue_score:g} >= {SIG_ALONE})")

    return {
        "source": str(src.path),
        "verdict": "FAIL" if reasons else "PASS",
        "reasons": reasons,
        "chain": [{"ours": i + 1, "our_text": short(events[i]), "src_time": src.beats[j]["time"],
                   "src_beat": short(src.beats[j]["text"]), "shared": ev} for i, j, ev in chain],
        "twists": [{"ours": i + 1, "our_text": short(events[i]), "src_twist": src.twists[j]["n"],
                    "src_text": short(src.twists[j]["text"]), "shared": ev} for i, j, ev in tchain],
        "matched_events": len({i for i, _, _ in pairs}),
        "names": names,
        "clues": clues,
        "generic_mechanics_shared": sorted(mechanics(all_text) & mechanics(
            " ".join(b["mech"] + " " + b["text"] for b in src.beats))),
    }


def short(s, n=90):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def collect_sources(args):
    out = []
    for a in args:
        p = pathlib.Path(a)
        if p.is_dir():
            out += sorted(q for q in p.glob("*.md"))
        elif p.is_file():
            out.append(p)
        else:
            raise SystemExit(f"no such source: {a}")
    return out


def corpus_for(paths):
    """Annotation files used for the generic filter: every beat-table file next to each source."""
    dirs = {p.resolve().parent for p in paths}
    files = set()
    for d in dirs:
        files |= {q.resolve() for q in d.glob("*.md")}
    files |= {p.resolve() for p in paths}
    srcs = [Source(f) for f in sorted(files)]
    return [s for s in srcs if s.ok()]


def report(res, verbose):
    lines = [f"{res['verdict']}  {res['source']}"]
    for r in res["reasons"]:
        lines.append(f"  reason: {r}")
    if res["chain"] and (res["verdict"] == "FAIL" or verbose):
        lines.append(f"  event chain ({len(res['chain'])}):")
        for c in res["chain"]:
            lines.append(f"    ours #{c['ours']} ~ src {c['src_time']}  shared: {', '.join(c['shared'])}")
            lines.append(f"      ours: {c['our_text']}")
            lines.append(f"      src:  {c['src_beat']}")
    if res["twists"] and (res["verdict"] == "FAIL" or verbose):
        lines.append(f"  twist chain ({len(res['twists'])}):")
        for c in res["twists"]:
            lines.append(f"    ours #{c['ours']} ~ twist {c['src_twist']}  shared: {', '.join(c['shared'])}")
            lines.append(f"      src:  {c['src_text']}")
    if res["names"]:
        lines.append(f"  names/roles from source: {', '.join(res['names'])}")
    if res["clues"]:
        lines.append(f"  signature clues from source: {', '.join(res['clues'])}")
    if verbose or res["verdict"] == "FAIL":
        lines.append(f"  generic mechanics shared (allowed): {', '.join(res['generic_mechanics_shared']) or 'none'}")
    return "\n".join(lines)


def main(argv):
    flags = {a for a in argv if a.startswith("-")}
    args = [a for a in argv if not a.startswith("-")]
    if len(args) < 2 or "-h" in flags or "--help" in flags:
        print(__doc__)
        return 2
    script, src_args = args[0], args[1:]
    events = our_events(script)
    if not events:
        print("FAIL: no narration or prose events found in", script)
        return 1
    paths = collect_sources(src_args)
    corpus = corpus_for(paths)
    by_path = {s.path.resolve(): s for s in corpus}
    vocab = Vocab([s.story_text() for s in corpus])
    results = []
    for p in paths:
        src = by_path.get(p.resolve())
        if src is None:
            continue  # not an annotation (no beat table), e.g. SOURCES.md
        others = [s.story_text() for s in corpus if s is not src]
        results.append(check(events, src, vocab, others))
    if not results:
        print("ERROR: no source annotation with a beat table among", " ".join(src_args))
        return 2
    verdict = "FAIL" if any(r["verdict"] == "FAIL" for r in results) else "PASS"
    if "--json" in flags:
        print(json.dumps({"verdict": verdict, "events": len(events), "results": results}, ensure_ascii=False, indent=1))
    else:
        verbose = "-v" in flags or "--verbose" in flags
        for r in results:
            if r["verdict"] == "FAIL" or verbose or len(results) == 1:
                print(report(r, verbose))
        print(verdict)
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
