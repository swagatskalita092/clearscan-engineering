#!/usr/bin/env python3
"""Draws resumes/overview.png: the first page of every resume as a thumbnail.

Usage: python generator/make_overview.py   (from research/synthetic-resumes)
Needs pypdfium2 and pillow.
"""
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
COLUMNS, THUMB_W, GAP, LABEL_H = 6, 320, 12, 34
BACKGROUND, LABEL = (244, 246, 248), (180, 83, 9)


def main():
    files = sorted((ROOT / "resumes").glob("[0-9][0-9]-*.pdf"))
    thumbs = []
    for f in files:
        page = pdfium.PdfDocument(str(f))[0]
        img = page.render(scale=1.0).to_pil().convert("RGB")
        h = int(img.height * THUMB_W / img.width)
        thumbs.append((f.name[:2], img.resize((THUMB_W, h), Image.LANCZOS)))
    cell_h = max(t.height for _, t in thumbs) + LABEL_H
    rows = -(-len(thumbs) // COLUMNS)
    sheet = Image.new("RGB", (COLUMNS * (THUMB_W + GAP) + GAP,
                              rows * (cell_h + GAP) + GAP), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    for i, (label, thumb) in enumerate(thumbs):
        x = GAP + (i % COLUMNS) * (THUMB_W + GAP)
        y = GAP + (i // COLUMNS) * (cell_h + GAP)
        draw.text((x, y), label, fill=LABEL, font=font)
        sheet.paste(thumb, (x, y + LABEL_H))
        draw.rectangle([x, y + LABEL_H, x + THUMB_W - 1,
                        y + LABEL_H + thumb.height - 1], outline=(214, 218, 223))
    sheet.save(ROOT / "resumes" / "overview.png", optimize=True)
    print(f"Wrote overview of {len(thumbs)} resumes.")


if __name__ == "__main__":
    main()
