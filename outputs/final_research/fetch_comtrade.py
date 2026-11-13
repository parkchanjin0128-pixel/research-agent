from pathlib import Path
import urllib.request,urllib.parse,urllib.error,json,datetime,hashlib
H=Path(__file__).resolve().parent/'trade';H.mkdir(exist_ok=True)
url='https://comtradeapi.un.org/public/v1/preview/C/A/HS'
params={'reporterCode':156,'period':2017,'partnerCode':'0,842','cmdCode':'8486,8542','flowCode':'M','partner2Code':0,'customsCode':'C00','motCode':0,'maxRecords':500}
request_url=url+'?'+urllib.parse.urlencode(params)
try:
 with urllib.request.urlopen(request_url,timeout=45) as response:
  body=response.read();status=response.status
except urllib.error.HTTPError as exc:
 body=exc.read();status=exc.code
(H/'pilot_2017_response.json').write_bytes(body)
meta={'url':request_url,'status':status,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'no_key':True}
(H/'pilot_2017_meta.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
print(json.dumps(meta))
if status==200:
 d=json.loads(body);print('top_keys',list(d));print('count',d.get('count'));print(json.dumps([{k:x.get(k) for k in ['period','reporterCode','partnerCode','flowCode','cmdCode','cmdDesc','classificationCode','isOriginalClassification','primaryValue','cifvalue','fobvalue','isAggregate']} for x in d.get('data',[])],ensure_ascii=False))
