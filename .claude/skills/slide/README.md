# slide — Editable PPTX 빌더 (자기완결 번들)

이 폴더는 통째로 zip해서 Claude Code 또는 claude.ai에 업로드할 수 있는 자기완결 스킬 번들입니다. 슬라이드별 HTML(960pt × 540pt)을 PowerPoint/Keynote에서 텍스트 편집이 가능한 `.pptx`로 변환합니다.

## 폴더 구조

```
slide/
├── SKILL.md                    스킬 정의 + 워크플로우
├── package.json                런타임 의존성 (playwright, pptxgenjs, sharp)
├── README.md                   이 파일
├── scripts/
│   ├── init-project.sh         새 슬라이드 프로젝트 셋업
│   ├── prebuild-svg.mjs        icons/*.svg → PNG 래스터화 (PptxGenJS 우회)
│   ├── export_deck_pptx.mjs    PPTX 빌드 CLI
│   └── html2pptx.js            HTML → PPTX 변환 엔진 (Playwright)
├── templates/
│   └── build.mjs.template      빌드 스크립트 템플릿
├── references/                 4 hard constraint, 에러 카탈로그 등
└── assets/
    └── design-systems/
        ├── README.md           프리셋 카탈로그 (theme-init이 자동 갱신)
        ├── jangpm/             기본 프리셋 (Pretendard 폰트 포함, ~20MB)
        └── acme-warm/          예제 프리셋
```

## 설치

### 로컬 (slide-html 리포)

리포 루트에 이미 `node_modules`가 있으면 추가 설치 불필요. 없으면:

```bash
cd <repo-root>
npm install playwright pptxgenjs sharp
npx playwright install chromium
```

### claude.ai (이 폴더만 zip해서 업로드한 경우)

```bash
cd .claude/skills/slide
npm install
npx playwright install chromium
```

## 사용 — 두 경로

`/slide`는 진입 시 `output/<project-name>-pptx/slide_plan.json` 존재 여부로 자동 분기합니다.

### Simple (default)

```bash
bash .claude/skills/slide/scripts/init-project.sh <project-name> [<preset>]
cd output/<project-name>-pptx
node build.mjs
```

LLM이 brief에서 슬라이드 구조를 즉흥 결정. 짧은 데크·1회성 초안에 적합. 4 hard constraint만 검증.

### Systematic (선택, slide-plan 사용)

체계적 기획이 필요하면 별도 `slide-plan` 스킬(같은 리포의 `.claude/skills/slide-plan/`)이 먼저 `slide_plan.json`을 산출하고, 본 스킬이 그걸 입력으로 받아 R2(차트↔takeaway 일체화)/R5(evidence 매핑)을 빌드 시점에 검증합니다.

```bash
# 1. /slide-plan 호출 → output/<project>-pptx/slide_plan.json 산출
# 2. 빌드 — slide_plan.json이 있으면 자동 systematic 경로 + R2/R5 검증
node build.mjs
```

> claude.ai 업로드 시나리오에선 본 슬라이드 번들만 올리는 흐름이 일반적이라 systematic 경로는 Claude Code 로컬 환경에서 주로 사용. 번들에 `slide_plan.json`이 없으면 simple 경로로 자동 동작.

자세한 워크플로우는 `SKILL.md` 참고.

## 새 디자인 시스템 추가 (Claude Code 로컬 전용)

별도 `theme-init` 스킬(`.claude/skills/theme-init/`)이 새 프리셋을 만들면 결과를 이 번들의 `assets/design-systems/<new-preset>/`에 직접 떨구고, `assets/design-systems/README.md` 카탈로그를 자동으로 갱신합니다.

theme-init은 claude.ai에 업로드하지 않습니다 — 디자인 시스템은 로컬에서 굽고, 그 결과가 박힌 slide 번들만 claude.ai에 올리는 흐름.

## 폰트 라이센스

`assets/design-systems/jangpm/fonts/` 안의 Pretendard는 SIL Open Font License 1.1로 자유 배포 가능합니다. 동봉된 `LICENSE-fonts.txt` 참고.
