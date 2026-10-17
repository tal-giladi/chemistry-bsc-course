"""Turn photos from your phone spectrometer into one CSV that lesson01_phone_spectrometer.py can read.

Every photo must be taken with the phone in the same place and with exposure and white balance locked,
so the same pixel column means the same wavelength in every photo. The spectrum should run left to right
(use --vertical if it runs top to bottom).

    py photo_to_profile.py my_spectra.csv cfl=cfl.jpg blank=water.jpg blue_0.1=b01.jpg blue_0.5=b05.jpg ^
        yellow_0.5=y05.jpg green_unknown=drink.jpg

Options:
    --rows 0.45 0.55    use the band of image rows between these fractions of the height (default 0.45 0.55)
    --vertical          the spectrum runs top to bottom (columns become rows)
Names on the left of = become the CSV columns. lesson01 needs cfl, blank, blue_<f> (with blue_0.5),
yellow_<f> (with yellow_0.5) and green_unknown.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.image as mpimg

from ana25 import srgb_to_linear


def profile(path, r0, r1, vertical):
    img = mpimg.imread(path)                    # JPEG via Pillow (installed with matplotlib); PNG natively
    img = np.asarray(img, float)
    if img.max() <= 1.0:
        img = img * 255.0
    img = img[..., :3]
    if vertical:
        img = np.transpose(img, (1, 0, 2))
    h = img.shape[0]
    band = img[int(r0 * h):max(int(r1 * h), int(r0 * h) + 1)]
    clipped = np.mean(band >= 254.5)
    if clipped > 0.005:
        print(f"WARNING {path}: {100 * clipped:.1f} % of pixels are saturated; lower the exposure and retake.")
    lin = srgb_to_linear(band)                 # undo the sRGB curve (Lesson 09.6)
    return lin.sum(axis=2).mean(axis=0)        # R + G + B, averaged over the band of rows


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return
    out = Path(argv[1])
    r0, r1, vertical = 0.45, 0.55, False
    pairs = []
    i = 2
    while i < len(argv):
        a = argv[i]
        if a == "--rows":
            r0, r1 = float(argv[i + 1]), float(argv[i + 2])
            i += 3
            continue
        if a == "--vertical":
            vertical = True
        elif "=" in a:
            pairs.append(a.split("=", 1))
        i += 1
    cols = {name: profile(p, r0, r1, vertical) for name, p in pairs}
    n = min(v.size for v in cols.values())
    names = list(cols)
    lines = ["# made by photo_to_profile.py: linear R+G+B intensity per pixel column", "pixel," + ",".join(names)]
    for j in range(n):
        lines.append(f"{j}," + ",".join(f"{cols[k][j]:.5f}" for k in names))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out} with {n} pixels and columns {names}")


if __name__ == "__main__":
    main(sys.argv)
