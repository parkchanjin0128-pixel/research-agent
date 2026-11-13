# 반증분석 산출물

`exploratory_execution_record.md`는 원 결과를 이미 읽은 뒤 새 계산을 하기 전에 기록한 탐색 계획이다. `analysis.md`는 실제 자료의 반증·실질크기 검토이며 인과가설의 검증 완료가 아니다.

재현은 작업공간 루트에서 다음 두 명령을 순서대로 실행한다. NumPy만 필요하며 SciPy를 사용하지 않는다.

```powershell
& 'python' 'outputs/final_research/empirics/run_falsification.py'
& 'python' 'outputs/final_research/empirics/verify_falsification.py'
```

JSON은 입력 해시·모든 월별 계수·가짜사건일·국가교체·기술별 holdout·조건부 편향격자·24개 simulation을 담는다. 각 결과의 CSV도 제공한다. `verification.json`은 별도 직접 OLS 산술검증이며 DB 원자료나 식별가정의 검증이 아니다. 스크립트는 이 디렉터리에만 쓴다.


## 효과 단위 정정

효과 크기의 legacy 5pct/10pct 필드명은 각각 ±log(1.05)/±log(1.10)의 대칭 로그이동이다. 음의 이동을 비율로 환산하면 각각 -4.7619048%/-9.0909091%이다. 정확한 -5%/-10%는 log(0.95)/log(0.90)이다. 유의수준 5% 및 검정력 80%는 이 효과크기 표기와 별개다. 24개 시나리오는 8개 기본모형의 calibration/evaluation 쌍을 3배율에 공통 사용하며, 독립 기본 난수 seed는 16개다.
