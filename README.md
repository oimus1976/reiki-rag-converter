# reiki-rag-converter  
例規HTML → AI/RAG 向け Markdown/TXT 変換ツール

[![E2E Tests](https://github.com/oimus1976/reiki-rag-converter/actions/workflows/e2e.yml/badge.svg)](https://github.com/oimus1976/reiki-rag-converter/actions)

---

## 📌 このプロジェクトについて

**reiki-rag-converter** は、地方自治体が公開する **例規集（条例 HTML）** を  
**AI/RAG 用の構造化テキスト（Markdown/TXT）へ変換する OSS ツール**です。

以下の作業を **自動化** します：

- **validate**：条例 HTML の DOM 構造を解析し、条・項・号・附則・表を検出  
- **convert**：AI/RAG が読みやすい Markdown/TXT に変換  
- **frontmatter**：条例番号・公布日・タイトル等を YAML として付与  

RAG システム（例：QommonsAI、ChatGPT・OpenAI の RAG チャットボット）での条例検索に最適化されています。

---

## 🚀 特徴（Features）

### ✔ 条・項・号を正確に抽出  
DVD 例規HTMLに最適化された DOM パターン解析。

### ✔ 附則（複数）に完全対応  
`.s-head` による附則判定、複数附則の分離が可能。

### ✔ 表（table）→ Markdown 表に変換  
簡易版（colspan/rowspan無し）だが実務では十分。

### ✔ validate → convert の構造整合テスト  
E2E テストで品質を保証。

### ✔ YAML frontmatter でメタデータ付き  
RAG の前処理として最適。

### ✔ OSS として拡張性を重視  
DOM 揺れ対応、将来の colspan 対応、改正文モデル v0.6 に対応しやすい設計。

---

## 📦 インストール

```bash
git clone https://github.com/oimus1976/reiki-rag-converter.git
cd reiki-rag-converter
pip install -r requirements.txt  # ※必要なら作成予定
````

---

## 🧪 使用方法

### 1. validate（整合性チェック）

```bash
python src/validate_reiki_structure_v0.5.2.py --source reiki_honbun --output logs_v3_1
```

出力：

* JSON ログ（exceptions / structure_summary）
* class_statistics.json
* summary_report.json

例外（E系）や構造イベント（S系）が検出されます。

---

### 2. convert（Markdown/TXT 生成）

```bash
python src/convert_reiki_v2.7.py --source reiki_honbun --output output_md
```

出力：

* `*.html.txt`（条例1件 → 1ファイル）
* YAML frontmatter 付き
* Markdown構造（条・項・号・附則・表）

---

## 📁 ディレクトリ構成

```
reiki-rag-converter/
├── src/                     # 変換エンジン
│   ├── convert_reiki_v2.7.py
│   └── validate_reiki_structure_v0.5.2.py
│
├── docs/                    # 設計書（仕様・要件・テスト）
│   ├── Design_convert_v2.6.md
│   ├── Design_exception_check_v3.1.md
│   ├── test_plan.md
│   ├── test_e2e_design.md
│   └── requirements.md
│
├── tests/                   # テストコード
│   ├── test_e2e.py
│   └── golden/              # 変換結果のゴールデンファイル
│       ├── k518RG00000012.html.txt
│       ├── k518RG00000055.html.txt
│       └── k518RG00000080.html.txt
│
├── reiki_honbun/            # 例規HTML（代表3件のみ）
├── .github/workflows/       # CI
│   └── e2e.yml
├── CHANGELOG.md
├── LICENSE
└── README.md
```

---

## 🧪 CI / E2E テスト（GitHub Actions）

このリポジトリは Push・PR 時に **自動 E2E テストが実行**されます。

### CI が行うこと：

1. Python 3.10 / 3.11 / 3.12 で test_e2e.py を実行
2. validate → convert の一括実行
3. golden ファイル（12/55/80）との **差分チェック（回帰テスト）**
4. 表の検出数 / 附則数の構造整合性チェック
5. 文字化け検査
6. 失敗時は artifacts（TXT/JSON）を保存

品質を自動で保証する仕組みです。

---

## 📚 ドキュメント（仕様書）

* [変換ロジック設計書（v2.6）](docs/Design_convert_v2.6.md)
* [例外検証ロジック（v3.1）](docs/Design_exception_check_v3.1.md)
* [テスト計画書](docs/test_plan.md)
* [E2E テスト設計書（v1.1）](docs/test_e2e_design.md)
* [要件定義書](docs/requirements.md)

---

## 📌 サンプル（reiki_honbun）

以下の3つの条例は、DVD 例規HTMLの代表パターンです：

* k518RG00000012.html
* k518RG00000055.html
* k518RG00000080.html（表あり）

E2Eテスト / 開発要件の最小セットとして同梱しています。

※ 著作権保護のため全文 HTML は GitHub への追加を制限しています。

---

## 🔄 将来の拡張（Roadmap）

* colspan/rowspan の完全対応（表モデル v3）
* 附則モデル v0.6（改正文抽出）
* 見出しと条体系の YAML 構造化
* RAG 用チャンク分割（semantic chunking）
* synthetic HTML による CI 強化
* 別記様式（image/iframe）対応
* cli ユーティリティ化（pip install 対応）

---

## 🛠 貢献（Contributing）

Pull Request・Issue 歓迎です！

品質を保つため、PR では以下が自動チェックされます：

* validate / convert が正常動作
* golden diff が一致
* E2E が Pass
* Lint（将来導入予定）

---

## 📄 ライセンス

MIT License
詳細は [LICENSE](LICENSE) を参照してください。

---

# 🙌 作者

かつらぎ町（和歌山県）で条例・行政文書のデジタル化と AI 活用を推進するプロジェクト
GitHub: [https://github.com/oimus1976](https://github.com/oimus1976)

---

**reiki-rag-converter** は、
自治体の例規集を「AI の読める形式」へと進化させるための OSS です。
ご活用・ご協力をお待ちしています。

```

---
