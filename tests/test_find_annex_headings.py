# tests/test_find_annex_headings.py

from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import _find_annex_headings


def load_html(path: str) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_annex_with_table_detected():
    soup = load_html("reiki-html/k518RG00000219.html")
    headings = _find_annex_headings(soup)
    assert len(headings) >= 1


def test_annex_reference_only_not_detected():
    soup = load_html("reiki-html/k518RG00000030.html")
    headings = _find_annex_headings(soup)
    assert headings == []
