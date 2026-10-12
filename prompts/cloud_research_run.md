# GitHub 클라우드 연구 실행

이 실행은 GitHub 호스팅 Linux에서 실행된다. 사용자 PC나 로컬 캐시에 접근할 수 없다. 연구질문과 3회차 dose 검토는 이미 승인되어 있다. AGENTS.md, state/research_charter.md, state/decision_log.md, state/threat_register.md, state/claims_ledger.csv, outputs/progress_log.md, prompts/round_03.md를 읽고 현재 회차를 이어간다. Claude 리뷰가 있으면 우선 반영한다.

컨트롤러가 이미 원격 잠금을 점유했다. scripts/claim_turn.py를 다시 실행하지 않는다. git commit/push를 하지 말고 state/turn.md, 연구 charter, user_inbox, 워크플로, 스크립트/프롬프트 설정을 수정하지 않는다. 최종 커밋과 잠금 해제는 별도의 GitHub job이 수행한다. API 키나 GitHub 인증정보를 읽거나 출력하지 않는다.

AGENTS.md의 역할 파일을 읽고 지원되는 명시적 subagent 생성 기능으로 독립 작업을 배정한다. 각 생산자는 다른 파일에 쓴다. verifier와 referee는 작성자와 별도 에이전트이며 작성자의 대화·추론을 전달하지 않는다. 이 런타임에서 별도 에이전트를 실행할 수 없으면 자기 검증을 독립 검증으로 기록하지 말고 필요한 후속 검증을 남긴다. 가능한 생산 작업은 계속한다.

이번 실행은 30분 정도의 작은 작업 묶음으로 제한한다. 자주 파일을 저장하고 outputs/progress_log.md를 갱신한다. 전체 3회차를 한 번에 끝내려 하지 않는다. 작업 중단에도 다음 실행이 재개할 수 있도록 완료/미완료를 구분한다. 다음 회차 지시가 필요하면 기존 승인 범위의 master_prompt에 근거한 제안만 남기며 Gate 채택을 대신하지 않는다.

수정 가능한 파일은 현재 회차 outputs/round_XX/, outputs/reviews/, outputs/progress_log.md, state/claims_ledger.csv, state/threat_register.md, state/decision_log.md다. 기존 round_01과 round_02 산출물은 원본으로 보존한다. 코딩/SQL 초안이 필요하면 현재 회차 data_tests 아래에 둔다. 원문 전체나 PDF를 outputs에 복사하지 않는다. 공개 출처는 브라우징·네트워크로 확인할 수 있으나 유료 호출/대량 스캔/배분 outcome 집계는 하지 않는다.

outputs/round_03/sources_manifest.json의 공개 출처와 기존 검토 결과를 이용한다. 사용자 제공 PDF는 이 클라우드 저장소에 없다. 필요한 원문에 접근하지 못하면 미확인과 접근 실패를 기록한다. 기존 작성자의 resume_notes는 확정된 사실표가 아니다. 41행 미확인을 규제 미통제 확인으로 바꾸려면 행별 ECCN·규칙 근거가 필요하다.

새 Gate 채택, 불가역 freeze, 질문 변경, 비용 작업은 사용자에게 구체적인 보고서를 준비한 뒤 올린다. 사용자가 이미 승인한 Gate 2·3 실패·질문 유지·dose 후보 검토를 다시 승인받지 않는다. Claude 심사로 보낼 준비가 되면 독립 verifier/referee 파일과 현재 회차 필수 산출물이 모두 있어야 한다.

마지막 응답은 제공된 JSON schema를 따른다. 남은 생산/검증 작업이 있으면 next=codex, 심사 준비 완료면 next=claude, 실제 사용자 결정이 필요하면 next=user다. 실행 중 환경 오류나 자료 접근 실패는 숨기지 말고 summary 및 진행 로그에 적는다. 컨트롤러는 이를 실제 turn 전환에 사용한다.
