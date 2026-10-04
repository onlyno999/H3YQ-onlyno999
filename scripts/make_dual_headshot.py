#!/usr/bin/env python3
"""Dual HEADSHOT composite for slot 2 (Node 101) — user rule 2026-10-05:
for two-person scenes prefer BIG HEAD portraits of both people pasted side by side
(stronger face lock than full three-view cards). Crops the rightmost headshot panel
of each 4-panel card (head+shoulders), pastes them side by side.
Usage: make_dual_headshot.py cardA.png cardB.png --out dual_head.jpg [--frac 0.62]
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("cards", nargs=2)
ap.add_argument("--out", required=True)
ap.add_argument("--frac", type=float, default=0.62, help="x fraction where the headshot panel starts")
a = ap.parse_args()

H = 1024
imgs = []
for p in a.cards:
    im = Image.open(p).convert("RGB")
    im = im.crop((int(im.width * a.frac), 0, im.width, im.height))
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    imgs.append(im)
W = sum(i.width for i in imgs) + 16
canvas = Image.new("RGB", (W, H), "white")
x = 0
for im in imgs:
    canvas.paste(im, (x, 0)); x += im.width + 16
canvas.save(a.out, quality=92)
print("saved:", a.out, canvas.size)
