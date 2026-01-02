# tests/customized_question_set/test_concretizer.py

from customized_question_set.concretizer import concretize_questions
from customized_question_set.ordinance_structure import (
    OrdinanceArticle,
    OrdinanceParagraph,
    OrdinanceStructure,
)
from customized_question_set.types import GoldenQuestionTemplate


def _structure_for_test():
    # Article 1: no paragraphs
    a1 = OrdinanceArticle(index=1, element_id="a1", paragraphs=[])
    # Article 2: has 2 paragraphs
    a2 = OrdinanceArticle(
        index=2,
        element_id="a2",
        paragraphs=[
            OrdinanceParagraph(index=1, element_id="p21"),
            OrdinanceParagraph(index=2, element_id="p22"),
        ],
    )
    # Article 3: has 1 paragraph
    a3 = OrdinanceArticle(
        index=3,
        element_id="a3",
        paragraphs=[OrdinanceParagraph(index=1, element_id="p31")],
    )

    return OrdinanceStructure(
        has_articles=True,
        has_paragraphs=True,
        has_supplementary=False,
        articles=[a1, a2, a3],
        first_article=a1,
        first_paragraph=None,
    )


def test_concretize_article_only_q3_positions():
    st = _structure_for_test()
    templates = [
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条の内容を要約してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        )
    ]

    qs = concretize_questions(templates, st, source_golden_question_pool="A")
    # n=3 -> positions [1,2,3] (unique)
    assert [q.text for q in qs] == [
        "第1条の内容を要約してください。",
        "第2条の内容を要約してください。",
        "第3条の内容を要約してください。",
    ]


def test_concretize_relation_q12_pairs():
    st = _structure_for_test()
    templates = [
        GoldenQuestionTemplate(
            template_id="Q12",
            text="第○条と第○条の関係性を説明してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        )
    ]
    qs = concretize_questions(templates, st, source_golden_question_pool="A")
    # n=3 -> pairs (1,3) and (1,2)
    assert [q.text for q in qs] == [
        "第1条と第3条の関係性を説明してください。",
        "第1条と第2条の関係性を説明してください。",
    ]


def test_concretize_article_paragraph_q4_with_safety():
    st = _structure_for_test()
    # Force selection to hit article 1 (no paragraphs) as part of [1,2,3], but still should generate from others
    templates = [
        GoldenQuestionTemplate(
            template_id="Q4",
            text="第○条第○項の内容を説明してください。",
            requires_article=True,
            requires_paragraph=True,
            requires_supplementary=False,
        )
    ]
    qs = concretize_questions(templates, st, source_golden_question_pool="A")
    # For a2: paragraphs [1,2] => 2 questions; for a3: [1] => 1 question; a1 => 0
    assert "第2条第1項の内容を説明してください。" in [q.text for q in qs]
    assert "第2条第2項の内容を説明してください。" in [q.text for q in qs]
    assert "第3条第1項の内容を説明してください。" in [q.text for q in qs]
    assert len(qs) >= 3


def test_structural_exclusion_only_when_impossible():
    # No articles at all -> requires_article templates excluded
    st = OrdinanceStructure(
        has_articles=False,
        has_paragraphs=False,
        has_supplementary=False,
        articles=[],
        first_article=None,
        first_paragraph=None,
    )
    templates = [
        GoldenQuestionTemplate(
            template_id="Q1",
            text="この条例の目的を分かりやすく説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条の内容を要約してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
    ]
    qs = concretize_questions(templates, st, source_golden_question_pool="A")
    assert len(qs) == 1
    assert qs[0].text == "この条例の目的を分かりやすく説明してください。"


def test_deterministic_order_and_ids():
    st = _structure_for_test()
    templates = [
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条の内容を要約してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q12",
            text="第○条と第○条の関係性を説明してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
    ]
    qs1 = concretize_questions(templates, st, source_golden_question_pool="A")
    qs2 = concretize_questions(templates, st, source_golden_question_pool="A")
    assert [q.question_id for q in qs1] == [q.question_id for q in qs2]
    assert [q.text for q in qs1] == [q.text for q in qs2]
