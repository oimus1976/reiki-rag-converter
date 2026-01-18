#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
compare_answers.py

Answer Diff Observation (v0.1)
- CLI skeleton only
- No diff logic implemented yet
- Output schema is FIXED and compliant
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


SCHEMA_VERSION = "0.1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare HTML/Markdown answer.md and emit observation result (observation only)."
    )
    parser.add_argument(
        "--html-input",
        required=True,
        help="HTML-based answer.md root (zip file or directory)",
    )
    parser.add_argument(
        "--markdown-input",
        required=True,
        help="Markdown-based answer.md root (zip file or directory)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for observation result",
    )
    return parser.parse_args()


def ensure_output_dir(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)


def generate_empty_observation_result() -> dict:
    """
    Generate an empty-but-valid ObservationResult root object.

    NOTE:
    - observations is intentionally empty
    - This is valid for v0.1
    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "observations": [],
    }


def write_observation_result(output_dir: Path, result: dict) -> None:
    json_path = output_dir / "observation_result.json"
    md_path = output_dir / "observation_summary.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Answer Diff Observation Summary\n\n")
        f.write("- No observations generated (skeleton run)\n")


def main() -> int:
    args = parse_args()

    html_input = Path(args.html_input)
    md_input = Path(args.markdown_input)
    output_dir = Path(args.output)

    # NOTE:
    # zip / directory handling is intentionally NOT implemented yet.
    # This skeleton only validates CLI + output contract.
    if not html_input.exists():
        print(f"[ERROR] html-input not found: {html_input}", file=sys.stderr)
        return 1

    if not md_input.exists():
        print(f"[ERROR] markdown-input not found: {md_input}", file=sys.stderr)
        return 1

    ensure_output_dir(output_dir)

    result = generate_empty_observation_result()
    write_observation_result(output_dir, result)

    print("[OK] Observation skeleton executed successfully.")
    print(f"     Output: {output_dir / 'observation_result.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
