"""Generic Color-by-Code book engine (single-sided pictures, answer key, cover, listing).

python3 cbc_engine.py <book-id|all>
"""
import os, sys, random
from lib import *

AUTHOR = "Abdelrahman Maghraby"

DOLCH = {
    "pre": "a and away big blue can come down find for funny go help here I in is it jump little look make me my not one play red run said see the three to two up we where yellow you".split(),
    "primer": "all am are at ate be black brown but came did do eat four get good have he into like must new no now on our out please pretty ran ride saw say she so soon that there they this too under want was well went what white who will with yes".split(),
    "first": "after again an any as ask by could every fly from give going had has her him his how just know let live may of old once open over put round some stop take thank them then think walk were when".split(),
    "second": "always around because been before best both buy call cold does fast first five found gave goes green its made many off or pull read right sing sit sleep tell their these those upon us use very wash which why wish work would write your".split(),
    "third": "about better bring carry clean cut done draw drink eight fall far full got grow hold hot hurt if keep kind laugh light long much myself never only own pick seven shall show six small start ten today together try warm".split(),
}
COLOR_WORDS = {"red", "blue", "yellow", "green", "black", "brown", "white", "pink", "orange", "purple", "gray"}

SPANISH = {
    "colors": [("rojo", "red"), ("azul", "blue"), ("amarillo", "yellow"), ("verde", "green"), ("naranja", "orange"),
               ("morado", "purple"), ("rosa", "pink"), ("negro", "black"), ("blanco", "white"), ("gris", "gray"), ("marrón", "brown")],
    "numbers": [("uno", "1"), ("dos", "2"), ("tres", "3"), ("cuatro", "4"), ("cinco", "5"), ("seis", "6"), ("siete", "7"),
                ("ocho", "8"), ("nueve", "9"), ("diez", "10"), ("once", "11"), ("doce", "12"), ("trece", "13"), ("catorce", "14"),
                ("quince", "15"), ("veinte", "20")],
    "animals": [("perro", "dog"), ("gato", "cat"), ("pez", "fish"), ("pájaro", "bird"), ("vaca", "cow"), ("cerdo", "pig"),
                ("caballo", "horse"), ("oso", "bear"), ("león", "lion"), ("mono", "monkey"), ("rana", "frog"), ("pato", "duck"),
                ("conejo", "rabbit"), ("ratón", "mouse")],
    "food": [("manzana", "apple"), ("pan", "bread"), ("leche", "milk"), ("queso", "cheese"), ("huevo", "egg"), ("agua", "water"),
             ("plátano", "banana"), ("uva", "grape"), ("pastel", "cake"), ("helado", "ice cream"), ("sopa", "soup"), ("arroz", "rice")],
    "home": [("casa", "house"), ("mesa", "table"), ("silla", "chair"), ("cama", "bed"), ("libro", "book"), ("puerta", "door"),
             ("mamá", "mom"), ("papá", "dad"), ("sol", "sun"), ("luna", "moon"), ("flor", "flower"), ("árbol", "tree"),
             ("escuela", "school"), ("amigo", "friend")],
}


def codes(kind, colors, rng):
    n = len(colors); typ, _, arg = kind.partition(":")
    if typ == "num":
        top = max(int(arg), n); vals = rng.sample(range(1, top + 1), n); m = dict(zip(colors, vals))
        return [(str(m[c]), c) for c in colors], lambda c: str(m[c])
    if typ in ("add", "sub"):
        lo, hi = map(int, arg.split("-")); vals = rng.sample(range(lo, hi + 1), n); m = dict(zip(colors, vals))
        def f(c):
            a = m[c]
            if typ == "add":
                x = rng.randint(max(0, a - hi // 2 - 2) if hi > 10 else 0, min(a, hi // 2 + 2) if hi > 10 else a)
                return f"{x}+{a - x}"
            top = rng.randint(a, min(a + 10, hi + 10)); return f"{top}-{top - a}"
        return [(str(m[c]), c) for c in colors], f
    if typ == "dbl":
        vals = rng.sample(range(1, 11), n); m = dict(zip(colors, vals))
        return [(str(2 * m[c]), c) for c in colors], lambda c: f"{m[c]}+{m[c]}"
    if typ == "miss":
        vals = rng.sample(range(0, 11), n); m = dict(zip(colors, vals))
        def f(c):
            a = m[c]; x = rng.randint(0, 10); return f"{x}+?={x + a}"
        return [(f"? = {m[c]}", c) for c in colors], f
    if typ == "add2d":
        vals = rng.sample(range(20, 99), n); m = dict(zip(colors, vals))
        def f(c):
            s = m[c]; t1 = rng.randint(1, s // 10 - 1) if s >= 20 else 0; o1 = rng.randint(0, s % 10)
            return f"{t1 * 10 + o1}+{s - t1 * 10 - o1}"
        return [(str(m[c]), c) for c in colors], f
    if typ == "sub2d":
        vals = rng.sample(range(10, 80), n); m = dict(zip(colors, vals))
        def f(c):
            a = m[c]; t = rng.randint(1, (99 - a) // 10) if a < 90 else 0; o = rng.randint(0, 9 - a % 10)
            return f"{a + t * 10 + o}-{t * 10 + o}"
        return [(str(m[c]), c) for c in colors], f
    if typ == "mul":
        tabs = list(map(int, arg.split(","))); exprs = {}
        for t in tabs:
            for k in range(1, 11):
                exprs.setdefault(t * k, []).extend([f"{t}x{k}", f"{k}x{t}"])
        vals = rng.sample(sorted(exprs), n); m = dict(zip(colors, vals))
        return [(str(m[c]), c) for c in colors], lambda c: rng.choice(exprs[m[c]])
    if typ == "div":
        vals = rng.sample(range(1, 11), n); m = dict(zip(colors, vals))
        def f(c):
            d = rng.randint(2, 10); return f"{d * m[c]}÷{d}"
        return [(str(m[c]), c) for c in colors], f
    if kind == "es:colors":
        es = {"r": "rojo", "o": "naranja", "y": "amarillo", "g": "verde", "l": "verde claro", "b": "azul",
              "s": "azul claro", "p": "morado", "k": "rosa", "n": "marrón", "x": "negro", "a": "gris", "w": "blanco"}
        return [(es[c], c) for c in colors], lambda c: es[c]
    if typ == "es":
        pairs = rng.sample(SPANISH[arg], n); m = dict(zip(colors, pairs))
        return [(f"{m[c][0]} ({m[c][1]})", c) for c in colors], lambda c: m[c][0]
    if typ == "sw":
        bank = [w for lvl in arg.split(",") for w in DOLCH[lvl] if w.lower() not in COLOR_WORDS]
        ws = rng.sample(bank, n); m = dict(zip(colors, ws))
        return [(m[c], c) for c in colors], lambda c: m[c]
    raise ValueError(kind)


ALL_KEYS = [k for k in D if k not in ("bone", "footprint", "dinoegg")]

BOOKS = {
    "preschool-cbn": dict(
        title1="Preschool", title2="Color by Number", ages="Ages 3-5 | Pre-K & Kindergarten",
        full_title="Preschool Color by Number",
        subtitle="100 Mystery Pictures with Big Squares — Learn Numbers 1 to 10 & Colors | Coloring Activity Book for Kids Ages 3-5",
        tagline="100 Mystery Pictures with BIG Squares!", hero="owl", thumbs=["cat", "dino", "bunny", "car"],
        accent="o", accent2="y", badges=[("1-5", "r"), ("1-10", "b"), ("Colors", "g"), ("Fun!", "p")],
        sections=[("num:5", "Part 1: Numbers 1 to 5", "Find the number and color the square.", 50),
                  ("num:8", "Part 2: Numbers 1 to 8", "A few more numbers to find!", 25),
                  ("num:10", "Part 3: Numbers 1 to 10", "You are a number star!", 25)],
        maxcells=14, price="$9.99", age="3-5",
        instr="Find the number in each square. Color it with the matching color.",
        keywords=["color by number for kids ages 3-5", "preschool coloring book numbers", "toddler color by number",
                  "pre k activity book ages 4-5", "learn numbers 1-10 coloring", "kindergarten coloring workbook", "mystery pictures for preschoolers"],
        categories=["Children's Books > Activities, Crafts & Games > Coloring Books", "Children's Books > Early Learning > Counting"],
        blurb=["Big squares, simple numbers, and a surprise picture on every page!",
               "Little learners match numbers to colors and watch",
               "a cute animal, vehicle or treat appear."],
        features=["100 original mystery pictures with extra-big squares", "Numbers 1-5, then 1-8, then 1-10",
                  "Single-sided pages - no bleed-through", "Color test page, progress tracker and answer key",
                  "Builds number recognition, color names and fine motor skills"]),
    "multiplication-cbc": dict(
        title1="Multiplication", title2="Color by Number", ages="Ages 8-10 | Grades 3-4",
        full_title="Multiplication & Division Color by Number",
        subtitle="150 Mystery Pictures to Master Times Tables 1-10 and Division Facts | Math Coloring Workbook for Kids Ages 8-10, Grades 3-4",
        tagline="150 Mystery Pictures - Times Tables & Division!", hero="rocket", thumbs=["robot", "planet", "dragon", "guitar"],
        accent="p", accent2="y", badges=[("x2 x5 x10", "r"), ("x3 x4", "b"), ("x6-x9", "g"), ("÷", "o")],
        sections=[("mul:2,5,10", "Part 1: Times 2, 5 and 10", "The easiest tables first.", 25),
                  ("mul:3,4", "Part 2: Times 3 and 4", "Keep building your facts.", 25),
                  ("mul:6,7", "Part 3: Times 6 and 7", "Tricky tables - you can do it!", 25),
                  ("mul:8,9", "Part 4: Times 8 and 9", "The big ones!", 25),
                  ("mul:2,3,4,5,6,7,8,9,10", "Part 5: Mixed Multiplication", "All the tables together.", 25),
                  ("div:", "Part 6: Division Facts", "Divide, then color by the answer.", 25)],
        maxcells=16, price="$12.99", age="8-10",
        instr="Solve each problem. Color the square with the color of its answer.",
        keywords=["multiplication color by number", "times tables workbook for kids", "3rd grade math workbook",
                  "division practice coloring", "math coloring book ages 8-10", "multiplication facts practice", "4th grade math activity book"],
        categories=["Children's Books > Education & Reference > Math > Arithmetic", "Children's Books > Activities, Crafts & Games > Activity Books"],
        blurb=["Times tables have never been this much fun!",
               "Solve each fact, find its color, and reveal a secret picture.",
               "Perfect daily practice for grades 3 and 4."],
        features=["150 original mystery pictures", "Tables 2-10 in a smart order, then mixed practice",
                  "Division facts section", "Single-sided pages, answer key and progress tracker",
                  "Great for homework, homeschool and summer review"]),
    "spanish-cbc": dict(
        title1="Spanish", title2="Color by Code", ages="Ages 5-9 | Learn Spanish Words",
        full_title="Spanish Color by Code",
        subtitle="100 Mystery Pictures to Learn Spanish Colors, Numbers, Animals & First Words | Bilingual Coloring Activity Book for Kids Ages 5-9",
        tagline="100 Mystery Pictures - Learn Spanish While You Color!", hero="parrot", thumbs=["cat", "dog", "apple", "house"],
        accent="r", accent2="y", badges=[("Colores", "r"), ("Números", "b"), ("Animales", "g"), ("Palabras", "p")],
        sections=[("es:colors", "Part 1: Los Colores", "Colors in Spanish.", 20),
                  ("es:numbers", "Part 2: Los Números", "Numbers in Spanish.", 20),
                  ("es:animals", "Part 3: Los Animales", "Animals in Spanish.", 20),
                  ("es:food", "Part 4: La Comida", "Food in Spanish.", 20),
                  ("es:home", "Part 5: Mi Mundo", "Home, family and everyday words.", 20)],
        maxcells=16, price="$10.99", age="5-9",
        instr="Read the Spanish word in each square. Find it in the code and color the square.",
        keywords=["spanish workbook for kids", "learn spanish coloring book", "bilingual activity book kids",
                  "spanish for kids ages 5-9", "color by number spanish", "spanish vocabulary for children", "homeschool spanish workbook"],
        categories=["Children's Books > Education & Reference > Foreign Language Study > Spanish", "Children's Books > Activities, Crafts & Games > Coloring Books"],
        blurb=["Learn Spanish one mystery picture at a time!",
               "Read the Spanish word, find its color in the code,",
               "and discover the hidden picture. Every code shows the English meaning."],
        features=["100 original mystery pictures", "5 themes: colors, numbers, animals, food, everyday words",
                  "English meaning in every code key - no Spanish needed to start", "Single-sided pages, answer key and progress tracker",
                  "Great for bilingual families, classrooms and homeschool"]),
    "sight-words-cbc": dict(
        title1="Sight Words", title2="Color by Code", ages="Ages 4-8 | Pre-K to 3rd Grade",
        full_title="Sight Words Color by Code",
        subtitle="150 Mystery Pictures to Learn 200+ Dolch Sight Words — Pre-Primer, Primer, 1st, 2nd & 3rd Grade | Reading Coloring Workbook for Kids",
        tagline="150 Mystery Pictures - 200+ Sight Words!", hero="owl", thumbs=["book", "pencil", "backpack", "apple"],
        accent="g", accent2="y", badges=[("Pre-K", "r"), ("K", "b"), ("1st", "o"), ("2nd-3rd", "p")],
        sections=[("sw:pre", "Level 1: Pre-Primer Words", "The very first words readers learn.", 30),
                  ("sw:primer", "Level 2: Primer Words", "Kindergarten sight words.", 30),
                  ("sw:first", "Level 3: First Grade Words", "Growing reader words.", 30),
                  ("sw:second", "Level 4: Second Grade Words", "Strong reader words.", 30),
                  ("sw:third", "Level 5: Third Grade Words", "Super reader words!", 30)],
        maxcells=16, price="$12.99", age="4-8",
        instr="Read each word. Find it in the code and color the square.",
        keywords=["sight words workbook", "dolch sight words for kids", "color by sight word", "kindergarten reading workbook",
                  "first grade sight words", "learn to read activity book", "sight word coloring book"],
        categories=["Children's Books > Education & Reference > Language Arts > Reading Skills", "Children's Books > Activities, Crafts & Games > Coloring Books"],
        blurb=["Make sight word practice something kids ask for!",
               "Read each word, find its color, and reveal a mystery picture.",
               "Covers the Dolch lists from pre-primer to third grade."],
        features=["150 original mystery pictures", "5 levels following the Dolch sight word lists",
                  "200+ high-frequency words", "Single-sided pages, answer key and progress tracker",
                  "Perfect for reading practice at home and in class"]),
    "math-cbc": dict(
        title1="Math Facts", title2="Color by Number", ages="Ages 6-8 | Grades 1-2",
        full_title="Addition & Subtraction Color by Number",
        subtitle="150 Mystery Pictures for Math Fact Fluency — Within 10, Within 20, Doubles, Missing Numbers & 2-Digit Math | Grades 1-2 Workbook",
        tagline="150 Mystery Pictures - Addition & Subtraction!", hero="robot", thumbs=["truck", "fish", "ufo", "cupcake"],
        accent="b", accent2="y", badges=[("+", "r"), ("-", "g"), ("Doubles", "o"), ("2-Digit", "p")],
        sections=[("add:2-10", "Part 1: Addition Within 10", "Add, then color.", 25),
                  ("sub:0-9", "Part 2: Subtraction Within 10", "Take away, then color.", 25),
                  ("dbl:", "Part 3: Doubles", "Double the number!", 20),
                  ("miss:", "Part 4: Missing Numbers", "Find the number that makes it true.", 20),
                  ("add:11-20", "Part 5: Addition Within 20", "Bigger sums!", 20),
                  ("sub:2-15", "Part 6: Subtraction Within 20", "Bigger take-aways!", 20),
                  ("add2d:", "Part 7: Two-Digit Addition", "No regrouping needed.", 10),
                  ("sub2d:", "Part 8: Two-Digit Subtraction", "No regrouping needed.", 10)],
        maxcells=16, price="$12.99", age="6-8",
        instr="Solve each problem. Color the square with the color of its answer.",
        keywords=["addition and subtraction workbook", "math color by number grade 1", "first grade math workbook",
                  "2nd grade math practice", "math facts coloring book", "addition color by number", "math activity book ages 6-8"],
        categories=["Children's Books > Education & Reference > Math > Arithmetic", "Children's Books > Activities, Crafts & Games > Activity Books"],
        blurb=["Build fast, confident math facts - one secret picture at a time.",
               "Solve, color, and watch the mystery picture appear!",
               "Eight levels from sums within 10 to two-digit problems."],
        features=["150 original mystery pictures", "Within 10, within 20, doubles and missing numbers",
                  "Two-digit addition and subtraction without regrouping", "Single-sided pages, answer key and progress tracker",
                  "Ideal for grades 1-2, homeschool and summer review"]),
}


def build_book(bid):
    cfg = BOOKS[bid]
    out = os.path.join(OUTROOT, bid); os.makedirs(out, exist_ok=True)
    rng0 = random.Random(bid)
    pool = ALL_KEYS[:]; rng0.shuffle(pool)
    # prefer smaller designs for books with big cells
    if cfg["maxcells"] < 16:
        pool.sort(key=lambda k: max(len(grid_of(k)[0]), len(grid_of(k)[0][0])))
    pages, num, used = [], 0, 0
    for kind, title, sub, count in cfg["sections"]:
        for i in range(count):
            num += 1
            k = pool[used % len(pool)]; used += 1
            g, bg = grid_of(k)
            cols = [];  [cols.append(ch) for row in g for ch in row if ch not in cols]
            cols.remove(bg); cols.insert(0, bg)
            rng = random.Random(f"{bid}-{num}")
            key, fn = codes(kind, cols, rng)
            pages.append(dict(num=num, section=title, title=D[k][0], grid=g, texts=[[fn(ch) for ch in row] for row in g], key=key, design=k))
    if cfg["maxcells"] < 16:
        rng0.shuffle(pages)    # mix small/large designs after selection
        for i, p in enumerate(pages):
            p["num"] = i + 1
        secs = []
        idx = 0
        for kind, title, sub, count in cfg["sections"]:
            for p in pages[idx:idx + count]:
                p["section"] = title
            idx += count
        # codes must match section kind -> regenerate texts for reassigned sections
        idx = 0
        for kind, title, sub, count in cfg["sections"]:
            for p in pages[idx:idx + count]:
                g = p["grid"]; bg = g[0][0]
                cols = []; [cols.append(ch) for row in g for ch in row if ch not in cols]
                cols.remove(bg); cols.insert(0, bg)
                key, fn = codes(kind, cols, random.Random(f"{bid}-{p['num']}"))
                p["key"] = key; p["texts"] = [[fn(ch) for ch in row] for row in g]
            idx += count

    b = Book(os.path.join(out, "interior.pdf"))
    c = b.c
    # title page
    cx = b.center()
    c.setFont("Fredoka-Bold", 40); c.drawCentredString(cx, H - 2.4 * inch, cfg["title1"])
    c.setFont("Fredoka-Bold", 34); c.drawCentredString(cx, H - 3.0 * inch, cfg["title2"])
    c.setFont("Andika", 15); c.drawCentredString(cx, H - 3.6 * inch, cfg["tagline"])
    c.setFont("Andika-Bold", 14); c.drawCentredString(cx, H - 4.0 * inch, cfg["ages"])
    draw_grid(c, pages[0], cx - 1.6 * inch, cx + 1.6 * inch, H - 4.6 * inch, H - 8.0 * inch)
    c.setFont("Fredoka", 16); c.drawCentredString(cx, 1.4 * inch, AUTHOR)
    b.next(number=False)
    copyright_block(b, cfg["full_title"], AUTHOR)
    cbc.belongs_page(b); b.blank_back()
    # how to
    l, r = b.margins()
    c.setFont("Fredoka-Bold", 26); c.drawCentredString(b.center(), H - 1.2 * inch, "How to Use This Book")
    y = H - 1.9 * inch
    lines = ["1. Look at the code box at the top of the page.",
             "2. Color each little circle in the code box with its color first.",
             "3. Read or solve what is written in each square.",
             "4. Find the answer in the code and color the square with that color.",
             "5. Keep going until the mystery picture appears!", "",
             "This book has these parts:"] + [f"   {t} - {s}" for _, t, s, _ in cfg["sections"]] + [
             "", "Every picture is printed on its own page, so colors do not bleed through.",
             "Crayons and colored pencils work best. The answer key is at the back.",
             "Answer key colors: R Red, O Orange, Y Yellow, G Green, LG Light Green, B Blue,",
             "LB Light Blue, P Purple, Pk Pink, Br Brown, Bk Black, Gy Gray, W White."]
    for ln in lines:
        fs = fit_font(c, ln, "Andika", r - l - 30, 12.5); c.setFont("Andika", fs); c.drawString(l + 15, y, ln); y -= 19
    b.next()
    cbc.color_test_page(b)
    cbc.tracker_page(b, pages)
    for kind, title, sub, count in cfg["sections"]:
        ps = [p for p in pages if p["section"] == title]
        sample = list(dict.fromkeys(x for row in ps[0]["texts"] for x in row))[:5]
        cbc.divider(b, title, sub, sample)
        for p in ps:
            cbc.picture_page(b, p, cfg["instr"])
    cbc.answer_pages(b, pages)
    # certificate
    b.ensure_odd(); l, r = b.margins(); cx = b.center()
    c.setLineWidth(4); c.roundRect(l, 1.2 * inch, r - l, H - 2.4 * inch, 20)
    c.setFont("Fredoka-Bold", 34); c.drawCentredString(cx, H - 2.5 * inch, "Certificate")
    c.setFont("Fredoka", 20); c.drawCentredString(cx, H - 3.0 * inch, "of Super Coloring Achievement")
    c.setFont("Andika", 14); c.drawCentredString(cx, H - 4.0 * inch, "This certificate is proudly presented to")
    c.line(cx - 2.5 * inch, H - 4.9 * inch, cx + 2.5 * inch, H - 4.9 * inch)
    c.drawCentredString(cx, H - 5.6 * inch, f"for finishing all {len(pages)} mystery pictures in")
    c.drawCentredString(cx, H - 5.85 * inch, f"{cfg['full_title']}!")
    for i in range(5):
        draw_star(c, cx - 2 * inch + i * inch, H - 7.0 * inch, 20)
    c.setFont("Andika", 12)
    c.line(l + 0.6 * inch, 2.2 * inch, l + 3 * inch, 2.2 * inch); c.drawString(l + 0.6 * inch, 1.95 * inch, "Date")
    c.line(r - 3 * inch, 2.2 * inch, r - 0.6 * inch, 2.2 * inch); c.drawString(r - 3 * inch, 1.95 * inch, "Signed")
    b.next(number=False); b.blank_back()
    if b.page % 2 == 0:
        b.next(number=False)
    c.save()
    npages = b.page - 1
    hero_codes = None
    sp, cw, ch = generic_cover(os.path.join(out, "cover.pdf"), npages, dict(
        title1=cfg["title1"], title2=cfg["title2"], tagline=cfg["tagline"], ages=cfg["ages"], author=AUTHOR,
        hero=cfg["hero"], thumbs=cfg["thumbs"], accent=cfg["accent"], accent2=cfg["accent2"], badges=cfg["badges"],
        blurb=cfg["blurb"], features=cfg["features"], back_head="Solve. Color. Discover!",
        hero_coded={k: v for k, v in zip(set(ch for row in grid_of(cfg["hero"])[0] for ch in row),
                                          [t.split(" ")[0] for t, _ in pages[0]["key"]] * 3)}))
    desc = (f"**Every page hides a secret picture!** {cfg['blurb'][1]}\n\n**Inside:**\n"
            + "".join(f"- **{t}** — {s} ({n} pictures)\n" for _, t, s, n in cfg["sections"])
            + "".join(f"- {f}\n" for f in cfg["features"]))
    write_readme(os.path.join(out, "README.md"), dict(
        title=cfg["full_title"], subtitle=cfg["subtitle"], pages=npages, cw=cw, ch=ch, spine=sp, author=AUTHOR,
        price=cfg["price"], age=cfg["age"], description=desc, keywords=cfg["keywords"], categories=cfg["categories"]))
    print(f"{bid}: {len(pages)} pictures, {npages} pages, spine {sp:.3f}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for bid in (BOOKS if which == "all" else [which]):
        build_book(bid)
