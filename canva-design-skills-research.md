# ريسرش: السكيلز والأدوات اللي بتخلي Claude يطلع تصميمات متناسقة على Canva

> النطاق: سوشيال ميديا · برزنتيشن · كومباني بروفايل · CV · برشورز
> تاريخ الريسرش: نوفمبر 2026
> المصادر: أدوات Canva Connector المتوصّلة بحسابك (اتقرت مواصفاتها مباشرة)، مركز مساعدة Canva الرسمي (عن طريق أداة `help`)، وقائمة السكيلز المفعّلة على حسابك في claude.ai.

---

## الخلاصة في سطور

1. **مفيش سكيل جاهز اسمه "Canva Design"** على حسابك ولا في الكتالوج (البحث رجّع صفر نتايج). اللي موجود هو **Canva Connector** (حوالي 35 أداة) + سكيلز مساعدة.
2. التناسق مش بييجي من أداة واحدة؛ بييجي من **3 طبقات**:
   - **Brand Kit** في Canva (ألوان + خطوط + لوجو) ← عندك 5 Brand Kits جاهزين.
   - **Brand Templates** (قوالب ثابتة فيها حقول Autofill) ← تضمن إن كل تصميم يطلع بنفس الهيكل.
   - **قواعد تصميم مكتوبة** يمشي عليها Claude في كل طلب ← دي اللي كانت ناقصة، وعملتهالك كسكيل في `skills/canva-design-system/SKILL.md`.
3. **أهم ملاحظة تقنية:** أداة `create-design` (الجديدة) **مابتطبقش الـ Brand Kit**. لو عاوز تصميم بهويتك لازم يستخدم `generate-design` مع `brand_kit_id`، أو يبدأ من Brand Template.

---

## 1) السكيلز الموجودة فعلًا على حسابك

| السكيل | حالته | يفيد في التصميم إزاي |
|---|---|---|
| **skill-creator** | مفعّل | الأهم: بيه تبني سكيل التصميم بتاعك وتختبره وتحسّنه (اللي عملته مسودته هنا). |
| **pptx** | مفعّل | برزنتيشن PowerPoint من الصفر أو تعديل ملف؛ بديل/مكمّل لما تحتاج ملف .pptx مش Canva. |
| **docx** | مفعّل | CV أو كومباني بروفايل بصيغة Word (ATS-friendly للـ CV). |
| **pdf** | مفعّل | دمج/تقسيم/علامة مائية على PDF البروفايل أو البرشور بعد التصدير. |
| **docs** | مفعّل | مستند Claude Docs قابل للتعليق — مفيد لكتابة محتوى البروفايل/الـ CV قبل التصميم. |
| **egyptian-content-agent** | مفعّل | كتابة كابشنز ومحتوى بوستات السوشيال باللهجة المصرية. |
| **deep-research** | مفعّل | ريسرش منافسين وترندات قبل التصميم. |
| **dataviz** | مدمج | قواعد الرسوم البيانية (ألوان، محاور) للبروفايل والبرزنتيشن. |
| **artifact-design** | مدمج | قواعد تصميم صفحات HTML — نفس مبادئ الهيراركي والمسافات. |
| **Adobe for creativity** (plugin) | **فشل الاتصال** (Proxy 403) | فيه `create_visual_design_express_skill` و`font_recommend` و`suggest_type_palettes` — ممتاز لاختيار الخطوط. محتاج تعيد توصيله من إعدادات الـ Connectors. |
| **3dicons / IconScout** | Connector متوصّل | أيقونات و3D وIllustrations، وبيلوّنها بألوان البراند (Brand Palette). |

---

## 2) أدوات Canva Connector — مقسّمة حسب الوظيفة

### أ) الإنشاء (Create)
| الأداة | بتعمل إيه | متى تستخدمها |
|---|---|---|
| `create-design` | تصميم جديد من Brief + Outline للبرزنتيشن | أي تصميم **من غير** هوية براند. يدعم `format` (مثل "Instagram Post"). |
| `generate-design` | يولّد عدة **Candidates** وتختار منهم | **لما تحتاج Brand Kit** (`brand_kit_id`) أو صور معينة (`asset_ids`). أنواعه: instagram_post, your_story, facebook_post, twitter_post, pinterest_pin, presentation(لا)، resume, flyer, poster, proposal, report, infographic, document, doc, business_card… |
| `create-design-from-candidate` | يحوّل الـ Candidate لتصميم قابل للتعديل | بعد `generate-design` دايمًا. |
| `request-outline-review` → `generate-design-structured` | برزنتيشن بالبراند بعد مراجعة الـ Outline | البرزنتيشن بهوية البراند. لازم موافقة على الـ Outline الأول. يدعم `source_document` (يبني من تصميم/تمبليت موجود). |
| `create-design-from-brand-template` | نسخة جديدة من Brand Template | أقوى ضمان للتناسق. |
| `autofill-design` | يملا حقول التمبليت بنصوص/صور/Charts | CV لعدة أشخاص، بوستات سلسلة، كروت. |
| `import-design-from-url` | يحوّل PDF/PPTX/DOCX/HTML عام لتصميم Canva | لو عندك بروفايل قديم على رابط عام. |
| `generate-image` | صورة/Illustration/أيقونة بالذكاء الاصطناعي | صور الخلفيات والـ Hero. |

### ب) التعديل والضبط (Edit) — هنا بيتعمل التناسق الدقيق
`read-design` (افتح Transaction) → `edit-design` (عمليات) → معاينة وموافقتك → `commit`.

العمليات المتاحة داخل `edit-design`:
- **نصوص:** `replace_text`, `find_and_replace_text`, `add_text`, `format_text` (لون HEX، حجم 1–800px، Bold/Normal، Italic، `line_height` من 0.5 لـ 2.5، محاذاة start/center/end، قوائم).
- **تخطيط:** `position_element`, `resize_element`, `rotate_element`, `layer_element`, `group_elements`, `update_text_anchoring`.
- **ألوان وأشكال:** `recolor_element`, `insert_shape` (SVG path بزوايا مستديرة), `update_stroke_properties`, `update_opacity`, `add_page` بلون خلفية.
- **صور:** `update_fill`, `insert_fill`, `crop_media`, `flip_media` (+ `alt_text` إجباري).
- **برزنتيشن:** `reorder_page`, `replace_speaker_notes`.
- **Autofill:** `update_autofill_field` لتحويل أي تصميم لتمبليت بحقول.

> ⚠️ قيود لازم Claude يعرفها: `format_text` مابيغيّرش **نوع الخط (Font family)** — الخط بييجي من الـ Brand Kit أو التمبليت. الوزن Bold/Normal بس. الصفحات Responsive (Docs) بتقبل عمليات محدودة.

### ج) الهوية والتنظيم
| الأداة | الاستخدام |
|---|---|
| `list-brand-kits` | يجيب الـ Brand Kits (عندك: `abdelrahman maghraby`, `IB Creative studio`, `qsandreg`, `DR Asmahan`, `saudi national day`). |
| `search-brand-templates` / `get-brand-template-dataset` | تلاقي التمبليت وتشوف حقوله. |
| `create-brand-template-draft` → `publish-brand-template` | تحوّل تصميم ناجح لتمبليت براند للفريق. |
| `create-folder`, `move-item-to-folder`, `search-folders`, `list-folder-items` | فولدر لكل عميل/مشروع. |
| `copy-design`, `merge-designs` | نسخ احتياطية، ودمج صفحات (مثلًا غلاف + محتوى البروفايل). |

### د) المقاسات والتصدير
| الأداة | الاستخدام |
|---|---|
| `resize-design` | نفس التصميم لكل المنصات (مقاس مخصص بالبكسل). |
| `get-export-formats` → `export-design` | PDF (A4/A3/Letter، جودة pro)، PNG شفاف، JPG، PPTX، MP4، GIF. |
| `remove-background`, `separate-image-layers` | تفريغ صور، وتحويل صورة مسطحة لتصميم قابل للتعديل. |
| `help` | أسئلة Canva الرسمية (طباعة، RTL…). |

---

## 3) معايير التصميم العامة (اللي لازم يلتزم بيها Claude في كل طلب)

### الألوان
- قاعدة **60-30-10**: 60% لون أساسي/محايد، 30% ثانوي، 10% Accent للـ CTA بس.
- **أقصى 3 ألوان + محايدين** (أبيض/رمادي/أسود). كلها من الـ Brand Kit بأكواد HEX ثابتة.
- **التباين**: نص عادي ≥ 4.5:1، نص كبير (≥ 24px أو 19px Bold) ≥ 3:1.

### الخطوط (Typography)
- **خطين بحد أقصى**: واحد للعناوين وواحد للنص. للعربي: Cairo / Tajawal / IBM Plex Sans Arabic / Almarai / Noto Kufi Arabic.
- **سلّم أحجام ثابت (Type Scale بنسبة 1.25–1.333)**، مثال للسوشيال 1080px: عنوان 72–96 · فرعي 40–48 · نص 28–32 · ملاحظات 22–24.
- **Line height**: نص 1.4–1.6، عناوين 1.1–1.25. (العربي محتاج 1.5–1.7).
- طول السطر 45–75 حرف.

### التخطيط (Layout)
- **Grid**: 12 عمود للبرزنتيشن/البروفايل، 4–6 للسوشيال. **وحدة مسافات 8px** (8/16/24/32/48/64).
- **هوامش**: سوشيال ≥ 60–80px، برزنتيشن ≥ 80–100px، مطبوعات ≥ 10–15mm من القص.
- **هيراركي**: عنصر واحد بطل في الصفحة. القراءة Z أو F (وفي العربي معكوسة من اليمين).
- **محاذاة** موحّدة؛ كل عنصر لازم يكون محاذي لعنصر تاني.
- **مساحة بيضاء** 30–40% على الأقل.

### العربي (RTL)
- محاذاة يمين (`text_align: end` في السياقات العربية)، اللوجو والعناوين يبدأوا من اليمين، الأسهم والـ Timelines معكوسة.
- Canva فيها **Translate → Mirror page to match text direction** لعكس الصفحة، واختيار الخط من "Fonts in your language" لتجنب المربعات الفاضية.
- الأرقام: اختار نظام واحد (عربي ١٢٣ أو لاتيني 123) ومتغيّرش جوه التصميم.

### الصور والأيقونات
- ستايل أيقونات واحد (Line أو Filled، نفس السُمك). من IconScout بـ Brand Palette.
- كل الصور نفس المعالجة (فلتر/حرارة لون/Overlay واحد).
- دقة الطباعة 300 DPI.

---

## 4) معايير كل نوع تصميم

### 4.1 السوشيال ميديا
| المنصة | المقاس | ملاحظات |
|---|---|---|
| Instagram Feed | **1080×1350** (4:5) — الأفضل؛ أو 1080×1080 | `generate-design` بيطلّعه 1080×1350 تلقائي. |
| Story / Reels / TikTok | 1080×1920 | سيب ~250px فوق و~350px تحت فاضيين (واجهة التطبيق). |
| Carousel | 1080×1350 × (5–10 شرايح) | نفس الـ Grid، رقم الشريحة، الشريحة الأخيرة CTA. |
| Facebook Post | 1080×1350 أو 1200×630 للينك | |
| LinkedIn Post | 1080×1350 أو 1200×1200 · Banner 1584×396 | |
| X / Twitter | 1600×900 | |
| YouTube Thumbnail | 1280×720 | نص ≤ 4–5 كلمات، وجه + تباين عالي. |

قواعد: رسالة واحدة لكل بوست · نص على التصميم ≤ 20% من المساحة تقريبًا · اللوجو في نفس الركن دايمًا · سلسلة البوستات تعيش على 2–3 Layouts ثابتة (Quote / Tip / Promo) — أحسن طريقة: Brand Template + `autofill-design`، وبعدها `resize-design` لكل منصة.

### 4.2 البرزنتيشن
- 1920×1080 (16:9). **فكرة واحدة لكل سلايد**، قاعدة 6×6 كحد أقصى (6 نقاط × 6 كلمات).
- عنوان السلايد 40–60px، نص ≥ 24px.
- هيكل ثابت: غلاف · أجندة · فواصل أقسام · محتوى (3–4 Layouts متكررة) · أرقام/Charts · خاتمة/CTA.
- Speaker notes بـ `replace_speaker_notes` بدل حشو النص على السلايد.
- Workflow: Outline → `request-outline-review` → موافقة → `generate-design-structured` مع `brand_kit_id`.

### 4.3 الكومباني بروفايل
- A4 عمودي (210×297mm) أو أفقي، 12–24 صفحة. **Bleed 3mm**، Safe margin 10–15mm.
- الهيكل: غلاف · كلمة المدير · من نحن · الرؤية/الرسالة/القيم · الخدمات · المشاريع/Case Studies · الأرقام والإنجازات · العملاء/الشركاء · الفريق · الشهادات · تواصل معنا · الغلاف الخلفي.
- Master Layout ثابت: هيدر/فوتر، رقم الصفحة، نفس مكان اللوجو.
- تصدير: PDF Print + **CMYK + Crop marks & bleed** (Pro) للطباعة، وPDF عادي مضغوط للإيميل/الواتساب.

### 4.4 الـ CV
- A4 أو US Letter، **صفحة واحدة** (أو 2 للخبرة الطويلة).
- **ATS-friendly**: عمود واحد أو عمودين بسيطين، من غير جداول معقدة ولا نص جوه صور، عناوين قياسية (Experience, Education, Skills).
- الترتيب: الاسم والمسمى · التواصل · ملخص 3–4 سطور · الخبرة (عكسي زمنيًا، إنجازات بأرقام) · التعليم · المهارات · الشهادات · اللغات.
- خط 10–12pt للنص، 14–18 للأقسام، 22–28 للاسم. لون Accent واحد. الصورة الشخصية حسب السوق (الخليج/مصر غالبًا مقبولة، أوروبا/أمريكا لأ).
- Workflow: `generate-design` (design_type: resume) + `brand_kit_id` أو Brand Template + `autofill-design`، وكمان نسخة `docx` للـ ATS.

### 4.5 البرشورز
| النوع | المقاس | ملاحظات |
|---|---|---|
| Tri-fold A4 | 297×210mm × وشّين | 3 بانلز (البانل اللي بيتطوي جوه أصغر 2–3mm). |
| Tri-fold Letter | 11×8.5in | |
| Bi-fold | A4 → A5 | 4 صفحات. |

- ترتيب البانلز: الغلاف (بانل يمين برا)، الخلفي (نص برا)، الـ Flap الداخلي، ثم الـ 3 الداخلية. في العربي اتجاه الفتح معكوس.
- Bleed 3mm، ماتحطش نص على خطوط الطي (سيب 5mm حواليها).
- `insert_shape` لتحديد البانلز، `add_page` للوش التاني. تصدير PDF Print + CMYK.

---

## 5) الـ Workflow الموحد اللي يضمن التناسق

```
1. Brief       ← هدف، جمهور، رسالة، المنصة، اللغة (عربي/إنجليزي)
2. Brand       ← list-brand-kits → اختيار الكيت (أو تأكيد إن مفيش براند)
3. Template?   ← search-brand-templates → لو موجود: create-design-from-brand-template / autofill-design
4. Generate    ← generate-design (+brand_kit_id) → create-design-from-candidate
                 أو create-design لو مفيش براند
5. Polish      ← read-design(open_transaction) → edit-design: محاذاة، أحجام خط، ألوان HEX، مسافات
6. QA          ← Checklist (تحت) + thumbnails
7. Approve     ← تعرض المعاينة وتاخد موافقتك → commit
8. Variants    ← resize-design لكل منصة
9. Export      ← get-export-formats → export-design
10. Organize   ← create-folder / move-item-to-folder ، ولو التصميم نجح: publish-brand-template
```

## 6) Checklist الجودة قبل التسليم
- [ ] كل الألوان من الـ Brand Kit (≤ 3 + محايدين) وتباين ≥ 4.5:1
- [ ] خطين بس، والأحجام من السلّم
- [ ] كل العناصر على الـ Grid ومحاذية، والمسافات مضاعفات 8
- [ ] عنصر بطل واحد، CTA واضح
- [ ] الهوامش/Safe zones محترمة (Story، Bleed للطباعة)
- [ ] العربي: محاذاة يمين، اتجاه معكوس، نظام أرقام واحد، الخط بيعرض كل الحروف
- [ ] مفيش أخطاء إملائية، والأسماء والأرقام صح
- [ ] الصور عالية الدقة، `alt_text` موجود
- [ ] الصيغة الصح: PNG للسوشيال، PDF Print CMYK للطباعة، PPTX/PDF للبرزنتيشن

---

## 7) الفجوات والتوصيات
1. **ثبّت السكيل** `skills/canva-design-system/SKILL.md` (موجود في الريبو ده) على claude.ai: Settings → Capabilities → Skills → Upload (مضغوط ZIP للفولدر)، أو حسّنه بـ `skill-creator` واختبره على 5 طلبات حقيقية.
2. **كمّل الـ Brand Kits**: كيت `abdelrahman maghraby` و`IB Creative studio` من غير Thumbnail — غالبًا ناقصين لوجو. ضيف لكل كيت: لوجو (أفقي/مربع/أبيض)، 3 ألوان HEX، خط عناوين + خط نص.
3. **ابنِ Brand Templates** لكل نوع (بوست Quote، بوست Promo، Story، سلايد، CV، صفحة بروفايل) وعلّم الحقول بـ `update_autofill_field` ← ده اللي بيخلّي النتايج متطابقة كل مرة.
4. **أعد توصيل Adobe plugin** (فشل بـ 403) عشان أدوات اقتراح الخطوط والـ Type palettes.
5. الطباعة بـ CMYK محتاجة **Canva Pro**.

---

## 8) السكيلز المتاحة أونلاين على GitHub (بحث نوفمبر 2026)

> ⚠️ **تنبيه أمان:** دي سكيلز مفتوحة المصدر من طرف تالت. أنا جمعتها من بحث GitHub (الاسم + الوصف + النجوم) **ومراجعتش الكود بتاعها**. السكيل ممكن يكون فيه سكريبتات بتتنفّذ، فاقرا ملف `SKILL.md` وأي سكريبتات جواه قبل ما تثبّته. النجوم مش ضمان جودة.

### أ) السكيلز الرسمية من Anthropic — `github.com/anthropics/skills`
ابدأ بيها لأنها الأكثر أمانًا (مقدرتش أفتح الريبو من الجلسة دي، فالقائمة من معرفتي بالريبو):
| السكيل | الفايدة |
|---|---|
| **brand-guidelines** | مثال لسكيل بيطبّق ألوان وخطوط هوية ثابتة على أي ناتج ← **أحسن نموذج تبني عليه سكيل البراند بتاعك**. |
| **theme-factory** | ثيمات جاهزة (ألوان + خطوط) تتطبق على سلايدز/مستندات/صفحات. |
| **canvas-design** | تصميم بوسترات وفن بصري PNG/PDF بـ "فلسفة تصميم". |
| **frontend-design** | قواعد ضد "الشكل العام الممل" للـ AI — مفيدة للهيراركي والمسافات. |
| **pptx / docx / pdf / xlsx** | نفس اللي مفعّلين عندك. |
| **skill-creator** | لبناء واختبار سكيلز جديدة. |

### ب) مجموعات (Awesome lists) — مكان تدوّر فيه
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| ComposioHQ/awesome-claude-skills | 78.5k | أكبر قائمة منسّقة لسكيلز Claude. |
| VoltAgent/awesome-agent-skills | 36.7k | +1000 سكيل من فرق رسمية والمجتمع. |
| travisvn/awesome-claude-skills | 15.7k | قائمة منسّقة. |
| BehiSecc/awesome-claude-skills | 10.3k | قائمة منسّقة. |
| sickn33/agentic-awesome-skills | 49k | +2800 سكيل (كمية كبيرة، فلتر بحذر). |

### ج) سكيلز تصميم عامة (تناسق + جودة بصرية)
| الريبو | ⭐ | الفايدة لينا |
|---|---|---|
| nextlevelbuilder/ui-ux-pro-max-skill | 143k | "ذكاء تصميم": ألوان، خطوط، أنماط — موجّه أكتر للـ UI بس قواعده مفيدة. |
| Nutlope/hallmark | 44.8k | سكيل ضد "AI slop" — بيمنع الشكل العام المكرر. |
| alchaincyf/huashu-design | 28.4k | من جملة لتصميم: PPTX قابل للتعديل، إنفوجرافيك، 84 ستايل (صيني). |
| ConardLi/garden-skills | 13.5k | مجموعة فيها تصميم وتوليد صور. |
| fatihaydost/brand-identity-skill | 281 | بيبني هوية كاملة (لوجو + خطوط + ألوان) كنظام واحد ← مفيد قبل ما تعمل Brand Kit. |
| arvindrk/extract-design-system | 267 | يستخرج Design tokens (ألوان/خطوط/مسافات) من أي موقع ← تاخد هوية عميل من موقعه. |

### د) Canva تحديدًا
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| OpenAnalystInc/10x-Canva-Skills | 7 | تكامل Canva API + تعديل PDF/PPTX/DOCX (بيستخدم الـ API مباشرة مش الـ Connector). |
| 10x-Anit/10X-Canva-Skills | 4 | نسخة مشابهة. |
| OpenAnalystInc/10x-Content-Expert | 22 | محتوى: إيميلات وسوشيال. |
> الخلاصة: **مفيش سكيل Canva قوي ومنتشر** — عشان كده السكيل اللي في الريبو ده (`skills/canva-design-system`) هو اللي بيسد الفجوة لأنه مبني على أدوات الـ Connector اللي عندك فعلًا.

### هـ) سوشيال ميديا
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| sergebulaev/instagram-skills | 697 | كابشنز، كاروسيل، Hooks، هاشتاجات، خطة أسبوعية. |
| social-media-skills/skills | 232 | 106 سكيل: استراتيجية، كتابة، فيديو، تصميم، نشر. |
| itchernetski/threads-carousel-claude-skill | 119 | يحوّل بوست نصي لكاروسيل صور (IG/LinkedIn/TikTok). |
| **saoudphotos/arabic-brand-carousel** | 20 | **كاروسيل إنستجرام عربي بهويتك** ← الأقرب لاحتياجك العربي. |
| VicUgochukwu/brand-design-skill | 6 | تصميمات LinkedIn بالبراند (كاروسيل، بانر). |
| omrajguru/brand-social-design | 2 | جرافيكس سوشيال متناسقة مع البراند كـ HTML. |
| kmcdotninja/social-post-designer | 3 | من Brief لمعرض بوستات كامل. |

### و) برزنتيشن
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| Gabberflast/academic-pptx-skill | 1.4k | برزنتيشن أكاديمي (مؤتمرات، مناقشات رسائل). |
| likaku/Mck-ppt-design-skill | 328 | ستايل شركات الاستشارات (McKinsey-like)، 70 Layout ← ممتاز للبرزنتيشن البيزنس. |
| Akxan/ppt-agent-skill | 172 | 26 ستايل و18 نوع Chart. |
| SlideSpeak/slide-design-skill | 33 | بيستنتج ستايل خاص ويطلع 1920×1080. |
| Phlegonlabs/Powerpoint-fancy-design | 42 | Markdown → سلايدز مصممة. |

### ز) CV
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| Paramchoudhary/ResumeSkills | 3k | مجموعة لتحسين الـ CV والتقديم. |
| varunr89/resume-tailoring-skill | 851 | تفصيل الـ CV على كل وظيفة. |
| ndpvt-web/latex-document-skill | 809 | 27 تمبليت LaTeX (CV ومستندات احترافية). |
| yanliudesign/offer-toolkit-skill | 551 | Resume builder بـ 11 تمبليت + تحليل الوظيفة. |
| proficientlyjobs/proficiently-claude-skills | 444 | CV + Cover letter. |

### ح) كومباني بروفايل وبرشورز (مطبوعات)
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| stanesjenson11-lgtm/Folio---Claude-Design-Skill-For-Poster-Brochure-Magazine | 3 | مطبوعات: مجلات، **برشورز، كومباني بروفايل**، بوسترات. |
| alphaparkinc/genpark-print-ready-vector-brochure-catalog-typesetter-skill | 8 | برشور/كتالوج جاهز للطباعة CMYK. |

### إنفوجرافيك (للبروفايل والبرزنتيشن)
| الريبو | ⭐ | ملاحظة |
|---|---|---|
| joshua-heygen/viz-pack | 64 | 4 سكيلز: دياجرامز، إنفوجرافيك، شرح تفاعلي. |
| ericblue/visual-explainer-skill | 64 | يحوّل أي محتوى لشرح بصري. |

### ترشيحي: Stack عملي ليك
1. **الأساس:** `skills/canva-design-system` (اللي في الريبو) + Brand Kits بتوعك في Canva.
2. **من Anthropic:** `brand-guidelines` (كنموذج) + `theme-factory`.
3. **حسب النوع:** `arabic-brand-carousel` للسوشيال العربي · `Mck-ppt-design-skill` للبرزنتيشن · `ResumeSkills` للـ CV · `Folio` للبروفايل والبرشور.
4. **ضد الشكل المكرر:** `hallmark`.
5. ثبّت كل واحد على حدة واختبره على طلب حقيقي قبل ما تضيف التاني — كتر السكيلز المتعارضة بيلخبط Claude.
