#!/usr/bin/env node
/**
 * active-accent.mjs — resolve the active preset's accent palette for image
 * style-lock injection (PIPELINE_UPDATE_PLAN.md item E / Fix2).
 *
 * The /slide §2.5 image prompt must lock generated images to the *actual* theme
 * accent (a precise hex), not a generic "single accent color". This prints the
 * resolved palette so the prompt can bake in the real hex + mood.
 *
 * Resolution order for colors_and_type.css:
 *   1. --css <path>                       (explicit)
 *   2. --deck <dir>/design-system/colors_and_type.css
 *   3. ./design-system/colors_and_type.css   (run from inside a deck)
 *   4. slide bundle active.json -> <preset>/colors_and_type.css   (fallback)
 *
 * Usage:
 *   node active-accent.mjs                 # auto-resolve, human summary
 *   node active-accent.mjs --json          # machine-readable
 *   node active-accent.mjs --deck output/foo-pptx
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DS_ROOT = path.resolve(__dirname, '../assets/design-systems');

function arg(name) {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
}

function resolveCssPath() {
  const explicit = arg('--css');
  if (explicit) return explicit;
  const deck = arg('--deck');
  if (deck) return path.join(deck, 'design-system', 'colors_and_type.css');
  const local = path.resolve('design-system/colors_and_type.css');
  if (fs.existsSync(local)) return local;
  // fallback: active preset in the slide bundle
  try {
    const active = JSON.parse(fs.readFileSync(path.join(DS_ROOT, 'active.json'), 'utf8')).active;
    if (active) return path.join(DS_ROOT, active, 'colors_and_type.css');
  } catch { /* no active.json — fall through */ }
  return path.join(DS_ROOT, 'jangpm', 'colors_and_type.css'); // seed default
}

function readVar(css, name) {
  const m = css.match(new RegExp('--' + name + '\\s*:\\s*(#[0-9A-Fa-f]{3,8}|[^;]+);'));
  return m ? m[1].trim() : null;
}

function main() {
  const cssPath = resolveCssPath();
  if (!fs.existsSync(cssPath)) {
    console.error(`active-accent: colors_and_type.css not found at ${cssPath}`);
    process.exit(2);
  }
  const css = fs.readFileSync(cssPath, 'utf8');
  const pal = {
    source: cssPath,
    accent: readVar(css, 'accent'),
    accentSoft: readVar(css, 'accent-soft'),
    accentInk: readVar(css, 'accent-ink'),
    bg: readVar(css, 'bg'),
    text: readVar(css, 'text'),
  };

  if (process.argv.includes('--json')) {
    console.log(JSON.stringify(pal, null, 2));
    return;
  }

  // Human / paste-ready summary for the image style-lock.
  console.log(`source : ${pal.source}`);
  console.log(`accent : ${pal.accent}   (single accent — lock generated images to THIS hex)`);
  console.log(`palette: bg ${pal.bg} / text ${pal.text} / accent-soft ${pal.accentSoft} / accent-ink ${pal.accentInk}`);
  console.log('');
  console.log('style-lock fragment (combine with the preset mood from DESIGN.md §1):');
  console.log(`  "...editorial composition, monochrome palette with a SINGLE accent color ${pal.accent},`);
  console.log(`   on background ${pal.bg}, generous negative space, no text overlay, no gradient, no glow"`);
}

main();
