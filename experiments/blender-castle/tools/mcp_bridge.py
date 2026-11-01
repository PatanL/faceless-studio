# Load the pinned mcp-for-blender addon.py from vendor/ WITHOUT installing it into Blender's
# user addon dir, register it, and start its socket bridge on 127.0.0.1:<port>.
# Usage: BLENDERMCP_NO_UPDATE_CHECK=1 Blender --factory-startup --python mcp_bridge.py -- <addon.py> <port> <ready_file>
import bpy, sys, os, json, importlib.util
argv = sys.argv[sys.argv.index('--') + 1:]
addon_path, port, ready = argv[0], int(argv[1]), argv[2]
spec = importlib.util.spec_from_file_location('mcp_for_blender_pinned', addon_path)
mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod)
mod.register()
srv = mod.BlenderMCPServer(host='127.0.0.1', port=port)
srv.start()
bpy.types.blendermcp_server = srv  # so the addon's auto-start sees a running server and skips port 9876
open(ready, 'w').write(json.dumps({'pid': os.getpid(), 'port': port, 'running': bool(srv.running),
                                   'background': bpy.app.background, 'blender': bpy.app.version_string}))
print('BRIDGE', 'running' if srv.running else 'NOT running', 'background' if bpy.app.background else 'gui', flush=True)
