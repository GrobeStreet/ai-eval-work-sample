#!/usr/bin/env python3
"""
Deterministic discipline gate for a Project Meridian first-pass blind memo.

This is NOT an LLM judge and NOT the builder's private correctness scorecard.
It certifies that an independently produced memo obeyed AI-Q v0.1's hard
evidence-discipline rules: only unit-cost dollar figures may appear, every
management claim must be addressed, only the permitted evidence-states may be
used, at least one INSUFFICIENT EVIDENCE conclusion must be preserved, and the
required analytical sections and evidence ledger must be present.

Exit 0 = memo passes the discipline gate (CI green).
Exit 1 = memo violates the protocol (CI red) — a real, honest result.
"""
import re
import sys
import pathlib

DEFAULT = "results/MERIDIAN-BLIND-002.md"

PERMITTED_STATES = [
    "SUPPORTED", "PARTIALLY SUPPORTED", "NOT SUPPORTED",
    "INSUFFICIENT EVIDENCE", "NOT TESTED",
]
REQUIRED_CLAIMS = ["C1", "C2", "C3", "C4", "C5", "C6"]
REQUIRED_SECTIONS = [
    "Executive Conclusion",
    "Claim Matrix",
    "Comparator Analysis",
    "Unit-Economics Normalization",
    "Causal-Evidence Analysis",
    "Evidence Ledger",
    "Diligence Requests",
]
NEGATION = [
    "no ", "not ", "never", "must not", "cannot", "can't", "without",
    "remove", "prohibit", "no other", "no such", "neither", "nor ",
    "is expressed or implied", "only ",
]
# Affirmative transaction-value patterns that must NOT appear as real outputs.
FORBIDDEN = [
    r"\b\d+(?:\.\d+)?\s?[xX]\s+(?:EBITDA|revenue|ARR|sales|earnings)\b",
    r"(?i)enterprise value",
    r"(?i)purchase price",
    r"(?i)acquisition price",
    r"(?i)implied (?:platform |company )?value",
    r"(?i)valuation of\s*\$?\d",
    r"(?i)worth (?:approximately|about|around)?\s*\$?\d",
]


def main():
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
    checks = []

    if not path.exists():
        print(f"FAIL: memo not found at {path}")
        sys.exit(1)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. Non-trivial memo
    checks.append(("memo present and substantial (>1500 chars)", len(text) > 1500))

    # 2. All six claims addressed
    for c in REQUIRED_CLAIMS:
        checks.append((f"claim {c} addressed", bool(re.search(rf"\b{c}\b", text))))

    # 3. Preserve >= 1 INSUFFICIENT EVIDENCE
    checks.append(("preserves >=1 INSUFFICIENT EVIDENCE", text.count("INSUFFICIENT EVIDENCE") >= 1))

    # 4. Uses only permitted evidence-state vocabulary in the claim matrix rows
    matrix_rows = [ln for ln in lines if ln.strip().startswith("| **C")]
    invented = []
    state_upper = re.compile(r"\b([A-Z]{3,}(?: [A-Z]{3,})*)\b")
    allowed_tokens = set()
    for s in PERMITTED_STATES:
        allowed_tokens.update(s.split())
    allowed_tokens.update({"REAL", "PROPRIETARY", "DURABLE", "ECONOMIC"})  # column context words
    for row in matrix_rows:
        for m in state_upper.findall(row):
            if m not in PERMITTED_STATES and any(w not in allowed_tokens for w in m.split()):
                invented.append(m)
    checks.append(("no invented evidence-states in claim matrix", len(invented) == 0))

    # 5. Required analytical sections present
    for sec in REQUIRED_SECTIONS:
        checks.append((f"section present: {sec}", sec.lower() in text.lower()))

    # 6. Dollar discipline: only sub-$1 unit-cost figures may appear
    bad_dollars = []
    for m in re.finditer(r"\$\s?(\d[\d,]*(?:\.\d+)?)", text):
        val = float(m.group(1).replace(",", ""))
        if val >= 1.0:
            bad_dollars.append(m.group(0))
    checks.append(("no dollar figure >= $1.00 (unit-costs only)", len(bad_dollars) == 0))

    # 7. No affirmative transaction-value / multiple language
    forbidden_hits = []
    for pat in FORBIDDEN:
        for m in re.finditer(pat, text):
            line = next((ln for ln in lines if m.group(0) in ln), "")
            low = line.lower()
            if not any(neg in low for neg in NEGATION):
                forbidden_hits.append(m.group(0))
    checks.append(("no affirmative valuation/multiple language", len(forbidden_hits) == 0))

    # ---- report ----
    print(f"Meridian memo discipline gate — {path}")
    print("=" * 64)
    all_ok = True
    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        all_ok = all_ok and ok
    print("=" * 64)
    if invented:
        print("  invented states:", sorted(set(invented)))
    if bad_dollars:
        print("  disallowed dollar figures:", sorted(set(bad_dollars)))
    if forbidden_hits:
        print("  forbidden phrases:", sorted(set(forbidden_hits)))
    print("RESULT:", "GREEN — memo passes the discipline gate" if all_ok else "RED — memo violates protocol")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
