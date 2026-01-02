from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import List

from customized_question_set.ordinance_structure import extract_ordinance_structure
from customized_question_set.concretizer import concretize_questions
from customized_question_set.types import GoldenQuestionTemplate
from customized_question_set.writer import write_customized_question_set
from customized_question_set.question_pool_a import load_golden_question_pool_a


def generate_customized_question_set(
    *,
    html: str,
    target_ordinance_id: str,
    source_golden_question_pool: str,
    question_set_id: str,
    schema_version: str,
    output_path: str | Path,
) -> None:
    """
    generator は接続層のみ。
    判断・補正・並び替え・ID生成は一切行わない。
    """

    # 1. 条例構造の事実抽出
    structure = extract_ordinance_structure(html)

    # 2. Golden Question Pool A の読み込み（そのまま）
    templates: List[GoldenQuestionTemplate] = load_golden_question_pool_a()

    # 3. 質問具体化（Coverage Policy v0.1.1 を内包）
    questions = concretize_questions(
        templates,
        structure,
        source_golden_question_pool=source_golden_question_pool,
    )

    # 4. JSON ルート（dict）を組み立てる（順序は writer に委譲）
    data = {
        "schema_version": schema_version,
        "question_set_id": question_set_id,
        "source_golden_question_pool": source_golden_question_pool,
        "target_ordinance_id": target_ordinance_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "questions": [
            {
                "question_id": q.question_id,
                "text": q.text,
                "source_template_id": q.source_template_id,
            }
            for q in questions
        ],
    }

    # 5. 決定的に書き出す
    write_customized_question_set(data, output_path)
