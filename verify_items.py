"""
Ground-truth computation + self-verification for the 10-item eval work sample.
Every canonical answer below is COMPUTED here (not asserted from memory), then the
same values are what appear in the published item set. Run: python3 verify_items.py
Requires: numpy, scipy, scikit-learn, sympy, mpmath.
"""
import numpy as np
from fractions import Fraction
from itertools import combinations
import mpmath as mp

RESULTS = {}

# ----------------------------------------------------------------------
# M1 — consecutive sums of two squares (exact integer)
# ----------------------------------------------------------------------
def m1():
    N = 10**6
    spf = np.zeros(N + 2, dtype=np.int64)
    lim = int((N + 1) ** 0.5) + 1
    for i in range(2, lim + 1):
        if spf[i] == 0:
            sl = spf[i * i::i]
            sl[sl == 0] = i
    mask = spf == 0
    spf[mask] = np.arange(N + 2)[mask]
    spf[0] = 0; spf[1] = 1
    spf_l = spf.tolist()
    def is_sos(n):
        if n <= 1:
            return True
        while n > 1:
            p = spf_l[n]; e = 0
            while n % p == 0:
                n //= p; e += 1
            if p % 4 == 3 and e % 2 == 1:
                return False
        return True
    sos = bytearray(N + 2)
    for n in range(1, N + 2):
        sos[n] = 1 if is_sos(n) else 0
    cnt = sum(1 for n in range(1, N + 1) if sos[n] and sos[n + 1])
    return cnt
RESULTS["M1"] = m1()

# ----------------------------------------------------------------------
# M2 — Euler integral
# ----------------------------------------------------------------------
def m2():
    mp.mp.dps = 40
    I = mp.quad(lambda x: mp.log(1 + x) * mp.log(1 - x) / x, [0, 1])
    closed = -mp.mpf(5) / 8 * mp.zeta(3)
    return I, closed, abs(I - closed)
_i, _c, _err = m2()
RESULTS["M2"] = {"numeric_integral": mp.nstr(_i, 20),
                 "closed_-5/8*zeta3": mp.nstr(_c, 20),
                 "abs_err": mp.nstr(_err, 3)}
assert _err < mp.mpf(10) ** (-25), "M2 closed form mismatch"

# ----------------------------------------------------------------------
# M3 — connected labeled simple graphs on 7 vertices with exactly 8 edges
# ----------------------------------------------------------------------
def m3():
    verts = range(7)
    edges = list(combinations(verts, 2))
    def connected(chosen):
        adj = {v: set() for v in verts}
        for a, b in chosen:
            adj[a].add(b); adj[b].add(a)
        seen = {0}; stack = [0]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); stack.append(w)
        return len(seen) == 7
    return sum(1 for c in combinations(edges, 8) if connected(c))
RESULTS["M3"] = m3()

# ----------------------------------------------------------------------
# S1 — weak-lensing shape noise per pixel + averaging
# ----------------------------------------------------------------------
def s1():
    sigma_e, n_gal, A_pix = 0.4, 30.0, 4.0
    sigma_pix = sigma_e / np.sqrt(2 * n_gal * A_pix)
    import math
    N = math.floor((sigma_pix / 0.005) ** 2) + 1
    assert sigma_pix / np.sqrt(N) < 0.005 <= sigma_pix / np.sqrt(N - 1)
    return round(float(sigma_pix), 6), int(N)
RESULTS["S1"] = s1()

# ----------------------------------------------------------------------
# S2 — exact (Garwood) central Poisson CI for k=17 at 68.27% confidence
# ----------------------------------------------------------------------
def s2():
    from scipy.stats import chi2
    k = 17; cl = 0.6827; alpha = 1 - cl
    lo = 0.5 * chi2.ppf(alpha / 2, 2 * k)
    hi = 0.5 * chi2.ppf(1 - alpha / 2, 2 * k + 2)
    return round(float(lo), 3), round(float(hi), 3)
RESULTS["S2"] = s2()

# ----------------------------------------------------------------------
# Q1 — low-FPR partial metric on a SEEDED dataset
# ----------------------------------------------------------------------
def q1():
    from sklearn.metrics import roc_curve
    rng = np.random.default_rng(20260818)
    ind = rng.normal(0.0, 1.0, size=500)
    ood = rng.normal(0.7, 1.2, size=500)
    scores = np.concatenate([ind, ood])
    labels = np.concatenate([np.zeros(500), np.ones(500)])
    fpr, tpr, _ = roc_curve(labels, scores)
    grid = np.logspace(np.log10(0.001), np.log10(0.05), 100)
    val = float(np.mean(np.interp(grid, fpr, tpr)))
    return val
_q1 = q1()
RESULTS["Q1"] = {"value_10dp": round(_q1, 10), "canonical_6dp": round(_q1, 6)}

# ----------------------------------------------------------------------
# Q2 — P(running sum of a fair d6 ever equals exactly 100), exact fraction
# ----------------------------------------------------------------------
def q2():
    p = [Fraction(0)] * 101
    p[0] = Fraction(1)
    for n in range(1, 101):
        p[n] = sum(p[n - k] for k in range(1, 7) if n - k >= 0) / 6
    return p[100]
_q2 = q2()
RESULTS["Q2"] = {"fraction": f"{_q2.numerator}/{_q2.denominator}",
                 "decimal": round(float(_q2), 10)}

# ----------------------------------------------------------------------
# C1 — reference implementation + oracle check: k-th smallest pair distance
# ----------------------------------------------------------------------
def kth_smallest_pair_distance(nums, k):
    a = sorted(nums); n = len(a)
    def count_le(d):
        c = 0; i = 0
        for j in range(n):
            while a[j] - a[i] > d:
                i += 1
            c += j - i
        return c
    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo

def c1_oracle_test():
    rng = np.random.default_rng(7)
    for _ in range(300):
        n = int(rng.integers(2, 40))
        nums = list(map(int, rng.integers(-50, 50, size=n)))
        pd = sorted(abs(x - y) for i, x in enumerate(nums) for y in nums[i + 1:])
        k = int(rng.integers(1, len(pd) + 1))
        assert kth_smallest_pair_distance(nums, k) == pd[k - 1]
    return "oracle 300/300 OK"
RESULTS["C1"] = c1_oracle_test()

# ----------------------------------------------------------------------
# C2 — exact output of a trap snippet
# ----------------------------------------------------------------------
def c2():
    out = []
    def acc(x, _bin=[]):
        _bin.append(x); return list(_bin)
    r1 = acc(1); r2 = acc(2)
    fns = [lambda: i for i in range(3)]
    lb = [f() for f in fns]
    chain = (1 < 2 < 3, (1 < 2) < 3, 1 < (2 < 3))
    d = {}; d['a'] = 1; d['c'] = 3; d['b'] = 2
    order = list(d.keys())
    return (r1, r2, lb, chain, order)
RESULTS["C2"] = repr(c2())

# ----------------------------------------------------------------------
# A1 — planning env
# ----------------------------------------------------------------------
def a1():
    from collections import deque
    target = 2026
    start = 0
    seen = {start}
    dq = deque([(start, "")])
    while dq:
        x, path = dq.popleft()
        if x == target:
            return path, len(path)
        for op, nx in (("D", 2 * x), ("I", x + 1), ("Z", 0)):
            if 0 <= nx <= 2 * target and nx not in seen:
                seen.add(nx); dq.append((nx, path + op))
    return None
_a1_path, _a1_len = a1()
RESULTS["A1"] = {"answer": _a1_path, "length": _a1_len}

def a1_len_check():
    x, ops = 2026, 0
    while x > 0:
        if x % 2 == 0:
            x //= 2
        else:
            x -= 1
        ops += 1
    return ops
assert a1_len_check() == _a1_len, "A1 length mismatch vs reverse-greedy"

print("="*70)
for k in ["M1","M2","M3","S1","S2","Q1","Q2","C1","C2","A1"]:
    print(f"{k}: {RESULTS[k]}")
print("="*70)
print("ALL CHECKS PASSED")
