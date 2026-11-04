# tests/test_detect_annex_candidate_regions.py

from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
)

# 実条例HTML fixture（CI でも利用するため Git 追跡対象。tests/fixtures/reiki_html/README.md 参照）
REIKI_HTML_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "reiki_html"


def load_soup(path: Path) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_regions_with_explicit_annex():
    soup = load_soup(REIKI_HTML_FIXTURES / "k518RG00000205.html")
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    assert len(regions) >= 1
    assert all(r.heading is not None for r in regions)


def test_regions_with_multiple_annexes_in_fee_ordinance():
    soup = load_soup(REIKI_HTML_FIXTURES / "k518RG00000219.html")
    headings = _find_annex_headings(soup)

    # AnnexHeading は存在する（HTML事実）
    assert len(headings) >= 1

    regions = _detect_annex_candidate_regions(soup, headings)

    # 重要なのはここ
    # 「条文後〜附則前」の region が1つ立つこと
    assert len(regions) == 2
    assert all(r.heading is not None for r in regions)
    assert regions[0].start_idx < regions[0].end_idx

