"""Local-only original-source backup; never upload this archive to public GitHub."""
from pathlib import Path
import hashlib,json,zipfile
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
paths=[p for p in HERE.rglob('*') if p.is_file() and not any(s.startswith('.') or s=='__pycache__' for s in p.relative_to(HERE).parts) and p.name not in ('local_backup_receipt.json','release_receipt.json')]
paths += [p for p in (ROOT/'outputs/identification_rescue_2026-11-12').iterdir() if p.is_file() and p.suffix in {'.md','.json','.py','.sql'}]
paths += [p for p in (ROOT/'outputs/presentation_2026-11-13/data').iterdir() if p.is_file()]
manifest={str(p.relative_to(ROOT)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(paths))}
provided=[];seen=set()
for name in ['ssrn-5373282.pdf','ssrn-5373282 (1).pdf','ssrn-6210408.pdf','ssrn-7042518.pdf','1-s2.0-S0304387825001506-main.pdf','1-s2.0-S0048733325001404-main.pdf','1-s2.0-S1057521924004423-main.pdf','1-s2.0-S026156062400216X-main.pdf']:
 p=Path.home()/'Downloads'/name
 if not p.exists():continue
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if h in seen:continue
 seen.add(h);arc='private_provided_pdfs/'+name;provided.append((p,arc));manifest[arc]={'bytes':p.stat().st_size,'sha256':h}
zpath=ROOT/'outputs/연구_원자료포함_로컬백업_2026-11-13.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in sorted(set(paths)):z.write(p,str(p.relative_to(ROOT)).replace('\\','/'))
 for p,arc in provided:z.write(p,arc)
 z.writestr('LOCAL_BACKUP_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2))
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for name,m in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==m['sha256']
receipt={'generated_utc':datetime.now(timezone.utc).isoformat(),'local_only':True,'name':zpath.name,'bytes':zpath.stat().st_size,'sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'verified_original_files':len(manifest),'provided_unique_pdfs':len(provided),'copyrighted_and_primary_source_fulltexts_not_for_publication':True}
(HERE/'local_backup_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
