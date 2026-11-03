"""Fetch the kit's CC0 model library from Poly Haven's official API (our own code).

usage: python3 scripts/fetch_models.py            (from experiments/three-lane; skips models already present)

Only Poly Haven is used: its public API (api.polyhaven.com) and file host (dl.polyhaven.org) are the official
programmatic sources, and every asset on the site is CC0 (https://polyhaven.com/license, read 2026-11-02).
Kenney (kenney.nl answers 403 to scripted requests) and Quaternius (downloads go through itch.io's browser flow) are
not scraped. Geometry only: each glTF is saved with its .bin and with every image/texture reference removed, because
the kit repaints every model (kit/models.ts) - the stock textures are never used, so they are not shipped.
Writes public/models/ph/<id>/<id>.gltf + .bin and public/models/ph/LICENSES.md (source page, author, licence, size).
"""
import json, os, sys, urllib.request

# id -> (kind for the restyle, what it stands in for)
MODELS = {
    # containers and stores
    "barrel_03": ("wood", "barrel"), "wine_barrel_01": ("wood", "barrel, banded"), "wooden_barrels_01": ("wood", "barrel stack"),
    "wooden_crate_01": ("wood", "crate"), "wooden_crate_02": ("wood", "crate"), "wooden_bucket_01": ("wood", "bucket"),
    "wicker_basket_01": ("wicker", "basket"), "wicker_basket_02": ("wicker", "basket"), "ceramic_pot": ("clay", "pot"),
    "ceramic_vase_01": ("clay", "amphora"), "ceramic_vase_03": ("clay", "jar"), "planter_pot_clay": ("clay", "pot"),
    "brass_pot_01": ("bronze", "cauldron"), "wooden_bowl_02": ("wood", "bowl"),
    # rocks and nature
    "rock_07": ("rock", "rock"), "rock_09": ("rock", "rock"), "moon_rock_02": ("rock", "small rock"), "moon_rock_04": ("rock", "rock"),
    "namaqualand_boulders_01": ("rock", "boulders"), "tree_stump_01": ("bark", "stump"), "fern_02": ("leaf", "fern"),
    "nettle_plant": ("leaf", "weed"),
    # tools and gear
    "wooden_axe": ("tool", "axe"), "cross_pein_hammer": ("tool", "hammer"), "sledgehammer_01": ("tool", "sledgehammer"),
    "rusted_spade_01": ("tool", "spade"), "wooden_ladder": ("wood", "ladder"), "wooden_lantern_01": ("wood", "lantern"),
    "stone_fire_pit": ("rock", "fire pit"), "kite_shield": ("tool", "shield"), "wooden_broom": ("wood", "broom"),
    # furniture
    "wooden_stool_01": ("wood", "stool"), "painted_wooden_table": ("wood", "table"), "painted_wooden_bench": ("wood", "bench"),
    "wooden_display_shelves_01": ("wood", "shelves"), "wooden_picnic_table": ("wood", "trestle table"),
    # ships and structures
    "dutch_ship_medium": ("wood", "ship"), "modular_wooden_pier": ("wood", "pier"),
}

ROOT = os.path.join(os.path.dirname(__file__), "..", "public", "models", "ph")
UA = {"User-Agent": "faceless-studio-three-lane/1.0 (asset fetch; contact: repo owner)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def main():
    os.makedirs(ROOT, exist_ok=True)
    rows = []
    for mid, (kind, what) in MODELS.items():
        info = json.loads(get(f"https://api.polyhaven.com/info/{mid}"))
        d = os.path.join(ROOT, mid)
        g = os.path.join(d, f"{mid}.gltf")
        if not os.path.exists(g):
            files = json.loads(get(f"https://api.polyhaven.com/files/{mid}"))
            gl = files["gltf"]["1k"]["gltf"]
            doc = json.loads(get(gl["url"]))
            os.makedirs(d, exist_ok=True)
            for name, f in gl["include"].items():
                if name.endswith(".bin"):
                    with open(os.path.join(d, os.path.basename(name)), "wb") as fh:
                        fh.write(get(f["url"]))
                    for b in doc.get("buffers", []):
                        if b.get("uri", "").endswith(".bin"):
                            b["uri"] = os.path.basename(name)
            # drop the stock textures: no images, textures or samplers, materials keep only their names
            for k in ("images", "textures", "samplers"):
                doc.pop(k, None)
            for m in doc.get("materials", []):
                m.pop("pbrMetallicRoughness", None); m.pop("normalTexture", None); m.pop("occlusionTexture", None); m.pop("emissiveTexture", None)
            with open(g, "w") as fh:
                json.dump(doc, fh)
        size = sum(os.path.getsize(os.path.join(d, f)) for f in os.listdir(d))
        authors = ", ".join(info.get("authors", {}).keys())
        rows.append(f"| {info.get('name', mid)} | `{mid}` | {what} | {kind} | https://polyhaven.com/a/{mid} | {authors} | CC0 1.0 | {info.get('polycount', '?')} | {size // 1024} KB |")
        print(mid, size // 1024, "KB", file=sys.stderr)
    with open(os.path.join(ROOT, "LICENSES.md"), "w") as fh:
        fh.write("# Kit model library: sources and licences\n\n"
                 "Downloaded 2026-11-02 by `experiments/three-lane/scripts/fetch_models.py` from Poly Haven's official API\n"
                 "(`api.polyhaven.com`) and file host (`dl.polyhaven.org`), glTF at 1k.\n\n"
                 "**Licence.** https://polyhaven.com/license (read 2026-11-02): every asset on Poly Haven is CC0. That is\n"
                 "effectively public domain: any use, commercial included, with no attribution required. Authors are credited\n"
                 "below anyway.\n\n"
                 "**What is kept.** Geometry only (`.gltf` + `.bin`). The stock texture references were removed at download and no\n"
                 "stock images are stored. `kit/models.ts` repaints every model:\n"
                 "- code-painted textures and our palette per material kind;\n"
                 "- the world ink pass;\n"
                 "- two-tone shading.\n\n"
                 "**Not used.**\n"
                 "- Kenney (kenney.nl answers 403 to scripted requests).\n"
                 "- Quaternius (CC0, but its downloads go through itch.io's browser flow).\n\n"
                 "Neither site was scraped. Walls, towers, tents, carts and market stalls are built in code (`kit/architecture.ts`).\n\n"
                 "| Model | Id | Stands in for | Restyle kind | Source | Author | Licence | Polycount | Size |\n|---|---|---|---|---|---|---|---|---|\n"
                 + "\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
