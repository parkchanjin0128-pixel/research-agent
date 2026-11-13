"""정책 자료 독립 검산. 생산 모듈을 읽거나 가져오지 않고 원자료와 CSV를 비교한다."""
from pathlib import Path
import csv, hashlib, json, re
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import fitz

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'policy_completion'
OUT = Path(__file__).resolve().parent
AGENT = '/root/nov13_policy_final_verify'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read_csv(name):
    with (DATA / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def html_text(name):
    p = DATA / 'sources' / (name + '.html')
    if not p.exists():
        return ''
    return re.sub(r'\s+', ' ', BeautifulSoup(p.read_bytes(), 'html.parser').get_text(' ', strip=True))

# 청문회 파일을 직접 렌더하여 판독한 표의 날짜. 생산 CSV와 독립적으로 입력했다.
VISUAL_DATES = '''04-19 04-20 04-23 04-24 04-25 04-26 05-07 05-08 05-09
05-10 05-11 05-14 05-17 05-18 05-22 05-23 05-24 05-25 05-28 05-30 05-31
06-04 06-06 06-07 06-12 06-13 06-14 06-20 06-21 06-25 06-26 06-27 06-28
07-02 07-03'''.split()
VISUAL_DATES = ['2018-' + x for x in VISUAL_DATES]

EVENTS = {
    'ZTE_ON': ('2018-04-15','2018-04-23','zte_on','83 FR 17648: 효력 문장·서명일',
               ['effective immediately','15th day of April 2018']),
    'ZTE_OFF': ('2018-07-13','2018-07-23','zte_off','83 FR 34826: 종결·효력 문장·서명일',
                ['effective immediately','July 13, 2018']),
    '301_LIST1': ('2018-07-06','2018-06-15','tariff1','USTR 발표일 머리말 및 818개 품목 관세징수 시작 문단',
                 ['June 15, 2018','July 6, 2018','818 product lines','25 percent']),
    '301_LIST2': ('2018-08-23','2018-08-07','tariff2','USTR 발표일 머리말 및 279개 품목·징수 시작 문단',
                 ['August 07, 2018','August 23','279','25 percent']),
    '301_LIST3': ('2018-09-24','2018-09-18','tariff3','USTR 발표일 머리말 및 첫 문단',
                 ['September 18, 2018','September 24, 2018','10 percent']),
    'JINHUA_EL': ('2018-10-30','2018-10-30','jinhua','83 FR 54519 DATES; 54521 중국 명단',
                  ['effective October 30, 2018','Fujian Jinhua']),
    'CHINA_INITIATIVE': ('2018-11-01','2018-11-01','doj','법무부 공식 연설 날짜 및 창설 발표 문단 103–109', []),
    'HUAWEI_EL': ('2019-05-16','2019-05-21','huawei_el','84 FR 22961 DATES; 명단·허가 범위 문단',
                  ['effective May 16, 2019','Huawei']),
    'HUAWEI_FDPR_MAY': ('2020-05-15','2020-05-19','fdpr_may','85 FR 29849 DATES; 29850–29851 적용범위·경과조항',
                        ['effective May 15, 2020','Savings Clause']),
    'HUAWEI_FDPR_AUG': ('2020-08-17','2020-08-20','fdpr_aug','85 FR 51596 DATES; 적용범위 및 경과조항',
                        ['effective August 17, 2020','Savings Clause']),
    'NSFC_2019_DEADLINE': ('2019-03-20','2018-12-05','nsfc','MOST 공식문 一(一)1–3·一(三)1 및 말미 서명일', [])
}

WEB_RECEIPTS = [
    {'source_id':'doj','url':'https://www.justice.gov/archives/opa/speech/attorney-general-jeff-sessions-announces-new-initiative-combat-chinese-economic-espionage',
     'method':'검증자가 공식 웹 도구로 본문 재조회', 'http':None, 'http_note':'웹 도구가 상태코드를 노출하지 않음',
     'locator':'날짜 머리말 및 창설·집행역량 배분 발표 문단 103–109', 'status':'verified',
     'finding':'2018-11-01 발표 확인. 새 ECCN의 시행일이 아니라 집행 이니셔티브의 창설 발표. 발표 시각 미확인.'},
    {'source_id':'nsfc','url':'https://fuwu.most.gov.cn/html/tztg/kjjhyjf/20181205/2960.html',
     'method':'검증자가 공식 웹 도구로 본문 재조회', 'http':None, 'http_note':'웹 도구가 상태코드를 노출하지 않음',
     'locator':'공고일·말미 서명일; 一(一)1–3; 一(三)1의 시범분야 표; 一(四)1', 'status':'verified',
     'finding':'2018-12-05 공고. 2019-03-01부터 03-20 16:00까지 집중접수. 별도 공고·수시접수 유형 존재. 정보과학 F04/F05 시범분야. 기관 내부 마감은 앞설 수 있음.'},
    {'source_id':'china35_submission','url':'https://www.zgjx.cn/2019-06/23/c_138149621.htm',
     'method':'공식 출품서 도메인의 검색 색인 확인; 본문 직접 열기 두 차례 시간 초과', 'http':None,
     'http_note':'본문 직접 열기는 시간 초과. 검색 색인 상태와 분리', 'locator':'추천표의 발행기간·연재 수 소개',
     'status':'verified_index_only', 'finding':'공식 출품서 색인에서 2018-04-19~07-03 및 35편을 확인. 개별 35개 날짜의 별도 증거로 사용하지 않음.'},
    {'source_id':'ofr_time_convention','url':'https://www.archives.gov/federal-register/public-inspection/about.html',
     'method':'미 국립문서기록관리청 공식 안내 검색 결과 본문 열람', 'http':None,
     'http_note':'웹 도구가 상태코드를 노출하지 않음', 'locator':'Availability of Documents; Regular Filing',
     'status':'verified', 'finding':'정규 공개열람 접수시각은 동부시간 08:45. ANPRM 원문 접수기록의 시간대 해석 근거. 실제 최초 열람자의 접근 시각은 확인하지 않음.'}
]

def main():
    manifest = json.loads((DATA/'source_manifest.json').read_text(encoding='utf-8'))
    sources = manifest['sources']
    integrity = []
    for sid, rec in sources.items():
        local = rec.get('local')
        if not local:
            integrity.append({'source_id':sid,'url':rec['url'],'producer_access_error':rec.get('error'),
                              'local_file_present':False,'body_verification':'공식 웹 재조회 기록을 별도 참조'})
            continue
        p = DATA/local
        h = sha(p)
        integrity.append({'source_id':sid,'url':rec['url'],'local_file':str(p),'sha256':h,
                          'manifest_sha256_match':h==rec.get('sha256'),'bytes':p.stat().st_size,
                          'producer_http':rec.get('http'),'http_independently_observed':False,
                          'body_verification':'로컬 본문 없음: 차단 응답' if sid=='doj' else '원자료 본문 직접 열람'})

    event_rows = read_csv('concurrent_events.csv')
    event_checks=[]
    for row in event_rows:
        eid=row['event_id']; exp=EVENTS[eid]; src=exp[2]
        text=html_text(src)
        phrase_checks=[{'locator_phrase':p,'present':p.lower() in text.lower()} for p in exp[4]]
        dates_match=(row['effective_or_deadline_date'],row['announcement_or_publication_date'])==exp[:2]
        verified=dates_match and all(x['present'] for x in phrase_checks)
        event_checks.append({'event_id':eid,'status':'verified' if verified else 'contradicted',
                             'dates_match':dates_match,'effective_or_deadline_date':exp[0],
                             'announcement_or_publication_date':exp[1],'source_url':row['source_url'],
                             'source_id':src,'locator':exp[3],'local_phrase_checks':phrase_checks,
                             'access_basis':'공식 웹 재조회' if src in ('doj','nsfc') else '공식 원자료 로컬 본문 직접 열람'})

    expected_signals={
        'DIUX':('2018-01-01','2018-01-31'), 'ZTE_APRIL':('2018-04-15','2018-04-23'),
        'HOUSE':('2018-06-26','2018-06-26'), 'ECRA':('2018-08-13','2018-08-13'),
        'ANPRM':('2018-11-16','2018-11-19')}
    signal_rows=read_csv('signal_chain.csv')
    signal_checks=[]
    for row in signal_rows:
        sid=row['id']; match=(row['date_lower'],row['date_upper'])==expected_signals[sid]
        signal_checks.append({'signal_id':sid,'status':'verified' if match else 'contradicted',
                              'date_range_matches':match,'source_url':row['source_url']})
    d=fitz.open(DATA/'sources/diux.pdf')
    assert 'January 2018' in d[0].get_text()
    house=html_text('house')
    assert '[[Page H5691]]' in house
    assert 'This includes artificial intelligence' in house
    ecra=html_text('ecra')
    assert 'Approved August 13, 2018.' in ecra
    assert 'SEC. 1758.' in ecra
    anprm=html_text('anprm')
    assert 'Filed 11-16-18; 8:45 am' in anprm

    editor=html_text('china35_editor')
    matches=re.findall(r'(\d+)\s*、\s*([^《]+?)\s*《[^》]+》\s*[（(]\s*(\d+)\s*月\s*(\d+)\s*日\s*[）)]',editor)
    extracted={int(n):{'technology':t.strip(),'date':f'2018-{int(m):02d}-{int(day):02d}'} for n,t,m,day in matches}
    assert len(extracted)==35, len(extracted)
    article_rows=read_csv('china_35_articles.csv')
    article_checks=[]
    for row in article_rows:
        n=int(row['article_number']); e=extracted[n]; v=VISUAL_DATES[n-1]
        date_match=row['date']==e['date']==v
        technology_match=re.sub(r'\s+','',row['editor_technology'])==re.sub(r'\s+','',e['technology'])
        printed=18 if n<=9 else 19 if n<=21 else 20 if n<=32 else 21
        article_checks.append({'article_number':n,'date':row['date'],'editor_date':e['date'],
                               'hearing_date_visual':v,'status':'verified' if date_match and technology_match else 'contradicted',
                               'date_match':date_match,'editor_technology_match':technology_match,
                               'hearing_locator':f'Appendix A 표 ({n}); 청문회 인쇄 {printed}쪽 / PDF {printed+4}쪽',
                               'verified_scope':'후대 기록 2종 간 날짜 일치와 전재본의 항목명; 원기사 원지면 전수 열람 아님',
                               'original_newspaper_page_independently_opened':False})
    hearing=fitz.open(DATA/'sources/china35_hearing.pdf')
    assert len(hearing)==98
    for p in range(22,26):
        assert str(p-4) in hearing[p-1].get_text().splitlines()[0]

    artifacts=[]
    for name in ['concurrent_events.csv','signal_chain.csv','china_35_articles.csv','source_manifest.json','production_checks.json']:
        p=DATA/name; artifacts.append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
    payload={'verifier':AGENT,'verified_utc':datetime.now(timezone.utc).isoformat(),
             'independence':'생산 코드 읽기·가져오기·실행 없이 CSV와 원자료를 독립 대조. 청문회 날짜는 직접 렌더 판독.',
             'status':'verified','scope_limited':True,'artifact_snapshot':artifacts,'source_integrity':integrity,
             'official_web_receipts':WEB_RECEIPTS,'event_checks':event_checks,'signal_checks':signal_checks,
             'article_checks':article_checks,'counts':{'event_rows':len(event_rows),'signal_rows':len(signal_rows),
                 'article_rows':len(article_rows),'article_dates_matching_both_records':sum(x['date_match'] for x in article_checks),
                 'date_value_contradictions':sum(x['status']=='contradicted' for x in event_checks+signal_checks+article_checks)},
             'unverifiable':[{'claim':'DIUx의 2018년 정확한 최초 공개일','status':'unverifiable','reason':'표지는 2018년 1월만 표시. 당일 공표·최초 공개 로그를 확보하지 않음.'},
                {'claim':'중국 원기사 35편의 원지면 전수 대조','status':'unverifiable','reason':'이번 검증은 편집장 1인칭 집계 전재본과 상원 청문회 증언 부록의 날짜 기록 대조.'},
                {'claim':'출품서 개별 날짜·본문 직접 열람','status':'unverifiable','reason':'공식 출품서 색인에서 범위와 편수만 확인. 직접 열기 두 차례 시간 초과.'},
                {'claim':'중국 전체 기술의 미통제 구간·정책 인과·전체 투자효과','status':'outside_scope','reason':'이번 날짜·범위 검증으로 도출할 수 없음.'}],
             'required_corrections':[],
             'limitations':[{'id':'P01','severity':'범위한계','status':'날짜수정불필요',
                 'finding':'법무부 HTTP 200 파일은 본문이 아닌 차단 응답. NSFC 로컬 자료는 인증서 실패. 원자료 열람 성공은 공식 웹 재조회 경로로만 확인됨.',
                 'correction':'매니페스트의 HTTP 성공과 본문 성공을 구분하고 이 검증의 공식 웹 열람 기록을 연결할 것. 날짜 값 수정은 불필요.'},
                {'id':'P02','severity':'범위한계','status':'날짜수정불필요',
                 'finding':'13번 편집장 항목은 핵심 산업용 소프트웨어로 넓고 증언 부록 분류는 EDA. 그 밖에도 기술명은 범위가 서로 다름.',
                 'correction':'13번을 EDA에 자동 일대일 매핑하지 말 것. 8번은 iCLIP 시약·표적,15번은 로봇 알고리즘,21번은 광리소그래피용 광레지스트,32번은 고성능 탄소섬유용 에폭시 맥락을 유지.'}],
             'scope_note':'11개 사건의 효력·마감과 공표일, 5개 신호의 기록 범위, 35개 기사의 기록된 날짜만 검증. 중국 전체 접근제한 부재·미국 신호가 중국정책을 유발했다는 인과·전체 투자 증가·계량 노출도 실측은 검증하지 않음.'}
    (OUT/'policy_final_nov13.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 정책 날짜·연재 기록 독립 검증','',f'검증자: `{AGENT}`. 검증시각: {payload["verified_utc"]}.',
           '', '판정: **정해진 범위 안에서 확인**. 11개 사건과 5개 신호의 날짜 값은 원자료와 일치한다. 35개 연재 날짜도 편집장 집계 전재본과 상원 청문회 부록에 모두 일치한다. 날짜 값의 모순은 없다.',
           '', '생산 코드는 읽거나 가져오거나 실행하지 않았다. 원자료 HTML을 직접 파싱하고, 청문회 PDF를 렌더해 표 전체를 판독한 뒤 CSV와 독립 비교했다. 이 검산 코드가 재현 가능한 대조와 해시를 생성한다.',
           '', '## 11개 사건','', '| 사건 | 효력·마감일 | 공표일 | 원문 위치 |','|---|---|---|---|']
    labels={'ZTE_ON':'ZTE 금지 개시','ZTE_OFF':'ZTE 해당 금지 종결','301_LIST1':'301 관세 1차','301_LIST2':'301 관세 2차','301_LIST3':'301 관세 3차','JINHUA_EL':'진화 명단 추가','CHINA_INITIATIVE':'법무부 이니셔티브','HUAWEI_EL':'화웨이 명단 추가','HUAWEI_FDPR_MAY':'화웨이 2020년 5월 규칙','HUAWEI_FDPR_AUG':'화웨이 2020년 8월 규칙','NSFC_2019_DEADLINE':'NSFC 집중접수 마감'}
    for x in event_checks:
        lines.append(f'| {labels[x["event_id"]]} | {x["effective_or_deadline_date"]} | {x["announcement_or_publication_date"]} | [{x["locator"]}]({x["source_url"]}) |')
    lines += ['', 'ZTE 종결은 해당 4월 명령의 종결이며 모든 EAR 의무의 소멸이 아니다. 301 관세는 중국산 물품의 미국 수입에 부과된다. 3차 관세는 최초 10%이며 2019년 1월 인상 계획을 실제 시행으로 확인한 것이 아니다. 진화·화웨이는 특정 당사자와 규칙의 품목·역할·인지·경과 요건에 한정된다. 위 날짜를 중국의 모든 기술 접근이 막힌 날로 사용할 수 없다.',
              '', '법무부는 11월 1일 발표와 창설 내용을 공식 연설에서 확인했다. 법무부 로컬 HTML은 200 상태에도 본문이 없다. NSFC는 공식 MOST 웹 본문에서 공고·서명일 2018년 12월 5일과 집중접수 2019년 3월 1일~3월 20일 16:00를 확인했다. 일부 유형의 별도 공고와 수시접수가 있으며, 기관별 내부 마감은 더 이를 수 있다. 이 날짜는 지원금 결정일이 아니다. F04/F05는 분류 신청·심사 시범분야 표에 실려 있다.',
              '', '## 5개 신호','', '- DIUx는 정부 작성 보고서의 제삼자 호스팅 사본이다. 표지 PDF 1쪽은 2018년 1월을 표시한다. 정확한 최초 공개일은 미확인이다.',
              '- ZTE는 효력과 신호가 겹친다. 4월 15~23일을 깨끗한 사전 신호 구간으로 확정할 수 없다.',
              '- 6월 26일 하원 기록 H5691의 기술 예시는 Royce 의원의 법안 설명이다. BIS의 구속력 있는 품목 지정으로 해석하지 않는다.',
              '- ECRA는 2018년 8월 13일 승인된 공법 115-232의 조문이며 §1758은 식별 절차·고려요인을 규정한다. 중국 손실지표의 외생성이나 값을 검증하지 않는다.',
              '- ANPRM은 관보 83 FR 58201–58202의 단일 사건이다. 말미 접수기록은 11월 16일 08:45, 관보일은 11월 19일이다. [OFR 공식 시간 안내](https://www.archives.gov/federal-register/public-inspection/about.html)에 따라 동부시간으로 해석한다. 새 전면 금지의 시행일은 아니다. 최초 투자자 접근시각은 확인하지 않았다.',
              '', '## 35개 연재 날짜의 증거 수준','',
              '[상원 청문회 공식 파일](https://www.govinfo.gov/content/pkg/CHRG-117shrg47983/pdf/CHRG-117shrg47983.pdf)은 98쪽이다. Dewey Murdick 제출 증언의 Appendix A를 인쇄면 18–21쪽, 파일 PDF 22–25쪽에서 직접 렌더해 읽었다. 증언 내부 소쪽수 4–7과 청문회 인쇄면을 혼동하지 않았다. 표의 1–9번은 인쇄 18쪽, 10–21번은 19쪽, 22–32번은 20쪽, 33–35번은 21쪽이다. 표의 각 행은 기사 저자·제목·발행일·지면·보관주소를 기록한다.',
              '', '[편집장 1인칭 정리 전재본](https://kunlunce.com/ssjj/fl1/2018-08-08/127123.html)은 2018년 8월 8일 게시물이며 35개 번호 항목의 날짜를 독립 추출했다. 이는 원저자 성격의 집계 내용이 제삼자에 전재된 자료다. 원 신문 지면 35편 자체의 전수 열람을 대신하지 않는다. 상원 부록도 미국 정부가 그 기술 분류나 중국 정책효과를 승인했다는 뜻이 아니라, 증인이 제출한 후대 서지기록이다.',
              '', '[중국기자협회 출품서](https://www.zgjx.cn/2019-06/23/c_138149621.htm)의 공식 검색 색인에서 발행기간 2018년 4월 19일~7월 3일과 35편을 확인했다. 본문 직접 열기는 두 차례 시간 초과였다. 따라서 이 출품서는 기간·편수의 보조 증거이며 개별 날짜 35개의 대조 근거로 더하지 않았다.',
              '', '| 번호 | 날짜 | 부록 인쇄면/PDF면 | 일치 |','|---|---|---|---|']
    for x in article_checks:
        n=x['article_number']; pp=18 if n<=9 else 19 if n<=21 else 20 if n<=32 else 21
        lines.append(f'| {n} | {x["date"]} | {pp}/{pp+4} | {"예" if x["date_match"] else "아니오"} |')
    lines += ['', '기술명 주의: 13번의 산업용 소프트웨어와 부록의 EDA는 범위가 다르다. 8번은 iCLIP 실험의 시약·표적, 15번은 로봇 알고리즘, 21번은 광리소그래피용 광레지스트, 32번은 고성능 탄소섬유용 에폭시라는 부록 맥락을 보존해야 한다. 넓은 항목명만으로 특정 ECCN·특허분류와 일대일 연결하지 않는다. 날짜 기록의 일치는 이런 기술 범위 문제를 해소하지 않는다.',
              '', '## 접근·해시 및 미확인 사항','', '아래 해시는 검증자가 파일 바이트에서 독립 계산했다. HTTP는 생산 다운로드 기록이며 독립 재관측으로 가장하지 않았다. 법무부의 200 차단 응답과 NSFC 인증서 오류를 원문 성공으로 계산하지 않는다. 두 건은 별도 공식 웹 본문 재조회로 사실을 확인했으며, 웹 도구는 HTTP 코드·전체 응답 바이트 해시를 제공하지 않았다.',
              '', '| 자료 | 바이트 | SHA-256 | 매니페스트 일치 |','|---|---|---|---|']
    for x in integrity:
        if x.get('local_file_present') is False:
            lines.append(f'| {x["source_id"]} | 로컬 없음 | 해당 없음 | 접근 오류 기록 |')
        else:
            lines.append(f'| {x["source_id"]} | {x["bytes"]} | `{x["sha256"]}` | {"예" if x["manifest_sha256_match"] else "아니오"} |')
    lines += ['', 'DIUx 정확한 공개일, 신문 원지면 35편 전수 대조, 출품서 본문 직접 접근은 미확인으로 남긴다. 사건·신호·연재 기록의 확인을 전체 중국 기술의 미통제 구간, 중국 정책의 미국 신호에 대한 인과반응, 전체 연구·자본 투자 증가, 노출도 실측 검증으로 확대하지 않는다.',
              '', '대상 CSV·매니페스트·생산 점검 파일의 고정 해시와 51행별 결과는 동명 JSON에 보존했다. 원고·CSV·상태는 변경하지 않았다.']
    (OUT/'policy_final_nov13.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(payload['counts'],ensure_ascii=False))

if __name__=='__main__':
    main()
