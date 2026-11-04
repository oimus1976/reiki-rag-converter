#!/usr/bin/env python
# observation_log_q2.py
#
# Phase 3.5 Observation Log (Q2 / S1) CLI.
#
# 正本仕様:
#   docs/eval/log_schema/Phase_3_5_Observation_Log_Schema_Q2_v0.1.md
#
# 責務（本スクリプトが行うこと）:
#   - validate : JSON 正本ログのスキーマ検証・命名規約検証
#   - summarize: JSON 正本ログ（run 単位）から observation_summary_<run_id>.csv を生成
#   - render-md: JSON 正本ログから人間レビュー用 Markdown を生成
#
# 本スクリプトが行わないこと:
#   - 観測値の解釈・判断・スコアリング
#   - 表記揺れの正規化
#   - 回答生成・観測ログ（実行データ）の作成
#
# CSV / Markdown は JSON の派生であり、正本ではない。

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Schema constants (schema v0.1 §1–§7)
# ---------------------------------------------------------------------------

PHASE = "3.5"
SCENARIO = "S1"
QUESTION_ID = "Q-S1-02"

MODE_A = "A_md"
MODE_B = "B_md_csv"
MODES = (MODE_A, MODE_B)

# §4.2.4: csv_used は mode により決まる（A=false / B=true）
CSV_USED_BY_MODE = {MODE_A: False, MODE_B: True}

# §4.2.2: Q2 固定の期待値
EXPECTED_ROWS = (
    "工事又は製造の請負",
    "財産の買入れ",
    "物件の借入れ",
    "財産の売払い",
    "前各号以外",
)

SOURCES = ("markdown", "csv", "none")
EXTRACTION_STATUSES = ("none", "partial", "success")

# §7: 判断語（例として列挙されている語）
JUDGMENT_WORDS = ("正しい", "誤り", "適切", "不適切", "合格", "不合格")

# §2.1: p35_<YYYYMMDD>_<ordinance_id>_<scenario>_<seq>
RUN_ID_RE = re.compile(r"^p35_(?P<date>\d{8})_(?P<ordinance_id>.+)_(?P<scenario>S1)_(?P<seq>\d+)$")

# §2.3: observation_<run_id>_<mode>.<ext>
OBSERVATION_FILE_RE = re.compile(
    r"^observation_(?P<run_id>p35_.+)_(?P<mode>A_md|B_md_csv)\.(?P<ext>json|md)$"
)

# §5.2
CSV_COLUMNS = (
    "run_id",
    "mode",
    "category",
    "amount_present",
    "source",
    "missing_category",
    "mixed_category",
    "representative_value_bias",
)

# Field specs: key -> (expected type tag, required)
ROOT_FIELDS = {
    "schema_version": ("string", True),
    "phase": ("string", True),
    "run_id": ("string", True),
    "scenario": ("string", True),
    "question_id": ("string", True),
    "ordinance_id": ("string", True),
    "mode": ("string", True),
    "answer_text": ("string", True),
    "table_expectation": ("object", True),
    "table_observation": ("array", True),
    "reference_behavior": ("object", True),
    "observations": ("object", True),
    "meta": ("object", False),
}

TABLE_EXPECTATION_FIELDS = {
    "expected_rows": ("array[string]", True),
}

TABLE_OBSERVATION_FIELDS = {
    "category": ("string", True),
    "amount_present": ("boolean", True),
    "amount_value": ("string|null", False),
    "source": ("string", True),
    "notes": ("string", False),
}

REFERENCE_BEHAVIOR_FIELDS = {
    "mentions_table": ("boolean", True),
    "mentions_article": ("array[string]", False),
    "csv_used": ("boolean", True),
    "extraction_status": ("string", True),
}

OBSERVATIONS_FIELDS = {
    "missing_category": ("boolean", True),
    "mixed_category": ("boolean", True),
    "representative_value_bias": ("boolean", True),
}

META_FIELDS = {
    "observer": ("string", False),
    "notes": ("string", False),
}


class ObservationLogError(Exception):
    """Raised when one or more schema / naming violations are found."""

    def __init__(self, errors: list[str]):
        self.errors = list(errors)
        super().__init__("\n".join(self.errors))


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _type_ok(value: Any, tag: str) -> bool:
    if tag == "string":
        return isinstance(value, str)
    if tag == "boolean":
        # bool は int のサブクラスではなく、厳密に bool のみ許容する
        return isinstance(value, bool)
    if tag == "object":
        return isinstance(value, dict)
    if tag == "array":
        return isinstance(value, list)
    if tag == "array[string]":
        return isinstance(value, list) and all(isinstance(v, str) for v in value)
    if tag == "string|null":
        return value is None or isinstance(value, str)
    raise ValueError(f"unknown type tag: {tag}")


def _check_fields(obj: dict, spec: dict, path: str, errors: list[str]) -> None:
    for key, (tag, required) in spec.items():
        if key not in obj:
            if required:
                errors.append(f"{path}.{key}: required field is missing")
            continue
        if not _type_ok(obj[key], tag):
            errors.append(
                f"{path}.{key}: expected {tag}, got {type(obj[key]).__name__}"
            )
    for key in obj:
        if key not in spec:
            errors.append(f"{path}.{key}: field is not defined in schema v0.1")


def _check_judgment_words(text: str, path: str, errors: list[str]) -> None:
    found = [w for w in JUDGMENT_WORDS if w in text]
    if found:
        errors.append(f"{path}: contains prohibited judgment word(s): {', '.join(found)}")


def parse_run_id(run_id: str) -> dict[str, str] | None:
    """Return run_id components, or None if it does not follow §2.1."""
    m = RUN_ID_RE.match(run_id)
    if not m:
        return None
    try:
        datetime.strptime(m.group("date"), "%Y%m%d")
    except ValueError:
        return None
    return m.groupdict()


def observation_filename(run_id: str, mode: str, ext: str) -> str:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}: {mode!r}")
    if ext not in ("json", "md"):
        raise ValueError(f"ext must be 'json' or 'md': {ext!r}")
    return f"observation_{run_id}_{mode}.{ext}"


def summary_filename(run_id: str) -> str:
    return f"observation_summary_{run_id}.csv"


def validate_observation(data: Any) -> list[str]:
    """Validate a JSON observation log object against schema v0.1.

    Returns a list of violation messages (empty list means no violation).
    """
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["$: root must be an object"]

    _check_fields(data, ROOT_FIELDS, "$", errors)

    # --- fixed values ------------------------------------------------------
    if isinstance(data.get("schema_version"), str) and not data["schema_version"]:
        errors.append("$.schema_version: must be a non-empty string")
    if isinstance(data.get("phase"), str) and data["phase"] != PHASE:
        errors.append(f"$.phase: must be {PHASE!r}, got {data['phase']!r}")
    if isinstance(data.get("scenario"), str) and data["scenario"] != SCENARIO:
        errors.append(f"$.scenario: must be {SCENARIO!r}, got {data['scenario']!r}")
    if isinstance(data.get("question_id"), str) and data["question_id"] != QUESTION_ID:
        errors.append(
            f"$.question_id: must be {QUESTION_ID!r}, got {data['question_id']!r}"
        )
    if isinstance(data.get("ordinance_id"), str) and not data["ordinance_id"]:
        errors.append("$.ordinance_id: must be a non-empty string")

    mode = data.get("mode")
    mode_valid = isinstance(mode, str) and mode in MODES
    if isinstance(mode, str) and not mode_valid:
        errors.append(f"$.mode: must be one of {list(MODES)}, got {mode!r}")

    # --- run_id naming convention (§2.1) -----------------------------------
    run_id = data.get("run_id")
    if isinstance(run_id, str):
        parts = parse_run_id(run_id)
        if parts is None:
            errors.append(
                "$.run_id: must follow p35_<YYYYMMDD>_<ordinance_id>_S1_<seq>, "
                f"got {run_id!r}"
            )
        elif isinstance(data.get("ordinance_id"), str) and parts["ordinance_id"] != data["ordinance_id"]:
            errors.append(
                f"$.run_id: ordinance_id part {parts['ordinance_id']!r} "
                f"does not match $.ordinance_id {data['ordinance_id']!r}"
            )

    # --- table_expectation (§4.2.2) ----------------------------------------
    expected_rows: list[str] | None = None
    te = data.get("table_expectation")
    if isinstance(te, dict):
        _check_fields(te, TABLE_EXPECTATION_FIELDS, "$.table_expectation", errors)
        rows = te.get("expected_rows")
        if _type_ok(rows, "array[string]"):
            if tuple(rows) != EXPECTED_ROWS:
                errors.append(
                    "$.table_expectation.expected_rows: must equal the Q2 fixed "
                    f"expected rows {list(EXPECTED_ROWS)}, got {rows}"
                )
            else:
                expected_rows = list(rows)

    # --- table_observation (§4.2.3) ----------------------------------------
    to = data.get("table_observation")
    if isinstance(to, list):
        seen: list[str] = []
        for i, item in enumerate(to):
            p = f"$.table_observation[{i}]"
            if not isinstance(item, dict):
                errors.append(f"{p}: must be an object")
                continue
            _check_fields(item, TABLE_OBSERVATION_FIELDS, p, errors)
            cat = item.get("category")
            if isinstance(cat, str):
                if cat not in EXPECTED_ROWS:
                    errors.append(
                        f"{p}.category: {cat!r} is not an element of expected_rows"
                    )
                elif cat in seen:
                    errors.append(f"{p}.category: duplicated category {cat!r}")
                seen.append(cat)
            src = item.get("source")
            if isinstance(src, str) and src not in SOURCES:
                errors.append(f"{p}.source: must be one of {list(SOURCES)}, got {src!r}")
            if isinstance(item.get("notes"), str):
                _check_judgment_words(item["notes"], f"{p}.notes", errors)
        if expected_rows is not None:
            missing = [r for r in expected_rows if r not in seen]
            if missing:
                errors.append(
                    "$.table_observation: one element per category is required; "
                    f"missing categories {missing}"
                )

    # --- reference_behavior (§4.2.4) ---------------------------------------
    rb = data.get("reference_behavior")
    if isinstance(rb, dict):
        _check_fields(rb, REFERENCE_BEHAVIOR_FIELDS, "$.reference_behavior", errors)
        status = rb.get("extraction_status")
        if isinstance(status, str) and status not in EXTRACTION_STATUSES:
            errors.append(
                "$.reference_behavior.extraction_status: must be one of "
                f"{list(EXTRACTION_STATUSES)}, got {status!r}"
            )
        csv_used = rb.get("csv_used")
        if mode_valid and isinstance(csv_used, bool) and csv_used != CSV_USED_BY_MODE[mode]:
            errors.append(
                f"$.reference_behavior.csv_used: must be "
                f"{str(CSV_USED_BY_MODE[mode]).lower()} for mode {mode!r}"
            )

    # --- observations (§4.2.5) ---------------------------------------------
    ob = data.get("observations")
    if isinstance(ob, dict):
        _check_fields(ob, OBSERVATIONS_FIELDS, "$.observations", errors)

    # --- meta (§4.2.6) -----------------------------------------------------
    meta = data.get("meta")
    if isinstance(meta, dict):
        _check_fields(meta, META_FIELDS, "$.meta", errors)
        if isinstance(meta.get("notes"), str):
            _check_judgment_words(meta["notes"], "$.meta.notes", errors)

    return errors


def validate_filename(path: Path, data: Any) -> list[str]:
    """Check that the JSON file name follows §2.3 and matches its content."""
    errors: list[str] = []
    m = OBSERVATION_FILE_RE.match(path.name)
    if not m or m.group("ext") != "json":
        return [
            f"{path.name}: file name must follow observation_<run_id>_<mode>.json"
        ]
    if isinstance(data, dict):
        if data.get("run_id") != m.group("run_id"):
            errors.append(
                f"{path.name}: run_id in file name {m.group('run_id')!r} "
                f"does not match $.run_id {data.get('run_id')!r}"
            )
        if data.get("mode") != m.group("mode"):
            errors.append(
                f"{path.name}: mode in file name {m.group('mode')!r} "
                f"does not match $.mode {data.get('mode')!r}"
            )
    return errors


def load_observation(path: Path) -> dict:
    """Load and fully validate one JSON observation log file.

    Raises ObservationLogError on any violation.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ObservationLogError([f"{path.name}: invalid JSON: {e}"]) from e
    errors = validate_filename(path, data) + [
        f"{path.name}: {msg}" for msg in validate_observation(data)
    ]
    if errors:
        raise ObservationLogError(errors)
    return data


# ---------------------------------------------------------------------------
# CSV summary (§5)
# ---------------------------------------------------------------------------


def _bool_str(v: bool) -> str:
    return "true" if v else "false"


def build_summary_rows(observations: list[dict]) -> list[dict[str, str]]:
    """Build CSV rows from validated observation logs of a single run.

    Rows are ordered by mode (A_md, B_md_csv), then by table_observation order.
    """
    run_ids = {o["run_id"] for o in observations}
    if len(run_ids) != 1:
        raise ObservationLogError(
            [f"all observation logs must share one run_id, got {sorted(run_ids)}"]
        )
    modes = [o["mode"] for o in observations]
    dup = sorted({m for m in modes if modes.count(m) > 1})
    if dup:
        raise ObservationLogError(
            [f"one file per mode is allowed in a run; duplicated mode(s) {dup}"]
        )

    rows: list[dict[str, str]] = []
    for obs in sorted(observations, key=lambda o: MODES.index(o["mode"])):
        flags = obs["observations"]
        for item in obs["table_observation"]:
            rows.append(
                {
                    "run_id": obs["run_id"],
                    "mode": obs["mode"],
                    "category": item["category"],
                    "amount_present": _bool_str(item["amount_present"]),
                    "source": item["source"],
                    "missing_category": _bool_str(flags["missing_category"]),
                    "mixed_category": _bool_str(flags["mixed_category"]),
                    "representative_value_bias": _bool_str(
                        flags["representative_value_bias"]
                    ),
                }
            )
    return rows


def write_summary_csv(observations: list[dict], out_dir: Path) -> Path:
    rows = build_summary_rows(observations)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / summary_filename(observations[0]["run_id"])
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return out_path


# ---------------------------------------------------------------------------
# Markdown review log (§6)
# ---------------------------------------------------------------------------


def _md_cell(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\r\n", "<br>").replace("\n", "<br>")


def _blockquote(text: str) -> str:
    lines = text.splitlines() or [""]
    return "\n".join(f"> {line}" if line else ">" for line in lines)


def render_markdown(obs: dict, question_text: str) -> str:
    """Render a human review Markdown from one validated observation log."""
    flags = obs["observations"]
    rb = obs["reference_behavior"]

    lines: list[str] = [
        "---",
        f"run_id: {obs['run_id']}",
        f"question_id: {obs['question_id']}",
        f"mode: {obs['mode']}",
        "---",
        "",
        f"# Observation {obs['run_id']} ({obs['mode']})",
        "",
        "## 質問本文（Q2）",
        "",
        question_text.strip("\n"),
        "",
        "## 回答原文",
        "",
        _blockquote(obs["answer_text"]),
        "",
        "## 区分別テーブル",
        "",
        "| 区分 | 金額提示 | 情報源 | メモ |",
        "| --- | --- | --- | --- |",
    ]
    for item in obs["table_observation"]:
        lines.append(
            "| {cat} | {present} | {src} | {notes} |".format(
                cat=_md_cell(item["category"]),
                present=_bool_str(item["amount_present"]),
                src=item["source"],
                notes=_md_cell(item.get("notes") or ""),
            )
        )
    lines += [
        "",
        "## 観測サマリ",
        "",
        f"- 欠落（missing_category）: {_bool_str(flags['missing_category'])}",
        f"- 混在（mixed_category）: {_bool_str(flags['mixed_category'])}",
        "- 代表値引きずり（representative_value_bias）: "
        f"{_bool_str(flags['representative_value_bias'])}",
        f"- 表参照（mentions_table）: {_bool_str(rb['mentions_table'])}",
        "",
    ]
    return "\n".join(lines)


def write_markdown(obs: dict, question_text: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / observation_filename(obs["run_id"], obs["mode"], "md")
    out_path.write_text(render_markdown(obs, question_text), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _load_all(paths: list[Path]) -> list[dict]:
    errors: list[str] = []
    loaded: list[dict] = []
    for p in paths:
        try:
            loaded.append(load_observation(p))
        except ObservationLogError as e:
            errors.extend(e.errors)
        except OSError as e:
            errors.append(f"{p}: cannot read file: {e}")
    if errors:
        raise ObservationLogError(errors)
    return loaded


def cmd_validate(args: argparse.Namespace) -> int:
    _load_all(args.json_files)
    for p in args.json_files:
        print(f"OK: {p}")
    return 0


def cmd_summarize(args: argparse.Namespace) -> int:
    loaded = _load_all(args.json_files)
    out = write_summary_csv(loaded, args.out_dir)
    print(f"wrote: {out}")
    return 0


def cmd_render_md(args: argparse.Namespace) -> int:
    question_text = args.question_file.read_text(encoding="utf-8")
    if not question_text.strip():
        raise ObservationLogError([f"{args.question_file}: question text is empty"])
    loaded = _load_all(args.json_files)
    for obs in loaded:
        out = write_markdown(obs, question_text, args.out_dir)
        print(f"wrote: {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Phase 3.5 Observation Log (Q2 / S1) tool: validate JSON logs, "
            "derive summary CSV and review Markdown "
            "(schema: docs/eval/log_schema/Phase_3_5_Observation_Log_Schema_Q2_v0.1.md)"
        )
    )
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate", help="validate JSON observation logs")
    v.add_argument("json_files", nargs="+", type=Path)
    v.set_defaults(func=cmd_validate)

    s = sub.add_parser(
        "summarize", help="generate observation_summary_<run_id>.csv from JSON logs of one run"
    )
    s.add_argument("json_files", nargs="+", type=Path)
    s.add_argument("--out-dir", required=True, type=Path)
    s.set_defaults(func=cmd_summarize)

    r = sub.add_parser(
        "render-md", help="generate observation_<run_id>_<mode>.md from JSON logs"
    )
    r.add_argument("json_files", nargs="+", type=Path)
    r.add_argument(
        "--question-file",
        required=True,
        type=Path,
        help="UTF-8 text file holding the Q2 question text (not part of the JSON schema)",
    )
    r.add_argument("--out-dir", required=True, type=Path)
    r.set_defaults(func=cmd_render_md)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ObservationLogError as e:
        for msg in e.errors:
            print(f"ERROR: {msg}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
