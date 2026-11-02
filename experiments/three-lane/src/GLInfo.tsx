// Prints headless Chrome's WebGL vendor / renderer strings into the frame, so a 1-frame render shows which GL
// backend (SwiftShader, ANGLE Metal, ...) a machine's render actually used.
import React, { useEffect, useState } from "react";
import { AbsoluteFill, continueRender, delayRender } from "remotion";

export const GLInfo: React.FC = () => {
  const [info, setInfo] = useState<string[] | null>(null);
  const [handle] = useState(() => delayRender("gl info"));
  useEffect(() => {
    const c = document.createElement("canvas");
    const gl = (c.getContext("webgl2") ?? c.getContext("webgl")) as WebGLRenderingContext | null;
    const lines: string[] = [];
    if (!gl) lines.push("NO WEBGL");
    else {
      const ext = gl.getExtension("WEBGL_debug_renderer_info");
      lines.push(`context: ${gl instanceof WebGL2RenderingContext ? "webgl2" : "webgl"}`);
      lines.push(`VENDOR: ${gl.getParameter(gl.VENDOR)}`, `RENDERER: ${gl.getParameter(gl.RENDERER)}`);
      if (ext) lines.push(`UNMASKED_VENDOR: ${gl.getParameter(ext.UNMASKED_VENDOR_WEBGL)}`, `UNMASKED_RENDERER: ${gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)}`);
      lines.push(`MAX_SAMPLES: ${gl.getParameter((gl as WebGL2RenderingContext).MAX_SAMPLES ?? 0)}`);
    }
    lines.push(`UA: ${navigator.userAgent}`, `cores: ${navigator.hardwareConcurrency}`);
    console.log("[GLInfo]", lines.join(" | "));
    setInfo(lines);
    continueRender(handle);
  }, [handle]);
  return (
    <AbsoluteFill style={{ background: "#ffffff", color: "#000000", fontFamily: "monospace", fontSize: 34, padding: 40, wordBreak: "break-all", gap: 24 }}>
      {(info ?? []).map((l, i) => <div key={i}>{l}</div>)}
    </AbsoluteFill>
  );
};
