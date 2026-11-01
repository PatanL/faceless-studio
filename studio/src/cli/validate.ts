// usage: node --experimental-strip-types src/cli/validate.ts <storyboard.json> [...]
//        node --experimental-strip-types src/cli/validate.ts --json-schema > storyboard.schema.json
import {readFileSync} from 'node:fs';
import {z} from 'zod';
import {StoryboardSchema, sceneTimings} from '../core/schema.ts';

const args = process.argv.slice(2);
if (args[0] === '--json-schema') {
	process.stdout.write(JSON.stringify(z.toJSONSchema(StoryboardSchema, {io: 'input'}), null, 2) + '\n');
	process.exit(0);
}
if (!args.length) {
	console.error('usage: validate.ts <storyboard.json> [...] | --json-schema');
	process.exit(2);
}
let bad = 0;
for (const file of args) {
	const r = StoryboardSchema.safeParse(JSON.parse(readFileSync(file, 'utf8')));
	if (!r.success) {
		bad++;
		console.error(`FAIL ${file}\n${z.prettifyError(r.error)}`);
		continue;
	}
	const sb = r.data;
	const {totalFrames} = sceneTimings(sb);
	const comps = new Set<string>();
	for (const s of sb.scenes) {
		if (s.background.type === 'component') comps.add(s.background.name);
		for (const l of s.layers) if (l.type === 'component') comps.add(l.name);
	}
	console.log(
		`ok   ${file}: ${sb.format} ${sb.fps}fps ${sb.scenes.length} scenes ${(totalFrames / sb.fps).toFixed(2)}s` +
			` captions=${sb.captions?.words.length ?? 0} words` +
			(comps.size ? ` components=${[...comps].join(',')}` : ''),
	);
}
process.exit(bad ? 1 : 0);
