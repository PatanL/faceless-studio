# Runs cc-blender-skill's own 35-check recipe suite inside background Blender (no MCP).
# Usage: Blender -b --factory-startup --python-exit-code 1 --python run_core_suite.py -- <vendor_repo> <out_dir>
import sys, json, importlib.util
argv = sys.argv[sys.argv.index('--') + 1:]
repo, out = argv[0], argv[1]
spec = importlib.util.spec_from_file_location('core', repo + '/tests/core_recipe_regressions.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
rep = mod.run_suite(repo, out)
fails = [t for t in rep['tests'] if t['status'] != 'PASS']
print('VERSION', rep['blender_version'], 'PASS', len(rep['tests']) - len(fails), 'FAIL', len(fails))
for t in fails: print('FAIL', t['id'], t['error'])
