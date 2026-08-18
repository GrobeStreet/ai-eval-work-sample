"""
Per-item deterministic checkers for the eval work sample.

These checkers are designed as total functions on malformed submissions: invalid inputs
return False rather than raising. Exact-integer items reject non-integral numeric values,
and the symbolic checker whitelists its expression vocabulary before parsing.
"""
import re
import numpy as np
from fractions import Fraction
import sympy as sp
import mpmath as mp


def _coerce_exact_int(value):
    """Return an integer only when the submitted value is exactly integral."""
    if isinstance(value, (bool, np.bool_)):
        raise ValueError("booleans are not integer answers")
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        x = float(value)
        if np.isfinite(x) and x.is_integer():
            return int(x)
        raise ValueError("non-integral numeric answer")
    s = str(value).strip()
    if re.fullmatch(r"[+-]?\d+", s):
        return int(s)
    raise ValueError("not an exact integer")


def _finite_float(value):
    x = float(value)
    if not np.isfinite(x):
        raise ValueError("non-finite numeric answer")
    return x


# ---------- M1: exact integer ----------
def check_M1(submitted):
    try:
        return _coerce_exact_int(submitted) == 40799
    except Exception:
        return False


# ---------- M2: symbolic equality / high-precision numeric ----------
def check_M2(submitted):
    mp.mp.dps = 40
    target = -mp.mpf(5) / 8 * mp.zeta(3)
    s = str(submitted).strip()
    try:
        # Keep the symbolic parser's vocabulary deliberately tiny for untrusted input.
        if not re.fullmatch(r"[0-9A-Za-z+\-*/().\s]+", s):
            raise ValueError("disallowed token")
        words = set(re.findall(r"[A-Za-z]+", s))
        if not words.issubset({"zeta", "pi"}):
            raise ValueError("disallowed symbol")
        expr = sp.sympify(s, locals={"zeta": sp.zeta, "pi": sp.pi})
        if sp.simplify(expr - (-sp.Rational(5, 8) * sp.zeta(3))) == 0:
            return True
        num = mp.mpf(str(sp.N(expr, 35)))
        return abs(num - target) < mp.mpf(10) ** (-20)
    except Exception:
        try:
            return abs(mp.mpf(s) - target) < mp.mpf(10) ** (-9)
        except Exception:
            return False


# ---------- M3: exact integer ----------
def check_M3(submitted):
    try:
        return _coerce_exact_int(submitted) == 156555
    except Exception:
        return False


# ---------- S1: numeric tolerance + exact integer ----------
def check_S1(sigma_pix, N):
    try:
        return abs(_finite_float(sigma_pix) - 0.025820) < 1e-5 and _coerce_exact_int(N) == 27
    except Exception:
        return False


# ---------- S2: numeric tolerance (both bounds) ----------
def check_S2(lo, hi):
    try:
        return abs(_finite_float(lo) - 12.918) < 5e-3 and abs(_finite_float(hi) - 22.204) < 5e-3
    except Exception:
        return False


# ---------- Q1: numeric tolerance ----------
def check_Q1(submitted):
    try:
        return abs(_finite_float(submitted) - 0.066700) < 1e-6
    except Exception:
        return False


# ---------- Q2: exact rational OR tight decimal ----------
_Q2_NUM = 186662463857159746887081233650939816277072280598086888295658941442344128837463
_Q2_DEN = 653318623500070906096690267158057820537143710472954871543071966369497141477376

def check_Q2(submitted):
    exact = Fraction(_Q2_NUM, _Q2_DEN)
    s = str(submitted).strip()
    try:
        if "/" in s:
            return Fraction(s) == exact
        x = _finite_float(s)
        return abs(x - float(exact)) < 1e-12
    except Exception:
        return False


# ---------- C1: unit tests against a brute oracle ----------
def check_C1(fn):
    def oracle(nums, k):
        pd = sorted(abs(x - y) for i, x in enumerate(nums) for y in nums[i + 1:])
        return pd[k - 1]
    fixed = [([1, 1], 1, 0), ([1, 3, 1], 1, 0), ([1, 3, 1], 3, 2),
             ([-5, 5], 1, 10), ([0, 0, 0], 3, 0), ([10, 1, 4, 7], 6, 9)]
    try:
        for nums, k, want in fixed:
            if fn(list(nums), k) != want:
                return False
        rng = np.random.default_rng(123)
        for _ in range(200):
            n = int(rng.integers(2, 30))
            nums = list(map(int, rng.integers(-40, 40, size=n)))
            m = n * (n - 1) // 2
            k = int(rng.integers(1, m + 1))
            if fn(list(nums), k) != oracle(nums, k):
                return False
        return True
    except Exception:
        return False


# ---------- C2: exact structural match ----------
_C2_CANON = ([1], [1, 2], [2, 2, 2], (True, True, False), ['a', 'c', 'b'])
def check_C2(submitted):
    return submitted == _C2_CANON


# ---------- A1: simulator + BFS optimum ----------
def _a1_optimum():
    from collections import deque
    target, seen, dq = 2026, {0}, deque([(0, "")])
    while dq:
        x, p = dq.popleft()
        if x == target:
            return p
        for op, nx in (("D", 2 * x), ("I", x + 1), ("Z", 0)):
            if 0 <= nx <= 2 * target and nx not in seen:
                seen.add(nx); dq.append((nx, p + op))


def _a1_run(path):
    if not isinstance(path, str):
        return None
    x = 0
    for ch in path:
        if ch == "D":
            x = 2 * x
        elif ch == "I":
            x += 1
        elif ch == "Z":
            x = 0
        else:
            return None
    return x

_A1_OPT = _a1_optimum()
def check_A1(path, require_canonical=True):
    try:
        if _a1_run(path) != 2026:
            return False
        if len(path) != len(_A1_OPT):
            return False
        return (path == _A1_OPT) if require_canonical else True
    except Exception:
        return False


if __name__ == "__main__":
    def c1_ref(nums, k):
        a = sorted(nums); n = len(a)
        def cnt(d):
            c = i = 0
            for j in range(n):
                while a[j] - a[i] > d:
                    i += 1
                c += j - i
            return c
        lo, hi = 0, a[-1] - a[0]
        while lo < hi:
            m = (lo + hi) // 2
            if cnt(m) >= k: hi = m
            else: lo = m + 1
        return lo
    passes = {
        "M1": check_M1(40799),
        "M2": check_M2("-5*zeta(3)/8"),
        "M3": check_M3(156555),
        "S1": check_S1(0.025820, 27),
        "S2": check_S2(12.918, 22.204),
        "Q1": check_Q1(0.066700),
        "Q2": check_Q2(f"{_Q2_NUM}/{_Q2_DEN}"),
        "C1": check_C1(c1_ref),
        "C2": check_C2(([1], [1, 2], [2, 2, 2], (True, True, False), ['a', 'c', 'b'])),
        "A1": check_A1("IDIDIDIDIDIDDIDDID"),
    }
    rejects = {
        "M1_wrong": check_M1(40800),
        "M2_wrong": check_M2("-zeta(3)"),
        "Q1_wrong": check_Q1(0.0670),
        "Q2_wrong2/7": check_Q2("2/7"),
        "C1_wrong": check_C1(lambda nums, k: 0),
        "C2_wrong": check_C2(([1], [1, 2], [2, 2, 2], (True, True, True), ['a', 'c', 'b'])),
        "A1_wrong": check_A1("IIII"),
    }
    print("ACCEPT canonical:", passes)
    print("all accept:", all(passes.values()))
    print("REJECT wrong:  ", rejects)
    print("all reject:", not any(rejects.values()))
    print("A1 canonical optimum =", _A1_OPT)
