---
preset: jangpm
last_updated: 2026-04-24
source: Jangpm Slide Design System 정본 패키지 (이 폴더 자체)
canonical: 이 파일은 huashu-design 포맷의 랩퍼. 상세는 이 폴더의 README.md + reference/*.md 참조
---

# Jangpm · huashu-design Brand Spec

> **핵심**: 한국어 강의 슬라이드. 무채색 베이스 + 단일 인디고 악센트 `#4633E3`. 1280×720 고정. 리포트/에비던스 퍼스트, SaaS 대시보드 금지.

## 🎯 핵심 자산 (이 폴더 내부)

| 자산 | 경로 (이 폴더 기준) | 용도 |
|---|---|---|
| **토큰 CSS** | `colors_and_type.css` | `:root` 토큰 + `@font-face` (폰트는 `fonts/` 상대경로 self-contained) |
| **토큰 HTML 미리보기** | `colors_and_type.html` | 색/타입 토큰 브라우저에서 눈으로 확인 |
| **슬라이드 레이아웃** | `slides/*.html` (30개) + `slides/_slide.css` | 새 슬라이드 = 여기서 가까운 패턴 복사 → 내용만 교체 |
| **시각 갤러리** | `preview/*.html` (20개) | 컴포넌트/타입/색/스페이싱을 페이지로 렌더한 레퍼런스. 설계 중 계속 참조 |
| **UI 키트** | `ui_kits/slide-deck/` | 레브럴 인터랙티브 인덱스 |
| **장피엠 캐릭터** | `assets/jangpm-character.png` | 1024×1024 투명 PNG. 유일한 브랜드 일러스트 |
| **Pretendard 폰트** | `fonts/` (9 OTF + Variable TTF) | 폴더째 이동해도 안 깨짐 (CSS가 상대경로) |
| **원본 레퍼런스** | `uploads/reference 2.pptx` | 디자인 타겟이 된 한국 비즈니스 리포트 데크 |

## 📖 이 프리셋의 상세 규칙 (reference/ 폴더)

| 파일 | 내용 |
|---|---|
| `reference/anti-slop.md` | **18가지 금지 패턴** — 슬라이드 만들 때 반드시 통과 체크리스트 |
| `reference/design-system.md` | 토큰/스케일/컴포넌트 전체 스펙 |
| `reference/patterns.md` | **24가지 슬라이드 패턴** 상세 분류 |
| `reference/skeleton.md` | HTML 뼈대 템플릿 (복붙용) |
| `reference/libraries.md` | Reveal.js / Chart.js / Mermaid / Lucide 아이콘 설정 |
| `reference/visual-assets.md` | 일러스트 생성 프롬프트 (nanobanana2 등) |
| `reference/export.md` | PPTX / PDF / Drive 내보내기 가이드 |
| `reference/reference-2-text.txt` | `reference 2.pptx` 텍스트 추출 |

**작업 전에 읽어야 할 순서**: `anti-slop.md` → `design-system.md` → `patterns.md` → `skeleton.md`

## 🎨 핵심 규칙 요약 (자세한 건 reference/ 참조)

### 색 (Jangpm Lock)
- Background `#FAFAF9` 웜 오프화이트 · 순수 `#FFFFFF` 금지
- Text `#1A1A1A` · 순수 `#000` 금지
- **악센트 `#4633E3` 인디고 1종만**. 그라디언트 / 다색 / 글로우 전부 금지
- **페이지당 악센트 이벤트 최대 1–2개** (핵심 메트릭 1개 + 하이라이트 컬럼 1개 정도)
- 차트: 단일 악센트 + opacity 사다리 `0.85 / 0.6 / 0.4 / 0.25`. 무지개 금지
- Semantic 색 (positive `#059669` / negative `#E11D48` / warning `#D97706`) 은 **데이터 맥락에만**, 장식 금지

### 타이포 (Pretendard 9 weights)
- Display 800 / Headline 700 / Title 600 / Body 400
- 큰 글씨 트래킹 타이트: Display `-0.03em`, Headline `-0.02em`
- 시멘틱 클래스만 사용: `.display / .headline / .title / .body / .caption`. 임의 `font-size` 금지
- **한글 본문 + 영문 토큰** 혼용. 영문 고유명사는 Title Case, 일반 기술용어는 lowercase (`chart`, `metric`)

### 카피 톤 (한국어 강의 리포트)
- **언어**: 한국어 주, 영문 약어 유지 (`LTV`, `ROI`, `KPI`, `D2C`)
- **어조**: 선언형, 분석형, 3인칭 기관체. "당신/저는" 직접 지칭 금지. `~입니다 / ~합니다 / ~해야 합니다`
- **타이틀**: 명사구, 마침표 없음
  - ✅ `2030년 한눈에 보기` / `시장 및 트렌드 전망`
  - ❌ `2030년을 한눈에 살펴보겠습니다.`
- **본문**: 존댓말 완성형 문장. 블록당 최대 4줄
- **이모지**: **절대 금지**. 아이콘은 SVG line-art만
- **숫자**: 단위 + 선택적 증감치 포함. `58억 원 (+21% vs 전년)` / `재고 회전율 5.5회`
- **Governing Message (`.gm`)**: 모든 콘텐츠 슬라이드 하단에 에디토리얼 요약 1줄. "so-what" 문장형

### 레이아웃
- 캔버스 1280×720 고정. 오버플로 금지
- 구조: 상단 `.headline` + 중단 `.slide-body` + 하단 `.gm` (absolute 하단 고정)
- 페이지 패딩: 좌우 `3.5rem` (`--space-14`), 하단 `4rem` (`--space-16`, GM 영역)
- **CSS Grid `gap`** 으로만 간격. margin 핵 금지
- 카드는 보조 도구. 텍스트 블록 + 룰 라인이 리포트 스타일의 본체
- 페이지당 최대 **4–5 불릿 / 3–4 카드**. 밀도 강박 금지
- **텍스트 온리 슬라이드 금지** — 항상 비주얼 요소 (아이콘/카드/차트/테이블)와 페어

### 아이콘 (Lucide-style inline SVG)
- `24×24` viewBox, `stroke="currentColor"`, `stroke-width="2"`, round linecap/linejoin
- 사이즈: `.icon` 20px · `.icon-lg` 32px · `.icon-xl` 48px
- **맨 아이콘만**: 원형 래퍼 금지, 컬러 배경 배지 금지, 필드 배지 금지
- CDN 금지, 인라인 붙여넣기. 경로는 `reference/libraries.md`에 정리
- 이모지 / 유니코드 `→ ✓ ★` 대체 금지

### 보더 / 섀도우 / 라운드
- 보더: 항상 `1px solid var(--border)` (`#E5E7EB`). **장식 보더 금지** (좌측 색 스트립 카드 금지)
- 섀도우: 데이터/KPI 강조 카드에만. 3단계 (`--shadow-sm/md/lg`). 기본 카드는 섀도우 없음
- 라운드: 카드 `12px` (`--radius-lg`) / 칩 `4–6px` / 필 완전 라운드

### 모션
- **콘텐츠에는 모션 없음**. Reveal.js `transition: 'none'`
- hover 스케일 / translateY / pulse / float / glow 전부 금지
- `Chart.defaults.animation = false` 전역

### 배경 / 투명도
- 배경은 **웜 오프화이트 솔리드만**. 그라디언트 / 오브 / 텍스처 금지
- 타이틀/섹션 디바이더는 subtle dot pattern (`--bg-dots`) 선택적 허용
- 콘텐츠 슬라이드에 풀블리드 이미지 금지
- blur / backdrop-filter 금지. opacity는 1. 예외는 `.agenda-item-past { opacity: 0.5 }` 하나

## 🚫 금지 패턴 요약 (자세한 건 reference/anti-slop.md)
- 보라/핑크 그라디언트 표지, gradient text, gradient border
- 이모지 아이콘, 유니코드 글리프 아이콘
- 원형 래퍼 안의 컬러 아이콘
- 좌측 accent border 스트립 카드
- SVG로 사람 얼굴 그리기 (캐릭터는 `assets/jangpm-character.png` 사용)
- Inter 디스플레이 폰트
- hover scale / glow / pulse / float
- 풀블리드 배경 이미지 / 오브
- 순수 `#000` 텍스트 / 순수 `#FFF` 텍스트
- 페이지당 악센트 2개 초과
- text-align: justify
- SaaS 대시보드 룩 (현란한 게이지, 다색 차트, 네온 보더)

## 기질 키워드
editorial · minimal · Korean-lecture · monochrome-first · report-style · trustworthy · dense-but-breathing · evidence-first

## 사용 체크리스트 (huashu-design이 이 프리셋 썼을 때)

1. 프로젝트 폴더에 프리셋 링크/복사
   ```bash
   # 심볼릭 링크 (권장: 프리셋 업데이트가 즉시 반영)
   ln -s ../../../.claude/skills/huashu-design/assets/design-systems/jangpm <project>/design-system
   # 또는 복사 (프로젝트별 수정이 필요하면)
   cp -r <skill>/assets/design-systems/jangpm <project>/design-system
   ```
2. `<project>/brand-spec.md` 로 이 파일 복사
3. HTML `<head>`에 `<link rel="stylesheet" href="design-system/colors_and_type.css">` + 슬라이드면 `<link rel="stylesheet" href="design-system/slides/_slide.css">`
4. 새 슬라이드 = `design-system/slides/` 에서 가까운 패턴 복사 → 텍스트만 교체
5. 작업 중 `design-system/preview/*.html` 을 브라우저에 열어 토큰/컴포넌트 시각 체크
6. 완료 전 `reference/anti-slop.md` 18개 체크리스트 한 번 훑기
7. 그레이스케일로 스크린샷 떠서 읽히는지 확인 (악센트 없이도 hierarchy가 살아야 함)

## huashu-design §1.a 브랜드 자산 프로토콜과의 관계
- 이 프리셋이 있을 땐 **§1.a 5단계 스킵**. 이 프리셋이 logo/폰트/색/캐릭터 전부 대체
- 특정 기업 브랜드를 Jangpm 위에 얹어야 하는 경우에만 §1.a 수행: accent 변수 등 일부만 덮어씀
- Logo는 Jangpm에 없으므로 (캐릭터가 그 역할 대체), 기업 브랜드 작업 시 logo는 §1.a로 별도 수집
