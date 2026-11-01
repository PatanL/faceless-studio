# Test 2 (Blender lane): Zack-style castle gatehouse trap, 9:16, ~12.2 s.
# Whole shot as code. Rebuilds from an empty factory scene every run, then renders.
#
#   Blender -b --factory-startup --python build_scene.py -- --frames 1,48,120 --pct 50 --samples 16 --out out/preview
#   Blender -b --factory-startup --python build_scene.py -- --frames 1-366 --pct 100 --samples 48 --out out/frames
#   ... --look 150   (orbit views of frame 150 from fixed angles, like the MCP `look` tool)
#
# Follows vendor/cc-blender-skill (pinned a2634b5): text-to-blender order (world reset -> block-out ->
# camera -> light -> geometry -> materials -> detail -> render), GEO-/MAT-/LGT-/CAM-/RIG-/FX- names,
# hard-surface Bevel stack, metallic-as-a-switch PBR, procedural texture variation, area/sun soft
# shadows, aim_at lighting, Track-style look-at camera, EEVEE Next preset with 4.3 names.
#
# Axes: X across the gate passage, Y along it (outside = -Y, courtyard = +Y), Z up. Metres.
import bpy, bmesh, math, random, sys, time, os, argparse
from mathutils import Vector, Matrix, Euler

import json
HERE = os.path.dirname(os.path.abspath(__file__))
CUT_X = -1.8                        # section plane: everything at X < CUT_X is the removable near half

# ------------------------------------------------------------------ word times (Kokoro on the Spark -> audio/captions.json)
_words = json.load(open(os.path.join(HERE, 'audio', 'captions.json')))['words']
W = {}
for _w in _words:
    k = _w['text'].strip('.,').lower()
    W.setdefault(k, _w['start'])
W['end'] = _words[-1]['end']
HIT1 = 0.10                         # first blow (impact sfx on "The")
PRE = -0.16                         # an earlier blow, just before frame 0 (doors already bulging at frame 0)
FPS = 30
DUR = round(W['end'] + 0.8, 1)      # 0.8 s caption-free tail
NF = int(round(DUR * FPS))          # frame f <-> t = (f-1)/FPS

def tf(f): return (f - 1) / FPS
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, u): return a + (b - a) * u
def smooth(u): u = clamp(u); return u * u * (3 - 2 * u)
def smoother(u): u = clamp(u); return u * u * u * (u * (6 * u - 15) + 10)
def ease_in(u): u = clamp(u); return u * u
def ease_out(u): u = clamp(u); return 1 - (1 - u) ** 2
def ramp(t, t0, t1, fn=smooth): return fn((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)

def hexlin(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (c[0], c[1], c[2], a)

# ------------------------------------------------------------------ args
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--frames', default='1')
ap.add_argument('--pct', type=int, default=50)
ap.add_argument('--samples', type=int, default=16)
ap.add_argument('--out', default='out/preview')
ap.add_argument('--look', type=int, default=0, help='frame to view from fixed orbit angles')
ap.add_argument('--nomb', action='store_true', help='disable motion blur')
ap.add_argument('--nort', action='store_true', help='disable EEVEE ray tracing / fast GI')
ap.add_argument('--save', default='')
A = ap.parse_args(argv)
OUT = A.out if os.path.isabs(A.out) else os.path.join(HERE, A.out)
os.makedirs(OUT, exist_ok=True)

def parse_frames(s):
    fr = []
    for part in s.split(','):
        if '-' in part:
            a, b = part.split('-'); fr += list(range(int(a), int(b) + 1))
        elif part:
            fr.append(int(part))
    return fr

# ------------------------------------------------------------------ scene reset (skill: world reset first)
T0 = time.time()
for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
for m in list(bpy.data.meshes): bpy.data.meshes.remove(m)
scene = bpy.context.scene
scene.render.fps = FPS                      # skill: set fps BEFORE animating
scene.frame_start, scene.frame_end = 1, NF
col_root = scene.collection

def reset_world(color=(0.04, 0.04, 0.05, 1.0), strength=0.4):
    world = scene.world or bpy.data.worlds.new('World')
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt
wnt = reset_world()

# Zack sky: vertical gradient, horizon pale cyan -> top saturated cyan (VISUAL_GRAMMAR 4.2 sky.top / sky.horizon)
def build_sky():
    n, l = wnt.nodes, wnt.links
    out = n.new('ShaderNodeOutputWorld'); bg = n.new('ShaderNodeBackground')
    tc = n.new('ShaderNodeTexCoord'); sep = n.new('ShaderNodeSeparateXYZ')
    mr = n.new('ShaderNodeMapRange'); cr = n.new('ShaderNodeValToRGB')
    mr.inputs['From Min'].default_value = -0.02; mr.inputs['From Max'].default_value = 0.55
    cr.color_ramp.elements[0].color = hexlin('#a8eefc'); cr.color_ramp.elements[1].color = hexlin('#14c8f2')
    cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[1].position = 1.0
    l.new(tc.outputs['Generated'], sep.inputs[0]); l.new(sep.outputs['Z'], mr.inputs['Value'])
    l.new(mr.outputs['Result'], cr.inputs['Fac']); l.new(cr.outputs['Color'], bg.inputs['Color'])
    bg.inputs['Strength'].default_value = 1.0
    l.new(bg.outputs['Background'], out.inputs['Surface'])
build_sky()

# ------------------------------------------------------------------ materials (skill: metallic is a switch; procedural variation)
MATS = {}
def principled(name, color, rough=0.6, metal=0.0, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = color
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = spec
    MATS[name] = m
    return m, b

def _mixvec(nt, a, b, fac):
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'VECTOR'
    ins = {s.identifier: s for s in mx.inputs}
    nt.links.new(fac, ins['Factor_Float']); nt.links.new(a, ins['A_Vector']); nt.links.new(b, ins['B_Vector'])
    return {s.identifier: s for s in mx.outputs}['Result_Vector']

def triplanar_uv(nt):
    """Box-projected 2D coords from object position, picked by the dominant normal axis."""
    n, l = nt.nodes, nt.links
    tc = n.new('ShaderNodeTexCoord'); P = n.new('ShaderNodeSeparateXYZ'); N = n.new('ShaderNodeSeparateXYZ')
    l.new(tc.outputs['Object'], P.inputs[0]); l.new(tc.outputs['Normal'], N.inputs[0])
    def absgt(sock):
        ab = n.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; l.new(sock, ab.inputs[0])
        gt = n.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; l.new(ab.outputs[0], gt.inputs[0]); gt.inputs[1].default_value = 0.5
        return gt.outputs[0]
    wx, wz = absgt(N.outputs['X']), absgt(N.outputs['Z'])
    def comb(a, b):
        c = n.new('ShaderNodeCombineXYZ'); l.new(a, c.inputs[0]); l.new(b, c.inputs[1]); return c.outputs[0]
    vA = comb(P.outputs['X'], P.outputs['Z']); vB = comb(P.outputs['Y'], P.outputs['Z']); vC = comb(P.outputs['X'], P.outputs['Y'])
    return _mixvec(nt, _mixvec(nt, vA, vB, wx), vC, wz), tc

def stone(name, c1, c2, mortar, bw=0.9, rh=0.42, rough=0.86, bump=0.35, scale_noise=2.5):
    m, b = principled(name, c1, rough)
    nt = m.node_tree; n, l = nt.nodes, nt.links
    uv, tc = triplanar_uv(nt)
    br = n.new('ShaderNodeTexBrick')
    br.inputs['Color1'].default_value = c1; br.inputs['Color2'].default_value = c2
    br.inputs['Mortar'].default_value = mortar
    br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = 0.035
    br.inputs['Mortar Smooth'].default_value = 0.5; br.inputs['Bias'].default_value = 0.0
    br.inputs['Brick Width'].default_value = bw; br.inputs['Row Height'].default_value = rh
    br.offset = 0.5; br.squash = 1.0
    l.new(uv, br.inputs['Vector'])
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = scale_noise; nz.inputs['Detail'].default_value = 3.0
    l.new(tc.outputs['Object'], nz.inputs['Vector'])
    mul = n.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'OVERLAY'
    mi = {s.identifier: s for s in mul.inputs}
    mi['Factor_Float'].default_value = 0.35
    l.new(br.outputs['Color'], mi['A_Color']); l.new(nz.outputs['Fac'], mi['B_Color'])   # grey noise: no rainbow tint
    l.new({s.identifier: s for s in mul.outputs}['Result_Color'], b.inputs['Base Color'])
    bp = n.new('ShaderNodeBump'); bp.invert = True
    bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.04
    l.new(br.outputs['Fac'], bp.inputs['Height']); l.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def wood(name, dark, light, rough=0.62, scale=3.0):
    """skill blender-materials Recipe 12 (procedural wood), retuned to Zack's tan wood tokens."""
    m, b = principled(name, light, rough)
    nt = m.node_tree; n, l = nt.nodes, nt.links
    tc = n.new('ShaderNodeTexCoord'); mp = n.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (scale, scale, scale * 0.25)
    wv = n.new('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'X'
    wv.inputs['Scale'].default_value = 2.0; wv.inputs['Distortion'].default_value = 3.0; wv.inputs['Detail'].default_value = 2.0
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6.0
    mx = n.new('ShaderNodeMixRGB'); mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 0.3
    cr = n.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = dark; cr.color_ramp.elements[1].color = light
    cr.color_ramp.elements[0].position = 0.05; cr.color_ramp.elements[1].position = 0.95
    l.new(tc.outputs['Object'], mp.inputs['Vector']); l.new(mp.outputs['Vector'], wv.inputs['Vector'])
    l.new(mp.outputs['Vector'], nz.inputs['Vector'])
    l.new(wv.outputs['Color'], mx.inputs[1]); l.new(nz.outputs['Color'], mx.inputs[2])
    l.new(mx.outputs['Color'], cr.inputs['Fac']); l.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08; bp.inputs['Distance'].default_value = 0.01
    l.new(wv.outputs['Fac'], bp.inputs['Height']); l.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m

def iron(name, color, rough=0.42):
    m, b = principled(name, color, rough, metal=1.0)
    nt = m.node_tree; n, l = nt.nodes, nt.links
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 9.0
    mr = n.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = rough - 0.12; mr.inputs['To Max'].default_value = rough + 0.15
    l.new(nz.outputs['Fac'], mr.inputs['Value']); l.new(mr.outputs['Result'], b.inputs['Roughness'])
    return m

def glow(name, color, strength, fresnel_core=None, cull=False):
    """Emission mixed with Transparent; FAC (input 0 of the mix) is keyframed 0..1 for on/off."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n, l = nt.nodes, nt.links
    for x in list(n):
        if x.type == 'BSDF_PRINCIPLED': n.remove(x)
    em = n.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    if fresnel_core:
        lw = n.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.45
        mx = n.new('ShaderNodeMixRGB'); mx.inputs['Color1'].default_value = fresnel_core; mx.inputs['Color2'].default_value = color
        l.new(lw.outputs['Facing'], mx.inputs[0]); l.new(mx.outputs['Color'], em.inputs['Color'])
    else:
        em.inputs['Color'].default_value = color
    tr = n.new('ShaderNodeBsdfTransparent'); ms = n.new('ShaderNodeMixShader')
    l.new(tr.outputs[0], ms.inputs[1]); l.new(em.outputs[0], ms.inputs[2])
    l.new(ms.outputs[0], n['Material Output'].inputs['Surface'])
    ms.inputs[0].default_value = 1.0
    m.use_backface_culling = cull
    m.use_transparent_shadow = True
    MATS[name] = m
    return m, ms, em

def fade_mat(name, color, alpha=0.7, rough=0.9):
    m, b = principled(name, color, rough)
    b.inputs['Alpha'].default_value = alpha
    m.use_transparent_shadow = True
    return m, b

M_STONE = stone('MAT-stone_ashlar_blue', hexlin('#a3b6cc'), hexlin('#7e93ad'), hexlin('#6a7a92'), bw=1.15, rh=0.52, bump=0.3)
M_STONE_DK = stone('MAT-stone_floor', hexlin('#8796ab'), hexlin('#7a8aa1'), hexlin('#64728a'), bw=0.75, rh=0.6)
M_SECTION, _b = principled('MAT-section_cut_cobalt', hexlin('#2a4a8a'), 0.95)
M_WOOD_A = wood('MAT-wood_tan_a', hexlin('#b07a3e'), hexlin('#e6bb7c'))
M_WOOD_B = wood('MAT-wood_tan_b', hexlin('#a06a33'), hexlin('#d9a96a'), scale=2.4)
M_WOOD_DK = wood('MAT-wood_beam_dark', hexlin('#8a5a2c'), hexlin('#c48d52'))
M_LOG = wood('MAT-wood_log_bark', hexlin('#93602f'), hexlin('#d29a5c'), scale=1.5)
M_IRON = iron('MAT-iron_blued', hexlin('#7d8796'))
M_IRON_DK = iron('MAT-iron_dark', hexlin('#5c6573'), 0.5)
M_ROPE, _b = principled('MAT-rope_hemp', hexlin('#c7a46b'), 0.9)
M_GRASS, _gb = principled('MAT-grass_lime', hexlin('#7fb03a'), 0.92)
M_DIRT, _db = principled('MAT-dirt_road', hexlin('#c2a77a'), 0.95)
M_ROOF, _rb = principled('MAT-roof_slate_cobalt', hexlin('#3f6fb0'), 0.55)
M_HILL, _hb = principled('MAT-hill_far', hexlin('#8cc35a'), 0.95)
M_SLIT, _sb = principled('MAT-slit_navy', hexlin('#14244a'), 0.9)
M_TAG, TAG_MIX, _ = glow('MAT-tag_green', hexlin('#2edb31'), 7.0, cull=True)
M_BOX, BOX_MIX, _ = glow('MAT-tag_box_green', hexlin('#3be83e'), 5.0)
M_SEAL, SEAL_MIX, _ = glow('MAT-seal_cyan', hexlin('#38d4eb'), 7.0)
M_FLAME, FLAME_MIX, _ = glow('MAT-flame', hexlin('#ff8a1f'), 9.0, fresnel_core=hexlin('#ffe9a0'))
M_COAL, COAL_MIX, COAL_EM = glow('MAT-coals', hexlin('#ff5a14'), 1.5, fresnel_core=hexlin('#ffd36a'))
M_POUR, POUR_MIX, _ = glow('MAT-boiling_pour', hexlin('#ff7a1a'), 5.0, fresnel_core=hexlin('#ffe27a'))
M_DUST, DUST_B = fade_mat('MAT-dust_puff', hexlin('#dfeaf3'), 0.0)

# ------------------------------------------------------------------ mesh builder (skill: name everything, bevel stack)
class MB:
    def __init__(self): self.bm = bmesh.new()
    def _take(self, ret, mat, M):
        vs = ret['verts']
        bmesh.ops.transform(self.bm, matrix=M, verts=vs)
        new = list({f for v in vs for f in v.link_faces})
        for f in new: f.material_index = mat
        return new
    def box(self, x0, x1, y0, y1, z0, z1, mat=0, inflate=0.0):
        ret = bmesh.ops.create_cube(self.bm, size=1.0)
        c = Vector(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        S = Matrix.Diagonal((x1 - x0 + 2 * inflate, y1 - y0 + 2 * inflate, z1 - z0 + 2 * inflate, 1.0))
        return self._take(ret, mat, Matrix.Translation(c) @ S)
    def obox(self, center, dims, rot=(0, 0, 0), mat=0, inflate=0.0):
        ret = bmesh.ops.create_cube(self.bm, size=1.0)
        S = Matrix.Diagonal((dims[0] + 2 * inflate, dims[1] + 2 * inflate, dims[2] + 2 * inflate, 1.0))
        return self._take(ret, mat, Matrix.Translation(Vector(center)) @ Euler(rot).to_matrix().to_4x4() @ S)
    def cyl(self, center, r, depth, rot=(0, 0, 0), mat=0, seg=20, r2=None, inflate=0.0):
        ret = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r + inflate,
                                    radius2=(r if r2 is None else r2) + inflate, depth=depth + 2 * inflate)
        return self._take(ret, mat, Matrix.Translation(Vector(center)) @ Euler(rot).to_matrix().to_4x4())
    def sphere(self, center, r, scale=(1, 1, 1), mat=0, seg=16):
        ret = bmesh.ops.create_uvsphere(self.bm, u_segments=seg, v_segments=max(6, seg // 2), radius=r)
        return self._take(ret, mat, Matrix.Translation(Vector(center)) @ Matrix.Diagonal((*scale, 1.0)))
    def build(self, name, mats, parent=None, bevel=0.0, seg=2, smooth=False, flip=False, loc=(0, 0, 0)):
        if flip: bmesh.ops.reverse_faces(self.bm, faces=self.bm.faces[:])
        me = bpy.data.meshes.new(name); self.bm.to_mesh(me); self.bm.free()
        for m in mats: me.materials.append(m)
        ob = bpy.data.objects.new(name, me); col_root.objects.link(ob)
        ob.location = loc
        if parent: ob.parent = parent
        if smooth:
            for p in me.polygons: p.use_smooth = True
        if bevel > 0:
            bv = ob.modifiers.new('Bevel', 'BEVEL'); bv.width = bevel; bv.segments = seg
            bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(30); bv.harden_normals = False
        return ob

def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None); col_root.objects.link(e); e.location = loc
    if parent: e.parent = parent
    e.empty_display_size = 0.3
    return e

# ------------------------------------------------------------------ masonry: gatehouse + towers + curtain walls
STONE, SECT, FLOOR = 0, 1, 2
FW0, FW1 = -1.4, 0.0           # front wall Y range
BW0, BW1 = 8.0, 9.2            # back wall Y range
PH = 4.4                       # passage height
SLAB1 = 5.2                    # top of passage ceiling slab = chamber floor
CH1 = 9.0                      # chamber ceiling (roof slab bottom)
TOP = 9.8                      # roof deck
HX = 5.0                       # gatehouse half width
OSLOT = (-0.9, -0.6)           # outer portcullis slot (Y)
ISLOT = (8.45, 8.75)           # inner portcullis slot (Y)
HOLES_Y = (2.4, 4.0, 5.6)      # murder holes along the passage ceiling
HOLE = 0.26                    # half size

boxes = []
def B(x0, x1, y0, y1, z0, z1, mat=STONE): boxes.append((x0, x1, y0, y1, z0, z1, mat))

def wall_with_slot(y0, y1, slot, chamber_side):
    # the slot opens into the murder-hole chamber above the slab, so a raised portcullis hangs there in view
    s0, s1 = slot
    B(-HX, -1.95, y0, y1, 0, TOP); B(1.95, HX, y0, y1, 0, TOP)
    for k, (a, b) in enumerate(((y0, s0), (s1, y1))):
        B(-1.95, -1.8, a, b, 0, PH); B(1.8, 1.95, a, b, 0, PH)     # jambs with the groove between
        open_ = (k == 1) == (chamber_side > 0)
        B(-1.95, 1.95, a, b, PH, SLAB1 if open_ else CH1)          # wall above the opening, slot between
    B(-1.95, 1.95, y0, y1, CH1, TOP)

wall_with_slot(FW0, FW1, OSLOT, +1)
wall_with_slot(BW0, BW1, ISLOT, -1)
# side walls: solid up to the chamber floor, then thinner around the murder-hole chamber (X +-3.5)
for s in (-1, 1):
    a, b = sorted((s * 1.8, s * HX)); B(a, b, FW1, BW0, 0, SLAB1)
    a, b = sorted((s * 3.5, s * HX)); B(a, b, FW1, BW0, SLAB1, CH1)
    a, b = sorted((s * 1.8, s * HX)); B(a, b, FW1, BW0, CH1, TOP)
B(-3.5, -1.8, FW1, BW0, CH1, TOP); B(1.8, 3.5, FW1, BW0, CH1, TOP)   # roof slab over the chamber wings
B(-1.8, 1.8, FW1, BW0, CH1, TOP)
# passage ceiling slab with three square murder holes on the centre line
B(-1.8, -HOLE, FW1, BW0, PH, SLAB1); B(HOLE, 1.8, FW1, BW0, PH, SLAB1)
ys = [FW1] + [v for y in HOLES_Y for v in (y - HOLE, y + HOLE)] + [BW0]
for i in range(0, len(ys), 2): B(-HOLE, HOLE, ys[i], ys[i + 1], PH, SLAB1)
# parapet + merlons around the roof
for (x0, x1, y0, y1) in ((-HX, HX, FW0, FW0 + 0.5), (-HX, HX, BW1 - 0.5, BW1), (-HX, -HX + 0.5, FW0, BW1), (HX - 0.5, HX, FW0, BW1)):
    B(x0, x1, y0, y1, TOP, TOP + 0.75)
mx = -HX
while mx < HX - 0.3:
    for (y0, y1) in ((FW0, FW0 + 0.5), (BW1 - 0.5, BW1)): B(mx, mx + 0.6, y0, y1, TOP + 0.75, TOP + 1.45)
    mx += 1.15
my = FW0 + 0.6
while my < BW1 - 0.6:
    for (x0, x1) in ((-HX, -HX + 0.5), (HX - 0.5, HX)): B(x0, x1, my, my + 0.6, TOP + 0.75, TOP + 1.45)
    my += 1.15
# curtain walls running off both sides
for s in (1,):                      # only the far side: the near side is never seen intact
    a, b = sorted((s * 7.6, s * 40.0)); B(a, b, 2.0, 4.2, 0, 7.0)
    x = s * 7.9
    while abs(x) < 40:
        a, b = sorted((x, x + s * 0.7)); B(a, b, 2.0, 2.5, 7.0, 7.8); x += s * 1.3
# passage floor (own material)
B(-1.8, 1.8, FW0, BW1, -0.2, 0.0, FLOOR)
B(-HX, -1.8, FW0, BW1, -0.2, -0.005, FLOOR); B(1.8, HX, FW0, BW1, -0.2, -0.005, FLOOR)   # under the walls: no grass in bevel gaps

def split(bx):
    near, main = [], []
    for (x0, x1, y0, y1, z0, z1, m) in bx:
        if x1 <= CUT_X + 1e-6: near.append((x0, x1, y0, y1, z0, z1, m))
        elif x0 >= CUT_X - 1e-6: main.append((x0, x1, y0, y1, z0, z1, m))
        else:
            near.append((x0, CUT_X, y0, y1, z0, z1, m)); main.append((CUT_X, x1, y0, y1, z0, z1, m))
    return near, main
near_b, main_b = split(boxes)

mb = MB()
for bx in main_b: mb.box(*bx)
# section faces: everything on the cut plane facing the camera side gets the flat cobalt section fill
for f in mb.bm.faces:
    if abs(f.calc_center_median().x - CUT_X) < 1e-4 and f.normal.x < -0.9: f.material_index = SECT
# right flanking tower (round) + roof cone, arrow slits (as recessed navy panels)
mb.cyl((6.3, -0.6, 6.0), 2.0, 12.0, mat=STONE, seg=28)
mb.cyl((6.3, -0.6, 12.35), 2.25, 0.7, mat=STONE, seg=28)
GEO_MAIN = mb.build('GEO-gatehouse_main', [M_STONE, M_SECTION, M_STONE_DK], bevel=0.035)
mb = MB()
mb.cyl((6.3, -0.6, 14.2), 2.35, 3.0, r2=0.0, seg=28)
GEO_ROOF_R = mb.build('GEO-tower_roof_R', [M_ROOF])
for p in GEO_ROOF_R.data.polygons: p.use_smooth = True

mb = MB()
for bx in near_b: mb.box(*bx)
for (x, z) in ((-3.3, 6.6), (-3.3, 2.6)): mb.box(x - 0.12, x + 0.12, FW0 - 0.03, FW0 + 0.05, z - 0.7, z + 0.7, 4)
GEO_NEAR = mb.build('GEO-gatehouse_near', [M_STONE, M_SECTION, M_STONE_DK, M_ROOF, M_SLIT], bevel=0.035)
mb = MB()
for (x, z) in ((3.3, 6.6), (3.3, 2.6)): mb.box(x - 0.12, x + 0.12, FW0 - 0.03, FW0 + 0.05, z - 0.7, z + 0.7)
mb.build('GEO-arrow_slits_R', [M_SLIT])

# the section cutter: a box that drops through the near half (skill Recipe 4, Boolean DIFFERENCE, exact)
mb = MB(); mb.box(-60, CUT_X + 0.012, -20, 30, 0, 30)
CUTTER = mb.build('GEO-section_cutter', [M_SECTION])
CUTTER.hide_render = True; CUTTER.display_type = 'WIRE'
bo = GEO_NEAR.modifiers.new('Section', 'BOOLEAN'); bo.operation = 'DIFFERENCE'; bo.object = CUTTER
bo.solver = 'EXACT'; bo.material_mode = 'TRANSFER'; bo.use_hole_tolerant = True

# ground, road, distant hills
mb = MB(); mb.box(-150, 150, -150, 150, -0.6, -0.02)
mb.build('GEO-ground_grass', [M_GRASS])
mb = MB(); mb.box(-2.3, 2.3, -60, FW0, -0.04, 0.0); mb.box(-2.3, 2.3, BW1, 40, -0.04, 0.0)
mb.build('GEO-road_dirt', [M_DIRT])
mb = MB()
for (x, y, r, h) in ((-40, 70, 30, 9), (25, 85, 38, 12), (70, 40, 30, 8), (-70, 20, 26, 7), (60, -50, 30, 7), (-60, -60, 28, 8)):
    mb.sphere((x, y, -2), r, scale=(1, 1, h / r), seg=24)
hills = mb.build('GEO-hills_far', [M_HILL], smooth=True)

# ------------------------------------------------------------------ portcullises, glow tag, seal strips, box outline
def portcullis_geo(mb, inflate=0.0, mat=0):
    for i in range(11):
        x = -1.75 + i * 0.35
        mb.box(x - 0.06, x + 0.06, -0.075, 0.075, 0.0, 4.3, mat, inflate)
        mb.cyl((x, 0, -0.14), 0.07, 0.28, rot=(math.pi, 0, 0), r2=0.0, seg=8, mat=mat, inflate=inflate)
    for j in range(6):
        z = 0.45 + j * 0.66
        mb.box(-1.93, 1.93, -0.1, 0.1, z - 0.065, z + 0.065, mat, inflate)
    mb.box(-1.93, 1.93, -0.11, 0.11, 4.2, 4.4, mat, inflate)
    for x in (-1.2, 1.2): mb.cyl((x, 0, 4.48), 0.1, 0.06, rot=(math.pi / 2, 0, 0), mat=mat, seg=10, inflate=inflate)

PC_Y = sum(OSLOT) / 2
PC_UP, PC_DOWN = 4.53, 0.2
mb = MB(); portcullis_geo(mb)
PORT_O = mb.build('GEO-portcullis_outer', [M_IRON], bevel=0.015, loc=(0, PC_Y, PC_UP))
mb = MB(); portcullis_geo(mb, inflate=0.035); TAG = mb.build('FX-portcullis_tag', [M_TAG], parent=PORT_O, flip=True)
mb = MB(); portcullis_geo(mb)
PORT_I = mb.build('GEO-portcullis_inner', [M_IRON], bevel=0.015, loc=(0, sum(ISLOT) / 2, PC_DOWN))

mb = MB()
for yy in (PC_Y, sum(ISLOT) / 2):
    mb.box(-1.8, 1.8, yy - 0.13, yy + 0.13, 0.0, 0.07)
    for s in (-1, 1): mb.box(s * 1.8 - 0.04, s * 1.8 + 0.04, yy - 0.13, yy + 0.13, 0.0, PH)
SEAL = mb.build('FX-seal_cyan', [M_SEAL])
mb = MB(); e = 0.035
for (yy, zz) in ((FW1, 0.0), (FW1, PH), (BW0, 0.0), (BW0, PH)):
    mb.box(-1.8, 1.8, yy - e, yy + e, zz - e, zz + e)
for xx in (-1.8, 1.8):
    for zz in (0.0, PH): mb.box(xx - e, xx + e, FW1, BW0, zz - e, zz + e)
    for yy in (FW1, BW0): mb.box(xx - e, xx + e, yy - e, yy + e, 0.0, PH)
BOXTAG = mb.build('FX-stone_box_tag', [M_BOX])
M_HTAG, HTAG_MIX, _ = glow('MAT-tag_holes_green', hexlin('#2edb31'), 6.0)
mb = MB(); e = 0.04; hh = HOLE + 0.05
for hy in HOLES_Y:
    for zz in (SLAB1 + 0.02, PH - 0.02):
        mb.box(-hh, hh, hy - hh - e, hy - hh + e, zz - e, zz + e); mb.box(-hh, hh, hy + hh - e, hy + hh + e, zz - e, zz + e)
        mb.box(-hh - e, -hh + e, hy - hh, hy + hh, zz - e, zz + e); mb.box(hh - e, hh + e, hy - hh, hy + hh, zz - e, zz + e)
HOLETAG = mb.build('FX-murder_hole_tags', [M_HTAG])

# ------------------------------------------------------------------ outer gate leaves + draw-bar
LEAF_W, LEAF_T = 1.8, 0.12
def leaf(name, side):
    hinge = empty('RIG-' + name + '_hinge', (side * 1.8, FW1 + LEAF_T, 0))
    mb = MB()
    for i in range(5):
        x0 = -side * (0.02 + i * 0.356); x1 = x0 - side * 0.34
        a, b = sorted((x0, x1)); mb.box(a, b, -LEAF_T, 0, 0.02, PH - 0.05, i % 2)
    for z in (0.7, 2.1, 3.5):
        a, b = sorted((-side * 0.03, -side * 1.77)); mb.box(a, b, -LEAF_T - 0.025, -LEAF_T + 0.005, z - 0.07, z + 0.07, 2)
        for k in range(5):
            xx = -side * (0.2 + k * 0.356); mb.sphere((xx, -LEAF_T - 0.03, z), 0.035, mat=2, seg=8)
    ob = mb.build('GEO-' + name, [M_WOOD_A, M_WOOD_B, M_IRON_DK], parent=hinge, bevel=0.012)
    return hinge, ob
HINGE_L, LEAF_L = leaf('gate_leaf_L', -1)
HINGE_R, LEAF_R = leaf('gate_leaf_R', 1)
BAR_PIECES = []
for s in (-1, 1):
    mb = MB(); mb.box(-0.85, 0.85, -0.11, 0.11, -0.12, 0.12)
    ob = mb.build('GEO-drawbar_' + ('L' if s < 0 else 'R'), [M_WOOD_DK], bevel=0.02)
    ob.location = (s * 0.88, FW1 + LEAF_T + 0.12, 1.55)
    BAR_PIECES.append(ob)

# ------------------------------------------------------------------ the ram shed (rolling "tortoise") + hanging ram
SHED = empty('RIG-ram_shed', (0, 0, 0))
WR = 0.45
mb = MB()
for s in (-1, 1):
    mb.box(s * 1.2 - 0.12, s * 1.2 + 0.12, -2.3, 2.3, 0.45, 0.72, 0)                 # sole beams
    mb.box(s * 1.32 - 0.1, s * 1.32 + 0.1, -2.3, 2.3, 2.42, 2.62, 0)                 # top plates
    for yy in (-2.15, -0.7, 0.7, 2.15):
        mb.box(s * 1.25 - 0.1, s * 1.25 + 0.1, yy - 0.1, yy + 0.1, 0.72, 2.45, 0)   # posts
for yy in (-2.2, 0.0, 2.2): mb.box(-1.3, 1.3, yy - 0.1, yy + 0.1, 0.48, 0.7, 0)     # cross sills
mb.box(-0.11, 0.11, -2.4, 2.4, 3.38, 3.6, 0)                                        # ridge beam
for yy in (-2.15, 0.7, 2.15):                                                       # rafters
    for s in (-1, 1):
        mb.obox((s * 0.72, yy, 3.02), (0.14, 0.14, 1.85), rot=(0, -s * math.radians(57), 0), mat=0)
FRAME = mb.build('GEO-shed_frame', [M_WOOD_DK], parent=SHED, bevel=0.02)
mb = MB()
ang = math.atan2(0.95, 1.45); plen = math.hypot(1.55, 1.0)
for s in (-1, 1):
    for i in range(11):
        yy = -2.3 + 0.21 + i * 0.418
        c = (s * 0.76, yy, 3.08 + 0.09)
        mb.obox(c, (plen, 0.39, 0.07), rot=(0, s * ang, 0), mat=(i + (s > 0)) % 2)
ROOF = mb.build('GEO-shed_roof_planks', [M_WOOD_A, M_WOOD_B], parent=SHED, bevel=0.012)
WHEELS = []
for s in (-1, 1):
    for yy in (-1.6, 1.6):
        e_ = empty('RIG-wheel', (s * 1.25, yy, WR), parent=SHED)
        mb = MB()
        mb.cyl((0, 0, 0), WR, 0.16, rot=(0, math.pi / 2, 0), mat=0, seg=24)
        mb.cyl((0, 0, 0), WR + 0.025, 0.1, rot=(0, math.pi / 2, 0), mat=1, seg=24)
        mb.cyl((s * 0.06, 0, 0), 0.11, 0.12, rot=(0, math.pi / 2, 0), mat=1, seg=12)
        for k in range(3):
            mb.obox((0, 0, 0), (0.17, 0.07, 2 * WR - 0.06), rot=(k * math.pi / 3, 0, 0), mat=0)
        mb.build('GEO-shed_wheel', [M_WOOD_DK, M_IRON_DK], parent=e_, bevel=0.01)
        WHEELS.append(e_)
PIV_Y, PIV_Z, ROPE_L = 0.3, 3.38, 1.68
RAM = empty('RIG-ram', (0, PIV_Y, PIV_Z - ROPE_L), parent=SHED)
mb = MB()
mb.cyl((0, 0, 0), 0.23, 5.0, rot=(math.pi / 2, 0, 0), mat=0, seg=18)
for yy in (-1.6, 0.0, 1.6): mb.cyl((0, yy, 0), 0.245, 0.1, rot=(math.pi / 2, 0, 0), mat=1, seg=18)
mb.cyl((0, 2.62, 0), 0.29, 0.28, rot=(-math.pi / 2, 0, 0), r2=0.2, mat=1, seg=18)
mb.cyl((0, 2.84, 0), 0.2, 0.18, rot=(-math.pi / 2, 0, 0), r2=0.12, mat=1, seg=18)
RAMGEO = mb.build('GEO-ram_log', [M_LOG, M_IRON], parent=RAM, bevel=0.01, smooth=True)
ROPES = []
for yy in (-1.2, 1.2):
    e_ = empty('RIG-rope', (0, PIV_Y + yy, PIV_Z), parent=SHED)
    mb = MB(); mb.cyl((0, 0, -ROPE_L / 2), 0.035, ROPE_L, mat=0, seg=8)
    mb.cyl((0, 0, -ROPE_L), 0.27, 0.08, rot=(math.pi / 2, 0, 0), mat=0, seg=16)   # loop around the log
    mb.build('GEO-ram_rope', [M_ROPE], parent=e_, smooth=True)
    ROPES.append(e_)
TIP = PIV_Y + 2.98          # ram tip, local Y relative to the shed, at rest

# ------------------------------------------------------------------ murder-hole chamber: braziers, cauldrons, pours
CAUL = []
for hy in HOLES_Y:
    px, pz = 0.78, 5.95
    mb = MB()
    for s in (-1, 1):
        mb.box(px - 0.05, px + 0.05, hy + s * 0.55 - 0.05, hy + s * 0.55 + 0.05, SLAB1, pz + 0.05, 0)
    mb.box(px - 0.04, px + 0.04, hy - 0.6, hy + 0.6, pz - 0.04, pz + 0.04, 0)
    mb.cyl((px + 0.05, hy, SLAB1 + 0.18), 0.32, 0.12, mat=0, seg=16)
    mb.build('GEO-cauldron_stand', [M_IRON_DK], bevel=0.008)
    mb = MB()
    for k in range(9):
        a = k * 2.4; mb.sphere((px + 0.05 + 0.18 * math.cos(a), hy + 0.18 * math.sin(a), SLAB1 + 0.27), 0.085, mat=0, seg=8)
    coals = mb.build('FX-coals', [M_COAL], smooth=True)
    piv = empty('RIG-cauldron_pivot', (px, hy, pz))
    mb = MB()
    bowl = mb.sphere((0, 0, 0.05), 0.44, scale=(1, 1, 0.95), mat=0, seg=20)
    kill = [f for f in bowl if f.calc_center_median().z > 0.12]
    bmesh.ops.delete(mb.bm, geom=kill, context='FACES')
    mb.cyl((0, 0, 0.1), 0.45, 0.06, mat=0, seg=24)
    mb.cyl((0, 0, 0.07), 0.41, 0.02, mat=1, seg=24)       # glowing surface of the boiling contents
    caul = mb.build('GEO-cauldron', [M_IRON, M_POUR], parent=piv, smooth=True)
    sol = caul.modifiers.new('Solidify', 'SOLIDIFY'); sol.thickness = 0.04
    lt = bpy.data.lights.new('LGT-brazier', 'POINT'); lt.color = (1.0, 0.55, 0.22); lt.shadow_soft_size = 0.25; lt.energy = 40
    lo = bpy.data.objects.new('LGT-brazier', lt); col_root.objects.link(lo); lo.location = (px + 0.05, hy, SLAB1 + 0.55)
    # pour: a bevelled curve that grows with bevel_factor_end
    cu = bpy.data.curves.new('FX-pour', 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = 0.1; cu.bevel_resolution = 3
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(3)
    pts = [(0.5, hy, 5.62), (0.12, hy, 5.25), (0.0, hy, 4.6), (0.0, hy, 3.62)]
    for bp_, p in zip(sp.bezier_points, pts):
        bp_.co = p; bp_.handle_left_type = bp_.handle_right_type = 'AUTO'
    cu.bevel_factor_end = 0.0; cu.use_fill_caps = True
    po = bpy.data.objects.new('FX-pour', cu); col_root.objects.link(po); cu.materials.append(M_POUR)
    mb = MB(); mb.sphere((0, 0, 0), 0.5, scale=(1.0, 1.0, 0.18), seg=16)
    spl = mb.build('FX-splash', [M_POUR], smooth=True, loc=(0, hy, 3.6))
    sl = bpy.data.lights.new('LGT-splash', 'POINT'); sl.color = (1.0, 0.5, 0.15); sl.shadow_soft_size = 0.3; sl.energy = 0
    slo = bpy.data.objects.new('LGT-splash', sl); col_root.objects.link(slo); slo.location = (0.0, hy, 4.1)
    CAUL.append(dict(piv=piv, light=lt, pour=cu, pour_ob=po, splash=spl, slight=sl, y=hy))

# passage torches on the far wall (warm practicals)
TORCH_L = []
for ty in (1.2, 6.8):
    mb = MB(); mb.box(1.62, 1.8, ty - 0.06, ty + 0.06, 2.6, 2.9); mb.cyl((1.6, ty, 3.0), 0.07, 0.3, r2=0.09, seg=10)
    mb.build('GEO-torch_bracket', [M_IRON_DK], bevel=0.005)
    mb = MB(); mb.cyl((1.6, ty, 3.32), 0.09, 0.34, r2=0.0, seg=10)
    mb.build('FX-torch_flame', [M_FLAME], smooth=True)
    tl = bpy.data.lights.new('LGT-torch', 'POINT'); tl.color = (1.0, 0.6, 0.3); tl.energy = 110; tl.shadow_soft_size = 0.12
    to = bpy.data.objects.new('LGT-torch', tl); col_root.objects.link(to); to.location = (1.45, ty, 3.3)
    TORCH_L.append(tl)

# dust puffs where the portcullis lands
DUST = []
rng = random.Random(7)
for i in range(9):
    mb = MB(); mb.sphere((0, 0, 0), 1.0, seg=12)
    d = mb.build('FX-dust', [M_DUST], smooth=True)
    d.location = (-1.6 + i * 0.4, PC_Y + rng.uniform(-0.25, 0.25), 0.15)
    d.scale = (0.01, 0.01, 0.01)
    DUST.append(d)

# splinters
SPL = []
rng = random.Random(11)
for i in range(30):
    mb = MB(); L_ = rng.uniform(0.18, 0.5)
    mb.box(-0.025, 0.025, -0.02, 0.02, -L_ / 2, L_ / 2, i % 2)
    s = mb.build('GEO-splinter', [M_WOOD_A, M_WOOD_B])
    early = i < 9
    t0 = (PRE if i < 4 else HIT1) if early else W['breaks']
    v = Vector((rng.gauss(0, 1.8), rng.uniform(2.5, 7.5) if i % 4 else -rng.uniform(1.0, 3.0), rng.uniform(0.8, 4.5)))
    p0 = Vector((rng.uniform(-0.35, 0.35), FW1 + LEAF_T + 0.03, 1.7 + rng.uniform(-0.5, 0.5)))
    spin = Vector((rng.uniform(-14, 14), rng.uniform(-14, 14), rng.uniform(-8, 8)))
    SPL.append(dict(ob=s, t0=t0, v=v, p0=p0, spin=spin, r0=Vector((rng.uniform(0, 3), rng.uniform(0, 3), 0))))

# ------------------------------------------------------------------ lights (skill: sun + sky fill + warm rim; aim_at)
def aim(ob, direction):
    ob.rotation_euler = Vector(direction).normalized().to_track_quat('-Z', 'Y').to_euler()
sun = bpy.data.lights.new('LGT-key_sun', 'SUN'); sun.energy = 3.2; sun.color = (1.0, 0.95, 0.86); sun.angle = math.radians(4.0)
so = bpy.data.objects.new('LGT-key_sun', sun); col_root.objects.link(so); aim(so, (0.62, 0.42, -0.66))
rim = bpy.data.lights.new('LGT-rim_gold', 'SUN'); rim.energy = 1.4; rim.color = hexlin('#ffd9a0')[:3]; rim.angle = math.radians(6)
ro = bpy.data.objects.new('LGT-rim_gold', rim); col_root.objects.link(ro); aim(ro, (0.25, -0.75, -0.45))
fill = bpy.data.lights.new('LGT-fill_area', 'AREA'); fill.energy = 500; fill.size = 8.0; fill.color = hexlin('#bfe9ff')[:3]
fo = bpy.data.objects.new('LGT-fill_area', fill); col_root.objects.link(fo); fo.location = (-9, 3.5, 3.0); aim(fo, (1, 0, -0.05))
pf = bpy.data.lights.new('LGT-passage_fill', 'AREA'); pf.energy = 110; pf.shape = 'RECTANGLE'; pf.size = 2.6; pf.size_y = 6.0
pf.color = hexlin('#d6f1ff')[:3]
pfo = bpy.data.objects.new('LGT-passage_fill', pf); col_root.objects.link(pfo); pfo.location = (0, 4.0, 4.25)

# ------------------------------------------------------------------ camera (skill: Track-style look-at; push-ins, orbit)
cam_d = bpy.data.cameras.new('CAM-hero'); cam_d.sensor_fit = 'VERTICAL'; cam_d.sensor_height = 36.0
cam_d.clip_start = 0.05; cam_d.clip_end = 600
CAM = bpy.data.objects.new('CAM-hero', cam_d); col_root.objects.link(CAM); scene.camera = CAM

# keys: (t, position, target, focal mm). C1 Hermite through them so the move never stops between keys.
E = DUR
CK = [   # opening inside the passage (defender side, doors toward camera), out through the cut, oblique on the
         # entrance for the drop, orbit to the side for the "box", crane up over the slab for the murder holes
    (0.00, (0.55, 5.7, 1.25), (0.0, 0.0, 1.95), 19.0),
    (W['breaks'] - 0.03, (0.45, 5.2, 1.3), (0.0, 0.0, 1.9), 19.0),
    (W['gate'] - 0.2, (-0.6, 6.3, 1.8), (0.0, 1.5, 1.8), 19.0),
    (W['gate'] + 0.5, (-5.0, 6.9, 2.6), (0.0, 2.4, 2.5), 21.0),
    (W['iron'] + 0.42, (-9.0, 8.6, 3.4), (0.0, 0.6, 3.4), 23.0),
    (W['slams'] - 0.04, (-8.2, 7.8, 3.3), (0.0, 0.0, 3.2), 24.0),
    (W['sealing'] - 0.1, (-10.0, 7.4, 3.6), (0.0, 2.0, 2.8), 23.0),
    (W['box'] + 0.3, (-15.0, 3.9, 4.2), (0.0, 3.9, 3.7), 24.0),
    (W['murder'] + 0.02, (-7.4, 2.3, 9.9), (0.0, 4.0, 4.1), 24.0),
    (E, (-6.9, 2.7, 8.7), (0.0, 4.0, 3.9), 25.0),
]
def hermite(keys, t, idx):
    ts = [k[0] for k in keys]
    if t <= ts[0]: return keys[0][idx]
    if t >= ts[-1]: return keys[-1][idx]
    i = max(j for j in range(len(ts) - 1) if ts[j] <= t)
    def val(j): v = keys[j][idx]; return list(v) if isinstance(v, tuple) else [v]
    def tan(j):
        if j == 0 or j == len(ts) - 1: return [0.0] * len(val(j))
        return [(a - b) / (ts[j + 1] - ts[j - 1]) for a, b in zip(val(j + 1), val(j - 1))]
    t0, t1 = ts[i], ts[i + 1]; dt = t1 - t0; u = (t - t0) / dt
    h00 = 2 * u ** 3 - 3 * u ** 2 + 1; h10 = u ** 3 - 2 * u ** 2 + u; h01 = -2 * u ** 3 + 3 * u ** 2; h11 = u ** 3 - u ** 2
    r = [h00 * a + h10 * dt * ma + h01 * b + h11 * dt * mb for a, ma, b, mb in zip(val(i), tan(i), val(i + 1), tan(i + 1))]
    return tuple(r) if len(r) > 1 else r[0]

PC_T1 = W['slams']                # portcullis lands on the boom
SHAKES = [(HIT1, 0.55), (W['breaks'], 1.0), (PC_T1, 1.25), (PC_T1 + 0.12, 0.25)]
def shake(t):
    yaw = pitch = 0.0
    for (t0, a) in SHAKES:
        if t >= t0:
            d = t - t0; env = a * math.exp(-d / 0.16) * (1 if d < 0.6 else 0)
            yaw += env * math.radians(0.55) * math.sin(2 * math.pi * 5.2 * d + 0.3)
            pitch += env * math.radians(0.7) * math.sin(2 * math.pi * 6.1 * d + 1.1)
    return yaw, pitch

def cam_state(t):
    pos = Vector(hermite(CK, t, 1)); tgt = Vector(hermite(CK, t, 2)); lens = hermite(CK, t, 3)
    # snap zoom on "slams" (+18% in 5 frames, relax over 0.7 s)
    if t >= PC_T1: lens *= 1 + 0.18 * (ramp(t, PC_T1, PC_T1 + 5 / FPS, ease_out) - ramp(t, PC_T1 + 0.25, PC_T1 + 0.95))
    q = (tgt - pos).to_track_quat('-Z', 'Y')
    e = q.to_euler('XYZ', _PREV[0]) if _PREV[0] is not None else q.to_euler()
    _PREV[0] = e.copy()
    yaw, pitch = shake(t); e = e.copy(); e.z += yaw; e.x += pitch
    return pos, e, lens
_PREV = [None]

# ------------------------------------------------------------------ animation (every state is a pure function of t)
PC_T0 = PC_T1 - 0.24              # portcullis release; lands on the "slams" boom
def portcullis_z(t):
    if t < PC_T0: return PC_UP
    if t < PC_T1: return lerp(PC_UP, PC_DOWN, ease_in((t - PC_T0) / (PC_T1 - PC_T0)))
    d = t - PC_T1
    if d < 0.16: return PC_DOWN + 0.11 * math.sin(math.pi * d / 0.16)
    if d < 0.26: return PC_DOWN + 0.03 * math.sin(math.pi * (d - 0.16) / 0.10)
    return PC_DOWN

TH_HIT = 0.26
def ram_theta(t):
    if t < HIT1: return 0.2 + (TH_HIT + 0.07 - 0.2) * (t / HIT1)            # frame 0: ram already driving in (unseen)
    if t < 0.85: return TH_HIT + 0.07 - (TH_HIT + 0.07 + 0.5) * math.sin(math.pi / 2 * clamp((t - HIT1) / (0.85 - HIT1)))
    if t < W['breaks']: return -0.5 + (TH_HIT + 0.5) * (1 - math.cos(math.pi / 2 * (t - 0.85) / (W['breaks'] - 0.85)))
    d = t - W['breaks']
    if d < 0.3: return TH_HIT + 0.16 * math.sin(math.pi / 2 * d / 0.3)
    return 0.42 * math.exp(-(d - 0.3) / 0.55) * math.cos(2 * math.pi * (d - 0.3) / 1.6)

SHED_Y0 = -(TIP + ROPE_L * math.sin(TH_HIT))   # ram tip touches the gate's outer face at impact
SHED_Y1 = 4.3
ROLL0, ROLL1 = W['breaks'] + 0.07, W['slams'] - 0.45
def shed_y(t):
    if t < ROLL0: return SHED_Y0
    return lerp(SHED_Y0, SHED_Y1, smoother((t - ROLL0) / (ROLL1 - ROLL0)))

def leaf_angle(t):
    if t < W['breaks']:
        d0 = t - PRE
        pre = 0.05 * math.exp(-d0 / 0.12) * math.cos(2 * math.pi * 3.5 * d0)
        d = t - HIT1
        if d < 0: return pre
        return pre + 0.075 * math.exp(-d / 0.16) * abs(math.sin(math.pi * d / 0.22) if d < 0.22 else 0.0) + \
               0.02 * math.exp(-d / 0.2) * math.sin(2 * math.pi * 6 * d) * (d >= 0.22)
    d = t - W['breaks']
    if d < 0.2: return math.radians(89) * ease_out(d / 0.2)
    return math.radians(89) - math.radians(10) * math.exp(-(d - 0.2) / 0.12) * abs(math.sin(math.pi * (d - 0.2) / 0.3))

def bar_pose(t, s):
    p0 = Vector((s * 0.88, FW1 + LEAF_T + 0.12, 1.55)); p2 = Vector((s * 1.55, 1.9 + (0.25 if s > 0 else -0.1), 0.12))
    p1 = Vector((s * 1.35, 1.0, 2.6))
    if t < W['breaks']: return p0, Euler((0, 0, 0))
    u = clamp((t - W['breaks']) / 0.55)
    p = (1 - u) ** 2 * p0 + 2 * (1 - u) * u * p1 + u * u * p2
    ue = ease_out(u)
    return p, Euler((s * 2 * math.pi * ue + 0.0, 0.15 * s * ue, math.pi / 2 * ue * s))

def splinter_pose(sp, t):
    d = t - sp['t0']
    if d < 0: return None
    g = Vector((0, 0, -9.8))
    p = sp['p0'] + sp['v'] * d + 0.5 * g * d * d
    if p.z < 0.03:
        # time of ground contact; freeze there
        a, b, c = 0.5 * g.z, sp['v'].z, sp['p0'].z - 0.03
        dl = (-b - math.sqrt(max(0, b * b - 4 * a * c))) / (2 * a)
        p = sp['p0'] + sp['v'] * dl + 0.5 * g * dl * dl; p.z = 0.03; d = dl
    r = sp['r0'] + sp['spin'] * d
    return p, Euler((r.x, r.y, r.z))

CUT0 = W['gate'] - 0.2                # the near half is sliced away while the camera backs out
def key_all():
    for f in range(1, NF + 1):
        t = tf(f)
        pos, e, lens = cam_state(t)
        CAM.location = pos; CAM.rotation_euler = e; cam_d.lens = lens
        CAM.keyframe_insert('location', frame=f); CAM.keyframe_insert('rotation_euler', frame=f); cam_d.keyframe_insert('lens', frame=f)
        # shed, wheels, ram, ropes
        y = shed_y(t); SHED.location = (0, y, 0); SHED.keyframe_insert('location', frame=f)
        for wh in WHEELS:
            wh.rotation_euler = (-(y - SHED_Y0) / WR, 0, 0); wh.keyframe_insert('rotation_euler', frame=f)
        th = ram_theta(t)
        RAM.location = (0, PIV_Y + ROPE_L * math.sin(th), PIV_Z - ROPE_L * math.cos(th)); RAM.keyframe_insert('location', frame=f)
        for rp in ROPES:
            rp.rotation_euler = (th, 0, 0); rp.keyframe_insert('rotation_euler', frame=f)
        a = leaf_angle(t)
        HINGE_L.rotation_euler = (0, 0, a); HINGE_R.rotation_euler = (0, 0, -a)
        HINGE_L.keyframe_insert('rotation_euler', frame=f); HINGE_R.keyframe_insert('rotation_euler', frame=f)
        if t < W['breaks'] + 0.7:
            for s, ob in zip((-1, 1), BAR_PIECES):
                p, r = bar_pose(t, s); ob.location = p; ob.rotation_euler = r
                ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_euler', frame=f)
        PORT_O.location.z = portcullis_z(t); PORT_O.keyframe_insert('location', index=2, frame=f)
        # cutaway: the cutter box drops through the near half on "an iron"
        CUTTER.location.z = lerp(17.0, -0.6, ramp(t, CUT0, CUT0 + 0.42, ease_in)); CUTTER.keyframe_insert('location', index=2, frame=f)
        # splinters
        if t < 3.6:
            for sp in SPL:
                pr = splinter_pose(sp, t)
                ob = sp['ob']
                if pr is None:
                    ob.hide_render = True
                else:
                    ob.hide_render = False; ob.location, ob.rotation_euler = pr
                ob.keyframe_insert('hide_render', frame=f)
                ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_euler', frame=f)
        # dust puffs on landing
        if PC_T1 - 0.1 < t < PC_T1 + 1.0:
            for i, d in enumerate(DUST):
                u = clamp((t - PC_T1) / 0.8)
                s_ = 0.01 if t < PC_T1 else 0.15 + 0.55 * ease_out(u) * (0.8 + 0.4 * ((i * 37) % 10) / 10)
                d.scale = (s_ * 1.3, s_, s_ * 0.8)
                d.location.z = 0.15 + 0.5 * ease_out(u)
                d.keyframe_insert('scale', frame=f); d.keyframe_insert('location', frame=f)
        DUST_B.inputs['Alpha'].default_value = 0.0 if t < PC_T1 else 0.75 * (1 - ramp(t, PC_T1 + 0.1, PC_T1 + 0.85))
        DUST_B.inputs['Alpha'].keyframe_insert('default_value', frame=f)
        # signal glows (meaning-locked): green = the thing being named, cyan = seal, orange = heat
        tag = ramp(t, W['portcullis'] - 0.05, W['portcullis'] + 0.12) * (1 - ramp(t, PC_T1 + 0.35, PC_T1 + 0.7))
        TAG_MIX.inputs[0].default_value = tag; TAG_MIX.inputs[0].keyframe_insert('default_value', frame=f)
        TAG.hide_render = tag < 0.01; TAG.keyframe_insert('hide_render', frame=f)
        seal = ramp(t, W['sealing'] - 0.05, W['sealing'] + 0.15) * (1 - ramp(t, W['stone'] - 0.2, W['stone'] + 0.1))
        seal *= 0.75 + 0.25 * math.cos(2 * math.pi * 2.0 * (t - W['sealing']))
        SEAL_MIX.inputs[0].default_value = seal; SEAL_MIX.inputs[0].keyframe_insert('default_value', frame=f)
        SEAL.hide_render = seal < 0.01; SEAL.keyframe_insert('hide_render', frame=f)
        bx = ramp(t, W['stone'] - 0.05, W['stone'] + 0.15) * (1 - ramp(t, W['ceiling'] + 0.1, W['ceiling'] + 0.4))
        BOX_MIX.inputs[0].default_value = bx; BOX_MIX.inputs[0].keyframe_insert('default_value', frame=f)
        BOXTAG.hide_render = bx < 0.01; BOXTAG.keyframe_insert('hide_render', frame=f)
        ht = ramp(t, W['murder'] - 0.05, W['murder'] + 0.1) * (1 - ramp(t, W['murder'] + 0.9, W['murder'] + 1.2))
        HTAG_MIX.inputs[0].default_value = ht; HTAG_MIX.inputs[0].keyframe_insert('default_value', frame=f)
        HOLETAG.hide_render = ht < 0.01; HOLETAG.keyframe_insert('hide_render', frame=f)
        LEAF_L.hide_render = t > CUT0 + 0.22; LEAF_L.keyframe_insert('hide_render', frame=f)   # sliced away with the near wall
        heat = ramp(t, W['murder'] - 0.35, W['murder'] + 0.2)
        COAL_EM.inputs['Strength'].default_value = 1.2 + 2.8 * heat; COAL_EM.inputs['Strength'].keyframe_insert('default_value', frame=f)
        for k, c in enumerate(CAUL):
            c['light'].energy = 30 + 150 * heat; c['light'].keyframe_insert('energy', frame=f)
            tip0 = W['murder'] + 0.05 + 0.12 * k
            c['piv'].rotation_euler = (0, -math.radians(64) * ramp(t, tip0, tip0 + 0.4, smoother), 0)
            c['piv'].keyframe_insert('rotation_euler', frame=f)
            pour = ramp(t, tip0 + 0.22, tip0 + 0.62, ease_in)
            c['pour'].bevel_factor_end = pour; c['pour'].keyframe_insert('bevel_factor_end', frame=f)
            c['pour_ob'].hide_render = pour < 0.005; c['pour_ob'].keyframe_insert('hide_render', frame=f)
            sp_ = ramp(t, tip0 + 0.6, tip0 + 1.1, ease_out)
            c['splash'].scale = (0.05 + 1.1 * sp_, 0.05 + 1.5 * sp_, 0.05 + 1.0 * sp_)
            c['splash'].keyframe_insert('scale', frame=f)
            c['splash'].hide_render = sp_ < 0.01; c['splash'].keyframe_insert('hide_render', frame=f)
            c['slight'].energy = 160 * sp_ + 60 * pour; c['slight'].keyframe_insert('energy', frame=f)
        for i, tl in enumerate(TORCH_L):
            tl.energy = 110 + 18 * math.sin(t * 13.0 + i * 2) + 10 * math.sin(t * 29 + i); tl.keyframe_insert('energy', frame=f)
key_all()

# ------------------------------------------------------------------ render settings (skill Recipe 3 EEVEE preset, 4.3 names)
r = scene.render
scene.render.engine = 'BLENDER_EEVEE_NEXT'
ee = scene.eevee
ee.taa_render_samples = A.samples
ee.shadow_pool_size = '1024'; ee.use_shadows = True; ee.shadow_ray_count = 2; ee.shadow_step_count = 6
if not A.nort:
    ee.use_raytracing = True; ee.ray_tracing_method = 'SCREEN'
    ee.ray_tracing_options.resolution_scale = '2'
    ee.use_fast_gi = True; ee.fast_gi_method = 'GLOBAL_ILLUMINATION'; ee.fast_gi_distance = 2.5
    ee.fast_gi_resolution = '2'; ee.fast_gi_quality = 0.5
ee.use_gtao = True; ee.gtao_distance = 1.2
r.use_motion_blur = not A.nomb; r.motion_blur_shutter = 0.35
r.resolution_x, r.resolution_y, r.resolution_percentage = 1080, 1920, A.pct
r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.image_settings.compression = 15
r.film_transparent = False
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0.0
# compositor bloom (EEVEE Next has no use_bloom; 4.3 Glare node glare_type BLOOM)
scene.use_nodes = True
cnt = scene.node_tree
for n in list(cnt.nodes): cnt.nodes.remove(n)
rl = cnt.nodes.new('CompositorNodeRLayers'); gl = cnt.nodes.new('CompositorNodeGlare'); co = cnt.nodes.new('CompositorNodeComposite')
gl.glare_type = 'BLOOM'; gl.quality = 'HIGH'; gl.threshold = 1.0; gl.size = 7; gl.mix = 0.0
cnt.links.new(rl.outputs['Image'], gl.inputs['Image']); cnt.links.new(gl.outputs['Image'], co.inputs['Image'])

print(f'[build] scene ready in {time.time() - T0:.1f}s, objects={len(bpy.data.objects)}', flush=True)
if A.save: bpy.ops.wm.save_as_mainfile(filepath=A.save)

# ------------------------------------------------------------------ render
def render_frame(f, path):
    scene.frame_set(f)
    r.filepath = path
    t = time.time(); bpy.ops.render.render(write_still=True)
    return time.time() - t

if A.look:
    f = A.look; scene.frame_set(f)
    c = Vector((0, 3.5, 4.0))
    cam_d.animation_data_clear(); CAM.animation_data_clear()
    for i, (az, el, dist) in enumerate(((-90, 15, 26), (-45, 25, 28), (-150, 20, 26), (180, 10, 28), (-90, 70, 30))):
        a, e_ = math.radians(az), math.radians(el)
        CAM.location = c + Vector((math.cos(a) * math.cos(e_), math.sin(a) * math.cos(e_), math.sin(e_))) * dist
        CAM.rotation_euler = (c - CAM.location).to_track_quat('-Z', 'Y').to_euler(); cam_d.lens = 24
        dt = render_frame(f, os.path.join(OUT, f'look_f{f:03d}_{i}.png'))
        print(f'[look] {i} az{az} el{el} {dt:.1f}s', flush=True)
else:
    tot = 0.0; frames = parse_frames(A.frames)
    for f in frames:
        dt = render_frame(f, os.path.join(OUT, f'{f:04d}.png')); tot += dt
        print(f'[frame] {f} t={tf(f):.2f}s render {dt:.2f}s', flush=True)
    print(f'[render] {len(frames)} frames, {tot:.1f}s, {tot / max(1, len(frames)):.2f}s/frame', flush=True)
