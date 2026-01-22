---
title: Design_Judgment_JSON_v0.2
version: v0.2
status: design
category: evaluation
role: judgment-json-design
created: 2026-01-21
author: Sumio Nishioka
---

# Design Judgment JSON 正本 v0.2 設計

## 1. 本設計書の目的

本設計書は、Evaluation フレームワークにおける  
**Judgment JSON 正本 v0.2** の役割と構造を定義する。

Judgment JSON v0.2 は、

- 評価内容を記述するためのものではない
- 判断理由を説明するためのものではない

**「この判断は完了している」  
という状態を、機械的に分かる形で示すための JSON**  
として設計される。

---

## 2. Judgment JSON が必要になった背景

v0.1 までの Evaluation では、

- 観測結果（AUTO）
- 人手による解釈（HUMAN）
- 判断内容（Markdown Judgment）

が存在していたが、

- その判断が「最終かどうか」
- これ以上再解釈してよいかどうか

を **機械が判別できなかった**。

その結果、

- Bundle 間での比較が難しい
- 評価が完了しているかどうかが曖昧
- 判断文書が「メモ」なのか「確定判断」なのか分からない

という問題が残っていた。

Judgment JSON v0.2 は、  
この **「判断が確定したかどうか分からない」状態を解消するため**に導入される。

---

## 3. Judgment JSON v0.2 の役割（分かる言葉で）

Judgment JSON v0.2 がやることは **1つだけ**である。

> **この件については、もう決めた。  
> これ以上の解釈や評価は行わない。**

という状態を、  
**プログラムが確実に判別できる形で残すこと**。

---

## 4. Judgment JSON がやらないこと（重要）

Judgment JSON v0.2 は、以下を行わない。

- 判断理由の記述  
- 観測結果の要約  
- HTML / Markdown の優劣説明  
- スコア付けや評価ランク付け  
- 判断内容の再表現

これらはすべて、  
**Markdown の Judgment 文書が唯一の正本**である。

Judgment JSON は、  
Markdown Judgment を **繰り返し書かない**。

---

## 5. Markdown Judgment との役割分担

| 項目 | Markdown Judgment | Judgment JSON |
| --- | --- | --- |
| 判断理由 | 記述する | 記述しない |
| 観測内容 | 記述する | 記述しない |
| 結論の文章 | 記述する | 記述しない |
| 判断が確定した事実 | 間接的 | 明示的 |
| 機械判別 | 不可 | 可能 |

この分離により、

- 人が読むべき内容と
- 機械が判断すべき状態

を混同しない設計とする。

---

## 6. Judgment JSON v0.2 の基本設計方針

### 6.1 最小情報主義

Judgment JSON には、  
**判断が確定したことを示すために必要な最小限の情報のみ**を持たせる。

### 6.2 再解釈防止

Judgment JSON 単体を読んでも、  
判断の中身を理解できない設計とする。

判断の意味を知りたい場合は、  
必ず Markdown Judgment を参照させる。

### 6.3 再評価は新 Judgment

同一内容であっても、

- 前提条件が変わった
- 再度判断し直した

場合は、  
**新しい judgment_id を持つ Judgment JSON を作成する**。

既存 Judgment JSON は変更しない。

---

## 7. Judgment JSON v0.2 最小スキーマ（設計）

```json
{
  "schema_version": "judgment.v0.2",

  "judgment_id": "string",

  "judgment_type": "string",

  "judgment_scope": {
    "target": "string",
    "subject": "string",
    "comparison": ["string"]
  },

  "applies_to": {
    "bundle_id": "string",
    "run_ids": ["string"]
  },

  "judgment_status": "finalized",

  "judgment_reference": {
    "document": "path/to/markdown"
  },

  "declared_at": "ISO-8601 timestamp"
}
```

---

## 8. 各フィールドの意味

### schema_version

- Judgment JSON の契約バージョン
- v0.2 は初の正式 JSON 正本

### judgment_id

- Judgment を一意に識別する ID
- 再評価時は必ず別 ID

### judgment_type

- 判断の性質を示す分類用識別子
  例：

  - canonical_format_selection
  - evaluation_completion

### judgment_scope

- この判断が **何についてのものか** を明示
- 誤用・誤解を防ぐための情報

### applies_to

- この Judgment が適用される Evaluation の範囲
- どの Bundle / run を閉じたかを明確化

### judgment_status

- v0.2 では "finalized" のみを使用
- 将来拡張は想定するが、本設計では扱わない

### judgment_reference

- 判断内容が書かれた Markdown 文書への参照
- Judgment JSON 自体には意味を書かない

### declared_at

- Judgment が確定した日時
- 履歴管理・差分整理用

---

## 9. 本設計の位置づけ

Judgment JSON v0.2 は、

- 評価を自動化するための仕組みではない
- 判断の正しさを保証するものでもない

**評価プロセスを「完了状態」に遷移させるための
最終マーカー**として位置づけられる。

---

## 10. 本設計で意図的に行っていないこと

- Judgment 内容の JSON 化
- 判断理由の構造化
- Bundle 間の自動比較
- 判断の自動生成

これらはすべて、
**v0.2 以降の別フェーズまたは別プロジェクト**で扱う。

---

## 11. まとめ

Judgment JSON v0.2 は、

- 「なぜそう判断したか」を書くものではなく
- 「その判断は、もう終わっている」ことを示すためのもの

である。

人間向けの理解は Markdown Judgment に委ね、
機械向けの状態管理を Judgment JSON が担う。

この役割分担を崩さないことが、
本設計の最重要原則である。

---
