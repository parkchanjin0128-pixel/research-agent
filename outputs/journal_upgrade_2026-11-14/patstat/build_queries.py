"""Prepare new queries before reading new post outcomes. No paid API calls."""
from pathlib import Path
import csv, json, hashlib, base64, zlib
P=Path(__file__).parent
C=P.parent/'crosswalk'
mapping=list(csv.DictReader((C/'sql_exact_membership_union_2017_2026.csv').open(encoding='utf-8-sig')))
units={r['group_id']:r['analysis_unit_merged_ai_am'] for r in csv.DictReader((C/'analysis_unit_map.csv').open(encoding='utf-8-sig'))}
tu={}
for r in mapping:tu.setdefault((units[r['group_id']],r['label']),set()).add(r['ipc_compact'])
tm='technology_map AS (SELECT t.unit,t.label,ipc FROM UNNEST(['+','.join("STRUCT('%s' AS unit,'%s' AS label,'%s' AS codes)"%(u,l,','.join(sorted(cs))) for (u,l),cs in sorted(tu.items()))+"])t CROSS JOIN UNNEST(SPLIT(codes,','))ipc)"
# Table placeholders are replaced inside the authenticated notebook from public schema names.
common='WITH '+tm+''',
members AS (
 SELECT a.appln_id,a.docdb_family_id,a.earliest_filing_date,a.earliest_publn_date,
 m.unit,m.label,LOGICAL_OR(i.ipc_position='F') AS has_first
 FROM {A} a JOIN {I} i USING(appln_id)
 JOIN technology_map m ON REGEXP_REPLACE(UPPER(i.ipc_class_symbol),r'\\s+','')=m.ipc
 WHERE a.appln_auth='WO' AND a.docdb_family_id>0
 GROUP BY 1,2,3,4,5,6
),
wc AS (SELECT DISTINCT pa.appln_id,TRIM(p.person_ctry_code) AS country
 FROM {PA} pa JOIN {P} p USING(person_id)
 WHERE pa.applt_seq_nr>0 AND TRIM(p.person_ctry_code) IN ('CN','US','JP','KR','DE')),
source AS (SELECT DISTINCT m.unit,m.label,m.docdb_family_id,m.appln_id
 FROM members m JOIN wc USING(appln_id)
 WHERE country='CN' AND m.earliest_publn_date BETWEEN DATE'2013-01-01' AND DATE'2017-12-31')
'''
support=common+'''
SELECT m.unit,m.label,c.country,EXTRACT(YEAR FROM m.earliest_filing_date) AS year,
 COUNT(DISTINCT m.docdb_family_id) AS families,
 COUNT(DISTINCT IF(m.has_first,m.docdb_family_id,NULL)) AS first_families
FROM members m JOIN wc c USING(appln_id)
WHERE m.earliest_filing_date BETWEEN DATE'2010-01-01' AND DATE'2015-12-31'
 AND m.earliest_publn_date<=DATE_ADD(m.earliest_filing_date,INTERVAL 24 MONTH)
GROUP BY 1,2,3,4 ORDER BY 1,3,4
'''
# Family-pair ALL vs applicant-tagged APP; cited document selected identically for both.
dose=common+''',
pairdoc AS (
 SELECT s.unit,s.label,s.docdb_family_id AS source_family,
 ta.docdb_family_id AS target_family,t.pat_publn_id AS target_doc,t.publn_date,
 LOGICAL_OR(REGEXP_CONTAINS(UPPER(c.citn_origin),r'(^|[^A-Z])APP([^A-Z]|$)')) AS app
 FROM source s JOIN {PUB} sp ON sp.appln_id=s.appln_id
 JOIN {CIT} c ON c.pat_publn_id=sp.pat_publn_id
 LEFT JOIN {PUB} cd ON cd.pat_publn_id=c.cited_pat_publn_id AND c.cited_pat_publn_id>0
 JOIN {A} ta ON ta.appln_id=COALESCE(cd.appln_id,NULLIF(c.cited_appln_id,0))
 JOIN {PUB} t ON t.appln_id=ta.appln_id
 WHERE sp.publn_date BETWEEN DATE'2013-01-01' AND DATE'2017-12-31'
 AND t.publn_date<=DATE'2017-12-31' AND t.publn_date>=DATE'1800-01-01'
 AND ta.docdb_family_id>0 AND ta.docdb_family_id!=s.docdb_family_id
 AND (c.cited_pat_publn_id=0 OR c.cited_pat_publn_id IS NULL OR t.pat_publn_id=c.cited_pat_publn_id)
 GROUP BY 1,2,3,4,5,6
), pair AS (
 SELECT unit,label,source_family,target_family,
 ARRAY_AGG(STRUCT(target_doc,publn_date) ORDER BY publn_date,target_doc LIMIT 1)[OFFSET(0)].target_doc AS target_doc,
 LOGICAL_OR(app) AS app FROM pairdoc GROUP BY 1,2,3,4
), target_country AS (
 SELECT pp.pat_publn_id,COUNT(DISTINCT NULLIF(TRIM(p.person_ctry_code),'')) AS n_country,
 COUNT(DISTINCT IF(TRIM(p.person_ctry_code)='US','US',NULL)) AS n_us
 FROM {PP} pp JOIN {P} p USING(person_id)
 JOIN (SELECT DISTINCT target_doc FROM pair) x ON x.target_doc=pp.pat_publn_id
 WHERE pp.applt_seq_nr>0 GROUP BY 1
), d AS (SELECT pair.*,IFNULL(tc.n_country,0) n_country,
 SAFE_DIVIDE(tc.n_us,tc.n_country) AS us_fraction FROM pair
 LEFT JOIN target_country tc ON tc.pat_publn_id=pair.target_doc),
variants AS (SELECT *,v AS variant FROM d CROSS JOIN UNNEST(['ALL','APP'])v WHERE v='ALL' OR app),
agg AS (SELECT unit,label,variant,COUNT(*) AS pairs,
 COUNT(DISTINCT source_family) AS citing_families,COUNTIF(n_country>0) AS known_pairs,
 SUM(IFNULL(us_fraction,0)) AS known_us_mass FROM variants GROUP BY 1,2,3),
ns AS (SELECT unit,label,COUNT(DISTINCT docdb_family_id) AS source_families FROM source GROUP BY 1,2)
SELECT ns.*,v AS variant,IFNULL(a.pairs,0) pairs,IFNULL(a.citing_families,0) citing_families,
 IFNULL(a.known_pairs,0) known_pairs,IFNULL(a.known_us_mass,0) known_us_mass
FROM ns CROSS JOIN UNNEST(['ALL','APP'])v LEFT JOIN agg a ON a.unit=ns.unit AND a.variant=v
ORDER BY unit,variant
'''
panel=common+'''
SELECT m.unit,m.label,c.country,FORMAT_DATE('%Y-%m',m.earliest_filing_date) AS month,
 COUNT(DISTINCT m.docdb_family_id) AS families,
 COUNT(DISTINCT IF(m.has_first,m.docdb_family_id,NULL)) AS first_families
FROM members m JOIN wc c USING(appln_id)
WHERE m.earliest_filing_date BETWEEN DATE'2010-01-01' AND DATE'2019-12-31'
 AND m.earliest_publn_date<=DATE_ADD(m.earliest_filing_date,INTERVAL 24 MONTH)
GROUP BY 1,2,3,4 ORDER BY 1,3,4
'''
overlap=common+'''
SELECT a.unit AS unit_a,b.unit AS unit_b,COUNT(DISTINCT a.docdb_family_id) AS families
FROM members a JOIN members b USING(docdb_family_id)
WHERE a.earliest_filing_date BETWEEN DATE'2010-01-01' AND DATE'2015-12-31'
AND b.earliest_filing_date BETWEEN DATE'2010-01-01' AND DATE'2015-12-31'
AND a.unit<=b.unit GROUP BY 1,2 ORDER BY 1,2
'''
queries={'support':support,'dose':dose,'panel':panel,'overlap':overlap}
for k,v in queries.items():(P/(k+'.sql')).write_text(v,encoding='utf-8')
payload=json.dumps(queries,separators=(',',':')).encode()
(P/'queries.json').write_bytes(payload)
(P/'queries.b64').write_text(base64.b64encode(zlib.compress(payload,9)).decode())
print(json.dumps({'units':len(tu),'listed':sum(l=='positive' for u,l in tu),'alias_codes':sum(map(len,tu.values())),'queries_sha256':hashlib.sha256(payload).hexdigest(),'encoded_length':(P/'queries.b64').stat().st_size}))
