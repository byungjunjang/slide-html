# chart-rhetoric.md

차트·표 슬라이드의 `chart_strategy` 필드에 박는 9개 어휘. 출처는 mckinsey-pptx의 차트 함수 분류를 **시각 구현 빼고 수사적 역할만** 추출한 것.

**시각 구현은 각 preset의 DESIGN.md `Chart / table treatment` 섹션이 책임진다.** 이 어휘는 "어떤 수사를 하려는가"만 박는다.

## 9 chart_strategy

| 어휘 | 의미 | 추천 데이터 케이스 | mckinsey-pptx 대응 (참고) |
|---|---|---|---|
| `growth-trend` | 단일 metric의 시간 흐름 | YoY 매출, 사용자 증가 | column_simple_growth |
| `forecast` | 과거 실측 + 미래 예측, 시각 구분 | 분기 예측, target line | column_historic_forecast |
| `structural-break` | 성장률 단절·변곡점 강조 | 정책 전후, 위기 전후 | column_split_growth |
| `focus-comparison` | 카테고리 비교 + 한 항목 하이라이트 | 경쟁사 비교, 부서별 KPI | column_comparison |
| `distribution` | 산점·버블, 두 축 분포 | 시장 매핑, 고객 segment | bubble_chart |
| `quadrant` | 2×2 분면 | BCG, 우선순위 매트릭스 | growth_share |
| `priority-matrix` | 3×3 매트릭스 (시급성 × 중요도 등) | 의사결정 grid | prioritization_matrix |
| `split-segment` | stacked / grouped 구성 비율 | 매출 구성, 비용 분해 | stacked_column_chart |
| `funnel` | 깔때기형 단계 축소 | TAM/SAM/SOM, conversion funnel | funnel |

## custom fallback

위 9개로 표현 안 되는 경우 `chart_strategy: "custom"` 허용. 단 그때는:

- `chart_takeaway` 필수 (R2)
- `content_blocks[].content_instruction`에 **자유 description 필수** — 어떤 시각을 의도하는지 한 문단

custom을 남발하지 말 것. 9개 중 하나로 표현 가능하면 그쪽을 쓴다 — preset의 시각 구현이 9개 어휘에 이미 매핑돼 있으므로.

---

## R2 — takeaway 일체화 (강제)

`chart_strategy`가 비어있지 않은 모든 슬라이드는 `chart_takeaway`도 비어있지 않아야 한다. 표(table)도 동일: `table_strategy` ↔ `table_takeaway`.

차트만 두고 결론 없는 슬라이드는 `validate_plan.py` exit 1로 빌드 거부.

```json
// OK
{
  "chart_strategy": "forecast",
  "chart_takeaway": "Q4 예측치는 이미 신규 채널이 자기잠식 단계 진입을 시사."
}

// NG — R2 위반
{
  "chart_strategy": "forecast",
  "chart_takeaway": ""
}
```

---

## jangpm preset 매핑 (빠른 참조)

DESIGN.md `Chart / table treatment` 섹션에서 가져온 가용성 표:

| chart_strategy | jangpm 구현 | 상태 |
|---|---|---|
| `growth-trend` | forecast-table (20) 또는 PptxGenJS bar chart 합성 | available |
| `forecast` | forecast-table (20) | available |
| `structural-break` | matrix-trends (27) 좌우 대비 | available (변형) |
| `focus-comparison` | comparison (14) + table-detailed (19) hi-column | available |
| `distribution` | — | **requires custom** |
| `quadrant` | paired-concept (30) 응용 또는 custom div grid | available (custom 권장) |
| `priority-matrix` | matrix-trends (27) 응용 | available |
| `split-segment` | — (PptxGenJS stacked column) | **requires custom** |
| `funnel` | — | **requires custom** |

다른 preset 추가 시 각 preset의 DESIGN.md에 동일 형식의 매핑 표를 둔다.
