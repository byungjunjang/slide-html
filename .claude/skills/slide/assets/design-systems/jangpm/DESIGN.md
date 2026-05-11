---
preset: jangpm
display_name: Jangpm
generated_by: manual_backfill (Phase 0 of slide-plan introduction)
schema_version: 1.0
status: confirmed
---

# Jangpm · DESIGN.md

> Layer 3 산출물 (slide-plan introduction guide §Layer 3). 이 문서는 jangpm preset의 **편집·기획 의도**를 박제한 SSOT — slide-plan은 이 어휘로 `recommended_layout_family`를 채우고, `/slide` simple 경로의 LLM도 이를 참조해 layout 일관성을 유지한다.
>
> Token·CSS·boilerplate는 자동 산출물이고, 이 문서는 그 위에 얹는 **편집 규약**이다.

---

## 1. Visual theme & atmosphere

한국어 강의·리포트 데크. **에디토리얼·분석적·선언형**. 슬라이드는 발표자가 무대에서 쳐다보는 매체가 아니라 **혼자 읽어도 결론까지 도달하는 인쇄물**에 가깝다.

- 색은 단조로움(monochrome warm off-white) + 인디고 단일 악센트.
- 무드는 SaaS 마케팅 데크가 아니라 **컨설팅 보고서·신문 분석면**.
- 정보 밀도는 중간~높음 (한 슬라이드에 여러 카드 그리드 OK), 단 텍스트는 항상 `t-body` 12pt 이상 가독 우선.
- "발표용 큐 카드"가 아니라 "독립적으로 읽히는 페이지"로 설계.

---

## 2. Palette & contrast behavior

### 토큰 (출처: `colors_and_type.css`, `_pptx-slide.css`)

| 그룹 | 토큰 | Hex | 사용 규칙 |
|---|---|---|---|
| 배경 | `--bg` | `#FAFAF9` | 페이지 디폴트. 거의 모든 슬라이드 background |
| 배경 | `--surface` | `#FFFFFF` | 카드·컨테이너 |
| 배경 | `--surface-alt` | `#F5F5F4` | 그룹된 sub-블록, placeholder 프레임 |
| 텍스트 | `--text` | `#1A1A1A` | 본문. **순수 #000 사용 금지** |
| 텍스트 | `--text-secondary` | `#6B7280` | 부연·메타 |
| 텍스트 | `--text-tertiary` | `#9CA3AF` | 캡션·페이지 카운터 |
| 라인 | `--border` | `#E5E7EB` | 카드 테두리·divider |
| 라인 | `--border-strong` | `#D4D4D4` | 강한 divider, dashed placeholder |
| 악센트 | `--accent` | `#4633E3` | 인디고-바이올렛. **슬라이드당 1~2 events**만 사용 |
| 악센트 | `--accent-soft` | `#E8E5FC` | 악센트 tinted bg, badge, 표 헤더 |
| 악센트 | `--accent-ink` | `#2E1FB3` | accent 강조형 |
| 데이터 | `--positive` `#059669` / `--negative` `#E11D48` / `--warning` `#D97706` | (소프트 페어 동봉) | **데이터 표시 전용**. 일반 텍스트 강조에는 금지 |

### 대비·악센트 규칙

- **악센트는 한 슬라이드에 1~2 events만.** 헤드라인 안의 키워드 1개 + 카드 강조 1개 정도가 한계. 모든 카드를 악센트로 칠하지 말 것.
- semantic 색(positive/negative/warning)은 **숫자·데이터·트렌드 표시 전용**. "이 단어 강조하고 싶다" 용도로 negative red를 쓰지 말 것.
- accent-soft 위에 accent-ink 텍스트는 OK. accent 위에는 white(`c-white`).
- 다크 카드(`card-dark`, `bg-text`) 위에는 모든 텍스트가 `c-white` 또는 `c-bg`.

---

## 3. Typography hierarchy

폰트: **Pretendard 9 weights** (Thin~Black). 한글 우선, 영문은 자동 fallback.

### Pt scale (`_pptx-slide.css` 기준 — 캔버스 960×540pt에 calibrated)

| 클래스 | size | weight | 사용 |
|---|---|---|---|
| `.t-display` | 42pt / 800 | line 1.05, ls -1pt | 표지 메인 |
| `.t-display2` | 36pt / 800 | | 표지 서브, kpi 큰 숫자 |
| `.t-h1` | 30pt / 800 | | section divider 헤드 |
| `.t-h2` | 24pt / 700 | | **본문 슬라이드 타이틀 디폴트** |
| `.t-h3` | 18pt / 700 | | 서브헤드, 카드 메인 |
| `.t-title` | 14pt / 600 | | 카드 타이틀, 표 헤드 |
| `.t-body` | 12pt / 400 | line 1.5 | **본문 디폴트** |
| `.t-body-sec` | 12pt / 400 secondary | | 부연 |
| `.t-cap` | 9pt / 500 | | 캡션·메타 |
| `.t-cap-up` | 9pt / 600 uppercase, ls 0.4pt | | section eyebrow ("Section 02 · 핵심") |

### 규칙

- **타이틀은 항상 `<h*>` 태그**, 본문은 `<p>`. div 안에 raw 텍스트 두지 말 것 (4 hard constraint R1).
- `.t-h2`(24pt) 슬라이드 타이틀에 **인라인 span으로 키워드만 `c-accent`**: jangpm의 시그니처 패턴.
  ```html
  <h2 class="t-h2">메타적 접근은 <span class="c-accent">세 개의 루프</span>로 구성됩니다.</h2>
  ```
- 본문 1줄당 ~50자 한글. 50자 넘기면 강제 줄바꿈하거나 카드 분리.
- 캡션 9pt 미만 금지. 9pt가 PPTX 가독 하한.

---

## 4. Spacing & density

8px grid. 토큰 `--space-1`~`--space-16` (4px~64px).

### 핵심 간격

- **슬라이드 패딩**: `.pad` = `42pt 42pt 36pt 42pt` (좌우 동일, 하단 약간 좁게 — bottom edge 안전 마진 위해)
- **카드 padding**: `18pt 20pt`
- **카드 grid gap**: `14pt`(grid-4) ~ `18pt`(grid-2/3)
- **bottom edge 안전 마진**: 모든 콘텐츠는 bottom으로부터 ≥ 36pt (gm-band 자리 보호)

### 밀도 규칙

- grid-2: 카드 2개 / 페어 컨셉 / 좌우 비교
- grid-3: 3-point 패턴
- grid-4: overview, kpi, 6-point의 상단 행
- grid-5/6: dense kpi-dashboard, 표 셀
- 한 슬라이드의 grid 깊이는 최대 2단 (grid 안의 grid). 3단 이상은 디자인 실패.

---

## 5. Visual vocabulary — compose, don't copy

이 섹션은 **시각 주역(visual main-character) 어휘**다. 슬라이드는 보일러플레이트 카탈로그에서 "복사"하는 게 아니라, 이 어휘에서 골라 jangpm 토큰으로 **즉흥 작곡**한다.

**위상**: 보일러플레이트 37장은 어휘의 일부 — "메뉴"가 아니라 "참고 갤러리". 어휘 항목 옆에 매칭되는 보일러플레이트가 있으면 링크하지만, 보일러플레이트가 없거나 살짝 다른 변형을 원하면 jangpm 토큰(`colors_and_type.css` + `_pptx-slide.css`)으로 **새로 작곡**한다 (4 hard constraint만 통과).

### 6 카테고리

데크의 시각 다양성은 **카테고리 간 분포**에서 나온다. 한 데크에 모든 카테고리가 골고루 등장하면 톤은 jangpm 그대로 유지되면서 슬라이드별 인상은 다르다.

| 카테고리 | 목적 | jangpm에서 권장 빈도 (12장 데크 기준) |
|---|---|---|
| **A. Hero / Impact** | 한 페이지 전체로 강한 메시지 — 큰 인용·큰 숫자·큰 타이포 | **1-2장 (의무)** |
| **B. Visual-Primary** | 시각 자체가 메시지 — 다이어그램·이미지·관계도·UI 캡쳐 | **2-3장 (의무)** |
| **C. Editorial** | 잡지·신문 톤 — 마진 노트·드롭캡·인라인 풀쿼트 | 1-2장 (선택) |
| **D. Density** | 정보 밀도 — 카드 그리드·KPI·표 | **3-4장 (백본)** |
| **E. Sequence** | 시간 흐름 — process·timeline·agenda | 1-2장 |
| **F. Narrative** | 데크 흐름 마디 — cover·section-divider·summary·closing | **3-4장 (백본)** |

**카테고리 분포 검증** (anti-pattern §10에서 강제):
- ❌ Hero/Impact 0장 데크 — "120% 다듬은 hero 슬라이드 없음 = 데크 임팩트 0"
- ❌ Visual-Primary 0장 데크 — 텍스트만 N장 = 단조
- ❌ Density 카테고리만으로 채워진 데크 — "카드 그리드 12장" 안티패턴
- ❌ 같은 카테고리 연속 3장 이상

---

### Category A · Hero / Impact (의무 1-2장)

한 페이지 전체로 한 가지 강력한 메시지를 던진다. 데크의 "120% 다듬은 한 장"이 여기서 나온다. 풀블리드 또는 90%+ 화면 점유.

| 어휘 | 언제 쓰는지 | **anchor 보일러플레이트** (chrome 골격 의무 복사) | body 작곡 가이드 (이 영역만 자유) | **변형 영감 (1개 이상 적용 권장)** |
|---|---|---|---|---|
| `mega-quote` | 명제·테제·결론 한 줄을 전 데크에서 가장 큰 글자로 박는 슬라이드 | **`18-quote-attribution`** (밝음) 또는 **`07-quote-section`** chrome. attribution 영역 그대로 사용 (다크 chrome 빌리지 말 것 — closing-light only 규칙과 일관) | 인용 텍스트만 `t-display` 50-72pt로 격상. accent는 키워드 1개 인라인 span. attribution은 `t-cap c-secondary` 그대로 | • 좌측 정렬 vs 가운데 정렬 선택<br>• 인용 위 작은 attribution + 아래 큰 인용 (역순 패턴)<br>• 키워드 1개만 c-accent 인라인<br>• 인용 옆 작은 supporting metric 동반<br>• 좌측 작은 portrait + 우측 큰 인용 split<br>• 인용 위 .rule-accent 짧은 강조선 |
| `mega-number` | 단일 KPI 또는 집약 수치를 페이지 전체로 강조 — "70%", "×2.3", "3개월" | **`16-stats`** — chrome (top eyebrow + page counter + .rule + 옵션 gm-band) 그대로 | KPI 영역만 `t-display` 80-120pt 단일 숫자로 교체. 단위 0.55em. 다른 KPI 카드 제거. 한 줄 컨텍스트는 `t-h3` 또는 `t-body` | • 숫자 좌측 + 컨텍스트 단락 우측 split<br>• 숫자 위 작은 라벨 + 아래 인용/설명<br>• 숫자 옆 trend `↑↓` 화살표<br>• 숫자 안 sub-unit 0.55em (예: "70%"의 "%")<br>• 숫자 + 4 supporting KPI strip 아래에 추가<br>• 숫자에 sparkline-like underline accent |
| `dramatic-type` | 단어/구절을 타이포 자체로 시각화 — line-break를 의도적으로 강조 | **`02-overview`** chrome 간소화 (top eyebrow + page counter만, .rule 생략 가능). 다크 chrome 빌리지 말 것 — light 톤 유지 | body 영역만 `t-display` 40-60pt + line-height 0.95-1.05 + `<br>` 패턴. 키워드만 `c-accent`. 다른 시각 요소 없음 | • 단어별 다른 weight (Pretendard 9 weights 활용)<br>• 단어별 size variation (40pt → 60pt 점진)<br>• 좌측 정렬 vs 가운데 정렬<br>• 단어 사이 .rule-accent 구분선<br>• 한 단어만 c-accent 강조<br>• ls 변주 (-1pt vs 0.5pt) |
| `full-bleed-image-with-overlay` | 풀블리드 이미지 + 텍스트 overlay (제품 사진·풍경·인물) | **`36-image-1up`** chrome — 이미지 자리 풀블리드로 확장 | `<img>` 풀블리드 + 어두운 반투명 단색 div overlay (rgba(26,26,26,0.55)) + `<p class="c-white">`. 그라데이션 금지 | • overlay 위치: 전면 vs 좌하단 vs 우상단 박스만<br>• overlay 농도: 0.45 vs 0.55 vs 0.7<br>• 텍스트 좌측 정렬 + 하단 attribution<br>• 큰 인용 + 작은 supporting label<br>• KPI 한 개 inline (예: "+38%")<br>• 흰 .rule-accent 강조선 추가 |
| `bold-statement-split` | 좌측 50%에 큰 선언, 우측은 단일 디테일 또는 빈 공간 | **`25-cover-vertical`** chrome + 좌우 split 비율 | 좌: `t-display 36-50pt` + accent 키워드. 우: 작은 메타 또는 jangpm-character / 빈 공간 (도형 데코 금지 — §9 규칙) | • 좌 dark + 우 light split (대비 강도 ↑)<br>• 좌측 statement + 우측 supporting bullet 3개<br>• 좌 t-display + 우 작은 visual (image/diagram)<br>• 좌측 단언 + 우측 reasoning 단락<br>• 좌 60% / 우 40% 비대칭 비율<br>• 좌측 위 small eyebrow + 큰 statement |

---

### Category B · Visual-Primary (의무 2-3장)

시각이 주역. 텍스트는 visual을 설명하거나 라벨링.

| 어휘 | 언제 쓰는지 | **anchor 보일러플레이트** (chrome 골격 의무 복사) | body 작곡 가이드 (이 영역만 자유) | **변형 영감 (1개 이상 적용 권장)** |
|---|---|---|---|---|
| `annotated-screenshot` | 제품·UI·결과물 캡쳐를 큰 이미지로 두고 4-6개 화살표·라벨 callout | **`36-image-1up`** chrome | 이미지 영역에 `<img>` 60-70% + 외부 callout 라벨(`t-cap` + 1pt accent line). 라벨은 div로 위치, 텍스트는 `<p>` 안. 화살표는 `.rule-accent` 또는 prebuildSvg된 PNG | • 이미지 좌측 60% + 우측 라벨 컬럼 (방사형 대신 정렬형)<br>• 라벨 1개만 card-accent 강조 (key insight)<br>• 라벨에 number-circle 부착 (1·2·3)<br>• 이미지 위쪽 큰 takeaway + 아래 callouts<br>• 라벨 그룹화 (전/후 / 좌/우)<br>• 이미지 둘레 dashed border 강조 |
| `single-portrait-quote` | 큰 인물 사진 좌측 + 인용·증언 우측 | **`23-cover-with-character`** chrome 좌우 split 비율 | 좌: `<img>` 35-45% 풀높이. 우: `t-h3` 인용 + `t-cap c-secondary` 속성 | • 좌 35% + 우 65% vs 좌 50% + 우 50%<br>• 인용 위에 큰 따옴표 mark (c-accent 60pt)<br>• 인용 아래 KPI 한 개 (인물 성과 metric)<br>• 인물 옆 작은 c-accent vertical bar<br>• 인용 일부 c-accent inline 강조<br>• 우측 위 attribution + 아래 큰 인용 (역순) |
| `diagram-as-hero` | 노드+화살표 다이어그램이 슬라이드 메인 | **`36-image-1up`** chrome | 이미지 자리에 외부 SVG → PNG (prebuildSvg). 라벨은 다이어그램 밖에 별도 `<p>`. div 합성 fallback 가능하지만 외부 SVG 권장 | • 다이어그램 + 우측 1줄 takeaway 컬럼<br>• 다이어그램 위 큰 statement + 아래 visual<br>• 노드 한 개만 accent-soft fill 강조<br>• 다이어그램 + 하단 sub-step 라벨 strip<br>• 좌측 컨텍스트 단락 + 우측 다이어그램 split<br>• 다이어그램 둘레 .rule frame |
| `before-after-split` | 좌우 split + 가운데 화살표/구분 — "변화 전" vs "변화 후" | **`14-comparison`** chrome + `grid-2` split | body만: 좌측 `card` (전 상태) / 가운데 `→` 화살표 / 우측 `card-accent` (후 상태). 카드 padding 18pt 20pt 그대로 | • 가운데 화살표 + KPI 변화량 (예: "+38%")<br>• 좌 dark card + 우 light card-accent (대비 강도)<br>• 카드 안 sub-bullet 3개씩 비교 row<br>• 가운데 vertical .rule + 양쪽 자유 leyout<br>• 위 1줄 takeaway gm-band 추가<br>• 좌·우 카드 위에 eyebrow ("BEFORE" / "AFTER") |
| `image-with-callouts` | 한 큰 이미지 + 4-6 callout이 이미지 주변에 분포 | **`36-image-1up`** chrome | 이미지 50-60% + 주변 `t-cap` 라벨 박스. 라벨에서 이미지로 향하는 미세 line은 div border | • callouts 4 cardinal (상하좌우) vs 한쪽 정렬<br>• callout 1개만 card-accent로 hero<br>• callout에 number-circle 추가<br>• 이미지 위 큰 takeaway 헤드<br>• 이미지 둘레 dashed border + ".key area" 표기<br>• callouts 그룹화 (좌측 = 문제 / 우측 = 해결) |
| `knowledge-graph` | 개념 간 관계도 — 노드 + 연결선 (관계·의존·흐름) | **`36-image-1up`** chrome | 외부 SVG → `<img>` 임베드. 라벨은 SVG 안 또는 absolute `<p>` overlay | • 그래프 + 우측 핵심 노드 라벨 컬럼<br>• 중심 노드만 accent fill 강조<br>• 그래프 위 1줄 takeaway 헤드<br>• 그래프 아래 sub-cluster 라벨 strip<br>• 좌측 narrative 단락 + 우측 그래프 split<br>• 노드 색 강도 differ (중요도 layer) |
| `image-2up-comparison` | 두 이미지 나란히 비교 | **`37-image-2up`** 그대로 | body의 두 이미지·캡션만 교체 | • 가운데 vs/→ 마커 추가<br>• 한쪽 이미지에 c-accent border<br>• 위 1줄 takeaway + 아래 이미지<br>• 캡션에 KPI metric 동반<br>• 두 이미지 아래 통합 결론 한 줄<br>• 이미지 1개만 풀높이 + 다른 1개 보조 |

---

### Category C · Editorial (선택 1-2장)

잡지·신문 톤. 책처럼 "읽히는" 페이지. jangpm의 "에디토리얼·인쇄물" 정체성을 강하게 드러내는 카테고리.

| 어휘 | 언제 쓰는지 | **anchor 보일러플레이트** (chrome 골격 의무 복사) | body 작곡 가이드 (이 영역만 자유) | **변형 영감 (1개 이상 적용 권장)** |
|---|---|---|---|---|
| `margin-note-layout` | 본문 좌측 65-70% + 우측 25-30% 좁은 마진 노트 | **`02-overview`** chrome | body만: 좌측 `t-body` 본문 grid + 우측 `t-cap c-secondary` 마진 컬럼. 가운데 1pt `.rule` 분리선 | • 마진 노트에 number-circle 부착<br>• 마진 노트 1개만 accent-soft 박스 강조<br>• 본문 안에 inline pull-quote (card-accent)<br>• 좌 본문 + 우 마진에 KPI 1개<br>• 본문 단락별 sub-eyebrow 추가<br>• 가운데 .rule 대신 .rule-accent 분리선 |
| `pull-quote-inline` | 본문 안에 큰 인용문 박스 — 본문이 인용으로 끊겼다가 이어짐 | **`02-overview`** chrome | body만: 위 `t-body` 단락 + 가운데 `card-accent` 안에 `t-h2` 큰 인용 + 아래 `t-body` 단락 | • 인용 박스 좌측 vertical accent bar 4pt<br>• 인용 위 큰 따옴표 mark (c-accent)<br>• 인용 아래 attribution `t-cap c-secondary`<br>• 인용 박스 풀-width vs 80%-width 변주<br>• 본문 단락마다 sub-eyebrow 추가<br>• 인용 일부 단어 c-accent inline |
| `drop-cap-opener` | 챕터·섹션 본문의 첫 슬라이드 — 큰 첫 글자(드롭캡)로 시작 | **`02-overview`** chrome | body만: 좌측 첫 글자 `t-display 60pt c-accent` 단독 (별도 `<h1>`/sibling block, **inline span 금지** — margin 위반), 옆에 `t-body` 단락 | • 드롭캡 80pt vs 100pt 스케일 변주<br>• 드롭캡 옆 작은 attribution 또는 KPI<br>• 드롭캡 + 본문 + 우측 작은 마진 노트 3-column<br>• 드롭캡 c-accent vs c-text + accent-soft bg<br>• 드롭캡 다른 글자 weight (Black 900)<br>• 본문 단락 끝에 .rule + summary 한 줄 |
| `magazine-columns` | 2-3 컬럼 신문 레이아웃 — 정보 밀도 + 에디토리얼 톤 | **`02-overview`** chrome | body만: `grid-2` 또는 `grid-3` + 각 컬럼에 `t-cap-up` kicker + `t-h3` 헤드 + `t-body` 본문 | • 컬럼 1개만 accent-soft bg로 hero<br>• 첫 컬럼만 드롭캡 추가<br>• 컬럼별 sub-KPI metric 동반<br>• 컬럼 사이 vertical .rule 분리선<br>• 위 통합 takeaway + 아래 컬럼<br>• 3-column 대신 1+2 비대칭 (큰 lead + 2 supporting) |

---

### Category D · Density (백본 — jangpm 톤의 핵심)

카드 그리드·KPI·표. **데크의 정보 밀도 백본이자 jangpm "분석적·고밀도 컨설팅" 정체성의 원천**. 50% 넘으면 안티패턴. 양 권장 분포는 두지 않는다 — 어휘 다양성·변형 자유도가 우선.

anchor에서 **chrome + 미세 서식만 복사 의무**. body는 jangpm 시그니처(`tbl-row` div grid / `card` vs `card-accent` 강조 / `number-circle` 패턴) 보존하면서 **자유 변형 권장** — anchor를 그대로 복사하지 말고 **변형 영감 컬럼에서 1개 이상 적용**. v2의 창의성은 표준 패턴 위에 의도적 변형을 더한 데서 나왔다.

| 어휘 | 언제 쓰는지 | **anchor 보일러플레이트** (chrome + 미세 서식 의무 복사) | body 가이드 (시그니처 보존하면서 변형 권장) | **변형 영감 (1개 이상 적용 권장)** |
|---|---|---|---|---|
| `overview-cards` | 4분할 개념 나열 — 개요·구성요소·특징 | **`02-overview`** 또는 **`26-overview-split`** — 콘텐츠만 교체 가능 | 카드 padding 18pt 20pt, accent 카드 1개 한도 | • 4+1 패턴 (4 카드 + 하단 summary card)<br>• 1개 카드만 dark + accent로 강조<br>• 카드 위에 카테고리 eyebrow (`t-cap-up`)<br>• 카드 안에 mini-stat KPI badge<br>• 2+2 grid (좌측 dark + 우측 light)<br>• 카드 간 `.rule` divider 추가 |
| `three-point` | 3개 핵심 (번호 카드 3개) | **`11-three-point`** chrome + number-circle line-height 28pt 의무 | number-circle-lg 패턴 보존, 1개 카드 강조 가능 | • 1개 카드만 `card-accent` 강조<br>• 1개 카드 dark `card-dark` + `c-white` 처리<br>• 카드 사이 `.rule` 분리선<br>• 카드 위에 mini-icon 라벨 추가<br>• 표준 위에 한 줄 `gm-band` 인사이트<br>• 카드 안에 mini KPI badge<br>• 카드 높이 비대칭 (1번 카드만 높이 ↑) |
| `four-point` | 4개 핵심 (2×2 또는 4열) | **`12-four-point`** chrome + number-circle 시그니처 | number-circle 패턴 보존 | • 2×2 vs 1×4 row 배열 변주<br>• 1개 카드만 card-accent 강조<br>• 카드별 다른 number-circle 색 강도<br>• 위 통합 takeaway + 아래 4 카드<br>• 카드 사이 `.rule` grid divider<br>• 카드 안에 mini-stat |
| `six-point` | 6개 항목 (2×3) — 한도. 7개+ 면 분할 | **`13-six-point`** chrome + small cell padding | t-title + t-cap 작은 셀 | • 마지막 항목만 `card-accent`<br>• 첫 행 강조 (3 카드) + 둘째 행 supporting<br>• 항목별 number-circle 색 구분<br>• 항목 사이 .rule grid 분리선<br>• 항목별 icon 라벨 추가<br>• 6 항목 → 3+3 분리 (위/아래 그룹화) |
| `kpi-grid` | 큰 숫자 + 메타 3-6열 (mega-number 단일 슬라이드와 다름) | **`05-card-kpi`** / **`16-stats`** / **`31-kpi-dashboard`** chrome + t-display2 시그니처 | t-display2 숫자 크기 일관 | • 한 KPI를 mega-number로 lead, 나머지 작은 카드<br>• KPI 위에 trend `↑↓` 화살표 (c-positive/c-negative)<br>• 4-column 대신 1+3 비대칭 분할<br>• KPI별 sub-trend 라인 (sparkline 같은 단순 형태)<br>• 좌측 컨텍스트 + 우측 KPI 그리드 split<br>• KPI 사이 `.rule` divider<br>• 한 KPI만 c-accent로 hero |
| `paired-concept` | 두 개 큰 축, 각각 깊이 있는 본문 | **`30-paired-concept`** chrome + grid-2 + 카드 padding | grid-2 + 카드 padding 보존 | • 가운데 dark+accent 구분 컬럼 추가<br>• 양쪽 축에 추가 sub-bullet<br>• 좌·우 비교 + 가운데 화살표<br>• 위쪽 통합 헤드 + 아래 paired<br>• 한쪽 카드만 dark, 다른쪽 light<br>• 양쪽 카드 위에 eyebrow ("FOR" / "AGAINST" 등) |
| `table-detailed` | 데이터 표 — 하이라이트 컬럼·행 | **`06-table`** / **`19-table-detailed`** chrome + tbl-row div grid | tbl-row/tbl-cell div grid (jangpm 시그니처), tbl-hi 하이라이트 컬럼 | • 우측 inline insight 컬럼 추가 (5번째 열)<br>• 특정 row를 `tbl-hi`로 강조<br>• 헤드 행에 sub-label<br>• zebra striping + tbl-hi column 동시 사용<br>• 표 아래 한 줄 takeaway gm-band<br>• 표 위 큰 takeaway 헤드 + 표 본문<br>• 행 내 키워드 c-accent inline |
| `forecast-table` | 시계열 표 — 실측/예측 구분 | **`20-forecast-table`** chrome + tbl-row | 우측 tbl-hi + "예측" 캡션 | • 우측 예측 컬럼 + 위 trend 라인<br>• 분기별 gradient highlight (단색 alpha만)<br>• 헤드에 시점 구분 marker<br>• 실측/예측 경계 vertical .rule-accent<br>• 표 아래 한 줄 결론<br>• 한 row만 c-accent 강조 (key metric) |
| `matrix-trends` | 카테고리×트렌드 매트릭스 (2D grid) | **`27-matrix-trends`** chrome + grid-N | grid-N 격자 | • 우측 inline insight 컬럼<br>• 셀별 컬러 강도 다르게<br>• 매트릭스 + 우측 핵심 takeaway<br>• 셀 안 mini number-circle<br>• 한 row/column만 accent-soft fill<br>• 매트릭스 위 통합 헤드 |

---

### Category E · Sequence (1-2장)

시간·단계 흐름.

| 어휘 | 언제 쓰는지 | **anchor 보일러플레이트** (chrome 골격 의무 복사) | body 작곡 가이드 | **변형 영감 (1개 이상 적용 권장)** |
|---|---|---|---|---|
| `process-arrow` | 가로 단계 흐름 — 단계 N개 + 화살표 | **`15-process`** chrome + number-circle 시그니처 | flex row + number-circle + t-h3 + `→` | • 마지막 단계만 card-accent 강조<br>• 단계별 sub-bullet 추가<br>• 위 통합 takeaway 헤드<br>• 단계 사이 `→` 대신 `.rule-accent`<br>• 단계별 KPI metric 동반<br>• 4 단계 → 위 2 + 아래 2 곡선 배치 |
| `timeline-horizontal` | 시간축 가로 — 마일스톤 점 + 라벨 | **`15-process`** chrome + number-circle line-height 22pt | body만: 굵은 가로 `.rule` + 그 위에 `number-circle` 마일스톤 | • 마일스톤 1개만 c-accent 강조<br>• 라인 위 단계 / 아래 결과 split<br>• 마일스톤 위 KPI 또는 인용 추가<br>• 시간축 양 끝에 시점 라벨 (시작/끝)<br>• 라인 굵기 단계별 변주 (현재 진행 ↑)<br>• 라인 색 segment별 다르게 |
| `agenda-spread` | 데크 목차 (좌 인덱스 + 우 설명) | **`10-agenda`** chrome + number-circle | 좌측 번호 리스트 + 우측 짧은 설명 | • 우측 설명에 KPI 또는 시간 metric<br>• 항목 1개만 card-accent 강조 (현재 위치)<br>• 좌 번호 + 우 설명 + 우끝 sub-eyebrow 3-column<br>• 항목 사이 `.rule` 분리<br>• 위 통합 데크 takeaway + 아래 agenda<br>• 우측 설명 옆 아이콘 라벨 |
| `numbered-progression` | 1→2→3 단계별 흐름 (process보다 비주얼) | **`11-three-point`** chrome + number-circle-lg line-height 28pt | body만: 위→아래 `number-circle-lg` + `t-h3` + `t-body`. 각 단계 사이 `.rule` 분리 | • 마지막 단계만 c-accent 강조<br>• 각 단계에 KPI 또는 결과 metric<br>• 가로 (좌→우) vs 세로 (위→아래) 배치 변주<br>• 단계별 sub-bullet 2-3개 추가<br>• 단계 사이 `.rule` 대신 화살표 `→`<br>• 한 단계만 dark card 강조 |

---

### Category F · Narrative (백본 3-4장 — chrome 톤의 keepers)

데크의 마디. 표지·섹션 마디·요약·마무리. **이 카테고리는 anchor 보일러플레이트를 거의 그대로 사용 권장** — 데크의 톤·정체성을 가장 많이 박제하는 슬라이드들. 변형 영감 컬럼은 짧음 (변형 자유도 < 톤 일관성 우선).

| 어휘 | 언제 쓰는지 | **anchor 보일러플레이트** (거의 그대로 사용) | body 가이드 | **변형 영감** (짧게) |
|---|---|---|---|---|
| `cover` | 데크 표지 1장 — 톤별 3종 | **`01-title`** (기본) / **`23-cover-with-character`** (친근·캐릭터 동반) / **`25-cover-vertical`** (세로형 미니멀) | 데크 톤에 맞게 1개 선택. 우측 캐릭터 영역 도형 데코 금지 (§9) | • 캐릭터 vs 빈 공간 선택<br>• KPI strip 추가 vs 단일 메시지<br>• 메타 (날짜·발표자) 위치 변주 |
| `section-divider` | 챕터 전환 — 큰 번호 + 챕터 제목 | **`09-section`** 또는 **`07-quote-section`** | 큰 번호 + t-h2 제목 | • 큰 번호 + 우측 짧은 setup 단락<br>• 번호 옆 작은 eyebrow 추가<br>• 인용 스타일 vs 번호 스타일 선택 |
| `summary` | 챕터·데크 요약 — 체크리스트 형태 다열 | **`17-summary`** — 거의 그대로 | grid-3/grid-4 + number-circle + t-h3 요약 | • 1개 항목만 card-accent 강조<br>• 위 통합 결론 1줄 + 아래 항목<br>• 항목별 KPI metric 동반 |
| `closing-light` | 모든 closing — light 톤만 사용 (사용자 명시 규칙) | **`21-closing-light`** | character 가능 — 단 우측 데코 도형 금지 | • 캐릭터 vs 빈 공간 선택<br>• CTA 메시지 vs 감사 메시지<br>• 메타 (연락처·다음 액션) 위치 변주<br>• 큰 한 줄 메시지 vs 짧은 두 줄 |
| `quote-section` | 챕터 전환 + 인용 (cover와 section-divider 사이) | **`18-quote-attribution`** 또는 **`07-quote-section`** | 큰 인용 + 속성 | • 인용 위 큰 따옴표 mark<br>• 인용 일부 c-accent inline<br>• 좌측 attribution + 우측 인용 split |

**Closing 규칙 (사용자 명시)**: closing은 항상 `closing-light` (21-closing-light) 사용. **`closing-big` (22, 다크), `closing-dark` (08, 다크) 둘 다 사용 금지** — 데크 톤 무관, 모든 데크의 closing은 light 모드. 어휘 표에서 제거됨.

---

### 보조 어휘 (specialty)

다음은 jangpm 데크에서 가끔 등장하는 specialty. 일반 데크에선 거의 안 씀.

| 어휘 | 보일러플레이트 |
|---|---|
| `terminal-split` / `terminal-full` | 32, 33 — 코딩 강의·기술 데크 |
| `exercise-1up` / `exercise-2up` | 34, 35 — 실습 슬라이드 |
| `pnl-table` / `seasonal-table` | 28, 29 — 회계·계절성 표 |
| `checklist` | 24 — 체크박스 리스트 (보통 summary에 통합) |
| `image-1up` | 36 — 단일 이미지 (보통 Visual-Primary로 격상) |
| `reference-utility` | 03, 04 — 디자인 시스템 데모용 (실 데크에 거의 안 씀) |

---

### 작곡 흐름 (LLM 행동 모델)

각 슬라이드 작성 시 순서:

1. **서사 역할 결정** — 이 슬라이드가 데크에서 무엇을 하는가? (cover / context / data / hero / quote / summary / closing)
2. **카테고리 선택** — 위 6 카테고리 중 어느 카테고리가 그 역할에 맞나?
3. **어휘 선택** — 그 카테고리의 어휘 중 1개 선택
4. **anchor 보일러플레이트 식별 + Read** — 어휘 표의 "anchor 보일러플레이트" 컬럼 참조. 그 파일을 `Read` 해서 chrome (top eyebrow + page counter + .rule + 옵션 gm-band) + 미세 서식 (카드 padding / number-circle line-height / accent 사용 빈도)을 정확히 파악. **chrome 골격은 거의 그대로 복사 의무**.
5. **body 영역만 작곡** — chrome은 anchor 그대로, body 영역만 어휘 가이드대로 변형. Density·Narrative 카테고리는 body도 거의 그대로 사용 권장 (jangpm 시그니처 보존).
6. **미세 서식 self-check** — `references/text-formatting-rules.md` 통과 확인 (원형 텍스트 line-height, 카드 padding, accent 빈도, BR 처리 등)
7. **카테고리 분포 검증** — 데크 전체에서 카테고리 분포가 안티패턴(§10)에 걸리지 않는지 자기 점검.

**핵심 모델**: chrome + 미세 서식 = jangpm 정체성 (anchor에서 그대로 가져옴). body 영역 = 어휘 다양성 (시각 다양성의 원천). 둘은 분리 관리.

**slide-plan(systematic 경로) 사용 시:** `recommended_layout_family` 값은 위 어휘에서 선택. 보일러플레이트 파일명이 아니라 어휘 이름을 쓴다.

---

## 6. Chrome 의무 (모든 본문 슬라이드 공통)

> **chrome = 데크 톤 keepers**. body 영역은 어휘별로 자유 작곡하지만, chrome은 **모든 본문 슬라이드에서 동일** — anchor 보일러플레이트에서 그대로 가져온다. chrome이 흔들리면 jangpm 정체성이 슬라이드별로 옅어진다.

### 본문 슬라이드 공통 골격 (cover·closing 제외)

```
┌──────────────────────────────────────────────┐
│ Section NN · 카테고리          NN / Total    │  ← top header (의무)
│ ──────────────────────────────────────────── │  ← .rule divider (권장)
│                                              │
│ [Slide Title with <span class="c-accent">]   │  ← <h2 class="t-h2">
│ Optional one-line intro paragraph.           │  ← <p class="t-body-sec">
│                                              │
│ [Body — 카테고리별 어휘로 자유 작곡]         │  ← 이 영역만 다양화
│                                              │
│ [Optional GM band — bottom centered]         │  ← .gm-band, bottom 18pt
└──────────────────────────────────────────────┘
```

### Chrome 의무 항목 (본문 슬라이드 모두)

이 항목들은 **anchor 보일러플레이트에서 그대로 복사**하고 슬라이드마다 흔들리지 말 것:

| 항목 | 위치/스타일 | HTML |
|---|---|---|
| **Top eyebrow** (좌) | top: 42pt; left: 56pt | `<p class="t-cap-up">SECTION NN · <카테고리></p>` |
| **Page counter** (우) | top: 42pt; right: 56pt | `<p class="t-cap c-tertiary">NN / Total</p>` |
| **Divider rule** | top: 64pt; left: 56pt; right: 56pt | `<div class="rule"></div>` |
| **Slide title** | top: 88pt; left: 56pt; width: 760pt | `<h2 class="t-h2">...<span class="c-accent">키워드</span>...</h2>` |
| **GM band** (옵션) | bottom: 18pt; left: 56pt; right: 56pt; text-align: center | `<div class="gm-band"><p class="t-body c-secondary">...</p></div>` |

**chrome 변경 허용 예외**:
- Hero/Impact 카테고리 (`mega-quote`, `dramatic-type`, `mega-number` 등): chrome 간소화 또는 제거 가능 — 단 light 톤 유지 (다크 풀블리드 chrome 사용 금지, closing-light only 규칙과 일관). top eyebrow + page counter만 남기고 .rule 생략 OK
- Editorial 카테고리: chrome 그대로 유지하면서 body만 magazine-style 변형

### Body 영역 (자유 작곡)

- 슬라이드 타이틀 직후 14~20pt margin
- 어휘별 가이드대로 작곡 (§5 참조)
- 카드 padding 18pt 20pt 기본 (Density 카테고리)
- accent 슬라이드당 1-2 events
- 하단 콘텐츠는 bottom ≥ 44pt 안전 마진 (4 hard constraint)

### Footer / GM band

- `gm-band` 는 슬라이드 하단 가운데 한 줄로 "so-what" 인사이트 박는 자리
- 모든 슬라이드 의무는 아니지만 insight·summary·data 슬라이드에서 권장
- bottom: 18pt 고정, line-height 자연스럽게

### Cover·Closing 예외

- cover (`01`, `23`, `25`)는 chrome 없음. `t-display` 풀블리드.
- closing-light (`21`)은 밝은 톤 풀페이지 + `t-display` 메시지. **closing은 light 모드만 사용** (사용자 명시 규칙). closing-big (`22`, 다크), closing-dark (`08`, 다크) 사용 금지.
- 이 예외 슬라이드들도 anchor 보일러플레이트의 chrome 패턴(메타 표기, 페이지 카운터)은 따른다.

---

## 7. Title / body / end page flow

- **title page**: 데크 시작 1장. `cover` family 중 1개. 23(캐릭터 동반)은 친근한 컨텍스트, 25(세로형)은 미니멀, 01(기본)은 디폴트.
- **section-divider**: 데크가 5장 이상이면 챕터 사이 1장씩 두는 것이 권장. 09 또는 07.
- **agenda**: title 직후 1장 (10). 12장 이상 데크에서만 의미 있음.
- **body slides**: 이상의 어떤 family든 mix. 같은 family 연속 3장 금지.
- **summary**: 데크 끝 직전 1장 (17). evidence를 묶어서 한 페이지에 결론.
- **end page**: 마지막 1장. **항상 `closing-light` (21)** 사용 — 데크 톤 무관 (사용자 명시 규칙). closing-big (22, 다크), closing-dark (08, 다크) 사용 금지.

권장 시퀀스 (10장 기준):
```
cover → agenda → section-divider → 3~4 body → section-divider → 2~3 body → summary → closing
```

---

## 8. Chart / table treatment

slide-plan introduction guide §"차트의 수사적 역할 어휘" 9종을 jangpm의 시각 구현에 매핑.

| chart_strategy | 의미 | jangpm 구현 | 상태 |
|---|---|---|---|
| `growth-trend` | 단일 시계열 | `forecast-table` (20) 또는 PptxGenJS bar chart로 합성 | available (table-as-chart) |
| `forecast` | 실측+예측 구분 | `forecast-table` (20) — 좌측 실측, 우측 예측 컬럼 강조 | available |
| `structural-break` | 변곡점 강조 | `matrix-trends` (27)의 좌우 대비 활용 | available (변형) |
| `focus-comparison` | 카테고리 비교 + 하이라이트 | `comparison` (14) + `table-detailed` (19)의 hi-column | available |
| `distribution` | 산점/버블 | 현재 boilerplate에 없음 | **requires custom** |
| `quadrant` | 2×2 분면 | `paired-concept` (30) 그리드 응용 또는 custom div grid | available (custom 권장) |
| `priority-matrix` | 3×3 매트릭스 | `matrix-trends` (27)의 mx-grid 응용 | available |
| `split-segment` | stacked/grouped | 현재 boilerplate에 없음. PptxGenJS stacked column | **requires custom** |
| `funnel` | 깔때기 단계 | 현재 boilerplate에 없음 | **requires custom** |

### 표 (table) 규칙

- **html2pptx-friendly**: `<table>` 대신 `tbl-row` / `tbl-cell` div grid 사용 (CSS `display: grid`)
- 헤드 행: `tbl-head` (accent-soft bg + accent ink)
- 하이라이트 컬럼: `tbl-hi` (좌우 accent border + 미세 accent tint)
- zebra: `tbl-zebra` (`#FAFAF9` alt)
- forecast/predicted 컬럼은 hi 컬럼 + 캡션에 "예측" 명시

### Takeaway 텍스트 (R2 강제)

- 모든 chart/table 슬라이드는 시각 위(헤드라인) 또는 아래(gm-band)에 **한 문장 인사이트**를 둔다.
- 표만 두고 결론을 청중에 맡기는 슬라이드는 plan 단계에서 거부 (R2).

---

## 9. Icon system

- **기본 아이콘 팩**: `tabler-outline` (line 스타일, stroke 1.5px 기준)
- **fallback**: tabler-filled
- 아이콘 색은 `c-text` 또는 `c-accent`. semantic color 아이콘은 trend(`c-positive`/`c-negative`)에만.
- **embed 방식**: 외부 `.svg` 파일을 `icons/` 폴더에 두고 `<img src="../icons/<name>.svg">` (`build.mjs`의 `prebuildSvg`가 PNG로 변환). **inline `<svg>` 금지** — html2pptx가 처리 못 함.
- 사이즈: 카드 안 16pt, 헤드라인 옆 20pt, 큰 강조 24pt.

### Brand character (선택)

- `assets/jangpm-character.png` 일러스트 캐릭터. cover-with-character (23) 같은 친근한 표지에서만 사용.
- 본문 슬라이드에 캐릭터 등장 금지 (톤 일관성).
- **표지 우측 영역 규칙**: 캐릭터가 들어갈 자리에는 캐릭터 이미지 또는 빈 공간만. 도형(원/halo/dot 등) 데코레이션 금지 — 어색해진다.

---

## 10. Anti-patterns

다음은 jangpm 톤·기술 제약을 깨는 실패 패턴. plan 단계와 빌드 단계 양쪽에서 거부 대상.

### 디자인 톤

- ❌ CSS gradient (linear/radial) — 4 hard constraint
- ❌ 슬라이드 1장 안에서 accent를 3 events 이상 사용 — monochrome 무드 깨짐
- ❌ semantic color(positive/negative/warning)를 데이터 외 강조에 사용 — 의미 충돌
- ❌ 다크 배경(`card-dark`, `bg-text`)을 본문 카드로 남발 — 다크는 terminal 슬라이드 또는 본문 내 1개 카드 강조에만 (closing 자체는 light only)
- ❌ multi-accent palette 도입 — jangpm은 single-accent system

### 구조 — 카테고리 분포 (R6 시각 다양성 강제)

- ❌ **Hero/Impact 카테고리(A) 0장 데크** — 데크 안에 "120% 다듬은 한 장"이 없으면 임팩트 0. 12장 데크면 1-2장 의무, ≥5장 데크면 1장 의무
- ❌ **Visual-Primary 카테고리(B) 0장 데크** — 텍스트만 N장 = 단조. ≥8장 데크면 2장 이상 의무 (다이어그램/이미지/UI 캡쳐/관계도 중)
- ❌ **Density 카테고리(D)가 데크의 50% 초과** — 카드 그리드만 12장 중 7장 이상 = "SaaS 컨설팅 슬라이드 도배" 안티패턴
- ❌ 같은 카테고리 연속 3장 이상 — 카테고리 간 회전 강제
- ❌ 같은 어휘(`three-point`, `kpi-grid` 등) 연속 2장 이상 — 어휘 회전 강제
- ❌ closing이 다크 모드 (`closing-big` / `closing-dark` / `bg-text` 풀블리드 closing) — 사용자 규칙: closing은 light 모드만 사용. 다크 closing 절대 금지.
- ❌ "title + 3 bullets" 만 반복하는 데크 — overview-cards / three-point / four-point를 mix
- ❌ chart·table만 두고 takeaway 텍스트 누락 — R2 위반
- ❌ 슬라이드 20장 초과인데 split/merge 미검토 — R3
- ❌ evidence_sources 빈 슬라이드 — R5

### 절대 cap·floor (양 권장 아닌 cap만)

> Density는 데크의 백본이지만 **어휘 다양성·변형 자유도가 우선**. 양으로 권장 분포를 박지 않는다 — 아래 cap만 안 넘기면 자유.

- **D 카테고리 50% 초과 ❌** — 어떤 데크든 카드 그리드 도배는 안 됨 (절대 cap)
- **A 카테고리 0장 ❌** — ≥5장 데크면 Hero 1장 의무 ("120% 다듬은 한 장")
- **B 카테고리 0장 ❌** — ≥8장 데크면 Visual-Primary 2장 이상 의무 (텍스트만 N장 = 단조)
- **F 카테고리는 cover + closing 최소 2장**
- 같은 카테고리 연속 3장 이상 ❌
- 같은 어휘 연속 2장 이상 ❌

### 기술 (4 hard constraint)

- ❌ `<p>` 또는 `<h*>` 밖의 raw 텍스트
- ❌ `<p>/<h*>`에 background/border/shadow (외부 div가 담당)
- ❌ div에 `background-image` — `<img>` 태그 사용
- ❌ inline `<svg>` — 외부 svg 파일 + prebuildSvg
- ❌ bottom에서 44pt 이내 콘텐츠
- ❌ inline `<span>`에 margin (대신 `&nbsp;` 사용)

### 카피·언어 (Voice 규약)

- ❌ "여러분", "당신", "저는" — 1·2인칭 금지 (third-person institutional)
- ❌ 의문형 슬라이드 타이틀 — 선언형으로 결론 진술
- ❌ "~합니다만", "~할 수도 있습니다" 같은 hedging — analytical declarative

---

## Provenance

- `colors_and_type.css` v1 (theme-init render)
- `_pptx-slide.css` v1 (theme-init render)
- `pptx-boilerplate/01..37.html` (37 patterns — 8 baseline + 29 contextual)
- 본 DESIGN.md는 위 자료의 **편집 의도 박제**. 토큰·CSS가 바뀌면 본 문서도 함께 갱신.
