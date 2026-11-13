"""행동자료 독립 검산. 원 생산자의 추출 함수를 호출하지 않는다."""
from pathlib import Path
from html.parser import HTMLParser
from decimal import Decimal
from urllib.parse import urlsplit, urlunsplit, urljoin
from collections import Counter
import csv
import datetime
import hashlib
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'outputs/final_research/behavior_data'
OUT = ROOT / 'outputs/final_research/verification'

def load(name):
    return json.loads((BASE / name).read_text(encoding='utf-8-sig'))

def records(name):
    with (BASE / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

class TableRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.row = []
        if tag in ('td', 'th') and self.row is not None: self.cell = []
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(norm(''.join(self.cell)))
            self.cell = None
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None

def main():
    summary, sources = load('behavior_summary.json'), load('sources.json')
    manifest = {x['id']: x for x in sources}
    nsfc, rd = records('nsfc_approved_records.csv'), records('national_rd_proposed_records.csv')
    hashes = {}
    for name, expected in summary['files'].items():
        hashes[name] = sha(BASE / name)
        assert hashes[name] == expected
    for x in sources:
        assert sha(BASE / x['local']) == x['sha256']
    nsfc_result = []
    for year, expected_n, expected_amount, expected_date in [(2017,112,33500,'2017-10-10'),(2018,113,32300,'2020-04-01'),(2019,115,34500,'2020-04-02')]:
        source = manifest[f'nsfc_life_key_{year}']
        html = (BASE / source['local']).read_text(encoding='utf-8-sig')
        if year == 2017:
            plain = re.sub(r'<[^>]+>', '', html)
            assert '接收重点项目申请537项' in plain
            assert '受理499项' in plain and '推荐150项重点项目上会答辩' in plain
        parser = TableRows(); parser.feed(html)
        rows = [x for x in parser.rows if len(x) == 6 and x[0].isdigit() and re.fullmatch(r'\d{10}', x[1])]
        assert len(rows) == expected_n
        assert [int(x[0]) for x in rows] == list(range(1, expected_n+1))
        assert len({x[1] for x in rows}) == expected_n
        total = sum(Decimal(x[5].replace(',','')) for x in rows)
        assert total == expected_amount
        assert re.search(r'日期：\s*<span>\s*' + expected_date, html)
        tab = [x for x in nsfc if x['allocation_year'] == str(year)]
        assert len(tab) == expected_n
        assert sum(Decimal(x['amount_cny_10000']) for x in tab) == total
        lookup = {x['project_id']: x for x in tab}
        for x in rows:
            t = lookup[x[1]]
            assert norm(t['title']) == x[2] and norm(t['organization']) == x[4]
            assert Decimal(t['amount_cny_10000']) == Decimal(x[5])
            assert int(t['row_number']) == int(x[0]) and t['page_publication_date'] == expected_date
            assert not t['application_date'] and not t['approval_date']
        nsfc_result.append({'연도':year,'승인행':len(rows),'직접경비_만위안':float(total),'페이지게시일':expected_date,'원HTML과CSV_대조':True,'원문해시':source['sha256'],'공식URL':source['url']})
    assert len(nsfc) == len({x['project_id'] for x in nsfc}) == 340
    nsfc_result[1]['전년대비_금액증감률_퍼센트'] = float((Decimal(32300)/Decimal(33500)-1)*100)
    nsfc_result[2]['전년대비_금액증감률_퍼센트'] = float((Decimal(34500)/Decimal(32300)-1)*100)
    rd_result = []
    for sid, count, expected_amount, program in [('rd_transformative_2017',13,35166,'변혁기술 핵심 과학문제'),('rd_hpc_2018',4,3859,'고성능계산'),('rd_transformative_2019',23,None,'변혁기술 핵심 과학문제')]:
        source = manifest[sid]
        pdf = PdfReader(BASE / source['local'])
        text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
        ids = re.findall(r'20\d{2}YF[A-Z]\d{7}', text)
        tab = [x for x in rd if x['source_id'] == sid]
        assert len(ids) == len(set(ids)) == len(tab) == count
        assert set(ids) == {x['project_id'] for x in tab}
        assert '拟立项' in text
        assert ('高性能计算' in text) if sid == 'rd_hpc_2018' else ('变革性技术关键科学问题' in text)
        if expected_amount is None:
            assert all(not x['amount_cny_10000'] for x in tab)
            assert '中央财政经费' not in text
        else:
            assert sum(Decimal(x['amount_cny_10000']) for x in tab) == expected_amount
            if sid.endswith('2017'):
                money = [Decimal(x) for x in re.findall(r'\b\d{4}\.00\b', text)]
            else:
                money = [Decimal(x) for x in re.findall(r'\s(\d{3,4})\s+3年', text)]
            assert len(money) == count and sum(money) == expected_amount
        assert all(not x['application_date'] and not x['approval_date'] and not x['page_publication_date'] for x in tab)
        rd_result.append({'자료ID':sid,'목록연도':source['year'],'프로그램':program,'상태':'선정 예정 공시','행수':count,'예정중앙재정_만위안':expected_amount,'PDF쪽수':len(pdf.pages),'원PDF와CSV_ID대조':True,'공식URL':source['url']})
    assert len(rd) == 40
    assert len(records('procurement_records.csv')) == 3
    assert summary['total_project_records'] == len(nsfc) + len(rd) + 3 == 383
    archive = load('archive_final_summary.json')
    protocol = load('archive_protocol.json')
    inventory = records('archive_final_2016_2019_inventory.csv')
    candidates = records('archive_final_keyword_candidates.csv')
    raw_rows = []
    preserved = []
    for log in archive['logs']:
        path = BASE / log['retained']
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        preserved.append({'파일':log['retained'],'보존파일SHA256':sha(path),'원HTML_SHA256_기록':log['html_text_sha256'],'보존형식':'추출 배열; 전체 HTML 아님'})
        for x in data:
            if 'szu' in log['label']:
                url = urljoin(log['url'], x['url']['asString'])
                date, title = x['date'][:10], norm(x['showTitle'])
                inst, category = '深圳大学', log['label']
            else:
                q = urlsplit(x['original_href'])
                url = urlunsplit(('https', q.hostname, q.path, q.query, q.fragment))
                date, title = x['date'], norm(x['title'])
                inst, category = '南京理工大学', 'cgxx' if '/cgxx/' in log['url'] else 'cjgg'
            raw_rows.append(dict(institution=inst,category=category,date=date,title=title,url=url,archive_url=log['url']))
    merged = list({(x['category'],x['url']):x for x in raw_rows}.values())
    period = [x for x in merged if protocol['period'][0] <= x['date'] <= protocol['period'][1]]
    def compare_key(x):
        return tuple(norm(x[k]) for k in ['institution','category','date','title','url'])
    assert {compare_key(x) for x in period} == {compare_key(x) for x in inventory}
    filtered = [x for x in period if re.search(protocol['title_screen_regex'], x['title'], re.I)]
    assert {compare_key(x) for x in filtered} == {compare_key(x) for x in candidates}
    inst = Counter(x['institution'] for x in inventory)
    cand_inst = Counter(x['institution'] for x in candidates)
    assert len(archive['logs']) == len({x['url'] for x in archive['logs']}) == 40
    assert len(merged) == 15590 and len(period) == len(inventory) == 7120 and len(candidates) == 112
    assert inst == archive['institution_counts'] and cand_inst == archive['candidate_institution_counts']
    assert inst['深圳大学'] == 6806 and inst['南京理工大学'] == 314
    assert cand_inst['深圳大学'] == 104 and cand_inst['南京理工大学'] == 8
    ids = [m.group() for x in candidates if x['institution']=='深圳大学' for m in re.finditer(r'SZUCG\d+[A-Z]*', x['title'])]
    archive_result = {'원목록문서':40,'현재목록_분류URL행':15590,'기간내행':7120,'제목후보행':112,'기관별행':{'선전대학교':inst['深圳大学'],'난징이공대학교':inst['南京理工大学']},'기관별후보행':{'선전대학교':cand_inst['深圳大学'],'난징이공대학교':cand_inst['南京理工大学']},'전체고유URL':len({x['url'] for x in inventory}),'후보고유URL':len({x['url'] for x in candidates}),'전체중복URL행':len(inventory)-len({x['url'] for x in inventory}),'후보중복URL행':len(candidates)-len({x['url'] for x in candidates}),'선전후보제목의_식별가능고유사업번호':len(set(ids)),'전체프로젝트수':'미확정','보존배열_재구성대조':True,'원래모집단_완전성':False,'원문보존_한계':preserved}
    lineage = load('lineage_sources.json')
    checks = [('szu_20180519_tender','2018/11/16 17:00:00','560,000.00'),('szu_20180519_change','2018/11/23 14:28:00','1.2、1.3'),('szu_20180519_award','2018/11/28 10:59:00','555800')]
    lineage_result = []
    for sid, date, fact in checks:
        x = next(x for x in lineage if x['id']==sid)
        text = (BASE / x['retained']).read_text(encoding='utf-8-sig')
        assert date in text and fact in text and not x['missing_patterns']
        lineage_result.append({'자료ID':sid,'게시시각_표기그대로':date,'확인사실':fact,'공식URL':x['url'],'보존형식':'사실 발췌; 원HTML 전문 아님','원HTML_SHA256_생산자기록':x['html_text_sha256'],'발췌파일SHA256':sha(BASE/x['retained'])})
    for name in ['behavior_findings.md','behavior_summary.json','sources.json','lineage_sources.json','archive_final_summary.json','archive_protocol.json']:
        hashes[name] = sha(BASE/name)
    result = {'검증일':'2026-11-13','생성UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'독립성':'원 생산자는 다른 에이전트이며, 검증자는 본 자료와 추출코드를 작성하지 않았다. 생산자 자체 검산을 독립 검증 횟수로 세지 않는다.','입력해시':hashes,'NSFC':nsfc_result,'NSFC2017_공식서두집계':{'신청':537,'접수':499,'답변심사추천':150,'승인':112,'해석':'한 프로그램 한 해의 총계가 존재한다. 미승인 개별 신청자료와 신청시점은 확보되지 않았다.'},'국가중점RD':rd_result,'아카이브':archive_result,'연결사례':lineage_result,'독립온라인확인':{'NSFC3페이지':'웹 도구로 공식 제목과 게시일 확인','선전원입찰':'웹 도구로 공식 게시시각 확인','선전변경':{'HTTP':200,'응답바이트':67285,'응답SHA256':'0427faeb2d3fb2cc5ec65aa4088458b2846ecf83c1d0fad71fc7d6602fdd1813','날짜확인':'2018/11/23 14:28:00'},'선전낙찰':{'HTTP':200,'응답바이트':57442,'응답SHA256':'d53a60b68cfa15f21a162f4733d661a72c4eb898307f2a41054a46c1f30ac4dd','날짜확인':'2018/11/28 10:59:00','금액위안':555800},'ANPRM':'GovInfo 원문에서 2018-11-16 08:45 filed 표시 확인','원문전체보존':'이번 온라인 응답 전체는 파일로 보존하지 않고 선택 사실과 해시를 도구 기록에 남겼다.'},'시계해석':'웹 게시시각 자체의 시간대는 미기재다. 개찰의 베이징 시간 표기를 웹 게시시각에 자동 적용하지 않는다. ANPRM 선공개도 11월16일이므로 달력 날짜만으로 신호 전이라고 확정할 수 없다.','미수행':['아카이브 원래 모집단 전수성 확인','모든 공식페이지의 재다운로드','미승인 개별 신청자료 확보','최초 연구·투자결정일 확인','개별 장비의 법적 규제 적용 판정','신호의 인과효과 추정'],'판정':'보존 표·원HTML/PDF와 주요 집계 재현. 자료는 승인·선정예정·공고 단계의 탐색 표본이며 전체 신청수요 또는 정책효과를 입증하지 않는다.','검산':'모든 assertion 통과'}
    (OUT/'behavior_nov13.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'검산':result['검산'],'NSFC':nsfc_result,'국가RD':rd_result,'아카이브':{k:v for k,v in archive_result.items() if k!='원문보존_한계'}},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
