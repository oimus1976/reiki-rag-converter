# Qommons.AI テスト自動化

## 成果物インターフェース定義 v0.1r+（FIX）

```yaml
version: v0.1r+
status: fixed
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

※ 本成果物における `Golden_*` の指定は参照・識別目的であり、
Golden 資産を CI や定期処理などの自動実行対象に含めること、
また品質判定や PASS/FAIL を決定するゲートとして用いることを
意味しない。

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

同一条件で複数回実行した場合は、
**各実行ごとに run_id を分け、N 回分を N ファイルとして記録する。**

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
schema_version: v0.1r+

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

`knowledge.files` には、
当該観測において **実際に Qommons.AI に投入された主要なファイル**を列挙する。
投入されたすべての補助ファイルや内部参照を完全に網羅することは
要求しない。

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
* 推測・補完は禁止
* UI 表示に現れた事実のみを記述する

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
  （**CI とは独立した評価・設計判断用のゲート**）
* 差分比較
* 設計仮説検証
* Golden 更新判断

※ 本インターフェース定義は、
これらの評価・判断方法を **一切規定しない**。

---

## 10. バージョニング方針

* v0.1：初版
* v0.1r：品質要件の用語修正
* v0.1r+：誤解防止・行為否定・解釈補足（本書）
* **v1.0：生成・収集の自動化を想定した安定版**
* v1.x：後方互換を維持した拡張

---

## 11. 一文サマリー（最終）

> **本成果物は、
> 評価を行うための一次観測データであり、
> 生成・収集は将来自動化され得るが、
> 判定や Gate は常に CI 外で行われる。**

---
