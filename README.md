# slide-html

> **per-slide HTML × html2pptx 기반의 16:9 editable PPTX 디자인 시스템.**
> Claude Code 채팅창에 "Q3 사업 리뷰 슬라이드 만들어줘"라고 한 줄만 입력하면,
> `/slide` 스킬이 슬라이드별 독립 HTML(960pt×540pt)을 작성 →
> html2pptx가 DOM의 computedStyle을 PowerPoint 객체로 1:1 번역 →
> `output/<주제>-pptx/<주제>.pptx`를 떨어뜨립니다.
> PowerPoint/Keynote에서 **텍스트 더블클릭으로 직접 편집** 가능한 진짜 .pptx입니다 — 이미지 깔린 가짜 PPTX가 아닙니다.

![Theme](https://img.shields.io/badge/theme-Jangpm-4633E3)
![Viewport](https://img.shields.io/badge/viewport-960pt%C3%97540pt-0b1f3a)
![Patterns](https://img.shields.io/badge/patterns-37-brightgreen)
![Stack](https://img.shields.io/badge/stack-HTML%20%C2%B7%20html2pptx%20%C2%B7%20pptxgenjs-6b4bff)
![Platform](https://img.shields.io/badge/platform-Claude%20Code-6b4bff)

<sub>📦 Based on <a href="https://github.com/alchaincyf/huashu-design">alchaincyf/huashu-design</a> · `/slide` editable PPTX 파이프라인 + `/theme-init` 멀티 프리셋 시스템 추가</sub>

---

## 이게 뭔가요? (1분 요약)

- **무엇을 하는 도구:** 글로만 지시하면 PowerPoint에서 바로 편집 가능한 슬라이드 덱을 자동으로 만들어주는 도구입니다.
- **누가 쓰면 좋은가:** 기획자·마케터·강사·임원·컨설턴트 — **PPT 한 장씩 만들기 지겹고, 나중에 회사 템플릿으로 옮겨야 하는 누구나.**
- **어떻게 쓰는가:** Claude Code 안에서 `/slide` 또는 자연어로 요청하면 됩니다. 명령어 암기 불필요.
- **결과물:**
  - **editable PPTX** (`output/<주제>-pptx/<주제>.pptx`) — PowerPoint/Keynote에서 텍스트 더블클릭 편집
  - 슬라이드별 HTML (`output/<주제>-pptx/slides/NN-name.html`) — 브라우저로 미리보기·인쇄
  - Google Slides (`/upload-drive` 실행 시) — Drive 자동 업로드 + Slides 변환

**예시 한 줄:**
> "사내 AI 도구 도입 효과 슬라이드 12장 만들어줘. KPI 위주로."

↓ 1~3분 후 ↓

→ `output/사내-AI-도입-pptx/사내-AI-도입.pptx` 생성. 표지 → 컨텍스트 → KPI 대시보드 →
사례 카드 → 로드맵 → 클로징 12장이 Jangpm 디자인 시스템(모노크롬 + accent `#4633E3`)으로 통일되어 들어 있고, 각 텍스트는 PowerPoint에서 그대로 편집 가능합니다.

---

## 디자인 시스템 — Jangpm

이 저장소의 활성 테마는 **Jangpm Slide Design System**입니다. 한 마디로:
**"맥킨지 표지처럼 임팩트, 본문은 미니멀 모노크롬, 강조는 단 한 가지 색."**

| 항목 | 값 |
|---|---|
| 뷰포트 | **960pt × 540pt (16:9, LAYOUT_WIDE)** — PowerPoint 네이티브 슬라이드 사이즈 |
| 폰트 | **Pretendard** 9 weights (한글/영어 통합) |
| 강조색 | **`#4633E3`** — 한 슬라이드당 1~2회만 사용 |
| accent-soft | `#E8E5FC` — 강조 카드 배경 |
| 모드 | **라이트 전용** (다크 배경 슬라이드는 closing-dark 패턴 한정) |
| 카드 | 12px radius · 24pt padding · 1px border |
| 그림자 | 미사용 (텍스트는 그림자 없는 `<p>/<h*>` 안에만) |
| 아이콘 | 인라인 SVG (stroke `currentColor`, 2px) 또는 외부 SVG 파일. **이모지·유니코드 장식 기호 금지** |

**타이포 스케일 (시맨틱 클래스 우선):**

| 클래스 | 크기(pt) | 굵기 | 용도 |
|---|---|---|---|
| `.t-display` | 56 | 800 | 커버·섹션 타이틀 |
| `.t-display-sm` | 40 | 800 | KPI 큰 숫자 |
| `.t-headline` | 32 | 700 | h2 (콘텐츠 슬라이드 헤딩) |
| `.t-title` | 18 | 600 | 카드 제목 |
| `.t-body` | 14 | 400 | 본문 |
| `.t-cap-up` | 11 | 600 | 라벨 / 카테고리 (uppercase) |

> 시각 레퍼런스의 단일 진실 원천(SSOT)은
> **`.claude/skills/huashu-design/assets/design-systems/jangpm/`** 폴더 전체입니다 (`brand-spec.md` + `colors_and_type.css` + `_pptx-slide.css` + `pptx-boilerplate/`).
> 다른 디자인 시스템으로 바꾸거나 새 브랜드 프리셋을 추가하려면 → **`/theme-init`** (수동 편집 금지).

---

## 처음 설치하는 분을 위한 준비 (5분)

### 1단계. Claude Code 설치

[Claude Code 공식 다운로드](https://claude.com/claude-code) — Mac / Windows / Linux 모두 지원.

### 2단계. 이 저장소 클론

```bash
git clone https://github.com/byungjunjang/slide-html.git ~/Desktop/slide-html
cd ~/Desktop/slide-html
```

### 3단계. 의존성 설치 (한 번만)

```bash
npm install                          # playwright, pptxgenjs, sharp
npx playwright install chromium      # html2pptx의 브라우저 캡처용
```

### 4단계. (선택) Google Drive 업로드 도구

| 변환 종류 | 필요 도구 | 설치 |
|---|---|---|
| editable PPTX | 위 의존성 (이미 설치됨) | — |
| Google Slides 업로드 | `gws-drive-upload` 스킬 + Google 인증 | Claude Code Skills 안내 따라 인증 |

> 💡 슬라이드별 HTML 미리보기는 별도 빌드 없이 브라우저로 그대로 열면 됩니다 (`output/<주제>-pptx/slides/01-title.html` 더블클릭).

---

## 쓰는 법 — 두 경로

목적에 맞게 두 가지 경로 중 선택. `/slide`가 진입 시 `output/<주제>-pptx/slide_plan.json` 존재 여부로 자동 분기합니다.

### 🟢 경로 A — Simple (default, 짧은 데크·1회성)

```
/slide AI 코딩 도구 도입 효과 발표 12장 만들어줘. KPI 중심으로.
```

또는 **슬래시 없이 자연어로**:

```
사내 발표용으로 우리 팀 AI 도입 효과 슬라이드 만들어줘.
```

Claude는 자동으로 다음 5단계를 순서대로 실행합니다 (slide_plan.json 없이 즉흥 결정):

1. **프로젝트 셋업** — `init-project.sh <주제>` 실행 → `output/<주제>-pptx/` 생성, jangpm 프리셋 심볼릭 링크 + 보일러플레이트 1장 복사
2. **주제 분석 + 패턴 배치** — 슬라이드 수와 패턴 시퀀스 결정 (37 패턴 중 다양성 룰)
3. **슬라이드 작성** — `slides/NN-name.html` 한 파일씩 작성. 보일러플레이트에서 가까운 패턴 복사 → 콘텐츠만 교체
4. **빌드** — `cd output/<주제>-pptx && node build.mjs` → html2pptx가 슬라이드별 HTML을 OOXML 객체로 번역
5. **검증** — `<주제>.pptx`를 PowerPoint/Keynote에서 열어 텍스트 더블클릭 편집 확인

### 🟣 경로 B — Systematic (체계적 기획이 필요할 때)

컨설팅 데크·멀티 evidence·재현성이 필요할 때. `/slide-plan`이 먼저 데크 구조를 기획하고 그 결과(`slide_plan.json`)를 `/slide`가 소비합니다.

```
/slide-plan Q3 보드 리뷰 데크. 신규 채널 자기잠식 분석. 이사회 30분.
```

→ `output/Q3-보드-리뷰-pptx/slide_plan.json` 생성 + 슬라이드별 1줄 markdown 요약 → 사용자 검토·confirm

```
/slide
```

→ slide_plan.json을 입력으로 받아 R2(차트↔takeaway)/R5(evidence 매핑) 빌드 시점 검증 → 각 슬라이드는 plan의 `recommended_layout_family`에 박힌 boilerplate를 그대로 따라 렌더.

R2/R5 위반 시 빌드 자동 차단 (exit 1). 자세한 사양은 `.claude/skills/slide-plan/SKILL.md`.

### 추가로 변환하기

```
/upload-drive          ← PPTX → Google Drive 업로드 + Slides 변환
```

> PDF가 필요하면 PowerPoint/Keynote에서 직접 export하세요. 이 저장소는 **editable PPTX 단일 경로**로 설계되어 있어 별도 PDF 파이프라인을 두지 않습니다.

### 디자인 테마 자체를 바꾸고 싶으면

```
/theme-init            ← 새 브랜드 프리셋 추가 (기존 jangpm 보존)
```

테마 가이드 마크다운(필수)을 사용자가 제공하면, 토큰을 추출 → `theme.json`(v1 컨트랙트) → `colors_and_type.css` + `_pptx-slide.css` + 8장 보일러플레이트까지 일괄 렌더링합니다. 새 폴더로 추가될 뿐 **기존 프리셋은 손대지 않습니다** (멀티 프리셋 모델).

---

## claude.ai에 단독 업로드하기

이 프로젝트의 `/slide` 스킬은 **`.claude/skills/slide/` 폴더만 zip으로 묶어 claude.ai에 그대로 업로드**할 수 있게 자기완결화되어 있습니다. 외부 MCP 서버나 다른 스킬 폴더를 참조하지 않으며, 변환 엔진(`export_deck_pptx.mjs` + `html2pptx.js`), 디자인 시스템(jangpm + acme-warm + Pretendard 폰트), 보일러플레이트 37개가 모두 폴더 안에 들어 있습니다 (~21MB).

claude.ai 업로드 후 첫 사용 시:

```bash
cd .claude/skills/slide
npm install
npx playwright install chromium
```

`html2pptx.js`가 Playwright로 HTML 레이아웃을 측정하므로 Chromium 바이너리 설치가 필수입니다.

권장 동봉 안 하는 것:

- **`/theme-init` 스킬** — 새 디자인 시스템을 굽는 용도라 Claude Code 로컬 전용. theme-init은 자기 출력물을 `slide/assets/design-systems/`에 직접 떨궈 카탈로그(`README.md`)까지 자동 갱신하므로, 로컬에서 새 프리셋을 굽고 그 결과가 박힌 slide 번들을 claude.ai에 올리는 흐름.
- **`/upload-drive` 스킬** — Google Drive 인증 토큰이 필요해 claude.ai 샌드박스에서 동작하지 않음.

번들 사용 가이드는 `.claude/skills/slide/README.md`에 더 자세히 적혀 있습니다.

---

## 실전 가이드 — 폴더 정리 & 시나리오

### 폴더 정리 방법

```
slide-html/
├── inputs/                              ← 원본 자료 (직접 만들고 채워넣음, 선택)
│   ├── KPI지표.xlsx
│   ├── 사례리서치.pdf
│   └── 메시지요약.md
├── output/                              ← 완성물 (자동 생성)
│   └── <주제>-pptx/
│       ├── slides/NN-*.html             ← 슬라이드별 HTML (자동 생성)
│       ├── design-system/  → jangpm     ← 심볼릭 링크 (자동)
│       ├── _pptx-slide.css              ← html2pptx-safe 헬퍼 (자동 복사)
│       ├── build.mjs                    ← 빌드 스크립트 (자동 생성)
│       ├── icons/                       ← 외부 SVG 두는 곳
│       ├── <주제>.pptx                  ← 빌드 결과물 (editable)
│       └── README.md
└── ...
```

폴더 이름은 한글/영어 무관. **각 생성 요청 = `output/<주제>-pptx/` 한 폴더로 격리** — 자기완결적이라 다른 프로젝트와 절대 섞이지 않습니다. 이전 덱이 새 덱에 영향 주지 않음.

### 시나리오 A. 분기 사업 리뷰 덱

```
inputs/
├── 4분기_재무.xlsx
└── 리스크_리스트.md
```

```
inputs/ 자료 보고 Q4 사업 리뷰 12장 만들어줘.
4분기_재무.xlsx 요약 시트로 KPI 대시보드 한 장,
리스크는 매트릭스로, 결론은 투자 승인 요청.
```

### 시나리오 B. 사내 AI 도입 발표

```
inputs/
├── 도입사례.csv
└── 메시지초안.md
```

```
사내 AI 도입 성과 발표 10장. 이미지 표지 + 도입 전후 비교 +
KPI 4개 + 사례 6개 + 로드맵 + 클로징.
```

### 시나리오 C. 숫자만 있고 스토리는 모를 때

```
inputs/
└── 5년_매출.csv
```

```
5년_매출.csv만 보고 핵심 메시지 5장으로 뽑아줘. 추세, 변곡점, 이상치 중심.
```

### 결과가 마음에 안 들면 바로 수정

```
슬라이드 4를 KPI 대시보드 패턴(31-kpi-dashboard)으로 바꿔줘. 전년 대비 화살표 포함.
```

```
슬라이드 7의 세 번째 카드를 accent 톤으로 바꿔줘 (시선 앵커).
```

```
전체적으로 그라디언트 잔존하는 거 다 빼고, 다크 배경은 closing 한 장만 남겨.
```

```
영문판도 같이 만들어줘. 구조·숫자는 동일하게.
```

대화하듯 계속 다듬을 수 있습니다. 각 수정은 슬라이드 HTML 파일 하나만 건드리므로 부분 재빌드도 가능합니다.

---

## 자주 묻는 질문

**Q. 이거 진짜 PowerPoint에서 텍스트 편집되나요? 이미지 PPTX 아닙니까?**
A. 진짜 됩니다. `html2pptx.js`가 슬라이드 HTML의 모든 `<p>` / `<h1~h6>`를 PowerPoint 텍스트 프레임(`<a:txBody>`)으로 번역하기 때문에, PowerPoint/Keynote/Google Slides에서 텍스트를 더블클릭하면 직접 편집할 수 있습니다. 이미지 깔린 가짜 PPTX가 아닙니다.

**Q. 왜 React/Vite 안 쓰고 슬라이드별 HTML 파일을 만드나요?**
A. html2pptx는 DOM의 computedStyle을 슬라이드 단위로 캡처합니다. 슬라이드 1장 = HTML 파일 1개로 격리하면 (1) 슬라이드 간 CSS 누수 방지, (2) 한 장만 빌드/디버그 가능, (3) PowerPoint의 슬라이드-당-XML 모델과 1:1 매핑 — 세 가지가 자동으로 보장됩니다. 자매 프로젝트 `slide-pencil`은 React 경로, 이 저장소는 HTML 경로입니다 (아래 "자매 프로젝트" 참고).

**Q. 디자인 색상·폰트를 우리 회사 브랜드로 바꾸고 싶어요.**
A. `/theme-init`을 쓰세요. 디자인 가이드 마크다운(필수)을 주면 35개 토큰을 추출 → `theme.json` → `colors_and_type.css` + `_pptx-slide.css` + 보일러플레이트 8장까지 새 폴더로 렌더링합니다. 기존 jangpm은 그대로 보존되므로, 한 사용자가 N개 프리셋을 동시에 가질 수 있습니다. 수동 편집 금지 — 토큰 컨트랙트가 어긋나면 빌드가 실패합니다.

**Q. 슬라이드 개수를 지정할 수 있나요?**
A. 네. "10장으로", "15슬라이드짜리"라고 말하면 그대로 만듭니다. 미지정 시 주제 분량에 맞게 자동 결정 (보통 8–15장).

**Q. 영어 덱도 만들 수 있나요?**
A. 네. 한국어로 요청하면서 "영문으로 만들어줘"라고 하거나, 영어로 요청하면 영어 덱이 나옵니다. Pretendard는 영문도 깔끔하게 처리합니다.

**Q. 빌드가 4 hard constraint로 실패해요.**
A. 가장 흔한 4가지: (1) DIV 안에 `<p>` 없이 맨텍스트, (2) `linear-gradient`/`radial-gradient` 사용, (3) `<p>`에 `background`/`border`/`shadow`, (4) DIV에 `background-image`. 자세한 픽스는 `.claude/skills/slide/references/error-patterns.md`. Claude는 빌드 실패 시 자동으로 픽스를 시도합니다.

**Q. 기밀 데이터인데 안전한가요?**
A. 파일은 모두 로컬에서 처리됩니다 (브라우저 캡처도 로컬 chromium). 단, Claude와의 대화 내용은 AI 응답을 받기 위해 Anthropic 서버로 전달됩니다. 회사 보안 정책에 따라 판단하세요.

**Q. 이전 슬라이드 덱이 다음 작업에 끼어드나요?**
A. 안 끼어듭니다. 각 요청 = `output/<주제>-pptx/` 독립 폴더로 격리되며, 디자인 시스템만 심볼릭 링크로 공유합니다. 이전 덱을 삭제할 필요 없이 그냥 새 주제로 요청하면 됩니다.

---

## 어떤 슬라이드 패턴을 만들어주나요? — 37개 Jangpm 패턴

Claude가 자동으로 골라주지만, 직접 지정하고 싶으면 패턴 ID로 부르면 됩니다.
패턴 HTML 원본은 `.claude/skills/huashu-design/assets/design-systems/jangpm/pptx-boilerplate/`에 있습니다.

### 🪪 표지·구조 슬라이드
- **01-title** — 메인 표지
- **23-cover-with-character** — 캐릭터 포함 표지
- **25-cover-vertical** — 세로형 표지 (이미지 강한 슬라이드용)
- **10-agenda** — 목차
- **09-section** — 섹션 구분 (큰 번호 + 섹션 타이틀)
- **17-summary** — 요약
- **21-closing-light** / **22-closing-big** — 라이트 클로징
- **08-closing-dark** — 다크 풀블리드 클로징 (다크 배경 허용 예외)

### 🎨 디자인 시스템 쇼케이스
- **03-color-grid** — 컬러 토큰 스와치
- **04-type-scale** — 타이포 스케일 데모

### 🧱 그리드 카드 (고밀도)
- **02-overview** — 헤더 + 카드
- **11-three-point** — 3분할 카드
- **12-four-point** — 4분할 카드
- **13-six-point** — 6분할 카드
- **27-matrix-trends** — 트렌드 매트릭스
- **31-kpi-dashboard** — KPI 4~8개 타일

### 📊 데이터·테이블 패턴
- **05-card-kpi** — 카드 + KPI 큰 숫자 + 배지
- **16-stats** — 큰 숫자 + 본문
- **06-table** — 비교 테이블 (하이라이트 컬럼)
- **19-table-detailed** — 상세 비교 테이블
- **20-forecast-table** — 실적 + 전망 테이블
- **28-pnl** — 손익 테이블
- **29-seasonal** — 계절성 차트형 테이블

### 🔁 비교·프로세스
- **14-comparison** — 좌우 비교 (Before/After)
- **15-process** — 프로세스 흐름도 (3~6단계)
- **30-paired-concept** — 짝개념 카드

### 📝 진행·체크리스트
- **24-checklist** — 체크리스트
- **34-exercise-1up** — 실습 슬라이드 (1단)
- **35-exercise-2up** — 실습 슬라이드 (2단)

### 🖼 이미지·인용
- **07-quote-section** — 인용 + 섹션 디바이더
- **18-quote-attribution** — 출처 포함 인용
- **36-image-1up** — 이미지 1장 풀폭
- **37-image-2up** — 이미지 2장
- **26-overview-split** — 좌우 분할 (이미지 + 본문)

### 💻 데모·기술 콘텐츠
- **32-terminal-split** — 터미널 + 설명 분할
- **33-terminal-full** — 터미널 풀스크린

> **다양성 룰:** 연속 동일 패턴 금지(section 예외), 8장 이하 → 3종 이상, 10장 이상 → 4종 이상, 고밀도 grid 패턴은 콘텐츠의 30% 이상.

---

## 저장소 구조

```
slide-html/
├── .claude/
│   └── skills/
│       ├── slide/                                    ← /slide 스킬 (메인 파이프라인)
│       │   ├── SKILL.md
│       │   ├── references/
│       │   │   ├── 4-constraints.md                  ← html2pptx-safe HTML 룰
│       │   │   ├── canvas-spec.md                    ← 960pt × 540pt 좌표/폰트
│       │   │   ├── css-helpers.md                    ← _pptx-slide.css 클래스 카탈로그
│       │   │   └── error-patterns.md                 ← 빌드 에러 픽스 (E1~E10)
│       │   ├── scripts/init-project.sh               ← 프로젝트 셋업 자동화
│       │   └── templates/build.mjs.template          ← 빌드 스크립트 템플릿
│       │
│       ├── huashu-design/                            ← 디자인 시스템 자산 + 헤리티지
│       │   ├── SKILL.md
│       │   └── assets/design-systems/
│       │       ├── jangpm/                           ← 활성 프리셋 (SSOT)
│       │       │   ├── theme.json                    ← v1 토큰 컨트랙트
│       │       │   ├── brand-spec.md
│       │       │   ├── colors_and_type.css           ← CSS 변수
│       │       │   ├── _pptx-slide.css               ← html2pptx-safe 헬퍼
│       │       │   ├── pptx-boilerplate/01..37.html  ← 37 패턴 HTML
│       │       │   ├── fonts/                        ← Pretendard
│       │       │   └── assets/                       ← character.png, icons
│       │       │
│       │       └── acme-warm/                        ← 추가 프리셋 (예시)
│       │
│       ├── theme-init/                               ← 새 브랜드 프리셋 생성기
│       │   ├── SKILL.md
│       │   ├── scripts/init_theme.py
│       │   ├── templates/
│       │   ├── examples/acme-warm.md                 ← 가이드 마크다운 예시
│       │   └── docs/
│       │       └── 2026-04-27-pattern-compatibility-audit.md
│       │
│       └── upload-drive/                             ← PPTX → Google Slides
│           └── SKILL.md
│
├── output/                                           ← 빌드 결과물 (주제별 폴더)
│   └── <주제>-pptx/
│       ├── slides/NN-*.html                          ← 슬라이드별 독립 HTML
│       ├── design-system/  → jangpm                  ← 심볼릭 링크
│       ├── _pptx-slide.css                           ← 프리셋에서 복사
│       ├── build.mjs
│       ├── icons/                                    ← 외부 SVG
│       └── <주제>.pptx                               ← editable 결과물
│
├── package.json                                      ← playwright, pptxgenjs, sharp
├── README.md                                         ← (이 파일)
└── LICENSE
```

---

## 핵심 제약 (4 HARD CONSTRAINTS)

`/slide` 스킬이 모든 슬라이드 HTML에 강제하는 4가지 룰. **PowerPoint 파일 포맷(OOXML) 자체의 물리적 약속**을 HTML에 투영한 것이라 우회할 수 없습니다 (도구가 게을러서가 아님).

- **C1. 텍스트는 `<p>` 또는 `<h1>~<h6>` 안에만** — DIV에 맨텍스트 금지. PowerPoint 텍스트는 반드시 text frame(`<a:txBody>`) 안에 존재. text frame은 HTML의 단락 레벨 요소(p / h1~h6 / li)에 매핑되며, 맨 div는 PPTX에서 대응되는 텍스트 컨테이너가 없음.
- **C2. CSS 그라디언트 금지 (linear / radial 모두) — 순색만** — PowerPoint의 shape fill은 solid / preset gradient만 지원. CSS의 임의 각도/위치 그라디언트는 PPTX 그라디언트 문법으로 1:1 매핑 불가. 다색이 필요하면 flex 자식 div가 각자 순색.
- **C3. `<p>/<h*>`에 `background` / `border` / `shadow` 금지 — 외부 div가 담당** — 텍스트 프레임 자체에 배경을 칠하면 OOXML이 텍스트와 도형을 분리할 수 없음. 카드 모양은 외부 div가, 텍스트는 안쪽 `<p>`가 분담.
- **C4. div에 `background-image` 금지 — `<img>` 태그 사용** — html2pptx는 `<img>`만 PowerPoint Picture로 추출. div의 background-image는 무시되어 결과 PPTX에 사라짐.

빌드 실패 시 다음 검증 메시지 중 하나가 뜹니다:

| 에러 | 픽스 |
|---|---|
| `Text element <p> has background` | 외부 div가 배경 담당 |
| `DIV element contains unwrapped text` | `<p>` 또는 `<h*>`로 감싸기 |
| `CSS gradients are not supported` | 순색으로 |
| `Background images on DIV` | `<img>` 태그로 |
| `HTML content overflows body` | 콘텐츠 줄이기 / 폰트 축소 |
| `ends too close to bottom edge` | bottom ≥ 44pt |
| `Inline element <span> has margin` | margin 제거, `&nbsp;` 사용 |

전체 카탈로그: `.claude/skills/slide/references/error-patterns.md` (E1~E10).

---

## 빌드 & 개발

### 새 프로젝트 시작

```bash
# 1. 프로젝트 셋업 (jangpm 프리셋 기본)
bash .claude/skills/slide/scripts/init-project.sh q3-board-report

# 2. (선택) 다른 프리셋으로
bash .claude/skills/slide/scripts/init-project.sh q3-board-report acme-warm

# 3. 슬라이드 HTML 작성/수정 후 빌드
cd output/q3-board-report-pptx
node build.mjs

# → output/q3-board-report-pptx/q3-board-report.pptx 생성
```

### 단일 슬라이드 디버깅

```bash
# 슬라이드 HTML을 브라우저로 직접 열어 시각 검증
open output/q3-board-report-pptx/slides/03-kpi.html

# 4 constraint 위반 자동 검증 (build.mjs가 슬라이드별로 실행)
node build.mjs
```

### 의존성 (저장소 루트에서 1회)

```bash
npm install                      # playwright + pptxgenjs + sharp
npx playwright install chromium  # html2pptx의 DOM 캡처용
```

---

## 자매 프로젝트

이 저장소는 **세 가지 슬라이드 파이프라인** 중 하나입니다. 같은 주제로 세 가지 다른 결과물을 동시에 만들 수 있게 설계되어 있습니다.

| 프로젝트 | 입력 → 출력 | 강점 |
|---|---|---|
| **slide-html** (이 저장소) | 자연어 → 슬라이드별 HTML(960pt×540pt) → html2pptx → editable PPTX | **PowerPoint 네이티브 편집성**, OOXML 1:1 매핑, 가벼운 스택 |
| **slide-pencil** | 자연어 → Pencil MCP → React/Tailwind → 단일 HTML/PPTX | 디자인 일관성, 시각 레퍼런스(.pen) 기반, Vite 단일 파일 |
| **slide-svg** | 자연어 → 네이티브 SVG → DrawingML PPTX | 도형 단위 정밀도, 활성 테마 락 |

세 파이프라인 모두 같은 Jangpm 토큰 컨트랙트를 공유하므로, 한 결과물의 변경사항을 다른 두 결과물에 옮기는 것도 어렵지 않습니다.

---

## 기반 (Acknowledgments)

이 저장소는 [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)을 기반으로 만들어졌습니다.
huashu-design의 디자인 시스템 자산(Jangpm preset, character, fonts)과 React/HTML/SVG 도구 체인을 그대로 가져와,
editable PPTX 파이프라인(`/slide` 스킬)과 멀티 프리셋 생성기(`/theme-init` 스킬)를 추가한 fork입니다.

- **원본:** [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)
- **라이선스:** 원본 huashu-design Personal-Use License를 그대로 계승 (`LICENSE` 참조)
- **추가 기여:** per-slide HTML(960pt×540pt) → html2pptx 파이프라인, 4 hard constraint, theme-init v1 token contract, 37 jangpm 패턴 보일러플레이트

---

## 라이선스 & 기여

- **라이선스:** 본 저장소는 [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)의 **Personal-Use License를 계승**합니다 — 개인·학습·비상업 용도에 한해 자유롭게 사용 가능, **상업적 이용은 금지**. 자세한 조건은 [`LICENSE`](./LICENSE) 참조.
- **버그 리포트·패턴 제안:** GitHub 이슈 환영
- **PR:** 새 프리셋 추가, 보일러플레이트 패턴 추가, 4 constraint 위반 사례 환영
- **테마 추가 제안:** `/theme-init` 사용법은 `.claude/skills/theme-init/SKILL.md` 참조

---

<details>
<summary>🛠 개발자용 (스킬 내부 구조 · 토큰 컨트랙트 · html2pptx 파이프라인)</summary>

### 토큰 컨트랙트 v1

`.claude/skills/theme-init/` 가 강제하는 35개 토큰. **테마와 무관하게 항상 같은 의미**로 유지되어야 합니다:

| 그룹 | 토큰 |
|---|---|
| Identity | `name`, `display_name`, `description` |
| Colors (17) | `bg`, `surface`, `surface-alt`, `text`, `text-secondary`, `text-tertiary`, `border`, `border-strong`, `accent`, `accent-soft`, `accent-ink`, `positive`, `positive-soft`, `negative`, `negative-soft`, `warning`, `warning-soft` |
| Typography | `font-chain`, 7-step type scale (display, display-sm, headline, title, body, caption, label) — 각각 size/weight/line-height/letter-spacing/transform |
| Radius (6) | xs, sm, md, lg, xl, pill |
| Stroke (3) | icon, divider, emphasis |
| Spacing (11) | 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16 (8px grid) |
| Assets | `icon-pack-default`, `icon-pack-fallback`, `character` (optional) |
| Voice | `tone`, `pov`, `register`, `forbidden_phrases`, `gm_style_hint` |

`/theme-init`은 이 35개 키 이름을 유지한 채 값만 새 테마로 교체합니다. 가이드에 명시되지 않은 토큰은 **null로 두거나 생략** — `fill_theme_defaults.py`가 단조로운 안전 기본값으로 채웁니다. **추측해서 채우지 말 것** (잘못된 브랜드 색보다 회색 기본값이 낫다).

### `/slide` 5단계 워크플로우

```
Step 1: 프로젝트 셋업
  bash .claude/skills/slide/scripts/init-project.sh <name> [<preset>]
  → output/<name>-pptx/  (slides/, design-system/→preset, _pptx-slide.css, build.mjs)

Step 2: 슬라이드 작성 (LLM)
  ├─ 보일러플레이트(<preset>/pptx-boilerplate/)에서 가까운 패턴 복사
  ├─ 콘텐츠만 교체 — 처음부터 그리지 않음
  └─ 4 hard constraint (C1-C4) 통과

  → 게이트: 모든 슬라이드 HTML이 brace `<p>` 안에 텍스트, 그라디언트 없음, 텍스트 프레임에 box style 없음, img 태그만 사용

Step 3: 빌드
  cd output/<name>-pptx && node build.mjs
  → html2pptx가 슬라이드별 HTML → PowerPoint XML 객체 변환
    1. Playwright 로 chromium에서 슬라이드 HTML 렌더
    2. computedStyle 추출 (위치, 폰트, 색)
    3. pptxgenjs 객체 빌드 (txBody, sp, pic)
    4. ZIP 패키징 → .pptx

Step 4: 에러 픽스 (실패 시)
  references/error-patterns.md 의 알려진 픽스 적용

Step 5: 검증
  PowerPoint/Keynote 에서 .pptx 열기 → 텍스트 더블클릭 편집 가능 확인
```

### `/theme-init` 6단계 오케스트레이터

```
1. fill_theme_defaults — 부분 드래프트 → 모든 토큰 채워진 theme.json
2. patch name         — --preset 인자로 name/display_name 덮어쓰기
3. validate_theme     — v1 토큰 컨트랙트 schema 검증
4. resolve prelude    — --fonts-prelude → 기존 _fonts.css → 자동 생성 _header.css
5. render             — colors_and_type.css, _pptx-slide.css, brand-spec-generated.md,
                       pptx-boilerplate/01..08.html
6. report             — 다음 단계 안내
```

산출물 구조 (preset 한 개당):

```
.claude/skills/huashu-design/assets/design-systems/<preset>/
├── theme.json                    # source of truth (v1 contract)
├── colors_and_type.css           # CSS 변수 (--bg, --accent, --fs-display, ...)
├── _pptx-slide.css               # html2pptx-safe 헬퍼 (.card-accent, .bg-accent, ...)
├── brand-spec-generated.md       # 인간 가독 토큰 레퍼런스
├── _header.css 또는 _fonts.css   # 코멘트 헤더 (+ 옵션 @font-face)
├── pptx-boilerplate/01..37.html  # 37 패턴 HTML (preset 토큰으로 reskin)
└── (옵션) fonts/, assets/        # 사용자 폰트, 캐릭터, 아이콘 팩
```

### 4 Hard Constraint의 OOXML 근거

| 제약 | OOXML 근거 |
|---|---|
| C1: 텍스트는 단락 요소 안에 | `<p:sp>` 안의 `<p:txBody>` 는 `<a:p>` 의 시퀀스. div 단위 텍스트는 매핑 슬롯 없음 |
| C2: 그라디언트 순색만 | `<a:solidFill>` / `<a:gradFill>` 는 preset stop 만 지원. CSS 임의 그라디언트 1:1 변환 불가 |
| C3: 단락에 box style 금지 | 단락 요소(`<a:p>`)에는 `bodyPr`/`pPr`/`rPr` 만. background/border는 부모 `<p:sp>` 의 `<p:spPr>` 책임 |
| C4: img만 picture로 | `<p:pic>` 의 `<p:blipFill>` 은 `<img>` 의 src와 1:1. CSS background-image는 추출 대상 아님 |

자세한 내용: `.claude/skills/slide/references/4-constraints.md` 및 `references/canvas-spec.md`.

### 의존성 한눈에

```
playwright 1.59  — chromium 헤드리스 (DOM 측정용)
pptxgenjs  4.0   — OOXML 객체 모델 빌더
sharp      0.34  — 이미지 리사이즈/포맷 변환
```

### 주요 경로 한눈에

```
.claude/skills/slide/SKILL.md                                           ← /slide 스킬 정의
.claude/skills/slide/references/4-constraints.md                        ← 4 hard constraint
.claude/skills/slide/references/error-patterns.md                       ← 빌드 에러 픽스
.claude/skills/slide/scripts/init-project.sh                            ← 프로젝트 셋업
.claude/skills/slide/templates/build.mjs.template                       ← 빌드 스크립트 템플릿
.claude/skills/huashu-design/assets/design-systems/jangpm/              ← 활성 프리셋 SSOT
.claude/skills/huashu-design/assets/design-systems/jangpm/pptx-boilerplate/  ← 37 패턴 HTML
.claude/skills/theme-init/SKILL.md                                      ← 새 프리셋 생성기
.claude/skills/theme-init/scripts/init_theme.py                         ← /theme-init 오케스트레이터
.claude/skills/upload-drive/SKILL.md                                    ← Google Slides 업로드
output/                                                                 ← 빌드 결과물 (주제별)
```

</details>
