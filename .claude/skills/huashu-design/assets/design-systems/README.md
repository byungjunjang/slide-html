---
name: huashu-design 디자인 시스템 프리셋
last_updated: 2026-04-24
scope: project (Labs/huashu-design/.claude/skills/huashu-design)
---

# Design System Presets

huashu-design는 프로젝트별 `brand-spec.md` + CSS 토큰을 기반으로 동작한다 (SKILL.md §1.a). 이 폴더는 자주 쓰는 디자인 시스템을 **정본 프리셋**으로 저장해 매번 처음부터 만들지 않게 한다.

## 사용 규칙

사용자가 "**<preset-name>으로 해줘**" / "**<preset-name> 디자인 시스템 적용**" 이라고 하면:

1. `assets/design-systems/<preset>/brand-spec.md` 를 먼저 읽어 해당 프리셋의 토큰/규칙/금지/카피 톤 학습
2. 프리셋에 `reference/` 폴더가 있으면 그 안의 md들도 (특히 `anti-slop.md`, `patterns.md`, `skeleton.md`) 읽기
3. 프로젝트 폴더에 프리셋을 심볼릭 링크 또는 복사:
   ```bash
   # 권장: 심볼릭 링크 (프리셋 수정이 즉시 반영됨)
   ln -s <skill-path>/assets/design-systems/<preset> <project>/design-system

   # 프로젝트별 커스텀이 필요하면: 복사
   cp -r <skill-path>/assets/design-systems/<preset> <project>/design-system
   ```
4. `<project>/brand-spec.md` = 프리셋의 brand-spec.md 복사
5. HTML `<head>`에 프리셋 CSS 링크:
   ```html
   <link rel="stylesheet" href="design-system/colors_and_type.css">
   <link rel="stylesheet" href="design-system/slides/_slide.css"> <!-- 슬라이드일 때 -->
   ```
6. 새 슬라이드/페이지 = `design-system/slides/` 또는 유사 폴더에서 가까운 패턴 복사 → 콘텐츠만 교체 (처음부터 새로 그리지 말 것)
7. SKILL.md §1.a의 **브랜드 자산 수집 5단계는 스킵** — 프리셋이 그 역할을 이미 수행. 단, 특정 기업 브랜드를 프리셋 위에 얹어야 하면 5단계를 실행해 `--accent` 등 일부 토큰만 덮어씀

## 여러 프리셋 공존

- 각 프리셋은 `assets/design-systems/<이름>/` 아래 독립 폴더로 존재
- 프로젝트 하나당 프리셋 하나 (섞지 않는다)
- 유저가 프리셋을 지정하지 않으면 기본 프리셋(`jangpm`)을 사용하고, 본인 브랜드에 맞춰 새 프리셋을 만들어 교체할 수 있다 (`acme-warm`이 그 예시)

## 프리셋 구조 규약

각 프리셋은 최소 아래 구조를 가진다:

```
<preset-name>/
├── brand-spec.md              # [필수] huashu-design 포맷의 스펙 (tokens + rules + don'ts)
├── colors_and_type.css        # [필수] :root 토큰 정의 + @font-face
├── _slide.css 또는 slides/    # [슬라이드 프리셋일 때] 캔버스 + 공통 컴포넌트 + 레이아웃
├── preview/                   # [권장] 토큰/컴포넌트 시각 갤러리 (브라우저에서 확인용)
├── reference/                 # [권장] anti-slop / patterns / skeleton 등 상세 규칙 md
├── fonts/                     # [선택] OTF/TTF/WOFF2
├── assets/                    # [선택] 브랜드 이미지 (캐릭터/일러스트)
└── ui_kits/                   # [선택] 상호작용 키트
```

## 현재 설치된 프리셋

| 프리셋 | 용도 | 캔버스 | 악센트 | 폰트 | 레이아웃 | 갤러리 | 상세 규칙 md |
|---|---|---|---|---|---|---|---|
| **jangpm** | 한국어 강의/비즈니스 리포트 데크 | 1280×720 | `#4633E3` 인디고 | Pretendard (9 OTF) | 30 slides | 20 HTML | 8개 (anti-slop/patterns/skeleton 포함) |

---

## 기본 huashu-design 워크플로우와의 관계

huashu-design SKILL.md의 §1.a 브랜드 자산 프로토콜은 "기업 브랜드용 스펙 수집" 용도로 쓰였다. 프리셋 시스템은 그 결과물을 재사용 가능하게 저장한 것:

- **프리셋 있는 경우** → 프리셋 사용, §1.a 스킵
- **특정 기업 브랜드 작업** → §1.a 5단계 실행, 필요하면 결과를 이 폴더로 프리셋화
- **혼합** (예: jangpm 베이스 + 특정 기업 accent) → 프리셋 위에 brand-spec 얹고 `--accent` 등 일부 토큰만 덮어씀

결과물 형태는 동일: `<project>/brand-spec.md` + CSS 변수 + 모든 HTML이 `var(--*)`만 참조.
