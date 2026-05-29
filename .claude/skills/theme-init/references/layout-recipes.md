# Layout Recipes — html2pptx-safe brand recomposition

> theme-init **Phase 2 (Layout Authoring)** reference. This is the recipe book the
> agent composes from when recomposing a preset's **identity slides** (cover /
> section / closing / feature-board / hero-impact / summary / agenda) into brand
> layouts. Data slides keep their token-rendered tone — do not touch them.
>
> Everything here is **html2pptx-safe**: solid fills only (no gradients), helper
> classes from `_pptx-slide.css` + literal hex only, text in `<p>/<h*>`, no inline
> `<svg>`, no `background-image`. A composed slide that violates these will fail
> `node build.mjs` or `unzip -t` — the Phase 2 completion gate.

---

## 0. Non-negotiable locks (every composed slide)

- **960pt × 540pt** canvas (`<body>` fixed). One slide = one HTML file.
- **4 hard constraint** (`slide/references/4-constraints.md`):
  - text only inside `<p>`/`<h*>` — no raw text in a `<div>`
  - no `background`/`border`/`box-shadow` on `<p>`/`<h*>` — put it on the wrapping `<div>`
  - no `background-image` on a div — use an `<img>` tag
  - no inline `<svg>` — external `.svg` in `icons/` (build's `prebuildSvg` rasterizes it)
  - bottom-edge safe margin ≥ 44pt
  - no `margin` on an inline `<span>` — use `&nbsp;`
- **single accent principle** — the preset's one accent; no multi-hue, no glow.
- **no gradients** — a navy hero band is `background: #1A1A2E` (solid literal hex), never `linear-gradient(...)`.
- **editable text** — every word stays in `<p>/<span>`; never flatten copy into an `<img>`.
- **no emoji** — icons are external line-art SVG only.

## 1. Coordinate grid (960 × 540pt)

| edge | value |
|---|---|
| content left / right margin | `56pt` (chrome), `42pt` (`.pad`) |
| top eyebrow / page counter | `top: 42pt` |
| divider rule | `top: 64pt` |
| slide title | `top: 88pt` |
| body start | `~120pt` |
| bottom safe margin | content bottom ≤ `496pt` (≥ 44pt from 540) |

Compose with absolute-positioned `<div>` blocks (`position: absolute; top/left/width`)
exactly like the stock boilerplate — read the matching `.stock/<stem>.html` first to
copy the chrome skeleton, then rebuild the body.

## 2. Helper catalog (from `_pptx-slide.css`)

### 2.1 Existing structural helpers (all presets)

| helper | shape | typical use |
|---|---|---|
| `.pad` / `.pad-wide` | full-canvas padded wrapper | page frame |
| `.card` / `.card-accent` / `.card-alt` / `.card-dark` | rounded container | content blocks |
| `.badge-accent` / `.badge-accent-soft` / `.badge-dark` / `.badge-square` | pill / square chip | eyebrows, tags |
| `.number-circle` / `.number-circle-lg` | round counter | steps, lists |
| `.rule` / `.rule-accent` | divider lines | chrome, separators |
| `.strip-accent` | 3pt vertical accent bar | left-edge emphasis |
| `.row` / `.col` / `.between` / `.center` / `.gap-N` | flex layout | composition |
| `.grid-2..6` | CSS grid | card boards |
| `.t-display` … `.t-cap-up` | type scale (pt) | all text |
| `.c-accent` / `.c-white` / `.c-secondary` … | text color | emphasis |
| `.bg-accent` / `.bg-accent-soft` / `.bg-surface-alt` / `.bg-text` | solid fills | bands, cards |

### 2.2 Phase-2 brand helpers (new — shape only, color via token default or inline hex)

| helper | shape | color model |
|---|---|---|
| `.hero-band` | full-width top band (`left:0;right:0;top:0;height:220pt`) | default `--text`; override `background:<hex>` inline (e.g. brand navy) + adjust `height`/`top` inline |
| `.band-full` | bare full-width band (set `top`/`height`/`background` inline) | inline |
| `.banner-strip` | inline rounded strip | set `background:<hex>` inline (e.g. yellow-bold banner); text `<p>` inside |
| `.dot-row` | flex row of dots | layout only |
| `.spectrum-dot` / `.spectrum-dot-sm` | 10pt / 7pt round dot | set each `background:<hex>` inline → brand spectrum |
| `.btn-cta` / `.btn-cta-sq` | pill / squared button | accent fill default; `<p class="c-white">` label inside |
| `.btn-outline` | outlined button | accent border + surface fill |
| `.feature-tile` / `.feature-tile-accent` | feature-board card (surface-alt / accent-soft) | token default |
| `.chip` | eyebrow pill on a band | set `background`/text color inline when on a dark band |

**Rule of thumb:** a helper carries the *shape* (radius, padding, position); the
*color* comes from a token-default helper (`.bg-accent`, `.c-accent`) when it
matches the accent, or from an **inline literal hex** when the brand needs a hue
that isn't in the token set (navy band, yellow banner, spectrum dots). Inline hex
on a `<div>` is allowed; inline hex on a `<p>`/`<h*>` background is not (4-constraint).

If a brand needs a structural primitive not above, add it to
`templates/_pptx-slide.tpl.css` (shape-only, token/inline color), regenerate the
preset CSS, and document it here.

## 3. Per-family composition recipes

Each recipe: read the anchor `.stock` file → keep what the brand keeps → rebuild the body.

### cover (`01-title`, `23-cover-with-character`, `25-cover-vertical`)
Brand's front door. Common devices: full-width hero band (`.hero-band` + inline brand
hex), oversized `.t-display` wordmark, eyebrow `.chip` on the band, a `.dot-row` of
`.spectrum-dot`s, bottom meta bar. Character image (if `assets.character`) via `<img>`.

### section (`09-section`, `07-quote-section`)
Chapter break. Devices: big `.t-display` chapter number + `.t-h2` title, optional band
or `.strip-accent`, one accent keyword inline. Keep it sparse.

### closing (`21-closing-light`, and per-preset `22`/`08` if allowed)
Last slide. Devices: big message `.t-display`, a `.btn-cta` call-to-action, contact /
next-action meta. Respect the preset's light/dark closing policy in DESIGN.md.

### feature-board (`02-overview`, `26-overview-split`, `12-four-point`)
The signature "what we offer" grid. Devices: `.grid-2/3/4` of `.feature-tile`
(pastel/surface) with one `.feature-tile-accent` hero, eyebrow per tile, optional
`.banner-strip` header. One accent tile max per board.

**Density — fill the canvas.** A single short row of tiles leaves the bottom ~40% empty
(the cardinal feature-board failure). Make the board occupy the body band: either give the
tile row real height (`top:178pt; bottom:56pt` on the wrapper + tiles that grow), add a
second row (e.g. 3 tiles + a full-width summary `.feature-tile` below), or pair the grid
with a left intro column. Each tile should carry a title **and** 1-2 lines of body so it
reads as content, not a label. If you can only fill the top third, the layout is wrong —
switch to a denser vocabulary or add supporting content.

### hero-impact (`16-stats`, `18-quote-attribution`)
The 120% slide. Devices: one mega number (`.t-display` 80–120pt) or mega quote, minimal
chrome, one accent event.

### summary (`17-summary`) / agenda (`10-agenda`)
Recap / table of contents. Devices: `.number-circle` list, `.grid-N` of short cards,
one accent item = "you are here" / key takeaway.

## 4. Worked example — Notion preset

Signature devices extracted from a Notion brand deck (the hand-made reference blueprint):
navy hero band, brand-spectrum dots, pastel feature board with a yellow-bold banner,
purple CTA button.

**cover** — navy hero band + wordmark + spectrum dots:
```html
<div class="hero-band" style="height: 300pt; background: #1F2544;"></div>
<div style="position: absolute; top: 120pt; left: 56pt; width: 560pt;">
  <div class="chip" style="background: rgba(255,255,255,0.14); margin-bottom: 16pt;">
    <p class="t-cap-up c-white">PRODUCT OVERVIEW · 2026</p>
  </div>
  <h1 class="t-display c-white" style="margin-bottom: 10pt;">Notion</h1>
  <h1 class="t-display" style="color: #C9C2FF; margin-bottom: 22pt;">하나의 워크스페이스</h1>
  <div class="dot-row">
    <span class="spectrum-dot" style="background: #F2C94C;"></span>
    <span class="spectrum-dot" style="background: #6FCF97;"></span>
    <span class="spectrum-dot" style="background: #56CCF2;"></span>
    <span class="spectrum-dot" style="background: #BB6BD9;"></span>
  </div>
</div>
```

**feature-board** — pastel tiles + yellow-bold banner + one accent tile:
```html
<div class="banner-strip" style="background: #F2C94C; margin-bottom: 18pt;">
  <p class="t-cap-up" style="color: #1F2544;">왜 Notion인가</p>
</div>
<div class="grid-3">
  <div class="feature-tile"><h3 class="t-h3">문서</h3><p class="t-body c-secondary">...</p></div>
  <div class="feature-tile"><h3 class="t-h3">위키</h3><p class="t-body c-secondary">...</p></div>
  <div class="feature-tile-accent"><h3 class="t-h3 c-accent-ink">프로젝트</h3><p class="t-body">...</p></div>
</div>
```

**closing** — purple CTA button:
```html
<div class="btn-cta" style="margin-top: 22pt;">
  <p class="t-title c-white">지금 시작하기</p>
</div>
```

All fills above are solid (literal hex or token helper) — no gradient — so they survive
`html2pptx` into editable PPTX shapes with the text intact.

## 5. Self-check before `confirm`

1. `author_layouts.py validate` → lint + `node build.mjs` + `unzip -t` all PASS.
2. Each identity slide: chrome skeleton copied from `.stock`, body recomposed, one accent event.
3. No gradient / inline svg / background-image / emoji (lint catches these).
4. `author_layouts.py thumbs` → before/after shown to the user → feedback applied.
5. Data slides untouched (`git diff` on `pptx-boilerplate/` touches only identity stems).
