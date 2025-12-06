---
title: Design_convert_v2.6
version: v2.6
doc_type: design
project: reiki-rag-converter
created: 2025-12-01
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - design
  - convert
  - oss
  - reiki-rag-converter
---

# convert_reiki 設計書 v2.6  
（v2.7.1 の元となる基本仕様）

本設計書は、例規HTML を RAG/AI向けの Markdown/TXT に変換する  
**convert_reiki v2 系の仕様**をまとめたものである。

v2.6 は「附則直後に本文が結合する問題」など多数の不具合を修正し、  
AI が誤読しない構造を重視した安定版である。

---

# 1. 目的

- 例規HTML → Markdown風TXT への変換  
- RAG（AI検索）で高精度に扱えるよう構造を明示化  
- 条・項・号・附則・表を機械的に理解可能にする  
- YAML frontmatter にメタ情報を付与  
- 行政文書の解析・自動回答精度向上を目的とする

---

# 2. 変換対象と入力

## 2.1 入力HTMLの条件

- DVD内収録の例規HTML  
- `#primaryInner2` 配下に `.eline` が並ぶ構造  
- 条・項・号は DOM class により特定（article/clause/item）  
- 表は `<table>` および `div.table_frame` 内の `<table>`

## 2.2 変換コマンド

````

python convert_reiki_v2.7.py --source "E:/reiki_honbun" --output "output_md"

```

---

# 3. 全体フロー

```

HTML読込
↓
#primaryInner2 抽出
↓
.eline を順次処理
↓
条見出し → 項 → 号 → 本文
↓
附則（s-head）
↓
表（table）→ Markdown
↓
YAML frontmatter + 本文出力

```

---

# 4. 条レベル（article）

- `.eline` 内の `div.article` により判定  
- `<p.num><span class="num cm">第X条</span></p>`  
- `<p.title><span class="cm">（目的）</span></p>`  

### 出力形式

```

## 第X条（目的）

本文…

```

---

# 5. 項レベル（clause）

- `span.clause` 内に項の本文が入る  
- 条見出し直後に clause を抽出する必要がある（v2.7.1で修正済）

### 例

```

<p class="num">
  <span class="num cm">第1条</span>
  <span class="clause"><span class="p cm">本文</span></span>
</p>
```

---

# 6. 号レベル（item）

* `(1)` / `（1）` / `(２)` のような括弧数字で識別
* 条・項と同じ `.eline` 内に存在
* 簡易判定：行頭の括弧数字で bullet 化

### 出力形式

```
- (1) ○○○
- (2) ○○○
```

---

# 7. 附則（s-head）

* `.s-head` class で判定
* `附則（平成○年○月○日 条例第X号）` のパターンをサポート
* 複数の附則に対応（附則2、附則3…）

### 出力例

```
## 附則（平成10年3月30日条例第5号）
本文…
```

---

# 8. 表（table）

* `.table_frame table` または `<table>` を検出
* thead → tbody の順に取得
* colspan/rowspan は v2 系では簡易無視
* Markdown表として整形

---

# 9. YAML frontmatter

出力例：

```yaml
---
id: k518RG00000012
title: 駐車場条例
number: 条例第15号
promulgation_date: 平成10年3月30日
promulgation_date_normalized: 1998-03-30
source_html: k518RG00000012.html
converted_at: 2025-12-02 15:30:12
converter_version: 2.7
tags:
  - 例規
  - 条例
---
```

---

# 10. 出力仕様

* UTF-8
* `.txt` 拡張子
* 改行は `\n`
* 1ファイル＝1条例

---

# 11. 今後の拡張（v3以降）

* colspan/rowspan対応（高度化）
* 条・項・号の階層構造を YAML として別出力
* 別記様式の抽出
* 附則モデル v0.6（改正文対応）
