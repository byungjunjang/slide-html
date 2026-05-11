# Export Workflow Reference

Guide for converting HTML slide decks to PPTX, PDF, and uploading to Google Drive.

---

## Export Pipeline

```
HTML (.html)
  │
  ├─ /export-pptx ─→ PowerPoint (.pptx)  [~98% fidelity, handcrafted]
  │                      │
  │                      ├─ /export-pdf ─→ PDF (.pdf)
  │                      │
  │                      └─ /upload-drive ─→ Google Drive URL
  │                                           └─ Google Slides (optional)
  │
  └─ Direct PDF (fallback) ─→ Puppeteer HTML → PDF
```

Each step is independent — users can export to any format without requiring previous steps (except PDF which needs PPTX first via the primary path).

---

## PPTX Conversion

### Primary Method: Handcrafted (Recommended)

Claude reads the HTML, analyzes each slide's layout, and writes a dedicated PptxGenJS script with hand-placed coordinates. **~98% visual fidelity.**

Workflow:
1. Read HTML → analyze `<section>` patterns, text, charts, CSS variables
2. Write `output/{slug}/{slug}-generate-pptx.js` with per-slide IIFE blocks
3. Run the script → produces `.pptx`

See `/export-pptx` SKILL.md for full details.

### High-Fidelity Scripted Converter (Default)

The default scripted path measures the real browser layout, then rebuilds the slide in PPTX with editable text, shapes, and tables.

```bash
cd .claude/skills/export-pptx/scripts
node convert.js --input <html-path> [--output <pptx-path>] [--render-dir <asset-dir>]
```

Uses browser DOM measurement rather than pattern heuristics. `canvas`, complex `svg`, and `img` elements can still become per-element fallback assets, but the slide is not flattened into a single screenshot.

### What Gets Converted

| HTML Element | PPTX Element |
|-------------|-------------|
| `<section>` | Slide |
| `.display`, `.headline`, `.title` | Text box (sized by type scale) |
| `.body`, `p` | Text box (body size) |
| `.card` | Rectangle shape + text boxes |
| `<table>` | PPTX table |
| Chart.js `<canvas>` | Element fallback image |
| `<img>` | Image |
| `.gm` | Shape + text box |
| Mermaid `<pre>` | Text/code or fallback asset depending on complexity |
| `<pre><code>` | Text box + optional raster fallback for complex styling |

### Design Token Mapping

CSS variables map to PPTX constants:

| CSS Variable | PPTX Color (hex) |
|-------------|-----------------|
| `--bg` | `FAFAF9` |
| `--surface` | `FFFFFF` |
| `--text` | `1A1A1A` |
| `--text-secondary` | `6B7280` |
| `--accent` | `4633E3` |
| `--accent-soft` | `E8E5FC` |
| `--border` | `E5E7EB` |

### Known Limitations

1. Canvas-based charts remain raster fallback assets
2. Complex SVGs may stay as assets instead of editable vectors
3. Fine browser line wrapping can differ slightly in PowerPoint
4. CSS effects beyond fills/borders/typography are not guaranteed

---

## PDF Conversion

### Method 1: LibreOffice Headless (Recommended)

Requires LibreOffice installed on the system.

```bash
soffice --headless --convert-to pdf "output/deck.pptx" --outdir "output/"
```

### Method 2: Google Slides Export

1. Upload PPTX via `/upload-drive`
2. Export as PDF from Google Slides

### Method 3: Direct HTML → PDF (Fallback)

Uses Puppeteer to render each slide as a PDF page. Lower quality than PPTX → PDF path.

---

## Google Drive Upload

### Prerequisites

- Google Workspace authentication configured via `gws` CLI
- Target folder specified or uses default "Slide Decks" folder

### Workflow

1. Upload `.pptx` file to Google Drive
2. (Optional) Convert to Google Slides format for online editing
3. Return shareable URL

### Command

```
/upload-drive output/deck.pptx
/upload-drive output/deck.pptx --folder "Presentations/2026"
/upload-drive output/deck.pptx --as-slides  # Convert to Google Slides
```

---

## Recommended Workflow

For best results:

1. Generate HTML with `/slide`
2. Review in browser, make adjustments
3. Run `/export-pptx` to create PowerPoint file (handcrafted ~98% fidelity)
4. Open PPTX in PowerPoint — fix any remaining layout issues
5. (Optional) `/export-pdf` for distribution
6. (Optional) `/upload-drive` for sharing
