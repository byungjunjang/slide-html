# slide-plan-schema.md

`slide_plan.json`의 핵심 필드 + 변형 자유 영역. **스키마 통일은 안 한다** — 각 preset의 layout_family 어휘가 자유로워야 하므로. 다음 표의 "공통" 필드만 고정, 나머지는 자유.

## 핵심 (공통, 고정)

| 경로 | 타입 | 필수 | 의미 |
|---|---|---|---|
| `deck_meta.working_title` | string | ✓ | 데크 작업 제목 |
| `deck_meta.deck_goal` | string | ✓ | 한 줄 목적 |
| `deck_meta.deck_type` | enum (8종) | ✓ | `consulting` / `educational` / `report` / `sales` / `internal_update` / `proposal` / `keynote` / `unknown` |
| `deck_meta.target_audience` | string | ✓ | 청중 |
| `deck_meta.tone` | string | | 톤 (옵션) |
| `deck_meta.target_length.slides` | int | ✓ | 목표 슬라이드 수 (R3) |
| `deck_meta.target_length.reasoning` | string | | 근거 |
| `design_dependency.preset_name` | string | ✓ | jangpm / acme-warm / ... |
| `design_dependency.design_md_path` | string | ✓ | DESIGN.md 절대/상대 경로 |
| `design_dependency.allowed_layout_families` | string[] | ✓ | DESIGN.md에서 추출한 family 어휘 (jangpm이면 27종) |
| `design_dependency.consistency_notes` | string[] | | preset 특이사항 |
| `story_arc.narrative_shape` | string | | deck_type별 arc (deck-types.md 참조) |
| `story_arc.why_this_order_is_persuasive` | string | | 한 줄 |
| `content_inventory[]` | object[] | ✓ | 각 source 분류 (R5) |
| `content_inventory[].source_id` | string | ✓ | 식별자 |
| `content_inventory[].source_type` | enum | ✓ | `file` / `prompt` / `inference` |
| `content_inventory[].summary` | string | ✓ | 한 줄 |
| `content_inventory[].relevance` | enum | | `high` / `medium` / `low` |
| `content_inventory[].usable_for` | string[] | | 어떤 슬라이드/role에 쓰이는지 |
| `slides[]` | object[] | ✓ | 슬라이드 배열 |
| `slides[].slide_number` | int | ✓ | 1부터 |
| `slides[].slide_role` | string | ✓ | slide-roles.md enum |
| `slides[].page_family` | enum | ✓ | `title` / `body` / `end` / `appendix` |
| `slides[].working_title` | string | ✓ | 슬라이드 작업 제목 |
| `slides[].core_message` | string | ✓ | **R1** — 단일 주장 |
| `slides[].audience_takeaway` | string | ✓ | **R1** — 청중이 가져갈 한 줄 |
| `slides[].why_here` | string | ✓ | **R1** — 이 위치인 이유 |
| `slides[].recommended_layout_family` | string | ✓ | **R1** — DESIGN.md 어휘 (preset별) |
| `slides[].content_blocks[]` | object[] | ✓ | 슬롯 단위 |
| `slides[].content_blocks[].block_type` | string | ✓ | `title` / `subtitle` / `bullets` / `chart` / `table` / `callout` / `quote` / `metric_cards` / `icon_group` / `infographic` / `diagram_flow` / `footer_note` (확장 가능) |
| `slides[].content_blocks[].purpose` | string | ✓ | 이 슬롯의 의도 |
| `slides[].content_blocks[].content_instruction` | string | ✓ | 채울 내용 지침 |
| `slides[].chart_strategy` | string | (조건부) | chart 슬라이드면 필수 — chart-rhetoric.md 9 어휘 또는 `custom` |
| `slides[].chart_takeaway` | string | (조건부) | **R2** — chart_strategy 있으면 비울 수 없음 |
| `slides[].table_strategy` | string | (조건부) | 동일 |
| `slides[].table_takeaway` | string | (조건부) | **R2** |
| `slides[].evidence_sources[]` | string[] | ✓ | **R5** — content_inventory[].source_id 참조 또는 `inference` |
| `slides[].content_constraints` | object | | must/must_not/evidence |
| `slides[].priority` | enum | | `must` / `should` / `could` |
| `ordering_notes.split_topics` | string[] | | 한 슬라이드를 둘로 쪼갠 흔적 |
| `ordering_notes.merged_topics` | string[] | | 두 토픽을 합친 흔적 |
| `ordering_notes.deferred_topics` | string[] | | 다음 데크로 미룬 항목 |
| `ordering_notes.appendix_candidates` | string[] | | 본문 빠지고 부록 후보 |

## 변형 자유 영역

- `recommended_layout_family` 값 — preset마다 자유 (jangpm 27종, acme-warm은 다를 수 있음)
- `slide_role` — 공통 8개 + deck_type별 추가 + 자유 확장 가능
- `content_blocks[].block_type` — 위 12종 + 자유 추가
- `chart_strategy` — 9 어휘 + `custom` fallback

위는 의도된 자유. 통일하지 않아 각 preset/도메인 특성을 살린다.

---

## R1~R5 자동 검증 (validate_plan.py)

```bash
python3 .claude/skills/slide-plan/scripts/validate_plan.py <plan-path>
```

| 규율 | 검사 | 위반 시 |
|---|---|---|
| R1 | 슬라이드별 4 필드 채움 | exit 0 + stderr lint |
| R2 | chart/table strategy ↔ takeaway 일체화 | **exit 1 (block)** |
| R3 | slides 길이 0 또는 >20 | exit 0 + stderr lint |
| R4 | 동일 layout_family 연속 3장 | exit 0 + stderr lint |
| R5 | evidence_sources 빈 값 | **exit 1 (block)** |

---

## 최소 예시

```json
{
  "deck_meta": {
    "working_title": "Q3 보드 리뷰",
    "deck_goal": "신규 채널 성장의 지속가능성에 대한 의사결정 요청",
    "deck_type": "consulting",
    "target_audience": "이사회",
    "tone": "선언형, 분석적",
    "target_length": { "slides": 10, "reasoning": "이사회 30분 + Q&A" }
  },
  "design_dependency": {
    "preset_name": "jangpm",
    "design_md_path": ".claude/skills/slide/assets/design-systems/jangpm/DESIGN.md",
    "allowed_layout_families": ["cover","kpi-grid","summary","forecast-table","matrix-trends","comparison","four-point","process","closing-big","table-detailed"],
    "consistency_notes": ["악센트 1~2 events/슬라이드"]
  },
  "story_arc": {
    "narrative_shape": "consulting (answer-first)",
    "why_this_order_is_persuasive": "결론 먼저 박고 evidence로 정당화"
  },
  "content_inventory": [
    {
      "source_id": "q3_revenue_xlsx",
      "source_type": "file",
      "summary": "Q1~Q3 채널별 매출",
      "relevance": "high",
      "usable_for": ["slide_2", "slide_4"]
    }
  ],
  "slides": [
    {
      "slide_number": 1,
      "slide_role": "cover",
      "page_family": "title",
      "working_title": "Q3 보드 리뷰",
      "core_message": "Q3 보드 리뷰",
      "audience_takeaway": "오늘의 의사결정 영역 3가지",
      "why_here": "데크 진입점",
      "recommended_layout_family": "cover",
      "content_blocks": [
        { "block_type": "title", "purpose": "데크 제목", "content_instruction": "Q3 보드 리뷰 — 신규 채널의 지속가능성" }
      ],
      "evidence_sources": ["inference"],
      "priority": "must"
    }
  ],
  "ordering_notes": {
    "split_topics": [],
    "merged_topics": [],
    "deferred_topics": [],
    "appendix_candidates": []
  }
}
```

전체 골든 예시: `examples/consulting-deck-plan.json` (10장).
