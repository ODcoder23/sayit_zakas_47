# Builds site assets from the master img/logo.png (high-res icon, RGBA):
#   logo-icon.png       - trimmed, original colors (cream boarding pass, light bgs)
#   logo-icon-light.png - navy recolored to #EAF2FC (dark header/hero bgs)
#   favicon.png         - square-padded 256px icon
from PIL import Image
import numpy as np

im = Image.open('img/logo.png').convert('RGBA')
a = np.array(im)

# trim with a small alpha threshold to drop stray near-invisible pixels
al = a[..., 3]
ys, xs = np.where(al > 8)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
icon = im.crop(box)
icon.save('img/logo-icon.png')

# light variant: only near-black navy turns light; teal/orange/gradient untouched
ia = np.array(icon).astype(int)
r, g, b = ia[..., 0], ia[..., 1], ia[..., 2]
navy = (np.maximum(np.maximum(r, g), b) < 110) & (ia[..., 3] > 0)
light = ia.copy()
light[navy, 0], light[navy, 1], light[navy, 2] = 0xEA, 0xF2, 0xFC
Image.fromarray(light.astype(np.uint8)).save('img/logo-icon-light.png')

# favicon: square canvas with 6% padding, downscaled to 256
w, h = icon.size
side = int(max(w, h) * 1.12)
sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
sq.paste(icon, ((side - w) // 2, (side - h) // 2))
sq.resize((256, 256), Image.LANCZOS).save('img/favicon.png')

import os
for f in ('img/logo-icon.png', 'img/logo-icon-light.png', 'img/favicon.png'):
    print(f, Image.open(f).size, os.path.getsize(f), 'bytes')
