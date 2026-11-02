---
name: canva-design-system
description: Use whenever the user asks to design anything in Canva — social media posts, stories, carousels, presentations/decks, company profiles, CVs/resumes, brochures, flyers — in Arabic or English. Enforces a consistent design system (brand kit, type scale, 8px grid, 60-30-10 color, safe zones, RTL rules) and the correct Canva connector tool sequence, then runs a QA checklist before saving or exporting.
---

# Canva Design System

Goal: every Canva design Claude produces looks like it came from the same professional designer: on-brand, aligned, readable, correctly sized, print/export ready.

## 0. Before any tool call: collect the brief
Ask only for what is missing (one short message):
- Design type + platform/size (see section 3)
- Language (Arabic → apply RTL rules in section 2.5)
- Goal and the single key message / CTA
- Brand: which Brand Kit, or "no brand"
- Content: exact text, numbers, photos, logo

## 1. Tool workflow (Canva connector)

1. **Brand**: `list-brand-kits` → confirm which kit with the user.
2. **Template first**: `search-brand-templates` (use `dataset: "non_empty"` for fillable ones).
   - Found → `get-brand-template-dataset` → `autofill-design` (or `create-design-from-brand-template`).
3. **Generate**:
   - On-brand (brand kit chosen): `generate-design` with `brand_kit_id` and the right `design_type`, then `create-design-from-candidate` on the candidate the user picks.
   - On-brand presentation: `request-outline-review` → user approves → `generate-design-structured` with `brand_kit_id` (strip punctuation from outline titles/descriptions as that tool requires).
   - No brand: `create-design` with a detailed brief and explicit `format` incl. orientation (e.g. "Flyer (Portrait A4)"); for decks pass an approved `outline`.
   - Always put the design rules from section 2 inside the brief/query text (colors as HEX, fonts, tone, layout, RTL).
4. **Polish**: `read-design` with `open_transaction: true` + `thumbnails` → `edit-design` (`keep_open`) to fix alignment, sizes, colors, spacing → show the thumbnail → get explicit approval → `edit-design` `commit`.
   - Note: `format_text` cannot change font family (comes from Brand Kit/template); weight is bold/normal only.
5. **Variants**: `resize-design` (custom width/height) for each extra platform.
6. **Export**: `get-export-formats` → `export-design`.
7. **Organize**: `create-folder` per client/project, `move-item-to-folder`. When a design is approved and reusable, offer `publish-brand-template` (after tagging fields with `update_autofill_field`).

Never commit edits, delete pages (`merge-designs`) or overwrite with `autofill-design update_in_place` without explicit user approval.

## 2. Design rules (apply to every design)

### 2.1 Color
- 60-30-10: 60% base/neutral, 30% secondary, 10% accent (CTA only).
- Max 3 brand colors + neutrals. Use exact HEX from the Brand Kit.
- Contrast: body text ≥ 4.5:1, large text ≥ 3:1. Text over photos → add a solid/gradient overlay (opacity 0.5–0.7).

### 2.2 Typography
- Max 2 families (heading + body). Arabic: Cairo, Tajawal, IBM Plex Sans Arabic, Almarai, Noto Kufi Arabic. Latin: Montserrat, Poppins, Inter, Playfair Display (headings only).
- Type scale ratio 1.25–1.333. Social (1080 wide): H1 72–96, H2 40–48, body 28–32, caption 22–24. Slides (1920): title 48–60, subtitle 32–36, body 24–28. Print A4: H1 28–36pt, H2 16–20pt, body 9.5–11pt.
- Line height: body 1.4–1.6 (Arabic 1.5–1.7), headings 1.1–1.25. Line length 45–75 characters.

### 2.3 Layout
- Spacing unit 8px: use 8/16/24/32/48/64/96 only.
- Margins: social ≥ 64–80px, slides ≥ 80–100px, print ≥ 10–15mm inside trim.
- Grid: 12 columns for slides/print, 4–6 for social. Every element aligns to the grid or to another element.
- One hero element per page; clear visual hierarchy; ≥ 30% white space.
- Logo: same corner and size on every page/post of a series.

### 2.4 Imagery & icons
- One icon style (line or filled, same stroke). One photo treatment across the set. Always set `alt_text`.
- Print images ≥ 300 DPI.

### 2.5 Arabic / RTL
- Right-aligned text (`text_align: end` in RTL context), reading flow starts top-right; mirror arrows, timelines, progress and brochure panel order.
- Pick a font that renders all Arabic glyphs; Canva's Translate setting "Mirror page to match text direction" can mirror a layout.
- One numeral system per design (١٢٣ or 123). Don't mix Arabic and Latin in one line unless necessary.

## 2.6 Arabic social media playbook (learned from pro reference work)

Define a **series system** before the first post and reuse it on every post:
- 2 background colors (alternate them across the 3-column feed grid) + 1 accent + neutrals.
- Heading font (heavy, 800–900) + body font (400–500). Cairo / Tajawal / Almarai / El Messiri; calligraphy (Thuluth/Diwani style) only as a single premium hero (e.g. a campaign name), never for body.
- One image style for the whole series: cut-out 3D objects, warm-graded photos, or surreal collage.
- One motif: a cultural pattern (Sadu, Islamic geometry) on edges or as a low-opacity watermark, or a supergraphic derived from the logo shape that continues across adjacent posts.

Fixed zones on every post: logo/partner logos (top center or one fixed corner) · headline zone · hero zone · footer (phone, website or handle; QR for events).

Headline: max 2 lines, very heavy weight. Emphasize **one** word only, using one of: accent color, a solid accent rectangle behind it (`insert_shape` + `layer_element: back`), an 8–12px underline bar, or kashida/tatweel stretching (طبـــاعة).

Hero: one cut-out subject (`generate-image` → `remove-background` → `insert_fill`), may overlap frame/card edges for depth. Keep lighting/color grading identical across the series.

Backgrounds: textured (paper, grain, soft gradient, vignette) rather than flat.

Information-heavy posts (events, competitions, courses): never paragraphs. Use modules: pill sub-heading → 2×2 icon cards (rounded 16–24px) → speaker card (cut-out photo + name + title) → date/time/place rows with icons → CTA pill "سجّل الآن" + QR + phone.

Content mix in one template family: service · offer (giant 3D-style number in accent) · engagement question · tip/info · quote (torn-paper note) · timeline.

Carousel: cover = topic + one stretched/highlighted word + numeric promise ("10 نقاط") + storytelling hero (subject + props); every slide shows a swipe cue (arrow in circle or progress dashes) in the same spot; last slide = one CTA.

Canva limits: the connector cannot add drop shadows, text effects or change font family. Put fonts/styles in a Brand Kit or a master Brand Template; build one master post, tag fields with `update_autofill_field`, `publish-brand-template`, then produce the series with `autofill-design`.

## 3. Per-type specs

### Social media
| Use | Size |
|---|---|
| Instagram/Facebook feed | 1080×1350 (default) or 1080×1080 |
| Story / Reels / TikTok | 1080×1920, keep top ~250px and bottom ~350px clear |
| Carousel | 1080×1350, 5–10 slides, slide numbers, last slide = CTA |
| LinkedIn post / banner | 1080×1350 or 1200×1200 / 1584×396 |
| X post | 1600×900 |
| YouTube thumbnail | 1280×720, ≤ 5 words |
Rules: one message per post; minimal on-image text; a series uses 2–3 fixed layouts (e.g. quote, tip, promo).

### Presentation
1920×1080. One idea per slide, max 6 bullets × 6 words. Structure: cover → agenda → section dividers → 3–4 repeating content layouts → data/charts → closing CTA. Put detail in speaker notes (`replace_speaker_notes`).

### Company profile
A4 (portrait default), 12–24 pages, 3mm bleed, 10–15mm safe margin. Sections: cover, chairman/CEO word, about, vision/mission/values, services, projects/case studies, numbers, clients/partners, team, certifications, contact, back cover. Fixed header/footer, page numbers, logo position. Export: PDF Print + CMYK + crop marks & bleed for print; standard compressed PDF for digital.

### CV / Resume
A4 or Letter, 1 page (2 max for 10+ years). ATS-safe: single or simple two-column, no text in images, standard headings. Order: name + title, contact, 3–4 line summary, experience (reverse-chronological, quantified achievements), education, skills, certifications, languages. Body 10–12pt, section 14–18pt, name 22–28pt, one accent color. Offer a parallel .docx version (docx skill) for ATS portals.

### Brochure
Tri-fold A4 (297×210mm, 2 sides, 3 panels; inner fold panel 2–3mm narrower) or bi-fold A4→A5. Panel order outside: back-middle, cover-right (mirrored for Arabic). Keep text ≥ 5mm from folds, 3mm bleed. Export PDF Print + CMYK.

## 4. QA checklist (run before asking for commit approval)
- [ ] Colors only from brand (≤ 3 + neutrals); contrast passes
- [ ] ≤ 2 fonts; sizes follow the scale; consistent weights
- [ ] Aligned to grid; spacing multiples of 8; margins/safe zones respected
- [ ] One hero, clear CTA, enough white space
- [ ] Arabic: RTL alignment and mirrored flow, glyphs render, one numeral system
- [ ] Spelling, names, numbers, contact info verified with the user's input
- [ ] Images sharp, alt text set
- [ ] Correct export: PNG/JPG social, PDF Print CMYK for print, PPTX/PDF for decks

Report to the user: what was created, design link, which rules were applied, and anything that needs their decision.
