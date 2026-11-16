import numpy as np, sys, os, json
CACHE=os.environ.get('RENDER_CACHE','/tmp/render-cache')+'/stlbb.json'
def bbox(p):
    os.makedirs(os.path.dirname(CACHE),exist_ok=True); c=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    k=p+':'+str(os.path.getmtime(p))
    if k in c: return np.array(c[k][0]),np.array(c[k][1])
    with open(p,'rb') as f:
        head=f.read(84); n=int(np.frombuffer(head[80:84],'<u4')[0])
        if os.path.getsize(p)==84+n*50:
            rec=np.frombuffer(f.read(n*50),dtype=np.dtype([('n','<f4',3),('v','<f4',(3,3)),('a','<u2')])); V=rec['v'].reshape(-1,3)
        else:
            f.seek(0); txt=f.read().decode('ascii','ignore'); import re
            V=np.array(re.findall(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)',txt),float)
    lo,hi=V.min(0).astype(float),V.max(0).astype(float); c[k]=[lo.tolist(),hi.tolist()]; json.dump(c,open(CACHE,'w')); return lo,hi
if __name__=='__main__':
    for p in sys.argv[1:]:
        lo,hi=bbox(p); print(os.path.basename(p),'lo',np.round(lo,1),'hi',np.round(hi,1))
