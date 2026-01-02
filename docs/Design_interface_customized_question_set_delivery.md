---
title: Design_interface_customized_question_set_delivery
version: v0.1
status: fixed
doc_type: interface_note
project: reiki-rag-converter
audience:
  - ai_test_automation_project
  - integration_partner
scope:
  - customized_question_set_delivery
  - responsibility_boundary
  - execution_input_contract
created: 2026-01-02
author: Sumio Nishioka
related_docs:
  - Design_Master.md
  - Design_Note_Question_Instantiation.md
  - Qommons_Test_Artifact_Interface_v0.1r+
notes:
  - This document defines delivery contract and responsibility boundaries.
  - This is not an evaluation specification nor an implementation spec.
---

# 生成AIテスト自動化プロジェクト向け

**条例別カスタマイズ質問セット提供仕様・責務整理（FIX版）**

reiki-rag-converter × 生成AIテスト自動化 連携文書

---

## 1. 本文書の目的

本書は、reiki-rag-converter プロジェクトと
生成AIテスト自動化プロジェクトとの連携において、

* これまでの設計検討の経緯
* 責務分担の整理
* 今後、テスト自動化プロジェクトへ提供する
  **質問セットの仕様と位置づけ**

を明文化し、
**誤解・責務逆流・実装迷子を防止すること**を目的とする。

本書は評価方法・アルゴリズム・実装詳細を定義しない。

---

## 2. 背景とこれまでの経緯

### 2.1 ゴールデン質問セットの従来位置づけ

これまで、評価基準として
**ゴールデン質問セット**（抽象的な質問母集団）を用意し、

* 「第○条」「第○条第○項」などの抽象表現を含む質問を
* 機械的に具体化して実行する

という運用を行ってきた
---

### 2.2 実務上顕在化した課題

運用を進める中で、以下の課題が明確になった。

* 汎用的な質問が多く、
  **評価観点として冗長・非効率**
* 最初から特定の条・項を対象とした方が
  **HTML / Markdown 差による性能差が観測しやすい**
* 抽象質問を前提とした機械展開は、
  **評価意図が伝わりにくい**

---

## 3. 基本設計方針（重要）

### 3.1 「聞きたい質問」ではない

本連携で用いられる質問は、

* 業務上の疑問
* 利用者ニーズ
* 条例の重要度

に基づくものではない。

> **HTML と Markdown の入力差によって
> 生成AIの検索・引用・到達挙動の差が
> 顕在化しやすいかどうかを観測するための
> 評価観測用入力**である。

---

### 3.2 ゴールデン質問セットの扱い

* ゴールデン質問セットは
  **評価基準・観点の母集団（凍結資産）**
* 改変・削除・最適化は行わない
* 実行時に用いる質問は、
  ゴールデン質問セットを起点に生成された
  **条例別カスタマイズ質問セット（派生物）**

---

## 4. 責務分担（FIX）

### 4.1 reiki-rag-converter の責務

reiki-rag-converter プロジェクトは、以下を担う。

* ゴールデン質問セットの保持・管理
* 評価対象とする条例（条例ID）の指定
  ※業務選定ではなく、評価観測用入力の技術指定
* 条例構造（条・項・附則有無等）の把握
* **条例別カスタマイズ質問セットの生成**
* 当該質問セットの設計意図・選定理由の説明責任

---

### 4.2 生成AIテスト自動化プロジェクトの責務

生成AIテスト自動化プロジェクトは、

* reiki-rag-converter から提供された

  * 条例ID
  * 条例別カスタマイズ質問セット

を **外部入力として受け取り**、

* そのまま実行
* 生成AIの応答を一次観測データとして記録

するのみとする。

以下は **一切行わない**。

* 条例の選定
* 質問の選定・削除・修正
* 意味解釈・評価
* PASS/FAIL や Gate 判定

---

## 5. 条例別カスタマイズ質問セット提供仕様（実装可能レベル）

### 5.1 提供単位

* **1 条例（ordinance_id）につき、1 質問セット**
* 1 run において：

  * ordinance_id
  * 条例別カスタマイズ質問セット
    が **不変の入力**として与えられる

質問セットは、実行時に分割・編集されない。

---

### 5.2 提供形態

* 質問セットは **構造化データ**として提供される
  （YAML / JSON 等、形式は実装側裁量）
* ファイル名・拡張子は本仕様では規定しない

---

### 5.3 論理データ構造（最小）

```text
customized_question_set
├─ ordinance_id        （必須）
├─ question_set_id     （必須・一意）
├─ questions[]         （必須）
│   ├─ question_id     （必須・安定）
│   └─ question_text   （必須・具体化済み）
└─ metadata            （任意）
```

* `question_id` はゴールデン質問セット由来の識別子を継承する
* `questions[]` の並び順は **意味を持つ**（実行順安定化）

---

## 付録A：customized_question_set.json 仕様（確定）

本節では、条例別カスタマイズ質問セットの成果物  
`customized_question_set.json` を  
**評価観測用の実行入力契約（Execution Input Contract）**として  
凍結するための JSON 仕様を定義する。

本仕様は、下流（生成AIテスト自動化プロジェクト）において  
**解釈・補完・修正を行わず、そのまま実行される入力契約**である。

---

### A.1 versioning 方針

`customized_question_set.json` は、  
以下の 3 層で versioning を管理する。

#### schema_version（JSON 構造の契約）

* JSON の **ルートキー**として必須
* `<artifact>.<major>` 形式のみを許容する  
  （例：`customized_question_set.v1`）
* minor / patch バージョンの概念は持たない
* **破壊的変更が発生した場合のみ** `v2` へ更新する

以下は破壊的変更に該当する：

* 必須キーの削除
* 既存キーの意味変更
* 構造階層の変更

以下は破壊的変更に該当しない：

* 任意キーの追加
* `metadata` の拡張
* 並び順に影響しない補助情報の追加

---

#### source_golden_question_pool（質問母集団の識別）

* `customized_question_set` 配下の必須キー
* 本質問セットが **どの Golden Question Pool から派生したか**を示す
* Golden Question Pool の更新時：
  * 本キーを更新する
  * **schema_version は更新しない**

Golden の変化は  
**「入力内容の変化」であり  
「JSON 構造契約の変化」ではない**。

---

#### question_set_id（人間可読な識別子）

* `customized_question_set` 配下の必須キー
* ログ・保存・比較・人間の把握のための識別子
* **機械判定・分岐には使用しない**

---

### A.2 JSON 最終構造（キー一覧・必須/任意）

#### ルートレベル

| キー名 | 必須 | 型 | 意味 |
| --- | :-: | --- | --- |
| `schema_version` | ✔ | string | JSON 構造の契約バージョン |
| `customized_question_set` | ✔ | object | 条例別カスタマイズ質問セット本体 |

---

#### customized_question_set オブジェクト

| キー名 | 必須 | 型 | 意味 |
| --- | :-: | --- | --- |
| `ordinance_id` | ✔ | string | 対象条例の識別子 |
| `question_set_id` | ✔ | string | 人間可読な質問セット識別子 |
| `source_golden_question_pool` | ✔ | string | 派生元 Golden Question Pool |
| `questions` | ✔ | array | 実行順序付き質問配列 |
| `metadata` | ✖ | object | 補助情報（非契約） |

---

#### questions[] 配列要素

※ 配列の順序は **意味を持つ（実行順）**

| キー名 | 必須 | 型 | 意味 |
| --- | :-: | --- | --- |
| `question_id` | ✔ | string | Golden 由来の安定識別子 |
| `question_text` | ✔ | string | 具体化済み質問文 |

---

### A.3 制約および禁止事項

* `questions` 配列は **1件以上を必須**とする  
  0 件となる場合は生成失敗とし、fail-fast で処理を終了する
* `question_set_id` の文字列解析に依存した分岐を行ってはならない
* `metadata` は完全に非契約情報とし、以下を含めてはならない：
  * 評価結果
  * 正誤判定
  * 除外理由
  * PASS / FAIL / Gate 判定に相当する情報
* `metadata` の追加・拡張を理由に  
  `schema_version` を更新してはならない

---

### A.4 最小構成例

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

---

## ✅ この追記ブロックの設計的メリット

- **既存設計を壊さない**
- Execution Input Contract の  
  - versioning
  - JSON構造
  - 禁止事項  
  が **1箇所に集約**
- 下流が **ここだけ読めば実装できる**

---

### 5.4 テスト自動化プロジェクト側での扱い

生成AIテスト自動化プロジェクトは：

* 質問文を **編集・最適化・要約しない**
* 質問の追加・削除・並び替えを行わない
* 質問セット全体を **ブラックボックス入力**として扱う

---

### 5.5 質問除外の扱い

質問が除外される場合：

* 条例構造上成立しないことが理由
* 意味的・業務的判断ではない
* 除外は **reiki-rag-converter 側で完結**

テスト自動化プロジェクトは
除外理由を再解釈・再判断しない。

---

### 5.6 互換性方針

* 本仕様は **後方互換を維持**する
* 項目追加は行われ得るが、

  * 既存項目の意味変更
  * 必須項目の削除
    は行わない

---

## 6. 本方針が意図すること／しないこと

### 意図すること

* HTML / Markdown 差による挙動差の観測
* 評価意図の明確化
* テスト自動化側の設計・実装容易化

### 意図しないこと

* 業務QAの最適化
* 生成AIの意味理解能力評価
* テスト側での質問生成・最適化

---

## 7. まとめ

> 今後、生成AIテスト自動化プロジェクトへ提供される質問セットは、
> reiki-rag-converter が評価観測用入力として指定した条例を前提に生成された
> **条例別カスタマイズ質問セット**である。
> テスト自動化プロジェクトは、これを判断せず実行・記録する。

---

## 8. 合意状況（記録）

本仕様について、生成AIテスト自動化プロジェクトより  
「評価観測用の実行入力契約（Execution Input Contract）として受け入れる」  
旨の回答を得ている。

本合意において、質問内容・選定理由・除外判断の再解釈や修正は行われず、  
追加の制約・変更要請はないことが確認された。

## 9. 参考資料

* Design_Note_Question_Instantiation.md
* Design_Master.md
* Qommons_Test_Artifact_Interface_v0.1r+

---
