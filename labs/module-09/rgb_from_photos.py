"""Module 9 practical helper: average red, green and blue values in the centre of each photo.

Photograph each cup from straight above, filling most of the frame with the liquid, then run (from this folder):
    py rgb_from_photos.py blank1.jpg blank2.jpg std_0.jpg std_1.jpg ...
It prints one CSV line per photo (file name, R, G, B on the 0-255 sRGB scale), averaged over a central square
that is 20 % of the shorter side. Copy the numbers into your data file (columns type,c_percent_stock,R,G,B).
Reads PNG directly and JPEG through Pillow, which matplotlib already installs.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib.image as mpimg

BOX = 0.20      # side of the central square, as a fraction of the shorter image side


def centre_rgb(path, box=BOX):
    img = mpimg.imread(path)
    if img.dtype != np.uint8:            # PNG comes in as floats 0-1
        img = np.round(img * 255)
    h, w = img.shape[:2]
    half = max(1, int(min(h, w) * box / 2))
    patch = img[h // 2 - half:h // 2 + half, w // 2 - half:w // 2 + half, :3].astype(float)
    return patch.reshape(-1, 3).mean(axis=0), patch.reshape(-1, 3).std(axis=0)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    print("file,R,G,B,sd_R")
    for p in sys.argv[1:]:
        mean, sd = centre_rgb(p)
        print(f"{Path(p).name},{mean[0]:.1f},{mean[1]:.1f},{mean[2]:.1f},{sd[0]:.1f}")


if __name__ == "__main__":
    main()
