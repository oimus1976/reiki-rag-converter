# src/customized_question_set/ordinance_structure.py

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup, Tag


# =========================
# Data models (fact only)
# =========================

@dataclass(frozen=True)
class OrdinanceParagraph:
    """
    項のDOM上の事実表現（意味は扱わない）
    """
    index: int               # DOM順（1始まり）
    element_id: Optional[str]


@dataclass(frozen=True)
class OrdinanceArticle:
    """
    条のDOM上の事実表現
    """
    index: int               # DOM順（1始まり）
    number: int              # HTML上の条番号（数字部のみ）
    element_id: Optional[str]
    paragraphs: List[OrdinanceParagraph]


@dataclass(frozen=True)
class OrdinanceSupplementary:
    """
    附則見出しのDOM上の事実表現
    """
    index: int               # DOM順（1始まり）
    element_id: Optional[str]
    heading_text: str


@dataclass(frozen=True)
class OrdinanceStructureFacts:
    """
    条例HTMLから抽出したDOM構造の事実表現（完全版）
    concretizer / generator が使用する
    """
    has_articles: bool
    has_paragraphs: bool
    has_supplementary: bool

    articles: List[OrdinanceArticle]
    supplementary: List[OrdinanceSupplementary]

    first_article: Optional[OrdinanceArticle]
    first_paragraph: Optional[OrdinanceParagraph]


# =========================
# Extractor
# =========================

_DIGIT_TABLE = str.maketrans(
    {
        "０": "0",
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
    }
)


def _normalize_digits(value: str) -> str:
    return value.translate(_DIGIT_TABLE)


def _parse_article_number(article_el: Tag) -> Optional[int]:
    """
    条の表示番号（第○条の○ の数字部のみ）を抽出する。
    - 数字部が取得できない場合は None を返す
    - 文字列の解釈は行わず、数字部分の抽出のみ
    """
    text = article_el.get_text(" ", strip=True)
    match = re.search(r"第\s*([0-9０-９]+)", text)
    if not match:
        return None
    try:
        return int(_normalize_digits(match.group(1)))
    except ValueError:
        return None


def _is_supplementary_heading_text(text: str) -> bool:
    normalized = re.sub(r"\s+", "", text)
    return normalized.startswith("附則")


def _collect_supplementary_headings(soup: BeautifulSoup) -> List[OrdinanceSupplementary]:
    body = soup.body if soup.body is not None else soup
    supplementary: List[OrdinanceSupplementary] = []
    captured_ids: set[int] = set()

    for tag in body.find_all(True):
        heading_text = tag.get_text(" ", strip=True)
        if not heading_text:
            continue
        if not _is_supplementary_heading_text(heading_text):
            continue
        if any(id(parent) in captured_ids for parent in tag.parents if isinstance(parent, Tag)):
            continue
        supplementary.append(
            OrdinanceSupplementary(
                index=len(supplementary) + 1,
                element_id=tag.get("id"),
                heading_text=heading_text,
            )
        )
        captured_ids.add(id(tag))

    return supplementary


def extract_ordinance_structure(html: str) -> OrdinanceStructureFacts:
    """
    条例HTMLから、条・項・附則の存在とDOM順構造を抽出する。

    - 意味解釈は行わない
    - DOM順をそのまま使用する
    - 前段／後段／ただし書き等は無視する
    """
    soup = BeautifulSoup(html, "html.parser")

    # --- 条の抽出 ---
    # 前提：
    # reiki-rag-converter の出力では <div class="article"> が条単位
    article_elements = soup.select(".article")

    articles: List[OrdinanceArticle] = []

    for a_idx, article_el in enumerate(article_elements, start=1):
        article_id = article_el.get("id")
        article_number = _parse_article_number(article_el)

        # --- 項の抽出 ---
        # 項は <div class="clause"> を想定
        paragraph_elements = article_el.select(".clause")

        paragraphs: List[OrdinanceParagraph] = []
        for p_idx, para_el in enumerate(paragraph_elements, start=1):
            paragraphs.append(
                OrdinanceParagraph(
                    index=p_idx,
                    element_id=para_el.get("id"),
                )
            )

        articles.append(
            OrdinanceArticle(
                index=a_idx,
                number=article_number if article_number is not None else a_idx,
                element_id=article_id,
                paragraphs=paragraphs,
            )
        )

    has_articles = len(articles) > 0
    has_paragraphs = any(len(a.paragraphs) > 0 for a in articles)

    # --- 附則の存在判定 ---
    supplementary = _collect_supplementary_headings(soup)
    has_supplementary = len(supplementary) > 0

    first_article = articles[0] if articles else None

    if first_article and first_article.paragraphs:
        first_paragraph = first_article.paragraphs[0]
    else:
        first_paragraph = None

    return OrdinanceStructureFacts(
        has_articles=has_articles,
        has_paragraphs=has_paragraphs,
        has_supplementary=has_supplementary,
        articles=articles,
        supplementary=supplementary,
        first_article=first_article,
        first_paragraph=first_paragraph,
    )
