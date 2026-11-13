"""Read primary cached PDFs/HTML afresh; never use producer text extractions."""
from pathlib import Path
import argparse, hashlib, json, sys
from pypdf import PdfReader
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / 'outputs/final_research/methods_completion/sources'

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser()
    p.add_argument('source')
    p.add_argument('--pages',nargs='*',type=int,default=[])
    p.add_argument('--anchors',nargs='*',default=[])
    a=p.parse_args()
    f=(ROOT/'work/stage3'/(a.source+'.pdf')) if a.source in ('pierce2016','cgbs2024') else SRC/(a.source+('.html' if a.source=='blume2013' else '.pdf'))
    meta={'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    if f.suffix=='.pdf':
        r=PdfReader(f);meta['pdf_pages']=len(r.pages);print(json.dumps(meta))
        for n in a.pages:
            print(f'\n--- {f.name} PDF page {n} ---\n'+(r.pages[n-1].extract_text() or ''))
    else:
        s=BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser');print(json.dumps(meta))
        if a.anchors:
            for ident in a.anchors:
                e=s.find(id=ident)
                print(f'\n--- HTML #{ident} ---\n'+(e.get_text(' ',strip=True) if e else 'ANCHOR NOT FOUND'))
        else:
            article=s.find('article') or s
            print(article.get_text(' ',strip=True))

if __name__=='__main__':main()
