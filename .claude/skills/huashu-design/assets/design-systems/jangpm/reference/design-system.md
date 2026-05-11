# Design System Reference

## Design Tone
미니멀 모던 (Notion/Linear/Vercel 참조)
- Generous whitespace, restrained color (single accent), clear typographic hierarchy
- Forbidden: excessive decoration, icon spam, dense card interiors
- **Single accent color** — `#4633e3` only; all other colors must be achromatic (black/gray/white)
- **Visually full slides** — use visual elements (icons, cards, diagrams, charts) to fill vertical space; never add more text to fill space
- **No text-only slides** — even quote/hero patterns require at least one visual element alongside the text
- **High content density** — slides should feel informationally rich, not sparse. Prefer 2 visual elements per slide over 1. Add supporting context (subtitle, benchmark comparison, trend annotation) alongside primary visuals. Stats cards should include context lines (e.g., "vs industry avg 3.2%"). Chart slides can pair with a compact callout or key takeaway card.
- **Card differentiation rule** — In any card grid, at least one card should be visually distinct (accent-soft background or highlighted metric). Equal-weight cards are a design smell.
- **Density minimum** — Every card should contain at least 3 content layers (e.g., icon/badge + title + body + caption/metric). Two-layer cards (icon + title only) look unfinished.
- **Icon badges preferred, number badges for steps** — Default to SVG icon badges for card grids. Use `.number-badge` (01–04) only when sequential order is the primary information (numbered steps, ranked priorities). Mix icons and numbers when appropriate — icons are more visually interesting.
- **Charts use single accent with opacity** — `rgba(70,51,227,0.85/0.6/0.4/0.25)`; never multiple distinct hues
- **Semantic colors in data contexts** — Use `--positive` (green), `--negative` (red), `--warning` (amber) to encode meaning in trend indicators, metric badges, and chart colors. Example: churn rate trend arrow uses `color: var(--negative)`, growth metric badge uses `color: var(--positive)`
- **Chart container height** — Use `height: 400px` (not 320px) for single-chart slides to fill vertical space properly
- **Comparison tables need a winner** — Always highlight one column with `col-recommended` class (accent-soft background). Equal-weight columns are a design smell. Add subtitle/stat in column headers for density. Use check/x SVG icons for binary features. Include a verdict/summary bottom row.
- **Bare line icons only** — Use bare SVG line icons (`icon-lg` class) without any circle wrapper or background. Icons should be simple, monochrome line art that lets typography and layout carry the visual weight.
- **Bento-grid visual hierarchy** — The `bento-span-2` (hero) card uses `background: var(--accent-soft); border: 1px solid var(--accent)`. Other cards use `background: var(--surface-alt)` for subtle differentiation. No colored left-borders.
- **Concept-cards differentiation** — Differentiate cards through content hierarchy (number-badge or icon + title + body + caption), not through color coding. Use `var(--surface-alt)` background for all cards. The accent card (primary concept) may use `var(--accent-soft)` background for emphasis.
- **Label captions as taxonomy markers** — When a caption serves as a category label (e.g., "Foundation", "Growth", "Enterprise"), use `text-transform: uppercase; letter-spacing: 0.05em` for a polished SaaS feel. This applies to: card category captions, agenda item subtitles, and comparison header subtitles. Regular captions (metrics, descriptions) remain sentence-case.
- **Agenda pattern polish** — Agenda items use number-badges (not plain text numbers), each item includes a subtitle caption + right-aligned duration annotation. Current item has accent left-border + accent-soft bg. The card wrapper uses `padding: 0; overflow: hidden` so items control their own internal spacing with consistent bottom borders.

## Color Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#FAFAF9` | Body background (warm off-white) |
| `--surface` | `#FFFFFF` | Card/container background |
| `--text` | `#1a1a1a` | Main text (never pure `#000`) |
| `--text-secondary` | `#6b7280` | Secondary text |
| `--accent` | `#4633e3` | Primary accent (indigo-violet) |
| `--accent-soft` | `#e8e5fc` | Accent background |
| `--border` | `#e5e7eb` | Default border |

## Semantic Colors

| Token | Value | Use Case |
|-------|-------|----------|
| `--positive` | `#059669` | Success, growth, positive metrics |
| `--positive-soft` | `#ecfdf5` | Light green background for trend badges, table cell highlights |
| `--negative` | `#e11d48` | Error, decline, negative metrics. **Also use for trend indicators on negative-direction metrics** (e.g., churn increase = `trend-negative` even if the number has a `+` sign) |
| `--negative-soft` | `#fff1f2` | Light red background for trend badges, table cell highlights |
| `--warning` | `#d97706` | Caution, attention needed |
| `--warning-soft` | `#fffbeb` | Light amber background for trend badges, table cell highlights |

> **Semantic colors are used ONLY in data contexts:** trend indicators, metric badges, chart colors, table cell highlights. Never as card backgrounds or border decorations.

## Typography Scale

| Level | CSS Var | Size | Weight | Use Case |
|-------|---------|------|--------|----------|
| Display | `--fs-display` / `--fw-display` | 3.5rem (56px) | 800 | Title slide large text |
| Headline | `--fs-headline` / `--fw-headline` | 2rem (32px) | 700 | Content slide titles |
| Title | `--fs-title` / `--fw-title` | 1.15rem (18.4px) | 600 | Card titles, subtitles |
| Body | `--fs-body` / `--fw-body` | 0.95rem (15.2px) | 400 | Body text |
| Caption | `--fs-caption` / `--fw-caption` | 0.75rem (12px) | 500 | Labels, annotations |

Additional typography rules:
- `letter-spacing: -0.03em` for Display, `-0.02em` for Headline
- `line-height: 1.08` for Display, `1.2` for Headline, `1.3` for Title, `1.6` for Body, `1.4` for Caption

## Spacing System

8px grid system. All spacing uses CSS custom properties:

| Token | Value |
|-------|-------|
| `--space-1` | 0.25rem (4px) |
| `--space-2` | 0.5rem (8px) |
| `--space-3` | 0.75rem (12px) |
| `--space-4` | 1rem (16px) |
| `--space-5` | 1.25rem (20px) |
| `--space-6` | 1.5rem (24px) |
| `--space-8` | 2rem (32px) |
| `--space-10` | 2.5rem (40px) |
| `--space-12` | 3rem (48px) |
| `--space-14` | 3.5rem (56px) |
| `--space-16` | 4rem (64px) |

Key spacing values:
- Slide padding: `var(--space-14)` = 3.5rem (56px); bottom padding `var(--space-16)` = 4rem (64px) to reserve GM space
- Card padding: `var(--card-padding)` = `var(--space-6)` = 1.5rem (24px)
- Card gap: `var(--card-gap)` = `var(--space-6)` = 1.5rem (24px)

## Slide Layout

- Title/section/closing slides: add `.slide-centered` class for `justify-content: center`
- Content slides: title (`<h2 class="headline">`) stays at top, body content wrapped in `<div class="slide-body">` which fills remaining space from the top
- **CRITICAL: Content slides MUST use `<div class="slide-body">` wrapper** — NOT `<div class="flex-col gap-6">`. The `.slide-body` class has `flex: 1; justify-content: flex-start; padding-top: var(--space-4);` which places content immediately below the headline, maximizing fill rate.
- Structure for content slides: `<section> → <h2 class="headline"> + <div class="slide-body"> (content fills from top) + <div class="gm"> (absolutely positioned bottom)`
- GM is absolutely positioned at the bottom; do NOT add `position: relative` to section (Reveal.js's own positioning serves as context)
- Must add `.reveal .slides > section.present { display: flex !important; }` to override Reveal.js's `display: block`
- `.accent-badge` uses `padding: var(--space-2) var(--space-4)` and `font-size: var(--fs-body)` — NOT caption size
- `.display` class is reserved for title slides, section dividers, and closing slides only
- Body content slides should use `.headline` (2rem) for emphasized text, never `.display` (3.5rem)

## Card System

| Property | Value |
|----------|-------|
| `--card-padding` | `var(--space-6)` |
| `--card-gap` | `var(--space-6)` |
| `--card-radius` | `0.75rem` (12px) |
| Background | `var(--surface)` or `var(--surface-alt)` |
| Border | `1px solid var(--border)` |

## Calibration Anchors

| Score | Reference |
|-------|-----------|
| 10점 | Notion/Linear quality — generous whitespace, minimal color, clear hierarchy |
| 8점 | Clean SaaS intro page — well-organized but less refined |
| 6점 | Generic Bootstrap template — functional but generic |
