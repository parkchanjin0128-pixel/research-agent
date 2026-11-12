
WITH family_country AS (
 SELECT SUBSTR(i.ipc_class_symbol,1,4) cls,TRIM(p.person_ctry_code) country,a.docdb_family_id family,
 MIN(a.earliest_filing_date) filing
 FROM `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls201_appln` a JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls209_appln_ipc` i USING(appln_id)
 JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls207_pers_appln` pa ON pa.appln_id=a.appln_id AND pa.applt_seq_nr>0
 JOIN `p-epo-tip-prj-3a1f.p_epo_tip_euwe4_bqd_patstatb.tls206_person` p USING(person_id)
 WHERE a.appln_auth='WO' AND a.ipr_type='PI' AND a.docdb_family_id>0
 AND a.earliest_filing_date BETWEEN DATE '2013-01-01' AND DATE '2019-12-31'
 AND a.earliest_publn_date<=DATE '2021-12-31'
 AND TRIM(p.person_ctry_code) IN ('CN','US','JP','KR','DE')
 AND SUBSTR(i.ipc_class_symbol,1,4) IN ('C12N','G01S','G06F','G06N','H01L')
 GROUP BY 1,2,3
) SELECT cls,country,FORMAT_DATE('%Y-%m',filing) month,COUNT(*) n
FROM family_country GROUP BY 1,2,3 ORDER BY 1,2,3

