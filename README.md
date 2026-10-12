# 사용법

이 폴더는 여러 에이전트가 역할을 나눠 연구를 진행하도록 구성한 작업 환경이다.

## 구성

| 경로 | 내용 |
|---|---|
| `AGENTS.md` | orchestrator 규칙: 회차 루프, 독립성 규칙, 멈춤 규칙, 보고 형식 |
| `.codex/agents/*.toml` | 역할 6개 (referee, verifier, identification_designer, lit_scout, policy_archivist, data_engineer) |
| `state/research_charter.md` | 고정된 연구질문과 주장 가능 범위. **너만 수정한다** |
| `state/decision_log.md` | Gate 판정과 네 결정의 기록 (추가만 가능) |
| `state/threat_register.md` | 지금까지 찾은 식별 위협 19개와 처리 상태 |
| `state/claims_ledger.csv` | 판단 근거가 되는 사실과 검증 상태 |
| `prompts/round_03.md` | 다음 회차 지시 |
| `docs/master_prompt.md` | 원래 마스터 프롬프트 (세부 규칙 참조용) |
| `outputs/round_01`, `outputs/round_02` | **GPT Work에서 받은 1·2회차 산출물을 여기에 복사해 넣어라** |

## 시작 전 할 일

1. GPT Work에서 1·2회차 산출물을 다운로드해서 `outputs/round_01`, `outputs/round_02`에 넣어라. `progress_log.md`는 `outputs/` 바로 아래에 둬.
2. `.codex/agents/*.toml`의 `model` 값이 실제 모델 문자열과 맞는지 확인해라. 지금은 `gpt-6-astra`, `gpt-6.1-sol`로 적어 뒀는데, 정확한 문자열은 확인하지 못했어. 틀리면 그 줄을 지우면 상위 설정을 따른다.

## 실행

### Codex (VS Code) — 권장
Codex는 이 폴더의 `AGENTS.md`와 `.codex/agents/`를 직접 인식한다.

```
AGENTS.md를 따라 prompts/round_03.md를 실행해. 역할별로 subagent를 생성하고, 회차 루프 3절 순서를 지켜.
```

### ChatGPT Work
Work는 subagent를 쓸 수 있지만, `.codex/agents/` 정의 파일을 읽는다는 근거는 찾지 못했다. 그래서 `AGENTS.md` 2절에 역할 설명을 같이 넣어 뒀다.
- 데스크톱 앱에서 이 폴더를 연결하고 같은 지시를 보내라.
- 모델과 effort는 composer에서 고르게 되어 있다. 주로 판단하는 회차에서는 Astra high를 골라라.

## 회차가 끝나면

1. 보고에서 **referee blocker**와 **verifier의 contradicted 항목**부터 확인해라.
2. 결정 사항을 정하면 다음 회차 지시와 함께 보내라. 결정은 orchestrator가 `decision_log.md`에 기록한다.
3. 연구질문을 바꾸고 싶어지면 `research_charter.md`를 직접 수정해라. 에이전트는 이 파일을 수정하지 못하게 되어 있다.

## 한계 (중요)

- **같은 모델 계열끼리는 맹점을 공유한다.** referee를 분리해도 같은 GPT 계열이면 같은 실수를 놓칠 수 있다. 중요한 회차(설계 확정, Gate 판정) 뒤에는 `main_design.md`와 referee 리뷰를 **다른 모델 계열**에게 따로 심사받는 것이 가장 효과적인 보완이다.
- 하네스는 "최적 방향"을 보장하지 않는다. 할 수 있는 것은 세 가지다.
  1. 알려진 위협을 잊지 않게 한다 (threat register).
  2. 검증 안 된 사실 위에 판단을 쌓지 않게 한다 (claims ledger).
  3. 방향을 바꾸는 결정을 너에게 올린다 (멈춤 규칙).
- `claims_ledger.csv`의 C001(2018-06 하원 기록)은 Gate 2 판정을 사실상 결정한 근거다. 링크를 열어 해당 문단을 직접 확인해라.

---

## 자동 실행 설정 (GitHub repo 방식)

### 구조
- **GPT:** 5시간마다 예약 실행해서 생산 작업을 한다.
- **Claude:** 2시간마다 예약 실행해서 교차 모델 심사와 검증을 한다.
- 둘 다 `state/turn.md`를 보고 자기 차례일 때만 일한다.
- Gate 같은 결정 지점이 오면 `next: user`로 멈춘다. 결정은 `state/user_inbox.md`에 적고 `next: codex`로 바꾸면 다시 돈다.

### 설정 순서
1. GitHub에 **private repo**를 만든다 (예: `export-control-research`). 비어 있어도 된다.
2. claude.ai 설정의 Connectors에서 **GitHub을 연결**한다. 그 다음 Claude에게 `owner/repo` 이름을 알려준다.
   - Claude가 이 폴더를 repo에 올리고 2시간 간격 예약 작업을 만든다.
3. GPT Work의 1·2회차 산출물을 repo의 `outputs/round_01`, `outputs/round_02`에 올린다.
   - GitHub 웹의 "Add file → Upload files"를 쓰거나, Work의 GitHub 플러그인으로 올린다.
   - 올린 뒤 `state/turn.md`의 `next: user`를 `next: codex`로 바꿔 커밋한다.
4. ChatGPT에서 GitHub 플러그인을 연결하고 **scheduled task**를 만든다.
   - 간격: 5시간
   - 지시문: `prompts/gpt_scheduled_run.md`의 코드 블록
   - 모델: 6 Astra high (설계 회차)

### GPT 쪽이 repo에 push하지 못할 때
ChatGPT Work의 웹 예약 실행은 실행 사이에 로컬 폴더를 유지하지 않는다. GitHub 플러그인으로 커밋까지 할 수 있는지는 확인하지 못했다. 첫 실행에서 push가 실패하면 이렇게 바꿔라.
- 컴퓨터에 repo를 clone한다.
- ChatGPT 데스크톱 앱에서 그 폴더로 **로컬 scheduled task(Codex automation)**를 만든다.
- 이 경우 GPT 실행 시간에만 컴퓨터가 켜져 있으면 된다. Claude 쪽은 GitHub에서 돌기 때문에 컴퓨터와 무관하다.

### 주의
- 예약 실행은 승인 없이 돈다. GPT 쪽 sandbox가 웹 검색이나 네트워크를 막으면 연구가 진행되지 않는다. 첫 실행 결과를 꼭 확인해라.
- 둘 다 사용량을 쓴다. Claude 실행은 자기 차례가 아니면 바로 끝나서 사용량이 거의 들지 않는다.
- 회차당 Claude 심사는 최대 2회다. 그래도 blocker가 남으면 너에게 넘어온다.
