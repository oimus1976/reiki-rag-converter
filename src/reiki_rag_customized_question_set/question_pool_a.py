from __future__ import annotations

from typing import List

from reiki_rag_customized_question_set.types import GoldenQuestionTemplate


def load_golden_question_pool_a() -> List[GoldenQuestionTemplate]:
    """
    Golden Question Pool A（v1.1, 凍結資産）をそのまま返す。

    - 本プールは 18 問で構成される知的資産（Golden Question Pool）
    - 加工・並び替え・条件分岐は一切行わない
    - 並び順・内容は正本（Golden_Question_Pool_A v1.1）に厳密に一致させる
    """

    return [
        # A-1：条例の基本理解
        GoldenQuestionTemplate(
            template_id="Q1",
            text="この条例の目的を分かりやすく説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q2",
            text="この条例が何条で構成されているかを示し、それぞれの条の概要を説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),

        # A-2：条・項の検索精度
        GoldenQuestionTemplate(
            template_id="Q3",
            text="第○条の内容を要約してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q4",
            text="第○条第○項の内容を説明してください。",
            requires_article=True,
            requires_paragraph=True,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q5",
            text="この条例で定められている義務・禁止事項をすべて抽出し、箇条書きで説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),

        # A-3：参照統合（条・附則）
        GoldenQuestionTemplate(
            template_id="Q6",
            text="この条例に基づく手続きの全体的な流れを、関連条文を引用しながら説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q7",
            text="他の条文の解釈に影響を与える条があれば、引用して説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q8",
            text="附則がある場合、その内容を要約し、本則との関係を説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=True,
        ),

        # A-4：曖昧質問耐性
        GoldenQuestionTemplate(
            template_id="Q9",
            text="住民（関係者）が特に注意すべき点を説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q10",
            text="例外規定がある場合、その内容を説明してください。なければ「ない」と答えてください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),

        # A-5：正答一意・誤答誘発ポイント
        GoldenQuestionTemplate(
            template_id="Q11",
            text="定義されている用語があれば、定義条を引用して説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q12",
            text="第○条と第○条の関係性を説明してください。",
            requires_article=True,
            requires_paragraph=False,
            requires_supplementary=False,
        ),

        # A-6：根拠提示強制
        GoldenQuestionTemplate(
            template_id="Q13",
            text="回答の根拠となる条文を引用して示してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q14",
            text="判断基準を本文の記載箇所を引用しながらまとめてください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),

        # A-7：構造化再生成
        GoldenQuestionTemplate(
            template_id="Q15",
            text="条例を「目的→手続き→義務→例外→附則」の順に再構成してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q16",
            text="第三者に説明する場合の最適な説明順を、条文に基づいて示してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),

        # A-8：統合まとめ
        GoldenQuestionTemplate(
            template_id="Q17",
            text="条例全体を統合して説明してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
        GoldenQuestionTemplate(
            template_id="Q18",
            text="条例全体を100字以内で要約してください。",
            requires_article=False,
            requires_paragraph=False,
            requires_supplementary=False,
        ),
    ]
