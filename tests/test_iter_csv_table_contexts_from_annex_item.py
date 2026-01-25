from bs4 import BeautifulSoup

from converter.plugins.table_extractor import (
    AnnexItem,
    AnnexTextPart,
    AnnexTablePart,
    ExtractedTable,
    CsvTableContext,
    iter_csv_table_contexts_from_annex_item,
)


def test_iter_csv_table_contexts_from_annex_item():
    soup = BeautifulSoup(
        """
        <table><tr><td>A</td></tr></table>
        <table><tr><td>B</td></tr></table>
        """,
        "html.parser",
    )

    tables = soup.find_all("table")
    assert len(tables) == 2

    item = AnnexItem(
        item_no="11",
        order=1,
        parts=[
            AnnexTextPart(kind="text", content="説明文"),
            AnnexTablePart(
                kind="table",
                content=ExtractedTable(table_node=tables[0], order=1),
            ),
            AnnexTextPart(kind="text", content="補足"),
            AnnexTablePart(
                kind="table",
                content=ExtractedTable(table_node=tables[1], order=2),
            ),
        ],
    )

    contexts = iter_csv_table_contexts_from_annex_item(
        annex_no="2",
        item=item,
    )

    # ---- 型ガード（ここが今回の修正ポイント） ----
    part1 = item.parts[1]
    part2 = item.parts[3]

    assert isinstance(part1, AnnexTablePart)
    assert isinstance(part2, AnnexTablePart)
    # --------------------------------------------

    assert contexts == [
        CsvTableContext(
            table=part1.content,
            annex_no="2",
            item_no="11",
            table_no=1,
        ),
        CsvTableContext(
            table=part2.content,
            annex_no="2",
            item_no="11",
            table_no=2,
        ),
    ]
