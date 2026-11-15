#!/usr/bin/env python3
"""수출통제 분석용 추가 종목 수집 (Yahoo만, 5분 이내).
기존 수집기(Polymarket)가 돌고 있어도 다른 터미널에서 실행해도 된다: 새 파일만 만든다.
  python collect_xc.py
결과: data_raw/yahoo/<종목>_1d.json.gz, _1h.json.gz
"""
import datetime as dt, gzip, os, sys, time
try:
    import requests
except ImportError:
    sys.exit("pip install requests")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_raw", "yahoo")
SYMS = {
 "cn_substitute": ["0981.HK", "1347.HK", "688981.SS", "002371.SZ", "688012.SS", "688256.SS",
                   "688041.SS", "603501.SS", "688008.SS", "301269.SZ", "688120.SS", "688072.SS"],
 "cn_bench": ["512480.SS", "588000.SS", "159995.SZ", "000300.SS", "^HSI", "3033.HK", "2800.HK", "000688.SS"],
 "us_supplier": ["NVDA", "AMD", "AMAT", "LRCX", "KLAC", "SNPS", "CDNS", "MU", "QCOM", "INTC"],
 "ally_supplier": ["ASML", "TSM", "8035.T", "000660.KS", "005930.KS"],
}
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0 Safari/537.36"
NOW = dt.datetime.now(dt.timezone.utc)
os.makedirs(ROOT, exist_ok=True); ok = fail = 0
for sym in [s for g in SYMS.values() for s in g]:
    for itv, days in (("1d", 3300), ("1h", 725)):
        out = os.path.join(ROOT, "%s_%s.json.gz" % (sym.replace("^", "_").replace("=", "_"), itv))
        if os.path.exists(out) and os.path.getsize(out) > 0:
            ok += 1; continue
        p = {"period1": int((NOW - dt.timedelta(days=days)).timestamp()), "period2": int(NOW.timestamp()),
             "interval": itv, "includePrePost": "true"}
        body = b""
        for host in ("query1", "query2"):
            try:
                r = S.get("https://%s.finance.yahoo.com/v8/finance/chart/%s" % (host, sym), params=p, timeout=40)
                body = r.content
                if r.status_code == 200 and b'"timestamp"' in body: break
            except Exception as e:
                body = repr(e).encode()
            time.sleep(1.0)
        if b'"timestamp"' in body:
            gzip.open(out, "wb").write(body); ok += 1; print("ok  ", sym, itv, len(body))
        else:
            fail += 1; print("FAIL", sym, itv, body[:100])
        time.sleep(0.4)
print("done: ok=%d fail=%d  ->  %s" % (ok, fail, ROOT))
