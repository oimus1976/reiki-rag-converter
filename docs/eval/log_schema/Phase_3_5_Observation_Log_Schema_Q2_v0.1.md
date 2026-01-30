---
title: Phase 3.5 Observation Log Schema (Q2 / S1)
version: v0.1
status: draft
phase: phase-3.5
scenario: S1
question_id: Q-S1-02
doc_type: log-schema
project: reiki-rag-converter
created: 2026-01-26
author: Sumio Nishioka + ChatGPT
scope:
  - observation-log
  - schema
  - naming-convention
excludes:
  - artifacts
  - execution-results
  - judgment
---

# Phase 3.5 Observation Log Schema (Q2 / S1) v0.1

## 0. 位置づけ

本書は Phase 3.5 において、質問 **Q-S1-02**（S1: 条件 × 金額表）を対象に生成される観測ログの

- **正本（JSON）**
- **横断集計（CSV）**
- **人間レビュー（Markdown）**

の **型（schema）と命名規約**を定義する。

本書は **生成データ（artifacts）を含まない**。  
生成データは `artifacts/` 配下に出力し、本書は docs として固定される。

---

## 1. 適用範囲

- Phase: **3.5**
- Scenario: **S1**
- Question: **Q-S1-02**
- 対象: 「区分 × 金額（表の行）を列挙させる」タイプの質問

---

## 2. 命名規約（FIX候補）

### 2.1 run_id

`run_id` は Phase 3.5 の 1回の実行単位を一意に識別する。

**形式**

```text
p35_<YYYYMMDD>_<ordinance_id>_<scenario>_<seq>
```

**例（example）**

```text
p35_20260125_k518RG00000200_S1_01
```

- `p35`: Phase 3.5 固定
- `YYYYMMDD`: 実行日（ローカル日付）
- `ordinance_id`: 対象条例 ID
- `scenario`: `S1` 固定（本書の対象）
- `seq`: 同日複数 run 対策の連番

### 2.2 question_id

- `Q-S1-02` を固定で使用する（文言修正があっても ID は不変）

### 2.3 ファイル名

観測ログは A/B 構成ごとに **1回答 = 1ファイル**とする。

**形式**

```text
observation_<run_id>_<mode>.<ext>
```

- `<mode>`:

  - `A_md`（Markdown 単独）
  - `B_md_csv`（Markdown + CSV 併用）
- `<ext>`:

  - `json` / `md`

集計 CSV は run ごとに 1本。

**形式**

```text
observation_summary_<run_id>.csv
```

---

## 3. 比較構成（mode）

- **A_md**: Markdown 単独
- **B_md_csv**: Markdown + CSV 併用

---

## 4. JSON 正本ログ（schema）

### 4.1 目的

JSON は観測ログの **正本**であり、後続フェーズで機械的・横断的に参照できることを目的とする。
「正しい／間違い」「優劣」等の判断語を含めない。

### 4.2 フィールド定義

#### 4.2.1 ルート

| key | type | required | description |
| ------------------ | -----: | :------: | ------------------------ |
| schema_version | string | yes | 例: `observation.q2.v0.1` |
| phase | string | yes | `3.5` |
| run_id | string | yes | 命名規約に従う |
| scenario | string | yes | `S1` |
| question_id | string | yes | `Q-S1-02` |
| ordinance_id | string | yes | 対象条例 ID |
| mode | string | yes | `A_md` or `B_md_csv` |
| answer_text | string | yes | 生成回答（原文） |
| table_expectation  object | yes | 期待する区分（行）定義 |
| table_observation | array | yes | 区分ごとの観測 |
| reference_behavior | object | yes | 参照行動の観測 |
| observations | object | yes | 横断フラグ（欠落/混在など） |
| meta | object | no | 観測者メモ（判断ではない） |

#### 4.2.2 table_expectation

| key           |          type | required | description   |
| ------------- | ------------: | :------: | ------------- |
| expected_rows | array[string] |    yes   | Q2 が要求する区分名一覧 |

**expected_rows（example）**

- 工事又は製造の請負
- 財産の買入れ
- 物件の借入れ
- 財産の売払い
- 前各号以外

※ これは Q2 固定の期待値。表記揺れは `notes` に記録し、勝手に正規化しない。

#### 4.2.3 table_observation（配列）

要素は区分（category）ごとに 1つ。

| key            |        type | required | description                 |
| -------------- | ----------: | :------: | --------------------------- |
| category       |      string |    yes   | 区分名（expected_rows の要素に対応）   |
| amount_present |     boolean |    yes   | 回答内に当該区分の金額が提示されているか        |
| amount_value   | string|null |    no    | 金額表現（原文）。未記載/不明は null 可     |
| source         |      string |    yes   | `markdown` / `csv` / `none` |
| notes          |      string |    no    | 事実メモ（判断語禁止）                 |

#### 4.2.4 reference_behavior

| key               |          type | required | description                    |
| ----------------- | ------------: | :------: | ------------------------------ |
| mentions_table    |       boolean |    yes   | 表への言及があるか                      |
| mentions_article  | array[string] |    no    | 条文参照（例: `第84条第3項`）             |
| csv_used          |       boolean |    yes   | mode により決まる（A=false / B=true）  |
| extraction_status |        string |    yes   | `none` / `partial` / `success` |

#### 4.2.5 observations（横断フラグ）

| key                       |    type | required | description          |
| ------------------------- | ------: | :------: | -------------------- |
| missing_category          | boolean |    yes   | 期待区分の欠落があるか          |
| mixed_category            | boolean |    yes   | 区分と金額の混在（取り違え疑い）があるか |
| representative_value_bias | boolean |    yes   | 代表値に引きずられた兆候があるか     |

※ いずれも「正誤」ではなく「兆候」の観測フラグ。

#### 4.2.6 meta（任意）

| key      |   type | required | description      |
| -------- | -----: | :------: | ---------------- |
| observer | string |    no    | 例: `human`       |
| notes    | string |    no    | 判断・結論ではなく、観測補助メモ |

---

## 5. CSV 集計ログ（schema）

### 5.1 目的

CSV は run 内で A/B を横断比較し、集計・可視化に利用する。
CSV は JSON の派生であり、正本ではない。

### 5.2 列定義

```csv
run_id,mode,category,amount_present,source,missing_category,mixed_category,representative_value_bias
```

- `category` は `table_observation.category`
- `missing_category` 等の横断フラグは JSON `observations` から転記

---

## 6. Markdown レビューログ（schema）

### 6.1 目的

Markdown は人間が A/B の差分をレビューしやすい形で保持する。
Markdown は JSON の派生であり、正本ではない。

### 6.2 必須構成（見出し）

- YAML frontmatter（run_id, question_id, mode）
- 質問本文（Q2）
- 回答原文（引用）
- 区分別テーブル（区分 / 金額提示 / 情報源 / メモ）
- 観測サマリ（欠落・混在・代表値引きずり・表参照）

---

## 7. 記述ルール（共通）

- **判断語禁止**（例: 正しい／誤り／適切／不適切／合格／不合格）
- 事実・挙動・参照関係のみ記録する
- 表記揺れは正規化せず、notes に残す
- `mode` は必ず A/B のどちらかを明示する

---

## 8. artifacts の出力先（参考）

生成データは `artifacts/` 配下に出力すること。
docs/ 配下に生成データを配置しない。

（例）

```text
artifacts/evaluation/phase_3_5/<run_id>/
  observation_<run_id>_A_md.json
  observation_<run_id>_B_md_csv.json
  observation_summary_<run_id>.csv
  observation_<run_id>_A_md.md
  observation_<run_id>_B_md_csv.md
```
