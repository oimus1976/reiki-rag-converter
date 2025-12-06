---
title: Design_synthetic_generator_v0.2
version: v0.2
doc_type: design
project: reiki-rag-converter
created: 2025-12-05
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - design
  - convert
  - oss
  - reiki-rag-converter
---

# synthetic_generator_v0.2 設計書

## 0. 位置づけ

synthetic_generator は **例規HTMLの“人工サンプル”を自動生成するツール**である。  
本物の条例 HTML は著作権制約により GitHub で管理できないため、本プロジェクトの CI / convert / validate の主要テスト基盤は **synthetic_html** が担う。

v0.2 は以下を目標とする：

- convert_v2.7 が 100% 正しく変換できる HTML を生成する  
- validate_v0.5.3 が構造イベント・例外を正しく検出できる HTML を生成する  
- 章・条・項・号・表（colspan/rowspan 含む）・附則（複条含む）の構造を meta JSON から再現する  
- 自治体ごとに異なる DOM 揺れ（title-irregular、span.cm、eline 構造等）の再現が可能  
- synthetic_html P1〜P10 の次世代版（P11〜P15）を自動生成できる

---

# 1. 全体アーキテクチャ

```

meta.json  ──→  synthetic_generator_v0.2.py
│
▼
synthetic_html/P11.html

```

meta.json の **抽象表現（structure model）** をもとに、DVD 例規HTMLに近い DOM 構造を生成する。

主な生成対象：

- 条（article）
- 項（clause）
- 号（item）
- 表（table）
- 附則（supplement）
- タイトル・公布日・番号
- 第二画面の目次（optional）

---

# 2. meta.json の仕様（v0.2）

meta は以下の 5 つの要素で構成される：

1. **ルート情報（title/publish info/options）**  
2. **blocks（本文・附則の主要構造）**  
3. **article（条の階層構造）**  
4. **table（caption/rows/colspan/rowspan）**  
5. **supplement（複条附則を含む構造）**

---

## 2.1 ルート構造

```json
{
  "id": "P11",
  "title": "○サンプル条例",
  "promulgation": {
    "date": "平成10年3月30日",
    "number": "条例第5号"
  },
  "blocks": [ ... ],
  "options": {
    "inject_blank_elines": 0,
    "style_variation": "standard"
  }
}
```

### ■ options（v0.2は最小限）

| 項目                  | 意味                                        |
| ------------------- | ----------------------------------------- |
| inject_blank_elines | 意図的に `.eline` の空行を挿入して揺れを生成               |
| style_variation     | title-irregular / span.cm の使用など DOM 揺れセット |

---

# 3. blocks の構成要素

本文・附則・表など、HTML出力の主要構造を「ブロック」として表現する。

```
blocks = [
  {type: "article", ...},
  {type: "table", ...},
  {type: "supplement", ...}
]
```

順番は **上からそのまま HTML の表示順になる**。

---

# 4. article（条）の仕様

例規HTMLのもっとも重要な構造であり、次の階層モデルを採用する。

```json
{
  "type": "article",
  "num": 3,
  "title": {
    "text": "名称及び位置",
    "style": "irregular",         // title-irregular または title
    "position": "before"          // before | after
  },
  "clauses": [
    {
      "num": 1,
      "text": "駐車場等の名称及び位置は次の表のとおりとする。",
      "items": []
    }
  ]
}
```

### ■ 設計理由（PENTAレビュー反映）

* 条 → 項 → 号の階層を meta で明示すると、convert / validate が常に安定する
* 実HTMLの揺れ（title-irregular, span.cm など）を title.style で表現できる
* 条タイトルが「条番号の前／後」に現れるパターンを position で制御可能

---

# 5. clause（項）・item（号）

```json
{
  "num": 1,
  "text": "この条例は〜〜〜",
  "items": [
    {"num": 1, "text": "第一号の内容"},
    {"num": 2, "text": "第二号の内容"}
  ]
}
```

### 号（items）

* `(1)〜` 形式だけでなく、`一、二、三` の生成も v0.3 で拡張予定
* v0.2 では `(1)` の標準型を採用する

---

# 6. table の仕様（RAG最適化版）

表構造は以下のように抽象化する。

```json
{
  "type": "table",
  "caption": {
    "text": "第3条関係",
    "article": 3,
    "category": "一覧"
  },
  "rows": [
    [
      { "text": "名称", "colspan": 1, "rowspan": 1 },
      { "text": "位置" }
    ],
    [
      { "text": "船岡山駐車場" },
      { "text": "かつらぎ町大字西渋田372番地の5" }
    ]
  ]
}
```

### ■ 設計上の重要ポイント

* v0.2 から colspan/rowspan を正式サポート
* RAG で重要になる「何条の表か」を caption.article に明示
* 実HTMLの `<caption>` / `p.center` / `div.table_frame` の揺れは generator 側で制御

---

# 7. supplement（附則）

附則は複雑な構造（複条・経過措置・改正文）を持つが、v0.2 では次の階層モデルを採用する。

```json
{
  "type": "supplement",
  "meta": {
    "label": "附則",
    "date_raw": "平成10年3月30日",
    "number_raw": "条例第5号"
  },
  "articles": [
    {
      "num": 1,
      "clauses": [
        { "num": 1, "text": "この条例は公布の日から施行する。" }
      ]
    }
  ]
}
```

### ■ なぜ附則を article 構造にしたか？

* 多くの自治体が「附則の中に条を持つ」タイプを採用
* 改正文（例：第2条を次のように改める）の生成が容易になる
* validate で S101/S103 を正しく再現可能

---

# 8. DOM揺れの生成方針（v0.2）

v0.2 では最小限の揺れのみ正式サポートする。

| 揺れ種別                    | meta での制御              |
| ----------------------- | ---------------------- |
| title-irregular / title | article.title.style    |
| span.cm の有無             | options.title_span_cm  |
| e-line の空行混入            | inject_blank_elines    |
| 条タイトルの位置揺れ              | article.title.position |

### v0.3 で追加予定の揺れ：

* `.article` の階層入れ替え
* `p.num` と `p.title` の前後逆転
* `<div class="head">` の有無
* `<div class="article">` の中にさらに `<div>` が入る揺れ

---

# 9. HTML生成ポリシー（概要）

meta → HTML の生成は次のステップを踏む。

1. ルートの wrapper / container / primaryInner2 を固定テンプレで出力
2. blocks を順番に `.eline` 構造化して挿入
3. article は DVD 仕様の DOM を忠実に再現
4. table は `div.table_frame → table → tr → td` の完全再現
5. supplement は `.s-head` → clause の順に生成
6. options に応じて DOM 揺れを注入

---

# 10. 出力 HTML の必須DOMパターン

以下は convert/validate の正確な動作に必須である。

* `#primaryInner2` 配下に `.eline` が並ぶ
* 条は `<div class="article">` を起点に生成
* 附則見出しは `<p class="s-head">` または `.s-head span.title`
* 表は `<div class="table_frame">` → `<table>` の入れ子構造
* 号 `(1)` は `<div class="item"><p class="num"><span class="num cm">(1)</span></p>` 形式

---

# 11. CI / Golden Diff への適合性

synthetic_html_v0.2 は次を満たす必要がある：

* convert_v2.7 で Markdown 出力が安定
* validate_v0.5.3 で構造イベントが再現
* smoke test（tests/test_smoketest.py）にて **最低1件は常に生成されること**
* P11〜P15 が今後の Golden diff 基盤となる

---

# 12. 今後の拡張（v0.3〜v1.0）

| バージョン | 内容                              |
| ----- | ------------------------------- |
| v0.3  | DOM揺れ拡張、条・項・号の異体字生成、list構造の混在表現 |
| v0.4  | 改正文モデル（附則の中の読み替え・削除・挿入など）       |
| v0.5  | 別記様式（iframe/PDF/画像リンク）の生成       |
| v1.0  | “自治体ごとの揺れテンプレート” を選択可能にする       |

---

# 13. まとめ

synthetic_generator_v0.2 は、以下の点でプロジェクトの基盤を強化する：

* 例規HTMLの共通構造（条・項・号・表・附則）をデータモデル化
* convert / validate / CI の 3層に対して安定したテストデータを供給
* 実条例を扱わずに網羅的な検証が可能
* 将来の自治体揺れ対応や法令改正文抽象化の基礎となる
* RAG最適化のためのメタデータ（caption.article など）を追加

今後はこの仕様に基づき、
**P11〜P15 の meta JSON → synthetic_html → Golden diff** を構築する。

---

# Appendix. meta.json スケルトン（雛形）

```json
{
  "id": "PXX",
  "title": "○サンプル条例",
  "promulgation": {
    "date": "令和X年X月X日",
    "number": "条例第X号"
  },
  "blocks": [
    {
      "type": "article",
      "num": 1,
      "title": {"text": "目的", "style": "irregular", "position": "before"},
      "clauses": [
        {
          "num": 1,
          "text": "この条例は〜〜〜",
          "items": []
        }
      ]
    }
  ],
  "options": {}
}
```

```

---
