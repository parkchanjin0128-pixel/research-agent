
WITH apps AS (
 SELECT DISTINCT a.appln_id,a.docdb_family_id family,a.appln_auth
 FROM `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls201_appln` a JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls209_appln_ipc` i USING(appln_id)
 WHERE a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2017-12-31'
 AND a.earliest_publn_date<=DATE '2017-12-31' AND a.ipr_type='PI' AND a.docdb_family_id>0
 AND SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G06N','G06F','H01L','G01S')
), ac AS (
 SELECT a.appln_id,MAX(IF(TRIM(p.person_ctry_code)='CN',1,0)) cn207,MAX(IF(TRIM(p.person_ctry_code)!='',1,0)) known207
 FROM apps a LEFT JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls207_pers_appln` pa ON pa.appln_id=a.appln_id AND pa.applt_seq_nr>0
 LEFT JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls206_person` p USING(person_id) GROUP BY 1
), pc AS (
 SELECT a.appln_id,MAX(IF(TRIM(p.person_ctry_code)='CN',1,0)) cn227,MAX(IF(TRIM(p.person_ctry_code)!='',1,0)) known227
 FROM apps a LEFT JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls211_pat_publn` pub ON pub.appln_id=a.appln_id AND pub.publn_date<=DATE '2017-12-31'
 LEFT JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls227_pers_publn` pa ON pa.pat_publn_id=pub.pat_publn_id AND pa.applt_seq_nr>0
 LEFT JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls206_person` p USING(person_id) GROUP BY 1
) SELECT a.appln_auth,COUNT(*) apps,SUM(cn207) cn207,SUM(known207) known207,SUM(cn227) cn227,SUM(known227) known227
 FROM apps a JOIN ac USING(appln_id) JOIN pc USING(appln_id)
 WHERE a.appln_auth IN ('CN','US','JP','KR','DE','EP','WO')
 GROUP BY 1 ORDER BY 1

