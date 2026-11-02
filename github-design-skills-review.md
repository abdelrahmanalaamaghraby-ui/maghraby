# مراجعة سكيلز التصميم المفتوحة على GitHub

> تاريخ المراجعة: 2 نوفمبر 2026 · عدد الريبوهات: 12
> **إزاي اتراجعت:** عملت نسخة (clone) من كل ريبو، وعديت على كل الملفات أدوّر على: اتصالات شبكة ورايحة لأنهي دومين، تشغيل أوامر (subprocess/exec)، قراية مفاتيح أو ملفات حساسة، تشفير مخفي، Hooks وإعدادات بتتغيّر لوحدها، وجمل جوه الـ SKILL.md بتطلب من Claude يخبّي حاجة أو يتجاهل المستخدم. وبعدين قريت ملف SKILL.md الأساسي لكل واحد عشان أقيّم الجودة ومدى مناسبته ليك.
> **حدود المراجعة:** دي مراجعة يدوية سريعة، مش تدقيق أمني كامل سطر بسطر للريبوهات الكبيرة (hallmark فيه 845 ملف، ui-ux-pro-max فيه 700). مشغّلتش أي سكريبت منهم.

---

## الحكم السريع

| السكيل | الأمان | الجودة | مناسب ليك؟ | القرار |
|---|---|---|---|---|
| **anthropics/skills** (brand-guidelines, theme-factory, canvas-design) | ✅ رسمي | عالية | جزئيًا | ✅ **ثبّت theme-factory**، واستخدم brand-guidelines كنموذج بس |
| **saoudphotos/arabic-brand-carousel** | ✅ نص بس، مفيهوش كود | عالية | **جدًا** (كاروسيل عربي) | ✅ **ثبّته** |
| **Paramchoudhary/ResumeSkills** | ✅ نص بس، مفيهوش كود | جيدة | **جدًا** (CV) | ✅ **ثبّت 3 بس منه** |
| **stanesjenson11-lgtm/Folio** | 🟡 سكريبتات بتنزّل خطوط، وبتكتب في `~/.claude/commands` | **عالية جدًا** | **جدًا** (بروفايل وبرشور) | 🟡 **ثبّته بحذر** (في Claude Code) |
| **fatihaydost/brand-identity-skill** | 🟡 بيفتح مواقع عشان يستخرج الألوان | عالية | مفيد قبل ما تعمل Brand Kit | 🟡 اختياري |
| **likaku/Mck-ppt-design-skill** | 🟡 بيبعت لـ Tencent Cloud (لو حطيت مفاتيح) | جيدة | برزنتيشن PPTX مش Canva | 🟡 اختياري، ومن غير مفاتيح Tencent |
| **sergebulaev/instagram-skills** | 🟡 APIs خارجية (Apify, Publora, Pixfaro) لو حطيت مفاتيح | جيدة | محتوى وكابشن، مش تصميم | 🟡 اختياري (ممكن يتعارض مع egyptian-content-agent) |
| **Nutlope/hallmark** | 🟡 Hook بيشغّل linter، وAPIs اختيارية | عالية | **لأ**: للمواقع بس | ❌ مش ليك دلوقتي |
| **nextlevelbuilder/ui-ux-pro-max** | 🟠 فيه إعدادات `enableAllProjectMcpServers` و`Read(//home/**)` في مجلد فرعي | عالية | **لأ**: UI/مواقع | ❌ مش ليك |
| **OpenAnalystInc/10x-Canva-Skills** | 🟠 محتاج Canva Client Secret وملف .env، وفيه statusline بيشغّل أوامر | متوسطة | **لأ**: عندك الـ Connector الرسمي | ❌ **ماتثبّتوش** |
| **VicUgochukwu/brand-design-skill** | ✅ | ضعيفة: README بس، مفيش SKILL.md | — | ❌ فاضي تقريبًا |
| **alphaparkinc/genpark-…brochure** | ⚠️ | **مزيف**: الكود بيرجّع نتايج ثابتة وروابط وهمية | — | ❌ **تجنّبه** |

مالقيتش في أي ريبو منهم جمل في SKILL.md بتطلب من Claude يخبّي حاجة عن المستخدم، ولا كود بيبعت بياناتك لسيرفر غريب من غير ما تحط بنفسك مفتاح للخدمة دي.

---

## التفاصيل

### ✅ 1. anthropics/skills — الرسمي
- **brand-guidelines**: 329 كلمة، وبيطبّق ألوان وخطوط **Anthropic نفسها**. مش هتستخدمه زي ما هو؛ **انسخ هيكله** وحط ألوانك. ده بالظبط اللي عملته في `skills/canva-design-system`.
- **theme-factory**: 10 ثيمات جاهزة، كل واحد فيه ألوان HEX وخط عناوين وخط نص (Ocean Depths, Modern Minimalist, Tech Innovation, Golden Hour…). **مفيد جدًا** لما العميل مايكونش عنده هوية. بيعرض للمستخدم ملف PDF فيه الثيمات ويستنى يختار.
- **canvas-design**: بيعمل "فلسفة تصميم" وبعدين بوستر PNG/PDF فني (90% بصري و10% نص). كويس للبوسترات الفنية، **مش مناسب** للبروفايل والـ CV.
- آخر تحديث: 28 أكتوبر 2026.

### ✅ 2. saoudphotos/arabic-brand-carousel — أفضل سكيل عربي
- 960 كلمة، ومفيهوش أي كود (ملف SKILL.md وصور أمثلة).
- **نقط قوته:** RTL، خط Cairo 900/700، أحجام محددة (عناوين 110–130px، نص 40–50px)، هامش 80px، "Brand bar" ثابت في كل شريحة (عدّاد، تصنيف، لوجو، سهم سحب)، كلمة واحدة مميزة بلون الـ Accent، تقل عن 40 كلمة في الشريحة، وتقييم من 100 قبل التسليم.
- **ملاحظة:** بيطلّع HTML وبعدين PNG، **مش Canva**. ممكن تاخد الـ PNG وتعمله import في Canva، أو تاخد قواعده وتحطها في سكيل الـ Canva (وده اللي هعمله تحت).
- آخر تحديث: 18 أكتوبر 2026.

### ✅ 3. Paramchoudhary/ResumeSkills — مكتبة CV
- 22 سكيل، كلهم نصوص من غير كود. **ماتثبّتهمش كلهم**؛ هيلخبطوا Claude في اختيار السكيل المناسب.
- **الأهم ليك:** `resume-formatter` (تنسيق متوافق مع ATS وتخطيط)، و`resume-ats-optimizer`، و`resume-bullet-writer` (إنجازات بأرقام).
- لا يغطي التصميم البصري على Canva؛ هو للمحتوى والهيكل. يتكامل مع سكيل Canva بتاعك.
- آخر تحديث: يونيو 2026.

### 🟡 4. Folio — أقوى سكيل للمطبوعات (بروفايل وبرشور ومجلات)
- 3,167 كلمة ومكتبة ستايلات كبيرة. **الجودة ممتازة**: بيفكّر زي Art Director (Flatplan، Spreads، Grid من 12 عمود، تنويع بين صفحات "عالية" و"هادية"، تحذير صريح من شكل "Canva template"، قاعدة "الحقائق قبل الافتراضات" وماينفعش يخترع أرقام أو أسماء).
- بيطلّع HTML ثم PDF، **وكمان نسخة قابلة للتعديل على Canva**.
- **ليه 🟡:**
  - `fonts.py` بينزّل خطوط من Google Fonts ومن npm (`@fontsource`). المصادر معروفة، بس بيشغّل `npm pack`.
  - أمر `setup` بيكتب ملفات في `~/.claude/commands/`.
  - محتاج Claude Code (ترمينال/ديسكتوب) عشان يشتغل كامل، وعلى claude.ai هيشتغل جزئيًا.
  - مفيهوش دعم واضح للعربي/RTL جوه القواعد.
- **التوصية:** ثبّته لو هتشتغل بروفايلات كتير، وراجع `scripts/` قبل أول تشغيل.

### 🟡 5. fatihaydost/brand-identity-skill
- بيبني هوية (لوجو وخطوط وألوان) **ويقيسها**: تباين، عمى ألوان، تغطية الحروف، رخص الخطوط. فيه `site_palette.py` بيفتح موقع العميل عشان يستخرج ألوانه، وده طبيعي.
- مفيد **مرة واحدة لكل عميل جديد** قبل ما تعمل له Brand Kit على Canva. آخر تحديث: أمس.

### 🟡 6. likaku/Mck-ppt-design-skill
- بيطلّع PPTX بستايل McKinsey وفيه 67 Layout، وبيشتغل بـ python-pptx.
- `cover_image.py` بيستخدم **Tencent Hunyuan** (سيرفرات صينية) لتوليد صور الغلاف **لو** حطيت `TENCENT_SECRET_ID`. من غير المفاتيح دي مابيبعتش حاجة.
- جزء كبير من التعليمات **بالصيني**. مناسب لو عاوز PPTX، **مش Canva**.

### 🟡 7. sergebulaev/instagram-skills
- 9 سكيلز (كابشن، تخطيط كاروسيل، Hooks، هاشتاجات…). خدمات خارجية (Apify, Publora, Pixfaro) بتشتغل **بس** لو حطيت مفاتيحها.
- ده محتوى مش تصميم، وبيتداخل مع `egyptian-content-agent` اللي عندك. ممكن تاخد منه `ig-carousel-planner` بس.

### ❌ 8. Nutlope/hallmark و ui-ux-pro-max
- الاتنين ممتازين بس **للمواقع والتطبيقات**، مش للسوشيال والمطبوعات.
- ui-ux-pro-max فيه مجلد `stack/.claude/settings.json` بيدّي صلاحيات واسعة (`Read(//home/**)` و`enableAllProjectMcpServers`). مش خطر وأنت بتثبّت السكيل نفسه، بس لو فتحت المجلد ده كمشروع في Claude Code الصلاحيات دي هتشتغل.

### ❌ 9. OpenAnalystInc/10x-Canva-Skills
- بيستخدم **Canva REST API** مباشرة، ومحتاج تعمل Canva Developer App وتحط Client Secret وAccess Token في ملف `.env`. بيبعت بس لـ `api.canva.com`، وده سليم، **بس**:
  - عندك أصلًا **Canva Connector الرسمي** وهو أأمن (OAuth من غير ما تحفظ مفاتيح).
  - فيه `statusline.cjs` و`settings.json` بيغيّروا إعدادات Claude Code ويشغّلوا أوامر.
  - السكيلز نفسها CRUD عادي (إنشاء/بحث/تصدير) **من غير قواعد تصميم**.
- **ماتثبّتوش.**

### ❌ 10. alphaparkinc/genpark-…brochure — مزيف
- ملف `client.py` بيرجّع **نتيجة ثابتة مكتوبة يدويًا** (`'cmyk_color_separation_verified': True` ورابط PDF وهمي)، يعني مابيعملش أي تصميم. حسابات alphaparkinc عندها عشرات الريبوهات بنفس الشكل. **تجنّبها كلها.**

---

## الـ Stack النهائي اللي أنصحك بيه

| الاحتياج | السكيل |
|---|---|
| **أي تصميم على Canva** | `canva-design-system` (في الريبو ده، واتحدّث بقواعد الكاروسيل العربي) |
| عميل بدون هوية | `theme-factory` (رسمي) |
| كاروسيل عربي PNG بسرعة | `arabic-brand-carousel` |
| CV | `resume-formatter` + `resume-ats-optimizer` + `resume-bullet-writer` + `docx` (عندك) |
| كومباني بروفايل / برشور جودة عالية | `folio` (في Claude Code، بعد مراجعة السكريبتات) |
| هوية لعميل جديد | `brand-identity-skill` (اختياري) |

**قاعدة:** ثبّت واحد واحد، وجرّبه على طلب حقيقي، وبعدين اللي بعده.
