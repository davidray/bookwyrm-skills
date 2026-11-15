import bpy, sys, json, math, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import room, lantern
from mathutils import Vector
argv=sys.argv[sys.argv.index('--')+1:]
spec=json.load(open(argv[0])); shots=argv[1].split(','); samples=int(argv[2]); res=argv[3]; outdir=argv[4]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
room.world(0.05)
oil=room.build_room()
TABLE=(0.15,0.75,0.551)
root=bpy.data.objects.new('lantern',None); sc.collection.objects.link(root); root.location=TABLE
root.rotation_euler=(0,0,math.radians(spec.get('rotz',160)))
M=lantern.mk_mats()
lantern.place_parts(spec['dir'],spec['parts']+spec.get('stl_parts',[]),M,root)
for fr in spec.get('frames',[]):
    w,h,t=fr['w'],fr['h'],fr['t']; x0,x1,z0,z1=fr['open']
    rects=[(-w/2,x0,0,h),(x1,w/2,0,h),(x0,x1,0,z0),(x0,x1,z1,h)]
    for a in fr['angles']:
        for (ax0,ax1,az0,az1) in rects:
            if ax1-ax0<0.01 or az1-az0<0.01: continue
            cx=(ax0+ax1)/2; cy=fr['apothem_in']+t/2; cz=fr['z0']+(az0+az1)/2
            ar=math.radians(a-90); X=cx*math.cos(ar)-cy*math.sin(ar); Y=cx*math.sin(ar)+cy*math.cos(ar)
            b=room.box('acr',((ax1-ax0)/1000,t/1000,(az1-az0)/1000),(X/1000,Y/1000,cz/1000),M[fr.get('mat','acrylic')],rot=(0,0,ar))
            b.parent=root
L=spec['leds']
for a in L['angles']:
    ar=math.radians(a); x=L['r']*math.cos(ar); y=L['r']*math.sin(ar)
    lantern.led_lights(root,L['z0'],L['z1'],n=L['n'],power=L['power'],xy=(x,y),radius=0.008)
for o in L.get('extra',[]):
    lantern.led_lights(root,o['z0'],o['z1'],n=o.get('n',2),power=o['power'],xy=tuple(o['xy']),radius=0.004)
# room practical lights
def light(name,typ,loc,energy,color,size=0.1,rot=None):
    ld=bpy.data.lights.new(name,typ); ld.energy=energy; ld.color=color
    if typ=='AREA': ld.size=size
    else: ld.shadow_soft_size=size
    o=bpy.data.objects.new(name,ld); sc.collection.objects.link(o); o.location=loc
    if rot: o.rotation_euler=rot
    return o
light('oil_lamp','POINT',(-2.1,-0.15,1.12),25,(1.0,0.62,0.32),0.03)
light('fill','AREA',(0.6,-1.2,2.6),5,(1.0,0.85,0.7),1.2)
light('reading','POINT',(-1.75,1.25,1.45),35,(1.0,0.7,0.42),0.12)
light('shelf_wash','AREA',(0.0,1.2,2.65),22,(1.0,0.8,0.6),3.0)
H=spec['height']/1000; W=spec['width']/1000
tgt=Vector(TABLE)+Vector((0,0,H*0.5))
cams={
 'wide':  dict(lens=28, pos=Vector((1.55,-1.75,1.25)), tgt=Vector((-0.25,1.0,0.75))),
 'front34': dict(lens=55, pos=tgt+Vector((0.55,-1.25,0.22))*max(0.45,H/0.4), tgt=tgt),
 'back34': dict(lens=55, pos=tgt+Vector((-0.65,-1.2,0.30))*max(0.45,H/0.4), tgt=tgt, turn=180),
 'close': dict(lens=85, pos=tgt+Vector((0.25,-1.0,0.12))*max(0.45,H/0.4), tgt=tgt+Vector((0,0,0.0))),
 'high':  dict(lens=50, pos=tgt+Vector((0.9,-0.9,0.75))*max(0.45,H/0.4), tgt=tgt+Vector((0,0,-0.03))),
}
r=sc.render; r.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=samples; sc.cycles.use_denoising=True
sc.cycles.use_adaptive_sampling=True; sc.cycles.adaptive_threshold=0.015
sc.cycles.max_bounces=8; r.use_persistent_data=True; sc.cycles.transparent_max_bounces=8
w,h=map(int,res.split('x')); r.resolution_x=w; r.resolution_y=h; r.resolution_percentage=100
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast' if 'AgX - Medium High Contrast' in [l for l in []] else 'None'
sc.view_settings.exposure=float(spec.get('exposure',0.0))
r.image_settings.file_format='JPEG'; r.image_settings.quality=90
base_rot=root.rotation_euler.z
for s in shots:
    c=cams[s]
    cd=bpy.data.cameras.new(s); cd.lens=c['lens']; cd.sensor_width=36
    co=bpy.data.objects.new(s,cd); sc.collection.objects.link(co); co.location=c['pos']; room.look_at(co,c['tgt'])
    if s!='wide':
        cd.dof.use_dof=True; cd.dof.focus_distance=(c['pos']-c['tgt']).length; cd.dof.aperture_fstop=4.0
    root.rotation_euler.z=base_rot+math.radians(c.get('turn',0))
    sc.camera=co; r.filepath=os.path.join(outdir,f"{spec['slug']}_{s}.jpg")
    bpy.ops.render.render(write_still=True); print('WROTE',r.filepath,flush=True)
