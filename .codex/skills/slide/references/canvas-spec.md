# Canvas Spec — 960pt × 540pt (LAYOUT_WIDE)

editable PPTX 의 모든 슬라이드는 **960pt × 540pt** 캔버스에서 작업한다. PowerPoint 기본 widescreen 규격 (LAYOUT_WIDE) 과 1:1 매칭.

## 캔버스 크기 환산표

| 단위 | 가로 | 세로 |
|---|---|---|
| **pt** (point, 권장) | 960pt | 540pt |
| **px** (96dpi) | 1280px | 720px |
| **inch** (PowerPoint 표준) | 13.333″ | 7.5″ |
| **EMU** (OOXML 내부 단위) | 12,192,000 | 6,858,000 |

환산: `1pt = 4/3 px = 1/72 in = 12,700 EMU`

## body 선언

```css
/* ✅ 권장: pt — 직관적이고 PowerPoint와 같은 단위 */
body { width: 960pt; height: 540pt; }

/* ✅ 등가: px — 웹 익숙한 사람용 */
body { width: 1280px; height: 720px; }

/* ✅ 등가: inch — 인쇄 익숙한 사람용 */
body { width: 13.333in; height: 7.5in; }
```

`html2pptx.js` 의 `validateDimensions()` 가 ±0.1″ 안에 일치 확인.

## pptxgenjs layout 매칭

```javascript
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';  // 13.333" × 7.5", 자동 매칭
```

`build.mjs` 가 이미 이 설정으로 호출하므로 수동 설정 불필요.

## 안전 영역 (Safe Margins)

```
┌─────────────────────────────────────────────────┐  ← top edge
│ ↕ 42pt (top padding)                            │
│ ┌───────────────────────────────────────────┐   │
│ │  안전한 콘텐츠 영역                          │   │
│ │  너비: 848pt (= 960 - 56*2)                │   │
│ │  높이: 462pt (= 540 - 42 - 36)             │   │
│ │ ←─ 56pt left/right padding ─→              │   │
│ │                                            │   │
│ │                                            │   │
│ │                                            │   │
│ │  ··· GM band (bottom: 18pt) ···            │   │
│ │ ↕ 36pt (bottom padding)                    │   │
│ └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘  ← bottom edge
```

**중요한 마진**:
- 좌우 56pt: 콘텐츠 시작/끝 위치
- 상단 42pt: 헤더 시작 위치
- 하단 36pt 이상: PowerPoint 가 잘릴 수 있는 영역, **bottom 값은 44pt+ 권장**
- GM (governing message) 는 `bottom: 18pt` 에 배치되며 36pt 룰의 예외 (스킬이 위치 보정 알고 있음)

## 좌표 시스템

CSS `position: absolute` + pt 단위 사용. 원점은 좌상단.

```html
<!-- 헤더: 좌상단 -->
<div style="position:absolute; top: 42pt; left: 56pt;">...</div>

<!-- 우상단 라벨 -->
<div style="position: absolute; top: 42pt; right: 56pt;">...</div>

<!-- 좌하단 푸터 -->
<div style="position: absolute; bottom: 44pt; left: 56pt;">...</div>

<!-- 우하단 페이지 번호 -->
<div style="position: absolute; bottom: 44pt; right: 56pt;">...</div>

<!-- 캔버스 중앙 영역 -->
<div style="position: absolute; top: 100pt; left: 56pt; right: 56pt;">...</div>
```

## 폰트 사이즈 가이드 (캔버스 비율 고려)

`templates/_pptx-slide.css` 의 시멘틱 클래스 사용 권장. 임의 px/rem 사용 X.

| 클래스 | 사이즈 | 캔버스 대비 |
|---|---|---|
| `.t-display` | 42pt | 7.8% (큰 표지용) |
| `.t-h1` | 30pt | 5.6% (큰 헤드라인) |
| `.t-h2` | 24pt | 4.4% (슬라이드 타이틀 — **주력**) |
| `.t-title` | 14pt | 2.6% (카드 타이틀) |
| `.t-body` | 12pt | 2.2% (본문 — **주력**) |
| `.t-cap` | 9pt | 1.7% (caption / 라벨) |

**경험칙**:
- 슬라이드당 .t-h2 (헤드라인) 1개
- 본문은 .t-body (12pt) 기본, 강조는 .t-title (14pt)
- 9pt 미만은 사용하지 말 것 (프로젝터에서 안 보임)

## 슬라이드 종횡비 비교

| 종횡비 | pt 사이즈 | 비고 |
|---|---|---|
| **16:9 (LAYOUT_WIDE)** | **960 × 540** | **이 스킬이 사용** |
| 4:3 (LAYOUT_STD) | 720 × 540 | 옛날 PowerPoint, 사용 안 함 |
| 16:10 (LAYOUT_LAYOUT) | 960 × 600 | 비표준 |

이 스킬은 LAYOUT_WIDE 만 지원. 다른 종횡비가 필요하면 별도 작업 필요 (희귀 케이스).
