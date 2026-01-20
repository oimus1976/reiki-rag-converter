---
title: Design_Evaluation_Auto_Result
version: v0.2
status: FIX
scope: evaluation
role: auto_result_schema
---

# Design: Evaluation AUTO Result（v0.2）

## 1. 目的

本ドキュメントは、Evaluation フェーズにおける  
**AUTO（自動生成）評価結果の正本データ構造**を定義する。

Evaluation AUTO Result は、

- Observation 成果物を入力とし
- 差分の「事実」を集約するのみで
- 良否判断・意味付け・評価結論を一切含まない

**評価判断は HUMAN フェーズの責務**とする。

---

## 2. 位置づけと責務分離

### 2.1 全体構造

```text
Observation Result（JSON）
↓
Evaluation AUTO Result（JSON）  ← 正本
↓
Evaluation Record（Markdown）   ← 表示用（派生）
```

### 2.2 本成果物の責務（AUTO）

- diff_flags の分布を集計する
- Reference Diff に関する「事実のみ」を要約する
- 評価・解釈・合否判断は **行わない**

---

## 3. 出力物の契約（ディレクトリ）

```text
<out_dir>/
├── evaluation_auto.json      # Evaluation AUTO Result（正本）
└── Evaluation_Record.md      # 表示用 Markdown（派生）
```

- ファイル名は **固定**
- バージョン管理は JSON 内の `schema_version` によって行う

---

## 4. JSON スキーマ定義（v0.2）

### 4.1 トップレベル

```json
{
  "schema_version": "0.2",
  "run_id": "string",
  "generated_at": "YYYY-MM-DD",
  "source": { ... },
  "summary": { ... },
  "diff_flags_summary": { ... },
  "reference_diff_facts": { ... },
  "notes": { ... }
}
```

---

### 4.2 メタ情報

```json
"schema_version": "0.2",
"run_id": "eval_auto_YYYY-MM-DD_xx",
"generated_at": "2026-01-20"
```

- `schema_version`：AUTO Result の構造バージョン
- `run_id`：Evaluation 実行単位の識別子

---

### 4.3 source

```json
"source": {
  "observation_version": "v0.1",
  "evaluation_procedure_version": "v0.1"
}
```

- 入力元となる Observation / 手順のバージョンを明示する

---

### 4.4 summary

```json
"summary": {
  "total_observations": 230
}
```

- Observation 件数のみを記録する

---

### 4.5 diff_flags_summary（事実集計）

```json
"diff_flags_summary": {
  "reference_diff": { "true": 185, "false": 45 },
  "volume_diff":    { "true": 230, "false": 0 },
  "structural_diff":{ "true": 230, "false": 0 }
}
```

- Observation に含まれる `diff_flags` を **そのまま集計**
- 正規化・再解釈・重み付けは禁止

---

### 4.6 reference_diff_facts（AUTO で許可された追加集計）

```json
"reference_diff_facts": {
  "false_count": 45,
  "ordinance_count": 8
}
```

- Reference Diff = false の件数
- 影響を受けた条例数

※ 内容は **Observation から直接導出可能な事実のみ**

---

### 4.7 notes

```json
"notes": {
  "interpretation": "prohibited"
}
```

- 本 JSON が **評価・解釈を含まない**ことを明示するための宣言

---

## 5. 明示的に「やらない」こと（重要）

Evaluation AUTO Result では以下を行わない。

- diff の良否判断
- 差分の意味付け
- HTML / Markdown の再解釈
- Observation の再計算
- run 間の比較・時系列評価

これらは **Evaluation Framework / HUMAN フェーズの責務**とする。

---

## 6. テストと保証

- 本スキーマは `pytest` により自動検証される
- `evaluation_auto.json` は CI / ローカル実行の双方で同一契約を持つ
- Markdown 表示は JSON の派生物であり、正本ではない

---

## 7. 将来拡張方針

- 構造変更は `schema_version` を更新して行う
- v0.2 では後方互換を考慮しない
- 拡張は **Evaluation 実行後に必要性が確認されてから**行う

---
