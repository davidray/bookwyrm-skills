"""Neutral grey Cycles renders of generated meshes at print scale, with close-ups, for judging detail.

Judge image-to-3D results with real renders like these (or a slicer preview), never a point-cloud or a
numeric smoothness score: both made a clear improvement look like a tie. Every model is scaled to the
same height so close-ups compare like with like.

usage (headless bpy): CLOSE='[["face",0.5,0.5,0.86,0.5,0], ...]' \
  python render_closeups.py -- OUTDIR HEIGHT_MM nameA=a.glb nameB=b.glb
  CLOSE   list of [label, u, v, w, dist, azimuth]: target at normalized bounding-box coords (u, v, w),
          camera dist as a fraction of HEIGHT_MM, azimuth in radians (0 = front, pi = back)
  SAMPLES Cycles samples (default 48); RES square image size (default 900)
Writes OUTDIR/<name>_{front,threeq,back,top}.png, <name>_close_<label>.png and a summary JSON
(raw height in source units, print dims in mm, face count)."""
import bpy, sys, os, math, json
from mathutils import Vector
argv = sys.argv[sys.argv.index('--')+1:]
OUT, HMM = argv[0], float(argv[1]); items = [a.split('=', 1) for a in argv[2:]]
CLOSE = json.loads(os.environ.get('CLOSE', '[]'))   # list of [label, u, v, w, frac] in normalized bbox coords + view az
os.makedirs(OUT, exist_ok=True)
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene; s.render.engine = 'CYCLES'; s.cycles.samples = int(os.environ.get('SAMPLES', 48)); s.cycles.use_denoising = True
    s.cycles.device = 'CPU'; s.render.resolution_x = s.render.resolution_y = int(os.environ.get('RES', 900))
    s.unit_settings.scale_length = 0.001
    w = bpy.data.worlds.new('w'); s.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.9, 0.9, 0.92, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.12
    s.view_settings.view_transform = 'Standard'
    return s
def load(path):
    bpy.ops.import_scene.gltf(filepath=path)
    obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in bpy.context.scene.objects: o.select_set(o in obs)
    bpy.context.view_layer.objects.active = obs[0]
    if len(obs) > 1: bpy.ops.object.join()
    o = bpy.context.view_layer.objects.active
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM'); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for e in [x for x in bpy.context.scene.objects if x.type != 'MESH']: bpy.data.objects.remove(e)
    me = o.data; vs = [v.co for v in me.vertices]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs))); mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    raw_h = mx.z - mn.z; k = HMM / raw_h; c = (mn + mx) / 2
    for v in me.vertices: v.co = Vector(((v.co.x-c.x)*k, (v.co.y-c.y)*k, (v.co.z-mn.z)*k))
    me.update(); o.data.materials.clear()
    m = bpy.data.materials.new('grey'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.55, 0.55, 0.57, 1); b.inputs['Roughness'].default_value = 0.6; o.data.materials.append(m)
    for p in me.polygons: p.use_smooth = False
    dims = [(mx[i]-mn[i])*k for i in range(3)]
    return o, raw_h, dims, len(me.polygons)
def cam_light(s, target, dist, az, el, lens=50, ortho=None):
    for x in [x for x in s.objects if x.type in ('CAMERA', 'LIGHT')]: bpy.data.objects.remove(x)
    t = Vector(target); d = Vector((math.cos(el)*math.sin(az), -math.cos(el)*math.cos(az), math.sin(el)))
    cd = bpy.data.cameras.new('c'); cd.lens = lens; cd.clip_start = 0.1; cd.clip_end = 5000
    if ortho: cd.type = 'ORTHO'; cd.ortho_scale = ortho
    co = bpy.data.objects.new('c', cd); s.collection.objects.link(co); s.camera = co
    co.location = t + d*dist; co.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    for nm, a2, e2, en, sz in [('key', az+1.1, 0.55, 0.55e6, 0.02), ('fill', az-1.4, 0.25, 0.08e6, 0.4), ('rim', az+math.pi, 0.8, 0.25e6, 0.1)]:
        ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = en * (dist/300)**2; ld.size = sz*dist
        lo = bpy.data.objects.new(nm, ld); s.collection.objects.link(lo)
        dd = Vector((math.cos(e2)*math.sin(a2), -math.cos(e2)*math.cos(a2), math.sin(e2)))
        lo.location = t + dd*dist*1.5; lo.rotation_euler = (-dd).to_track_quat('-Z', 'Y').to_euler()
summary = {}
for name, path in items:
    s = reset(); o, raw_h, dims, nf = load(path)
    summary[name] = dict(raw_height_units=raw_h, dims_mm=dims, faces=nf)
    H = HMM; R = max(dims)
    for vn, az, el in [('front', 0, 0.12), ('threeq', 0.8, 0.3), ('back', math.pi, 0.12), ('top', 0, 1.45)]:
        cam_light(s, (0, 0, H*0.5 if vn != 'top' else 0), max(H, dims[0], dims[1] if vn == 'top' else 0)*2.5, az, el)
        s.render.filepath = f'{OUT}/{name}_{vn}.png'; bpy.ops.render.render(write_still=True)
    for lab, u, v, w, frac, az in CLOSE:
        tgt = ((u-0.5)*dims[0], (v-0.5)*dims[1], w*dims[2])
        cam_light(s, tgt, H*frac, az, 0.15, lens=50)
        s.render.filepath = f'{OUT}/{name}_close_{lab}.png'; bpy.ops.render.render(write_still=True)
json.dump(summary, open(f'{OUT}/summary-{"-".join(n for n,_ in items)}.json', 'w'), indent=1); print(summary)
