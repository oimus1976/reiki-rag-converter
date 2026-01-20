---
title: Evaluation 実行手順
version: v0.1
status: FIX
phase: evaluation
scope: post-observation
related:
  - Observation_Summary_v0.1.md
  - Qommons_Evaluation_Framework_v0.1.md
  - PROJECT_STATUS.md
---

# Evaluation 実行手順（v0.1）

## 0. 目的と立場

本手順は、
**Observation v0.1 の成果物を、Evaluation Framework に基づく判断へ接続するための
人間向け実行手順を固定すること**を目的とする。

Evaluation は「評価前の観測」を行う Observation とは明確に責務が異なる。
本手順は **判断の再現性を人力で保証するための規範文書**である。

### 本手順が目的としないこと（厳守）

以下を一切行わない。

* HTML版 / Markdown版の優劣決定
* 差分の妥当性・品質の断定
* Observation 手法・設計・実装そのものの評価
* Observation 結果の再解釈・再計算

---

## 1. 入力前提（開始条件）

以下が **すべて揃っている場合のみ** Evaluation を開始してよい。

* `observation_summary.md`
* `observation_result.json`
* 上記 2 点が **同一 run_id** に紐づくこと
* 成果物が zip 展開直後であり **未加工**であること

### 開始禁止条件

以下のいずれかに該当する場合、Evaluation を実施してはならない。

* 成果物の欠落
* run_id 不一致
* `observation_result.json` 単体での入手・確認

---

## 2. 読む順（固定）

Evaluation は **必ず次の順序**で実施する。

### Step 1：observation_summary.md を読む

* run の前提条件
* 対象範囲
* Observation 側で明示された注意事項
* 禁止事項の再確認

Evaluation の思考起点は **必ず Summary** とする。

---

### Step 2：diff_flags の分布を確認する

* 全件 true / 一部 true / 偏りの有無
* Diff 種別ごとの発生状況

#### 解釈ルール

* diff_flags は異常検知ではない
* diff_flags は **Evaluation 観点の優先順位付け情報**
* true が多いこと自体に意味的評価を与えてはならない

---

### Step 3：Diff 種別ごとに分離して確認する

以下を **混在させて解釈してはならない**。

#### Reference Diff

* 条・項・附則の出現有無のみを扱う

#### Volume Diff

* chars / lines / paragraphs
* 定量情報のみを扱い、意味解釈は禁止

#### Structural Diff

* 見出し・箇条書き・附則の有無
* v0.1 では boolean（一致／不一致）のみ

#### 注意事項

* `observation_result.json` は **裏取り・集計確認用途のみ**
* 同ファイルを評価の起点としてはならない

---

## 3. 判断ルール

### やってよいこと（OK）

* Observation で得られた **差分事実をそのまま** Evaluation Framework の評価軸へ写像する
* 差分の意味付けを行わず、影響可能性・論点整理に留める
* Gate 判定（OK / △ / NG）を Evaluation Framework に基づいて行う
* 評価所見・判断留保点・比較観点を記録する

> 原則：**写像は OK、再構成は NG**

---

### やってはいけないこと（NG）

* Observation の再解釈・再計算
* 差分事実の要約・抽象化・再分類
* Diff の良否・品質判断
* Observation 結果を用いた run 間の直接比較
* Structural Diff v0.1 を詳細解釈する行為
* Observation の不足を Evaluation 側で補完する行為

---

## 4. 判断の出口（成果物）

Evaluation の成果は **合否ではない**。

以下を成果として残す。

* Gate 判定結果（OK / △ / NG）
* 主な論点・観測された傾向
* 判断留保点
* 次回 Evaluation で再確認すべき観点

### 記載粒度（例）

* Gate 判定：OK / △ / NG
* 主因：Reference / Volume / Structural
* 補足：次回 Evaluation での注視点

※ 書式の厳密化は v0.2 以降で検討する。

---

## 5. 典型的な落とし穴

* diff_flags が全件 true となる run は存在し得る
* observations 配列の並び順に意味はない
* Structural Diff v0.1 は詳細解釈不可
* Observation の粗さを理由に独自判断を足してはならない
* Observation の出来を評価する場ではない

---

## 6. スコープと非対象

* 本手順は **Observation v0.1 完了後の Evaluation** にのみ適用する
* Observation v0.1 の仕様変更は対象外
* Structural Diff v0.2 以降の議論は本手順に含めない

---

## 7. 位置づけの再確認

* Observation：評価前の **観測**
* Evaluation：Framework に基づく **判断**
* 本文書：判断手順の **固定化**

この境界を越えた場合、
Evaluation の再現性は失われる。

---

## 文書化に伴う実務メモ（重要）

**想定配置先（推奨）**

```
docs/evaluation/README_evaluation_procedure_v0.1.md
```

**関連更新の注意**

* PROJECT_STATUS.md
  → 「Evaluation 実行手順 v0.1 文書化完了」を Completed に反映検討
* CHANGELOG.md
  → Docs 追加として 1 行追記検討

---
