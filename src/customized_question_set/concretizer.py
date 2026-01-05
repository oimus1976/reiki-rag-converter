# src/customized_question_set/concretizer.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from customized_question_set.types import ConcreteQuestion, GoldenQuestionTemplate
from customized_question_set.ordinance_structure import OrdinanceStructureFacts, OrdinanceArticle


# =========================
# Limits (Coverage Policy v0.1.1 - standard caps)
# =========================
MAX_Q_ARTICLE = 3      # e.g., Q3
MAX_Q_ARTICLE_PARA = 6 # e.g., Q4
MAX_Q_RELATION = 2     # e.g., Q12


# =========================
# Helpers: ID and placeholder replacement
# =========================

def _make_question_id(
    source_pool: str,
    template_id: str,
    *,
    a1: Optional[int] = None,
    p1: Optional[int] = None,
    a2: Optional[int] = None,
) -> str:
    # Deterministic, human-readable
    parts = [source_pool, template_id]
    if a1 is not None:
        parts.append(f"a{a1}")
    if p1 is not None:
        parts.append(f"p{p1}")
    if a2 is not None:
        parts.append(f"a{a2}")
    return ":".join(parts)


def _replace_article_once(text: str, article_pos: int) -> str:
    return text.replace("第○条", f"第{article_pos}条", 1)


def _replace_paragraph_once(text: str, paragraph_pos: int) -> str:
    return text.replace("第○項", f"第{paragraph_pos}項", 1)


def _replace_two_articles(text: str, a1: int, a2: int) -> str:
    # Replace first then second occurrence deterministically
    t = text.replace("第○条", f"第{a1}条", 1)
    t = t.replace("第○条", f"第{a2}条", 1)
    return t


def _normalize_legal_term(text: str) -> str:
    return text.replace("条例", "法規文書")


def _cap(items: List[ConcreteQuestion], max_n: int) -> List[ConcreteQuestion]:
    return items[:max_n]


# =========================
# Coverage Policy v0.1.1 selection rules (fact-only inputs)
# =========================

def _article_number(article: OrdinanceArticle) -> int:
    """
    条番号として使用する値を決定する（number を優先）。
    """
    return article.number if isinstance(article.number, int) else article.index


def _unique_article_numbers(articles: List[OrdinanceArticle]) -> List[int]:
    """
    条番号の重複を除去し、DOM順のまま返す。
    """
    seen = set()
    nums: List[int] = []
    for article in articles:
        num = _article_number(article)
        if num not in seen:
            seen.add(num)
            nums.append(num)
    return nums


def _index_articles_by_number(articles: List[OrdinanceArticle]) -> dict[int, OrdinanceArticle]:
    """
    条番号→最初に出現した OrdinanceArticle へのマップ。
    """
    mapping: dict[int, OrdinanceArticle] = {}
    for article in articles:
        num = _article_number(article)
        if num not in mapping:
            mapping[num] = article
    return mapping


def _select_article_positions(valid_article_numbers: List[int]) -> List[int]:
    """
    1-based positions: [1, ceil(n/2), n] unique, preserving order.
    """
    if not valid_article_numbers:
        return []
    mid_idx = (len(valid_article_numbers) - 1) // 2
    candidates = [
        valid_article_numbers[0],
        valid_article_numbers[mid_idx],
        valid_article_numbers[-1],
    ]
    out: List[int] = []
    for x in candidates:
        if x not in out:
            out.append(x)
    return out


def _select_article_pairs(valid_article_numbers: List[int]) -> List[Tuple[int, int]]:
    """
    1-based pairs:
      always (1, n)
      and if n>=3 then (1, ceil(n/2))
    unique, preserving order.
    """
    if not valid_article_numbers:
        return []
    mid_idx = (len(valid_article_numbers) - 1) // 2
    first = valid_article_numbers[0]
    last = valid_article_numbers[-1]
    mid = valid_article_numbers[mid_idx]

    pairs = [(first, last)]
    if len(valid_article_numbers) >= 3:
        pairs.append((first, mid))
    out: List[Tuple[int, int]] = []
    for p in pairs:
        if p not in out:
            out.append(p)
    return out


def _select_paragraph_positions(article: OrdinanceArticle) -> List[int]:
    """
    1-based positions: [1, last] unique, preserving order.
    """
    m = len(article.paragraphs)
    if m <= 0:
        return []
    candidates = [1, m]
    out: List[int] = []
    for x in candidates:
        if x not in out:
            out.append(x)
    return out


# =========================
# Template classification (minimal)
# =========================

def _count_article_placeholders(text: str) -> int:
    return text.count("第○条")


def _is_relation_template(t: GoldenQuestionTemplate) -> bool:
    return _count_article_placeholders(t.text) >= 2


def _is_article_paragraph_template(t: GoldenQuestionTemplate) -> bool:
    return t.requires_paragraph is True


def _is_article_only_template(t: GoldenQuestionTemplate) -> bool:
    return t.requires_article is True and not _is_relation_template(t) and not _is_article_paragraph_template(t)


# =========================
# Public API
# =========================

def concretize_questions(
    templates: List[GoldenQuestionTemplate],
    structure: OrdinanceStructureFacts,
    *,
    source_golden_question_pool: str,
) -> List[ConcreteQuestion]:
    """
    Coverage Policy v0.1.1 を忠実に適用し、テンプレを具体化する。
    生成順は意味を持つ（生成順＝実行順）ため、順序を保持する。
    """
    concrete: List[ConcreteQuestion] = []

    article_numbers = _unique_article_numbers(structure.articles)
    article_by_number = _index_articles_by_number(structure.articles)

    for t in templates:
        # ---- Structural exclusion (Policy §8 minimal) ----
        if t.requires_article and not structure.has_articles:
            continue
        if t.requires_paragraph and not structure.has_paragraphs:
            continue
        if t.requires_supplementary and not structure.has_supplementary:
            continue

        # ---- Relation (e.g., Q12) ----
        if _is_relation_template(t):
            pairs = _select_article_pairs(article_numbers)
            qs: List[ConcreteQuestion] = []
            for (a1, a2) in pairs:
                text = _replace_two_articles(t.text, a1, a2)
                text = _normalize_legal_term(text)
                qid = _make_question_id(source_golden_question_pool, t.template_id, a1=a1, a2=a2)
                qs.append(ConcreteQuestion(question_id=qid, text=text, source_template_id=t.template_id))
            concrete.extend(_cap(qs, MAX_Q_RELATION))
            continue

        # ---- Article + Paragraph (e.g., Q4) ----
        if _is_article_paragraph_template(t):
            # Primary: select among articles that have paragraphs
            articles_with_paragraphs = [a for a in structure.articles if len(a.paragraphs) > 0]
            article_numbers_with_paragraphs = _unique_article_numbers(articles_with_paragraphs)
            article_with_paragraph_map = _index_articles_by_number(articles_with_paragraphs)
            qs: List[ConcreteQuestion] = []

            for a_num in _select_article_positions(article_numbers_with_paragraphs):
                article = article_with_paragraph_map.get(a_num)
                if article is None or len(article.paragraphs) == 0:
                    continue

                para_positions = _select_paragraph_positions(article)
                for p_pos in para_positions:
                    text = _replace_article_once(t.text, a_num)
                    text = _replace_paragraph_once(text, p_pos)
                    text = _normalize_legal_term(text)
                    qid = _make_question_id(source_golden_question_pool, t.template_id, a1=a_num, p1=p_pos)
                    qs.append(ConcreteQuestion(question_id=qid, text=text, source_template_id=t.template_id))

            # Safety: if still empty but paragraphs are reported, do not fabricate;
            # allow Coverage Policy to skip this template.

            concrete.extend(_cap(qs, MAX_Q_ARTICLE_PARA))
            continue

        # ---- Article only (e.g., Q3) ----
        if _is_article_only_template(t):
            article_positions = _select_article_positions(article_numbers)
            qs: List[ConcreteQuestion] = []
            for a_pos in article_positions:
                text = _replace_article_once(t.text, a_pos)
                text = _normalize_legal_term(text)
                qid = _make_question_id(source_golden_question_pool, t.template_id, a1=a_pos)
                qs.append(ConcreteQuestion(question_id=qid, text=text, source_template_id=t.template_id))
            concrete.extend(_cap(qs, MAX_Q_ARTICLE))
            continue

        # ---- Non-placeholder (e.g., Q1/Q2/Q5...) ----
        qid = _make_question_id(source_golden_question_pool, t.template_id)
        text = _normalize_legal_term(t.text)
        concrete.append(ConcreteQuestion(question_id=qid, text=text, source_template_id=t.template_id))

    if structure.has_articles and len(concrete) == 0:
        raise ValueError(
            "Invariant violation: ordinance has articles but no questions were generated"
        )

    return concrete
