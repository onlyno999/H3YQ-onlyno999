#!/usr/bin/env python3
"""Mosaic the face(s) in a tail frame before it is used as a relay reference.
User rule 2026-10-05: a generated tail frame's face has already drifted; feeding it
back makes the face drift further every segment. Mosaic it, so the next segment takes
ONLY scene/position/body from the tail frame and takes the FACE from the big headshot.
Run with the whisper venv python (has cv2): ~/workspace/tools/whisper_venv/bin/python
Usage: mosaic_face.py in.png out.png [--scale 1.5] [--blocks 12]
Fails loudly (exit 2) when no face is detected - never pass an unmosaicked frame on.
"""
import argparse, sys
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--scale", type=float, default=1.5)
ap.add_argument("--blocks", type=int, default=12)
a = ap.parse_args()

img = cv2.imread(a.inp)
if img is None: sys.exit(f"cannot read {a.inp}")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
if len(faces) == 0:
    print("NO FACE DETECTED - refusing to pass unmosaicked frame", file=sys.stderr); sys.exit(2)
h_img, w_img = img.shape[:2]
for (x, y, w, h) in faces:
    cx, cy = x + w / 2, y + h / 2
    nw, nh = w * a.scale, h * a.scale
    x0, y0 = max(0, int(cx - nw / 2)), max(0, int(cy - nh / 2))
    x1, y1 = min(w_img, int(cx + nw / 2)), min(h_img, int(cy + nh / 2))
    roi = img[y0:y1, x0:x1]
    small = cv2.resize(roi, (a.blocks, a.blocks), interpolation=cv2.INTER_LINEAR)
    img[y0:y1, x0:x1] = cv2.resize(small, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST)
    print(f"mosaicked face at ({x0},{y0})-({x1},{y1})")
cv2.imwrite(a.out, img)
print("saved:", a.out)
