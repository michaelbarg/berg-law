# REDESIGN NOTES — "Train Bleu" (Orient Express) redesign

Art-direction pass over `index.html` + `scripts/build-articles.js`. Single-file architecture, i18n mechanism, IDs, and config constants untouched. This file is the running log for the principal.

## 1. Palette — "Train Bleu"

One committed scheme, 1920s grand-luxe rail (CIWL navy-and-brass livery, oxblood leather, ivory menu card):

| Token | Hex | Role |
|---|---|---|
| `--night` | `#0F1E2E` | Prussian midnight — dark lacquer ground (hero, story, contact, featured tariff column) |
| `--night-950` | `#0A1520` | deepest night — footer |
| `--night-800` | `#16293C` | raised panel on night |
| `--ivory` | `#F2EDDF` | paper ground |
| `--ivory-2` | `#FAF7EC` | raised paper (ledger, wizard, tariff card) |
| `--ink` | `#25231C` | walnut-black text on paper |
| `--sepia` | `#57503F` | muted body on paper (6.8:1 on ivory) |
| `--brass` | `#C8A45C` | brass on dark (refined from #DAAD57) |
| `--brass-bright` | `#E3C88F` | champagne highlight |
| `--brass-deep` | `#8A6420` | brass legible on paper (4.6:1 — AA small text) |
| `--oxblood` | `#59202A` | burgundy lacquer (press card, verify band, hover accents) |
| `--parch` | `#D8CDB2` | body text on night (10.7:1) |
| `--mute-d` | `#A89E88` | secondary on night (6.4:1) |

All text pairs verified ≥4.5:1 (WCAG AA small text); most are 6:1+. Old variable names (`--dark`, `--gold`, `--paper`, `--gray`…) kept as aliases so nothing orphaned breaks.

`theme-color` meta updated `#0E141E → #0F1E2E` (not part of the protected SEO head; matches new night).

## 2. Structural changes

- **Section order** (nav + mobile menu reordered to match): hero → **01 about** (the principal, portrait presence) → **02 story** (heritage, night panel + oxblood press card) → **03 services** (numbered ledger) → **04 pricing** ("מסלולי ליווי" tariff) → **05 articles** (journal) → **06 pay** (bureau/order form) → **07 contact** → footer colophon. All sections present and reachable; all anchors unchanged.
- **Numbered kickers**: each section head gets `<div class="kicker"><span class="sec-no">NN</span>…` — the numerals are language-neutral static siblings of the i18n eyebrow, so `applyLang` cannot disturb them.
- **Hero**: full-height night carriage with double hairline frame + corner ticks (`.hero-frame`, top edge dropped below nav), fine brass pinstripes (coach lining), italic champagne em-line, gazette restyled as a departures board (2px brass rule + hairline, tabular date stamps). The giant ghost "§" removed. Radial gold "blob" gradients removed everywhere.
- **Pricing → tariff**: one framed table on paper, hairline columns, prices set in serif oldstyle numerals between hairline rules, features as ruled ledger lines with em-dash markers, middle column as night lacquer panel with framed brass badge plate. No SaaS cards, no rounded corners, no glassmorphism.
- **Articles → journal**: newspaper construction — heavy 2px rule + hairline under the masthead, three ruled columns, no card boxes, small-caps tags, hover = title turns oxblood + 2px brass rule draws across the top of the column. CSS-only restyle; `renderArticles` markup contract (classes `article/article-meta/tag/stamp/read-more/arr`) untouched.
- **Wizard → bureau order form**: steps as roman-numeral plates (I · II · III — static text, JS `data-step` logic untouched), doc options as menu-card rows with dotted leaders (name … price), underlined ledger inputs, summary table with night total row.
- **Contact → correspondence**: underline fields on night, brass-framed hairline icon squares.
- **Footer → colophon**: centered monogram (`logoMarkFooter` preserved) over a diamond-and-rule ornament, then the four columns, livery double-line along the top edge.
- **Livery line**: fixed 1px brass + 1px deep-brass double line across the very top of the viewport (`.livery`), echoed on footer top edge.
- **Emoji removed from all UI chrome** (📞💬✉️📍🕗🔒 in contact lines, mobile bar, WA float, pay-secure) → inline hairline SVG icons, brass `currentColor`, placed *outside* `data-i18n` elements so language switching can't destroy them. Articles/posts content data untouched.
- **WhatsApp float**: night disc, brass double ring, brass WA glyph (recognizable silhouette, no #25D366 green). Moved to `inset-inline-end` so it no longer covers the hero stats in RTL. Mobile bar keeps a deep muted green `#0E4A38` for the WhatsApp cell (recognition + AA contrast with cream text).

## 3. i18n dictionary value edits (keys/structure untouched)

Only these values changed, in all four dictionaries + matching static HTML defaults:

- `navPricing`: he "מסלולי ליווי" · en "Retainers" · ru "Сопровождение" · fr "Formules"
- `prTitle`: he "מסלולי ליווי משפטי לעסקים" · en "Retainer Programmes for Businesses" · ru "Программы юридического сопровождения бизнеса" · fr "Formules d'accompagnement juridique des entreprises"
- Nav-length fixes (labels only, so nav fits 1280px in all 4 languages): `navPay` en "Tabu Extracts"; `navArticles` en "Daily Brief"; `navCta` fr "Rendez-vous"
- Burger breakpoint raised 1100 → 1240px (long RU/FR navs).

No other dictionary values touched. No keys added/renamed/removed.

## 4. Typography

Same five font families (Google Fonts link untouched except nothing — weights kept). Lora/Frank Ruhl for display at weight 500, italic champagne for Latin `em`; Inter Tight/Heebo for UI. Latin small-caps eyebrows at .3em tracking; Hebrew keeps normal case/.14em per existing `html[lang="he"]` override pattern (extended to every new small-caps element). Oldstyle/tabular numerals via `font-variant-numeric` for prices, stamps, phone.

## 5. scripts/build-articles.js

Template CSS/markup restyled to the same system: livery line, night header with ringed monogram, serif lead with brass side-rule + double-rule divider (`.lead-rule` added), framed CTA card on paper, night-950 footer. Build logic, SLUGS, sitemap generation untouched.

## 6. Things the principal should know

- The two protected legacy colors that remain: WhatsApp deep green `#0E4A38` only in the mobile bar cell; everything else is on-palette.
- The favicon still carries the old `#0E141E/#C6A75E` — visually compatible with the new scheme; left untouched per constraint 5.
- Hero/story/contact pinstripes are 3–4% alpha brass; if they moiré on some screens, delete the `repeating-linear-gradient` lines in `.hero::before`, `#story::before`, `#contact::before`.
- `legal.html` was out of scope and still carries the old look.
- Screenshots (desktop 1280×900 / mobile 390×844 × he/en + article page) in `/home/claude/berg-shots/`.

## 7. Verification (final run — see report)

- Language switch he→en→ru→fr→he: no console errors, dir flips correctly.
- `renderArticles`: 3 cards render from `content/articles.json` with `_todayEnd` date gating.
- Wizard: doc select → fields → step II summary advances; roman plates update.
- Contact form fields + placeholders render in all languages.
- `node scripts/build-articles.js` builds 8 pages + sitemap without error.
