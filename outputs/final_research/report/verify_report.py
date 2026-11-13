"""Completeness, geometry and visual-QA artifact creation for the research PDF."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
import pdfplumber, hashlib, json, re

HERE=Path(__file__).resolve().parent
QA=HERE/'qa'
PDF=HERE/'연구보고서_최종.pdf'
source=(HERE/'연구보고서_원문.md').read_text(encoding='utf-8')
current=(HERE.parent/'report_main.md').read_text(encoding='utf-8-sig')
norm_source=lambda s:s.replace('原문','원문').replace('−','-').replace('–','-').replace('—','-').replace('\u2011','-').replace('\u2010','-')
reader=PdfReader(PDF)
chunks=[]
for n,page in enumerate(reader.pages,1):
    lines=page.extract_text().splitlines()
    if lines and lines[0]=='수출통제 신호와 중국의 선제적 연구·자본 배분':lines.pop(0)
    if lines and lines[0]=='2026년 11월 13일 · 공개자료 실증 검증':lines.pop(0)
    if lines and lines[0]==str(n):lines.pop(0)
    chunks.append('\n'.join(lines))
flat=re.sub(r'\s+','',''.join(chunks))
parts=[]
for line in source.splitlines():
    line=line.strip()
    if not line or re.fullmatch(r'\|[-:| ]+\|',line):continue
    if line.startswith('|'):parts.extend(line.strip('|').split('|'))
    else:parts.append(line.lstrip('#').strip())
missing=[]
for s in parts:
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s).replace('`','').replace('**','')
    if re.sub(r'\s+','',s) not in flat:missing.append(s)
geometry=[]
with pdfplumber.open(PDF) as doc:
    for n,page in enumerate(doc.pages,1):
        outside=[c for c in page.chars if c['x0']<51 or c['x1']>page.width-51 or c['top']<18 or c['bottom']>page.height-16]
        body=[c for c in page.chars if 45<c['top']<page.height-52]
        geometry.append({'page':n,'characters':len(page.chars),'outside_safe_area':len(outside),
            'examples':[c['text'] for c in outside[:15]],
            'body_bottom':round(max((c['bottom'] for c in body),default=0),1)})
files=[QA/f'page-{i:02d}.png' for i in range(1,len(reader.pages)+1)]
assert all(f.exists() for f in files)
cols=5;rows=(len(files)+cols-1)//cols;tw,th=236,344
canvas=Image.new('RGB',(tw*cols,th*rows),'#D9DFE4');draw=ImageDraw.Draw(canvas)
for i,path in enumerate(files):
    im=ImageOps.contain(Image.open(path),(tw-10,th-22))
    canvas.paste(im,((i%cols)*tw+5,(i//cols)*th+18))
    draw.text(((i%cols)*tw+8,(i//cols)*th+2),str(i+1),fill='black')
canvas.save(QA/'contactsheet.png')
result={'pages':len(reader.pages),'source_snapshot_current':source==norm_source(current),
    'source_sha256':hashlib.sha256(current.encode()).hexdigest(),
    'checked_source_blocks_or_cells':len(parts),'missing_source_blocks_or_cells':missing,
    'geometry':geometry,'all_pages_rendered':len(files),
    'contains_replacement_character':'\ufffd' in flat,'contains_original_typo':'原문' in flat}
(QA/'completeness.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
