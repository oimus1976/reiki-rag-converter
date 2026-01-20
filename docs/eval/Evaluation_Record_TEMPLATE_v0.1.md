---
title: Evaluation Record
version: v0.1
status: FIX
phase: evaluation
run_type: manual-first
related:
  - README_evaluation_procedure_v0.1.md
  - Checklist_first_evaluation_run_v0.1.md
  - Observation_Summary_v0.1.md
---

# Evaluation Record（v0.1）

## 0. 本記録の位置づけ

本記録は、
**Observation v0.1 成果物を前提に実施した Evaluation の結果を固定するための記録**である。

* 考察文書ではない
* 改善提案書ではない
* 判断ログである

---

## 1. Evaluation メタ情報【AUTO】

※ 観測成果物・実行環境から自動取得可能

* run_id：
* 評価日時：
* 評価者：
* Observation version：v0.1
* Evaluation Procedure：v0.1

---

## 2. Observation 前提確認【AUTO】

* Observation Summary 読了：yes
* 再解釈・再計算なし：yes
* 未加工成果物を使用：yes

---

## 3. diff_flags 分布【AUTO】

```text
reference_diff  : true XXX / false YYY
volume_diff     : true ZZZ
structural_diff : true ZZZ
```

---

## 4. Diff 種別ごとの事実【AUTO】

### 4.1 Reference Diff（事実）

* false 件数：
* 分布：複数条例に分布 / 単一条例に集中 など（※分類のみ）

### 4.2 Volume Diff（事実）

* 全件 true / 一部 false

### 4.3 Structural Diff（事実）

* 全件 true / 一部 false

---

## 5. Gate 判定【HUMAN｜必須】

> **Gate 判定：OK / △ / NG**

### 判定理由（1〜3行）

※ Observation の事実のみを根拠に記載すること
※ 評価語・原因推定は禁止

---

## 6. 判断留保・次回確認点【HUMAN｜任意】

* 本 Evaluation では判断しなかった点
* 次回 Evaluation で再確認すべき観点

---

## 7. 評価範囲外メモ【HUMAN｜任意】

※ 本 v0.1 のスコープ外だが、気づきとして残す場合のみ記載
※ **Gate 判定には影響させない**

---

## 8. 固定宣言【AUTO】

* 本記録は Observation v0.1 / Evaluation v0.1 に基づく
* 後続 Evaluation のための再解釈を意図しない

---

## 自動化前提メモ（重要）

* 【AUTO】セクションは将来 CLI / Script で生成する
* 【HUMAN】セクションのみ人手入力
* 本テンプレは **自動生成 Markdown の後段に人が追記する前提**で設計されている

---

## 自動化できる余地（今回の run から見えた点）

### 即自動化できる（v0.1.x）

* run_id / version / diff_flags 分布
* Reference / Volume / Structural の事実要約
* 「全件 true」「一部 false」の定型文生成

### v0.2 以降で検討

* Reference Diff false の分類（条・項／附則）
* 複数 run の Gate 判定比較表
* Evaluation Record JSON 正本 → Markdown 派生

---
