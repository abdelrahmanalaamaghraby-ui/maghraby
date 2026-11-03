"""Build the KDP interior PDF and full-wrap cover PDF for
'Color by Code Mega Book' (8.5 x 11 in, black & white interior).

Usage:  python3 build.py
Output: output/interior.pdf, output/cover.pdf
"""
import os, random
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from designs import D, PALETTE, RGB, SECTION_ORDER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
os.makedirs(OUT, exist_ok=True)
for name, f in [("Andika", "Andika-Regular.ttf"), ("Andika-Bold", "Andika-Bold.ttf"),
                ("Fredoka", "Fredoka-SemiBold.ttf"), ("Fredoka-Bold", "Fredoka-Bold.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, "fonts", f)))

TITLE = "Color by Code Mega Book"
SUBTITLE = "150 Mystery Pictures: Letters, Sight Words, Phonics, Addition & Subtraction"
AGES = "Ages 5-8 | Kindergarten to 2nd Grade"
AUTHOR = "Abdelrahman Maghraby"
YEAR = 2026

W, H = 8.5 * inch, 11 * inch
GUTTER = 0.625 * inch   # KDP inside margin for 301-500 pages
OUTSIDE = 0.4 * inch
TOP, BOTTOM = 0.5 * inch, 0.5 * inch
GRAY = 0.45

ABBR = {"r": "R", "o": "O", "y": "Y", "g": "G", "l": "LG", "b": "B", "s": "LB",
        "p": "P", "k": "Pk", "n": "Br", "x": "Bk", "a": "Gy", "w": "W"}

# ---------------------------------------------------------------- word banks
SIGHT1 = ("a and away big can come down find for funny go help here I in is it jump little "
          "look make me my not one play run said see the three to two up we where you all am "
          "are at ate be but came did do eat four get good have he into like must new no now "
          "on our out please pretty ran ride saw say she so soon that there they this too "
          "under want was well went what who will with yes").split()
SIGHT2 = ("after again any ask by could every fly from give going had has her him his how just "
          "know let live may of old once open over put round some stop take thank them then "
          "think walk were when always around because been before best both buy call cold "
          "does fast first found gave goes made many off or pull read right sing sit sleep "
          "tell their these those upon us use very wash which why wish work would write your").split()
VOWELS = {
    "a": ("cat", "hat bag map van jam cap fan bat rat pan dad sad tap wag ham".split()),
    "e": ("bed", "pen hen net web leg jet ten wet pet beg men vet peg den".split()),
    "i": ("pig", "pin sit lip big fin wig kid mix dig hit six zip bib rib".split()),
    "o": ("dog", "pot mop log box fox hop top cot dot hot jog rod cob nod".split()),
    "u": ("bug", "sun cup bus mud rug hug nut tub gum cub run pup jug bun".split()),
}
STARTS = {
    "sh": "ship shop shell shed shut shin".split(), "ch": "chip chin chop chat chick chest".split(),
    "th": "thin thick thud thump thank".split(), "b": "bat bed bug bib box bun bag".split(),
    "m": "map mop mud men mix mat mug".split(), "p": "pig pen pot pan pup pin pet".split(),
    "d": "dog dig dad dot den duck dip".split(), "f": "fan fox fin fig fun fit".split(),
    "h": "hat hen hop hug hit ham hot".split(), "l": "log leg lip lap lid lot".split(),
    "n": "net nut nap nod nip".split(), "r": "rat rug run rib rod rip".split(),
    "w": "web wig wet wag win".split(), "g": "gum gas got gift gap".split(),
}

SECTIONS = [
    ("letters", "Part 1: Letter Match",
     "Find the letter in the code. Big or small, it is the same letter!",
     "Each square shows a letter. Match it to the code (uppercase or lowercase) and color it."),
    ("sight1", "Part 2: Sight Words - Level 1",
     "Read the word, find it in the code, and color!",
     "Read each word. Find it in the code and color the square."),
    ("sight2", "Part 3: Sight Words - Level 2",
     "Bigger words for growing readers.",
     "Read each word. Find it in the code and color the square."),
    ("phonics", "Part 4: Phonics Fun",
     "Listen for the vowel sound or the first sound in each word.",
     "Say each word out loud. Which sound do you hear? Use the code to color."),
    ("add", "Part 5: Addition",
     "Solve the sum, then color by the answer.",
     "Solve each addition problem. Color the square with the answer's color."),
    ("sub", "Part 6: Subtraction",
     "Take away, then color by the answer.",
     "Solve each subtraction problem. Color the square with the answer's color."),
    ("seasonal", "Part 7: Holiday Review",
     "Halloween, winter, spring and more - mixing everything you learned!",
     "Solve or read each square, then color it using the code."),
]


def norm(rows, bg):
    w = max(map(len, rows))
    rows = [r.ljust(w, ".") for r in rows]
    ys = [i for i, r in enumerate(rows) if r.strip(".")]
    xs = [j for j in range(w) if any(r[j] != "." for r in rows)]
    rows = [r[min(xs):max(xs) + 1] for r in rows[min(ys):max(ys) + 1]]
    w = len(rows[0])
    pad = "." * (w + 2)
    rows = [pad] + ["." + r + "." for r in rows] + [pad]
    return [[bg if ch == "." else ch for ch in r] for r in rows]


# ---------------------------------------------------------------- code makers
def make_codes(kind, idx, colors, rng):
    """Return (key_entries[(label, color)], cell_text_fn(color)->str)."""
    n = len(colors)
    if kind == "letters":
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        start = (idx * 5) % 26
        letters = [alpha[(start + i * 3) % 26] for i in range(n)]
        if len(set(letters)) < n:
            letters = rng.sample(alpha, n)
        m = dict(zip(colors, letters))
        return [(f"{m[c]} {m[c].lower()}", c) for c in colors], \
            lambda c: m[c] if rng.random() < 0.5 else m[c].lower()
    if kind in ("sight1", "sight2"):
        bank = SIGHT1 if kind == "sight1" else SIGHT2
        words = rng.sample(bank, n)
        m = dict(zip(colors, words))
        return [(m[c], c) for c in colors], lambda c: m[c]
    if kind == "phonics":
        if n <= 5:
            vs = rng.sample(list(VOWELS), n)
            m = dict(zip(colors, vs))
            key = [(f"short {m[c]} ({VOWELS[m[c]][0]})", c) for c in colors]
            return key, lambda c: rng.choice(VOWELS[m[c]][1])
        ss = rng.sample(list(STARTS), n)
        m = dict(zip(colors, ss))
        key = [(f"starts with {m[c]}", c) for c in colors]
        return key, lambda c: rng.choice(STARTS[m[c]])
    if kind in ("add", "sub", "add10", "sub10"):
        small = kind.endswith("10") or idx < 12
        lo, hi = (1, 10) if small else (5, 20)
        if kind.startswith("sub"):
            lo, hi = (0, 9) if small else (2, 15)
        answers = rng.sample(range(lo, hi + 1), n)
        m = dict(zip(colors, answers))
        def expr(c):
            a = m[c]
            if kind.startswith("add"):
                x = rng.randint(0, a) if a <= 10 else rng.randint(a - 10, 10)
                return f"{x}+{a - x}"
            top = rng.randint(a, min(a + 10, 20) if not small else 10)
            return f"{top}-{top - a}"
        return [(str(m[c]), c) for c in colors], expr
    raise ValueError(kind)


SEASONAL_MIX = ["add10", "sight1", "sub10", "letters"]


def build_pages():
    pages = []
    num = 0
    for key, *_ in SECTIONS:
        for i, dk in enumerate(SECTION_ORDER[key]):
            num += 1
            title, bg, rows = D[dk]
            grid = norm(rows, bg)
            colors = []
            for r in grid:
                for c in r:
                    if c not in colors:
                        colors.append(c)
            # put background first so it is the first key entry
            colors.remove(bg); colors.insert(0, bg)
            rng = random.Random(1000 + num)
            kind = SEASONAL_MIX[i % 4] if key == "seasonal" else key
            entries, fn = make_codes(kind, i, colors, rng)
            texts = [[fn(c) for c in r] for r in grid]
            pages.append(dict(num=num, section=key, kind=kind, title=title, grid=grid,
                              texts=texts, key=entries))
    return pages


# ---------------------------------------------------------------- drawing helpers
class Book:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=(W, H))
        self.c.setTitle(TITLE); self.c.setAuthor(AUTHOR)
        self.page = 1

    def margins(self):
        odd = self.page % 2 == 1
        left = GUTTER if odd else OUTSIDE
        right = OUTSIDE if odd else GUTTER
        return left, W - right

    def footer(self, show=True):
        if show:
            l, r = self.margins()
            self.c.setFont("Andika", 10); self.c.setFillGray(GRAY)
            self.c.drawCentredString((l + r) / 2, 0.3 * inch, str(self.page))
            self.c.setFillGray(0)

    def next(self, number=True):
        self.footer(number)
        self.c.showPage(); self.page += 1

    def blank_back(self):
        """Back of a single-sided coloring page."""
        l, r = self.margins()
        self.c.setFont("Andika", 9); self.c.setFillGray(0.6)
        self.c.drawCentredString((l + r) / 2, H / 2,
                                 "This page is left blank to stop colors from bleeding through.")
        self.c.setFillGray(0)
        self.next(number=False)

    def ensure_odd(self):
        if self.page % 2 == 0:
            self.next(number=False)

    def center(self):
        l, r = self.margins(); return (l + r) / 2


def fit_font(c, text, font, maxw, size):
    while size > 4 and c.stringWidth(text, font, size) > maxw:
        size -= 0.25
    return size


def draw_star(c, x, y, r, fill=False):
    import math
    p = c.beginPath()
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        px, py = x + rad * math.cos(ang), y + rad * math.sin(ang)
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close(); c.drawPath(p, fill=1 if fill else 0, stroke=1)


def draw_key(c, entries, x0, x1, ytop):
    """Code key: [circle to pre-color] code = Color. Returns bottom y."""
    per_row = 4 if len(entries) > 4 else len(entries)
    rows = (len(entries) + per_row - 1) // per_row
    bw = (x1 - x0) / per_row
    bh = 34
    c.setLineWidth(1.2); c.setStrokeGray(0)
    c.roundRect(x0, ytop - rows * bh - 10, x1 - x0, rows * bh + 10, 8)
    for i, (label, col) in enumerate(entries):
        rx = x0 + (i % per_row) * bw
        ry = ytop - 5 - (i // per_row) * bh - bh / 2
        c.setLineWidth(1); c.circle(rx + 16, ry, 9)
        txt = f"{label} = {PALETTE[col]}"
        fs = fit_font(c, txt, "Andika-Bold", bw - 34, 12.5)
        c.setFont("Andika-Bold", fs)
        c.drawString(rx + 30, ry - fs * 0.35, txt)
    return ytop - rows * bh - 10


def draw_grid(c, p, x0, x1, ytop, ybot):
    g, t = p["grid"], p["texts"]
    rows, cols = len(g), len(g[0])
    cell = min((x1 - x0) / cols, (ytop - ybot) / rows, 44)
    gw, gh = cell * cols, cell * rows
    gx = (x0 + x1) / 2 - gw / 2
    gy = ytop - (ytop - ybot - gh) / 2   # vertically centered in area
    c.setStrokeGray(0.35); c.setLineWidth(0.6)
    for r in range(rows):
        for k in range(cols):
            x, y = gx + k * cell, gy - (r + 1) * cell
            c.rect(x, y, cell, cell)
            txt = t[r][k]
            fs = fit_font(c, txt, "Andika", cell - 5, min(cell * 0.42, 15))
            c.setFont("Andika", fs); c.setFillGray(0.1)
            c.drawCentredString(x + cell / 2, y + cell / 2 - fs * 0.33, txt)
    c.setFillGray(0); c.setStrokeGray(0); c.setLineWidth(1.6)
    c.rect(gx, gy - gh, gw, gh)


# ---------------------------------------------------------------- pages
def title_page(b):
    c = b.c; cx = b.center()
    c.setFont("Fredoka-Bold", 40); c.drawCentredString(cx, H - 2.6 * inch, "Color by Code")
    c.setFont("Fredoka-Bold", 34); c.drawCentredString(cx, H - 3.2 * inch, "MEGA BOOK")
    c.setFont("Andika", 15)
    c.drawCentredString(cx, H - 4.0 * inch, "150 Mystery Pictures")
    c.drawCentredString(cx, H - 4.3 * inch, "Letters - Sight Words - Phonics - Addition - Subtraction")
    c.setFont("Andika-Bold", 14); c.drawCentredString(cx, H - 4.75 * inch, AGES)
    # small sample grid
    p = PAGES[0]
    draw_grid(c, p, cx - 1.6 * inch, cx + 1.6 * inch, H - 5.2 * inch, H - 8.4 * inch)
    c.setFont("Fredoka", 16); c.drawCentredString(cx, 1.4 * inch, AUTHOR)
    b.next(number=False)


def copyright_page(b):
    c = b.c; l, r = b.margins()
    lines = [
        f"{TITLE}", SUBTITLE, "",
        f"Copyright (c) {YEAR} {AUTHOR}. All rights reserved.", "",
        "No part of this book may be reproduced, stored, or transmitted in any form",
        "or by any means without written permission from the publisher, except that",
        "parents and teachers may copy pages for use with their own children or",
        "students in a single home or classroom.", "",
        "All pixel-art pictures in this book are original works created for this book.",
        "Fonts: Andika and Fredoka, used under the SIL Open Font License.", "",
        "Independently published.",
    ]
    c.setFont("Andika", 10.5)
    y = 3.6 * inch
    for ln in lines:
        c.drawString(l, y, ln); y -= 15
    b.next(number=False)


def belongs_page(b):
    c = b.c; cx = b.center()
    c.setLineWidth(2); c.roundRect(b.margins()[0] + 20, 2.5 * inch, b.margins()[1] - b.margins()[0] - 40, 6 * inch, 24)
    c.setFont("Fredoka-Bold", 36); c.drawCentredString(cx, 7.4 * inch, "This Book")
    c.drawCentredString(cx, 6.8 * inch, "Belongs To:")
    c.setLineWidth(1.5); c.line(cx - 2.6 * inch, 5.3 * inch, cx + 2.6 * inch, 5.3 * inch)
    for i in range(5):
        draw_star(c, cx - 2 * inch + i * inch, 3.6 * inch, 22)
    b.next(number=False)


def how_to_page(b):
    c = b.c; l, r = b.margins()
    c.setFont("Fredoka-Bold", 26); c.drawCentredString(b.center(), H - 1.2 * inch, "How to Use This Book")
    y = H - 1.9 * inch
    blocks = [
        ("For kids", [
            "1. Look at the code box at the top of the page.",
            "2. Color each little circle in the code box with its color first.",
            "3. Read the word, letter, or problem in each square.",
            "4. Find it in the code and color the square with that color.",
            "5. Keep going until the mystery picture appears!",
        ]),
        ("For grown-ups", [
            "The book gets harder step by step, in 7 parts:",
            "  Part 1  Letter Match - uppercase and lowercase letters",
            "  Part 2  Sight Words Level 1 - pre-primer and primer words",
            "  Part 3  Sight Words Level 2 - first and second grade words",
            "  Part 4  Phonics - short vowel sounds and beginning sounds",
            "  Part 5  Addition - within 10, then within 20",
            "  Part 6  Subtraction - within 10, then within 20",
            "  Part 7  Holiday Review - mixed practice",
            "",
            "Every picture is printed on its own page, so colors do not bleed",
            "through. Crayons and colored pencils work best.",
            "",
            "Use the Progress Tracker to celebrate each finished picture,",
            "and check the Answer Key at the back of the book.",
            "Answer key colors: R Red, O Orange, Y Yellow, G Green, LG Light Green,",
            "B Blue, LB Light Blue, P Purple, Pk Pink, Br Brown, Bk Black, Gy Gray, W White.",
        ]),
    ]
    for head, lines in blocks:
        c.setFont("Fredoka-Bold", 17); c.drawString(l + 10, y, head); y -= 24
        c.setFont("Andika", 12.5)
        for ln in lines:
            c.drawString(l + 20, y, ln); y -= 18
        y -= 14
    b.next()


def color_test_page(b):
    c = b.c; l, r = b.margins(); cx = b.center()
    c.setFont("Fredoka-Bold", 26); c.drawCentredString(cx, H - 1.2 * inch, "Color Test Page")
    c.setFont("Andika", 12.5)
    c.drawCentredString(cx, H - 1.55 * inch, "Test your crayons here! Color each shape with its color.")
    names = list(PALETTE.items())
    colw = (r - l) / 3
    for i, (k, nm) in enumerate(names):
        x = l + (i % 3) * colw + 30
        y = H - 2.6 * inch - (i // 3) * 1.45 * inch
        c.setLineWidth(1.4); c.roundRect(x, y - 30, 70, 60, 10)
        c.setFont("Andika-Bold", 14); c.drawString(x + 82, y - 5, nm)
    b.next()


def tracker_page(b, pages):
    c = b.c; l, r = b.margins(); cx = b.center()
    c.setFont("Fredoka-Bold", 26); c.drawCentredString(cx, H - 1.1 * inch, "My Progress Tracker")
    c.setFont("Andika", 12)
    c.drawCentredString(cx, H - 1.45 * inch, "Color a star each time you finish a mystery picture!")
    cols = 10; cw = (r - l) / cols; rh = 0.58 * inch
    for i, p in enumerate(pages):
        x = l + (i % cols) * cw + cw / 2
        y = H - 2.0 * inch - (i // cols) * rh
        c.setLineWidth(1); draw_star(c, x, y, 12)
        c.setFont("Andika", 8); c.drawCentredString(x, y - 21, str(p["num"]))
    b.next()


def divider(b, title, sub, sample):
    b.ensure_odd()
    c = b.c; l, r = b.margins(); cx = b.center()
    c.setLineWidth(3); c.roundRect(l, 1 * inch, r - l, H - 2 * inch, 30)
    c.setFont("Fredoka-Bold", 34)
    fs = fit_font(c, title, "Fredoka-Bold", r - l - 60, 34); c.setFont("Fredoka-Bold", fs)
    c.drawCentredString(cx, H - 2.6 * inch, title)
    c.setFont("Andika", 15); c.drawCentredString(cx, H - 3.2 * inch, sub)
    # sample code key preview, just for fun
    c.setFont("Andika-Bold", 13)
    c.drawCentredString(cx, H - 4.0 * inch, "Example squares:")
    texts = sample
    cell = 0.8 * inch
    x0 = cx - cell * len(texts) / 2
    for i, t in enumerate(texts):
        c.setLineWidth(1); c.rect(x0 + i * cell, H - 5.1 * inch, cell, cell)
        fs = fit_font(c, t, "Andika", cell - 8, 18); c.setFont("Andika", fs)
        c.drawCentredString(x0 + i * cell + cell / 2, H - 5.1 * inch + cell / 2 - fs * 0.33, t)
    for i in range(3):
        draw_star(c, cx - 1.2 * inch + i * 1.2 * inch, 2.4 * inch, 26)
    b.next()
    b.blank_back()


def picture_page(b, p, instr):
    b.ensure_odd()
    c = b.c; l, r = b.margins()
    y = H - TOP
    c.setFont("Fredoka-Bold", 20); c.drawString(l, y - 16, f"Mystery Picture #{p['num']}")
    c.setFont("Andika", 11.5); c.drawRightString(r, y - 14, "Name: ____________________")
    fs = fit_font(c, instr, "Andika", r - l, 11.5); c.setFont("Andika", fs)
    c.setFillGray(0.2); c.drawString(l, y - 36, instr); c.setFillGray(0)
    kb = draw_key(c, p["key"], l, r, y - 46)
    draw_grid(c, p, l, r, kb - 14, BOTTOM + 14)
    b.next()
    b.blank_back()


def answer_pages(b, pages):
    b.ensure_odd()
    c = b.c
    per = 4
    for s in range(0, len(pages), per):
        l, r = b.margins()
        c.setFont("Fredoka-Bold", 20); c.drawCentredString(b.center(), H - 0.85 * inch, "Answer Key")
        c.setFont("Andika", 8.5); c.setFillGray(0.25)
        c.drawCentredString(b.center(), H - 1.08 * inch,
                            "R Red  O Orange  Y Yellow  G Green  LG Light Green  B Blue  LB Light Blue  "
                            "P Purple  Pk Pink  Br Brown  Bk Black  Gy Gray  W White")
        c.setFillGray(0)
        cw = (r - l) / 2; chh = (H - 1.5 * inch - BOTTOM) / 2
        for j, p in enumerate(pages[s:s + per]):
            x0 = l + (j % 2) * cw; ytop = H - 1.3 * inch - (j // 2) * chh
            c.setFont("Andika-Bold", 11)
            c.drawCentredString(x0 + cw / 2, ytop - 12, f"#{p['num']}  {p['title']}")
            g = p["grid"]; rows, cols = len(g), len(g[0])
            cell = min((cw - 20) / cols, (chh - 40) / rows)
            gx = x0 + cw / 2 - cell * cols / 2; gy = ytop - 22
            c.setLineWidth(0.4); c.setStrokeGray(0.5)
            for rr in range(rows):
                for k in range(cols):
                    ch = g[rr][k]
                    x, yy = gx + k * cell, gy - (rr + 1) * cell
                    shade = {"x": 0.25, "w": 1.0}.get(ch, 0.9)
                    c.setFillGray(shade); c.rect(x, yy, cell, cell, fill=1)
                    c.setFillGray(1 if ch == "x" else 0)
                    t = ABBR[ch]; fs = fit_font(c, t, "Andika", cell - 1.5, cell * 0.55)
                    c.setFont("Andika", fs); c.drawCentredString(x + cell / 2, yy + cell / 2 - fs * 0.33, t)
            c.setFillGray(0); c.setStrokeGray(0)
        b.next()


def certificate(b):
    b.ensure_odd()
    c = b.c; l, r = b.margins(); cx = b.center()
    c.setLineWidth(4); c.roundRect(l, 1.2 * inch, r - l, H - 2.4 * inch, 20)
    c.setLineWidth(1.5); c.roundRect(l + 12, 1.2 * inch + 12, r - l - 24, H - 2.4 * inch - 24, 14)
    c.setFont("Fredoka-Bold", 34); c.drawCentredString(cx, H - 2.5 * inch, "Certificate")
    c.setFont("Fredoka", 20); c.drawCentredString(cx, H - 3.0 * inch, "of Super Coloring Achievement")
    c.setFont("Andika", 14); c.drawCentredString(cx, H - 4.0 * inch, "This certificate is proudly presented to")
    c.line(cx - 2.5 * inch, H - 4.9 * inch, cx + 2.5 * inch, H - 4.9 * inch)
    c.drawCentredString(cx, H - 5.6 * inch, "for finishing all 150 Mystery Pictures and")
    c.drawCentredString(cx, H - 5.85 * inch, "practicing letters, words, sounds, and math!")
    for i in range(5):
        draw_star(c, cx - 2 * inch + i * inch, H - 7.0 * inch, 20)
    c.setFont("Andika", 12)
    c.line(l + 0.6 * inch, 2.2 * inch, l + 3 * inch, 2.2 * inch); c.drawString(l + 0.6 * inch, 1.95 * inch, "Date")
    c.line(r - 3 * inch, 2.2 * inch, r - 0.6 * inch, 2.2 * inch); c.drawString(r - 3 * inch, 1.95 * inch, "Signed")
    b.next(number=False)
    b.blank_back()


def thanks_page(b):
    c = b.c; cx = b.center()
    c.setFont("Fredoka-Bold", 28); c.drawCentredString(cx, H - 3 * inch, "Thank You!")
    c.setFont("Andika", 13)
    for i, ln in enumerate([
        "We hope your little learner had fun discovering every mystery picture.",
        "If you enjoyed this book, a short review on Amazon helps other",
        "families and teachers find it - and helps us make more books like it.",
        "", f"- {AUTHOR}"]):
        c.drawCentredString(cx, H - 3.7 * inch - i * 20, ln)
    b.next(number=False)


PAGES = build_pages()


def build_interior():
    b = Book(os.path.join(OUT, "interior.pdf"))
    title_page(b); copyright_page(b)
    belongs_page(b); b.blank_back()
    how_to_page(b); color_test_page(b)
    tracker_page(b, PAGES)
    by_sec = {}
    for p in PAGES:
        by_sec.setdefault(p["section"], []).append(p)
    for key, title, sub, instr in SECTIONS:
        ps = by_sec[key]
        sample = [t for t in dict.fromkeys(x for row in ps[0]["texts"] for x in row)][:5]
        divider(b, title, sub, sample)
        for p in ps:
            picture_page(b, p, instr)
    answer_pages(b, PAGES)
    certificate(b)
    thanks_page(b)
    if b.page % 2 == 0:        # make total page count even
        b.next(number=False)
    b.c.save()
    return b.page - 1


# ---------------------------------------------------------------- cover
def draw_color_art(c, dk, x, y, size, coded_half=False, codes=None):
    title, bg, rows = D[dk]
    g = norm(rows, bg)
    n = max(len(g), len(g[0])); cell = size / n
    ox = x + (size - cell * len(g[0])) / 2; oy = y + (size - cell * len(g)) / 2
    for r, row in enumerate(g):
        for k, ch in enumerate(row):
            px, py = ox + k * cell, oy + (len(g) - 1 - r) * cell
            if coded_half and k < len(row) // 2:
                c.setFillColorRGB(1, 1, 1); c.setStrokeGray(0.4); c.setLineWidth(0.5)
                c.rect(px, py, cell, cell, fill=1, stroke=1)
                t = codes[ch]; fs = fit_font(c, t, "Andika", cell - 3, cell * 0.45)
                c.setFillGray(0.15); c.setFont("Andika", fs)
                c.drawCentredString(px + cell / 2, py + cell / 2 - fs * 0.33, t)
            else:
                c.setFillColorRGB(*RGB[ch]); c.setStrokeColorRGB(*[v * 0.8 for v in RGB[ch]]); c.setLineWidth(0.4)
                c.rect(px, py, cell, cell, fill=1, stroke=1)
    c.setStrokeGray(0); c.setLineWidth(2); c.rect(ox, oy, cell * len(g[0]), cell * len(g))


def build_cover(page_count):
    bleed = 0.125 * inch
    spine = page_count * 0.002252 * inch       # white paper
    CW = bleed * 2 + W * 2 + spine; CH = H + bleed * 2
    c = canvas.Canvas(os.path.join(OUT, "cover.pdf"), pagesize=(CW, CH))
    c.setTitle(TITLE + " - Cover")
    front_x = bleed + W + spine
    # background
    c.setFillColorRGB(0.99, 0.95, 0.80); c.rect(0, 0, CW, CH, fill=1, stroke=0)
    # confetti pixels
    rng = random.Random(7)
    for _ in range(260):
        k = rng.choice("roygbpk")
        c.setFillColorRGB(*RGB[k]); s = rng.choice([6, 8, 10])
        x = rng.uniform(0, CW); yy = rng.uniform(0, CH)
        if front_x - 10 < x < front_x + spine + 10 and False:
            continue
        c.rect(x, yy, s, s, fill=1, stroke=0)
    # spine band
    c.setFillColorRGB(*RGB["b"]); c.rect(bleed + W, 0, spine, CH, fill=1, stroke=0)
    # ---------------- FRONT
    fx0 = front_x + 0.5 * inch; fx1 = front_x + W - 0.5 * inch; fcx = (fx0 + fx1) / 2
    c.setFillColorRGB(*RGB["b"]); c.roundRect(fx0 - 10, CH - bleed - 3.15 * inch, fx1 - fx0 + 20, 2.6 * inch, 24, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); c.setFont("Fredoka-Bold", 58)
    c.drawCentredString(fcx, CH - bleed - 1.35 * inch, "Color by Code")
    c.setFillColorRGB(*RGB["y"]); c.setFont("Fredoka-Bold", 64)
    c.drawCentredString(fcx, CH - bleed - 2.25 * inch, "MEGA BOOK")
    c.setFillColorRGB(1, 1, 1); c.setFont("Andika-Bold", 17)
    c.drawCentredString(fcx, CH - bleed - 2.8 * inch, "150 Mystery Pictures to Color & Discover!")
    # hero: half-coded dino
    hero = "dino"
    _, bg, rows = D[hero]
    codes = {bg: "3+4", "g": "2+3", "x": "6+2", "l": "1+1", "w": "4+5"}
    draw_color_art(c, hero, fcx - 2.25 * inch, CH - bleed - 7.85 * inch, 4.5 * inch, True, codes)
    # skill badges
    badges = [("ABC", "r"), ("Sight Words", "g"), ("Phonics", "p"), ("+  -", "o")]
    bw = (fx1 - fx0) / 4
    for i, (t, k) in enumerate(badges):
        x = fx0 + i * bw + bw / 2; y = CH - bleed - 8.55 * inch
        c.setFillColorRGB(*RGB[k]); c.circle(x, y, 0.47 * inch, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1); fs = fit_font(c, t, "Fredoka-Bold", 0.85 * inch, 17); c.setFont("Fredoka-Bold", fs)
        c.drawCentredString(x, y - fs * 0.35, t)
    c.setFillColorRGB(*RGB["r"]); c.roundRect(fx0 + 0.6 * inch, bleed + 0.95 * inch, fx1 - fx0 - 1.2 * inch, 0.55 * inch, 14, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); c.setFont("Fredoka-Bold", 20)
    c.drawCentredString(fcx, bleed + 1.13 * inch, AGES)
    c.setFillColorRGB(0.15, 0.15, 0.2); c.setFont("Fredoka", 15)
    c.drawCentredString(fcx, bleed + 0.55 * inch, AUTHOR)
    # ---------------- SPINE
    if spine > 0.3 * inch:
        c.saveState(); c.translate(bleed + W + spine / 2, CH / 2); c.rotate(-90)
        c.setFillColorRGB(1, 1, 1); fs = min(spine * 0.5, 22)
        c.setFont("Fredoka-Bold", fs); c.drawCentredString(-0.6 * inch, -fs * 0.35, "COLOR BY CODE MEGA BOOK")
        c.setFont("Fredoka", fs * 0.75); c.drawCentredString(3.4 * inch, -fs * 0.3, AUTHOR)
        c.restoreState()
    # ---------------- BACK
    bx0 = bleed + 0.5 * inch; bx1 = bleed + W - 0.5 * inch; bcx = (bx0 + bx1) / 2
    c.setFillColorRGB(1, 1, 1); c.roundRect(bx0, bleed + 2.0 * inch, bx1 - bx0, H - 2.6 * inch, 24, fill=1, stroke=0)
    c.setFillColorRGB(*RGB["b"]); c.setFont("Fredoka-Bold", 28)
    c.drawCentredString(bcx, CH - bleed - 1.3 * inch, "Learn. Color. Discover!")
    c.setFillColorRGB(0.15, 0.15, 0.2); c.setFont("Andika", 13.5)
    blurb = [
        "Every page hides a secret picture. Read the letter, word, or",
        "math problem in each square, find its color in the code, and",
        "watch the mystery picture appear!",
    ]
    y = CH - bleed - 1.85 * inch
    for ln in blurb:
        c.drawCentredString(bcx, y, ln); y -= 19
    y -= 10
    feats = [
        "150 original mystery pictures - animals, food, space, holidays & more",
        "7 levels: letters, sight words, phonics, addition & subtraction",
        "Single-sided pages - no bleed-through",
        "Code key with color circles kids pre-color themselves",
        "Progress tracker, answer key & completion certificate",
        "Perfect for home, classroom, homeschool & travel",
    ]
    c.setFont("Andika-Bold", 12.5)
    for f in feats:
        c.setFillColorRGB(*RGB["g"]); draw_star(c, bx0 + 0.45 * inch, y + 4, 6, fill=True)
        c.setFillColorRGB(0.15, 0.15, 0.2); c.drawString(bx0 + 0.65 * inch, y, f); y -= 21
    # thumbnails row
    th = ["unicorn", "rocket", "pumpkin", "icecream"]
    s = 1.6 * inch; gap = (bx1 - bx0 - 0.4 * inch - s * 4) / 3
    for i, k in enumerate(th):
        draw_color_art(c, k, bx0 + 0.2 * inch + i * (s + gap), bleed + 2.6 * inch, s)
    # barcode area (KDP places barcode bottom-right of back cover)
    c.setFillColorRGB(1, 1, 1)
    c.rect(bleed + W - 0.25 * inch - 2.1 * inch, bleed + 0.25 * inch, 2.1 * inch, 1.3 * inch, fill=1, stroke=0)
    c.save()
    return spine / inch, CW / inch, CH / inch


if __name__ == "__main__":
    n = build_interior()
    sp, cw, ch = build_cover(n)
    print(f"Interior pages: {n}")
    print(f"Cover: {cw:.3f} x {ch:.3f} in, spine {sp:.3f} in")
