"""Rule-based word emphasis for narration (research/music/VOICE_CADENCE.md).

Marks the words a top Shorts storyteller stresses, from rules measured on 8 RicksClips3000 and 9 Zack D. Films
narrations (per-word pitch, loudness and length): the hook's act verb, numbers, contrast and negation words,
"so"/"too" + adjective and superlatives, names, the "You see" turn, and the twist word (the last content word of a
short sentence, of the hook and of the whole script), the object right after the act verb, one early content word in
any phrase that has no other stress, and the last content word of a long phrase. About a quarter of the words get stress (refs 25 %), never function words, at most
one stress per three words inside a phrase.

The marks drive the TTS in two ways (pipeline/audio/qwen3_tts.py):
- `instruct_for(...)`: a delivery instruction naming the words to hit (Qwen3-TTS VoiceDesign instruction control);
- `markup(...)`: the text sent to the TTS with the stressed words in capitals (captions keep the script's own text).

A script can force or veto words in its front matter: `stress: brush, thirteen` / `unstress: navy`.
No dependencies beyond the standard library, so it runs in the pipeline env on the Spark and in the Qwen venv.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

FUNCTION = set("""a an the and or nor of to in on at by for from with into onto over under about as than that this these
those there here it its it's is are was were be been being am do does did done have has had having will would shall
should can could may might must he she they we i you me him her them us my your his our their who whom whose which what
when where why how if then just also very up down out off back away again too one's if's across through around behind
inside outside toward towards against along upon near past beyond without within between among before after during
while until since because though although so such""".split())
SUBJECT = {"he", "she", "they", "it", "we", "i", "you"}
# negation / contrast / scalar words the references stress (pitch reset; "but" gets pitch, not length)
CONTRAST = {"but", "only", "never", "nobody", "nothing", "none", "no", "not", "even", "still", "yet", "every",
            "whole", "entire", "single", "nobody's", "everyone", "everything", "instead", "except", "all",
            "actually", "really", "first", "last", "alone"}
NUMBER_WORDS = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "hundreds", "thousand",
                "thousands", "million", "millions", "billion", "dozen", "dozens", "half", "twice", "once", "double",
                "triple"}
IRREGULAR_PAST = set("""ate bet bit blew bought brought built burned burnt burst buried caught chose came cut dealt dug
dived dove drank drew drove dropped fed felt fell fled flew flung forgot fought found froze gave got grabbed grew hid hit
held hung hurt kept knelt knew laid led leapt left lent let lit lost made meant met paid put quit ran rang rode rose
said sank sat saw sawed sent set sewed shook shot shut sang slid slept slung smashed snuck sold sought spat spent split
spoke spun spread sprang stole stood struck stuck stung swore swam swept swung taught tore told threw took trod woke
wore won wove wrote""".split())
AUX = {"is", "are", "was", "were", "be", "been", "had", "has", "have", "would", "could", "should", "will", "can",
       "did", "does", "do", "might", "must", "may", "just", "never", "also", "still", "even", "then", "only"}


@dataclass
class Mark:
    index: int
    word: str
    reason: str


def _norm(w: str) -> str:
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'")).strip("'")


def _sentences(words: list[str]) -> list[list[int]]:
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if re.search(r"[.!?][\"'”’)]*$", w):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _phrases(idx: list[int], words: list[str]) -> list[list[int]]:
    out, cur = [], []
    for i in idx:
        cur.append(i)
        if re.search(r"[,;:—–][\"'”’)]*$", words[i]) or words[i].endswith(("—", "-")):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def _is_content(n: str) -> bool:
    return bool(n) and n not in FUNCTION and n not in SUBJECT


def _is_number(raw: str, n: str) -> bool:
    return bool(re.search(r"\d", raw)) or n in NUMBER_WORDS or any(p in NUMBER_WORDS for p in n.split("-"))


def _act_verb(sent: list[int], words: list[str]) -> int | None:
    """The hook's act verb: the first past-tense verb that follows a subject (pronoun, noun or name)."""
    for k, i in enumerate(sent):
        n = _norm(words[i])
        past = n in IRREGULAR_PAST or (n.endswith("ed") and len(n) > 4)
        if not past or k == 0:
            continue
        prev = _norm(words[sent[k - 1]])
        if prev in SUBJECT or (prev not in FUNCTION and prev not in AUX and not words[sent[k - 1]].endswith(",")):
            return i
    return None


def mark(text: str, force: list[str] | None = None, veto: list[str] | None = None, density: float = 0.25):
    """-> [Mark] for the whitespace-split words of `text` (indices into text.split())."""
    words = text.split()
    norms = [_norm(w) for w in words]
    force = {_norm(w) for w in (force or [])}
    veto = {_norm(w) for w in (veto or [])}
    cand: dict[int, tuple[int, str]] = {}  # index -> (priority, reason); lower priority = stronger

    def add(i, pri, why):
        if i is None or not norms[i] or norms[i] in veto:
            return
        if i not in cand or pri < cand[i][0]:
            cand[i] = (pri, why)

    sents = _sentences(words)
    for si, sent in enumerate(sents):
        content = [i for i in sent if _is_content(norms[i])]
        if si == 0:  # the hook: act verb (pitch peak), the strange object right after it, the last word (~2x long)
            av = _act_verb(sent, words)
            add(av, 0, "act verb")
            if av is not None:
                after = [i for i in sent if i > av and _is_content(norms[i]) and not _is_number(words[i], norms[i])]
                if after:
                    add(after[0], 1, "act object")
            if content:
                add(content[-1], 2, "hook end")
        for k, i in enumerate(sent):
            n, raw = norms[i], words[i]
            prev = norms[sent[k - 1]] if k else ""
            if n in force:
                add(i, -1, "forced")
            if _is_number(raw, n) and n not in ("one",):
                add(i, 1, "number")
            elif n in CONTRAST or n.endswith("n't"):
                add(i, 3 if n in ("but", "all", "first", "last") else 2, "contrast")
            elif prev in ("so", "too") and _is_content(n):
                add(i, 2, "so + adjective")
            elif (n.endswith("est") and len(n) > 5 and n not in ("forest", "honest", "interest", "chest", "west",
                                                                   "rest", "test", "nest", "guest", "quest")) \
                    or prev == "most":
                add(i, 2, "superlative")
            elif n == "see" and prev == "you":
                add(i, 1, "turn")
            elif raw[:1].isupper() and k > 0 and _is_content(n) and not words[sent[k - 1]].endswith((":", '"', "“")) \
                    and not (k + 1 < len(sent) and words[sent[k + 1]][:1].isupper()):  # last word of a name run
                add(i, 4, "name")
        # a short sentence lands on its last content word (the twist / punch line, said slower)
        if 1 <= len(sent) <= 6 and content:
            add(content[-1], 1, "twist")
    # every phrase of 4+ words carries a stress: with no rule hit, its first longer content word (refs: nouns and
    # modifiers are stressed 35-60 % of the time, and the phrase's pitch peak comes early, at ~20 % of its length)
    for sent in sents:
        for ph in _phrases(sent, words):
            fill = [i for i in ph if _is_content(norms[i]) and norms[i] not in AUX and len(norms[i]) >= 4
                    and not norms[i].endswith("ly")]
            if len(ph) >= 4 and not any(i in cand for i in ph) and fill:
                add(fill[0], 5, "phrase peak")
            # long phrases also land on their last content word (objects end phrases: stressed 45 %, x1.24 long)
            if len(ph) >= 6 and fill and fill[-1] not in cand and fill[-1] != fill[0]:
                add(fill[-1], 6, "phrase end")
    if sents:  # the payoff: the last content word of the script
        last = [i for i in sents[-1] if _is_content(norms[i])]
        if last:
            add(last[-1], 1, "payoff")
    # density: at most one stress per 3 words inside a phrase, about `density` of all words overall
    keep: set[int] = set()
    for sent in sents:
        for ph in _phrases(sent, words):
            chosen = sorted((cand[i][0], i) for i in ph if i in cand)
            cap = max(1, round(len(ph) / 3))
            for _, i in chosen[:cap]:
                keep.add(i)
    limit = max(1, math.ceil(density * len(words)))
    if len(keep) > limit:
        keep = set(sorted(keep, key=lambda i: (cand[i][0], i))[:limit])
    return [Mark(i, words[i], cand[i][1]) for i in sorted(keep)]


def markup(text: str, marks: list[Mark]) -> str:
    """Stressed words in capitals (punctuation kept); other words unchanged."""
    words = text.split()
    for m in marks:
        w = words[m.index]
        words[m.index] = re.sub(r"[A-Za-z][A-Za-z'’\-]*", lambda x: x.group().upper(), w)
    return " ".join(words)


def instruct_for(marks: list[Mark], base: str = "", long: bool = False) -> str:
    """A delivery instruction for an instruction-following TTS: the cadence rules plus the words to hit.
    Kept short by default: a long instruction pulls Qwen3 VoiceDesign's voice itself around (pilot: median f0 moved
    from ~165 Hz to 250-335 Hz with the long form)."""
    hit = ", ".join(re.sub(r"[^A-Za-z0-9' -]", "", m.word) for m in marks)
    if long:
        rules = ("Deliver it like a top short-video storyteller: fast and continuous, about four words a second, with "
                 "only a tiny breath at full stops. Start each sentence high and let it fall to a low, firm finish. "
                 "Hit the key words with a big upward pitch jump, a little louder and a little longer")
        rules += f": {hit}." if hit else "."
        rules += " Slow down and stretch the last word of a short punch line. Keep the small words light and quick."
    else:
        rules = "Quick, punchy storytelling, no pauses" + (f"; hit these words hard: {hit}." if hit else ".")
    return (base.rstrip(". ") + ". " if base else "") + rules


if __name__ == "__main__":
    import sys
    t = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    ms = mark(t)
    print(markup(t, ms))
    for m in ms:
        print(f"  {m.index:3d} {m.word:15s} {m.reason}")
