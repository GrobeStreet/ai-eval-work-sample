import json
from checkers import _Q2_NUM, _Q2_DEN     # verified constants

items = [
 {"id":"M1","domain":"number theory","difficulty":{"background":3,"creativity_hrs":0.5,"execution_hrs":0.5},
  "answer_type":"exact_integer","verifier":"exact_match",
  "prompt":"A positive integer is representable if it equals a^2+b^2 for integers a,b>=0 (so 0 and perfect squares count). How many integers n with 1<=n<=10^6 have both n and n+1 representable?",
  "canonical_answer":"40799"},
 {"id":"M2","domain":"real analysis","difficulty":{"background":4,"creativity_hrs":1.5,"execution_hrs":0.5},
  "answer_type":"closed_form","verifier":"sympy_equality_or_highprec_numeric",
  "prompt":"Evaluate in closed form: I = integral_0^1 ln(1+x)*ln(1-x)/x dx.",
  "canonical_answer":"-5*zeta(3)/8"},
 {"id":"M3","domain":"combinatorics","difficulty":{"background":3,"creativity_hrs":0.5,"execution_hrs":0.5},
  "answer_type":"exact_integer","verifier":"exact_match",
  "prompt":"How many connected, labeled, simple graphs on 7 vertices have exactly 8 edges?",
  "canonical_answer":"156555"},
 {"id":"S1","domain":"cosmology/observational statistics","difficulty":{"background":3,"creativity_hrs":0.3,"execution_hrs":0.2},
  "answer_type":"numeric_plus_integer","verifier":"numeric_tol_1e-5_and_exact_int",
  "prompt":"Convergence maps on 2-arcmin square pixels. Per-pixel shape noise sigma_pix = sigma_e/sqrt(2*n_gal*A_pix), sigma_e=0.4, n_gal=30 per arcmin^2, A_pix in arcmin^2. (a) sigma_pix to 4 sig figs. (b) smallest integer N so averaging N independent pixels gives noise-on-mean < 0.005.",
  "canonical_answer":"sigma_pix=0.02582; N=27"},
 {"id":"S2","domain":"statistics","difficulty":{"background":3,"creativity_hrs":0.3,"execution_hrs":0.2},
  "answer_type":"numeric_interval","verifier":"numeric_tol_5e-3_both_bounds",
  "prompt":"Observe k=17 Poisson counts in a fixed exposure. Give the exact (Garwood) central 68.27% confidence interval for the mean lambda, [lo,hi], each to 3 decimals.",
  "canonical_answer":"[12.918, 22.204]"},
 {"id":"Q1","domain":"ML evaluation methodology","difficulty":{"background":3,"creativity_hrs":0.5,"execution_hrs":0.5},
  "answer_type":"numeric","verifier":"numeric_tol_1e-6",
  "prompt":"Score = mean TPR over 100 log-spaced FPR points in [0.001,0.05] from sklearn roc_curve via numpy.interp. Data: rng=numpy.random.default_rng(20260818); InD=rng.normal(0,1,500); OOD=rng.normal(0.7,1.2,500); OOD is positive class. Report score to 6 dp.",
  "canonical_answer":"0.066700"},
 {"id":"Q2","domain":"probability","difficulty":{"background":3,"creativity_hrs":1.0,"execution_hrs":0.3},
  "answer_type":"exact_rational","verifier":"exact_fraction_or_decimal_1e-12",
  "prompt":"Fair d6 rolled repeatedly, running total starts at 0. Exact probability the total ever equals exactly 100? Reduced fraction (decimal to 12 places also accepted). Note: it is NOT 2/7.",
  "canonical_answer":f"{_Q2_NUM}/{_Q2_DEN}"},
 {"id":"C1","domain":"algorithms/code","difficulty":{"background":2,"creativity_hrs":0.5,"execution_hrs":1.0},
  "answer_type":"function","verifier":"unit_tests_vs_oracle",
  "prompt":"Implement kth_smallest_pair_distance(nums,k): k-th smallest |nums[i]-nums[j]| over pairs i<j (1-indexed). Target O(n log n + n log(range)). Correct with duplicates, negatives, boundary k.",
  "canonical_answer":"reference: binary-search-on-distance + two-pointer count (see checkers.py)"},
 {"id":"C2","domain":"code/language semantics","difficulty":{"background":2,"creativity_hrs":0.3,"execution_hrs":0.2},
  "answer_type":"exact_output","verifier":"exact_match",
  "prompt":"Under CPython 3.11+, exact return value of c2() (mutable default arg; late-binding closures; comparison chaining vs grouping; dict insertion order). See work-sample doc for the code.",
  "canonical_answer":"([1], [1, 2], [2, 2, 2], (True, True, False), ['a', 'c', 'b'])"},
 {"id":"A1","domain":"planning/agentic reasoning","difficulty":{"background":2,"creativity_hrs":0.5,"execution_hrs":0.5},
  "answer_type":"exact_string","verifier":"simulator_plus_bfs_optimum",
  "prompt":"Token at 0. Actions D(x->2x), I(x->x+1), Z(x->0). Reach exactly 2026 in fewest actions; among shortest, return lexicographically smallest (D<I<Z).",
  "canonical_answer":"IDIDIDIDIDIDDIDDID"},
]

with open("items.json","w") as f:
    json.dump({"title":"Verifiable eval work sample (10 items)","author":"Robert 'Bobby' Morong (GrobeStreet)",
               "date":"2026-08-18","n_items":len(items),
               "verifier_note":"All checks deterministic (exact-match / SymPy / numeric-tol / unit-tests). Never an LLM judge.",
               "items":items}, f, indent=2)
print("wrote items.json with", len(items), "items")
print("Q2 answer length (chars):", len(items[6]["canonical_answer"]))
