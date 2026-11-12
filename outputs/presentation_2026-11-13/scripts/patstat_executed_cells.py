# Executed notebook cell 4
# Exploratory pre-2018 patent linkage pilot. Aggregate output only.
from epo.tipdata.patstat import PatstatClient
import json, re, datetime
patstat = PatstatClient(env='PROD')
dataset = patstat.full_dataset.strip(chr(96)).replace(':','.')
assert re.fullmatch(r'[A-Za-z0-9_-]+[.][A-Za-z0-9_]+', dataset)
def tbl(t): return chr(96)+dataset+'.'+t+chr(96)
sql = '''
WITH cn AS (
 SELECT DISTINCT pa.appln_id
 FROM @tls207_pers_appln@ pa JOIN @tls206_person@ p USING(person_id)
 WHERE pa.applt_seq_nr>0 AND p.person_ctry_code='CN'
), eligible AS (
 SELECT DISTINCT SUBSTR(i.ipc_class_symbol,1,4) cls,a.docdb_family_id family
 FROM @tls201_appln@ a JOIN cn USING(appln_id) JOIN @tls209_appln_ipc@ i USING(appln_id)
 WHERE a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
 AND a.earliest_publn_date<=DATE '2017-12-31' AND a.ipr_type='PI' AND a.docdb_family_id>0
 AND SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G06N','G06F','H01L','G01S')
), ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY cls ORDER BY FARM_FINGERPRINT(CAST(family AS STRING))) rn FROM eligible
), sample AS (SELECT cls,family FROM ranked WHERE rn<=200), pubs AS (
 SELECT DISTINCT s.cls,s.family,p.pat_publn_id FROM sample s
 JOIN @tls201_appln@ a ON a.docdb_family_id=s.family
 JOIN @tls211_pat_publn@ p USING(appln_id)
 WHERE p.publn_date<=DATE '2017-12-31'
), links AS (
 SELECT DISTINCT s.cls,s.family,c.citn_origin,c.cited_pat_publn_id,
 t.appln_id target_application,t.publn_date target_date,a.docdb_family_id target_family
 FROM pubs s JOIN @tls212_citation@ c USING(pat_publn_id)
 JOIN @tls211_pat_publn@ t ON t.pat_publn_id=c.cited_pat_publn_id
 JOIN @tls201_appln@ a ON a.appln_id=t.appln_id
 WHERE c.cited_pat_publn_id>0 AND t.publn_date<=DATE '2017-12-31'
 AND a.docdb_family_id>0 AND a.docdb_family_id!=s.family
), countries AS (
 SELECT l.cls,l.family,l.target_family,l.cited_pat_publn_id,l.target_date,
 MAX(IF(l.citn_origin='APP',1,0)) app,
 COUNT(DISTINCT IF(p.person_ctry_code IS NOT NULL AND p.person_ctry_code!='',p.person_id,NULL)) known,
 COUNT(DISTINCT IF(p.person_ctry_code='US',p.person_id,NULL)) us,
 COUNT(DISTINCT IF(p.person_ctry_code='CN',p.person_id,NULL)) cn
 FROM links l LEFT JOIN @tls227_pers_publn@ pa ON pa.pat_publn_id=l.cited_pat_publn_id AND pa.applt_seq_nr>0
 LEFT JOIN @tls206_person@ p USING(person_id)
 GROUP BY 1,2,3,4,5
), pairs AS (
 SELECT * EXCEPT(rn),MAX(app) OVER(PARTITION BY cls,family,target_family) any_app
 FROM (SELECT *,ROW_NUMBER() OVER(PARTITION BY cls,family,target_family ORDER BY target_date,cited_pat_publn_id) rn FROM countries)
 QUALIFY rn=1
), totals AS (
 SELECT cls,COUNT(*) eligible_families FROM eligible GROUP BY cls
), samples AS (SELECT cls,COUNT(*) sampled_families FROM sample GROUP BY cls)
SELECT t.cls,t.eligible_families,s.sampled_families,
COUNT(p.target_family) cited_family_pairs,COUNT(DISTINCT p.family) citing_families_with_edges,
COUNTIF(p.known>0) known_country_pairs,
SUM(IF(p.known>0,SAFE_DIVIDE(p.us,p.known),0)) us_fractional_pairs,
SUM(IF(p.known>0,SAFE_DIVIDE(p.cn,p.known),0)) cn_fractional_pairs,
COUNTIF(p.any_app=1) applicant_origin_pairs,
COUNTIF(p.any_app=1 AND p.known>0) applicant_known_pairs,
SUM(IF(p.any_app=1 AND p.known>0,SAFE_DIVIDE(p.us,p.known),0)) applicant_us_fractional_pairs
FROM totals t JOIN samples s USING(cls) LEFT JOIN pairs p USING(cls)
GROUP BY 1,2,3 ORDER BY cls
'''
sql=re.sub(r'@([a-z0-9_]+)@',lambda m:tbl(m[1]),sql)
print('PILOT_STARTED',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
try:
 rows=patstat.sql_query(sql,use_legacy_sql=False)
 pilot_result=[dict(r) for r in rows]
 print('PILOT_AGGREGATES',json.dumps(pilot_result,default=str),flush=True)
except Exception as exc:
 print('PILOT_ERROR',type(exc).__name__,str(exc)[:1200],flush=True)


# Executed notebook cell 5
# Coverage diagnostic. Same temporal and IPC filters; no post-2017 outcome.
coverage_sql='''
WITH apps AS (
 SELECT DISTINCT SUBSTR(i.ipc_class_symbol,1,4) cls,a.appln_id,a.docdb_family_id family,a.appln_auth
 FROM @tls201_appln@ a JOIN @tls209_appln_ipc@ i USING(appln_id)
 WHERE a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
 AND a.earliest_publn_date<=DATE '2017-12-31' AND a.ipr_type='PI' AND a.docdb_family_id>0
 AND SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G06N','G06F','H01L','G01S')
), app_country AS (
 SELECT a.cls,a.family,MAX(IF(a.appln_auth='CN',1,0)) cn_office,
 MAX(IF(p.person_ctry_code='CN',1,0)) cn_address,
 MAX(IF(p.person_ctry_code IS NOT NULL AND p.person_ctry_code!='',1,0)) known_address,
 MAX(IF(a.appln_auth='CN' AND p.person_ctry_code='CN',1,0)) cn_office_address
 FROM apps a LEFT JOIN @tls207_pers_appln@ pa ON pa.appln_id=a.appln_id AND pa.applt_seq_nr>0
 LEFT JOIN @tls206_person@ p USING(person_id) GROUP BY 1,2
)
SELECT cls,COUNT(*) all_families,SUM(cn_office) cn_office_families,SUM(cn_address) cn_address_families,
SUM(known_address) any_known_address_families,SUM(cn_office_address) cn_office_cn_address_families
FROM app_country GROUP BY cls ORDER BY cls
'''
coverage_sql=re.sub(r'@([a-z0-9_]+)@',lambda m:tbl(m[1]),coverage_sql)
try:
 coverage_rows=[dict(r) for r in patstat.sql_query(coverage_sql,use_legacy_sql=False)]
 print('COVERAGE_AGGREGATES',json.dumps(coverage_rows),flush=True)
except Exception as exc: print('COVERAGE_ERROR',type(exc).__name__,str(exc)[:800],flush=True)


# Executed notebook cell 6
# Exploratory pre-2018 patent linkage pilot. Aggregate output only.
from epo.tipdata.patstat import PatstatClient
import json, re, datetime
patstat = PatstatClient(env='PROD')
dataset = patstat.full_dataset.strip(chr(96)).replace(':','.')
assert re.fullmatch(r'[A-Za-z0-9_-]+[.][A-Za-z0-9_]+', dataset)
def tbl(t): return chr(96)+dataset+'.'+t+chr(96)
sql = '''
WITH cn AS (
 SELECT DISTINCT pa.appln_id
 FROM @tls207_pers_appln@ pa JOIN @tls206_person@ p USING(person_id)
 WHERE pa.applt_seq_nr>0 AND TRIM(p.person_ctry_code)='CN'
), eligible AS (
 SELECT DISTINCT SUBSTR(i.ipc_class_symbol,1,4) cls,a.docdb_family_id family
 FROM @tls201_appln@ a JOIN cn USING(appln_id) JOIN @tls209_appln_ipc@ i USING(appln_id)
 WHERE a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
 AND a.earliest_publn_date<=DATE '2017-12-31' AND a.ipr_type='PI' AND a.docdb_family_id>0
 AND SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G06N','G06F','H01L','G01S')
), ranked AS (
 SELECT *,ROW_NUMBER() OVER(PARTITION BY cls ORDER BY FARM_FINGERPRINT(CAST(family AS STRING))) rn FROM eligible
), sample AS (SELECT cls,family FROM ranked WHERE rn<=200), pubs AS (
 SELECT DISTINCT s.cls,s.family,p.pat_publn_id FROM sample s
 JOIN @tls201_appln@ a ON a.docdb_family_id=s.family
 JOIN @tls211_pat_publn@ p USING(appln_id)
 WHERE p.publn_date<=DATE '2017-12-31'
), links AS (
 SELECT DISTINCT s.cls,s.family,c.citn_origin,c.cited_pat_publn_id,
 t.appln_id target_application,t.publn_date target_date,a.docdb_family_id target_family
 FROM pubs s JOIN @tls212_citation@ c USING(pat_publn_id)
 JOIN @tls211_pat_publn@ t ON t.pat_publn_id=c.cited_pat_publn_id
 JOIN @tls201_appln@ a ON a.appln_id=t.appln_id
 WHERE c.cited_pat_publn_id>0 AND t.publn_date<=DATE '2017-12-31'
 AND a.docdb_family_id>0 AND a.docdb_family_id!=s.family
), countries AS (
 SELECT l.cls,l.family,l.target_family,l.cited_pat_publn_id,l.target_date,
 MAX(IF(l.citn_origin='APP',1,0)) app,
 COUNT(DISTINCT IF(p.person_ctry_code IS NOT NULL AND TRIM(p.person_ctry_code)!='',p.person_id,NULL)) known,
 COUNT(DISTINCT IF(TRIM(p.person_ctry_code)='US',p.person_id,NULL)) us,
 COUNT(DISTINCT IF(TRIM(p.person_ctry_code)='CN',p.person_id,NULL)) cn
 FROM links l LEFT JOIN @tls227_pers_publn@ pa ON pa.pat_publn_id=l.cited_pat_publn_id AND pa.applt_seq_nr>0
 LEFT JOIN @tls206_person@ p USING(person_id)
 GROUP BY 1,2,3,4,5
), pairs AS (
 SELECT * EXCEPT(rn),MAX(app) OVER(PARTITION BY cls,family,target_family) any_app
 FROM (SELECT *,ROW_NUMBER() OVER(PARTITION BY cls,family,target_family ORDER BY target_date,cited_pat_publn_id) rn FROM countries)
 QUALIFY rn=1
), totals AS (
 SELECT cls,COUNT(*) eligible_families FROM eligible GROUP BY cls
), samples AS (SELECT cls,COUNT(*) sampled_families FROM sample GROUP BY cls)
SELECT t.cls,t.eligible_families,s.sampled_families,
COUNT(p.target_family) cited_family_pairs,COUNT(DISTINCT p.family) citing_families_with_edges,
COUNTIF(p.known>0) known_country_pairs,
SUM(IF(p.known>0,SAFE_DIVIDE(p.us,p.known),0)) us_fractional_pairs,
SUM(IF(p.known>0,SAFE_DIVIDE(p.cn,p.known),0)) cn_fractional_pairs,
COUNTIF(p.any_app=1) applicant_origin_pairs,
COUNTIF(p.any_app=1 AND p.known>0) applicant_known_pairs,
SUM(IF(p.any_app=1 AND p.known>0,SAFE_DIVIDE(p.us,p.known),0)) applicant_us_fractional_pairs
FROM totals t JOIN samples s USING(cls) LEFT JOIN pairs p USING(cls)
GROUP BY 1,2,3 ORDER BY cls
'''
sql=re.sub(r'@([a-z0-9_]+)@',lambda m:tbl(m[1]),sql)
print('PILOT_STARTED',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
try:
 rows=patstat.sql_query(sql,use_legacy_sql=False)
 pilot_result=[dict(r) for r in rows]
 print('PILOT_TRIMMED_AGGREGATES',json.dumps(pilot_result,default=str),flush=True)
except Exception as exc:
 print('PILOT_ERROR',type(exc).__name__,str(exc)[:1200],flush=True)


# Executed notebook cell 7
# Coverage diagnostic. Same temporal and IPC filters; no post-2017 outcome.
coverage_sql='''
WITH apps AS (
 SELECT DISTINCT SUBSTR(i.ipc_class_symbol,1,4) cls,a.appln_id,a.docdb_family_id family,a.appln_auth
 FROM @tls201_appln@ a JOIN @tls209_appln_ipc@ i USING(appln_id)
 WHERE a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
 AND a.earliest_publn_date<=DATE '2017-12-31' AND a.ipr_type='PI' AND a.docdb_family_id>0
 AND SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G06N','G06F','H01L','G01S')
), app_country AS (
 SELECT a.cls,a.family,MAX(IF(a.appln_auth='CN',1,0)) cn_office,
 MAX(IF(TRIM(p.person_ctry_code)='CN',1,0)) cn_address,
 MAX(IF(p.person_ctry_code IS NOT NULL AND TRIM(p.person_ctry_code)!='',1,0)) known_address,
 MAX(IF(a.appln_auth='CN' AND TRIM(p.person_ctry_code)='CN',1,0)) cn_office_address
 FROM apps a LEFT JOIN @tls207_pers_appln@ pa ON pa.appln_id=a.appln_id AND pa.applt_seq_nr>0
 LEFT JOIN @tls206_person@ p USING(person_id) GROUP BY 1,2
)
SELECT cls,COUNT(*) all_families,SUM(cn_office) cn_office_families,SUM(cn_address) cn_address_families,
SUM(known_address) any_known_address_families,SUM(cn_office_address) cn_office_cn_address_families
FROM app_country GROUP BY cls ORDER BY cls
'''
coverage_sql=re.sub(r'@([a-z0-9_]+)@',lambda m:tbl(m[1]),coverage_sql)
try:
 coverage_rows=[dict(r) for r in patstat.sql_query(coverage_sql,use_legacy_sql=False)]
 print('COVERAGE_TRIMMED_AGGREGATES',json.dumps(coverage_rows),flush=True)
except Exception as exc: print('COVERAGE_ERROR',type(exc).__name__,str(exc)[:800],flush=True)

