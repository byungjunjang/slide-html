# slide-html

## Source of Truth

**This file is the project SSOT.** Before any slide task, read `.claude/skills/slide/SKILL.md` for the full workflow and execution rules. If another skill's conventions conflict with this document, this document wins.

## 개요

**per-slide HTML × html2pptx 기반의 editable PPTX 생성기.** 슬라이드 한 장당 독립 HTML 파일(960pt × 540pt = LAYOUT_WIDE) → Playwright로 DOM의 computedStyle을 캡처 → `pptxgenjs`로 PPTX 객체 1:1 번역 → `output/<slug>-pptx/<slug>.pptx`. PowerPoint/Keynote에서 텍스트를 더블클릭으로 편집할 수 있는 진짜 .pptx (이미지 플래튼된 가짜 PPTX 아님).

활성 테마는 `assets/design-systems/<preset>/` 가 결정하며 `init-project.sh <project> <preset>` 으로 선택, `/theme-init`로 새 프리셋 추가. 기본 프리셋은 **jangpm** (모노크롬 + 단일 `#4633E3` 인디고 액센트, Pretendard 9 weights).

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
│       │   │   ├── error-patterns.md      ← 빌드 에러 → 픽스 패턴
│       │   │   └── text-formatting-rules.md
│       │   ├── scripts/
│       │   │   ├── init-project.sh        ← 프로젝트 셋업
│       │   │   ├── export_deck_pptx.mjs   ← HTML → PPTX 빌드 엔트리
│       │   │   ├── html2pptx.js           ← computedStyle → pptxgenjs 변환
│       │   │   └── prebuild-svg.mjs       ← inline SVG 전처리
│       │   ├── templates/                 ← build.mjs / _pptx-slide.css 템플릿
│       │   └── assets/design-systems/     ← 프리셋 (jangpm 기본 + theme-init 산출물)
│       ├── slide-plan/                ← 기획 단계 (Systematic 모드용 slide_plan.json 생성)
│       ├── theme-init/                ← 새 프리셋 추가 (Claude Code 로컬 전용)
│       ├── upload-drive/              ← Google Drive 업로드 + Slides 변환 (로컬 전용)
│       ├── codex-image/               ← OAuth 경유 이미지 생성 (gpt-image-2)
│       └── huashu-design/             ← 디자인 레퍼런스 (보조)
├── node_modules/
└── output/                            ← 사용자 워크스페이스 (각 데크 = <slug>-pptx/)
```

## 자주 쓰는 명령

```bash
# 1. 프로젝트 셋업 (jangpm 기본; 다른 프리셋은 두 번째 인자로)
bash .claude/skills/slide/scripts/init-project.sh <slug>
bash .claude/skills/slide/scripts/init-project.sh <slug> <preset>

# 2. 슬라이드 작성 → output/<slug>-pptx/slides/NN-*.html
#    (4-constraints + css-helpers를 준수하며 LLM이 직접 작성)

# 3. 빌드 (PPTX 생성)
cd output/<slug>-pptx && node build.mjs

# 4. 무결성 검증 (필수 — 완료 판정 게이트)
unzip -t output/<slug>-pptx/<slug>.pptx

# 5. (선택) Google Drive 업로드 + Slides 변환
/upload-drive
```

## 빌드 시 주의

- `init-project.sh` 가 `output/<slug>-pptx/` 에 `build.mjs`, `_pptx-slide.css`, `slides/01-title.html` 스캐폴드를 만든다. `01-title.html` 만 있으면 init 상태일 뿐 — 계획한 장수만큼 `NN-*.html` 이 채워지고 `node build.mjs` 가 성공해야 `built`로 본다 (WorkOS 운영 게이트).
- 빌드 에러는 `references/error-patterns.md` 의 픽스 패턴부터 적용. 임의 CSS 변경으로 우회하지 말 것.
- 완료 판정: PPTX 존재 + 빌드 성공 + `unzip -t` 무결성 통과 + (Systematic 모드면) `slide_plan.json` plan-fidelity self-check 통과.

## 이미지 생성

`/slide` Step 2.5(이미지 슬롯이 있을 때만)가 사용. 기본 경로는 `codex-image` 스킬 (Codex CLI OAuth → `gpt-image-2`, API key 불필요). 16:9 슬롯은 `1536x1024` 생성 후 `<img object-fit:cover object-position:center>` 로 960×540 크롭 — html2pptx가 박스 크기 그대로 PPTX `pic` frame에 임베드하므로 양옆 크롭이 보존된다.

## 참고

- **풀 사용자 가이드:** `README.md` (디자인 시스템 상세, FAQ, 사용 예제 포함)
- **워크플로우 상세:** `.claude/skills/slide/SKILL.md` (5단계 + Systematic/Simple 분기 + 검증)
- **WorkOS 루트 규칙:** `../CLAUDE.md` §3 (슬라이드 3종 병렬 실행 + 운영 게이트 + fallback)
