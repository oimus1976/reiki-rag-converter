# src/converter/plugins/table_extractor.py

from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup, Tag


@dataclass
class AnnexHeading:
    node: Tag
    text: str


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
