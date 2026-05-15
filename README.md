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

**예시 한 줄:**
> "사내 AI 도구 도입 효과 슬라이드 12장 만들어줘. KPI 위주로."

↓ 1~3분 후 ↓

→ `output/사내-AI-도입-pptx/사내-AI-도입.pptx` 생성. 표지 → 컨텍스트 → KPI 대시보드 →
사례 카드 → 로드맵 → 클로징 12장이 Jangpm 디자인 시스템(모노크롬 + accent `#4633E3`)으로 통일되어 들어 있고, 각 텍스트는 PowerPoint에서 그대로 편집 가능합니다.

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

Node 18 이상이 필요합니다.

```bash
npm install                          # playwright, pptxgenjs, sharp
npx playwright install chromium      # html2pptx의 브라우저 캡처용
```

> 루트의 `package.json` / `package-lock.json`은 로컬 사용용이고, `.claude/skills/slide/package.json`은 claude.ai에 zip으로 올렸을 때 self-contained로 동작하도록 동일한 의존성을 따로 들고 있습니다. 의존성 버전을 바꿀 때는 **두 파일을 같이 갱신**하세요 (드리프트 시 claude.ai 번들이 어긋남).

### 4단계. (선택) AI 이미지 생성 — `/codex-image`

표지·인포그래픽·세로 카드에 AI 이미지가 필요할 때 `/slide` 2.5단계가 자동으로 호출하는 기본 경로입니다.
**API 키 발급·관리 없이 Codex CLI OAuth(ChatGPT 로그인)만으로** `gpt-image-2`를 호출하고, 슬라이드 빌더가 미리 정한 슬롯명 그대로 (`images/<slot>.png`) 파일을 떨굽니다.

**최초 1회 준비 (한 번만 하면 됩니다):**

```bash
npm install -g @openai/codex      # Codex CLI 설치
codex login                        # ChatGPT 계정으로 OAuth 인증 (브라우저 자동 오픈)
codex login status                 # "Logged in using ChatGPT" 표시되면 끝
```

`codex login`은 OAuth 토큰을 `~/.codex/auth.json`에 한 번 저장하고, 이후 모든 이미지 호출은 그 토큰을 자동 재사용합니다.
**`sk-*` 형식 API 키는 어디에도 저장되지 않습니다.** Codex OAuth 토큰은 ChatGPT 세션 토큰이라 OpenAI REST API로 직접 던지면 401이 떨어지지만, `codex exec`의 내부 브릿지가 OAuth → 내장 `image_gen` 도구 → `gpt-image-2` 경로로 라우팅해줍니다.

`/slide` 외에 직접 호출하고 싶을 때는 Claude Code 채팅창에 그대로:

```
/codex-image --size 1536x1024 --out output/my-deck-pptx/images --filename hero-cover \
  "minimal flat line-art illustration of a globe, single accent color, neutral palette"
```

| 증상 | 해결 |
|---|---|
| `auth expired` / 401 | `codex login` 재실행 (토큰 갱신) |
| `NOT_FOUND` | `npm install -g @openai/codex` |
| 트러스트 오류 | 스킬이 `--skip-git-repo-check` 사용 — 자세한 내용은 `.claude/skills/codex-image/README.md` |
| 생성 파일이 슬롯명과 다름 | `--filename <slot>` 인자 확인. 슬라이드 HTML의 `<img src>` 경로와 정확히 일치해야 함 |
| 16:9 인데 양옆이 좀 잘림 | 정상. `gpt-image-2`는 1536×1024(약 3:2)만 가능 → CSS `object-fit: cover`로 960×540 슬롯에 맞춰 자동 크롭 |

**스킬 위치:** `.claude/skills/codex-image/` (이 저장소에 vendored. 업스트림: [wjb127/codex-image](https://github.com/wjb127/codex-image))
**비용:** ChatGPT Plus/Team/Enterprise 계정의 OpenAI 사용량에 청구 (`1024x1024 high` ≈ $0.04, `1536x1024 high` ≈ $0.06).

**(옵션) API 키 백엔드로 강제 전환:**

별도 API 키로 다른 백엔드(gemini / openai / stability / bfl / ideogram / qwen / zhipu / volcengine / siliconflow / fal / replicate)를 쓰고 싶을 때만:

```bash
# 셸 또는 .env 둘 다 인식 (slide-html은 .env.example 미동봉 — 직접 만들거나 export로 설정)
export IMAGE_BACKEND=gemini  # 또는 openai 등
export GEMINI_API_KEY=...    # 백엔드별 키
```

`IMAGE_BACKEND`가 설정되면 codex-image 대신 외부 멀티 백엔드 스크립트(`image_gen.py` 등 — 사용자가 별도 제공)로 분기합니다. 이 경로에선 진짜 16:9 출력 호출이 가능합니다.

두 경로 모두 비워두면 (Codex CLI 미설치 + `IMAGE_BACKEND` 미설정) 슬라이드는 **이미지 슬롯 없이 텍스트·아이콘·도형**만으로 생성됩니다 (Jangpm 기본 동작에서도 충분히 임팩트 있는 데크가 됩니다).

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
- **`/codex-image` 스킬** — Codex CLI 바이너리가 claude.ai 샌드박스에 설치되지 않음. claude.ai 환경에서 이미지가 필요한 슬롯은 텍스트·아이콘·도형으로 대체되거나, 사용자가 직접 이미지를 슬롯 경로에 떨궈서 사용.

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

## 라이선스 & 기여

- **라이선스:** 본 저장소는 [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)의 **Personal-Use License를 계승**합니다 — 개인·학습·비상업 용도에 한해 자유롭게 사용 가능, **상업적 이용은 금지**. 자세한 조건은 [`LICENSE`](./LICENSE) 참조.
- **버그 리포트·패턴 제안:** GitHub 이슈 환영
- **PR:** 새 프리셋 추가, 보일러플레이트 패턴 추가, 4 constraint 위반 사례 환영
- **테마 추가 제안:** `/theme-init` 사용법은 `.claude/skills/theme-init/SKILL.md` 참조

