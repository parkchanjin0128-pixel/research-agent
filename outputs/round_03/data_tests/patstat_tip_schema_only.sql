-- EPO PATSTAT Global / TIP: unexecuted zero-row schema checks.
-- Run individually only after confirming the workspace's connection,
-- catalogue edition and actual schema namespace. No outcome rows requested.
SELECT appln_id, appln_auth, appln_kind, ipr_type, appln_filing_date,
       earliest_filing_date, earliest_publn_date, docdb_family_id
FROM tls201_appln WHERE 1 = 0;

SELECT person_id, person_ctry_code
FROM tls206_person WHERE 1 = 0;

SELECT appln_id, person_id, applt_seq_nr
FROM tls207_pers_appln WHERE 1 = 0;

SELECT appln_id, ipc_class_symbol
FROM tls209_appln_ipc WHERE 1 = 0;

SELECT pat_publn_id, appln_id, publn_date
FROM tls211_pat_publn WHERE 1 = 0;

SELECT pat_publn_id, citn_id, citn_origin, cited_pat_publn_id,
       cited_appln_id, cited_npl_publn_id
FROM tls212_citation WHERE 1 = 0;

SELECT appln_id, cpc_class_symbol
FROM tls224_appln_cpc WHERE 1 = 0;

SELECT docdb_family_id, cpc_class_symbol, cpc_action_date, cpc_version
FROM tls225_docdb_fam_cpc WHERE 1 = 0;

SELECT pat_publn_id, person_id, applt_seq_nr
FROM tls227_pers_publn WHERE 1 = 0;
