"""분석 파이프라인 (PAP_v1.md 대로). 사용:
  python pipeline.py decode <data_raw 경로>      # 원자료 → work/fx_min.pkl, work/yahoo_*.parquet
  python pipeline.py run                          # 사건 반응·placebo·회귀·강건성 → out/*.csv
  python pipeline.py selftest                     # 합성 자료로 전 과정 점검
"""
import sys, os, io, json, gzip, zipfile, lzma, struct, glob, math
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work"); OUT = os.path.join(HERE, "out")
RNG = np.random.default_rng(20261115)
# 대략적 환율 수준(스케일 자동 판별용). 달러 대비 대상국 통화 약세가 +가 되도록 부호를 정한다.
LEVEL = {"USDCNH": 7.2, "USDMXN": 19, "USDCAD": 1.4, "EURUSD": 1.1, "USDJPY": 150, "GBPUSD": 1.3, "USDCHF": 0.85,
         "AUDUSD": 0.65, "USDZAR": 18, "USDSGD": 1.3, "USDTRY": 38, "USDHKD": 7.8, "XAUUSD": 3300}
SIGN = {k: (1 if k.startswith("USD") else -1) for k in LEVEL}


# ------------------------------------------------------------------ 디코딩
def decode_bi5(raw, day, inst):
    """Dukascopy 1분봉: LZMA 해제 후 24바이트 레코드(>5I f). 가격 열의 순서와 스케일은 자료로 판별한다."""
    try:
        b = lzma.decompress(raw)
    except lzma.LZMAError:
        return None
    n = len(b) // 24
    if n == 0:
        return None
    a = np.frombuffer(b[: n * 24], dtype=np.dtype([("t", ">u4"), ("a", ">u4"), ("b", ">u4"), ("c", ">u4"), ("d", ">u4"), ("v", ">f4")]))
    P = np.stack([a["a"], a["b"], a["c"], a["d"]], axis=1).astype(float)
    hi = int(np.argmax(P.sum(0))); lo = int(np.argmin(P.sum(0)))
    rest = [i for i in range(4) if i not in (hi, lo)]
    if len(rest) != 2:            # 변동이 없는 날: 관례 순서(open, close, low, high) 사용
        o, c = 0, 1
    else:                          # 종가[t] ≈ 시가[t+1] 인 쪽이 (open, close)
        x, y = rest
        e1 = np.abs(P[:-1, y] - P[1:, x]).mean() if n > 1 else 0
        e2 = np.abs(P[:-1, x] - P[1:, y]).mean() if n > 1 else 0
        o, c = (x, y) if e1 <= e2 else (y, x)
    med = np.median(P[:, c])
    scale = min((1e5, 1e3, 1e2, 1e4, 1e1, 1e6), key=lambda s: abs(math.log((med / s) / LEVEL.get(inst, med / 1e5))))
    ts = pd.Timestamp(day, tz="UTC") + pd.to_timedelta(a["t"].astype("int64"), unit="s")
    return pd.DataFrame({"ts": ts, "inst": inst, "close": P[:, c] / scale, "open": P[:, o] / scale, "vol": a["v"].astype("float64")})


def decode(raw_root):
    os.makedirs(WORK, exist_ok=True)
    rep = {}
    frames = []
    for zp in sorted(glob.glob(os.path.join(raw_root, "dukascopy", "*.zip"))):
        inst = os.path.basename(zp).rsplit("_", 1)[0]
        nd = 0
        with zipfile.ZipFile(zp) as z:
            for nm in z.namelist():
                if nm.endswith(".bi5"):
                    df = decode_bi5(z.read(nm), nm[:-4], inst)
                    if df is not None:
                        frames.append(df[df["vol"] > 0]); nd += 1
        rep[os.path.basename(zp)] = nd
    if frames:
        fx = pd.concat(frames, ignore_index=True).sort_values(["inst", "ts"])
        fx.to_pickle(os.path.join(WORK, "fx_min.pkl"))
        rep["fx_levels"] = fx.groupby("inst")["close"].median().round(4).to_dict()
    rows = []
    for fp in sorted(glob.glob(os.path.join(raw_root, "yahoo", "*.json.gz"))):
        sym, itv = os.path.basename(fp)[:-8].rsplit("_", 1)
        try:
            r = json.loads(gzip.open(fp).read())["chart"]["result"][0]
            q = r["indicators"]["quote"][0]
            d = pd.DataFrame({"ts": pd.to_datetime(r["timestamp"], unit="s", utc=True), "sym": sym, "itv": itv,
                              "open": q["open"], "close": q["close"], "vol": q.get("volume")})
            rows.append(d.dropna(subset=["close"]))
        except Exception as e:  # noqa
            rep["yahoo_fail_" + sym + itv] = repr(e)[:80]
    if rows:
        pd.concat(rows, ignore_index=True).to_pickle(os.path.join(WORK, "yahoo.pkl"))
        rep["yahoo_series"] = len(rows)
    json.dump(rep, open(os.path.join(WORK, "decode_report.json"), "w"), indent=1, default=str)
    print(json.dumps(rep, default=str)[:1500])


# ------------------------------------------------------------------ 사건·신뢰도
W = {"EXECUTED": 1.0, "EXECUTED_PARTIAL": 0.5, "NOT_EXECUTED": 0.0}


def load_events(partial=0.5, rule_days=90):
    ev = pd.read_csv(os.path.join(HERE, "events_v1.csv"), encoding="utf-8-sig", dtype=str).fillna("")
    def ts(r):
        if r["time_et"] and ":" in r["time_et"]:
            return pd.Timestamp(r["date"] + " " + r["time_et"], tz="America/New_York").tz_convert("UTC")
        return pd.NaT
    ev["ts"] = ev.apply(ts, axis=1)
    ev["day"] = pd.to_datetime(ev["date"])
    ev["odate"] = pd.to_datetime(ev["outcome_date"], errors="coerce")
    if rule_days != 90:   # 90일 규칙으로 확정한 사건만 날짜를 옮긴다
        m = ev["outcome_basis"].str.contains("90일 규칙")
        ev.loc[m, "odate"] = ev.loc[m, "day"] + pd.Timedelta(days=rule_days)
    w = dict(W); w["EXECUTED_PARTIAL"] = partial
    ev["w"] = ev["outcome"].map(w)
    return ev


def credibility(ev, window_days=None):
    """각 사건 시점까지 결과가 확정된 과거 ESC만으로 Beta(1,1) 사후평균."""
    esc = ev[(ev["type"] == "ESC") & ev["w"].notna()]
    out = []
    for _, r in ev.iterrows():
        past = esc[(esc["odate"] <= r["day"]) & (esc["day"] < r["day"])]
        if window_days:
            past = past[past["odate"] >= r["day"] - pd.Timedelta(days=window_days)]
        tg = set(r["target"].split(";"))
        same = past[past["target"].apply(lambda s: bool(tg & set(s.split(";"))))]
        c_all = (1 + past["w"].sum()) / (2 + len(past))
        c_tgt = (1 + same["w"].sum()) / (2 + len(same)) if len(same) else c_all
        out.append((c_all, c_tgt, len(past), int((past["w"] == 0).sum())))
    return pd.DataFrame(out, columns=["C_all", "C_tgt", "n_past", "N_fail"], index=ev.index)


# ------------------------------------------------------------------ 반응
class Series:
    """UTC 나노초 정렬 배열. tol_min: 창 끝에서 허용하는 최대 공백(분)."""
    def __init__(self, ts, px, tol_min=10):
        self.t = np.asarray(ts.astype("datetime64[ns]").astype("int64")); self.p = np.asarray(px, float); self.tol = tol_min * 60 * 10**9

    def ret(self, t0, pre, post):
        """[t0-pre, t0+post] 로그수익률(%). 사건 시각에 시장이 닫혀 있으면 직전 마지막 가격 → 재개 후 post분. (값, 휴장여부)"""
        M = 60 * 10**9
        j = np.searchsorted(self.t, t0, side="right")            # 사건 뒤 첫 관측
        if j >= len(self.t) or j == 0:
            return np.nan, False
        closed = (self.t[j] - t0) > 30 * M
        if closed:
            ia = j - 1; t_end = self.t[j] + post * M
        else:
            ia = np.searchsorted(self.t, t0 - pre * M, side="right") - 1; t_end = t0 + post * M
            if ia < 0 or (t0 - pre * M) - self.t[ia] > self.tol:
                return np.nan, False
        ib = np.searchsorted(self.t, t_end, side="right") - 1
        if ib <= ia or t_end - self.t[ib] > self.tol:
            return np.nan, closed
        return 100 * math.log(self.p[ib] / self.p[ia]), closed


MKT = ["USA500IDXUSD", "ES_F"]       # 시장 전체 반응: 분 단위 CFD가 있으면 그것, 없으면 Yahoo 선물 시간봉


def build_series(fx, yh=None):
    # Dukascopy 타임스탬프는 1분봉의 시작 시각 → 종가 시각(+1분)으로 옮긴다
    S = {k: Series((g["ts"] + pd.Timedelta(minutes=1)).dt.tz_convert(None).to_numpy(), g["close"].to_numpy()) for k, g in fx.sort_values("ts").groupby("inst")}
    if yh is not None:
        g = yh[(yh["sym"] == "ES_F") & (yh["itv"] == "1h")].sort_values("ts")
        if len(g):   # Yahoo 타임스탬프는 bar 시작 → 종가 시각으로 옮긴다
            S["ES_F"] = Series((g["ts"] + pd.Timedelta(hours=1)).dt.tz_convert(None).to_numpy(), g["close"].to_numpy(), tol_min=75)
    return S


def one(Sr, t0, pre, post, sign, edays, n_placebo=60):
    x, closed = Sr.ret(t0, pre, post)
    pl = []; D = 86400 * 10**9
    for k in list(range(7, 7 * 3 * n_placebo, 7)) + [d for d in range(1, 121) if d % 7]:
        if len(pl) >= n_placebo:
            break
        t = t0 - k * D
        if str((pd.Timestamp(t, tz="UTC").tz_convert("America/New_York")).date()) in edays:
            continue
        v, _ = Sr.ret(t, pre, post)
        if not np.isnan(v):
            pl.append(v)
    sd = np.std(pl, ddof=1) if len(pl) >= 20 else np.nan
    return dict(ret=sign * x, sd=sd, z=(sign * x / sd if sd and not np.isnan(sd) else np.nan), n_pl=len(pl), closed=closed,
                p_pl=(float(np.mean(np.abs(pl) >= abs(x))) if len(pl) >= 20 and not np.isnan(x) else np.nan))


def responses(ev, S, win=(5, 30)):
    """사건별: 시장 전체(주가 하락=+)와 대상 통화(약세=+)의 표준화 반응, 둘의 평균(z_comp)."""
    edays = set(ev["date"]); rows = []
    mk = next((m for m in MKT if m in S), None)
    for _, r in ev.iterrows():
        if pd.isna(r["ts"]):
            continue
        t0 = int(r["ts"].tz_convert(None).to_datetime64().astype("datetime64[ns]").astype("int64"))
        rec = dict(id=r["id"])
        if mk:
            w = win if mk != "ES_F" else (60, 60)
            m = one(S[mk], t0, w[0], w[1], -1, edays); rec.update(z_mkt=m["z"], ret_mkt=m["ret"], p_mkt=m["p_pl"], closed=m["closed"])
        zs = []; rs = []
        for inst in [i for i in r["fx"].split(";") if i in S]:
            f = one(S[inst], t0, win[0], win[1], SIGN.get(inst, 1), edays); zs.append(f["z"]); rs.append(f["ret"])
            rec.setdefault("closed", f["closed"])
        if zs:
            rec.update(z_fx=np.nanmean(zs), ret_fx=np.nanmean(rs))
        zz = [v for v in (rec.get("z_mkt"), rec.get("z_fx")) if v is not None and not np.isnan(v)]
        rec["z"] = float(np.mean(zz)) if zz else np.nan
        rows.append(rec)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ 추정·추론
def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    XtXi = np.linalg.pinv(X.T @ X)
    h = np.clip(np.einsum("ij,jk,ik->i", X, XtXi, X), 0, 0.99)
    V = XtXi @ (X.T * (e / (1 - h)) ** 2) @ X @ XtXi      # HC3
    return b, np.sqrt(np.diag(V)), e


def infer(y, x, Z=None, B=9999):
    """y = a + b·x (+Z). b의 HC3 표준오차, wild bootstrap(Rademacher, 귀무 부과) p, 순열 p."""
    n = len(y)
    X = np.column_stack([np.ones(n), x] + ([Z] if Z is not None else []))
    b, se, e = ols(y, X)
    t = b[1] / se[1] if se[1] > 0 else np.nan
    X0 = np.delete(X, 1, axis=1); b0, _, e0 = ols(y, X0)
    tb = np.empty(B); tp = np.empty(B)
    for i in range(B):
        yb = X0 @ b0 + e0 * RNG.choice([-1.0, 1.0], n)
        bb, sb, _ = ols(yb, X); tb[i] = bb[1] / sb[1] if sb[1] > 0 else 0
        Xp = X.copy(); Xp[:, 1] = RNG.permutation(x)
        bp, sp, _ = ols(y, Xp); tp[i] = bp[1] / sp[1] if sp[1] > 0 else 0
    return dict(n=n, b=b[1], se=se[1], t=t, p_wild=float(np.mean(np.abs(tb) >= abs(t))), p_perm=float(np.mean(np.abs(tp) >= abs(t))),
                sd_resid=float(np.std(e, ddof=X.shape[1])))


def mde(x, sd_resid, power=0.8, alpha=0.05):
    """단순회귀 기울기의 최소검출효과(양측 5%, 검정력 80%, 정규근사)."""
    sx = np.std(x, ddof=1) * math.sqrt(len(x) - 1)
    return (1.96 + 0.8416) * sd_resid / sx if sx > 0 else np.nan


def perm_diff(x, y, B=9999):
    """두 집단 평균 차이(x-y)의 순열 p값(양측)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3 or len(y) < 3:
        return dict(n1=len(x), n2=len(y))
    d = x.mean() - y.mean(); z = np.r_[x, y]; n = len(x); c = 0
    for _ in range(B):
        p = RNG.permutation(z); c += abs(p[:n].mean() - p[n:].mean()) >= abs(d)
    return dict(n1=len(x), n2=len(y), m1=x.mean(), m2=y.mean(), diff=d, p_perm=c / B,
                se=math.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y)))


def mean_test(z):
    """표준화 반응의 평균이 0인지: 귀무에서 z~(0,1) → 평균의 표준오차 1/sqrt(n). 표본 t도 함께."""
    z = np.asarray(z, float); n = len(z)
    if n < 3:
        return dict(n=n)
    return dict(n=n, mean=z.mean(), z_stat=z.mean() * math.sqrt(n), t_stat=z.mean() / (z.std(ddof=1) / math.sqrt(n)), share_pos=float((z > 0).mean()))


def contrasts(d, tag=""):
    """PAP v1.1의 주 검정(수준·대비). d: run()의 main 사건표."""
    rows = []
    def add(name, r): r = dict(r); r["test"] = name; rows.append(r)
    for y in ("z", "z_mkt", "z_fx"):
        if y not in d:
            continue
        E = d[(d["type"] == "ESC")].dropna(subset=[y]).sort_values("day")
        Dn = d[(d["type"] == "DEESC")].dropna(subset=[y]).sort_values("day")
        Im = d[(d["type"] == "IMPL")].dropna(subset=[y])
        add(f"T1 ESC mean [{y}]", mean_test(E[y]))
        h = len(E) // 2
        add(f"T1a ESC early [{y}]", mean_test(E[y].iloc[:h])); add(f"T1b ESC late [{y}]", mean_test(E[y].iloc[h:]))
        add(f"T1c ESC early-late [{y}]", perm_diff(E[y].iloc[:h], E[y].iloc[h:]))
        ex = E[E["outcome"].isin(["EXECUTED", "EXECUTED_PARTIAL"])][y]; nx = E[E["outcome"] == "NOT_EXECUTED"][y]
        add(f"T2 ESC executed-notexecuted [{y}]", perm_diff(ex, nx))
        add(f"T3 IMPL mean [{y}]", mean_test(Im[y])); add(f"T3a |IMPL|-|ESC| [{y}]", perm_diff(Im[y].abs(), E[y].abs()))
        add(f"T4 DEESC mean [{y}]", mean_test(Dn[y]))
        h2 = len(Dn) // 2
        add(f"T4a DEESC early-late [{y}]", perm_diff(Dn[y].iloc[:h2], Dn[y].iloc[h2:]))
    T = pd.DataFrame(rows); T.to_csv(os.path.join(OUT, f"contrasts{tag}.csv"), index=False)
    return T


def run(S=None, tag="", B_main=9999):
    os.makedirs(OUT, exist_ok=True)
    if S is None:
        fx = pd.read_pickle(os.path.join(WORK, "fx_min.pkl"))
        yp = os.path.join(WORK, "yahoo.pkl")
        S = build_series(fx, pd.read_pickle(yp) if os.path.exists(yp) else None)
    I = lambda e: e
    specs = [("main", {}, "C_all", None, (5, 30), I), ("C_tgt", {}, "C_tgt", None, (5, 30), I), ("C_180", {}, "C_all", 180, (5, 30), I),
             ("N_fail", {}, "N_fail", None, (5, 30), I), ("win15", {}, "C_all", None, (5, 15), I), ("win60", {}, "C_all", None, (5, 60), I),
             ("win120", {}, "C_all", None, (5, 120), I),
             ("no_prior_viewed", {}, "C_all", None, (5, 30), lambda e: e[e["prior_viewed"] != "1"]),
             ("no_closed", {}, "C_all", None, (5, 30), lambda e: e[e["closed"] != True]),
             ("no_apr2025", {}, "C_all", None, (5, 30), lambda e: e[~e["date"].between("2025-04-02", "2025-04-09")]),
             ("partial0", dict(partial=0.0), "C_all", None, (5, 30), I), ("partial1", dict(partial=1.0), "C_all", None, (5, 30), I),
             ("rule60", dict(rule_days=60), "C_all", None, (5, 30), I), ("rule120", dict(rule_days=120), "C_all", None, (5, 30), I)]
    res = []; keep = None; cache = {}
    for name, kw, cvar, wd, win, filt in specs:
        ev = load_events(**kw); ev = pd.concat([ev, credibility(ev, wd)], axis=1)
        if win not in cache:
            cache[win] = responses(ev, S, win)
        d = filt(ev.merge(cache[win], on="id")).dropna(subset=["z"]).copy()
        d["days"] = (d["day"] - pd.Timestamp("2025-01-20")).dt.days / 365
        if name == "main":
            keep = d; d.drop(columns=["ts", "day", "odate"]).to_csv(os.path.join(OUT, f"event_responses{tag}.csv"), index=False, encoding="utf-8-sig")
        for typ in ("ESC", "DEESC", "IMPL"):
            for yv in (("z", "z_mkt", "z_fx", "absz") if name == "main" else ("z",)):
                s = d[d["type"] == typ]
                col = "z" if yv == "absz" else yv
                s = s.dropna(subset=[col]) if col in s else s.iloc[:0]
                if len(s) < 6 or s[cvar].std() == 0:
                    res.append(dict(spec=name, type=typ, y=yv, n=len(s))); continue
                y = (s["z"].abs() if yv == "absz" else s[col]).to_numpy(float); x = s[cvar].to_numpy(float)
                r1 = infer(y, x, B=B_main if name == "main" else 1999)
                r1.update(spec=name, type=typ, y=yv, mean_y=float(y.mean()), mde80=mde(x, r1["sd_resid"])); res.append(r1)
                if name == "main" and yv == "z":
                    r2 = infer(y, x, Z=s["days"].to_numpy(float), B=B_main); r2.update(spec="main+time", type=typ, y=yv); res.append(r2)
    T = pd.DataFrame(res); T.to_csv(os.path.join(OUT, f"regressions{tag}.csv"), index=False)
    return keep, T


# ------------------------------------------------------------------ 자체 점검
def selftest(true_b=3.0):
    """합성 1분봉에 '신뢰도에 비례하는 점프'(z 단위 기울기 true_b)를 심어 디코더·휴장 처리·회귀가 되찾는지 본다."""
    ev = load_events(); ev = pd.concat([ev, credibility(ev)], axis=1)
    idx = pd.date_range("2024-11-01", "2026-11-13", freq="1min", tz="UTC"); idx = idx[idx.dayofweek < 5]
    sig = 0.00012; frames = []
    for inst, lv in list(LEVEL.items()) + [("USA500IDXUSD", 6000)]:
        r = RNG.normal(0, sig, len(idx)); sg = SIGN.get(inst, -1)
        for _, e in ev[ev["ts"].notna() & (ev["type"] == "ESC")].iterrows():
            if inst == "USA500IDXUSD" or inst in e["fx"].split(";"):
                j = idx.searchsorted(e["ts"]) + 2
                if j < len(idx):
                    r[j] += sg * true_b * e["C_all"] * sig * math.sqrt(35)
        frames.append(pd.DataFrame({"ts": idx, "inst": inst, "close": lv * np.exp(np.cumsum(r)), "vol": 1.0}))
    fx = pd.concat(frames)
    d = fx[(fx["inst"] == "USDJPY") & (fx["ts"].dt.date == pd.Timestamp("2025-03-11").date())]
    c = d["close"].to_numpy(); o = np.r_[c[0], c[:-1]]
    rec = b"".join(struct.pack(">5If", int((t - pd.Timestamp("2025-03-11", tz="UTC")).total_seconds()), int(round(a * 1e3)), int(round(b * 1e3)),
                               int(round(min(a, b) * 1e3)) - 1, int(round(max(a, b) * 1e3)) + 1, 1.0) for t, a, b in zip(d["ts"], o, c))
    back = decode_bi5(lzma.compress(rec), "2025-03-11", "USDJPY")
    print("bi5 왕복 최대오차:", float(np.abs(back["close"].to_numpy() - np.round(c, 3)).max()))
    keep, T = run(build_series(fx), tag="_selftest", B_main=1999)
    print("심은 기울기(z 단위)", true_b, "| C_all 범위", round(keep["C_all"].min(), 3), "–", round(keep["C_all"].max(), 3),
          "| 휴장 중 사건", int(keep["closed"].sum()))
    print(T[(T["spec"] == "main") & (T["y"] == "z")][["spec", "type", "y", "n", "mean_y", "b", "se", "p_wild", "mde80"]].round(3).to_string(index=False))
    print(contrasts(keep, "_selftest").round(3).to_string(index=False))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "selftest"
    if cmd == "decode":
        decode(sys.argv[2])
    elif cmd == "run":
        k, T = run(); print(T.round(3).to_string(index=False)); print(contrasts(k).round(3).to_string(index=False))
    else:
        selftest()
