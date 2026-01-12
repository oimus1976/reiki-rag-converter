#!/usr/bin/env python3
"""
Run reiki_rag_customized_question_set CLI for multiple ordinances.

Default behavior:
- Scan data/ directory
- Pick ordinance HTMLs by pattern (default: k*.html)
- Derive ordinance_id from filename
- Run CLI for each ordinance_id
- Write a run manifest for reproducibility

This script is intended for user-test / batch verification.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Batch run customized_question_set generation for ordinances in data/"
    )

    p.add_argument(
        "--pattern",
        default="k*.html",
        help="Glob pattern to select ordinance HTML files under data/ (default: k*.html)",
    )

    p.add_argument(
        "--output-root",
        default="artifacts/user_test",
        help="Root directory for outputs (default: artifacts/user_test)",
    )

    p.add_argument(
        "--schema-version",
        required=True,
        help="schema_version passed to reiki_rag_customized_question_set.cli",
    )

    p.add_argument(
        "--question-pool",
        required=True,
        help="Golden Question Pool version (e.g. GQPA:v1.1)",
    )

    p.add_argument(
        "--question-set-id-template",
        default="customized_question_set:{ordinance_id}:v1",
        help=(
            "Template for question_set_id. "
            "Use {ordinance_id} placeholder. "
            "(default: customized_question_set:{ordinance_id}:v1)"
        ),
    )

    p.add_argument(
        "--write-manifest",
        action="store_true",
        default=True,
        help="Write run manifest to output-root/_run_manifest.txt (default: on)",
    )

    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing",
    )

    return p.parse_args()


def collect_ordinance_ids(pattern: str) -> list[str]:
    if not DATA_DIR.exists():
        raise RuntimeError(f"data/ directory not found: {DATA_DIR}")

    paths = sorted(DATA_DIR.glob(pattern))

    if not paths:
        raise RuntimeError(f"No files matched pattern '{pattern}' in data/")

    ids: list[str] = []
    for p in paths:
        if p.suffix.lower() != ".html":
            continue
        ids.append(p.stem)

    if not ids:
        raise RuntimeError("No ordinance IDs extracted from matched files")

    return ids


def run_one(
    ordinance_id: str,
    args: argparse.Namespace,
    output_root: Path,
) -> None:
    ordinance_html = DATA_DIR / f"{ordinance_id}.html"
    output_dir = output_root / ordinance_id

    question_set_id = args.question_set_id_template.format(
        ordinance_id=ordinance_id
    )

    cmd = [
        sys.executable,
        "-m",
        "reiki_rag_customized_question_set.cli",
        "--ordinance-html",
        str(ordinance_html),
        "--output",
        str(output_dir),
        "--schema-version",
        args.schema_version,
        "--target-ordinance-id",
        ordinance_id,
        "--question-set-id",
        question_set_id,
        "--question-pool",
        args.question_pool,
    ]

    print(f"[RUN] {ordinance_id}")
    print(" ".join(cmd))

    if args.dry_run:
        return

    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"Generation failed for ordinance_id={ordinance_id}")


def write_manifest(
    output_root: Path,
    ordinance_ids: list[str],
    args: argparse.Namespace,
) -> None:
    ts = datetime.now(timezone.utc).isoformat()

    lines = [
        "# customized_question_set user test run manifest",
        f"timestamp: {ts}",
        f"data_dir: {DATA_DIR}",
        f"pattern: {args.pattern}",
        f"schema_version: {args.schema_version}",
        f"question_pool: {args.question_pool}",
        f"question_set_id_template: {args.question_set_id_template}",
        "",
        "ordinance_ids:",
    ]

    for oid in ordinance_ids:
        lines.append(f"  - {oid}")

    manifest_path = output_root / "_run_manifest.txt"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()

    ordinance_ids = collect_ordinance_ids(args.pattern)
    output_root = PROJECT_ROOT / args.output_root
    output_root.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Found {len(ordinance_ids)} ordinances")
    for oid in ordinance_ids:
        run_one(oid, args, output_root)

    if args.write_manifest:
        write_manifest(output_root, ordinance_ids, args)
        print(f"[INFO] Manifest written to {output_root / '_run_manifest.txt'}")

    print("[OK] Batch generation completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
