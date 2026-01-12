# src/customized_question_set/types.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


# =========================
# Ordinance structure summary
# =========================

@dataclass(frozen=True)
class OrdinanceStructureSummary:
    """
    customized_question_set.json 用の構造サマリ。
    articles などの詳細構造は持たない。
    """
    has_articles: bool          # 条 が存在するか
    has_paragraphs: bool        # 項 が存在するか
    has_supplementary: bool     # 附則 が存在するか


# =========================
# Golden Question Pool
# =========================

@dataclass(frozen=True)
class GoldenQuestionTemplate:
    """
    Golden Question Pool から読み込んだ質問テンプレート。
    まだ具体化されていない状態。
    """
    template_id: str
    text: str                   # 例: 「第○条はどのような内容を定めていますか。」
    requires_article: bool      # 条 が必要か
    requires_paragraph: bool    # 項 が必要か
    requires_supplementary: bool  # 附則 が必要か


# =========================
# Skipped question
# =========================

@dataclass(frozen=True)
class SkippedQuestion:
    """
    extensions.skipped_questions に出力するスキップ理由。
    """
    source_template_id: str
    reason: str


# =========================
# Concrete question
# =========================

@dataclass(frozen=True)
class ConcreteQuestion:
    """
    条例構造に基づいて具体化された質問。
    最終的に customized_question_set.json の questions[] に入る単位。
    """
    question_id: str
    text: str
    source_template_id: str     # Golden Question Pool 側の template_id


# =========================
# Customized Question Set (internal model)
# =========================

@dataclass(frozen=True)
class CustomizedQuestionSet:
    """
    customized_question_set.json の内部表現。
    JSONとは完全一致させる必要はない（writerが責務を持つ）。
    """
    schema_version: str
    question_set_id: str
    source_golden_question_pool: str
    target_ordinance_id: str
    questions: List[ConcreteQuestion]
