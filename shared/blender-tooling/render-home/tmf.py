# Minimal 3MF reader -> list of (name, V (n,3) float64 mm, F (m,3) int) with build/component transforms applied.
import zipfile, re, numpy as np, os, hashlib
NS=re.compile(r'\{[^}]*\}')
def _mat(s):
    if not s: return np.eye(4)
    a=[float(x) for x in s.split()]; M=np.eye(4)
    M[:3,:3]=np.array(a[:9]).reshape(3,3).T if False else np.array([[a[0],a[3],a[6]],[a[1],a[4],a[7]],[a[2],a[5],a[8]]])
    M[:3,3]=a[9:12]; return M
def _parse_mesh(txt):
    vx=re.findall(r'<vertex\s+x="([^"]+)"\s+y="([^"]+)"\s+z="([^"]+)"',txt)
    tr=re.findall(r'<triangle\s+v1="(\d+)"\s+v2="(\d+)"\s+v3="(\d+)"',txt)
    V=np.array(vx,dtype=np.float64).reshape(-1,3); F=np.array(tr,dtype=np.int64).reshape(-1,3)
    return V,F
def load(path, cache=os.environ.get('RENDER_CACHE','/tmp/render-cache')):
    os.makedirs(cache,exist_ok=True)
    key=hashlib.md5((os.path.abspath(path)+str(os.path.getmtime(path))).encode()).hexdigest()
    cp=os.path.join(cache,key+'.npz')
    if os.path.exists(cp):
        d=np.load(cp,allow_pickle=True); return list(d['parts'])
    z=zipfile.ZipFile(path); models={n:z.read(n).decode('utf8','ignore') for n in z.namelist() if n.endswith('.model')}
    objs={}  # (file,id) -> ('mesh',V,F,name) or ('comp',[(file,id,M)])
    for fn,txt in models.items():
        for m in re.finditer(r'<object\b([^>]*)>(.*?)</object>',txt,re.S):
            attrs=m.group(1); body=m.group(2)
            oid=re.search(r'\bid="(\d+)"',attrs).group(1); nm=re.search(r'\bname="([^"]*)"',attrs); nm=nm.group(1) if nm else oid
            if '<mesh' in body:
                V,F=_parse_mesh(body); objs[('/'+fn.lstrip('/'),oid)]=('mesh',V,F,nm)
            else:
                comps=[]
                for c in re.finditer(r'<component\b([^>]*)/>',body):
                    ca=c.group(1); cid=re.search(r'objectid="(\d+)"',ca).group(1)
                    p=re.search(r'p:path="([^"]+)"',ca); cf=p.group(1) if p else '/'+fn.lstrip('/')
                    t=re.search(r'transform="([^"]+)"',ca)
                    comps.append((cf,cid,_mat(t.group(1) if t else None)))
                objs[('/'+fn.lstrip('/'),oid)]=('comp',comps,nm)
    root=[n for n in models if n.lower().endswith('3d/3dmodel.model')][0]
    out=[]
    def emit(key,M,name):
        o=objs[key]
        if o[0]=='mesh':
            V=(np.c_[o[1],np.ones(len(o[1]))]@M.T)[:,:3]; out.append((name or o[3],V,o[2]))
        else:
            for cf,cid,CM in o[1]: emit((cf,cid),M@CM,name or o[2])
    for it in re.finditer(r'<item\b([^>]*)/>',models[root]):
        a=it.group(1); oid=re.search(r'objectid="(\d+)"',a).group(1); t=re.search(r'transform="([^"]+)"',a)
        emit(('/'+root.lstrip('/'),oid),_mat(t.group(1) if t else None),None)
    parts=np.empty(len(out),dtype=object)
    for i,p in enumerate(out): parts[i]=p
    np.savez(cp,parts=parts); return out
if __name__=='__main__':
    import sys
    for p in sys.argv[1:]:
        ps=load(p)
        for n,V,F in ps:
            lo,hi=V.min(0),V.max(0); print(os.path.basename(p),'|',n,'|',len(F),'tris | size',np.round(hi-lo,1),'lo',np.round(lo,1))
def load_stl(p):
    import numpy as np
    with open(p,'rb') as f:
        f.seek(80); n=int(np.frombuffer(f.read(4),'<u4')[0]); rec=np.frombuffer(f.read(n*50),dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')]))
    P=rec['v'].reshape(-1,3).astype(np.float64); V,inv=np.unique(np.round(P,4),axis=0,return_inverse=True)
    return [(os.path.basename(p),V,inv.reshape(-1,3))]
