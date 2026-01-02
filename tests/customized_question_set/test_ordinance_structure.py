# tests/customized_question_set/test_ordinance_structure.py

from customized_question_set.ordinance_structure import (
    extract_ordinance_structure,
)


def test_extract_basic_structure():
    html = """
    <html>
      <body>
        <div class="article" id="a1">
          <div class="paragraph" id="p1">本文</div>
          <div class="paragraph" id="p2">本文</div>
        </div>
        <div class="article" id="a2">
          <div class="paragraph" id="p3">本文</div>
        </div>
        <div class="supplementary">
          附則
        </div>
      </body>
    </html>
    """

    structure = extract_ordinance_structure(html)

    # --- 存在判定 ---
    assert structure.has_articles is True
    assert structure.has_paragraphs is True
    assert structure.has_supplementary is True

    # --- 条の確認 ---
    assert len(structure.articles) == 2
    assert structure.articles[0].index == 1
    assert structure.articles[0].element_id == "a1"
    assert structure.articles[1].index == 2

    # --- 項の確認 ---
    assert len(structure.articles[0].paragraphs) == 2
    assert structure.articles[0].paragraphs[0].index == 1
    assert structure.articles[0].paragraphs[0].element_id == "p1"

    # --- first ---
    assert structure.first_article.index == 1
    assert structure.first_paragraph.index == 1


def test_no_paragraphs():
    html = """
    <html>
      <body>
        <div class="article" id="a1">
          本文のみ
        </div>
      </body>
    </html>
    """

    structure = extract_ordinance_structure(html)

    assert structure.has_articles is True
    assert structure.has_paragraphs is False
    assert structure.first_article is not None
    assert structure.first_paragraph is None


def test_no_articles():
    html = """
    <html>
      <body>
        <div class="supplementary">
          附則のみ
        </div>
      </body>
    </html>
    """

    structure = extract_ordinance_structure(html)

    assert structure.has_articles is False
    assert structure.has_paragraphs is False
    assert structure.has_supplementary is True
    assert structure.first_article is None
    assert structure.first_paragraph is None
