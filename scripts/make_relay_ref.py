#!/usr/bin/env python3
"""Relay reference composer (user-taught method, 2026-10-05):
next segment's reference = previous segment's TAIL FRAME + characters' three-view cards,
pasted into ONE composite image -> the model continues the scene/composition/positions
from the tail frame while the cards keep faces/outfits locked. Feed composite as ref0
(72.image) and, when a second slot is free, the lead card as ref1 (101.image).

Layout: canvas 1536x1152 (4:3). Top band (full width, h=640): tail frame (cover-crop).
Bottom band (h=512): cards side by side (contain-fit on white).
Usage: make_relay_ref.py --tail tail.png --cards cardA.png [cardB.png] --out relay.jpg
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--tail", required=True)
ap.add_argument("--cards", nargs="+", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

W, H, TOP = 1536, 1152, 640
canvas = Image.new("RGB", (W, H), "white")

def cover(img, w, h):
    img = img.convert("RGB")
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2; y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))

def contain(img, w, h):
    img = img.convert("RGB")
    s = min(w / img.width, h / img.height)
    return img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)

canvas.paste(cover(Image.open(a.tail), W, TOP), (0, 0))
n = len(a.cards); cw = W // n
for i, cp in enumerate(a.cards):
    c = contain(Image.open(cp), cw - 16, H - TOP - 16)
    canvas.paste(c, (i * cw + (cw - c.width) // 2, TOP + (H - TOP - c.height) // 2))
canvas.save(a.out, quality=92)
print("saved:", a.out, canvas.size)
