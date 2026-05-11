# deck-types.md

slide-plan의 1단계(deck_type 감지) + 2단계(narrative arc 선택)에 사용하는 8개 deck_type. 각 arc는 **시작점 휴리스틱**이지 강제가 아님 — brief에 맞게 자유 적응.

## 8 deck_type

| deck_type | 정의 | 적용 시나리오 예시 |
|---|---|---|
| `consulting` | 사업 리뷰·전략 보고·경영진 보고 | 분기 보드 데크, M&A 권고, 시장 진입 전략 |
| `educational` | 강의·워크숍·트레이닝 | 사내 교육, 부트캠프 강의, 신입 온보딩 자료 |
| `report` | 분석 리포트·research summary | 시장 조사 결과, 사용자 리서치, 분기 데이터 보고 |
| `sales` | 제품 소개·고객 제안서·pitching | 고객 미팅 데크, 영업 first-call, 데모 보조자료 |
| `internal_update` | OKR 리뷰·진행 상황·팀 공유 | 위클리 리뷰, 분기 OKR 리캡, 프로젝트 weekly |
| `proposal` | RFP 응답·사업 제안 | 입찰 응답, SOW 부속자료, 파트너십 제안 |
| `keynote` | 컨퍼런스 발표·신제품 발표 | 컨퍼런스 키노트, 신제품 announce, 비전 토크 |
| `unknown` | 분류 자신없음 / 사용자에게 묻기 | brief가 모호하거나 hybrid일 때 |

`unknown`으로 두면 강제 narrative arc가 적용되지 않는다. 슬라이드별 plan은 사용자 brief에서 직접 추출.

---

## narrative arc — deck_type별 시퀀스

### consulting

```
cover → bottom_line(insight) → executive_summary →
analysis(evidence) × 1~3 → implication(comparison) × 0~2 →
recommendation(solution) → roadmap → cta(closing)
```

특징: bottom_line을 표지 직후 두는 "answer-first" 구조. evidence는 결론을 뒷받침할 만큼만.

### educational

```
cover → context(why_now) → agenda →
concept(insight) × 1~2 → example(evidence) × 1~3 →
exercise × 0~2 → recap(summary) → qna/closing
```

특징: agenda를 명시. concept → example → exercise 순으로 학습 곡선 따라가기.

### report

```
cover → executive_summary → context →
findings(evidence) × 2~5 → analysis(insight) × 1~2 →
implications(comparison) × 0~2 → conclusion → appendix(선택)
```

특징: findings를 두텁게. consulting은 결론 우선이지만 report는 발견 사실 자체가 자산.

### sales

```
cover → problem(context) → opportunity(insight) →
solution × 1~2 → proof(evidence) × 1~3 → comparison(vs alternative) →
roadmap/pricing → cta
```

특징: 고객의 problem에서 시작. comparison은 경쟁사 대비 vs 또는 status quo 대비 vs.

### internal_update

```
cover → status_summary → progress(evidence) × 2~4 →
blockers(comparison) → next_steps(roadmap) → asks(cta)
```

특징: 진행 상황 + 블로커 + 다음 단계의 균형. asks를 분명히 끝에.

### proposal

```
cover → problem(context) → solution × 1~2 → proof × 1~2 →
team → roadmap → pricing → cta
```

(brief에서 추출 후 적응. 강제 arc 아님.)

### keynote

```
cover → hook → vision → proof(demo) × 1~3 → availability → cta
```

(brief에서 추출 후 적응. 강제 arc 아님. hook은 강한 첫 메시지.)

### unknown

강제 arc 없음. 사용자 brief를 그대로 따라 슬라이드 시퀀스 작성. 가능하면 한 번 더 사용자에게 확인.

---

## arc 적응 규칙

- 각 arc의 **× N~M**은 가이드라인. brief의 evidence 풀 크기·청중 시간 제약에 따라 줄이거나 늘린다.
- arc 안의 단계는 **건너뛸 수 있음** (예: educational에서 exercise가 없는 데크).
- 단계 **순서는 가능한 보존**. 결론을 먼저 두는 변형(answer-first 패턴 변형)은 consulting에서만.
- arc 내 동일 슬라이드 role을 연속 3장 이상 두지 않는다 (R4 lazy 반복 금지). 같은 evidence 단계 3장 = layout_family를 바꾸어 다양화.
