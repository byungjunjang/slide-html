# Error Patterns — 알려진 빌드 에러 + 즉시 픽스

이 번들의 `scripts/export_deck_pptx.mjs` 빌드 시 자주 만나는 에러들과 즉시 적용 가능한 픽스. 2026-04-27 41장 데크 작업에서 실측한 패턴들.

---

## E1 — `Text element <p> has background`

**에러 메시지 예**:
```
Multiple validation errors found:
1. Text element <p> has background. Backgrounds, borders, and shadows are
   only supported on <div> elements, not text elements.
```

**원인**: `<p>` 또는 `<h*>` 에 inline `style="background:..."` 또는 클래스로 배경/보더/섀도우 적용.

**자주 발생하는 곳**:
- 표 셀의 하이라이트 컬럼:
  ```html
  <!-- ❌ -->
  <p class="t-body" style="padding: 10pt 14pt; text-align: center; background: rgba(70,51,227,0.06); font-weight: 600;">중</p>

  <!-- ✅ -->
  <div style="background: rgba(70,51,227,0.06); padding: 10pt 14pt;">
    <p class="t-body" style="text-align: center; font-weight: 600;">중</p>
  </div>
  ```
- 라벨 셀 (회색 배경):
  ```html
  <!-- ❌ -->
  <p class="t-cap" style="padding: 8pt 12pt; font-weight: 600; background: #F5F5F4;">캔버스</p>

  <!-- ✅ -->
  <div style="background: #F5F5F4; padding: 8pt 12pt;">
    <p class="t-cap" style="font-weight: 600;">캔버스</p>
  </div>
  ```

**일괄 픽스 패턴**: `<p ... style="...background:..."` 검색 → 외부 div 로 wrap.

---

## E2 — `DIV element contains unwrapped text "..."`

**에러 메시지 예**:
```
DIV element contains unwrapped text "Color Tokens"
```

**원인**: `<div>` 안에 `<p>/<h*>` 없이 맨텍스트 직접 작성.

**픽스**:
```html
<!-- ❌ -->
<div class="title">Color Tokens</div>

<!-- ✅ -->
<div class="title"><p class="t-title">Color Tokens</p></div>
```

---

## E3 — `CSS gradients are not supported`

**원인**: `linear-gradient` 또는 `radial-gradient`.

**자주 발생하는 곳**:
- placeholder frame (디자인 시스템의 .ph-frame):
  ```css
  /* ❌ */
  background: linear-gradient(135deg, var(--surface) 0%, var(--surface-alt) 100%);

  /* ✅ */
  background: #F5F5F4;
  ```
- bg-dots 패턴:
  ```css
  /* ❌ */
  background-image: radial-gradient(circle at 1px 1px, var(--border) 1px, transparent 0);

  /* ✅ — 그냥 삭제 (시각 손실 감수) */
  ```
- 그라디언트 글로우 / 캐릭터 뒤 후광:
  ```html
  <!-- ❌ -->
  <div style="background: radial-gradient(...); ..."></div>

  <!-- ✅ — 단색 원으로 대체 -->
  <div style="background: #E8E5FC; border-radius: 50%; width: 280pt; height: 280pt;"></div>
  ```

---

## E4 — `Background images on DIV elements are not supported`

**원인**: `<div style="background-image: url(...)">`.

**픽스**:
```html
<!-- ❌ -->
<div style="background-image: url('chart.png'); width: 300pt; height: 200pt;"></div>

<!-- ✅ -->
<img src="chart.png" style="width: 300pt; height: 200pt;">
```

---

## E5 — `HTML content overflows body by Xpt vertically`

**원인**: 콘텐츠가 540pt 캔버스를 넘어감.

**픽스 우선순위**:
1. 콘텐츠 줄이기 (불릿 6 → 4)
2. 폰트 사이즈 한 단계 작게 (`.t-title 14pt` → `.t-body 12pt`)
3. 섹션 분리 (한 슬라이드에 너무 많이 → 두 슬라이드로)
4. `padding/gap` 줄이기 (`gap: 24pt` → `gap: 14pt`)
5. **마지막 수단** body `overflow: hidden` 으로 잘라내기 (콘텐츠가 잘림 — 권장 X)

---

## E6 — `Text box "..." ends too close to bottom edge (X" from bottom, minimum 0.5" required)`

**원인**: 하단 absolute 텍스트의 bottom 값이 36pt (= 0.5″) 미만.

**픽스**: bottom 을 44pt 이상으로 (안전한 마진).

```html
<!-- ❌ -->
<div style="position: absolute; bottom: 30pt;"><p>FOOTER</p></div>

<!-- ✅ -->
<div style="position: absolute; bottom: 44pt;"><p>FOOTER</p></div>
```

---

## E7 — `Inline element <span> has margin-right which is not supported`

**원인**: inline `<span>` 에 margin 적용. PowerPoint 텍스트 런에는 margin 개념 없음.

**픽스**:
```html
<!-- ❌ -->
<p>Item <span style="margin-right: 6pt;">(1)</span>제목</p>

<!-- ✅ — &nbsp; 으로 간격 -->
<p>Item <span>(1)</span>&nbsp;제목</p>

<!-- ✅ — 공백 문자로 간격 -->
<p>Item <span>(1) </span>제목</p>
```

---

## E8 — `el.className.includes is not a function` (인라인 SVG 에러)

**원인**: 인라인 `<svg>` 안의 자식 요소 (`<path>`, `<circle>` 등) 의 className 은 `SVGAnimatedString` 타입이라 `.includes()` 메서드 없음. `html2pptx.js` 가 DOM 순회 중 폭발.

**픽스**: SVG 를 별도 .svg 파일로 빼고 `<img>` 로 참조.

```html
<!-- ❌ inline SVG -->
<svg width="32" height="32" viewBox="0 0 24 24"><path d="..."/></svg>

<!-- ✅ external SVG via img -->
<img src="../icons/arrow-right.svg" style="width: 28pt; height: 28pt;">
```

별도 .svg 파일 만들 때 root SVG에 `xmlns="http://www.w3.org/2000/svg"` 잊지 말 것.

---

## E9 — 이미지 경로 `Unable to read media`

**에러 예**:
```
Error: ENOENT: no such file or directory, open '/.../slides/design-system/assets/jangpm-character.png'
```

**원인**: 이미지 src 가 슬라이드 HTML 위치 기준이 아님. CSS 의 @import 와 달리 `<img src>` 는 HTML 파일 위치 기준.

**픽스**: 슬라이드는 `slides/` 폴더에 있고 디자인 시스템 자산은 `design-system/` 에 있으니 한 단계 위로:

```html
<!-- ❌ HTML이 slides/ 안에 있는데 design-system/ 으로 직접 -->
<img src="design-system/assets/jangpm-character.png">

<!-- ✅ ../ 로 한 단계 위 -->
<img src="../design-system/assets/jangpm-character.png">

<!-- icons/ 폴더도 마찬가지 -->
<img src="../icons/arrow-right.svg">
```

---

## E10 — `HTML dimensions don't match presentation layout`

**에러 예**:
```
HTML dimensions (12.0" × 6.7") don't match presentation layout (13.3" × 7.5") by more than 0.1"
```

**원인**: body 사이즈가 LAYOUT_WIDE (960pt × 540pt) 와 안 맞음.

**픽스**:
```css
/* ✅ 권장 */
body { width: 960pt; height: 540pt; }
```

`<html>` 에도 같은 사이즈 적용 권장 (overflow 방지):
```css
html { width: 960pt; height: 540pt; }
```

---

## E11 — 차트 SVG가 PowerPoint에서 깨진 이미지로 표시됨

**증상**: 슬라이드에서 `<img src="../icons/chart.svg">`로 외부 SVG를 참조한
deck을 빌드한 뒤 PowerPoint(특히 모바일/웹/일부 데스크톱)에서 열면 해당 차트
자리에 재로드 아이콘만 표시되고, "일부 PowerPoint 기능은 표시할 수 없으며..."
경고가 뜬다.

**원인**: PptxGenJS가 SVG 임베드를 위해 `image-N-1.png` (raster fallback) +
`image-N-2.svg` (벡터 원본) 두 멤버를 쓰는데, raster fallback을 sharp 등으로
생성하지 않고 같은 SVG XML 데이터를 .png 확장자로 저장한다. 그래서 PowerPoint
가 .png 멤버를 PNG로 디코드하려다 실패해 깨진 이미지로 표시된다. 추가로
디버깅 목적으로 SVG를 600 DPI(8.33×)로 raster하면 PNG가 2000px를 초과해
Anthropic API의 many-image dimension 한도(2000px)에 걸려 첨부 자체가 실패한다.

**픽스**: build.mjs가 빌드 직전에 자동으로 처리하므로 작성자는 신경쓰지
않아도 된다.

```js
// build.mjs (templates/build.mjs.template 에 포함됨)
import { prebuildSvg } from '../../.claude/skills/slide/scripts/prebuild-svg.mjs';
// ...
await prebuildSvg({ projectDir: __dirname });
```

prebuild는:
1. `icons/*.svg`를 sharp로 진짜 PNG raster (long edge 최대 1920px, 4× retina cap)
2. `slides/*.html` 내 `src="…/foo.svg"` 참조를 `src="…/foo.png"`로 in-place 치환
3. PNG가 SVG보다 새것이고 사이즈 제한 안에 있으면 raster 단계 skip (idempotent)

**수동 점검**:
```bash
unzip -p <deck>.pptx ppt/media/image-11-1.png | file -
# → "PNG image data, …" 이 나와야 정상.
# → "SVG"면 prebuild 가 적용 안 된 deck. build.mjs 에 prebuildSvg() 호출 누락.
```

E8(인라인 SVG 금지)에서 권장하는 "외부 .svg + img" 패턴을 그대로 써도 된다.
build.mjs가 raster 단계에서 .png로 변환하므로 작성자 입장에서는 SVG로 작업
가능.

---

## E12 — `Text elements overlap` (자동 패치 — 빌드 실패 안 함)

**감지**: 두 텍스트 요소(`<p>`/`<h*>`/`<ul>`)의 박스가 X 5pt + Y 8pt 초과로 겹침. 가장 흔한 패턴은 하단 `gm-band` 또는 contact box가 위 카드/콘텐츠 아래로 파고드는 경우.

**자동 패치** (`autoFixOverlaps` in `html2pptx.js`):

1. **그룹 빌드 (union-find)** — 각 요소를 "rigid group"에 배정.
   - shape(배경/border 있는 div) 안에 있는 텍스트는 outermost shape의 그룹에 합류.
   - 중첩된 shape (예: card 안의 circle) 도 outer shape의 그룹에 합류.
   - **same-row heuristic**: 작은 shape(circle/badge)와 같은 baseline (y center 4pt 이내) + 인접 (gap ≤ 14pt) 한 텍스트는 한 그룹으로 union — `<div class="row"><circle/><p/></div>` 패턴에서 wrapper에 background가 없어도 함께 움직이도록.
2. **Top-down 단일 패스** — 그룹들을 minY 오름차순으로 정렬하고 위에서 아래로 처리. 각 그룹은 자기 위에 있는 모든 그룹을 X-overlap 기준으로 검사 → 충돌 시 그룹 전체를 충분히 아래로 이동.
3. **upward shift 없음** — 항상 아래로만 이동하므로 진동(oscillation) 불가능.
4. **하단 안전선 초과 시** — 가능한 만큼만 shift 적용 + warning. 빌드는 계속 성공.

**Auto-fix 로그 예**:
```
[overlap auto-fix] slides/11-qa.html: Auto-fixed overlap: shifted "Q" group
down by 17.9pt.
```

**부분 패치 로그 예** (콘텐츠가 너무 많아 완전 해소 불가):
```
[overlap auto-fix] Partial auto-fix: shifted "..." group down by 12pt
(needed 30pt — 18pt of overlap remains; slide is overstuffed, trim content
in source HTML).
```

**왜 auto-patch가 안전한가**:
- 그룹 단위로 shift하므로 카드 박스와 안의 텍스트, circle과 라벨 텍스트가 함께 움직임 — 박스 밖으로 텍스트가 빠져나가지 않음.
- Containment(부모-자식 관계) 케이스는 사전 skip — `<ul><li><p>` 같은 false positive 없음.
- 빌드는 항상 성공 (slide 자체가 잘못된 경우만 partial-fix warning).

**HTML도 같이 고치고 싶으면**: warning 로그를 보고 해당 슬라이드의 충돌 요소 `top:` 또는 `padding:` 을 직접 손봄. (auto-fix는 PPT 출력만 보정하고 HTML은 미수정 — 매 빌드마다 같은 warning 이 뜸)

**제약**:
- 그룹은 shape 기반 + same-row heuristic 으로 구성. 깊게 중첩된 layout container(여러 단계 wrapper div without background)에서 형제 요소는 같이 움직이지 않을 수 있음. 이런 경우 wrapper에 임시 background 또는 명시적 위치 조정으로 강제 그룹화 가능.

---

## 자주 한꺼번에 다 잡히는 픽스 시나리오

빌드 결과가 `34/41 ✓ 7 ✗` 같은 부분 실패면, **실패 슬라이드 7개를 한 번에**:

1. 에러 메시지 그룹화 (어떤 에러 코드가 몇 번 발생했는지 카운트)
2. 가장 빈번한 에러 코드부터 픽스 (E1, E3 가 보통 다수)
3. 각 에러 코드별로 위 픽스 패턴 적용 (Edit 툴로 `replace_all` 활용)
4. 재빌드 → 보통 한 번에 다 통과

이번 (2026-04-27) 작업 통계:
- E1 (p에 background) × 3 슬라이드 (총 13곳)
- E6 (bottom edge) × 2 슬라이드
- E7 (span margin) × 2 슬라이드
- 한 번에 다 픽스 후 재빌드 → 41/41 통과 (총 빌드 시간 < 2분)
