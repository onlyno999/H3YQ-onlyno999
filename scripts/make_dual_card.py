#!/usr/bin/env python3
"""Dual-card composer (user rule, 2026-10-05): for two-person scenes, slot 2 (Node 101)
gets ONE composite image = both characters' three-view cards pasted side by side,
so both faces/outfits are locked from a single reference.
Usage: make_dual_card.py cardA.png cardB.png --out dual.jpg
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("cards", nargs=2)
ap.add_argument("--out", required=True)
a = ap.parse_args()

H = 1024
imgs = []
for p in a.cards:
    im = Image.open(p).convert("RGB")
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    imgs.append(im)
W = sum(i.width for i in imgs) + 16
canvas = Image.new("RGB", (W, H), "white")
x = 0
for im in imgs:
    canvas.paste(im, (x, 0)); x += im.width + 16
canvas.save(a.out, quality=92)
print("saved:", a.out, canvas.size)
