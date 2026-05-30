// render-diagram.mjs — diagram HTML (inline SVG) → high-DPI transparent PNG
//
// WHY THIS EXISTS
// html2pptx.js translates a slide's DOM into native PPTX objects element by
// element. It only understands text tags, <img>, <div>, and lists — it has NO
// handler for inline <svg>, so any inline SVG is silently dropped from the
// .pptx. The project's only supported SVG path is therefore: SVG → raster PNG →
// <img> slot (the same path prebuild-svg.mjs uses for icons and charts).
//
// prebuild-svg.mjs rasterizes external icons/*.svg with `sharp`. sharp does NOT
// load web fonts (Google Fonts) or reliably shape CJK glyphs, so diagram text —
// especially Korean — renders as fallback faces or tofu. This script instead
// renders the diagram in the SAME Chromium that html2pptx uses, so Pretendard /
// any @font-face / CJK text comes out pixel-perfect, then screenshots just the
// <svg> figure to a transparent PNG. The diagram then fills a normal
// images/<slot>.png slot referenced by <img> in the slide HTML.
//
// USAGE
//   node render-diagram.mjs <input.html> <output.png> [--selector "svg"] [--scale 3] [--bg]
//     --selector  CSS selector of the element to capture (default: "svg")
//     --scale     deviceScaleFactor for crispness (default: 3)
//     --bg        keep the element/page background (default: transparent PNG)
//     --quiet     suppress the per-render log line
//
// The diagram-only HTML this consumes is authored via the `diagram-design`
// skill (SVG figure only, no slide chrome) and should link the deck's
// design-system/colors_and_type.css so SVG `style="fill:var(--accent)"` etc.
// resolve to the active preset at render time. See
// .claude/skills/slide/references/diagram-slots.md for the full contract.

import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs/promises';
import { pathToFileURL } from 'url';

function parseArgs(argv) {
  const positional = [];
  const opts = { selector: 'svg', scale: 3, bg: false, quiet: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--selector') opts.selector = argv[++i];
    else if (a === '--scale') opts.scale = Math.max(1, parseFloat(argv[++i]) || 3);
    else if (a === '--bg') opts.bg = true;
    else if (a === '--quiet') opts.quiet = true;
    else positional.push(a);
  }
  return { positional, opts };
}

/**
 * Render a diagram HTML file to a PNG by screenshotting one element.
 * @param {string} inputHtml  path to the diagram-only HTML
 * @param {string} outputPng  path to write the PNG
 * @param {object} [opts]
 * @param {string} [opts.selector="svg"]  element to capture
 * @param {number} [opts.scale=3]         deviceScaleFactor
 * @param {boolean} [opts.bg=false]        keep background (false → transparent)
 * @param {boolean} [opts.quiet=false]
 * @returns {Promise<{output:string,width:number,height:number}>}
 */
export async function renderDiagram(inputHtml, outputPng, opts = {}) {
  const { selector = 'svg', scale = 3, bg = false, quiet = false } = opts;
  const inPath = path.isAbsolute(inputHtml) ? inputHtml : path.join(process.cwd(), inputHtml);
  const outPath = path.isAbsolute(outputPng) ? outputPng : path.join(process.cwd(), outputPng);

  await fs.access(inPath); // throws a clear ENOENT if the diagram HTML is missing
  await fs.mkdir(path.dirname(outPath), { recursive: true });

  const browser = await chromium.launch();
  try {
    const context = await browser.newContext({ deviceScaleFactor: scale });
    const page = await context.newPage();
    page.on('console', (msg) => { if (!quiet) console.log(`  [browser] ${msg.text()}`); });

    await page.goto(pathToFileURL(inPath).href, { waitUntil: 'networkidle' });
    // Wait for @font-face / Google Fonts to finish so text shapes correctly.
    await page.evaluate(() => document.fonts && document.fonts.ready);
    await page.waitForTimeout(250);

    let target = await page.$(selector);
    if (!target) {
      if (!quiet) console.warn(`  [render-diagram] selector "${selector}" not found — capturing <body>`);
      target = await page.$('body');
    }
    if (!target) throw new Error('render-diagram: nothing to capture (no matching element and no <body>)');

    const box = await target.boundingBox();
    await target.screenshot({ path: outPath, omitBackground: !bg });

    const w = box ? Math.round(box.width * scale) : 0;
    const h = box ? Math.round(box.height * scale) : 0;
    if (!quiet) console.log(`  render ${path.basename(inPath)} → ${path.basename(outPath)} ${w}×${h}px @${scale}x${bg ? '' : ' (transparent)'}`);
    return { output: outPath, width: w, height: h };
  } finally {
    await browser.close();
  }
}

// CLI
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { positional, opts } = parseArgs(process.argv.slice(2));
  const [input, output] = positional;
  if (!input || !output) {
    console.error('Usage: node render-diagram.mjs <input.html> <output.png> [--selector "svg"] [--scale 3] [--bg] [--quiet]');
    process.exit(1);
  }
  renderDiagram(input, output, opts)
    .then((r) => { console.log(`render-diagram done: ${r.output} (${r.width}×${r.height})`); })
    .catch((e) => { console.error('render-diagram failed:', e.message || e); process.exit(1); });
}
