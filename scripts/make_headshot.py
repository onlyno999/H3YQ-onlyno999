#!/usr/bin/env python3
"""Single-person HEADSHOT for slot 2 (Node 101) — user rule 2026-10-05:
even for single-person scenes, slot 2 carries a BIG HEAD portrait (face large = locked tight).
Crops the rightmost headshot panel of a 4-panel card.
Usage: make_headshot.py card.png --out head.jpg [--frac 0.62]
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("card")
ap.add_argument("--out", required=True)
ap.add_argument("--frac", type=float, default=0.62)
a = ap.parse_args()

im = Image.open(a.card).convert("RGB")
im = im.crop((int(im.width * a.frac), 0, im.width, im.height))
im.save(a.out, quality=92)
print("saved:", a.out, im.size)
