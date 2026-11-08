# 3회차 내부 심사 3 — UVL 원규칙 첫 수정 재심

- 단위: `uvl_2019_14610`. 판정: **accept**. 기존 지적 **resolved 2 / open 0**, 신규 지적 0.
- 심사자: `/root/uvl_r1_referee_nov09`, 2026-11-08 23:22 UTC / 2026-11-09 08:22 KST. 최초 생산자 `/root/rule14610_checkpoint`, 수정 생산자 `/root/uvl_minor_revision_nov09`, 현재 검증자 `/root/uvl_r1_verifier_nov09`, 이전 검증자 `/root/independent_verifier_probe`, 이전 심사자 `/root/internal_referee_probe`와 다르다. 고정 queue의 이력에 이 심사자 ID가 없다.
- 검토한 불변 커밋: [`d0b66be9a1ac233db7ddb192f6207a7439e6dadc`](https://github.com/parkchanjin0128-pixel/research-agent/tree/d0b66be9a1ac233db7ddb192f6207a7439e6dadc). 범위는 원규칙 1건(C028)의 수정판과 기존 지적 R1·R2다. 정식 3회차 전체, 기술별 cutoff, Gate 및 freeze는 판정 범위 밖이다.

## 지적별 재판정

| ID | 등급 | 위치 | 이전 문제 | 재심 증거 | 통과 기준 | 상태 |
|---|---|---|---|---|---|---|
| R1 | minor | 생산 메모 `직접 관측`의 Savings Clause 행 | 두 시각 표현 중 하나만 기록 | [GPO 공식 PDF 인쇄 14609 / PDF 2쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=2)을 직접 대조했다. 수정판은 `before May 13, 2019`와 `before midnight on May 13, 2019`를 모두 보존한다. 이 규칙으로 달라진 적격성·요건, 종전 무허가 적격성, 실제 주문 및 4월 11일 당시 네 운송 단계 조건도 유지한다. | 두 문구와 적용 조건을 보존하고 마지막 허용 시각과 보편적 차단일을 정하지 않는다. 충족. | **resolved** |
| R2 | minor | 생산 메모 첫 문단과 `접근·후속` | 최초의 검증·심사 대기가 최신 상태로 읽힐 수 있었음 | 최초 생산 기록을 과거로 명시했고 2026-11-09 KST 수정 이력에 2026-11-02 UTC C028 검증 및 minor 2건 단위 심사를 연결했다. 링크 대상인 실제 이전 검증·리뷰와 첫 수정 대응을 고정 커밋에서 대조했다. 수정판의 재검증 대기는 그 생산 시점의 기록이며, 현재 고정 queue에는 후속 독립 검증 `verified` 및 phase `review`가 기록되어 있다. | 최초 이력을 보존하고 날짜 있는 한정 검증·심사 이력과 전체 심사 미완료를 구분한다. 충족. | **resolved** |

## 원문과 범위

[GPO 공식 PDF](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf)의 본문에서 인쇄 14608의 BIS 머리말·DATES, 14609의 거래 요건 설명·Changes·Savings Clause, 14610의 Part 744 개정지시 1과 2(a)–(p), 14614의 BIS 문서번호를 직접 확인했다. 2019-07211의 게재·효력일은 2019-04-11이며, 개정 내용은 Part 744 권한 인용 재기재 및 Supplement No. 6 UVL 개정이다. 총 50 추가·10 삭제와 기존 1건 주소 추가는 규칙 설명의 수치이고, China 37 추가·3 삭제 및 Hong Kong 6 추가·기존 1건 수정은 개정지시에도 있다. 숫자는 문언으로 확인했으며 전수 재계수하지 않았다. 공식 GovInfo HTML은 이번에 열리지 않았고 PDF 텍스트는 직접 읽었다. 표 시각 감사, 인용된 EAR 조문의 당시 전문·후속 연혁, 과거 다운로드 재현은 수행하지 않았다. Malaysia의 설명문과 단수 개정지시 사이 차이는 독립 검증에 명시되어 있고, 수정판은 전수 정합성을 주장하지 않는다.

수정판은 지정 당사자의 UVL 거래 요건과 기술별 중국 접근 제한을 구분하므로, 실제 제한 이전의 공식 신호에 대한 배분 반응을 묻는 charter와 양립한다. 이 규칙은 조사 창 안에서 찾아낸 단서 한 건이다. 거래·허가예외 사용·대체조달·기관 노출·기술 매핑이 확인되지 않아 실제 제한의 시점·강도, 창 전체의 추가 제한 부재, 41행·세 바이오 행의 상태는 판단하지 않는다. T12와 동시기 제한 위협 T05는 미해결이다. T01–T03은 기존 대응 진행 중이며 이 단위가 검증하지 않았다. 나머지 critical/major 위협도 기존 상태를 유지한다: T04·T06–T10·T13–T15·T17–T22는 open, T11은 기존 accepted-limitation이다. 식별 변동·estimand, 국가×기술×시점 교란, dose의 차등 효과와 수준 효과, 가장 가까운 문헌·novelty, 중국 정책·placebo·MDE·포기 기준은 이 단위의 승인 대상이 아니다.

## 사전 실패 점검

1. 게재·효력일이나 조건부 경과조항의 날짜가 기술별 China-binding cutoff로 옮겨지면, 종전 적격성과 실제 거래·대체 공급의 증거 없이 신호 구간을 잘못 자를 수 있다.
2. 지정 당사자 명단을 기술별 처치로 연결하거나 관측 한 건으로 전체 창이 깨끗하다고 가정하면, 같은 국가·기술·시점의 실제 제한 또는 누락된 사건을 신호 효과로 잘못 분류할 수 있다. 거래·기관·품목 연결과 별도의 창 전체 감사가 필요하다.
3. 공표된 인원수를 재계수 결과로 쓰거나 원규칙 승인으로 회차 완료를 기록하면 재현과 범위 판정에 실패한다. 전수 계수와 회차 검증·심사는 각각 별도 근거가 필요하다.

## 결정과 입력 무결성

**accept**는 이 수정판의 한정 원규칙 기록에만 적용한다. 기존 두 지적을 같은 ID와 등급으로 종결할 수 있고, 이 범위에 추가 수정은 요구하지 않는다. 현재 artifact의 별도 독립 검증도 `verified`이며 양쪽 근거가 같은 artifact SHA256에 묶여 있다. orchestrator가 별도 response 및 receipt를 만들고 전환 검사를 거친 후에만 이 단위를 완료로 기록할 것을 권고한다. 이 심사는 queue·ledger·위협 상태를 직접 변경하지 않는다.

| 고정 입력 | 직접 계산한 SHA256 |
|---|---|
| `AGENTS.md` | `e7bb717d23e8a37ae10d46e1d00fad8a650628cca4460a26d937f32c95254a5c` |
| `docs/INTERNAL_REVIEW.md` | `7a9710675548e804a473760d0d5244115d3ed281c789a27e10e1aec15116fadf` |
| `state/work_queue.json` | `10de0a889e1fe96f9b84e3d963a54695e5d4657936ce50f47b3e3a4e20fd4f30` |
| `state/research_charter.md` | `32225e9dbf67054f3ab8f7d3b45c0a83f7733b80db51c0c4f1e663654244a602` |
| `state/threat_register.md` | `7d8cfa045194fe73a191bf77ec24c6f2dd4691b8347469075c16dc91391a7a09` |
| `outputs/round_03/part744_uvl_14610_source.md` | `028a9ed38fa3e41df933d4a027ca8aeed9b20b9ca42f800190017a6830c9fd50` |
| `outputs/round_03/verification_uvl_r1_nov09.md` | `daed84697ec17ff338c2d06f00d66d2557279c0f0c0b9cf4480bbc8eb79fddad` |
| `outputs/reviews/internal/uvl_2019_14610_referee_1.md` | `f9f8f36bd0fef71ca3af14ccd4a64ebf32eb5d2f7195667f65bb43e072cda74e` |
| `outputs/reviews/internal/uvl_2019_14610_referee_1_r1_response.md` | `58e1a5895d4694138a1d3eb2809dee127d9c21deafb1d66099cfb8001ff59c00` |
| `outputs/round_03/verification_C028.md` | `19b826cdffae9922e543dfafc0bdd9f98001e51bf73924ab94734ba36f3df14c` |
