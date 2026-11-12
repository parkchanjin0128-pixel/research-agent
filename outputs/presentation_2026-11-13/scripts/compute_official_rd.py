"""Reproduce descriptive statistics from verified official source transcription.
Usage: python compute_official_rd.py [--data PATH] [--out-dir PATH]
Standard library only. No network calls and no model-based causal estimate.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean

FIELDS = (
    "rd_total_100m_rmb",
    "basic_research_100m_rmb",
    "enterprise_rd_100m_rmb",
    "government_institute_rd_100m_rmb",
    "higher_education_rd_100m_rmb",
)

def growth(current, previous):
    return 100.0 * (current / previous - 1.0)

def fit_log_trend(rows, field):
    """OLS log(y) = a + b*(year-2013), using 2013-2017 only."""
    xs = [r["year"] - 2013 for r in rows]
    ys = [math.log(r[field]) for r in rows]
    xbar, ybar = mean(xs), mean(ys)
    slope = sum((x-xbar)*(y-ybar) for x,y in zip(xs,ys)) / sum((x-xbar)**2 for x in xs)
    return ybar - slope*xbar, slope

def main():
    here = Path(__file__).resolve()
    default_data = here.parent.parent / "data" / "official_rd_series.json"
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=default_data)
    parser.add_argument("--out-dir", type=Path, default=default_data.parent)
    args = parser.parse_args()
    dataset = json.loads(args.data.read_text(encoding="utf-8"))
    rows = sorted(dataset["observations"], key=lambda r: r["year"])
    assert [r["year"] for r in rows] == list(range(2013, 2021))
    assert all(r[f] > 0 for r in rows for f in FIELDS)
    derived = []
    for i, row in enumerate(rows):
        item = {"year": row["year"]}
        item["basic_share_recomputed_pct"] = 100*row["basic_research_100m_rmb"]/row["rd_total_100m_rmb"]
        for sector in ("enterprise", "government_institute", "higher_education"):
            item[sector+"_share_recomputed_pct"] = 100*row[sector+"_rd_100m_rmb"]/row["rd_total_100m_rmb"]
        item["other_performers_100m_rmb"] = row["rd_total_100m_rmb"] - sum(row[f] for f in FIELDS[2:])
        for f in FIELDS:
            item[f.replace("_100m_rmb","_billion_rmb")] = row[f] / 10
            item[f.replace("_100m_rmb","_yoy_calculated_pct")] = growth(row[f], rows[i-1][f]) if i else None
        item["basic_share_change_calculated_pp"] = item["basic_share_recomputed_pct"] - derived[-1]["basic_share_recomputed_pct"] if i else None
        derived.append(item)

    lookup = {r["year"]: r for r in derived}
    group_summary = {}
    for label, years in (("pre_2018_growth_years_2014_2017", range(2014,2018)),
                         ("2018_2019_growth_years", range(2018,2020)),
                         ("post_2018_growth_year_2019_only", [2019])):
        group_summary[label] = {
            "years": list(years),
            "mean_total_yoy_pct": mean(lookup[y]["rd_total_yoy_calculated_pct"] for y in years),
            "mean_basic_yoy_pct": mean(lookup[y]["basic_research_yoy_calculated_pct"] for y in years),
            "mean_basic_share_change_pp": mean(lookup[y]["basic_share_change_calculated_pp"] for y in years),
        }
    trend_diagnostics = {}
    for f in FIELDS[:2]:
        a,b = fit_log_trend(rows[:5],f)
        trend_diagnostics[f] = {
            "training_years": [2013,2014,2015,2016,2017],
            "annual_log_slope": b,
            "fitted_annual_growth_pct": 100*math.expm1(b),
            "2018_2020": [
                {"year": r["year"], "predicted_100m_rmb": math.exp(a+b*(r["year"]-2013)),
                 "actual_vs_prediction_pct": 100*(r[f]/math.exp(a+b*(r["year"]-2013))-1)}
                for r in rows[5:]
            ],
        }
    result = {
        "method": "Arithmetic year-on-year growth from published rounded nominal levels; shares recalculated from these levels. Original source-reported growth/shares remain in input. Minor differences are rounding, not corrections.",
        "units": {"expenditure": "100 million nominal RMB; _billion_rmb fields convert by dividing by 10", "growth": "%", "share_change": "percentage points"},
        "causal_status": "Exploratory aggregate diagnostic only. The chosen 2018 split is not a structural-break test, treatment effect, or anticipation test. No p-values. Eight observations and no control group.",
        "annual": derived,
        "exploratory_2018_split": group_summary,
        "pre_2018_log_trend_diagnostic": trend_diagnostics,
    }
    args.out_dir.mkdir(parents=True,exist_ok=True)
    dest = args.out_dir / "official_rd_derived.json"
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for y in (2017,2018,2019,2020):
        r = lookup[y]
        print(f"{y}: total YoY {r['rd_total_yoy_calculated_pct']:.3f}%; basic YoY {r['basic_research_yoy_calculated_pct']:.3f}%; basic share {r['basic_share_recomputed_pct']:.4f}%; share change {r['basic_share_change_calculated_pp']:.4f} pp")
    print(f"Wrote {dest}")
    print("DESCRIPTIVE ONLY: no causal identification.")

if __name__ == "__main__":
    main()

