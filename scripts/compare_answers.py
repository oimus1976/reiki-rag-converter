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

from dataclasses import dataclass
from typing import Dict, Tuple, List

@dataclass(frozen=True)
class AnswerEntry:
    ordinance_id: str
    question_id: str
    path: Path

def collect_answer_entries(root: Path) -> Dict[Tuple[str, str], AnswerEntry]:
    """
    Recursively scan root directory and collect answer entries.

    Spec v0.1 detection rule:
    - file name must be <question_id>_answer.md
    - parent directory name must equal <question_id>
    - parent's parent directory name is treated as <ordinance_id>
    """
    entries: Dict[Tuple[str, str], AnswerEntry] = {}

    for md_file in root.rglob("*_answer.md"):
        question_dir = md_file.parent
        question_id = question_dir.name

        expected_name = f"{question_id}_answer.md"
        if md_file.name != expected_name:
            continue

        ordinance_dir = question_dir.parent
        if ordinance_dir is None:
            continue

        ordinance_id = ordinance_dir.name
        key = (ordinance_id, question_id)

        if key not in entries:
            entries[key] = AnswerEntry(
                ordinance_id=ordinance_id,
                question_id=question_id,
                path=md_file,
            )

    return entries

def build_answer_pairs(
    html_entries: Dict[Tuple[str, str], AnswerEntry],
    md_entries: Dict[Tuple[str, str], AnswerEntry],
) -> Tuple[List[Tuple[AnswerEntry, AnswerEntry]], List[str]]:
    """
    Build AnswerPair candidates and collect missing-entry errors.
    """
    pairs: List[Tuple[AnswerEntry, AnswerEntry]] = []
    errors: List[str] = []

    html_keys = set(html_entries.keys())
    md_keys = set(md_entries.keys())

    common_keys = html_keys & md_keys
    missing_in_html = md_keys - html_keys
    missing_in_md = html_keys - md_keys

    for key in common_keys:
        pairs.append((html_entries[key], md_entries[key]))

    for ordinance_id, question_id in sorted(missing_in_html):
        errors.append(
            f"Missing HTML answer for ordinance={ordinance_id}, question={question_id}"
        )

    for ordinance_id, question_id in sorted(missing_in_md):
        errors.append(
            f"Missing Markdown answer for ordinance={ordinance_id}, question={question_id}"
        )

    # Deterministic ordering (Spec 10.3.4)
    pairs.sort(key=lambda p: (p[0].ordinance_id, p[0].question_id))

    return pairs, errors


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
    
    # Input scan (Spec v0.1 compliant)
    html_entries = collect_answer_entries(html_input)
    md_entries = collect_answer_entries(md_input)

    pairs, errors = build_answer_pairs(html_entries, md_entries)

    # For now: just log counts (no observation yet)
    print(f"[INFO] HTML entries: {len(html_entries)}")
    print(f"[INFO] Markdown entries: {len(md_entries)}")
    print(f"[INFO] Matched AnswerPairs: {len(pairs)}")

    for err in errors:
        print(f"[WARN] {err}")

    ensure_output_dir(output_dir)

    result = generate_empty_observation_result()
    write_observation_result(output_dir, result)

    print("[OK] Observation skeleton executed successfully.")
    print(f"     Output: {output_dir / 'observation_result.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
