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

という運用を行ってきた。
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

## 8. 参考資料

* Design_Note_Question_Instantiation.md
* Design_Master.md
* Qommons_Test_Artifact_Interface_v0.1r+

---
