"""Mazes for Kids Ages 4-8: 100 mazes in 4 levels + solutions."""
import os, random
from collections import deque
from lib import *
from workbook import WB, AUTHOR

PAIRS = [("dog", "bone"), ("bunny", "carrot"), ("bee", "flower"), ("mouse", "cheese"), ("rocket", "moon"),
         ("car", "house"), ("fish", "starfish"), ("monkey", "banana"), ("bear", "cupcake"), ("hatch", "dinoegg"),
         ("cat", "fish"), ("chick", "chicken"), ("penguin", "snowflake"), ("squirrel", "acorn"), ("pirate" if False else "boat", "lighthouse"),
         ("unicorn", "rainbow"), ("owl", "moon"), ("frog", "lightning"), ("ufo", "planet"), ("pig", "apple")]
LEVELS = [("Level 1: Easy Mazes", "Warm up with small mazes.", (5, 6)),
          ("Level 2: Medium Mazes", "A little bigger and trickier.", (8, 10)),
          ("Level 3: Hard Mazes", "Lots of turns and dead ends!", (11, 14)),
          ("Level 4: Expert Mazes", "Only for maze masters!", (15, 19))]


class MZ(WB):
    def __init__(self):
        self.T = dict(mascots=["owl", "cat", "dog", "rocket"], word="friend")
        self.out = os.path.join(OUTROOT, "mazes-for-kids"); os.makedirs(self.out, exist_ok=True)
        self.b = Book(os.path.join(self.out, "interior.pdf")); self.c = self.b.c
        self.rng = random.Random("mazes"); self.toc = []; self.sol = []

    def maze_full(self, cols, rows, seed):
        rng = random.Random(seed)
        walls = {(x, y): [True, True, True, True] for x in range(cols) for y in range(rows)}
        stack = [(0, 0)]; seen = {(0, 0)}
        while stack:
            x, y = stack[-1]
            nb = [(x, y - 1, 0, 2), (x + 1, y, 1, 3), (x, y + 1, 2, 0), (x - 1, y, 3, 1)]
            nb = [n for n in nb if 0 <= n[0] < cols and 0 <= n[1] < rows and (n[0], n[1]) not in seen]
            if not nb:
                stack.pop(); continue
            nx, ny, wa, wb = rng.choice(nb)
            walls[(x, y)][wa] = False; walls[(nx, ny)][wb] = False; seen.add((nx, ny)); stack.append((nx, ny))
        walls[(0, 0)][3] = False; walls[(cols - 1, rows - 1)][1] = False
        prev = {(0, 0): None}; q = deque([(0, 0)])
        while q:
            x, y = q.popleft()
            for d, (dx, dy) in enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]):
                n = (x + dx, y + dy)
                if not walls[(x, y)][d] and n in walls and n not in prev:
                    prev[n] = (x, y); q.append(n)
        path = []; p = (cols - 1, rows - 1)
        while p: path.append(p); p = prev[p]
        return walls, path[::-1]

    def draw_maze(self, walls, cols, rows, x0, y0, w, h, lw, path=None):
        c = self.c; cs = min(w / cols, h / rows)
        ox = x0 + (w - cs * cols) / 2; oy = y0 + h - (h - cs * rows) / 2
        c.setLineWidth(lw); c.setLineCap(1); c.setStrokeGray(0)
        for (x, y), wl in walls.items():
            px, py = ox + x * cs, oy - y * cs
            if wl[0]: c.line(px, py, px + cs, py)
            if wl[1]: c.line(px + cs, py, px + cs, py - cs)
            if wl[2]: c.line(px, py - cs, px + cs, py - cs)
            if wl[3]: c.line(px, py, px, py - cs)
        if path:
            c.setStrokeGray(0.45); c.setLineWidth(max(1.2, cs * 0.3))
            pts = [(ox - cs * 0.5, oy - cs / 2)] + [(ox + (x + 0.5) * cs, oy - (y + 0.5) * cs) for x, y in path] + \
                  [(ox + (cols + 0.5) * cs, oy - (rows - 0.5) * cs)]
            p = c.beginPath(); p.moveTo(*pts[0])
            for q in pts[1:]: p.lineTo(*q)
            c.drawPath(p, stroke=1, fill=0); c.setStrokeGray(0)
        return ox, oy, cs

    def build(self):
        c = self.c; l, r = self.lr(); cx = (l + r) / 2
        c.setFont("Fredoka-Bold", 44); c.drawCentredString(cx, H - 2.3 * inch, "Mazes for Kids")
        c.setFont("Andika", 16); c.drawCentredString(cx, H - 2.9 * inch, "100 Fun Mazes from Easy to Expert")
        c.setFont("Andika-Bold", 14); c.drawCentredString(cx, H - 3.3 * inch, "Ages 4-8")
        lineart(c, "mouse", cx - 2.6 * inch, 2.4 * inch, 2.4 * inch, pad=False, lw=2)
        lineart(c, "cheese", cx + 0.4 * inch, 2.4 * inch, 2.2 * inch, pad=False, lw=2)
        c.setFont("Fredoka", 16); c.drawCentredString(cx, 1.3 * inch, AUTHOR)
        self.b.next(number=False)
        copyright_block(self.b, "Mazes for Kids Ages 4-8", AUTHOR)
        cbc.belongs_page(self.b); self.b.blank_back()
        n = 0
        for title, sub, (lo, hi) in LEVELS:
            self.divider(title, sub)
            for i in range(25):
                n += 1; size = lo + (hi - lo) * i // 24
                cols, rows = size, size + max(1, size // 4)
                s, e = PAIRS[(n - 1) % len(PAIRS)]
                walls, path = self.maze_full(cols, rows, n)
                self.sol.append((n, walls, cols, rows, path))
                l, r = self.lr()
                self.head(f"Maze {n}", f"Help the {D[s][0].lower()} get to the {D[e][0].lower()}!", mascot=s)
                lw = 3.2 if size < 8 else 2.4 if size < 12 else 1.8
                ox, oy, cs = self.draw_maze(walls, cols, rows, l + 0.9 * inch, 0.9 * inch, r - l - 1.8 * inch, H - 2.6 * inch, lw)
                lineart(c, s, l, oy - 0.85 * inch + min(0, 0), 0.85 * inch, pad=False, lw=1)
                lineart(c, e, r - 0.85 * inch, oy - rows * cs, 0.85 * inch, pad=False, lw=1)
                self.page()
        # solutions, 6 per page
        if self.b.page % 2 == 0: self.b.next(number=False)
        self.toc.append(("Solutions", self.b.page))
        for s0 in range(0, len(self.sol), 6):
            l, r = self.lr()
            c.setFont("Fredoka-Bold", 22); c.drawCentredString((l + r) / 2, H - 0.85 * inch, "Solutions")
            cw = (r - l) / 2; chh = (H - 1.3 * inch - 0.6 * inch) / 3
            for j, (num, walls, cols, rows, path) in enumerate(self.sol[s0:s0 + 6]):
                x0 = l + (j % 2) * cw; yt = H - 1.15 * inch - (j // 2) * chh
                c.setFont("Andika-Bold", 11); c.drawCentredString(x0 + cw / 2, yt - 10, f"Maze {num}")
                self.draw_maze(walls, cols, rows, x0 + 0.3 * inch, yt - chh + 0.1 * inch, cw - 0.6 * inch, chh - 0.4 * inch, 0.8, path)
            self.page()
        self.T["name"] = "Mazes for Kids"; self.T["hero"] = "mouse"
        c.setFont("Fredoka-Bold", 30)
        l, r = self.lr(); cx = (l + r) / 2
        c.setLineWidth(4); c.roundRect(l, 1.2 * inch, r - l, H - 2.4 * inch, 20)
        c.drawCentredString(cx, H - 2.5 * inch, "Maze Master Certificate")
        c.setFont("Andika", 14); c.drawCentredString(cx, H - 3.6 * inch, "This certificate is proudly presented to")
        c.line(cx - 2.5 * inch, H - 4.5 * inch, cx + 2.5 * inch, H - 4.5 * inch)
        c.drawCentredString(cx, H - 5.1 * inch, "for solving all 100 mazes!")
        lineart(c, "crown", cx - 1.1 * inch, 2.4 * inch, 2.2 * inch, pad=False)
        self.b.next(number=False)
        if self.b.page % 2 == 0: self.b.next(number=False)
        c.save()
        return self.b.page - 1


if __name__ == "__main__":
    m = MZ(); pages = m.build()
    sp, cw, ch = generic_cover(os.path.join(m.out, "cover.pdf"), pages, dict(
        title1="Mazes for Kids", title2="100 Fun Mazes", tagline="From Easy to Expert - 4 Levels!", ages="Ages 4-8",
        author=AUTHOR, hero="mouse", thumbs=["rocket", "bunny", "dog", "bee"], accent="o", accent2="w",
        badges=[("Easy", "g"), ("Medium", "b"), ("Hard", "p"), ("Expert", "r")], back_head="Find the Way!",
        blurb=["100 mazes that grow with your child - from simple paths", "to tricky expert puzzles. Every maze has a cute",
               "friend to help and a full solution at the back."],
        features=["100 original mazes in 4 levels of difficulty", "Big, clear paths for little hands at the start",
                  "Cute characters on every page", "Full solutions section and a Maze Master certificate",
                  "Builds focus, problem solving and pencil control"]))
    write_readme(os.path.join(m.out, "README.md"), dict(
        title="Mazes for Kids Ages 4-8", pages=pages, cw=cw, ch=ch, spine=sp, author=AUTHOR, price="$8.99", age="4-8",
        subtitle="100 Fun Mazes from Easy to Expert — Maze Activity Book for Kids with Solutions | Problem Solving Workbook",
        description=("**100 mazes that grow with your child!** Start with big, simple paths and work up to expert puzzles full of "
                     "twists and dead ends.\n\n**Inside:**\n- Level 1: Easy (25 mazes)\n- Level 2: Medium (25 mazes)\n- Level 3: Hard (25 mazes)\n"
                     "- Level 4: Expert (25 mazes)\n- Cute characters on every page\n- Full solutions and a Maze Master certificate\n\n"
                     "Great for travel, quiet time, classrooms and screen-free fun."),
        keywords=["mazes for kids ages 4-8", "maze book for kids", "activity book for kids ages 4-8", "maze puzzles for kids",
                  "kids puzzle book", "travel activity book for kids", "mazes for kids ages 6-8"],
        categories=["Children's Books > Activities, Crafts & Games > Activity Books", "Children's Books > Activities, Crafts & Games > Games > Puzzles"]))
    print(f"mazes: {pages} pages, spine {sp:.3f}")
