---
preset: {{TOKEN:name}}
display_name: {{TOKEN:display_name}}
generated_by: theme-init render_design_md
schema_version: 1.0
status: draft
---

# {{TOKEN:display_name}} · DESIGN.md

> **Status:** `draft` — 자동 생성 초안. 사용자 검토 후 빈 섹션을 채우고 frontmatter `status: confirmed`로 변경하세요.
>
> 이 문서는 slide-plan introduction guide §Layer 3의 산출물입니다. slide-plan은 이 어휘로 `recommended_layout_family`를 채우고, simple `/slide` 경로의 LLM도 이를 참조해 layout 일관성과 **변형 자유도**를 유지합니다.
>
> 5 questions / 7-step 작곡 흐름 / anti-slop self-check / 미세 서식 polish는 **`/slide` 스킬 본체** (`SKILL.md`, `references/anti-slop.md`, `references/text-formatting-rules.md`)에 박혀 있습니다 — preset 무관, 모든 preset에서 자동 적용. 본 DESIGN.md는 그 위에 얹는 **이 preset의 편집 어휘·시각 vocabulary** 입니다.

---

## 1. Visual theme & atmosphere

> **Description:** {{TOKEN:description}}

(LLM 추출 자리 — brand description 한 줄 위에 톤·무드·정보 밀도 2~3줄 보강하세요. 이 preset이 발표용/인쇄용/SaaS/컨설팅/마케팅 중 어느 결인지가 §5 카테고리 분포 의도를 결정합니다.)

---

## 2. Palette & contrast behavior

| Token | Hex | Role |
|---|---|---|
| `--bg` | `{{TOKEN:colors.bg}}` | page background |
| `--surface` | `{{TOKEN:colors.surface}}` | card / container |
| `--surface-alt` | `{{TOKEN:colors.surface-alt}}` | grouped block |
| `--text` | `{{TOKEN:colors.text}}` | primary text |
| `--text-secondary` | `{{TOKEN:colors.text-secondary}}` | body secondary |
| `--text-tertiary` | `{{TOKEN:colors.text-tertiary}}` | captions |
| `--border` | `{{TOKEN:colors.border}}` | divider / card border |
| `--border-strong` | `{{TOKEN:colors.border-strong}}` | strong divider |
| `--accent` | `{{TOKEN:colors.accent}}` | primary accent — **slide당 1~2 events** |
| `--accent-soft` | `{{TOKEN:colors.accent-soft}}` | accent tinted bg |
| `--accent-ink` | `{{TOKEN:colors.accent-ink}}` | accent pressed |
| `--positive` | `{{TOKEN:colors.positive}}` | data only |
| `--negative` | `{{TOKEN:colors.negative}}` | data only |
| `--warning` | `{{TOKEN:colors.warning}}` | data only |

(추가 사용 규칙 — accent 이벤트 한도, semantic 사용 제한, dark surface 정책 등을 손으로 채우세요. accent multi-color 사용 여부도 명시.)

---

## 3. Typography hierarchy

(font chain은 theme.json에서 자동 추출됩니다. pt scale이 캔버스 960×540pt에 calibrated 됐는지 확인하고, 본문 디폴트·타이틀 디폴트 클래스명을 명시하세요.)

---

## 4. Spacing & density

(8px grid 기준 spacing 토큰. 카드 padding·grid gap·bottom 안전 마진을 명시하세요.)

---

## 5. Visual vocabulary — compose, don't copy

> **이 섹션은 시각 주역(visual main-character) 어휘**입니다. 슬라이드는 보일러플레이트 카탈로그에서 "복사"하는 게 아니라, 이 어휘에서 골라 preset 토큰으로 **즉흥 작곡**합니다.
>
> **위상**: 보일러플레이트는 어휘의 일부 — "메뉴"가 아니라 "참고 갤러리". 어휘 항목 옆에 매칭되는 보일러플레이트가 있으면 anchor로 링크하지만, 보일러플레이트가 없거나 살짝 다른 변형을 원하면 preset 토큰으로 **새로 작곡**합니다 (4 hard constraint만 통과).

### 6 카테고리

데크의 시각 다양성은 **카테고리 간 분포**에서 나옵니다. 한 데크에 모든 카테고리가 골고루 등장하면 톤은 preset 그대로 유지되면서 슬라이드별 인상은 다릅니다.

| 카테고리 | 목적 |
|---|---|
| **A. Hero / Impact** | 한 페이지 전체로 강한 메시지 — 큰 인용·큰 숫자·큰 타이포 |
| **B. Visual-Primary** | 시각 자체가 메시지 — 다이어그램·이미지·관계도·UI 캡쳐 |
| **C. Editorial** | 잡지·신문 톤 — 마진 노트·드롭캡·인라인 풀쿼트 |
| **D. Density** | 정보 밀도 — 카드 그리드·KPI·표 |
| **E. Sequence** | 시간 흐름 — process·timeline·agenda |
| **F. Narrative** | 데크 흐름 마디 — cover·section-divider·summary·closing |

### 어휘 표 작성 가이드 (이 preset의 §5 본문)

각 카테고리 아래에 다음 4컬럼 표를 작성하세요. **변형 영감 컬럼이 LLM에게 v4 변형 자유도를 알려주는 핵심**입니다 — 누락 시 LLM이 anchor를 그대로 복사해 슬라이드 다양성이 깎입니다.

| 어휘 | anchor 보일러플레이트 | body 작곡 가이드 | **변형 영감 (1개 이상 적용 권장)** |
|---|---|---|---|
| `kebab-case` 어휘명 | `pptx-boilerplate/NN-name.html` | chrome 그대로, body 영역만 변형 가이드 | • 이 어휘에 적용 가능한 의도적 변형 옵션 4-6개<br>• 표준 패턴 위에 한 가지만 더해도 다양성 회복<br>• 예: 카드 1개만 강조 / 비대칭 분할 / mini-stat 부착 / KPI metric 동반 / 사이 .rule divider 등 |

#### Category A · Hero / Impact 어휘

(예: `mega-quote`, `mega-number`, `dramatic-type`, `bold-statement-split`, `full-bleed-image-with-overlay` 등을 이 preset의 톤에 맞게 선별·작성하세요.)

#### Category B · Visual-Primary 어휘

(예: `annotated-screenshot`, `single-portrait-quote`, `diagram-as-hero`, `before-after-split`, `image-with-callouts`, `knowledge-graph` 등.)

#### Category C · Editorial 어휘

(예: `margin-note-layout`, `pull-quote-inline`, `drop-cap-opener`, `magazine-columns` 등. preset이 잡지·인쇄물 톤이 아니면 비울 수 있음.)

#### Category D · Density 어휘 (대부분 데크의 백본)

(예: `overview-cards`, `three-point`, `four-point`, `six-point`, `kpi-grid`, `paired-concept`, `table-detailed`, `forecast-table`, `matrix-trends` 등. 보일러플레이트와 1:1 매핑되는 경우가 많음.)

#### Category E · Sequence 어휘

(예: `process-arrow`, `timeline-horizontal`, `agenda-spread`, `numbered-progression` 등.)

#### Category F · Narrative 어휘 (chrome 톤의 keepers)

(예: `cover`, `section-divider`, `summary`, `closing-light`, `closing-big`, `closing-dark`, `quote-section` 등. 이 카테고리 어휘는 anchor 거의 그대로 사용 권장 — 톤 일관성 우선. 변형 영감 컬럼은 짧게.)

> **Narrative 예외**: §5 어휘 중 Narrative 카테고리만 anchor 거의 그대로 사용 권장 (톤 keepers). 다른 5 카테고리(Hero/Visual-Primary/Editorial/Density/Sequence)는 anchor에서 chrome + 미세 서식만 복사한 뒤 **body는 변형 영감 컬럼에서 1개 이상 적용 권장**. v2 식 자유도가 여기서 회복됩니다.

**slide-plan(systematic 경로) 사용 시:** `recommended_layout_family` 값은 위 어휘에서 선택. 보일러플레이트 파일명이 아니라 어휘 이름을 씁니다.

---

## 6. Chrome 의무 (모든 본문 슬라이드 공통)

> **chrome = 데크 톤 keepers**. body 영역은 어휘별로 자유 작곡하지만, chrome은 **모든 본문 슬라이드에서 동일** — anchor 보일러플레이트에서 그대로 가져옵니다. chrome이 흔들리면 preset 정체성이 슬라이드별로 옅어집니다.

### 본문 슬라이드 공통 골격 (cover·closing 제외)

```
┌──────────────────────────────────────────────┐
│ Section NN · 카테고리          NN / Total    │  ← top header (의무)
│ ──────────────────────────────────────────── │  ← .rule divider (권장)
│                                              │
│ [Slide Title with accent keyword]            │  ← <h2> 타이틀
│ Optional one-line intro paragraph.           │  ← 부연 (옵션)
│                                              │
│ [Body — 카테고리별 어휘로 자유 작곡]         │  ← 이 영역만 다양화
│                                              │
│ [Optional GM band — bottom centered]         │  ← .gm-band, bottom 18pt
└──────────────────────────────────────────────┘
```

(Chrome 의무 항목 — top eyebrow / page counter / divider rule / slide title / GM band의 정확한 좌표·스타일·HTML 패턴을 anchor 보일러플레이트에서 추출해 손으로 채우세요. 본 preset의 모든 본문 슬라이드가 같은 chrome을 공유해야 합니다.)

### Chrome 변경 허용 예외

- Hero/Impact 카테고리 (`mega-quote`, `dramatic-type`, `mega-number` 등): chrome 간소화 또는 제거 가능 — 단 anchor 보일러플레이트의 패턴 따를 것
- Editorial 카테고리: chrome 그대로 유지하면서 body만 magazine-style 변형

---

## 7. Title / body / end page flow

(데크 시퀀스 권장 순서. 표지 → agenda → 본문 → section-divider → summary → closing 어디에 어떤 어휘를 두는지. closing 어휘 선택 가이드도 이 preset 톤에 맞게 명시하세요.)

---

## 8. Chart / table treatment

slide-plan introduction guide §"차트의 수사적 역할 어휘" 9종을 이 preset의 시각 구현에 매핑하세요.

| chart_strategy | 이 preset 구현 | 상태 |
|---|---|---|
| `growth-trend` | (boilerplate 또는 custom) | available / requires custom |
| `forecast` | | |
| `structural-break` | | |
| `focus-comparison` | | |
| `distribution` | | |
| `quadrant` | | |
| `priority-matrix` | | |
| `split-segment` | | |
| `funnel` | | |

### Takeaway 텍스트 (R2 강제)

- 모든 chart/table 슬라이드는 시각 위(헤드라인) 또는 아래(gm-band)에 **한 문장 인사이트**를 둡니다.
- 표만 두고 결론을 청중에 맡기는 슬라이드는 plan 단계에서 거부 (R2).

---

## 9. Icon system

- 기본 아이콘 팩: `{{TOKEN:assets.icon-pack-default}}`
- fallback: `{{TOKEN:assets.icon-pack-fallback}}`

(임베드 방식·사이즈 가이드·brand character가 있으면 사용 규칙을 손으로 채우세요. character는 본문 슬라이드 등장 금지·cover/closing 한정 같은 톤 일관성 룰을 명시.)

---

## 10. Anti-patterns

다음은 이 preset 톤·기술 제약을 깨는 실패 패턴. plan 단계와 빌드 단계 양쪽에서 거부 대상.

### 디자인 톤 (이 preset 특이)

- ❌ CSS gradient (linear/radial) — 4 hard constraint
- ❌ 슬라이드 1장 안에서 accent 3 events 이상 — monochrome 무드 깨짐
- ❌ semantic color(positive/negative/warning)를 데이터 외 강조에 사용
- (이 preset 특이 anti-pattern — multi-accent 정책, dark surface 정책, 캐릭터 사용 정책 등을 손으로 추가)

### 구조 — 카테고리 분포 (universal cap)

> 양 권장 분포는 두지 않습니다 — 어휘 다양성·변형 자유도가 우선. 아래 cap만 안 넘기면 자유.

- ❌ **D 카테고리 50% 초과** — 어떤 데크든 카드 그리드 도배는 안 됨 (절대 cap)
- ❌ **A 카테고리 0장** — ≥5장 데크면 Hero 1장 의무 ("120% 다듬은 한 장")
- ❌ **B 카테고리 0장** — ≥8장 데크면 Visual-Primary 2장 이상 의무 (텍스트만 N장 = 단조)
- ❌ **F 카테고리는 cover + closing 최소 2장**
- ❌ 같은 카테고리 연속 3장 이상
- ❌ 같은 어휘(`three-point`, `kpi-grid` 등) 연속 2장 이상

### Plan 규칙 (R-rules · slide-plan introduction guide)

- ❌ chart·table만 두고 takeaway 텍스트 누락 (R2)
- ❌ 슬라이드 20장 초과인데 split/merge 미검토 (R3)
- ❌ 같은 layout_family 연속 3장 이상 (R4)
- ❌ evidence_sources 빈 슬라이드 (R5)

### 기술 (4 hard constraint)

- ❌ `<p>` 또는 `<h*>` 밖의 raw 텍스트
- ❌ `<p>/<h*>`에 background/border/shadow (외부 div가 담당)
- ❌ div에 `background-image` — `<img>` 태그 사용
- ❌ inline `<svg>` — 외부 svg 파일 + prebuildSvg
- ❌ bottom에서 44pt 이내 콘텐츠
- ❌ inline `<span>`에 margin (대신 `&nbsp;` 사용)

(preset 특이 anti-pattern — 카피·언어 voice 규약, 캐릭터 사용 한도 등을 손으로 추가.)

---

## 11. 스킬 본체와의 관계 (preset 무관 — 자동 적용)

이 DESIGN.md는 본 preset의 시각 어휘만 박제합니다. 다음은 **모든 preset에 동일하게 적용**되며, `/slide` 스킬 본체에서 관리:

| 항목 | 위치 | 내용 |
|---|---|---|
| **5 questions** (서사 역할 / 관객 거리 / 시각 온도 / 카테고리 / 변형) | `slide/SKILL.md` §2.1 | 매 슬라이드 작성 전 답하는 5개 질문. Q5 = "이 슬라이드의 한 가지 변형은?" |
| **7-step 작곡 흐름** | `slide/SKILL.md` §2.2 | 카테고리 → 어휘 → anchor Read → body 작곡 (변형 영감 1개 이상) → self-check |
| **anti-slop self-check** | `slide/references/anti-slop.md` | 카테고리 분포 / 시각 주역 회전 / 120% hero / 색·톤 / 카피·언어 |
| **미세 서식 polish** | `slide/references/text-formatting-rules.md` | 원형/badge line-height / 카드 padding / chrome 일관 / 오버랩 자기 점검 |

새 preset이 위 본체 룰을 따로 명시할 필요는 없습니다 — 자동 적용. 본 DESIGN.md는 §5 어휘 표 + §6 chrome + §10 preset 특이 anti-pattern만 정확히 채우면 됩니다.

---

## Provenance

- `theme.json` v1
- `colors_and_type.css`, `_pptx-slide.css`
- `pptx-boilerplate/*.html`
- 본 DESIGN.md는 위 자료의 **편집 의도 박제**. 토큰·CSS가 바뀌면 본 문서도 함께 갱신.
