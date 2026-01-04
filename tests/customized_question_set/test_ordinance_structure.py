# tests/customized_question_set/test_ordinance_structure.py

from pathlib import Path
import pytest

from customized_question_set.ordinance_structure import extract_ordinance_structure


FIXTURES = Path("tests/fixtures/html")


def load_html(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_single_article_no_paragraph():
    """
    条のみ・項なしの最小ケース
    """
    html = load_html("minimal_article_only.html")
    structure = extract_ordinance_structure(html)

    assert structure.has_articles is True
    assert structure.has_paragraphs is False
    assert structure.has_supplementary is False

    assert len(structure.articles) == 1
    assert structure.articles[0].index == 1
    assert structure.articles[0].number == 1
    assert structure.articles[0].paragraphs == []


def test_single_article_with_paragraphs():
    """
    1条・複数項あり
    """
    html = load_html("article_with_paragraphs.html")
    structure = extract_ordinance_structure(html)

    assert structure.has_articles is True
    assert structure.has_paragraphs is True
    assert structure.has_supplementary is False

    assert len(structure.articles) == 1
    article = structure.articles[0]
    assert article.index == 1
    assert article.number == 1
    assert len(article.paragraphs) == 2
    assert [p.index for p in article.paragraphs] == [1, 2]


def test_multiple_articles():
    """
    複数条が順序通りに抽出される
    """
    html = load_html("multiple_articles.html")
    structure = extract_ordinance_structure(html)

    assert structure.has_articles is True
    assert structure.has_supplementary is False

    assert [a.index for a in structure.articles] == [1, 2, 3]
    assert [a.number for a in structure.articles] == [1, 2, 3]


def test_with_supplementary():
    """
    附則の有無判定のみを見る
    """
    html = load_html("with_supplementary.html")
    structure = extract_ordinance_structure(html)

    assert structure.has_articles is True
    assert structure.has_supplementary is True


def test_no_article_returns_empty_structure():
    """
    条が1つも抽出できない場合は空構造を返す
    """
    html = load_html("no_article.html")

    structure = extract_ordinance_structure(html)

    assert structure.has_articles is False
    assert structure.has_paragraphs is False
    assert structure.articles == []
