---
title: Design – Bundle Manifest v0.2
schema_version: design.bundle_manifest.v0.2
created_at: 2026-01-20
status: fixed
related:
  - docs/judgment/Judgment_Primary_Format_Selection_Markdown_v0.2.md
  - docs/judgment/json/judgment_primary_format_markdown_v0.2.json
---

# Design – Bundle Manifest v0.2

## 1. 本設計書の目的

本設計書は、Evaluation Bundle に含まれる  
`bundle_manifest.json` の役割・構造・運用方針を定義する。

特に v0.2 では、

- Evaluation が完了しているか
- Judgment が確定しているか

を **機械的に判定可能**とすることを目的とする。

---

## 2. bundle_manifest.json の位置づけ

`bundle_manifest.json` は、

> **Bundle の「現在地」を示す索引・状態表**

である。

本ファイルは：

- Bundle に含まれる成果物の一覧
- 各成果物の参照先
- Evaluation / Judgment の進捗状態

を示すが、

- 評価結果の内容
- Judgment の理由
- Evidence の詳細

を保持しない。

---

## 3. artifacts 配下に置く理由

`bundle_manifest.json` は  
`artifacts/evaluation/<bundle_id>/` 配下に配置される。

これは、本ファイルが：

- 実行結果に付随する生成物であり
- 再生成・上書きされる前提であり
- Git による履歴管理を期待しない

という性質を持つためである。

**履歴・正本性は docs 側で担保する。**

---

## 4. v0.2 における設計原則

### 4.1 単一正本

- Bundle 内に `bundle_manifest.json` は **常に1本**
- 複数バージョンの manifest を併存させない

### 4.2 状態の明示

Bundle の状態は、manifest 内で明示する。

- Evaluation が完了しているか
- Judgment が確定しているか

を、フラグとして保持する。

### 4.3 Judgment の独立性

Judgment は、

- Evaluation の一工程ではなく
- Bundle の終端成果物

として扱う。

そのため、Judgment JSON は  
Bundle 直下に `judgment.json` として配置される。

---

## 5. v0.2 bundle_manifest.json の構造

### 最小構成（概念）

```json
{
  "schema_version": "bundle.v0.2",
  "bundle_id": "<bundle_id>",
  "created_at": "<date>",
  "status": {
    "evaluation": "completed",
    "judgment": "decided"
  },
  "contents": {
    "evaluation": { ... },
    "judgment": { ... }
  }
}
```

---

## 6. status フィールドの定義

### evaluation

| 値 | 意味 |
| --------- | -------------- |
| running | Evaluation 進行中 |
| completed | Evaluation 完了 |

### judgment

| 値 | 意味 |
| ------- | ------------ |
| pending | Judgment 未確定 |
| decided | Judgment 確定 |

---

## 7. contents フィールドの責務

`contents` は、

- Bundle に含まれる成果物の **目録**
- 各成果物への **参照パス**
- 各成果物の **schema_version**

を列挙する。

成果物の内容説明は行わない。

---

## 8. Judgment JSON との関係

Bundle v0.2 では、

- Judgment JSON v0.2 を
  - `judgment.json` として Bundle 直下に配置
- Judgment Markdown 文書を
  - `document` として参照

する。

```json
"judgment": {
  "json": "judgment.json",
  "schema_version": "judgment.v0.2",
  "document": "docs/judgment/Judgment_Primary_Format_Selection_Markdown_v0.2.md"
}
```

Judgment の理由・背景は  
Markdown 文書側が正本となる。

---

## 9. v0.1 との主な差分

| 観点 | v0.1 | v0.2 |
| ------------- | -------------- | ---------- |
| Bundle 状態 | 不明示 | status で明示 |
| Judgment | Evaluation の一部 | Bundle 終端 |
| Judgment JSON | なし | 明示的に同梱 |
| manifest の役割 | 目録 | 目録＋状態表 |

---

## 10. 運用上の注意

- `bundle_manifest.json` は artifacts 配下に置かれるため、  
  Git 管理対象外となる場合がある
- 過去の状態・判断履歴は、  
  docs 配下の Judgment 文書および JSON により管理する
- Bundle v0.2 は、  
  manifest の上書きを前提とする

---

## 11. 本設計の適用範囲

本設計は、以下に適用される。

- Evaluation Bundle v0.2
- Judgment JSON v0.2 を含む Bundle

将来、Bundle v0.3 以降で複数 Judgment を扱う場合は、  
本設計を拡張する。

---
