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

## 산출물 컨벤션

- **루트:** `output/` (단수). `outputs/` (복수)를 새로 만들지 말 것
- **폴더명:** `output/<slug>-pptx/` — 예: `output/kospi-7400-supercycle-pptx/`
- **PPTX 파일명:** `<slug>.pptx` — 예: `output/kospi-7400-supercycle-pptx/kospi-7400-supercycle.pptx`
- **슬라이드 HTML:** `output/<slug>-pptx/slides/NN-name.html` (NN은 두 자리 zero-padded)
- 새 작업 전에 `ls output/` 으로 기존 slug 컨벤션을 확인한 뒤 폴더명 결정

산출물은 항상 이 저장소의 `output/` 아래에 저장한다 — 저장소 밖 임의 위치에 만들지 말 것.

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
│       └── huashu-design/             ← 비슬라이드 시각물 담당 (프로토타입·애니메이션·MP4/GIF·디자인 컨설팅 — 슬라이드는 /slide가 정본. Codex mirror 제외, 경량 번들)
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

`.codex/skills`는 **생성물이다. 직접 편집 금지.** `.claude/skills`를 고친 뒤 반드시 미러를 재생성한다. 단, Claude-only 스킬은 mirror 생성기에서 제외된다 — `codex-image`(Codex 기본 기능 존재) + `huashu-design`(파이프라인 비참여 디자인 레퍼런스):

```bash
python3 .claude/skills/slide/scripts/dev/sync_codex_mirror.py         # 미러 재생성
python3 .claude/skills/slide/scripts/dev/sync_codex_mirror.py --check  # 드리프트 확인 (게이트)
```

완료 게이트(두 호스트 공용): `node build.mjs`가 빌드 후 `verify_deck.py`를 자동 호출한다(네이티브성·dangling `<img>`·미디어 하한·placeholder가 남은 declared image slot·≥10장 plan·미러 freshness 하드 페일). Codex는 done 선언 전 `python3 .codex/skills/slide/scripts/verify_deck.py output/<slug>-pptx` 통과 필수. 미러가 stale면 게이트가 하드 페일하므로 위 sync를 먼저 돌린다.

## 빌드 시 주의

- `init-project.sh` 가 `output/<slug>-pptx/` 에 `build.mjs`, `_pptx-slide.css`, `slides/01-title.html` 스캐폴드를 만든다. `01-title.html` 만 있으면 init 상태일 뿐 — 계획한 장수만큼 `NN-*.html` 이 채워지고 `node build.mjs` 가 성공해야 `built`로 본다 (운영 게이트).
- `node build.mjs` prebuild 체인: 다양성 게이트(`validate-diversity.mjs --strict`, **HARD** — `<body data-layout>` 누락/다양성 미달 시 빌드 실패) → 디자인 B-게이트(`check_design_gates.py`, WARN — FAIL 항목은 완료 선언 전 수정 의무) → stale-hex 가드(WARN). postbuild: `verify_deck.py` (HARD).
- 빌드가 `_screenshots/NN-*.png` 슬라이드 렌더를 자동 저장한다 — Step 5 비주얼 self-review 의무 (Read로 직접 보고 겹침/여백/chrome 점검).
- 빌드가 `build-report.json`(슬라이드별 성공/실패 + overlap auto-fix 내역)을 남긴다 — `overlap_autofix_total > 0`이면 소스 HTML을 고쳐 0으로 만든 뒤 완료 선언.
- 빌드 에러는 `references/error-patterns.md` 의 픽스 패턴부터 적용. 임의 CSS 변경으로 우회하지 말 것.
- 완료 판정: PPTX 존재 + 빌드 성공 + `unzip -t` 무결성 통과 + (Systematic 모드면) `slide_plan.json` plan-fidelity self-check 통과.
- (선택) 변환 충실도 회귀 점검: `python3 .claude/skills/slide/scripts/dev/roundtrip_check.py output/<slug>-pptx` — PPTX를 LibreOffice로 재렌더해 `_screenshots/`와 비교 (기본 임계 0.90).

## 이미지 생성

`/slide` Step 2.5(이미지 슬롯이 있을 때만)가 사용. **백엔드는 단일** — Codex 내장 `imagegen`/`image_gen` 경로(`gpt-image-2`, OAuth, API key 불필요). 다른 이미지 백엔드는 동봉하지 않는다.

preflight(`codex --version` / `codex login status`) 실패 시 대체 생성기로 넘어가지 않고 이미지 단계를 중단, `<img>` 슬롯을 placeholder 도형(`<div class="img-placeholder">`)으로 대체하며 이때 **`data-image-slot`을 반드시 제거**한다 — 남아 있으면 `verify_deck.py`가 하드 페일한다.

preflight 명령, per-slot 호출 패턴, 성공 판정(non-fatal WARN 무시 · saved path/byte 확인), size 매핑(16:9 = `1536x1024` + cover 크롭), 스타일 락 상세는 `.claude/skills/slide/SKILL.md` §2.5.

## 다이어그램

`/slide` Step 2.6(시각 주역이 "구조적 관계"인 슬라이드에만)가 사용 — 손으로 SVG를 짜지 않고 **`diagram-design` 스킬**(14종)로 작곡한다.

**왜 별도 경로인가**: `html2pptx.js`에는 inline `<svg>` 핸들러가 없어 슬라이드 HTML에 SVG를 직접 넣으면 PPTX에서 **조용히 사라진다** — 유일한 SVG 경로는 SVG → PNG 래스터 → `<img>` 슬롯(다이어그램 텍스트는 PPTX에서 편집 불가, 수정은 `diagrams/<slot>.html` 재렌더).

**래스터 백엔드**: `prebuild-svg`(sharp)가 아니라 **`scripts/render-diagram.mjs`(Playwright/Chromium)** — sharp는 웹폰트·CJK가 깨진다.

**영구 락 준수**: 단일 액센트(focal ≤2) · 이모지 금지 · 그라디언트/글로우 금지는 다이어그램에도 그대로. 워크플로우는 `.claude/skills/slide/SKILL.md` §2.6, 전체 계약·프리셋 CSS변수 스킨·온보딩 게이트 스킵 규칙은 `references/diagram-slots.md` 단일 문서, diagram-design 라우팅은 `.claude/skills/diagram-design/SKILL.md` §0.5.

## 참고

- **풀 사용자 가이드:** `README.md` (디자인 시스템 상세, FAQ, 사용 예제 포함)
