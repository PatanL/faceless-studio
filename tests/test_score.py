"""pipeline/audio/score.py planning rules (no rendering). Needs numpy + soundfile: skipped where they are missing,
run on the Spark inside ~/studio/.venv:  cd tests && python -m unittest test_score"""
import unittest

import _util  # noqa: F401

try:
    from pipeline.audio import score
except Exception as e:  # noqa: BLE001
    score = None
    REASON = f"audio deps missing ({e})"


def _sb():
    """four scenes: open ocean hook, a numbers board, a polar hunt with a pivot and a marker, back to the hook place"""
    text = [("Wild orcas could hurt you. They never have.", 0.0),
            ("It weighs six tonnes. That is four cars. Is that heavy?", 4.0),
            ("In Antarctica a pod charges the ice. The seal is washed off. But the calf stays close to its mother. "
             "And then it hunts.", 12.0),
            ("Maybe they just have not decided about you, because", 30.0)]
    words, scenes = [], []
    for i, (para, t0) in enumerate(text):
        t = t0 + 0.1
        for w in para.split():
            words.append({"text": w, "start": round(t, 3), "end": round(t + 0.3, 3)})
            t += 0.38
    ends = [4.0, 12.0, 30.0, 34.5]
    settings = [{"kind": "place", "biome": "open_ocean", "place": "open ocean", "depth": 6, "light": "day"},
                {"kind": "board", "board": "blue"},
                {"kind": "place", "biome": "polar_ice", "place": "Antarctic Peninsula", "depth": 3, "waterline": 0.33,
                 "light": "overcast"},
                {"kind": "place", "biome": "open_ocean", "place": "open ocean", "depth": 6, "light": "day"}]
    t0 = 0.0
    for e, st in zip(ends, settings):
        scenes.append({"duration": e - t0, "setting": {**st, "at": 0.0}})
        t0 = e
    return {"id": "test", "scenes": scenes, "captions": {"words": words}}


@unittest.skipIf(score is None, "audio deps missing; run on the Spark venv")
class Plan(unittest.TestCase):
    def setUp(self):
        self.sb = _sb()
        self.words = score._words(self.sb, None)
        marker_t = next(w["start"] for w in self.sb["captions"]["words"] if w["text"] == "The" and w["start"] > 12)
        self.pl = score.plan(self.sb, self.words, 34.5, True,
                             [{"cue": "impact", "at": marker_t, "source": "marker"}])

    def test_moods_follow_settings_and_words(self):
        moods = [c["mood"] for c in self.pl["cues"]]
        self.assertEqual(moods[0], "question")         # the 4 s hook joins the asking board (cues >= MIN_CUE s)
        self.assertIn("cold", moods)                     # polar
        self.assertEqual(self.pl["cues"][0]["role"], "hook")
        self.assertGreaterEqual(self.pl["cues"][0]["intensity"], 1)  # Shorts: full from frame 0, not a sparse intro

    def test_cue_lengths_and_device_caps(self):
        for c in self.pl["cues"][:-1]:
            self.assertGreaterEqual(c["t1"] - c["t0"], score.MIN_CUE - 0.01)
        self.assertLessEqual(len(self.pl["stings"]), score.MAX_STINGS)
        self.assertLessEqual(len(self.pl["drops"]), score.MAX_DROPS)
        self.assertLessEqual(len(self.pl["risers"]), score.MAX_RISERS)

    def test_slow_harmonic_rhythm(self):
        long = [c for c in self.pl["cues"] if c["t1"] - c["t0"] > 12 and c["role"] != "bookend"]
        for c in long:
            beats = [(ch[1] - ch[0]) / ch[4] for ch in c["chords"]]
            self.assertGreaterEqual(min(beats[:-1] or beats), 7.5)  # two bars a chord

    def test_transition_hits_only_when_asked(self):
        self.assertEqual(self.pl["transition_hits"], [])
        pl = score.plan(self.sb, self.words, 34.5, True, [], transitions=True)
        self.assertTrue(all(any(abs(x - r["t0"]) < 0.01 for r in pl["settings"]) for x in pl["transition_hits"]))

    def test_loop_bookend_returns_to_the_hook(self):
        first, last = self.pl["cues"][0], self.pl["cues"][-1]
        self.assertEqual(last["role"], "bookend")
        self.assertEqual(last["mood"], first["mood"])
        prog = score.MOODS[first["mood"]]["prog"]
        key = first["key"]
        # the last chord is the one before bar 1 in the hook's progression (it leads back into the start)
        self.assertEqual(last["chords"][-1][2], (key + prog[-1][0]) % 12)
        self.assertEqual(first["chords"][0][2], (key + prog[0][0]) % 12)

    def test_boundaries_sit_on_settings_or_words(self):
        changes = [4.0, 12.0, 30.0]
        starts = [w["s"] for w in self.words]
        for c in self.pl["cues"][1:]:
            near_change = min(abs(c["t0"] - x) for x in changes) < 0.05
            near_word = min(abs(c["t0"] + 0.03 - x) for x in starts) < 0.05
            self.assertTrue(near_change or near_word, c["t0"])

    def test_reveals_stings_and_dropouts(self):
        whys = [s["why"] for s in self.pl["stings"]]
        self.assertTrue(any(w.startswith("marker") for w in whys), whys)
        ts = sorted(s["t"] for s in self.pl["stings"])
        self.assertTrue(all(b - a >= 4.0 for a, b in zip(ts, ts[1:])))
        ds = self.pl["drops"]
        self.assertTrue(all(0.25 <= d["t1"] - d["t0"] <= 1.3 for d in ds))
        self.assertTrue(all(b["t0"] - a["t1"] >= 13.0 for a, b in zip(ds, ds[1:])))
        self.assertTrue(all(d["t0"] > 8.0 for d in ds))   # never in the hook

    def test_bars_cover_each_cue(self):
        for c in self.pl["cues"]:
            ch = c["chords"]
            self.assertAlmostEqual(ch[0][0], c["t0"], places=3)
            self.assertAlmostEqual(ch[-1][1], c["t1"], places=3)
            for a, b in zip(ch, ch[1:]):
                self.assertAlmostEqual(a[1], b[0], places=3)

    def test_settingless_storyboard_still_gets_sections(self):
        sb = _sb()
        for s in sb["scenes"]:
            s.pop("setting")
        pl = score.plan(sb, score._words(sb, None), 34.5, False, [])
        self.assertGreaterEqual(len(pl["cues"]), 2)


@unittest.skipIf(score is None, "audio deps missing; run on the Spark venv")
class MusicalSfx(unittest.TestCase):
    def test_r14_thins_the_sfx_layer(self):
        from pipeline.audio.make import musical_sfx
        cues = [{"cue": "whoosh", "at": float(t), "source": "cut"} for t in range(0, 60, 3)]
        cues += [{"cue": "pop", "at": t + 0.5, "source": "storyboard"} for t in range(0, 60, 2)]
        cues += [{"cue": "impact", "at": 20.0, "source": "marker"}, {"cue": "impact", "at": 40.2, "source": "storyboard"}]
        out = musical_sfx(cues, {"min_gap": 2.5, "max_per_min": 6})
        self.assertFalse(any(c["cue"] == "whoosh" for c in out))
        self.assertIn(20.0, [c["at"] for c in out if c["source"] == "marker"])
        self.assertLessEqual(len(out), 7)
        ts = sorted(c["at"] for c in out)
        self.assertTrue(all(b - a >= 2.5 for a, b in zip(ts, ts[1:])))


if __name__ == "__main__":
    unittest.main()
