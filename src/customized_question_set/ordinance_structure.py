# src/customized_question_set/ordinance_structure.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup


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
    element_id: Optional[str]
    paragraphs: List[OrdinanceParagraph]


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

    first_article: Optional[OrdinanceArticle]
    first_paragraph: Optional[OrdinanceParagraph]


# =========================
# Extractor
# =========================

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

        # --- 項の抽出 ---
        # 項は <div class="paragraph"> を想定
        paragraph_elements = article_el.select(".paragraph")

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
                element_id=article_id,
                paragraphs=paragraphs,
            )
        )

    has_articles = len(articles) > 0
    has_paragraphs = any(len(a.paragraphs) > 0 for a in articles)

    # --- 附則の存在判定 ---
    # class="supplementary" を附則とみなす（内容は見ない）
    has_supplementary = soup.select_one(".supplementary") is not None

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
        first_article=first_article,
        first_paragraph=first_paragraph,
    )
