// Entry for the src/next proving ground (KitLab). Separate from src/index.ts so the shared kit's Root stays as it is.
// render: npx remotion render src/next/index.ts KitLab out/kitlab/kitlab.mp4 --gl=angle
import { registerRoot } from "remotion";
import { NextRoot } from "./NextRoot";

registerRoot(NextRoot);
