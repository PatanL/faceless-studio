# End-to-end MCP check: start the server exactly as mcp-config.json says (stdio), list tools,
# call get_scene_info and execute_blender_code against the GUI bridge.
import asyncio, json, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
cfg = json.load(open(sys.argv[1]))['mcpServers']['blender']
async def main():
    p = StdioServerParameters(command=cfg['command'], args=cfg['args'], env=cfg['env'])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()
            print('TOOLS', len(tools.tools), [t.name for t in tools.tools])
            res = await s.call_tool('execute_blender_code', {'code': "import bpy\nprint('n_objects', len(bpy.data.objects))"})
            print('EXEC', res.isError, [getattr(c, 'text', '')[:200] for c in res.content])
            res = await s.call_tool('get_scene_info', {})
            print('SCENE', res.isError, [getattr(c, 'text', '')[:200] for c in res.content])
asyncio.run(main())
