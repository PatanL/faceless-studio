# Exec every '### Recipe N' python block from the domain skills on Blender 4.3 in a fresh scene,
# to find API breaks the vendor's 35-check suite does not cover. Render calls are stubbed out.
# Usage: Blender -b --factory-startup --python recipe_sweep.py -- <vendor_repo> <out_dir>
import bpy, sys, re, json, traceback
from pathlib import Path
argv = sys.argv[sys.argv.index('--') + 1:]
root, out = Path(argv[0]), Path(argv[1]); out.mkdir(parents=True, exist_ok=True)
SKILLS = ['blender-modeling', 'blender-materials', 'blender-lighting', 'blender-cameras',
          'blender-rendering', 'blender-animation', 'blender-pro-workflow']
rows = []
def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=False)
    cube = bpy.data.objects['Cube']; cube.name = 'GEO-target'
    for n in ['GEO-subject', 'GEO-base_box', 'GEO-character_face', 'GEO-character_half', 'GEO-bulb',
              'GEO-follower', 'GEO-character']:
        bpy.ops.mesh.primitive_cube_add(location=(3, 0, 0)); bpy.context.object.name = n
    bpy.context.view_layer.objects.active = bpy.data.objects['GEO-target']
    bpy.data.objects['GEO-target'].select_set(True)
    t = bpy.data.objects['GEO-target']; t.keyframe_insert('location', frame=1); t.location.x = 2; t.keyframe_insert('location', frame=24)
    c = bpy.data.objects['GEO-character']; c.keyframe_insert('location', frame=1)
    bpy.data.objects['Camera'].name = 'CAM-hero'; bpy.data.objects['Light'].name = 'LGT-key'
    bpy.context.scene.cycles.samples = 1; bpy.context.scene.eevee.taa_render_samples = 1
for skill in SKILLS:
    text = (root / 'plugin/skills' / skill / 'SKILL.md').read_text()
    for m in re.finditer(r'^### (Recipe [^\n]*)\n(.*?)(?=^### |\Z)', text, re.S | re.M):
        title, body = m.group(1), m.group(2)
        blocks = re.findall(r'```python\n(.*?)```', body, re.S)
        if not blocks: continue
        code = '\n'.join(blocks)
        code = code.replace('/tmp/', str(out) + '/')
        code = re.sub(r'bpy\.ops\.render\.(render|opengl)\(', '_stub_render(', code)
        fresh()
        hdr = out / 'fixture.hdr'
        if not hdr.exists():
            im = bpy.data.images.new('HDR', 4, 2, float_buffer=True); im.filepath_raw = str(hdr); im.file_format = 'HDR'; im.save()
        code = code.replace('/path/to/your.hdr', str(hdr))
        try:
            exec(code, {'bpy': bpy, '__name__': '__recipe__', 'scene': bpy.context.scene,
                        '_stub_render': lambda *a, **k: print('stubbed render', k)})
            rows.append({'skill': skill, 'recipe': title[:70], 'status': 'PASS'})
        except Exception as e:
            tb = traceback.format_exc().strip().splitlines()
            rows.append({'skill': skill, 'recipe': title[:70], 'status': 'FAIL',
                         'error': f'{type(e).__name__}: {e}'[:300], 'where': tb[-3:-1]})
(out / 'recipe_sweep.json').write_text(json.dumps({'blender': bpy.app.version_string, 'rows': rows}, indent=2))
for r in rows: print('SWEEP', r['status'], r['skill'], '|', r['recipe'], '|', r.get('error', ''))
