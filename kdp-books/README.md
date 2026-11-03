# KDP Book Library — Abdelrahman Maghraby

Each book lives in `output/<book>/` with `interior.pdf`, `cover.pdf` and a `README.md` (title, subtitle, description, keywords, categories, price).
Book 1 (Color by Code Mega Book) lives in `../kdp-color-by-code/`.

**Full step-by-step upload instructions and copy-paste listing content for all 12 books:** run `python3 make_guide.py <folder>` —
it creates `KDP-Upload-Guide.pdf` and `KDP-Books-All-12.zip` (all PDFs + the guide).

| # | Book | Ages | Pages | Suggested price | Folder |
|---|---|---|---|---|---|
| 1 | Color by Code Mega Book | 5-8 | 364 | $12.99 | `../kdp-color-by-code/output` |
| 2 | Dino Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/dino-big-preschool-workbook` |
| 3 | Vehicles Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/vehicles-big-preschool-workbook` |
| 4 | Ocean Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/ocean-big-preschool-workbook` |
| 5 | Space Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/space-big-preschool-workbook` |
| 6 | Unicorn Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/unicorn-big-preschool-workbook` |
| 7 | Preschool Color by Number (100 pictures) | 3-5 | 242 | $9.99 | `output/preschool-cbn` |
| 8 | Multiplication & Division Color by Number | 8-10 | 360 | $12.99 | `output/multiplication-cbc` |
| 9 | Spanish Color by Code | 5-9 | 246 | $10.99 | `output/spanish-cbc` |
| 10 | Sight Words Color by Code (Dolch) | 4-8 | 358 | $12.99 | `output/sight-words-cbc` |
| 11 | Addition & Subtraction Color by Number | 6-8 | 364 | $12.99 | `output/math-cbc` |
| 12 | Mazes for Kids (100 mazes) | 4-8 | 126 | $8.99 | `output/mazes-for-kids` |

## Rebuilding
```bash
python3 workbook.py all      # books 2-6
python3 cbc_engine.py all    # books 7-11
python3 mazes.py             # book 12
python3 make_guide.py dist   # guide PDF + ZIP of everything
```
A new theme = one new entry in `THEMES` (workbook.py) or `BOOKS` (cbc_engine.py).

## Important notes
- KDP allows only **3 new titles per day** — upload over 4 days (schedule in the guide).
- Order a **printed proof** of at least one book of each type before publishing.
- The color-by-code books share one library of original pictures in different orders, so some pictures repeat between books (never inside one book).
- The five workbooks share the same learning structure with different themes and artwork.
- AI disclosure: answer **Yes** in KDP (text and images were made with AI assistance).
