# Today — Sun Nov 1 (times PST)

Goal: two videos that clear the owner's bar (hook ≥ 8/10; continuity and audio ≥ 7/10, per FEEDBACK.md), made by the automated pipeline, plus a loop that learns from what's posted. Owner time: ~15 minutes total.

| Time | Who | What |
|---|---|---|
| 1:00–3:00 | auto | **Judges from FEEDBACK.md**: hook judge (vs the top 3 references for the topic), continuity judge (static holds, scale/colour drift, choppy or snapping motion, loops), and audio judge (seams, gaps, unnatural pauses, late SFX), all wired into the QA gate. Calibration: re-score the 3 pilots. The orca's real numbers must be consistent with its scores. |
| 1:30 | **you, 3 min** | Screenshots of the orca's YouTube Studio analytics (retention graph and "viewed vs swiped away") and its Instagram/Facebook reel insights (average watch time, skip rate). Send them in the chat. |
| 1:30–3:00 | auto | **Orca diagnosis**: line the retention up with the storyboard (the exact second, line and shot where viewers leave) and write it into LEARNING.md. |
| 1:30–3:30 | auto | **Voice lab**: the same hook read 4 ways (Kokoro voices, speed, and pause/prosody tuning; other CPU-only open TTS if it beats Kokoro). |
| 3:30 | **you, 1 min** | Listen to the 4 samples and reply with a number. |
| 2:30–5:00 | auto | **Hook lab + 2 new videos**: each with 3 hook variants judged against references, built by `studio-make --source` with the new gate. Fix rounds until hook ≥ 8 and every other rule ≥ 7. |
| 5:00–6:00 | auto | Final gate, title/caption/description, and frame sheets for you. |
| 6:00 | **you, 3 min** | Post video #1 (YouTube, Instagram, Facebook). |
| ~7:00 | **you, 10 min, optional** | Connect Buffer and put the API key in `~/studio/.env` on the Spark, so posting is automated from tomorrow (drafts for one-tap approval). |
| 6:00–8:30 | auto | **Learning**: 24 h orca numbers plus your screenshots → LEARNING.md entry and the next experiment (one variable). |
| 9:00 | **you, 3 min** | Post video #2 and reply with a one-line rating ("6/10, hook slow at 0:02"). It goes into FEEDBACK.md automatically. |
| overnight | auto | Make tomorrow's 2 videos through the same gate, ready by 8:00 AM. |

From tomorrow, the steady state is ~5 min/day for the owner: approve 2 Buffer drafts, and optionally one line of feedback. The weekly retention screenshots stop once YouTube Analytics OAuth is connected (10 min, one time).

TikTok: the account looks flagged as a bot (0 distribution). Validate on YouTube, Instagram and Facebook. If we want TikTok later, warm up a fresh account by hand (a few days of normal use) and post natively from the phone.
