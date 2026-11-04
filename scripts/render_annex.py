from pathlib import Path
from bs4 import BeautifulSoup

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
    render_annex_region_to_markdown,
)

# リポジトリルート（実行ディレクトリに依存しないよう、本ファイル基準で解決する）
ROOT = Path(__file__).resolve().parents[1]

# 実条例HTML fixture（Git 追跡対象。tests/fixtures/reiki_html/README.md 参照）
REIKI_HTML_FIXTURES = ROOT / "tests" / "fixtures" / "reiki_html"


def load_soup(path: Path) -> BeautifulSoup:
    return BeautifulSoup(Path(path).read_text(encoding="utf-8"), "html.parser")

def main():
    html_path = REIKI_HTML_FIXTURES / "k518RG00000219.html"
    out_path = ROOT / "artifacts" / "annex" / "k518RG00000219_annex2.md"

    soup = load_soup(html_path)
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    annex2 = next(
        r for r in regions
        if r.heading is not None and "別表第2" in r.heading.text
    )

    md = render_annex_region_to_markdown(soup, annex2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

if __name__ == "__main__":
    main()
