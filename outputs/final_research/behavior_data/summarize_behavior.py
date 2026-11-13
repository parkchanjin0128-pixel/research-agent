"""Descriptive pilot audit; does not estimate a causal signal effect."""
from acquire_behavior import ROOT
import csv, json, hashlib

def rows(name):
 with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
 nsfc=rows('nsfc_approved_records.csv'); rd=rows('national_rd_proposed_records.csv'); proc=rows('procurement_records.csv')
 assert len(nsfc)==340 and len(rd)==40 and len(proc)==3
 totals=[]
 for year in ['2017','2018','2019']:
  part=[r for r in nsfc if r['allocation_year']==year]
  total=sum(float(r['amount_cny_10000']) for r in part)
  totals.append(dict(year=int(year),program='NSFC life sciences key projects only',rows=len(part),approved_direct_cost_cny_10000=total,mean_cny_10000=total/len(part),page_publication_date=part[0]['page_publication_date']))
 for i in range(1,3):
  totals[i]['amount_yoy_percent']=100*(totals[i]['approved_direct_cost_cny_10000']/totals[i-1]['approved_direct_cost_cny_10000']-1)
 # Validate against the 2017 page's own stated total and count, without extrapolating.
 assert totals[0]['rows']==112 and totals[0]['approved_direct_cost_cny_10000']==33500
 assert not any(r['application_date'] or r['approval_date'] for r in nsfc+rd)
 summary=dict(total_project_records=383,nsfc=totals,national_rd=[dict(source_id=source,rows=len([r for r in rd if r['source_id']==source]),funding_reported_rows=len([r for r in rd if r['source_id']==source and r['amount_cny_10000']])) for source in sorted({r['source_id'] for r in rd})],procurement=proc,clock_audit=dict(nsfc_exact_application_dates=0,nsfc_exact_approval_dates=0,national_rd_exact_application_dates=0,national_rd_exact_approval_dates=0,procurement_explicit_supplier_selection_dates=sum(bool(r['decision_date']) for r in proc),procurement_explicit_solicitation_dates=sum(bool(r['solicitation_date']) for r in proc),procurement_explicit_award_notice_dates=sum(bool(r['award_notice_date']) for r in proc),initial_research_topic_or_investment_choice_dates=0),estimand='descriptive annual approved/proposed public resources and selected public procurement notices; not applicant choice or causal signal response',files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.csv')})
 (ROOT/'behavior_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
