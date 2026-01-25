from bs4 import BeautifulSoup

from converter.plugins.table_extractor import (
    AnnexCandidateRegion,
    extract_csv_cells_from_annex_region,
)


def test_extract_csv_cells_from_annex_region_simple():
    # reiki-html の前提：div.eline を単位に走査する
    html = """
    <div class="eline"><p>1　テキスト</p><table><tr><td>A</td></tr></table></div>
    <div class="eline"><p>2　テキスト</p><table><tr><td>B</td></tr></table></div>
    """
    soup = BeautifulSoup(html, "html.parser")

    region = AnnexCandidateRegion(
        start_idx=0,
        end_idx=2,   # eline が2個なので明示（999でも動くが、意図が伝わる）
        heading=None,
    )

    cells = extract_csv_cells_from_annex_region(
        annex_no="2",
        soup=soup,
        region=region,
    )

    assert [c.value for c in cells] == ["A", "B"]
