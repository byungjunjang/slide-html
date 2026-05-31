# Layout Registry — `data-layout` families (Jangpm)

> **목적**: 슬라이드 레이아웃을 **머신 체크 가능한 coarse family**로 태깅해 데크 시각 다양성을 강제한다 (`PIPELINE_UPDATE_PLAN.md` 항목 A·B). 각 슬라이드 `<body>`에 `data-layout="<family>"`를 부여하면, 빌드 prebuild 게이트(`scripts/validate-diversity.mjs`)가 커버리지 · distinct 수 · card-type 비율 · visual 존재를 점검한다.
>
> **두 단계 어휘**: 세밀한 작곡 어휘는 `assets/design-systems/<preset>/DESIGN.md` §5(6 카테고리, ~30 어휘)가 SSOT. 본 레지스트리는 그 위에 얹는 **coarse 분류 태그**(14 family)일 뿐 — 다양성 카운팅용이지 작곡 메뉴가 아니다. §5 어휘 항목은 아래 매핑 컬럼으로 한 family에 귀속된다.

## `data-layout` 부여 규칙

- 모든 슬라이드 루트에 `<body data-layout="<family-id>">` — **한 슬라이드 = 한 family**.
- `family-id`는 아래 14개 중 하나. (게이트는 distinct 카운팅에 임의 문자열도 허용하지만, **레지스트리 id 사용 권장** — card-type/visual 분류가 정확해진다.)
- 이미지/차트/다이어그램 **증거 슬롯**이 있으면 그 슬롯 컨테이너에 `data-image-slot="<name>"`을 추가한다 (Phase 3·C evidence-slots 계약과 연결). 게이트의 visual 존재 점검이 이를 인식한다. `<img>` 태그 자체도 visual 신호로 인정.

## 14 family

| family-id | 카테고리 (§5) | card? | visual? | §5 어휘 매핑 | 언제 |
|---|---|:--:|:--:|---|---|
| `hero-statement` | A Hero | | | `mega-quote` · `dramatic-type` · `bold-statement-split` | 한 줄 명제/테제 |
| `hero-number` | A Hero | | | `mega-number` | 단일 집약 수치 |
| `image-hero` | B Visual | | ✓ | `full-bleed-image-with-overlay` · `image-1up` | 풀블리드 이미지 |
| `annotated-visual` | B Visual | | ✓ | `annotated-screenshot` · `image-with-callouts` | 캡쳐 + 콜아웃 |
| `diagram-hero` | B Visual | | ✓ | `diagram-as-hero` · `knowledge-graph` | 다이어그램 주역 |
| `compare-split` | B Visual | | ✓ | `before-after-split` · `image-2up-comparison` · `single-portrait-quote` | 좌우 비교/대조 |
| `editorial-prose` | C Editorial | | | `margin-note-layout` · `pull-quote-inline` · `drop-cap-opener` · `magazine-columns` | 읽히는 산문 |
| `data-table` | D Density | | | `table-detailed` · `forecast-table` · `matrix-trends` | 데이터 표 |
| `sequence-flow` | E Sequence | | | `process-arrow` · `numbered-progression` · `timeline-horizontal` · `agenda-spread` | 시간/단계 흐름 |
| `narrative-frame` | F Narrative | | | `cover` · `section-divider` · `summary` · `closing-light` · `quote-section` | 데크 마디 |
| `cards-overview` | D Density | ✓ | | `overview-cards` | 개요 카드 나열 |
| `cards-points` | D Density | ✓ | | `three-point` · `four-point` · `six-point` | 번호 포인트 카드 |
| `kpi-grid` | D Density | ✓ | | `kpi-grid` | KPI 타일 그리드 |
| `paired-concept` | D Density | ✓ | | `paired-concept` | 2축 큰 카드 |

**card-type 4/14 ≤ 1/3** — 레지스트리 구성 자체가 카드형을 소수로 묶어 "카드 반복 탈피"(P1)를 구조적으로 유도한다. 데크 단위 cap은 `DESIGN.md` §10(Density ≤ 50%, 이상적으로 ≤ 1/3) · `anti-slop.md` §13이 SSOT.

## 게이트(B)가 보는 것 — WARN

`scripts/validate-diversity.mjs` — `build.mjs` prebuild에서 **non-blocking** 실행:

1. **커버리지** — `data-layout` 없는 슬라이드 → WARN (어느 파일인지 나열).
2. **distinct** — 서로 다른 family 수 < `⌈슬라이드수 × 0.6⌉` → WARN (이상 ≥ 0.7).
3. **card-type 비율** — card-type family 슬라이드 > 데크의 50% → WARN (이상 ≤ 1/3).
4. **visual 존재** — 데크(≥5장)에 visual family / `<img>` / `data-image-slot`이 하나도 없음 → WARN.

게이트는 vocabulary에 관대하다 — 레지스트리에 없는 family-id도 distinct 카운트엔 포함되고, 오타로 의심되면 INFO로만 알린다. **card-type/visual 분류만** 위 표에서 인지한다 (그래서 새 비-카드 family를 추가해도 거짓 경고가 안 난다).

WARN은 빌드를 막지 않는다. `--strict` 플래그로 게이트화 — Phase 4에서 레지스트리 정착 후 `build.mjs`에 `--strict` 승격 예정.
