# tests/test_extract_tables_from_region.py

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


def test_fee_ordinance_annex_items_contain_tables_when_expected():
    soup = load_soup("reiki-html/k518RG00000219.html")
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    # 別表第2 を対象
    annex2 = next(
        r for r in regions
        if r.heading and "別表第2" in r.heading.text
    )
    
    items = _iter_annex_items_from_region(soup, annex2)

    # table を含む item を抽出
    items_with_table = [
        item for item in items
        if any(part.kind == "table" for part in item.parts)
    ]

    # HTML事実：別表第2には table を含む項が複数ある
    assert len(items_with_table) >= 2

    # 各 item の table は1つまで（最小保証）
    for item in items_with_table:
        tables = [p for p in item.parts if p.kind == "table"]
        assert len(tables) == 1
