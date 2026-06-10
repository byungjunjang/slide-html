#!/usr/bin/env node
/**
 * export_deck_pptx.mjs — 멀티 파일 slide deck → editable PPTX 빌더
 *
 * 사용:
 *   node export_deck_pptx.mjs --slides <dir> --out <file.pptx> [--screenshots <dir>] [--no-screenshots]
 *
 * 동작:
 *   - scripts/html2pptx.js 가 HTML DOM 을 요소 단위로 PowerPoint 네이티브 객체로 번역
 *   - 텍스트는 진짜 텍스트박스 — PPT 에서 더블클릭으로 바로 편집 가능
 *   - body 크기 960pt × 540pt (LAYOUT_WIDE, 13.333″ × 7.5″)
 *   - 브라우저는 데크당 1회만 기동해 모든 슬라이드가 공유 (슬라이드당 재기동 금지)
 *   - 슬라이드별 렌더 스크린샷을 <deck>/_screenshots/ 에 저장 (visual self-review 용)
 *
 * ⚠️ HTML 은 4 hard constraint 를 통과해야 한다 (references/4-constraints.md):
 *   1. 텍스트는 <p>/<h1>-<h6> 안에만 (div 직접 텍스트 금지)
 *   2. CSS gradient 금지
 *   3. <p>/<h*> 에 background/border/shadow 금지 (외부 div 가 담당)
 *   4. div 에 background-image 금지 (<img> 사용)
 *
 * slide-html 의 유일한 경로는 editable PPTX 다 — 시각 자유도가 필요한 요구는
 * 다른 익스포터로 우회하지 않고 시각 복잡도를 낮춰 제약을 통과시킨다.
 *
 * 의존성: npm install playwright pptxgenjs sharp
 *
 * 슬라이드는 파일명 순으로 빌드된다 (01-xxx.html → 02-xxx.html → ...).
 */

import pptxgen from 'pptxgenjs';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs() {
  const args = { screenshots: undefined, noScreenshots: false };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--no-screenshots') { args.noScreenshots = true; continue; }
    const k = a[i].replace(/^--/, '');
    args[k] = a[i + 1];
    i++;
  }
  if (!args.slides || !args.out) {
    console.error('사용: node export_deck_pptx.mjs --slides <dir> --out <file.pptx> [--screenshots <dir>] [--no-screenshots]');
    console.error('');
    console.error('⚠️ HTML 은 4 hard constraint 를 통과해야 합니다 (references/4-constraints.md).');
    console.error('   slide-html 은 editable PPTX 단일 경로입니다 — PDF 폴백 없음.');
    process.exit(1);
  }
  return args;
}

async function main() {
  const args = parseArgs();
  const slidesDir = path.resolve(args.slides);
  const outFile = path.resolve(args.out);
  const deckRoot = path.dirname(slidesDir);
  const screenshotsDir = args.noScreenshots
    ? null
    : path.resolve(args.screenshots || path.join(deckRoot, '_screenshots'));

  const files = (await fs.readdir(slidesDir))
    .filter(f => f.endsWith('.html'))
    .sort();
  if (!files.length) {
    console.error(`No .html files found in ${slidesDir}`);
    process.exit(1);
  }

  console.log(`Converting ${files.length} slides via html2pptx...`);

  const { createRequire } = await import('module');
  const require = createRequire(import.meta.url);
  let html2pptx;
  try {
    html2pptx = require(path.join(__dirname, 'html2pptx.js'));
  } catch (e) {
    console.error(`✗ html2pptx.js 로드 실패: ${e.message}`);
    console.error(`  의존성 누락 시: npm install playwright pptxgenjs sharp`);
    process.exit(1);
  }

  if (screenshotsDir) await fs.mkdir(screenshotsDir, { recursive: true });

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch — HTML body 960 × 540 pt 대응

  // 브라우저는 데크당 1회 기동. 슬라이드마다 재기동하면 N×(부팅 비용)이 든다.
  const browser = await html2pptx.launchBrowser();

  const errors = [];
  const report = [];
  try {
    for (let i = 0; i < files.length; i++) {
      const f = files[i];
      const fullPath = path.join(slidesDir, f);
      const screenshotPath = screenshotsDir
        ? path.join(screenshotsDir, f.replace(/\.html$/, '.png'))
        : null;
      try {
        const { warnings = [] } = await html2pptx(fullPath, pres, { browser, screenshotPath });
        const mark = warnings.length ? `✓ (${warnings.length} overlap auto-fix)` : '✓';
        console.log(`  [${i + 1}/${files.length}] ${f} ${mark}`);
        report.push({ file: f, ok: true, warnings });
      } catch (e) {
        console.error(`  [${i + 1}/${files.length}] ${f} ✗  ${e.message}`);
        errors.push({ file: f, error: e.message });
        report.push({ file: f, ok: false, error: e.message, warnings: [] });
      }
    }
  } finally {
    await browser.close();
  }

  // Persist the per-slide outcome. Overlap auto-fixes only patch the PPTX
  // coordinates — the source HTML still overlaps — so they must survive the
  // console (background/subagent runs lose stdout). /slide Step 5 reads this
  // and fixes the HTML instead of shipping silently-corrected decks.
  const totalWarnings = report.reduce((n, r) => n + r.warnings.length, 0);
  const reportPath = path.join(deckRoot, 'build-report.json');
  await fs.writeFile(reportPath, JSON.stringify({
    generated_at: new Date().toISOString(),
    deck: path.basename(deckRoot),
    slides_total: files.length,
    slides_ok: files.length - errors.length,
    overlap_autofix_total: totalWarnings,
    slides: report,
  }, null, 2));
  if (totalWarnings) {
    console.warn(`⚠️ ${totalWarnings} overlap auto-fix(es) applied — 소스 HTML과 PPTX 좌표가 다릅니다. build-report.json을 보고 해당 슬라이드 HTML을 고치세요.`);
  }

  if (errors.length) {
    console.error(`\n⚠️ ${errors.length} 장 변환 실패. 흔한 원인: 4 hard constraint 위반.`);
    console.error(`  references/error-patterns.md 의 픽스 패턴을 참조하세요.`);
    if (errors.length === files.length) {
      console.error(`✗ 전부 실패 — PPTX 를 생성하지 않습니다.`);
      process.exit(1);
    }
  }

  await pres.writeFile({ fileName: outFile });
  console.log(`\n✓ Wrote ${outFile}  (${files.length - errors.length}/${files.length} slides, editable PPTX)`);
  if (screenshotsDir) {
    console.log(`✓ Slide screenshots → ${screenshotsDir} (visual self-review: SKILL.md Step 5)`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });
