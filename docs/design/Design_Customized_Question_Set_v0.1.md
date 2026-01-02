---
title: Design_Customized_Question_Set
version: v0.1
status: fixed
origin_issue: #1
project: reiki-rag-converter
last_updated: 2026-01-02
---

## 1. 概要

本書は、条例別カスタマイズ質問セットの成果物  
`customized_question_set.json` を  
**評価観測用の実行入力契約（Execution Input Contract）**として  
凍結するための設計仕様を定義する。

本仕様は、JSON の最終構造および versioning 方針を確定し、  
下流（生成AIテスト自動化プロジェクト）が  
解釈・補完・修正を行わず、そのまま実行できる入力契約を提供することを目的とする。

---

## 2. 背景 / 問題意識

- 条例別カスタマイズ質問セットは  
  業務QAではなく、**評価観測用の実行入力**である
- YAML / JSON の揺れや versioning の曖昧さは、  
  後方互換・回帰観測・CI において事故要因となる
- `question_set_id` に version 情報を埋め込むだけでは  
  機械的に判定できず、将来の拡張で破綻しやすい

---

## 3. 目的

- 公式成果物を JSON に固定し、  
  キー名・最小必須・順序意味・versioning を凍結する
- 将来のフィールド追加を許容しつつ、  
  **破壊的変更を明確に区別できる設計**を成立させる

---

## 4. スコープ

### 4.1 本設計で行うこと

- JSON 最終構造（キー名・必須 / 任意）の確定
- `schema_version` の導入および運用ルールの確定
- `source_golden_question_pool` の導入および運用ルールの確定
- Execution Input Contract としての凍結宣言

### 4.2 本設計で行わないこと

- テスト自動化プロジェクト側の I/F 設計変更
- Golden Question Pool（凍結資産）の改変

---

## 5. 設計方針

- 公式成果物は `customized_question_set.json` とする（JSON 固定）
- ルートに `schema_version` を配置する
- `source_golden_question_pool` により質問母集団を識別する
- `question_set_id` は人間可読の識別子とし、機械判定には使用しない

---

## 6. versioning 方針（確定）

### 6.1. 基本原則

条例別カスタマイズ質問セットの成果物
`customized_question_set.json` は、

> **評価観測用の実行入力契約（Execution Input Contract）**

として扱い、
**後方互換を最優先**とする。

そのため、versioning は以下の3層で管理する。

---

### 6.2. `schema_version`（JSON構造の契約）

#### 位置

- JSON の **ルートキー**として必須

```json
{
  "schema_version": "customized_question_set.v1",
  ...
}
```

#### 意味

- `schema_version` は
  **JSON 構造そのものの契約バージョン**を表す
- `schema_version` は `<artifact>.<major>` 形式のみを許容し、minor / patch 概念は持たない。
- 下流（生成AIテスト自動化）は
  `schema_version` を **機械的に判定**して処理を切り替える

#### 更新ルール

- `v1` → `v2` に上げるのは **破壊的変更のみ**
  - 必須キーの削除
  - 既存キーの意味変更
  - 構造階層の変更
- 以下は **v1 のまま** とする
  - 任意キーの追加
  - metadata の拡張
  - 並び順に影響しない補助情報の追加

👉
**「壊れたら v2」
「壊れなければ v1 のまま」**
という単純ルールを採用する。

---

### 6.3. `source_golden_question_pool`（質問母集団の識別）

#### 位置

- `customized_question_set` 配下の必須キー

```json
{
  "customized_question_set": {
    "source_golden_question_pool": "A-v1.1",
    ...
  }
}
```

#### 意味

- 本質問セットが **どの Golden Question Pool から派生したか**を示す
- 回帰比較・差分観測における **最重要トレーサビリティ情報**

#### 更新ルール

- Golden Question Pool が更新された場合：
  - `source_golden_question_pool` を更新する
  - **schema_version は変更しない**
- Golden の改変・最適化は行わない
  （変更が必要な場合は派生セットを新設する）

👉
**Golden の変化は
「入力内容の変化」であり
「JSON契約の変化」ではない**。

---

### 6.4. `question_set_id`（人間可読な識別子）

#### 位置

- `customized_question_set` 配下の必須キー

```json
{
  "customized_question_set": {
    "question_set_id": "cqset-k518RG00000022-A-v1.1",
    ...
  }
}
```

#### 意味

- ログ・保存・比較・人間の把握のための識別子
- **機械判定・分岐には使用しない**

#### 更新ルール

- 原則として以下を含める
  - ordinance_id
  - source_golden_question_pool
- フォーマットは人間可読性を優先し、将来変更され得る

👉
**question_set_id は「表示名」schema_version は「契約」**という役割分離を明確にする。

---

### 6.5. versioning に関する禁止事項

- `question_set_id` の文字列解析に依存した分岐
- Golden 更新を理由に `schema_version` を上げること
- 下流で version を推測・補完させる設計

---

### 6.6. 判断のまとめ（短文）

- **schema_version**
  → JSON構造の破壊的変更検知用
- **source_golden_question_pool**
  → 評価入力の母集団トレーサビリティ
- **question_set_id**
  → 人間向け識別子（非契約）

---

## 7. customized_question_set.json 最終構造

### 最終構造（キー一覧・必須/任意）【FIX】

#### 7.1. ルートレベル

| キー名 | 必須 | 型 | 意味 / 役割 | versioning との関係 |
| ------------------------- | :-: | ------ | ---------------- | --------------- |
| `schema_version` | ✔ | string | JSON 構造の契約バージョン | **破壊的変更時のみ更新** |
| `customized_question_set` | ✔ | object | 条例別カスタマイズ質問セット本体 | v1 では固定 |

---

#### 7.2. `customized_question_set` オブジェクト

| キー名 | 必須 | 型 | 意味 / 役割 | versioning との関係 |
| ----------------------------- | :-: | ------ | ------------------------ | ------------------- |
| `ordinance_id` | ✔ | string | 対象条例の識別子 | 入力データ識別 |
| `question_set_id` | ✔ | string | 人間可読な質問セット識別子 | **非契約**（機械判定に使用しない） |
| `source_golden_question_pool` | ✔ | string | 派生元 Golden Question Pool | Golden 変更時に更新 |
| `questions` | ✔ | array | 実行順序付き質問配列 | v1 で必須 |
| `metadata` | ✖ | object | 補助情報 | 任意・拡張可 |

---

#### 7.3. `questions[]` 配列要素

※ **配列の順序は意味を持つ（実行順）**

| キー名 | 必須 | 型 | 意味 / 役割 | versioning との関係 |
| --------------- | :-: | ------ | --------------- | --------------- |
| `question_id` | ✔ | string | Golden 由来の安定識別子 | Golden と 1:1 |
| `question_text` | ✔ | string | 具体化済み質問文 | 入力本文 |

---

#### 7.4. `metadata`（任意・非契約）

| キー名 | 必須 | 型 | 意味 / 役割 | 注意点 |
| -------------- | :-: | ------ | -------------------------- | ------------ |
| `generated_by` | ✖ | string | 生成元（例：reiki-rag-converter） | 下流依存禁止 |
| `generated_at` | ✖ | string | 生成日時（ISO-8601） | 比較ロジックに使用しない |
| `note` | ✖ | string | 補足説明 | 評価・判断文言は禁止 |

📌 **重要ルール**

- `metadata` は **完全に非契約**
- `metadata` には 評価結果・除外理由・正誤判断を含めてはならない。
- 下流は **存在を前提にしてはいけない**
- ここに情報を足しても `schema_version` は上げない

---

#### 7.5. 明示的な禁止事項（構造面）

- 必須キーの削除・意味変更（→ schema_version v2）
- `questions[]` の順序を意味なしとして扱うこと
- `question_set_id` を機械分岐に利用すること
- `metadata` に評価・除外理由・判定結果を入れること
- `questions` は 1件以上を必須とし、0件になる場合は生成失敗とする。

---

#### 7.6. 構造まとめ（最小形）

```json
{
  "schema_version": "customized_question_set.v1",
  "customized_question_set": {
    "ordinance_id": "k518RG00000022",
    "question_set_id": "cqset-k518RG00000022-A-v1.1",
    "source_golden_question_pool": "A-v1.1",
    "questions": [
      {
        "question_id": "A-1-Q1",
        "question_text": "この条例の目的を分かりやすく説明してください。"
      }
    ]
  }
}
```

- `schema_version` は `<artifact>.<major>` 形式のみを許容する  
  （例：`customized_question_set.v1`）。
  minor / patch バージョンの概念は持たず、
  破壊的変更が発生した場合のみ `v2` へ更新する。

- `questions` 配列は **1件以上を必須** とする。
  条例構造上すべての質問が除外される場合、
  または生成結果が 0 件となった場合は、
  `customized_question_set.json` の生成を失敗とし、
  fail-fast で処理を終了する。

- `metadata` は完全に非契約情報とし、
  以下を含めてはならない：
  - 評価結果
  - 正誤判定
  - 除外理由
  - PASS / FAIL / Gate 判定に相当する情報

---
 
## 8. 運用上の制約と禁止事項（要約）

- `questions` 配列は **1件以上必須**
- `schema_version` は破壊的変更時のみ更新
- `metadata` は非契約情報であり、評価・判定情報を含めてはならない
- `question_set_id` を機械分岐に使用してはならない

---

## 9. 本設計の状態

本設計は **status: fixed** とし、  
`customized_question_set.json` は  
Execution Input Contract として凍結される。

以後の変更は、本設計書の改訂として扱う。
