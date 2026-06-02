# slide-html

## Source of Truth

**This file is the project SSOT.** Before any slide task, read `.claude/skills/slide/SKILL.md` for the full workflow and execution rules. If another skill's conventions conflict with this document, this document wins.

## 개요

**per-slide HTML × html2pptx 기반의 editable PPTX 생성기.** 슬라이드 한 장당 독립 HTML 파일(960pt × 540pt = LAYOUT_WIDE) → Playwright로 DOM의 computedStyle을 캡처 → `pptxgenjs`로 PPTX 객체 1:1 번역 → `output/<slug>-pptx/<slug>.pptx`. PowerPoint/Keynote에서 텍스트를 더블클릭으로 편집할 수 있는 진짜 .pptx (이미지 플래튼된 가짜 PPTX 아님).

활성 테마는 `assets/design-systems/active.json`(SSOT)이 가리키는 프리셋이 결정한다 — `/slide` Step 0가 이를 읽어 선언하고, `init-project.sh`를 프리셋 인자 없이 호출하면 이 프리셋이 자동 선택된다. `init-project.sh <project> <preset>`로 명시 지정하면 그게 최우선. `/theme-init`은 새 프리셋을 구울 때 자동으로 active로 표기한다(`--no-set-active`로 끌 수 있음). active.json이 없으면 카탈로그 시드 기본값 **jangpm** (모노크롬 + 단일 `#4633E3` 인디고 액센트, Pretendard 9 weights)으로 폴백.

## 핵심 제약 (non-negotiable)

다음 제약은 **프리셋에 관계없이 영구 락**이다. 디자인 시스템을 바꿔도 이 규칙들은 그대로.

- **960pt × 540pt 전용** — `<body>` 사이즈 고정, LAYOUT_WIDE. 다른 캔버스 포맷 지원 안 함
- **per-slide HTML 1:1** — 한 슬라이드 = 한 HTML 파일 (`slides/NN-name.html`). 한 파일에 여러 슬라이드 금지
- **4 hard constraint** — `references/4-constraints.md`. 모든 슬라이드가 통과해야 빌드 인정
- **단일 액센트 원칙** — 활성 프리셋의 accent 하나만 사용, 멀티 휴 / 그라디언트 / 글로우 금지 (jangpm 기본: `#4633E3`)
- **이모지 금지** — 아이콘은 활성 프리셋의 라인아이콘 또는 SVG만
- **html2pptx-safe CSS만** — `_pptx-slide.css` 헬퍼 클래스 위에서만 작성. 임의 CSS는 PPTX 번역 실패 위험. 상세는 `references/css-helpers.md`
- **editable text 유지** — `<text>`/`<p>`/`<span>`은 PPTX `text` 객체로 임베드되어야 함, `<img>` 플래튼 금지

## 스킬

| 스킬 | 트리거 | 위치 |
|------|--------|------|
| `/slide` | `"슬라이드 만들어"`, `"PPT"`, `"프레젠테이션"`, `"pptx"`, `"발표 자료"`, `"강의 슬라이드"` | 핵심 파이프라인 |
| `/slide-plan` | `"체계적으로 기획"`, `"데크 구조부터"`, `"/slide-plan"` | 선택적 강화 단계 — `/slide` 이전에 실행 |
| `/theme-init` | `"테마 추가"`, `"새 디자인 시스템"`, `"새 프리셋"` | 새 프리셋 추가 (1회성) |
| `/upload-drive` | `"드라이브 올려"`, `"슬라이드로 변환"` | Google Drive 업로드 + Slides 변환 |
| `diagram-design` | `"다이어그램"`, `"구성도/아키텍처"`, `"플로우/순서도"`, `"시퀀스/상태도"`, `"조직도/계층도"`, `"ER/벤/피라미드"` (슬라이드 시각 주역이 "구조적 관계") | 다이어그램 작곡 → `/slide` Step 2.6에서 PNG `<img>` 슬롯으로 임베드 |

`/slide`는 `output/<slug>-pptx/slide_plan.json` 존재 여부로 Systematic/Simple 자동 분기. 자세한 워크플로우는 `.claude/skills/slide/SKILL.md`.

**Auto-trigger → Systematic 모드:** 슬라이드 수 ≥ 10장, 사용자가 참고 파일 첨부, brief에 `계획/체계/꼼꼼/제대로/thorough/detailed` 등 태도 키워드 포함 — 하나라도 충족하면 `/slide-plan` 먼저 호출.

## 산출물 컨벤션 (WorkOS 루트 규칙)

- **루트:** `output/` (단수). `outputs/` (복수)를 새로 만들지 말 것
- **폴더명:** `output/<slug>-pptx/` — 예: `output/kospi-7400-supercycle-pptx/`
- **PPTX 파일명:** `<slug>.pptx` — 예: `output/kospi-7400-supercycle-pptx/kospi-7400-supercycle.pptx`
- **슬라이드 HTML:** `output/<slug>-pptx/slides/NN-name.html` (NN은 두 자리 zero-padded)
- 새 작업 전에 `ls output/` 으로 기존 slug 컨벤션을 확인한 뒤 폴더명 결정

WorkOS 루트 CLAUDE.md의 `cokacdir-outputs` 규칙은 슬라이드 3종에 적용되지 않는다 — 자기 프로젝트 `output/` 안에 저장한 뒤 cokacdir 전송.

## 디렉터리

```
slide-html/
├── CLAUDE.md                          ← 이 파일 (SSOT)
├── README.md                          ← 사용자용 풀 가이드 (35KB+)
├── LICENSE
├── package.json                       ← playwright + pptxgenjs + sharp
├── .claude/
│   ├── settings.local.json            ← 스크립트 실행 allow-list
│   └── skills/
│       ├── slide/
│       │   ├── SKILL.md               ← 스킬 엔트리 (5단계 워크플로우)
│       │   ├── package.json
│       │   ├── references/            ← 핵심 제약 + 디자인 어휘
│       │   │   ├── 4-constraints.md       ← 4 hard constraint
│       │   │   ├── anti-slop.md           ← 금지 패턴
│       │   │   ├── canvas-spec.md         ← 960pt × 540pt 좌표/폰트
│       │   │   ├── css-helpers.md         ← _pptx-slide.css 헬퍼 클래스
│       │   │   ├── diagram-slots.md       ← 다이어그램 슬롯 계약 (diagram-design → PNG <img>)
│       │   │   ├── error-patterns.md      ← 빌드 에러 → 픽스 패턴
│       │   │   └── text-formatting-rules.md
│       │   ├── scripts/
│       │   │   ├── init-project.sh        ← 프로젝트 셋업
│       │   │   ├── export_deck_pptx.mjs   ← HTML → PPTX 빌드 엔트리
│       │   │   ├── html2pptx.js           ← computedStyle → pptxgenjs 변환
│       │   │   ├── prebuild-svg.mjs       ← icons/*.svg → PNG 래스터 (sharp)
│       │   │   └── render-diagram.mjs     ← diagram-design HTML → 투명 PNG (Playwright, 2.6단계)
│       │   ├── templates/                 ← build.mjs / _pptx-slide.css 템플릿
│       │   └── assets/design-systems/     ← 프리셋 (jangpm 기본 + theme-init 산출물)
│       ├── diagram-design/            ← 다이어그램 작곡 스킬 (14종, /slide Step 2.6 경유 임베드)
│       ├── slide-plan/                ← 기획 단계 (Systematic 모드용 slide_plan.json 생성)
│       ├── theme-init/                ← 새 프리셋 추가 (Claude Code 로컬 전용)
│       ├── upload-drive/              ← Google Drive 업로드 + Slides 변환 (로컬 전용)
│       ├── codex-image/               ← Claude Code 전용 선택 헬퍼 (Codex mirror 제외)
│       └── huashu-design/             ← 디자인 레퍼런스 (보조)
├── node_modules/
└── output/                            ← 사용자 워크스페이스 (각 데크 = <slug>-pptx/)
```

## 자주 쓰는 명령

```bash
# 1. 프로젝트 셋업 (jangpm 기본; 다른 프리셋은 두 번째 인자로)
bash .claude/skills/slide/scripts/init-project.sh <slug>
bash .claude/skills/slide/scripts/init-project.sh <slug> <preset>

# Windows PowerShell without Git Bash
powershell -ExecutionPolicy Bypass -File .claude/skills/slide/scripts/init-project.ps1 <slug>
powershell -ExecutionPolicy Bypass -File .claude/skills/slide/scripts/init-project.ps1 <slug> <preset>

# 2. 슬라이드 작성 → output/<slug>-pptx/slides/NN-*.html
#    (4-constraints + css-helpers를 준수하며 LLM이 직접 작성)

# 3. 빌드 (PPTX 생성)
cd output/<slug>-pptx && node build.mjs

# 4. 무결성 검증 (필수 — 완료 판정 게이트)
unzip -t output/<slug>-pptx/<slug>.pptx

# 5. (선택) Google Drive 업로드 + Slides 변환
/upload-drive
```

## Codex dual-host (정본 + 생성형 미러)

이 repo는 Claude Code와 Codex(클라우드/웹) 양쪽에서 동작한다. 진입점:

- **Claude Code:** `.claude/skills/` (정본) — Skill 런타임이 `SKILL.md`를 절차로 실행.
- **Codex:** 루트 `AGENTS.md` → `.codex/skills/`(생성형 미러)를 절차로 실행.

`.codex/skills`는 **생성물이다. 직접 편집 금지.** `.claude/skills`를 고친 뒤 반드시 미러를 재생성한다. 단, `codex-image`처럼 Codex에 기본 기능이 있는 Claude-only 헬퍼는 mirror 생성기에서 제외된다:

```bash
python3 .claude/skills/slide/scripts/dev/sync_codex_mirror.py         # 미러 재생성
python3 .claude/skills/slide/scripts/dev/sync_codex_mirror.py --check  # 드리프트 확인 (게이트)
```

완료 게이트(두 호스트 공용): `node build.mjs`가 빌드 후 `verify_deck.py`를 자동 호출한다(네이티브성·dangling `<img>`·미디어 하한·placeholder가 남은 declared image slot·≥10장 plan·미러 freshness 하드 페일). Codex는 done 선언 전 `python3 .codex/skills/slide/scripts/verify_deck.py output/<slug>-pptx` 통과 필수. 미러가 stale면 게이트가 하드 페일하므로 위 sync를 먼저 돌린다.

## 빌드 시 주의

- `init-project.sh` 가 `output/<slug>-pptx/` 에 `build.mjs`, `_pptx-slide.css`, `slides/01-title.html` 스캐폴드를 만든다. `01-title.html` 만 있으면 init 상태일 뿐 — 계획한 장수만큼 `NN-*.html` 이 채워지고 `node build.mjs` 가 성공해야 `built`로 본다 (WorkOS 운영 게이트).
- 빌드 에러는 `references/error-patterns.md` 의 픽스 패턴부터 적용. 임의 CSS 변경으로 우회하지 말 것.
- 완료 판정: PPTX 존재 + 빌드 성공 + `unzip -t` 무결성 통과 + (Systematic 모드면) `slide_plan.json` plan-fidelity self-check 통과.

## 이미지 생성

`/slide` Step 2.5(이미지 슬롯이 있을 때만)가 사용.

**백엔드는 단일**: Codex 기본 `imagegen`/`image_gen` 경로 → `gpt-image-2` (OAuth, API key 불필요). slide-html은 이 외 다른 이미지 백엔드를 동봉하지 않는다 — preflight(`codex --version` / `codex login status`)가 실패하면 대체 생성기로 넘어가지 않고 이미지 단계를 중단한 뒤 `<img>` 슬롯을 placeholder 도형(`<div class="img-placeholder">`)으로 대체한다. 이 fallback은 **`data-image-slot`을 제거해야** 한다. `data-image-slot`이 남아 있으면 verify가 "실제 미디어가 있어야 하는 슬롯"으로 보고 하드 페일한다.

`codex exec`는 성공해도 플러그인/메모리 관련 non-fatal WARN을 함께 찍을 수 있다. 성공 판정은 마지막의 saved path, byte size, dimensions 라인과 실제 `output/<deck>-pptx/images/<slot>.png` 존재 여부로 한다.

**호출 경로**: `/slide` Step 2.5는 Codex 기본 이미지 생성 경로를 직접 사용한다. Codex 사용자용 `.codex/skills` 패키지에는 `codex-image` 스킬을 포함하지 않는다. Claude Code 사용자는 `.claude/skills/codex-image/`를 독립 편의 헬퍼로 쓸 수 있지만, slide 파이프라인의 필수 계약은 아니다.

16:9 슬롯은 `1536x1024` 생성 후 `<img object-fit:cover object-position:center>` 로 960×540 크롭 — html2pptx가 박스 크기 그대로 PPTX `pic` frame에 임베드하므로 양옆 크롭이 보존된다.

## 다이어그램

`/slide` Step 2.6(시각 주역이 "구조적 관계"인 슬라이드에만)가 사용. 손으로 SVG를 짜지 않고 **`diagram-design` 스킬**(14종: 아키텍처/플로우/시퀀스/상태도/ER/타임라인/스윔레인/사분면/nested/트리/조직도/계층/벤/피라미드)로 작곡한다.

**왜 별도 경로인가**: `html2pptx.js`에는 inline `<svg>` 핸들러가 없다 — 슬라이드 HTML에 SVG를 직접 넣으면 PPTX에서 **조용히 사라진다**. 이 프로젝트의 유일한 SVG 경로는 **SVG → PNG 래스터 → `<img>` 슬롯**(차트·아이콘도 동일). 따라서 다이어그램은 차트·AI이미지와 같은 **그림(raster figure)** 으로 임베드되며, 도형 텍스트는 PPTX에서 더블클릭 편집 불가다(슬라이드의 나머지 텍스트는 편집 가능). 텍스트 수정은 `diagrams/<slot>.html`을 고쳐 재렌더.

**래스터 백엔드**: `prebuild-svg`(sharp)가 아니라 **`scripts/render-diagram.mjs`(Playwright/Chromium)** — sharp는 웹폰트·CJK를 못 불러와 한글이 깨지지만 Chromium은 Pretendard·한글을 정확히 렌더한다.

**스킨**: 다이어그램은 색·폰트를 하드코딩하지 않고 데크의 `design-system/colors_and_type.css`를 `<link>` 해 **프리셋 CSS 변수**(`var(--accent)` 등)를 참조 → 활성 프리셋과 자동으로 한 몸. diagram-design 자체의 first-run 온보딩/style-guide 게이트는 slide-html 안에서 **건너뛴다**(활성 프리셋이 SSOT).

**영구 락 준수**: 단일 액센트(focal ≤2) · 이모지 금지 · 그라디언트/글로우 금지는 다이어그램에도 그대로. 전체 계약·단계·의미역→CSS변수 매핑은 `.claude/skills/slide/references/diagram-slots.md` 단일 문서, diagram-design 라우팅은 `.claude/skills/diagram-design/SKILL.md` §0.5.

## 참고

- **풀 사용자 가이드:** `README.md` (디자인 시스템 상세, FAQ, 사용 예제 포함)
- **워크플로우 상세:** `.claude/skills/slide/SKILL.md` (5단계 + Systematic/Simple 분기 + 검증)
- **WorkOS 루트 규칙:** `../CLAUDE.md` §3 (슬라이드 3종 병렬 실행 + 운영 게이트 + fallback)
