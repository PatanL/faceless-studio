# Send raw JSON commands to the addon bridge (no MCP server involved).
import socket, json, sys
port = int(sys.argv[1])
def call(cmd):
    s = socket.create_connection(('127.0.0.1', port), timeout=60)
    s.sendall(json.dumps(cmd).encode()); buf = b''
    while True:
        chunk = s.recv(65536)
        if not chunk: break
        buf += chunk
        try: r = json.loads(buf); break
        except ValueError: continue
    s.close(); return r
print(json.dumps(call({'type': 'get_scene_info', 'params': {}}))[:400])
code = "import bpy\nbpy.ops.mesh.primitive_cube_add(size=2)\nbpy.context.object.name='GEO-probe'\nprint('objs', len(bpy.data.objects), bpy.app.version_string)"
print(json.dumps(call({'type': 'execute_code', 'params': {'code': code}}))[:400])
