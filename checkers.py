"""
Per-item deterministic checkers for the eval work sample.
Design principle (from FrontierMath / SWE-bench / GPQA practice): the canonical
answer is checked by a DETERMINISTIC verifier — exact-match, SymPy equality,
numeric tolerance, or unit tests — never an LLM judge.

Each check_* returns True/False. `submitted` is whatever a solver would hand in
(a value, an expression string, or — for code items — a callable / string).
"""
import numpy as np
from fractions import Fraction
import sympy as sp
import mpmath as mp

# ---------- M1: exact integer ----------
def check_M1(submitted):                        # sums of two squares, consecutive
    return int(submitted) == 40799

# ---------- M2: SymPy / high-precision symbolic equality ----------
def check_M2(submitted):                        # submitted: expression string
    mp.mp.dps = 40
    target = -mp.mpf(5) / 8 * mp.zeta(3)
    # symbolic path
    try:
        expr = sp.sympify(submitted, locals={"zeta": sp.zeta, "pi": sp.pi})
        if sp.simplify(expr - (-sp.Rational(5, 8) * sp.zeta(3))) == 0:
            return True
        num = mp.mpf(str(sp.N(expr, 35)))
        return abs(num - target) < mp.mpf(10) ** (-20)
    except Exception:
        try:
            return abs(mp.mpf(str(submitted)) - target) < mp.mpf(10) ** (-9)
        except Exception:
            return False

# ---------- M3: exact integer ----------
def check_M3(submitted):
    return int(submitted) == 156555

# ---------- S1: numeric tolerance + exact integer ----------
def check_S1(sigma_pix, N):
    return abs(float(sigma_pix) - 0.025820) < 1e-5 and int(N) == 27

# ---------- S2: numeric tolerance (both bounds) ----------
def check_S2(lo, hi):
    return abs(float(lo) - 12.918) < 5e-3 and abs(float(hi) - 22.204) < 5e-3

# ---------- Q1: numeric tolerance ----------
def check_Q1(submitted):
    return abs(float(submitted) - 0.066700) < 1e-6

# ---------- Q2: exact rational (fraction) OR tight decimal ----------
_Q2_NUM = 186662463857159746887081233650939816277072280598086888295658941442344128837463
_Q2_DEN = 653318623500070906096690267158057820537143710472954871543071966369497141477376
def check_Q2(submitted):
    exact = Fraction(_Q2_NUM, _Q2_DEN)
    s = str(submitted).strip()
    try:
        if "/" in s:
            return Fraction(s) == exact
        return abs(float(s) - float(exact)) < 1e-12
    except Exception:
        return False

# ---------- C1: unit tests against a brute oracle (FAIL_TO_PASS + PASS_TO_PASS) ----------
def check_C1(fn):                               # fn: candidate callable(nums,k)->int
    def oracle(nums, k):
        pd = sorted(abs(x - y) for i, x in enumerate(nums) for y in nums[i + 1:])
        return pd[k - 1]
    # fixed edge cases
    fixed = [([1, 1], 1, 0), ([1, 3, 1], 1, 0), ([1, 3, 1], 3, 2),
             ([-5, 5], 1, 10), ([0, 0, 0], 3, 0), ([10, 1, 4, 7], 6, 9)]
    for nums, k, want in fixed:
        if fn(list(nums), k) != want:
            return False
    # randomized differential test
    rng = np.random.default_rng(123)
    for _ in range(200):
        n = int(rng.integers(2, 30))
        nums = list(map(int, rng.integers(-40, 40, size=n)))
        m = n * (n - 1) // 2
        k = int(rng.integers(1, m + 1))
        if fn(list(nums), k) != oracle(nums, k):
            return False
    return True

# ---------- C2: exact-match of the produced object ----------
_C2_CANON = ([1], [1, 2], [2, 2, 2], (True, True, False), ['a', 'c', 'b'])
def check_C2(submitted):
    return submitted == _C2_CANON

# ---------- A1: run the action string through the deterministic simulator ----------
def _a1_optimum():
    from collections import deque
    target, seen, dq = 2026, {0}, __import__("collections").deque([(0, "")])
    while dq:
        x, p = dq.popleft()
        if x == target:
            return p
        for op, nx in (("D", 2 * x), ("I", x + 1), ("Z", 0)):
            if 0 <= nx <= 2 * target and nx not in seen:
                seen.add(nx); dq.append((nx, p + op))
def _a1_run(path):
    x = 0
    for ch in path:
        x = {"D": 2 * x, "I": x + 1, "Z": 0}[ch]
    return x
_A1_OPT = _a1_optimum()
def check_A1(path, require_canonical=True):
    if _a1_run(path) != 2026:
        return False
    if len(path) != len(_A1_OPT):                # must be optimal length
        return False
    return (path == _A1_OPT) if require_canonical else True


if __name__ == "__main__":
    # accept the canonical answers
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
    # reject deliberately wrong answers
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
