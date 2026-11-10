"""Outcome-free exact arithmetic checks for the placebo crosswalk. Python 3."""
from collections import Counter
from fractions import Fraction as F


def slope(xs, ps, ys):
    mean = sum(p * x for p, x in zip(ps, xs))
    var = sum(p * (x - mean) ** 2 for p, x in zip(ps, xs))
    if not var:
        raise ValueError("rank")
    return sum(p * (x - mean) * y for p, x, y in zip(ps, xs, ys)) / var


def common_law(a, b, *, audit_complete=True):
    cells = {}
    for h in sorted({h for h, _ in a} & {h for h, _ in b}):
        xs = {x for hh, x in a if hh == h and (h, x) in b}
        if any(x + 1 in xs for x in xs):
            cells.update({(h, x): (a[h, x], b[h, x]) for x in sorted(xs)})
    if not cells:
        return ("no_support" if audit_complete else "input_pending"), {}
    n1, n0 = map(sum, zip(*cells.values()))
    raw = {k: min(F(i, n1), F(j, n0)) for k, (i, j) in cells.items()}
    total = sum(raw.values())
    return "supported", {k: v / total for k, v in raw.items()}


def contrast(law, listed, nonlisted):
    if not law:
        raise ValueError("unsupported contrast")
    result = F(0)
    for h in sorted({h for h, _ in law}):
        xs = [x for hh, x in law if hh == h]
        mass = sum(law[h, x] for x in xs)
        ps = [law[h, x] / mass for x in xs]
        result += mass * slope(xs, ps, [listed(h, x) - nonlisted(h, x) for x in xs])
    return result


def classify_exposure(records, complete):
    if any(r in {"direct", "adjacent"} for r in records):
        return "confirmed_contamination"
    if not complete or not records or any(r != "no_path" for r in records):
        return "indeterminate"
    return "low_exposure_candidate"


def main():
    xs = [F(i, 10) for i in (1, 3, 5, 7, 11, 13, 15, 17)]
    a = Counter(dict(zip((("h", x) for x in xs), (5, 1, 7, 3) * 2)))
    b = Counter(dict(zip((("h", x) for x in xs), (3, 7, 1, 5) * 2)))
    old = [
        slope(xs, [F(arm["h", x], sum(arm.values())) for x in xs], [x*x for x in xs])
        for arm in (a, b)
    ]
    assert old == [F(179, 100), F(181, 100)]
    _, law = common_law(a, b)

    def catchup(h, x):
        return x*x

    assert contrast(law, catchup, catchup) == 0
    inc = F(3, 7)
    assert contrast(law, lambda h, x: catchup(h, x) + inc*x, catchup) == inc
    shifted = Counter({(h, x + F(1, 100)): n for (h, x), n in b.items()})
    assert common_law(a, shifted) == ("no_support", {})
    assert common_law(a, shifted, audit_complete=False) == ("input_pending", {})
    point = Counter({("h", xs[0]): 1})
    assert common_law(point, point) == ("no_support", {})
    try:
        slope([xs[0]], [F(1)], [F(0)])
    except ValueError as exc:
        assert str(exc) == "rank"
    else:
        raise AssertionError("rank failure not detected")
    # Synthetic country-arm slopes: CN listed +3, CN nonlisted +1;
    # each comparator listed +2 and nonlisted +1, so all leave-outs agree.
    controls = [F(1)] * 4
    results = []
    for i in range(len(controls)):
        kept = controls[:i] + controls[i+1:]
        avg = sum(kept) / len(kept)
        results.append(contrast(law, lambda h, x: catchup(h, x)+(3-1-avg)*x, catchup))
    assert results == [F(1)] * 4
    assert all(c - controls[0] == 0 for c in controls[1:])
    assert results[0] + F(1) + controls[0] == 3
    assert classify_exposure(["no_path", "unknown"], False) == "indeterminate"
    assert classify_exposure(["adjacent", "unknown"], False) == "confirmed_contamination"
    assert classify_exposure(["no_path"], True) == "low_exposure_candidate"
    print("PASS: nonlinear shared curve, one-arm increment, support/rank, shared spillover/unknown")


if __name__ == "__main__":
    main()
