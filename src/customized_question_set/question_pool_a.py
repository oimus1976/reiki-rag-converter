from __future__ import annotations

from typing import List

from customized_question_set.types import GoldenQuestionTemplate


def load_golden_question_pool_a() -> List[GoldenQuestionTemplate]:
    """
    Golden Question Pool A（凍結資産）をそのまま返す。
    加工・並び替え・条件分岐は一切行わない。
    """

    return [
        GoldenQuestionTemplate(
            template_id="Q1",
            text="この条例の目的は何ですか。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条はどのような内容を定めていますか。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q4",
            text="第○条第○項では何を規定していますか。",
            requires_article=True,
            requires_paragraph=True,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q12",
            text="第○条と第○条の関係はどのようになっていますか。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
    ]
