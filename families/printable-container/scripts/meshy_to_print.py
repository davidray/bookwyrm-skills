"""Scale a raw Meshy GLB to print size: Z-up, feet on the plate, optional flat-bottom cut and round base, STL out.

Meshy's raw output is in arbitrary units (figures come in about 1.9 units tall). This script fixes scale and
placement only; it does not repair or thicken anything.

usage (headless bpy, e.g. `pip install bpy`):
  python meshy_to_print.py IN.glb OUT.stl --height 32 [--cut 0.4] [--base-d 25 --base-h 3]
  --height  target height in mm of the figure (plus Meshy's own base), after the cut; an added base adds base-h - 0.3
  --cut     mm to slice off the bottom so it sits flat on the plate (0 to skip), default 0.4
  --base-d  diameter of a plain cylinder base to union under the figure, mm (0 = none; keep Meshy's own base)
  --base-h  base height in mm, default 3
"""
import argparse, sys
import bpy, bmesh
from mathutils import Vector

ap = argparse.ArgumentParser()
ap.add_argument('inp'); ap.add_argument('out')
ap.add_argument('--height', type=float, default=32.0)
ap.add_argument('--cut', type=float, default=0.4)
ap.add_argument('--base-d', type=float, default=0.0)
ap.add_argument('--base-h', type=float, default=3.0)
a = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a.inp)          # importer converts glTF Y-up to Blender Z-up
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
for o in bpy.context.scene.objects:
    o.select_set(o in meshes)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

bm = bmesh.new(); bm.from_mesh(ob.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)   # Meshy splits the mesh along UV islands
zs = [v.co.z for v in bm.verts]; raw_h = max(zs) - min(zs)
xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]
cx, cy, z0 = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, min(zs)
k = (a.height + max(a.cut, 0)) / raw_h   # height measured after the flat-bottom cut
for v in bm.verts:
    v.co = Vector(((v.co.x - cx) * k, (v.co.y - cy) * k, (v.co.z - z0) * k))
if a.cut > 0:
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    r = bmesh.ops.bisect_plane(bm, geom=geom, plane_co=(0, 0, a.cut), plane_no=(0, 0, 1), clear_inner=True)
    edges = [e for e in r['geom_cut'] if isinstance(e, bmesh.types.BMEdge)]
    bmesh.ops.holes_fill(bm, edges=edges)
    for v in bm.verts:
        v.co.z -= a.cut
bm.to_mesh(ob.data); bm.free(); ob.data.update()
print(f'raw height {raw_h:.4g} units -> scale x{k:.5g}')

if a.base_d > 0:
    for v in ob.data.vertices:
        v.co.z += a.base_h - 0.3                       # sink figure 0.3 mm into the base
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=a.base_d / 2, depth=a.base_h, location=(0, 0, a.base_h / 2))
    base = bpy.context.active_object
    m = ob.modifiers.new('base', 'BOOLEAN'); m.operation = 'UNION'; m.object = base; m.solver = 'MANIFOLD'
    bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier='base')
    bpy.data.objects.remove(base)

for o in bpy.context.scene.objects:
    o.select_set(o == ob)
bpy.ops.wm.stl_export(filepath=a.out, export_selected_objects=True, global_scale=1.0, apply_modifiers=True)
print('wrote', a.out, 'dims mm', tuple(round(d, 2) for d in ob.dimensions))
