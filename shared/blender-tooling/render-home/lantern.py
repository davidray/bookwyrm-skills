import bpy, numpy as np, math, sys, json, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import tmf, lithomat, stlbb
from mathutils import Matrix, Vector
def mk_mats():
    M={}
    def principled(name,col,rough,ss=0.0,ssr=(1,1,1),sss=0.001,trans=0.0,coat=0.0):
        m=bpy.data.materials.new(name); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value=col+(1,); b.inputs['Roughness'].default_value=rough
        if ss: 
            b.inputs['Subsurface Weight'].default_value=ss; b.inputs['Subsurface Radius'].default_value=ssr; b.inputs['Subsurface Scale'].default_value=sss
            m.node_tree.nodes['Principled BSDF'].subsurface_method='RANDOM_WALK'
        if coat: b.inputs['Coat Weight'].default_value=coat
        b.inputs['Specular IOR Level'].default_value=0.35
        return m
    M['white']=principled('pla_white_matte',(0.86,0.85,0.82),0.62,ss=0.25,ssr=(1.0,0.9,0.75),sss=0.0006)
    M['litho']=principled('pla_white_litho',(0.92,0.91,0.88),0.45,ss=1.0,ssr=(1.0,0.85,0.7),sss=0.0009)
    M['white_trans']=principled('pla_white_basic_translucent',(0.9,0.89,0.86),0.45,ss=1.0,ssr=(1.0,0.85,0.65),sss=0.0005)
    M['black']=principled('pla_black',(0.025,0.025,0.025),0.55)
    M['acrylic']=principled('acrylic_black',(0.01,0.01,0.01),0.06)
    M['led']=bpy.data.materials.new('led'); M['led'].use_nodes=True
    return M
def mesh_obj(name, V, F, mat):
    me=bpy.data.meshes.new(name); me.vertices.add(len(V)); me.vertices.foreach_set('co',V.astype(np.float32).ravel())
    me.loops.add(F.size); me.loops.foreach_set('vertex_index',F.astype(np.int32).ravel())
    me.polygons.add(len(F)); me.polygons.foreach_set('loop_start',np.arange(0,F.size,3,dtype=np.int32)); me.polygons.foreach_set('loop_total',np.full(len(F),3,np.int32))
    me.update(calc_edges=True)
    o=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat); return o
def rotm(spec):
    R=np.eye(3)
    for ax,deg in spec:  # applied in order
        a=math.radians(deg); c,s=math.cos(a),math.sin(a)
        r={'x':[[1,0,0],[0,c,-s],[0,s,c]],'y':[[c,0,s],[0,1,0],[-s,0,c]],'z':[[c,-s,0],[s,c,0],[0,0,1]]}[ax]
        R=np.array(r)@R
    return R
def place_parts(root_dir, parts, mats, parent):
    objs=[]
    for p in parts:
        fp=p['file'] if p['file'].startswith('/') else root_dir+'/'+p['file']
        loaded=tmf.load_stl(fp) if fp.endswith('.stl') else tmf.load(fp)
        for i,(n,V,F) in enumerate(loaded):
            if 'only' in p and i not in p['only']: continue
            V=V.copy(); Vprint=V.copy()
            if p.get('mirror'): V[:,0]*=-1; F=F[:,::-1]
            if 'rot' in p: V=V@rotm(p['rot']).T
            if 'matrix' in p:
                Mx=np.array(p['matrix'],float); V=V@Mx[:3,:3].T+Mx[:3,3]
                if np.linalg.det(Mx[:3,:3])<0: F=F[:,::-1]
            if 'wedge' in p:
                A=[];b=[]
                for ang,val in p['wedge']:
                    u=np.array([math.cos(math.radians(ang)),math.sin(math.radians(ang))]); A.append(u); b.append(val-(V[:,:2]@u).min())
                t=np.linalg.solve(np.array(A),np.array(b)); V=V+[t[0],t[1],p.get('zmin',0)-V[:,2].min()]
            if 'ref' in p:
                rlo,rhi=stlbb.bbox(p['ref']); p=dict(p); p['center']=[(rlo[0]+rhi[0])/2,(rlo[1]+rhi[1])/2,rlo[2]]
            if 'center' in p:
                lo,hi=V.min(0),V.max(0); c=(lo+hi)/2
                V=V-[c[0],c[1],lo[2]]+[p['center'][0],p['center'][1],p['center'][2]]
            if 'offset' in p: V=V+np.array(p['offset'])
            if 'post_rotz' in p: V=V@rotm([('z',p['post_rotz'])]).T
            if 'top' in p: V=V+[0,0,p['top']-V[:,2].max()]
            mk=p['mats'][i] if 'mats' in p else p.get('mat','white')
            if mk=='litho':
                im,lo,hi=lithomat.thickness_image(p.get('name',n)+'_t',Vprint)
                mat=lithomat.litho_mat(p.get('name',n)+'_m',im,**p.get('litho',{}))
            elif mk=='tube':
                tp=p['tube']; im,uvs=lithomat.tube_litho(n+'_tube',V,F,tp['ap'],tp['z0'],tp['z1'])
                mat=lithomat.litho_mat(n+'_tubem',im,**p.get('litho',{}))
            elif mk.startswith('skin'):
                t=float(mk[4:] or 1.6); mat=lithomat.litho_mat(p.get('name',n)+'_skin',lithomat.const_image(n+'_c',t),**p.get('litho',{}))
            else: mat=mats[mk]
            o=mesh_obj(p.get('name',n),V*0.001,F,mat)
            for k,cz in enumerate(p.get('copies_rotz',[])):
                o2=bpy.data.objects.new(o.name+'_c%d'%k,o.data); bpy.context.scene.collection.objects.link(o2); o2.rotation_euler=(0,0,math.radians(cz)); o2.parent=parent; objs.append(o2)
            if mk.startswith('skin'):
                o.data.uv_layers.new(name='UV')
            if mk=='tube':
                uvl=o.data.uv_layers.new(name='UV'); uvl.data.foreach_set('uv',uvs.ravel())
            if mk=='litho':
                uvl=o.data.uv_layers.new(name='UV'); uvp=(Vprint[:,:2]-lo[:2])/(hi[:2]-lo[:2])
                uvl.data.foreach_set('uv',uvp[F.ravel()].astype(np.float32).ravel())
            o.parent=parent; objs.append(o)
            for poly in o.data.polygons: pass
    return objs
def led_lights(parent, z0, z1, n=4, power=1.2, radius=0.006, temp_rgb=(1.0,0.78,0.52), xy=(0,0)):
    ls=[]
    for k in range(n):
        z=z0+(z1-z0)*(k+0.5)/n
        ld=bpy.data.lights.new('led%d'%k,'POINT'); ld.energy=power/n; ld.color=temp_rgb; ld.shadow_soft_size=radius
        o=bpy.data.objects.new('led%d'%k,ld); bpy.context.scene.collection.objects.link(o)
        o.location=(xy[0]*0.001,xy[1]*0.001,z*0.001); o.parent=parent; ls.append(o)
    return ls
