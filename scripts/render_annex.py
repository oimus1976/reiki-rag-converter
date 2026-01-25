from pathlib import Path
from bs4 import BeautifulSoup

from converter.plugins.table_extractor import (
    _find_annex_headings,
    _detect_annex_candidate_regions,
    render_annex_region_to_markdown,
)

def load_soup(path: str) -> BeautifulSoup:
    return BeautifulSoup(Path(path).read_text(encoding="utf-8"), "html.parser")

def main():
    html_path = "reiki-html/k518RG00000219.html"
    out_path = "artifacts/annex/k518RG00000219_annex2.md"

    soup = load_soup(html_path)
    headings = _find_annex_headings(soup)
    regions = _detect_annex_candidate_regions(soup, headings)

    annex2 = next(
        r for r in regions
        if r.heading is not None and "別表第2" in r.heading.text
    )

    md = render_annex_region_to_markdown(soup, annex2)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(md, encoding="utf-8")

if __name__ == "__main__":
    main()
