---
preset: {{TOKEN:name}}
display_name: {{TOKEN:display_name}}
generated_by: theme-init
schema_version: {{TOKEN:version}}
---

# {{TOKEN:display_name}} · Brand Spec (auto-generated)

> **Description:** {{TOKEN:description}}

## Color Tokens

| Token | Hex | Role |
|---|---|---|
| `--bg` | `{{TOKEN:colors.bg}}` | page background |
| `--surface` | `{{TOKEN:colors.surface}}` | card / container |
| `--surface-alt` | `{{TOKEN:colors.surface-alt}}` | grouped block |
| `--text` | `{{TOKEN:colors.text}}` | primary text |
| `--text-secondary` | `{{TOKEN:colors.text-secondary}}` | body secondary |
| `--text-tertiary` | `{{TOKEN:colors.text-tertiary}}` | captions |
| `--border` | `{{TOKEN:colors.border}}` | dividers / card edges |
| `--border-strong` | `{{TOKEN:colors.border-strong}}` | strong dividers |
| `--accent` | `{{TOKEN:colors.accent}}` | primary accent (use 1–2 events / slide) |
| `--accent-soft` | `{{TOKEN:colors.accent-soft}}` | accent-tinted bg |
| `--accent-ink` | `{{TOKEN:colors.accent-ink}}` | accent pressed |
| `--positive` | `{{TOKEN:colors.positive}}` | growth (data only) |
| `--negative` | `{{TOKEN:colors.negative}}` | decline (data only) |
| `--warning` | `{{TOKEN:colors.warning}}` | caution (data only) |

## Typography

- **Font chain:** `{{TOKEN:typography.font-chain}}`
- **Display** {{TOKEN:typography.display.size}}px / {{TOKEN:typography.display.weight}}
- **Headline** {{TOKEN:typography.headline.size}}px / {{TOKEN:typography.headline.weight}}
- **Title** {{TOKEN:typography.title.size}}px / {{TOKEN:typography.title.weight}}
- **Body** {{TOKEN:typography.body.size}}px / {{TOKEN:typography.body.weight}}
- **Caption** {{TOKEN:typography.caption.size}}px / {{TOKEN:typography.caption.weight}}

## Voice

- **Tone:** {{TOKEN:voice.tone}}
- **POV:** {{TOKEN:voice.pov}}
- **Register:** {{TOKEN:voice.register}}
- **Forbidden phrases:** {{TOKEN:voice.forbidden_phrases|csv}}
- **GM style hint:** {{TOKEN:voice.gm_style_hint}}

## Assets

- **Icon pack (default):** {{TOKEN:assets.icon-pack-default}}
{{IF:assets.character}}
- **Brand character:** `{{TOKEN:assets.character}}`
{{/IF}}

---

> **Provenance:** generated from `theme.json` v{{TOKEN:version}} via `/theme-init`. Edit `theme.json` and re-run to regenerate.
