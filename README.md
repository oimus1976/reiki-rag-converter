# reiki-rag-converter

自治体例規（条例・規則等）の HTML を解析し、  
構造化テキストや AI 利用向けデータを生成するためのツール群です。

本リポジトリは、例規文書を **再現可能・検証可能な形で加工する**ことを目的としています。

---

## 📌 特徴

- 地方自治体の **例規HTML**（条・項・号・附則・表）を  
  **AI/RAG が扱いやすい Markdown/TXT** に自動変換する  
- validate（構造解析） → convert（変換）の2ステップ  
- YAML frontmatter で RAG 用メタデータを付与  
- E2E テスト＋Golden diffにより高品質を維持  
- QommonsAI / LangChain / ChatGPT RAG などの前処理に最適

---

## 📘 このプロジェクトについて

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

## 🧩 機能 (Features)

- ✔ **条・項・号** を DOM から正確に抽出  
- ✔ **附則（複数）** に対応  
- ✔ **表（table）** を Markdown 表に変換  
- ✔ **構造イベント（S系）と例外（E系）** を出力  
- ✔ **YAML frontmatter** でメタデータを付与  
- ✔ **validate→convert の整合性** を E2E テストで保証  
- ✔ **Golden diff** による回帰テスト  
- ✔ OSS として拡張しやすい設計（colspan・別記様式など将来拡張）

---

## 🏁 Quick Start

### 1. リポジトリの取得

```bash
git clone https://github.com/oimus1976/reiki-rag-converter.git
cd reiki-rag-converter
pip install -r requirements.txt
```

### 2. 検証（例）

```bash
python scripts/validate_html.py data/sample.html
```

### 3. 変換（例）

```bash
python scripts/convert_html.py data/sample.html
```

---

## 🔁 Customized Question Set（質問セット生成）

本プロジェクトでは、例規 HTML と Golden Question Pool を入力として、
AI テストや評価観測に利用可能な質問セット
`customized_question_set.json` を生成できます。

この質問セットは、
同一入力条件に対して **常に同一内容が生成される** よう設計されており、
CLI コマンドから再現可能に実行できます。

---

### 前提条件

- Python 3.10 以上
- 本リポジトリを clone 済み
- 依存ライブラリがインストール済み（`pip install -r requirements.txt` 等）

※ `reiki_rag_customized_question_set` は `src/` 配下に配置されているため、
リポジトリルートでコマンドを実行してください。

---

### 🛠 CLI による生成

以下の CLI を実行することで、
`customized_question_set.json` を指定したディレクトリに生成します。

```bash
python -m reiki_rag_customized_question_set.cli \
  --ordinance-html <ORDINANCE_HTML_PATH> \
  --output <OUTPUT_DIR> \
  --schema-version <SCHEMA_VERSION> \
  --target-ordinance-id <ORDINANCE_ID> \
  --question-set-id <QUESTION_SET_ID> \
  --question-pool <GOLDEN_QUESTION_POOL_ID>
```

---

### 🧾 引数一覧

| 引数                      | 説明                                              |
| ----------------------- | ----------------------------------------------- |
| `--ordinance-html`      | 対象となる条例 HTML ファイルのパス                            |
| `--output`              | 出力ディレクトリ（`customized_question_set.json` が生成される） |
| `--schema-version`      | 出力 JSON に設定される `schema_version`                 |
| `--target-ordinance-id` | 対象条例の ID                                        |
| `--question-set-id`     | 生成される質問セットの一意 ID                                |
| `--question-pool`       | 使用する Golden Question Pool の識別子                  |

※ CLI は引数の意味解釈や妥当性判断を行わず、
　指定された値をそのまま generator に渡します。

---

### 📌 生成例（既存成果物の再生成）

以下は、リポジトリ内に固定されている
`customized_question_set.json` を、
同一条件で再生成するための例です。

```bash
python -m reiki_rag_customized_question_set.cli \
  --ordinance-html data/k518RG00000022.html \
  --output artifacts/tmp_k518RG00000022 \
  --schema-version 0.1 \
  --target-ordinance-id k518RG00000022 \
  --question-set-id customized_question_set:k518RG00000022:v1 \
  --question-pool GQPA:v1.1
```

実行成功時：

```text
[OK] customized_question_set generated at: artifacts/tmp_k518RG00000022
```

---

### 🔍 再現性の確認（diff）

生成結果が既存成果物と一致することは、
以下のように確認できます。

```bash
diff -u \
  artifacts/customized_question_set/k518RG00000022/customized_question_set.json \
  artifacts/tmp_k518RG00000022/customized_question_set.json
```

`generated_at` などの非契約情報を除き、
差分が存在しないことが期待されます。

---

### ℹ 補足：Execution Input Contract について

`customized_question_set.json` は、
下流の AI テストや評価観測処理において
そのまま利用される **実行入力（Execution Input Contract）** として扱われます。

そのため、本プロジェクトでは、

* CLI は値の意味解釈を行わない
* 同一入力条件で常に同一 JSON が生成される

ことを重視しています。

仕様の更新や拡張が必要な場合は、
別フェーズ（別 Epic）として切り出して扱います。

---

## 📝 Before / After（変換例）

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

## ⚙ validate（構造解析）

```bash
python src/validate_reiki_structure_v0.5.2.py --source reiki_honbun --output logs
```

生成物：

- `summary_report.json`
- `structure_summary.json`
- `exceptions/`（E系例外）
- `class_statistics.json`

例外例:

| コード | 内容 |
| ---- | ----------------- |
| E003 | 条の欠落 |
| E004 | 順序逆転 |
| E007 | #primaryInner2 欠落 |

---

## 🛠 convert（変換）

```bash
python src/convert_reiki_v2.7.py --source reiki_honbun --output output_md
```

変換内容：

- 条・項・号の抽出
- 附則の分離
- 表（簡易）を Markdown 表へ変換
- frontmatter を付与
- UTF-8 LF に統一

---

## 📁 ディレクトリ構成

```text
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

## 🧪 CI / E2E テスト（GitHub Actions）

本リポジトリは Push/PR のたびに **validate→convert→golden diff** が自動実行されます。

CI の確認項目：

- validate の JSON 正常生成
- convert の TXT 正常生成
- golden ファイルとの完全一致（回帰テスト）
- 表・附則の構造整合性
- 文字化け防止（� の検出）
- Python 3.10/3.11/3.12 の互換性チェック

### Smoke Test 必須ポリシー

本プロジェクトでは CI（GitHub Actions）を安定稼働させるため、
必ず最低 1 件のテストが実行される必要があります。

実HTML E2E は `SKIP_E2E=true` によりスキップされるため、
テストが 0 件になると pytest の終了コードが `5` となり CI が失敗します。

そのため、以下のファイルは **削除禁止の必須テスト** と位置付けています：

```text
    tests/test_smoketest.py
```

これは CI の正常性を保証するためのインフラであり、
変更や削除を行ってはなりません。

---

## 📚 ドキュメント（主要設計書）

- [変換ロジック設計書（v2.6）](docs/Design_convert_v2.6.md)
- [例外検証ロジック（v3.1）](docs/Design_exception_check_v3.1.md)
- [テスト計画書](docs/test_plan.md)
- [E2Eテスト設計書（v1.1）](docs/test_e2e_design.md)
- [要件定義書](docs/requirements.md)

- Execution Input Contract の詳細は設計書を正本とします。

---

## ⚠ 著作権・取り扱い注意

例規HTMLは **自治体の著作物とみなされる可能性があるため**：

- リポジトリには **代表3件のみ（12/55/80）** を同梱
- 他の条例は GitHub へ直接アップロードしないことを推奨
- 必要な場合は `samples/` を **個人環境のみに配置**してください

---

## 🔄 RAG 連携例（サンプルコード）

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

## 🛠  Contributing（貢献のお願い）

PR歓迎です！
ただし品質維持のため以下を守ってください：

- E2Eテストが PASS すること
- golden diff を壊す場合は説明コメントを必須
- docs/ を更新する場合はバージョン付与
- License（MIT）に従うこと

---

## 📄 ライセンス

MIT License
詳細は [LICENSE](LICENSE) を参照してください。

---

## 🙌 作者

Sumio Nishioka
GitHub: [https://github.com/oimus1976](https://github.com/oimus1976)

---

自治体の例規集を「AI が読める形式」へ変換し、
行政文書の利活用を次のステージに進めるための OSS です。

ぜひご活用ください。

---
