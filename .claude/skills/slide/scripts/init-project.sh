#!/usr/bin/env bash
# init-project.sh — /slide 스킬의 새 PPTX 프로젝트 셋업
#
# 사용:
#   bash .claude/skills/slide/scripts/init-project.sh <project-name> [<design-system>]
#
# 자동 생성:
#   output/<project-name>-pptx/
#   ├── slides/                          (작성할 슬라이드들)
#   │   └── 01-title.html                (보일러플레이트 1장, 즉시 빌드 검증 가능)
#   ├── icons/                           (인라인 SVG 대신 외부 .svg 두는 곳)
#   ├── design-system/                   (선택된 프리셋 폴더 복사 — 자기완결, zip/이동 안전)
#   ├── _pptx-slide.css                  (html2pptx-safe 헬퍼 클래스)
#   ├── build.mjs                        (export_deck_pptx 호출 래퍼)
#   ├── <project-name>.pptx              (빌드 결과물 — 작업공간과 같은 폴더)
#   └── README.md                        (사용법 메모)

set -e

# --- 입력 파싱 ---
if [ -z "$1" ]; then
  echo "Usage: bash init-project.sh <project-name> [<design-system>]"
  echo "  project-name : 프로젝트 식별자 (e.g., q3-board-report)"
  echo "  design-system: 디자인 시스템 프리셋 (default: jangpm)"
  exit 1
fi

PROJECT_NAME="$1"
DESIGN_SYSTEM="${2:-jangpm}"

# --- 경로 계산 ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"
REPO_ROOT="$(cd "$SKILL_DIR/../../.." && pwd)"
PROJECT_DIR="$REPO_ROOT/output/${PROJECT_NAME}-pptx"
DS_ROOT="$SKILL_DIR/assets/design-systems"
DS_SOURCE="$DS_ROOT/$DESIGN_SYSTEM"

# --- 검증 ---
if [ ! -d "$DS_SOURCE" ]; then
  echo "✗ Design system 프리셋을 찾을 수 없습니다: $DESIGN_SYSTEM"
  echo "  사용 가능한 프리셋:"
  ls "$DS_ROOT" | grep -v README | grep -v LICENSE | sed 's/^/    /'
  exit 1
fi

if [ -d "$PROJECT_DIR" ]; then
  echo "✗ 이미 존재하는 프로젝트: $PROJECT_DIR"
  echo "  다른 이름으로 시도하거나 폴더를 먼저 삭제하세요"
  exit 1
fi

# --- 폴더 생성 ---
mkdir -p "$PROJECT_DIR/slides" "$PROJECT_DIR/icons"

# --- 디자인 시스템 복사 ---
# 프로젝트 폴더 자기완결을 위해 심볼릭 링크 대신 디자인 시스템을 복사한다.
# 이 폴더 통째로 zip해서 옮겨도 깨지지 않는다.
cp -R "$DS_SOURCE" "$PROJECT_DIR/design-system"

# --- CSS 복사 ---
# _pptx-slide.css comes from the chosen preset (tokenized per design system)
if [ -f "$DS_SOURCE/_pptx-slide.css" ]; then
  cp "$DS_SOURCE/_pptx-slide.css" "$PROJECT_DIR/_pptx-slide.css"
else
  echo "✗ preset $DESIGN_SYSTEM is missing _pptx-slide.css"
  echo "  Generate it via /theme-init:"
  echo "    python3 $REPO_ROOT/.claude/skills/theme-init/scripts/init_theme.py \\"
  echo "      --preset $DESIGN_SYSTEM \\"
  echo "      --from <draft.json> \\"
  echo "      --force"
  echo "  (theme-init은 기본적으로 이 번들의 assets/design-systems/ 에 출력합니다)"
  exit 1
fi

# --- build.mjs 생성 (output 파일명을 프로젝트 이름으로) ---
sed "s|__OUT_FILENAME__|${PROJECT_NAME}.pptx|" "$TEMPLATES_DIR/build.mjs.template" > "$PROJECT_DIR/build.mjs"

# 만약 template 에 placeholder가 없으면 그대로 복사
if ! grep -q "__OUT_FILENAME__" "$TEMPLATES_DIR/build.mjs.template"; then
  cp "$TEMPLATES_DIR/build.mjs.template" "$PROJECT_DIR/build.mjs"
  # 출력 파일명 패치 (default jangpm-ds-showcase.pptx → 프로젝트명.pptx)
  sed -i.bak "s|jangpm-ds-showcase.pptx|${PROJECT_NAME}.pptx|g" "$PROJECT_DIR/build.mjs"
  rm -f "$PROJECT_DIR/build.mjs.bak"
fi

# --- 보일러플레이트 슬라이드 1장 (Title) ---
# Starter slide comes from the preset's pptx-boilerplate (tokenized per theme)
if [ -f "$DS_SOURCE/pptx-boilerplate/01-title.html" ]; then
  cp "$DS_SOURCE/pptx-boilerplate/01-title.html" "$PROJECT_DIR/slides/01-title.html"
else
  echo "✗ preset $DESIGN_SYSTEM is missing pptx-boilerplate/01-title.html"
  echo "  Generate it via /theme-init (see message above)"
  exit 1
fi

# --- README ---
cat > "$PROJECT_DIR/README.md" <<EOF
# ${PROJECT_NAME} (editable PPTX)

생성됨: $(date +%Y-%m-%d) · 디자인 시스템: ${DESIGN_SYSTEM}

## 작업 흐름

1. \`slides/\` 안에 슬라이드 HTML 파일 작성/추가 (\`NN-name.html\` 형식, 파일명 순으로 빌드됨)
2. 모든 슬라이드는 \`/slide\` 스킬의 4 hard constraint 통과 필수 (\`.claude/skills/slide/references/4-constraints.md\`)
3. 새 슬라이드는 처음부터 그리지 말고 \`.claude/skills/slide/templates/\` 의 가까운 패턴 복사 → 콘텐츠만 교체
4. 빌드:

   \`\`\`bash
   node build.mjs
   \`\`\`

5. 결과: \`${PROJECT_NAME}.pptx\` (이 프로젝트 폴더 안. PowerPoint/Keynote 더블클릭으로 텍스트 편집 가능)

## 의존성 (프로젝트 루트에서 1회)

\`\`\`bash
cd $REPO_ROOT
npm install playwright pptxgenjs sharp
npx playwright install chromium
\`\`\`

## 자주 만나는 빌드 에러

- \`Text element <p> has background\` → 외부 div 가 배경 담당 (E1)
- \`CSS gradients are not supported\` → 순색으로 (E3)
- \`ends too close to bottom edge\` → bottom ≥ 44pt (E6)
- 더 보려면: \`.claude/skills/slide/references/error-patterns.md\`
EOF

# --- 완료 메시지 ---
cat <<EOF

✓ 프로젝트 생성 완료: ${PROJECT_DIR}

  ├── slides/01-title.html         (보일러플레이트 1장)
  ├── icons/                       (외부 SVG 폴더)
  ├── design-system/                (${DESIGN_SYSTEM} 복사본)
  ├── _pptx-slide.css              (html2pptx-safe 헬퍼)
  ├── build.mjs                    (빌드 스크립트)
  └── README.md

다음 단계 — 두 경로 중 선택:

  [Simple]  바로 슬라이드 작성 → node build.mjs
            slides/01-title.html을 보일러플레이트 기준으로 채우거나 추가.

  [Systematic]  /slide-plan 으로 먼저 데크 구조 기획
                → ${PROJECT_DIR}/slide_plan.json 확정
                → node build.mjs (자동으로 R2/R5 검증 후 빌드)

빌드 결과: ${PROJECT_DIR}/${PROJECT_NAME}.pptx
EOF
