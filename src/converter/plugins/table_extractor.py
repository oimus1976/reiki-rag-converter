# src/converter/plugins/table_extractor.py

from dataclasses import dataclass
from typing import List, Union, Literal, Optional
from bs4 import BeautifulSoup, Tag

import re

_ITEM_HEAD_RE = re.compile(r"^\s*(\d+)\s+")

def _extract_item_no_from_text(text: str) -> Optional[str]:
    """
    Detect leading item number like '11　...' or '11 ...'.
    Returns item number as string if detected.
    """
    m = _ITEM_HEAD_RE.match(text)
    return m.group(1) if m else None


@dataclass
class AnnexHeading:
    node: Tag
    text: str

@dataclass
class AnnexBlock:
    heading: AnnexHeading
    nodes: List[Tag]

@dataclass
class AnnexCandidateRegion:
    start_idx: int
    end_idx: int
    heading: Optional[AnnexHeading]

@dataclass
class ExtractedTable:
    table_node: Tag
    order: int

@dataclass
class AnnexTextPart:
    kind: Literal["text"]
    content: str

@dataclass
class AnnexTablePart:
    kind: Literal["table"]
    content: ExtractedTable

AnnexPart = Union[AnnexTextPart, AnnexTablePart]

@dataclass
class AnnexItem:
    item_no: Optional[str]   # "11" など。取れない場合は None
    order: int               # annex 内の順序
    parts: List[AnnexPart]

@dataclass(frozen=True)
class CsvTableContext:
    table: ExtractedTable
    annex_no: Optional[str]
    item_no: Optional[str]
    table_no: int

@dataclass(frozen=True)
class CsvCell:
    annex_no: Optional[str]
    item_no: Optional[str]
    table_no: int
    row_no: int
    col_no: int
    value: str

def _iter_annex_items_from_region(
    soup,
    region: AnnexCandidateRegion
) -> List[AnnexItem]:
    """
    Segment annex region into item-based structure.
    - Item starts when text eline begins with an item number.
    - Tables are attached to the most recent item.
    """
    elines = soup.select("div.eline")
    items: List[AnnexItem] = []

    current_item: Optional[AnnexItem] = None
    order = 0

    for eline in elines[region.start_idx : region.end_idx]:
        # collect tables in this eline (non-nested)
        tables = [
            t for t in eline.select("table")
            if t.find_parent("table") is None
        ]

        # extract visible text (rough, minimal)
        text = eline.get_text(strip=True)

        item_no = _extract_item_no_from_text(text)

        # start a new item if item number detected
        if item_no is not None:
            current_item = AnnexItem(
                item_no=item_no,
                order=order,
                parts=[],
            )
            order += 1
            items.append(current_item)

            # add text part (even if tables follow)
            if text:
                # text
                current_item.parts.append(
                    AnnexTextPart(kind="text", content=text)
                )

            # attach tables (if any)
            for table in tables:
                # table
                current_item.parts.append(
                    AnnexTablePart(
                        kind="table",
                        content=ExtractedTable(
                            table_node=table,
                            order=len([p for p in current_item.parts if p.kind == "table"])
                        )
                    )
                )

            continue

        # no new item starts here
        if current_item is None:
            # ignore preamble noise safely (別表見出しなど)
            continue

        # attach text (if meaningful)
        if text:
            current_item.parts.append(
                AnnexTextPart(kind="text", content=text)
            )

        # attach tables
        for table in tables:
            current_item.parts.append(
                AnnexTablePart(
                    kind="table",
                    content=ExtractedTable(
                        table_node=table,
                        order=len([p for p in current_item.parts if p.kind == "table"])
                    ),
                )
            )

    return items

def extract_csv_cells_from_annex_region(
    annex_no: Optional[str],
    soup: BeautifulSoup,
    region: AnnexCandidateRegion,
) -> list[CsvCell]:
    cells: list[CsvCell] = []

    for item in _iter_annex_items_from_region(soup, region):
        contexts = iter_csv_table_contexts_from_annex_item(
            annex_no=annex_no,
            item=item,
        )

        for ctx in contexts:
            cells.extend(extract_table_to_csv(ctx))

    return cells

def iter_csv_table_contexts_from_annex_item(
    annex_no: Optional[str],
    item: AnnexItem,
) -> list[CsvTableContext]:
    contexts: list[CsvTableContext] = []
    table_no = 0

    for part in item.parts:
        if part.kind != "table":
            continue

        table_no += 1

        contexts.append(
            CsvTableContext(
                table=part.content,   # ExtractedTable
                annex_no=annex_no,
                item_no=item.item_no,
                table_no=table_no,
            )
        )

    return contexts

def extract_table_to_csv(ctx: CsvTableContext) -> list[CsvCell]:
    table_node = ctx.table.table_node
    cells: list[CsvCell] = []

    if table_node is None:
        return cells

    rows = table_node.find_all("tr")
    for row_idx, tr in enumerate(rows, start=1):
        cols = tr.find_all(["td", "th"])
        for col_idx, td in enumerate(cols, start=1):
            text = td.get_text(strip=True)
            cells.append(
                CsvCell(
                    annex_no=ctx.annex_no,
                    item_no=ctx.item_no,
                    table_no=ctx.table_no,
                    row_no=row_idx,
                    col_no=col_idx,
                    value=text,
                )
            )
    return cells


def render_annex_item_to_markdown(item: AnnexItem) -> str:
    lines: List[str] = []

    # item heading（1回だけ）
    lines.append(f"#### {item.item_no}" if item.item_no else "#### （番号なし）")

    for part in item.parts:
        if part.kind == "text":
            text = part.content.strip()
            if text:
                lines.append(text)

        elif part.kind == "table":
            table_md = render_table_to_markdown(part.content)
            if table_md:
                lines.append(table_md)

    return "\n\n".join(lines).strip() + "\n"

def render_annex_region_to_markdown(
    soup: "BeautifulSoup",
    region: "AnnexCandidateRegion",
) -> str:
    """
    Render a single AnnexCandidateRegion (annex) into Markdown.
    Minimal: heading + concatenated items, order-preserving.
    """
    lines: list[str] = []

    # Annex heading
    if region.heading is not None:
        lines.append(f"### {region.heading.text}")
    else:
        # implicit annex fallback (should be rare for our golden)
        lines.append("### 別表")

    lines.append("")  # blank line

    items = _iter_annex_items_from_region(soup, region)

    for item in items:
        item_md = render_annex_item_to_markdown(item).rstrip()
        if item_md:
            lines.append(item_md)
            lines.append("")  # blank line between items

    return "\n".join(lines).rstrip() + "\n"

def render_table_to_markdown(table: ExtractedTable) -> str:
    """
    Temporary minimal table renderer.
    """
    return "| dummy |\n| --- |\n"

def _extract_tables_from_region(soup, region: AnnexCandidateRegion) -> List[ExtractedTable]:
    """
    Extract tables from the given annex candidate region.
    Pure extraction only; no semantic judgment.
    """
    elines = soup.select("div.eline")
    tables: List[ExtractedTable] = []
    order = 0

    for eline in elines[region.start_idx : region.end_idx]:
        # find tables directly under this eline
        for table in eline.select("table"):
            # ignore nested tables
            if table.find_parent("table") is not None:
                continue

            tables.append(
                ExtractedTable(
                    table_node=table,
                    order=order,
                )
            )
            order += 1

    return tables

def _is_reference_only_annex_heading(heading_node) -> bool:
    section = heading_node.select_one(".table_section")
    if not section:
        return False

    # 同一 table_section 内に table がある = 参照用
    return section.select_one("table") is not None

def _region_contains_table(elines, start: int, end: int, *, skip_first: bool = False) -> bool:
    begin = start + 1 if skip_first else start
    return any(
        elines[idx].select_one("table")
        for idx in range(begin, end)
    )


def _detect_annex_candidate_regions(soup, headings: List[AnnexHeading]):
    regions: List[AnnexCandidateRegion] = []

    elines = soup.select("div.eline")
    eline_index = {eline: idx for idx, eline in enumerate(elines)}

    # --- Case A: explicit annex headings (keep only regions that actually contain tables) ---
    for i, heading in enumerate(headings):
        # 参照用別表（使用料条例パターン）を除外
        if _is_reference_only_annex_heading(heading.node):
            continue
        start = eline_index.get(heading.node)
        if start is None:
            continue

        end = len(elines)

        # next annex heading
        if i + 1 < len(headings):
            next_start = eline_index.get(headings[i + 1].node)
            if next_start is not None:
                end = min(end, next_start)

        # supplement
        for idx in range(start + 1, len(elines)):
            if elines[idx].select_one(".s-head"):
                end = min(end, idx)
                break

        if start < end and _region_contains_table(elines, start, end):
            regions.append(
                AnnexCandidateRegion(
                    start_idx=start,
                    end_idx=end,
                    heading=heading,
                )
            )

    # --- Case B: implicit annex region (fallback only) ---
    if not regions:
        last_article_idx = None
        for idx, eline in enumerate(elines):
            if eline.select_one(".article, .clause, .item"):
                last_article_idx = idx

        if last_article_idx is not None:
            start = last_article_idx + 1
            end = len(elines)

            for idx in range(start, len(elines)):
                if elines[idx].select_one(".s-head"):
                    end = idx
                    break

            if start < end and _region_contains_table(elines, start, end, skip_first=True):
                regions.append(
                    AnnexCandidateRegion(
                        start_idx=start,
                        end_idx=end,
                        heading=None,
                    )
                )

    return regions

def _find_annex_headings(soup: BeautifulSoup) -> List[AnnexHeading]:
    """
    Detect annex (別表) block start points.

    Definition (Golden-based):
    - Appears as an independent eline block
    - Contains '別表第'
    - Is NOT an article / clause / item / supplement
    - Has <table> in following eline blocks
    """
    headings: List[AnnexHeading] = []

    elines = soup.select("div.eline")

    for idx, eline in enumerate(elines):
        text = eline.get_text(strip=True)

        # (1) must mention 別表第
        if "別表第" not in text:
            continue

        # (2) exclude normal article / clause / supplement blocks
        if eline.select_one(".article, .clause, .item, .s-head"):
            continue

        # (3) must have table in following block range
        if not _has_table_in_following_elines(elines, idx):
            continue

        headings.append(
            AnnexHeading(
                node=eline,
                text=text,
            )
        )

    return headings


def _has_table_in_following_elines(elines: List[Tag], start_idx: int) -> bool:
    """
    Scan forward until:
    - next annex-like heading
    - supplement
    - end of document

    Return True if <table> appears before that.
    """
    for eline in elines[start_idx + 1:]:
        # stop conditions
        if eline.select_one(".s-head"):
            return False
        if "別表第" in eline.get_text(strip=True):
            return False

        # positive condition
        if eline.select_one("table"):
            return True

    return False

def _iter_annex_blocks(soup, headings: List[AnnexHeading]):
    """
    Yield AnnexBlock objects.

    Each block starts at an AnnexHeading node and continues
    until:
      - next AnnexHeading
      - supplement (.s-head)
      - end of document
    """
    elines = soup.select("div.eline")

    # eline → index の逆引き
    eline_index = {eline: idx for idx, eline in enumerate(elines)}

    for i, heading in enumerate(headings):
        start_idx = eline_index.get(heading.node)
        if start_idx is None:
            continue  # safety guard

        nodes = [headings[i].node]

        for eline in elines[start_idx + 1:]:
            # stop: next annex heading
            if any(eline is h.node for h in headings[i + 1:]):
                break

            # stop: supplement
            if eline.select_one(".s-head"):
                break

            nodes.append(eline)

        yield AnnexBlock(
            heading=heading,
            nodes=nodes,
        )

