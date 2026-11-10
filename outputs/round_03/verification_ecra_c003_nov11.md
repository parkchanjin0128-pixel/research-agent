# C003 독립 검증 — ECRA §1758의 세 고려요소

- 검증자: `/root/ecra_c003_verifier_nov11` (독립 검증). 열람: 2026-11-10 UTC / 2026-11-11 KST.
- 기준 커밋: `parkchanjin0128-pixel/research-agent@845f5ec3e323e403e79c4e21686edd3a091b6533`.
- 읽은 기준본: `outputs/round_03/ecra_c003_source_note.md` (blob `9b420409122cdacc984887724aa62dde32088d5e`), `state/claims_ledger.csv` C003 (blob `7d1664c1944594a6a59e6f85b6311d6f1c804ccf`), `prompts/round_03.md` B1 (blob `f583fc5f57bdaefc858f14f3486c62021edd55cd`). 기준 원장의 C003은 `unverified`이며 2차 미러를 인용한다.

**판정: C003의 조문상 고려 의무를 독립 확인했다. 아래 문안으로 좁혀 `verified`를 권고한다.**

> ECRA §1758(a)(2)(B)(i)–(iii) (50 U.S.C. §4817(a)(2)(B))는 신흥·기반기술을 식별하는 관계기관 절차에서 (i) 외국에서의 해당 기술 발전, (ii) 이 조에 따른 수출통제가 미국 내 해당 기술 발전에 미칠 수 있는 영향, (iii) 이 조에 따른 수출통제가 해당 기술의 외국으로의 확산을 제한하는 데 얼마나 효과적인지를 고려하도록 요구한다.

원장의 문안에는 (ii)의 **미국 내**와 (iii)의 **외국으로의 확산**을 명시한다. 세 요소는 기술 식별 절차의 고려 의무다. 어느 하나를 충족하면 자동 통제한다거나 통제의 실제 효과가 입증됐다는 뜻은 아니다.

| 독립 열람한 공식 원문 | 정확한 위치와 확인 사항 |
| --- | --- |
| [GovInfo, U.S. Statutes at Large](https://www.govinfo.gov/content/pkg/STATUTE-132/pdf/STATUTE-132-Pg1636.pdf#page=584), Pub. L. 115–232, div. A, title XVII, subtitle B, §1758 (2018-08-13) | 132 Stat. **2218** / PDF **583쪽**(0부터 세면 582): §1758 표제, (a)(1), (a)(2)의 본문과 (A)(i) 시작. 132 Stat. **2219** / PDF **584쪽**(인덱스 583): (a)(2)(B)(i)–(iii) 세 고려요소(추출문 30676–30685행), 이어 (a)(2)(C) 공고·의견제출 기간 및 (b)(1)–(2) 통제 설정·수준. (b)(2)(B)는 통제 수준을 정할 때 수출 제한국 목록과 잠재적 최종용도·최종사용자를 별도로 고려하도록 한다. |
| [GovInfo, 공법 Star Print PDF](https://www.govinfo.gov/content/pkg/PLAW-115publ232/pdf/PLAW-115publ232.pdf#page=585) 및 [공법 HTML](https://www.govinfo.gov/content/pkg/PLAW-115publ232/html/PLAW-115publ232.htm) | 앞표지가 있어 PDF 쪽 번호가 다르다. 인쇄면 2218 / PDF 584쪽에 §1758 시작, 인쇄면 2219 / PDF 585쪽에 세 고려요소(30651–30660행). HTML 인쇄면 2219, 36498–36508행도 일치한다. |
| [미 하원 법률개정고문실(OLRC), 50 U.S.C. §4817](https://uscode.house.gov/us/usc/119-120/t50/s4817/) | (a)(2)(B)(i)–(iii), 44–49행; (a)(2)(C), 51행; (b)(1)–(2), 53–71행; 제정법 출전, 165행. 119–120 경로의 표제는 2026-10-07까지의 효력 법률을 수록한다고 표시한다. 생산자 노트의 119–118 경로에서도 44–49행의 동일 조문을 확인했다. |
| [GovInfo, BIS ANPRM, 83 FR 58201–58202](https://www.govinfo.gov/content/pkg/FR-2018-11-19/pdf/2018-25221.pdf), FR Doc. 2018–25221 | 인쇄면 58201 / PDF 1쪽의 ACTION·SUMMARY 및 Background(41–79, 103–157행): 식별 기준에 관한 의견 요청과 이후 별도 통제 절차. 인쇄면 58202 / PDF 2쪽의 Foundational Technology·Representative Technology Categories(220–234행): 기반기술 식별에는 별도 ANPRM을 예고했고 대표 범주는 검토 범주였다. 이 공고가 새 통제를 부과한 것으로 해석하지 않는다. C002는 이번 판정에 포함하지 않는다. |

**B1의 사용 범위.** 법이 외국에서의 기술 발전 및 외국으로의 확산 제한 가능성을 고려한다는 사실은 기술별 통제 위협을 연구할 제도적 동기다. 외국은 중국에 한정되지 않으며, 미국 기술 발전에 미칠 영향과 확산 제한 효과성은 중국의 잠재적 손실과 별개의 개념이다. 2013–2017년 중국 출원인 특허의 미국 출원인 인용 비중, IP5 패밀리 중 미국 비중, 하드웨어의 HS 매핑 대미 수입 의존도는 B1의 측정 후보다. 조문은 이 후보의 타당성, 산식·가중치·임계값, 외생성, 발표효과의 인과 식별, 중국에 실제 적용되는 품목·구속력·효력일 또는 공통 컷오프를 확정하지 않는다. (a)(2)(C)의 의견 수렴과 (b)의 수출·재수출·해당국 내 이전 통제는 단계가 다르다.

**접근 기록.** GitHub의 고정 커밋에서 세 파일을 읽었다. 웹에서 Statutes at Large PDF, 공법 Star Print PDF·HTML, OLRC 두 경로 및 ANPRM PDF를 직접 열고 해당 본문을 추출해 대조했다. Statutes at Large PDF의 두 면에 대한 스크린샷 요청은 응답했으나 이번 인터페이스에 이미지 바이트가 전달되지 않아 시각 검증으로 기록하지 않는다. 같은 PDF의 셸 `curl -I`는 6초 후 시간 초과였고, 본문 검증은 성공한 웹 PDF 추출을 사용했다. 원문 열람의 대상은 C003과 그 해석에 필요한 인접 조항·공고 문구로 한정했다. 다른 원장 항목, Gate, 설계 동결을 판정하지 않았으며 결과변수를 열람하거나 집계하지 않았다.

**원장 제안.** `source_url`은 [미 하원 공식 법전](https://uscode.house.gov/us/usc/119-120/t50/s4817/), `source_type`은 `1차(미 하원 법전·제정법 대조)`, `verification_status`는 `verified`, `verified_by`는 `independent_verifier`. UTC 기준 `verified_date`는 `2026-11-10`(한국 기준 2026-11-11). 비고: “제정법 132 Stat. 2219 및 OLRC §4817(a)(2)(B)(i)–(iii) 독립 대조. B_k의 제도적 동기만 확인; 중국 손실·측정식·외생성·인과효과·실제 통제·효력일 및 Gate 미검증. outputs/round_03/verification_ecra_c003_nov11.md.”
