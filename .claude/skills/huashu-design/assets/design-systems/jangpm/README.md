# Jangpm Slide Design System

A clean, report-style design system for **Jangpm (장피엠) lecture slide decks** — Korean business-lecture presentations built around a monochrome base with a single restrained indigo accent (`#4633E3`).

The system is optimized for:
- **1280×720** fixed-ratio slides (16:9 lecture deck)
- **Korean + English** typography (Pretendard)
- **Report / evidence-first** layouts over SaaS dashboard aesthetics
- **Reveal.js** as the rendering runtime, with a defined PPTX export path

---

## Sources provided

| Source | Location in project |
|--------|---------------------|
| `CLAUDE.md` (SSOT from `lecture-slide-html` repo) | originally uploaded, absorbed into this README |
| `design-system.md` (tokens, scales, anti-slop) | `reference/design-system.md` |
| `anti-slop.md` (18 forbidden patterns) | `reference/anti-slop.md` |
| `patterns.md` (24 slide patterns) | `reference/patterns.md` |
| `skeleton.md` (HTML skeleton template) | `reference/skeleton.md` |
| `libraries.md` (Reveal/Chart/Mermaid/Lucide) | `reference/libraries.md` |
| `visual-assets.md` (illustrations / screenshots) | `reference/visual-assets.md` |
| `export.md` (PPTX/PDF/Drive export) | `reference/export.md` |
| Pretendard font family (9 OTF + variable TTF) | `fonts/` |
| 장피엠 저자 캐릭터 (author illustration) | `assets/jangpm-character.png` |
| `reference 2.pptx` — target visual reference (Korean business-report deck) | extracted sample content informed slide designs |

> The `강의 슬라이드 예시_AI 성과를 극대화하는 메타적인 접근법.pptx` file was listed in the upload manifest but did not appear in the uploaded directory. See **Caveats** at the end.

---

## Index / Manifest

- `README.md` — this file
- `SKILL.md` — Agent Skill entrypoint (Claude Code compatible)
- `colors_and_type.css` — core CSS variables + typography classes
- `fonts/` — Pretendard 9 weights + variable
- `assets/` — brand imagery (author character, visual assets)
- `reference/` — upstream markdown references (tokens, patterns, skeleton, libraries, anti-slop)
- `preview/` — small HTML cards that populate the Design System review tab
- `slides/` — sample slide types reproducing `reference 2` style
- `ui_kits/slide-deck/` — the lecture-deck "UI kit" (components + interactive index)

---

## CONTENT FUNDAMENTALS

Jangpm decks are **Korean-first lecture slides**, typically delivered as structured business / educational reports. Copywriting tone:

- **Language:** Korean primary (한국어), occasional English terms kept in English (e.g., "LTV", "ROI", "D2C", "KPI").
- **Voice:** Declarative, analytical, third-person institutional. No "you/I" direct-address. Prefer noun phrases and verb endings like `~입니다`, `~합니다`, `~해야 합니다`.
- **Casing:** Korean uses no casing; for English tokens, use **Title Case** for proper nouns and **lowercase** for generic tech terms (`chart`, `metric`).
- **Titles:** Fragmentary, noun-led, no trailing period.
  - ✅ `2030년 한눈에 보기`, `시장 및 트렌드 전망`, `수익성 및 비용구조`
  - ❌ `2030년 한눈에 보겠습니다.`
- **Subtitles / body:** Full sentences with Korean polite endings. Max ~4 lines per block.
- **Emoji:** **Never.** The system explicitly forbids emoji — iconography is SVG line-art only.
- **Data vocabulary:** Numbers always carry a unit + optional delta.
  - ✅ `58억 원 (+21% vs 전년)`, `재고 회전율 5.5회`, `경고 기준 60점 이하`
- **Governing Message (`.gm`):** Every content slide ends with a one-line editorial takeaway at the bottom — the "so-what" statement, 문장형, 1줄 ideal.

### Copy examples (from `reference 2.pptx`)

| Slide | Title | GM-style line |
|-------|-------|---------------|
| 2 | `2030년 한눈에 보기` | "안정적 매출 유지, 수익성 개선 및 확장 단계" |
| 4 | `시장 및 트렌드 전망` | "덜 사고, 더 따진다 / 온라인 증가, 오프라인 감소 / 감(感) → 데이터" |
| 5 | `2030년 매출 예측` | "월 평균 매출 4억 → 4.8억" |
| 9 | `성과 측정 지표` | "목표 미달 시 즉각 원인 분석과 적절한 개선 조치" |

---

## VISUAL FOUNDATIONS

### Colors
- **Base palette is achromatic.** Warm off-white `#FAFAF9` background, near-black `#1A1A1A` text, neutral grays for borders and secondary text.
- **One accent: `#4633E3` (indigo-violet).** Used ≤ 1–2 times per slide — a headline emphasis, a highlighted table column, a single badge. Accent-soft `#E8E5FC` fills accent pill backgrounds and recommended columns.
- **Semantic colors (positive `#059669`, negative `#E11D48`, warning `#D97706`) are for data meaning only** — never decorative.
- **Charts** use a single accent with opacity ladders (`0.85 / 0.6 / 0.4 / 0.25`), never rainbow.

### Typography
- **Pretendard** (9 weights) — a Korean/Latin hybrid similar in feel to Inter but tuned for Hangul. Variable font also shipped.
- Strong weight contrast: Display 800, Headline 700, Title 600, Body 400.
- Tight tracking on large type: `-0.03em` on Display, `-0.02em` on Headline.
- Line-heights: Display 1.08, Headline 1.2, Title 1.3, Body 1.6, Caption 1.4.

### Spacing
- Strict **8 px grid** (`--space-1` = 4 px … `--space-16` = 64 px).
- Slide padding: `3.5rem` sides, `4rem` bottom (reserve for GM).
- Card padding & inter-card gap: `1.5rem` (`--space-6`).

### Backgrounds
- **Solid warm off-white only.** No gradients, no orbs, no textures.
- Title + section dividers may use a subtle dot pattern via `--bg-dots` (optional, not used in `reference 2`).
- No full-bleed imagery on content slides.

### Imagery
- Monochrome / muted; flat illustration style; transparent PNG when possible.
- The author character (`assets/jangpm-character.png`) is the canonical brand illustration — warm peach skin, dark gray vest, round glasses, line-art style.
- Stock / generated illustrations follow the same "minimal, flat, clean, pastel/muted, transparent background" prompt recipe (see `reference/visual-assets.md`).

### Iconography
- **Lucide-style SVG line-art, stroke `currentColor`, 2 px weight.** `.icon` = 20 px, `.icon-lg` = 32 px, `.icon-xl` = 48 px.
- **Bare icons only** — no circle wrappers, no colored icon badges, no icon backgrounds.
- No emoji, no unicode glyphs as icons.
- Common glyphs enumerated in `reference/libraries.md` (arrow-right, check-circle, zap, brain, users, trending-up, etc.).

### Corner radii
- Cards: **`12 px` (`--radius-lg`)**.
- Small chips / badges: `4–6 px`.
- Pills (accent badges, number circles): fully rounded.

### Borders
- Always `1px solid var(--border)` (`#E5E7EB`).
- **No decorative partial borders** (no colored left-strip cards). Borders are structural, not ornamental.
- Accent-emphasis columns use full `accent-soft` fill, not a colored border.

### Shadows
- Used **sparingly** on cards with data/KPI emphasis.
- 3-step system: `--shadow-sm` / `--shadow-md` / `--shadow-lg`. Default card has **no shadow** and relies on border.

### Animation & motion
- **None on content.** `transition: 'none'` in Reveal.js. No hover scale, no translateY, no pulse, no float, no glow.
- Chart.js animation is disabled globally (`Chart.defaults.animation = false`).

### Hover / press states
- Slides are not interactive — no hover states inside decks.
- For UI kit prototypes, hover = subtle `--shadow-md` change only. No transform.

### Transparency / blur
- **Not used.** Keep opacity at 1 and let structure carry the design.
- Exception: disabled/past `.agenda-item` uses `opacity: 0.5`.

### Layout rules
- Title at top (`.headline`) + `.slide-body` fills middle + `.gm` absolutely positioned at bottom.
- Use **CSS Grid `gap`** for all multi-element layouts. Never margin hacks.
- Cards are a *secondary* tool — text blocks + rule lines are the primary report-style layout.
- Max 1–2 accent events per slide. Slide must work in grayscale first.
- Max 4–5 bullets / 3–4 cards per slide. Dense interiors forbidden.

---

## ICONOGRAPHY

Jangpm uses **Lucide-style inline SVG** line-art icons drawn at 24×24 viewBox with `stroke="currentColor"`, `stroke-width="2"`, `stroke-linecap="round"`, `stroke-linejoin="round"`. Icons always inherit text color; there are no colored icon backgrounds, no circle wrappers, no filled badges.

- **No emoji, ever.** The system forbids decorative emoji across all patterns.
- **No unicode pseudo-icons** (no `→`, `✓`, `★` as standalone marks — use the SVG equivalents).
- **No raster icons** (no PNG sprites).
- **Inline, not CDN.** Canonical glyph paths live in `reference/libraries.md`; the `preview/` + `slides/` files embed them directly.
- **Sizes:** `.icon` = 20 px, `.icon-lg` = 32 px, `.icon-xl` = 48 px.

Brand images:
- `assets/jangpm-character.png` — author/lecturer character (1024×1024, transparent)

For slide illustrations beyond the character, the system follows the nanobanana2 generator prompts in `reference/visual-assets.md`: "minimal flat illustration", "transparent background", "muted / pastel tones".

---

## Caveats / what's missing

- The example deck **`강의 슬라이드 예시_AI 성과를 극대화하는 메타적인 접근법.pptx`** listed in the upload manifest did not appear in the uploads folder — only `reference 2.pptx` was present. Slide samples draw from `reference 2` only.
- No logo / wordmark was provided — only the author character illustration. A dedicated brand logo is absent from the system.
- The upstream project (`lecture-slide-html`) points to skills (`/slide`, `/export-pptx`, etc.); those skills are **documented** here as references but not packaged — they live in the originating codebase.
