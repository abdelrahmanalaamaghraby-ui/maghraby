# Arabic social recipes (Canva-only)

Six production recipes distilled from professional Arabic social media work. Every step uses only Canva connector tools; items marked **[manual]** are quick finishing touches the user does in the Canva editor (tell them exactly which ones).

HEX values are starting points. Replace them with the chosen Brand Kit colors when one exists.

## Shared build pattern (use for every recipe)

1. `list-brand-kits` → confirm the kit (or use the recipe palette).
2. Hero imagery: `generate-image` with one fixed lighting/style sentence reused for every image in the series → `remove-background` on each subject → keep the returned media ids.
3. Master post: `generate-design` (with `brand_kit_id`) or `create-design` with a brief that states: size, palette HEX, heading weight 900 + body 400–500, Arabic RTL, fixed zones (logo / headline / hero / footer), the motif, and the emphasis style.
4. Polish the master: `read-design` (`open_transaction: true`, thumbnails) → `edit-design`:
   - emphasis rectangle: `insert_shape` (accent, rect path) + `layer_element: back` behind the keyword;
   - underline bar: `insert_shape` 8–12px high under the keyword;
   - kashida: `find_and_replace_text` (e.g. "طباعة" → "طبـــاعة");
   - hero: `insert_fill` with the cut-out media id, `position_element`/`resize_element` so it overlaps a card or frame edge;
   - pills/cards: `insert_shape` with `corner_rounding` (pill = half the height; cards 16–24) + `add_text` + `group_elements`;
   - watermark motif: `insert_shape` or an inserted image + `update_opacity` 0.06–0.12;
   - swipe cue / progress dashes: `insert_shape` at the same coordinates on every page.
   Show the thumbnail → user approves → `commit`.
5. Make it repeatable: tag headline/subhead/hero/CTA with `update_autofill_field` → `publish-brand-template` → produce the series with `autofill-design` (one call per post).
6. Alternate backgrounds when the recipe says so: `copy-design` the master → `edit-design` recolor background (`recolor_element`/`update_fill`) → publish as a second template.
7. Variants: `resize-design` (Story 1080×1920, Feed 1080×1350). Export: `export-design` PNG per page.
8. Organize: `create-folder` "<client> – <campaign>" → `move-item-to-folder`.

**[manual] finishing list to give the user:** drop shadow under cut-outs (Effects → Shadows → Drop, blur ~30, 25% opacity) · QR code (Apps → QR Code) · cultural patterns from Elements (search "Sadu", "Islamic pattern") · font swap if the Brand Kit lacks the font.

---

## R1 · Seasonal heritage campaign (e.g. Saudi Founding Day for a restaurant)
- Size 1080×1350. Palette: deep green `#1E3A2B`, parchment `#E9DCC3`, warm brown/gold from photos. Two templates: green bg and parchment bg, alternate in the 3-column grid.
- Background brief: "aged parchment paper texture, soft vignette".
- Motif: vertical Sadu/heritage pattern strip on one edge (`generate-image` "vertical Sadu Najdi weave pattern strip, green and beige" → `remove-background` → `insert_fill` on the edge) + small ornament divider under the headline.
- Zones: occasion logo top-left (fixed) · headline centered upper half · hero dish bottom-center with heritage architecture behind · bottom strip with brand line.
- Image style sentence: "warm golden-hour light, traditional mud-brick architecture, rich Saudi dish, cinematic, shallow depth of field".
- Types: hero announcement · heritage story · offer ("خصم 20%" in a pill) · pride/quote post.

## R2 · Brand puzzle feed (e.g. printing/agency brand, 9–12 posts)
- Size 1080×1350 (or 1080×1080). Palette: brand yellow `#FFD400` (10–20% of area), light textured grey `#E6E6E6`, black text.
- Supergraphic: a huge curve derived from the logo shape (`insert_shape` SVG path, stroke or fill in accent), cropped at the page edge so it visually continues into the neighbouring post; plan positions in a 3-column grid.
- Zones: logo top-center · headline + one highlighted word (yellow rectangle behind) · 3D/cut-out product or person breaking out of the frame · footer phone + website (identical on all posts).
- Opening row of 3 single-word verb posts (اطبع / صوّر / صمّم) with the yellow box behind the word.
- Types: service · offer with giant number (`add_text` 300–450px, bold, accent) · engagement question · tip ("دليل الهوية") · testimonial person.

## R3 · News / explainer carousel cover
- Size 1080×1350. Parchment or soft paper background; headline in a dark brand color (e.g. `#2F5D45`).
- Hierarchy: line 1 topic (bold) → line 2 key word larger, kashida-stretched, with underline bar → line 3 numeric promise ("10 نقاط تختصر…").
- Hero: subject photo cut out rising from the bottom (`generate-image` → `remove-background`) + 1–2 storytelling props behind it (documents, tools) also cut out.
- Footer: logo bottom-left, handle bottom-right, swipe icon + progress dashes centered (same spot on every slide).
- Inner slides: one point per slide, number badge, ≤ 40 words. Last slide: single CTA (follow / save / share).

## R4 · Institutional series (ministry / authority / academy)
Pick one system per client and never mix:
- **Culture style:** off-white `#F1EEE6`, olive/khaki accent `#8C7B4E`, headline top + khaki label pill, one central realistic 3D object (column, hourglass, compass) with a soft shadow [manual], big stats ("+23000").
- **Utility/energy style:** deep teal `#1F4A44` background, white text, documentary photos of places, low-opacity floral/leaf motif in a fixed corner.
- **Academy/education style:** two alternating colors (teal `#1F6F6B` / maroon `#6B2338`), surreal collage hero (person with head replaced by a camera, bulb, TV — via `generate-image`), text on a torn-paper card (`generate-image` "torn white paper note" → `remove-background`).
- Always: partner logos top-center, same headline zone, one hero, kashida on one keyword.

## R5 · Gulf storytelling carousel
- Size 1080×1350. Palette: cream `#F3EEE6`, orange accent `#E8892B`, dark text.
- Cover: full-bleed family/lifestyle photo + dark gradient overlay (`insert_shape` full-page rect, black, `update_opacity` 0.45 at bottom area), white headline, one orange word.
- Inner slides: plain cream background, photo inside a tilted polaroid frame (`insert_shape` white rect + photo `insert_fill`, `rotate_element` −4…−6°, `group_elements`), headline with one orange word.
- Swipe cue: arrow inside a circle, bottom-right, every slide except the last. Last slide: orange pill CTA ("قدّم الآن في الرابط").

## R6 · Event / competition stories (information-heavy)
- Size 1080×1920. Palette: emerald gradient `#1E8C6E`→`#0E5A47`, mint-white `#EEF6F2`, gold `#C9A55A`. Alternate green and white posts.
- Premium hero: the award/event name as gold calligraphy (`generate-image` "gold Thuluth Arabic calligraphy of the words '<name>' on transparent background" → `remove-background`). Use it as the only ornate element.
- Header: row of partner logos top-center (fixed). Watermark: Islamic geometric pattern at opacity 0.06–0.1; small ornament tile in the top corner of white posts.
- Module order for info posts: title → pill sub-heading ("محاور اللقاء") → 2×2 icon cards (rounded 20, mint/white) → speaker card (cut-out photo, name, title) → date / time / place rows with icons → CTA pill "سجّل الآن" + QR [manual] + phone footer.
- Other post types: prize amount ("100,000 ﷼" in a large pill), "10+ participating centers" big number, vertical timeline (icon square + stage + date per row), quote note on torn paper with page number "01".

---

## Quality bar (check on every post before asking to commit)
- Same logo position/size, footer, margins (≥ 64–80px) and emphasis style across the series.
- One emphasized word, one hero, one premium element per post.
- Headline ≤ 2 lines; body text ≥ 28px on 1080-wide posts.
- All images share one lighting/grade sentence.
- In the 3-column grid preview the alternation/supergraphic reads as intended (ask for `thumbnails` of each design).
