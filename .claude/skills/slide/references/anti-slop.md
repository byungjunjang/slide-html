# Anti-slop — 슬라이드 디자인 자기 검증 체크리스트

> 4 hard constraint(`references/4-constraints.md`)는 **PPTX 호환성**을 보장한다. 본 문서는 **디자인 톤·시각 다양성**을 보장한다. 둘은 직교한다.

LLM이 작성을 마치고 빌드 직전, **데크 전체를 자기 점검**한다. 한 가지 항목이라도 ❌면 그 슬라이드/데크를 수정한다. ✅는 적극 추구한다.

---

## 1. 카테고리 분포 (Most Important)

DESIGN.md §5 의 6 카테고리(Hero / Visual-Primary / Editorial / Density / Sequence / Narrative) 분포 자체 점검.

- ❌ **Hero/Impact (A) 0장** — 데크 안에 "120% 다듬은 한 장"이 없으면 임팩트 0. ≥5장 데크면 1장 이상 의무.
  - 픽스: `mega-quote` / `mega-number` / `dramatic-type` / `bold-statement-split` 중 1장 추가 또는 기존 슬라이드 1장을 격상.
- ❌ **Visual-Primary (B) 0장** — 텍스트만 N장 = 단조. ≥8장 데크면 2장 이상 의무.
  - 픽스: `annotated-screenshot` / `diagram-as-hero` / `before-after-split` / `knowledge-graph` 중 1-2장 추가.
- ❌ **Density (D)가 데크의 50% 초과** — "카드 그리드 도배" 안티패턴. 12장 중 7장 이상 D 카테고리면 ❌.
  - 픽스: 일부 D 슬라이드를 Visual-Primary 또는 Editorial로 재할당. 예: kpi-grid → annotated-screenshot, three-point → numbered-progression.
- ❌ **같은 카테고리 연속 3장 이상** — 카테고리 간 회전 강제.
  - 픽스: 슬라이드 순서 재배열. 또는 1-2장을 다른 카테고리로 격상.
- ❌ **같은 어휘(`three-point`, `kpi-grid` 등) 연속 2장 이상** — 어휘 회전.

---

## 2. 시각 주역 다양성 (visual main-character rotation)

데크 안에서 **시각 주역 타입**이 회전해야 한다. huashu-design의 "13페이지 주역 회전" 원칙 그대로.

- ❌ "title + 3 bullets" 패턴이 데크의 절반 이상 — 가장 흔한 안티패턴.
- ❌ 모든 슬라이드의 H2 타이틀이 같은 위치·크기·색 — 격상이 없는 데크.
- ❌ 모든 number-circle 슬라이드의 동일 layout (왼쪽 circle + 우측 텍스트) 반복.
- ❌ 모든 Density 슬라이드가 `card-accent` 1개 + `card` 2개의 동일 강조 패턴.
- ✅ 시각 주역 타입 회전: 카드 그리드 → 다이어그램 → 큰 인용 → 표 → 이미지 + callout → 본문 + 마진 노트
- ✅ Hero 슬라이드 1장은 의도적으로 임팩트 ↑ (다른 슬라이드 대비 글자 크기·여백·색 강도 격상)

---

## 3. "120% 다듬은 한 장" 의무 (huashu-design 원칙)

> 한 디테일은 120%, 나머지는 80%. 균등하게 80%는 평범, 1장 120%가 데크의 인상을 결정.

- ❌ 모든 슬라이드가 같은 가공 강도(글자 크기·여백·색 강도가 균질) — 데크에 hero 슬라이드 0장.
- ✅ 데크 안에 1장: 가장 임팩트 있는 hero 슬라이드 (Category A · Hero/Impact 중 1개)
- ✅ 그 1장에서 typography·여백·accent를 데크 평균보다 **확실히** 다르게

---

## 4. closing 규칙 (사용자 명시)

- ❌ closing이 다크 모드 (`closing-big` / `closing-dark` / `bg-text` 풀블리드 closing) — 사용자 규칙: closing은 light only.
- ✅ closing은 항상 `closing-light` (21-closing-light) 사용. 데크 톤 무관, 모든 데크가 light closing.
- ✅ closing-light **안에서 변형은 자유** — 캐릭터 vs 빈 공간 / CTA 메시지 vs 감사 메시지 / 메타 위치 변주 / 큰 한 줄 vs 짧은 두 줄 등.
- 다양성은 closing 어휘 선택이 아니라 **closing-light 안의 body 변형**에서 만든다.

---

## 5. 색·톤 감정

- ❌ accent를 슬라이드 1장에 3 events 이상 — monochrome 무드 깨짐.
- ❌ semantic 색(positive/negative/warning) 일반 텍스트 강조에 사용 — 데이터 전용.
- ❌ 다크 카드(`card-dark`, `bg-text`)를 본문 카드로 남발 — 다크는 closing 또는 terminal에만.
- ❌ 모든 카드를 `card-accent`로 — 강조의 의미 사라짐.
- ✅ accent 슬라이드당 1-2 events
- ✅ 카드 강조는 1개만 `card-accent`, 나머지는 `card`

---

## 6. 카피·언어 (Voice 규약 — jangpm 디폴트)

- ❌ "여러분", "당신", "저는" — 1·2인칭 금지 (third-person institutional)
- ❌ 의문형 슬라이드 타이틀 (e.g., "AI는 정말 위협일까?") — 선언형으로 결론 진술 ("AI는 보조도구일 뿐 위협이 아니다.")
- ❌ "~합니다만", "~할 수도 있습니다" hedging — analytical declarative ("~다", "~한다")
- ❌ 50자 넘는 한 줄 본문 — 강제 줄바꿈 또는 카드 분리
- ✅ 슬라이드 타이틀: 키워드만 `c-accent` 인라인 span (jangpm 시그니처)

---

## 7. 정보 밀도 균형

- ❌ 한 슬라이드에 7+ 항목의 카드 그리드 — 사람이 한 번에 처리 못 함. 6개 한도, 그 이상은 카테고리화 후 분할.
- ❌ 한 카드에 50자 이상 본문 — 카드 작아져서 가독성 ↓
- ❌ chart·table 슬라이드에서 takeaway 누락 — R2 위반.
- ✅ 한 슬라이드 = 1 핵심 메시지 + 3-6개 지원 항목 + 1 시각 주역
- ✅ chart/table 항상 한 줄 인사이트 동반 (헤드라인 또는 gm-band)

---

## 8. 캐릭터 / 데코 (jangpm 특수)

- ❌ 본문 슬라이드에 jangpm-character 등장 — character는 cover 한정.
- ❌ 표지 우측 캐릭터 자리에 도형(원/halo/dot) 데코 — 어색해진다. 캐릭터 또는 빈 공간만.
- ❌ 모든 표지가 `01-title` 변형 — 23(친근) / 25(세로형) 중 데크 톤에 맞게 선택.

---

## 9. chrome 일관성 (preset 톤 보존)

- ❌ 슬라이드마다 헤더 위치/스타일이 다름 — 데크 grammar 깨짐.
- ❌ section eyebrow ("SECTION 02 · 핵심") 폰트·색 슬라이드별 변동.
- ❌ gm-band 어떤 슬라이드는 있고 어떤 슬라이드는 없는데 일관 기준 없음.
- ✅ chrome (header eyebrow + page counter + footer/gm-band)는 모든 슬라이드 통일 — preset의 시그니처.
- ✅ body 영역(시각 주역)만 다양화 — chrome 통일 + body 다양 = jangpm 톤 유지하면서 다양성 회복.

---

## 10. 자기 검증 흐름 (LLM 작성 마무리 직전)

LLM이 데크 작성을 마치고 빌드 직전:

1. 카테고리 분포 카운트 — Hero/Visual-Primary/Editorial/Density/Sequence/Narrative 별로 몇 장씩
2. 위 §1 ~ §9 체크리스트 항목 위반 여부 점검
3. **§11 jangpm 시그니처 self-check** — preset 정체성 보존 확인
4. **§12 미세 서식 self-check** — `references/text-formatting-rules.md` 통과
5. 위반 발견 시 슬라이드 재할당 또는 어휘 교체
6. 재빌드 후 PPTX 검증

**한 항목이라도 ❌면 빌드를 mark complete 하지 말 것**. 위반은 필연적으로 "매번 비슷한 패턴" 또는 "jangpm 톤 옅어짐" 결과로 이어진다.

---

## 11. jangpm 시그니처 self-check (preset 정체성)

> 새 어휘로 작곡한 슬라이드도 jangpm 톤이 살아 있어야 한다. 어휘 다양성은 늘리되 **preset 정체성은 모든 슬라이드에서 보존**.

### 데크 전체 체크

- [ ] **모든 본문 슬라이드 chrome 동일**: top eyebrow + page counter + .rule divider 위치/스타일이 N장 모두 일치
- [ ] **모든 본문 슬라이드가 anchor 보일러플레이트에서 chrome 골격 복사**: §5 어휘 표의 anchor 컬럼 따랐는지
- [ ] **Density 카테고리 50% 이하** (절대 cap). 카테고리 분포는 양 권장하지 않음 — 어휘 다양성·변형 자유도가 우선. 50% 안 넘기면 자유
- [ ] **jangpm 토큰만 사용**: `colors_and_type.css` 변수 + `_pptx-slide.css` 헬퍼만. 임의 hex / 임의 폰트 / 외부 색 ❌
- [ ] **single-accent 정책**: accent 색은 `#4633E3` 인디고만. 슬라이드별 임의 accent 색 ❌
- [ ] **monochrome 무드**: 전체 데크가 warm off-white 배경 + indigo accent로 통일. 다크 배경은 closing/terminal 만

### 슬라이드별 시그니처 1개 이상

각 본문 슬라이드는 다음 jangpm 시그니처 중 **1개 이상** 포함:

- [ ] 슬라이드 타이틀의 키워드 인라인 c-accent (`<h2 class="t-h2">...<span class="c-accent">키워드</span>...</h2>`)
- [ ] `tbl-row`/`tbl-cell` div grid 표 (Density 카테고리)
- [ ] `card` vs `card-accent` 강조 1개 패턴 (overview/three-point/four-point)
- [ ] `number-circle` / `number-circle-lg` 번호 패턴 (line-height = 컨테이너 height 의무)
- [ ] `gm-band` 한 줄 인사이트
- [ ] `t-cap-up` uppercase eyebrow (chrome 또는 카드 헤드)
- [ ] Pretendard 9 weights 활용 (가벼운 본문 + 굵은 강조 대비)

### 시그니처 0개 슬라이드 = ❌

새 어휘로 작곡했는데 위 시그니처가 하나도 없으면 → "다른 디자인 시스템처럼 보이는" 슬라이드. anchor 보일러플레이트로 돌아가서 chrome/시그니처 다시 가져올 것.

### Hero/Editorial 카테고리 예외

- Hero/Impact 슬라이드는 chrome 간소화 가능 (mega-quote, dramatic-type 등) — 단 anchor의 메타 표기(JANGPM × ... · EP.NN, 페이지 번호) 패턴은 유지
- Editorial 카테고리는 chrome 그대로 + body만 magazine-style — 시그니처 자동 보존

---

## 12. 미세 서식 self-check

`references/text-formatting-rules.md` §10 체크리스트 통과 확인:

### 슬라이드별 (작성 직후)

- [ ] 원/badge 안 텍스트 `line-height` = 컨테이너 height 와 일치 (number-circle: 22pt, number-circle-lg: 28pt, badge: 9pt)
- [ ] **number-circle 같은 row 안 다른 텍스트(t-h3, t-title 등)에도 line-height = 원 height 명시** — vertical center 정렬 강제
- [ ] **요소 간 좌표 오버랩 없음** — `references/text-formatting-rules.md` §11 오버랩 자기 점검 통과. 특히 본문 길어진 row와 다음 absolute 블록, pull-quote 박스 height와 다음 블록, 마지막 블록과 gm-band(bottom 18pt)
- [ ] 카드 padding 18pt 20pt (또는 ±4pt 이내)
- [ ] gm-band 있으면 bottom: 18pt + text-align: center
- [ ] inline span에 margin 없음
- [ ] 본문 1줄 ≤ 50자 한글
- [ ] accent events 슬라이드당 1-2

### 데크 전체

- [ ] chrome (top eyebrow + page counter + .rule) 모든 본문 슬라이드 동일
- [ ] 본문 슬라이드 chrome이 anchor 보일러플레이트와 일치
- [ ] 표지 우측 도형 데코 없음 (캐릭터 또는 빈 공간만)
- [ ] closing은 항상 `closing-light` (다크 closing 사용 금지)

미세 서식 위반은 빌드는 통과하지만 **PPT에서 visual polish가 깨진다** — 원형 텍스트가 살짝 하단으로 쏠리거나, 카드 호흡이 슬라이드별로 다르거나, gm-band가 양쪽 정렬이 안 맞거나. 한 슬라이드의 미세 서식이 깨지면 데크 완결성이 무너진다.
