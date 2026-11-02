// Cast-size check on any kit episode (our own code): the projected head size of every group's people, from the
// story file and storyboard alone (no render). Usage (from experiments/three-lane):
//   node_modules/.bin/esbuild src/next/tools/cast_check.ts --bundle --platform=node --outfile=<scratch>/cast.cjs \
//     --loader:.woff=empty --loader:.woff2=empty --loader:.css=empty && node <scratch>/cast.cjs vasa ../../episodes/story-vasa/storyboard.json
//   node <scratch>/cast.cjs kitlab
import fs from "fs";
import { parseStoryboard } from "../../../../../studio/src/core/schema";
import { Timing } from "../../kit/timing";
import { buildStory } from "../../vasa/story";
import { synthWords } from "../kitlab/script";
import { buildLab } from "../kitlab/story";
import { castCheck, peopleCast } from "../../kit/castframe";
import type { GroupSpec, V3 } from "../../kit/Stage";

const [which, sbPath] = process.argv.slice(2);
let groups: GroupSpec[], castOf = peopleCast;
if (which === "vasa") {
  const sb = parseStoryboard(JSON.parse(fs.readFileSync(sbPath, "utf8")));
  const words = (sb.captions?.words ?? []).map((w, i) => (i === 0 && w.start < 0.4 ? { ...w, start: 0 } : w));
  groups = buildStory(new Timing(sb.scenes.map((s) => s.duration), words)).groups;
} else {
  const lab = synthWords();
  const s = buildLab(new Timing([lab.words[lab.words.length - 1].end + 0.4], lab.words));
  groups = s.groups;
  castOf = (g, t) => (s.cast[g.id]?.(t) ?? []) as V3[];
}
console.log(JSON.stringify(castCheck(groups, castOf), null, 1));
