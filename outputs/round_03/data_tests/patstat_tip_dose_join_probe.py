# EPO TIP notebook cell. The SQL checks field resolution and join syntax.
# Both branches enforce empty inputs and empty outputs in the SQL itself.
from epo.tipdata.patstat import PatstatClient
import re

patstat = PatstatClient(env="PROD")
dataset = patstat.full_dataset.strip("`").replace(":", ".")
if not re.fullmatch(r"[A-Za-z0-9_-]+[.][A-Za-z0-9_]+", dataset):
    raise ValueError("Unexpected TIP dataset reference format.")

citation_sql = """
WITH citing AS (
    SELECT c.pat_publn_id, c.citn_id, c.citn_replenished, c.citn_origin,
           c.citn_gener_auth, c.pat_citn_seq_nr, c.npl_citn_seq_nr,
           c.cited_pat_publn_id, c.cited_appln_id, c.cited_npl_publn_id,
           src.appln_id AS source_application, src.docdb_family_id AS source_family,
           pub.publn_date AS source_publication_date, src.appln_filing_date,
           p.person_ctry_code AS citing_applicant_country, ipc.ipc_class_symbol
    FROM @TLS212_CITATION@ AS c
    JOIN @TLS211_PAT_PUBLN@ AS pub ON pub.pat_publn_id = c.pat_publn_id
    JOIN @TLS201_APPLN@ AS src ON src.appln_id = pub.appln_id
    LEFT JOIN @TLS227_PERS_PUBLN@ AS ca
           ON ca.pat_publn_id = pub.pat_publn_id AND ca.applt_seq_nr > 0
    LEFT JOIN @TLS206_PERSON@ AS p ON p.person_id = ca.person_id
    LEFT JOIN @TLS209_APPLN_IPC@ AS ipc ON ipc.appln_id = src.appln_id
    WHERE FALSE
),
targets AS (
    SELECT s.*, 'publication' AS target_kind, a.docdb_family_id AS target_family,
           t.publn_date AS target_publication_date, p.person_ctry_code AS cited_applicant_country
    FROM citing AS s
    LEFT JOIN @TLS211_PAT_PUBLN@ AS t ON t.pat_publn_id = s.cited_pat_publn_id
    LEFT JOIN @TLS201_APPLN@ AS a ON a.appln_id = t.appln_id
    LEFT JOIN @TLS227_PERS_PUBLN@ AS pa
           ON pa.pat_publn_id = t.pat_publn_id AND pa.applt_seq_nr > 0
    LEFT JOIN @TLS206_PERSON@ AS p ON p.person_id = pa.person_id
    WHERE s.cited_pat_publn_id > 0 AND s.cited_appln_id = 0
    UNION ALL
    SELECT s.*, 'application' AS target_kind, a.docdb_family_id AS target_family,
           a.earliest_publn_date AS target_publication_date,
           p.person_ctry_code AS cited_applicant_country
    FROM citing AS s
    LEFT JOIN @TLS201_APPLN@ AS a ON a.appln_id = s.cited_appln_id
    LEFT JOIN @TLS207_PERS_APPLN@ AS pa ON pa.appln_id = a.appln_id AND pa.applt_seq_nr > 0
    LEFT JOIN @TLS206_PERSON@ AS p ON p.person_id = pa.person_id
    WHERE s.cited_appln_id > 0 AND s.cited_pat_publn_id = 0
)
SELECT * FROM targets WHERE FALSE
"""

family_sql = """
WITH seeds AS (
    SELECT a.appln_id, a.appln_filing_date, a.earliest_filing_id,
           a.earliest_filing_date, a.earliest_publn_date, a.docdb_family_id,
           pri.prior_appln_id
    FROM @TLS201_APPLN@ AS a
    LEFT JOIN @TLS204_APPLN_PRIOR@ AS pri ON pri.appln_id = a.appln_id
    WHERE FALSE
),
paths AS (
    SELECT s.*, root.appln_id AS root_application, origin.person_ctry_code,
           m.appln_id AS member_application, m.appln_auth AS filing_authority,
           m.appln_kind, m.ipr_type, m.appln_filing_date AS member_filing_date,
           m.nat_phase, m.reg_phase, m.int_phase, m.internat_appln_id,
           pub.publn_date AS member_publication_date, ipc.ipc_class_symbol, ipc.ipc_version,
           cpc.cpc_class_symbol, cpc.cpc_action_date, cpc.cpc_version
    FROM seeds AS s
    LEFT JOIN @TLS201_APPLN@ AS root ON root.appln_id = s.earliest_filing_id
    LEFT JOIN @TLS207_PERS_APPLN@ AS pa ON pa.appln_id = root.appln_id AND pa.applt_seq_nr > 0
    LEFT JOIN @TLS206_PERSON@ AS origin ON origin.person_id = pa.person_id
    LEFT JOIN @TLS201_APPLN@ AS m ON m.docdb_family_id = s.docdb_family_id
    LEFT JOIN @TLS211_PAT_PUBLN@ AS pub ON pub.appln_id = m.appln_id
    LEFT JOIN @TLS209_APPLN_IPC@ AS ipc ON ipc.appln_id = m.appln_id
    LEFT JOIN @TLS225_DOCDB_FAM_CPC@ AS cpc ON cpc.docdb_family_id = s.docdb_family_id
)
SELECT * FROM paths WHERE FALSE
"""

for label, template in (("Citation links", citation_sql), ("Family links", family_sql)):
    sql = re.sub(r"@(TLS\d{3}_[A-Z_]+)@", lambda match: f"`{dataset}.{match[1].lower()}`", template)
    if sql.count("WHERE FALSE") != 2 or "@" in sql:
        raise ValueError("Query is not a fully resolved empty-result check.")
    try:
        result = patstat.sql_query(sql, use_legacy_sql=False)
        print(f"{label}: " + ("PASS (zero rows)" if not result else "STOP (unexpected rows)"), flush=True)
        if result:
            break
    except Exception as exc:
        reasons = [e.get("reason", "unknown") for e in (getattr(exc, "errors", None) or []) if isinstance(e, dict)]
        print(f"{label}: FAIL ({type(exc).__name__}; {', '.join(reasons)})", flush=True)
