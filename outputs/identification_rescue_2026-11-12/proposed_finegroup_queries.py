"""Paste into EPO TIP notebook. Production proposal, NOT independently verified.

Default execution: PRE-2018 selection/support only. No post outcome is queried.
Dose is a separate explicit function, added below after the pre-only block.
"""
from epo.tipdata.patstat import PatstatClient
import collections
import datetime
import hashlib
import json
import re

patstat = PatstatClient(env="PROD")
dataset = patstat.full_dataset.strip(chr(96)).replace(":", ".")
assert re.fullmatch(r"[A-Za-z0-9_-]+[.][A-Za-z0-9_]+", dataset)

def fq_table(name):
    assert re.fullmatch(r"tls[0-9]{3}_[a-z_]+", name)
    return chr(96) + dataset + "." + name + chr(96)

def render_sql(template):
    return re.sub(r"@([a-z0-9_]+)@", lambda m: fq_table(m[1]), template)

def nested_builtin(value):
    """Convert BigQuery Row (including nested STRUCT arrays) before JSON export."""
    if hasattr(value,"items"):
        return {key:nested_builtin(item) for key,item in value.items()}
    if isinstance(value,(list,tuple)):
        return [nested_builtin(item) for item in value]
    return value

PRE_ONLY_SELECTION_SQL = r"""
WITH wo_apps AS (
  SELECT a.appln_id, a.docdb_family_id family, a.earliest_filing_date filing
  FROM @tls201_appln@ a
  WHERE a.appln_auth='WO' AND a.ipr_type='PI' AND a.docdb_family_id>0
    AND a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
    AND a.earliest_publn_date<=DATE '2017-12-31'
    AND EXISTS (SELECT 1 FROM @tls211_pat_publn@ wp
      WHERE wp.appln_id=a.appln_id
        AND wp.publn_date BETWEEN DATE '1900-01-01' AND DATE '2017-12-31')
), app_group AS (
  SELECT DISTINCT a.appln_id,a.family,a.filing,
    SUBSTR(i.ipc_class_symbol,1,4) cls,
    REGEXP_REPLACE(
      REGEXP_EXTRACT(i.ipc_class_symbol,r'^([A-H][0-9]{2}[A-Z][[:space:]]*[0-9]+/)'),
      r'[[:space:]]+','') main_group
  FROM wo_apps a JOIN @tls209_appln_ipc@ i USING(appln_id)
  WHERE SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G01S','G06F','G06N','H01L')
), family_country AS (
  SELECT g.cls,g.main_group,g.family,TRIM(p.person_ctry_code) country,
    MIN(g.filing) filing
  FROM app_group g
  JOIN @tls207_pers_appln@ pa ON pa.appln_id=g.appln_id AND pa.applt_seq_nr>0
  JOIN @tls206_person@ p USING(person_id)
  WHERE g.main_group IS NOT NULL
    AND TRIM(p.person_ctry_code) IN ('CN','US','JP','KR','DE')
  GROUP BY 1,2,3,4
), yearly AS (
  SELECT cls,main_group,country,EXTRACT(YEAR FROM filing) year,COUNT(*) n
  FROM family_country GROUP BY 1,2,3,4
), cn_selection AS (
  SELECT cls,main_group,SUM(n) cn_pre_total,MIN(n) cn_min_annual,
    COUNT(DISTINCT year) cn_years_observed
  FROM yearly WHERE country='CN' GROUP BY 1,2
  HAVING SUM(n)>=100 AND COUNT(DISTINCT year)=5 AND MIN(n)>=5
), support_grid AS (
  SELECT s.*,country,year,IFNULL(y.n,0) n
  FROM cn_selection s CROSS JOIN UNNEST(['CN','US','JP','KR','DE']) country
    CROSS JOIN UNNEST([2013,2014,2015,2016,2017]) year
  LEFT JOIN yearly y USING(cls,main_group,country,year)
)
SELECT cls,main_group,cn_pre_total,cn_min_annual,cn_years_observed,
  ARRAY_AGG(STRUCT(country,year,n) ORDER BY country,year) pre_support
FROM support_grid
GROUP BY 1,2,3,4,5 ORDER BY cls,main_group
"""

print("FINEGROUP_PREONLY_STARTED", datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
print("FINEGROUP_PREONLY_QUERY_SHA256", hashlib.sha256(render_sql(PRE_ONLY_SELECTION_SQL).encode()).hexdigest(), flush=True)
finegroup_pre_rows = [nested_builtin(row) for row in patstat.sql_query(render_sql(PRE_ONLY_SELECTION_SQL), use_legacy_sql=False)]
finegroup_selected = sorted(row["main_group"] for row in finegroup_pre_rows)
assert len(finegroup_selected) == len(set(finegroup_selected))
finegroup_meta = {
    "dataset": dataset,
    "post2017_outcome_queried": False,
    "selection_rule": "CN WO families pre2013-2017 total>=100 and every preyear>=5; own WO application publication<=2017-12-31",
    "selected_group_count": len(finegroup_selected),
    "groups_by_broad_class": dict(collections.Counter(row["cls"] for row in finegroup_pre_rows)),
    "cn_pre_total_range": [min((row["cn_pre_total"] for row in finegroup_pre_rows), default=None), max((row["cn_pre_total"] for row in finegroup_pre_rows), default=None)],
    "groups_with_all_four_donors_every_preyear_ge5": sum(all(x["n"]>=5 for x in row["pre_support"] if x["country"]!="CN") for row in finegroup_pre_rows),
}
print("FINEGROUP_PREONLY_META", json.dumps(finegroup_meta, default=str), flush=True)
print("FINEGROUP_PREONLY_ROWS", json.dumps(finegroup_pre_rows, default=str), flush=True)
print("FINEGROUP_SELECTED_SAVED_PROVISIONAL", json.dumps(finegroup_selected), flush=True)

# Separate, newly documented exploration. Original strict five-year rule above
# stays intact even if it returns zero. Never silently replace its output.
_strict_having = "HAVING SUM(n)>=100 AND COUNT(DISTINCT year)=5 AND MIN(n)>=5"
_mature_having = """HAVING SUM(n)>=100
    AND COUNT(DISTINCT IF(year BETWEEN 2013 AND 2015,year,NULL))=3
    AND MIN(IF(year BETWEEN 2013 AND 2015,n,NULL))>=5"""
assert PRE_ONLY_SELECTION_SQL.count(_strict_having)==1
MATURE_PRE_ONLY_SELECTION_SQL = PRE_ONLY_SELECTION_SQL.replace(_strict_having,_mature_having)

def run_mature_finegroup_pre():
    """New provisional rule: total2013-17>=100; each2013/14/15>=5.

    Only pre data. 2016/17 counts stay in the support grid as diagnostics.
    See root's finegroup_mature_rule.md for the result-before-rule history.
    """
    query = render_sql(MATURE_PRE_ONLY_SELECTION_SQL)
    print("FINEGROUP_MATURE_PREONLY_STARTED", datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
    print("FINEGROUP_MATURE_PREONLY_QUERY_SHA256", hashlib.sha256(query.encode()).hexdigest(), flush=True)
    rows = [nested_builtin(row) for row in patstat.sql_query(query,use_legacy_sql=False)]
    selected = sorted(row["main_group"] for row in rows)
    assert len(selected)==len(set(selected))
    meta = {
        "dataset":dataset,"post2017_outcome_queried":False,
        "selection_rule_id":"mature13_15_support_total13_17_100_v1",
        "selection_rule":"CN own-published WO pre2013-17total>=100; each2013/14/15>=5;2016/17support diagnostic only",
        "selected_group_count":len(selected),
        "groups_by_broad_class":dict(collections.Counter(row["cls"] for row in rows)),
        "groups_with_all_four_donors_every_2013_2015_year_ge5":sum(
            all(x["n"]>=5 for x in row["pre_support"] if x["country"]!="CN" and 2013<=x["year"]<=2015)
            for row in rows),
    }
    print("FINEGROUP_MATURE_PREONLY_META",json.dumps(meta,default=str),flush=True)
    print("FINEGROUP_MATURE_PREONLY_ROWS",json.dumps(rows,default=str),flush=True)
    print("FINEGROUP_MATURE_SELECTED_SAVED_PROVISIONAL",json.dumps(selected),flush=True)
    return {"meta":meta,"rows":rows,"selected_groups":selected}

# Explicit first step for the newly documented mature rule, not auto-executed:
# finegroup_mature = run_mature_finegroup_pre()

# STOP HERE to inspect pre-only metadata and save the selected group list.
# No query below runs automatically.

DOSE_PAIR_SQL = r"""
WITH wo_apps AS (
  SELECT a.appln_id,a.docdb_family_id family,a.earliest_filing_date filing
  FROM @tls201_appln@ a
  WHERE a.appln_auth='WO' AND a.ipr_type='PI' AND a.docdb_family_id>0
    AND a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
    AND a.earliest_publn_date<=DATE '2017-12-31'
    AND EXISTS (SELECT 1 FROM @tls211_pat_publn@ wp
      WHERE wp.appln_id=a.appln_id
        AND wp.publn_date BETWEEN DATE '1900-01-01' AND DATE '2017-12-31')
), app_group AS (
  SELECT DISTINCT a.appln_id,a.family,a.filing,
    REGEXP_REPLACE(
      REGEXP_EXTRACT(i.ipc_class_symbol,r'^([A-H][0-9]{2}[A-Z][[:space:]]*[0-9]+/)'),
      r'[[:space:]]+','') main_group
  FROM wo_apps a JOIN @tls209_appln_ipc@ i USING(appln_id)
  WHERE SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G01S','G06F','G06N','H01L')
), cn_apps AS (
  SELECT DISTINCT g.* FROM app_group g
  WHERE g.main_group IN (__GROUP_LIST__)
    AND EXISTS (SELECT 1 FROM @tls207_pers_appln@ pa
      JOIN @tls206_person@ p USING(person_id)
      WHERE pa.appln_id=g.appln_id AND pa.applt_seq_nr>0
        AND TRIM(p.person_ctry_code)='CN')
), eligible AS (
  SELECT DISTINCT main_group,family FROM cn_apps
), ranked AS (
  SELECT *,ROW_NUMBER() OVER(PARTITION BY main_group
    ORDER BY FARM_FINGERPRINT(CONCAT('wo-main-v1|',CAST(family AS STRING))),family) rn
  FROM eligible
), sample AS (
  SELECT main_group,family FROM ranked WHERE rn<=100
), pubs AS (
  SELECT DISTINCT s.main_group,s.family,p.pat_publn_id
  FROM sample s JOIN cn_apps a USING(main_group,family)
  JOIN @tls211_pat_publn@ p USING(appln_id)
  WHERE p.publn_date BETWEEN DATE '1900-01-01' AND DATE '2017-12-31'
), raw_refs AS (
  SELECT DISTINCT p.main_group,p.family,c.cited_pat_publn_id,c.citn_origin
  FROM pubs p JOIN @tls212_citation@ c USING(pat_publn_id)
  WHERE c.cited_pat_publn_id>0
), links AS (
  SELECT DISTINCT r.main_group,r.family,r.cited_pat_publn_id,r.citn_origin,
    t.publn_date target_date,a.docdb_family_id target_family
  FROM raw_refs r JOIN @tls211_pat_publn@ t
    ON t.pat_publn_id=r.cited_pat_publn_id
  JOIN @tls201_appln@ a ON a.appln_id=t.appln_id
  WHERE t.publn_date BETWEEN DATE '1900-01-01' AND DATE '2017-12-31'
    AND a.docdb_family_id>0 AND a.docdb_family_id!=r.family
), origin_links AS (
  SELECT l.*,origin FROM links l
  CROSS JOIN UNNEST(IF(l.citn_origin='APP',['ALL','APP'],['ALL'])) origin
), pair_representative AS (
  -- Separate representatives for ALL and APP: APP uses an APP edge's document.
  SELECT * EXCEPT(citn_origin,rn) FROM (
    SELECT *,ROW_NUMBER() OVER(
      PARTITION BY main_group,family,target_family,origin
      ORDER BY target_date,cited_pat_publn_id) rn
    FROM origin_links
  ) WHERE rn=1
), person_slots AS (
  SELECT r.*,
    CASE WHEN pa.applt_seq_nr IS NULL THEN NULL
      WHEN pa.person_id>0 THEN CONCAT('P',CAST(pa.person_id AS STRING))
      ELSE CONCAT('MISSING_SEQ',CAST(pa.applt_seq_nr AS STRING)) END person_key,
    TRIM(p.person_ctry_code) country
  FROM pair_representative r
  LEFT JOIN @tls227_pers_publn@ pa
    ON pa.pat_publn_id=r.cited_pat_publn_id AND pa.applt_seq_nr>0
  LEFT JOIN @tls206_person@ p ON p.person_id=pa.person_id
), pair_counts AS (
  SELECT main_group,family,target_family,origin,
    COUNT(DISTINCT person_key) listed_persons,
    COUNT(DISTINCT IF(REGEXP_CONTAINS(country,r'^[A-Z]{2}$')
      AND country NOT IN ('XX','ZZ','WO','EP','AP','EA','OA','GC','IB'),person_key,NULL)) known_persons,
    COUNT(DISTINCT IF(country='US',person_key,NULL)) us_persons
  FROM person_slots GROUP BY 1,2,3,4
), pair_bounds AS (
  SELECT *,
    IF(listed_persons>0,SAFE_DIVIDE(us_persons,listed_persons),0.0) us_lower,
    IF(listed_persons>0,
       SAFE_DIVIDE(us_persons+listed_persons-known_persons,listed_persons),1.0) us_upper,
    IF(known_persons>0,SAFE_DIVIDE(us_persons,known_persons),NULL) us_known_only
  FROM pair_counts
), eligible_n AS (
  SELECT main_group,COUNT(*) eligible_cn_wo_families FROM eligible GROUP BY 1
), sample_n AS (
  SELECT main_group,COUNT(*) sampled_families FROM sample GROUP BY 1
), raw_origin AS (
  SELECT r.main_group,r.family,r.cited_pat_publn_id,origin FROM raw_refs r
  CROSS JOIN UNNEST(IF(r.citn_origin='APP',['ALL','APP'],['ALL'])) origin
), raw_n AS (
  SELECT main_group,origin,
    COUNT(DISTINCT CONCAT(CAST(family AS STRING),'|',CAST(cited_pat_publn_id AS STRING))) raw_patent_document_refs
  FROM raw_origin GROUP BY 1,2
), valid_n AS (
  SELECT main_group,origin,
    COUNT(DISTINCT CONCAT(CAST(family AS STRING),'|',CAST(cited_pat_publn_id AS STRING))) valid_patent_document_refs
  FROM origin_links GROUP BY 1,2
), sums AS (
  SELECT main_group,origin,COUNT(*) cited_family_pairs,
    COUNT(DISTINCT family) citing_families_with_edges,
    COUNTIF(known_persons>0) pairs_any_known_country,
    COUNTIF(listed_persons=0) pairs_no_applicant_list,
    COUNTIF(listed_persons>known_persons) pairs_unknown_person_country,
    SUM(listed_persons) listed_persons_over_pairs,
    SUM(known_persons) known_persons_over_pairs,
    SUM(us_persons) us_persons_over_pairs,
    SUM(us_lower) us_fraction_lower_sum,
    SUM(us_upper) us_fraction_upper_sum,
    AVG(us_lower) b_pair_us_lower,
    AVG(us_upper) b_pair_us_upper,
    AVG(us_known_only) b_pair_us_known_only
  FROM pair_bounds GROUP BY 1,2
)
SELECT e.main_group,origin,e.eligible_cn_wo_families,s.sampled_families,
  IFNULL(r.raw_patent_document_refs,0) raw_patent_document_refs,
  IFNULL(v.valid_patent_document_refs,0) valid_patent_document_refs,
  IFNULL(z.cited_family_pairs,0) cited_family_pairs,
  IFNULL(z.citing_families_with_edges,0) citing_families_with_edges,
  IFNULL(z.pairs_any_known_country,0) pairs_any_known_country,
  IFNULL(z.pairs_no_applicant_list,0) pairs_no_applicant_list,
  IFNULL(z.pairs_unknown_person_country,0) pairs_unknown_person_country,
  IFNULL(z.listed_persons_over_pairs,0) listed_persons_over_pairs,
  IFNULL(z.known_persons_over_pairs,0) known_persons_over_pairs,
  IFNULL(z.us_persons_over_pairs,0) us_persons_over_pairs,
  z.us_fraction_lower_sum,z.us_fraction_upper_sum,
  z.b_pair_us_lower,z.b_pair_us_upper,z.b_pair_us_known_only
FROM eligible_n e JOIN sample_n s USING(main_group)
CROSS JOIN UNNEST(['ALL','APP']) origin
LEFT JOIN sums z USING(main_group,origin)
LEFT JOIN raw_n r USING(main_group,origin)
LEFT JOIN valid_n v USING(main_group,origin)
ORDER BY main_group,origin
"""

def build_finegroup_dose_sql(groups):
    groups = sorted(set(groups))
    if not groups or len(groups)>20:
        raise ValueError("Require 1..20 saved provisional groups per query; never silently truncate")
    if not all(re.fullmatch(r"[A-H][0-9]{2}[A-Z][0-9]+/", group) for group in groups):
        raise ValueError("Unexpected main-group identifier")
    # Strictly validated alphanumerics and slash; literal quoting is safe here.
    literals = ",".join("'" + group + "'" for group in groups)
    return render_sql(DOSE_PAIR_SQL.replace("__GROUP_LIST__", literals))

def run_finegroup_dose(groups, batch_size=20, selection=None):
    """Explicit call only, e.g. run_finegroup_dose(finegroup_selected[:20]).

    Save every returned aggregate and query hash before running the next batch.
    This bounds source-family expansions (<=2000 per query), NOT scan bytes.
    """
    if not 1<=batch_size<=20:
        raise ValueError("batch_size must be 1..20")
    saved = sorted(set(groups))
    allowed = finegroup_selected if selection is None else selection["selected_groups"]
    rule_id = "strict_fiveyear_pre_support_v1" if selection is None else selection["meta"]["selection_rule_id"]
    if not set(saved).issubset(set(allowed)):
        raise ValueError("Dose groups must come from saved provisional pre-only selection")
    output = []
    for offset in range(0,len(saved),batch_size):
        batch = saved[offset:offset+batch_size]
        query = build_finegroup_dose_sql(batch)
        print("FINEGROUP_DOSE_BATCH", json.dumps({"offset":offset,"groups":batch,"selection_rule_id":rule_id,
              "max_source_families":100*len(batch),
              "query_sha256":hashlib.sha256(query.encode()).hexdigest()}), flush=True)
        rows = [nested_builtin(row) for row in patstat.sql_query(query,use_legacy_sql=False)]
        print("FINEGROUP_DOSE_ROWS", json.dumps(rows,default=str), flush=True)
        output.extend(rows)
    return output

# Not executed by default:
# finegroup_dose_rows = run_finegroup_dose(finegroup_selected)
# Under the separately documented mature rule, after saving its pre metadata:
# finegroup_dose_rows = run_finegroup_dose(finegroup_mature["selected_groups"], selection=finegroup_mature)
