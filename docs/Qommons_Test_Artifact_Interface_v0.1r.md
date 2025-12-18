# Qommons.AI テスト自動化

## 成果物インターフェース定義 v0.1r（Revised）

```yaml
version: v0.1r
status: draft
role: interface_contract
scope:
  from: Qommons.AI test automation project
  to: reiki-rag-converter project
principle:
  - no_evaluation_added
  - no_interpretation_added
  - raw_observation_data
  - reproducible_execution
```

---

## 1. 目的（Purpose）

本インターフェース定義は、
**Qommons.AI テスト自動化プロジェクトが
reiki-rag-converter プロジェクトへ提供する成果物の
形式・内容・責務境界を定義する**ものである。

本成果物は、

* 評価を含まない
* 解釈を含まない
* 結論を含まない

**Qommons.AI の応答を一次観測データとして記録したもの**であり、
評価・判断はすべて reiki-rag-converter 側で行われる。

---

## 2. 責務境界（Responsibility Boundary）

### 2.1 自動化プロジェクトの責務（やること）

* 指定された実行条件で Qommons.AI に質問を送信する
* Qommons.AI が返した **回答・引用表示を改変せず取得する**
* 実行条件を **再現可能な形で記録する**
* 成果物を **未評価の観測データ**として保存する

---

### 2.2 自動化プロジェクトの禁止事項（やらないこと）

以下を **一切行ってはならない**：

* 正答／誤答の判定
* OK / NG / △ 等のラベル付け
* スコアリング
* 回答内容の要約・修正・言い換え
* 「良い／悪い」「改善した／劣化した」等の評価語の付与
* Golden 更新可否・設計妥当性に関する示唆

---

## 3. 成果物の単位（Granularity）

成果物は **1ファイル = 1観測実行単位** とする。

```text
1 観測実行単位 =
  条例 × 質問 × モデル × ナレッジ構成 × 実行条件
```

---

## 4. 成果物フォーマット（File Format）

### 4.1 基本形式

* **Markdown（必須）**
* 構造化メタデータは YAML front-matter に格納
* JSON 併設は任意（将来拡張）

---

## 5. 必須メタデータ（YAML front-matter）

```yaml
---
schema_version: v0.1r

# 実行識別
run_id: qommons-20251218-001
executed_at: 2025-12-18T14:32:00+09:00

# Qommons 実行条件
qommons:
  model: Claude 4.5 Sonnet
  web_search: off
  region: jp
  ui_mode: standard

# ナレッジ構成
knowledge:
  scope: department
  files:
    - type: txt
      name: k518RG00000064.md
    - type: csv
      name: k518RG00000064_table.csv
    - type: html
      name: k518RG00000064.html

# テスト対象
target:
  ordinance_id: k518RG00000064
  ordinance_set: Golden_Ordinance_Set_v1.0
  question_id: Q13
  question_pool: Golden_Question_Pool_A_v1.1

# 実行制御
execution:
  retry: false
  temperature: default
  max_tokens: default

---
```

---

## 6. 本文構造（Markdown Body）

### 6.1 質問（原文そのまま）

```markdown
## Question

Q13. 回答の根拠となる条文を引用して示してください。
```

---

### 6.2 Qommons.AI 回答（未評価・完全生データ）

```markdown
## Answer (Raw)

（Qommons.AI の UI 上に表示された回答全文を、
 改変せず、そのまま記録する）
```

---

### 6.3 引用・参照表示（UI 表示準拠）

```markdown
## Citations (As Displayed)

- 第3条（k518RG00000064.md）
- 附則第2項（k518RG00000064.md）
```

※ 引用が存在しない場合も
`## Citations` セクションは **必ず存在させ、空で記録**する。

---

### 6.4 観測メモ（任意・非評価）

```markdown
## Observation Notes (Optional)

- 回答が途中で終了した
- 引用表示が出なかった
- 別条例名が文字列として出現した
```

⚠️ 注意事項：

* 評価語・判断語は禁止
* 事実の記述のみ可
* 「正しい」「誤り」「良い」等の表現は禁止

---

## 7. 品質要件（Quality Requirement）

本成果物の品質は、
**評価ができないこと**ではなく、
**評価を行うための一次観測データとして十分であること**によって判断される。

以下をすべて満たすことを必須要件とする：

* 回答・引用が **Qommons.AI の表示内容と一致している**
* 実行条件が **再現可能な粒度で記録されている**
* 正誤・良否・優劣といった **評価・解釈が一切付与されていない**
* reiki-rag-converter 側が
  独自の評価基準で判断できるだけの情報が **欠落なく揃っている**

---

## 8. ファイル命名規則（推奨）

```text
YYYYMMDD/
  k518RG00000064/
    Q13/
      Claude45Sonnet_txt+csv.md
```

---

## 9. reiki-rag-converter 側の責務（参考・非拘束）

* Gate 判定
* 差分比較
* 設計仮説検証
* Golden 更新判断

※ 本インターフェース定義は、
これらの評価・判断方法を **一切規定しない**。

---

## 10. バージョニング方針

* v0.1：初版
* **v0.1r：用語修正・品質要件明確化（本書）**
* v0.2：JSON 正式化／自動差分比較対応
* v1.0：CI 連携前提の安定版

---

## 11. 一文サマリー（修正版）

> **本成果物は、
> 評価を行うための「一次観測データ」であり、
> 評価そのものを含まないことを品質要件とする。**

---

