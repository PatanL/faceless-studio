"""Phrase-boundary caption pages (orca review: cards split mid-phrase, 'KILLED A SINGLE' | 'PERSON').

phrase_pages(words) marks word["br"] = True on the first word of every caption card. Cards are chosen per sentence
by dynamic programming over a small cost model: 1-3 words (4 when short), <= max_chars, never ending on a function
word ('a', 'the', 'has', 'ever', 'her'...) or a number word ('one | organ'), never splitting a capitalised name
('Western | Australia'), preferring breaks after commas and before conjunctions / prepositions. The renderer
(studio/src/core/captions.tsx paginate) breaks only at br words when any are present.

rule="phrase" (per-episode opt-in, shots.json "caption_rule": "phrase"; default off so other episodes are unchanged):
a page may only end where a phrase ends - after punctuation, or before a word that starts a new phrase (a conjunction,
preposition, relative word, subject pronoun or a finite verb / auxiliary). It never ends on a small connecting word
(article, preposition, conjunction, auxiliary, possessive, intensifier) or a number, and never splits a noun phrase
("museum | fire", "chess | board", "decks | of guns", "a hundred | and twenty"), and a subject from its verb costs extra
("the admiral | stopped the test") or a verb from its object ("play | it", "showed | him", "beat | nearly every player"). Pages
may run to 32 characters / 6 words (7 when short) (two caption lines; the episode sets a smaller caption size) and 3.6 s so whole
phrases fit; past 22 characters a page costs a little more, so short phrase pages win when nothing is split.
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
# rule="phrase": extra page-final words that connect forward, and words that may open a new phrase
STRICT_WEAK = (WEAK_END - {"off"}) | set("nearly almost even right just over behind under every all both life-size "
                                          "wooden first third above below across through about only".split())
OBJ_ADVERB = set("about nearly almost just only over back forth out up down away off".split())   # opens the object
# irregular finite verbs the suffix test misses, and modals (the word after a modal is a verb: "would push | the ports")
IRREG = set("ran sat got took made put beat built set let held stood sank went came saw gave found kept left said sent told "
            "brought bought thought felt lost won hit cut shut".split())
MODALS = set("would could will can should might must may".split())
PRONOUN_OBJ = set("it him her them me us".split())
ARTICLES = set("a an the every each this these those his her its their my your our".split())
PHRASE_START = GOOD_START | set("he she they we i you there then when where as after before until behind under inside "
                                "through by into onto one".split())
SENT_END = re.compile(r"[.!?…]+[\"')\]]?$")
SOFT_END = re.compile(r"[,;:]+[\"')\]]?$")


def _n(w: str) -> str:
    return re.sub(r"[^a-z0-9'-]", "", w.lower().replace("’", "'"))


def _verbish(w: str) -> bool:
    """a finite verb that starts a predicate ('gets', 'moved', 'showed', 'slipped'): cheap suffix test"""
    return bool(re.match(r"^[a-z]+(ed|es|s)$", w)) and w not in ("is", "was", "has", "his", "its", "this", "us", "gears",
                                                               "pieces", "magnets", "doors", "years", "moves")


def _cost_phrase(ws: list[str], nxt: str | None, max_chars: int, pairs=frozenset()) -> float:
    """rule="phrase": a page ends only at a phrase boundary"""
    n = len(ws)
    chars = sum(len(w) for w in ws) + n - 1
    if n > (7 if chars <= 32 else 6) or chars > max_chars:
        return float("inf")
    c = 2.0 + (0.3 if n == 5 else 0.9 if n == 6 else 1.4 if n == 7 else 0) + (2.0 if n == 1 and not SENT_END.search(ws[-1]) else 0)
    c += 0.25 * max(0, chars - 24)
    last, ln = ws[-1], _n(ws[-1])
    if SENT_END.search(last):
        return c - 1.0
    if SOFT_END.search(last):
        return c - 1.5
    if nxt is None:
        return c
    nn = _n(nxt)
    prev_verb = n >= 2 and (_verbish(_n(ws[-2])) or _n(ws[-2]) in ("play", "beat", "put", "hit", "let", "set") or _n(ws[-2]) in IRREG)
    # a word ending in -s after an article or a number on the same page is a plural noun ("the lower gun ports"), not a verb
    in_np = any(_n(x) in ARTICLES or _n(x) in NUMWORDS for x in ws[:-1]) and ln.endswith("s") \
        and not ln.endswith(("shes", "ches", "sses", "xes", "zes"))
    lverb = (_verbish(ln) and not in_np) or ln in IRREG or ln in ("play", "beat", "put", "sits", "built", "rolled", "push") or (n >= 2 and _n(ws[-2]) in MODALS)
    nverb = _verbish(nn) or nn in IRREG or nn in MODALS
    if ln in NUMWORDS or re.match(r"^\d", ln) or ("-" in ln and ln.split("-")[0] in NUMWORDS):
        c += 9                                   # a number never ends a page before what it counts ("seventy-two | cannons")
    if nn == "of" or (nn == "and" and ln in NUMWORDS):
        c += 6                                   # "decks | of guns", "a hundred | and twenty": the phrase goes on
    if ln in STRICT_WEAK and not (ln in PRONOUN_OBJ and prev_verb):
        c += 9.5                                 # never end on a connecting word ("play it" may end a page)
    if (ln, nn) in pairs:
        c += 9                                   # a glued phrase
    if nn in OBJ_ADVERB and lverb:
        c += 9                                   # verb | adverb that opens its object ("needed | about twice that ballast")
    elif nn in PRONOUN_OBJ and lverb:
        c += 9                                   # verb | object ("play | it", "showed | him")
    elif nn in ARTICLES:
        c += 9 if lverb else -0.5                # verb | object NP ("would push | the lower gun ports"), else a new NP
    elif nn in ("is", "are", "was", "were", "has", "have", "had"):
        c += 0 if ln in STRICT_WEAK else 3       # "the ship | was warning": an auxiliary after a noun continues the clause
    elif nverb and ln not in STRICT_WEAK:
        c += 3                                   # subject | verb ("the admiral | stopped the test", "every run | rocks it")
    elif nn in PHRASE_START:
        c -= 0.8                                 # the next page opens a phrase
    elif nn in OBJ_ADVERB:
        c -= 0.3                                 # an adverbial after a complete object ("the ports | down to the waterline")
    elif lverb:
        c += 9                                   # verb | object ("beat | nearly every player", "beats | Benjamin")
    else:
        c += 6                                   # inside a noun phrase ("museum | fire", "chess | board")
    return c


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


def phrase_pages(words: list[dict], max_chars: int = 16, gap_break: float = 0.45, glue=(), max_card_s: float = 3.0,
                 rule: str = "default") -> list[dict]:
    """Mark word["br"] on caption page starts (in place); returns words. glue: extra phrases never split.
    max_card_s: a card never stays up longer than this (first word start -> last word end).
    rule: "default" (the live behaviour) or "phrase" (opt-in, module doc)."""
    strict = rule == "phrase"
    if strict:
        max_chars, max_card_s = max(max_chars, 32), max(max_card_s, 3.6)
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
            for i in range(max(0, j - (7 if strict else 5)), j):
                c = _cost_phrase(toks[i:j], toks[j] if j < m else None, max_chars, pairs) if strict else \
                    _cost(toks[i:j], toks[j] if j < m else None, i == 0, max_chars, pairs, ends)
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
