# src/customized_question_set/writer.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


# ルートレベルのキー順はここで固定する
ROOT_KEY_ORDER = [
    "schema_version",
    "question_set_id",
    "source_golden_question_pool",
    "target_ordinance_id",
    "generated_at",
    "questions",
]


def _ordered_root(obj: Mapping[str, Any]) -> dict:
    """
    Root object のキー順を固定する。
    未定義キーが来た場合も後ろに付ける（破壊しない）
    """
    ordered: dict[str, Any] = {}

    for key in ROOT_KEY_ORDER:
        if key in obj:
            ordered[key] = obj[key]

    # 想定外キーがあっても捨てずに末尾へ
    for key, value in obj.items():
        if key not in ordered:
            ordered[key] = value

    return ordered


def write_customized_question_set(
    data: Mapping[str, Any],
    output_path: str | Path,
) -> None:
    """
    customized_question_set.json を
    ・キー順固定
    ・pretty
    ・UTF-8
    で決定的に書き出す
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    ordered_root = _ordered_root(data)

    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(
            ordered_root,
            f,
            ensure_ascii=False,
            indent=2,
            sort_keys=False,  # ← ここ重要
        )
        f.write("\n")  # 末尾改行を固定
