# Cell 1: PATSTAT Global schema only; no patent records or counts.
from epo.tipdata.patstat import PatstatClient
import re

checks = {
    'tls201_appln': 'appln_id appln_auth appln_kind ipr_type appln_filing_date earliest_filing_date earliest_publn_date docdb_family_id',
    'tls206_person': 'person_id person_ctry_code',
    'tls207_pers_appln': 'appln_id person_id applt_seq_nr',
    'tls209_appln_ipc': 'appln_id ipc_class_symbol',
    'tls211_pat_publn': 'pat_publn_id appln_id publn_date',
    'tls212_citation': 'pat_publn_id citn_id citn_origin cited_pat_publn_id cited_appln_id cited_npl_publn_id',
    'tls224_appln_cpc': 'appln_id cpc_class_symbol',
    'tls225_docdb_fam_cpc': 'docdb_family_id cpc_class_symbol cpc_action_date cpc_version',
    'tls227_pers_publn': 'pat_publn_id person_id applt_seq_nr',
}
patstat = PatstatClient(env='PROD')
dataset = patstat.full_dataset.strip(chr(96)).replace(':', '.')
if not re.fullmatch(r'[a-zA-Z0-9_-]+[.][a-zA-Z0-9_]+', dataset):
    raise ValueError('Unexpected dataset reference format; no query sent.')
print('PATSTAT PROD dataset label:', dataset.rsplit('.', 1)[-1], flush=True)
for table, fields in checks.items():
    sql = 'SELECT ' + ', '.join(fields.split()) + ' FROM ' + chr(96) + dataset + '.' + table + chr(96) + ' WHERE FALSE'
    try:
        rows = patstat.sql_query(sql, use_legacy_sql=False)
        print(table, 'PASS: no result rows' if not rows else 'STOP: unexpected output', flush=True)
        if rows:
            break
    except Exception as exc:
        errors = getattr(exc, 'errors', None) or []
        reasons = ','.join(str(item.get('reason', 'unknown')) for item in errors if isinstance(item, dict))
        print(table, 'FAIL:', type(exc).__name__, reasons, flush=True)
        break

# Cell 2: only the database catalogue.
from collections import Counter

q = ('SELECT table_name, column_name, data_type FROM ' + chr(96) + dataset
     + '.INFORMATION_SCHEMA.COLUMNS' + chr(96)
     + ' WHERE LOWER(table_name) IN (' + ', '.join(repr(x) for x in checks) + ')')
try:
    meta = patstat.sql_query(q, use_legacy_sql=False)
    fields_found = {(r['table_name'].lower(), r['column_name'].lower()): r['data_type'] for r in meta}
    wanted = [(tab, col) for tab, cols in checks.items() for col in cols.split()]
    print('Requested schema fields present:', sum(key in fields_found for key in wanted), '/', len(wanted))
    print('Observed requested field types:', dict(Counter(fields_found[k] for k in wanted if k in fields_found)))
except Exception as exc:
    print('COLUMNS metadata unavailable:', type(exc).__name__)

q = ('SELECT option_value FROM ' + chr(96) + dataset + '.INFORMATION_SCHEMA.TABLE_OPTIONS' + chr(96)
     + " WHERE LOWER(table_name) IN ('tls201_appln','tls211_pat_publn') AND option_name IN ('description','labels')")
try:
    options = patstat.sql_query(q, use_legacy_sql=False)
    labels = sorted({m.group(0) for r in options for m in re.finditer(r'20[12][0-9][ _-]*(?:Spring|Autumn|Fall)|(?:Spring|Autumn|Fall)[ _-]*20[12][0-9]', str(r['option_value']), re.I)})
    print('Explicit release labels in application/publication table metadata:', labels or 'none')
except Exception as exc:
    print('TABLE_OPTIONS metadata unavailable:', type(exc).__name__)
