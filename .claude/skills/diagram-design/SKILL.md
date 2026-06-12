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
- If you're past the complexity budget (`references/diagram-grammar.md`), split into an overview + detail.

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

The full design-vocabulary tables — semantic roles, node type → fill/stroke treatment, typography spec, and the font stack — live in [`references/style-guide.md`](references/style-guide.md). Read it before assigning colors or fonts.

**Focal rule:** `accent` goes on 1–2 elements max. Everything else is `ink` / `muted` / `soft`. If you're tempted to accent 4 things, you haven't decided what's focal yet.

---

## 6–8. Universal Diagram Grammar

**작곡(드로잉) 전에 [`references/diagram-grammar.md`](references/diagram-grammar.md)를 반드시 읽는다.** Core SVG primitives (background, arrow markers, node-box pattern, arrow-label masking, bottom legend strip), the 4px grid, the complexity budget, page layout, and the summary-card pattern all live there — every rule binds exactly as before.

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
- [ ] Within the type's complexity budget (`references/diagram-grammar.md`)?

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
