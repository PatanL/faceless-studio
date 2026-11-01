import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
for f in sys.argv[1:]:
    a = np.asarray(Image.open(f).convert("RGB"), np.float32); L = a @ np.array([.2126, .7152, .0722], np.float32)
    bg = ndi.median_filter(L[::4, ::4], 15); bg = np.kron(bg, np.ones((4, 4)))[:L.shape[0], :L.shape[1]]
    m = (L - bg) > 12
    lab, n = ndi.label(m); sz = ndi.sum(m, lab, range(1, n + 1))
    small = ((sz >= 6) & (sz <= 400)).sum(); med = ((sz > 400) & (sz <= 5000)).sum()
    print(f.split("/")[-1], "small specks(6-400px):", int(small), " medium(400-5000px):", int(med), " median speck area:", float(np.median(sz[(sz >= 6) & (sz <= 400)])) if small else None)
