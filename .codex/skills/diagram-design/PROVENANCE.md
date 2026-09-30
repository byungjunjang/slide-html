# Provenance — vendored `diagram-design`

Vendored (copied, not symlinked) into this repo so it travels with the slide-html bundle.

- **Upstream:** https://github.com/cathrynlavery/diagram-design
- **Source path:** `skills/diagram-design/` (the inner skill folder)
- **Commit:** `0ab077f2291e9056554d48a90c4ff45f0b7029a5` (2026-05-11)
- **License:** MIT — see `LICENSE` in this folder. Author: Cathryn Lavery.
- **Vendored:** 2026-05-31

## slide-html 통합 패치 (upstream과의 차이)

이 폴더는 upstream 그대로가 아니라, slide-html(editable PPTX 파이프라인)에 맞춰 **추가 라우팅만** 얹었다. 타입 레퍼런스·assets·primitives는 upstream 그대로.

1. **`SKILL.md` §0.5 추가** — slide-html 안에서 실행될 때의 라우팅: 온보딩 게이트 skip, 색·폰트는 프리셋 CSS 변수 참조, 산출물은 "다이어그램만 든 HTML" → PNG `<img>` 슬롯. 단일 진입점으로 `../slide/references/diagram-slots.md`를 가리킴. frontmatter `description`도 통합 맥락 반영.
2. **`references/style-guide.md` 상단 노트** — slide-html 안에서는 이 파일이 SSOT가 아니라 **활성 프리셋**이 SSOT임을 명시.
3. **`SKILL.md` 기본 토큰 정정** — upstream SKILL.md의 온보딩 게이트가 적은 기본값(paper `#faf7f2`·ink `#1c1917`·accent `#b5523a` rust)이 `references/style-guide.md` 실제 기본값과 달라, style-guide 값(`#f5f5f5`·`#2d3142`·`#eb6c36` atomic-tangerine)으로 맞췄다. 같은 이유로 본문의 "Coral"을 `accent`로 바꿨다.

## 바깥쪽(번들) 연결 파일 — 이 폴더 밖

- `../slide/references/diagram-slots.md` — 통합 계약(단계·매핑표·주의)의 단일 출처.
- `../slide/scripts/render-diagram.mjs` — diagram-only HTML → 투명 PNG (Playwright).
- `../slide/SKILL.md` Step 2.6 — `/slide` 파이프라인 진입점.
- `../../../CLAUDE.md` §다이어그램 — 프로젝트 SSOT 요약.

## 업스트림 재동기화 시

upstream을 다시 당길 때는 `skills/diagram-design/`를 이 폴더에 복사한 뒤 위 1~3 패치(§0.5, style-guide 노트, SKILL.md 기본 토큰 정정)와 `LICENSE`·이 파일을 다시 얹는다. 통합 로직 본체는 이 폴더 밖(`../slide/...`)에 있으므로 영향받지 않는다.
