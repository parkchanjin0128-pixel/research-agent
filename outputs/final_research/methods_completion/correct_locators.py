from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;hist=HERE/'history_before_locator_correction';hist.mkdir(exist_ok=True)
paths=[HERE/'precedents.md',HERE/'precedents.json',HERE/'source_manifest.json'];old={}
for p in paths:
 b=p.read_bytes();(hist/p.name).write_bytes(b);old[p.name]=hashlib.sha256(b).hexdigest()
replacements={'§§2.1–2.4·3.1–3.2':'§§2.1–2.4·3.1(#S8), 식(3)#FD3','§3.2·식(3)':'§3.1(#S8)·식(3,#FD3)','3.2; equations: 3; tables: 2, 3':'3.1 (#S8); equations: 3 (#FD3); tables: 2, 3','Blume §§2.2·3.2':'Blume §§2.2·3.1(#S8)','실증 postTWEA=1918년 이후.':'실증 postTWEA=after 1918, 즉1919년부터.'}
def walk(x):
 if isinstance(x,dict):
  out={k:walk(v) for k,v in x.items()}
  if out.get('claim')=='시기별회귀·추론' and out.get('section')=='3.2':out['section']='3.1';out['html_anchors']=['#S8','#FD3']
  return out
 if isinstance(x,list):return [walk(v) for v in x]
 if isinstance(x,str):
  for a,b in replacements.items():x=x.replace(a,b)
 return x
for p in paths:
 if p.suffix=='.json':s=json.dumps(walk(json.loads(p.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)+'\n'
 else:s=walk(p.read_text(encoding='utf-8'))
 p.write_text(s,encoding='utf-8')
receipt={'author':'/root','scope':'verifier locator finding correction, no estimand or scientific conclusion change','old_sha256':old,'new_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'Blume_correction':'equation3/Tables2–3 in section3.1 #S8; equation #FD3; not nonexistent3.2','Moser_precision':'after1918 means1919 onward','independent_recheck':'pending'}
(HERE/'locator_correction_nov13.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
