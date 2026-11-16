"""Split a 4-view turnaround sheet (row or 2x2 grid) into square views that all keep the sheet's pixel scale.
usage: split_turnaround_sheet.py sheet.png outprefix [--norm-base]   (needs numpy, pillow, scipy)
Writes outprefix_v0..v3.png in reading order (front first for Meshy multi-image-to-3D).
--norm-base rescales each view so its round base has the median width. Use it only when the views are
visibly drawn at different sizes; a horizon line or a leg over the base edge throws the measurement off.
Check the printed view heights: they should agree within a few percent, otherwise regenerate the sheet.
Every view is pasted unscaled onto one common canvas size, ground-aligned, then all are resized by the same
factor, so relative scale between views is preserved (Meshy multi-image needs matched scale)."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
im = Image.open(sys.argv[1]).convert('RGB'); a = np.asarray(im).astype(int)
edge = np.concatenate([a[:4].reshape(-1,3), a[-4:].reshape(-1,3), a[:, :4].reshape(-1,3), a[:, -4:].reshape(-1,3)])
bg = np.median(edge, axis=0)
fg = np.abs(a - bg).sum(-1) > 30
fg = ndimage.binary_opening(fg, structure=np.ones((5, 1)))  # drop thin horizon lines
blob = ndimage.binary_closing(fg, structure=np.ones((15, 15)))
blob = ndimage.binary_fill_holes(blob)
lab, n = ndimage.label(blob)
sizes = ndimage.sum(blob, lab, range(1, n+1))
keep = np.argsort(sizes)[::-1][:4] + 1
boxes = [ndimage.find_objects((lab == k).astype(int))[0] for k in keep]
H = a.shape[0]
boxes.sort(key=lambda b: (round(b[0].start / (H/3)), b[1].start))   # rows, then left->right
dims = [(b[0].stop-b[0].start, b[1].stop-b[1].start) for b in boxes]
print('views', [(b[0].start, b[0].stop, b[1].start, b[1].stop) for b in boxes], 'heights', [d[0] for d in dims])
NB = '--norm-base' in sys.argv
def base_w(b):
    m = blob[b]; h = m.shape[0]; rows = m[int(h*0.93):int(h*0.98)]
    xs = np.where(rows.any(0))[0]; return xs[-1] - xs[0]
bw = [base_w(b) for b in boxes]; ref = float(np.median(bw))
fac = [ref / w if NB else 1.0 for w in bw]; print('base widths', bw, 'factors', [round(f, 3) for f in fac])
side = int(max(max(d)*f for d, f in zip(dims, fac)) * 1.12)
for i, b in enumerate(boxes):
    crop = im.crop((b[1].start, b[0].start, b[1].stop, b[0].stop))
    if fac[i] != 1.0: crop = crop.resize((round(crop.width*fac[i]), round(crop.height*fac[i])), Image.LANCZOS)
    c = Image.new('RGB', (side, side), tuple(int(x) for x in bg))
    c.paste(crop, ((side - crop.width)//2, side - crop.height - int(side*0.05)))
    c.resize((1024, 1024), Image.LANCZOS).save(f'{sys.argv[2]}_v{i}.png')


