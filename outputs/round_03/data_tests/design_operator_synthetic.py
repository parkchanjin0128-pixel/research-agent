"""Exact arithmetic checks for the balanced, separable-weight reduced WLS."""
from fractions import Fraction as F


def mean(values):
    return sum(values, F(0)) / len(values)


def slope(x, y):
    cx, cy = mean(x), mean(y)
    den = sum((v - cx) ** 2 for v in x)
    if den == 0:
        raise ValueError("dose rank failure within arm")
    return sum((a - cx) * (b - cy) for a, b in zip(x, y, strict=True)) / den


def demand_support(a, b):
    for x in (a, b):
        slope(x, [F(0)] * len(x))
    if min(max(a), max(b)) - max(min(a), min(b)) < F(1, 10):
        raise ValueError("no common 10pp span")


def contrast(a, b, y1, y0):
    demand_support(a, b)
    return slope(a, y1) - slope(b, y0)


def fit_path(by_month, base, ref, window):
    omitted = by_month[base]
    raw = [y - omitted for y in by_month]
    center = mean([raw[i] for i in ref])
    return mean([raw[i] - center for i in window])


def expect_failure(call, expected):
    try:
        call()
    except ValueError as exc:
        assert expected in str(exc), exc
    else:
        raise AssertionError("expected failure did not occur")


if __name__ == "__main__":
    dose = list(map(F, ["0", ".2", ".8", "1"]))
    b1 = contrast(dose, dose, [F(0), F(0), F(1), F(1)], [F(0)] * 4)
    assert b1 == F(20, 17), b1
    a = [F(i, 100) for i in [2, 2, 5, 8, 12, 12, 15, 18]]
    b = [F(i, 100) for i in [2, 5, 8, 8, 12, 15, 18, 18]]
    b2 = contrast(a, b, [i**2 for i in a], [i**2 for i in b])
    assert abs(float(b2) - (-0.025130)) < 1e-6, b2
    target = F(3, 4)
    y1, y0 = [2 + 10 * target * i for i in dose], [F(2)] * 4
    assert contrast(dose, dose, y1, y0) == 10 * target
    x = [10 * i for i in dose]
    assert slope(x, y1) - slope(x, y0) == target
    path = [F(1), F(3), F(9, 4), F(13, 4)]
    assert fit_path(path, 0, [0, 1], [2, 3]) == target
    assert fit_path(path, 1, [0, 1], [2, 3]) == target
    expect_failure(lambda: demand_support([F(0), F(0)], dose), "rank failure")
    expect_failure(lambda: demand_support([F(0), F(1, 20)], dose), "10pp span")
    print(f"Counterexamples: {float(b1):.6f}, {float(b2):.6f} per unit; "
          "positive injection, two references, 10pp scaling, and two failures passed.")
