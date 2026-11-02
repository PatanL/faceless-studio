// three-lane renders the 3D story lane. It reuses the studio's 2D components (stick-kit characters drawn into
// textures, captions, tags) by importing them from ../../studio/src. Those files would otherwise resolve react /
// remotion from studio/node_modules (a second copy -> broken hooks), so every shared runtime is pinned to this
// project's node_modules. Same versions as studio (react 19.1.0, remotion 4.0.539).
import path from "path";
import { Config } from "@remotion/cli/config";

const here = (m: string) => path.resolve(process.cwd(), "node_modules", m);

Config.overrideWebpackConfig((c) => ({
  ...c,
  resolve: {
    ...c.resolve,
    alias: {
      ...((c.resolve?.alias as Record<string, string>) ?? {}),
      react: here("react"),
      "react-dom": here("react-dom"),
      "react/jsx-runtime": here("react/jsx-runtime"),
      "react/jsx-dev-runtime": here("react/jsx-dev-runtime"),
      remotion: here("remotion"),
    },
  },
}));
