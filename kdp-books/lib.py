"""Shared helpers for all KDP book engines (fonts, page class, pixel art, generic cover)."""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "kdp-color-by-code"))
import build as cbc  # registers fonts; gives Book, draw_key, draw_grid, norm, fit_font, draw_star
from build import Book, fit_font, draw_star, norm, draw_key, draw_grid, W, H, inch, canvas
from designs import D, PALETTE, RGB

OUTROOT = os.path.join(HERE, "output")


def grid_of(key):
    title, bg, rows = D[key]
    return norm(rows, bg), bg


def lineart(c, key, x, y, size, pad=True, lw=1.6):
    """Draw a pixel design as black-and-white coloring line art inside box (x,y,size)."""
    g, bg = grid_of(key)
    if not pad:
        g = [r[1:-1] for r in g[1:-1]]
    rows, cols = len(g), len(g[0])
    cell = size / max(rows, cols)
    ox = x + (size - cell * cols) / 2
    oy = y + (size - cell * rows) / 2
    def col(r, k):
        if 0 <= r < rows and 0 <= k < cols:
            return g[r][k]
        return bg
    c.setStrokeGray(0); c.setLineCap(1)
    for r in range(rows):
        for k in range(cols):
            ch = g[r][k]
            px, py = ox + k * cell, oy + (rows - 1 - r) * cell
            if ch == "x":
                c.setFillGray(0); c.rect(px, py, cell, cell, fill=1, stroke=0)
            if ch == bg:
                continue
            c.setLineWidth(lw)
            for dr, dk, (x1, y1, x2, y2) in [(-1, 0, (px, py + cell, px + cell, py + cell)),
                                             (1, 0, (px, py, px + cell, py)),
                                             (0, -1, (px, py, px, py + cell)),
                                             (0, 1, (px + cell, py, px + cell, py + cell))]:
                n = col(r + dr, k + dk)
                if n != ch:
                    c.line(x1, y1, x2, y2)
    c.setFillGray(0)


def color_art(c, key, x, y, size, border=True):
    g, bg = grid_of(key)
    rows, cols = len(g), len(g[0])
    cell = size / max(rows, cols)
    ox = x + (size - cell * cols) / 2; oy = y + (size - cell * rows) / 2
    for r, row in enumerate(g):
        for k, ch in enumerate(row):
            c.setFillColorRGB(*RGB[ch]); c.setStrokeColorRGB(*[v * 0.82 for v in RGB[ch]]); c.setLineWidth(0.4)
            c.rect(ox + k * cell, oy + (rows - 1 - r) * cell, cell, cell, fill=1, stroke=1)
    if border:
        c.setStrokeGray(0); c.setLineWidth(2); c.rect(ox, oy, cell * cols, cell * rows)


def generic_cover(path, pages, t):
    """t: dict(title1,title2,tagline,ages,author,hero,thumbs,blurb,features,badges,accent,accent2,spine)"""
    bleed = 0.125 * inch
    spine = pages * 0.002252 * inch
    CW = bleed * 2 + W * 2 + spine; CH = H + bleed * 2
    c = canvas.Canvas(path, pagesize=(CW, CH)); c.setTitle(t["title1"] + " " + t["title2"])
    A = RGB[t.get("accent", "b")]; A2 = RGB[t.get("accent2", "y")]
    fx = bleed + W + spine
    c.setFillColorRGB(*t.get("bgcol", (0.99, 0.95, 0.80))); c.rect(0, 0, CW, CH, fill=1, stroke=0)
    rng = random.Random(len(t["title1"]))
    for _ in range(240):
        c.setFillColorRGB(*RGB[rng.choice("roygbpk")]); s = rng.choice([6, 8, 10])
        c.rect(rng.uniform(0, CW), rng.uniform(0, CH), s, s, fill=1, stroke=0)
    c.setFillColorRGB(*A); c.rect(bleed + W, 0, spine, CH, fill=1, stroke=0)
    # front
    x0, x1 = fx + 0.5 * inch, fx + W - 0.5 * inch; cx = (x0 + x1) / 2
    c.setFillColorRGB(*A); c.roundRect(x0 - 10, CH - bleed - 3.15 * inch, x1 - x0 + 20, 2.6 * inch, 24, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); fs = fit_font(c, t["title1"], "Fredoka-Bold", x1 - x0 - 30, 58)
    c.setFont("Fredoka-Bold", fs); c.drawCentredString(cx, CH - bleed - 1.35 * inch, t["title1"])
    c.setFillColorRGB(*A2); fs = fit_font(c, t["title2"], "Fredoka-Bold", x1 - x0 - 30, 60)
    c.setFont("Fredoka-Bold", fs); c.drawCentredString(cx, CH - bleed - 2.25 * inch, t["title2"])
    c.setFillColorRGB(1, 1, 1); fs = fit_font(c, t["tagline"], "Andika-Bold", x1 - x0 - 30, 17)
    c.setFont("Andika-Bold", fs); c.drawCentredString(cx, CH - bleed - 2.8 * inch, t["tagline"])
    if t.get("hero_coded"):
        cbc.draw_color_art(c, t["hero"], cx - 2.25 * inch, CH - bleed - 7.85 * inch, 4.5 * inch, True, t["hero_coded"])
    else:
        color_art(c, t["hero"], cx - 2.25 * inch, CH - bleed - 7.85 * inch, 4.5 * inch)
    bw = (x1 - x0) / len(t["badges"])
    for i, (txt, k) in enumerate(t["badges"]):
        bx = x0 + i * bw + bw / 2; by = CH - bleed - 8.55 * inch
        c.setFillColorRGB(*RGB[k]); c.circle(bx, by, 0.47 * inch, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1); fs = fit_font(c, txt, "Fredoka-Bold", 0.85 * inch, 17)
        c.setFont("Fredoka-Bold", fs); c.drawCentredString(bx, by - fs * 0.35, txt)
    c.setFillColorRGB(*RGB["r"]); c.roundRect(x0 + 0.6 * inch, bleed + 0.95 * inch, x1 - x0 - 1.2 * inch, 0.55 * inch, 14, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); fs = fit_font(c, t["ages"], "Fredoka-Bold", x1 - x0 - 1.5 * inch, 20)
    c.setFont("Fredoka-Bold", fs); c.drawCentredString(cx, bleed + 1.13 * inch, t["ages"])
    c.setFillColorRGB(0.15, 0.15, 0.2); c.setFont("Fredoka", 15)
    c.drawCentredString(cx, bleed + 0.55 * inch, t["author"])
    # spine
    if spine > 0.3 * inch:
        c.saveState(); c.translate(bleed + W + spine / 2, CH / 2); c.rotate(-90)
        c.setFillColorRGB(1, 1, 1); fs = min(spine * 0.5, 22)
        st = t.get("spine", (t["title1"] + " " + t["title2"]).upper())
        fs = fit_font(c, st, "Fredoka-Bold", 6.5 * inch, fs)
        c.setFont("Fredoka-Bold", fs); c.drawCentredString(-0.8 * inch, -fs * 0.35, st)
        c.setFont("Fredoka", min(fs * 0.8, 14)); c.drawCentredString(3.6 * inch, -fs * 0.3, t["author"])
        c.restoreState()
    # back
    bx0, bx1 = bleed + 0.5 * inch, bleed + W - 0.5 * inch; bcx = (bx0 + bx1) / 2
    c.setFillColorRGB(1, 1, 1); c.roundRect(bx0, bleed + 2.0 * inch, bx1 - bx0, H - 2.6 * inch, 24, fill=1, stroke=0)
    c.setFillColorRGB(*A); c.setFont("Fredoka-Bold", 28)
    c.drawCentredString(bcx, CH - bleed - 1.3 * inch, t.get("back_head", "Learn. Play. Discover!"))
    c.setFillColorRGB(0.15, 0.15, 0.2); c.setFont("Andika", 13.5)
    y = CH - bleed - 1.85 * inch
    for ln in t["blurb"]:
        c.drawCentredString(bcx, y, ln); y -= 19
    y -= 10
    for f in t["features"]:
        c.setFillColorRGB(*RGB["g"]); draw_star(c, bx0 + 0.45 * inch, y + 4, 6, fill=True)
        c.setFillColorRGB(0.15, 0.15, 0.2); fs = fit_font(c, f, "Andika-Bold", bx1 - bx0 - 0.9 * inch, 12.5)
        c.setFont("Andika-Bold", fs); c.drawString(bx0 + 0.65 * inch, y, f); y -= 21
    s = 1.6 * inch; th = t["thumbs"]; gap = (bx1 - bx0 - 0.4 * inch - s * len(th)) / max(1, len(th) - 1)
    for i, k in enumerate(th):
        color_art(c, k, bx0 + 0.2 * inch + i * (s + gap), bleed + 2.6 * inch, s)
    c.setFillColorRGB(1, 1, 1)
    c.rect(bleed + W - 0.25 * inch - 2.1 * inch, bleed + 0.25 * inch, 2.1 * inch, 1.3 * inch, fill=1, stroke=0)
    c.save()
    return spine / inch, CW / inch, CH / inch


def copyright_block(b, title, author, year=2026, extra=()):
    c = b.c; l, r = b.margins()
    lines = [title, "", f"Copyright (c) {year} {author}. All rights reserved.", "",
             "No part of this book may be reproduced, stored, or transmitted in any form",
             "or by any means without written permission from the publisher, except that",
             "parents and teachers may copy pages for use with their own children or",
             "students in a single home or classroom.", "",
             "All pictures in this book are original works created for this book.",
             "Fonts: Andika and Fredoka, used under the SIL Open Font License.", *extra, "",
             "Independently published."]
    c.setFont("Andika", 10.5); y = 3.6 * inch
    for ln in lines:
        c.drawString(l, y, ln); y -= 15
    b.next(number=False)


def write_readme(path, d):
    with open(path, "w") as f:
        f.write(f"# {d['title']}\n\n")
        f.write(f"- **Interior:** `interior.pdf` — {d['pages']} pages, 8.5x11 in, black & white, white paper, no bleed\n")
        f.write(f"- **Cover:** `cover.pdf` — {d['cw']:.3f} x {d['ch']:.3f} in, spine {d['spine']:.3f} in, glossy\n")
        f.write(f"- **Print cost (approx):** $1.00 + {d['pages']} x $0.012 = ${1 + d['pages'] * 0.012:.2f} — verify in KDP Pricing\n")
        f.write(f"- **Suggested price:** {d['price']}\n\n")
        f.write(f"**Title:** {d['title']}\n\n**Subtitle:** {d['subtitle']}\n\n**Author:** {d['author']}\n\n")
        f.write("**Description:**\n\n" + d["description"] + "\n\n**Keywords:**\n")
        for i, k in enumerate(d["keywords"], 1):
            f.write(f"{i}. {k}\n")
        f.write("\n**Categories:**\n" + "".join(f"- {x}\n" for x in d["categories"]))
        f.write(f"\n**Reading age:** {d['age']}\n\n**AI disclosure:** pictures and text were made with AI assistance — answer *Yes* in KDP.\n")
