# tests/test_find_annex_headings.py

from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import _find_annex_headings

# 実条例HTML fixture（CI でも利用するため Git 追跡対象。tests/fixtures/reiki_html/README.md 参照）
REIKI_HTML_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "reiki_html"


def load_html(path: Path) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_annex_with_table_detected():
    soup = load_html(REIKI_HTML_FIXTURES / "k518RG00000219.html")
    headings = _find_annex_headings(soup)
    assert len(headings) >= 1


def test_annex_reference_only_not_detected():
    soup = load_html(REIKI_HTML_FIXTURES / "k518RG00000030.html")
    headings = _find_annex_headings(soup)
    assert headings == []
