# AI Eval Work Sample — 10 hard, machine-verifiable items

A small, self-contained benchmark: ten original evaluation items across math, analysis, combinatorics, cosmology, statistics, ML-evaluation methodology, probability, algorithms, language semantics, and planning. Every item ships a **deterministic checker**, and every canonical answer is **recomputed from scratch** by the included script — nothing is asserted by hand.

**Author:** Robert "Bobby" Morong (GrobeStreet) · independent AI-evaluation & research-verification specialist.

## Why this exists
Eval buyers pay for items whose answers a *machine* can certify, not a human vibe. This sample demonstrates that discipline end-to-end: hard, guess-resistant, leakage-resistant items, each verified by exact-match, SymPy equality, numeric tolerance, or unit tests — **never an LLM judge**.

## What's inside
| File | Purpose |
|---|---|
| `eval_work_sample.md` | The item set: prompt, canonical answer, verifier, worked solution, "why it's hard / typical failure," and guard notes for all 10 items. |
| `items.json` | Machine-readable item set (id, domain, difficulty, prompt, answer_type, canonical_answer, verifier). |
| `verify_items.py` | Recomputes every ground-truth answer from first principles and self-asserts. |
| `checkers.py` | The ten deterministic checkers + a demo that they accept each canonical answer and reject near-miss wrong ones. |
| `make_items_json.py` | Regenerates `items.json` from the verified constants. |

## Reproduce it
```bash
pip install numpy scipy scikit-learn sympy mpmath
python3 verify_items.py     # derives all 10 answers, prints them, self-asserts  -> "ALL CHECKS PASSED"
python3 checkers.py         # accept-canonical / reject-wrong demonstration      -> all accept True, all reject True
```

## Design standard
Grounded in current practice at FrontierMath (Epoch AI), GPQA, SWE-bench Verified, and Humanity's Last Exam: high-entropy answers (guessing ≪ 1%), constructed-not-copied prompts, reproducible-by-seed where applicable, and deterministic verification for every item. Difficulty is rated on three axes (background / creativity-hours / execution-hours); the set spans GPQA-hard to FrontierMath-adjacent.

## License
MIT — see `LICENSE`.
