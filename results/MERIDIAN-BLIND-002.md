# Project Meridian — First-Pass Blind IC Memo

- Run ID: `MERIDIAN-BLIND-002`
- Execution context: Independent evaluator (frontier model) in an isolated context. The evaluator received ONLY the evaluator-facing blind prompt (`cleanroom/run_meridian_blind.py` → `PROMPT`): the AI-Q v0.1 protocol, the six management claims, and the deterministic data-room evidence.
- Builder answer key supplied to evaluator: **NO**
- Expected scorecard / verdict supplied to evaluator: **NO**
- Verification: deterministic discipline gate `cleanroom/verify_memo.py` (no LLM judge).

---

# FIRST-PASS INVESTMENT COMMITTEE MEMO
## Project Meridian — AI-Q v0.1 Acquisition-Claim Review
**Clean-room run:** MERIDIAN-BLIND-002 | **Basis:** Evaluator-facing protocol, six management claims (C1–C6), and the deterministic data-room extract only | **Status:** FIRST PASS — not for final underwriting

> Operating rule applied throughout: *AI proposes; deterministic systems verify; evidence remains traceable.* Conclusions below are stated in evidence-state language. Where a metric is arithmetically real but narrowly defined, it is labeled and normalized, not characterized as intentional misstatement.

---

## 1. Executive Conclusion (≤8 bullets)

- **The core capability is real but the headline rate is a mature-cohort number, not a portfolio number.** Full-Meridian successful automated resolution reconstructs to **83.92%** on mature customers (≈ the represented ~84%) but falls to **70.11%** on the fresh-customer holdout — a **13.81-point** drop.
- **The represented ~18-point architecture lift is arithmetically real only against an under-configured comparator.** The 18.375-point figure is *full stack vs. a thin single-pass baseline*. Decomposed against a normalized generic scaffold, the genuine target-specific contribution is **~8.6 points (full stack)**, of which **~5.1 points is architecture** and **~3.5 points is proprietary data** (mature).
- **A genuine, if modest, proprietary-architecture advantage exists and partially survives transfer** (~5.1 pts mature → ~3.9 pts fresh over a normalized generic). This is the most defensible technical asset in the pack.
- **The proprietary-data advantage is real but concentrated and non-transferring.** It is large exactly where theory predicts (knowledge-need-true: **+7.63 pts** mature) and ~zero where it should be (knowledge-need-false: **0.0 pts**), but collapses to **+0.33 pts** on fresh customers.
- **The ~$0.09 unit cost is real but narrowly scoped.** It is inference cost per *success* only. Normalized to model/infra including retries and failed attempts it is **~$0.157 (mature) / ~$0.195 (fresh)**; fully loaded with variable human review/fallback it is **~$0.427 (mature) / ~$0.814 (fresh)**. What this means for overall ROI is *not* determinable from these unit costs alone.
- **The ~34% labor reduction is a real observed before/after association, not an identified causal effect.** The supplied cohort has no randomized or matched control and documents concurrent initiatives and volume changes; the Meridian-attributable share is **INSUFFICIENT EVIDENCE**.
- **A genuine operational strength is present: quality gating works.** The "successful" metric already nets out wrong auto-resolutions, and the wrong-auto rate stays low (0.74% mature; 2.17% fresh) even under distribution shift.
- **"Broadly stable across customers and verticals" is not supported as stated**, but degradation is heterogeneous — e-commerce transfers well (86.6→80.0), fintech moderately (82.8→71.3), and the new healthcare vertical is weak (59.0). Do not read the healthcare result as a universal vertical failure.

---

## 2. Claim Matrix (C1–C6)

States: SUPPORTED · PARTIALLY SUPPORTED · NOT SUPPORTED · INSUFFICIENT EVIDENCE · NOT TESTED. `n/a` = dimension not load-bearing for that claim (assessed under another claim).

| Claim | REAL | PROPRIETARY | DURABLE | ECONOMIC |
|---|---|---|---|---|
| **C1** — ~84% resolved w/o human intervention at quality threshold | **SUPPORTED** (mature 83.92% reconstructs, net of wrong-autos) | n/a | **NOT SUPPORTED** (fresh 70.11%; −13.8 pts; wrong-auto ~3×) | n/a |
| **C2** — ~18 pt lift from proprietary orchestration vs. generic scaffold | **SUPPORTED** as arithmetic (18.375) — but rests on a thin baseline | **NOT SUPPORTED** for the *18-pt attribution*; a real ~5.1-pt architecture effect exists | **NOT SUPPORTED** (architecture-only 5.1→3.9; full-stack 8.6→4.2) | n/a |
| **C3** — ~34% support-labor-hour reduction | **SUPPORTED** as *observed association* (33.93%/34.33%) | n/a | INSUFFICIENT EVIDENCE | **INSUFFICIENT EVIDENCE** (no control; causal share not identified) |
| **C4** — ~$0.09 inference cost per successful resolution | **SUPPORTED** ($0.0915 / $0.0930 reconstruct) | n/a | **PARTIALLY SUPPORTED** (narrow metric stable; loaded costs rise on fresh) | **PARTIALLY SUPPORTED** (narrow definition; production-relevant cost materially higher) |
| **C5** — accumulated data → measurable advantage + increasing defensibility | **PARTIALLY SUPPORTED** (real in mature, ~0 in fresh) | **SUPPORTED** (effect is by-construction target-specific; concentrated on knowledge-need cases) | **NOT SUPPORTED** (data effect 3.5→0.33 on fresh) | INSUFFICIENT EVIDENCE (defensibility *trajectory*) |
| **C6** — broadly stable across new customers & verticals | n/a | n/a | **NOT SUPPORTED** (−13.8 pt cohort drop; wide vertical dispersion) — heterogeneous, not uniform | n/a |

**C5 defensibility note:** "increasing defensibility" is assessed **INSUFFICIENT EVIDENCE** — the data are cross-sectional (mature vs. fresh cohorts), not a within-customer longitudinal accumulation curve, and no competitor-replication evidence is supplied. This is neither a confirmation of a compounding moat nor a finding that a moat is absent.

---

## 3. Reproduced / Reconstructed Quantitative Findings

**C1 — headline rate reconstructs and is quality-netted.**
- Mature: auto-resolved incl. wrong = 84.5417%; wrong-auto among auto-resolved = 0.7393%. Net success = 84.5417% × (1 − 0.007393) = **83.92%** (matches `successful_automated_resolution_pct.full_meridian`).
- Fresh: 71.6667% × (1 − 0.021705) = **70.11%**.
- The success metric is therefore *already net of wrong auto-resolutions* — a quality gate is applied, not a raw containment rate.

**C2 — the 18-point headline decomposes cleanly (mature).**
Headline = full_meridian − management_baseline = 83.9167 − 65.5417 = **18.375 pts**, which splits into three additive parts:

| Component | Arithmetic | Points | Share of headline |
|---|---|---|---|
| Comparator-envelope normalization (weak baseline → normalized generic) | 75.2917 − 65.5417 | **9.750** | **53%** |
| Architecture-only (Meridian-no-data − normalized generic) | 80.4167 − 75.2917 | **5.125** | **28%** |
| Proprietary data (full − Meridian-no-data) | 83.9167 − 80.4167 | **3.500** | **19%** |
| **Total** | | **18.375** | 100% |

**Fresh cohort, same decomposition:** headline 12.556 = 8.333 (comparator) + 3.889 (architecture) + 0.333 (data). Architecture share holds (~31%); the data share nearly vanishes (~3%).

**C5 — data effect is mechanistically localized (mature):** knowledge-need-true = 88.37% (full) vs. 80.74% (no-data) = **+7.63 pts**; knowledge-need-false = **0.0 pts**. Vertical data-lift: e-commerce +4.5, fintech +3.5, SaaS +2.5.

---

## 4. Comparator Analysis (do not collapse the four ladders)

The pack supplies four configurations; the represented lift depends entirely on which two are differenced.

| Comparison | What it isolates | Mature | Fresh |
|---|---|---|---|
| Full Meridian vs. **management baseline** (thin single-pass envelope) | Marketing-grade headline; conflates envelope + architecture + data | **18.375** | 12.556 |
| Normalized generic vs. management baseline | Pure comparator handicap (envelope, not Meridian IP) | **9.750** | 8.333 |
| Meridian-no-data vs. **normalized generic** | **Architecture-only** target contribution | **5.125** | 3.889 |
| Full Meridian vs. **normalized generic** | **Full target-specific advantage** (architecture + data) | **8.625** | 4.222 |
| Full Meridian vs. Meridian-no-data | **Data-only** contribution | **3.500** | 0.333 |

**Reading.** A "standard generic agent scaffold using the same frontier model family" is most faithfully represented by the *normalized generic*, not the thin management baseline. Against that fair comparator, the target's genuine advantage is **8.625 pts (full stack)** / **5.125 pts (architecture only)** in mature customers — real and non-trivial, but well below the ~18-pt headline. Roughly **53% of the headline is attributable to the comparator being under-configured**, not to Meridian technology. This is a definition/attribution gap to be corrected in underwriting, not evidence of intent.

---

## 5. Transfer / Durability Analysis (fresh customers + verticals)

**Customer transfer (the central durability finding).** Full-Meridian success falls **83.92% → 70.11% (−13.81 pts)** from mature to fresh. Wrong-auto rate rises **0.74% → 2.17%** (≈3×, still low single digits). The target-specific advantage over a normalized generic compresses **8.6 → 4.2 pts**, and the data component all but disappears (**3.5 → 0.33 pts**). The advantage that persists is the **architecture** component (5.1 → 3.9 pts).

**Vertical heterogeneity — describe, do not over-generalize.**

| Vertical | Mature success | Fresh success | Read |
|---|---|---|---|
| E-commerce | 86.63 | 80.00 | Transfers well |
| Fintech | 82.75 | 71.33 | Moderate degradation |
| SaaS | 82.38 | — (not in fresh set) | Mature only |
| Healthcare | — (not in mature set) | 59.00 | New vertical, weak |

Mature verticals are tightly clustered (~4.25-pt range); the fresh set is wide (~21-pt range) driven largely by **healthcare (59.0)**, a vertical that appears *only* in the fresh holdout. **The healthcare weakness should not be generalized to all verticals** — e-commerce holds up at 80.0 even out-of-cohort. The pattern is consistent with degradation driven by *customer newness and vertical-specific knowledge*, concentrated where the accumulated-data layer contributes least (fresh data-lift: e-commerce +0.67, fintech 0.0, healthcare +0.33).

---

## 6. Unit-Economics Normalization (state what is measured; infer no ROI)

Three nested cost definitions are supplied per successful automated resolution:

| Definition | What it counts | Mature | Fresh | Fresh/Mature |
|---|---|---|---|---|
| Management narrow metric (**C4**) | Inference for successful resolutions only | **$0.0915** | **$0.0930** | 1.02× |
| Model + retrieval + orchestration incl. retries & failed attempts | Full model/infra to *produce* the successes | **$0.1570** | **$0.1949** | 1.24× |
| Fully loaded incl. variable human review & fallback labor | Above + human-in-the-loop cost | **$0.4270** | **$0.8141** | **1.91×** |

**What is measured:** the ~$0.09 figure is arithmetically real and stable across cohorts, but it **excludes the retries, failed attempts, and human review/fallback that are part of delivering a resolution.** Normalizing:
- Model/infra is **~1.72× (mature) / ~2.10× (fresh)** the narrow metric.
- Fully loaded is **~4.67× (mature) / ~8.76× (fresh)** the narrow metric, and **nearly doubles** from mature to fresh (driven by the higher fallback/human-review incidence on lower-containment fresh customers).

**What is *not* concluded:** these unit costs alone do **not** establish overall customer ROI, gross margin, or competitiveness, and no such inference is drawn here. They establish only that the decision-relevant cost per resolution is materially higher than the represented narrow metric, and cohort-sensitive.

---

## 7. Causal-Evidence Analysis — Customer Labor Reduction (C3)

**Observation (supported):** across 12 customers the before/after support-labor-hour reduction is **33.93% (unweighted) / 34.33% (weighted)** — the represented ~34% is a real observed number.

**Attribution (not identified):** the supplied `important_design_notes` state directly that (a) monthly ticket volume changes between periods, (b) some customers ran concurrent process/help-center/staffing initiatives during the window, and (c) **the cohort contains no randomized or adequately matched control** that isolates the Meridian-caused share.

**Conclusion:** the Meridian-attributable portion of the 34% is **INSUFFICIENT EVIDENCE**. The observed reduction is an association that bundles Meridian with volume shifts and concurrent initiatives; per protocol, the hidden treatment effect is **not** inferred, imputed, or bounded here. This is the memo's preserved INSUFFICIENT EVIDENCE conclusion and should be treated as an open, resolvable question rather than a negative finding.

---

## 8. Genuine Technical / Operational Strengths

1. **Working quality gate ("deterministic systems verify").** The headline success metric is *already net of wrong auto-resolutions*: mature auto-resolved 84.54% → net 83.92% after removing a 0.74% wrong-auto rate. Even under distribution shift the wrong-auto rate stays low (2.17% on fresh). The system is willing to *not* auto-resolve, and the gate holds most errors down out-of-cohort — a credible safety/quality control, not just a containment number.
2. **A real, transfer-surviving architecture contribution.** After the comparator is fairly normalized *and* the data layer is removed, the orchestration still adds **5.1 pts (mature) / 3.9 pts (fresh)**. This is the most defensible piece of proprietary IP in the pack.
3. **Mechanistically coherent data effect.** The data layer helps precisely where it should (knowledge-need-true +7.63 pts) and not where it shouldn't (knowledge-need-false 0.0) — raising confidence that the mature-cohort data lift is real signal rather than artifact.
4. **Diligence-friendly instrumentation.** The target supplied the exact ablations (no-data, normalized-generic) and a sample evaluation harness that let this decomposition be performed at all, plus stable, low retry counts (0.513 mature / 0.538 fresh).

---

## 9. Evidence Ledger (source/measurement for each load-bearing conclusion)

| # | Conclusion | Supplied source / measurement |
|---|---|---|
| E1 | Mature success ≈84% and quality-netted | `mature_internal_evaluation.successful_automated_resolution_pct.full_meridian` (83.917); `auto_resolved_including_wrong_auto_pct_full_meridian` (84.542); `wrong_auto_errors_among_auto_resolved_pct_full_meridian` (0.739) |
| E2 | Fresh success 70.11%; wrong-auto ~3× | `fresh_customer_holdout.successful_automated_resolution_pct.full_meridian` (70.111); `...wrong_auto_errors...` (2.171) |
| E3 | 18-pt headline = full vs. thin baseline | `derived_arithmetic...management_headline_full_vs_management_baseline_lift_points_mature` (18.375); `benchmark_configuration.management_baseline` (thin envelope) |
| E4 | Comparator handicap = 9.75 pts | `mature...normalized_generic` (75.292) − `management_baseline` (65.542) |
| E5 | Architecture-only = 5.125; data-only = 3.500; full-stack fair = 8.625 (mature) | `derived_arithmetic...architecture_only_lift...` (5.125), `...full_stack_vs_normalized_generic...` (8.625); `proprietary_data_effect.overall_percentage_point_lift_full_vs_no_data` (3.5) |
| E6 | Fresh decomposition (3.889 arch / 0.333 data / 4.222 full-stack) | `derived_arithmetic...fresh_architecture_only_lift_points`, `...fresh_full_stack_vs_normalized_generic_points`; `fresh...proprietary_data_effect.overall...` (0.333) |
| E7 | Cohort drop −13.81 pts | `derived_arithmetic...mature_to_fresh_full_meridian_drop_points` (13.806) |
| E8 | Data effect localized to knowledge-need | `mature...proprietary_data_effect.knowledge_need_true_lift_points` (7.629); `knowledge_need_false_lift_points` (0.0) |
| E9 | Vertical transfer heterogeneity | `mature/fresh...vertical_success_pct_full_meridian` (ecom 86.6→80.0; fintech 82.8→71.3; saas 82.4; healthcare 59.0 fresh) |
| E10 | Unit-cost ladder | `cost_per_successful_automated_resolution_usd.{management_narrow_metric, all_..._including_retries_and_failed_attempts, including_variable_human_review_and_fallback_labor}` for mature ($0.0915/$0.1570/$0.4270) and fresh ($0.0930/$0.1949/$0.8141) |
| E11 | Labor reduction observed ~34% | `customer_roi_cohort.observed_before_after_support_labor_hour_reduction_pct_{unweighted_mean 33.93, aggregate_weighted 34.33}` |
| E12 | Causal share not identified | `customer_roi_cohort.important_design_notes` (volume change; concurrent initiatives; no randomized/matched control) |
| E13 | Retry stability | `mature/fresh...mean_retries_per_eligible_case` (0.513 / 0.538) |

*Referenced but not independently re-executed:* `Model_Architecture_Whitepaper.pdf`, `Data_Dictionary.pdf`, `benchmark_configuration.csv`, `code/Sample_Evaluation_Harness.py`, `CIM_Executive_Summary.pdf`, `Management_AI_Claims_Ledger.xlsx` (see diligence requests).

---

## 10. Transaction Implications & Prioritized Diligence Requests

*Qualitative underwriting posture only. No price, value, range, multiple, or EBITDA implication is expressed or implied.*

**What the IC can reasonably underwrite now:**
- A **real, quality-gated automation capability** with a mature-cohort success rate near the represented level and a functioning wrong-auto gate that holds under shift.
- A **genuine, comparator-normalized target-specific advantage of ~8.6 pts (mature)**, of which **~5.1 pts is architecture that partially survives transfer** — this is the durable technical core.
- A **narrow inference-cost figure (~$0.09) that is arithmetically accurate** and stable across cohorts *as defined*.

**What the IC cannot yet safely underwrite:**
- The **~18-pt lift as a proprietary-architecture claim** — the majority is comparator handicap and data; the architecture-only figure is ~5 pts.
- The **~84% rate as a portfolio/new-customer expectation** — it is a mature-cohort figure that degrades ~14 pts on fresh customers.
- The **proprietary-data layer as a *transferring* or *compounding* moat** — measurable in mature, ~zero in fresh; the defensibility trajectory is unproven either way.
- **Any labor-cost/ROI conclusion from the 34% figure** — causal share unidentified.
- **Production unit economics from the $0.09 metric** — the decision-relevant loaded cost is ~$0.427 (mature) / ~$0.814 (fresh) per resolution and cohort-sensitive.

**Prioritized diligence requests (evidence that would resolve the uncertainty):**
1. **Restate the lift on the normalized comparator** and have management adopt the full-stack-vs-normalized-generic (~8.6-pt) and architecture-only (~5.1-pt) figures as the represented numbers; reconcile against `benchmark_configuration.csv` and the harness.
2. **Longitudinal, within-customer ramp curves** (success and data-lift vs. customer tenure/interaction volume) to test whether the mature→fresh gap is a *maturation* effect (supports "increasing" defensibility) or a *selection* effect — directly resolves C5's INSUFFICIENT EVIDENCE.
3. **A controlled or adequately matched design for the labor result** (staggered rollout, matched controls, or holdout) to identify the Meridian-attributable share of the ~34% — resolves C3.
4. **Fully-loaded cost bridge** per resolution by cohort and vertical, with the fallback/human-review driver behind the mature→fresh near-doubling, and the retry/failed-attempt distribution from the harness.
5. **Expanded fresh + vertical coverage**, especially additional healthcare and additional non-e-commerce fresh customers, to characterize the transfer curve rather than infer it from one 900-case holdout (3 fresh customers).
6. **Quality-threshold definition and SLA conformance**: the represented quality threshold value is not in the extract; supply the threshold and per-customer wrong-auto/appeal data to confirm the gate meets a named standard, not just a low observed rate.
7. **Independent re-execution** of `Sample_Evaluation_Harness.py` on raw case-level data to confirm the reconstructions in §3–§6 end-to-end.

*First-pass memo ends. Findings are provisional pending the diligence items above; no conclusion here should be read as final or as a valuation input.*
