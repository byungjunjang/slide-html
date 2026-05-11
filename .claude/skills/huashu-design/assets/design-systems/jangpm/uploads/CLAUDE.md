# lecture-slide-html

Single `/slide` skill that generates high-quality HTML slide decks using Reveal.js. Replaces v2's 3-agent pipeline with a unified skill + example-driven design system.

## Source Of Truth

`CLAUDE.md` is the project SSOT.

If any other document conflicts with this file, follow `CLAUDE.md` and update the other document to match.

## Core Constraints

- **Light mode only** — no dark mode, no theme toggle
- **1280×720 fixed** — overflow absolutely forbidden
- **Single HTML file** — inline CSS/JS, CDN for libraries
- **No animations** — `transition: 'none'` in Reveal.js
- **CSS variables only** — no hardcoded HEX values in HTML
- **`var` top-level** — use `var` for top-level JS variables (TDZ prevention)

## Visual Authority

Target: `reference/reference 2.pptx`

- Monochrome business report tone
- Restrained indigo emphasis
- Evidence-first layouts
- Typography and structural alignment over decorative variety
- Text blocks, tables, and charts are first-class visual modules

## Skills

| Skill | Status | Trigger |
|-------|--------|---------|
| `/slide` | Active | "슬라이드 만들어", "make slides", "/slide" |
| `/export-pptx` | Active | HTML → PPTX conversion |
| `/export-pdf` | Active | PPTX → PDF conversion |
| `/upload-drive` | Active | Google Drive upload |
| `/nanobanana2` | Active | AI illustration generation |
| `/capture-screenshot` | Active | Website screenshot capture |

## Directory Structure

```
lecture-slide-html/
├── CLAUDE.md
├── .claude/skills/
│   ├── slide/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── skeleton.md
│   │       ├── design-system.md
│   │       ├── patterns.md
│   │       ├── anti-slop.md
│   │       ├── libraries.md
│   │       ├── visual-assets.md
│   │       └── export.md
│   ├── export-pptx/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       ├── tokens.js
│   │       ├── pptx-helpers.js
│   │       ├── parser.js
│   │       ├── renderer.js
│   │       ├── chart-converter.js
│   │       ├── convert-auto.js
│   │       └── pptx-screenshot.js
│   ├── export-pdf/
│   │   └── SKILL.md
│   ├── upload-drive/
│   │   └── SKILL.md
│   ├── nanobanana2/
│   │   └── SKILL.md
│   └── capture-screenshot/
│       └── SKILL.md
├── eval/                  # Slide-specific eval pipeline
│   ├── pipeline/          # Node.js eval scripts
│   │   ├── run.js         # L1+L2+L3 scoring orchestrator (WIP: check modules not yet implemented)
│   │   └── pptx-compare.js # HTML vs PPTX side-by-side comparison
│   └── stress-tests.md    # 36 test prompts by category
└── docs/                  # Specs and plans
```

## Coding Rules

- `var` for top-level JS variables, `let`/`const` inside functions/blocks only
- `Chart.defaults.animation = false` immediately after Chart.js CDN
- `rgba()` for Chart.js colors (CSS variables don't resolve)
- CSS Grid `gap` for consistent card/element spacing
- `maintainAspectRatio: false` + `responsive: true` for Chart.js

## Anti-Slop (18 Rules)

1. No gradient orbs → `.bg-dots` (title/section only)
2. No gradient borders → `1px solid var(--border)`
3. No gradient text → solid `var(--text)` or `var(--accent)`
4. No hover scale/translateY → shadow only
5. No glow effects → `var(--shadow-md)`
6. No animations → static elements
7. No decorative partial color borders → semantic/structural emphasis only in approved patterns
8. Avoid inline styles → use classes/tokens by default, allow only documented pattern exceptions
9. No hardcoded HEX → `var(--*)`
10. No dense text → max 4-5 bullets, 2-3 lines
11. No inconsistent spacing → CSS Grid `gap`
12. No decorative images → content images only
13. No `position: relative` on sections → Reveal.js manages positioning
14. No card-first layouts → text blocks + rule lines when sufficient
15. No accent-soft as default → rare accent, monochrome first
16. No decorative semantic colors → data meaning only
17. No SaaS dashboard aesthetics → report-style layouts
18. No text-only slides → structured text with visual hierarchy is valid, but avoid plain walls of text

## Pattern System

The active pattern library lives in `.claude/skills/slide/references/patterns.md`.

Pattern policy:

- Keep a small core set that clearly reflects `reference 2`
- Prefer stronger repeated grammar over many loosely related layouts
- New patterns are allowed, but only if they extend the same visual language
- New patterns must not force card-heavy or dashboard-like composition

Extension gate for new patterns:

1. The pattern must work in grayscale first.
2. The pattern must preserve PPTX feasibility with simple layout primitives.
3. The pattern must add a genuinely new information structure, not cosmetic variation.
4. The pattern must define when it should be used and when an existing pattern is sufficient.
5. The pattern must not weaken GM placement, spacing rules, or accent restraint.

Practical split:

- Core patterns: title, section, closing, report-summary, report-two-column, goal-breakdown, kpi-row, comparison-table, chart-with-callout, process-row, icon-explainer, data-table
- Optional extension patterns: timeline-report, evidence-grid, code-explain, diagram

If better design ideas appear later, add them as candidate patterns first, validate them against the gate above, then promote them into the core set only if they improve the system rather than increasing variety for its own sake.

## Common Pitfalls

- **Chart.js colors**: Use `rgba()`, never CSS variables — Chart.js can't resolve `var(--accent)`
- **TDZ errors**: Use `var` for top-level variables, not `let`/`const`
- **720px overflow**: Keep content density low — max 4-5 items per slide, short text
- **GM placement**: Every content slide needs `.gm` as last child (not on title/section/closing)
- **Card overuse**: Cards are secondary. Use text blocks + rule lines + tables as primary building blocks
- **Accent flooding**: Max 1-2 accent events per slide. Slide should work in grayscale first
- **Pattern drift**: Do not add layout variants unless they pass the pattern extension gate above
- **HTML/PPTX drift**: If a pattern cannot be represented cleanly in PPTX, it is not ready to be a core pattern

## Eval Pipeline

**Reliable (use these now):**
- `eval/stress-tests.md` — 36 test prompts by category
- `eval/pipeline/run.js` — full L1+L2 scoring orchestrator (use: `node eval/pipeline/run.js --dir output/ --round N --no-l3`)
- `eval/pipeline/pptx-compare.js` — HTML vs PPTX side-by-side screenshot comparison
- `eval/pipeline/checks/gm-presence.js` — GM presence check on all content slides (L2, 10pts)
- `eval/pipeline/checks/typo-hierarchy.js` — typography scale consistency (L2, 20pts)
- `eval/pipeline/checks/layout-overflow.js` — viewport overflow detection (L2, 20pts)
- `eval/pipeline/checks/pattern-diversity.js` — pattern variety rules (L2, 15pts)
- `eval/pipeline/checks/anti-slop.js` — anti-slop rule compliance (L2, 15pts)
- `eval/pipeline/checks/visual-elements.js` — structured layout / visual elements presence (L2, 15pts)
- `eval/pipeline/checks/chart-diagram.js` — Chart.js + Mermaid config correctness (L2, 15pts)

**Not yet implemented (do not reference in prod):**
- `eval/pipeline/vision-scorer.js` — L3 vision scoring (requires agent)

**Quality gates (target):** SHIP ≥9.0 (L1+L2 only until L3 is live), ACCEPTABLE ≥8.0
