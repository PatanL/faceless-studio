import {Config} from '@remotion/cli/config';

// CPU-only Spark: software GL, JPEG intermediates, H.264 MP4 output.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setChromiumOpenGlRenderer('swangle');
Config.setConcurrency(2); // bench: always 2 (BRIEF budget)
Config.setOverwriteOutput(true);
