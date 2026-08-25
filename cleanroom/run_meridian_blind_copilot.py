import json
import pathlib
import subprocess
from datetime import datetime, timezone

import run_meridian_blind as source

RUN_ID = source.RUN_ID
PROMPT = source.PROMPT


def main():
    attempts = [
        {"label": "auto", "args": []},
    ]
    errors = []
    memo = None
    model_used = None
    for attempt in attempts:
        try:
            cmd = [
                "copilot",
                "-sp",
                PROMPT,
                "--no-ask-user",
                "--no-custom-instructions",
            ] + attempt["args"]
            proc = subprocess.run(
                cmd,
                text=True,
                capture_output=True,
                timeout=600,
                check=False,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                memo = proc.stdout.strip()
                model_used = attempt["label"]
                break
            errors.append({"attempt": attempt["label"], "returncode": proc.returncode, "stderr": proc.stderr[-4000:]})
        except Exception as exc:
            errors.append({"attempt": attempt["label"], "error": repr(exc)})

    if not memo:
        raise RuntimeError("Copilot CLI evaluation failed: " + json.dumps(errors))

    outdir = pathlib.Path("results")
    outdir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    header = (
        f"# Project Meridian — First-Pass Blind IC Memo\n\n"
        f"- Run ID: `{RUN_ID}`\n"
        f"- Execution context: GitHub Actions clean-room runner via GitHub Copilot CLI\n"
        f"- Model selection: `{model_used}`\n"
        f"- Timestamp UTC: `{now}`\n"
        f"- Builder answer key supplied to evaluator: **NO**\n"
        f"- Expected scorecard / verdict supplied to evaluator: **NO**\n\n"
        f"---\n\n"
    )
    (outdir / f"{RUN_ID}.md").write_text(header + memo + "\n", encoding="utf-8")
    metadata = {
        "run_id": RUN_ID,
        "execution_context": "GitHub Actions + GitHub Copilot CLI",
        "model_selection": model_used,
        "timestamp_utc": now,
        "input_contains_hidden_answer_key": False,
        "input_contains_expected_scorecard": False,
        "input_contains_prescribed_verdict": False,
        "errors": errors,
    }
    (outdir / f"{RUN_ID}.metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print("Wrote first-pass memo using Copilot CLI auto model selection")


if __name__ == "__main__":
    main()
