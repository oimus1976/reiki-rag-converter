from bs4 import BeautifulSoup
from pathlib import Path

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
    extract_csv_cells_from_annex_region,
)

# 実条例HTML fixture（CI でも利用するため Git 追跡対象。tests/fixtures/reiki_html/README.md 参照）
REIKI_HTML_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "reiki_html"


def test_extract_csv_cells_from_real_fee_ordinance_annex2():
    # 実DOM読み込み
    html_path = REIKI_HTML_FIXTURES / "k518RG00000219.html"
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Annex 検出
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    # 別表第2 を選択
    annex2 = next(
        r for r in regions
        if r.heading and "別表第2" in r.heading.text
    )

    # CSV 抽出
    cells = extract_csv_cells_from_annex_region(
        annex_no="2",
        soup=soup,
        region=annex2,
    )

    # 「0ではない」ことのみ保証
    assert len(cells) > 0
