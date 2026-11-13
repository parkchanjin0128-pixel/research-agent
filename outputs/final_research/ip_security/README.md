# 지식재산·기술안보 산출물

2026-11-12, `/root/final_ip_security` 독립 생산. `state/`·Gate·기존 연구결과는 수정하지 않았다.

- `ip_security_memo.md`: 공개 특허정보·영토적 특허권·비공개 노하우·장비/코드·deemed export의2018제도적구분,US인용비중타당성,구체반증표,발표대본.
- `historical_taxonomy_solution.md`:2017고정의미로새코드회수하는방법과회고분류/사후내생라벨의차이.
- `historical_crosswalk_edges.csv` / `.json`:WIPO2019F093·2020F097의관련76방향edge. `historical_scheme_rows.json`:2017–20해당scheme106행. `rcl_exact_extracts.xml.txt`:원문단위추출.
- `literature_update.md`:Kang/Shen기존전문검토와2025–26최신primary검색의차이를보존한기여평가.
- `gpu_case_legal_scope.md`:2018–19조달의당시CCL/군사용도범위,2018-10-24성능기준완화,기존허가·추가제한·실제거절·실제인도의분리.
- `source_manifest.json`:원문33개요청응답·바이트·SHA256및ZIPmember. HTTP403/400접근실패도기록. 성공표시한로컬파일33개가아니며실패HTML을원문확보로세지않는다.
- `download_primary.py`:최초23개원문요청재현. 추가10개는manifest에URL/해시로기록되어있다. 재실행은기존manifest추가행을보존하고같은파일명행만갱신한다.
- `extract_crosswalk.py`:다운로드된WIPO원문에서edge/scheme행을다시생성.

검사:76edge의from/to title결측0;모든source_manifest기재성공로컬파일의SHA256재계산불일치0. 원문분류·규제시계·실증표본에대한독립심사를완료했다는뜻은아니다.

미완료:2017→현행2026전체revisionclosure·개별family원분류회수·B/outcome재집계;2018-11-18및각2019조달일까지모든EAR개정/정정/개별통지·entity/enduse의완결감사;TeslaV100개별partnumber의당시공식ECCN·서버/집계APP·허가/인도자료. 따라서여기서cleanwindow·법준수·순수anticipation효과를확정하지않는다.
