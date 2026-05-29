# Legacy → Canonical boilerplate migration map

> **✅ Status (2026-05-29): COMPLETE.** All 29 legacy templates (`09-37.tpl.html`) have
> been migrated to the canonical `_pptx-slide.css` system. All 37 boilerplate slides now
> build (`node build.mjs` 37/37) and pass `unzip -t`. This document is retained as the
> reference for the conventions used, and for any future template added to the set.

> theme-init boilerplate templates `09-37.tpl.html` were imported verbatim from an
> earlier jangpm slide set, which depended on a legacy `_slide.css` design system that
> **does not exist inside a preset folder**. They link a dead stylesheet and use
> `var(--*)` / rem / `<hr>` / `<span>`-badges — so they render unstyled (collapse
> to top-left) and are not html2pptx-safe.
>
> This document is the SSOT for converting them to the **canonical** system used by
> `01-08.tpl.html`: helper classes from `_pptx-slide.css` + `{{TOKEN:...}}` color
> placeholders + absolute pt positioning. Every migrated template must build via
> `node build.mjs` and pass `unzip -t`.

## Target idiom (copy 01-08 exactly)

```html
<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>NN Name</title>
<link rel="stylesheet" href="../_pptx-slide.css"></head>
<body>

<!-- HEADER (chrome) -->
<div style="position:absolute; top:42pt; left:56pt; right:56pt;">
  <div class="row between" style="align-items: flex-end;">
    <div>
      <p class="t-cap-up" style="margin-bottom: 6pt;">NN · SECTION</p>
      <h2 class="t-h2">슬라이드 타이틀 <span class="c-accent">키워드</span></h2>
    </div>
    <p class="t-cap c-tertiary">NN / 41</p>
  </div>
  <div class="rule" style="margin-top: 14pt;"></div>
</div>

<!-- BODY (absolute block, top ~156pt) -->
<div style="position: absolute; top: 156pt; left: 56pt; right: 56pt;">
  ...helper-class content...
</div>

<!-- GM band (optional) -->
<div class="gm-band">
  <p class="t-body c-secondary" style="font-weight: 700;">so-what 한 줄.</p>
</div>

</body></html>
```

**Hard rules (non-negotiable):**
- **No** `<link ... _slide.css>`. Only `../_pptx-slide.css`.
- **No** `<style>` blocks. **No** `<section class="slide">`. **No** `var(--*)`. **No** rem. **No** `<hr>`. **No** CSS `@keyframes`/`animation`.
- Text only in `<p>`/`<h1-6>`. Never raw text in a `<div>`/`<span>` wrapper that carries a background.
- Background/border/radius go on a wrapping `<div>` — never on `<p>`/`<h*>`.
- Colors: helper class (`.c-accent`, `.bg-accent`, `.card-accent`…) where one exists; otherwise inline `{{TOKEN:colors.NAME}}` literal. Keep `rgba({{TOKEN:colors.accent|rgb}}, 0.06)` for tints.
- Positions/sizes in **pt**. Bottom-most content ≤ 496pt (≥44pt safe margin).
- Preserve all `{{TOKEN:...}}` placeholders already present.

## Class / construct map

| Legacy | Canonical |
|---|---|
| `<section class="slide">…</section>` | drop wrapper; absolute-positioned `<div>` blocks |
| `.flex-row justify-between items-center` | `class="row between center"` |
| `.flex-col` / `.flex-row` | `.col` / `.row` (+ `.gap-N`) |
| `.label-caption` | `.t-cap-up` |
| `.caption` (page counter) | `.t-cap c-tertiary` |
| `.caption` (body caption) | `.t-cap c-secondary` |
| `.headline` (slide title) | `<h2 class="t-h2">` |
| `.display` / giant `<div style="font-size:5-7rem">` | `<h1 class="t-display">` (hero) |
| `.gm` | `<div class="gm-band"><p class="t-body c-secondary" style="font-weight:700;">…</p></div>` |
| `.number-badge` / `.num` circle | `<div class="number-circle"><p class="t-cap c-white" style="line-height:22pt;font-weight:800;">N</p></div>` |
| `<hr class="rule">` / `.tp-rule` | `<div class="rule"></div>` (or `.rule-accent`) |
| `.grid-3` / `.grid-2` … | same names exist (`.grid-2..6`) ✓ |
| `.tp-card` / `.fp-card` / generic card | `.card` (default) · `.card-accent` (1 hero) · `.card-alt` (grouped) |
| `.tp-title`/`.fp-title`/`.sp-title`/`.proc-title` (1.4rem 700) | `<h3 class="t-h3">` |
| `.tp-body`/body paragraph | `<p class="t-body c-secondary">` |
| `.tp-caption` | `<p class="t-cap c-secondary">` |
| `.tp-head` (badge+label row) | `<div class="row center gap-3">` |
| `.accent-badge` / pill `<span>` | `<div class="badge-accent-soft"><p class="t-cap-up c-accent">…</p></div>` |
| inline `style="color: var(--accent)"` | `class="c-accent"` or `style="color: {{TOKEN:colors.accent}}"` |
| `var(--surface)` | `{{TOKEN:colors.surface}}` (or use `.card`) |
| `var(--accent-soft)` | `{{TOKEN:colors.accent-soft}}` (or `.card-accent`) |
| `var(--text)` / `--text-secondary` / `--text-tertiary` | `.c-text` / `.c-secondary` / `.c-tertiary` |
| `var(--border)` | `{{TOKEN:colors.border}}` |
| `var(--card-radius)` | `12pt` |
| `var(--space-3/4/5/6)` | `12pt / 16pt / 20pt / 24pt` |

### Type scale (rem → canonical pt class)
| Legacy rem | Class | pt |
|---|---|---|
| ~5–7rem (hero) | `.t-display` / `.t-display2` | 42 / 36 |
| ~2.3rem (title) | `.t-h2` | 24 |
| ~1.8–2rem | `.t-h1` / `.t-h2` | 30 / 24 |
| ~1.35–1.4rem | `.t-h3` | 18 |
| ~1.05–1.15rem | `.t-title` | 14 |
| 1rem (body) | `.t-body` | 12 |
| ~0.8–0.95rem (caption) | `.t-cap` | 9 |

## Table family (06-table idiom)
Use a CSS-grid of `<p>` cells (NOT `<table>`/`<td>`):
```html
<div style="display: grid; grid-template-columns: 2fr 1fr 1fr; background: {{TOKEN:colors.accent-soft}};">
  <p class="t-cap c-accent" style="padding: 10pt 14pt; font-weight: 700;">헤더</p> …
</div>
<div style="display: grid; grid-template-columns: 2fr 1fr 1fr; border-bottom: 1px solid {{TOKEN:colors.border}};">
  <p class="t-body" style="padding: 10pt 14pt;">셀</p> …
</div>
```
Highlight column = wrap cell in `<div style="background: rgba({{TOKEN:colors.accent|rgb}}, 0.06); padding:10pt 14pt;"><p …></p></div>`. Zebra = alt row `background: {{TOKEN:colors.bg}}`.

## Terminal family (use existing `.term-*` helpers)
`_pptx-slide.css` already has `.term-window`/`.term-chrome`/`.term-dot`/`.term-body`.
- `.tm-window` → `.term-window` ; `.tm-chrome` → `.term-chrome` ; `.tm-body` → `.term-body` (`<div class="term-body">`, pad 14pt 16pt).
- chrome dots: `<span class="term-dot" style="background:#ff5f56;"></span>` (red), `#ffbd2e` (yellow), `#27c93f` (green) — inline literal hex, html2pptx-safe.
- terminal lines: each line is a `<p class="t-cap t-mono" style="color:#a8b1ba; line-height:1.6;">…</p>`. Syntax color via inline `<span style="color:#…">`. Prompt `$` green `#27c93f`, command white `#FFFFFF`, comment `{{TOKEN:colors.text-secondary}}`.
- **Drop** the blinking `.cursor` (`animation`) and `@keyframes` — replace cursor with a static `<span style="color:#27c93f;">▋</span>` or omit.
- blank line: `<p class="t-cap t-mono">&nbsp;</p>`.

## Image / exercise family (use `.ph-frame` helper)
`_pptx-slide.css` has `.ph-frame` (dashed placeholder) and `.ph-frame-accent`.
- `.im-placeholder` → `<div class="ph-frame">` with `<p class="t-title c-secondary">스크린샷 / 예시 이미지 영역</p>` + `<p class="t-cap c-secondary">1280×480 권장</p>` inside.
- Real images: `<img src="../icons/…" style="width:…; height:…; object-fit:cover;">` — never a div `background-image`.
- The `.im-index` accent bar → `<div class="strip-accent" style="height:36pt;">`.
- Icon glyphs like `▦` are geometric (not emoji) — OK to keep, or replace with a `.ph-frame` label.

## Closing / cover / section (Narrative)
- closing-light (21): light bg, `<h1 class="t-display">` message, `.btn-cta` CTA (purple), contact meta. **No dark bg.**
- closing-big (22) / closing-dark (08-style): may use `.bg-text` full bleed + `.c-white` text.
- cover (23/25): `<h1 class="t-display">`, optional `{{IF:assets.character}}<img>{{/IF}}`, meta bar. No decorative shapes.
- section (09): big `<h1 class="t-display">` number + `<h2 class="t-h2">` title + `.rule-accent`.

## Checklist (24)
- check icon: `<div class="number-circle" style="background: {{TOKEN:colors.positive}};"><p class="t-cap c-white" style="line-height:22pt;">✓</p></div>` (✓ is a dingbat, allowed) — never `margin` on an inline span.
- each row: `<div class="row center gap-3">` + icon + `<div>` with `<p class="t-title">` + `<p class="t-cap c-secondary">`.
