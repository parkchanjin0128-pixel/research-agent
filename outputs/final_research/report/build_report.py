"""A4 Korean research report. Preserve supplied text; all figures use saved observations.

Run with bundled Python. No Office application or COM is used.
"""
from pathlib import Path
from html import escape
import csv, hashlib, json, math, re, unicodedata
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, String, Line, Rect, PolyLine, Circle
from reportlab.graphics import renderPDF
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FINAL = HERE.parent
RESCUE = ROOT/'outputs/identification_rescue_2026-11-12'
PRESENT = ROOT/'outputs/presentation_2026-11-13'
FIG = HERE/'figures'; FIG.mkdir(parents=True, exist_ok=True)
QA = HERE/'qa'; QA.mkdir(exist_ok=True)
W, H = A4
M = 53
BW = W-2*M

for name, file, kwargs in [('KR','malgun.ttf',{}),('KRB','malgunbd.ttf',{}),
                          ('CN','simsun.ttc',{'subfontIndex':0}),('SYM','seguisym.ttf',{})]:
    pdfmetrics.registerFont(TTFont(name, 'C:/Windows/Fonts/'+file, **kwargs))
pdfmetrics.registerFontFamily('KR',normal='KR',bold='KRB',italic='KR',boldItalic='KRB')
INK=colors.HexColor('#192C41'); TEAL=colors.HexColor('#087D82')
GRAY=colors.HexColor('#5A6875'); LIGHT=colors.HexColor('#E8EEF1')
ORANGE=colors.HexColor('#C27036'); PALE=colors.HexColor('#F3F6F8')
S={
'body':ParagraphStyle('body',fontName='KR',fontSize=10.5,leading=18.2,wordWrap='CJK',spaceAfter=9.2,textColor=INK,allowWidows=0,allowOrphans=0),
'title':ParagraphStyle('title',fontName='KRB',fontSize=28,leading=42,wordWrap='CJK',spaceAfter=24,textColor=INK),
'subtitle':ParagraphStyle('subtitle',fontName='KR',fontSize=15,leading=25,wordWrap='CJK',spaceAfter=20,textColor=TEAL),
'h1':ParagraphStyle('h1',fontName='KRB',fontSize=17,leading=26,wordWrap='CJK',spaceBefore=17,spaceAfter=14,textColor=INK,keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='KRB',fontSize=12.3,leading=20,wordWrap='CJK',spaceBefore=14,spaceAfter=8,textColor=INK,keepWithNext=True),
'cell':ParagraphStyle('cell',fontName='KR',fontSize=8.7,leading=14.5,wordWrap='CJK',textColor=INK),
'th':ParagraphStyle('th',fontName='KRB',fontSize=8.7,leading=14.5,wordWrap='CJK',textColor=colors.white),
'small':ParagraphStyle('small',fontName='KR',fontSize=8.5,leading=14,wordWrap='CJK',spaceAfter=8,textColor=GRAY),
'caption':ParagraphStyle('caption',fontName='KR',fontSize=8.8,leading=14.4,wordWrap='CJK',spaceAfter=13,textColor=GRAY),
'eq':ParagraphStyle('eq',fontName='KR',fontSize=10,leading=19,wordWrap='CJK',leftIndent=11,rightIndent=8,spaceBefore=8,spaceAfter=14,textColor=INK,backColor=PALE,borderPadding=9),
'ref':ParagraphStyle('ref',fontName='KR',fontSize=9.5,leading=16.8,wordWrap='CJK',spaceAfter=11,textColor=INK),
'toc':ParagraphStyle('toc',fontName='KR',fontSize=11,leading=20,wordWrap='CJK',spaceBefore=7,textColor=INK,leftIndent=0,rightIndent=18),
}
def norm(s):
    return s.replace('原문','원문').replace('−','-').replace('–','-').replace('—','-').replace('\u2011','-').replace('\u2010','-')
def fonts(s):
    # SimSun for Chinese names. Every other unsupported non-ASCII symbol gets a checked fallback.
    out=[]; current=None; run=''
    cmap=pdfmetrics.getFont('KR').face.charToGlyph
    for c in s:
        f='CN' if '\u4e00'<=c<='\u9fff' else ('KR' if ord(c) in cmap else 'SYM')
        if f!=current and run:
            out.append(escape(run) if current=='KR' else '<font name="'+current+'">'+escape(run)+'</font>');run=''
        current=f;run+=c
    if run:out.append(escape(run) if current=='KR' else '<font name="'+current+'">'+escape(run)+'</font>')
    return ''.join(out)
def inline(s):
    s=norm(s); tokens=[]
    def token(m):
        idx=len(tokens)
        if m.group(1): label,url=m.group(1),m.group(2)
        else: label=url=m.group(3)
        tokens.append('<link href="'+escape(url,quote=True)+'" color="#087D82">'+fonts(label)+'</link>')
        return '\x00'+str(idx)+'\x00'
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)|(https?://[^\s<>;]+)',token,s)
    pieces=re.split(r'(\x00\d+\x00)',s)
    out=''.join(tokens[int(p[1:-1])] if p.startswith('\x00') else fonts(p) for p in pieces)
    out=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',out)
    return out.replace('`','')
def p(s,kind='body'):return Paragraph(inline(s),S[kind])
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
official=load(PRESENT/'data/official_rd_derived.json')['annual']
original=load(RESCUE/'finegroup_pre_dose_raw.json')
recovered=load(FINAL/'family_country_recovery_raw.json')
monthly=load(RESCUE/'monthly_diagnostics.json')
with (FINAL/'empirics/simulation_pilot.csv').open(encoding='utf-8-sig',newline='') as f: sim=list(csv.DictReader(f))

def label(d,x,y,s,size=8.5,font='KR',color=INK,anchor='start'):
    d.add(String(x,y,norm(s),fontName=font,fontSize=size,fillColor=color,textAnchor=anchor))
def frame(title,subtitle,height=250):
    d=Drawing(BW,height)
    label(d,0,height-17,title,11.8,'KRB')
    label(d,0,height-35,subtitle,8.2,color=GRAY)
    return d
def axes(d,x,y,w,h,lo,hi,ticks,formatter=lambda v:f'{v:g}'):
    for v in ticks:
        yp=y+h*(v-lo)/(hi-lo)
        d.add(Line(x,yp,x+w,yp,strokeColor=LIGHT,strokeWidth=.6))
        label(d,x-9,yp-3,formatter(v),8,color=GRAY,anchor='end')
    d.add(Line(x,y,x+w,y,strokeColor=GRAY,strokeWidth=.7))
def linechart(title,subtitle,vals,lo,hi,ticks,fmt,highlight=None):
    d=frame(title,subtitle,253);x,y,w,h=46,44,BW-68,151
    axes(d,x,y,w,h,lo,hi,ticks,fmt)
    xx=lambda i:x+w*i/(len(vals)-1)
    yy=lambda v:y+h*(v-lo)/(hi-lo)
    for i,r in enumerate(official):label(d,xx(i),27,str(r['year']),8,color=GRAY,anchor='middle')
    d.add(PolyLine([a for i,v in enumerate(vals) for a in (xx(i),yy(v))],strokeColor=TEAL,strokeWidth=2.1))
    for i,v in enumerate(vals):
        d.add(Circle(xx(i),yy(v),2.5,fillColor=TEAL,strokeColor=None))
        if i in (0,len(vals)-1) or highlight and i in highlight:
            label(d,xx(i),yy(v)+9,fmt(v),8.2,'KRB',TEAL,'middle')
    return d
figures=[]
figures.append(('01_china_rd_total',linechart('그림 1. 중국의 명목 R&D 지출','단위: 십억 위안 | 공표된 연도별 명목 지출액',[r['rd_total_billion_rmb'] for r in official],0,2600,[0,500,1000,1500,2000,2500],lambda v:f'{v:,.0f}'),
    '자료: 중국 NBS·MOST·MOF, 2013-2020년 R&D 공보. 공표액을 십억 위안으로 변환했다. 국가 연간 기술통계이며 신호의 인과효과나 구조변화 검정이 아니다.'))
figures.append(('02_china_basic_share',linechart('그림 2. 기초연구 지출의 R&D 내 비중','단위: % | 2018년 5.54% → 2019년 6.03%, +0.4903%p',[r['basic_share_recomputed_pct'] for r in official],4,6.5,[4,4.5,5,5.5,6,6.5],lambda v:f'{v:.2f}',[5,6]),
    '자료: 동일 공식 공보의 기초연구 지출/총 R&D 지출에서 재계산. 명목액 비중이며 자금 결정월·기술별 배분반응을 보여 주지 않는다.'))

origrows=original['dose_rows']; recrows=recovered['rows']
known={}
for origin in ['ALL','APP']:
    oo=[r for r in origrows if r['origin']==origin];rr=[r for r in recrows if r['origin']==origin]
    known[origin]=(sum(r['pairs_any_known_country'] for r in oo),sum(r['family_known_pairs'] for r in rr),sum(r['cited_family_pairs'] for r in oo))
d=frame('그림 3. 인용쌍의 국가정보 연결 비율','분모: ALL 10,747쌍 / APP 765쌍 | 한 국가 이상 알려진 쌍',165)
x,y,w,h=63,40,BW-90,75
axes(d,x,y,w,h,0,100,[0,25,50,75,100],lambda v:f'{v:.0f}%')
for i,origin in enumerate(['ALL','APP']):
    a,b,n=known[origin];cx=x+w*(.25+.5*i)
    for j,(v,col) in enumerate([(100*a/n,INK),(100*b/n,TEAL)]):
        xp=cx+(j-.5)*48
        d.add(Rect(xp-16,y,32,h*v/100,fillColor=col,strokeColor=None))
        label(d,xp,y+h*v/100+7,f'{v:.2f}%',8.4,'KRB',col,'middle')
    label(d,cx,24,origin,9.5,'KRB',INK,'middle')
label(d,80,7,'진한색: 원 피인용 공보',8.5,color=INK)
label(d,270,7,'청록색: 사전 family 공보',8.5,color=TEAL)
figures.append(('03_country_information',d,'자료: 동일 source 표본과 인용쌍의 보존 집계. 원 공보 신청인의 국가와 family 내 사전 다른 공보의 footprint는 다른 측정대상이다. 연결률 상승은 원래 신청인의 누락국가가 모두 회수되었다는 뜻이 아니다.'))

d=frame('그림 4. 24개 기술의 미국 비중: 두 문헌 기준의 경계','ALL 인용 | 국가미상에 대한 조건부 산술 경계, 표본오차 신뢰구간 아님',450)
x,y,w,h=79,42,BW-97,340
for v in [0,.2,.4,.6,.8,1]:
    xp=x+w*v; d.add(Line(xp,y,xp,y+h,strokeColor=LIGHT,strokeWidth=.6));label(d,xp,y-17,f'{v*100:.0f}%',8,color=GRAY,anchor='middle')
lookup={r['main_group']:r for r in recrows if r['origin']=='ALL'}
oo=[r for r in origrows if r['origin']=='ALL']
for i,r in enumerate(oo):
    yy=y+h-(i+.5)*h/24; q=lookup[r['main_group']]
    if i%2==0:d.add(Rect(0,yy-h/48,BW,h/24,fillColor=PALE,strokeColor=None))
    label(d,x-8,yy-2.8,r['main_group'],8.3,anchor='end')
    for dy,lo,hi,col in [(2.4,r['b_pair_us_lower'],r['b_pair_us_upper'],INK),(-2.4,q['b_family_lower'],q['b_family_upper'],TEAL)]:
        yp=yy+dy;xl=x+w*lo;xh=x+w*hi
        d.add(Line(xl,yp,xh,yp,strokeColor=col,strokeWidth=2))
        d.add(Line(xl,yp-2,xl,yp+2,strokeColor=col,strokeWidth=.7));d.add(Line(xh,yp-2,xh,yp+2,strokeColor=col,strokeWidth=.7))
label(d,12,9,'진한색 위: 원 피인용 공보 / 청록색 아래: 같은 family의 사전 공보',8.2,color=GRAY)
figures.append(('04_technology_bounds',d,'자료: 24 main group×각 100 family의 동일 source 표본. 목록에 나타난 미상국가만 배정하는 marginal bounds이다. 신청인 명단 누락·잘못된 매칭·역사적 갱신·표본오차는 포괄하지 않는다. 두 색은 추정대상이 다르며 전체 기술순위의 식별을 뜻하지 않는다.'))

d=frame('그림 5. 다섯 IPC의 월별 상대 기울기 변화','단위: 사전 B 10%p당 국가상대 log(1+건수) | 2017년 월평균 기준',290)
vals=[monthly['results'][a]['equal_controls']['monthly_baseline_normalized_beta'] for a in ['ALL','APP']]
x,y,w,h=49,58,BW-71,172
lo=math.floor(min(min(v) for v in vals)*5)/5;hi=math.ceil(max(max(v) for v in vals)*5)/5
xx=lambda i:x+w*i/83;yy=lambda v:y+h*(v-lo)/(hi-lo)
d.add(Rect(xx(70.5),y,xx(75.5)-xx(70.5),h,fillColor=colors.HexColor('#DFECEB'),strokeColor=None))
axes(d,x,y,w,h,lo,hi,[lo+(hi-lo)*i/5 for i in range(6)],lambda v:f'{v:.2f}')
d.add(Line(x,yy(0),x+w,yy(0),strokeColor=GRAY,strokeWidth=.8))
for year in range(2013,2020):label(d,xx((year-2013)*12),39,str(year),8,color=GRAY,anchor='middle')
for v,col in zip(vals,[INK,TEAL]):d.add(PolyLine([a for i,n in enumerate(v) for a in (xx(i),yy(n))],strokeColor=col,strokeWidth=1.25))
label(d,BW-85,272,'ALL',8.8,'KRB',INK);label(d,BW-41,272,'APP',8.8,'KRB',TEAL)
label(d,0,18,'음영: 2018-12~2019-04 후보 요약창. 인과·청정 의사결정창으로 검증되지 않음.',8.1,color=GRAY)
figures.append(('05_monthly_beta',d,'자료: EPO PATSTAT의 C12N·G01S·G06F·G06N·H01L, 5국, 84개월. 비교국은 US·JP·KR·DE의 동일가중 평균이다. 사전 의존도는 효과수정변수 후보다. 선은 선정된 국제출원 표본의 기술통계이며 정책효과나 중국 R&D 지출 변화가 아니다.'))

d=frame('그림 6. 잔차모형에 따른 조건부 80% MDE','원 잔차규모(1.0) | 단위: 로그단위/10%p B, 양·음 방향 모두 80% 검정력',282)
ss=[r for r in sim if float(r['residual_scale'])==1]
model_names={'circular_moving_block12':'12개월 원형 block','gaussian_AR1_rho0':'Gaussian AR(1), ρ=0','gaussian_AR1_rho0.5':'Gaussian AR(1), ρ=0.5','gaussian_AR1_rho0.8':'Gaussian AR(1), ρ=0.8'}
models=list(dict.fromkeys(r['noise_model'] for r in ss))
x,y,w,h=168,53,BW-190,164
for v in [0,.1,.2,.3,.4]:
    xp=x+w*v/.4;d.add(Line(xp,y,xp,y+h,strokeColor=LIGHT,strokeWidth=.6));label(d,xp,34,f'{v:.1f}',8,color=GRAY,anchor='middle')
for i,model in enumerate(models):
    yp=y+h-(i+.5)*h/len(models)
    label(d,x-10,yp-3,model_names.get(model,model),8.5,anchor='end')
    for j,origin in enumerate(['ALL','APP']):
        r=next(r for r in ss if r['noise_model']==model and r['definition']==origin)
        v=float(r['MDE80_log_per10pp_both_directions']);dy=4 if j==0 else -5;col=INK if j==0 else TEAL
        d.add(Line(x,yp+dy,x+w*v/.4,yp+dy,strokeColor=col,strokeWidth=3.7))
        label(d,x+w*v/.4+5,yp+dy-3,f'{v:.4f}',8,color=col)
label(d,0,14,'진한색: ALL / 청록색: APP. 조건부 정상 잔차·고정 B; 실제 정책효과의 MDE 아님.',8.1,color=GRAY)
figures.append(('06_conditional_mde',d,'자료: 실제 잔차에 보정한 8개 기본모형×3 잔차배율의 simulation 중 원 잔차배율을 표시. 추세·계절 추정불확실성, B 오차, 표본선택, 새 정책충격과 연구결정 시차는 포함하지 않았다. MDE는 로그단위이며 % 또는 %p가 아니다.'))

for name,d,caption in figures:renderPDF.drawToFile(d,str(FIG/(name+'.pdf')))

source=(FINAL/'report_main.md').read_text(encoding='utf-8-sig')
text=norm(source)
(HERE/'연구보고서_원문.md').write_text(text,encoding='utf-8')
lines=text.splitlines()
title=lines[0][2:]
subtitle=next(l[3:] for l in lines if l.startswith('## '))
cover_intro=next(l for l in lines if l.startswith('작성일'))

class ResearchDoc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=51,bottomMargin=53,
            title=title,author='공개자료 실증 연구',subject=subtitle,allowSplitting=1)
        self.addPageTemplates(PageTemplate(id='main',frames=[Frame(M,53,BW,H-104,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.decorate))
        self.section_pages={}
    def decorate(self,canvas,doc):
        canvas.saveState()
        if doc.page>1:
            canvas.setFillColor(GRAY);canvas.setFont('KR',7.4)
            canvas.drawString(M,H-29,'수출통제 신호와 중국의 선제적 연구·자본 배분')
            canvas.setStrokeColor(LIGHT);canvas.setLineWidth(.6);canvas.line(M,H-35,W-M,H-35)
        canvas.setStrokeColor(LIGHT);canvas.line(M,39,W-M,39)
        canvas.setFont('KR',7.6);canvas.setFillColor(GRAY)
        canvas.drawString(M,25,'2026년 11월 13일 · 공개자료 실증 검증')
        canvas.drawRightString(W-M,25,str(doc.page))
        canvas.restoreState()
    def afterFlowable(self,f):
        if hasattr(f,'toc_key'):
            self.canv.bookmarkPage(f.toc_key)
            self.canv.addOutlineEntry(f.getPlainText(),f.toc_key,level=0,closed=False)
            self.notify('TOCEntry',(0,f.toc_label,self.page,f.toc_key))
            self.section_pages[f.getPlainText()]=self.page

class AtomicTable(Table):
    """All five source tables fit one page; preserve complete tables and preceding headings."""
    def split(self,availWidth,availHeight):return []

toc_start=next(i for i,l in enumerate(lines) if l=='## 목차')
body_start=next(i for i,l in enumerate(lines) if l=='## 1. 연구질문과 기여')
toc_labels=[l.strip() for l in lines[toc_start+1:body_start] if l.strip()]
toc=TableOfContents();toc.levelStyles=[S['toc']];toc.dotsMinLevel=0
story=[Spacer(1,80),p('연구보고서','small'),p(title,'title'),p(subtitle,'subtitle'),
       Spacer(1,21),p(cover_intro,'body'),Spacer(1,31),
       p('특허 · 조달 · 규제 원문 · 조건부 계량 진단','small'),PageBreak()]
abs_start=next(i for i,l in enumerate(lines) if l=='## 초록')
story.append(p('초록','h1'))
for line in lines[abs_start+1:toc_start]:
    if line.strip():story.append(p(line.strip()))
story += [PageBreak(),p('목차','h1'),toc,PageBreak()]

def addfig(index):
    name,d,caption=figures[index]
    story.append(KeepTogether([d,Spacer(1,5),p(caption,'caption')]))
def heading(value,level):
    q=p(value,'h1' if level==2 else 'h2')
    if level==2:
        q.toc_key='section_'+str(len([f for f in story if hasattr(f,'toc_key')]))
        prefix=re.match(r'(\d+\.|부록 [ABC]\.)',value)
        q.toc_label=next((t for t in toc_labels if (prefix and t.startswith(prefix[1])) or t==value),value)
    story.append(q)

table_count=0; table_meta=[]; paragraphs=[]
i=body_start
while i<len(lines):
    line=lines[i].strip()
    if not line:i+=1;continue
    if line.startswith('#'):
        level=len(line)-len(line.lstrip('#'));value=line[level:].strip()
        if value.startswith('6. 사전'):addfig(0);addfig(1)
        if value.startswith('6.3'):addfig(2);addfig(3)
        if value.startswith('7.2'):addfig(4)
        if value.startswith('8. 직접'):addfig(5)
        if value.startswith('부록 A.') or value=='참고문헌과 1차자료':story.append(PageBreak())
        heading(value,level);i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[v.strip() for v in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[:\-\s]+',c) for c in cells):rows.append(cells)
            i+=1
        nc=len(rows[0]);assert all(len(r)==nc for r in rows)
        if nc==4:widths=[85,125,119,BW-329]
        elif nc==3:widths=[BW*.51,BW*.245,BW*.245] if table_count in (1,2) else [BW*.29,BW*.39,BW*.32]
        else:widths=[BW/nc]*nc
        t=AtomicTable([[p(c,'th' if j==0 else 'cell') for c in row] for j,row in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
            ('LINEBELOW',(0,0),(-1,0),.7,INK),('LINEBELOW',(0,-1),(-1,-1),.7,LIGHT),
            ('INNERGRID',(0,1),(-1,-1),.35,LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
        story.extend([t,Spacer(1,13)]);table_meta.append({'rows':len(rows),'columns':nc});table_count+=1;continue
    is_ref=any(getattr(f,'toc_label','')=='참고문헌과 1차자료' for f in story)
    block=[line];i+=1
    while not is_ref and i<len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#','|')):
        block.append(lines[i].strip());i+=1
    value=' '.join(block);paragraphs.append(value)
    if value.startswith('Y_ckt ='):
        # Exact source expression, only line breaks are introduced. No equation substitution.
        parts=value.split(' + ')
        display=' + '.join(parts[:4])+'<br/>+ '+' + '.join(parts[4:-2])+'<br/>+ '+' + '.join(parts[-2:])
        story.append(Paragraph(inline(display).replace('&lt;br/&gt;','<br/>'),S['eq']))
    else:story.append(p(value,'ref' if is_ref else 'body'))

out=HERE/'연구보고서_최종.pdf'
doc=ResearchDoc(out);doc.multiBuild(story)
reader=PdfReader(out)
extracted='\n'.join(page.extract_text() for page in reader.pages)
(QA/'pdf_extracted_text.txt').write_text(extracted,encoding='utf-8')
unsupported=[]
for c in sorted(set(text)):
    if c.isspace():continue
    f='CN' if '\u4e00'<=c<='\u9fff' else ('KR' if ord(c) in pdfmetrics.getFont('KR').face.charToGlyph else 'SYM')
    if ord(c) not in pdfmetrics.getFont(f).face.charToGlyph:unsupported.append({'char':c,'unicode':f'U+{ord(c):04X}','font':f})
inputs=[FINAL/'report_main.md',PRESENT/'data/official_rd_derived.json',RESCUE/'finegroup_pre_dose_raw.json',FINAL/'family_country_recovery_raw.json',RESCUE/'monthly_diagnostics.json',FINAL/'empirics/simulation_pilot.csv']
manifest={'pdf':str(out),'pages':len(reader.pages),'source_characters':len(source),'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
          'source_policy':'All supplied paragraphs, table cells and references retained; 原문→원문 and dash normalization only. Markdown links stay clickable. TOC labels retained and page numbers generated.',
          'figures':[{'file':name+'.pdf','caption':cap} for name,d,cap in figures],
          'tables':table_meta,'section_pages':doc.section_pages,'unsupported_source_glyphs':unsupported,
          'hyperlink_count':sum(len(page.get('/Annots',[])) for page in reader.pages),
          'inputs_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
          'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(QA/'build_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(out),'pages':len(reader.pages),'unsupported_glyphs':unsupported,'figures':len(figures),'links':manifest['hyperlink_count'],'section_pages':doc.section_pages},ensure_ascii=False))
