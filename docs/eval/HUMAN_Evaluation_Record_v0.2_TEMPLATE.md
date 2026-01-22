---
title: HUMAN Evaluation Record v0.2
schema_version: human_eval.v0.2
evaluation_run_id: <run_id>
bundle_id: <bundle_id>
generated_at: <YYYY-MM-DD>
evaluator: <name / role>
based_on:
  - evaluation_auto.json
  - answer artifacts (html / markdown)
---

# HUMAN Evaluation Record v0.2

## 1. 本記録の位置づけ

本記録は、AUTO Evaluation の結果を受けて、

- Evaluation が成立しているか
- 差異が設計判断に関係する性質を持つか

を **人間が確認するための記録**である。

本記録は、

- 回答の良し悪しを評価するものではない
- モデル性能を断定するものではない

---

## 2. AUTO Evaluation 概要（要約）

- Reference Diff 分布：
  - true: <n>
  - false: <m>
- Structural Diff 分布：
  - true: <n>
  - false: <m>

AUTO の結果から、
HTML / Markdown 間に差異が存在することは確認された。

---

## 3. Gate 判定（全体）

| 観点 | 判定 | 備考 |
|---|---|---|
| 評価条件の同一性 | OK | 入力条件に差異なし |
| Evaluation 手順 | OK | 想定フロー通り |
| 評価結果の妥当性 | OK | 分布は想定範囲 |

※ 本 Gate 判定は  
Evaluation が「失敗していない」ことのみを示す。

---

## 4. 逸脱事例（Evidence）

以下は、AUTO が示した差異の中から、  
**設計判断に関係すると考えられる代表例**である。

### Evidence-01

- Ordinance ID:
- Question ID:
- Question Text:

#### 対象条文（抜粋）
（条例本文の該当箇所）

#### HTML Answer（抜粋）
（引用）

#### Markdown Answer（抜粋）
（引用）

#### 観測結果
- 到達性（Retrieval Reach）: OK / △ / NG  
  - 判定理由：
- 構造保持（Structural Integrity）: OK / NG  
  - 判定理由：
- 補完耐性（Hallucination Control）: OK / NG  
  - 判定理由：

---

### Evidence-02（任意）

（同上。最大でも 3〜5 件まで）

---

## 5. 観測軸ごとの整理（要約）

※ 網羅ではなく、傾向の言語化のみ行う。

- **到達性**
  - 条番号指定質問において、
    HTML Answer 側で参照ズレが発生する事例が確認された。
- **構造保持**
  - 附則・定義に関する質問で、
    本文規定との混同が見られる事例が存在した。
- **補完耐性**
  - 条例本文に明示のない手続について、
    一般的な行政手続を補完する傾向が確認された。

---

## 6. 本 Evaluation から得られる示唆（限定）

本記録は、以下を示唆する。

- HTML / Markdown の差異は、
  単なる表現差ではなく、
  ナレッジ投入後の意味解釈に影響する可能性がある。
- ただし、本記録は
  正本形式の選択を直接決定するものではない。

---

## 7. 次フェーズへの引き渡し

本 HUMAN Evaluation Record は、

- Design Judgment
- Judgment JSON

において参照される **観測事実の一部**として扱われる。

本記録自体が判断を下すことはない。

---
