# Check the MCP 'look' tool (the render-feedback loop) against the GUI bridge; saves the returned image.
import asyncio, json, sys, base64
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
cfg = json.load(open(sys.argv[1]))['mcpServers']['blender']; out = sys.argv[2]
async def main():
    p = StdioServerParameters(command=cfg['command'], args=cfg['args'], env=cfg['env'])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool('look', {'mode': 'angles', 'shading': 'material', 'max_size': 512})
            for c in res.content:
                if getattr(c, 'type', '') == 'image':
                    open(out, 'wb').write(base64.b64decode(c.data)); print('IMAGE saved', out, c.mimeType)
                else: print('TEXT', getattr(c, 'text', '')[:300])
            print('isError', res.isError)
asyncio.run(main())
