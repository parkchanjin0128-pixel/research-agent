-- BigQuery Standard SQL CTE. WITH 뒤 또는 기존 CTE와 쉼표로 연결한다.
-- 실제 IPC 열에서 공백을 제거한 값과 ipc_compact를 완전일치 JOIN한다.
-- REGEXP_REPLACE(UPPER(actual_ipc_column), r'\s+', '') = technology_map.ipc_compact
-- 2017~2026 exact alias UNION이다. 임의 prefix로 바꾸지 않는다.
technology_map AS (
 SELECT t.group_id, t.label, t.domain_block, ipc_compact
 FROM UNNEST([
  STRUCT('P01' AS group_id, 'positive' AS label, 'ai_computing' AS domain_block, 'G06N3/02,G06N3/04,G06N3/042,G06N3/043,G06N3/044,G06N3/0442,G06N3/045,G06N3/0455,G06N3/0464,G06N3/047,G06N3/0475,G06N3/048,G06N3/049,G06N3/0495,G06N3/0499,G06N3/06,G06N3/063,G06N3/065,G06N3/067,G06N3/08,G06N3/082,G06N3/084,G06N3/086,G06N3/088,G06N3/0895,G06N3/09,G06N3/091,G06N3/092,G06N3/094,G06N3/096,G06N3/098,G06N3/0985,G06N3/10' AS exact_codes),
  STRUCT('P02' AS group_id, 'positive' AS label, 'ai_computing' AS domain_block, 'G06N3/12,G06N3/123,G06N3/126' AS exact_codes),
  STRUCT('P03' AS group_id, 'positive' AS label, 'ai_computing' AS domain_block, 'G06N5/00,G06N5/01,G06N5/02,G06N5/022,G06N5/025,G06N5/04,G06N5/043,G06N5/045,G06N5/046,G06N5/047,G06N5/048' AS exact_codes),
  STRUCT('P04' AS group_id, 'positive' AS label, 'computer_vision' AS domain_block, 'G06T7/00,G06T7/10,G06T7/11,G06T7/12,G06T7/13,G06T7/136,G06T7/143,G06T7/149,G06T7/155,G06T7/162,G06T7/168,G06T7/174,G06T7/181,G06T7/187,G06T7/194,G06T7/20,G06T7/207,G06T7/215,G06T7/223,G06T7/231,G06T7/238,G06T7/246,G06T7/254,G06T7/262,G06T7/269,G06T7/277,G06T7/285,G06T7/292,G06T7/30,G06T7/32,G06T7/33,G06T7/35,G06T7/37,G06T7/38,G06T7/40,G06T7/41,G06T7/42,G06T7/44,G06T7/45,G06T7/46,G06T7/48,G06T7/49,G06T7/50,G06T7/507,G06T7/514,G06T7/521,G06T7/529,G06T7/536,G06T7/543,G06T7/55,G06T7/557,G06T7/564,G06T7/571,G06T7/579,G06T7/586,G06T7/593,G06T7/60,G06T7/62,G06T7/64,G06T7/66,G06T7/68,G06T7/70,G06T7/73,G06T7/77,G06T7/80,G06T7/90' AS exact_codes),
  STRUCT('P05' AS group_id, 'positive' AS label, 'speech' AS domain_block, 'G10L13/00,G10L13/02,G10L13/027,G10L13/033,G10L13/04,G10L13/047,G10L13/06,G10L13/07,G10L13/08,G10L13/10' AS exact_codes),
  STRUCT('P06' AS group_id, 'positive' AS label, 'speech' AS domain_block, 'G10L15/00,G10L15/01,G10L15/02,G10L15/04,G10L15/05,G10L15/06,G10L15/065,G10L15/07,G10L15/08,G10L15/10,G10L15/12,G10L15/14,G10L15/16,G10L15/18,G10L15/183,G10L15/187,G10L15/19,G10L15/193,G10L15/197,G10L15/20,G10L15/22,G10L15/24,G10L15/25,G10L15/26,G10L15/28,G10L15/30,G10L15/32,G10L15/34' AS exact_codes),
  STRUCT('P07' AS group_id, 'positive' AS label, 'additive_manufacturing' AS domain_block, 'B33Y10/00' AS exact_codes),
  STRUCT('P08' AS group_id, 'positive' AS label, 'additive_manufacturing' AS domain_block, 'B33Y30/00' AS exact_codes),
  STRUCT('P09' AS group_id, 'positive' AS label, 'additive_manufacturing' AS domain_block, 'B33Y40/00,B33Y40/10,B33Y40/20' AS exact_codes),
  STRUCT('P10' AS group_id, 'positive' AS label, 'additive_manufacturing' AS domain_block, 'B33Y50/00,B33Y50/02' AS exact_codes),
  STRUCT('P11' AS group_id, 'positive' AS label, 'additive_manufacturing' AS domain_block, 'B33Y70/00,B33Y70/10' AS exact_codes),
  STRUCT('P12' AS group_id, 'positive' AS label, 'additive_manufacturing' AS domain_block, 'B33Y80/00' AS exact_codes),
  STRUCT('N01' AS group_id, 'nonlisted' AS label, 'conventional_forming' AS domain_block, 'B21B1/00,B21B1/02,B21B1/04,B21B1/06,B21B1/08,B21B1/082,B21B1/085,B21B1/088,B21B1/09,B21B1/092,B21B1/095,B21B1/098,B21B1/10,B21B1/12,B21B1/14,B21B1/16,B21B1/18,B21B1/20,B21B1/22,B21B1/24,B21B1/26,B21B1/28,B21B1/30,B21B1/32,B21B1/34,B21B1/36,B21B1/38,B21B1/40,B21B1/42,B21B1/46' AS exact_codes),
  STRUCT('N02' AS group_id, 'nonlisted' AS label, 'conventional_forming' AS domain_block, 'B21C1/00,B21C1/02,B21C1/04,B21C1/06,B21C1/08,B21C1/10,B21C1/12,B21C1/14,B21C1/16,B21C1/18,B21C1/20,B21C1/22,B21C1/24,B21C1/26,B21C1/27,B21C1/28,B21C1/30,B21C1/32,B21C1/34' AS exact_codes),
  STRUCT('N03' AS group_id, 'nonlisted' AS label, 'conventional_forming' AS domain_block, 'B21D5/00,B21D5/01,B21D5/02,B21D5/04,B21D5/06,B21D5/08,B21D5/10,B21D5/12,B21D5/14,B21D5/16' AS exact_codes),
  STRUCT('N04' AS group_id, 'nonlisted' AS label, 'conventional_forming' AS domain_block, 'B21D7/00,B21D7/02,B21D7/022,B21D7/024,B21D7/025,B21D7/028,B21D7/03,B21D7/04,B21D7/06,B21D7/08,B21D7/10,B21D7/12,B21D7/14,B21D7/16' AS exact_codes),
  STRUCT('N05' AS group_id, 'nonlisted' AS label, 'conventional_cutting' AS domain_block, 'B23B1/00' AS exact_codes),
  STRUCT('N06' AS group_id, 'nonlisted' AS label, 'conventional_cutting' AS domain_block, 'B23C3/00,B23C3/02,B23C3/04,B23C3/05,B23C3/06,B23C3/08,B23C3/10,B23C3/12,B23C3/13,B23C3/14,B23C3/16,B23C3/18,B23C3/20,B23C3/22,B23C3/24,B23C3/26,B23C3/28,B23C3/30,B23C3/32,B23C3/34,B23C3/35,B23C3/36' AS exact_codes),
  STRUCT('N07' AS group_id, 'nonlisted' AS label, 'conventional_cutting' AS domain_block, 'B23D1/00,B23D1/02,B23D1/04,B23D1/06,B23D1/08,B23D1/10,B23D1/12,B23D1/14,B23D1/16,B23D1/18,B23D1/20,B23D1/22,B23D1/24,B23D1/26,B23D1/28,B23D1/30' AS exact_codes),
  STRUCT('N08' AS group_id, 'nonlisted' AS label, 'conventional_cutting' AS domain_block, 'B23D5/00,B23D5/02,B23D5/04' AS exact_codes),
  STRUCT('N09' AS group_id, 'nonlisted' AS label, 'conventional_cutting' AS domain_block, 'B23D15/00,B23D15/02,B23D15/04,B23D15/06,B23D15/08,B23D15/10,B23D15/12,B23D15/14' AS exact_codes),
  STRUCT('N10' AS group_id, 'nonlisted' AS label, 'conventional_cutting' AS domain_block, 'B23D45/00,B23D45/02,B23D45/04,B23D45/06,B23D45/08,B23D45/10,B23D45/12,B23D45/14,B23D45/16,B23D45/18,B23D45/20,B23D45/22,B23D45/24,B23D45/26' AS exact_codes),
  STRUCT('N11' AS group_id, 'nonlisted' AS label, 'conventional_grinding' AS domain_block, 'B24B5/00,B24B5/01,B24B5/02,B24B5/04,B24B5/06,B24B5/08,B24B5/10,B24B5/12,B24B5/14,B24B5/16,B24B5/18,B24B5/20,B24B5/22,B24B5/24,B24B5/26,B24B5/28,B24B5/30,B24B5/307,B24B5/313,B24B5/32,B24B5/35,B24B5/36,B24B5/37,B24B5/38,B24B5/40,B24B5/42,B24B5/44,B24B5/46,B24B5/48,B24B5/50' AS exact_codes),
  STRUCT('N12' AS group_id, 'nonlisted' AS label, 'conventional_grinding' AS domain_block, 'B24B7/00,B24B7/02,B24B7/04,B24B7/06,B24B7/07,B24B7/08,B24B7/10,B24B7/12,B24B7/13,B24B7/14,B24B7/16,B24B7/17,B24B7/18,B24B7/19,B24B7/20,B24B7/22,B24B7/24,B24B7/26,B24B7/28,B24B7/30' AS exact_codes)
 ]) AS t
 CROSS JOIN UNNEST(SPLIT(t.exact_codes, ',')) AS ipc_compact
)
