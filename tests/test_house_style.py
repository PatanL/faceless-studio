"""House style pass (pipeline/episodes/house.py) and staging checker (pipeline/episodes/staging.py). python3 only."""
import copy
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from pipeline.episodes import house, staging  # noqa: E402


def ocean(depth=30, **p):
    return {"type": "component", "name": "explainer/Ocean", "props": {"depth": depth, **p}}


def orca(x="50%", y="35%", **kw):
    return {"type": "component", "name": "explainer/Orca", "x": x, "y": y, "width": 1000, "height": 360,
            "props": {"pxPerM": 105}, **kw}


def car(at, y="35%", **kw):
    return {"type": "component", "name": "explainer/Car", "x": "50%", "y": y, "width": 190, "height": 95, "props": {},
            "start": at, "enter": {"type": "drop", "at": at, "duration": 0.3, "distance": 60}, **kw}


def sb(scenes, words=None):
    return {"id": "t", "format": "9:16", "fps": 30, "overlays": {"grain": 0.04},
            "captions": {"words": words or [], "maxWords": 4, "maxChars": 20,
                         "style": {"fontSize": 84, "y": 0.72, "strokeWidth": 12, "uppercase": True}},
            "scenes": scenes}


def scene(i, layers, dur=4.0, bg=None, **kw):
    return {"id": f"p{i:02d}", "duration": dur, "background": bg or ocean(), "layers": layers, **kw}


class HouseTest(unittest.TestCase):
    def test_defaults(self):
        s = sb([scene(0, [orca(), car(1.0, y="60%")], camera={"keyframes": [{"t": 0, "zoom": 1.2}, {"t": 1, "zoom": 1.0}]}),
                scene(1, [orca(), {**car(1.0, y="60%"), "enter": {"type": "pop", "at": 0.5, "duration": 0.35}}]),
                scene(2, [orca()])])
        out = house.apply(s)
        self.assertEqual(out["overlays"]["grain"], 0)
        self.assertEqual(s["overlays"]["grain"], 0.04, "apply() is pure")
        for sc in out["scenes"]:
            self.assertEqual(sc["light"]["setup"], "lantern")
            self.assertIn("grade", sc)
        sc0, sc1, sc2 = out["scenes"]
        self.assertEqual(sc0["camera"]["preroll"], 0.3)
        drop = [l for l in sc0["layers"] if l.get("name") == "explainer/Car"][0]
        self.assertEqual(drop["enter"]["type"], "dropSquash")
        self.assertTrue(any(sh.get("decay") for sh in sc0["camera"]["shake"]), "landing kick")
        pop = [l for l in sc1["layers"] if l.get("name") == "explainer/Car"][0]
        self.assertEqual(pop["enter"]["type"], "popSpring")
        self.assertIn("drift", sc0["camera"])
        self.assertNotIn("drift", sc2["camera"], "last scene is the loop bookend: no drift")
        keys = [sc["background"]["props"]["key"] for sc in out["scenes"]]
        self.assertTrue(all(a != b for a, b in zip(keys, keys[1:])), keys)

    def test_shift_mark_and_wide_opt_in(self):
        s = sb([scene(0, [orca()]), scene(1, [orca()], _house={"shift": {"at": 1.5, "to": "warm"}}), scene(2, [orca()])])
        out = house.apply(s)
        p = out["scenes"][1]["background"]["props"]
        self.assertEqual((p["shiftTo"], p["shiftAt"]), ("warm", 1.5))
        self.assertFalse(any("_house" in sc for sc in out["scenes"]))
        # the v3 set persists through the whole video: every environment scene gets the reef, kelp, jellies and school
        for sc in out["scenes"]:
            names = {l.get("name") for l in sc["layers"] if l.get("role") == "dressing"}
            self.assertTrue({"explainer/Reef", "explainer/Kelp", "explainer/Jellies", "explainer/FishSchool"} <= names, names)
        # soft foreground in >= 60 % of scenes, never on the cover / bookend (loop seam)
        out = house.apply(sb([scene(i, [orca()]) for i in range(6)]))
        fore = [any(l.get("depth") == 1.45 for l in sc["layers"]) for sc in out["scenes"]]
        self.assertFalse(fore[0] or fore[-1], fore)
        self.assertGreaterEqual(sum(fore[1:-1]) / 4, 0.6, fore)
        self.assertTrue(all(l.get("blur") and l["role"] == "dressing" for sc in out["scenes"] for l in sc["layers"] if l.get("depth") == 1.45))
        # opt out per scene
        out = house.apply(sb([scene(0, [orca()], _house={"set": False}), scene(1, [orca()])]))
        self.assertFalse(any(l.get("name") == "explainer/Reef" for l in out["scenes"][0]["layers"]))

    def test_cuts_become_transitions(self):
        out = house.apply(sb([scene(i, [orca()]) for i in range(5)]))
        kinds = [sc.get("transitionIn", {}).get("type", "cut") for sc in out["scenes"][1:]]
        self.assertNotIn("cut", kinds)
        self.assertGreaterEqual(len(set(kinds)), 3, kinds)

    def test_you_chip_tether_becomes_leader(self):
        tether = {"type": "svg", "markup": '<svg viewBox="0 0 10 100"><line x1="5" y1="0" x2="5" y2="100"/></svg>',
                  "x": "50%", "y": "48%", "width": 10, "height": 40}
        chip = {"type": "component", "name": "explainer/Tag", "x": "50%", "y": "51%", "width": 175, "height": 77,
                "props": {"text": "YOU", "at": 0, "size": 32, "bg": "#f3f6f7"}}
        out = house.apply(sb([scene(0, [orca(), tether, chip])]))
        layers = out["scenes"][0]["layers"]
        self.assertFalse(any(l.get("type") == "svg" for l in layers))
        tag = [l for l in layers if l.get("name") == "explainer/Tag"][0]
        self.assertLess(tag["props"]["leader"][1], 0)
        self.assertNotIn("bg", tag["props"])

    def test_auto_shift_on_scale_beat(self):
        you = {"type": "component", "name": "explainer/You", "x": "70%", "y": "30%", "width": 150, "height": 230,
               "props": {}, "start": 2.0}
        out = house.apply(sb([scene(0, [orca()]), scene(1, [orca(), you])]))
        self.assertEqual(out["scenes"][1]["background"]["props"]["shiftAt"], 1.8)
        self.assertEqual(staging.check_colour(out), [])

    def test_label_lag(self):
        diver = {"type": "component", "name": "explainer/Diver", "x": "70%", "y": "40%", "width": 280, "height": 90,
                 "props": {}, "idle": [{"type": "float", "amount": 6, "speed": 0.35}]}
        tag = {"type": "component", "name": "explainer/Tag", "x": "70%", "y": "45%", "width": 200, "height": 80,
               "props": {"text": "YOU", "at": 0}}
        out = house.apply(sb([scene(0, [diver, tag]), scene(1, [])]))
        t = [l for l in out["scenes"][0]["layers"] if l.get("name") == "explainer/Tag"][0]
        self.assertAlmostEqual(t["idle"][0]["phase"], house.lag_phase(0.35, 0.16), places=3)


class StagingTest(unittest.TestCase):
    def test_car_through_hero(self):
        bad = staging.check(sb([scene(0, [orca(), car(1.0)], bg=ocean(shiftTo="warm", shiftAt=1))]))
        self.assertTrue(any("[hero]" in m and "Car" in m for m in bad), bad)
        ok = staging.check(sb([scene(0, [orca(), car(1.0, allowOverlap=True)], bg=ocean(shiftTo="warm", shiftAt=1))]))
        self.assertFalse(any("[hero]" in m for m in ok), ok)

    def test_label_on_caption_and_prop_under_caption(self):
        words = [{"text": w, "start": 0.2 + 0.3 * i, "end": 0.45 + 0.3 * i} for i, w in enumerate("and its fin alone".split())]
        tag = {"type": "component", "name": "explainer/Tag", "x": "50%", "y": "68%", "width": 600, "height": 110,
               "props": {"text": "YOU", "at": 0.0, "size": 46}, "depth": 0, "z": 20}
        plat = car(0.0, y="72%")
        bad = staging.check(sb([scene(0, [orca(), tag, plat], bg=ocean(shiftTo="warm", shiftAt=1))], words))
        self.assertTrue(any("[caption]" in m for m in bad), bad)
        self.assertTrue(any("[under]" in m and "Car" in m for m in bad), bad)

    def test_number_clipped_by_prop_above(self):
        num = {"type": "component", "name": "explainer/Tag", "x": "50%", "y": "60%", "width": 300, "height": 110,
               "props": {"text": "8 M", "at": 0, "size": 52}, "z": 1}
        plat = {**car(0.0, y="60%"), "z": 5, "width": 400, "height": 140}
        bad = staging.check(sb([scene(0, [num, plat], bg=ocean(shiftTo="warm", shiftAt=1))]))
        self.assertTrue(any("[clipped]" in m for m in bad), bad)
        num["z"] = 30
        ok = staging.check(sb([scene(0, [num, plat], bg=ocean(shiftTo="warm", shiftAt=1))]))
        self.assertFalse(any("[clipped]" in m for m in ok), ok)

    def test_freeze_then_abrupt_push(self):
        cam = {"keyframes": [{"t": 0, "zoom": 1.0}, {"t": 0.5, "zoom": 1.0}, {"t": 1.6, "zoom": 1.0},
                             {"t": 2.6, "zoom": 1.6, "ease": "out"}]}
        bad = staging.check(sb([scene(0, [orca()], dur=3.0, camera=cam, bg=ocean(shiftTo="warm", shiftAt=0))]))
        self.assertTrue(any("[freeze]" in m for m in bad), bad)
        cam2 = copy.deepcopy(cam)
        cam2["keyframes"][-1]["ease"] = "inOut"
        ok = staging.check(sb([scene(0, [orca()], dur=3.0, camera=cam2, bg=ocean(shiftTo="warm", shiftAt=0))]))
        self.assertFalse(any("[freeze]" in m for m in ok), ok)

    def test_colour_shift_required(self):
        self.assertTrue(staging.check_colour(sb([scene(0, []), scene(1, [])])))
        self.assertEqual(staging.check_colour(sb([scene(0, [], bg=ocean(look="legacy"))])), [])

    def test_camera_preroll_keeps_first_key(self):
        cam = {"keyframes": [{"t": 0, "zoom": 1.65, "x": 600, "y": 700}, {"t": 1, "zoom": 1.0, "x": 540, "y": 960}], "preroll": 0.3}
        x, y, z = staging.camera_at(cam, 0.0, 1080, 1920, 3)
        self.assertAlmostEqual(z, 1.65, places=6)
        z1 = staging.camera_at(cam, 1 / 30, 1080, 1920, 3)[2]
        z1_plain = staging.camera_at({**cam, "preroll": 0}, 1 / 30, 1080, 1920, 3)[2]
        self.assertLess(z1, z1_plain, "pre-rolled move is already under way on frame 1")

    def test_built_explainers_pass(self):
        """every committed house-style explainer storyboard passes the checker it was built with"""
        for slug in ("explainer-orca", "explainer-blue-whale", "explainer-anglerfish", "explainer-pressure-ladder",
                     "explainer-saltwater-croc"):
            p = os.path.join(ROOT, "episodes", slug, "storyboard.json")
            if not os.path.exists(p):
                continue
            s = json.load(open(p))
            if "house" not in (s.get("_built") or {}).get("style", ""):
                continue
            self.assertEqual([m for m in staging.check(s) if not staging.is_warning(m)], [], slug)

    def test_new_checks(self):
        """orca_full_v1 judge misses: a tag on a subject, a bubble off the safe area, a headline that repeats the caption"""
        words = [{"text": "Bigger", "start": 1.0, "end": 1.4}, {"text": "wins.", "start": 1.4, "end": 2.0},
                 {"text": "Next", "start": 2.6, "end": 3.0}]
        tag = {"type": "component", "name": "explainer/Tag", "x": "50%", "y": "35%", "width": 600, "height": 110,
               "depth": 0, "props": {"text": "NOT TO SCALE", "at": 0.2, "size": 46}}
        bubble = {"type": "svg", "markup": '<svg viewBox="0 0 260 110"><text>YUCK?</text></svg>', "x": "97%", "y": "40%",
                  "width": 230, "height": 98}
        head = {"type": "component", "name": "explainer/Headline", "x": "50%", "y": "13%", "width": 1000, "height": 220,
                "depth": 0, "props": {"text": "BIGGER WINS", "at": 0.5, "size": 80}}
        v = staging.check(sb([scene(0, [orca(), tag, bubble, head])], words))
        kinds = {m.split("[")[1].split("]")[0] for m in v}
        self.assertTrue({"cover", "safe", "dup"} <= kinds, v)


if __name__ == "__main__":
    unittest.main()
