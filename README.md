# AI Eval Work Sample — deterministic eval construction + blind claim verification

This repository contains two related demonstrations of the same standard: **AI can propose or evaluate, but the decisive checks remain inspectable and deterministic.**

## 1. Ten hard, machine-verifiable evaluation items

The original work sample is a self-contained set of ten evaluation items across math, analysis, combinatorics, cosmology, statistics, ML-evaluation methodology, probability, algorithms, language semantics, and planning. Every canonical answer is recomputed from scratch and every item ships a deterministic checker — no LLM judge is used to grade correctness.

| File | Purpose |
|---|---|
| `eval_work_sample.md` | Prompts, canonical answers, worked solutions, failure modes, and guard notes for all ten items. |
| `items.json` | Machine-readable item set. |
| `verify_items.py` | Recomputes every ground-truth answer from first principles and self-asserts. |
| `checkers.py` | Deterministic checkers plus accept-canonical / reject-near-miss tests. |
| `make_items_json.py` | Regenerates `items.json` from verified constants. |

Reproduce it:

```bash
pip install numpy scipy scikit-learn sympy mpmath
python3 verify_items.py
python3 checkers.py
```

## 2. MERIDIAN-BLIND-002 — constructed acquisition-claim verification case

The repository now also preserves a **constructed, blind technical-diligence exercise** designed to test a harder question: can an evaluator take a management claim set plus a deterministic evidence pack, without a builder answer key, and produce an investment-committee-readable conclusion that survives a non-LLM verification gate?

Meridian is **not a real company, client, or transaction**. It is a constructed evidence pack used to test the claim-verification process.

The frozen first-pass memo reconstructs the represented mature-customer performance advantage as:

- **18.375 points total**
- **9.750 points** from the comparator envelope
- **5.125 points** from target-specific architecture
- **3.500 points** from the proprietary-data layer

On the fresh-customer holdout, the same decomposition becomes:

- **12.556 points total**
- **8.333 points** comparator envelope
- **3.889 points** architecture
- **0.333 points** data

So the target-specific advantage over the normalized generic comparator compresses from **8.625 to 4.222 points**, while the data contribution nearly disappears. The exercise also separates narrow inference cost from fuller production-relevant cost and treats the represented labor reduction as an observed association rather than an identified causal effect.

Key artifacts:

| File | Purpose |
|---|---|
| `results/MERIDIAN-BLIND-002.md` | Frozen first-pass blind IC memo. |
| `cleanroom/run_meridian_blind.py` | Evaluator-facing blind prompt and deterministic evidence pack. |
| `cleanroom/verify_memo.py` | Non-LLM discipline gate for the memo. |
| `.github/workflows/meridian-blind.yml` | Public workflow for the blind-run path. |
| `results/MERIDIAN-BLIND-002.failure.md` | Preserved failed-attempt record rather than hidden cleanup. |

The latest validation workflow for the published Meridian branch completed successfully before the case was merged to `main`.

## Design standard

The two halves of this repository share the same operating principle:

1. state the exact thing being tested;
2. preserve the evidence boundary;
3. prevent the evaluator from seeing the answer key where blindness matters;
4. use deterministic verification for claims that can be mechanically checked;
5. distinguish reproduced, qualified, unsupported, and insufficient-evidence states;
6. preserve failed attempts and corrections instead of rewriting history.

**Author:** Robert "Bobby" Morong (GrobeStreet) — independent AI-evaluation and research-verification work.

## License

MIT — see `LICENSE`.
