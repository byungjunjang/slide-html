#!/usr/bin/env node
/**
 * validate-diversity.mjs — deck layout-diversity gate (PIPELINE_UPDATE_PLAN.md item B)
 *
 * Reads slides/*.html and checks, per the data-layout registry
 * (references/layouts.md):
 *   1. coverage    — every slide <body> carries data-layout
 *   2. distinct    — distinct family count >= ceil(slides * 0.6)
 *   3. card ratio  — card-type slides <= 50% of the deck
 *   4. visual      — deck (>=5 slides) has a visual family / <img> / data-image-slot
 *
 * WARN-only by default (exit 0) so it never blocks a build during rollout.
 * Pass --strict to exit 1 on any violation (Phase 4 hard-promotion).
 *
 * The gate is permissive about the family vocabulary: any string counts toward
 * distinctness, and unrecognized ids are reported as INFO (typo radar), not a
 * violation. Only the card-type and visual family SETS are hardcoded here — so
 * adding a new non-card family to layouts.md never triggers a false warning.
 *
 * Usage: node validate-diversity.mjs --slides <dir> [--strict]
 */
import fs from 'fs';
import path from 'path';

// Keep in sync with references/layouts.md (the human SSOT for the registry).
const CARD_FAMILIES = new Set(['cards-overview', 'cards-points', 'kpi-grid', 'paired-concept']);
const VISUAL_FAMILIES = new Set(['image-hero', 'annotated-visual', 'diagram-hero', 'compare-split']);
const KNOWN_FAMILIES = new Set([
  'hero-statement', 'hero-number', 'image-hero', 'annotated-visual', 'diagram-hero',
  'compare-split', 'editorial-prose', 'data-table', 'sequence-flow', 'narrative-frame',
  'chart',
  ...CARD_FAMILIES,
]);

function parseArgs() {
  const a = process.argv.slice(2);
  const args = { strict: false };
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--strict') args.strict = true;
    else if (a[i] === '--slides') args.slides = a[++i];
  }
  if (!args.slides) {
    console.error('usage: node validate-diversity.mjs --slides <dir> [--strict]');
    process.exit(2);
  }
  return args;
}

function layoutOf(html) {
  // Prefer data-layout on <body>; fall back to the first data-layout anywhere.
  const body = html.match(/<body\b[^>]*\bdata-layout\s*=\s*["']([^"']+)["']/i);
  if (body) return body[1].trim();
  const any = html.match(/\bdata-layout\s*=\s*["']([^"']+)["']/i);
  return any ? any[1].trim() : null;
}

function hasVisualSignal(html, family) {
  if (family && VISUAL_FAMILIES.has(family)) return true;
  if (/<img\b/i.test(html)) return true;
  if (/\bdata-image-slot\s*=/i.test(html)) return true;
  return false;
}

function main() {
  const args = parseArgs();
  const dir = path.resolve(args.slides);
  if (!fs.existsSync(dir)) {
    console.error(`[diversity] slides dir not found: ${dir}`);
    process.exit(2);
  }
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  if (!files.length) {
    console.log('[diversity] no slides to check.');
    return 0;
  }

  const missing = [];
  const unknown = [];
  const counts = new Map();
  let cardSlides = 0;
  let anyVisual = false;

  for (const f of files) {
    const html = fs.readFileSync(path.join(dir, f), 'utf8');
    const fam = layoutOf(html);
    if (!fam) { missing.push(f); }
    else {
      counts.set(fam, (counts.get(fam) || 0) + 1);
      if (CARD_FAMILIES.has(fam)) cardSlides++;
      if (!KNOWN_FAMILIES.has(fam)) unknown.push(`${f} -> "${fam}"`);
    }
    if (hasVisualSignal(html, fam)) anyVisual = true;
  }

  const n = files.length;
  const distinct = counts.size;
  const distinctFloor = n <= 2 ? n : Math.max(3, Math.ceil(n * 0.6));
  const cardCap = Math.floor(n * 0.5);

  const warnings = [];
  if (missing.length)
    warnings.push(`coverage: ${missing.length}/${n} slide(s) missing data-layout: ${missing.join(', ')}`);
  if (distinct < distinctFloor)
    warnings.push(`distinct: ${distinct} distinct layout(s) < floor ${distinctFloor} (ideal >= ${Math.ceil(n * 0.7)}). Rotate layouts.`);
  if (cardSlides > cardCap)
    warnings.push(`card ratio: ${cardSlides}/${n} card-type slides > 50% cap (ideal <= 1/3). Reach for visual/editorial/hero layouts.`);
  if (n >= 5 && !anyVisual)
    warnings.push(`visual: no visual family / <img> / data-image-slot anywhere in a ${n}-slide deck. Add a visual-primary slide (P1 visual=evidence).`);

  console.log(`[diversity] ${n} slide(s); ${distinct} distinct layout(s); ${cardSlides} card-type; visual=${anyVisual ? 'yes' : 'no'}.`);
  if (unknown.length)
    console.log(`[diversity] INFO unrecognized family-id (typo? see references/layouts.md): ${unknown.join('; ')}`);

  if (warnings.length) {
    const tag = args.strict ? 'FAIL' : 'WARN';
    for (const w of warnings) console.error(`[diversity] ${tag} ${w}`);
    console.error('[diversity] see references/layouts.md + anti-slop.md §13.');
    if (args.strict) return 1;
  } else {
    console.log('[diversity] ok: layout diversity checks passed.');
  }
  return 0;
}

process.exit(main());
