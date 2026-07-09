# Builds site assets from the master img/logotxt.png (gold lockup, RGBA):
#   top band  = icon row (suitcase | divider | passport)
#   bottom    = "FLIP TRAVEL" + "ADVENTURE AWAITS YOU" text
# Outputs:
#   logo-icon.png - icon row only (site header, boarding pass)
#   logo-text.png - text block only (kept for future use)
#   favicon.png   - suitcase glyph, square-padded 256px
from PIL import Image
import numpy as np

im = Image.open('img/logotxt.png').convert('RGBA')
a = np.array(im)
al = a[..., 3]

def bands(proj):
    out, start = [], None
    for i, v in enumerate(proj):
        if v > 0 and start is None:
            start = i
        if v == 0 and start is not None:
            out.append((start, i)); start = None
    if start is not None:
        out.append((start, len(proj)))
    return out

def trim(img):
    arr = np.array(img)[..., 3]
    ys, xs = np.where(arr > 8)
    return img.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

row_bands = bands((al > 16).sum(axis=1))
icon_band, text_top = row_bands[0], row_bands[1][0]

icon = trim(im.crop((0, icon_band[0], im.width, icon_band[1])))
icon.save('img/logo-icon.png')

text = trim(im.crop((0, text_top, im.width, im.height)))
text.save('img/logo-text.png')

# favicon: leftmost column group of the icon row = suitcase glyph
ia = np.array(icon)[..., 3]
col_bands = bands((ia > 16).sum(axis=0))
# merge column bands separated by tiny gaps (<12px) so glyph parts stay whole
merged = [list(col_bands[0])]
for s, e in col_bands[1:]:
    if s - merged[-1][1] < 12:
        merged[-1][1] = e
    else:
        merged.append([s, e])
suitcase = trim(icon.crop((merged[0][0], 0, merged[0][1], icon.height)))
w, h = suitcase.size
side = int(max(w, h) * 1.14)
sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
sq.paste(suitcase, ((side - w) // 2, (side - h) // 2))
sq.resize((256, 256), Image.LANCZOS).save('img/favicon.png')

import os
for f in ('img/logo-icon.png', 'img/logo-text.png', 'img/favicon.png'):
    print(f, Image.open(f).size, os.path.getsize(f), 'bytes')
