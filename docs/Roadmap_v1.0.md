---
title: Roadmap
version: v1.0
doc_type: status
project: reiki-rag-converter
created: 2025-12-05
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - roadmap
  - planning
  - oss
  - reiki-rag-converter
---

# reiki-rag-converter — Roadmap v1.0

本ドキュメントは、条例HTML → Markdown/TXT → RAG（検索）向け最適化パイプラインである  
**reiki-rag-converter プロジェクトの公式ロードマップ（固定版）**である。

ChatGPT との対話で都度揺れるロードマップを排除し、  
**今後は本書を唯一の参照点として開発を進める。**

変更は **GitHub 上での Pull Request により明示的に行う**。

---

# 1. 現行バージョン（安定版）

## 1.1 実装モジュール

- **convert_reiki_v2.7**  
  - 条・項・号・表（単純構造）を 100% 抽出  
  - 複数附則対応  
  - synthetic_html（P01〜P15）に対し Golden diff を確保

- **validate_reiki_structure_v0.5.3**  
  - set → list 変換により JSON 互換問題を解消  
  - Sイベント（S1〜S3）の安定検出  
  - exit code を 0 に固定（CI 安定化）

- **synthetic_html（P01〜P10：legacy / P11〜P15：generator）**  
  - P01〜P10：人手で最適化された Golden パターン  
  - P11〜P15：synthetic_generator_v0.2 により自動生成

- **CI（GitHub Actions）**  
  - smoke test（test_smoketest.py）  
  - e2e（meta → validate → convert → diff）  
  - SKIP_E2E=true 時の exit code 問題を解消

---

# 2. 次期バージョン計画（短期：v2.8 / v0.6 系）

## 2.1 convert_v2.8（短期）

- 表の **colspan / rowspan** への正式対応
- 別記様式（iframe / 画像 / PDFリンク）の変換改善
- ul/li 混入時のハイブリッド構造に強いロジックへ改良
- synthetic_html_v0.2（P11〜）での実データ拡大テスト

---

## 2.2 validate_v0.6（短期）

- Sイベント体系の拡張  
  - chapter（編構造）  
  - form, PDF, iframe の識別  
- 改正文モデルの抽象化準備  
- synthetic_html（P11〜P15）の構造整合性テストの導入

---

## 2.3 synthetic_generator_v0.3（短期）

- DOM揺れテンプレートを追加  
  - title-irregular / span.cm / nested div 等の再現  
- meta.json に `"version": "v0.2"` の明示を要求（誤読防止）
- 新規 synthetic パターン P16〜P20 を定義し、coverage を拡大

---

# 3. 中期計画（v3.x / v1.x 系）

## 3.1 convert_v3.0

- 条・項・号の **アンカーID体系を安定化**（RAG最適化）
- Markdownアウトラインの再設計（長文条例に強い構造）
- 大規模条例（100KB〜）向けの **chunking 最適化**

---

## 3.2 validate_v1.0

- 改正文・読み替え・施行期日管理への正式対応
- 例外体系 E100〜E120 の整理と統合
- ルールベース + モデルベースの **ハイブリッドバリデータ**

---

## 3.3 synthetic_generator_v1.0

- 自治体ごとの DOM 揺れテンプレート切り替え  
  （政令市・県・町村で DOM の癖が異なることを吸収）
- meta → HTML → Markdown の round-trip 完全保証
- synthetic_html の拡大（P01〜P50 体系）

---

# 4. 長期計画（自治体RAG統合フェーズ）

## 4.1 法令データ RAG プラットフォーム

- 条例 → Markdown → Embedding → Query → Citation  
- 条・項・号・表・附則の粒度で検索可能  
- 改正文の時系列管理（“施行日ベースの検索”）

---

## 4.2 オープンソース化準備

- コード基盤の一般化  
- synthetic_html の公開用最低限版を整備  
- 法的観点を踏まえたライセンス選定（MIT / Apache 2.0）

---

# 5. メンテナンス方針（固定）

- **P01〜P10**  
  - 不変の Golden パターン（変更禁止）

- **P11 以降**  
  - synthetic_generator による進化パターン（更新可）

- CI  
  - smoke test が存在すること  
  - E2E が常に green であること  
  - 破壊的変更時は Golden diff の更新プロセスを必須とする

- ロードマップ  
  - 本書は version 固定  
  - 変更は PR によってのみ行う  
  - ChatGPT との回答も本書に準拠して行う

---

# 6. 次回アップデート（v1.1 予定）

- convert_v2.8 の正式仕様書  
- synthetic_generator_v0.3 の meta 拡張案  
- validate_v0.6 の構造イベント分類案  
- Golden diff（P11〜P15）維持手順書

---

# 7. 付録：ディレクトリ構成（標準）

```

reiki-rag-converter/
├─ src/
├─ synthetic_html/
│    ├─ P01〜P10（legacy固定）
│    ├─ P11〜（generator）
├─ synthetic_html_meta/
│    ├─ v0.1_legacy/
│    └─ v0.2/
├─ docs/
│    ├─ Roadmap_v1.0.md
│    ├─ Design_convert_v2.x.md
│    ├─ Design_validate_v0.x.md
│    └─ Design_synthetic_generator_v0.2.md
└─ tests/
├─ test_smoketest.py
└─ e2e/

```
```

---
