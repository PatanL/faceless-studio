// REPLICATION STUDY entry point (internal, never published): its own Remotion root so the study never touches the
// episode Root. Render: npx remotion render src/study/index.ts VS1Z <out>
import { registerRoot } from "remotion";
import { StudyRoot } from "./StudyRoot";
registerRoot(StudyRoot);
