"""Reproduce the four additional logged archive pages used to locate original tenders.
Run after archive_probe.py and before finalize_archive.py. 36+4=40 archive documents.
"""
from archive_probe import ROOT,get,logs
import json
def main():
 base=json.loads((ROOT/'archive_probe_summary.json').read_text(encoding='utf-8'))
 logs.extend(base['logs']); start=len(logs); records=[]
 for page in [215,225,219,220]:
  rows,meta=get(f'https://zbpt.njust.edu.cn/cgxx/index_{page}.jhtml',f'cgxx_{page}')
  records+=rows
 (ROOT/'archive_followup_probe.json').write_text(json.dumps(dict(logs=logs[start:],records=records),ensure_ascii=False,indent=2),encoding='utf-8')
 print({'additional_documents':len(logs)-start,'records':len(records)})
if __name__=='__main__':main()
