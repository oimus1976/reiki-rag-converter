# Changelog
本プロジェクトにおける全変更履歴をまとめた公式 CHANGELOG です。  
バージョン管理は Keep a Changelog に準拠しています。

---

## v0.6.0 (2025-12-07)

### Added

- Qommons.AI 連携方針を PROJECT_GRAND_RULES.md に正式追加  
  - 対応RAGは Qommons.AI を第一級対象とすることを明文化  
  - HTML がタグ削除 → プレーンテキスト → 文字数チャンク化される仕様を前提に設計  
  - TXT（Markdown互換）＋CSV（説明行付き）を標準出力形式とする運用ルールを追加  
  - モデル選択（Claude 4.5 Sonnet / PLaMo 2.1 Prime 推奨）および Web検索OFF の標準化  
  - ナレッジ範囲（共有・非公開・所属部署）の制約と「単一ファイル選択モード」の扱いを明記

- RAG / Qommons.AI 要件を requirements.md に拡張  
  - TXT⇔CSV 連携（相互参照・語彙同期）を必須要件として追加  
  - 別表CSV では 1 行目ヘッダー必須・説明行の挿入を要件化  
  - RAG検索精度基準（正答＋部分正答＝80%以上）を具体化  
  - 国内リージョンモデル＋Web検索OFF を標準テスト設定と定義

- Qommons.AI 結合テスト計画を test_plan.md に新規追加  
  - 質問シナリオ（RAG-01〜06）を整備  
  - TXT/CSV 版と HTML 版の比較テストを標準化  
  - ノイズファイル混在時の回帰テスト手順を追加  
  - Golden質問セットを GOLDEN_POLICY に統合する方針を明示

### Changed

- .gitignore を強化し、著作権配慮のため **実条例HTML（samples/ / reiki_honbun/）を完全に Git 管理外に**  
- test_html_set/ や __pycache__/ など生成物フォルダを ignore 対象に追加  
- docs/PROJECT_GRAND_RULES.md / docs/requirements.md / docs/test_plan.md を Qommons.AI 前提の最新仕様に更新  
- プロジェクト全体の RAG 前提を「一般RAG → Qommons.AI 最適化」へ変更（設計方針の重大変更）

### Fixed

- ドキュメント例外指定の !docs/** などが誤ってデータを拾う可能性があったため、安全なパス粒度へ調整  
- RAG要件の不十分だった部分（モデル・ナレッジスコープ・前処理仕様）を明確化し、仕様の不整合を解消

### Notes

- convert_v2.8（colspan/rowspan対応）の設計は Qommons.AI 仕様を踏まえて再定義予定  
  - 「HTMLそのままでもある程度動く」→「CSV化で構造を保証し、検索を安定させる」へ方向性転換  
- GOLDEN_POLICY_v1.0 に Qommons.AI 章を今後正式追加する

---

## [2025-12-06] Documentation & Governance Update（本スレッド）

### Added

- **ChatGPT_Startup_Template_v1.0**  
  - ChatGPT の開発モード・人格・行動規則の正式化
- **ChatGPT_Startup_Workflow_v1.0**  
  - /start 起動プロセス、状態再構築、SSoT（PROJECT_STATUS）の仕組みを標準化
- **AI_Development_Standard_v1.0**  
  - OSS で AI を利用する際の包括的ガイドラインを制定
- **PROJECT_GRAND_RULES.md**（更新版）
  - Startup Workflow との連動ルールを正式追加

### Updated

- **docs/** 配下すべての Markdown に **frontmatter（拡張版 C案）** を統一適用  
- **PROJECT_STATUS.md** を最新状態に整理  
  - Completed / Pending / Next Action の全体再構成  
  - Startup 系文書の追加を反映
- **.github/workflows/e2e.yml**
  - Golden diff における `converted_at` 差分除外フィルターを追加  
  - CI の安定運用をさらに強化

### Improved

- プロジェクト運用基盤が **4層体系**（Template / Workflow / GRAND_RULES / STATUS）で確立  
- ChatGPT の誤作動防止（状態ズレ、Next Action逸脱）が制度的に保証されるようになった
- OSS プロジェクトとして長期保守が可能な構造へ進化

---

## v0.5.3 (2025-12-06) — validator 安定化

### Validate Module

- FIX: JSON 出力時 `set` が含まれると serialization error → `_to_serializable()` 導入で解消
- FIX: `write_json()` を安全な JSON データ専用に変更
- IMPROVED: validate の終了コードが常に `0` となり CI が完全安定

### Test / CI

- synthetic_html（P1〜P10）がすべて validate v0.5.3 に対応
- e2e.yml が新仕様へ刷新され、CI 全体の安定性が向上

### Documentation

- **Design_exception_check_v3.2** を公開  
  - イベント／例外モデルの再整理  
  - JSON 出力仕様（set → list）の公式反映

---

## [Unreleased]（履歴統合済のため説明のみ）

- synthetic_html v0.2 系統（P1〜P10 相当）の準備  
- meta templates / generator v0.1 の試験投入

---

## v2.7.1-doc3 — 2025-12-04

### Added

- `requirements.txt` 追加  
- `.gitignore` 更新（requirements.txt を追跡対象に）

---

## v2.7.1-doc2 — 2025-12-04

### Documentation

- README v1.1 に全面更新  
- CI/E2E/GitHub Actions の説明を最新版に統合

---

## v2.7.1-doc1 — 2025-12-04

### Documentation

- `docs/test_e2e_design.md` v1.1 へ更新  
- 異常系テスト A01〜A06 を追加
- Golden diff の方針を正式化

---

## v2.7.1 — 2025-12-03

### Added

- **convert_reiki_v2.7.py** 公開  
- 表 → Markdown、複数附則、YAML frontmatter などの機能強化

---

## v2.6 — 2025-12-01

### Added

- **Design_convert_v2.6.md** 決定版  
- 表解析・附則処理の主要改善

---

## v0.5.2 — 2025-12-01

### Added

- validate v0.5.2 公開（条・項・号の100%抽出）

---

## v0.5.1 — 2025-11

- validate v0.5 系統の基礎構築

---

## v0.5.0 — 2025-11

- HTML 構造解析の初期 PoC

---

## v0.1.0 — 2025-11（初期）

- プロジェクト立ち上げ  
- 最初の HTML → TEXT 抽出実験
