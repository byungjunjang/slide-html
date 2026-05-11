# Text-formatting Rules — 슬라이드 텍스트 미세 서식 규칙

> 4 hard constraint(`4-constraints.md`)는 **PPTX 호환성**을 보장한다. anti-slop(`anti-slop.md`)은 **시각 다양성**을 보장한다. 본 문서는 **미세 서식 polish + 시각 완결성**을 보장한다 — 같은 어휘로 작곡해도 슬라이드 가독성·정렬·여백이 일관되게 깔끔하도록.
>
> LLM은 슬라이드 작성 시 anchor 보일러플레이트에서 chrome 골격을 가져온 다음, 본 문서 규칙을 self-check 한다.

---

## 1. 원형/배지 안 텍스트 (vertical centering)

`number-circle` / `number-circle-lg` / `badge-accent` / 작은 원형·pill 안 텍스트는 PPT에서 정확히 가운데 와야 한다.

### 규칙

```html
<!-- ✅ 권장 패턴 -->
<div class="number-circle-lg">
  <p class="t-cap c-white" style="line-height: 28pt; font-weight: 800;">01</p>
</div>

<div class="number-circle">
  <p class="t-cap c-white" style="line-height: 22pt; font-weight: 800;">1</p>
</div>

<!-- Q 표시같은 작은 원 -->
<div style="background: #4633E3; border-radius: 50%; width: 20pt; height: 20pt; text-align: center;">
  <p class="t-cap c-white" style="line-height: 20pt; font-weight: 800; font-size: 10pt;">Q</p>
</div>
```

### 작동 원리

- `<p>`의 `line-height` 가 컨테이너 높이와 같으면, html2pptx가 **자동으로 `valign: middle` + `lineSpacing = fontSize` (1.0)** 으로 변환 (auto-fix in `scripts/html2pptx.js`)
- 즉 line-height가 font-size의 1.5배 이상 + 박스 높이 ≈ line-height 인 single-line text는 PPT에서 정확히 vertical center
- 이걸 안 쓰면 text가 박스 상단 또는 살짝 하단으로 쏠림

### 컨테이너 크기별 line-height

| 컨테이너 | width × height | font-size | **line-height (의무)** |
|---|---|---|---|
| `number-circle` | 22pt × 22pt | 9pt | **22pt** |
| `number-circle-lg` | 28pt × 28pt | 9pt | **28pt** |
| 작은 원 (Q badge 등) | 20pt × 20pt | 10pt | **20pt** |
| 큰 원 (회사 로고 자리 등) | 36pt × 36pt | 12pt | **36pt** |
| `badge-accent`/`badge-accent-soft` | auto × auto (padding 5-6pt × 14pt) | 9pt (t-cap) | **9pt 명시 의무** — 외부 div padding이 위/아래 동일하면 textbox 안에서 자연 정렬되지만, html2pptx auto-fix 트리거를 위해 line-height = font-size 명시 권장. 누락 시 PPT에서 텍스트가 살짝 위로 쏠림 |

### number-circle과 같은 row의 다른 텍스트 (vertical center 정렬)

`number-circle` / `number-circle-lg` 옆에 같은 flex/grid row 안에서 `align-items: center`로 함께 배치되는 다른 텍스트(t-h3, t-title, t-body 등)에도 **`line-height: <원 height>` 명시 의무**. 누락 시 PPTX 변환 후 텍스트가 원과 vertical center로 정렬되지 않는다.

```html
<!-- ✅ 권장 -->
<div style="display: flex; gap: 10pt; align-items: center;">
  <div class="number-circle-lg" style="background: #1A1A1A;">
    <p class="t-cap c-white" style="line-height: 28pt; font-weight: 800;">01</p>
  </div>
  <p class="t-h3" style="line-height: 28pt;">Express</p>  <!-- 원 height와 동일 -->
</div>

<!-- ❌ 금지 (PPT에서 t-h3가 원과 정렬 안 됨) -->
<div style="display: flex; gap: 10pt; align-items: center;">
  <div class="number-circle-lg"><p ...>01</p></div>
  <p class="t-h3">Express</p>  <!-- line-height 없음 — vertical center 깨짐 -->
</div>
```

이 규칙은 **모든 작은 텍스트 박스에 동일** — pill 안 텍스트 (badge-accent), 원형 안 텍스트, number-circle 옆 라벨 텍스트 모두 line-height 명시. 자연 line-height (1.4)는 PPT 변환 시 valign middle 자동 적용을 트리거하지 못한다.

---

## 2. 본문 카드 텍스트 정렬

### 카드 padding

- `card` / `card-accent` / `card-alt` / `card-dark`: `18pt 20pt` 기본
- 변형 시 ±4pt 이내 (예: `padding: 16pt`, `padding: 22pt`)
- 카드 내부 첫 텍스트는 카드 top에서 18pt(padding) 떨어짐 — 이게 jangpm의 시그니처 호흡

### 카드 내 텍스트 vertical 정렬

- 카드 텍스트는 기본 **top-aligned** (PPT에서 자연 흐름)
- line-height: 1.5 (`t-body`) 또는 1.25 (`t-h3`) 이미 헬퍼 클래스에 박혀있음
- vertical-center 강제 안 함 — top-aligned 가 jangpm의 인쇄물 톤에 맞음

### 카드 사이 간격

- `grid-2`/`grid-3`: gap 18pt
- `grid-4`: gap 14pt
- `grid-5`/`grid-6`: gap 12pt

---

## 3. GM band (하단 인사이트 줄)

```html
<div class="gm-band">
  <p class="t-body c-secondary">한 줄 인사이트 메시지. <b class="c-text">키워드 강조</b>는 굵게.</p>
</div>
```

### 규칙

- `bottom: 18pt` 고정 (`.gm-band` CSS 헬퍼에 박힘)
- `text-align: center` 의무
- `t-body c-secondary` 디폴트 (12pt 회색)
- 키워드 강조는 `<b class="c-text">` (검정 굵게)
- 한 줄 한도 — 두 줄 넘어가면 카드로 격상

---

## 4. BR 처리 (제목·인용문 줄바꿈)

```html
<!-- ✅ 권장: 들여쓰기 공백 없이 BR 직후 다음 텍스트 -->
<h1 class="t-display">
  AI와 함께하는<br><span class="c-accent">업무 혁신</span>
</h1>

<!-- ⚠️ 동작은 함 (auto-fix가 처리): 들여쓰기 공백 -->
<h1 class="t-display">
  AI와 함께하는<br>
  <span class="c-accent">업무 혁신</span>
</h1>
```

- `html2pptx.js`의 BR 처리는 들여쓰기 공백을 자동 trim하고 `breakLine: true`로 변환 → 빈 paragraph 생성 안 함
- 작성 시 들여쓰기 안 하면 더 깔끔. 어느 쪽이든 결과는 동일하게 두 줄 (빈 줄 사이 없음)

---

## 5. 인라인 강조 (jangpm 시그니처)

### 키워드만 색 강조

```html
<!-- ✅ 권장: 인라인 span 으로 키워드만 accent 처리 -->
<h2 class="t-h2">메타적 접근은 <span class="c-accent">세 개의 루프</span>로 구성됩니다.</h2>

<!-- ✅ 굵기 강조 -->
<p class="t-body">프롬프트 결과를 평가하기 전에 <b class="c-text">나의 기대</b>부터 글로 적는다.</p>
```

### 규칙

- 슬라이드 타이틀(`t-h2`)에서 키워드 1개만 `c-accent` 인라인 — jangpm 시그니처
- 본문에서 굵기 강조는 `<b class="c-text">` (`t-body c-secondary` 위에서 검정으로 doubly contrast)
- accent inline span은 슬라이드당 1-2 events 한도 (모든 단어 accent → ❌)
- **inline `<span>`에 margin 절대 금지** (4 hard constraint 위반) — 줄바꿈/간격 필요시 `&nbsp;` 또는 별도 block 요소

---

## 6. 표지 우측 영역

```html
<!-- ✅ 권장: 캐릭터 이미지 또는 빈 공간 -->
<img src="../design-system/assets/jangpm-character.png" alt="Jangpm"
     style="position: absolute; top: 70pt; right: 60pt; width: 360pt; height: 360pt;">

<!-- ❌ 금지: halo / dot / 도형 데코 -->
<!-- 이전 세션에서 제거됨 — 어색해진다 -->
```

- 표지 (`01`/`23`/`25`) / closing (`21`) 의 우측 캐릭터 자리:
  - **캐릭터 이미지** 또는
  - **빈 공간**
- accent halo (큰 원), dark dot (작은 원), 기타 데코 도형 **금지**

---

## 7. Closing — light only (사용자 명시 규칙)

closing은 항상 `closing-light` (21-closing-light) 사용. **`closing-big` (22, 다크), `closing-dark` (08, 다크) 둘 다 사용 금지** — 데크 톤 무관, 모든 데크의 closing은 light 모드. 다양성은 closing-light 안의 body 변형(캐릭터 vs 빈 공간 / CTA vs 감사 / 메타 위치 등)으로 만든다.

---

## 8. 본문 폭 한도

- `t-h2` 슬라이드 타이틀: width 760pt (좌우 56pt 패딩에서)
- `t-body` 본문 1줄: ~50자 한글 한도. 50자 넘기면 줄바꿈 또는 카드 분리
- `t-cap` 캡션: 9pt 미만 절대 금지 (PPTX 가독 하한)

---

## 9. 색·accent 사용 빈도

- 슬라이드 1장 내 `c-accent` events: **1-2 한도**
  - "events" 정의: 같은 색의 인접한 영역(인라인 span / 카드 / 라벨)을 1 event로 셈
- semantic 색(`c-positive`/`c-negative`/`c-warning`): **데이터·트렌드 표시 전용**. 일반 강조에 ❌
- 다크 배경(`bg-text` / `card-dark`): closing 또는 terminal 슬라이드만

---

## 10. 자기 검증 체크리스트 (작성 마무리 시)

각 슬라이드 작성 후, 빌드 직전:

- [ ] 원/badge 안 텍스트 line-height = 컨테이너 height 와 일치
- [ ] **number-circle 같은 row 안 다른 텍스트(t-h3, t-title 등)에도 line-height = 원 height 명시** (vertical center 정렬)
- [ ] **요소 간 좌표 오버랩 없음** — §11 오버랩 자기 점검 표 통과
- [ ] 카드 padding 18pt 20pt (또는 ±4pt 이내)
- [ ] gm-band 가 있으면 bottom: 18pt + text-align: center
- [ ] BR 직후 들여쓰기 공백 OK (auto-fix 처리되지만 깔끔하게)
- [ ] 슬라이드 타이틀에 키워드 1개 c-accent 인라인 (jangpm 시그니처)
- [ ] inline span에 margin 없음
- [ ] 표지 우측 도형 데코 없음 (캐릭터 또는 빈 공간만)
- [ ] closing은 항상 `closing-light` (다크 closing 사용 금지)
- [ ] 본문 1줄 ≤ 50자 한글
- [ ] accent events 슬라이드당 1-2

데크 전체에서:

- [ ] chrome (top eyebrow + page counter + .rule) 모든 본문 슬라이드 동일
- [ ] 본문 슬라이드 chrome이 anchor 보일러플레이트와 일치

---

## 11. 오버랩 자기 점검 (좌표 충돌 방지)

PPTX 변환은 모든 요소를 절대 좌표로 펼친다. HTML에서 flex/grid 자연 흐름이라도 PPTX에서는 좌표가 고정되므로, **`position: absolute`로 둔 블록들이 콘텐츠 길이 변동에 의해 다른 absolute 블록과 오버랩될 수 있다**. 빌드 직전 반드시 점검한다.

### 검증 절차

1. 슬라이드의 모든 `position: absolute` 블록을 나열한다.
2. 각 블록의 **시작 좌표**(top)와 **콘텐츠 기반 끝 좌표**(top + 콘텐츠 추정 height)를 계산한다.
3. 인접한 블록의 (이전 끝) ≤ (다음 시작) 관계가 성립하는지 확인. **갭이 0 또는 음수면 오버랩**.
4. 콘텐츠가 `overflow` 가능성 있을 때(텍스트 길이가 가변적, `flex: 1`/`grid auto`로 폭이 자동), **콘텐츠 최악-케이스 height**(2줄 본문, 3줄 인용 등)로 계산.

### 콘텐츠 height 추정 가이드

| 콘텐츠 | height 추정 |
|---|---|
| `t-h2` 한 줄 (24pt × line 1.05) | ≈ 26pt (2줄이면 50pt) |
| `t-h3` 한 줄 (18pt × line 1.25) | ≈ 23pt (2줄이면 45pt) |
| `t-body` 한 줄 (12pt × line 1.5) | ≈ 18pt (2줄이면 36pt) |
| `t-cap` 한 줄 (9pt × line 1.4) | ≈ 13pt |
| `t-cap-up` 한 줄 (9pt × line 1.4) | ≈ 13pt |
| 카드 (padding 18pt 20pt) | padding 36pt + 콘텐츠 + 갭 |
| `pull-quote` (padding 14-16pt 22pt + 따옴표 + 인용 + attribution) | 95-130pt (인용 1-2줄에 따라) |
| `number-circle-lg` 행 (정렬 center) | ≈ 28pt + 카드 padding |

### 본문 폭 → 줄 수 추정

`t-body` (12pt) 폭에서 한 줄 자수 = `폭 / 12pt × 1.0` 한글 / `폭 / 6pt` 영문 (대략):

| 폭 | t-body 한 줄 한글 |
|---|---|
| 220pt | ~18자 |
| 400pt | ~33자 |
| 700pt | ~58자 |
| 760pt | ~63자 |

**한글 50자 넘으면 두 줄** 보수 가정.

### 자주 나오는 오버랩 패턴 (발생 시 fix)

- ❌ **본문 텍스트 길이가 길어 row가 커지는데 다음 absolute 블록이 고정 좌표** → row 본문 1줄로 압축 또는 다음 블록 좌표를 콘텐츠 max-height 기준으로 재계산
- ❌ **타이틀 직후 intro 단락 + 큰 콘텐츠 블록이 모두 들어감** — intro 단락이 공간을 잡아먹으면 콘텐츠 끝이 다음 블록(strip / gm-band)와 오버랩. 콘텐츠가 길면 **intro 단락 삭제로 공간 확보 권장**
- ❌ **pull-quote 박스 height를 padding 기준으로 추정 안 하고 좌표 고정** — 인용이 2줄이 되면 박스 끝이 BOTTOM block 시작과 충돌. pull-quote 박스 height = padding + 따옴표 + 인용 줄 수 × 24pt + attribution + margin으로 미리 계산
- ❌ **gm-band(bottom 18pt)와 마지막 absolute 블록 끝점 오버랩** — 마지막 블록 끝 ≤ 504pt 권장 (gm-band 2줄 한도)

### 오버랩 발생 시 fix 우선순위

1. **콘텐츠 압축** — 본문 1줄 한도, 인용 압축
2. **intro/sub-headline 삭제** — 공간 확보 (사용자 명시 허용)
3. **다음 블록 좌표 늘림** — top 값을 콘텐츠 max-height 기준 재계산
4. **블록 자체 삭제** — strip 등 부가 정보가 핵심 콘텐츠와 충돌하면 삭제 후 gm-band로 결론 통합

빌드 통과한다고 오버랩 없는 게 아니다 — `node build.mjs`의 4 hard constraint는 텍스트 위치만 검증하지 박스 간 좌표 충돌은 검증하지 않는다. **이 §11 self-check가 LLM의 책임**.
