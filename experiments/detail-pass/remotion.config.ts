import {Config} from '@remotion/cli/config';

// Same encoder settings as studio/remotion.config.ts, so render costs compare 1:1.
// CPU-only Spark: software GL, JPEG intermediates, H.264 MP4 output.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setChromiumOpenGlRenderer('swangle');
Config.setConcurrency(4); // BRIEF budget: <= 4 for Remotion on the Spark
Config.setOverwriteOutput(true);

// The hero orca is imported read-only from experiments/asset-gen/orca-b. Pin React (and the JSX runtime) to
// this project's single copy so a file outside the entry folder never pulls in a second React.
import path from 'node:path';
Config.overrideWebpackConfig((cfg) => ({
	...cfg,
	resolve: {
		...cfg.resolve,
		alias: {
			...(cfg.resolve?.alias as Record<string, string> | undefined),
			react: path.resolve(process.cwd(), 'node_modules/react'),
			'react-dom': path.resolve(process.cwd(), 'node_modules/react-dom'),
		},
	},
}));
