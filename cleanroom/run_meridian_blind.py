import json
import os
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone

RUN_ID = "MERIDIAN-BLIND-001"

# IMPORTANT: This clean-room runner contains evaluator-facing evidence only.
# It intentionally contains no hidden answer key, expected classifications,
# scorecard, release threshold, or prescribed investment conclusion.

PROTOCOL = r"""
AI-Q v0.1 evaluates each material AI/software claim across four dimensions:

REAL — Can the represented result be reproduced or independently reconstructed from the supplied evidence?
PROPRIETARY — How much demonstrated advantage is attributable to target-specific technology/data versus commodity model capability or an unfair comparator?
DURABLE — Does the demonstrated advantage survive fresh customers, distribution shift, vertical shift, and reasonable perturbation?
ECONOMIC — Does the represented advantage remain meaningful after retries, failures, orchestration, and variable human review/fallback costs are normalized?

Permitted evidence states: SUPPORTED, PARTIALLY SUPPORTED, NOT SUPPORTED, INSUFFICIENT EVIDENCE, NOT TESTED.

Operating rule: AI proposes. Deterministic systems verify. Evidence remains traceable.

Do not turn absence of evidence into a negative fact. Distinguish an observed association from causal attribution. Do not accuse management of deception unless evidence requires it. Do not invent acquisition price, EBITDA impact, or a valuation adjustment not supported by the supplied materials.
"""

MANAGEMENT_CLAIMS = [
    {
        "id": "C1",
        "claim": "Meridian successfully resolves approximately 84% of eligible customer-support cases without human intervention while meeting the represented quality threshold.",
    },
    {
        "id": "C2",
        "claim": "Meridian's proprietary orchestration architecture delivers roughly 18 percentage points of lift over a standard generic agent scaffold using the same frontier model family.",
    },
    {
        "id": "C3",
        "claim": "Customers reduce support labor hours by approximately 34% after Meridian deployment.",
    },
    {
        "id": "C4",
        "claim": "Meridian's unit AI inference cost is about $0.09 per successful automated resolution.",
    },
    {
        "id": "C5",
        "claim": "Meridian's accumulated customer-interaction data creates a measurable performance advantage and increasing defensibility.",
    },
    {
        "id": "C6",
        "claim": "Meridian's performance remains broadly stable across new customers and support verticals.",
    },
]

# These are deterministic measurements produced from the evaluator-facing data room.
# They are facts available to the evaluator pipeline, not hidden expected conclusions.
EVIDENCE = {
    "source_inventory": [
        "docs/CIM_Executive_Summary.pdf",
        "docs/Management_AI_Claims_Ledger.xlsx",
        "docs/Model_Architecture_Whitepaper.pdf",
        "docs/Data_Dictionary.pdf",
        "data/internal_mature_evaluation.csv (2,400 cases; 6 mature customers)",
        "data/fresh_customer_holdout.csv (900 cases; 3 fresh customers)",
        "data/customer_roi_cohort.csv (12 customers)",
        "data/benchmark_configuration.csv",
        "code/Sample_Evaluation_Harness.py",
    ],
    "benchmark_configuration": {
        "management_baseline": "single-pass generic comparison with a materially thinner retrieval/retry/tool envelope than the full Meridian stack",
        "normalized_generic": "generic scaffold normalized to a comparable retrieval/tool/retry operating envelope",
        "meridian_no_proprietary_data": "Meridian architecture evaluated with the target-specific customer-memory/data advantage removed",
        "full_meridian": "complete target stack including target-specific orchestration and customer-memory/data layer",
    },
    "mature_internal_evaluation": {
        "n": 2400,
        "successful_automated_resolution_pct": {
            "full_meridian": 83.9166667,
            "meridian_no_proprietary_data": 80.4166667,
            "normalized_generic": 75.2916667,
            "management_baseline": 65.5416667,
        },
        "auto_resolved_including_wrong_auto_pct_full_meridian": 84.5416667,
        "wrong_auto_errors_among_auto_resolved_pct_full_meridian": 0.7392804,
        "cost_per_successful_automated_resolution_usd": {
            "management_narrow_metric": 0.09153118,
            "all_model_retrieval_orchestration_spend_including_retries_and_failed_attempts": 0.15703876,
            "including_variable_human_review_and_fallback_labor": 0.42704050,
        },
        "mean_retries_per_eligible_case": 0.5129167,
        "vertical_success_pct_full_meridian": {
            "ecommerce": 86.625,
            "fintech": 82.750,
            "saas": 82.375,
        },
        "proprietary_data_effect": {
            "overall_percentage_point_lift_full_vs_no_data": 3.5000000,
            "knowledge_need_true_full_success_pct": 88.3742053,
            "knowledge_need_true_no_data_success_pct": 80.7447775,
            "knowledge_need_true_lift_points": 7.6294278,
            "knowledge_need_false_lift_points": 0.0,
            "vertical_lift_points": {"ecommerce": 4.5, "fintech": 3.5, "saas": 2.5},
        },
    },
    "fresh_customer_holdout": {
        "n": 900,
        "successful_automated_resolution_pct": {
            "full_meridian": 70.1111111,
            "meridian_no_proprietary_data": 69.7777778,
            "normalized_generic": 65.8888889,
            "management_baseline": 57.5555556,
        },
        "auto_resolved_including_wrong_auto_pct_full_meridian": 71.6666667,
        "wrong_auto_errors_among_auto_resolved_pct_full_meridian": 2.1705426,
        "cost_per_successful_automated_resolution_usd": {
            "management_narrow_metric": 0.09298242,
            "all_model_retrieval_orchestration_spend_including_retries_and_failed_attempts": 0.19493625,
            "including_variable_human_review_and_fallback_labor": 0.81411123,
        },
        "mean_retries_per_eligible_case": 0.5377778,
        "vertical_success_pct_full_meridian": {
            "ecommerce": 80.0000000,
            "fintech": 71.3333333,
            "healthcare": 59.0000000,
        },
        "proprietary_data_effect": {
            "overall_percentage_point_lift_full_vs_no_data": 0.3333333,
            "knowledge_need_true_lift_points": 0.6437768,
            "vertical_lift_points": {"ecommerce": 0.6666667, "fintech": 0.0, "healthcare": 0.3333333},
        },
    },
    "customer_roi_cohort": {
        "n_customers": 12,
        "observed_before_after_support_labor_hour_reduction_pct_unweighted_mean": 33.9322950,
        "observed_before_after_support_labor_hour_reduction_pct_aggregate_weighted": 34.3263080,
        "important_design_notes": [
            "Monthly ticket volume changes between the before and after periods.",
            "Some customers had concurrent process, help-center, and/or staffing initiatives during the observation window.",
            "The supplied cohort does not contain a randomized or adequately matched control that identifies how much of the observed labor-hour change was caused by Meridian alone.",
        ],
    },
    "derived_arithmetic_for_reference": {
        "management_headline_full_vs_management_baseline_lift_points_mature": 18.3750000,
        "architecture_only_lift_meridian_no_data_vs_normalized_generic_mature_points": 5.1250000,
        "full_stack_vs_normalized_generic_mature_points": 8.6250000,
        "fresh_full_vs_management_baseline_lift_points": 12.5555555,
        "fresh_architecture_only_lift_points": 3.8888889,
        "fresh_full_stack_vs_normalized_generic_points": 4.2222222,
        "mature_to_fresh_full_meridian_drop_points": 13.8055556,
    },
}

PROMPT = f"""
You are the independent evaluator for clean-room run {RUN_ID}. You have not been given any builder answer key or expected verdict.

Your task is to perform an AI-Q v0.1 acquisition-claim review of Project Meridian using ONLY the evaluator-facing protocol, management claims, and deterministic evidence below.

{PROTOCOL}

MANAGEMENT CLAIMS
{json.dumps(MANAGEMENT_CLAIMS, indent=2)}

DETERMINISTIC EVIDENCE EXTRACTED FROM THE DATA ROOM
{json.dumps(EVIDENCE, indent=2)}

Produce the untouched FIRST-PASS Investment Committee memo. It must include:
1. Executive conclusion in no more than 8 bullets.
2. A claim matrix for C1-C6. For each claim separately assess any applicable REAL / PROPRIETARY / DURABLE / ECONOMIC dimension using only: SUPPORTED, PARTIALLY SUPPORTED, NOT SUPPORTED, INSUFFICIENT EVIDENCE, NOT TESTED.
3. Reproduced or reconstructed quantitative findings with explicit arithmetic where useful.
4. Comparator analysis for the claimed proprietary architecture lift. Separate the weak management comparison, normalized generic comparison, architecture-only contribution, and data contribution rather than collapsing them.
5. Transfer/durability analysis using the fresh-customer and vertical evidence.
6. Unit-economics normalization separating the narrow management cost statistic from production-relevant model/infra cost and variable human review/fallback cost.
7. Causal-evidence analysis for the observed customer labor reduction. Do not infer an unobserved treatment effect.
8. At least one genuine positive technical/operational strength if the evidence supports one.
9. An evidence ledger citing the specific supplied source/measurement used for every load-bearing conclusion.
10. Transaction implications and a prioritized list of additional diligence requests. Do NOT invent an acquisition price, EBITDA impact, or valuation discount.

Be adversarial but fair. A represented metric can be arithmetically real while its broader interpretation is only partially supported. Preserve uncertainty explicitly.
"""


def call_model(token: str):
    endpoint = "https://models.github.ai/inference/chat/completions"
    # Ordered strongest-known-to-broadest fallback. The runner records the model actually used.
    candidates = [
        "openai/gpt-5",
        "openai/gpt-4.1",
        "openai/gpt-4o",
    ]
    errors = []
    for model in candidates:
        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an independent technical diligence evaluator. Follow the supplied protocol exactly and do not infer hidden answers."},
                {"role": "user", "content": PROMPT},
            ],
            "temperature": 0.1,
            "max_tokens": 7000,
        }
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "ai-q-meridian-cleanroom",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return model, content, data.get("usage", {})
        except Exception as exc:
            errors.append({"model": model, "error": repr(exc)})
    raise RuntimeError("All GitHub Models candidates failed: " + json.dumps(errors))


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    model, memo, usage = call_model(token)
    outdir = pathlib.Path("results")
    outdir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    header = (
        f"# Project Meridian — First-Pass Blind IC Memo\n\n"
        f"- Run ID: `{RUN_ID}`\n"
        f"- Execution context: GitHub Actions clean-room runner\n"
        f"- Model: `{model}`\n"
        f"- Timestamp UTC: `{now}`\n"
        f"- Builder answer key supplied to evaluator: **NO**\n"
        f"- Expected scorecard / verdict supplied to evaluator: **NO**\n\n"
        f"---\n\n"
    )
    (outdir / f"{RUN_ID}.md").write_text(header + memo.strip() + "\n", encoding="utf-8")
    metadata = {
        "run_id": RUN_ID,
        "model": model,
        "timestamp_utc": now,
        "usage": usage,
        "input_contains_hidden_answer_key": False,
        "input_contains_expected_scorecard": False,
        "input_contains_prescribed_verdict": False,
    }
    (outdir / f"{RUN_ID}.metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote first-pass memo using {model}")


if __name__ == "__main__":
    main()
