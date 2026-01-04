---
title: Design_Execution_Input_Contract_v0.2
version: v0.2
status: ready-for-freeze
project: reiki-rag-converter
related_epic: Epic 7
created: 2026-01-03
author: Sumio Nishioka & ChatGPT
tags:
  - execution-input-contract
  - design
  - rag-evaluation
  - customized-question-set
---

# Design: Execution Input Contract v0.2

## 1. Purpose（本設計の目的）

本設計書は、  
**条例別カスタマイズ質問セット（customized_question_set.json）**を  
**Execution Input Contract（実行入力契約）**として  
長期的・継続的に生成・消費・比較可能な状態で運用するための  
**v0.2 設計仕様**を定義する。

本 Contract は、生成AI（RAG）応答挙動を  
**再現可能に観測・比較するための入力資産**として位置づけられる。

---

## 2. Scope & Non-Scope

### 2.1 Scope（対象）

- customized_question_set.json の構造・意味論
- Consumer（CLI / CI / 評価基盤）向け解釈ルール
- v0.1 Contract の非破壊拡張

### 2.2 Non-Scope（対象外）

- 質問生成ロジックの変更
- CLI / ログ / UX 改善
- RAG 応答結果・評価スコア
- Golden Question Pool / Golden Ordinance Set の変更

---

## 3. Design Goals（設計ゴール）

### 根拠となるロードマップ文言（引用）

Roadmap v1.2 では、本プロジェクトの役割を次のように定義している：

> **生成AIテスト自動化と連携し、  
> RAG 応答挙動を再現可能に観測するための  
> 入力資産生成基盤**

また、2026年Q1〜Q2 の必須条件として：

> customized_question_set が  
> **Execution Input Contract として  
> 継続的に生成・消費可能**

と明示されている。

---

### 🎯 Execution Input Contract v0.2 の設計ゴール

**Execution Input Contract v0.2** は、
Epic 6 までに確立された v0.1 Contract
（customized_question_set.json）を **破壊せずに維持**したまま、

> **条例別カスタマイズ質問セットを
> 長期的・継続的に生成・消費・比較可能な
> 評価観測入力資産として成立させる**

ことを目的とする。

そのため、v0.2 は **新たな実行能力を追加するものではなく**、
次の点を設計ゴールとする。

---

#### 1. 契約の役割を「成果物」から「制度」へ昇格させる

v0.1 Contract は、

- JSON構造
- 不変条件（Invariant）
- テストによる保証

を備えた **完成した成果物**である。

v0.2 ではこれを一段階引き上げ、

- なぜこの質問集合が生成されたのか
- 何をカバーし、何を意図的にカバーしないのか
- 将来どのような拡張が想定されているのか

を **Contract 自身が説明可能な状態**にする。

---

#### 2. v0.1 Consumer との完全後方互換を保証する

v0.2 Contract は以下を厳守する：

- v0.1 の必須フィールド・意味・Invariant を変更しない
- v0.1 Consumer は **一切の修正なし**で v0.2 を消費できる
- v0.2 で追加される要素は **すべて optional** とする

これにより、

> **Contract の進化が
> 下流（gov-llm-e2e-testkit / CI / RAG評価）を破壊しない**

状態を保証する。

---

#### 3. 「評価観測入力」としての意味論を明示する

v0.2 Contract は、質問セットを単なる入力データではなく、

> **生成AI応答挙動を観測・比較・再現するための
> 実行入力契約（Execution Input Contract）**

として明確に位置づける。

そのため、

- question_set_id の識別性
- 元 Question Pool との関係
- 条例別カスタマイズにおける選択・除外の方針

といった **意味論的メタデータ**を追加可能とする。

---

#### 4. 将来 Contract（v0.3 / v1.0）への拡張余地を確保する

v0.2 は最終形ではない。

- 表特化質問
- HTML差分観測質問
- 複数 Question Pool 併存
- 評価軸別 Question Set

といった **将来の拡張**を見据え、

- schema_version の役割を明確化
- 無視可能フィールドの扱いを定義
- 「解釈してはいけない情報」の境界を定める

ことで、Contract の寿命を延ばす。

---

### 🚫 v0.2 で意図的に行わないこと（再確認）

本設計ゴールに基づき、v0.2 では以下を行わない：

- 質問生成ロジックの意味変更
- 実行結果に影響する仕様変更
- CLI / ログ / UX の改善
- Golden Ordinance Set / Golden Question Pool の変更

これらは **別 Epic の責務**とする。

---

### 🧩 位置づけのまとめ（1文）

> **Execution Input Contract v0.2 は、
> v0.1 で確立された入力契約を破壊せずに、
> 長期運用・比較・進化を可能にするための
> “意味論と拡張余白”を与える設計フェーズである。**

---

## 4. Design Principles（設計原則）

### Principle 1 **Backward Compatibility First（完全後方互換）**

Execution Input Contract v0.2 は、
v0.1 Contract の **必須フィールド・意味・Invariant を一切変更しない**。

- v0.1 Consumer は **無修正で v0.2 を消費できなければならない**
- 既存テスト・CI・Golden diff はそのまま成立すること

👉 **後方互換が壊れる変更は v0.2 の時点で禁止する**

---

### Principle 2 **Non-breaking Extension Only（非破壊拡張のみ）**

v0.2 における拡張は、以下に限定される：

- optional フィールドの追加
- 解釈補助・識別性向上のための metadata
- 将来拡張のための予約領域

**実行結果・質問内容・生成ロジックの意味を変える変更は禁止**。

---

### Principle 3 **Execution Semantics over Data Shape（形より意味）**

Contract の価値は JSON 構造そのものではなく、

> **生成AI応答挙動を
> 再現・比較・観測するための
> 実行入力としての意味**

にある。

そのため v0.2 では、

- なぜその質問集合が存在するか
- どの前提で解釈されるべきか

といった **意味論（Semantics）を優先**して設計する。

---

### Principle 4 **Explicit Ignore Rules（無視してよいことを明示）**

v0.2 Contract は、Consumer に対して次を保証する：

- v0.2 で追加された optional フィールドは
  **未対応 Consumer が無視してよい**
- 無視された場合でも Contract の成立性は損なわれない

👉
**「読まなくていい情報」を明示することも Contract の責務**とする。

---

### Principle 5 **Invariant Preservation（不変条件の継承）**

Epic 6 までに確立された Invariant は、
v0.2 においても **無条件に継承される**。

特に：

- 条 ≥1 の条例において
  **質問集合が空になることを禁止**
- fail-fast による異常検出

これらは **Contract の基盤条件**であり、
v0.2 設計の検討対象外とする。

---

### Principle 6 **Traceability as a First-class Concern（追跡可能性）**

Execution Input Contract は、
「どこから来た入力か」を説明できなければならない。

そのため v0.2 では：

- 元 Question Pool
- 条例別カスタマイズの判断根拠
- question_set_id の意味論

といった **追跡可能性（Traceability）**を
第一級の設計要素として扱う。

---

### Principle 7 **Future Contracts Must Coexist（将来版との共存）**

v0.2 は最終形ではない。

- v0.3 / v1.0
- 派生 Question Set
- 複数 Contract 併存

が **同一リポジトリ・同一CI・同一評価基盤で共存する**ことを前提に、

- schema_version の責務を限定
- 解釈してはいけない領域を定義
- Contract 同士を比較可能な設計

とする。

---

### 🚫 原則として禁止される設計判断（まとめ）

以下は **Design Principles 違反**とみなす：

- v0.1 Consumer に修正を要求する設計
- optional でないフィールド追加
- 「とりあえず入れておく」未定義フィールド
- 実行挙動に影響する metadata
- ログ・UX 改善を Contract に混入させること

---

### 🧩 原則の一文要約

> **Execution Input Contract v0.2 は、
> v0.1 を壊さず、意味を明確にし、
> 将来と共存できる最小限の拡張だけを許す。**

---

## 5. Contract Overview（全体像・参照起点）

本章は、**Execution Input Contract v0.2 全体の参照起点（Single Entry Point）**として、
本 Contract に含まれるフィールド群を **役割別に俯瞰**することを目的とする。

詳細な定義・制約・禁止事項は、
**第6章（Core Fields）**および **第7章（Extension Fields）**に委譲する。

---

### 5.1 基本方針（再確認）

Execution Input Contract v0.2 は、以下の原則に基づいて構成される。

- v0.1 Contract の構造・意味を **完全に保持**する
- v0.2 で追加される要素は **非破壊的拡張**に限定する
- 実行意味を持つフィールドは **明示的に限定**する
- 未対応 Consumer が **安全に無視できる設計**とする

---

### 5.2 ルート構造（トップレベル）

```jsonc
{
  "schema_version": "0.2",
  "question_set_id": "...",
  "target_ordinance_id": "...",
  "questions": [ ... ],

  // --- v0.2 Extension ---
  "metadata": { ... },
  "coverage": { ... }
}
```

本構造は、
**Core Fields（中核フィールド）**と
**Extension Fields（拡張フィールド）**の二層構造を取る。

---

### 5.3 フィールド分類（Core / Extension）

本 Contract に含まれるフィールドは、
**役割と Consumer に対する要求水準**に基づき、次の2区分に分類される。

#### Core Fields（中核フィールド）

- Contract の成立に **必須**
- すべての Consumer が **必ず理解・処理**しなければならない
- v0.1 から **意味・存在ともに不変**

#### Extension Fields（拡張フィールド）

- Contract の説明性・追跡性を高めるための **補助情報**
- 未対応 Consumer は **解釈せず無視してよい**
- 実行結果・評価挙動に **影響を与えてはならない**

---

### 5.4 フィールド分類一覧（参照用）

| フィールド名 | 区分 | 実行意味 | Consumer 必須対応 |
| --------------------- | --------- | ------- | ------------- |
| `schema_version` | Core | No | Yes |
| `question_set_id` | Core | No | Yes |
| `target_ordinance_id` | Core | No | Yes |
| `questions` | Core | **Yes** | Yes |
| `metadata` | Extension | No | No |
| `coverage` | Extension | No | No |

> **実行意味を持つフィールドは `questions` のみである。**

---

### 5.5 実行意味と非実行情報の境界

Consumer は、本 Contract を解釈する際、
次の境界を **明確に区別**しなければならない。

- **実行意味を持つ情報**
  → `questions`
- **実行意味を持たない情報**
  → Core / Extension を問わず、`questions` 以外のすべて
   （ただし識別・構造解釈・検証のための情報は含む）

この境界は **Contract の不変条件**であり、
以降の章（特に Consumer Rules）における判断基準となる。

---

### 5.6 後続章との対応関係

- **第6章：Core Fields**
  → Core Fields 各要素の定義・制約・Invariant
- **第7章：Extension Fields**
  → metadata / coverage の厳密定義（許容・禁止）

本章では、
**「何がどこに定義されているか」だけを示し、
詳細仕様には踏み込まない。**

---

### 第5章の一文要約

> **第5章は、Execution Input Contract v0.2 の全体構造と役割分担を示す
> 参照起点（Single Entry Point）である。**

---

## 6. Core Fields（中核フィールド）

本章では、Execution Input Contract v0.2 を成立させるために
**必須かつ中核となるフィールド（Core Fields）**について、
それぞれの **意味・制約・不変条件**を定義する。

Core Fields は、
**すべての Consumer が必ず理解し、適切に取り扱わなければならない要素**であり、
v0.1 Contract から **意味・役割ともに不変**である。

---

### 6.1 Core Fields 一覧（再掲）

| フィールド名 | 実行意味 | Consumer 必須対応 |
| --------------------- | ------- | ------------- |
| `schema_version` | No | Yes |
| `question_set_id` | No | Yes |
| `target_ordinance_id` | No | Yes |
| `questions` | **Yes** | Yes |

> 実行意味を持つフィールドは **`questions` のみ**である。

---

### 6.2 `schema_version`

#### 6.2.1 定義

```json
"schema_version": "0.1" | "0.2"
```

#### 6.2.2 意味

`schema_version` は、
**Execution Input Contract の解釈ルールを識別するためのフィールド**である。

- Contract の **構造的・意味的解釈方法**を示す
- 質問内容や実行結果そのものには **影響しない**

#### 6.2.3 制約

- 文字列型であること
- `"0.1"` または `"0.2"` を取る
- 数値型・セマンティックバージョンは禁止

#### 6.2.4 Invariant / 解釈ルール

- Consumer は `schema_version` を
  **解釈ルール選択のためだけに使用**しなければならない
- 未対応の `schema_version` を検出した場合でも、
  **未知の部分を解釈しようとせず、処理を継続**することを前提とする

---

### 6.3 `question_set_id`

#### 6.3.1 定義

```json
"question_set_id": "customized_question_set:<target_ordinance_id>:<set_version>"
```

#### 6.3.2 意味

`question_set_id` は、
**質問集合そのものの同一性を恒久的に識別するための識別子**である。

- 比較・保存・参照のキーとして使用される
- 実行制御や条件分岐のための情報ではない

#### 6.3.3 制約

- 固定 namespace `customized_question_set` を使用する
- `target_ordinance_id` と完全一致する ID を含む
- `<set_version>` は `v` + 正の整数とする

#### 6.3.4 Invariant / 解釈ルール

- `question_set_id` は **文字列としてのみ比較**してよい
- Consumer は内容をパースしてはならない
- `schema_version` の変更によって
  `question_set_id` を変更してはならない

---

### 6.4 `target_ordinance_id`

#### 6.4.1 定義

```json
"target_ordinance_id": "k518RG00000022"
```

#### 6.4.2 意味

`target_ordinance_id` は、
**本 Contract が対象とする条例を一意に識別するためのフィールド**である。

- Execution Input Contract の適用対象を定める
- Golden Ordinance Set / 実データ双方で使用される

#### 6.4.3 制約

- 文字列型であること
- 条例 ID の正規表現・桁数は別途定義された規則に従う
- `question_set_id` 内の条例 ID と **完全一致**すること

#### 6.4.4 Invariant / 解釈ルール

- Consumer は `target_ordinance_id` を
  条例単位の識別・紐付けにのみ使用する
- 実行入力の内容や実行順を切り替える条件として使用してはならない

---

### 6.5 `questions`

#### 6.5.1 定義

```json
"questions": [
  {
    "question_id": "Q1",
    "text": "この条例の目的を説明してください。"
  }
]
```

#### 6.5.2 意味

`questions` は、
**Execution Input Contract における唯一の実行入力**である。

- Consumer は本配列の内容を
  そのまま生成AI等への入力として使用する

#### 6.5.3 制約

- 配列型であること
- 各要素は v0.1 で定義された question オブジェクトに従う
- 配列の並び順は **意味を持つ**

#### 6.5.4 Invariant（最重要）

- `questions` は **空配列であってはならない**
- 条 ≥1 の条例において、
  **必ず1つ以上の質問が存在する**

これらの Invariant に違反する Contract は、
**生成段階で fail-fast とする**。

#### 6.5.5 解釈ルール

- Consumer は `questions` を
  **そのまま実行入力として信頼**しなければならない
- 再検証・補正・再解釈を行ってはならない

---

### 6.6 Core Fields に関する総則

- Core Fields は **Contract の成立条件そのもの**である
- v0.2 においても
  **追加・削除・意味変更は行わない**
- Core Fields に変更が入る場合は
  **Contract のメジャーバージョン更新を要する**

---

### 第6章の一文要約

> **第6章は、Execution Input Contract v0.2 を成立させる
> 中核フィールドの意味と不変条件を厳密に定義する章である。**

---

## 7. Extension Fields（拡張フィールド）

本章では、Execution Input Contract v0.2 において
**拡張フィールド（Extension Fields）として定義される要素**について、
それぞれの **意味・許容される内容・禁止事項**を定義する。

Extension Fields は、Contract の **説明性・追跡性・将来共存性**を高めるための
**非実行情報**であり、
Contract の成立条件や実行意味には影響しない。

---

### 7.1 Extension Fields 一覧（再掲）

本章では、Extension Fields の内部キーについて  
厳密な構造定義は行わない。
これは、Extension Fields が将来の拡張・変更を前提とした  
説明専用情報であるためである。

| フィールド名 | 目的 | 実行意味 | Consumer 必須対応 |
| ---------- | ------- | ---- | ------------- |
| `metadata` | 来歴・背景説明 | No | No |
| `coverage` | 対象範囲の説明 | No | No |

> Extension Fields は、未対応 Consumer によって
> **解釈されず、挙動に影響を与えなくても Contract は成立する**

---

### 7.2 `metadata`

#### 7.2.1 定義

```json
"metadata": {
  "source_question_pool": {
    "id": "GQPA",
    "version": "v1.1"
  },
  "generation_policy": "ordinance-specific customization",
  "generated_at": "2026-01-03T10:12:45Z",
  "notes": "附則構造を考慮してQ8を残した"
}
```

#### 7.2.2 意味

`metadata` は、
**当該質問セットがどのような背景・判断に基づいて生成されたか**を
人間に説明するための情報である。

- 実行制御や評価のための情報ではない
- Consumer が参照しなくても Contract の意味は変わらない

---

#### 7.2.3 許容される内容

`metadata` には、以下のような情報を含めてよい。

- 使用した Question Pool の識別情報
- 質問セット生成時の設計方針の要約
- 生成時刻（参考情報）
- 設計者・レビューア向けの補足メモ

これらはすべて
**人間の理解・追跡のための情報**である。

---

#### 7.2.4 制約

- すべて **任意項目**とする
- 値は原則として **文字列または単純なオブジェクト**
- 数値評価・閾値・条件分岐を意図した構造を含めてはならない

---

#### 7.2.5 禁止事項

`metadata` に、以下を含めてはならない。

- 実行条件・分岐条件となる情報
- 評価結果・スコア・品質指標
- RAG 応答内容やモデル設定
- Consumer の挙動を変える意図を持つ情報

---

### 7.3 `coverage`

#### 7.3.1 定義

```json
"coverage": {
  "articles": {
    "covered": [1, 2, 3, 5],
    "excluded": [4]
  },
  "appendix": {
    "included": true
  },
  "policy": "最低1条以上を必ず対象とする"
}
```

#### 7.3.2 意味

`coverage` は、
**本質問セットが条例のどの範囲を意図的に扱っているか**を
人間に説明するための情報である。

- 網羅性・完全性・品質を保証するものではない
- 自動評価や合否判定の根拠としては使用しない

---

#### 7.3.3 許容される内容

`coverage` には、以下の情報を含めてよい。

- 主に対象とした条番号
- 意図的に対象外とした条番号
- 附則を対象に含めたかどうか
- カバレッジ判断に用いた設計上の原則（自然言語）

---

#### 7.3.4 制約

- 条番号は **正の整数**で表現する
- `covered` と `excluded` は **重複してはならない**
- 数値スコア・割合・自動判定を含めてはならない

---

#### 7.3.5 禁止事項

`coverage` に、以下を含めてはならない。

- 網羅率・達成率などの定量評価
- 合否・十分性・品質を示す表現
- Consumer の実行挙動を左右する条件情報

---

### 7.4 Extension Fields に関する総則

- Extension Fields は **Contract の説明責務を担う**
- Core Fields の代替や補完として使用してはならない
- 将来の Contract 拡張では
  **Extension Fields の追加が優先される**

---

### 第7章の一文要約

> **第7章は、Execution Input Contract v0.2 における
> 非実行情報（Extension Fields）の意味と境界を定義する章である。**

---

## 8. Identifier Semantics（識別子の意味論）

本章では、Execution Input Contract v0.2 における
**識別子（Identifier）に関する意味論と設計原則**を定義する。

ここで扱う識別子は、Contract を
**保存・比較・参照・追跡**するための基盤であり、
実行入力そのものではない。

---

### 8.1 本章の位置づけ

Execution Input Contract には、複数の識別子が含まれるが、
それらはすべて次の性質を共有する。

- Contract の**同一性**を示す
- 実行内容や挙動を**規定しない**
- Consumer の条件分岐に**使用してはならない**

本章では、その代表として
**`question_set_id` の意味論を中心に**定義を行う。

---

### 8.2 `question_set_id` の役割

### 8.2.1 定義

```text
customized_question_set:<target_ordinance_id>:<set_version>
```

#### 8.2.2 意味

`question_set_id` は、
**特定の条例に対して定義された質問集合そのものを
恒久的に識別するための識別子**である。

この識別子が示すのは：

- 「どの条例に対する質問セットか」
- 「どの版（世代）の質問セットか」

であり、
**どのように生成されたか／どう実行するか**
を示すものではない。

---

### 8.3 `question_set_id` が示さないもの

`question_set_id` は、以下を**一切示さない**。

- schema_version
- 質問生成ロジック
- metadata / coverage の内容
- 実行結果・品質・評価
- RAG モデルや設定

これらの情報は、
**別フィールドまたは別 Contract の責務**である。

---

### 8.4 構成要素と制約

`question_set_id` は、以下の要素から構成される。

| 要素 | 意味 | 制約 |
| ------------------- | ----------- | ----------- |
| namespace | Contract 種別 | 固定文字列 |
| target_ordinance_id | 対象条例 | フィールド値と完全一致 |
| set_version | 質問集合の世代 | `v` + 正の整数 |

#### 設計原則

- 省略・短縮・意味付けの追加は禁止
- **人間が読める形式ではあるが、意味の解釈や推測を前提としない**

---

### 8.5 set_version の意味論

`set_version` は、
**質問集合としての同一性が保てなくなったときのみ更新**する。

#### 更新すべきケース

- 質問内容が変わった
- 質問数が変わった
- 質問の並び順が変わった

#### 更新してはならないケース

- schema_version の更新
- metadata / coverage のみの変更
- 生成時刻・備考の変更

---

### 8.6 schema_version との関係

| 観点 | schema_version | question_set_id |
| ---- | -------------- | --------------- |
| 役割 | 解釈ルール | 同一性識別 |
| 変更理由 | Contract 仕様変更 | 質問集合の意味的変更 |
| 相互依存 | なし | なし |

両者は **独立した軸**で管理されなければならない。

---

### 8.7 Consumer に対する解釈原則

Consumer は、`question_set_id` に対して次を守らなければならない。

- 文字列として比較・保存してよい
- 内容を分解・解釈してはならない
- 実行入力の内容や実行順を切り替える条件として使用してはならない

識別子は **識別のためにのみ存在する**。

---

### 8.8 Identifier Semantics の設計意図

本章を独立させた目的は、
次の設計判断を明示することにある。

- Identifier は **実行意味を持たない**
- Identifier は **Contract の安定性を担保する**
- Identifier の意味論は **長期にわたり不変であるべき**

この意味論を共有することで、
Contract は長期的な比較・保存・再利用に耐える。

---

### 第8章の一文要約

> **第8章は、Execution Input Contract における
> 識別子の意味論を定義し、
> 同一性と実行意味を明確に分離する章である。**

---

## 9. Invariants（不変条件）

本章では、Execution Input Contract v0.2 において
**常に満たされていなければならない不変条件（Invariants）**を定義する。

これらの Invariants は、
Contract の生成・保存・消費・比較のすべての局面において
**前提条件として信頼されるべき性質**である。

---

### 9.1 Invariants の位置づけ

Invariants は、次の性質を持つ。

- Contract の**成立条件そのもの**である
- Consumer が**再検証・補正する対象ではない**
- 破られた場合、**生成段階で fail-fast とする**

Invariants は、
第5〜8章で定義された設計原則・意味論を
**運用レベルで固定化したもの**である。

---

### 9.2 実行意味に関する Invariants

#### 9.2.1 実行意味を持つフィールドは `questions` のみである

- `questions` 以外のすべてのフィールドは
  **実行意味を持たない**
- Core / Extension の区分にかかわらず、この原則は不変である

この Invariant により、
実行入力と説明情報の境界が明確に保たれる。

---

#### 9.2.2 `questions` の並び順は意味を持つ

- `questions` は **順序付きの配列**として扱われる
- 並び順の変更は、質問集合としての同一性を破壊する

---

### 9.3 構造に関する Invariants

#### 9.3.1 `questions` は空配列であってはならない

- 条が1つ以上存在する条例において、
  `questions` は **必ず1件以上の要素を含む**
- 空配列の Contract は **不正**とみなす

この条件に違反する Contract は、
**生成段階で fail-fast とする**。

---

#### 9.3.2 Core Fields は常に存在する

以下のフィールドは、
**すべての Execution Input Contract に必ず存在**しなければならない。

- `schema_version`
- `question_set_id`
- `target_ordinance_id`
- `questions`

---

### 9.4 識別子に関する Invariants

#### 9.4.1 `question_set_id` は質問集合の同一性のみを表す

- `question_set_id` は、
  質問集合そのものの同一性を識別するためのものである
- 生成方法・実行方法・評価結果を含意してはならない

---

#### 9.4.2 `schema_version` と `question_set_id` は独立である

- `schema_version` の変更は、
  `question_set_id` の変更理由にはならない
- 両者を連動させてはならない

---

### 9.5 Extension Fields に関する Invariants

#### 9.5.1 Extension Fields は実行意味を持たない

- `metadata` / `coverage` は
  **説明専用の非実行情報**である
- Contract の成立・実行・評価に影響してはならない

---

#### 9.5.2 Extension Fields の有無で Contract の意味は変わらない

- Extension Fields が存在しない場合でも
  Contract は完全に成立する
- 未対応 Consumer により解釈されなくても
  Contract の意味は変化しない

---

### 9.6 Consumer に対する前提条件

Consumer は、次を **前提条件として信頼**しなければならない。

- 本章で定義された Invariants は常に満たされている
- Consumer は Invariants を再検証・補正してはならない
- Invariants に反する Contract が与えられた場合でも、
  **Consumer 側で回復処理を行ってはならない**

Invariant の担保責任は、
**Contract の生成側にある**。

---

### 9.7 Invariants 違反の扱い

- Invariants に違反する Contract は
  **不正な Execution Input Contract**とみなす
- 不正な Contract は
  比較・評価・CI の対象として使用してはならない

---

### 第9章の一文要約

> **第9章は、Execution Input Contract が
> 常に満たすべき不変条件を集約し、
> 生成側と Consumer 側の責務境界を固定する章である。**

---

## 10. Consumer Interpretation Rules（Consumer の解釈規則）

本章では、Execution Input Contract v0.2 を**消費（Consume）するすべての Consumer**が
**必ず守るべき解釈規則（Interpretation Rules）**を定義する。

本規則は推奨ではなく、**Contract の一部として拘束力を持つ**。

---

### 10.1 Consumer の定義

本 Contract における Consumer とは、
`customized_question_set.json` を読み込み、
その内容を用いて **実行・評価・観測・保存・比較**を行う
あらゆるプログラム・スクリプト・ツールを指す。

---

### 10.2 解釈の基本原則

Consumer は、Execution Input Contract を解釈するにあたり、
以下を**前提条件として信頼**しなければならない。

- 第9章で定義された **Invariants は常に満たされている**
- Contract の生成責務は **Consumer の外部にある**
- Consumer は **入力を補正・再解釈しない**

---

### 10.3 Do（必ず行うこと）

#### 10.3.1 `questions` のみを実行入力として扱う

- 実行意味を持つフィールドは **`questions` のみ**である
- Consumer は `questions` の内容と並び順を
  **そのまま実行入力として使用**しなければならない

---

#### 10.3.2 未知フィールドを安全に無視する

- 未知のキーや未対応の Extension Fields が存在しても
  **エラーとして扱ってはならない**
- 未知の部分を解釈しようとせず、処理を継続すること

これは、Contract の **前方互換性を担保するための必須要件**である。

---

#### 10.3.3 `question_set_id` を識別子としてのみ扱う

- `question_set_id` は **文字列として比較・保存**してよい
- Contract の同一性判定にのみ使用する

---

#### 10.3.4 `schema_version` を解釈ルール選択にのみ使用する

- `schema_version` は Contract の **解釈方法を選択するための情報**である
- 実行入力の内容や実行順を変更する目的で使用してはならない

---

### 10.4 Don’t（行ってはならないこと）

#### 10.4.1 optional / Extension Fields で挙動を変えてはならない

- `metadata` / `coverage` の有無や内容によって
  **実行内容・評価方法・実行順を変更してはならない**

---

#### 10.4.2 Identifier を分解・解釈してはならない

- `question_set_id` を分割・解析し、
  条例 ID や世代情報を取り出してはならない
- 正式フィールド（`target_ordinance_id` 等）を使用すること

---

#### 10.4.3 Invariants を再検証・回復処理してはならない

- Consumer は Invariants を **信頼する側**である
- Invariants に反する Contract が与えられた場合でも、
  **Consumer 側で補正・回復を行ってはならない**

---

#### 10.4.4 Contract に含まれない情報を仮定してはならない

- 実行モデル
- RAG 設定
- 評価基準
- 実行環境

これらは **Contract の責務外**である。

---

### 10.5 違反時の扱い

本章の規則に違反する Consumer は、

- Execution Input Contract に **非準拠**
- 比較結果・評価結果の **信頼性を保証できない**
- CI / 自動評価において **サポート対象外**

とみなされる。

---

### 第10章の一文要約

> **第10章は、Execution Input Contract を消費する側が
> 何を信頼し、何をしてはならないかを確定する章である。**

---

## 11. Versioning Policy

| 項目 | 役割 |
| --------------- | ----- |
| schema_version | 解釈ルール |
| question_set_id | 同一性識別 |

両者は独立して管理される。

---

## 12. Future Outlook

- v0.3：表特化・HTML差分観測対応
- v1.0：LTS / 長期凍結 Contract

---

## 13. Summary（一文要約）

> Execution Input Contract v0.2 は、
> v0.1 を壊さず、意味と追跡性を与え、
> 将来の Contract と共存できる入力契約である。

---
