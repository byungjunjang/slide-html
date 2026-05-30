---
name: diagram-design
description: Create technical and product diagrams — architecture, flowchart, sequence, state machine, ER / data model, timeline, swimlane, quadrant, nested, tree, org chart, layer stack, venn, pyramid — as HTML with inline SVG. Use whenever a slide or doc needs a structural-relationship visual (시스템 구성도/아키텍처/플로우차트/순서도/시퀀스/상태도/ER/타임라인/스윔레인/사분면/트리/조직도/계층도/벤다이어그램/피라미드·퍼널). Inside the slide-html PPTX pipeline this is the canonical diagram author — it emits a diagram-only HTML that gets rendered to a PNG <img> slot and skinned to the active /slide preset (see §0.5). Standalone, ships a neutral editorial skin + annotation-callout and sketchy primitives.
license: MIT
metadata:
  version: "1.0"
---

# Diagram Design

Create visual diagrams as self-contained HTML files with inline SVG and CSS, following an opinionated editorial design system.

Fourteen diagram types. One shared design system, complexity budget, and taste gate. Type-specific conventions live in `references/` and are loaded only when you pick a type.

---

## 0.5 slide-html 안에서 실행될 때 (이 리포 전용 — 필독, 최우선)

이 스킬은 `slide-html`(editable PPTX 빌더)에 통합돼 있다. **`/slide` 파이프라인 안에서, 또는 이 리포의 데크(`output/<project>-pptx/`)에 다이어그램을 넣으려고** 호출됐다면, 아래가 §0~§11보다 우선한다:

- **온보딩/first-run 게이트(§0)를 건너뛴다.** 브랜드는 이미 정해져 있다 — 활성 프리셋(`../slide/assets/design-systems/active.json`, `/slide` Step 0가 선언)이 곧 스킨이다. `style-guide.md`를 웹사이트에서 새로 굽지 않는다.
- **색·폰트를 hex로 쓰지 않는다.** 데크의 `design-system/colors_and_type.css`를 `<link>` 하고, SVG에서 `style="fill:var(--accent)"` 식으로 **프리셋 CSS 변수만** 참조한다(렌더 시점에 활성 프리셋 값으로 해석). 의미역→변수 매핑표는 통합 계약 문서에 있다.
- **산출물은 standalone 에디토리얼 페이지가 아니라 "다이어그램만 든 HTML"** 이다(슬라이드 제목/카드/푸터 chrome 금지, 전체 paper 배경 사각형 금지=투명). 그 HTML을 Playwright로 **PNG로 렌더해 `<img>` 슬롯**으로 슬라이드에 임베드한다 — inline `<svg>`는 html2pptx가 버리기 때문(편집 가능한 도형으로 안 들어감).
- **영구 락 준수**: 단일 액센트(focal ≤2) · 이모지 금지 · 그라디언트/글로우 금지. diagram-design 자체 그라마(복잡도 예산·4px 그리드·박스 전 화살표·라벨 마스킹·하단 legend strip·그림자 금지)도 함께.

> **단일 진입점 — 전체 계약·단계·매핑표·렌더 명령은 여기 한 곳:**
> [`../slide/references/diagram-slots.md`](../slide/references/diagram-slots.md)
>
> 그 문서를 먼저 Read 하고 따른다. 타입별 레이아웃 관례는 평소대로 `references/type-<name>.md`에서 가져온다.

리포 밖(일반 문서·README·블로그용 standalone 다이어그램)에서 호출됐다면 이 §0.5를 무시하고 §0부터 평소대로 진행한다.

---

## 0. First-time setup — style guide gate

> **slide-html 안에서는 이 게이트를 건너뛴다 (§0.5 참조).** 아래는 standalone 사용 시에만.

**Before generating your first diagram in a new project, verify the style guide has been customized.**

Open [`references/style-guide.md`](references/style-guide.md) and check the default tokens. If they're still the shipped defaults (paper `#faf7f2`, ink `#1c1917`, accent `#b5523a` rust), **pause and ask the user**:

> *"This is your first Schematic in this project. The style guide is still at the default (neutral stone + rust). Do you want to customize it to match your brand first? Options: (a) run onboarding — I'll pull colors and fonts from your website, (b) paste your tokens manually, (c) proceed with the default for now."*

Then branch:
- **(a)** → follow [`references/onboarding.md`](references/onboarding.md) to fetch the site, extract palette + fonts, propose a diff, and write `style-guide.md`.
- **(b)** → accept the user's tokens and write them into `style-guide.md` under a new "Custom tokens" section.
- **(c)** → proceed; optionally remind the user they can run onboarding later.

**Once the style guide has been customized** (or the user explicitly opted for default), skip this gate on subsequent runs. A simple way to detect customization: if the `accent` value in `style-guide.md` differs from `#b5523a`, assume custom.

Don't silently ship default-skinned diagrams into a branded project — that's the failure mode this gate exists to prevent.

---

## 1. Philosophy

**The highest-quality move is usually deletion.**

From `.impeccable.md`: *"Confident restraint. Earn every element. One color accent, two families, a small spacing vocabulary. If removing it wouldn't hurt the page, remove it."*

Applied to schematics:
- Every node represents a distinct idea. Two nodes that always travel together are one node.
- Every connection carries information. If the relationship is obvious from layout, remove the line.
- Coral is **editorial, not a flag.** 1–2 focal nodes per diagram. Using it on 5 nodes erases the signal.
- The schematic isn't done when everything is added. It's done when nothing can be removed.

**Target density: 4/10.** Enough to be technically complete. Not so dense it needs a guide. Above 9 nodes, it's probably two diagrams.

---

## 2. When to Use

Use for any of the 14 diagram types (§3) when a reader will learn more from a visual than from prose, a table, or a bulleted list.

**Don't use for:**
- Quick unicode diagrams → use **wiretext**.
- Lists of things → table or bullets.
- Simple before/after → table.
- One-shape "diagrams" → just write the sentence.

Before drawing, ask: *Would the reader learn more from this than from a well-written paragraph?* If no, don't draw.

---

## 3. Diagram Types

### Selection guide

| If you're showing… | Use | Reference |
|---|---|---|
| Components + connections in a system | **Architecture** | [type-architecture.md](references/type-architecture.md) |
| Decision logic with branches | **Flowchart** | [type-flowchart.md](references/type-flowchart.md) |
| Time-ordered messages between actors | **Sequence** | [type-sequence.md](references/type-sequence.md) |
| States + transitions + guards | **State machine** | [type-state.md](references/type-state.md) |
| Entities + fields + relationships | **ER / data model** | [type-er.md](references/type-er.md) |
| Events positioned in time | **Timeline** | [type-timeline.md](references/type-timeline.md) |
| Cross-functional process with handoffs | **Swimlane** | [type-swimlane.md](references/type-swimlane.md) |
| Two-axis positioning / prioritization | **Quadrant** | [type-quadrant.md](references/type-quadrant.md) |
| Hierarchy through containment / scope | **Nested** | [type-nested.md](references/type-nested.md) |
| Parent → children relationships | **Tree** | [type-tree.md](references/type-tree.md) |
| Human/agent/team ownership, reporting, routing, escalation | **Org chart** | [type-org-chart.md](references/type-org-chart.md) |
| Stacked abstraction levels | **Layer stack** | [type-layers.md](references/type-layers.md) |
| Overlap between sets | **Venn** | [type-venn.md](references/type-venn.md) |
| Ranked hierarchy or conversion drop-off | **Pyramid / funnel** | [type-pyramid.md](references/type-pyramid.md) |

Rules of thumb:
- If a 3-column table communicates the same thing, pick the table.
- If you're combining two types, pick the dominant axis — don't hybridize grammars.
- If you're past the complexity budget (§7), split into an overview + detail.

**Always load the relevant `references/type-*.md` before drawing** — it contains layout conventions, anti-patterns, and example files for that type.

---

## 4. Universal Anti-patterns

These mark "AI slop" schematics of any type:

| Anti-pattern | Why it fails |
|---|---|
| Dark mode + cyan/purple glow | Looks "technical" without design decisions |
| JetBrains Mono as blanket "dev" font | Mono is for *technical* content — ports, commands, URLs. Names go in Geist sans. |
| Identical boxes for every node | Erases hierarchy |
| Legend floating inside the diagram area | Collides with nodes |
| Arrow labels with no masking rect | Bleeds through the line |
| Vertical `writing-mode` text on arrows | Unreadable |
| 3 equal-width summary cards as default | Generic grid — vary widths |
| Shadow on any element | Shadows are out. Borders are in. |
| `rounded-2xl` on boxes | Max radius 6–10px or none |
| Coral on every "important" node | Coral is 1–2 editorial accents, not a signaling system |

Type-specific anti-patterns live in each `references/type-*.md`.

---

## 5. Design System

**The design system is skinnable.** All colors, typography, and tokens live in a single source of truth — [`references/style-guide.md`](references/style-guide.md). This file describes semantic roles (`paper`, `ink`, `muted`, `accent`, `link`, …). The default skin is a cool editorial palette (white-smoke paper, jet-black ink, atomic-tangerine accent, blue-slate muted, silver hairlines); to apply your own brand, either edit `style-guide.md` directly or run the URL-based flow described in [`references/onboarding.md`](references/onboarding.md).

> When specs below or in type references mention "ink", "accent", "muted", etc., look up the current hex value in `style-guide.md`.

### Semantic roles (at a glance)

| Role | Purpose |
|---|---|
| `paper`, `paper-2` | Page bg and container bg |
| `ink` | Primary text / stroke |
| `muted`, `soft` | Secondary text, default arrows, sublabels |
| `rule`, `rule-solid` | Hairline borders |
| `accent`, `accent-tint` | 1–2 focal elements per diagram |
| `link` | HTTP/API calls, external arrows |

**Focal rule:** `accent` goes on 1–2 elements max. Everything else is `ink` / `muted` / `soft`. If you're tempted to accent 4 things, you haven't decided what's focal yet.

### Node type → treatment

| Type | Fill | Stroke |
|---|---|---|
| **Focal** (1–2 max) | `accent-tint` | `accent` |
| **Backend / API / Step** | white | `ink` |
| **Store / State** | `ink @ 0.05` | `muted` |
| **External / Cloud** | `ink @ 0.03` | `ink @ 0.30` |
| **Input / User** | `muted @ 0.10` | `soft` |
| **Optional / Async** | `ink @ 0.02` | `ink @ 0.20` dashed `4,3` |
| **Security / Boundary** | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

### Typography (summary — full spec in style-guide.md)

- **Title** — Instrument Serif, 1.75rem, 400 — H1 only
- **Node name** — Geist (sans), 12px, 600 — human-readable labels
- **Sublabel** — Geist Mono, 9px — ports, URLs, field types
- **Eyebrow / tag** — Geist Mono, 7–8px, uppercase, tracked — type tags, axis labels
- **Arrow label** — Geist Mono, 8px — annotation on arrows
- **Editorial aside** — Instrument Serif *italic*, 14px — callouts only

**Mono is for technical content.** Names are Geist sans. Page title is Instrument Serif. Italic Instrument Serif is reserved for annotation callouts. Never JetBrains Mono as a blanket "dev" font.

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## 6. Core SVG Primitives

Universal building blocks. Type-specialized primitives (lifeline, activation bar, region) live in the relevant `references/type-*.md`. Optional primitives:
- Editorial callouts → [primitive-annotation.md](references/primitive-annotation.md)
- Hand-drawn variant → [primitive-sketchy.md](references/primitive-sketchy.md)

### Background

**Default: clean paper, no dot pattern.** Single `<rect>` filled with `paper`. Don't wrap the diagram in a secondary container background — the diagram sits directly on the page.

```svg
<rect width="100%" height="100%" fill="#f5f5f5"/>
```

**Optional: dotted paper variant.** When a long-form editorial diagram benefits from textured ground (essays, hero diagrams on a dedicated page), opt in by adding the `dots` pattern and a second rect:

```svg
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="0.9" fill="rgba(45,49,66,0.10)"/>
  </pattern>
</defs>
<rect width="100%" height="100%" fill="#f5f5f5"/>
<rect width="100%" height="100%" fill="url(#dots)" opacity="0.6"/>
```

Don't use the dot pattern when the diagram sits inside a product page, slide, or card — the texture compounds with surrounding chrome and reads as noise.

### Arrow markers (define all three, always)

```svg
<marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#4f5d75"/>
</marker>
<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#eb6c36"/>
</marker>
<marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
  <polygon points="0 0, 8 3, 0 6" fill="#2e5aa8"/>
</marker>
```

| Arrow | Stroke | When |
|---|---|---|
| Default | muted `#4f5d75` | Internal, generic |
| Accent | coral `#eb6c36` | Primary / highlighted / headline |
| Link-blue | `#2e5aa8` | HTTP/API calls, external systems |
| Dashed | `stroke-dasharray="5,4"` + any color | Optional, passive, return, async |

**Draw arrows before boxes** so z-order puts lines behind nodes.

### Node box — full pattern

```svg
<!-- 1. Opaque paper mask — prevents arrows bleeding through transparent fills -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="#f5f5f5"/>
<!-- 2. Styled box -->
<rect x="X" y="Y" width="W" height="H" rx="6" fill="FILL" stroke="STROKE" stroke-width="1"/>
<!-- 3. Rectangular type tag (rx=2, NOT a pill) -->
<rect x="X+8" y="Y+6" width="28" height="12" rx="2" fill="transparent" stroke="STROKE@0.40" stroke-width="0.8"/>
<text x="X+22" y="Y+15" fill="STROKE@0.8" font-size="7" font-family="'Geist Mono', monospace"
      text-anchor="middle" letter-spacing="0.08em">API</text>
<!-- 4. Node name (Geist sans — human-readable) -->
<text x="CX" y="CY+2" fill="#2d3142" font-size="12" font-weight="600"
      font-family="'Geist', sans-serif" text-anchor="middle">Node Name</text>
<!-- 5. Technical sublabel (Geist Mono) -->
<text x="CX" y="CY+18" fill="#4f5d75" font-size="9"
      font-family="'Geist Mono', monospace" text-anchor="middle">tech:port</text>
```

### Arrow labels — always mask

Every arrow label needs an opaque rect behind it. Without one it bleeds through the line.

```svg
<rect x="MID_X-18" y="ARROW_Y-12" width="36" height="12" rx="2" fill="#f5f5f5"/>
<text x="MID_X" y="ARROW_Y-3" fill="#7a8399" font-size="8"
      font-family="'Geist Mono', monospace" text-anchor="middle" letter-spacing="0.06em">WRITE</text>
```

Rules: ≤14 characters, all-caps, centered on segment midpoint, 8–10px above line. Never `writing-mode` vertical.

### Legend — horizontal strip at the bottom

**Never put the legend inside the diagram area.** Place as a horizontal strip after all nodes, with a hairline separator:

```svg
<line x1="30" y1="LEGEND_Y-8" x2="VIEWBOX_W-30" y2="LEGEND_Y-8"
      stroke="rgba(45,49,66,0.10)" stroke-width="0.8"/>
<text x="30" y="LEGEND_Y+8" fill="#4f5d75" font-size="8" font-family="'Geist Mono', monospace"
      letter-spacing="0.14em">LEGEND</text>
<!-- Items — horizontal row, ~160px apart -->
```

Expand SVG `viewBox` height by ~60px.

---

## 7. Layout & Spacing

### 4px grid

**All values — font sizes, padding, node dimensions, gaps, x/y coords — divisible by 4.** Non-negotiable.

| Category | Allowed values |
|---|---|
| Font sizes | 8, 12, 16, 20, 24, 28, 32, 40 |
| Node width / height | 80, 96, 112, 120, 128, 140, 144, 160, 180, 200, 240, 320 |
| x / y coordinates | multiples of 4 |
| Gap between nodes | 20, 24, 32, 40, 48 |
| Padding inside boxes | 8, 12, 16 |
| Border radius | 4, 6, 8 |

Exempt: stroke widths (0.8, 1, 1.2), opacity values, and the 22×22 dot-pattern.

Quick check: if a coordinate ends in 1, 2, 3, 5, 6, 7, 9 — fix it.

### Complexity budget (per diagram)

| Limit | Rule |
|---|---|
| Max nodes | 9 |
| Max arrows / transitions | 12 |
| Max coral elements | 2 |
| Max lifelines (sequence) | 5 |
| Max lanes (swimlane) | 5 |
| Max items (quadrant) | 12 |
| Max entities (ER) | 8 |
| Max nesting levels (nested) | 6 |
| Max tree depth | 4 |
| Max org chart depth | 4 |
| Max org chart nodes | 12 |
| Max layers (layer stack) | 6 |
| Max circles (venn) | 3 |
| Max layers (pyramid) | 6 |
| Max annotation callouts | 2 |

If you exceed, split into two diagrams (overview + detail).

### Page layout

1. **Header** — eyebrow (Geist Mono), title (Instrument Serif), optional subtitle (Geist muted).
2. **Diagram container** — default: **clean, borderless**, no background — the SVG sits directly on the page paper. Optional *framed* variant (for card-heavy layouts or hero placements): `paper-2` bg + 1px `rule` border + 8px radius + `1.5rem` padding + `overflow-x: auto`.
3. **Summary cards** — 2–3 col grid with *varied* widths (e.g., `1.1fr 1fr 0.9fr`).
4. **Footer** — colophon in Geist Mono, muted, hairline top border.

---

## 8. Summary Card Pattern

Don't use 3 identical generic cards. Vary the treatment:

```html
<div class="card">
  <p class="eyebrow">SECTION LABEL</p>
  <div class="card-header">
    <span class="card-dot coral"></span>
    <h3>Card Title</h3>
  </div>
  <ul><li>Item</li></ul>
</div>
```

Rules:
- `background: #ffffff` (not paper — slight lift without shadow)
- `border: 1px solid rgba(45,49,66,0.12)`
- `border-radius: 6px`, `padding: 1.25rem`
- **No `box-shadow`**
- Card dots: 7px, `border-radius: 50%` — ink / muted / coral / link / soft variants

---

## 9. Pre-Output Checklist (Taste Gate)

Run before producing any diagram.

**Type fit:**
- [ ] Right type for what I'm showing? (§3 selection guide)
- [ ] Would a table / paragraph do the same job? (If yes — don't draw.)
- [ ] Loaded the matching `references/type-*.md`?

**Remove test:**
- [ ] Can I remove any node? (Would a reader still understand?)
- [ ] Can I merge any two nodes? (Do they always travel together?)
- [ ] Can I remove any arrow? (Is the relationship obvious from layout?)
- [ ] Can I remove any label? (Does color or shape already signal it?)

**Signal:**
- [ ] Coral used on ≤2 elements? If more, which actually deserve focal status?
- [ ] Legend covers every type used — and nothing extra?
- [ ] Within the type's complexity budget (§7)?

**Technical:**
- [ ] Arrows drawn before boxes?
- [ ] Every arrow label has an opaque `fill="#f5f5f5"` rect behind it?
- [ ] Legend is a horizontal bottom strip, not floating?
- [ ] No vertical `writing-mode` text?
- [ ] `viewBox` expanded for the legend strip (~60px)?
- [ ] Every font size, coord, width, height, gap divisible by 4?

**Typography:**
- [ ] Human-readable names in Geist sans, not Geist Mono?
- [ ] Technical sublabels (ports, commands, URLs) in Geist Mono?
- [ ] Page title in Instrument Serif?
- [ ] Annotation callouts (if any) in *italic* Instrument Serif? (see [primitive-annotation.md](references/primitive-annotation.md))
- [ ] No JetBrains Mono anywhere?

---

## 10. Templates & Variants

Every diagram ships in three variants (see `assets/`):

| Variant | File pattern | When to use |
|---|---|---|
| **Minimal light** (default) | `template.html`, `example-<type>.html` | Screenshot-ready. Diagram + title. Warm paper. |
| **Minimal dark** | `template-dark.html`, `example-<type>-dark.html` | Dark mode sites, slides, high-contrast posts. |
| **Full editorial** | `template-full.html`, `example-<type>-full.html` | Long-form posts where the diagram is the hero. |
| **Consultant special** (quadrant only) | `example-quadrant-consultant.html` | BCG/McKinsey-style 2×2 scenario matrix. Clinical sans-serif, white bg, bold blue double-ended axes, named scenario cells. See [type-quadrant.md](references/type-quadrant.md#consultant-special-2x2-scenario-matrix). |

**Sketchy variant** (optional, applied to any of the above) — see [primitive-sketchy.md](references/primitive-sketchy.md). SVG turbulence filter wobbles strokes for a hand-drawn feel. Good for essays, not for technical docs.

### To create a new diagram

1. Copy the variant closest to what you want (`template.html` for minimal, `template-full.html` for cards).
2. Load the matching `references/type-<name>.md` for layout conventions.
3. Replace the eyebrow, h1, and SVG body.
4. Run the §9 taste gate.

---

## 11. Output

Always produce a single self-contained `.html` file:
- Embedded CSS (no external except Google Fonts)
- Inline SVG (no external images)
- No JavaScript required

Renders correctly in any modern browser.
