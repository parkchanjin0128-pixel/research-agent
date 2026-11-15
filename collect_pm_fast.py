#!/usr/bin/env python3
"""예측시장 가격 이력 병렬 수집 (Polymarket + Kalshi). 재개 가능.
느렸던 이유 두 가지를 고친다: (1) 시장별 존속 기간만 요청, (2) 스레드 16개로 병렬.
'say/mention' 류 발언 맞히기 시장은 실행 확률과 무관해 제외한다.
"""
import datetime as dt, gzip, json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
import requests
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_raw")
START = dt.datetime(2024, 11, 1, tzinfo=dt.timezone.utc); NOW = dt.datetime.now(dt.timezone.utc)
KEY = ["tariff", "trade deal", "trade war", "trade agreement", "reciprocal", "section 232", "ieepa",
       "export control", "liberation day", "duties", "trade truce", "customs"]
JUNK = re.compile(r"\bsays?\b|mention|tweet|\bpost\b", re.I)
hit = lambda t: any(k in (t or "").lower() for k in KEY)
tl = threading.local()
def sess():
    if not hasattr(tl, "s"):
        tl.s = requests.Session(); tl.s.headers["User-Agent"] = "Mozilla/5.0 Chrome/126.0 Safari/537.36"
    return tl.s
def get(url, params, tries=4):
    for i in range(tries):
        try:
            r = sess().get(url, params=params, timeout=30)
            if r.status_code == 200: return r.json()
            if r.status_code in (400, 404, 422): return None
        except Exception: pass
        time.sleep(1.5 * (i + 1))
    return None
def ts(s, default):
    try: return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception: return default
def exists(p): return os.path.exists(p) and os.path.getsize(p) > 0

def pm_one(job):
    tid, m = job; out = os.path.join(ROOT, "polymarket", "prices", tid + ".json")
    if exists(out): return 1
    js = get("https://clob.polymarket.com/prices-history", {"market": tid, "interval": "max", "fidelity": 60}, 2)
    hist = (js or {}).get("history") or []
    if not hist:
        a = max(START, ts(m.get("startDate") or "", START)) - dt.timedelta(days=1)
        b = min(NOW, ts(m.get("closedTime") or m.get("endDate") or "", NOW) + dt.timedelta(days=3))
        t0 = int(a.timestamp())
        while t0 < b.timestamp():
            t1 = t0 + 14 * 86400
            js = get("https://clob.polymarket.com/prices-history", {"market": tid, "startTs": t0, "endTs": t1, "fidelity": 60}, 2)
            hist += (js or {}).get("history") or []; t0 = t1
    json.dump({"token": tid, "question": m.get("question"), "slug": m.get("slug"), "startDate": m.get("startDate"),
               "endDate": m.get("endDate"), "closedTime": m.get("closedTime"), "closed": m.get("closed"),
               "outcomePrices": m.get("outcomePrices"), "history": hist}, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    return int(len(hist) > 0)

def run_pm():
    os.makedirs(os.path.join(ROOT, "polymarket", "prices"), exist_ok=True)
    jobs = []
    for line in gzip.open(os.path.join(ROOT, "polymarket", "events.jsonl.gz"), "rt", encoding="utf-8"):
        for m in json.loads(line).get("markets") or []:
            if JUNK.search(m.get("question") or ""): continue
            ids = m.get("clobTokenIds"); ids = json.loads(ids) if isinstance(ids, str) else (ids or [])
            if ids: jobs.append((str(ids[0]), m))
    with ThreadPoolExecutor(16) as ex: res = list(ex.map(pm_one, jobs))
    print("polymarket: 가격 이력 %d/%d 시장" % (sum(res), len(jobs)), flush=True)

API = "https://api.elections.kalshi.com/trade-api/v2"
def ks_one(job):
    e, m = job; tk = m["ticker"]; out = os.path.join(ROOT, "kalshi", "candles", tk + ".json")
    if exists(out): return 1
    a = max(START, ts(m.get("open_time") or "", START)); b = min(NOW, ts(m.get("close_time") or "", NOW))
    candles, t0 = [], int(a.timestamp())
    while t0 < b.timestamp():
        t1 = min(int(b.timestamp()), t0 + 180 * 86400); got = None
        for path in ("/series/%s/markets/%s/candlesticks" % (e.get("series_ticker"), tk), "/historical/markets/%s/candlesticks" % tk):
            js = get(API + path, {"start_ts": t0, "end_ts": t1, "period_interval": 60}, 2)
            got = (js or {}).get("candlesticks")
            if got: break
        candles += got or []; t0 = t1 + 1
    json.dump({"ticker": tk, "title": m.get("title"), "event_title": e.get("title"), "open_time": m.get("open_time"),
               "close_time": m.get("close_time"), "result": m.get("result"), "candlesticks": candles},
              open(out, "w", encoding="utf-8"), ensure_ascii=False)
    return int(len(candles) > 0)

def ks_list(status):
    evs, cursor = [], ""
    for page in range(600):
        js = get(API + "/events", {"limit": 200, "status": status, "cursor": cursor, "with_nested_markets": "true"})
        if not js: break
        evs += [e for e in js.get("events") or [] if hit(e.get("title")) or hit(e.get("sub_title")) or hit(e.get("series_ticker"))]
        cursor = js.get("cursor") or ""
        if not cursor: break
    print("kalshi %s: 해당 %d건 (%d쪽)" % (status, len(evs), page + 1), flush=True); return evs

def run_ks():
    os.makedirs(os.path.join(ROOT, "kalshi", "candles"), exist_ok=True)
    evp = os.path.join(ROOT, "kalshi", "events.jsonl.gz")
    if exists(evp): events = [json.loads(x) for x in gzip.open(evp, "rt", encoding="utf-8")]
    else:
        with ThreadPoolExecutor(3) as ex: events = [e for part in ex.map(ks_list, ("settled", "closed", "open")) for e in part]
        if events:
            with gzip.open(evp, "wt", encoding="utf-8") as f:
                for e in events: f.write(json.dumps(e, ensure_ascii=False) + "\n")
    jobs = [(e, m) for e in events for m in e.get("markets") or [] if m.get("ticker")]
    with ThreadPoolExecutor(8) as ex: res = list(ex.map(ks_one, jobs))
    print("kalshi: 가격 이력 %d/%d 시장" % (sum(res), len(jobs)), flush=True)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("pm", "both"): run_pm()
    if which in ("ks", "both"): run_ks()
