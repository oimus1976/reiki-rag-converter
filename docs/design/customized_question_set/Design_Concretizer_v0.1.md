---
title: Design Concretizer v0.1
status: fixed
version: v0.1
last_updated: 2026-01-02
scope: customized_question_set
depends_on:
  - docs/policy/Coverage_Policy_v0.1.1.md
  - src/customized_question_set/ordinance_structure.py
  - src/customized_question_set/types.py
---

# Concretizer 設計 v0.1（FIX）

## 1. 目的

Golden Question Pool のテンプレートを、条例構造（DOM順事実）に基づき機械的に具体化し、比較試験に用いる ConcreteQuestion 群を決定的に生成する。

## 2. 入力

- OrdinanceStructure（事実層：DOM順の条・項、存在判定、first参照）
- GoldenQuestionTemplate（テンプレ文、requires_* フラグ）
- Coverage Policy v0.1.1（条・項選択ルール、上限）

## 3. 出力

- ConcreteQuestion[]（question_id / text / source_template_id）
- 生成順は意味を持つ（生成順＝実行順）

## 4. 非目的

- 意味解釈、重要度判断、質問最適化
- HTML解析（ordinance_structure が責務）
- JSON整形（writer が責務）

## 5. Coverage Policy v0.1.1 のコード化方針

- 章4: 条選択 → DOM順 positions [1, ceil(n/2), n] をユニーク化
- 章5: 項選択 → 各条で [1, last] をユニーク化
- 章5.3: セーフティ → “項を持つ条集合”で条選択を再適用し、Q4が0件になる事故を回避
- 章6: 条間関係 → (1,n) と (1,ceil(n/2))（n>=3）
- 章7: 上限 → Q3<=3, Q4<=6, Q12<=2（生成後に順序維持で cap）
- 章8: 除外 → 構造的に不成立な場合のみ（理由は内部ログのみ）

## 6. テンプレ種別の分類ルール（最小）

- 条×条（関係）: テンプレ文に「第○条」が2回以上含まれる
- 条＋項: requires_paragraph=True
- 条のみ: requires_article=True かつ（条×条ではない）
- 非プレースホルダ: 上記以外

## 7. question_id 方針（concretizer内で決定的に生成）

- template_id と条/項 positions を材料に、決定的な文字列を構成
- 形式（例）:
  - no placeholder: "{pool}:{template_id}"
  - article: "{pool}:{template_id}:a{A}"
  - article+paragraph: "{pool}:{template_id}:a{A}:p{P}"
  - relation: "{pool}:{template_id}:a{A1}:a{A2}"
- ordinance_id 等の上位要素は generator 側の question_set_id と責務分離（v0.1では混ぜない）

## Appendix: Future Extensions (Non-Blocking)

（※ 今は実装しない。将来の拡張案を忘却防止のため記録する）

### A-1. 号（Item）単位への拡張

- 現状は「条」「項」までを構造単位として扱う
- 将来、号（第○号）が比較上重要になる可能性

想定拡張：

- OrdinanceParagraph に items: list[OrdinanceItem] を追加
- Coverage Policy v0.y（Item）を新設し、号選択も位置サンプリングで行う

非対応理由（現時点）：

- HTML構造のばらつきが大きい
- 比較試験価値（差が顕著になるか）が未検証

### A-2. 前段／後段／ただし書きの分節化

- 法制執務上、1項が前段／後段／ただし書きに分かれる場合がある

想定拡張：

- OrdinanceParagraph に segments: list[ParagraphSegment] を追加
- DOM上の特定クラスや区切りから機械分割（意味解釈はしない）

非対応理由（現時点）：

- 分割境界が安定しないケースがある
- 事実層が肥大化し、統制点が増え過ぎる

### A-3. Coverage Policy の切替（複数ポリシー対応）

想定拡張：

- policy を Strategy 化し、concretizer は policy.apply(...) を呼ぶだけにする

非対応理由（現時点）：

- v0.1.1 の安定前に抽象化すると過剰
- 実装コストが比較試験価値を上回る可能性

### A-4. ConcreteQuestion の構造メタデータ外部公開

想定拡張：

- JSONに debug_metadata（非必須）を追加（Execution Input Contract v2 で検討）

非対応理由（現時点）：

- ブラックボックス入力の思想と競合
- v1凍結方針と整合しない
