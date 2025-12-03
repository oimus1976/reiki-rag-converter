---
title: 例外チェックツール設計書（v3.1）
version: 3.1
status: active
updated: 2025-12-01
project: reiki-rag-converter
---

# 例外チェックツール設計書 v3.1

本書は、例規HTML解析における **構造検証・例外検出ツール（validate）** の  
バージョン **v3.1** の設計内容をまとめたものである。

v3 → v3.1 の差分として **構造イベント集計（structure_summary.json）** を追加し、  
convert_reiki の設計に資する「構造パターンの全体像」を明らかにすることを目的とする。

---

# 1. 目的

v3.1 の目的は以下の通り。

- 例規集HTMLを機械的に解析し、構造の揺れ・例外を検出する  
- 条・項・号、附則、表（table）、リスト（ul/li）などの出現位置を記録する  
- convert_reiki の設計に必要な **構造イベントの全体集計** を生成する  
- 将来的な例外E006X群（表・リストの異常配置）に備えた基盤整備

---

# 2. スコープ

## 2.1 本ツールが行うこと

- HTML 内の `.eline` を解析し、構造要素を抽出
- 例外（E001/E003/E004/E007 …）の検出
- 構造イベント（S1～S3）の検出
- 各条例ごとの JSON ログ出力
- 全条例の横断集計  
  - `summary_report.json`  
  - `class_statistics.json`  
  - `structure_summary.json`（v3.1 追加）

## 2.2 本ツールが行わないこと

- Markdown 変換（convert_reiki の責務）
- 表の再構成・正規化  
- データ補正やAI向けの整形

---

# 3. 入出力

## 3.1 入力

- 対象HTML：DVD収録の例規集HTML（`*.html`）
- 起動パラメータ  
```

python validate_reiki_structure_v0.5.2.py --source "E:/reiki_honbun"

```

## 3.2 出力

すべてローカル作業フォルダに保存される。

### 条例ごとのログ：  
```

logs_v3_1/exceptions/{条例ID}.json

```

### サマリファイル
```

logs_v3_1/summary_report.json
logs_v3_1/class_statistics.json
logs_v3_1/structure_summary.json  ← v3.1の新機能

````

---

# 4. KNOWN_CLASSES（v2系）

```python
KNOWN_CLASSES = {
    "eline", "article", "clause", "item", "num", "title",
    "title-irregular", "date", "number", "p", "s-head",
    "table_frame", "table-wrapper",
    "b-on", "bb-on", "br-on",
    "l-edge", "r-edge", "t-edge", "b-edge",
    "fixed-colspec",
    "inline", "quote", "xref_frame",
    "cm", "word-space", "top", "start",
    "none", "close", "open", "noicon",
    "main_rules", "supplement"
}
````

---

# 5. 例外体系（E 系）

* **E001**：未知 class
* **E003**：公布日欠落
* **E004**：条例番号欠落
* **E007**：`#primaryInner2` 欠落
* **E006X**：表／リストの異常配置（※v3.1では未実装、今後追加）

---

# 6. 構造イベント（S 系）

### **S1: table_in_main**

本則中で `<table>` を検出（補足：in_supplement=False）

### **S2: table_in_supplement**

附則中で `<table>` を検出（補足：in_supplement=True）

### **S3: ul_in_item**

`.eline` 内に `<ul>` または `<li>` を検出

※ 親子関係の厳密チェックは v3.1 では簡易版。

---

# 7. JSONログ形式

条例ごとに以下の形式でログを出力する：

```json
{
  "exceptions": ["E003"],
  "structures": [
    { "event": "table_in_main", "index": 9 }
  ],
  "classes": ["eline", "article", "num"]
}
```

---

# 8. structure_summary.json（新規）

集計イメージ：

```json
{
  "table_in_main": {
    "count": 12,
    "laws": [
      { "id": "k518RG00000080", "indexes": [9] }
    ]
  },
  "ul_in_item": {
    "count": 25,
    "laws": [
      { "id": "k518RG00000012", "indexes": [5, 7] }
    ]
  }
}
```

---

# 9. メイン処理フロー

1. HTML 読み込み
2. `#primaryInner2`→`.eline` 抽出
3. class 検出＋未知クラス→E001
4. 公布日／番号チェック（E003/E004）
5. `.s-head` による附則判定
6. 表構造→S1/S2
7. リスト構造→S3
8. JSONログ保存
9. 総合サマリー生成（v3.1）

---

# 10. 利用シナリオ

* convert_reiki の詳細設計
* 条例全体の DOM 揺れ把握
* 表／リスト出現傾向を可視化
* synthetic データ生成の判断材料
* RAG向けデータ整形に必要な構造の基礎分析

---

# 11. 今後の拡張

* E006X：表・リスト位置の異常詳細化
* 条・項・号の階層モデル v0.6 への布石
* 表解析ロジック（rowspan/colspan 判定）との連動強化
