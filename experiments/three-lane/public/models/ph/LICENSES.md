# Kit model library: sources and licences

Downloaded 2026-11-02 by `experiments/three-lane/scripts/fetch_models.py` from Poly Haven's official API
(`api.polyhaven.com`) and file host (`dl.polyhaven.org`), glTF at 1k.

**Licence.** https://polyhaven.com/license (read 2026-11-02): every asset on Poly Haven is CC0. That is
effectively public domain: any use, commercial included, with no attribution required. Authors are credited
below anyway.

**What is kept.** Geometry only (`.gltf` + `.bin`). The stock texture references were removed at download and no
stock images are stored. `kit/models.ts` repaints every model:
- code-painted textures and our palette per material kind;
- the world ink pass;
- two-tone shading.

**Not used.**
- Kenney (kenney.nl answers 403 to scripted requests).
- Quaternius (CC0, but its downloads go through itch.io's browser flow).

Neither site was scraped. Walls, towers, tents, carts and market stalls are built in code (`kit/architecture.ts`).

| Model | Id | Stands in for | Restyle kind | Source | Author | Licence | Polycount | Size |
|---|---|---|---|---|---|---|---|---|
| Barrel 03 | `barrel_03` | barrel | wood | https://polyhaven.com/a/barrel_03 | Serhii Khromov | CC0 1.0 | 1473 | 44 KB |
| Wine Barrel 01 | `wine_barrel_01` | barrel, banded | wood | https://polyhaven.com/a/wine_barrel_01 | James Ray Cock | CC0 1.0 | 10820 | 380 KB |
| Wooden Barrels 01 | `wooden_barrels_01` | barrel stack | wood | https://polyhaven.com/a/wooden_barrels_01 | James Ray Cock | CC0 1.0 | 33142 | 1232 KB |
| Wooden Crate 01 | `wooden_crate_01` | crate | wood | https://polyhaven.com/a/wooden_crate_01 | James Ray Cock | CC0 1.0 | 6576 | 187 KB |
| Wooden Crate 02 | `wooden_crate_02` | crate | wood | https://polyhaven.com/a/wooden_crate_02 | James Ray Cock, Jurita Burger | CC0 1.0 | 5176 | 148 KB |
| Wooden Bucket 01 | `wooden_bucket_01` | bucket | wood | https://polyhaven.com/a/wooden_bucket_01 | James Ray Cock | CC0 1.0 | 5116 | 156 KB |
| Wicker Basket 01 | `wicker_basket_01` | basket | wicker | https://polyhaven.com/a/wicker_basket_01 | Kuutti Siitonen | CC0 1.0 | 22276 | 611 KB |
| Wicker Basket 02 | `wicker_basket_02` | basket | wicker | https://polyhaven.com/a/wicker_basket_02 | Kuutti Siitonen | CC0 1.0 | 17850 | 424 KB |
| Ceramic Pot | `ceramic_pot` | pot | clay | https://polyhaven.com/a/ceramic_pot | Aron Łyczek | CC0 1.0 | 3592 | 87 KB |
| Ceramic Vase 01 | `ceramic_vase_01` | amphora | clay | https://polyhaven.com/a/ceramic_vase_01 | James Ray Cock | CC0 1.0 | 2548 | 267 KB |
| Ceramic Vase 03 | `ceramic_vase_03` | jar | clay | https://polyhaven.com/a/ceramic_vase_03 | James Ray Cock | CC0 1.0 | 2784 | 293 KB |
| Planter Pot Clay | `planter_pot_clay` | pot | clay | https://polyhaven.com/a/planter_pot_clay | Amal Kumar | CC0 1.0 | 3080 | 77 KB |
| Brass Pot 01 | `brass_pot_01` | cauldron | bronze | https://polyhaven.com/a/brass_pot_01 | Rico Cilliers | CC0 1.0 | 3760 | 93 KB |
| Wooden Bowl 02 | `wooden_bowl_02` | bowl | wood | https://polyhaven.com/a/wooden_bowl_02 | Kuutti Siitonen | CC0 1.0 | 4666 | 114 KB |
| Rock 07 | `rock_07` | rock | rock | https://polyhaven.com/a/rock_07 | Jenelle van Heerden | CC0 1.0 | 27830 | 459 KB |
| Rock 09 | `rock_09` | rock | rock | https://polyhaven.com/a/rock_09 | Jenelle van Heerden | CC0 1.0 | 23280 | 281 KB |
| Moon Rock 02 | `moon_rock_02` | small rock | rock | https://polyhaven.com/a/moon_rock_02 | Rico Cilliers, Greg Zaal, Jenelle van Heerden | CC0 1.0 | 6194 | 78 KB |
| Moon Rock 04 | `moon_rock_04` | rock | rock | https://polyhaven.com/a/moon_rock_04 | Greg Zaal, Rico Cilliers, Jenelle van Heerden | CC0 1.0 | 14316 | 173 KB |
| Namaqualand Boulders 01 | `namaqualand_boulders_01` | boulders | rock | https://polyhaven.com/a/namaqualand_boulders_01 | Greg Zaal, Jenelle van Heerden | CC0 1.0 | 76590 | 908 KB |
| Tree Stump 01 | `tree_stump_01` | stump | bark | https://polyhaven.com/a/tree_stump_01 | Rob Tuytel | CC0 1.0 | 41046 | 943 KB |
| Fern 02 | `fern_02` | fern | leaf | https://polyhaven.com/a/fern_02 | Rob Tuytel, Rico Cilliers | CC0 1.0 | 6232 | 175 KB |
| Nettle Plant | `nettle_plant` | weed | leaf | https://polyhaven.com/a/nettle_plant | Rob Tuytel, Rico Cilliers | CC0 1.0 | 46195 | 940 KB |
| Wooden Axe | `wooden_axe` | axe | tool | https://polyhaven.com/a/wooden_axe | Ulan Cabanilla | CC0 1.0 | 3348 | 90 KB |
| Cross Pein Hammer | `cross_pein_hammer` | hammer | tool | https://polyhaven.com/a/cross_pein_hammer | Tics | CC0 1.0 | 2124 | 58 KB |
| Sledgehammer 01 | `sledgehammer_01` | sledgehammer | tool | https://polyhaven.com/a/sledgehammer_01 | Dylan Guzman | CC0 1.0 | 2596 | 66 KB |
| Rusted Spade 01 | `rusted_spade_01` | spade | tool | https://polyhaven.com/a/rusted_spade_01 | Blemonade | CC0 1.0 | 11436 | 275 KB |
| Wooden Ladder | `wooden_ladder` | ladder | wood | https://polyhaven.com/a/wooden_ladder | Miroslav Turura | CC0 1.0 | 8492 | 277 KB |
| Wooden Lantern 01 | `wooden_lantern_01` | lantern | wood | https://polyhaven.com/a/wooden_lantern_01 | James Ray Cock | CC0 1.0 | 8321 | 266 KB |
| Stone Fire Pit | `stone_fire_pit` | fire pit | rock | https://polyhaven.com/a/stone_fire_pit | Sebastian Platen | CC0 1.0 | 3887 | 95 KB |
| Kite Shield | `kite_shield` | shield | tool | https://polyhaven.com/a/kite_shield | Ulan Cabanilla | CC0 1.0 | 10306 | 286 KB |
| Wooden Broom | `wooden_broom` | broom | wood | https://polyhaven.com/a/wooden_broom | Balen | CC0 1.0 | 14258 | 501 KB |
| Wooden Stool 01 | `wooden_stool_01` | stool | wood | https://polyhaven.com/a/wooden_stool_01 | Kuutti Siitonen | CC0 1.0 | 10946 | 285 KB |
| Painted Wooden Table | `painted_wooden_table` | table | wood | https://polyhaven.com/a/painted_wooden_table | Kirill Sannikov | CC0 1.0 | 600 | 26 KB |
| Painted Wooden Bench | `painted_wooden_bench` | bench | wood | https://polyhaven.com/a/painted_wooden_bench | Kirill Sannikov | CC0 1.0 | 630 | 26 KB |
| Wooden Display Shelves 01 | `wooden_display_shelves_01` | shelves | wood | https://polyhaven.com/a/wooden_display_shelves_01 | James Ray Cock | CC0 1.0 | 3174 | 107 KB |
| Wooden Picnic Table | `wooden_picnic_table` | trestle table | wood | https://polyhaven.com/a/wooden_picnic_table | Ulan Cabanilla | CC0 1.0 | 10210 | 274 KB |
| Dutch Ship Medium | `dutch_ship_medium` | ship | wood | https://polyhaven.com/a/dutch_ship_medium | James Ray Cock, Rico Cilliers, Nicolò Zubbini | CC0 1.0 | 69162 | 2425 KB |
| Modular Wooden Pier | `modular_wooden_pier` | pier | wood | https://polyhaven.com/a/modular_wooden_pier | Rico Cilliers | CC0 1.0 | 84780 | 2601 KB |
