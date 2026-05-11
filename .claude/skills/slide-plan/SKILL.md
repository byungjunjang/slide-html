---
name: slide-plan
description: 슬라이드 데크 기획 두뇌. 사용자 brief + 활성 preset의 DESIGN.md + (선택) 사용자 파일을 받아 단일 slide_plan.json을 산출한다. /slide의 opt-in pre-step — 짧은 데크는 /slide만 써도 되지만, 체계적 기획이 필요하면 이 스킬을 먼저 호출. 트리거 — "/slide-plan", "체계적으로 기획해줘", "데크 구조부터", "슬라이드 기획해줘".
trigger: /slide-plan, 슬라이드 기획, 데크 구조, deck plan, 체계적
---

# /slide-plan — 데크 기획 두뇌

`/slide`가 prerequisite로 쓰는 **기획 단계**. simple 경로(짧은 데크)는 이 스킬을 거치지 않고 `/slide` 직행해도 된다. systematic 경로일 때만 이 스킬을 먼저 호출하고, 산출된 `slide_plan.json`을 `/slide`가 소비한다.

본 스킬의 단 하나의 산출물: `output/<project-name>-pptx/slide_plan.json`.

---

## Layer 1 — 보편 규율 (절대 위반 금지)

slide_plan.json의 모든 슬라이드는 다음 5개 규율을 통과해야 한다. R2/R5는 자동 검증으로 빌드 거부, R1/R3/R4는 lint 경고.

### R1. 슬라이드별 사유 출력 의무

모든 슬라이드는 다음 4개 필드를 채운다 — 빈 값 금지:

- `core_message` — 이 슬라이드의 단일 주장
- `audience_takeaway` — 청중이 가져갈 한 줄
- `why_here` — 왜 다른 위치가 아니라 여기인지
- `recommended_layout_family` — 활성 preset의 DESIGN.md 어휘 중 하나 (jangpm이면 cover, three-point, kpi-grid, ... 등 27종)

### R2. 차트·표·다이어그램 슬라이드의 takeaway 텍스트 일체화

모든 visual-led 슬라이드는 시각 자료와 별개로 **인사이트 텍스트 슬롯**을 가진다:

- `chart_strategy` non-empty → `chart_takeaway` non-empty 강제
- `table_strategy` non-empty → `table_takeaway` non-empty 강제
- 차트만 두고 결론 없는 슬라이드는 plan 단계에서 거부 (validate_plan.py exit 1)

### R3. 분량 압박

- 사용자가 슬라이드 수 명시 안 하면 default **8~12장**
- 20장 초과 시 split / merge / defer 후보 한 번 더 점검
- "tighter deck > bloated deck"

### R4. Lazy 반복 금지

- title + 3 bullets 같은 단조로운 반복 패턴 금지
- 동일 `recommended_layout_family` 연속 3장 이상 사용 시 정당화 필수
- body slide는 한 family에 머물되 role(insight → evidence 등)이 바뀌면 family도 바꾼다

### R5. Evidence 매핑 의무

- 모든 슬라이드의 `evidence_sources` (또는 `content_constraints.evidence_to_use`) 필수
- 사용자 파일이 있으면 매핑, 없으면 `inference`로 명시
- **빈 값 금지** (사실 출처 추적성 보장)

---

## Layer 2 — 워크플로우

### 입력

1. **사용자 brief** (텍스트) — 어떤 데크, 누구에게, 어떤 결론
2. **활성 preset의 DESIGN.md** — `.claude/skills/slide/assets/design-systems/<preset>/DESIGN.md`
   - layout_families 어휘
   - header/body/footer 룰
   - chart/table treatment 매핑
   - anti-patterns
3. **(선택) 사용자 파일** — 엑셀, MD, PDF 등. evidence pool로 사용

### 워크플로우 (8단계, 순차)

#### 1. deck_type 감지

사용자 brief에서 도메인 추론. 후보 8종 (`references/deck-types.md` 참조):
`consulting` / `educational` / `report` / `sales` / `internal_update` / `proposal` / `keynote` / `unknown`

자신없으면 사용자에게 명시적으로 묻는다. `unknown`으로 두고 진행하면 강제 narrative arc가 적용되지 않는다.

#### 2. narrative arc 선택

`references/deck-types.md`의 deck_type별 시퀀스를 **시작점 휴리스틱**으로 사용. brief에 맞게 자유 적응 — 강제 아님.

#### 3. DESIGN.md 로드

활성 preset 폴더에서 DESIGN.md 통독. 다음을 흡수:
- `layout_families` 어휘 (이 어휘 외의 family명을 plan에 박지 말 것)
- `chart/table treatment` (어떤 chart_strategy가 available / requires custom 인지)
- `anti-patterns` (위반 시 plan 거부)

DESIGN.md가 없으면 (status: draft 상태이거나 백필 안 됨): preset의 `pptx-boilerplate/` 파일명에서 family 어휘를 추정 + 사용자에게 확인.

#### 4. content_inventory 작성

사용자 파일이 있으면 source별 분류:
- `source_id`, `source_type` (file|prompt|inference)
- `summary`, `relevance` (high|medium|low), `usable_for[]`

파일 없으면 inference 모드 — 한 source가 `inference`로 박히고 모든 슬라이드가 이를 참조.

#### 5. 슬라이드별 plan 작성

각 슬라이드:

- `slide_role` — `references/slide-roles.md`의 deck_type별 enum에서 선택
- `core_message`, `audience_takeaway`, `why_here` (R1)
- `recommended_layout_family` — DESIGN.md의 어휘 (R1)
- `content_blocks[]` — block_type, purpose, content_instruction
- `content_constraints` — must_include, must_not_include, evidence_to_use
- (해당 시) `chart_strategy` + `chart_takeaway` (R2)
- (해당 시) `table_strategy` + `table_takeaway` (R2)
- `evidence_sources[]` (R5)

스키마 전체: `references/slide-plan-schema.md`.

#### 6. 검증

자체 점검:
- 모든 슬라이드의 R1 4필드 채워짐
- visual-led 슬라이드의 R2 takeaway 채워짐
- R3 분량 (8~12 default, 20+ 재점검)
- R4 동일 family 연속 3장 미만
- R5 evidence_sources 빈 값 없음

자동 검증:
```bash
python3 .claude/skills/slide-plan/scripts/validate_plan.py \
  output/<project-name>-pptx/slide_plan.json
```
exit 1이면 R2/R5 위반 — 수정 후 재검증.

#### 7. JSON 출력

경로: `output/<project-name>-pptx/slide_plan.json` (각 프로젝트 자기완결 폴더)

스키마 변형은 자유 (preset마다 layout_family 어휘가 다르므로 통일 안 함). 단 핵심 공통 필드(`deck_meta`, `design_dependency`, `slides[]`의 R1 4필드 + R2 takeaway + R5 evidence_sources)는 고정.

#### 8. 사용자 검토 체크포인트

`slide_plan.json`과 함께 **슬라이드별 1줄 markdown 요약**을 사용자에게 제시:

```
1. cover           — "Q3 보드 리뷰" / why_here: 데크 진입점
2. bottom_line     — "매출 +18% YoY는 지속 불가, 신규 채널 의존 ↑" / kpi-grid
3. executive_summary — "3대 의사결정 필요 영역" / summary
4. evidence (chart) — "신규 채널 매출 비중 추이" / forecast-table / forecast
...
```

사용자 confirm 후 `/slide`로 진행.

### 출력

단일 파일: `output/<project-name>-pptx/slide_plan.json`

---

## /slide 와의 통합

`/slide`는 진입 시 `output/<project-name>-pptx/slide_plan.json` 존재 여부로 자동 분기:

- **있음** (systematic 경로) — 이 plan을 입력으로 받아 각 슬라이드의 `recommended_layout_family`를 `pptx-boilerplate/`에서 그대로 복사·교체. R2/R5는 빌드 시점에 재검증 (`build.mjs`가 validate_plan.py 호출).
- **없음** (simple 경로) — LLM이 brief에서 즉흥 결정. 본 스킬 미사용.

자동 chain wrapper(`/slide-with-plan` 같은)는 추가하지 않는다 — 사용자가 의도적으로 두 단계를 분리할 수 있어야 한다.

---

## 참고 문서

| 문서 | 내용 |
|---|---|
| `references/deck-types.md` | 8 deck_type 정의 + narrative arc 시작점 휴리스틱 |
| `references/slide-roles.md` | 공통 8 role + deck_type별 추가 enum |
| `references/chart-rhetoric.md` | 9 chart_strategy 어휘 (mckinsey-pptx 추상화) + custom fallback |
| `references/slide-plan-schema.md` | slide_plan.json 핵심 필드 + 변형 자유 영역 + 예시 |
| `examples/consulting-deck-plan.json` | 골든 예시 1건 (jangpm + consulting deck 10장) |
| `scripts/validate_plan.py` | R2/R5 자동 검증 (exit 1로 빌드 거부) + R1/R3/R4 lint |

---

## 사용자 발언별 행동 가이드

| 사용자 발언 | 행동 |
|---|---|
| "/slide-plan" / "체계적으로 기획해줘" | 즉시 이 스킬 진입 → 8단계 워크플로우 → slide_plan.json + markdown 요약 → 사용자 confirm → "/slide로 빌드하시겠어요?" |
| "데크 구조부터 짜줘" | 동일 |
| "그냥 슬라이드 만들어줘" | 이 스킬 사용 안 함 — `/slide` simple 경로로 직행 |
| 사용자가 이미 slide_plan.json을 손으로 만듦 | 이 스킬 skip — `/slide`가 자동 감지 |
