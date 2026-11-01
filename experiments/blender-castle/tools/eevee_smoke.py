# Smoke test: compat-doc probes + headless EEVEE (Metal) render timing on this Mac.
import bpy, sys, time
out = sys.argv[sys.argv.index('--') + 1]
scene = bpy.context.scene
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'; path = 'NEXT'
except (TypeError, ValueError):
    scene.render.engine = 'BLENDER_EEVEE'; path = 'fallback'
print('engine', path, scene.render.engine)
mat = bpy.data.materials.new('t'); mat.use_nodes = True
b = mat.node_tree.nodes['Principled BSDF']
print('disabled BSDF inputs', [i.name for i in b.inputs if not i.enabled])
print('version', bpy.app.version_string, 'Action.layers', hasattr(bpy.types.Action, 'layers'))
print('eevee raytracing attr', hasattr(scene.eevee, 'use_raytracing'), 'gtao', hasattr(scene.eevee, 'use_gtao'))
scene.render.resolution_x, scene.render.resolution_y = 540, 960
scene.eevee.taa_render_samples = 32
scene.render.filepath = out
t = time.time(); bpy.ops.render.render(write_still=True)
print('eevee_render_s', round(time.time() - t, 2))
try:
    import gpu; print('gpu backend', gpu.platform.backend_type_get(), gpu.platform.renderer_get())
except Exception as e: print('gpu info err', e)
