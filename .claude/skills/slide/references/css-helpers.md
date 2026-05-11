# CSS Helpers Reference — `_pptx-slide.css`

`templates/_pptx-slide.css` 가 제공하는 헬퍼 클래스 전체 카탈로그. 이 클래스들은 모두 4 hard constraint 통과를 보장한다.

---

## 캔버스 / 레이아웃

| 클래스 | 용도 |
|---|---|
| `.pad` | 표준 패딩 (42pt 42pt 36pt 42pt). body 안 wrapper로 사용 가능 |
| `.pad-wide` | 표지/마감용 와이드 패딩 (42pt 56pt 56pt 56pt) |
| `.gm-band` | GM (Governing Message) 하단 1줄. position: absolute, bottom: 18pt |

`<body>` 자체가 `width: 960pt; height: 540pt` 로 고정되므로 wrapper 없이 직접 absolute positioning 가능.

---

## 카드 (Card)

| 클래스 | 배경 | 보더 | 용도 |
|---|---|---|---|
| `.card` | #FFFFFF | 1px #E5E7EB | 기본 카드 |
| `.card-accent` | #E8E5FC | 1px #4633E3 | 강조 카드 (페이지당 1개) |
| `.card-alt` | #F5F5F4 | 1px #E5E7EB | 그룹 카드 |
| `.card-dark` | #1A1A1A | none | 다크 카드 (안에 흰 텍스트) |

모두 `border-radius: 12pt`, `padding: 18pt 20pt`.

---

## 배지 (Badge)

| 클래스 | 모양 | 색 | 용도 |
|---|---|---|---|
| `.badge-accent-soft` | pill | accent-soft + accent text | 헤더 카테고리 라벨 |
| `.badge-accent` | pill | accent + 흰 text | 강조 라벨 |
| `.badge-dark` | pill | dark + 흰 text | 어둡고 강한 라벨 |
| `.badge-square` | 사각형 | accent + 흰 text | 실습/카테고리 큰 라벨 |
| `.number-circle` | 원 22pt | accent + 흰 text | 작은 번호 (1-99) |
| `.number-circle-lg` | 원 28pt | accent + 흰 text | 큰 번호 |

**중요**: 배지는 텍스트를 안에 넣을 때 반드시 `<p>` 안에. 예:
```html
<div class="badge-accent">
  <p class="t-cap c-white">SECTION 02</p>
</div>
```

---

## 디바이더 / 룰

| 클래스 | 용도 |
|---|---|
| `.rule` | 가로 1px 회색선 (E5E7EB) — 헤더 아래 디바이더 |
| `.rule-accent` | 가로 2pt 인디고선 — 강조 디바이더 |
| `.strip-accent` | 세로 3pt 인디고 strip — 좌측 accent 라벨용 (`::before` 대체) |

---

## 표 (Table) — div grid 방식

`<table>` 대신 div grid 사용 (html2pptx 가 더 안정적).

```html
<div style="display: grid; grid-template-columns: 2fr 1fr 1fr; background: #E8E5FC;">
  <p class="t-cap c-accent" style="padding: 8pt 12pt; font-weight: 700;">지표</p>
  <p class="t-cap c-accent" style="padding: 8pt 12pt; font-weight: 700; text-align: center;">2025</p>
  <p class="t-cap c-accent" style="padding: 8pt 12pt; font-weight: 700; text-align: center;">2026</p>
</div>
<div style="display: grid; grid-template-columns: 2fr 1fr 1fr; border-bottom: 1px solid #E5E7EB;">
  <p class="t-body" style="padding: 8pt 12pt;">매출</p>
  <p class="t-body" style="padding: 8pt 12pt; text-align: center;">48억</p>
  <p class="t-body" style="padding: 8pt 12pt; text-align: center;">58억</p>
</div>
```

**하이라이트 컬럼**: p에 직접 background 못 하므로 div wrap:
```html
<div style="background: rgba(70,51,227,0.06); padding: 8pt 12pt;">
  <p class="t-body" style="text-align: center; font-weight: 700;">58억</p>
</div>
```

zebra row 는 grid div 의 background 로 OK: `background: #FAFAF9;`.

---

## Placeholder / 프레임

| 클래스 | 용도 |
|---|---|
| `.ph-frame` | 회색 점선 프레임 (스크린샷 영역) |
| `.ph-frame-accent` | 인디고 점선 프레임 (강조 슬롯, after) |

배경은 순색 (`#F5F5F4` / `#E8E5FC`), 그라디언트 사용 안 함.

---

## 터미널 윈도우

```html
<div class="term-window">
  <div class="term-chrome">
    <div style="display: flex; align-items: center; gap: 4pt;">
      <div class="term-dot" style="background: #ff5f56;"></div>
      <div class="term-dot" style="background: #ffbd2e;"></div>
      <div class="term-dot" style="background: #27c93f;"></div>
      <p class="t-cap t-mono" style="color: #888; flex: 1; text-align: center;">~/path — zsh</p>
    </div>
  </div>
  <div class="term-body">
    <p class="t-mono" style="font-size: 9pt;"><span style="color: #27c93f;">$</span> <span style="color: #fff;">npm install</span></p>
    <p class="t-mono" style="color: #a8b1ba; font-size: 9pt;">added 21 packages</p>
  </div>
</div>
```

색상 가이드:
- 프롬프트 `$`: `#27c93f` (녹색)
- 명령어: `#fff`
- 출력: `#a8b1ba` (회색)
- 주석: `#6b7280`
- 키워드: `#7dd3fc` (시안)
- 문자열: `#fbbf24` (노랑)
- 성공: `#4ade80`
- 에러: `#f87171`

---

## 타이포그래피 클래스

모두 pt 단위로 고정 (px/rem 사용 안 함).

| 클래스 | 사이즈 | 굵기 | 용도 |
|---|---|---|---|
| `.t-display` | 42pt | 800 | 대표 타이틀 (title slide, big quote) |
| `.t-display2` | 36pt | 800 | 작은 디스플레이 |
| `.t-h1` | 30pt | 800 | 큰 헤드라인 |
| `.t-h2` | 24pt | 700 | 슬라이드 타이틀 |
| `.t-h3` | 18pt | 700 | sub-heading |
| `.t-title` | 14pt | 600 | 카드 타이틀, sub-label |
| `.t-body` | 12pt | 400 | 본문 |
| `.t-body-sec` | 12pt | 400 | 본문 secondary 색 |
| `.t-cap` | 9pt | 500 | caption / annotation |
| `.t-cap-up` | 9pt | 600 | UPPERCASE caption (라벨용) |
| `.t-mono` | inherit | inherit | 모노스페이스 폰트 (코드/경로) |

---

## 색 modifier

```html
<p class="t-body c-accent">악센트 텍스트</p>
<p class="t-body c-accent-ink">진한 악센트</p>
<p class="t-body c-secondary">회색 본문</p>
<p class="t-body c-tertiary">연한 회색</p>
<p class="t-body c-positive">+21%</p>
<p class="t-body c-negative">-3%</p>
<p class="t-body c-warning">주의</p>
<p class="t-body c-white">다크 배경 위 흰 텍스트</p>
```

배경 modifier도 있음: `.bg-accent`, `.bg-accent-soft`, `.bg-surface-alt`, `.bg-text` (모두 div 에만).

---

## 그리드 / 플렉스

| 클래스 | 용도 |
|---|---|
| `.grid-2` | 2 컬럼 |
| `.grid-3` | 3 컬럼 |
| `.grid-4` | 4 컬럼 (gap 14pt) |
| `.grid-5` | 5 컬럼 (gap 12pt) |
| `.grid-6` | 6 컬럼 (gap 12pt) |
| `.row` | flex row |
| `.col` | flex column |
| `.between` | justify-content: space-between |
| `.center` | align-items: center |
| `.gap-{1,2,3,4,5,6,8,10}` | gap 4/8/12/16/20/24/32/40pt |

---

## 자주 쓰는 패턴 코드 조각

### 슬라이드 헤더 (라벨 + 타이틀 + 디바이더)

```html
<div style="position:absolute; top:42pt; left:56pt; right:56pt;">
  <div class="row between" style="align-items: flex-end;">
    <div>
      <p class="t-cap-up" style="margin-bottom: 6pt;">02 · OVERVIEW</p>
      <h2 class="t-h2">디자인 시스템 구성 자산</h2>
    </div>
    <p class="t-cap c-tertiary">우측 보조 라벨</p>
  </div>
  <div class="rule" style="margin-top: 14pt;"></div>
</div>
```

### GM 하단 결론

```html
<div class="gm-band">
  <p class="t-body c-secondary" style="font-weight: 700;">하단 1줄 so-what 결론.</p>
</div>
```

### Insight bar (강조 박스)

```html
<div style="background: #E8E5FC; border-radius: 12pt; padding: 14pt 20pt; text-align: center;">
  <p class="t-body c-text"><b>Highlight</b> — 짧은 강조 메시지.</p>
</div>
```

### 페이지 카운터

```html
<div style="position: absolute; bottom: 44pt; right: 56pt;">
  <p class="t-cap-up" style="color: #6B7280;">12 / 41</p>
</div>
```
