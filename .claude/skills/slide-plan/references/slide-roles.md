# slide-roles.md

`slide_role` 필드에 박는 어휘. **공통 8개**는 모든 deck_type에서 사용 가능 — 무조건 보존. **deck_type별 추가**는 자유 확장 가능 (단 공통 8개를 대체하지는 말 것).

## 공통 8 role

| role | 정의 | 자주 쓰는 layout_family (jangpm 기준) |
|---|---|---|
| `cover` | 데크 진입점·표지 | cover (01, 23, 25) |
| `context` | 배경·왜 지금·why_now | overview-cards, paired-concept |
| `insight` | 단일 주장·결론·so-what | summary, kpi-grid, three-point |
| `evidence` | 데이터·사실 뒷받침 | kpi-grid, forecast-table, table-detailed, matrix-trends |
| `solution` | 권고안·방향성 | three-point, four-point, paired-concept |
| `summary` | 챕터·데크 요약 | summary, four-point |
| `cta` | 의사결정 요청·다음 단계 | closing-light, closing-big, closing-dark |
| `appendix` | 참고·심화 자료 | table-detailed, reference-utility |

## deck_type별 추가 role

각 deck_type은 공통 8개 외에 다음을 추가로 사용할 수 있다.

| deck_type | 추가 role |
|---|---|
| `consulting` | `problem`, `comparison`, `roadmap` |
| `educational` | `concept`, `example`, `exercise`, `recap`, `qna`, `agenda` |
| `report` | `executive_summary`, `findings`, `methodology` |
| `sales` | `problem`, `proof`, `comparison`, `pricing`, `roadmap` |
| `internal_update` | `status_summary`, `progress`, `blockers`, `next_steps`, `asks` |
| `proposal` | `problem`, `comparison`, `pricing`, `team`, `roadmap` |
| `keynote` | `hook`, `vision`, `demo`, `availability` |

### 추가 role 1줄 정의

| role | 정의 |
|---|---|
| `problem` | 고객·시장의 문제·페인 (consulting/sales/proposal) |
| `comparison` | 대안·경쟁·상태 비교 (consulting/sales/proposal) |
| `roadmap` | 시간축 단계·이정표 (consulting/sales/proposal/internal_update) |
| `concept` | 핵심 개념·프레임 (educational) |
| `example` | 실사례·시나리오 (educational) |
| `exercise` | 실습·과제 (educational) |
| `recap` | 학습 요약·복습 (educational) |
| `qna` | Q&A 슬라이드 (educational) |
| `agenda` | 목차 (educational) |
| `executive_summary` | 보고서 도입 요약 (report) |
| `findings` | 발견 사실 (report) |
| `methodology` | 조사 방법·표본 (report) |
| `proof` | 증거·고객 사례·로고 (sales/keynote) |
| `pricing` | 가격·예산 (sales/proposal) |
| `team` | 팀·이력 (proposal) |
| `status_summary` | 현재 상태 요약 (internal_update) |
| `progress` | 진척도 (internal_update) |
| `blockers` | 장애요인 (internal_update) |
| `next_steps` | 다음 작업 (internal_update) |
| `asks` | 요청 사항 (internal_update) |
| `hook` | 첫 강한 메시지 (keynote) |
| `vision` | 큰 그림 (keynote) |
| `demo` | 시연·라이브 (keynote) |
| `availability` | 출시·접근 정보 (keynote) |

---

## 확장 규칙

- 이 enum을 자유롭게 확장 가능. **단 공통 8개는 보존**.
- 새 role을 추가했으면 본 문서에 1줄 정의 + 자주 쓰는 layout_family를 함께 등록.
- deck_type 간 같은 단어가 다른 의미로 쓰이지 않도록 주의 (예: `comparison`은 모든 deck_type에서 "대안 비교"로 일관).
