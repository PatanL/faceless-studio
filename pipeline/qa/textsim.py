"""Similarity measures used by the sameness check (pure python, no deps)."""
from __future__ import annotations

import math
import re
import unicodedata
import zlib
from collections import Counter

_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").translate(_QUOTES).lower()
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def words(s: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", norm(s))


def char_ngrams(s: str, n: int = 3) -> Counter:
    s = f" {norm(s)} "
    return Counter(s[i:i + n] for i in range(max(0, len(s) - n + 1)))


def cosine(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def trigram_cosine(a: str, b: str) -> float:
    return cosine(char_ngrams(a), char_ngrams(b))


def shingles(text: str, n: int = 5) -> list[int]:
    """Sorted crc32 hashes of the word n-grams (stored in fingerprints instead of the text)."""
    ws = words(text)
    return sorted({zlib.crc32(" ".join(ws[i:i + n]).encode()) for i in range(len(ws) - n + 1)})


def containment(a: list[int], b: list[int]) -> float:
    """Share of the smaller shingle set found in the other (1.0 = one text is inside the other)."""
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / min(len(sa), len(sb))


def edit_distance(a: list, b: list) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def norm_edit_distance(a: list, b: list) -> float:
    if not a and not b:
        return 0.0
    return edit_distance(a, b) / max(len(a), len(b))


def hamming_hex(a: str | None, b: str | None) -> int | None:
    if not a or not b or len(a) != len(b):
        return None
    return bin(int(a, 16) ^ int(b, 16)).count("1")


# Topic aliases: two names for one animal are the same topic. Keys and values are normalised topics.
ALIASES = {
    "killer whale": "orca", "killer whales": "orca", "orcas": "orca",
    "great white shark": "great white", "white shark": "great white", "great whites": "great white",
    "saltwater crocodile": "saltwater croc", "saltie": "saltwater croc", "crocodile": "croc",
    "giant pacific octopus": "octopus", "colossal squid": "colossal squid", "giant squid": "giant squid",
    "hippopotamus": "hippo", "grizzly bear": "grizzly", "brown bear": "grizzly",
    "sperm whales": "sperm whale", "blue whales": "blue whale", "anglerfish": "anglerfish", "angler fish": "anglerfish",
}
_TOPIC_STOP = {"the", "a", "an", "of", "short", "why", "how", "you", "your", "vs", "and"}
_ALIAS_VALUES = set(ALIASES.values())
# singular words that end in s: never strip it (octopus -> octopu would miss the alias table)
_KEEP_S = ("us", "ss", "is", "os")


def _singular(t: str) -> str:
    if t.endswith("s") and not t.endswith(_KEEP_S) and len(t) > 4:
        return t[:-1]
    return t


def topic_key(t: str) -> str:
    t = " ".join(w for w in words(t) if w not in _TOPIC_STOP)
    if t in ALIASES:
        return ALIASES[t]
    if t in _ALIAS_VALUES:
        return t
    if t.endswith("s") and not t.endswith("ss") and t[:-1] in ALIASES:
        return ALIASES[t[:-1]]
    if t.endswith("s") and not t.endswith("ss") and t[:-1] in _ALIAS_VALUES:
        return t[:-1]
    return ALIASES.get(_singular(t), _singular(t))


def same_topic(a: str, b: str) -> bool:
    """Equal after aliasing, or one topic's words contain the other's (orca / orca hunting)."""
    ka, kb = topic_key(a), topic_key(b)
    if not ka or not kb:
        return False
    if ka == kb:
        return True
    wa, wb = set(ka.split()), set(kb.split())
    return bool(wa) and bool(wb) and (wa <= wb or wb <= wa)


# ---------------------------------------------------------------------------------------------- title templates
# Packaging words of viral explainer titles ("What Happens If You Fall Into ...", "Why ... Are Terrifying"). Borrowing
# a source's title template on a different subject is the point of the loop, so title similarity is judged on what is
# left after these are removed (the subject words).
TEMPLATE_WORDS = set("""
a an the and or but of to in on at by for with from into onto inside outside under over through without as is are
was were be been being am it its it's this that these those there here what what's whats why how when where which who
whom whose if would could should will can can't cannot do does did don't doesn't you you're your yours i me my we us
our they them their he she his her happens happen happened happening fall falls fell falling really actually ever
never just only even still so very most more less much many every all any some no not get gets got make makes made
work works working look looks like real truth secret secrets explained explain explains facts fact things thing ways
way reason reasons why's terrifying scary insane crazy weird strange creepy deadly dangerous wild unbelievable
shocking amazing incredible biggest largest smallest strongest fastest worst best top new one two three five ten
times time day days year years life
""".split())


def content_words(s: str) -> list[str]:
    """Subject words of a title: words() minus TEMPLATE_WORDS, singularised."""
    return [_singular(w) for w in words(s) if w not in TEMPLATE_WORDS]


def title_compare(a: str, b: str, thresh: float = 0.6) -> dict:
    """{full, content, level}: full = char-trigram cosine of the whole titles; content = the same on the subject
    words only. level FAIL = similar titles about the same subject (or one title's subject is empty, i.e. the titles
    differ only in template words); WARN = the same template on a different subject; PASS otherwise."""
    full = trigram_cosine(a, b)
    ca, cb = content_words(a), content_words(b)
    content = trigram_cosine(" ".join(ca), " ".join(cb)) if ca and cb else (1.0 if norm(a) == norm(b) or not (ca or cb) else 0.0)
    if full >= thresh and (content >= thresh or not ca or not cb):
        level = "FAIL"
    elif full >= thresh:
        level = "WARN"
    else:
        level = "PASS"
    return {"full": round(full, 3), "content": round(content, 3), "level": level}


def topic_from_title(title: str, max_words: int = 3) -> str:
    """Fallback topic for a title no kit rule matched: its first subject words."""
    return " ".join(content_words(title)[:max_words])
