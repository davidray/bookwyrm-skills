import bpy, numpy as np
from scipy import ndimage
def thickness_image(name, V, res=0.25):
    lo=V.min(0); hi=V.max(0)
    W=int(round((hi[0]-lo[0])/res))+1; H=int(round((hi[1]-lo[1])/res))+1
    img=np.zeros((H,W),np.float32)
    top=V[V[:,2]>0.01]
    i=np.clip(np.round((top[:,0]-lo[0])/res).astype(int),0,W-1); j=np.clip(np.round((top[:,1]-lo[1])/res).astype(int),0,H-1)
    np.maximum.at(img,(j,i),top[:,2].astype(np.float32))
    miss=img==0
    if miss.any():
        idx=ndimage.distance_transform_edt(miss,return_distances=False,return_indices=True)
        img=img[tuple(idx)]
    im=bpy.data.images.new(name,W,H,alpha=False,float_buffer=True); im.colorspace_settings.name='Non-Color'
    px=np.zeros((H,W,4),np.float32); px[...,0]=img; px[...,1]=img; px[...,2]=img; px[...,3]=1
    im.pixels.foreach_set(px.ravel()); im.update(); im.pack()
    print('thick',name,img.min(),img.max(),flush=True)
    return im, lo, hi
def const_image(name,t):
    im=bpy.data.images.new(name,1,1,alpha=False,float_buffer=True); im.colorspace_settings.name='Non-Color'
    im.pixels.foreach_set([t,t,t,1.0]); im.update(); im.pack(); return im
def litho_mat(name, im, k=1.0, t0=0.8, diffuse=0.22, col=(1.0,0.93,0.82)):
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; N=nt.nodes; L=nt.links
    for n in list(N): N.remove(n)
    out=N.new('ShaderNodeOutputMaterial')
    tx=N.new('ShaderNodeTexImage'); tx.image=im; tx.interpolation='Cubic'
    uv=N.new('ShaderNodeUVMap'); L.new(uv.outputs[0],tx.inputs[0])
    sub=N.new('ShaderNodeMath'); sub.operation='SUBTRACT'; sub.inputs[1].default_value=t0; L.new(tx.outputs['Color'],sub.inputs[0])
    mul=N.new('ShaderNodeMath'); mul.operation='MULTIPLY'; mul.inputs[1].default_value=-k; L.new(sub.outputs[0],mul.inputs[0])
    ex=N.new('ShaderNodeMath'); ex.operation='EXPONENT'; L.new(mul.outputs[0],ex.inputs[0])
    tint=N.new('ShaderNodeMix'); tint.data_type='RGBA'; tint.blend_type='MULTIPLY'; tint.inputs['Factor'].default_value=1
    L.new(ex.outputs[0],tint.inputs[6]); tint.inputs[7].default_value=col+(1,)
    tr=N.new('ShaderNodeBsdfTranslucent'); L.new(tint.outputs[2],tr.inputs['Color'])
    df=N.new('ShaderNodeBsdfPrincipled'); df.inputs['Base Color'].default_value=(0.9,0.89,0.86,1); df.inputs['Roughness'].default_value=0.45
    mx=N.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value=1-diffuse
    L.new(df.outputs[0],mx.inputs[1]); L.new(tr.outputs[0],mx.inputs[2])
    lp=N.new('ShaderNodeLightPath'); tp=N.new('ShaderNodeBsdfTransparent'); L.new(tint.outputs[2],tp.inputs['Color'])
    sh=N.new('ShaderNodeMixShader'); L.new(lp.outputs['Is Shadow Ray'],sh.inputs['Fac']); L.new(mx.outputs[0],sh.inputs[1]); L.new(tp.outputs[0],sh.inputs[2])
    L.new(sh.outputs[0],out.inputs['Surface'])
    return m
def tube_litho(name, V, F, ap, z0, z1, res=0.5):
    """Square lithophane tube (outer flat faces at +-ap). Returns (image, per-loop uv array)."""
    nu=int(round(2*ap/res))+1; nz=int(round((z1-z0)/res))+1
    img=np.zeros((nz,4*nu),np.float32)
    def side_coords(P):
        D=np.stack([P[:,1],P[:,0],-P[:,1],-P[:,0]],1)
        U=np.stack([P[:,0],-P[:,1],-P[:,0],P[:,1]],1)
        return D,U
    D,U=side_coords(V)
    s=np.argmax(D,1); d=D[np.arange(len(V)),s]; u=U[np.arange(len(V)),s]
    m=(d<ap-0.05)&(d>ap-3.0)
    t=(ap-d)[m]; i=np.clip(np.round((u[m]+ap)/res).astype(int),0,nu-1)+s[m]*nu; j=np.clip(np.round((V[m,2]-z0)/res).astype(int),0,nz-1)
    np.maximum.at(img,(j,i),t.astype(np.float32))
    miss=img==0
    if miss.any():
        idx=ndimage.distance_transform_edt(miss,return_distances=False,return_indices=True); img=img[tuple(idx)]
    im=bpy.data.images.new(name,4*nu,nz,alpha=False,float_buffer=True); im.colorspace_settings.name='Non-Color'
    px=np.zeros((nz,4*nu,4),np.float32); px[...,0]=img; px[...,1]=img; px[...,2]=img; px[...,3]=1
    im.pixels.foreach_set(px.ravel()); im.update(); im.pack()
    C=V[F].mean(1); Dc,_=side_coords(C); sp=np.argmax(Dc,1)
    _,UL=side_coords(V[F.ravel()]); sl=np.repeat(sp,3)
    ul=UL[np.arange(len(sl)),sl]
    uvx=((ul+ap)/res/(nu-1)*(nu-1)+0.5+sl*nu)/(4*nu); uvy=(V[F.ravel(),2]-z0)/(z1-z0)
    print('tube',name,img.min(),img.max(),flush=True)
    return im, np.stack([uvx,uvy],1).astype(np.float32)
