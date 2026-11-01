#!/usr/bin/env python3
"""Build episodes/<slug>/storyboard.json from episodes/<slug>/script.md (+ audio/captions.json timings).

usage: python3 -m pipeline.episodes.build [slug ...]      (no args = every episode with a builder)

Timing comes from episodes/<slug>/audio/captions.json (pipeline.audio.make --meta-out episodes/<slug>/audio).
Without it, a words-per-minute estimate is used and the storyboard says so in "_built.timing".
"""
from __future__ import annotations

import json
import os
import sys

from . import explainer_eps, horror_eps
from .common import ROOT, load, norm, storyboard, visual_events

MAX_HOLD = 3.0  # s: longest stretch with no visual event (cut, layer in/out, keyframe, camera key, shake)


def check_holds(slug: str, scenes: list[dict], limit: float = MAX_HOLD) -> list[str]:
    bad, t0 = [], 0.0
    for s in scenes:
        ev = visual_events(s)
        for a, b in zip(ev, ev[1:]):
            if b - a > limit:
                bad.append(f"{s['id']} {t0 + a:.1f}-{t0 + b:.1f}s ({b - a:.1f}s)")
        t0 += s["duration"]
    return bad


def mark_emphasis(words: list[dict], tokens: list) -> None:
    """tokens: ["swallow", ("never", 1), ...] -> words[i]["emph"] = True (nth match, default first)."""
    for tok in tokens:
        tok, nth = (tok, 0) if isinstance(tok, str) else tok
        hits = [w for w in words if norm(w["text"]) == norm(tok)]
        if len(hits) <= nth:
            raise SystemExit(f"emphasis word {tok!r} #{nth} not in narration")
        hits[nth]["emph"] = True

STOPWORDS = set("a an the and as of to into onto on in its it's that's about when than with your but or for at from by "
                "just every being is was were be said say says dot so then this that these those my his her our their "
                "i me you he she we they it him them us what who'd who".split())


def auto_emphasis(words: list[dict], pattern: str, every: float = 2.5) -> None:
    """Red-highlight content words that match pattern (numbers, threat nouns, key verbs), never stopwords,
    at most one every `every` seconds so the red stays a signal."""
    import re
    rx = re.compile(pattern, re.I)
    last = -99.0
    for w in words:
        t = norm(w["text"])
        if t and t not in STOPWORDS and rx.search(t) and w["start"] - last >= every:
            w["emph"] = True
            last = w["start"]


BUILDERS = {**{k: (v, explainer_eps) for k, v in explainer_eps.EPISODES.items()},
            **{k: (v, horror_eps) for k, v in horror_eps.EPISODES.items()}}


def join_words(words: list[dict], joins: list) -> None:
    """Merge listed word runs into one caption token so no page can split them: "scared of" (a stranded preposition
    the pager would treat as dangling), "fifty-six kilometres" (number + unit); (src, text) also swaps the shown text,
    e.g. ("twenty twenty,", "2020,"). Match is case-insensitive and includes punctuation. Timings span the run."""
    key = lambda w: w["text"].lower().replace("\u2019", "'")
    for j in joins:
        src, rep = (j, None) if isinstance(j, str) else j
        toks = src.lower().split()
        i = 0
        while i <= len(words) - len(toks):
            run = words[i:i + len(toks)]
            if [key(w) for w in run] == toks:
                m = {**run[0], "text": rep or " ".join(w["text"] for w in run), "end": run[-1]["end"]}
                if any(w.get("emph") for w in run):
                    m["emph"] = True
                words[i:i + len(toks)] = [m]
            i += 1


def mark_pages(words: list[dict], pages: list[str], slug: str = "") -> None:
    """Explicit caption pages (explainer only; the core least-cost pager is shared with the locked horror pilot):
    `pages` is the narration split into whole readable pages, in order. Clears every word's `br`, then sets
    `br` on the word that starts each page (core paginate() breaks only there). Joined tokens ("two and a half")
    count as their sub-words; a page must start on a token start, and the pages must cover every word."""
    key = lambda s: [t for t in (x.lower().replace("’", "'").strip(".,!?;:\"") for x in s.split()) if t]
    toks = [(i, t) for i, w in enumerate(words) for t in key(w["text"])]
    starts, k = set(), 0
    for w in words:
        w.pop("br", None)
    for p in pages:
        want = key(p)
        got = [t for _, t in toks[k:k + len(want)]]
        if got != want:
            raise SystemExit(f"{slug}: caption page {p!r} does not match the words at {k}: {' '.join(got)!r}")
        wi = toks[k][0]
        if k and toks[k - 1][0] == wi:
            raise SystemExit(f"{slug}: caption page {p!r} starts inside the joined token {words[wi]['text']!r}")
        starts.add(wi)
        k += len(want)
    if k != len(toks):
        raise SystemExit(f"{slug}: caption pages stop at word {k} of {len(toks)}")
    for i in starts:
        words[i]["br"] = True


def build(slug: str) -> str:
    fn, mod = BUILDERS[slug]
    meta, scenes, words, total, source = load(slug)
    built = fn(scenes)
    if len(built) != len(scenes):
        raise SystemExit(f"{slug}: builder made {len(built)} scenes for {len(scenes)} paragraphs")
    explicit = getattr(mod, "EMPHASIS", {}).get(slug)
    if explicit:
        mark_emphasis(words, explicit)
    elif getattr(mod, "EMPH_AUTO", None):
        auto_emphasis(words, mod.EMPH_AUTO)
    stray = [w["text"] for w in words if w.get("emph") and norm(w["text"]) in STOPWORDS]
    if stray:  # red on 'and' / 'the' reads as random: fail the strict (pilot) builds, warn on the rest
        msg = f"{slug}: emphasis on stopwords {stray}"
        if slug in getattr(mod, "STRICT_HOLDS", ()):
            raise SystemExit(msg)
        print("WARN " + msg)
    join_words(words, getattr(mod, "CAPTION_JOIN", {}).get(slug, []))
    pp = getattr(mod, "PHRASE_PAGES", False)  # caption cards on phrase boundaries (pipeline/episodes/phrases.py)
    if pp is True or (isinstance(pp, (set, list, tuple)) and slug in pp):
        from .phrases import phrase_pages
        mc = (getattr(mod, "CAPTION_PAGING", None) or {}).get("maxChars", 16)
        phrase_pages(words, max_chars=mc, glue=getattr(mod, "PHRASE_GLUE", {}).get(slug, []))
    pages = getattr(mod, "CAPTION_PAGES", {}).get(slug)
    if pages:  # hand-checked whole-phrase pages (Word.br) win over the pager
        mark_pages(words, pages, slug)
    holds = check_holds(slug, built)
    if holds:
        msg = f"{slug}: visual holds over {MAX_HOLD:.0f}s: " + "; ".join(holds)
        if slug in getattr(mod, "STRICT_HOLDS", ()):
            raise SystemExit(msg)
        print("WARN " + msg)
    paging = dict(getattr(mod, "CAPTION_PAGING", None) or {})
    if slug in getattr(mod, "CAPTION_GLUE", {}):  # phrases a caption page never splits
        paging["glue"] = mod.CAPTION_GLUE[slug]
    sb = storyboard(slug, meta, built, words, total, mod.CAPTIONS, mod.OVERLAYS, source, paging)
    out = os.path.join(ROOT, "episodes", slug, "storyboard.json")
    with open(out, "w") as f:
        json.dump(sb, f, indent=1, ensure_ascii=False)
    dur = sum(s["duration"] for s in built)
    print(f"{slug}: {len(built)} scenes, {dur:.1f}s, {len(words)} words, timing={source.split()[0]} -> {os.path.relpath(out, ROOT)}")
    return out


if __name__ == "__main__":
    for s in sys.argv[1:] or sorted(BUILDERS):
        build(s)
