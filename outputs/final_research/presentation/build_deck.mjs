import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const {Presentation,PresentationFile}=await import(process.env.ARTIFACT_TOOL_ENTRY);
import {slides} from './content.mjs';
const root=import.meta.dirname,workspace=path.resolve(root,'../../..');
const skill=process.env.PRESENTATIONS_SKILL;
const runtime=process.env.CODEX_RUNTIME_DEPENDENCIES;
process.env.RUNTIME_NODE_MODULES=path.join(runtime,'node/node_modules');
process.env.RUNTIME_NODE=path.join(runtime,'node/bin/node.exe');
const build=path.join(root,'.build');
await fs.mkdir(path.join(build,'previews'),{recursive:true});
await fs.mkdir(path.join(root,'deliverables'),{recursive:true});
const {applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const load=async p=>JSON.parse(await fs.readFile(path.join(workspace,p),'utf8'));
const rd=await load('outputs/presentation_2026-11-13/data/official_rd_derived.json');
const rdsource=await load('outputs/presentation_2026-11-13/data/official_rd_series.json');
const refs=(await load('outputs/presentation_2026-11-13/references/references.json')).references;
const literatureAudit=await fs.readFile(path.join(workspace,'outputs/final_research/literature/pdf_audit.md'),'utf8');
const newlit=(await fs.readFile(path.join(workspace,'outputs/final_research/ip_security/literature_update.md'),'utf8')).split('\n').filter(line=>!line.startsWith('| [Gao,')).join('\n')+'\n\n# 2026년 11월 13일 제공 원문에 따른 현재 문헌 확인\n\nGao 등의 웹 전문 미확보는 11월 12일의 과거 검색 상태다. 현재는 제공된 2026년 6월 PDF 85쪽의 처치식·시점·연구투입 관련 쪽을 확인했다. 아래 원문감사가 현재 판본·확인범위의 기준이다.\n\n'+literatureAudit;
const sourceText={
 overview:'outputs/identification_rescue_2026-11-12/overview.md\n원자료 patstat_wo_monthly_raw.json\nEPO TIP PATSTAT PROD 실행 집계. release 미확인. query의 독립 재실행은 아님.',
 analysis:'outputs/final_research/empirics/analysis.md\n전체 계산 falsification_results.json, simulation_pilot.csv\n보존된 monthly raw와 old pilot B 재사용. 넓은 IPC 값 관찰 후 탐색. 정책 p값·인과적 CI 없음.',
 ip:'outputs/final_research/ip_security/ip_security_memo.md\n2018 EAR §734.10 https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec734-10.xml\n§734.3 https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec734-3.xml\n§772.1 https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec772-1.xml\nWIPO FAQ https://www.wipo.int/en/web/patents/faq_patents',
 law:'83 FR53742–53793, 개정문39·41–43 https://www.govinfo.gov/content/pkg/FR-2018-10-24/html/2018-22163.htm\nANPRM 83 FR58201 https://www.govinfo.gov/content/pkg/FR-2018-11-19/html/2018-25221.htm\nECRA https://www.govinfo.gov/content/pkg/PLAW-115publ232/html/PLAW-115publ232.htm\n2019 CFR https://www.govinfo.gov/content/pkg/CFR-2019-title15-vol2/xml/CFR-2019-title15-vol2-part774.xml\noutputs/final_research/ip_security/gpu_case_legal_scope.md\noutputs/final_research/verification/primary_sources.md',
 procurement:'outputs/final_research/behavior_data/behavior_findings.md\nSZU 원입찰 https://bidding.szu.edu.cn/info/1017/10945.htm\n변경 https://bidding.szu.edu.cn/info/1017/10913.htm\n낙찰 https://bidding.szu.edu.cn/info/1024/10878.htm\nNJUST V100 https://zbpt.njust.edu.cn/cjgg/5853.jhtml\nNJUST 1월 원입찰 https://zbpt.njust.edu.cn/cgxx/5583.jhtml\n1월 낙찰 https://zbpt.njust.edu.cn/cjgg/5723.jhtml\nSZU 가속카드 https://bidding.szu.edu.cn/info/1022/20188.htm\n공시 시각·금액·사양 관측. 최초 연구선택·실제 인도·지급·허가결과 미관측.',
 fine:'outputs/identification_rescue_2026-11-12/finegroup_progress.md\n원집계 finegroup_pre_dose_raw.json, finegroup_measurement_diagnostics.json\n24개 그룹 각100 deterministic hash 표집. 관측 신청인 슬롯 조건부 산술 경계는 CI 아님.',
 recovery:'outputs/final_research/family_country_recovery_raw.json\n같은 target family에서 2017-12-31 이전 공개·known 국가가 있는 최초 문헌을 선택. ALL 대표 문헌 변경3,221쌍. 국가귀속 구성개념 변경. 세부 post outcome 미조회.',
 taxonomy:'outputs/final_research/ip_security/historical_taxonomy_solution.md\nWIPO 공식 RCL https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20190101/MasterFiles/ipc_concordancelist_20190101.zip\nhttps://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20200101/MasterFiles/ipc_concordancelist_20200101.zip\nF093과F097 별개 개정. 특허별 실제 이동량 미집계.',
 trade:'outputs/final_research/trade/derived.json, all_rows.json\nUN Comtrade 중국 수입 HS4 공식 집계. 20행 중2013–2014 8행 isReported=true, 2015–2017 12행 isReported=false/isAggregate=true. isOriginalClassification은 원신고 여부와 별개. partner 국가는 미국 기업·부품설계·EAR관할과 다름.',
 behavior:'outputs/final_research/behavior_data/behavior_findings.md\nNSFC https://www.nsfc.gov.cn/p1/2853/3102/72662.html\nhttps://www.nsfc.gov.cn/p1/2853/3102/72653.html\nhttps://www.nsfc.gov.cn/p1/2853/3102/72645.html\n원표 nsfc_approved_records.csv, national_rd_proposed_records.csv, archive_final_2016_2019_inventory.csv\n승인·예정선정, 신청·집행, 현재 회수·모집단 완전성을 구분.'
};
sourceText.lineage='outputs/final_research/report_main.md §6.1·7.1\n월별 β는 기존 200-family/넓은 IPC B를 사용. 관청 제한 없는 중국 주소 cohort에서 표집하고 모든 family application으로 확장. any-APP 포함태그와 공통 earliest target 공보 국가귀속을 결합. 새 24 WO main-group의 100-family와 APP 안의 대표공보, 새 family footprint는 별도 측정이다. 이 새 지표로 β를 재추정하지 않았다.';
sourceText.literature='outputs/final_research/literature/pdf_audit.md/json, 2026-11-13 제공 PDF 8파일·7고유문헌 집중감사. Gao June2026 85쪽의 관련 주명세 확인. Zhang·Canlei Liu·Runjuan Liu February2026 SSRN6210408과 Liu·Ruan·Zheng June2026 SSRN7042518을 포함. He·Lyu의 자본·인력 재배분은 KZ·현금·학력구성의 간접 측정. 별도 예고–추가제한 구간의 독립효과로 확대하지 않음.';
const sourceMap=[[],['overview','analysis'],['overview','ip'],[],['overview','fine','behavior'],[],['ip'],['ip'],['law'],['law'],['procurement','law'],['procurement','law'],['fine','ip'],['overview','fine'],['overview'],['overview'],['overview','analysis'],['overview'],['analysis'],['analysis'],['overview','analysis'],['analysis'],['analysis'],['fine'],['fine'],['fine','recovery'],['taxonomy'],['trade'],['behavior'],['behavior'],['overview','ip','behavior'],['overview','ip','behavior'],['overview','fine','behavior'],['analysis'],['law','procurement'],['overview','recovery','analysis'],[],['overview','ip','behavior']];
for(const n of [12,13,23]) sourceMap[n].push('lineage');
for(const n of [3,36]) sourceMap[n].push('literature');
const P=Presentation.create({slideSize:{width:1280,height:720}});
const FONT='Malgun Gothic',NAVY='#102C46',TEAL='#087F82',GRAY='#4B5F70';
const chartOwners=[];
function txt(s,t,x,y,w,h,size=30,color=NAVY,bold=false){const sh=s.shapes.add({geometry:'textbox',name:bold?'heading':'text',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});sh.text=t;sh.text.style={fontSize:size,typeface:FONT,color,bold};return sh;}
function chart(s,key){
 let categories,series,max,min=0,unit,fmt='0.0',type='bar';
 if(key==='rd'){type='line';categories=rd.annual.map(x=>String(x.year));series=[{name:'명목 총 R&D',values:rd.annual.map(x=>x.rd_total_billion_rmb/1000)}];max=2.8;unit='명목 조 위안';}
 if(key==='coeff'){categories=['4개국 평균','미국'];series=[{name:'ALL',values:[-.080665,-.049046]},{name:'APP',values:[-.049947,-.052338]}];max=.02;min=-.1;unit='B 10%p당 상대 log(1+건수)의 기울기 변화';fmt='0.000';}
 if(key==='g06n'){categories=['2013','2017','2018','2019'];series=[{name:'중국 WO G06N family',values:[25,241,401,855]}];max=1000;unit='해당 연도 family 건수';fmt='0';}
 if(key==='mde'){categories=['ALL','APP'];series=[{name:'80% MDE',values:[.2468,.1902]}];max=.3;unit='조건부 MDE, B 10%p당 상대 log';fmt='0.0000';}
 if(key==='recovery'){categories=['원대표문헌','패밀리 내 회수'];series=[{name:'구간폭 중앙값',values:[60.87820261554358,41.413537900626696]}];max=75;unit='관측 국가미상 산술 구간폭, %p';fmt='0.0';}
 if(key==='trade'){categories=['HS8486 제조장비','HS8542 집적회로'];series=[{name:'미국 partner 비중',values:[14.5582222743409,4.751525867053626]}];max=20;unit='2013–2017 중국 수입액 합계 대비 %';fmt='0.0000';}
 if(key==='nsfc'){categories=['2017','2018','2019'];series=[{name:'승인 직접경비',values:[33500,32300,34500]}];max=40000;unit='만 위안, 동일 생명과학부 중점과제';fmt='#,##0';}
 txt(s,unit,74,154,1120,32,20,GRAY);
 const ch=s.charts.add(type,{position:{left:65,top:203,width:1135,height:325},categories,series:series.map((a,i)=>({...a,values:a.values.map(v=>Number(v.toFixed(6))),fill:i?NAVY:TEAL,line:{fill:i?NAVY:TEAL,width:3,style:'solid'},marker:{symbol:'circle',size:7}})),hasLegend:series.length>1,legend:{position:'bottom',textStyle:{fontSize:23,fill:NAVY}},barOptions:{direction:'column',grouping:'clustered',gapWidth:160},xAxis:{textStyle:{fontSize:23,fill:GRAY},line:{fill:'#BCC8CF',width:1}},yAxis:{min,max,numberFormatCode:fmt,textStyle:{fontSize:19,fill:GRAY},majorGridlines:{fill:'#DDE5EA',width:1,style:'solid'}},dataLabels:{showValue:type==='bar',position:'outEnd',numberFormatCode:fmt,textStyle:{fontSize:23,fill:NAVY}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',chartLine:{fill:'none',width:0}});
 applyPresentationChartFont(ch,{fontFamily:FONT});
}
let elapsed=0;const script=[];
for(let i=0;i<slides.length;i++){
 const a=slides[i],s=P.slides.add();s.background.fill='#FFFFFF';
 if(i===0){txt(s,a.title,72,135,1136,175,54,NAVY,true);txt(s,a.lines.join('\n'),76,375,1120,130,29,GRAY);txt(s,'최종 연구발표  2026년 11월 13일',76,570,1120,45,24,TEAL);}
 else{txt(s,a.kind,72,25,1100,28,19,TEAL,true);txt(s,a.title,72,70,1136,80,42,NAVY,true);
  if(a.chart){chart(s,a.chart);chartOwners.push(i+1);const bl=a.lines.length<=2?a.lines:[a.lines[0],a.chart==='trade'?a.lines[2]:a.lines.at(-1)];txt(s,bl.join('\n'),78,557,1120,85,26,NAVY);}
  else a.lines.forEach((line,j)=>txt(s,line,78,190+j*100,1120,87,30,j===0?TEAL:NAVY,j===0));
 }
 txt(s,a.src,74,661,1080,38,15,GRAY);txt(s,String(i+1).padStart(2,'0'),1174,661,48,30,17,GRAY);
 const mm=String(Math.floor(elapsed/60)).padStart(2,'0'),ss=String(elapsed%60).padStart(2,'0');
 let citations=(sourceMap[i]??[]).map(k=>sourceText[k]).join('\n\n');
 if(i===5)citations+=Object.values(rdsource.sources).map(x=>x.title+' '+x.url).join('\n');
 if(i===3||i===36)citations+='\n\n'+refs.map(x=>x.authors+' ('+x.year+'). '+x.title+'. '+x.publication+'. '+(x.doi?'https://doi.org/'+x.doi:x.url)+'\n확인범위: '+x.access_scope+' / '+x.locator).join('\n\n')+'\n\n신규 문헌\n'+newlit;
 s.speakerNotes.text=`${i<32?'본문 시작 '+mm+':'+ss+' / 권장 '+a.time+'초':'질의응답용 부록'}\n\n발표원고\n${a.notes}\n\n주장과 원문·데이터 대응\n${a.src}\n${citations}\n\n해석경계: 기술적 결과와 인과귀속 구분. 최종 Gate 미채택. 효과 입증·게재 보장 없음.`;
 script.push(`## ${i+1}. ${a.title.replaceAll('\n',' ')}\n\n${i<32?'시작 '+mm+':'+ss+' · 권장 '+a.time+'초':'질의응답용 부록'}\n\n${a.notes}\n\n근거와 해석 범위: ${a.src}\n\n${citations}\n`);
 elapsed+=a.time;
}
await fs.writeFile(path.join(root,'발표원고.md'),'# 35~40분 발표원고\n\n본문 32장 '+Math.floor(elapsed/60)+'분 '+elapsed%60+'초를 기준으로 한다. 부록 6장은 본문 시간에서 제외한다. 권장시간에는 차트의 축·분모를 짚고 핵심 숫자 사이에서 멈추는 시간을 포함한다. 실제 속도에 따라 35~40분으로 조정한다. 연구 질문과 미검증 경계를 생략하지 않는다.\n\n'+script.join('\n'),'utf8');
await fs.writeFile(path.join(root,'슬라이드_주장_근거표.md'),'# 슬라이드별 주장과 근거\n\n'+slides.map((a,i)=>`## ${i+1}. ${a.title.replaceAll('\n',' ')}\n\n${a.lines.join('\n\n')}\n\n발표자 해석과 제한: ${a.notes}\n\n근거: ${a.src}\n\n${(sourceMap[i]??[]).map(k=>sourceText[k]).join('\n\n')}\n`).join('\n'),'utf8');
await fs.writeFile(path.join(root,'참고문헌.md'),'# 참고문헌과 원문 확인 범위\n\n기존 14편의 확인범위를 보존했다. 전문 재실행과 초록 확인을 동일하게 취급하지 않는다.\n\n'+refs.map((x,i)=>`${i+1}. ${x.authors} (${x.year}). ${x.title}. ${x.publication}. ${x.doi?'https://doi.org/'+x.doi:x.url}\n\n확인범위: ${x.access_scope}, ${x.locator}.\n`).join('\n')+'\n\n'+newlit+'\n\n# 신규 1차자료\n\n'+Object.values(sourceText).join('\n\n'),'utf8');
await fs.writeFile(path.join(build,'slide_manifest.json'),JSON.stringify(slides,null,2),'utf8');
const candidate=path.join(build,'candidate.pptx');
await(await PresentationFile.exportPptx(P)).save(candidate);console.log('CANDIDATE',slides.length,elapsed,chartOwners);
for(let i=0;i<P.slides.items.length;i++){
 const blob=await P.export({slide:P.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(build,'previews','slide-'+String(i+1).padStart(2,'0')+'.png'),new Uint8Array(await blob.arrayBuffer()));
 if((i+1)%5===0)console.log('RENDERED',i+1);
}
const final=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:path.join(root,'deliverables/최종_연구발표_시간정정.pptx'),pythonExecutable:path.join(runtime,'python/python.exe'),integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:38,requiredNativeChartOwnerSlides:chartOwners,materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation_시간정정.json')});
console.log('FINAL',JSON.stringify(final));
