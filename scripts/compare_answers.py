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

import zipfile
import tempfile
import shutil

import re



@dataclass(frozen=True)
class AnswerEntry:
    ordinance_id: str
    question_id: str
    path: Path

def compute_structural_metrics(text: str) -> dict:
    """
    Structural metrics v0.1
    - heading_count
    - list_item_count
    - has_supplementary
    """
    heading_count = 0
    list_item_count = 0
    has_supplementary = False

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        # 見出し検出（Spec 9.2）
        if (
            stripped.startswith("#")
            or stripped.startswith("附則")
            or stripped.startswith("第")
        ):
            heading_count += 1

        # 箇条書き検出（Spec 9.3）
        if (
            stripped.startswith("- ")
            or stripped.startswith("* ")
            or stripped.startswith("+ ")
            or re.match(r"\d+\.\s+", stripped)
        ):
            list_item_count += 1

        # 附則セクション検出（Spec 9.4）
        if stripped.startswith("附則"):
            has_supplementary = True

    return {
        "heading_count": heading_count,
        "list_item_count": list_item_count,
        "has_supplementary": has_supplementary,
    }

def compute_structural_diff(html_text: str, md_text: str) -> bool:
    html_struct = compute_structural_metrics(html_text)
    md_struct = compute_structural_metrics(md_text)

    return html_struct != md_struct

def compute_volume_metrics(text: str) -> dict:
    # chars: Unicode code points
    chars = len(text)

    # lines: splitlines() は末尾改行の過剰カウントを避ける
    lines = len(text.splitlines())

    # paragraphs: 空行区切りの非空行ブロック
    count = 0
    in_block = False
    for line in text.splitlines():
        if line.strip() == "":
            if in_block:
                count += 1
                in_block = False
        else:
            in_block = True
    if in_block:
        count += 1

    return {
        "chars": chars,
        "lines": lines,
        "paragraphs": count,
    }


def prepare_input_root(input_path: Path) -> Path:
    """
    Prepare input root directory.

    - If input_path is a directory: return as-is
    - If input_path is a zip file: extract to a temporary directory and return it

    Caller is responsible for cleanup if needed.
    """
    if input_path.is_dir():
        return input_path

    if input_path.is_file() and input_path.suffix.lower() == ".zip":
        tmpdir = Path(tempfile.mkdtemp(prefix="compare_answers_"))
        with zipfile.ZipFile(input_path, "r") as zf:
            zf.extractall(tmpdir)
        return tmpdir

    raise ValueError(f"Unsupported input type: {input_path}")


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

ARTICLE_RE = re.compile(r"第[一二三四五六七八九十百千万0-9]+条")
PARAGRAPH_RE = re.compile(r"第[一二三四五六七八九十百千万0-9]+項")
SUPPLEMENTARY_RE = re.compile(r"附則")


def extract_references(text: str) -> dict[str, set[str]]:
    """
    Extract legal references from answer text.
    """
    return {
        "article": set(ARTICLE_RE.findall(text)),
        "paragraph": set(PARAGRAPH_RE.findall(text)),
        "supplementary": set(SUPPLEMENTARY_RE.findall(text)),
    }

def compute_reference_diff(
    html_text: str, md_text: str
) -> dict[str, dict[str, list[str]]]:
    """
    Compute reference diff between html and markdown answers.
    """
    html_refs = extract_references(html_text)
    md_refs = extract_references(md_text)

    diff: dict[str, dict[str, list[str]]] = {}

    for key in ["article", "paragraph", "supplementary"]:
        only_html = sorted(html_refs[key] - md_refs[key])
        only_md = sorted(md_refs[key] - html_refs[key])

        if only_html or only_md:
            diff[key] = {}
            if only_html:
                diff[key]["only_in_html"] = only_html
            if only_md:
                diff[key]["only_in_markdown"] = only_md

    return diff

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

        f.write(
            "## Observation Summary の位置づけ\n\n"
            "本ドキュメントおよび `observation_result.json` は、\n"
            "HTML 版 answer.md と Markdown 版 answer.md の差分を、\n"
            "**評価や解釈を行わず、観測事実として固定する**ことを目的とします。\n\n"
            "本フェーズでは、差分の有無や量を機械的に記録するに留め、\n"
            "それらの良否・適切性・意味付けは行いません。\n"
            "観測結果の解釈および評価は、Evaluation Framework 側の責務とします。\n\n"
        )

        f.write(
            "## 入力と出力\n\n"
            "- 入力：HTML 版 answer.md（zip / directory）\n"
            "- 入力：Markdown 版 answer.md（zip / directory）\n"
            "- 出力：`observation_result.json`（観測結果の正本）\n"
            "- 出力：`observation_summary.md`（本ドキュメント）\n\n"
        )

        f.write(
            "## 観測対象と Diff の種類（v0.1）\n\n"
            "本フェーズでは、以下 3 種類の Diff を観測対象とします。\n\n"
            "### Reference Diff（参照差）\n\n"
            "- 条（第○条）\n"
            "- 項（第○項）\n"
            "- 附則\n\n"
            "について、**出現有無のみ**を観測します。\n"
            "文章内容の言い換え、要約、説明粒度の違いは対象外です。\n\n"
            "### Volume Diff（情報量差）\n\n"
            "HTML 版と Markdown 版の間で、**文章量の差を定量的に観測**します。\n\n"
            "### Structural Diff（構造差）\n\n"
            "Structural Diff では、回答中に含まれる以下の構造要素について、\n"
            "HTML 版と Markdown 版の **一致／不一致のみ**を判定します。\n\n"
            "- 見出し行\n"
            "- 箇条書き項目\n"
            "- 附則の有無\n\n"
            "v0.1 では、構造要素の個数や内訳は記録せず、\n"
            "構造が同一かどうかの boolean 値のみを観測結果として出力します。\n\n"
        )

        f.write(
            "## Volume Diff（情報量差）について\n\n"
            "### 観測指標（v0.1）\n\n"
            "- **chars**  \n"
            "  回答全文の文字数（Unicode コードポイント数）\n\n"
            "- **lines**  \n"
            "  改行（\\n）で区切った行数\n\n"
            "- **paragraphs**  \n"
            "  空行で区切られた、1 行以上の非空行ブロック数  \n"
            "  （見出し・本文・箇条書き等の構文的区別は行いません）\n\n"
        )

        f.write(
            "## Structural Diff v0.1 に関する注意点\n\n"
            "Structural Diff v0.1 は、観測対象データセットの特性上、\n"
            "**すべての回答で差が検出される場合があります**。\n\n"
            "これは以下の理由によるものであり、異常や実装不備を示すものではありません。\n\n"
            "- Markdown 版には、章サマリや見出し構造が含まれる\n"
            "- HTML 版では、これらが平文化されている場合がある\n"
            "- 本 Diff は「差の有無」のみを判定する設計である\n\n"
            "差の種類や程度を分析することは、v0.2 以降、または Evaluation フェーズで扱う課題とします。\n\n"
        )

        f.write(
            "## 本フェーズの完了条件\n\n"
            "- 全 AnswerPair について ObservationResult が生成されている\n"
            "- Reference / Volume / Structural の各 Diff が算出されている\n"
            "- 観測結果が JSON と Markdown の成果物として固定されている\n"
            "- 成果物に評価・判断を含む記述が存在しない\n"
        )

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
    html_root = prepare_input_root(html_input)
    md_root = prepare_input_root(md_input)

    html_entries = collect_answer_entries(html_root)
    md_entries = collect_answer_entries(md_root)


    pairs, errors = build_answer_pairs(html_entries, md_entries)

    observations = []

    for html_entry, md_entry in pairs:
        html_text = html_entry.path.read_text(encoding="utf-8")
        md_text = md_entry.path.read_text(encoding="utf-8")

        reference_diff = compute_reference_diff(html_text, md_text)

        html_metrics = compute_volume_metrics(html_text)
        md_metrics = compute_volume_metrics(md_text)
        volume_diff = (html_metrics != md_metrics)

        structural_diff = compute_structural_diff(html_text, md_text)

        observations.append(
            {
                "ordinance_id": html_entry.ordinance_id,
                "question_id": html_entry.question_id,
                "diff_flags": {
                    "structural_diff": structural_diff,
                    "reference_diff": bool(reference_diff),
                    "volume_diff": volume_diff,
                },
                "metrics": {
                    "html": html_metrics,
                    "markdown": md_metrics,
                },
                "details": {
                    "reference_diff": reference_diff,
                },
            }
        )

    # For now: just log counts (no observation yet)
    print(f"[INFO] HTML entries: {len(html_entries)}")
    print(f"[INFO] Markdown entries: {len(md_entries)}")
    print(f"[INFO] Matched AnswerPairs: {len(pairs)}")

    for err in errors:
        print(f"[WARN] {err}")

    ensure_output_dir(output_dir)

    result = generate_empty_observation_result()
    result["observations"] = observations

    write_observation_result(output_dir, result)

    print("[OK] Observation skeleton executed successfully.")
    print(f"     Output: {output_dir / 'observation_result.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
