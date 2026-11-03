"""Build KDP-Upload-Guide.html/.pdf (all 12 books) and a ZIP of all PDFs.

python3 make_guide.py <dist_dir>
"""
import os, re, sys, glob, html, zipfile
from pypdf import PdfReader

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
DIST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

ORDER = [
    ("01-Color-by-Code-Mega-Book", os.path.join(REPO, "kdp-color-by-code", "output")),
    ("02-Dino-Big-Preschool-Workbook", "dino-big-preschool-workbook"),
    ("03-Vehicles-Big-Preschool-Workbook", "vehicles-big-preschool-workbook"),
    ("04-Ocean-Big-Preschool-Workbook", "ocean-big-preschool-workbook"),
    ("05-Space-Big-Preschool-Workbook", "space-big-preschool-workbook"),
    ("06-Unicorn-Big-Preschool-Workbook", "unicorn-big-preschool-workbook"),
    ("07-Preschool-Color-by-Number", "preschool-cbn"),
    ("08-Multiplication-Division-Color-by-Number", "multiplication-cbc"),
    ("09-Spanish-Color-by-Code", "spanish-cbc"),
    ("10-Sight-Words-Color-by-Code", "sight-words-cbc"),
    ("11-Addition-Subtraction-Color-by-Number", "math-cbc"),
    ("12-Mazes-for-Kids", "mazes-for-kids"),
]
UPLOAD_DAY = {1: 1, 2: 1, 8: 1, 7: 2, 10: 2, 12: 2, 3: 3, 9: 3, 11: 3, 4: 4, 5: 4, 6: 4}

BOOK1 = dict(
    title="Color by Code Mega Book",
    subtitle="150 Mystery Pictures — Letters, Sight Words, Phonics, Addition & Subtraction | Coloring Activity Workbook for Kids Ages 5-8, Kindergarten to 2nd Grade",
    price="$12.99", age="5-8",
    description=("**Every page hides a secret picture!** Kids read the letter, word, or math problem in each square, find its color in the code, "
                 "and watch a mystery picture appear — a puppy, a rocket, a unicorn, a pumpkin and 146 more!\n\n**7 levels that grow with your child:**\n"
                 "- **Letter Match** — uppercase and lowercase letters\n- **Sight Words Level 1** — pre-primer and primer words\n"
                 "- **Sight Words Level 2** — first and second grade words\n- **Phonics** — short vowel sounds and beginning sounds (sh, ch, th)\n"
                 "- **Addition** — within 10, then within 20\n- **Subtraction** — within 10, then within 20\n"
                 "- **Holiday Review** — Halloween, Christmas, Easter, Thanksgiving & more\n\n**Inside you'll find:**\n"
                 "- 150 original pixel-art mystery pictures\n- Large 8.5 x 11 pages, printed single-sided to prevent bleed-through\n"
                 "- A code key on every page with circles kids pre-color themselves\n"
                 "- A color test page, a progress tracker, a full answer key and a certificate of completion\n\n"
                 "Perfect for kindergarten, first and second grade, homeschool, classroom centers, quiet time, and travel."),
    keywords=["color by number for kids ages 5-8", "color by sight words kindergarten", "first grade math workbook addition subtraction",
              "phonics workbook kindergarten activity book", "mystery pictures coloring book for kids", "homeschool workbook 1st 2nd grade",
              "kindergarten workbook ages 5-6 learning"],
    categories=["Children's Books > Activities, Crafts & Games > Activity Books",
                "Children's Books > Education & Reference > Math > Arithmetic",
                "Children's Books > Education & Reference > Language Arts > Reading Skills"],
)


def parse_readme(path):
    s = open(path, encoding="utf-8").read()
    g = lambda pat: re.search(pat, s, re.S).group(1).strip()
    return dict(title=g(r"\*\*Title:\*\* (.*?)\n"), subtitle=g(r"\*\*Subtitle:\*\* (.*?)\n"),
                price=g(r"\*\*Suggested price:\*\* (.*?)\n"), age=g(r"\*\*Reading age:\*\* (.*?)\n"),
                description=g(r"\*\*Description:\*\*\n\n(.*?)\n\n\*\*Keywords:\*\*"),
                keywords=re.findall(r"^\d+\. (.*)$", g(r"\*\*Keywords:\*\*\n(.*?)\n\n"), re.M),
                categories=re.findall(r"^- (.*)$", g(r"\*\*Categories:\*\*\n(.*?)\n\n"), re.M))


def md_to_kdp_html(md):
    """Markdown subset -> HTML that KDP's description box accepts (<b>, <ul>, <li>, <p>, <br>)."""
    out, in_list = [], False
    for ln in md.split("\n"):
        ln = html.escape(ln.strip(), quote=False)
        ln = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ln)
        if ln.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"<li>{ln[2:]}</li>")
        else:
            if in_list: out.append("</ul>"); in_list = False
            if ln: out.append(f"<p>{ln}</p>")
    if in_list: out.append("</ul>")
    return "".join(out)


books = []
for i, (name, src) in enumerate(ORDER, 1):
    d = src if os.path.isabs(src) else os.path.join(ROOT, "output", src)
    info = BOOK1.copy() if i == 1 else parse_readme(os.path.join(d, "README.md"))
    info["pages"] = len(PdfReader(os.path.join(d, "interior.pdf")).pages)
    mb = PdfReader(os.path.join(d, "cover.pdf")).pages[0].mediabox
    info["cover"] = f'{float(mb.width) / 72:.3f} x {float(mb.height) / 72:.3f} in'
    info["spine"] = info["pages"] * 0.002252
    info["cost"] = 1 + info["pages"] * 0.012
    p = float(info["price"].strip("$"))
    rate = 0.6 if p >= 9.99 else 0.5
    info["royalty"] = p * rate - info["cost"]; info["rate"] = int(rate * 100)
    info["n"] = i; info["folder"] = name; info["dir"] = d
    books.append(info)

# ---------------------------------------------------------------- ZIP of all PDFs
zpath = os.path.join(DIST, "KDP-Books-All-12.zip")
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for b in books:
        z.write(os.path.join(b["dir"], "interior.pdf"), f"KDP-Books/{b['folder']}/interior.pdf")
        z.write(os.path.join(b["dir"], "cover.pdf"), f"KDP-Books/{b['folder']}/cover.pdf")

# ---------------------------------------------------------------- HTML guide
E = lambda s: html.escape(str(s))
font = lambda f: "file://" + os.path.join(REPO, "kdp-color-by-code", "fonts", f)
css = f"""
@font-face {{ font-family: Andika; src: url('{font("Andika-Regular.ttf")}'); }}
@font-face {{ font-family: Andika; font-weight: 700; src: url('{font("Andika-Bold.ttf")}'); }}
@font-face {{ font-family: Fredoka; font-weight: 700; src: url('{font("Fredoka-Bold.ttf")}'); }}
@page {{ size: Letter; margin: 0.6in 0.6in 0.7in; }}
body {{ font-family: Andika, sans-serif; color: #1d1d24; font-size: 10.5pt; line-height: 1.45; }}
h1, h2, h3 {{ font-family: Fredoka, sans-serif; color: #1f3d8a; margin: 0.2em 0 0.4em; }}
h1 {{ font-size: 28pt; }} h2 {{ font-size: 18pt; border-bottom: 3px solid #f6c23e; padding-bottom: 4px; margin-top: 0.8em; }}
h3 {{ font-size: 12.5pt; color: #333; margin-top: 1em; }}
table {{ border-collapse: collapse; width: 100%; margin: 6px 0 10px; }}
td, th {{ border: 1px solid #c9ccd6; padding: 4px 7px; vertical-align: top; text-align: left; }}
th {{ background: #eef1fa; }}
.copy {{ background: #f6f7fb; border: 1px solid #d6d9e4; border-radius: 6px; padding: 7px 9px; font-size: 9.5pt;
        white-space: pre-wrap; word-break: break-word; font-family: 'DejaVu Sans Mono', monospace; }}
.book {{ page-break-before: always; }}
.tag {{ display: inline-block; background: #1f3d8a; color: #fff; border-radius: 10px; padding: 1px 9px; font-size: 9pt; margin-right: 4px; }}
.warn {{ background: #fff6e0; border-left: 4px solid #f0a500; padding: 6px 10px; margin: 8px 0; }}
ol li, ul li {{ margin-bottom: 3px; }}
.cover {{ text-align: center; padding-top: 2.2in; }}
.small {{ font-size: 9pt; color: #555; }}
"""
H = [f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>KDP Upload Guide</title><style>{css}</style></head><body>"]
H.append(f"""<div class='cover'><h1>Amazon KDP Upload Guide</h1>
<p style='font-size:15pt'>12 Children's Activity Books — Step-by-Step Instructions &amp; Listing Content</p>
<p style='font-size:13pt'><b>Author / Publisher:</b> Abdelrahman Maghraby</p>
<p class='small'>Files: <b>KDP-Books-All-12.zip</b> — one folder per book, each with <code>interior.pdf</code> and <code>cover.pdf</code>.</p></div>""")

# catalog
H.append("<h2 class='book'>1. The Catalog</h2><table><tr><th>#</th><th>Book</th><th>Ages</th><th>Pages</th><th>Price</th><th>Print cost*</th><th>Royalty*</th><th>Upload day</th></tr>")
for b in books:
    H.append(f"<tr><td>{b['n']}</td><td>{E(b['title'])}</td><td>{E(b['age'])}</td><td>{b['pages']}</td><td>{E(b['price'])}</td>"
             f"<td>${b['cost']:.2f}</td><td>${b['royalty']:.2f} ({b['rate']}%)</td><td>Day {UPLOAD_DAY[b['n']]}</td></tr>")
H.append("</table><p class='small'>* Estimates for Amazon.com using KDP's published example formula (fixed $1.00 + $0.012 per page, black &amp; white). "
         "Royalty assumes 60% for list prices of $9.99 and up and 50% below $9.99. Always confirm the exact numbers on the KDP Pricing page.</p>")
H.append("""<div class='warn'><b>KDP limits new titles to 3 per day.</b> Follow the upload-day column: Day 1 = books 1, 2, 8 · Day 2 = 7, 10, 12 ·
Day 3 = 3, 9, 11 · Day 4 = 4, 5, 6. Similar themed workbooks are spread across days on purpose.</div>""")

# step by step
H.append("""<h2>2. One-Time Account Setup</h2><ol>
<li>Go to <b>kdp.amazon.com</b> and sign in (or create an account).</li>
<li>Open <b>Your Account</b> and complete: author/publisher name, address, <b>bank account</b> for payments, and the <b>tax interview</b> (non-US residents fill the W-8BEN form inside KDP).</li>
<li>Wait until the account shows as complete — you cannot publish before the tax and payment info is done.</li></ol>

<h2>3. How to Upload Each Book (repeat for all 12)</h2>
<h3>Step 1 — Create the paperback</h3><ol>
<li>Go to <b>Bookshelf</b> → <b>+ Create</b> → <b>Paperback</b> → <b>Create paperback</b>.</li></ol>
<h3>Step 2 — Paperback Details (tab 1)</h3><ol>
<li><b>Language:</b> English.</li>
<li><b>Book Title</b> and <b>Subtitle:</b> copy from the book's page in this guide.</li>
<li><b>Series:</b> optional. Books 2-6 can share a series named <i>Big Preschool Workbook</i>; books 1, 7-11 can share <i>Color by Code Learning</i>.</li>
<li><b>Edition Number:</b> leave empty.</li>
<li><b>Author:</b> First name <i>Abdelrahman</i>, Last name <i>Maghraby</i>.</li>
<li><b>Description:</b> click <i>Insert HTML</i> (or paste into the box) and copy the "Description (HTML)" block. KDP supports the &lt;b&gt;, &lt;p&gt;, &lt;ul&gt; and &lt;li&gt; tags used here.</li>
<li><b>Publishing Rights:</b> "I own the copyright and I hold the necessary publishing rights."</li>
<li><b>Primary Audience:</b> Sexually explicit content = <b>No</b>. Reading age: set the min/max from the book's page.</li>
<li><b>Primary marketplace:</b> Amazon.com.</li>
<li><b>Categories:</b> click <i>Choose categories</i> and pick the 3 categories listed for the book.</li>
<li><b>Keywords:</b> paste the 7 keywords, one per box.</li>
<li><b>Publication date:</b> leave empty. Release: <i>I'm ready to release my book now</i>.</li>
<li>Click <b>Save and Continue</b>.</li></ol>
<h3>Step 3 — Paperback Content (tab 2)</h3><ol>
<li><b>ISBN:</b> "Get a free KDP ISBN" → Assign. (The imprint will show as "Independently published".)</li>
<li><b>Print Options:</b> Ink and paper = <b>Black &amp; white interior with white paper</b>; Trim size = <b>8.5 x 11 in</b>;
Bleed settings = <b>No Bleed</b>; Paperback cover finish = <b>Glossy</b>.</li>
<li><b>Manuscript:</b> Upload <code>interior.pdf</code> from the book's folder.</li>
<li><b>Book Cover:</b> choose "Upload a cover you already have (print-ready PDF only)" → upload <code>cover.pdf</code>.
The cover already includes 0.125 in bleed, the correct spine width, and an empty area on the back for the barcode that KDP adds automatically.</li>
<li><b>AI-Generated Content:</b> select <b>Yes</b>. For <i>Texts</i> and <i>Images</i> choose that AI was used and enter the tool name (for example "Claude by Anthropic"); Translations = None.</li>
<li>Click <b>Launch Previewer</b>. Check every warning, flip through the pages, then click <b>Approve</b>.</li>
<li>Review the <b>Summary</b> (page count and printing cost should match this guide) → <b>Save and Continue</b>.</li></ol>
<h3>Step 4 — Rights &amp; Pricing (tab 3)</h3><ol>
<li><b>Territories:</b> All territories (worldwide rights).</li>
<li><b>Primary marketplace:</b> Amazon.com. Enter the list price from this guide; KDP fills other marketplaces automatically (you can round them).</li>
<li><b>Expanded Distribution:</b> optional — leave it off at first (lower royalty, higher minimum price).</li>
<li>Click <b>Request printed proofs</b> for at least one book of each type (workbook, color by code, mazes) and check the printed copy.</li>
<li>Click <b>Publish Your Paperback Book</b>. Review usually takes up to 72 hours.</li></ol>

<h2>4. Quality Checklist Before Publishing</h2><ul>
<li>Previewer shows no errors (margins, fonts, low-resolution images).</li>
<li>Page count in the KDP summary matches this guide (the cover spine depends on it — if the page count changes, the cover must be rebuilt).</li>
<li>Title, subtitle and author are spelled exactly the same on the cover and in the listing.</li>
<li>The printed proof looks right: lines are dark enough, text is readable, coloring pages are single-sided.</li></ul>

<h2>5. After Publishing</h2><ul>
<li><b>Author Central</b> (author.amazon.com): claim your books and add an author bio.</li>
<li><b>A+ Content</b> (KDP → Marketing): add images of sample pages — it raises conversion.</li>
<li><b>Amazon Ads:</b> start one Sponsored Products campaign per book with automatic targeting and a small daily budget (e.g. $3-5), then move winning keywords to manual campaigns.</li>
<li><b>Seasonality:</b> push the Holiday sections and Christmas gift angle in Oct-Dec; push workbooks before back-to-school (Jul-Aug).</li>
<li>Never offer free products or payment in exchange for reviews — this breaks Amazon's rules.</li></ul>
<div class='warn'><b>Content notes.</b> The six color-by-code books (1, 7-11) draw from the same library of original pixel-art pictures in different orders,
so a few pictures repeat between books (never inside the same book). The five Big Preschool Workbooks (2-6) share the same learning structure with
different themes and artwork. Make each listing clearly state its theme.</div>""")

for b in books:
    lo, _, hi = b["age"].partition("-"); hi = re.match(r"\d+", hi.strip()).group(0) if hi else lo
    H.append(f"<div class='book'><h2>Book {b['n']}: {E(b['title'])}</h2>")
    H.append(f"<p><span class='tag'>Folder: {E(b['folder'])}</span><span class='tag'>Upload day {UPLOAD_DAY[b['n']]}</span></p>")
    H.append("<table>"
             f"<tr><th>Interior</th><td>interior.pdf — {b['pages']} pages · 8.5 x 11 in · B&amp;W · white paper · No Bleed</td></tr>"
             f"<tr><th>Cover</th><td>cover.pdf — {b['cover']} · spine {b['spine']:.3f} in · Glossy</td></tr>"
             f"<tr><th>List price</th><td>{E(b['price'])} (est. print cost ${b['cost']:.2f}, est. royalty ${b['royalty']:.2f})</td></tr>"
             f"<tr><th>Reading age</th><td>Min {lo.strip()} · Max {hi}</td></tr></table>")
    H.append(f"<h3>Title</h3><div class='copy'>{E(b['title'])}</div>")
    H.append(f"<h3>Subtitle</h3><div class='copy'>{E(b['subtitle'])}</div>")
    H.append("<h3>Author</h3><div class='copy'>Abdelrahman Maghraby</div>")
    H.append(f"<h3>Description (HTML — paste into KDP)</h3><div class='copy'>{E(md_to_kdp_html(b['description']))}</div>")
    H.append("<h3>Keywords (one per box)</h3><table>" + "".join(f"<tr><td style='width:22px'>{i}</td><td>{E(k)}</td></tr>" for i, k in enumerate(b["keywords"], 1)) + "</table>")
    H.append("<h3>Categories</h3><ul>" + "".join(f"<li>{E(c)}</li>" for c in b["categories"]) + "</ul></div>")
H.append("</body></html>")

hpath = os.path.join(DIST, "KDP-Upload-Guide.html")
open(hpath, "w", encoding="utf-8").write("".join(H))

import subprocess
subprocess.run(["/opt/pw-browsers/chromium", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                "--allow-file-access-from-files", f"--print-to-pdf={os.path.join(DIST, 'KDP-Upload-Guide.pdf')}",
                "file://" + hpath], check=True, capture_output=True)

with zipfile.ZipFile(zpath, "a") as z:
    z.write(os.path.join(DIST, "KDP-Upload-Guide.pdf"), "KDP-Books/KDP-Upload-Guide.pdf")
print(zpath, os.path.getsize(zpath) // 1024, "KB")
