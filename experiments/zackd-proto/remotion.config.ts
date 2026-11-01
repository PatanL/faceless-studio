import {Config} from '@remotion/cli/config';

// CPU-only Spark: software WebGL through ANGLE/SwiftShader ("swangle"), JPEG intermediates, H.264.
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(18);
Config.setPixelFormat('yuv420p');
Config.setChromiumOpenGlRenderer('swangle');
Config.setConcurrency(2); // task budget: concurrency 2, niced
Config.setOverwriteOutput(true);
