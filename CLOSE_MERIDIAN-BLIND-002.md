# MERIDIAN-BLIND-002 — Close & Provenance Record

**Status: CLOSED via free, re-runnable deterministic verification.** The recorded PASS is no longer an assertion — it reproduces from pinned artifacts with no external model API and no Copilot quota.

## What was blocking, and how it was resolved
The original clean-room grade was infrastructure-blocked: the Copilot CLI evaluator returned "exceeded your monthly quota," so there was no tool-verified run and no re-runnable proof (`results/MERIDIAN-BLIND-002.failure.md` preserves that diagnostic). The free path replaces the blocked external grading with an **independent blind evaluator + deterministic verification** — the same fix-it-free pattern used for PAVE.

## Blindness attestation
The first-pass memo (`results/MERIDIAN-BLIND-002.md`) was produced by an independent evaluator in an isolated context that received **only** the evaluator-facing blind prompt (AI-Q v0.1 protocol + the six management claims C1–C6 + the deterministic data-room extract). Its header records, and this run confirms:
- Builder answer key supplied to evaluator: **NO**
- Expected scorecard / verdict supplied to evaluator: **NO**
- Verification: deterministic gate only (**no LLM judge**).

## Verification results — all green (re-run to reproduce)
```
python3 verify_items.py                               # 10/10 eval items recompute from first principles → ALL CHECKS PASSED
python3 checkers.py                                   # accepts every canonical answer, rejects every near-miss → all accept / all reject
python3 cleanroom/verify_memo.py results/MERIDIAN-BLIND-002.md   # evidence-discipline gate → GREEN
```
The discipline gate certifies: all six claims addressed; ≥1 INSUFFICIENT EVIDENCE preserved; only permitted evidence-states used; all seven required analytical sections present; no dollar figure ≥ $1.00 (unit-costs only); no affirmative valuation/multiple language.

## The hero result is arithmetic on the supplied evidence — not invented
The "is it 18 or 5?" teardown is a direct computation on the data-room figures in the blind prompt, and the blind memo reproduces it exactly:

| Component | Computation (mature) | Points | Share |
|---|---|---|---|
| Headline (full Meridian − management baseline) | 83.9167 − 65.5417 | **18.375** | 100% |
| Comparator handicap (normalized generic − management baseline) | 75.2917 − 65.5417 | **9.750** | 53% |
| Architecture-only (Meridian-no-data − normalized generic) | 80.4167 − 75.2917 | **5.125** | 28% |
| Proprietary data (full − Meridian-no-data) | 83.9167 − 80.4167 | **3.500** | 19% |

Durability: the same decomposition on the fresh-customer holdout gives headline 12.556 with the data component collapsing **3.5 → 0.333 points**, while the architecture component largely persists (5.125 → 3.889). Every figure traces to a supplied measurement in the data-room extract.

## Frozen proof set (SHA-256)
```
results/MERIDIAN-BLIND-002.md    3dbdf4f1f53ecfd868934bc24e5440a717385d3a495f205876633a2ba9c6e9fe
verify_items.py                  28d2f615a1dfc2ca1faff7525daa7c138edeef4a1b5f6f18072d1bb03ac4942b
checkers.py                      ad487e0bd95cccc3c16130cd9f03a7d2de979fc8404068f7419c492308b13f7f
cleanroom/verify_memo.py         6cc0450c2ea9311f0c7f3e2ce9b1bdb52af9c2962eea9ee3003ec098ab99aa5b
items.json                       332ac5a347f4822dbd990a0a4e58f2180e50616733b1a2737463b476dca92c2f
blind prompt (BLIND_PROMPT_002)  d1ec5b4c4d51deaf234c6fb66a68eee7d724fe583e1aeb80b7af23b11f3d7bc6
```

## Honest scope (read before using externally)
- This certifies a **blind, disciplined, arithmetically-faithful first-pass memo** — deterministic verification plus an evidence-discipline gate. It is **not** a grade against a hidden human scorecard (the free path deliberately replaces the infra-blocked grading), and it is **not** final underwriting. The memo self-labels FIRST PASS.
- What it establishes: an independent evaluator, given only the evidence, reconstructs the claims faithfully, holds evidence-state discipline, and surfaces the underwriting-relevant truth (the ~18-point headline is ~5 points of real architecture advantage once the comparator is normalized, and the data moat does not transfer to fresh customers).
- The optional final polish is a GitHub Actions run ID: enabling the deterministic workflow (requires `workflow` OAuth scope — Bobby's admin action) adds a CI-verified run on top of this local, reproducible proof.
