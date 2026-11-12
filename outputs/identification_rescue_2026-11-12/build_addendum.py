"""Render the additional empirical memo, retaining explicit identification limits."""
from pathlib import Path
from html import escape
import json,re,math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.graphics.shapes import Drawing,Line,PolyLine,Rect,String

HERE=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('KR','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('KRB','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('KR',normal='KR',bold='KRB',italic='KR',boldItalic='KRB')
navy=colors.HexColor('#17324D'); teal=colors.HexColor('#007F78'); orange=colors.HexColor('#C47429')
styles={
 'body':ParagraphStyle('body',fontName='KR',fontSize=9.6,leading=16.3,wordWrap='CJK',spaceAfter=7,textColor=navy),
 'title':ParagraphStyle('title',fontName='KRB',fontSize=23,leading=33,wordWrap='CJK',spaceAfter=17,textColor=navy),
 'heading':ParagraphStyle('heading',fontName='KRB',fontSize=14,leading=21,wordWrap='CJK',spaceBefore=12,spaceAfter=8,textColor=navy,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='KR',fontSize=8.3,leading=13,wordWrap='CJK',textColor=navy),
 'small':ParagraphStyle('small',fontName='KR',fontSize=8,leading=12,wordWrap='CJK',spaceAfter=6,textColor=navy)
}
def inline(s):
 s=s.replace('−','-').replace('–','-').replace('—','-')
 s=escape(s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<link href="'+m[2]+'" color="#007F78">'+m[1]+'</link>' if m[2].startswith('https://') else m[1],s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
 return s.replace(chr(96),'')
def para(s,style='body'):return Paragraph(inline(s),styles[style])
d=json.loads((HERE/'monthly_diagnostics.json').read_text(encoding='utf-8'))
def chart():
 drawing=Drawing(490,275); x0,y0,w,h=48,55,420,168
 vals=[d['results'][a]['equal_controls']['monthly_baseline_normalized_beta'] for a in ['ALL','APP']]
 lo=math.floor(min(min(v) for v in vals)*5)/5; hi=math.ceil(max(max(v) for v in vals)*5)/5
 def xx(i):return x0+w*i/83
 def yy(v):return y0+h*(v-lo)/(hi-lo)
 drawing.add(String(0,256,'月別相対活動のdose傾斜' if False else '월별 상대활동의 의존도 기울기 변화',fontName='KRB',fontSize=12,fillColor=navy))
 drawing.add(String(0,238,'기준: 2017년 평균 / 미국연결 10%p당 상대 log(1+건수) 변화',fontName='KR',fontSize=8,fillColor=navy))
 drawing.add(Rect(xx(70.5),y0,xx(75.5)-xx(70.5),h,fillColor=colors.HexColor('#EAF1F4'),strokeColor=None))
 for j in range(6):
  v=lo+(hi-lo)*j/5; ypos=yy(v)
  drawing.add(Line(x0,ypos,x0+w,ypos,strokeColor=colors.HexColor('#D8E1E8'),strokeWidth=.5))
  drawing.add(String(4,ypos-3,f'{v:.2f}',fontName='KR',fontSize=8,fillColor=navy))
 drawing.add(Line(x0,yy(0),x0+w,yy(0),strokeColor=navy,strokeWidth=.8))
 for year in range(2013,2020):
  xp=xx((year-2013)*12); drawing.add(String(xp-8,35,str(year),fontName='KR',fontSize=8,fillColor=navy))
 for v,col in zip(vals,[navy,teal]):
  drawing.add(PolyLine([p for i,a in enumerate(v) for p in (xx(i),yy(a))],strokeColor=col,strokeWidth=1.2))
 drawing.add(String(365,256,'ALL',fontName='KRB',fontSize=9,fillColor=navy))
 drawing.add(String(420,256,'APP',fontName='KRB',fontSize=9,fillColor=teal))
 drawing.add(String(0,14,'음영: 2018-12~2019-04 후보창. 실제 제한 전 의사결정창으로 검증되지 않음.',fontName='KR',fontSize=8,fillColor=navy))
 return drawing

story=[]; lines=(HERE/'overview.md').read_text(encoding='utf-8').splitlines()
lines += ['---PAGEBREAK---']+(HERE/'finegroup_progress.md').read_text(encoding='utf-8').splitlines()
i=0; inserted=False
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line=='---PAGEBREAK---':story.append(PageBreak())
 elif line.startswith('# '):story.append(para(line[2:],'title'))
 elif line.startswith('## '):
  story.append(para(line[3:],'heading'))
  if line.startswith('## 4.') and not inserted:
   story.insert(len(story)-1,chart()); story.insert(len(story)-1,Spacer(1,12)); inserted=True
 elif line.startswith('|'):
  block=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   row=[c.strip() for c in lines[i].strip().strip('|').split('|')]
   if not all(re.fullmatch(r':?-+:?',s) for s in row):block.append([para(c,'cell') for c in row])
   i+=1
  table=Table(block,colWidths=[255,115,115],repeatRows=1,hAlign='LEFT')
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF1F4')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#D5DFE6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
  story += [table,Spacer(1,10)];continue
 else:story.append(para(line))
 i+=1

def footer(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#D8E1E8'));canvas.line(48,37,A4[0]-48,37)
 canvas.setFont('KR',8);canvas.setFillColor(navy)
 canvas.drawString(48,24,'2026-11-12 추가 실증 진단 | 인과효과 입증 및 주설계 채택 아님')
 canvas.drawRightString(A4[0]-48,24,str(doc.page))
target=HERE/'추가실증검증_방법론검토.pdf'
SimpleDocTemplate(str(target),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=49,title='수출통제 신호 연구: 추가 실증 진단과 식별 경로',author='연구 작업 보고').build(story,onFirstPage=footer,onLaterPages=footer)
from pypdf import PdfReader
reader=PdfReader(target)
assert all(p.extract_text().strip() for p in reader.pages)
print(json.dumps({'pdf':str(target),'pages':len(reader.pages),'bytes':target.stat().st_size},ensure_ascii=False))
