"""독립 측정 검산. 표준 라이브러리만 사용하며 기본 실행은 네트워크를 호출하지 않는다.

원 특허 DB의 SQL을 재실행하지 않고 보존된 그룹별 결과를 재집계한다.
API_EVIDENCE는 2026-11-13 검증자가 별도 공개 API 요청 한 번으로 받은 4행의 선택 필드다.
"""
import collections
import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs/final_research/verification"
EXPECTED_RECOVERY_SHA = "d57a64d28c0199db098077edc7a9cbd7d6c8a91ddb4a526efa4e4252f6099d52"
API_EVIDENCE = {
    "url": "https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=156&period=2016&partnerCode=0%2C842&cmdCode=8486%2C8542&flowCode=M&partner2Code=0&customsCode=C00&motCode=0&maxRecords=4",
    "retrieved_utc": "2026-11-13T02:58:47.313030+00:00",
    "http_status": 200,
    "response_bytes": 3649,
    "response_sha256": "5882816298e181bd8cbb423b73350a41451f3de4be7616cb8b463c1bb1c9f91a",
    "requests": 1,
    "count": 4,
    "error": "",
    "no_key": True,
    "account_created": False,
    "rate_limit_response": False,
    "preservation": "도구 실행기록에서 응답 해시와 선택 필드를 기록했다. 전체 원문 바이트는 별도 파일로 보존하지 않았다.",
    "data": [
        {"refYear": 2016, "reporterCode": 156, "flowCode": "M", "partnerCode": 0, "partner2Code": 0, "cmdCode": "8486", "customsCode": "C00", "motCode": 0, "classificationCode": "H4", "isOriginalClassification": True, "primaryValue": 14033544468.0, "cifvalue": 14033544468.0, "isReported": False, "isAggregate": True},
        {"refYear": 2016, "reporterCode": 156, "flowCode": "M", "partnerCode": 842, "partner2Code": 0, "cmdCode": "8486", "customsCode": "C00", "motCode": 0, "classificationCode": "H4", "isOriginalClassification": True, "primaryValue": 2273811763.0, "cifvalue": 2273811763.0, "isReported": False, "isAggregate": True},
        {"refYear": 2016, "reporterCode": 156, "flowCode": "M", "partnerCode": 0, "partner2Code": 0, "cmdCode": "8542", "customsCode": "C00", "motCode": 0, "classificationCode": "H4", "isOriginalClassification": True, "primaryValue": 227616904239.0, "cifvalue": 227616904239.0, "isReported": False, "isAggregate": True},
        {"refYear": 2016, "reporterCode": 156, "flowCode": "M", "partnerCode": 842, "partner2Code": 0, "cmdCode": "8542", "customsCode": "C00", "motCode": 0, "classificationCode": "H4", "isOriginalClassification": True, "primaryValue": 8696121253.0, "cifvalue": 8696121253.0, "isReported": False, "isAggregate": True},
    ],
}

SOURCES = [
    {"title": "UN Comtrade 공개 API", "url": "https://comtradeplus.un.org/en/api-docs", "verified": "키 없는 public preview, 최대 500행"},
    {"title": "UN Comtrade Trade valuation", "url": "https://uncomtrade.org/docs/trade-valuation/", "verified": "primaryValue의 CIF/FOB 선택 및 CIF 평가 의미"},
    {"title": "UN Comtrade Conversion factors and current/constant value", "url": "https://uncomtrade.org/docs/conversion-factors-and-current-constant-value/", "verified": "무역금액은 경상 미국 달러"},
    {"title": "UN Comtrade Data items", "url": "https://comtradeplus.un.org/en/reference-tables?table=dataitem", "verified": "isOriginalClassification, isReported, isAggregate, primaryValue의 개별 정의"},
]

def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))

def sha(relative):
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

def close(a, b):
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)

def run():
    inputs = [
        "outputs/final_research/family_country_recovery_raw.json",
        "outputs/final_research/family_country_recovery_protocol.md",
        "outputs/identification_rescue_2026-11-12/finegroup_pre_dose_raw.json",
        "outputs/final_research/trade/all_rows.json",
        "outputs/final_research/trade/derived.json",
        "outputs/final_research/trade/history_sources.json",
        "outputs/final_research/trade/pilot_2017_meta.json",
    ]
    hashes = {p: sha(p) for p in inputs}
    assert hashes[inputs[0]] == EXPECTED_RECOVERY_SHA
    r, old = read(inputs[0]), read(inputs[2])
    assert set(r["selected_groups"]) == set(old["selected_groups"])
    assert r["base_script_sha256"] == old["script_sha256"]
    assert r["cutoff"] == "2017-12-31"
    assert len(r["rows"]) == 45
    assert len({(x["origin"], x["main_group"]) for x in r["rows"]}) == 45
    old_index = {(x["origin"], x["main_group"]): x for x in old["dose_rows"]}
    recovery = {}
    for origin in ("ALL", "APP"):
        rows = [x for x in r["rows"] if x["origin"] == origin]
        original = [x for x in old["dose_rows"] if x["origin"] == origin]
        widths = [x["b_family_upper"] - x["b_family_lower"] for x in rows]
        for x in rows:
            assert x["pairs"] == old_index[origin, x["main_group"]]["cited_family_pairs"]
            assert 0 < x["family_known_pairs"] <= x["pairs"]
            assert 0 <= x["changed_document_pairs"] <= x["pairs"]
            assert 0 <= x["b_family_lower"] <= x["b_family_upper"] <= 1
        pair_comparisons = []
        for a, b in itertools.combinations(rows, 2):
            if a["b_family_lower"] > b["b_family_upper"]:
                higher, lower = a, b
            elif b["b_family_lower"] > a["b_family_upper"]:
                higher, lower = b, a
            else:
                continue
            pair_comparisons.append({"higher": higher["main_group"], "lower": lower["main_group"]})
        absent = sorted(set(r["selected_groups"]) - {x["main_group"] for x in rows})
        assert all(old_index[origin, g]["cited_family_pairs"] == 0 for g in absent)
        total, known = sum(x["pairs"] for x in rows), sum(x["family_known_pairs"] for x in rows)
        original_known = sum(x["pairs_any_known_country"] for x in original)
        stats = {
            "groups_with_pairs": len(rows), "pairs": total,
            "family_known_pairs": known,
            "changed_document_pairs": sum(x["changed_document_pairs"] for x in rows),
            "median_interval_width": statistics.median(widths),
            "point_range": [min(x["b_family_known_only"] for x in rows), max(x["b_family_known_only"] for x in rows)],
            "marginal_intersection": [max(x["b_family_lower"] for x in rows), min(x["b_family_upper"] for x in rows)],
            "original_document_known_pairs": original_known,
            "original_document_known_share": original_known / total,
            "family_known_share": known / total,
            "net_known_pair_gain": known - original_known,
            "net_coverage_gain_percentage_points": (known - original_known) / total * 100,
            "original_document_median_interval_width_nonzero_pair_groups": statistics.median(x["b_pair_us_upper"] - x["b_pair_us_lower"] for x in original if x["cited_family_pairs"] > 0),
            "undefined_no_pair_groups": absent,
            "pairwise_comparisons": len(rows) * (len(rows) - 1) // 2,
            "strictly_separated_interval_pairs": len(pair_comparisons),
            "overlapping_or_touching_interval_pairs": len(rows) * (len(rows) - 1) // 2 - len(pair_comparisons),
            "separated_pairs": pair_comparisons,
            "zero_width_groups": sum(w == 0 for w in widths),
            "groups_with_at_most_6_pairs": sum(x["pairs"] <= 6 for x in rows),
            "groups_with_at_most_3_known_source_families": sum(x["source_families_known"] <= 3 for x in rows),
        }
        for k, v in r["summary"][origin].items():
            if isinstance(v, list):
                assert all(close(a, b) for a, b in zip(v, stats[k]))
            else:
                assert close(v, stats[k])
        recovery[origin] = stats
    assert recovery["ALL"]["pairs"] == 10747
    assert recovery["ALL"]["family_known_pairs"] == 6561
    assert recovery["ALL"]["changed_document_pairs"] == 3221
    assert recovery["ALL"]["original_document_known_pairs"] == 4659
    assert recovery["APP"]["pairs"] == 765 and recovery["APP"]["family_known_pairs"] == 745
    trade_rows, derived = read(inputs[3]), read(inputs[4])
    key = lambda x: (x["refYear"], x["cmdCode"], x["partnerCode"])
    index = {key(x): x for x in trade_rows}
    expected = set(itertools.product(range(2013, 2018), ("8486", "8542"), (0, 842)))
    assert len(trade_rows) == len(index) == 20 and set(index) == expected
    for x in trade_rows:
        assert x["reporterCode"] == 156 and x["flowCode"] == "M"
        assert x["partner2Code"] == 0 and x["customsCode"] == "C00" and x["motCode"] == 0
        assert x["typeCode"] == "C" and x["freqCode"] == "A"
        assert x["isOriginalClassification"] is True
        assert x["classificationCode"] == ("H5" if x["refYear"] == 2017 else "H4")
        assert x["isReported"] is (x["refYear"] <= 2014)
        assert x["isAggregate"] is (x["refYear"] >= 2015)
        assert x["primaryValue"] == x["cifvalue"]
    archives = []
    archive_rows = []
    source_meta = read(inputs[5]) + [dict(read(inputs[6]), year=2017)]
    for meta in source_meta:
        f = "pilot_2017_response.json" if meta["year"] == 2017 else f"{meta['year']}_response.json"
        path = f"outputs/final_research/trade/{f}"
        body = read(path)
        assert sha(path) == meta["sha256"]
        assert body["count"] == len(body["data"]) == 4 and not body["error"]
        archive_rows.extend(body["data"])
        archives.append({"file": path, "sha256": sha(path), "matches_source_hash": True, "count": body["count"], "url": meta["url"]})
    assert {key(x): x for x in archive_rows} == index
    trade = {}
    for hs in ("8486", "8542"):
        annual = []
        for year in range(2013, 2018):
            world, us = index[year, hs, 0], index[year, hs, 842]
            annual.append({"year": year, "world_import_value_current_usd": world["primaryValue"], "us_partner_import_value_current_usd": us["primaryValue"], "us_partner_share": us["primaryValue"] / world["primaryValue"], "classification": world["classificationCode"]})
        pooled = sum(x["us_partner_import_value_current_usd"] for x in annual) / sum(x["world_import_value_current_usd"] for x in annual)
        for actual, claimed in zip(annual, derived["results"][hs]["annual"]):
            assert actual["year"] == claimed["year"]
            assert close(actual["us_partner_share"], claimed["us_partner_share"])
        assert close(pooled, derived["results"][hs]["pooled2013_17_us_partner_share"])
        trade[hs] = {"annual": annual, "pooled_us_partner_share": pooled, "simple_mean_annual_share": statistics.mean(x["us_partner_share"] for x in annual), "pooled_world_current_usd": sum(x["world_import_value_current_usd"] for x in annual), "pooled_us_partner_current_usd": sum(x["us_partner_import_value_current_usd"] for x in annual)}
    for x in API_EVIDENCE["data"]:
        assert all(index[key(x)][k] == v for k, v in x.items())
    flags = [{"year": y, "rows": 4, "isOriginalClassification": True, "isReported": index[y, "8486", 0]["isReported"], "isAggregate": index[y, "8486", 0]["isAggregate"]} for y in range(2013, 2018)]
    result = {
        "검증일": "2026-11-13", "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "판정": "보존 집계 산술과 2016년 공개 API 4행은 일치. 구성개념, 조건부 구간, 인과해석에는 아래 제한이 적용된다.",
        "input_sha256": hashes, "recovery": recovery, "trade": trade,
        "trade_archives": archives, "trade_flags_by_year": flags,
        "independent_public_api": dict(API_EVIDENCE, selected_fields_match_archived_rows=True),
        "official_sources": SOURCES,
        "수행하지_않은_검증": ["원 특허 DB 독립 재쿼리", "개별 source-target pair 및 신청인 명단 재구축", "2016년 이외의 무역 API 독립 재조회", "HS4와 ECCN의 법률상 일대일 대응 확정", "미국 기업 국적 또는 실제 미국 기술 의존도 검증", "정책효과 인과식별 완료"],
        "해석": {
            "새_대리변수": "2017년 말까지 공개된 같은 target family 문헌 중 알려진 신청인 국가가 있는 가장 이른 공보의 국가 footprint. 원 피인용 문헌 국가의 결측치 대체로 간주하지 않는다.",
            "구간": "관측된 신청인 명단의 국가 미상 인원에 조건부인 하한·상한이다. 명단 자체 누락, family 공보 선택, 소유권·주소 변경 및 표본변동을 포괄하는 신뢰구간이 아니다.",
            "순위": "공통교집합 공집합은 모든 쌍의 순위식별을 뜻하지 않는다. 분리된 구간 쌍의 순서만 이 주변구간으로 보장할 수 있다.",
            "무역": "중국을 reporter로 하는 HS4 수입 중 미국 partner의 경상 달러 CIF 금액 비중. 미국 기업 국적, 미국 기술 함량, FDPR 관할, ECCN 또는 정책효과가 아니다.",
            "원보고": "원보고 분류판 isOriginalClassification과 직접 보고 행 isReported는 구분해야 한다. 2015–2017년 행은 isReported=false, isAggregate=true이다.",
        },
        "검산": "모든 assertion 통과",
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "measurement_nov13.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT / "measurement_nov13.json"), "검산": result["검산"], "ALL": recovery["ALL"], "APP": {k: v for k, v in recovery["APP"].items() if k != "separated_pairs"}, "trade_pooled": {k: v["pooled_us_partner_share"] for k, v in trade.items()}}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    run()
