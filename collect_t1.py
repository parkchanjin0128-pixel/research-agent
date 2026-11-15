#!/usr/bin/env python3
"""트럼프 1기(2018–2019) 분 단위 가격: Dukascopy 1분봉, 병렬. 기존 파일 형식과 같다."""
import datetime as dt, os, sys, threading, time, zipfile
from concurrent.futures import ThreadPoolExecutor
import requests
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_raw", "dukascopy")
INST = sys.argv[1:] or ["USA500IDXUSD", "USDCNH", "USDMXN", "EURUSD", "USDTRY"]
tl = threading.local()
def get(url):
    if not hasattr(tl, "s"):
        tl.s = requests.Session(); tl.s.headers["User-Agent"] = "Mozilla/5.0 Chrome/126.0 Safari/537.36"
    for i in range(4):
        try:
            r = tl.s.get(url, timeout=30)
            if r.status_code == 200: return r.content
            if r.status_code == 404: return b""
        except Exception: pass
        time.sleep(1.5 * (i + 1))
    return None
def one(job):
    inst, d = job
    return d, get("https://datafeed.dukascopy.com/datafeed/%s/%04d/%02d/%02d/BID_candles_min_1.bi5" % (inst, d.year, d.month - 1, d.day))
os.makedirs(ROOT, exist_ok=True)
for inst in INST:
    for year in (2018, 2019):
        out = os.path.join(ROOT, "%s_%d.zip" % (inst, year))
        if os.path.exists(out) and os.path.getsize(out) > 100000: continue
        days = [dt.date(year, 1, 1) + dt.timedelta(days=i) for i in range(365)]
        with ThreadPoolExecutor(12) as ex: res = list(ex.map(one, [(inst, d) for d in days]))
        ok = fail = 0
        with zipfile.ZipFile(out, "w", zipfile.ZIP_STORED) as z:
            for d, body in res:
                if body is None: fail += 1
                elif body: z.writestr(d.isoformat() + ".bi5", body); ok += 1
        print("%s %d: 자료 %d일, 실패 %d" % (inst, year, ok, fail), flush=True)
