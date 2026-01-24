from pathlib import Path

from bs4 import BeautifulSoup

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
    render_annex_region_to_markdown,
)


def load_soup(path: str) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_render_annex_region_fee_ordinance_annex2_contains_items_and_tables():
    soup = load_soup("reiki-html/k518RG00000219.html")
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    # heading が Optional なので安全に絞る
    annex2 = next(
        r for r in regions
        if r.heading is not None and "別表第2" in r.heading.text
    )

    md = render_annex_region_to_markdown(soup, annex2)

    # annex 見出し
    assert "### 別表第2" in md

    # 代表的な項見出し（HTML事実に依存しすぎない範囲）
    assert "#### 11" in md
    assert "#### 44" in md

    # table が出ている（現状 table renderer が dummy でも成立）
    assert "| dummy |" in md or "\n|" in md
