# tests/test_iter_annex_blocks.py

from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _iter_annex_blocks,
)


def load_soup(path: str) -> BeautifulSoup:
    html = Path(path).read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


def test_iter_annex_blocks_with_table():
    soup = load_soup("reiki-html/k518RG00000219.html")

    headings = _find_annex_headings(soup)
    blocks = list(_iter_annex_blocks(soup, headings))

    assert len(blocks) >= 1

    # each block must include at least one table
    for block in blocks:
        assert any(
            eline.select_one("table") is not None
            for eline in block.nodes
        )


def test_iter_annex_blocks_reference_only():
    soup = load_soup("reiki-html/k518RG00000030.html")

    headings = _find_annex_headings(soup)
    blocks = list(_iter_annex_blocks(soup, headings))

    assert blocks == []
