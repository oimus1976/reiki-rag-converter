"""
CLI entrypoint for customized_question_set generator.

Responsibility:
- Parse CLI arguments
- Validate input/output paths
- Delegate execution to generator (no business logic)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from reiki_rag_customized_question_set.generator import generate_customized_question_set

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="customized-question-set-generator",
        description=(
            "Generate a deterministic customized_question_set.json "
            "from ordinance HTML and Golden Question Pool."
        ),
    )

    parser.add_argument(
        "--ordinance-html",
        required=True,
        type=Path,
        help="Path to ordinance HTML file (e.g. k518RG00000022.html)",
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output directory for customized_question_set.json",
    )

    parser.add_argument(
        "--question-pool",
        required=True,
        help=(
            "Source Golden Question Pool identifier "
            "(e.g. GQPA:v1.1). "
            "Passed through without interpretation."
        ),
    )

    # cli.py（要点のみ）

    parser.add_argument(
        "--schema-version",
        required=True,
        help="Schema version of customized_question_set (e.g. 1.0)",
    )

    parser.add_argument(
        "--question-set-id",
        required=True,
        help="Deterministic question_set_id (precomputed)",
    )

    parser.add_argument(
        "--target-ordinance-id",
        required=True,
        help="Target ordinance ID (e.g. k518RG00000022)",
    )


    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    ordinance_html: Path = args.ordinance_html
    output_dir: Path = args.output

    # --- minimal validation (no interpretation) ---
    if not ordinance_html.exists():
        parser.error(f"ordinance HTML not found: {ordinance_html}")

    if not ordinance_html.is_file():
        parser.error(f"ordinance HTML is not a file: {ordinance_html}")

    output_dir.mkdir(parents=True, exist_ok=True)

    # --- delegate to generator ---
    html_text = ordinance_html.read_text(encoding="utf-8")

    generate_customized_question_set(
        html=html_text,
        target_ordinance_id=args.target_ordinance_id,
        source_golden_question_pool=args.question_pool,
        question_set_id=args.question_set_id,
        schema_version=args.schema_version,
        output_path=output_dir / "customized_question_set.json",
    )


    print(f"[OK] customized_question_set generated at: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
