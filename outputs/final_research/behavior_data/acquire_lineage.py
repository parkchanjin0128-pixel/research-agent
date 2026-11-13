"""Four bounded lineage documents; factual excerpts omit personal contacts."""
from acquire_behavior import ROOT,RAW,Parser
from acquire_procurement import fetch
import re,json,hashlib
SOURCES=[
('szu_20180519_tender','https://bidding.szu.edu.cn/info/1017/10945.htm',[r'2018/11/16\s*17:00:00',r'采购预算或最高限价[：:]\s*[\d,]+\.\d+\s*元',r'所有投标文件应于2018年11月28日\s*09:30时']),
('szu_20180519_change','https://bidding.szu.edu.cn/info/1017/10913.htm',[r'2018/11/23\s*\d{2}:\d{2}:\d{2}',r'SZUCG20180519EQ\s*GPU服务器，根据采购方要求对[^。]+。',r'本项目开标时间不变，2018年11月28日\s*09:30时']),
('szu_20180519_award','https://bidding.szu.edu.cn/info/1024/10878.htm',[r'2018/11/28\s*\d{2}:\d{2}:\d{2}',r'招标编号[：:]SZUCG20180519EQ',r'中标单位[：:]深圳市长城网信息科技股份有限公司',r'中标金额[：:]555800\s*元']),
('njust_jan2019_original_tender','https://zbpt.njust.edu.cn/cgxx/5583.jhtml',[r'发布日期[：:]\s*2018-12-20',r'预算金额[：:]310万元（人民币）',r'投标截止时间[：:]\s*2019\s*年\s*1\s*月\s*11\s*日09:00（北京时间）',r'开标时间[：:]\s*2019\s*年\s*1\s*月\s*11\s*日09:00（北京时间）']),
]
def main():
 out=[]
 for id,url,patterns in SOURCES:
  h,m=fetch(url);p=Parser();p.feed(h);text=re.sub(r'\s+',' ',''.join(p.all));ex=[];missing=[]
  for pattern in patterns:
   match=re.search(pattern,text)
   if match:ex.append(match.group(0))
   else:missing.append(pattern)
  evidence='\n'.join(ex)+'\n';path=RAW/(id+'_factual_excerpt.txt');path.write_text(evidence,encoding='utf-8')
  out.append(dict(id=id,url=url,retained=str(path.relative_to(ROOT)),html_text_sha256=hashlib.sha256(h.encode('utf-8')).hexdigest(),method=m,missing_patterns=missing,excerpts=ex))
 (ROOT/'lineage_sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
