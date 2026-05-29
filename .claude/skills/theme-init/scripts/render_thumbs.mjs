#!/usr/bin/env node
/**
 * render_thumbs.mjs — screenshot each slides/*.html in a scratch project to PNG.
 *
 * Used by author_layouts.py for the Phase 2 (Layout Authoring) review
 * checkpoint. The project must be a real /slide project layout (created by
 * init-project.sh) so the boilerplate's `../_pptx-slide.css` and its
 * `@import design-system/colors_and_type.css` resolve.
 *
 * Usage:
 *   node render_thumbs.mjs --project <project-dir> --out <out-dir> --tag <stock|authored>
 *
 * Writes <out-dir>/<stem>.<tag>.png at 1280x720 (= 960pt x 540pt @ 96dpi).
 */
import { chromium } from 'playwright';
import { readdirSync, mkdirSync } from 'node:fs';
import { resolve, join, basename } from 'node:path';
import { pathToFileURL } from 'node:url';

function arg(flag, def = null) {
  const i = process.argv.indexOf(flag);
  return i >= 0 && i + 1 < process.argv.length ? process.argv[i + 1] : def;
}

const projectDir = resolve(arg('--project'));
const outDir = resolve(arg('--out'));
const tag = arg('--tag', 'authored');
const slidesDir = join(projectDir, 'slides');

mkdirSync(outDir, { recursive: true });

const slides = readdirSync(slidesDir).filter((f) => f.endsWith('.html')).sort();
if (slides.length === 0) {
  console.error('[render_thumbs] no slides found in ' + slidesDir);
  process.exit(0);
}

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

for (const file of slides) {
  const stem = basename(file, '.html');
  const url = pathToFileURL(join(slidesDir, file)).href;
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
  } catch {
    await page.goto(url, { waitUntil: 'load', timeout: 15000 });
  }
  await page.screenshot({
    path: join(outDir, `${stem}.${tag}.png`),
    clip: { x: 0, y: 0, width: 1280, height: 720 },
  });
  console.error(`[render_thumbs] ${stem}.${tag}.png`);
}

await browser.close();
