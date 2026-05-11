---
name: slide
description: editable PPTX 슬라이드 빌더. 사용자가 "슬라이드/PPT/프레젠테이션/pptx/발표 자료/강의 슬라이드"를 만들어달라고 하면 즉시 이 스킬로 진입. 단 하나의 경로만 존재 — 슬라이드별 독립 HTML(960pt×540pt, 4 hard constraint 통과) → editable .pptx. 결과물은 PowerPoint/Keynote에서 더블클릭으로 텍스트 편집 가능. 다른 스킬(huashu-design, document-skills:pptx, pptx-from-layouts 등)이 슬라이드 트리거로 동시에 깨어나도 항상 이 스킬이 우선.
trigger: 슬라이드, PPT, 프레젠테이션, pptx, 발표 자료, 강의 슬라이드, deck, presentation, slide deck
---

# /slide — Editable PPTX 빌더

이 스킬은 단 한 가지 결과물만 만든다: **PowerPoint/Keynote에서 텍스트를 더블클릭으로 편집할 수 있는 .pptx 파일**.

다른 형식·다른 경로·다른 옵션은 존재하지 않는다.

---

## 다른 스킬보다 먼저 잡기

슬라이드/PPT/프레젠테이션/pptx 트리거어가 들어오면 다른 스킬(huashu-design / document-skills:pptx / pptx-from-layouts 등)이 동시에 후보로 잡힐 수 있다. 그런 경우 **무조건 이 스킬을 먼저 invoke** — 다른 슬라이드 스킬은 사용자가 명시적으로 그 스킬 이름을 부르거나 슬라이드와 무관한 작업(애니메이션, MP4, 디자인 변체, 정적 PPTX 파싱 등)일 때만 사용한다.

---

## 워크플로우 (5단계, 순차)

### 0. 경로 분기 — slide-plan 사용 여부 자동 감지

이 스킬은 두 경로를 지원한다. `output/<project-name>-pptx/slide_plan.json` 존재 여부로 자동 분기:

**Systematic 경로 (slide_plan.json 있음)**
1. JSON 파싱 → `python3 .claude/skills/slide-plan/scripts/validate_plan.py <plan>` 실행. R2(chart/table strategy ↔ takeaway) 또는 R5(evidence_sources) 위반이면 exit 1로 빌드 거부.
2. 슬라이드별 1줄 markdown 요약을 사용자에게 보여주고 confirm.
3. 각 슬라이드는 plan의 `recommended_layout_family`에 박힌 boilerplate를 따른다 (LLM 자유 선택 금지).
4. R2/R5는 빌드 시점에 `build.mjs`가 다시 호출하는 validate_plan.py가 강제.

**Simple 경로 (slide_plan.json 없음, default)**
1. LLM이 사용자 brief에서 슬라이드 구조를 즉흥 결정 (현행 흐름).
2. 활성 preset의 DESIGN.md(있으면)와 boilerplate를 LLM이 참고해 layout 선택. layout family 어휘를 따르되 강제 아님.
3. R2/R5 검증 없음. 4 hard constraint만 (export_deck_pptx 안에서) 수행.

**경로 선택 가이드 (사용자 발언별)**

| 사용자 발언 | 경로 |
|---|---|
| "슬라이드 만들어줘" / "PPTX로" / "발표자료 필요해" | **Simple** (default) |
| "체계적으로 기획해줘" / "데크 구조부터" / "/slide-plan" | **Systematic** — `/slide-plan` 먼저 호출 후 `/slide` |
| 사용자가 직접 `slide_plan.json`을 작성해 둠 | **Systematic** (자동 감지) |

### 1. 프로젝트 셋업

```bash
bash .claude/skills/slide/scripts/init-project.sh <project-name>
```

자동 생성: 각 생성 요청 = `output/<project-name>-pptx/` 한 폴더로 격리

```
output/<project-name>-pptx/
├── slides/                  (NN-name.html — 파일명 순으로 빌드)
│   └── 01-title.html        (보일러플레이트 1장)
├── icons/                   (외부 SVG)
├── design-system/           (선택된 프리셋의 복사본 — 자기완결, zip/이동 안전)
├── _pptx-slide.css          (html2pptx-safe 헬퍼)
├── build.mjs                (빌드 스크립트)
├── <project-name>.pptx      (빌드 결과물 — 같은 폴더에 떨어짐)
└── README.md
```

**의존성** (한 번만 설치):

로컬 (slide-html 리포):
```bash
cd <repo-root>          # 또는 cd .claude/skills/slide
npm install playwright pptxgenjs sharp
npx playwright install chromium
```

claude.ai (이 스킬 폴더만 zip해서 업로드한 경우):
```bash
cd .claude/skills/slide
npm install
npx playwright install chromium
```

이 스킬 번들은 자기완결입니다 — 빌드에 필요한 모든 코드(`scripts/export_deck_pptx.mjs`, `scripts/html2pptx.js`, `scripts/prebuild-svg.mjs`)와 디자인 시스템(`assets/design-systems/`)이 폴더 안에 들어 있습니다.

### 2. 슬라이드 작성 — Compose, don't copy

각 슬라이드 = `slides/NN-name.html` 한 파일. 파일명 순으로 데크가 빌드됨.

> **핵심 행동 모델 변경 (2026-04-30)**: 보일러플레이트는 **메뉴**가 아니라 **참고 갤러리**다. LLM은 brief를 받으면 보일러플레이트에서 "가까운 거 복사"하지 말고, **시각 어휘에서 작곡**한다. 같은 preset 안에서도 슬라이드 다양성이 회복되는 핵심 단계.

**모든 슬라이드 필수 사항**:
- body 사이즈 = `960pt × 540pt` (LAYOUT_WIDE)
- `<link rel="stylesheet" href="../_pptx-slide.css">`
- **4 hard constraint 통과** (자세한 룰: `references/4-constraints.md`)
  1. 텍스트는 `<p>` 또는 `<h1>~<h6>` 안에만
  2. CSS gradient (linear/radial) 금지 — 순색만
  3. `<p>/<h*>`에 background/border/shadow 금지 — 외부 div가 담당
  4. div에 `background-image` 금지 — `<img>` 태그 사용

#### 2.1 슬라이드별 5 questions (작성 전)

매 슬라이드를 작성하기 전, mentally 답한다 (1줄씩, 빨리). LLM이 default "카드 그리드"로 가는 걸 막는 break.

1. **서사 역할** — 이 슬라이드가 데크에서 무엇을 하는가? (cover / context / data / hero / quote / summary / closing 중 1개)
2. **관객 거리** — 발표(투영) / 인쇄물(혼자 읽기) / Slack 공유(썸네일)? 거리에 따라 글자 크기 다름.
3. **시각 온도** — 차분 / 단호 / 분석적 / 따뜻 / 강조 중 어떤 톤? (jangpm 디폴트 = 분석적·선언형, 단 hero 슬라이드는 단호 또는 강조로 변용 가능)
4. **시각 주역 카테고리** — 위 답에 맞는 visual main-character 카테고리는? (DESIGN.md §5 의 6 카테고리: Hero/Visual-Primary/Editorial/Density/Sequence/Narrative)
5. **이 슬라이드의 한 가지 변형은?** — anchor의 표준 패턴에서 어떤 한 가지를 다르게 할 것인가? DESIGN.md §5 어휘 표의 **"변형 영감" 컬럼** 참조. 표준 그대로 쓰지 말고 1개 이상 적용 — v2의 창의성은 표준 패턴 위에 의도적 변형을 더한 데서 나왔다. (예외: Narrative 카테고리는 anchor 거의 그대로 — 톤 keepers)

#### 2.2 작곡 흐름 (7 step)

1. **카테고리 결정** — 5 questions의 답이 카테고리를 알려줌 (Q4 답이 카테고리, Q5 답이 변형 의도)
2. **어휘 선택** — DESIGN.md §5 의 그 카테고리 어휘 표에서 1개 선택
3. **anchor 보일러플레이트 식별 + Read (의무)** — 어휘 옆 "anchor 보일러플레이트" 컬럼의 파일을 `Read` 해서 chrome 골격(top eyebrow + page counter + .rule + 옵션 gm-band) + 미세 서식(카드 padding, number-circle line-height, accent 사용 빈도)을 정확히 파악. **chrome은 그대로 복사**.
4. **body 영역 작곡** — chrome은 anchor에서 가져온 그대로, body 영역만 어휘 가이드대로 변형. **Narrative 카테고리(cover/closing-light/section-divider/summary)만 anchor 거의 그대로 사용** — 톤 keepers. 다른 5 카테고리(Hero/Visual-Primary/Editorial/Density/Sequence)는 anchor에서 chrome + 미세 서식 복사한 뒤 **body는 변형 영감 컬럼에서 1개 이상 선택 적용 권장**. 표준 패턴 그대로 쓰지 말고 한 가지 의도적 변형을 더해라 — v2의 창의성은 여기서 나왔다.
5. **미세 서식 self-check** — `references/text-formatting-rules.md` §10 체크리스트 통과 (원형 텍스트 line-height = 컨테이너 height, 카드 padding 18pt 20pt, accent 1-2 events, inline span margin 없음 등).
6. **jangpm 시그니처 self-check** — `references/anti-slop.md` §11 통과 (chrome 일관, jangpm 토큰만 사용, 슬라이드별 시그니처 1개 이상 — 키워드 c-accent 인라인 / tbl-row div grid / number-circle 패턴 등).
7. **카테고리 분포 자기 점검** — 데크 전체에서 cap을 안 넘기는지 확인 (DESIGN.md §10). 양 권장 분포는 두지 않음 — 어휘 다양성·변형 자유도가 우선. Hero/Visual-Primary 0장 / Density 50%+ / 같은 카테고리 연속 3장 / 같은 어휘 연속 2장 = ❌. closing은 항상 closing-light = ✅.

**핵심 모델**: chrome + 미세 서식 = jangpm 정체성 (anchor에서 그대로 복사). body 영역 = 어휘 다양성 (시각 다양성의 원천). 둘은 분리 관리.

#### 2.3 보일러플레이트 카탈로그 (참고용)

- 베이스라인 8개 (01~08): 모든 preset 공통. 디자인 시스템 검증·최소 동작 보장.
- 콘텐츠 패턴 09~: preset별로 보유 여부 다름. `jangpm`은 09~37 (29개) 추가 제공. 실제 보유 목록은 `ls assets/design-systems/<preset>/pptx-boilerplate/`.
- **위상**: 어휘 표(DESIGN.md §5)의 "보일러플레이트 참고" 컬럼에 매핑됨. 카탈로그에 없는 어휘(`mega-quote`, `mega-number`, `dramatic-type`, `annotated-screenshot`, `single-portrait-quote`, `diagram-as-hero`, `image-with-callouts`, `knowledge-graph`, `margin-note-layout`, `pull-quote-inline`, `drop-cap-opener`, `magazine-columns`, `timeline-horizontal`, `numbered-progression`, `bold-statement-split`, `full-bleed-image-with-overlay`)는 **신규 작곡** — 보일러플레이트 만들지 말고 슬라이드 안에서 직접 작곡.

#### 2.4 ≥5장 데크: 2-page Showcase Checkpoint (필수)

데크 5장 이상이면 처음부터 12장 일괄 작성하지 말 것. **시각적으로 가장 다른 2장**을 먼저 작성·빌드·사용자 확인 받고, 그 다음 일괄 추진.

**Showcase 페어 선택 가이드** (시각 차이 최대화):
- 옵션 A: cover (Narrative) + Hero/Impact 1장 — chrome 톤 + 임팩트 강도 모두 검증
- 옵션 B: Density 1장 (KPI 또는 표) + Visual-Primary 1장 (다이어그램 또는 이미지) — 정보 밀도 vs 시각 자체
- 옵션 C: section-divider + closing — 데크의 시작과 끝 톤 검증

흐름:
1. 위 페어 중 1개 선택해 2장 작성
2. `cd output/<project>-pptx && node build.mjs` (이때 빌드 성공·실패만 확인 — 디자인 검증은 사용자가 함)
3. 사용자에게 "이 2장의 grammar (chrome / 톤 / 인용 처리 / hero 임팩트 강도)로 나머지 N-2장 진행해도 될지" 확인
4. 확인 받으면 일괄 추진 (5단계 작곡 흐름 적용)

**왜 2장 먼저인가**: 같은 jangpm 안에서도 hero 슬라이드의 임팩트 강도, 인용 처리 방식, 카테고리 분포 같은 grammar는 데크마다 다르다. 12장 다 만들고 나서 "방향 다시" = 12번 재작업. 2장 sign-off = 2번 재작업.

**경로별 매핑 규칙**

- **Systematic 경로** — `slide_plan.json`의 각 슬라이드 `recommended_layout_family`를 어휘 이름(DESIGN.md §5의 카테고리 어휘)으로 채운다. `core_message`는 슬라이드 가장 큰 텍스트 슬롯, `chart_takeaway` / `table_takeaway`는 시각 위/아래 인사이트 슬롯 (R2 강제). 작곡은 4 hard constraint 통과 자유.
- **Simple 경로** — LLM이 5 questions → 어휘 선택 → 변형 영감 적용 → 작곡 흐름. 보일러플레이트는 참고 갤러리.

### 3. 빌드

```bash
cd output/<project-name>-pptx
node build.mjs
```

성공 시:
```
Converting N slides via html2pptx...
  [1/N] 01-title.html ✓
  ...
✓ Wrote .../output/<project-name>-pptx/<project-name>.pptx (N/N slides, editable PPTX)
```

**결과물 위치**: 작업 공간과 같은 폴더(`output/<project-name>-pptx/<project-name>.pptx`). 각 생성 요청 건이 `output/` 하위 한 폴더에 자기 슬라이드·CSS·빌드 산출물까지 모두 담아 자기완결적으로 유지된다.

### 4. 에러 픽스

실패한 슬라이드는 `references/error-patterns.md`의 알려진 픽스 적용. 자주 발생 7가지:

| 에러 | 픽스 |
|---|---|
| `Text element <p> has background` | 외부 div 가 배경 담당 |
| `DIV element contains unwrapped text` | `<p>` 또는 `<h*>` 으로 감싸기 |
| `CSS gradients are not supported` | 순색으로 |
| `Background images on DIV` | `<img>` 태그로 |
| `HTML content overflows body` | 콘텐츠 줄이기 / 폰트 축소 |
| `ends too close to bottom edge` | bottom ≥ 44pt |
| `Inline element <span> has margin` | margin 제거, `&nbsp;` 사용 |

### 5. 검증

- **디자인 anti-slop self-check** — 빌드 직전 `references/anti-slop.md` §1-§9 (시각 다양성), §11 (jangpm 시그니처), §12 (미세 서식) 통과 여부 확인. 한 항목이라도 ❌면 그 슬라이드 재작성.
- **미세 서식 self-check** — `references/text-formatting-rules.md` §10 체크리스트 통과. 원형/badge 텍스트 line-height = 컨테이너 height, 카드 padding 18pt 20pt, gm-band centered, inline span margin 없음 등.
- PowerPoint/Keynote/LibreOffice에서 .pptx 열기
- 임의 텍스트 더블클릭 → 직접 편집 가능 확인
- N/N 통과율 확인

---

## 디자인 시스템

기본: **jangpm** (한국어 강의/리포트 데크용, 인디고 단일 악센트, Pretendard 9 weights). 토큰은 `design-system/colors_and_type.css`에서 정의되고, `_pptx-slide.css` 가 그 위에 html2pptx-safe 헬퍼 클래스를 얹는다.

다른 프리셋은 `init-project.sh <name> <preset>` 으로 지정. 사용 가능한 프리셋 목록은 `assets/design-systems/README.md`에 자동 생성되어 있다 (theme-init이 새 프리셋을 만들 때 갱신).

---

## 새 디자인 시스템 추가 (Claude Code 로컬 전용)

이 스킬의 멀티 프리셋 모델은 사용자가 새 브랜드를 추가할 수 있게 한다. 새 디자인 가이드(MD) 또는 완결된 프리셋 폴더가 있으면 `/theme-init` 으로 한 번에 다음을 자동 생성한다:

- `theme.json` (v1 토큰 컨트랙트)
- `colors_and_type.css` (CSS 변수)
- `_pptx-slide.css` (이 프리셋의 헬퍼 클래스)
- `pptx-boilerplate/01~08-*.html` (이 프리셋으로 토큰 치환된 베이스라인 보일러플레이트 8장 — 모든 preset 공통 의무 산출물. preset 작성자가 콘텐츠 패턴 09~를 추가로 제공해도 되지만 의무는 아님)
- `brand-spec-generated.md` (인간 가독 토큰 레퍼런스)

`/theme-init`은 별도 스킬(`.claude/skills/theme-init/`)이며 **Claude Code 로컬 환경 전용**이다 (claude.ai에는 업로드하지 않음). theme-init은 결과물을 이 슬라이드 번들의 `assets/design-systems/<new-preset>/`에 직접 떨구고, `assets/design-systems/README.md` 카탈로그를 자동 갱신한다.

생성된 프리셋은 즉시 `init-project.sh <project> <new-preset>` 으로 사용 가능. theme-init 사용법 상세는 `.claude/skills/theme-init/SKILL.md`.

---

## 참고 문서

| 문서 | 내용 |
|---|---|
| `references/4-constraints.md` | 4 hard constraint 상세 + OOXML 근거 (PPTX 호환성) |
| `references/anti-slop.md` | **디자인 anti-slop 자기 검증 체크리스트 (시각 다양성 + jangpm 시그니처)** |
| `references/text-formatting-rules.md` | **미세 서식 polish 규칙 (원형 텍스트 valign, 카드 padding, BR 처리, accent 빈도 등)** |
| `references/error-patterns.md` | 알려진 빌드 에러 + 픽스 (E1~E12) |
| `references/css-helpers.md` | `_pptx-slide.css` 헬퍼 클래스 카탈로그 |
| `references/canvas-spec.md` | 960pt × 540pt 캔버스 / 좌표 / 폰트 가이드 |
| `assets/design-systems/<preset>/pptx-boilerplate/*.html` | 베이스라인 8 패턴 (01~08, 모든 preset 공통) + preset별 추가 콘텐츠 패턴. `jangpm`은 29 패턴(09~37) 추가 제공. 실제 보유 목록은 `ls assets/design-systems/<preset>/pptx-boilerplate/`로 확인 |
| `assets/design-systems/<preset>/_pptx-slide.css` | preset 별 공통 CSS (프로젝트마다 복사됨) |
| `assets/design-systems/<preset>/colors_and_type.css` | preset 토큰 (색/타이포) — 프로젝트마다 복사됨 |
| `assets/design-systems/README.md` | 사용 가능한 모든 preset 카탈로그 (theme-init이 자동 갱신) |
| `templates/build.mjs.template` | 빌드 스크립트 템플릿 (프로젝트마다 복사됨) |
| `scripts/init-project.sh` | 프로젝트 셋업 자동화 (preset → output 복사) |
| `scripts/export_deck_pptx.mjs` + `html2pptx.js` | HTML → editable PPTX 변환 엔진 (Playwright + pptxgenjs) |
| `scripts/prebuild-svg.mjs` | 빌드 직전 icons/*.svg를 PNG로 래스터화 (PptxGenJS의 SVG embed 버그 우회) |

---

## 사용자 발언별 행동 가이드

| 사용자 발언 | 행동 |
|---|---|
| "슬라이드 만들어줘" | 즉시 이 스킬 진입 → init-project → write → build |
| "PPTX로 변환해줘" | 동일 |
| "프레젠테이션 자료 필요해" | 동일 |
| "이거 PowerPoint로 줘" | 동일 |
| "PDF로 줄까 이미지 PPTX로 줄까" 옵션 묻기 | **금지**. 묻지 말고 editable PPTX로 직행 |
| "PPTX 말고 PDF가 더 좋을까?" | 사용자가 명시적으로 PDF를 요구한 경우만 PDF. 그 외엔 PPTX 직행 |
