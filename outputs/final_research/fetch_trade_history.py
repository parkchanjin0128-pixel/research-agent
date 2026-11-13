from pathlib import Path
import urllib.request,urllib.parse,urllib.error,json,hashlib,datetime,time
H=Path(__file__).resolve().parent/'trade';H.mkdir(exist_ok=True)
rows=json.loads((H/'pilot_2017_response.json').read_bytes())['data'];metadata=[]
for year in range(2013,2017):
 params={'reporterCode':156,'period':year,'partnerCode':'0,842','cmdCode':'8486,8542','flowCode':'M','partner2Code':0,'customsCode':'C00','motCode':0,'maxRecords':500}
 url='https://comtradeapi.un.org/public/v1/preview/C/A/HS?'+urllib.parse.urlencode(params)
 path=H/(str(year)+'_response.json')
 if path.exists():body=path.read_bytes();status=200
 else:
  for attempt in range(3):
   try:
    with urllib.request.urlopen(url,timeout=45) as response:body=response.read();status=response.status
    path.write_bytes(body);break
   except urllib.error.HTTPError as exc:
    error_body=exc.read();(H/(str(year)+'_error.json')).write_bytes(error_body)
    retry=exc.headers.get('Retry-After');print('HTTP_ERROR',year,exc.code,'retry_after',retry,flush=True)
    if exc.code!=429 or attempt==2:raise
    delay=int(retry) if retry and retry.isdigit() else 30
    if delay>60:raise RuntimeError('Rate limit requires longer wait; raw partial data saved')
    time.sleep(max(delay,10))
 d=json.loads(body);assert status==200 and d['count']==4 and len(d['data'])==4
 metadata.append({'year':year,'url':url,'sha256':hashlib.sha256(body).hexdigest(),'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'no_key':True})
 rows.extend(d['data']);print('SAVED',year,len(d['data']),flush=True);time.sleep(10)
assert len(rows)==20
index={(r['period'],r['cmdCode'],r['partnerCode']):r for r in rows};assert len(index)==20
result={}
for code in ['8486','8542']:
 out=[]
 for year in range(2013,2018):
  world=index[(str(year),code,0)];us=index[(str(year),code,842)]
  assert world['reporterCode']==us['reporterCode']==156 and world['flowCode']==us['flowCode']=='M'
  assert world['classificationCode']==us['classificationCode']
  assert 0<=us['primaryValue']<=world['primaryValue']
  out.append({'year':year,'world_import_value':world['primaryValue'],'us_partner_import_value':us['primaryValue'],'us_partner_share':us['primaryValue']/world['primaryValue'],'classification':world['classificationCode'],'original_classification':world['isOriginalClassification'],'primary_equals_cif':world['primaryValue']==world['cifvalue']})
 result[code]={'annual':out,'pooled2013_17_us_partner_share':sum(r['us_partner_import_value'] for r in out)/sum(r['world_import_value'] for r in out)}
(H/'history_sources.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
(H/'all_rows.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
(H/'derived.json').write_text(json.dumps({'results':result,'scope':'China reported imports, as-reported HS4, USA partner vs World, 2013-2017. Not firm-nationality, legal jurisdiction, ECCN scope or policy effects.'},indent=2),encoding='utf-8')
print(json.dumps(result,indent=2),flush=True)
