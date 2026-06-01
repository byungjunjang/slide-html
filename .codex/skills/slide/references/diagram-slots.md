# Diagram slots — `diagram-design` × editable PPTX

구조적 관계(아키텍처/플로우/시퀀스/계층 등)를 슬라이드에 넣어야 할 때, 손으로 SVG를 짜지 말고 **`diagram-design` 스킬**로 작곡한 뒤 **래스터 PNG 슬롯**으로 임베드한다. 이 문서는 그 단일 경로의 계약(contract)이다.

`/slide` Step 2.6과 `diagram-design/SKILL.md`(§0.5)가 둘 다 이 파일을 가리킨다.

> **이 문서 대부분 = Part A (다이어그램 슬롯)**. 차트·이미지까지 아우르는 일반 **evidence-slot 계약**(메시지 바인딩 + 지배 ≥~55%)은 맨 아래 **Part B — Evidence slots**. 다이어그램은 evidence 슬롯의 한 인스턴스다 (P1 비주얼=근거).

---

## 왜 이 경로인가 (비협상)

`html2pptx.js`는 DOM을 요소별로 PPTX 네이티브 객체로 번역한다. 처리하는 태그는 **텍스트 태그(`<p>`/`<h*>`/`<li>`) · `<img>` · `<div>` 컨테이너 · 리스트**뿐 — **inline `<svg>` 핸들러가 없다.** 따라서 슬라이드 HTML에 inline SVG를 그대로 넣으면 PPTX에서 **조용히 사라진다**.

이 프로젝트가 지원하는 유일한 SVG 경로는: **SVG → PNG 래스터화 → `<img>` 슬롯**. (차트 SVG·아이콘도 전부 이 경로를 탄다.) 그래서 diagram-design의 inline-SVG 산출물은 **렌더 단계를 한 번 거쳐** 이미지 슬롯이 된다.

래스터화는 `sharp`가 아니라 **Playwright(html2pptx와 동일한 Chromium)** 로 한다 — `sharp`는 웹폰트/CJK를 못 불러와 한글이 두부(口)로 깨진다. Chromium은 Pretendard·@font-face·한글을 정확히 렌더한다. 이 일을 하는 스크립트가 [`scripts/render-diagram.mjs`](../scripts/render-diagram.mjs).

> **결과물 성격**: 다이어그램은 PPTX에서 **차트·사진과 같은 그림(raster figure)** 이다 — 도형 텍스트를 더블클릭 편집할 수 없다. 슬라이드의 **나머지 텍스트는 그대로 편집 가능**. 다이어그램 텍스트를 고치려면 `diagrams/<slot>.html`을 수정하고 **다시 렌더**한다(아래 5단계). 그래서 소스 HTML을 `diagrams/`에 보존해 데크를 재현 가능하게 둔다.

---

## 언제 그리나 (게이트)

슬라이드의 **시각 주역이 "구조적 관계"** 일 때만. diagram-design 14종 중 하나로 떨어지는가? (레퍼런스 경로는 모두 **`../../diagram-design/`** 기준 — 예: `../../diagram-design/references/type-architecture.md`)

| 보여줄 것 | 타입 | diagram-design 레퍼런스 (`../../diagram-design/`) |
|---|---|---|
| 컴포넌트 + 연결 | architecture | `references/type-architecture.md` |
| 분기 의사결정 | flowchart | `type-flowchart.md` |
| 행위자 간 시간순 메시지 | sequence | `type-sequence.md` |
| 상태 + 전이 | state | `type-state.md` |
| 엔티티 + 필드 + 관계 | er | `type-er.md` |
| 시간축 위 이벤트 | timeline | `type-timeline.md` |
| 부서 간 핸드오프 | swimlane | `type-swimlane.md` |
| 2축 포지셔닝 | quadrant | `type-quadrant.md` |
| 포함(scope) 계층 | nested | `type-nested.md` |
| 부모→자식 | tree | `type-tree.md` |
| 소유/라우팅/에스컬레이션 | org-chart | `type-org-chart.md` |
| 추상화 레이어 스택 | layers | `type-layers.md` |
| 집합 겹침 | venn | `type-venn.md` |
| 랭크 위계 / 퍼널 드롭오프 | pyramid | `type-pyramid.md` |

**그리지 말 것 (diagram-design SKILL §2와 동일):** 표/불릿이 같은 일을 하면 → 그냥 슬라이드 텍스트로. 단일 숫자/한 도형이면 → 문장 한 줄로. 이건 `/slide`의 **Visual-Primary 카테고리(특히 `diagram-as-hero`)** 어휘에 매핑된다.

---

## 활성 프리셋 = SSOT (diagram-design 온보딩 게이트 건너뜀)

diagram-design 단독 모드의 "first-run style-guide 게이트 / 웹사이트 온보딩"은 **slide-html 안에서는 실행하지 않는다.** 브랜드는 이미 정해져 있다 — `/slide` Step 0가 선언한 **활성 프리셋**(`assets/design-systems/active.json`)이 곧 스킨이다.

다이어그램은 색/폰트를 **하드코딩하지 않고 프리셋 CSS 변수를 참조**한다. 데크의 `design-system/colors_and_type.css`를 `<link>` 하면 SVG의 `style="fill:var(--accent)"` 류가 **렌더 시점에 활성 프리셋 값으로 해석**된다(Chromium). 프리셋을 바꿔 다시 렌더하면 다이어그램도 자동으로 새 스킨이 된다.

**diagram-design 의미역(semantic role) → 프리셋 CSS 변수 매핑** (jangpm 기준; theme-init v1 토큰 계약은 같은 변수명을 공유):

| diagram-design 역할 | CSS 변수 | 비고 |
|---|---|---|
| `paper` (페이지 bg) | — (슬롯은 **투명**) / `--bg` | 슬롯 다이어그램은 전체 bg 사각형을 그리지 않는다 |
| `paper-2` | `--surface-alt` | 컨테이너/보조 fill |
| `ink` (본문/스트로크) | `--text` | |
| `muted` (기본 화살표·서브라벨) | `--text-secondary` | |
| `soft` | `--text-tertiary` | |
| `rule` (헤어라인) | `--border` | |
| `rule-solid` | `--border-strong` | |
| `accent` (focal 1–2개) | `--accent` | |
| `accent-tint` (focal fill) | `--accent-soft` | |
| `link` (HTTP/외부 화살표) | `--text-secondary` | **단일 액센트 원칙**: 파란 link-blue 같은 2번째 휴 금지 → muted로 흡수 |
| node-name 폰트 | `--font-sans` | jangpm=Pretendard |
| 기술 서브라벨(포트/URL) | `--font-mono` | 정말 기술적일 때만 |

**영구 락(프리셋 무관)도 그대로 적용**: 단일 액센트(focal ≤2)·이모지 금지·그라디언트/글로우 금지. diagram-design 자체 그라마(복잡도 예산, 4px 그리드, 박스 전에 화살표, 라벨 마스킹 사각형, 하단 가로 legend strip, 그림자 금지)도 함께 지킨다.

---

## 단계별 (deck 폴더 기준)

전제: `/slide` Step 0~2 진행 중, 어떤 슬라이드의 시각 주역이 다이어그램으로 결정됨. 작업 디렉터리 = `output/<project>-pptx/`.

**1. 타입 선택 + 레퍼런스 로드**
해당 `diagram-design/references/type-<name>.md`를 Read — 레이아웃 관례·안티패턴·복잡도 예산 확인.

**2. 슬롯 정의**
슬롯명과 슬라이드 위 영역(pt)을 먼저 정한다. 예: `arch-overview`, 영역 760pt × 360pt.
SVG `viewBox`의 W:H = 슬롯 영역의 W:H (왜곡 방지). 예: `viewBox="0 0 760 360"`.

**3. `diagrams/<slot>.html` 작곡 (diagram-only)**
```bash
mkdir -p diagrams images
```
- `<link rel="stylesheet" href="../design-system/colors_and_type.css">` (변수 상속)
- `html,body{margin:0;background:transparent}` — **슬라이드 chrome 금지** (제목/eyebrow/카드/푸터는 슬라이드가 담당)
- `<svg id="diagram" viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg">` 하나만. **전체 캔버스 paper 사각형을 그리지 않는다**(투명 합성).
- 색·폰트는 위 매핑표의 `var(--…)`로. diagram-design 그라마 준수.

**4. 렌더 → 투명 PNG**
```bash
node ../../.codex/skills/slide/scripts/render-diagram.mjs diagrams/<slot>.html images/<slot>.png --scale 3
```
`svg#diagram`(기본 셀렉터 `svg`)의 바운딩 박스를 3× 고해상도 투명 PNG로 캡처해 `images/<slot>.png`에 저장. 폰트 로드를 기다린 뒤 캡처하므로 한글도 선명.
- 불투명 배경이 필요하면 `--bg` (드물게: 다이어그램이 어두운 띠 위에 놓일 때 등).
- 다른 요소를 캡처하려면 `--selector "..."`.

**5. 슬라이드에 `<img>` 슬롯으로 배치**
슬라이드 HTML은 `slides/` 안에 있고 PNG는 데크 루트 `images/`에 있으므로 **`../images/`** 로 참조한다(이게 실제 데크 컨벤션 — `images/`만 쓰면 `slides/images/`로 잘못 풀려 빌드 실패):
```html
<img src="../images/<slot>.png"
     style="position:absolute; left:100pt; top:120pt; width:760pt; height:360pt;">
```
viewBox 비율 = 슬롯 비율이면 왜곡 없음(안전하게 `object-fit:contain` 추가 가능). 핵심 takeaway는 다이어그램 안 라벨이 아니라 **슬라이드의 실제 `<p>` 텍스트**로도 둔다 — 편집 가능성 유지 + `B-r2`(visual+takeaway) 통과.

**6. 빌드 (평소대로)**
```bash
node build.mjs
```
`images/<slot>.png`는 이미 PNG라 `prebuild-svg`(icons/*.svg 전용)와 무관하게 html2pptx가 `pic` 객체로 임베드한다. `unzip -t`로 무결성 확인.

---

## 자주 하는 실수

- ❌ inline `<svg>`를 슬라이드 HTML에 직접 → PPTX에서 사라짐. **항상 PNG 슬롯 경유.**
- ❌ 다이어그램 HTML에 전체 paper 배경 사각형 → 투명 합성이 깨져 슬라이드 위에 색 박스가 덮임. 슬롯은 배경 없이.
- ❌ 색을 hex로 하드코딩 → 프리셋 교체 시 안 따라옴. **`var(--…)`만.**
- ❌ `<img src="images/...">` (../없이) → `slides/images/`로 풀려 빌드 실패. 슬라이드에서는 **`../images/<slot>.png`**.
- ❌ viewBox 비율 ≠ `<img>` 박스 비율 → 왜곡. 둘을 일치시키거나 `object-fit:contain`.
- ❌ link-blue 등 2번째 색 사용 → 단일 액센트 위반. `--text-secondary`로.
- ❌ 다이어그램 텍스트를 슬라이드의 유일한 텍스트로 → 편집 불가 + takeaway 누락. 핵심 문구는 슬라이드 `<p>`로 중복.

---

## Part B — Evidence slots (차트·이미지·다이어그램 공통 계약)

> **P1 비주얼=근거**: Visual-Primary 슬라이드에서 비주얼은 **메시지의 증거/설명이자 지배 요소**다 — 장식이 아니다. 텍스트는 주장(claim)을 말하고, 비주얼은 그것을 증명한다. **다이어그램·차트·이미지 세 매체가 모두 이 계약을 공유**한다. 위(Part A)는 그 다이어그램 인스턴스.

### 공통 규칙 (세 매체 모두)

1. **메시지 바인딩** — 모든 evidence 슬롯은 한 주장(claim)에 묶인다. 그 주장은 **편집 가능한 슬라이드 텍스트**(`<p>`/`<h*>`, 보통 GM-band 또는 헤드라인)로 둔다 — 이미지/도형 안 라벨에만 두지 않는다. (anti-slop §13 장식-비주얼 금지 + R2 takeaway와 동일.)
2. **지배 (dominance ≥ ~55%)** — evidence 비주얼은 슬라이드 콘텐츠 영역의 ≥~55%를 차지하는 **시각 주역**이다. 텍스트는 캡션. 텍스트 옆 작은 썸네일 비주얼은 evidence가 아니라 장식.
3. **슬롯 마커** — 슬롯 컨테이너에 `data-image-slot="<name>"` (Phase 2·B 다양성 게이트가 visual 신호로 인식 + 슬롯 추적). 슬라이드 루트는 visual family `data-layout`(`image-hero`/`annotated-visual`/`diagram-hero`/`compare-split`).

### 매체별 생산 경로 (하이브리드)

| 매체 | 경로 | PPTX 편집? |
|---|---|---|
| **다이어그램** | diagram-design → PNG (위 Part A) | 도형 텍스트 불가 · 슬라이드 텍스트 가능 |
| **차트 — 단순 bar/column/KPI** | `_pptx-slide.css` div 프리미티브(`ev-bar`/`ev-col-*`/`ev-fill*`/`ev-spark` — `var(--accent)` + **rgba alpha**, `opacity`는 html2pptx가 무시) — html2pptx가 번역 | **텍스트 편집 가능** |
| **차트 — 복잡(산점·stacked·퍼널)** | diagram-design → PNG (Part A 경로) | 불가 |
| **이미지** | AI 이미지 슬롯(§2.5) 또는 사진, full-bleed / ≥55% | n/a |

하이브리드 원칙: **단순 bar/KPI = div(편집 가능), 복잡 = PNG.** 차트 라우팅 상세는 `assets/design-systems/<preset>/DESIGN.md` §8 + `css-helpers.md`(evidence-chart 프리미티브).

### slide_plan.json (Systematic 모드 · optional)

```jsonc
{
  "lead": "<이 슬라이드가 던지는 한 줄 주장>",      // 슬라이드 가장 큰 텍스트 슬롯 / GM-band
  "evidence": {
    "type": "chart",                              // chart | image | diagram
    "slot": "<slot-name>",                        // images/<slot>.png 또는 data-image-slot 값
    "proves": "<이 비주얼이 lead를 어떻게 증명하는가>",
    "dominance": "60%"                            // optional, 기본 ≥~55%
  }
}
```

optional 필드 — 없으면 기존 동작 그대로. 있으면 `/slide`는 `lead`를 편집 텍스트로 두고 `evidence` 슬롯을 지배 비주얼로 작곡한다. `validate_plan.py`는 **present일 때만** shape를 soft-check(없으면 무시).
