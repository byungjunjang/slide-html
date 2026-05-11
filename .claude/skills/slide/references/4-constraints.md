# 4 Hard Constraints — html2pptx-safe HTML

editable PPTX 변환을 위해 모든 슬라이드 HTML이 반드시 통과해야 하는 4가지 제약. 이 룰은 이 번들의 `scripts/html2pptx.js`의 검증을 통과하기 위함이며, **PowerPoint 파일 포맷 (OOXML) 자체의 물리적 약속**을 HTML에 투영한 것이다 (도구가 게을러서가 아님).

---

## 룰 1: DIV에 맨텍스트 금지 — 텍스트는 `<p>` 또는 `<h1>~<h6>` 안에

```html
<!-- ❌ 잘못 -->
<div class="title">2026 Q3 매출 전망</div>

<!-- ✅ 맞음 -->
<div class="title"><h2>2026 Q3 매출 전망</h2></div>
<div class="body"><p>전년 대비 21% 성장</p></div>
```

**왜**: PowerPoint 텍스트는 반드시 text frame (`<a:txBody>`) 안에 존재. text frame 은 HTML 의 단락 레벨 요소 (p / h1~h6 / li) 에 매핑된다. 맨 div 는 PPTX 에서 대응되는 텍스트 컨테이너가 없다.

**`<span>` 도 단독 본문 텍스트 금지**: span 은 inline 요소라 독립된 텍스트 박스로 정렬 불가. `<p>` / `<h*>` 안에서 부분 스타일링 (굵게, 컬러 변경) 용도로만 사용.

---

## 룰 2: CSS 그라디언트 금지 (linear / radial 모두) — 순색만

```css
/* ❌ 잘못 */
background: linear-gradient(to right, #FF6B6B, #4ECDC4);
background-image: radial-gradient(circle at 1px 1px, var(--border) 1px, transparent 0);  /* dot pattern */

/* ✅ 맞음: 순색 */
background: #FF6B6B;

/* ✅ 다색이 필요하면: flex 자식 div 각자 순색 */
.stripe { display: flex; }
.stripe .left  { flex: 1; background: #FF6B6B; }
.stripe .right { flex: 1; background: #4ECDC4; }
```

**왜**: PowerPoint 의 shape fill 은 solid / preset gradient 만 지원. CSS 의 임의 각도/위치 그라디언트는 PPTX 그라디언트 문법으로 1:1 매핑 불가. `pptxgenjs` 의 `fill: { color: ... }` 는 solid 만 처리.

**자주 위반하는 곳**:
- `.bg-dots` 같은 radial-gradient 도트 패턴 → 삭제 또는 `<img>` 텍스처
- placeholder frame 의 `linear-gradient(135deg, #fff 0%, #f5f5f4 100%)` → 단색 `#F5F5F4`
- 캐릭터 뒤 그라디언트 글로우 → 단색 원 (`border-radius: 50%`)

---

## 룰 3: `<p>/<h*>` 에 background / border / shadow 금지 — 외부 div 가 담당

```html
<!-- ❌ 잘못 -->
<p style="background: #FFD700; border-radius: 4pt; padding: 8pt;">중요</p>

<!-- ✅ 맞음 -->
<div style="background: #FFD700; border-radius: 4pt; padding: 8pt;">
  <p>중요</p>
</div>
```

**왜**: PowerPoint 에서 shape (사각형/원형 라운드) 와 text frame 은 두 개의 별개 객체. HTML 의 `<p>` 는 text frame 으로만 변환 — 배경/보더/섀도우는 shape 속성이라 **반드시 text 를 감싸는 div 에** 적용.

**자주 위반하는 곳**:
- 표 셀 하이라이트: `<p style="background: rgba(...);">` → 외부 div + 안에 p
- 배지: `<p style="background: var(--accent);">badge</p>` → div가 배경, 안에 p
- "tag-style" 라벨: `<span style="background: var(--accent-soft); padding: ...">label</span>` → div + 안에 p

---

## 룰 4: DIV 에 `background-image` 금지 — `<img>` 태그 사용

```html
<!-- ❌ 잘못 -->
<div style="background-image: url('chart.png'); width: 300pt; height: 200pt;"></div>

<!-- ✅ 맞음 -->
<img src="chart.png" style="position: absolute; left: 50%; top: 20%; width: 300pt; height: 200pt;">
```

**왜**: `html2pptx.js` 는 `<img>` 요소에서만 image path 를 추출. CSS 의 `background-image: url(...)` 은 파싱하지 않는다.

**예외**: SVG dot pattern 같은 거 정말 필요하면 별도 .svg 파일로 만들고 `<img>` 로 임베드.

---

## 보너스 룰들 (validation 으로 잡히는 자잘한 것들)

### `inline <span>` 에 margin 금지

```html
<!-- ❌ 잘못 -->
<p>... <span style="margin-right: 6pt;">(1)</span>본문 ...</p>

<!-- ✅ 맞음 -->
<p>... <span>(1)</span>&nbsp;본문 ...</p>
```

inline 요소는 PowerPoint 텍스트 런 (text run) 에 매핑되는데, run 에는 margin 개념이 없음. 간격은 `&nbsp;` 또는 공백 문자로.

### body 사이즈 ±0.1″ 매칭

HTML body 의 computed width/height 가 pptxgenjs 의 layout 사이즈 (LAYOUT_WIDE = 13.333″ × 7.5″) 와 ±0.1″ 안에 일치해야 함.

```css
/* ✅ 권장: pt 단위 */
body { width: 960pt; height: 540pt; }

/* ✅ 등가: px (1pt = 4/3 px = 1.333px @ 96dpi) */
body { width: 1280px; height: 720px; }

/* ✅ 등가: inch */
body { width: 13.333in; height: 7.5in; }
```

### 하단 텍스트는 bottom ≥ 36pt (= 0.5″)

```html
<!-- ❌ 잘못: bottom 30pt — PowerPoint 가 0.5" 미만이면 잘릴 수 있음 -->
<div style="position: absolute; bottom: 30pt; ...">
  <p class="t-cap">FOOTER</p>
</div>

<!-- ✅ 맞음: bottom 44pt+ -->
<div style="position: absolute; bottom: 44pt; ...">
  <p class="t-cap">FOOTER</p>
</div>
```

PowerPoint 슬라이드 하단 0.5″ (36pt) 는 일부 디스플레이/프린터에서 잘릴 수 있음. validation 이 경고로 잡아준다.

---

## 통과 자가 점검 체크리스트

새 슬라이드 작성 후 빌드 전에:

- [ ] 모든 텍스트가 `<p>` 또는 `<h1>~<h6>` 안에 있다
- [ ] `linear-gradient` / `radial-gradient` 검색 결과 0개
- [ ] `<p style="...background...">` / `<h* style="...background...">` 검색 결과 0개
- [ ] `<div style="...background-image...">` 검색 결과 0개
- [ ] `<span style="...margin...">` 검색 결과 0개
- [ ] body 사이즈 = `960pt × 540pt`
- [ ] `position: absolute; bottom:` 값들이 모두 ≥ 36pt
- [ ] 콘텐츠가 540pt 안에 들어간다 (브라우저에서 file:// 로 열어 확인)

이 체크리스트를 통과하면 빌드는 99% 성공한다. 실패하면 `error-patterns.md` 참조.

---

## Layer 1 빌드 검증 (slide-plan systematic 경로)

`slide_plan.json`이 프로젝트 폴더에 있을 때만 적용. simple 경로는 4 hard constraint만 검사. `build.mjs`가 빌드 직전에 `validate_plan.py`를 호출한다.

| 규율 | 검사 | 위반 시 |
|---|---|---|
| **R2** — chart/table strategy ↔ takeaway 일체화 | `chart_strategy` 또는 `table_strategy`가 비어있지 않으면 대응 takeaway도 비어있을 수 없음 | exit 1 — 빌드 차단 |
| **R5** — evidence 매핑 의무 | 슬라이드의 `evidence_sources` 또는 `content_constraints.evidence_to_use` 중 하나는 non-empty | exit 1 — 빌드 차단 |
| R1 — 슬라이드별 사유 4 필드 | core_message / audience_takeaway / why_here / recommended_layout_family 채움 | stderr lint (빌드 진행) |
| R3 — 분량 압박 | slides 길이 1~20 권장 | stderr lint |
| R4 — Lazy 반복 금지 | 동일 layout_family 연속 3장 이상 | stderr lint |

검증기: `.claude/skills/slide-plan/scripts/validate_plan.py`. simple 경로는 `slide_plan.json` 부재만으로 자동 skip된다.
