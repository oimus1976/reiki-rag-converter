# reiki-rag-converter  
例規HTML → AI/RAG 向け Markdown/TXT 変換ツール

[![E2E Tests](https://github.com/oimus1976/reiki-rag-converter/actions/workflows/e2e.yml/badge.svg)](https://github.com/oimus1976/reiki-rag-converter/actions)

---

# 📌 TL;DR（まず概要）

- 地方自治体の **例規HTML**（条・項・号・附則・表）を  
  **AI/RAG が扱いやすい Markdown/TXT** に自動変換する OSS  
- validate（構造解析） → convert（変換）の2ステップ  
- YAML frontmatter で RAG 用メタデータを付与  
- E2E テスト＋Golden diffにより高品質を維持  
- QommonsAI / LangChain / ChatGPT RAG などの前処理に最適

---

# 📘 このプロジェクトについて

**reiki-rag-converter** は、市町村等が公開する **例規集 HTML** を  
**構造解析 → 変換 → AI/RAG 読み込み用テキスト** に仕上げるためのツールです。

特に地方自治体の例規は：

- HTML構造がバラバラ  
- 附則が複数存在  
- 表（table）が混在  
- 年度改正が多く細かい

といった特徴があり、**既存のHTMLパーサでは正しく扱えません**。

本ツールは、それらの事情を考慮し、

- validate（構造解析・異常検出）
- convert（条文・附則・表をMarkdownへ変換）
- RAG用frontmatter付与

をワンストップで実現します。

---

# 🧩 機能 (Features)

- ✔ **条・項・号** を DOM から正確に抽出  
- ✔ **附則（複数）** に対応  
- ✔ **表（table）** を Markdown 表に変換  
- ✔ **構造イベント（S系）と例外（E系）** を出力  
- ✔ **YAML frontmatter** でメタデータを付与  
- ✔ **validate→convert の整合性** を E2E テストで保証  
- ✔ **Golden diff** による回帰テスト  
- ✔ OSS として拡張しやすい設計（colspan・別記様式など将来拡張）

---

# 🏁 Quick Start（最短3ステップ）

## 1. クローン

```bash
git clone https://github.com/oimus1976/reiki-rag-converter.git
cd reiki-rag-converter
pip install -r requirements.txt
````

## 2. validate（構造チェック）

```bash
python src/validate_reiki_structure_v0.5.2.py --source reiki_honbun --output logs
```

## 3. convert（Markdown/TXT生成）

```bash
python src/convert_reiki_v2.7.py --source reiki_honbun --output output_md
```

---

# 📝 Before / After（変換例）

入力（HTMLの一部）：

```html
<div class="article">
  <p class="articlenum">第2条（定義）</p>
  <p class="main">この条例において…</p>
  <div class="item"><span>(1)</span> 駐車場等 …</div>
</div>
```

出力（.html.txt）：

```markdown
---
id: k518RG00000080
title: かつらぎ町駐車場条例
promulgation_date: 平成○年○月○日
---

## 第2条（定義）
この条例において、次の各号に掲げる用語の意義は…

- (1) 駐車場等 …  
- (2) 駐輪場 …
```

AI/RAG モデルが扱いやすい構造に自動変換されます。

---

# ⚙ validate（構造解析）

```bash
python src/validate_reiki_structure_v0.5.2.py --source reiki_honbun --output logs
```

生成物：

* `summary_report.json`
* `structure_summary.json`
* `exceptions/`（E系例外）
* `class_statistics.json`

例外例:

| コード  | 内容                |
| ---- | ----------------- |
| E003 | 条の欠落              |
| E004 | 順序逆転              |
| E007 | #primaryInner2 欠落 |

---

# 🛠 convert（変換）

```bash
python src/convert_reiki_v2.7.py --source reiki_honbun --output output_md
```

変換内容：

* 条・項・号の抽出
* 附則の分離
* 表（簡易）を Markdown 表へ変換
* frontmatter を付与
* UTF-8 LF に統一

---

# 📁 ディレクトリ構成

```
reiki-rag-converter/
├── src/
│   ├── convert_reiki_v2.7.py
│   └── validate_reiki_structure_v0.5.2.py
│
├── docs/
│   ├── Design_convert_v2.6.md
│   ├── Design_exception_check_v3.1.md
│   ├── requirements.md
│   ├── test_plan.md
│   └── test_e2e_design.md
│
├── tests/
│   ├── test_e2e.py
│   └── golden/
│       ├── k518RG00000012.html.txt
│       ├── k518RG00000055.html.txt
│       └── k518RG00000080.html.txt
│
├── reiki_honbun/       # 代表3件のみ（著作権配慮）
├── .github/workflows/
│   └── e2e.yml
├── LICENSE
└── README.md
```

---

# 🧪 CI / E2E テスト（GitHub Actions）

本リポジトリは Push/PR のたびに **validate→convert→golden diff** が自動実行されます。

CI の確認項目：

* validate の JSON 正常生成
* convert の TXT 正常生成
* golden ファイルとの完全一致（回帰テスト）
* 表・附則の構造整合性
* 文字化け防止（� の検出）
* Python 3.10/3.11/3.12 の互換性チェック

---

# 📚 ドキュメント（主要設計書）

* [変換ロジック設計書（v2.6）](docs/Design_convert_v2.6.md)
* [例外検証ロジック（v3.1）](docs/Design_exception_check_v3.1.md)
* [テスト計画書](docs/test_plan.md)
* [E2Eテスト設計書（v1.1）](docs/test_e2e_design.md)
* [要件定義書](docs/requirements.md)

---

# ⚠ 著作権・取り扱い注意

例規HTMLは **自治体の著作物とみなされる可能性があるため**：

* リポジトリには **代表3件のみ（12/55/80）** を同梱
* 他の条例は GitHub へ直接アップロードしないことを推奨
* 必要な場合は `samples/` を **個人環境のみに配置**してください

---

# 🔄 RAG 連携例（サンプルコード）

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import MarkdownTextSplitter

docs = []

for file in output_md.glob("*.txt"):
    loader = TextLoader(str(file), encoding="utf-8")
    docs.extend(loader.load())

splitter = MarkdownTextSplitter(chunk_size=600, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# → ベクトルDBに投入
```

---

# 🛠 Contributing（貢献のお願い）

PR歓迎です！
ただし品質維持のため以下を守ってください：

* E2Eテストが PASS すること
* golden diff を壊す場合は説明コメントを必須
* docs/ を更新する場合はバージョン付与
* License（MIT）に従うこと

---

# 📄 ライセンス

MIT License
詳細は [LICENSE](LICENSE) を参照してください。

---

# 🙌 作者

Sumio Nishioka
GitHub: [https://github.com/oimus1976](https://github.com/oimus1976)

---

自治体の例規集を「AI が読める形式」へ変換し、
行政文書の利活用を次のステージに進めるための OSS です。

ぜひご活用ください。

```

---
