import bpy, math, random, os, glob
from mathutils import Vector, Euler, Matrix
A=os.environ.get('ROOM_ASSETS','/home/user/r/room/assets')
def look_at(obj, target):
    d=Vector(target)-obj.location; obj.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
def imp(name, loc=(0,0,0), rotz=0.0, scale=1.0):
    g=glob.glob(f'{A}/models/{name}/*.gltf')[0]
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=g)
    new=[o for o in bpy.data.objects if o not in before]
    root=bpy.data.objects.new(name+'_root',None); bpy.context.scene.collection.objects.link(root)
    for o in new:
        if o.parent is None: o.parent=root
    root.location=loc; root.rotation_euler=(0,0,rotz); root.scale=(scale,)*3
    return root,new
def pbr(name, folder, scale=1.0, disp=False, tint=None):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; N=nt.nodes; L=nt.links
    b=N['Principled BSDF']
    tc=N.new('ShaderNodeTexCoord'); mp=N.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value=(scale,scale,scale)
    L.new(tc.outputs['UV'],mp.inputs['Vector'])
    fs=glob.glob(f'{A}/textures/{folder}/*')
    def tex(key,cs='Non-Color'):
        f=[x for x in fs if key in os.path.basename(x)]
        if not f: return None
        t=N.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(f[0]); t.image.colorspace_settings.name=cs
        L.new(mp.outputs['Vector'],t.inputs['Vector']); return t
    d=tex('_diff_','sRGB') or tex('_col_','sRGB') or tex('_albedo_','sRGB')
    if d:
        if tint:
            mx=N.new('ShaderNodeMix'); mx.data_type='RGBA'; mx.blend_type='MULTIPLY'; mx.inputs['Factor'].default_value=1
            L.new(d.outputs['Color'],mx.inputs[6]); mx.inputs[7].default_value=tint+(1,); L.new(mx.outputs[2],b.inputs['Base Color'])
        else: L.new(d.outputs['Color'],b.inputs['Base Color'])
    r=tex('_rough_')
    if r: L.new(r.outputs['Color'],b.inputs['Roughness'])
    n=tex('_nor_gl_')
    if n:
        nm=N.new('ShaderNodeNormalMap'); L.new(n.outputs['Color'],nm.inputs['Color']); L.new(nm.outputs['Normal'],b.inputs['Normal'])
    return m
def plane(name, size, loc, rot, mat, uv_scale=1):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; o.scale=(size[0],size[1],1)
    bpy.ops.object.transform_apply(scale=True)
    # UVs in metres
    me=o.data
    for loop in me.loops:
        v=me.vertices[loop.vertex_index].co
        me.uv_layers.active.data[loop.index].uv=(v.x,v.y)
    o.data.materials.append(mat); return o
def box(name, dims, loc, mat, rot=(0,0,0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; o.scale=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel>0:
        mod=o.modifiers.new('bev','BEVEL'); mod.width=bevel; mod.segments=2
    if mat: o.data.materials.append(mat)
    return o
def simple_mat(name, color, rough=0.6, sheen=0.0, metal=0.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=tuple(color)+(1,) if len(color)==3 else color
    b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    if sheen: b.inputs['Sheen Weight'].default_value=sheen
    return m
BOOK_COLS0=[(0.28,0.04,0.03),(0.12,0.18,0.10),(0.06,0.08,0.16),(0.30,0.18,0.08),(0.45,0.38,0.26),(0.18,0.06,0.04),(0.05,0.12,0.10),(0.35,0.08,0.05),(0.10,0.07,0.05),(0.55,0.50,0.40),(0.20,0.20,0.22),(0.40,0.26,0.10)]
BOOK_COLS=None
def book_mats():
    global BOOK_COLS; BOOK_COLS=[tuple(min(1,c*1.2) for c in col) for col in BOOK_COLS0]
    ms=[]
    for i,c in enumerate(BOOK_COLS):
        m=bpy.data.materials.new(f'book{i}'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
        # spine bands via object-space gradient
        tc=nt.nodes.new('ShaderNodeTexCoord'); sep=nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Generated'],sep.inputs[0])
        ramp=nt.nodes.new('ShaderNodeValToRGB'); nt.links.new(sep.outputs['Z'],ramp.inputs[0])
        cr=ramp.color_ramp; cr.interpolation='CONSTANT'
        gold=(0.55,0.40,0.15,1); base=tuple(c)+(1,)
        cr.elements[0].position=0; cr.elements[0].color=base; cr.elements[1].position=0.08; cr.elements[1].color=base
        for p,col in ((0.10,gold),(0.12,base),(0.85,gold),(0.875,base)):
            e=cr.elements.new(p); e.color=col
        mix=nt.nodes.new('ShaderNodeMix'); mix.data_type='RGBA'; mix.inputs['Factor'].default_value=0.0 if i%3==0 else 1.0
        mix.inputs[6].default_value=base; nt.links.new(ramp.outputs['Color'],mix.inputs[7]); nt.links.new(mix.outputs[2],b.inputs['Base Color'])
        b.inputs['Roughness'].default_value=0.55; b.inputs['Sheen Weight'].default_value=0.2
        ms.append(m)
    pages=simple_mat('pages',(0.75,0.70,0.58),0.8); return ms,pages
def fill_shelf(x0,x1,z,depth_y,face_sign,rng,mats,pages,maxh=0.25):
    x=x0
    while x<x1-0.03:
        if rng.random()<0.07:  # gap / leaning or stack
            if rng.random()<0.5 and x1-x>0.25:
                # horizontal stack
                hz=z; w=rng.uniform(0.17,0.24)
                for k in range(rng.randint(2,5)):
                    t=rng.uniform(0.025,0.05); box('bk',(w,rng.uniform(0.14,0.2),t),(x+w/2,depth_y,hz+t/2),rng.choice(mats),rot=(0,0,rng.uniform(-.05,.05)),bevel=0.002); hz+=t
                x+=w+0.02; continue
            x+=rng.uniform(0.03,0.08); continue
        t=rng.uniform(0.022,0.05); h=rng.uniform(0.17,maxh); d=rng.uniform(0.13,0.2)
        b=box('bk',(t,d,h),(x+t/2,depth_y+face_sign*(0.1-d/2)*0.0,z+h/2),rng.choice(mats),bevel=0.002)
        b.location.y=depth_y - face_sign*(d/2) + face_sign*0.235
        x+=t+0.001
def world(strength=0.03, color=(0.35,0.42,0.6)):
    w=bpy.data.worlds.new('w'); bpy.context.scene.world=w; w.use_nodes=True
    bg=w.node_tree.nodes['Background']; bg.inputs[0].default_value=color+(1,); bg.inputs[1].default_value=strength
def build_room(seed=3):
    rng=random.Random(seed)
    sc=bpy.context.scene
    floor=pbr('parquet','herringbone_parquet',scale=0.6); wall=pbr('plaster','painted_plaster_wall',scale=0.4,tint=(0.62,0.55,0.45))
    panel=pbr('panel','dark_paneled_wood',scale=0.6); rug=pbr('rug','quatrefoil_jacquard_fabric',scale=1.2,tint=(0.55,0.18,0.12))
    plane('floor',(8,8),(0,0,0),(0,0,0),floor)
    plane('wall_back',(8,3),(0,2.3,1.5),(math.radians(90),0,0),wall)
    plane('wall_left',(8,3),(-2.6,0,1.5),(math.radians(90),0,math.radians(90)),wall)
    plane('wall_right',(8,3),(2.6,0,1.5),(math.radians(90),0,math.radians(-90)),wall)
    plane('ceiling',(8,8),(0,0,2.75),(math.radians(180),0,0),simple_mat('ceil',(0.7,0.68,0.62),0.9))
    plane('wall_front',(8,3),(0,-3.2,1.5),(math.radians(-90),0,0),wall)
    # wainscot on side walls
    plane('wains_l',(8,0.9),(-2.59,0,0.45),(math.radians(90),0,math.radians(90)),panel)
    plane('wains_r',(8,0.9),(2.59,0,0.45),(math.radians(90),0,math.radians(-90)),panel)
    r=plane('rug',(2.4,1.7),(0.1,0.6,0.004),(0,0,0),rug)
    # bookshelves on back wall
    mats,pages=book_mats()
    shelves_z=[0.1,0.39,0.67,0.96,1.27,1.66]
    for i,sx in enumerate((-1.85,-0.45,0.95,2.35)):
        root,_=imp('wooden_bookshelf_worn',(sx,2.0,0),0.0)
        for j,z in enumerate(shelves_z):
            if rng.random()<0.12 and j>0: continue
            seg=rng.random()
            x0,x1=sx-0.6,sx+0.6
            if seg<0.3: x1=sx+rng.uniform(0.1,0.4)
            fill_shelf(x0,x1,z+0.015,2.0,-1,rng,mats,pages,maxh=min(0.26,(shelves_z[j+1]-z-0.04) if j+1<len(shelves_z) else 0.3))
        if i in (0,2):
            imp('book_encyclopedia_set_01',(sx-0.55,1.80,0.96+0.015),math.pi*0+0.0)
        if i==1:
            imp('mantel_clock_01',(sx+0.38,1.98,1.66+0.015),math.pi)
        if i==2:
            imp('antique_ceramic_vase_01',(sx+0.42,1.98,1.27+0.015),0,0.6)
    # furniture
    imp('mid_century_lounge_chair',(-1.15,0.75,0),math.radians(-35))
    imp('side_table_01',(0.15,0.75,0),math.radians(5))
    imp('potted_plant_02',(2.1,1.2,0),0.4)
    imp('wooden_table_02',(-2.1,-0.4,0),math.radians(90))
    lamp,new=imp('vintage_oil_lamp',(-2.1,-0.15,0.8),0)
    return lamp
