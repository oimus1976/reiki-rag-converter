# tests/test_detect_annex_candidate_regions.py

from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
)


def load_soup(path: str) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_regions_with_explicit_annex():
    soup = load_soup("reiki-html/k518RG00000205.html")
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    assert len(regions) >= 1
    assert all(r.heading is not None for r in regions)


def test_regions_with_multiple_annexes_in_fee_ordinance():
    soup = load_soup("reiki-html/k518RG00000219.html")
    headings = _find_annex_headings(soup)

    # AnnexHeading は存在する（HTML事実）
    assert len(headings) >= 1

    regions = _detect_annex_candidate_regions(soup, headings)

    # 重要なのはここ
    # 「条文後〜附則前」の region が1つ立つこと
    assert len(regions) == 2
    assert all(r.heading is not None for r in regions)
    assert regions[0].start_idx < regions[0].end_idx

