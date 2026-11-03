"""Themed 'Big Preschool Workbook' engine (ages 3-5), 8.5x11 B&W, double-sided.

python3 workbook.py dino        (or vehicles / ocean / space / unicorn / all)
"""
import os, sys, random, math
from lib import *

AUTHOR = "Abdelrahman Maghraby"

THEMES = {
    "dino": dict(name="Dino", hero="dino", mascots=["dino", "trex", "stego", "trike", "brachio", "ptero", "hatch", "dragon"],
                 icon="dinoegg", start="hatch", end="dinoegg", accent="g", accent2="y",
                 thumbs=["trex", "stego", "trike", "ptero"], word="dinosaur"),
    "vehicles": dict(name="Vehicles", hero="truck", mascots=["car", "bus", "truck", "train", "airplane", "tractor", "helicopter", "boat"],
                     icon="car", start="car", end="house", accent="r", accent2="y",
                     thumbs=["bus", "train", "tractor", "airplane"], word="vehicle"),
    "ocean": dict(name="Ocean", hero="whale", mascots=["whale", "fish", "octopus", "crab", "shark", "starfish", "jellyfish", "dolphin", "turtle"],
                  icon="fish", start="fish", end="starfish", accent="b", accent2="y",
                  thumbs=["octopus", "crab", "dolphin", "turtle"], word="sea animal"),
    "space": dict(name="Space", hero="rocket", mascots=["rocket", "ufo", "planet", "earth", "moon", "star", "alien", "rocket2", "comet"],
                  icon="star", start="rocket", end="moon", accent="p", accent2="y",
                  thumbs=["ufo", "alien", "planet", "earth"], word="space friend"),
    "unicorn": dict(name="Unicorn", hero="unicorn", mascots=["unicorn", "rainbow", "star", "cupcake", "crown", "gem", "butterfly", "flower", "valentine"],
                    icon="valentine", start="unicorn", end="rainbow", accent="k", accent2="w",
                    thumbs=["rainbow", "crown", "cupcake", "butterfly"], word="magic friend"),
}

LETTER_PICS = [("apple", "Apple"), ("bear", "Bear"), ("cat", "Cat"), ("dog", "Dog"), ("easteregg", "Egg"),
               ("fish", "Fish"), ("gift", "Gift"), ("hat", "Hat"), ("icecream", "Ice cream"),
               ("jellyfish", "Jellyfish"), ("key", "Key"), ("lion", "Lion"), ("mouse", "Mouse"),
               ("acorn", "Nut"), ("owl", "Owl"), ("pig", "Pig"), ("crown", "Queen's crown"),
               ("rocket", "Rocket"), ("sun", "Sun"), ("tree", "Tree"), ("umbrella", "Umbrella"),
               ("volcano", "Volcano"), ("whale", "Whale"), ("xylophone", "Xylophone"), ("yoyo", "Yo-yo"),
               ("zebra", "Zebra")]
WORD_PICS = [("apple", "apple"), ("bus", "bus"), ("cat", "cat"), ("dog", "dog"), ("duck", "duck"),
             ("fish", "fish"), ("fox", "fox"), ("frog", "frog"), ("gift", "gift"), ("hat", "hat"),
             ("chicken", "hen"), ("key", "key"), ("kite", "kite"), ("lion", "lion"), ("moon", "moon"),
             ("mouse", "mouse"), ("owl", "owl"), ("pig", "pig"), ("pear", "pear"), ("rocket", "rocket"),
             ("sun", "sun"), ("star", "star"), ("tree", "tree"), ("truck", "truck"), ("whale", "whale"),
             ("zebra", "zebra"), ("bat", "bat"), ("bell", "bell"), ("boat", "boat"), ("book", "book"),
             ("cake", "cake"), ("car", "car"), ("cow", "cow"), ("crab", "crab"), ("drum", "drum"),
             ("ghost", "ghost"), ("horse", "horse"), ("house", "house"), ("leaf", "leaf"), ("milk", "milk"),
             ("robot", "robot"), ("sock", "sock"), ("snail", "snail"), ("snake", "snake"), ("tent", "tent"),
             ("train", "train"), ("turtle", "turtle"), ("drum", "drum"), ("lemon", "lemon"), ("nut", "nut")]
WORD_PICS = [(k, w) for k, w in WORD_PICS if k in D]
CVC = [("cat", "c_t", "a"), ("dog", "d_g", "o"), ("pig", "p_g", "i"), ("bus", "b_s", "u"), ("sun", "s_n", "u"),
       ("fox", "f_x", "o"), ("hat", "h_t", "a"), ("bat", "b_t", "a"), ("cup", "c_p", "u"), ("chicken", "h_n", "e"),
       ("ladybug", "b_g", "u"), ("tent", "t_nt", "e")]
NUMWORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
COLORS6 = ["r", "b", "y", "g", "o", "p"]


class WB:
    def __init__(self, theme):
        self.T = THEMES[theme]; self.key = theme
        self.out = os.path.join(OUTROOT, f"{self.T['name'].lower()}-big-preschool-workbook")
        os.makedirs(self.out, exist_ok=True)
        self.b = Book(os.path.join(self.out, "interior.pdf"))
        self.c = self.b.c; self.rng = random.Random(theme)
        self.toc = []

    # ------------------------------------------------ helpers
    def lr(self):
        return self.b.margins()

    def head(self, title, instr, mascot=None):
        c = self.c; l, r = self.lr()
        c.setFillGray(0); c.setFont("Fredoka-Bold", 24); c.drawString(l, H - 0.95 * inch, title)
        c.setFont("Andika", 13); fs = fit_font(c, instr, "Andika", r - l - 1.1 * inch, 13)
        c.setFont("Andika", fs); c.drawString(l, H - 1.27 * inch, instr)
        m = mascot or self.rng.choice(self.T["mascots"])
        lineart(c, m, r - 0.95 * inch, H - 1.45 * inch, 0.95 * inch, pad=False, lw=1)
        c.setLineWidth(1); c.setStrokeGray(0.6); c.line(l, H - 1.5 * inch, r, H - 1.5 * inch); c.setStrokeGray(0)

    def lines(self, l, r, base, h):
        c = self.c; c.setStrokeGray(0.55); c.setLineWidth(1)
        c.line(l, base + h, r, base + h); c.line(l, base, r, base)
        c.setDash(4, 4); c.line(l, base + h / 2, r, base + h / 2); c.setDash()
        c.setStrokeGray(0)

    def gray_text(self, txt, x, base, h, gray=0.78):
        c = self.c; fs = h / 0.72
        c.setFillGray(gray); c.setFont("Andika", fs); c.drawString(x, base, txt); c.setFillGray(0)
        return c.stringWidth(txt, "Andika", fs)

    def dashed(self, pts, lw=3.2):
        c = self.c; c.setLineWidth(lw); c.setStrokeGray(0.5); c.setDash(7, 5); c.setLineCap(1)
        p = c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0); c.setDash(); c.setStrokeGray(0)

    def page(self):
        self.b.next()

    def divider(self, title, sub):
        self.toc.append((title, self.b.page))
        c = self.c; l, r = self.lr(); cx = (l + r) / 2
        c.setLineWidth(3); c.roundRect(l, 1 * inch, r - l, H - 2 * inch, 30)
        fs = fit_font(c, title, "Fredoka-Bold", r - l - 60, 36); c.setFont("Fredoka-Bold", fs)
        c.drawCentredString(cx, H - 2.4 * inch, title)
        c.setFont("Andika", 15); c.drawCentredString(cx, H - 2.95 * inch, sub)
        lineart(c, self.rng.choice(self.T["mascots"]), cx - 2.2 * inch, 2.2 * inch, 4.4 * inch, pad=False, lw=2.2)
        self.page()

    # ------------------------------------------------ sections
    def front(self):
        c = self.c; T = self.T
        l, r = self.lr(); cx = (l + r) / 2
        c.setFont("Fredoka-Bold", 40); c.drawCentredString(cx, H - 2.2 * inch, f"{T['name']} Big")
        c.drawCentredString(cx, H - 2.8 * inch, "Preschool Workbook")
        c.setFont("Andika", 15); c.drawCentredString(cx, H - 3.4 * inch, "Tracing - Letters - Numbers - Shapes - Early Math - Phonics - Puzzles")
        c.setFont("Andika-Bold", 14); c.drawCentredString(cx, H - 3.75 * inch, "Ages 3-5 | Pre-K & Kindergarten Prep")
        lineart(c, T["hero"], cx - 2 * inch, 2.2 * inch, 4 * inch, pad=False, lw=2.2)
        c.setFont("Fredoka", 16); c.drawCentredString(cx, 1.3 * inch, AUTHOR)
        self.b.next(number=False)
        copyright_block(self.b, f"{T['name']} Big Preschool Workbook", AUTHOR)
        c.setLineWidth(2); c.roundRect(l + 20, 2.5 * inch, r - l - 40, 6 * inch, 24)
        c.setFont("Fredoka-Bold", 36); c.drawCentredString(cx, 7.4 * inch, "This Book"); c.drawCentredString(cx, 6.8 * inch, "Belongs To:")
        c.setLineWidth(1.5); c.line(cx - 2.6 * inch, 5.3 * inch, cx + 2.6 * inch, 5.3 * inch)
        lineart(c, T["start"], cx - 0.9 * inch, 2.8 * inch, 1.8 * inch, pad=False)
        self.b.next(number=False)
        self.b.blank_back()
        self.plan_page = self.b.page
        self.b.next()          # placeholder: plan drawn later via second pass
        self.b.next()

    def prewriting(self, n=24):
        self.divider("Part 1: Pencil Control", "Trace the dotted lines from left to right.")
        kinds = ["straight", "straight", "slant", "zigzag", "wave", "bumps", "castle", "loops"]
        for i in range(n):
            kind = kinds[min(i // 3, len(kinds) - 1)] if i < 24 else self.rng.choice(kinds)
            self.head("Trace the Path", f"Help each {self.T['word']} get home. Trace the dotted line!")
            l, r = self.lr(); rows = 5
            for j in range(rows):
                yc = H - 2.3 * inch - j * 1.65 * inch
                lineart(self.c, self.T["start"], l, yc - 0.4 * inch, 0.8 * inch, pad=False, lw=1)
                lineart(self.c, self.T["end"], r - 0.8 * inch, yc - 0.4 * inch, 0.8 * inch, pad=False, lw=1)
                x0, x1 = l + 0.95 * inch, r - 0.95 * inch
                pts = []
                N = 120; amp = 0.42 * inch; per = 6 + (i % 3) * 2
                for t in range(N + 1):
                    u = t / N; x = x0 + u * (x1 - x0)
                    if kind == "straight": y = yc
                    elif kind == "slant": y = yc + amp * (1 - 2 * u) * (1 if j % 2 else -1)
                    elif kind == "zigzag": y = yc + amp * (2 * abs((u * per) % 2 - 1) - 1)
                    elif kind == "wave": y = yc + amp * math.sin(u * per * math.pi)
                    elif kind == "bumps": y = yc - amp * 0.8 + amp * 1.6 * abs(math.sin(u * per * math.pi / 2))
                    elif kind == "castle": y = yc + amp * (1 if int(u * per) % 2 else -1)
                    else:  # loops
                        a = u * per * 2 * math.pi
                        x = x0 + u * (x1 - x0) * 0.92 + 0.18 * inch * math.sin(a)
                        y = yc + 0.3 * inch * -math.cos(a)
                    pts.append((x, y))
                if kind == "castle":   # make square corners
                    sq = []
                    for p, q in zip(pts, pts[1:]):
                        sq.append(p)
                        if abs(q[1] - p[1]) > 1: sq.append((q[0], p[1]))
                    pts = sq + [pts[-1]]
                self.dashed(pts)
            self.page()

    SHAPES = ["circle", "square", "triangle", "rectangle", "star", "heart", "oval", "diamond"]

    def shape_path(self, kind, cx, cy, s):
        c = self.c; p = c.beginPath()
        if kind == "circle": p.circle(cx, cy, s / 2)
        elif kind == "oval": p.ellipse(cx - s * 0.6, cy - s * 0.38, s * 1.2, s * 0.76)
        elif kind == "square": p.rect(cx - s / 2, cy - s / 2, s, s)
        elif kind == "rectangle": p.rect(cx - s * 0.7, cy - s * 0.38, s * 1.4, s * 0.76)
        else:
            if kind == "triangle": pts = [(0, 0.5), (0.5, -0.43), (-0.5, -0.43)]
            elif kind == "diamond": pts = [(0, 0.55), (0.4, 0), (0, -0.55), (-0.4, 0)]
            elif kind == "star":
                pts = [((0.52 if k % 2 == 0 else 0.22) * math.cos(math.pi / 2 + k * math.pi / 5),
                        (0.52 if k % 2 == 0 else 0.22) * math.sin(math.pi / 2 + k * math.pi / 5)) for k in range(10)]
            else:  # heart
                pts = [(0.5 * 16 * math.sin(t) ** 3 / 17, 0.5 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17 + 0.05)
                       for t in [k * 2 * math.pi / 60 for k in range(60)]]
            p.moveTo(cx + pts[0][0] * s, cy + pts[0][1] * s)
            for x, y in pts[1:]:
                p.lineTo(cx + x * s, cy + y * s)
            p.close()
        return p

    def shape(self, kind, cx, cy, s, dashed=True):
        c = self.c
        if dashed: c.setDash(6, 4); c.setStrokeGray(0.45)
        c.setLineWidth(3); c.drawPath(self.shape_path(kind, cx, cy, s), stroke=1, fill=0)
        c.setDash(); c.setStrokeGray(0)

    def shapes(self):
        self.divider("Part 2: Shapes & Colors", "Trace, color and find the shapes.")
        names = {"r": "red", "b": "blue", "y": "yellow", "g": "green", "o": "orange", "p": "purple"}
        for i, s in enumerate(self.SHAPES):
            col = names[COLORS6[i % 6]]
            self.head(f"This is a {s.title()}", f"Trace the big {s}. Color it {col}!")
            l, r = self.lr(); cx = (l + r) / 2
            self.shape(s, cx, H - 4.4 * inch, 4.2 * inch)
            self.c.setFont("Fredoka-Bold", 30); self.c.drawCentredString(cx, H - 7.0 * inch, s)
            for k in range(4):
                self.shape(s, l + (k + 0.5) * (r - l) / 4, 2.2 * inch, 1.3 * inch)
            self.page()
            self.head(f"Find the {s.title()}s", f"Color every {s} {col}. Trace the dotted ones first!")
            rng = random.Random(i)
            for k in range(20):
                kind = s if k % 3 == 0 else rng.choice(self.SHAPES)
                x = l + (k % 4 + 0.5) * (r - l) / 4; y = H - 2.4 * inch - (k // 4) * 1.6 * inch
                self.shape(kind, x, y, 1.1 * inch, dashed=False)
            self.page()
        for i in range(4):
            self.head("Shape Hunt", "Color the shapes: circles red, squares blue, triangles yellow, stars green.")
            l, r = self.lr(); rng = random.Random(100 + i)
            for k in range(24):
                kind = rng.choice(["circle", "square", "triangle", "star"])
                x = l + (k % 4 + 0.5) * (r - l) / 4; y = H - 2.3 * inch - (k // 4) * 1.35 * inch
                self.shape(kind, x, y, 0.95 * inch, dashed=False)
            self.page()

    def letters(self):
        self.divider("Part 3: Letters A to Z", "Trace each letter, then color the picture.")
        l, r = None, None
        for i, (pk, word) in enumerate(LETTER_PICS):
            U = chr(65 + i); low = U.lower()
            self.head(f"Letter {U} {low}", f"Trace the letters. Start at the dot!")
            l, r = self.lr()
            wbig = self.gray_text(U, l + 0.3 * inch, H - 4.3 * inch, 2.3 * inch)
            self.gray_text(low, l + 0.3 * inch + wbig + 0.5 * inch, H - 4.3 * inch, 2.3 * inch)
            self.c.setFont("Fredoka-Bold", 22)
            self.c.drawString(r - 2.6 * inch, H - 2.6 * inch, f"{U} is for")
            self.c.drawString(r - 2.6 * inch, H - 2.95 * inch, word)
            lineart(self.c, pk, r - 2.6 * inch, H - 4.55 * inch, 1.25 * inch, pad=False, lw=1.2)
            for row, ch in enumerate([U, U, low, low]):
                base = H - 5.6 * inch - row * 1.25 * inch; h = 0.75 * inch
                self.lines(l, r, base, h)
                x = l + 0.15 * inch; n = 6 if row % 2 == 0 else 3
                for k in range(n):
                    w = self.gray_text(ch, x, base, h if ch.isupper() else h * 0.68, 0.72 if k == 0 else 0.84)
                    x += w + 0.45 * inch
            self.page()
            self.head(f"{U} is for {word}", f"Color the {word.lower()}. Then circle every {U} and {low} below.", mascot=self.T["hero"])
            lineart(self.c, pk, (l + r) / 2 - 2.5 * inch, H - 7.3 * inch, 5.0 * inch, pad=False, lw=2)
            rng = random.Random(i)
            pool = [U, low] * 5 + rng.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".replace(U, "").replace(low, ""), 14)
            rng.shuffle(pool)
            cell = (r - l) / 12
            for k, ch in enumerate(pool):
                x = l + (k % 12 + 0.5) * cell; y = 2.0 * inch - (k // 12) * 0.62 * inch
                self.c.setFont("Andika", 30); self.c.drawCentredString(x, y, ch)
            self.page()

    def icons(self, n, x0, y0, w, h, cols=5, key=None):
        key = key or self.T["icon"]; rows = max(1, math.ceil(n / cols))
        s = min(w / cols, h / rows) * 0.9
        for k in range(n):
            lineart(self.c, key, x0 + (k % cols) * (w / cols), y0 + h - (k // cols + 1) * (h / rows), s, pad=False, lw=1)

    def numbers(self):
        self.divider("Part 4: Numbers 1 to 20", "Trace, count and color.")
        for n in range(1, 21):
            l, r = self.lr()
            self.head(f"Number {n}", f"Trace the number {n}. Say it out loud: {NUMWORDS[n]}!")
            self.gray_text(str(n), l + 0.3 * inch, H - 4.3 * inch, 2.3 * inch)
            self.c.setFont("Fredoka-Bold", 30); self.c.drawString(r - 3.0 * inch, H - 3.2 * inch, NUMWORDS[n])
            for row in range(4):
                base = H - 5.5 * inch - row * 1.3 * inch; h = 0.8 * inch
                self.lines(l, r, base, h)
                x = l + 0.15 * inch
                for k in range(6 if n < 10 else 4 if row % 2 == 0 else 2):
                    x += self.gray_text(str(n), x, base, h, 0.72 if k == 0 else 0.84) + 0.5 * inch
            self.page()
            l, r = self.lr()
            total = 10 if n <= 10 else 20
            self.head(f"Count to {n}", f"Color {n} {'picture' if n == 1 else 'pictures'}. Count as you color!")
            self.icons(total, l, H - 6.6 * inch, r - l, 4.8 * inch, cols=5)
            self.c.setFont("Fredoka-Bold", 20); self.c.drawString(l, 2.2 * inch, f"How many did you color?")
            self.c.setLineWidth(2); self.c.roundRect(r - 1.6 * inch, 1.6 * inch, 1.4 * inch, 1.1 * inch, 12)
            self.page()

    def math(self):
        self.divider("Part 5: Early Math", "Count, compare, add and find patterns.")
        rng = random.Random(5)
        for p in range(6):   # count and write
            l, r = self.lr(); self.head("Count and Write", "Count the pictures. Write the number in the box.")
            for j in range(5):
                n = rng.randint(1 + p, min(10, 4 + p * 2)); y = H - 2.1 * inch - j * 1.7 * inch
                self.icons(n, l, y - 1.3 * inch, r - l - 1.6 * inch, 1.3 * inch, cols=10 if n > 5 else 5)
                self.c.setLineWidth(2); self.c.roundRect(r - 1.3 * inch, y - 1.2 * inch, 1.2 * inch, 1.1 * inch, 10)
            self.page()
        for p in range(6):   # more / less
            l, r = self.lr(); word = "MORE" if p % 2 == 0 else "LESS"
            self.head(f"Which Has {word.title()}?", f"Circle the group that has {word.lower()}.")
            for j in range(3):
                a, bnum = rng.sample(range(1, 10), 2); y = H - 1.8 * inch - (j + 1) * 2.75 * inch + 0.2 * inch
                for s, n in enumerate([a, bnum]):
                    x = l + s * (r - l) / 2 + 0.15 * inch
                    self.c.setLineWidth(1.5); self.c.roundRect(x, y, (r - l) / 2 - 0.3 * inch, 2.4 * inch, 14)
                    self.icons(n, x + 0.15 * inch, y + 0.15 * inch, (r - l) / 2 - 0.6 * inch, 2.1 * inch, cols=3)
            self.page()
        for p in range(8):   # picture addition
            l, r = self.lr(); self.head("Add the Pictures", "Count both groups. How many in all?")
            for j in range(4):
                a = rng.randint(1, 4 + (p > 3)); bb = rng.randint(1, 4 + (p > 3)); y = H - 2.0 * inch - j * 2.15 * inch
                w = (r - l - 2.4 * inch) / 2
                self.icons(a, l, y - 1.6 * inch, w, 1.6 * inch, cols=3)
                self.c.setFont("Fredoka-Bold", 34); self.c.drawCentredString(l + w + 0.3 * inch, y - 1.0 * inch, "+")
                self.icons(bb, l + w + 0.6 * inch, y - 1.6 * inch, w, 1.6 * inch, cols=3)
                self.c.drawCentredString(r - 1.5 * inch, y - 1.0 * inch, "=")
                self.c.setLineWidth(2); self.c.roundRect(r - 1.2 * inch, y - 1.4 * inch, 1.1 * inch, 1.0 * inch, 10)
            self.page()
        for p in range(6):   # patterns
            l, r = self.lr(); self.head("What Comes Next?", "Look at the pattern. Draw the shape that comes next.")
            pats = ["AB", "AAB", "ABB", "ABC", "AABB", "ABCD"]
            for j in range(6):
                pat = pats[(p + j) % 6]; kinds = rng.sample(["circle", "square", "triangle", "star", "heart", "diamond"], 4)
                seq = [kinds["ABCD".index(ch)] for ch in (pat * 4)][:7]
                y = H - 2.3 * inch - j * 1.4 * inch
                cw = (r - l) / 8
                for k, s in enumerate(seq):
                    self.shape(s, l + (k + 0.5) * cw, y, 0.75 * inch, dashed=False)
                self.c.setLineWidth(2); self.c.setDash(5, 4)
                self.c.roundRect(l + 7 * cw + 0.05 * inch, y - 0.5 * inch, cw - 0.1 * inch, 1.0 * inch, 8); self.c.setDash()
            self.page()
        for p in range(4):   # big / small
            l, r = self.lr(); word = "BIGGER" if p % 2 == 0 else "SMALLER"
            self.head(f"Circle the {word.title()} One", f"Look at each row. Circle the {word.lower()} picture.")
            for j in range(4):
                k = self.T["mascots"][(p * 4 + j) % len(self.T["mascots"])]; y = H - 2.0 * inch - (j + 1) * 2.1 * inch
                big = rng.random() < 0.5
                lineart(self.c, k, l + 0.3 * inch, y + (0 if big else 0.5 * inch), (1.9 if big else 0.9) * inch, pad=False, lw=1.2)
                lineart(self.c, k, (l + r) / 2 + 0.6 * inch, y + (0.5 * inch if big else 0), (0.9 if big else 1.9) * inch, pad=False, lw=1.2)
            self.page()

    def phonics(self):
        self.divider("Part 6: First Sounds & Words", "Listen, match and read.")
        rng = random.Random(6)
        pics = [(k, w) for k, w in WORD_PICS]
        for p in range(10):   # beginning sound
            l, r = self.lr(); self.head("Beginning Sounds", "Say the name of each picture. Circle the letter it starts with.")
            chosen = rng.sample(pics, 6)
            for j, (k, w) in enumerate(chosen):
                x = l + (j % 2) * (r - l) / 2; y = H - 1.8 * inch - (j // 2 + 1) * 2.9 * inch + 0.3 * inch
                lineart(self.c, k, x + 0.1 * inch, y + 0.75 * inch, 1.8 * inch, pad=False, lw=1.2)
                opts = [w[0]] + rng.sample([ch for ch in "abcdefghijklmnoprstuvwz" if ch != w[0]], 2); rng.shuffle(opts)
                for q, ch in enumerate(opts):
                    self.c.setFont("Andika", 30); self.c.drawCentredString(x + 0.5 * inch + q * 1.05 * inch, y + 0.15 * inch, ch)
            self.page()
        for p in range(2):    # CVC
            l, r = self.lr(); self.head("Missing Sounds", "Say the word. Write the missing vowel: a, e, i, o, or u.")
            for j, (k, word, v) in enumerate(CVC[p * 6:(p + 1) * 6]):
                if k not in D: continue
                x = l + (j % 2) * (r - l) / 2; y = H - 1.8 * inch - (j // 2 + 1) * 2.9 * inch + 0.3 * inch
                lineart(self.c, k, x + 0.2 * inch, y + 0.8 * inch, 1.7 * inch, pad=False, lw=1.2)
                self.c.setFont("Andika", 40); self.c.drawString(x + 0.3 * inch, y + 0.1 * inch, word.replace("_", " __ "))
            self.page()
        for p in range(8):    # match picture to word
            l, r = self.lr(); self.head("Match the Words", "Draw a line from each picture to its word.")
            chosen = rng.sample([(k, w) for k, w in pics if len(w) <= 5], 4)
            words = [w for _, w in chosen]; rng.shuffle(words)
            for j, (k, w) in enumerate(chosen):
                y = H - 1.8 * inch - (j + 1) * 2.1 * inch + 0.2 * inch
                lineart(self.c, k, l + 0.2 * inch, y, 1.6 * inch, pad=False, lw=1.2)
                self.c.circle(l + 2.2 * inch, y + 0.8 * inch, 5, fill=1)
                self.c.circle(r - 2.4 * inch, y + 0.8 * inch, 5, fill=1)
                self.c.setFont("Andika", 34); self.c.drawString(r - 2.1 * inch, y + 0.6 * inch, words[j])
            self.page()
        for p in range(10):   # trace words
            l, r = self.lr(); self.head("Trace the Words", "Trace each word. Then color the picture!")
            chosen = rng.sample(pics, 4)
            for j, (k, w) in enumerate(chosen):
                y = H - 1.8 * inch - (j + 1) * 2.1 * inch + 0.2 * inch
                lineart(self.c, k, l + 0.1 * inch, y, 1.7 * inch, pad=False, lw=1.2)
                self.lines(l + 2.1 * inch, r, y + 0.35 * inch, 0.9 * inch)
                self.gray_text(w, l + 2.3 * inch, y + 0.35 * inch, 0.9 * inch * 0.68 / 0.68 * 0.66)
            self.page()

    def maze(self, cols, rows, x0, y0, w, h, seed):
        rng = random.Random(seed); c = self.c
        walls = {(x, y): [True, True, True, True] for x in range(cols) for y in range(rows)}  # N E S W
        stack = [(0, 0)]; seen = {(0, 0)}
        while stack:
            x, y = stack[-1]
            nb = [(x, y - 1, 0, 2), (x + 1, y, 1, 3), (x, y + 1, 2, 0), (x - 1, y, 3, 1)]
            nb = [n for n in nb if 0 <= n[0] < cols and 0 <= n[1] < rows and (n[0], n[1]) not in seen]
            if not nb:
                stack.pop(); continue
            nx, ny, wa, wb = rng.choice(nb)
            walls[(x, y)][wa] = False; walls[(nx, ny)][wb] = False
            seen.add((nx, ny)); stack.append((nx, ny))
        walls[(0, 0)][3] = False; walls[(cols - 1, rows - 1)][1] = False
        cs = min(w / cols, h / rows); ox = x0 + (w - cs * cols) / 2; oy = y0 + h - (h - cs * rows) / 2
        c.setLineWidth(3 if cols < 9 else 2.2); c.setLineCap(1)
        for (x, y), wl in walls.items():
            px, py = ox + x * cs, oy - y * cs
            if wl[0]: c.line(px, py, px + cs, py)
            if wl[1]: c.line(px + cs, py, px + cs, py - cs)
            if wl[2]: c.line(px, py - cs, px + cs, py - cs)
            if wl[3]: c.line(px, py, px, py - cs)
        return ox, oy, cs

    def puzzles(self):
        self.divider("Part 7: Puzzles & Fun", "Mazes, odd one out, and color by number.")
        T = self.T
        for i in range(20):
            l, r = self.lr(); self.head(f"Maze {i + 1}", f"Help the {T['word']} find the way to the end!")
            n = 4 + i // 3
            ox, oy, cs = self.maze(n, n + 1, l + 0.9 * inch, 1.0 * inch, r - l - 1.8 * inch, H - 2.8 * inch, i)
            lineart(self.c, T["start"], l, oy - 0.8 * inch, 0.8 * inch, pad=False, lw=1)
            lineart(self.c, T["end"], r - 0.8 * inch, oy - (n + 1) * cs, 0.8 * inch, pad=False, lw=1)
            self.page()
        rng = random.Random(7)
        for i in range(10):
            l, r = self.lr(); self.head("Odd One Out", "Which picture is different? Circle it!")
            for j in range(4):
                a, bb = rng.sample(T["mascots"] + ["apple", "star", "fish", "cat"], 2); odd = rng.randrange(4)
                y = H - 1.8 * inch - (j + 1) * 2.1 * inch + 0.2 * inch
                for k in range(4):
                    lineart(self.c, bb if k == odd else a, l + k * (r - l) / 4 + 0.1 * inch, y, (r - l) / 4 - 0.3 * inch, pad=False, lw=1.1)
            self.page()
        # preschool color by number (1-6)
        keys = (T["mascots"] * 3)[:20]
        for i, k in enumerate(keys):
            g, bg = grid_of(k)
            colors = []
            for row in g:
                for ch in row:
                    if ch not in colors: colors.append(ch)
            colors.remove(bg); colors.insert(0, bg)
            nums = list(range(1, len(colors) + 1)); random.Random(i).shuffle(nums)
            m = dict(zip(colors, nums))
            p = dict(grid=g, texts=[[str(m[ch]) for ch in row] for row in g], key=[(str(m[ch]), ch) for ch in colors])
            l, r = self.lr(); self.head("Color by Number", "Color each square using the number code. What do you see?", mascot=self.T["start"])
            kb = draw_key(self.c, p["key"], l, r, H - 1.7 * inch)
            draw_grid(self.c, p, l, r, kb - 14, 0.8 * inch)
            self.page()

    def coloring(self):
        self.divider("Part 8: Coloring Fun", "Color your favorite friends!")
        for i, k in enumerate(list(dict.fromkeys(self.T["mascots"] + ["owl", "cat", "dog", "bunny", "bear", "turtle", "bee", "butterfly", "frog"]))[:12]):
            l, r = self.lr(); self.head(D[k][0], "Color the picture any way you like!", mascot=k)
            lineart(self.c, k, l + 0.2 * inch, 1.2 * inch, r - l - 0.4 * inch, pad=False, lw=2.6)
            self.page()

    def certificate(self):
        c = self.c; l, r = self.lr(); cx = (l + r) / 2
        c.setLineWidth(4); c.roundRect(l, 1.2 * inch, r - l, H - 2.4 * inch, 20)
        c.setFont("Fredoka-Bold", 34); c.drawCentredString(cx, H - 2.5 * inch, "Certificate")
        c.setFont("Fredoka", 20); c.drawCentredString(cx, H - 3.0 * inch, "of Completion")
        c.setFont("Andika", 14); c.drawCentredString(cx, H - 3.9 * inch, "This certificate is proudly presented to")
        c.line(cx - 2.5 * inch, H - 4.8 * inch, cx + 2.5 * inch, H - 4.8 * inch)
        c.drawCentredString(cx, H - 5.4 * inch, f"for finishing the {self.T['name']} Big Preschool Workbook!")
        lineart(c, self.T["hero"], cx - 1.1 * inch, 2.6 * inch, 2.2 * inch, pad=False)
        c.line(l + 0.6 * inch, 2.2 * inch, l + 3 * inch, 2.2 * inch); c.drawString(l + 0.6 * inch, 1.95 * inch, "Date")
        c.line(r - 3 * inch, 2.2 * inch, r - 0.6 * inch, 2.2 * inch); c.drawString(r - 3 * inch, 1.95 * inch, "Signed")
        self.b.next(number=False)

    def build(self, plan=None):
        self.front()
        start = self.b.page
        self.prewriting(); self.shapes(); self.letters(); self.numbers()
        self.math(); self.phonics(); self.puzzles(); self.coloring()
        end = self.b.page - 1
        self.certificate()
        if self.b.page % 2 == 0:
            self.b.next(number=False)
        self.b.c.save()
        return self.b.page - 1, start, end


def plan_overlay(path, plan_page, start, end, toc, name):
    """Draw the 52-week plan + contents onto the two reserved pages."""
    from pypdf import PdfReader, PdfWriter
    import io
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H))
    # page A: contents + how to use (odd page => gutter on left)
    l, r = cbc.GUTTER, W - cbc.OUTSIDE
    c.setFont("Fredoka-Bold", 26); c.drawCentredString((l + r) / 2, H - 1.1 * inch, "What's Inside")
    y = H - 1.7 * inch
    for t, p in toc:
        c.setFont("Andika-Bold", 14); c.drawString(l + 0.3 * inch, y, t)
        c.drawRightString(r - 0.3 * inch, y, f"page {p}"); y -= 26
    y -= 20
    c.setFont("Fredoka-Bold", 18); c.drawString(l + 0.3 * inch, y, "Tips for grown-ups"); y -= 24
    c.setFont("Andika", 12.5)
    for ln in ["Do one page a day, five days a week - a full year of learning (see the plan).",
               "Keep sessions short and fun: 10 to 15 minutes is plenty for little hands.",
               "Use a thick pencil or crayons. Praise effort, not perfection!",
               "Say letters, sounds and numbers out loud together while tracing.",
               "Skip around if your child loves a section - every part stands alone."]:
        c.drawString(l + 0.3 * inch, y, "- " + ln); y -= 19
    c.showPage()
    # page B: 52-week plan (even page => gutter on right)
    l, r = cbc.OUTSIDE, W - cbc.GUTTER
    c.setFont("Fredoka-Bold", 24); c.drawCentredString((l + r) / 2, H - 1.0 * inch, "My 52-Week Learning Plan")
    c.setFont("Andika", 11); c.drawCentredString((l + r) / 2, H - 1.3 * inch, "Color a star when the week is done!")
    total = end - start + 1; per = total / 52
    cw = (r - l) / 4; rh = (H - 2.0 * inch) / 13
    for wk in range(52):
        a = start + round(wk * per); bpage = start + round((wk + 1) * per) - 1
        x = l + (wk // 13) * cw; yy = H - 1.65 * inch - (wk % 13) * rh
        draw_star(c, x + 12, yy - 4, 8)
        c.setFont("Andika-Bold", 10.5); c.drawString(x + 26, yy - 2, f"Week {wk + 1}")
        c.setFont("Andika", 9.5); c.drawString(x + 26, yy - 15, f"pages {a}-{bpage}")
    c.save()
    ov = PdfReader(io.BytesIO(buf.getvalue()))
    rd = PdfReader(path); wr = PdfWriter()
    for i, pg in enumerate(rd.pages):
        if i == plan_page - 1: pg.merge_page(ov.pages[0])
        if i == plan_page: pg.merge_page(ov.pages[1])
        wr.add_page(pg)
    with open(path, "wb") as f:
        wr.write(f)


def run(theme):
    wb = WB(theme)
    pages, start, end = wb.build()
    plan_overlay(os.path.join(wb.out, "interior.pdf"), wb.plan_page, start, end, wb.toc, wb.T["name"])
    T = wb.T; name = T["name"]
    sp, cw, ch = generic_cover(os.path.join(wb.out, "cover.pdf"), pages, dict(
        title1=f"{name} Big", title2="Preschool Workbook", tagline=f"{pages} Pages of Learning Fun!",
        ages="Ages 3-5 | Pre-K & Kindergarten Prep", author=AUTHOR, hero=T["hero"], thumbs=T["thumbs"],
        accent=T["accent"], accent2=T["accent2"],
        badges=[("ABC", "r"), ("123", "b"), ("Shapes", "p"), ("Mazes", "o")],
        blurb=[f"A whole year of preschool learning with your favorite {T['word']}s!",
               "Tracing, letters, numbers, shapes, early math, first sounds,",
               "mazes and coloring - all in one big workbook."],
        features=[f"{pages} pages - a complete 52-week Pre-K plan, one page a day",
                  "Pencil control: lines, zigzags, waves and loops",
                  "Letters A-Z and numbers 1-20 with tracing and coloring",
                  "Shapes, counting, more/less, picture addition and patterns",
                  "Beginning sounds, first words, mazes and color by number",
                  "Progress plan and certificate of completion"],
        back_head="Learn. Trace. Play!"))
    write_readme(os.path.join(wb.out, "README.md"), dict(
        title=f"{name} Big Preschool Workbook", pages=pages, cw=cw, ch=ch, spine=sp, author=AUTHOR,
        price="$14.99", age="3-5 (Pre-K, Kindergarten)",
        subtitle=f"{pages} Pages of Pre-K Learning: Tracing, Letters, Numbers, Shapes, Early Math, Phonics & Mazes | A 52-Week Preschool Curriculum for Kids Ages 3-5",
        description=(f"**A whole year of preschool learning with {T['word']}s!** This big workbook takes your child from first pencil lines "
                     "to letters, numbers, shapes, early math and first words - one fun page at a time.\n\n"
                     "**Inside:**\n- Pencil control: straight lines, zigzags, waves, bumps and loops\n"
                     "- Shapes & colors: trace, color and find 8 shapes\n- Letters A-Z: trace uppercase and lowercase, color a picture for every letter, find-the-letter games\n"
                     "- Numbers 1-20: trace, count and color\n- Early math: count and write, more or less, picture addition, patterns, bigger and smaller\n"
                     "- First sounds & words: beginning sounds, missing vowels, word matching, word tracing\n"
                     "- Puzzles: 20 mazes that grow with your child, odd one out, color by number\n"
                     "- A 52-week learning plan and a certificate of completion\n\n"
                     "Perfect for preschool, Pre-K, kindergarten prep, homeschool and screen-free quiet time."),
        keywords=["preschool workbook ages 3-5", f"{name.lower()} activity book for kids", "pre k workbooks ages 4-5",
                  "tracing letters and numbers for preschoolers", "kindergarten prep workbook", "homeschool preschool curriculum",
                  "big workbook for toddlers learning"],
        categories=["Children's Books > Activities, Crafts & Games > Activity Books",
                    "Children's Books > Education & Reference > Alphabet", "Children's Books > Early Learning > Counting"]))
    print(f"{name}: {pages} pages, cover {cw:.3f}x{ch:.3f}, spine {sp:.3f}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "dino"
    for t in (THEMES if which == "all" else [which]):
        run(t)
