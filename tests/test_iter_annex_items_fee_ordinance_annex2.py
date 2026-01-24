# tests/test_iter_annex_items_fee_ordinance_annex2.py

from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
    _iter_annex_items_from_region,
)

def load_soup(path: str) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_fee_ordinance_annex2_items_have_text_and_tables():
    soup = load_soup("reiki-html/k518RG00000219.html")
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    # 別表第2 を選択
    annex2 = next(
        r for r in regions
        if r.heading and "別表第2" in r.heading.text
    )

    items = _iter_annex_items_from_region(soup, annex2)

    # 11項が存在する
    item11 = next(i for i in items if i.item_no == "11")

    # 前提テキストがある
    assert any(p.kind == "text" for p in item11.parts)

    # table が少なくとも1つ紐づく
    assert any(p.kind == "table" for p in item11.parts)

    # 14項が存在する（table が無くてもOK）
    item14 = next(i for i in items if i.item_no == "14")
    assert any(p.kind == "text" for p in item14.parts)
