# tests/customized_question_set/test_concretizer.py

from customized_question_set.concretizer import concretize_questions
from customized_question_set.ordinance_structure import extract_ordinance_structure
from customized_question_set.types import GoldenQuestionTemplate


def _structure_from_html(html: str):
    return extract_ordinance_structure(html)


def test_concretize_generates_questions_when_structure_allows():
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
    st = _structure_from_html(html)

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

    assert len(qs) > 0
    assert all("第" in q.text for q in qs)


def test_concretize_excludes_when_structure_impossible():
    html = """
    <html>
      <body>
        <p>前文のみ</p>
      </body>
    </html>
    """
    st = _structure_from_html(html)

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

    # 条が存在しないため生成されない
    assert qs == []


def test_concretize_is_deterministic():
    html = """
    <html>
      <body>
        <div class="article" id="a1">
          <h2>第1条</h2>
        </div>
        <div class="article" id="a2">
          <h2>第2条</h2>
        </div>
      </body>
    </html>
    """
    st = _structure_from_html(html)

    templates = [
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条の内容を要約してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        )
    ]

    qs1 = concretize_questions(templates, st, source_golden_question_pool="A")
    qs2 = concretize_questions(templates, st, source_golden_question_pool="A")

    assert [q.question_id for q in qs1] == [q.question_id for q in qs2]
    assert [q.text for q in qs1] == [q.text for q in qs2]
