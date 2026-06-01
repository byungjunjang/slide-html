# Reference-deck ingestion — layout-device extraction

theme-init Phase 2 (`author_layouts.py`) can take `--reference <deck>` — the
hand-made brand deck a new preset should echo. `scripts/ingest_reference.py`
parses that deck **deterministically (stdlib only, no LLM)** and reports the
layout devices it actually uses, so `prep` can recommend a `surface.card_style`,
seed the DESIGN.md §5/§6 review draft with measured hints, and store the signals
in the authoring manifest.

It is a **recommender, not an applier**: it never edits `theme.json`, never
re-renders, and never replaces the human-authored §5/§6 vocabulary (it only adds
a clearly-labeled hint block). Applying a recommended `card_style` means
re-running `/theme-init` with that token — Phase 1 owns rendering.

## Run it directly

```bash
python3 .codex/skills/theme-init/scripts/ingest_reference.py \
  --reference output/<some-deck>-pptx        # project dir, preset dir, or any folder of *.html
  [--out devices.json] [--quiet]
```

`<reference>` resolution: slides come from `<ref>/slides/*.html`, else
`<ref>/pptx-boilerplate/*.html`, else `<ref>/*.html` (the `.stock` baseline is
skipped). The deck's own `_pptx-slide.css` (or `design-system/_pptx-slide.css`)
is read for the authoritative `.card` chrome.

## Output JSON schema (v1.0)

```jsonc
{
  "version": "1.0",
  "source": "<reference path>",
  "pptx_css": "<path to the deck's _pptx-slide.css, or null>",
  "slides_analyzed": 12,
  "devices": {
    // surface.card_style recommendation. value ∈ filled|hairline|borderless|null.
    // confidence: high = read from the deck's .card CSS rule;
    //             medium = inferred from inline card-like divs;
    //             low/null = could not tell → user fills by hand.
    "card_style": { "value": "hairline", "confidence": "high", "evidence": "…" },

    // slides that use a surface-alt fill (.card-alt / .bg-surface-alt)
    "surface_alternation": { "present": true, "slides_using": 4, "ratio": 0.33 },

    // .rule dividers + 1px/0.5px hairline borders across the deck
    "hairline_dividers": { "present": true, "count": 9 },

    // call-to-action buttons (.btn-cta / .btn-cta-sq / .btn-outline)
    "cta": { "present": true, "count": 2 },

    // uppercase eyebrow / kicker labels (.t-cap-up / .label-caption)
    "kicker": { "present": true, "count": 14 }
  },
  "per_slide": [
    { "slide": "01-title", "cards": 0, "surface_alt": false, "rules": 1, "cta": 0, "kicker": 1 }
    // … one row per analyzed slide
  ]
}
```

## How signals map to decisions

| device | signal read | feeds |
|---|---|---|
| `card_style` | deck `.card` rule: `border:` → hairline · `background:` only → filled · neither → borderless (inline card-like divs as fallback) | `surface.card_style` recommendation (re-init to apply) |
| `surface_alternation` | `.card-alt` / `.bg-surface-alt` usage per slide | DESIGN.md §5 — whether to alternate grouped surfaces |
| `hairline_dividers` | `.rule` + 1px/0.5px borders | DESIGN.md §6 chrome (divider weight) |
| `cta` | `.btn-cta*` / `.btn-outline` | DESIGN.md §5 — CTA device on closing/cover |
| `kicker` | `.t-cap-up` / `.label-caption` | DESIGN.md §6 chrome (eyebrow label) |

## Integration with `prep --reference`

`author_layouts.py prep --preset <p> --reference <deck>`:

1. runs the extractor and stores `devices` under `manifest.blueprint.reference_devices`;
2. prints the `card_style` recommendation — and, if it differs from the preset's
   current `surface.card_style`, the exact `/theme-init` re-run to apply it;
3. inserts an **additive, marker-fenced "참조 자동추출(초안)" hint block** into
   DESIGN.md §5 — it does **not** remove the section's placeholder prompts, so the
   strict `confirm` gate still requires the user to fill the canonical §5/§6 by
   hand (hints inform; they never bypass review). Re-running `prep` replaces the
   fenced block in place (idempotent).

## Shared-reference note

This extractor is the slide-html reference implementation. slide-svg and
slide-pencil should mirror the same device set, JSON schema, and
recommend-don't-apply contract so `card_style` and friends mean the same thing
across all three.
