from bs4 import BeautifulSoup

from converter.plugins.table_extractor import (
    ExtractedTable,
    CsvCell,
    CsvTableContext,
    extract_table_to_csv,
)


def test_extract_table_to_csv_simple_table():
    html = """
    <table>
      <tr><th>A</th><th>B</th></tr>
      <tr><td>1</td><td>2</td></tr>
    </table>
    """
    soup = BeautifulSoup(html, "html.parser")
    table_node = soup.find("table")
    assert table_node is not None

    extracted = ExtractedTable(
        table_node=table_node,
        order=1,
    )

    ctx = CsvTableContext(
        table=extracted,
        annex_no="2",
        item_no="11",
        table_no=1,
    )

    cells = extract_table_to_csv(ctx)

    assert len(cells) == 4

    assert cells[0] == CsvCell("2", "11", 1, 1, 1, "A")
    assert cells[1] == CsvCell("2", "11", 1, 1, 2, "B")
    assert cells[2] == CsvCell("2", "11", 1, 2, 1, "1")
    assert cells[3] == CsvCell("2", "11", 1, 2, 2, "2")
