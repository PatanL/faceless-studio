import {Config} from '@remotion/cli/config';

// Same encoder settings as studio/remotion.config.ts, so the A/B differs only in the scene code.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setChromiumOpenGlRenderer('swangle');
Config.setConcurrency(4);
Config.setOverwriteOutput(true);
