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

### 0. 활성 디자인 시스템 로드 & 선언 (필수 — 가장 먼저)

슬라이드를 한 장이라도 만들기 전에 **반드시** 활성 프리셋을 읽고 한 줄로 선언한다. 이 announce-게이트가 "잘못된 테마로 데크 전체를 만든 뒤에야 깨닫는" 사고를 시작 시점에 차단한다.

```bash
python3 -c "import json,sys; sys.stdout.reconfigure(encoding='utf-8'); r='.codex/skills/slide/assets/design-systems'; \
a=json.load(open(f'{r}/active.json',encoding='utf-8'))['active']; \
t=json.load(open(f'{r}/{a}/theme.json',encoding='utf-8')); \
print(f\"[active design-system] {a} — accent {t['colors']['accent']}\")"
```
출력 예: `[active design-system] notion — accent #7C3AED` (active.json이 없으면 `jangpm` 폴백).

- **활성 프리셋 SSOT는 `assets/design-systems/active.json` 한 곳**이다. `/theme-init`이 새 프리셋을 구우면 자동으로 이 값을 갱신한다.
- `init-project.sh`를 **프리셋 인자 없이** 호출하면 이 active 프리셋이 자동 선택된다 (인자를 주면 그게 최우선).
- 사용자가 말한 디자인 시스템과 active가 **다르면** 빌드 전에 멈추고 확인한다 — 사용자 의도가 우선이며, `init-project.sh <project> <preset>`로 명시 전달하거나 `/theme-init`으로 active를 바꾼다.

### 0b. 경로 분기 — slide-plan 사용 여부 자동 감지

이 스킬은 두 경로를 지원한다. `output/<project-name>-pptx/slide_plan.json` 존재 여부로 자동 분기:

**Systematic 경로 (slide_plan.json 있음) — HARD 강제 단계:**

1. **Validator 재실행** (post-edit drift 차단)
   ```bash
   python3 .codex/skills/slide-plan/scripts/validate_plan.py output/<project-name>-pptx/slide_plan.json
   ```
   exit 1이면 빌드 거부 — 사용자에게 plan 수정 요청.

2. **Plan을 Read tool로 명시적 로드 + 슬라이드별 필드 출력 (필수)**
   ```
   Read output/<project-name>-pptx/slide_plan.json
   ```
   읽은 후 슬라이드별 다음 5필드를 콘솔에 출력해서 prompt 안에 stick시킨다 — 빠뜨리면 plan 무시 회귀:
   ```
   slide #N:
     family = <recommended_layout_family>
     core   = <core_message>
     why    = <why_here>
     chart  = <chart_strategy>:<chart_takeaway> (있으면)
     evidence = <evidence_sources>
   ```

3. **슬라이드 작성 시 plan SSOT 의무**
   - 각 슬라이드는 plan의 `recommended_layout_family` 어휘를 그대로 사용 (LLM 자유 선택 금지)
   - `core_message`는 슬라이드의 가장 큰 텍스트 슬롯에 들어가야 한다 (paraphrasing OK, 의미 보존 필수)
   - `chart_takeaway` / `table_takeaway`는 시각 위 또는 아래 인사이트 슬롯으로 배치
   - `evidence_to_use`의 source_id를 슬라이드 footer 또는 caption에 표기 (선택)

4. **빌드 직후 plan-fidelity self-check 의무** — Step 5 검증 참조 (B-plan-count + B-plan-fidelity)

**Simple 경로 (slide_plan.json 없음, default)**
1. LLM이 사용자 brief에서 슬라이드 구조를 즉흥 결정 (현행 흐름).
2. 활성 preset의 DESIGN.md(있으면)와 boilerplate를 LLM이 참고해 layout 선택. layout family 어휘를 따르되 강제 아님.
3. R2/R5 검증 없음. 4 hard constraint + B-density(simple)만 수행.

**경로 선택 가이드 (사용자 발언별)**

| 사용자 발언 | 경로 |
|---|---|
| "슬라이드 만들어줘" / "PPTX로" / "발표자료 필요해" | **Simple** (default) |
| "체계적으로 기획해줘" / "데크 구조부터" / "/slide-plan" | **Systematic** — `/slide-plan` 먼저 호출 후 `/slide` |
| 사용자가 직접 `slide_plan.json`을 작성해 둠 | **Systematic** (자동 감지) |

**Auto-trigger — 다음 조건 중 1개라도 충족하면 Systematic 모드로 자동 진입:**

1. 사용자가 슬라이드 수를 명시했고 그 수가 **≥ 10장**
2. 사용자가 **참고 파일**(xlsx / md / pdf / docx / pptx)을 첨부했거나 `inputs/` 폴더에 1개 이상 있음
3. 사용자 brief에 **태도/기대 키워드** 1개 이상 — `계획` / `철저` / `상세` / `꼼꼼` / `체계` / `완벽` / `정성` / `신중` / `제대로` / `완성도` / `퀄리티` / `고품질` / `thorough` / `detailed` / `comprehensive` / `polished` / `careful` / `deep`

자동 진입 시 사용자에게 1줄 안내:
```
slide-plan 자동 진입 — 조건 충족: <어떤 조건이 트리거됐는지>
/slide-plan으로 slide_plan.json을 먼저 생성한 뒤 /slide가 그 plan을 소비합니다.
명시적으로 simple 모드를 원하시면 `simple로` / `plan 없이` 라고 응답하세요.
```

명시적 우회 keyword (`simple로`, `plan 없이`, `빠르게`, `간단히`, `quick`)가 들어오면 trigger 무시하고 simple로. **단 데크가 ≥10장이면** `output/<project-name>-pptx/.deck-mode`에 `simple` 한 단어를 기록한다 — `verify_deck.py`의 plan-강제 게이트가 이 마커로 정당한 대형 simple 덱을 통과시킨다 (마커가 없으면 ≥10장 무계획은 하드 페일).

### 1. 프로젝트 셋업

```bash
bash .codex/skills/slide/scripts/init-project.sh <project-name>
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
cd <repo-root>          # 또는 cd .codex/skills/slide
npm install playwright pptxgenjs sharp
npx playwright install chromium
```

claude.ai (이 스킬 폴더만 zip해서 업로드한 경우):
```bash
cd .codex/skills/slide
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
- **`data-layout` 태그** — 슬라이드 루트 `<body data-layout="<family>">`. family는 `references/layouts.md`의 15개 중 1개(선택한 §5 어휘가 귀속되는 family). 빌드 prebuild 다양성 게이트(**HARD, --strict**)가 커버리지·distinct·card-type 비율·visual 존재를 점검 — 태그 누락/다양성 미달이면 빌드가 실패한다. 증거 이미지/차트/다이어그램 슬롯에는 추가로 `data-image-slot="<name>"`.

#### 2.1 슬라이드별 5 questions (작성 전)

매 슬라이드를 작성하기 전, mentally 답한다 (1줄씩, 빨리). LLM이 default "카드 그리드"로 가는 걸 막는 break.

1. **서사 역할** — 이 슬라이드가 데크에서 무엇을 하는가? (cover / context / data / hero / quote / summary / closing 중 1개)
2. **관객 거리** — 발표(투영) / 인쇄물(혼자 읽기) / Slack 공유(썸네일)? 거리에 따라 글자 크기 다름.
3. **시각 온도** — 차분 / 단호 / 분석적 / 따뜻 / 강조 중 어떤 톤? (jangpm 디폴트 = 분석적·선언형, 단 hero 슬라이드는 단호 또는 강조로 변용 가능)
4. **시각 주역 카테고리** — 위 답에 맞는 visual main-character 카테고리는? (DESIGN.md §5 의 6 카테고리: Hero/Visual-Primary/Editorial/Density/Sequence/Narrative)
5. **이 슬라이드의 한 가지 변형은?** — anchor의 표준 패턴에서 어떤 한 가지를 다르게 할 것인가? DESIGN.md §5 어휘 표의 **"변형 영감" 컬럼** 참조. 표준 그대로 쓰지 말고 1개 이상 적용 — v2의 창의성은 표준 패턴 위에 의도적 변형을 더한 데서 나왔다. (예외: Narrative 카테고리는 anchor 거의 그대로 — 톤 keepers)

#### 2.2 작곡 흐름 (7 step)

1. **카테고리 결정** — 5 questions의 답이 카테고리를 알려줌 (Q4 답이 카테고리, Q5 답이 변형 의도)
2. **어휘 선택** — DESIGN.md §5 의 그 카테고리 어휘 표에서 1개 선택. 그 어휘가 귀속되는 `data-layout` family를 `<body>`에 부여 (`references/layouts.md` 매핑 표 — coarse 다양성 태그).
3. **anchor 보일러플레이트 식별 + Read (의무)** — 어휘 옆 "anchor 보일러플레이트" 컬럼의 파일을 `Read` 해서 chrome 골격(top eyebrow + page counter + .rule + 옵션 gm-band) + 미세 서식(카드 padding, number-circle line-height, accent 사용 빈도)을 정확히 파악. **chrome은 그대로 복사**.
4. **body 영역 작곡** — chrome은 anchor에서 가져온 그대로, body 영역만 어휘 가이드대로 변형. **Narrative 카테고리(cover/closing-light/section-divider/summary)만 anchor 거의 그대로 사용** — 톤 keepers. 다른 5 카테고리(Hero/Visual-Primary/Editorial/Density/Sequence)는 anchor에서 chrome + 미세 서식 복사한 뒤 **body는 변형 영감 컬럼에서 1개 이상 선택 적용 권장**. 표준 패턴 그대로 쓰지 말고 한 가지 의도적 변형을 더해라 — v2의 창의성은 여기서 나왔다.
5. **미세 서식 self-check** — `references/text-formatting-rules.md` §10 체크리스트 통과 (원형 텍스트 line-height = 컨테이너 height, 카드 padding 18pt 20pt, accent 1-2 events, inline span margin 없음 등).
6. **jangpm 시그니처 self-check** — `references/anti-slop.md` §11 통과 (chrome 일관, jangpm 토큰만 사용, 슬라이드별 시그니처 1개 이상 — 키워드 c-accent 인라인 / tbl-row div grid / number-circle 패턴 등).
7. **카테고리 분포 자기 점검** — 데크 전체에서 cap을 안 넘기는지 확인 (DESIGN.md §10). 양 권장 분포는 두지 않음 — 어휘 다양성·변형 자유도가 우선. Hero/Visual-Primary 0장 / Density 50%+ / 같은 카테고리 연속 3장 / 같은 어휘 연속 2장 = ❌. closing은 항상 closing-light = ✅.

**핵심 모델**: chrome + 미세 서식 = jangpm 정체성 (anchor에서 그대로 복사). body 영역 = 어휘 다양성 (시각 다양성의 원천). 둘은 분리 관리.

> **DESIGN.md가 draft인 프리셋(theme-init 산출물) 폴백**: `/theme-init`이 구운 프리셋의 `DESIGN.md`는 **draft 스텁**으로 생성된다(§5 어휘 표 비어 있음 — 사용자가 채우고 `status: confirmed`로 바꿔야 유효). 활성 프리셋의 `DESIGN.md`가 없거나 draft면 §5 어휘 표 대신 **`references/layouts.md`의 15 family**를 레이아웃 어휘로, 그 프리셋의 `pptx-boilerplate/`(37장 전체)를 참고 갤러리로 삼는다. §2.5 이미지 무드 형용사는 `DESIGN.md §1` 대신 프리셋의 `brand-spec-generated.md` / `theme.json` 토큰에서 가져온다. (Q4의 6 카테고리는 프리셋과 무관하게 유효하다.)

#### 2.3 보일러플레이트 카탈로그 (참고용)

- 모든 preset 공통 37장 (01~37): theme-init이 토큰 치환으로 전체 렌더. 01~08은 디자인 시스템 검증·최소 동작 보장용 베이스라인, 09~37은 콘텐츠 패턴. 실제 보유 목록은 `ls assets/design-systems/<preset>/pptx-boilerplate/`.
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

### 2.5 AI 이미지 생성 (선택, 슬롯이 있을 때만)

🚧 **GATE**: 2단계의 슬라이드 작곡 결과에 `<img src="../images/<slot>.png">` 슬롯이 한 개 이상 있어야 한다. 이미지 슬롯이 없는 데크는 이 단계를 건너뛰고 바로 3단계로. (슬라이드는 `slides/`, 이미지는 데크 루트 `images/` → `../images/`. `images/`만 쓰면 `slides/images/`로 잘못 풀려 빌드 실패.)

**필수 전제**: 슬라이드 빌더가 슬롯명을 **먼저** 정하고(예: `images/hero-cover.png`, `images/section-2-illustration.png`) HTML에 그 경로 그대로 쓴 뒤, 같은 슬롯명으로 파일을 생성해야 한다. 타임스탬프 파일명을 만들면 마크업 참조가 깨진다.

저장 위치: `output/<project>-pptx/images/<slot>.png` (디렉토리 없으면 `mkdir -p`).

**Preflight (2줄, 매 세션 1회):**

```bash
codex --version 2>/dev/null || { echo "NOT_FOUND — run: npm install -g @openai/codex"; exit 1; }
codex login status 2>&1 | grep -q "Logged in using ChatGPT" || { echo "NOT_LOGGED_IN — run: codex login"; exit 1; }
```

위 preflight가 실패하면 이 단계 중단 — 사용자에게 `codex login` 안내하고 이미지 슬롯이 있는 슬라이드는 `<img>` 슬롯을 placeholder 도형(예: `<div class="img-placeholder">…</div>`)으로 대체한다. 이때 **placeholder 컨테이너에는 `data-image-slot`을 남기지 않는다.** `data-image-slot`은 "실제 `images/<slot>.png`가 있어야 하는 증거 슬롯"이라는 계약이므로, placeholder에 남아 있으면 `verify_deck.py`가 하드 페일한다. Codex 사용자는 기본 내장 `imagegen`/`image_gen` 경로를 사용하며, slide-html은 별도 이미지 백엔드를 동봉하지 않는다.

**이미지 1장마다 per-slot 호출 (배치 단위 ❌). Codex 기본 이미지 생성 경로를 직접 호출:**

```bash
codex exec "Perform the following tasks:
1. Use the built-in image_gen tool to generate an image.
2. Prompt: '<style-anchor> <subject prompt> on a solid flat background. Avoid: <negative list>, transparent background, checkerboard'
3. Background rule (HARD): render on a SOLID FLAT background — never a transparency checkerboard (gray/white squares). 슬라이드 AI 이미지는 항상 프레임을 꽉 채우는 단색·실사 배경이지 투명 컷아웃이 아니다 (full-bleed/카드 fill).
4. Size: <size>
5. Quality: high
6. Count: 1
7. Copy the generated image to '<project>-pptx/images/<slot>.png'.
8. Print the saved file path and size." \
  -s workspace-write \
  --skip-git-repo-check \
  -c 'model_reasoning_effort="medium"'
```

직렬로 1장씩, 호출 사이 2–5초 간격. 다음 슬롯으로 넘어가기 전 `test -f output/<project>-pptx/images/<slot>.png && file …` 으로 산출 확인.

`codex exec`는 성공한 실행에서도 플러그인/메모리 관련 non-fatal WARN을 함께 출력할 수 있다. 성공 판정은 마지막의 saved path, byte size, dimensions 라인과 실제 `output/<project>-pptx/images/<slot>.png` 존재 여부다. saved path/bytes가 없거나 파일이 없으면 실패로 보고 placeholder fallback(위 규칙에 따라 `data-image-slot` 제거)로 전환한다.

**Size 매핑 (gpt-image-2는 1024×1024 / 1024×1536 / 1536×1024 세 가지뿐 — 진짜 16:9 없음):**

| 슬롯 타입 | `--size` | HTML 측 처리 |
|---|---|---|
| Hero / full-bleed 16:9 (960×540 캔버스 전폭) | `1536x1024` | `<img>`에 `width:960pt; height:540pt; object-fit:cover; object-position:center`로 1280×720 → 960×540 크롭 |
| 사이드 카드 1:1 | `1024x1024` | `<img>`에 `width:Xpt; height:Xpt; object-fit:cover` |
| 인물·세로 카드 3:4 | `1024x1536` | `<img>`에 `width:Wpt; height:Hpt; object-fit:cover` (W:H = 3:4) |

> 빌드 시점 메모: html2pptx는 `<img>`를 PPTX `pic` 객체로 임베드한다. `object-fit: cover`는 html2pptx가 슬라이드 단위로 캡처할 때 적용된 박스 크기 그대로 PPTX 도형 frame에 들어가므로, 16:9 슬롯의 양옆 크롭이 PPTX에서 그대로 보존된다.

**스타일 락 = 활성 accent 주입 (Fix2):** 이미지는 활성 프리셋의 **실제 accent hex**에 락한다 — 제네릭 "single accent color"는 새 테마 무드에 정밀 매칭이 안 된다. 데크에서 한 번 해석:

```bash
node ../../.codex/skills/slide/scripts/active-accent.mjs   # 또는 --deck output/<project>-pptx
```

출력된 `accent`/`bg`/`text` hex를 아래 아키타입 앵커의 `<accent>`·`<bg>`·`<text>`에 박는다. **무드 형용사는 DESIGN.md §1**(Step 0에서 이미 로드)에서 가져온다 (jangpm = editorial·analytical·monochrome·warm off-white).

**슬롯 스타일 아키타입 (bytonylee-inspired, 5종 — 프롬프트 prefix; 활성 preset에 맞춰 조정):**

| 아키타입 | 스타일 앵커 (활성 hex 주입) | Negative |
|---|---|---|
| `editorial-photo` (실제 사진 톤) | "editorial photograph, natural light, shallow depth of field, muted palette keyed to `<accent>`, no text overlay" | `illustration, cartoon, 3d render, vector, gradient, glow` (`photograph` 제외) |
| `flat-vector` (라인/플랫) | "minimal flat vector illustration, single accent color `<accent>` on `<bg>`, generous negative space, editorial poster style" | `photograph, photorealistic, gradient, neon glow` |
| `isometric-schematic` (인포그래픽) | "clean isometric technical illustration, monochrome with one accent `<accent>`, top-down or 3/4 view, no labels" | `photograph, hand-drawn sketch, watercolor, gradient` |
| `abstract-geometric` (추상 표지) | "restrained abstract geometric composition, single accent `<accent>` on `<bg>`, lots of whitespace, flat shapes" | `photograph, busy, neon, gradient, glow` |
| `textured-editorial` (리소/판화 톤) | "subtle risograph / paper-grain editorial illustration, two inks (ink `<text>` + accent `<accent>`), poster mood" | `photograph, 3d render, glossy, gradient` |

영구 락 그대로: 단일 accent(2번째 휴 금지) · 이모지 금지 · 그라디언트/글로우 금지 → 모든 negative에 `gradient, glow` 유지. **투명 배경 금지**도 함께 — gpt-image-2는 `transparent background` 요청을 회색 격자(체커보드)로 그리므로 negative에 `transparent background, checkerboard`를 유지하고 항상 단색 배경을 명시한다. (진짜 투명 PNG가 필요한 다이어그램은 §2.6의 Chromium `omitBackground` 경로이지 이 codex 경로가 아니다.)

> 아키타입 의도와 negative가 충돌하면(예: `editorial-photo`인데 negative에 `photograph`) 해당 단어를 negative에서 빼고 prefix에서 다시 강조한다.

**✅ Checkpoint — 모든 `<img src="../images/<slot>.png">` 슬롯 파일이 `images/`에 존재하면 3단계로.**

### 2.6 다이어그램 슬롯 (선택, 시각 주역이 "구조적 관계"일 때)

슬라이드의 시각 주역이 **구조적 관계**(아키텍처/플로우/순서도/시퀀스/상태도/ER/타임라인/스윔레인/사분면/트리/조직도/계층/벤/피라미드)면 — 즉 `/slide`의 **Visual-Primary 카테고리, 특히 `diagram-as-hero` 어휘** — 손으로 SVG를 짜지 말고 **`diagram-design` 스킬**로 작곡한다. (표/불릿/단일 숫자가 같은 일을 하면 다이어그램 금지 — 평소대로 슬라이드 텍스트로.)

핵심: **inline `<svg>`는 html2pptx가 버린다**(편집 도형으로 안 들어감). 그래서 다이어그램은 차트·AI이미지와 동일하게 **PNG로 렌더해 `images/<slot>.png` 슬롯**으로 임베드한다 — 단, 래스터화는 `prebuild-svg`(sharp, CJK 깨짐)가 아니라 **Playwright 렌더러**로 한다(한글·Pretendard 정확):

```bash
mkdir -p diagrams images
# 1) diagram-design 그라마로 diagrams/<slot>.html 작곡 (다이어그램만, chrome 없음, 투명 bg,
#    design-system/colors_and_type.css 링크 + SVG에서 var(--accent)/var(--text) 참조)
# 2) Playwright로 투명 고해상도 PNG 렌더 (deck 폴더 기준)
node ../../.codex/skills/slide/scripts/render-diagram.mjs diagrams/<slot>.html images/<slot>.png --scale 3
# 3) 슬라이드 HTML(slides/ 안)에서 <img src="../images/<slot>.png" style="...width/height..."> 로 배치
#    (슬라이드는 slides/, PNG는 데크루트 images/ → 반드시 ../images/. 'images/'만 쓰면 빌드 실패)
```

다이어그램은 활성 프리셋 색·폰트를 **변수로 상속**하므로 데크와 한 몸으로 보인다. 다이어그램 텍스트는 PPTX에서 편집 불가(그림)이므로 핵심 takeaway는 슬라이드 `<p>`로도 둔다.

> **전체 계약·의미역→CSS변수 매핑표·단계·주의사항은 단일 문서에:** [`references/diagram-slots.md`](references/diagram-slots.md). diagram-design 호출 시 그 문서와 해당 `type-<name>.md`를 먼저 Read.

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
- **B-게이트 (머신 체크)** — `node build.mjs`가 prebuild에서 자동 실행한다 (`scripts/check_design_gates.py`). 수동 실행:
  ```bash
  python3 .codex/skills/slide/scripts/check_design_gates.py output/<project-name>-pptx
  ```
  - simple 모드 (plan 없음): **B-r2-simple** (chart/table 의심 슬라이드에 takeaway 텍스트 동반) · **B-gm-simple** (콘텐츠 슬라이드에 `.gm-band` 존재) · **B-family-diversity-simple** (≥6장 데크는 distinct 파일명 slug ≥3)
  - plan 모드 (slide_plan.json 존재): **B-plan-count** (plan ↔ HTML 장수 1:1) · **B-plan-fidelity** (슬라이드별 core_message 키워드가 HTML에 존재)
  - 양쪽 공통: **B-density** (plan의 `min_lines_estimate` 또는 카테고리 기본 임계치 — chart/dense ≥80줄, 일반 ≥60줄, cover/section/closing ≥40줄) · **B-accent-card** (card-accent 슬라이드당 ≤1) · **B-dark-usage** (다크 카드는 closing/terminal만) · **B-chrome-consistency** (eyebrow/.rule/페이지 카운터가 콘텐츠 슬라이드 간 일관) · **B-line-length** (한글 한 줄 >60자 지목 — 규칙 자체는 50자, anti-slop §6)

  빌드는 WARN으로 통과시키지만(휴리스틱 오탐 방지), **FAIL 항목은 데크 완료 선언 전 반드시 수정**한다.
- **build-report.json 확인 (필수)** — 빌드가 데크 루트에 슬라이드별 결과를 남긴다. `overlap_autofix_total > 0`이면 해당 슬라이드의 PPTX 좌표가 겹침 회피를 위해 자동 보정된 것 — **소스 HTML과 산출물이 어긋난 상태**이므로, `slides[].warnings`에 지목된 슬라이드의 HTML 레이아웃을 고쳐 auto-fix가 0이 될 때까지 재빌드한다. auto-fix에 기댄 채 완료 선언 금지.
- **비주얼 self-review (필수)** — 빌드가 슬라이드별 렌더 스크린샷을 `output/<project-name>-pptx/_screenshots/NN-*.png`에 자동 저장한다. 각 PNG를 **Read 도구로 직접 보고** 다음을 점검:
  1. **겹침/잘림** — 텍스트가 카드 밖으로 나가거나, 블록끼리 겹치거나, 하단에서 잘리지 않는지
  2. **anti-slop §13** — 여백 ≥30%, 우상단 공백, 장식 비주얼 없음, 사진은 지배 요소
  3. **chrome 일관성** — eyebrow/page counter/rule 위치·스타일이 모든 본문 슬라이드에서 동일한지
  4. **미려함** — 카드 호흡 균일, accent 1-2 events, 시각 주역이 명확한지

  위반 슬라이드는 HTML 수정 → 재빌드 → 해당 스크린샷만 다시 확인. 텍스트 휴리스틱이 못 잡는 배치 문제는 이 단계가 마지막 방어선이다.
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
- `pptx-boilerplate/01~37-*.html` (이 프리셋으로 토큰 치환된 보일러플레이트 37장 전체 — 모든 preset 공통 의무 산출물)
- `brand-spec-generated.md` (인간 가독 토큰 레퍼런스)

`/theme-init`은 별도 스킬(`.codex/skills/theme-init/`)이며 **Claude Code 로컬 환경 전용**이다 (claude.ai에는 업로드하지 않음). theme-init은 결과물을 이 슬라이드 번들의 `assets/design-systems/<new-preset>/`에 직접 떨구고, `assets/design-systems/README.md` 카탈로그를 자동 갱신한다.

생성된 프리셋은 즉시 `init-project.sh <project> <new-preset>` 으로 사용 가능. theme-init 사용법 상세는 `.codex/skills/theme-init/SKILL.md`.

---

## 참고 문서

| 문서 | 내용 |
|---|---|
| `references/4-constraints.md` | 4 hard constraint 상세 + OOXML 근거 (PPTX 호환성) |
| `references/anti-slop.md` | **디자인 anti-slop 자기 검증 체크리스트 (시각 다양성 + jangpm 시그니처)** |
| `references/text-formatting-rules.md` | **미세 서식 polish 규칙 (원형 텍스트 valign, 카드 padding, BR 처리, accent 빈도 등)** |
| `references/error-patterns.md` | 알려진 빌드 에러 + 픽스 (E1~E12) |
| `references/css-helpers.md` | `_pptx-slide.css` 헬퍼 클래스 카탈로그 |
| `references/layouts.md` | **`data-layout` 레지스트리** — 15 family(card-type ≤1/3) + `<body data-layout>` 규칙 + 다양성 게이트(B)가 보는 것 |
| `references/diagram-slots.md` | **다이어그램 슬롯 계약** — `diagram-design` 스킬 → PNG `<img>` 슬롯 임베드 (2.6단계 전체 가이드 + 의미역→CSS변수 매핑) |
| `references/canvas-spec.md` | 960pt × 540pt 캔버스 / 좌표 / 폰트 가이드 |
| `assets/design-systems/<preset>/pptx-boilerplate/*.html` | 보일러플레이트 37 패턴 (01~37, 모든 preset 공통 — theme-init이 전체 토큰 렌더). 실제 보유 목록은 `ls assets/design-systems/<preset>/pptx-boilerplate/`로 확인 |
| `assets/design-systems/<preset>/_pptx-slide.css` | preset 별 공통 CSS (프로젝트마다 복사됨) |
| `assets/design-systems/<preset>/colors_and_type.css` | preset 토큰 (색/타이포) — 프로젝트마다 복사됨 |
| `assets/design-systems/README.md` | 사용 가능한 모든 preset 카탈로그 (theme-init이 자동 갱신) |
| `templates/build.mjs.template` | 빌드 스크립트 템플릿 (프로젝트마다 복사됨) |
| `scripts/init-project.sh` | 프로젝트 셋업 자동화 (preset → output 복사) |
| `scripts/export_deck_pptx.mjs` + `html2pptx.js` | HTML → editable PPTX 변환 엔진 (Playwright + pptxgenjs) |
| `scripts/prebuild-svg.mjs` | 빌드 직전 icons/*.svg를 PNG로 래스터화 (PptxGenJS의 SVG embed 버그 우회) |
| `scripts/validate-diversity.mjs` | 빌드 prebuild **다양성 게이트(HARD, --strict)** — `data-layout` 커버리지/distinct/card-type 비율/visual 존재. 위반 시 빌드 실패 (`references/layouts.md`) |
| `scripts/check_design_gates.py` | **B-게이트 통합 스크립트(WARN)** — B-r2/B-gm/B-family-diversity (simple) · B-plan-count/B-plan-fidelity (plan) · B-density + anti-slop 정적 체크 4종(B-accent-card/B-dark-usage/B-chrome-consistency/B-line-length) (공통). `build.mjs`가 prebuild에서 자동 실행 |
| `scripts/dev/roundtrip_check.py` | **변환 충실도 회귀 체크** — 빌드된 PPTX를 LibreOffice로 재렌더해 `_screenshots/`와 유사도 비교 (기본 임계 0.90). HTML은 멀쩡한데 PPTX만 깨지는 부류를 잡는 안전망 |
| `scripts/active-accent.mjs` | 활성 preset accent palette 해석 → §2.5 이미지 **style-lock accent 주입(Fix2)** |
| `scripts/render-diagram.mjs` | **diagram-design HTML → 투명 고해상도 PNG** (Playwright; 웹폰트·CJK 정확). 2.6 다이어그램 슬롯용 |
| `scripts/verify_deck.py` | **완료 게이트** — `build.mjs`가 빌드 후 자동 호출(dual-host 공용). 네이티브성 · 슬라이드 수 1:1 · dangling `<img>` · 미디어 하한 · placeholder가 남은 slot · ≥10장 plan · 미러 freshness 하드 페일 |
| `scripts/preflight.py` | **선택 환경 게이트** (파이프라인 시작 전) — node deps/chromium, `--images` 시 codex 로그인, 미러 freshness 점검. `build.mjs`엔 비연결, Codex `AGENTS.md` 6번/CI에서 옵션 호출 |
| `../diagram-design/SKILL.md` | **다이어그램 작곡 스킬** (14종). slide-html 안에서는 §0.5 라우팅 → `diagram-slots.md` 계약 |

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
