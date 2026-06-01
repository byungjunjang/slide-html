---
preset: notion
display_name: Notion
generated_by: manual (Phase 2 layout-authoring brief)
schema_version: 1.0
status: confirmed
---

# Notion · DESIGN.md

> Layer 3 산출물. Notion 프리셋의 **편집·시각 의도** SSOT. 토큰·CSS·boilerplate는 자동 산출물이고, 이 문서는 그 위에 얹는 브랜드 어휘다.

---

## 1. Visual theme & atmosphere

친근하고 명료한 **제품 소개 데크**. SaaS 마케팅보다 차분하고, 컨설팅 리포트보다 따뜻하다.

- 베이스는 따뜻한 그레이(`#F7F6F3`) + 화이트, 텍스트는 Notion 시그니처 웜 다크그레이(`#37352F`, 순수 검정 아님).
- 단일 액센트는 **퍼플 `#7C3AED`**. 강조·CTA·키워드에만.
- 아이덴티티 슬라이드(cover/section/closing)는 **네이비 히어로 밴드(`#1F2544`)** + 화이트 타이포 + **브랜드 스펙트럼 닷**(옐로/그린/블루/퍼플/레드)로 "Notion스러움"을 만든다.
- 정보 밀도는 중간. 한 슬라이드 = 한 메시지, 여백을 두려워하지 않되 비우지도 않는다.

---

## 2. Palette & contrast behavior

| Token | Hex | Role |
|---|---|---|
| `--bg` / `--surface` | `#FFFFFF` | page / card |
| `--surface-alt` | `#F7F6F3` | 따뜻한 그룹 배경 · feature tile |
| `--text` | `#37352F` | 본문 (순수 검정 금지) |
| `--text-secondary` | `#787774` | 부연 |
| `--accent` | `#7C3AED` | 단일 퍼플 액센트 — slide당 1~2 events |
| `--accent-soft` | `#EDE9FE` | 액센트 tint · feature-tile-accent |
| `--accent-ink` | `#5B21B6` | accent 위 텍스트 |

- 네이비 밴드(`#1F2544`)는 토큰이 아닌 **리터럴 hex** — 아이덴티티 슬라이드 전용. 위 텍스트는 화이트, eyebrow는 반투명 화이트 칩.
- 스펙트럼 닷 컬러는 리터럴 hex(`#F2C94C #6FCF97 #56CCF2 #BB6BD9 #EB5757`) — cover/section의 브랜드 시그니처에만, 본문 데이터엔 금지.

---

## 3. Typography hierarchy
폰트: **Inter** (한글 fallback Pretendard). 슬라이드 타이틀 `.t-h2`, 본문 `.t-body`, hero `.t-display`. pt 스케일은 `_pptx-slide.css` 캔버스 calibration 그대로.

## 4. Spacing & density
8px grid. 카드 padding 20pt 22pt(`.feature-tile`), grid gap 18pt. bottom 안전 마진 ≥ 44pt.

---

## 5. Visual vocabulary — compose, don't copy

> 아이덴티티 슬라이드는 stock 골격을 따르지 말고 아래 시그니처로 **재작곡**한다 (Phase 2 layout-authoring). 데이터 슬라이드는 token tone 유지.

### 시그니처 장치
1. **네이비 히어로 밴드** — cover/section 상단 풀폭 밴드(`#1F2544`), 위 화이트 워드마크 + 반투명 칩 eyebrow.
2. **브랜드 스펙트럼 닷** — 밴드 아래/표지에 5색 닷 row (`.dot-row` + `.spectrum-dot`).
3. **파스텔 피처보드** — `.feature-tile`(surface-alt) 그리드 + 하나만 `.feature-tile-accent`(퍼플 tint) hero + **옐로볼드 배너**(`.banner-strip` `#F2C94C`) 헤더.
4. **퍼플 CTA 버튼** — closing의 `.btn-cta` (accent fill + 화이트 라벨).

### 패밀리별 재작곡 가이드 (anchor → Notion 구성)
| family | slides | Notion 구성 |
|---|---|---|
| cover | 01·23·25 | 네이비 밴드 + 화이트 워드마크 + 스펙트럼 닷 + 밴드 아래 서브타이틀(웜 그레이). 25는 세로 스택 미니멀. |
| section | 09·07 | 네이비 밴드 축소 + 큰 챕터 `.t-display` + 퍼플 키워드 1개 + `.rule-accent`. |
| closing | 21·22·08 | 21(라이트): 퍼플 CTA 버튼 + 연락 메타. 22/08(다크): 네이비 풀블리드 + 화이트 메시지 + 스펙트럼 닷. |
| feature-board | 02·26·12 | 옐로볼드 배너 + `.feature-tile` 그리드 + accent tile 1개. 하단 여백 채우기(2행 또는 인트로 컬럼). |
| hero-impact | 16·18 | 단일 mega number/quote, 퍼플 키워드 1개, 미니멀 chrome. |
| summary·agenda | 17·10 | number-circle 리스트 + 현재/핵심 항목만 `.card-accent`. |

---

## 6. Chrome 의무 (본문 슬라이드 공통)

데이터 슬라이드(token tone)는 표준 chrome 유지:
- Top eyebrow `.t-cap-up` (좌, top 42pt) + page counter `.t-cap c-tertiary` (우)
- `.t-h2` 타이틀 + 퍼플 키워드 1개 인라인 `.c-accent`
- `.rule` divider, 옵션 `.gm-band` takeaway

아이덴티티 슬라이드(cover/section/closing/hero)는 chrome 간소화/제거 — 네이비 밴드가 chrome 역할. 단 라이트/다크 톤은 패밀리 규칙대로.

---

## 7. Title / body / end page flow
cover(01) → agenda(10) → section(09) → feature/data 본문 → summary(17) → closing(21, 라이트 기본 / 22 다크 임팩트).

## 8. Chart / table treatment
표는 `.tbl-*` div-grid, 헤더 accent-soft, 하이라이트 컬럼 1개. takeaway 한 줄 의무.

## 9. Icon system
tabler-outline. 색은 `c-text`/`c-accent`. 외부 svg + prebuildSvg. 이모지 금지.

## 10. Anti-patterns
- ❌ 스펙트럼 닷/네이비 밴드를 데이터 슬라이드에 사용 (아이덴티티 전용)
- ❌ 퍼플 외 멀티 액센트, 그라디언트
- ❌ feature-board 하단 절반 비우기 (밀도 부족)
- ❌ 1·2인칭 "여러분"

---

## Provenance
- `theme.json` v1 · `_pptx-slide.css` (notion tokens + brand helpers) · `pptx-boilerplate/*.html`
