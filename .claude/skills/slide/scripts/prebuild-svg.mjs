// prebuild-svg.mjs — SVG → PNG raster + slides HTML rewrite
//
// PptxGenJS bug: when a slide references <img src="…/foo.svg">, PptxGenJS
// embeds the SVG bytes under BOTH image-N-1.png AND image-N-2.svg. The .png
// member ends up holding raw SVG XML, which PowerPoint (especially mobile/web
// and some desktop renderers) refuses to decode — the chart shows as a
// broken-image icon.
//
// Workaround: before invoking export_deck_pptx, rasterize every icons/*.svg
// to a real PNG and rewrite slide HTML to point at the PNG. This forces
// PptxGenJS to embed a single, valid PNG.
//
// We also cap the long edge at 1920px so the rendered chart can be fed back
// to image-based debugging tools (e.g. Anthropic API has a 2000px ceiling on
// many-image requests).

import fs from 'fs/promises';
import path from 'path';
import sharp from 'sharp';

const DEFAULT_MAX_PX = 1920;

async function listSvgs(iconsDir) {
  try {
    const entries = await fs.readdir(iconsDir);
    return entries.filter(f => f.toLowerCase().endsWith('.svg'));
  } catch (e) {
    if (e.code === 'ENOENT') return [];
    throw e;
  }
}

async function rasterizeSvg(svgPath, pngPath, maxPx) {
  const meta = await sharp(svgPath).metadata();
  const baseW = meta.width || 1024;
  const baseH = meta.height || 768;
  const scale = Math.min(maxPx / baseW, maxPx / baseH, 4);
  const targetW = Math.max(1, Math.round(baseW * scale));
  const targetH = Math.max(1, Math.round(baseH * scale));

  await sharp(svgPath, { density: 150 })
    .resize(targetW, targetH, { fit: 'fill' })
    .png({ compressionLevel: 9 })
    .toFile(pngPath);

  return { width: targetW, height: targetH };
}

async function rewriteSlideHtml(slidesDir, svgBaseNames) {
  let files;
  try {
    files = (await fs.readdir(slidesDir)).filter(f => f.endsWith('.html'));
  } catch (e) {
    if (e.code === 'ENOENT') return 0;
    throw e;
  }

  let rewritten = 0;
  for (const f of files) {
    const p = path.join(slidesDir, f);
    const before = await fs.readFile(p, 'utf8');
    let after = before;
    for (const base of svgBaseNames) {
      // Only target src="…" attributes so unrelated mentions of .svg in
      // comments are left alone.
      const re = new RegExp(`(src=["'][^"']*?/?)${base}\\.svg(["'])`, 'g');
      after = after.replace(re, `$1${base}.png$2`);
    }
    if (after !== before) {
      await fs.writeFile(p, after);
      rewritten += 1;
    }
  }
  return rewritten;
}

/**
 * Run the SVG prebuild pass.
 * @param {object} opts
 * @param {string} opts.projectDir — the deck folder (contains slides/, icons/)
 * @param {number} [opts.maxPx=1920] — cap for the rasterized PNG long edge
 * @param {boolean} [opts.quiet=false] — suppress per-icon log lines
 * @returns {Promise<{rasterized: string[], rewrittenHtml: number}>}
 */
export async function prebuildSvg({ projectDir, maxPx = DEFAULT_MAX_PX, quiet = false } = {}) {
  if (!projectDir) throw new Error('prebuildSvg: projectDir is required');
  const iconsDir = path.join(projectDir, 'icons');
  const slidesDir = path.join(projectDir, 'slides');

  const svgs = await listSvgs(iconsDir);
  const rasterized = [];
  const baseNames = [];
  for (const svg of svgs) {
    const base = svg.replace(/\.svg$/i, '');
    const pngPath = path.join(iconsDir, `${base}.png`);
    const svgPath = path.join(iconsDir, svg);

    let needsBuild = true;
    try {
      const [svgStat, pngStat] = await Promise.all([fs.stat(svgPath), fs.stat(pngPath)]);
      // Skip if PNG already exists, is newer than the SVG, AND is within the
      // configured size cap. Re-raster anything oversized — that's the bug
      // we're fixing.
      if (pngStat.mtimeMs >= svgStat.mtimeMs) {
        const meta = await sharp(pngPath).metadata();
        if ((meta.width || 0) <= maxPx && (meta.height || 0) <= maxPx) {
          needsBuild = false;
        }
      }
    } catch (e) {
      if (e.code !== 'ENOENT') throw e;
    }

    if (needsBuild) {
      const dim = await rasterizeSvg(svgPath, pngPath, maxPx);
      rasterized.push(`${svg} → ${base}.png (${dim.width}×${dim.height})`);
      if (!quiet) console.log(`  raster ${svg} → ${base}.png ${dim.width}×${dim.height}`);
    }
    baseNames.push(base);
  }

  const rewrittenHtml = baseNames.length
    ? await rewriteSlideHtml(slidesDir, baseNames)
    : 0;
  if (rewrittenHtml > 0 && !quiet) {
    console.log(`  rewrote ${rewrittenHtml} slide HTML file(s): .svg refs → .png`);
  }

  return { rasterized, rewrittenHtml };
}

// CLI: `node prebuild-svg.mjs <projectDir> [maxPx]`
if (import.meta.url === `file://${process.argv[1]}`) {
  const projectDir = path.resolve(process.argv[2] || '.');
  const maxPx = process.argv[3] ? parseInt(process.argv[3], 10) : DEFAULT_MAX_PX;
  prebuildSvg({ projectDir, maxPx })
    .then(r => {
      console.log(`prebuild-svg done: ${r.rasterized.length} rasterized, ${r.rewrittenHtml} html rewritten`);
    })
    .catch(e => {
      console.error('prebuild-svg failed:', e);
      process.exit(1);
    });
}
