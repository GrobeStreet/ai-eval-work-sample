# A Verifiable Eval Work Sample — 10 hard, machine-checkable items

**Author:** Robert "Bobby" Morong (GrobeStreet) · **Date:** 2026-08-18
**Positioning:** Independent AI-evaluation & research-verification specialist. This is a work sample: ten original benchmark items across math, science, code, and reasoning, each with a **deterministic checker** and a **shipped script that recomputes every answer from scratch**. Nothing here is asserted from memory — `verify_items.py` derives all ten ground-truth answers, and `checkers.py` demonstrates that each item's verifier accepts the canonical answer and rejects near-miss wrong ones.

The point of the sample is not just "here are hard questions." It is to show the discipline eval buyers actually pay for: *answers you can trust because a machine, not a human vibe, certifies them* — and a reproducibility trail behind every number.

---

## How the set was authored (the standard I held)

Grounded in current practice at FrontierMath (Epoch AI), GPQA, SWE-bench Verified, and Humanity's Last Exam:

- **Every item is verified by a deterministic checker**, never an LLM judge. The four archetypes are all represented: exact-match (integers / traced output), symbolic equality (SymPy / high-precision), numeric tolerance, and unit tests (`FAIL_TO_PASS` + `PASS_TO_PASS`).
- **Guess-resistance.** Answers are high-entropy (large integers, exact fractions, 6-dp reals, or precise strings), so blind guessing is far below 1%. Where an "obvious" wrong answer exists, it is a *deliberate distractor* the checker rejects (e.g. Q2's 2/7).
- **Leakage-resistance.** Items are constructed, not copied; the science/quant items are anchored in parameter values a solver must combine correctly rather than look up. Reproducible-by-seed items (Q1) can't be memorized.
- **Saturation-resistance.** The hardest items (M2, Q2) require a genuine derivation, not retrieval.
- **Every answer field ships with:** a worked solution, a "why it's hard / typical failure mode" note, and guard notes.

**Difficulty is rated on three axes** (FrontierMath convention): *Background* (1–5, domain knowledge needed), *Creativity* (expert-hours to find the idea), *Execution* (expert-hours to carry it out). This set spans GPQA-hard to FrontierMath-adjacent; M2 and Q2 are the deepest. A production FrontierMath submission would push several items to Tier 3–4 and re-perturb any item with a published cousin (flagged per-item below).

**Reproduce everything:** `python3 verify_items.py` (derives all answers, self-asserts) and `python3 checkers.py` (accept-canonical / reject-wrong demonstration). Requires `numpy, scipy, scikit-learn, sympy, mpmath`.

---

## The items

### M1 — Consecutive sums of two squares
- **Domain:** number theory · **Difficulty:** Bg 3 · Creativity 0.5h · Execution 0.5h · **Answer type:** exact integer
- **Prompt:** A positive integer is *representable* if it equals a² + b² for some integers a, b ≥ 0 (so 0 and perfect squares count). How many integers n with 1 ≤ n ≤ 10⁶ are such that **both** n and n + 1 are representable?
- **Canonical answer:** `40799`
- **Verifier:** exact integer match (`check_M1`).
- **Worked solution:** By the sum-of-two-squares theorem, n is representable iff every prime p ≡ 3 (mod 4) occurs to an **even** power in n. Sieve a smallest-prime-factor table to 10⁶ + 1, mark each n representable via that parity test, then count indices where the flag holds for n and n + 1. Result 40799.
- **Why it's hard / typical failure:** The theorem must be recalled *exactly* (the even-exponent condition, and that "≥ 0" includes 0 and the squares). Coupling n with n + 1 kills any single-residue shortcut. Common failures: using a bogus "n ≢ 3 (mod 4)" rule; excluding perfect squares; off-by-one at the boundary.
- **Guard:** 5-digit integer → guessing ≈ 0; fully reproducible sieve.

### M2 — An Euler log-integral
- **Domain:** real analysis · **Difficulty:** Bg 4 · Creativity 1.5h · Execution 0.5h · **Answer type:** exact closed form (SymPy / high-precision)
- **Prompt:** Evaluate in closed form: I = ∫₀¹ [ln(1 + x) · ln(1 − x)] / x dx.
- **Canonical answer:** `-5*zeta(3)/8`  (≈ −0.7512855645)
- **Verifier:** SymPy symbolic equality, with a 25-digit `mpmath.quad` fallback (`check_M2`).
- **Worked solution:** Use ln(1+x)ln(1−x) = ¼[ln²(1−x²) − ln²((1+x)/(1−x))] and expand against 1/x, or expand ln(1±x) as power series and integrate term-by-term into Euler sums; both routes collapse to −5ζ(3)/8. Numerically confirmed to 25 digits: I = −0.7512855644747464…
- **Why it's hard / typical failure:** A nontrivial Euler integral; the sign and the 5/8 coefficient are the whole game. Models frequently emit −ζ(3), −ζ(3)/4, or a π²-flavored wrong form.
- **Guard:** verifiable to arbitrary precision, so numeric guessing fails. *Novelty note:* this is a known Euler integral; for a novelty-required venue, perturb (e.g. insert a weight xᵏ) to an unpublished combination.

### M3 — Connected labeled graphs, fixed edge count
- **Domain:** combinatorics · **Difficulty:** Bg 3 · Creativity 0.5h · Execution 0.5h · **Answer type:** exact integer
- **Prompt:** How many **connected**, labeled, simple graphs on 7 vertices have exactly 8 edges?
- **Canonical answer:** `156555`
- **Verifier:** exact integer match (`check_M3`).
- **Worked solution:** Two independent routes agree. (a) Direct: over all C(21, 8) = 203 490 edge subsets, count those whose graph is connected (DFS) → 156 555. (b) Complementary recurrence: total minus disconnected, where disconnected 8-edge graphs are counted by the component containing vertex 1 via the standard connected-graph convolution. Both give 156 555.
- **Why it's hard / typical failure:** Exact count, no closed form to recall; the complementary count requires correctly summing over the size of vertex 1's component and the edge split. Failures: double-counting components; forgetting graphs with an isolated vertex are possible at 8 edges on 7 nodes.
- **Guard:** 6-digit integer; two-method cross-check.

### S1 — Weak-lensing shape noise
- **Domain:** cosmology / observational statistics · **Difficulty:** Bg 3 · Creativity 0.3h · Execution 0.2h · **Answer type:** numeric (tol) + exact integer
- **Prompt:** A weak-lensing survey builds convergence (κ) maps on square pixels of side 2 arcmin. Per-pixel shape noise is σ_pix = σ_e / √(2 · n_gal · A_pix), with intrinsic ellipticity dispersion σ_e = 0.4, source density n_gal = 30 galaxies·arcmin⁻², and A_pix the pixel area in arcmin². (a) Give σ_pix to 4 significant figures. (b) If you average N independent such pixels, what is the smallest integer N for which the shape-noise standard deviation on the mean drops below 0.005?
- **Canonical answer:** σ_pix ≈ `0.02582`; N = `27`
- **Verifier:** numeric tolerance on σ_pix (1e-5) + exact integer on N (`check_S1`).
- **Worked solution:** A_pix = (2 arcmin)² = 4 arcmin². σ_pix = 0.4/√(2·30·4) = 0.4/√240 = 0.025820. Averaging N pixels scales noise by 1/√N; require 0.025820/√N < 0.005 ⇒ N > (0.025820/0.005)² = 26.66 ⇒ N = 27.
- **Why it's hard / typical failure:** Correct noise formula *and* unit bookkeeping (area in arcmin², the factor of 2), then a strict-inequality ceiling. Failures: dropping the 2; forgetting A_pix is an area; taking floor instead of "first N below threshold" (off-by-one to 26).
- **Guard:** two coupled sub-answers; the integer is exact. (This σ matches the noise level used in a live NeurIPS 2026 weak-lensing challenge, so it is domain-authentic.)

### S2 — Exact Poisson confidence interval
- **Domain:** statistics / measurement · **Difficulty:** Bg 3 · Creativity 0.3h · Execution 0.2h · **Answer type:** numeric (tol)
- **Prompt:** You observe k = 17 counts from a Poisson process in a fixed exposure. Give the **exact (Garwood) central** confidence interval for the mean λ at 68.27% confidence, [λ_lo, λ_hi], each to 3 decimals.
- **Canonical answer:** `[12.918, 22.204]`
- **Verifier:** numeric tolerance on both bounds (5e-3) (`check_S2`).
- **Worked solution:** The exact central interval uses chi-square quantiles: λ_lo = ½·χ²_{α/2}(2k), λ_hi = ½·χ²_{1−α/2}(2k + 2), with α = 1 − 0.6827. For k = 17: λ_lo = 12.918, λ_hi = 22.204 (note the interval is right-skewed and does **not** equal 17 ± √17).
- **Why it's hard / typical failure:** The 2k vs **2k + 2** degrees-of-freedom asymmetry is the classic trap; a √k Wald interval [12.88, 21.12] is wrong and symmetric. Failures: omitting the +2; using a normal approximation.
- **Guard:** two-bound numeric target; the skew makes the naive answer fail the tolerance.

### Q1 — The low-FPR partial-AUC metric (reproduced exactly)
- **Domain:** ML evaluation methodology · **Difficulty:** Bg 3 · Creativity 0.5h · Execution 0.5h · **Answer type:** numeric (tol)
- **Prompt:** Define the score = **mean TPR over 100 log-spaced FPR points in [0.001, 0.05]**, computed from `sklearn.metrics.roc_curve` outputs via `numpy.interp(grid, fpr, tpr)`. Build the data with NumPy's PCG64 generator: `rng = numpy.random.default_rng(20260818)`, in-distribution scores `rng.normal(0, 1, 500)`, out-of-distribution scores `rng.normal(0.7, 1.2, 500)`; label OOD as the positive class (1). Report the score to 6 decimal places.
- **Canonical answer:** `0.066700`
- **Verifier:** numeric tolerance 1e-6 (`check_Q1`).
- **Worked solution:** Concatenate scores/labels, `fpr,tpr,_ = roc_curve(labels, scores)`, grid `= np.logspace(log10(0.001), log10(0.05), 100)`, score `= mean(np.interp(grid, fpr, tpr))` = 0.066700. Because there are 500 positives, TPR is quantized to multiples of 1/500, and the 100-point mean lands cleanly on 0.0667.
- **Why it's hard / typical failure:** You must reproduce the *exact* metric mechanics — a **log**-spaced (not linear) grid, `roc_curve`'s threshold set, and `np.interp`'s endpoint semantics — and the RNG stream. Failures: linear grid; wrong positive class; calling `roc_auc_score` (full AUC ≈ 0.6, not the low-FPR partial); using the legacy `RandomState`.
- **Guard:** fully reproducible by seed (PCG64 is version-stable); no way to guess to 1e-6. *This is the exact metric family used in the FAIR Universe / NeurIPS 2026 weak-lensing challenge — an item drawn from lived methodology.*

### Q2 — Will a die's running sum hit exactly 100?
- **Domain:** probability · **Difficulty:** Bg 3 · Creativity 1.0h · Execution 0.3h · **Answer type:** exact rational
- **Prompt:** Roll a fair six-sided die repeatedly, keeping a running total that starts at 0. What is the **exact** probability that the running total is **ever equal to exactly 100**? Give a reduced fraction (a decimal to 12 places is also accepted).
- **Canonical answer:** ≈ `0.285714285702` — the exact reduced fraction is
  ```
  186662463857159746887081233650939816277072280598086888295658941442344128837463
  / 653318623500070906096690267158057820537143710472954871543071966369497141477376
  ```
- **Verifier:** exact `Fraction` equality, or decimal within 1e-12 (`check_Q2`).
- **Worked solution:** Let pₙ = P(the total ever equals n). Then p₀ = 1 and pₙ = (1/6)·Σ_{k=1..6} p_{n−k} (with p_j = 0 for j < 0). Iterate to n = 100. The value is ≈ 0.2857142857 — tantalizingly close to 2/7, which is the **limiting** hitting probability as n → ∞ (the stationary renewal density 1/E[step] = 1/3.5 = 2/7), but the finite-n answer is the exact fraction above and is **not** 2/7.
- **Why it's hard / typical failure:** Set up the renewal recurrence and resist the 2/7 trap (asymptotic ≠ exact). Failures: answering 2/7; mishandling the negative-index boundary; averaging instead of convolving.
- **Guard:** exact rational; the checker explicitly rejects 2/7.

### C1 — k-th smallest pairwise distance
- **Domain:** algorithms / code · **Difficulty:** Bg 2 · Creativity 0.5h · Execution 1.0h · **Answer type:** function, unit-tested
- **Prompt:** Implement `kth_smallest_pair_distance(nums, k)` returning the k-th smallest value of |nums[i] − nums[j]| over all pairs i < j (1-indexed k). Target O(n log n + n log(range)). Must be correct with duplicates, negatives, and boundary k.
- **Canonical answer:** reference implementation (binary-search on the distance + two-pointer pair-count); included in `checkers.py`.
- **Verifier:** differential unit tests vs an O(n²) oracle — fixed edge cases (`[1,1] k=1 → 0`, `[10,1,4,7] k=6 → 9`, all-equal arrays, negatives) plus 200 seeded random cases; the intended solution and any correct brute both pass, wrong ones fail (`check_C1`).
- **Worked solution:** Sort; binary-search d in [0, max−min]; for each d, count pairs with difference ≤ d in O(n) via a sliding left pointer; the smallest d with count ≥ k is the answer.
- **Why it's hard / typical failure:** The pair-count-with-two-pointers and binary-search-on-answer are error-prone; duplicates create zero distances that off-by-one counts drop. Failures: counting ≤ vs <; wrong search bounds; O(n²) that times out on the intended scale.
- **Guard:** unit tests (`FAIL_TO_PASS` on the edge battery, `PASS_TO_PASS` on randoms); no free-text to game.

### C2 — Exact output under CPython semantics
- **Domain:** code / language semantics · **Difficulty:** Bg 2 · Creativity 0.3h · Execution 0.2h · **Answer type:** exact-match (traced output)
- **Prompt:** Under CPython 3.11+, give the exact value returned by `c2()` below (do not run it):
  ```python
  def c2():
      def acc(x, _bin=[]):          # note the default argument
          _bin.append(x); return list(_bin)
      r1 = acc(1); r2 = acc(2)
      fns = [lambda: i for i in range(3)]
      lb = [f() for f in fns]
      chain = (1 < 2 < 3, (1 < 2) < 3, 1 < (2 < 3))
      d = {}; d['a'] = 1; d['c'] = 3; d['b'] = 2
      return (r1, r2, lb, chain, list(d.keys()))
  ```
- **Canonical answer:** `([1], [1, 2], [2, 2, 2], (True, True, False), ['a', 'c', 'b'])`
- **Verifier:** exact structural match (`check_C2`).
- **Worked solution:** The mutable default `_bin` persists across calls → r1 = [1], r2 = [1, 2]. Late-binding closures all read the final i = 2 → [2, 2, 2]. Comparison chaining: `1 < 2 < 3` is True; `(1 < 2) < 3` = `True < 3` = `1 < 3` = True; `1 < (2 < 3)` = `1 < True` = `1 < 1` = False. Dict preserves insertion order → ['a', 'c', 'b'].
- **Why it's hard / typical failure:** Four independent semantics traps compounded. Failures: fresh lists ([1], [2]); [0, 1, 2] (no late binding); (True, True, True) for the chain. Every element is guaranteed by the language spec (no implementation-defined behavior).
- **Guard:** exact-match; deterministic under the pinned interpreter.

### A1 — Optimal reach with a deterministic planner
- **Domain:** planning / agentic reasoning · **Difficulty:** Bg 2 · Creativity 0.5h · Execution 0.5h · **Answer type:** exact-match string, simulator-checked
- **Prompt:** A token sits on integer 0. Three actions: `D` (double: x → 2x), `I` (increment: x → x + 1), `Z` (zero: x → 0). Reach **exactly 2026** using the **fewest** actions; among all shortest action strings, return the **lexicographically smallest** (order D < I < Z).
- **Canonical answer:** `IDIDIDIDIDIDDIDDID`  (18 actions)
- **Verifier:** run the string through the deterministic simulator — must land on 2026, its length must equal the BFS-recomputed optimum (18), and it must equal the lexicographically-minimal optimal string (`check_A1`).
- **Worked solution:** `Z` never helps for a positive target (pure distractor). Working backward from 2026 (halve when even, subtract 1 when odd) reaches 0 in 18 steps → optimum 18. A breadth-first search expanding actions in order D, I, Z yields the lexicographically-smallest 18-move solution `IDIDIDIDIDIDDIDDID`.
- **Why it's hard / typical failure:** Recognize the Z distractor, prove optimality (not a greedy forward guess), then honor the lexicographic tie-break. Failures: using Z; a forward-greedy non-optimal path; correct length but wrong tie-break.
- **Guard:** simulator + BFS-recomputed optimum; an 18-character string is unguessable.

---

## Verification & integrity trail

- `verify_items.py` — recomputes **all ten** ground-truth answers from first principles and self-asserts (M2 to 25 digits; C1 via a 300-case oracle; A1's optimum cross-checked by reverse-greedy). Run it: every answer above is printed by this script, not typed by hand.
- `checkers.py` — the ten deterministic checkers, plus a demonstration that they **accept** each canonical answer and **reject** near-miss wrong ones (including Q2 = 2/7).
- `items.json` — machine-readable item set (id, domain, difficulty, prompt, answer_type, canonical_answer, verifier).

Reproducibility discipline is deliberate: it mirrors how I approach research verification (independent bit-for-bit re-execution) and is exactly the property eval buyers are paying to get.

---

## Where a set like this goes (routes, honestly labeled)

- **METR task/eval bounty** — the one *currently-published* rate: **$300 per task-hour** (+ up to 50% bonus), output-paid, form/PR-based, built to the METR Task Standard (environment + deterministic scorer). No video gate. Items A1, C1, Q1 are closest to their "capability, not memorization" task format. metr.org/careers.
- **Epoch AI — FrontierMath "Open Problems"** submission form (actively commissioning contributions). M1, M2, M3, Q2 fit the exact-answer + verification-script format; author pay is **not publicly posted**, so I don't quote a number. epoch.ai/frontiermath.
- **Humanity's Last Exam — rolling intake** (agibenchmark@safe.ai). The original round's $5k/$500 + co-authorship was a closed cycle; the rolling fork still accepts hard, verifiable items.
- **Portfolio / grant artifact.** The strongest immediate use: attach this to the Epoch AI Benchmark-Reviews and Mercor/METR applications and to an Emergent Ventures / Manifund note as proof of the "formulate new frontier data, verifiably" skill.
- **Marketplaces (Mercor, Surge, Handshake)** run eval-authoring queues (~$25–250+/hr) but gate on an AI **video** interview — flagged as blocked under your stated constraint unless you clear it.

*Honest caveat carried from the research pass: only METR's $300/task-hour is a currently-published rate; FrontierMath author pay is undisclosed and HLE's $5k/$500 was the closed round — don't quote those as live.*
