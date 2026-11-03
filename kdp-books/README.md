# مكتبة كتب KDP — Abdelrahman Maghraby

كل كتاب في `output/<اسم-الكتاب>/` فيه: `interior.pdf` + `cover.pdf` + `README.md` (العنوان، العنوان الفرعي، الوصف، الكلمات المفتاحية، الأقسام، السعر).
الكتاب الأول (Color by Code Mega Book) موجود في `../kdp-color-by-code/`.

| # | الكتاب | السن | الصفحات | السعر المقترح | الفولدر |
|---|---|---|---|---|---|
| 1 | Color by Code Mega Book | 5-8 | 364 | $12.99 | `../kdp-color-by-code/output` |
| 2 | Dino Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/dino-big-preschool-workbook` |
| 3 | Vehicles Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/vehicles-big-preschool-workbook` |
| 4 | Ocean Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/ocean-big-preschool-workbook` |
| 5 | Space Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/space-big-preschool-workbook` |
| 6 | Unicorn Big Preschool Workbook | 3-5 | 274 | $14.99 | `output/unicorn-big-preschool-workbook` |
| 7 | Preschool Color by Number (100 صورة) | 3-5 | 242 | $9.99 | `output/preschool-cbn` |
| 8 | Multiplication & Division Color by Number | 8-10 | 360 | $12.99 | `output/multiplication-cbc` |
| 9 | Spanish Color by Code | 5-9 | 246 | $10.99 | `output/spanish-cbc` |
| 10 | Sight Words Color by Code (Dolch) | 4-8 | 358 | $12.99 | `output/sight-words-cbc` |
| 11 | Addition & Subtraction Color by Number | 6-8 | 364 | $12.99 | `output/math-cbc` |
| 12 | Mazes for Kids (100 مزّة) | 4-8 | 126 | $8.99 | `output/mazes-for-kids` |

## إعادة البناء
```bash
python3 workbook.py all      # الكتب 2-6
python3 cbc_engine.py all    # الكتب 7-11
python3 mazes.py             # الكتاب 12
```
ثيم جديد = إضافة سطر في `THEMES` (workbook.py) أو `BOOKS` (cbc_engine.py).

## ملاحظات مهمة
- KDP بيسمح بـ **3 كتب في اليوم** بس — ارفعهم على 4 أيام.
- اطلب **Proof copy** لكتاب واحد من كل نوع (Workbook / Color by Code / Mazes) قبل النشر.
- كتب Color by Code بتستخدم نفس مكتبة الـ 167 صورة بترتيب مختلف — فيه صور بتتكرر بين الكتب (مش جوه نفس الكتاب). اذكر ده في الاعتبار لو بتسوّقهم كـ Bundle.
- الـ 5 Workbooks نفس المحتوى التعليمي بثيمات مختلفة (رسومات الغلاف والصفحات والأيقونات) — ده شائع في KDP بس خلّي الوصف يوضّح الثيم.
- الإفصاح عن الـ AI: اختار Yes (الصور والنصوص اتعملت بمساعدة AI).
