# tests/customized_question_set/test_invariant_execution_input.py

import pytest

from customized_question_set.concretizer import concretize_questions
from customized_question_set.types import GoldenQuestionTemplate
from customized_question_set.ordinance_structure import extract_ordinance_structure


def test_invariant_non_empty_questions_when_article_exists():
    """
    Invariant:
    If ordinance has >=1 article,
    customized_question_set.questions must not be empty.
    """
    html = """
    <html>
      <body>
        <div class="article" id="a1">
          <h2>第1条</h2>
          <div class="paragraph" id="p1">
            <p>1 本文</p>
          </div>
        </div>
        <div class="article" id="a2">
          <h2>第2条</h2>
        </div>
      </body>
    </html>
    """

    st = extract_ordinance_structure(html)

    templates = [
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条の内容を要約してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        )
    ]

    qs = concretize_questions(
        templates,
        st,
        source_golden_question_pool="A",
    )

    assert len(qs) >= 1, (
        "Invariant violation: "
        "ordinance has articles but no questions were generated"
    )


def test_fail_fast_when_articles_exist_and_no_questions_generated():
    """
    Fail-fast:
    If ordinance has >=1 article but no questions are generated,
    concretize_questions must raise.
    """
    html = """
    <html>
      <body>
        <div class="article" id="a1">
          <h2>第1条</h2>
        </div>
      </body>
    </html>
    """

    st = extract_ordinance_structure(html)

    templates = [
        GoldenQuestionTemplate(
            template_id="Q4",
            text="第○条第○項の内容を要約してください。",
            requires_article=True,
            requires_paragraph=True,
            requires_supplementary=False,
        )
    ]

    with pytest.raises(ValueError):
        concretize_questions(
            templates,
            st,
            source_golden_question_pool="A",
        )
