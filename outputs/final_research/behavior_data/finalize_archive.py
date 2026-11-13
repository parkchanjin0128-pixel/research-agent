"""Merge the predeclared 36-page probe and four logged lineage-targeted pages."""
from archive_probe import ROOT,PERIOD,KEYWORDS,write_csv
import json,csv,re
def main():
 s=json.loads((ROOT/'archive_probe_summary.json').read_text('utf-8'))
 f=json.loads((ROOT/'archive_followup_probe.json').read_text('utf-8'))
 with (ROOT/'archive_all_listed_records.csv').open(encoding='utf-8-sig') as handle:rows=list(csv.DictReader(handle))
 rows+=f['records'];rows=list({(r['category'],r['url']):r for r in rows}.values())
 period=[r for r in rows if PERIOD[0]<=r['date']<=PERIOD[1]]
 candidates=[r for r in period if re.search(KEYWORDS,r['title'],re.I)]
 write_csv('archive_final_2016_2019_inventory.csv',period)
 write_csv('archive_final_keyword_candidates.csv',candidates)
 logs=s['logs']+f['logs']
 result=dict(archive_document_count=len(logs),current_listed_category_url_rows=len(rows),within_2016_2019=len(period),keyword_candidate_notices=len(candidates),institution_counts={i:sum(r['institution']==i for r in period) for i in sorted({r['institution'] for r in period})},candidate_institution_counts={i:sum(r['institution']==i for r in candidates) for i in sorted({r['institution'] for r in candidates})},complete_original_population=False,unit='category-URL notice; amendments, re-tenders, unsuccessful tenders, services and awards are distinct notices; not projects',missing_channels='SZU government-procurement category arrays begin in 2023, no 2016-19 coverage; NJUST is a bounded page sample; departmental purchases not inventoried',logs=logs)
 (ROOT/'archive_final_summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='logs'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
