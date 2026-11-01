#!/usr/bin/env python3
"""Originality gate: compare a script against reference transcripts.

Usage: python3 scripts/originality_check.py <script.md> <corpus_dir> [<corpus_dir> ...]

Scans .txt/.md/.json files under each corpus dir. FAIL if the script shares any run of
8+ consecutive words with a single source, or >= 2% of its 5-grams with a single source.

Only the narration the TTS will speak is checked (pipeline.audio.script.parse); if that
can't parse the file, front matter, markdown tables and 'ref:'/'references:' lines are
dropped instead. Sources are normalized the same way before matching: '#' header lines,
'[mm:ss]' timestamps, '[TAG]' markers, VTT cue lines and table pipes are removed, and only
string values of JSON are kept, so a copied run can't hide across transcript line breaks
(code review F22-F24).
"""
import json
import pathlib
import re
import sys
import unicodedata

RUN_LIMIT = 8
NGRAM = 5
NGRAM_LIMIT = 0.02
ROOT = pathlib.Path(__file__).resolve().parent.parent

QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "ʼ": "'"})
MARKERS = re.compile(r"\[\s*\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?\s*\]|\[[A-Za-z][^\]\n]{0,40}\]")


def normalize(text):
    return unicodedata.normalize("NFKC", text).translate(QUOTES)


def words(text):
    return re.findall(r"[a-z0-9']+", normalize(text).lower())


def narration_text(path):
    # The words TTS will speak; None if the script can't be parsed that way.
    try:
        sys.path.insert(0, str(ROOT))
        from pipeline.audio.script import parse
        segs = parse(pathlib.Path(path).read_text(errors="ignore")).segments
        text = " ".join(s.text for s in segs)
        return text if len(text.split()) >= 20 else None
    except Exception:
        return None
    finally:
        if sys.path and sys.path[0] == str(ROOT):
            sys.path.pop(0)


def script_text(path):
    spoken = narration_text(path)
    if spoken:
        return spoken
    text = pathlib.Path(path).read_text(errors="ignore")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    keep = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") or s.lower().startswith(("ref:", "references:", "- ref")):
            continue
        keep.append(line)
    return "\n".join(keep)


def json_strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from json_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from json_strings(v)


def source_text(path):
    raw = normalize(path.read_text(errors="ignore"))
    if path.suffix == ".json":
        try:
            return "\n".join(json_strings(json.loads(raw)))
        except ValueError:
            pass
    keep = []
    for line in raw.splitlines():
        s = line.strip()
        if s.startswith("#") or "-->" in s or s.upper() == "WEBVTT":
            continue
        keep.append(MARKERS.sub(" ", s.replace("|", " ")))
    return " ".join(keep)


def longest_common_run(a, b_set_by_len, b_words):
    # Longest run of consecutive script words that also appears consecutively in the source.
    best, i = 0, 0
    b_join = " " + " ".join(b_words) + " "
    while i < len(a):
        n = RUN_LIMIT
        if i + n <= len(a) and " " + " ".join(a[i:i + n]) + " " in b_join:
            while i + n < len(a) and " " + " ".join(a[i:i + n + 1]) + " " in b_join:
                n += 1
            best = max(best, n)
            i += n
        else:
            i += 1
    return best


def ngrams(ws, n):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    script = words(script_text(sys.argv[1]))
    if not script:
        print("FAIL: empty script")
        sys.exit(1)
    grams = ngrams(script, NGRAM)
    worst = []
    for d in sys.argv[2:]:
        for p in pathlib.Path(d).rglob("*"):
            if p.suffix not in (".txt", ".md", ".json") or not p.is_file():
                continue
            if p.resolve() == pathlib.Path(sys.argv[1]).resolve():
                continue
            src = words(source_text(p))
            if len(src) < NGRAM:
                continue
            share = len(grams & ngrams(src, NGRAM)) / max(1, len(grams))
            run = longest_common_run(script, None, src)
            if run >= RUN_LIMIT or share >= NGRAM_LIMIT:
                worst.append((run, share, str(p)))
    if worst:
        print("FAIL")
        for run, share, p in sorted(worst, reverse=True)[:10]:
            print(f"  {p}: longest shared run {run} words, {share:.1%} shared {NGRAM}-grams")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
