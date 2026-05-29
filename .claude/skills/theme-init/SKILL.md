---
name: theme-init
description: >
  Generate a new design system preset for the /slide PPTX pipeline.
  Reads a design guide (markdown) or a complete preset folder, extracts
  tokens conforming to the v1 contract, and renders a full preset under
  the slide skill bundle's assets/design-systems/<preset>/ — colors,
  typography, brand-spec.md, _pptx-slide.css helpers, and 8 reskinned
  boilerplate slides. Also refreshes the slide bundle's preset catalog
  (assets/design-systems/README.md) so /slide picks up the new preset
  immediately. Claude Code 로컬 전용 (claude.ai 업로드 안 함).
  Trigger on: "/theme-init", "디자인 시스템 추가", "새 브랜드 프리셋",
  "set up a new theme".
---

# /theme-init — 디자인 시스템 프리셋 생성기

**Claude Code 로컬 전용.** 새 디자인 가이드(MD 또는 완결된 프리셋 폴더)를 받아서, `/slide` 스킬 번들이 즉시 사용할 수 있는 **완전한 프리셋 폴더**를 생성한다. 결과물은 슬라이드 번들의 `.claude/skills/slide/assets/design-systems/<preset>/`에 새 폴더로 추가되고, 같은 디렉토리의 `README.md` 카탈로그도 자동으로 갱신된다 — 기존 프리셋(jangpm 등)은 보존.

이 스킬은 claude.ai에 업로드하지 않는다. 디자인 시스템은 로컬에서 굽고, 그 결과가 박힌 slide 번들만 claude.ai에 올리는 흐름.

## 모델: 프리셋 추가 (액티브 테마 락 아님)

- 한 프로젝트가 acme-warm 으로 빌드 중이어도 jangpm 으로 빌드 중인 다른 프로젝트는 영향 없음
- /theme-init 은 새 폴더를 만들 뿐이지 기존 폴더를 갈아엎지 않음 (`--force` 명시했을 때만 덮어쓰기)
- 한 사용자가 N개 프리셋을 동시에 보유 가능

## 트리거

`/theme-init`, "디자인 시스템 추가", "새 브랜드 프리셋", "set up a new theme"

## 워크플로우

### 1. 디자인 가이드 읽기

사용자가 다음 중 하나를 제공:
- (a) 디자인 가이드 마크다운 (예: `.claude/skills/theme-init/examples/acme-warm.md`)
- (b) huashu-design 이 만든 완결된 프리셋 폴더 (`brand-spec.md` + `colors_and_type.css` + `fonts/` 등)

에이전트(LLM)가 가이드 전체를 읽고 다음 토큰을 추출한다:

| 그룹 | 토큰 |
|---|---|
| Identity | `name`, `display_name`, `description` |
| Colors (17) | `bg`, `surface`, `surface-alt`, `text`, `text-secondary`, `text-tertiary`, `border`, `border-strong`, `accent`, `accent-soft`, `accent-ink`, `positive`, `positive-soft`, `negative`, `negative-soft`, `warning`, `warning-soft` |
| Surface | `card_style` (filled / hairline / borderless) — 카드·타일 chrome 처리 (기본 hairline) |
| Typography | `font-chain`, `font-mono`, 7-step type scale (display, display-sm, headline, title, body, caption, label) — 각각 size/weight/line-height/letter-spacing/transform |
| Radius (6) | xs, sm, md, lg, xl, pill |
| Stroke (3) | icon, divider, emphasis |
| Spacing (11) | 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16 (8px grid) |
| Assets | `icon-pack-default`, `icon-pack-fallback`, `character` (optional) |
| Voice | `tone`, `pov`, `register`, `forbidden_phrases`, `gm_style_hint` |

가이드에 명시되지 않은 토큰은 **null로 두거나 생략** — `fill_theme_defaults.py` 가 단조로운 안전 기본값으로 채운다. **추측해서 채우지 말 것** (잘못된 브랜드 색보다 회색 기본값이 낫다).

추출 결과는 `/tmp/<preset>-draft.json` 같은 임시 파일에 작성.

### 2. /theme-init 실행

```bash
python3 .claude/skills/theme-init/scripts/init_theme.py \
  --from /tmp/<preset>-draft.json \
  --preset <kebab-name>
```

옵션:
- `--force` — 이미 존재하는 프리셋 폴더 덮어쓰기 (조심히 사용)
- `--fonts-prelude <path>` — `@font-face` 블록을 포함한 CSS 파일을 colors_and_type.css 앞에 prepend (사용자 폰트가 있을 때)
- `--presets-root <path>` — 출력 위치 변경 (기본: `.claude/skills/slide/assets/design-systems/`, 즉 slide 번들)

오케스트레이터의 단계:
1. **fill_theme_defaults** — 부분 드래프트 → 모든 토큰 채워진 theme.json
2. **patch name** — `--preset` 인자로 name/display_name 덮어쓰기
3. **validate_theme** — v1 토큰 컨트랙트 schema 검증
4. **resolve prelude** — `--fonts-prelude` → 기존 `_fonts.css` → 자동 생성 `_header.css` (캐스케이드)
5. **render** — colors_and_type.css, _pptx-slide.css, brand-spec-generated.md, pptx-boilerplate/01..08.html
6. **render_design_md** — `<preset>/DESIGN.md` 초안 생성 (slide-plan Layer 3). frontmatter `status: draft` — 사용자 검토 후 `confirmed`로 변경.
7. **render_presets_readme** — slide 번들의 `assets/design-systems/README.md` 카탈로그를 새 프리셋 행으로 갱신 (자동 생성, 직접 편집 금지)
8. **report** — 다음 단계 안내

#### 사용자 검토 체크포인트 — DESIGN.md (Step 6 산출물)

`render_design_md`가 생성하는 DESIGN.md는 **draft** 상태로 시작한다. 새 preset을 `/slide` 또는 `/slide-plan`에서 사용하기 전:

1. `assets/design-systems/<preset>/DESIGN.md` 열기
2. 빈 섹션을 손으로 채움 — 특히 §5 layout_families(boilerplate를 family 어휘로 묶기)와 §8 chart/table treatment(9 chart_strategy를 이 preset 시각 구현으로 매핑).
3. frontmatter `status: draft` → `status: confirmed`로 변경

이 단계가 누락되면 slide-plan이 layout_family 어휘를 신뢰하지 못해 fallback 동작하고, simple `/slide` 경로의 LLM도 layout 일관성을 잃는다.

### 3. 검증

```bash
# 새 프리셋으로 테스트 프로젝트 셋업
bash .claude/skills/slide/scripts/init-project.sh test-<preset> <preset>

# 빌드
cd output/test-<preset>-pptx/
node build.mjs

# 결과 PPTX를 PowerPoint/Keynote 로 열어 색·폰트 확인
open test-<preset>.pptx
```

확인 포인트:
- 악센트 색이 새 브랜드 색인지 (jangpm 인디고가 아니어야 함)
- 폰트가 가이드의 primary 폰트인지
- 보일러플레이트 8장 패턴이 새 프리셋 컬러로 reskin 됐는지

## Phase 2 — Layout Authoring (브랜드 레이아웃 재작곡)

> **위 워크플로우(Phase 1)는 token-render = 색·폰트만 바뀐 jangpm 골격이다.** Phase 2는 그 뒤에 붙는 **독립·멱등 단계**로, 에이전트(LLM)가 그 프리셋의 `DESIGN.md §5/§6` + 원본 `design.md`를 읽고 **아이덴티티 슬라이드를 브랜드 구성으로 재작곡**해 `pptx-boilerplate/*.html`을 제자리 덮어쓴다. Phase 1(token-render) 코드는 건드리지 않는다.

### 위상 / 멱등성

Phase 1이 끝나면 `init_theme.py`가 자동으로 token-render 결과를 `pptx-boilerplate/.stock/`에 스냅샷하고 `pptx-boilerplate/_authoring.json`(status: `not_authored`) 매니페스트를 만든다. Phase 2는 **항상 `.stock/` 베이스라인에서 출발**하므로 재실행해도 누적되지 않는다 (멱등). `init_theme.py --force` 재실행 시 `.stock/`이 갱신된다.

### 작곡 대상 분류 (락 — 데이터 슬라이드 톤 보존)

| 부류 | 패밀리 (기본) | Phase 2 동작 |
|---|---|---|
| **Identity (재작곡)** | cover(`01·23·25`), section(`09·07`), closing(`21`+허용 시 `22·08`), feature-board(`02·26·12`), hero-impact(`16·18`), summary(`17`), agenda(`10`) | 스톡 골격 버리고 **브랜드 구성으로 새로 그림** |
| **Data (톤 유지)** | table·kpi·matrix·ref·terminal·exercise·image 등 나머지 22장 | **token-render 그대로 — 건드리지 않음** |

분류는 `_authoring_common.py`의 `IDENTITY_FAMILIES`가 SSOT. 매니페스트 `identity_set`/`data_set`에 박제.

### 입력

- 프리셋 `DESIGN.md` §5 visual vocabulary / §6 chrome (`status: confirmed` 권장)
- 원본 `design.md` (브랜드 가이드 원문)
- `pptx-boilerplate/.stock/` (token-render baseline)
- 프리셋 `_pptx-slide.css` 헬퍼 + `colors_and_type.css` 토큰
- (선택) 사용자 스타일 지시 (`--direction "..."`)
- (선택·강력권장) **레퍼런스 블루프린트** — 직전에 손으로 만든 그 브랜드 데크 (`--reference <path>`)

### 보존 락 (작곡물도 통과 의무)

960pt×540pt · per-slide 1:1 · 4 hard constraint · **html2pptx-safe(헬퍼 클래스 + 리터럴 hex만, 그라디언트 금지)** · editable text · 이모지 금지. → **scratch 프로젝트에서 `node build.mjs` 성공 + `unzip -t` 무결성 통과**해야 confirm. 레시피·좌표·헬퍼 카탈로그는 `references/layout-recipes.md`.

### 작곡 + 리뷰 루프 (먼저 보여주고 → 피드백 → 수정)

```bash
# 1. prep — identity 슬라이드를 .stock 베이스라인으로 리셋 + 매니페스트 + source 기록
#    DESIGN.md status가 confirmed가 아니면 경고(§5/§6는 Phase 2 입력). --require-confirmed로 강제.
python3 .claude/skills/theme-init/scripts/author_layouts.py prep \
  --preset <name> --design-md <preset>/DESIGN.md \
  --original-design-md <원본> [--reference <손으로_만든_데크>] [--direction "..."] [--require-confirmed]

# 2. (에이전트) DESIGN.md §5/§6 + design.md에서 시그니처 레이아웃 추출 → blueprint 기록
#    → layout-recipes.md 레시피로 identity 슬라이드 HTML을 브랜드 구성으로 1차 작곡 (Write)

# 3. validate — lint + node build.mjs + unzip -t (깨진 안은 사용자에게 안 보여줌)
python3 .claude/skills/theme-init/scripts/author_layouts.py validate --preset <name>

# 4. thumbs — scratch 렌더로 before(.stock)/after(authored) PNG 생성
python3 .claude/skills/theme-init/scripts/author_layouts.py thumbs --preset <name>
#    ▶ before/after 썸네일을 사용자에게 "우선 구성한 수정본" 레퍼런스로 제시 (검토 체크포인트, 의무 1회)

# 5. 사용자 피드백 수집 → 반영해 재작곡 → 3~4 반복 (사용자 OK까지)

# 6. confirm — validate 통과 + authored ≥ 1 전제로 status: confirmed + DESIGN.md provenance 기록
#    (아무것도 작곡 안 했으면 거부. token-tone 그대로 confirm하려면 --allow-empty)
#    DESIGN.md §5/§6에 템플릿 placeholder가 남아 있으면 기본 차단(strict 기본값) — 검토 없이
#    넘기려면 --no-strict.
python3 .claude/skills/theme-init/scripts/author_layouts.py confirm --preset <name>

# (필요 시) restore — 작곡 취소, identity 슬라이드를 .stock으로 되돌림
python3 .claude/skills/theme-init/scripts/author_layouts.py restore --preset <name>
```

**핵심 원칙**: 4번 썸네일 before/after 제시가 "먼저 보여주는 레퍼런스"고 5번이 피드백 루프다. validate(3)가 실패하면 썸네일로 못 가므로 깨진 안은 사용자에게 보여주지 않는다. data 슬라이드는 `git diff pptx-boilerplate/`에 identity stem만 잡혀야 한다.

## 산출물 구조

```
.claude/skills/slide/assets/design-systems/<preset>/    # ← slide 번들 안
├── theme.json                    # source of truth (v1 contract)
├── colors_and_type.css            # CSS 변수 (--bg, --accent, --fs-display, ...)
├── _pptx-slide.css                # html2pptx-safe 헬퍼 클래스 (.card-accent, .bg-accent, ...)
├── brand-spec-generated.md        # 인간 가독 토큰 레퍼런스
├── DESIGN.md                      # slide-plan Layer 3 — draft 상태로 생성, 사용자 검토 필요
├── _header.css 또는 _fonts.css   # 코멘트 헤더 (+ 옵션 @font-face)
└── pptx-boilerplate/              # 37장 boilerplate (Phase 1 token-render)
    ├── 01-title.html  …  37-image-2up.html
    ├── .stock/                     # token-render baseline 스냅샷 (Phase 2 복원·diff용)
    ├── _authoring.json             # Phase 2 매니페스트 (분류·blueprint·status·verification)
    └── _thumbs/                    # Phase 2 리뷰 썸네일 (NN.stock.png / NN.authored.png)
```

Phase 2(Layout Authoring)를 거치면 identity 슬라이드(`01·23·25·09·07·21·02·26·12·16·18·17·10` 등)는 브랜드 구성으로 재작곡되어 덮어써지고, data 슬라이드는 token-render 그대로 유지된다.

추가로 `.claude/skills/slide/assets/design-systems/README.md` 카탈로그가 갱신된다 (모든 프리셋의 인덱스 표).

## /slide 와의 통합

theme-init은 결과물을 slide 번들의 `assets/design-systems/` 안에 직접 떨군다. 추가 동기화·이동 작업 없음. 새 프리셋 생성 직후 `/slide` (또는 `init-project.sh <project> <preset>`)를 호출하면 자동으로 새 프리셋 자산을 사용:
- `_pptx-slide.css`가 프리셋 폴더에서 복사됨 (jangpm 기본 코드와 다른 색)
- 첫 슬라이드 (`01-title.html`)도 프리셋 boilerplate에서 복사됨
- 사용자가 새 슬라이드 추가할 때 참고할 패턴은 `assets/design-systems/<preset>/pptx-boilerplate/02-08*.html`
- `assets/design-systems/README.md`에 새 프리셋이 자동으로 한 행 추가되어 카탈로그 최신 유지

## 참고 자산

| 파일 | 용도 |
|---|---|
| `references/token-contract.json` | v1 schema (35+ 토큰 정의) |
| `examples/acme-warm.md` | 샘플 디자인 가이드 (e2e 검증용) |
| `templates/colors_and_type.tpl.css` | colors_and_type.css 템플릿 |
| `templates/_pptx-slide.tpl.css` | _pptx-slide.css 템플릿 |
| `templates/brand-spec.tpl.md` | brand-spec-generated.md 템플릿 |
| `templates/boilerplate/*.tpl.html` | 8장 보일러플레이트 템플릿 |
| `scripts/init_theme.py` | Phase 1 오케스트레이터 (token-render + .stock 스냅샷 + 매니페스트 stub) |
| `scripts/_token_render.py` | 공통 placeholder 치환 엔진 (TOKEN, IF, rgb/rem/csv/optional 필터) |
| `scripts/render_presets_readme.py` | slide 번들의 `assets/design-systems/README.md` 카탈로그 자동 생성 |
| `scripts/author_layouts.py` | **Phase 2 하네스** — prep/classify/thumbs/validate/confirm/restore/status |
| `scripts/_authoring_common.py` | Phase 2 분류·`.stock` 스냅샷·`_authoring.json` 매니페스트 SSOT |
| `scripts/render_thumbs.mjs` | Phase 2 리뷰 썸네일 렌더러 (Playwright, scratch 프로젝트) |
| `references/layout-recipes.md` | **html2pptx-safe 레이아웃 레시피** — 헬퍼 카탈로그 + 좌표 + 패밀리별 레시피 |
| `tests/` | 골든·스모크 테스트 (renderer + Phase 2 회귀 방어) |

## 알려진 제약

- **타이포 사이즈·줄높이·자간은 토큰화 안 됨** — `_pptx-slide.css`의 pt 사이즈/line-height/letter-spacing(.t-display 42pt 등)은 캔버스 960pt × 540pt 에 calibrated 된 고정값(잠금). 단 **font-weight 는 타입스케일 토큰을 따른다** (프리셋의 weight 의도 반영 — 사이즈는 다르게 하려면 템플릿 직접 수정).
- **카드 chrome 는 `surface.card_style` 토큰** — `hairline`(배경+1px 보더, 에디토리얼 기본 = jangpm) / `filled`(배경만) / `borderless`(배경·보더 없이 패딩만). `.card*`·`.feature-tile*` 헬퍼가 `_token_render.py`의 `{{IFEQ}}`/`{{IFNEQ}}` 스위치로 렌더된다.
- **모노 폰트는 `typography.font-mono` 토큰** — `.t-mono` / `--font-mono` / code. 프리셋이 명시 안 하면 모노크롬 기본 mono 체인.
- **01-title.html 의 한국어 카피·캐릭터 이미지 경로는 jangpm 특이** — 새 프리셋 첫 슬라이드는 색만 reskin. 카피·이미지는 프리셋 폴더에서 직접 수정.
- **타이포·간격 등 일부 토큰은 가이드가 명시 안 하면 monochrome 기본값** — 의도. 잘못된 브랜드 값보다 안전한 기본값 우선.
- **DESIGN.md는 draft 상태로 생성됨** — LLM 자동 본문 추출은 의도적으로 stub. 사용자 손글씨가 잘못된 자동 추출보다 안전 (slide-plan introduction guide §살아남은 염려점 #4).

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `validate_theme.py FAILS the v1 token contract` | hex 형식 잘못, 필수 키 누락 | stderr 메시지 보고 드래프트 수정 후 재실행 |
| `missing theme token: X.Y` | 템플릿이 참조하는 토큰을 드래프트가 안 채움 | 드래프트에 토큰 추가, 또는 템플릿이 잘못 참조 중 |
| `init-project.sh` 가 "preset is missing _pptx-slide.css" 라고 함 | 프리셋이 아직 생성 안 됐거나 `--force` 안 한 갱신 후 일부 파일 누락 | `init_theme.py --preset <name> --from <theme.json> --force` 재실행 |
| 새 프리셋의 PPTX 가 jangpm 색으로 나옴 | init-project 가 옛 `slide/templates/` 에서 복사했음 (구버전 init-project.sh) | init-project.sh 가 최신본인지 확인 (Task 8 이후) |

## 다른 슬라이드 스킬과의 관계

이 스킬은 **/slide의 사전 단계**다. 슬라이드를 직접 만들지 않는다. 슬라이드 빌드는 `/slide` 스킬이 담당.

- 입력으로 디자인 가이드(MD) 또는 완결된 프리셋 폴더를 받음
- 출력은 slide 번들의 `assets/design-systems/<preset>/`로 직접 떨어짐 → /slide가 즉시 사용
- claude.ai 업로드 시나리오: theme-init은 로컬에서만 돌고, 그 결과 slide 번들이 새 프리셋과 함께 박제되어 zip → claude.ai 업로드

자산 누적: 프리셋이 늘어날수록 slide 번들의 `assets/design-systems/` 가 풍부해진다. 프리셋 간 비교나 cross-pollination 쉬워짐.
