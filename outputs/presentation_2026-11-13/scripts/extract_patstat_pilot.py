"""Extract executed code and aggregate-only outputs from the saved TIP notebook."""
import csv
import hashlib
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
notebook_path = root / "data/patstat_pilot_notebook.ipynb"
raw = notebook_path.read_bytes()
notebook = json.loads(raw)
data = {}
code = []
for index, cell in enumerate(notebook["cells"]):
    source = "".join(cell.get("source", []))
    if cell.get("cell_type") != "code" or not source.strip():
        continue
    if "PILOT_" in source or "COVERAGE_" in source:
        code.append(f"# Executed notebook cell {index + 1}\n" + source)
    for output in cell.get("outputs", []):
        text = "".join(output.get("text", []))
        for key in ["PILOT_TRIMMED_AGGREGATES", "COVERAGE_TRIMMED_AGGREGATES"]:
            match = re.search(key + r" (\[.*\])", text)
            if match:
                data[key] = json.loads(match.group(1))
assert len(data["PILOT_TRIMMED_AGGREGATES"]) == 5
assert len(data["COVERAGE_TRIMMED_AGGREGATES"]) == 5
(root / "scripts/patstat_executed_cells.py").write_text(
    "\n\n".join(code) + "\n", encoding="utf-8"
)
result = {
    "source": "EPO TIP PATSTAT PROD aggregate-only queries",
    "snapshot": "Retrieved 2026-11-12, exact release label unresolved",
    "notebook_sha256": hashlib.sha256(raw).hexdigest(),
    "temporal_filter": "earliest filing 2013–2017 and first publication through 2017",
    "sampling": "200 DOCDB families per IPC class, deterministic FARM_FINGERPRINT ordering",
    "country_rule": "TRIM; applicant address, not nationality; missing countries excluded from known denominator",
    "raw": data,
    "rows": [],
}
labels = {"C12N": "미생물과 유전공학", "G01S": "무선 위치결정", "G06F": "디지털 데이터 처리",
          "G06N": "특정 계산모형", "H01L": "반도체 소자"}
coverage = {r["cls"]: r for r in data["COVERAGE_TRIMMED_AGGREGATES"]}
for row in data["PILOT_TRIMMED_AGGREGATES"]:
    result["rows"].append({
        **row,
        "label": labels[row["cls"]],
        "all_us_pct": 100 * row["us_fractional_pairs"] / row["known_country_pairs"],
        "app_us_pct": 100 * row["applicant_us_fractional_pairs"] / row["applicant_known_pairs"],
        "missing_country_pairs_pct": 100 * (1 - row["known_country_pairs"] / row["cited_family_pairs"]),
        "app_origin_pairs_pct": 100 * row["applicant_origin_pairs"] / row["cited_family_pairs"],
        **coverage[row["cls"]],
    })
for key, value in result["raw"].items():
    assert all(r["cls"] in labels for r in value), key
result["totals"] = {
    "class_family_observations": sum(r["sampled_families"] for r in result["rows"]),
    "family_pair_observations": sum(r["cited_family_pairs"] for r in result["rows"]),
    "known_country_pair_observations": sum(r["known_country_pairs"] for r in result["rows"]),
    "app_origin_pair_observations": sum(r["applicant_origin_pairs"] for r in result["rows"]),
    "overlap_note": "IPC groups may share families; totals are class-specific observations",
}
all_order = sorted(result["rows"], key=lambda r: r["all_us_pct"], reverse=True)
app_order = sorted(result["rows"], key=lambda r: r["app_us_pct"], reverse=True)
result["ranks"] = {
    "all": [r["cls"] for r in all_order],
    "app": [r["cls"] for r in app_order],
    "interpretation": "Descriptive sample ranking only; no causal estimate or population sampling inference",
}
out = root / "data/patstat_pilot_final.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (root / "data/patstat_pilot_final.csv").open("w", encoding="utf-8-sig", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(result["rows"][0]))
    writer.writeheader()
    writer.writerows(result["rows"])
print(json.dumps({"totals": result["totals"], "ranks": result["ranks"]}, ensure_ascii=False, indent=2))
