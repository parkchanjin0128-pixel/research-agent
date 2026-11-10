"""PCX-02 only: outcome-free calendar fixture; run with python3, no dependencies.

Source pin: b83642b38db733d0d4e83e9a23eb14a45041c049.
CW = placebo_crosswalk.md §§2–4; MD = main_design_execution_revision_nov09.md
§§1–2 (Pool A main case). Inputs are synthetic UTC facts, not study dates.
The fixed oracles have separate CW/MD columns; the shared evaluator
is tested against each applicable column. No production data or outcomes.
"""
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone

OK, OUT, ACTIVE, MIXED, PRIOR, CONTROL, UNKNOWN, DATE = (
    "eligible", "outside_signal", "binding_active", "mixed",
    "prior_binding_history", "control_contaminated", "unknown", "outcome_date_unknown",
)
PENDING, EMPTY = "input_pending", "confirmed_empty"
UTC = timezone.utc
SECOND = timedelta(seconds=1)


def utc(s):
    return datetime.fromisoformat(s).replace(tzinfo=UTC)


def month(i):
    return datetime(i // 12, i % 12 + 1, 1, tzinfo=UTC)


def idx(s):
    d = utc(s + "-01")
    return d.year * 12 + d.month - 1


def key(i):
    return month(i).strftime("%Y-%m")


def span(lo, hi):
    return tuple(range(idx(lo), idx(hi) + 1))


def exact(t):
    return (t, t)


JAN = idx("2019-01")
A, B = month(JAN), month(JAN + 1)
MID, END = A + timedelta(days=14), B - SECOND
W_CANDIDATES = span("2018-12", "2019-04")
PRE_CANDIDATES = span("2015-01", "2018-12")
# Arm, country, transaction. "x2" must stay in the frozen risk set.
FRAME = (("L", "CN", "x1"), ("L", "JP", "x1"), ("N", "CN", "x1"),
         ("N", "JP", "x1"), ("N", "JP", "x2"))
L, N = FRAME[0], FRAME[-1]


@dataclass(frozen=True)
class Rule:
    source: str
    start: tuple = ()
    stop: tuple = ()
    scope: str = "binding"  # binding, zero (verified), or unknown
    history: bool = False  # confirmed actual added binding after R, ended by W start


@dataclass(frozen=True)
class Cell:
    signal: tuple = exact(A - SECOND)
    pre_event: tuple = exact(A - SECOND)  # earliest signal/anticipation/direct event
    rules: tuple = ()
    control: str = "clean"
    residual: str = "clean"  # residual direct effect of a prior measure
    coverage: str = "verified"
    decision: tuple = ()  # exact synthetic interval, empty means verified in-month
    decision_known: bool = True


def relation(values, predicate, fail):
    """An inclusive possible-time range passes only if all endpoints pass."""
    if not values:
        return UNKNOWN
    result = {predicate(t) for t in values}
    return OK if result == {True} else fail if result == {False} else UNKNOWN


def classify_rule(rule, a, b):
    if rule.scope == "zero":
        return "not_binding_in_scope"
    if rule.scope != "binding" or not rule.start:
        return UNKNOWN
    # Intervals [start, stop); evaluate all extreme admissible event times.
    def point(s, e):
        if s >= b or (e is not None and e <= a):
            return OK
        return ACTIVE if s <= a and (e is None or e >= b) else MIXED

    labels = {point(s, e) for s in rule.start for e in rule.stop or (None,)
              if e is None or s < e}
    if len(labels) != 1:
        return UNKNOWN
    return labels.pop()


def cell_audit(i, unit, c, phase):
    a, b = month(i), month(i + 1)
    reasons = []

    def add(label, source):
        if label != OK:
            reasons.append((label, source))

    if phase == "W" and unit[0] == "L":
        add(relation(c.signal, lambda t: t < a, OUT), "listed_signal")
    if phase == "pre":
        add(relation(c.pre_event, lambda t: b <= t, OUT), "pre_event")
    if unit[0] == "N":
        add({"clean": OK, "confirmed": CONTROL, "unknown": UNKNOWN}[c.control],
            "control_signal_or_spillover")
    add({"clean": OK, "confirmed": CONTROL, "unknown": UNKNOWN}[c.residual],
        "prior_residual_direct_effect")
    if c.coverage != "verified":
        add(UNKNOWN, "coverage")
    if not c.decision_known or any(not a <= t < b for t in c.decision):
        add(DATE, "decision_clock")
    for rule in c.rules:
        add(classify_rule(rule, a, b), rule.source)
        if phase == "W" and rule.history:
            add(PRIOR, rule.source)
    return tuple(reasons) or ((OK, "all_required_checks"),)


def audit_window(candidates, overrides, phase, base=Cell(), *, frame=FRAME):
    rows = {i: {u: cell_audit(i, u, overrides.get((i, u), base), phase)
                for u in frame} for i in candidates}
    def group(i):
        return {label for reasons in rows[i].values() for label, _ in reasons} - {
            OK, "not_binding_in_scope"}
    confirmed = tuple(i for i in candidates if not group(i))
    possible = tuple(i for i in candidates if group(i) and group(i) <= {UNKNOWN, DATE})
    return rows, confirmed, possible


def window_status(good, possible):
    return "eligible_window" if good else PENDING if possible else EMPTY


def check(value, expected, name):
    if value != expected:
        raise AssertionError(f"{name}: got {value!r}; expected {expected!r}")


# Each row has the two fixed document expectations (CW §3; MD §1/table).
# DATE and pre-event labels are normalized to the MD vocabulary for comparison.
CLEAN = Cell()
EARLY_BINDING = Rule("old_rule", exact(utc("2018-11-01")), exact(MID))
LABEL_CASES = (
    ("signal just before start", L, CLEAN, (OK,), (OK,)),
    ("signal exactly at start", L, replace(CLEAN, signal=exact(A)), (OUT,), (OUT,)),
    ("signal straddles start", L, replace(CLEAN, signal=(A - SECOND, A)), (UNKNOWN,), (UNKNOWN,)),
    ("clean nonlisted, no dummy signal", N, replace(CLEAN, signal=()), (OK,), (OK,)),
    ("binding starts exactly at end", N, replace(CLEAN, rules=(Rule("end", exact(B)),)), (OK,), (OK,)),
    ("binding starts one second before end", N, replace(CLEAN, rules=(Rule("last", exact(END)),)), (MIXED,), (MIXED,)),
    ("binding starts exactly at start and persists", N, replace(CLEAN, rules=(Rule("start", exact(A)),)), (ACTIVE,), (ACTIVE,)),
    ("binding starts mid-month", N, replace(CLEAN, rules=(Rule("mid", exact(MID)),)), (MIXED,), (MIXED,)),
    ("binding ends exactly at month end", N, replace(CLEAN, rules=(Rule(
        "end_exact", exact(A - SECOND), exact(B)),)), (ACTIVE,), (ACTIVE,)),
    ("binding ends mid-month", N, replace(CLEAN, rules=(EARLY_BINDING,)), (MIXED,), (MIXED,)),
    ("possible binding starts straddle end", N, replace(CLEAN, rules=(Rule("range", (END, B)),)), (UNKNOWN,), (UNKNOWN,)),
    ("date-only binding straddles end in UTC", N,
     replace(CLEAN, rules=(Rule("date_only",
         (datetime(2019, 2, 1, tzinfo=timezone(timedelta(hours=9))).astimezone(UTC),
          datetime(2019, 2, 1, 23, 59, 59, tzinfo=timezone(timedelta(hours=9))).astimezone(UTC))),)),
     (UNKNOWN,), (UNKNOWN,)),
    ("prior binding ended before W", N, replace(CLEAN, rules=(Rule("released",
        exact(utc("2018-12-05")), exact(A - SECOND), history=True),)), (PRIOR,), (PRIOR,)),
    ("zero intensity is evidence, not missing", N, replace(CLEAN, rules=(Rule("zero", scope="zero"),)),
     ("not_binding_in_scope",), ("not_binding_in_scope",)),
    ("unknown applicability is not zero", N, replace(CLEAN, rules=(Rule("unknown", scope="unknown"),)),
     (UNKNOWN,), (UNKNOWN,)),
    ("confirmed control contamination", N, replace(CLEAN, control="confirmed"), (CONTROL,), (CONTROL,)),
    ("unverified decision date", N, replace(CLEAN, decision_known=False), (DATE,), (DATE,)),
    ("decision interval crosses start", N, replace(CLEAN, decision=(A - SECOND, MID)), (DATE,), (DATE,)),
    ("decision interval inside month", N, replace(CLEAN, decision=(A, MID)), (OK,), (OK,)),
    ("unknown coverage", N, replace(CLEAN, coverage="unknown"), (UNKNOWN,), (UNKNOWN,)),
)


def labels_tests():
    for name, unit, cell, cw, md in LABEL_CASES:
        rows, good, possible = audit_window((JAN,), {(JAN, unit): cell}, "W")
        for doc, expected in (("CW", cw), ("MD", md)):
            check(tuple(x[0] for x in rows[JAN][unit]), expected, (name, doc, "labels"))
            expect_good = (JAN,) if expected[0] in {OK, "not_binding_in_scope"} else ()
            expect_possible = (JAN,) if expected[0] in {UNKNOWN, DATE} else ()
            check((good, possible), (expect_good, expect_possible), (name, doc, "W"))


def intersection_tests():
    # Other candidate months have verified direct restrictions on one transaction.
    blocked = replace(CLEAN, rules=(Rule("other_month_restriction", exact(utc("2018-12-01"))),))
    initial = {(i, N): blocked for i in W_CANDIDATES if i != JAN}
    mixed = replace(CLEAN, rules=(Rule("one_transaction_direct_measure", exact(MID)),))
    multi = replace(mixed, coverage="unknown", decision_known=False, control="confirmed",
                    rules=mixed.rules + (Rule("other_direct_measure", exact(MID)),))
    window_cases = (
        ("only January fully clean", CLEAN, ("eligible_window", (JAN,), ()),
         ("eligible_window", (JAN,), ())),
        ("one arm/transaction drops January", mixed, (EMPTY, (), ()), (EMPTY, (), ())),
        ("January possible with unknown", replace(CLEAN, coverage="unknown"),
         (PENDING, (), (JAN,)), (PENDING, (), (JAN,))),
        ("confirmed blockers plus unknown", multi, (EMPTY, (), ()), (EMPTY, (), ())),
    )
    for name, cell, cw, md in window_cases:
        rows, good, possible = audit_window(W_CANDIDATES, initial | {(JAN, N): cell}, "W")
        for doc, expected in (("CW", cw), ("MD", md)):
            check((window_status(good, possible), good, possible), expected, (name, doc))
        if cell is multi:
            check(rows[JAN][N], ((CONTROL, "control_signal_or_spillover"), (UNKNOWN, "coverage"),
                  (DATE, "decision_clock"), (MIXED, "one_transaction_direct_measure"),
                  (MIXED, "other_direct_measure")), "retain all source-linked reasons")
            check(all(rows[JAN][u][0][0] == OK for u in FRAME if u != N),
                  True, "other frozen cells cannot rescue January")
    return initial, mixed


def pool_c_gate(calendar, audited_events, equality):
    cutoff = min(bounds[0] for bounds in audited_events.values())
    labels = {i: OK if month(i + 1) < cutoff or
              (equality and month(i + 1) == cutoff) else "pool_c_cutoff_excluded"
              for i in calendar}
    return tuple(labels.values()), tuple(i for i in calendar if labels[i] == OK)


def pool_c_test():
    # CW §§2–3: earliest audited lower bound, not eventual listing.
    # Exact equality is not specified separately for Pool C; the strict wording
    # and inherited half-open convention yield different January sets.
    calendar = span("2018-12", "2019-02")
    outside = "pool_c_cutoff_excluded"  # fixture label for CW-specific gate
    cases = (
        ("month ends before lower bound", B + SECOND,
         ((OK, OK, outside), (JAN - 1, JAN)), ((OK, OK, outside), (JAN - 1, JAN)),
         ("out_of_scope", None)),
        ("month ends at lower bound", B,
         ((OK, outside, outside), (JAN - 1,)), ((OK, OK, outside), (JAN - 1, JAN)),
         ("out_of_scope", None)),
        ("possible first event straddles month end", B - SECOND,
         ((OK, outside, outside), (JAN - 1,)), ((OK, outside, outside), (JAN - 1,)),
         ("out_of_scope", None)),
    )
    for source in ("related_signal", "binding", "direct_concurrent_action"):
        for name, lo, cw_literal, cw_half_open, md in cases:
            events = dict.fromkeys(("related_signal", "binding", "direct_concurrent_action"),
                                   exact(B + timedelta(days=10)))
            events[source] = (lo, B + 2 * SECOND)
            check(pool_c_gate(calendar, events, equality=False), cw_literal, ("CW literal", source, name))
            check(pool_c_gate(calendar, events, equality=True), cw_half_open, ("CW half-open", source, name))
            # MD §1 specifies Pool A. Do not call either C rule in an MD run.
            check(md_pool_c(), md, ("MD scope", source, name))
            check(cw_literal == cw_half_open, lo != B, ("C conflict occurs only at equality", name))
    print("UNRESOLVED Pool C equality: CW literal gate={2018-12}; inherited half-open "
          "gate={2018-12,2019-01}; MD Pool C=out_of_scope (no applicable W/label).")


def md_pool_c():
    return "out_of_scope", None


def pre_windows(overrides, base, w):
    rows, good, _ = audit_window(PRE_CANDIDATES, overrides, "pre", base)
    ok = set(good)
    r = next((run for i in reversed(PRE_CANDIDATES)
              if set(run := tuple(range(i - 11, i + 1))) <= ok), ())
    if not (r and w):
        return rows, r, (), (), ()
    p = tuple(range(r[0] - len(w), r[0]))
    q = tuple(range(p[0] - 12, p[0]))
    if not set(q + p) <= ok:
        return rows, r, (), (), ()
    return rows, r, q, p, q + p + r


def pre_tests():
    dec = idx("2018-12")
    base = replace(CLEAN, pre_event=exact(month(dec)))
    # Both docs §1/§3: November exactly at the earliest related-event lower
    # bound passes. Both diagnostic sections use the same fixed eligible runs.
    w_expected = span("2019-01", "2019-02")
    w_base = replace(base, rules=(Rule("binding_at_march_start", exact(month(idx("2019-03")))),))
    _, w, _ = audit_window(W_CANDIDATES, {}, "W", w_base)
    for doc in ("CW", "MD"):
        check(w, w_expected, (doc, "W for placebo length"))
    r = span("2017-12", "2018-11")
    q = span("2016-10", "2017-09")
    p = span("2017-10", "2017-11")
    shared = (r, q, p, q + p + r)
    earlier_r = (span("2017-11", "2018-10"), span("2016-09", "2017-08"),
                 span("2017-09", "2017-10"), span("2016-09", "2018-10"))
    cases = (
        ("pre end exactly at event", {}, shared, shared),
        ("earlier anticipation straddles R end",
         {(dec - 1, N): replace(base, pre_event=(month(dec) - SECOND, month(dec)))},
         earlier_r, earlier_r),
        ("one-arm direct restriction in P",
         {(p[0], N): replace(base, rules=(Rule("pre_direct", exact(month(p[0]) + SECOND)),))},
         (r, (), (), ()), (r, (), (), ())),
        ("unresolved residual direct effect in Q",
         {(q[0], N): replace(base, residual="unknown")},
         (r, (), (), ()), (r, (), (), ())),
    )
    pre_labels = ((OK, OUT), (UNKNOWN, OUT), (MIXED, OUT), (UNKNOWN, OUT))
    targets = ((dec - 1, N), (dec - 1, N), (p[0], N), (q[0], N))
    for case, target, expected_labels in zip(cases, targets, pre_labels):
        name, changes, cw, md = case
        rows, *sets = pre_windows(changes, base, w)
        i, u = target
        actual_labels = rows[i][u][0][0], rows[dec][N][0][0]
        for doc, expected in (("CW", cw), ("MD", md)):
            check(tuple(sets), expected, (name, doc, "R/Q/P/V"))
            check(actual_labels, expected_labels, (name, doc, "pre labels"))


def order_test(initial, mixed):
    # Support/weights are trace-only spies: no WLS or outcome calculation.
    # A support change hypothetically drops N's node; the mask is never rerun
    # on that altered composition. A pending/empty mask never calls either.
    for cell, expect in ((CLEAN, ("mask", "support", "weights")),
                         (mixed, ("mask",)),
                         (replace(CLEAN, coverage="unknown"), ("mask",))):
        trace = []
        trace.append(("mask", FRAME))
        _, good, possible = audit_window(W_CANDIDATES, initial | {(JAN, N): cell}, "W")
        if good:
            frozen = (FRAME, good)
            trace.append(("support", frozen))
            support = (tuple(u for u in FRAME if u != N), good)
            trace.append(("weights", support))
            _, invalid_reopen, _ = audit_window(W_CANDIDATES, initial, "W", frame=support[0])
            check(invalid_reopen, span("2019-01", "2019-04"),
                  "dropping the blocked cell would illicitly reopen February-April")
            check(trace[1][1], (FRAME, (JAN,)), "support receives frozen month/frame")
            check(trace[2][1][1], (JAN,), "weights do not reopen the calendar")
        for doc in ("CW", "MD via CW linked §2 fixed order"):
            check(tuple(stage for stage, _ in trace), expect, (doc, "stage trace"))
        check(window_status(good, possible),
              "eligible_window" if cell is CLEAN else EMPTY if cell is mixed else PENDING,
              "calendar status precedes support and weighting")


def main():
    labels_tests()
    initial, mixed = intersection_tests()
    pre_tests()
    order_test(initial, mixed)
    print("PASS CW and MD common scope: 20 boundary rows; fixed W intersection; "
          "source-linked reasons; R/Q/P/V; mask -> support -> weights.")
    pool_c_test()
    print("PASS Pool C cutoff alternatives reproduced; unresolved boundary is not promoted to agreement.")


if __name__ == "__main__":
    main()
