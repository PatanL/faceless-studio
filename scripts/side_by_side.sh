#!/usr/bin/env bash
# side_by_side.sh: pilot-vs-reference QA sheet.
#
# Pulls one frame per QA shot class out of a pilot MP4 and tiles it next to the
# matching review-ref frames (research/library/review-refs/<niche>/<ref-id>/NN_<class>.jpg)
# into ONE comparison JPG: one row per shot class, one column per reference, the
# pilot in the last (red-framed) column.
#
# Usage:
#   scripts/side_by_side.sh <pilot.mp4> <explainer|horror> [options]
# Options:
#   --storyboard <sb.json>  storyboard used to render the pilot (default: auto-find
#                           episodes/<name>/storyboard.json or studio/storyboards/<name>.json,
#                           where <name> is the MP4 basename). Scenes are matched to shot
#                           classes by scene id, notes and component names.
#   --thumb <img>           the pilot's thumbnail (PNG/JPG) for the thumbnail row
#                           (default: the pilot's first frame, which is the Shorts/TikTok cover)
#   --refs <id,id>          which reference columns to show (default: all 3 for the niche)
#   --classes <c,c>         only these rows (default: all 12 classes in frames_spec.json)
#   --cell <W>              cell width in px; cells are 9:16 (default 360 -> 360x640)
#   --out <file.jpg>        output (default: out/qa/<name>_vs_<niche>.jpg)
#   --keep                  keep the temp folder with the individual cells
#
# Tiny ffmpeg job (about 15-40 single-frame grabs): fine on the Mac or the Spark.
# On the Spark: rsync the repo first, then
#   ssh dgx-spark 'cd ~/studio/app && scripts/side_by_side.sh out/pilot.mp4 horror'
# Needs python3 and ffmpeg/ffprobe (uses $FFMPEG, ~/studio/bin/ffmpeg or PATH). Labels are
# drawn when ffmpeg has drawtext (Homebrew build does; the Spark static build does not,
# then cells are unlabeled but keep the same order: rows = classes listed in stdout).
set -euo pipefail

usage() { sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-1}"; }
[[ $# -ge 2 ]] || usage
[[ "$1" == "-h" || "$1" == "--help" ]] && usage 0

PILOT="$1"; NICHE="$2"; shift 2
SB=""; THUMB=""; REFS=""; CLASSES=""; CELL=360; OUT=""; KEEP=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --storyboard) SB="$2"; shift 2;;
    --thumb) THUMB="$2"; shift 2;;
    --refs) REFS="$2"; shift 2;;
    --classes) CLASSES="$2"; shift 2;;
    --cell) CELL="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --keep) KEEP=1; shift;;
    -h|--help) usage 0;;
    *) echo "unknown option $1" >&2; usage;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RR="$ROOT/research/library/review-refs"
[[ -f "$PILOT" ]] || { echo "pilot not found: $PILOT" >&2; exit 1; }
[[ -d "$RR/$NICHE" ]] || { echo "no review refs for niche '$NICHE' in $RR" >&2; exit 1; }

FFMPEG="${FFMPEG:-}"
if [[ -z "$FFMPEG" ]]; then
  if [[ -x "$HOME/studio/bin/ffmpeg" ]]; then FFMPEG="$HOME/studio/bin/ffmpeg"; else FFMPEG="$(command -v ffmpeg)"; fi
fi
FFPROBE="${FFPROBE:-$(dirname "$FFMPEG")/ffprobe}"
[[ -x "$FFPROBE" ]] || FFPROBE="$(command -v ffprobe)"

NAME="$(basename "${PILOT%.*}")"
if [[ -z "$SB" ]]; then
  for c in "$ROOT/episodes/$NAME/storyboard.json" "$(dirname "$PILOT")/storyboard.json" \
           "$(dirname "$PILOT")/$NAME.json" "$ROOT/studio/storyboards/$NAME.json"; do
    [[ -f "$c" ]] && { SB="$c"; break; }
  done
fi
[[ -n "$OUT" ]] || { mkdir -p "$ROOT/out/qa"; OUT="$ROOT/out/qa/${NAME}_vs_${NICHE}.jpg"; }
mkdir -p "$(dirname "$OUT")"

DUR="$("$FFPROBE" -v error -show_entries format=duration -of csv=p=0 "$PILOT")"
HAS_DT=0; "$FFMPEG" -hide_banner -filters 2>/dev/null | grep -q " drawtext " && HAS_DT=1
FONT=""
for f in /System/Library/Fonts/Supplemental/Arial\ Bold.ttf /System/Library/Fonts/Supplemental/Arial.ttf \
         /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf; do
  [[ -f "$f" ]] && { FONT="$f"; break; }
done
[[ -n "$FONT" ]] || HAS_DT=0

TMP="$(mktemp -d "${TMPDIR:-/tmp}/sbs.XXXXXX")"
[[ $KEEP == 1 ]] || trap 'rm -rf "$TMP"' EXIT

# ---- plan: which ref frames + which pilot timestamps, one line per cell -------------------
python3 -I - "$RR" "$NICHE" "$DUR" "${SB:-}" "${REFS:-}" "${CLASSES:-}" "$ROOT" > "$TMP/plan.tsv" <<'PY'
import json, os, re, sys
rr, niche, dur, sb_path, refs_arg, classes_arg, root = sys.argv[1:8]
dur = float(dur)
spec = json.load(open(os.path.join(rr, "frames_spec.json")))[niche]
classes = spec["classes"]
if classes_arg:
    want = classes_arg.split(",")
    classes = [c for c in classes if c in want]
refs = list(spec["refs"].keys())
if refs_arg:
    refs = [r for r in refs_arg.split(",") if r in spec["refs"]]
# reference durations (for the relative-position fallback)
lib = {}
try:
    for v in json.load(open(os.path.join(root, "research/library/library.json")))["videos"]:
        lib[v["id"]] = v.get("duration_s") or 0
except Exception:
    pass

PAT = {
 "explainer": [
  ("options_or_list", r"options|choices|\blist\b"),
  ("map_or_depth", r"\bmap\b|depthmeter|depth|globe"),
  ("stat_counter", r"\bstat\b|counter|meter|timer|speedbars|\bdb\b|gauge"),
  ("you_scale", r"scalebar|heightchart|\bbus\b|\bcar\b|elephant|explainer/you\b|scale|compar|\bvs\b"),
  ("diagram_anatomy", r"anatomy|cutaway|diagram|x-?ray|sonar|organ|inside|cross|liver|heart"),
  ("title_question_card", r"headline|question|title|card|verdict|kinetic"),
  ("stock_proof", r"proof|photo|real|stock|archiv|sunk|sailboat"),
  ("hero_creature", r"spermwhale|colossalsquid|orca|greatwhite|bluewhale|anglerfish|octopus|crocodile|hippo|grizzly|creature|hero|reveal"),
 ],
 "horror": [
  ("phone_chat", r"handphone|featurephone|horror/phone|\bphone\b|chat|lock|notif|call"),
  ("phone_chat_2", r"handphone|featurephone|horror/phone|\bphone\b|chat|lock|notif|call"),
  ("two_shot", r"two.?shot|pair|(protagonist.*(neighbour|stranger))|((neighbour|stranger).*protagonist)"),
  ("reaction_closeup", r"react|close|face|darkness|eyes|fear|heartbeat"),
  ("character_medium", r"protagonist|neighbour|stranger|character"),
  ("insert_prop", r"peephole|elevatorpanel|redtext|insert|prop|frontdoor|door"),
  ("wide_establishing", r"hallway|stairwell|building|exterior|wide|establish|livingroom|bedroom"),
  ("overlay_or_pov", r"peephole|pov|glitch|flicker|overlay|comment"),
 ],
}[niche]

def scene_text(s):
    bits = [s.get("id", ""), s.get("notes", "") or ""]
    bg = s.get("background") or {}
    bits.append(str(bg.get("name", "")))
    for l in s.get("layers", []) or []:
        if l.get("type") == "component":
            bits.append(str(l.get("name", "")))
    return " ".join(bits).lower()

scenes = []
if sb_path and os.path.exists(sb_path):
    sb = json.load(open(sb_path))
    t = 0.0
    for s in sb.get("scenes", []):
        d = float(s.get("duration", 0))
        scenes.append({"id": s.get("id", "?"), "start": t, "end": t + d, "text": scene_text(s), "qa": s.get("qa_class")})
        t += d
    if t > 0 and abs(t - dur) > 1.0:
        # storyboard and MP4 disagree (e.g. a different cut): rescale scene times
        k = dur / t
        for s in scenes:
            s["start"] *= k; s["end"] *= k

pilot_t, why, used = {}, {}, set()
# explicit tags first: a builder can set scene["qa_class"] (pipeline/episodes/*_eps.py) to pin a scene to a class
for i, s in enumerate(scenes):
    if s.get("qa") in classes and s["qa"] not in pilot_t:
        used.add(i)
        pilot_t[s["qa"]] = round(s["start"] + 0.55 * (s["end"] - s["start"]), 2)
        why[s["qa"]] = "scene " + s["id"] + " (qa_class)"
for cls, pat in PAT:
    if cls not in classes or cls in pilot_t:
        continue
    for i, s in enumerate(scenes):
        if i in used or i == 0:  # scene 0 is the hook row
            continue
        if re.search(pat, s["text"]):
            used.add(i)
            pilot_t[cls] = round(s["start"] + 0.55 * (s["end"] - s["start"]), 2)
            why[cls] = "scene " + s["id"]
            break

def clamp(x):
    return max(0.0, min(dur - 0.1, x))

primary = refs[0] if refs else None
for cls in classes:
    if cls == "thumbnail":
        pilot_t[cls] = 0.0; why[cls] = "first frame"
    elif cls == "hook_0s":
        pilot_t[cls] = clamp(0.5); why[cls] = "hook 0.5s"
    elif cls in ("hook_caption", "hook_twist"):
        pilot_t[cls] = clamp(2.5 if cls == "hook_caption" else min(8.0, dur * 0.1)); why[cls] = "hook"
    elif cls in ("ending_verdict", "cliffhanger_end"):
        pilot_t[cls] = clamp(dur - 0.8); why[cls] = "last second"
    elif cls not in pilot_t:
        # no storyboard match: same relative position as in the primary reference
        rel = None
        for r in refs:
            fr = spec["refs"][r]["frames"].get(cls)
            if fr and lib.get(r):
                rel = fr[0] / lib[r]; break
        pilot_t[cls] = clamp((rel if rel is not None else 0.5) * dur)
        why[cls] = "relative pos (no storyboard match)"

for cls in classes:
    idx = spec["classes"].index(cls) + 1
    for r in refs:
        f = os.path.join(rr, niche, r, f"{idx:02d}_{cls}.jpg")
        note = spec["refs"][r]["frames"].get(cls, [None, "", ""])
        sub = "sub" if (len(note) > 2 and note[2]) else ""
        print("\t".join(["ref", cls, r, f if os.path.exists(f) else "-", sub]))
    print("\t".join(["pilot", cls, "%.2f" % pilot_t[cls], why[cls], ""]))
PY

NCOLS=0
while IFS=$'\t' read -r kind cls a b c; do
  [[ "$kind" == pilot ]] && break
  NCOLS=$((NCOLS+1))
done < "$TMP/plan.tsv"
NCOLS=$((NCOLS+1))
CW="$CELL"; CH=$(( CELL * 16 / 9 )); CH=$(( CH / 2 * 2 ))

label() {  # $1 text, $2 colour -> drawtext filter fragment (or nothing)
  [[ $HAS_DT == 1 ]] || { echo ""; return; }
  local t; t="$(printf '%s' "$1" | tr -cd 'A-Za-z0-9 ._@()+-')"
  echo ",drawbox=x=0:y=0:w=iw:h=34:color=black@0.72:t=fill,drawtext=fontfile='$FONT':text='$t':x=8:y=9:fontsize=17:fontcolor=$2"
}

n=0; rows=0
echo "QA sheet: $NAME vs $NICHE refs   (duration ${DUR}s, storyboard: ${SB:-none})"
while IFS=$'\t' read -r kind cls a b c; do
  n=$((n+1)); cellf="$TMP/cell_$(printf %03d $n).jpg"
  fit="scale=${CW}:${CH}:force_original_aspect_ratio=decrease,pad=${CW}:${CH}:(ow-iw)/2:(oh-ih)/2:color=0x1a1a1a"
  if [[ "$kind" == ref ]]; then
    if [[ "$b" == "-" ]]; then
      "$FFMPEG" -v error -y -f lavfi -i "color=c=0x1a1a1a:s=${CW}x${CH}" -frames:v 1 \
        -vf "null$(label "$a  (no frame)" white)" "$cellf"
    else
      tag="${a:0:8} $cls"; [[ -n "$c" ]] && tag="$tag (sub)"
      "$FFMPEG" -v error -y -i "$b" -frames:v 1 -vf "${fit}$(label "$tag" white)" -q:v 3 "$cellf"
    fi
  else
    rows=$((rows+1))
    if [[ "$cls" == thumbnail && -n "$THUMB" ]]; then
      src=(-i "$THUMB"); what="pilot thumbnail"
    else
      src=(-ss "$a" -i "$PILOT"); what="PILOT @${a}s ${b}"
    fi
    "$FFMPEG" -v error -y "${src[@]}" -frames:v 1 \
      -vf "${fit},drawbox=x=0:y=0:w=iw:h=ih:color=0xe0303a:t=6$(label "${what:0:40}" 0xffd0d0)" -q:v 3 "$cellf"
    printf '  row %2d  %-20s pilot t=%-7s (%s)\n' "$rows" "$cls" "$a" "$b"
  fi
done < "$TMP/plan.tsv"

"$FFMPEG" -v error -y -framerate 1 -i "$TMP/cell_%03d.jpg" \
  -vf "tile=${NCOLS}x${rows}:padding=6:margin=6:color=0x000000" -frames:v 1 -q:v 3 "$OUT"
echo "wrote $OUT  (${NCOLS} columns x ${rows} rows; last column = pilot)"
