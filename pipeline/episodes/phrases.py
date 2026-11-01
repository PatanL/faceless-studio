"""Phrase-boundary caption pages (orca review: cards split mid-phrase, 'KILLED A SINGLE' | 'PERSON').

phrase_pages(words) marks word["br"] = True on the first word of every caption card. Cards are chosen per sentence
by dynamic programming over a small cost model: 1-3 words (4 when short), <= max_chars, never ending on a function
word ('a', 'the', 'has', 'ever', 'her'...) or a number word ('one | organ'), never splitting a capitalised name
('Western | Australia'), preferring breaks after commas and before conjunctions / prepositions. The renderer
(studio/src/core/captions.tsx paginate) breaks only at br words when any are present.
"""
from __future__ import annotations

import re

WEAK_END = set(
    "a an the and or but nor of to in on at for with by from as into onto off its it's their her his my your our "
    "is are was were has have had be been being ever never not no very so too this that these those than "
    "can could would will just about own every each some any what it "
    # orca fix round 1: a card never ends on a subject pronoun / question word / auxiliary ('MAYBE THEY', 'WHAT
    # CHANCE' is fine, 'SO WHY' is not): merge it forward
    "they you'd you're we'd we he she i there why how since been which who whose".split())
# two/three-word units a card never splits (lowercased); episodes add their own via phrase_pages(glue=...)
GLUE = ["killer whale", "killer whales", "great white", "great whites", "blue whale", "ice floe", "sperm whale",
        "golf cart", "city bus", "city buses", "jet engine", "south africa", "western australia", "new zealand"]
GOOD_START = set("and but or because with to of in on at off from for since that which who if when than like "
                 "about so except while is are was were has have had".split())
NUMWORDS = set("one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty sixty "
               "seventy eighty ninety hundred thousand million billion".split())
SENT_END = re.compile(r"[.!?…]+[\"')\]]?$")
SOFT_END = re.compile(r"[,;:]+[\"')\]]?$")


def _n(w: str) -> str:
    return re.sub(r"[^a-z0-9'-]", "", w.lower().replace("’", "'"))


def _cost(ws: list[str], nxt: str | None, sentence_start: bool, max_chars: int, pairs=frozenset(), ends=frozenset()) -> float:
    """ends: (word, word) pairs that close a glue phrase ("scared of"): a card may end there on a weak word."""
    n = len(ws)
    chars = sum(len(w) for w in ws) + n - 1
    # 5 words only when short (the renderer's own merge allows maxWords+1 at maxChars+8): "the shark you're scared of"
    if n > 5 or chars > max_chars + (8 if n >= 4 else 6):
        return float("inf")
    c = 1.0 + (1.5 if n == 4 else 3.5 if n == 5 else 0) + 0.25 * max(0, chars - max_chars)
    if nxt is not None and (_n(ws[-1]), _n(nxt)) in pairs:
        c += 8
    last = ws[-1]
    ln = _n(last)
    if SENT_END.search(last):
        c -= 1.0
    elif SOFT_END.search(last):
        c -= 1.5
    else:
        if ln in WEAK_END and not (n >= 2 and (_n(ws[-2]), ln) in ends):
            c += 6
        if ln in NUMWORDS or re.match(r"^\d", ln):
            c += 5
        if nxt is not None:
            if last[:1].isupper() and nxt[:1].isupper() and not (sentence_start and n == 1):
                c += 5
            if _n(nxt) in GOOD_START:
                c -= 0.8
            if "-" in nxt and _n(nxt).split("-")[0] in NUMWORDS:
                c += 3
    if n == 1 and not (SENT_END.search(last) and len(last) >= 6):
        c += 2.5
    if n >= 3 and _n(ws[1]) in GOOD_START and not SOFT_END.search(ws[0]):  # "of | started": a page that begins mid-phrase
        c += 0.5
    return c


def phrase_pages(words: list[dict], max_chars: int = 16, gap_break: float = 0.45, glue=(), max_card_s: float = 3.0) -> list[dict]:
    """Mark word["br"] on caption page starts (in place); returns words. glue: extra phrases never split.
    max_card_s: a card never stays up longer than this (first word start -> last word end)."""
    pairs, ends = set(), set()
    for ph in [*GLUE, *glue]:
        ws = [_n(x) for x in ph.split()]
        pairs |= {(a, b) for a, b in zip(ws, ws[1:])}
        if len(ws) >= 2:
            ends.add((ws[-2], ws[-1]))
    # hard spans: sentence ends and pauses
    spans, s = [], 0
    for i, w in enumerate(words):
        end = i == len(words) - 1 or SENT_END.search(w["text"]) or words[i + 1]["start"] - w["end"] > gap_break
        if end:
            spans.append((s, i + 1))
            s = i + 1
    for a, b in spans:
        toks = [w["text"] for w in words[a:b]]
        m = len(toks)
        best = [0.0] + [float("inf")] * m
        back = [0] * (m + 1)
        for j in range(1, m + 1):
            for i in range(max(0, j - 5), j):
                c = _cost(toks[i:j], toks[j] if j < m else None, i == 0, max_chars, pairs, ends)
                if j - i > 1 and words[a + j - 1]["end"] - words[a + i]["start"] > max_card_s:
                    c = float("inf")
                if best[i] + c < best[j]:
                    best[j], back[j] = best[i] + c, i
        cuts, j = [], m
        while j > 0:
            cuts.append(back[j])
            j = back[j]
        for i in cuts:
            words[a + i]["br"] = True
    return words


def preview(words: list[dict]) -> str:
    out, cur = [], []
    for w in words:
        if w.get("br") and cur:
            out.append(" ".join(cur))
            cur = []
        cur.append(w["text"])
    out.append(" ".join(cur))
    return " | ".join(out)
