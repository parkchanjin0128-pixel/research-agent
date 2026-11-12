# 중국 공식 R&D 연속계열: 출처와 해석 범위

작성·원문 확인: 2026-11-12. 대상 보고연도는 2013~2020년, 연속 8년이다. 수치는 국가통계국(NBS)·과학기술부(MOST)·재정부(MOF)의 연도별 공동 공보에서 직접 전사했다. 공개일은 아래에 기록했다. 현재 NBS URL의 `202302`는 아카이브 경로이며 원래 공개일로 사용하지 않았다.

## 바로 사용할 수 있는 데이터

금액 단위는 **亿元 = 1억 위안 = 0.1 billion RMB**이다. 모두 해당 보고연도에 실제 지출된 명목금액이다. 불변가격·환율·PPP·현재가치 할인으로 조정하지 않았다. “정부연구기관”은 **수행부문**이며 정부의 전체 R&D 재원조달액이 아니다. 기업에는 국유기업과 민영기업이 포함되므로 “민간투자”로 바꿔 부르지 않는다.

| 보고연도 | 총 R&D | 기초연구 | 기초연구 비중(%) | 기업 수행 | 정부 소속 연구기관 수행 | 대학 수행 | 공식 원문·공개일 |
|---|---:|---:|---:|---:|---:|---:|---|
| 2013 | 11846.6 | 555.0 | 4.7 | 9075.8 | 1781.4 | 856.7 | [공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902123.html) · 2014-10-23 |
| 2014 | 13015.6 | 613.5 | 4.7 | 10060.6 | 1926.2 | 898.1 | [공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902124.html) · 2015-11-23 |
| 2015 | 14169.9 | 716.1 | 5.1 | 10881.3 | 2136.5 | 998.6 | [공보](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1899323.html) · 2016-11-11 |
| 2016 | 15676.7 | 822.9 | 5.2 | 12144.0 | 2260.2 | 1072.2 | [공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902126.html) · 2017-10-10 |
| 2017 | 17606.1 | 975.5 | 5.5 | 13660.2 | 2435.7 | 1266.0 | [공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902127.html) · 2018-10-09 |
| 2018 | 19677.9 | 1090.4 | 5.5 | 15233.7 | 2691.7 | 1457.9 | [공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902128.html) · 2019-08-30 |
| 2019 | 22143.6 | 1335.6 | 6.0 | 16921.8 | 3080.8 | 1796.6 | [공보](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/kjtj2020/202009/P020200917363989375844.pdf) · 2020-08-27 |
| 2020 | 24393.1 | 1467.0 | 6.0 | 18673.8 | 3408.8 | 1882.5 | [공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902130.html) · 2021-09-22 |

각 행의 모든 금액과 비중은 같은 행의 공식 공보에 연결된다. JSON의 `source_id`와 `field_source_locators`는 수치별로 아래 문단 위치를 연결한다. 이 자료의 연도는 지출 보고연도이며 수출통제 정책의 시행연도나 발표연도로 해석할 수 없다.

## 수치별 원문 위치

총 R&D 항목에는 총액·공보가 보도한 전년비 증가율·당시 GDP 대비 비중이 포함된다. 기초연구 항목에는 기초연구액·증가율·기초연구 비중이 포함된다. 수행부문 문단은 기업·정부연구기관·대학의 금액과 비중을 각각 제공한다. 브라우저 줄번호는 이번 추출본의 보조 locator이고, 재확인에는 절 제목과 문단 첫머리를 우선한다. PDF의 쪽수는 1부터 센다.

| 보고연도 | 총 R&D | 기초연구 | 수행부문 | GDP 판본 주석 |
|---|---|---|---|---|
| 2013 | I, first numeric paragraph (starts 2013年，全国共投入); browser lines 55 | I, 分活动类型看; browser line 59 | I, 分活动主体看; browser line 60 | Note [1], browser line 86 |
| 2014 | I, first numeric paragraph; browser line 57 | I, 分活动类型看; browser line 61 | I, 分活动主体看; browser line 62 | Note [1], browser line 188 |
| 2015 | I, first numeric paragraph; browser line 55 | I, 分活动类型看; browser line 59 | I, 分活动主体看; browser line 60 | 注释 [1], browser line 211; 附注 4.数据修订, lines 184-204 |
| 2016 | I, first numeric paragraph; browser line 57 | I, 分活动类型看; browser line 61 | I, 分活动主体看; browser line 62 | Notes [1]-[2], browser lines 193-194 |
| 2017 | I, first numeric paragraph; browser line 59 | I, 分活动类型看; browser line 63 | I, 分活动主体看; browser line 64 | Note [1], browser line 193 |
| 2018 | I, first numeric paragraph; browser line 59 | I, 分活动类型看; browser line 63 | I, 分活动主体看; browser line 64 | Notes [2]-[3], browser lines 92-94 |
| 2019 | PDF p.1, I, first numeric paragraph, lines 7-11 in extracted text | PDF p.1, I, 分活动类型看, extracted lines 12-14 | PDF p.1, I, 分活动主体看, extracted lines 15-18 | PDF p.2, Notes [2]-[3], extracted lines 53-55 |
| 2020 | I, first numeric paragraph; browser line 57 | I, 分活动类型看; browser line 61 | I, 分活动主体看; browser line 62 | Notes [2]-[3], browser lines 94-96 |

2015년 공보의 문서 날짜는 2016-11-10, NBS 웹 공개일은 2016-11-11이다. 2019년은 MOST에 게시된 공동 공보 PDF를 원문으로 사용했고, 같은 수치는 [NBS 원문](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902129.html)에서도 검색 확인했다.

## GDP 개정과 판본

총 R&D 및 기초연구 지출의 비율을 계산할 때 GDP는 필요하지 않다. 발표의 핵심 그림은 **명목지출 증가율**과 **기초연구/총 R&D 비중**으로 만드는 것이 적절하다. 원래 발표된 GDP 대비 R&D 비중을 연도별로 이어 붙이면 분모 판본이 섞인다. 아래는 확인된 개정 사례이며 최신 GDP 비중의 완전한 재구축 계열은 아니다.

- 2013 공보는 2013 GDP 초보계산(初步核算) 기준 2.08%를 발표했다. 2014·2015 공보는 각각 해당 연도 GDP 초보검증(初步核实) 기준이다. 2016·2017·2018·2019·2020 공보는 각 해당 연도 GDP 초보계산 기준이다. 각 행 원문의 GDP 주석을 참조한다.
- [2015 공보](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1899323.html), “附注 4.数据修订” 및 수정표: 2016년 7월 R&D 지출 GDP 회계 개혁으로 역사 GDP와 R&D/GDP 비중을 수정했다. 표의 2013 값은 수정 전 2.01% → 수정 후 1.99%, 2014는 2.05% → 2.02%다. 이 표의 수정 전 2013 값 2.01%도 최초 공보 2.08%와 다르다.
- [2016 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902126.html), 주 [2]: 최종 검증 GDP에 따라 2015 비중을 2.06%로 수정했다.
- [2018 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902128.html), 주 [3]: 2017 최종 검증 GDP에 따라 2017 비중을 2.15%로 수정했다.
- [2019 공보](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/kjtj2020/202009/P020200917363989375844.pdf), p.2 주 [3]: 제4차 경제총조사 후 2018 최종 검증 GDP에 따라 2018 비중을 2.19% → 2.14%로 수정했다.
- [2020 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902130.html), 주 [3]: 2019 최종 검증 GDP에 따라 2019 비중을 2.23% → 2.24%로 수정했다.

JSON은 `rd_gdp_intensity_original_release_pct`와 별도의 `gdp_intensity_revisions`를 구분한다. 최신 판본으로 통일됐다는 주장을 하지 않는다.

## 직접 관측되는 두 패턴

**1. 기초연구 구성 변화는 2018년보다 2019년에 나타난다.** 기초연구 지출은 2017년 975.5 → 2018년 1090.4 → 2019년 1335.6亿元이다. 공보상 증가율은 각각 18.5%, 11.8%, 22.5%다. 원자료로 다시 계산한 기초연구 비중은 2017년 5.5407%, 2018년 5.5412%, 2019년 6.0315%로, 2018년 변화는 약 +0.0005%p이고 2019년은 +0.4903%p다. 공보에서 반올림한 비중은 5.5% → 5.5% → 6.0%다. **2018년에 즉시 전환·가속했다는 주장은 이 계열에서 확인되지 않는다.** 2020 비중은 6.0140%이고 기초연구 증가율은 9.8%로 낮아진다. [2017 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902127.html), [2018 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902128.html), [2019 공보](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/kjtj2020/202009/P020200917363989375844.pdf), [2020 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902130.html).

**2. 2019년 R&D 증가는 기업 수행부문에만 집중되지 않는다.** 기업 R&D는 2018년 15233.7 → 2019년 16921.8亿元으로 증가하지만 공보상 증가율은 11.1%다. 대학은 1457.9 → 1796.6亿元(+23.2%), 정부연구기관은 2691.7 → 3080.8亿元(+14.5%)로 더 빠르게 늘었다. 기업 수행 비중은 77.4% → 76.4%, 대학은 7.4% → 8.1%다. 따라서 “민간기업의 선제적 R&D 재배분”을 직접 관측한 것으로 제시할 수 없다. [2018 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902128.html), [2019 공보 p.1, 수행부문 문단](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/kjtj2020/202009/P020200917363989375844.pdf).

## 2018 분할 탐색진단과 한계

producer는 전년비 증가율을 이용해 2014~2017년과 2018~2019년의 단순 평균을 비교하고, 2013~2017년 로그 선형 추세를 2018~2020년에 외삽한다. 이 분석은 **탐색적 집계 진단**이다. 2018~2019를 합치면 기초연구 평균 증가율은 17.133%로 2014~2017의 15.181%보다 높지만, 2018 단독 증가율은 낮다. 2013~2017 로그 추세 대비 기초연구는 2018 -1.364%, 2019 +4.806%, 2020 -0.138%다. 추세선 위·아래 차이를 수출통제의 효과로 해석하지 않는다.

관측치 8개, 비교집단 없음, 산업별 수출통제 노출도 없음, 기업 소유형태 구분 없음, 연중 예산·신호 순서 없음이다. 2019년 값만으로 사전 대응(anticipation)을 식별할 수 없다. 공보별 조사방법도 동일한 문구가 아니다. 2018 공보 “调查方法”은 일부 서비스업 대중형 기업 조사 등을 설명하고, 2019 공보는 규모 이하 공업기업 표본추계를, 2020 공보는 규모 이하 공업·서비스업 표본추계를 설명한다. [2018 공보 조사방법](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902128.html), [2019 공보 p.5 조사방법](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/kjtj2020/202009/P020200917363989375844.pdf), [2020 공보 조사방법](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902130.html). 이 문구 차이가 실제 단절을 만들었다는 주장은 하지 않으며 추가 비교성 감사가 필요하다.

## 재현 파일

- `data/official_rd_series.json`: 검증된 원문 수치·공개일·필드별 원문 위치·GDP 판본.
- `scripts/compute_official_rd.py`: 표준 라이브러리만 사용하는 계산 코드. 입력 JSON을 읽어 전년비·비중·비중 변화·탐색진단을 계산한다.
- `data/official_rd_derived.json`: producer 실행 결과. 공보 보고치와 재계산치를 별도로 보존한다.

실행: `python scripts/compute_official_rd.py` (발표자료 폴더에서). 기본 경로는 스크립트의 위치를 기준으로 하므로 다른 작업 폴더에서도 실행할 수 있다. 실제 번들 Python으로 실행 성공했고 2013~2020 연속성·양수 금액 검증을 통과했다. 반올림 때문에 재계산한 증가율이 공보의 한 자리 수와 미세하게 다를 수 있다.

