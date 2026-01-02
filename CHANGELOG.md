# Changelog
このプロジェクトにおける全変更履歴をまとめた公式 CHANGELOG です。
バージョンは [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) に準拠しています。

---

## [v1.1] - 2026-01-02

### Added

- 条例別カスタマイズ質問セット（customized_question_set.json）の
  JSON 最終構造および versioning 方針を確定
- Execution Input Contract としての位置づけを明文化し、
  下流（生成AIテスト自動化プロジェクト）との責務境界を固定
- docs/design 配下に設計運用ルールを追加
  - Issue → Design 昇格スキーム
  - docs/ 配下ディレクトリ整理方針

### Changed

- Design_interface_customized_question_set_delivery.md に
  JSON 仕様（schema_version / source_golden_question_pool 等）を追記

### Notes

- 本バージョンでは変換ロジック・CI・Golden 資産の変更は行っていない
- バージョンが飛んでいるのは本バージョンからPROJECT_STATUSとバージョンを同期させたことによるもの。

## [0.5.3] - 2025-12-05

### Fixed
- `validate_reiki_structure` の JSON 出力で、内部に `set` 型を含む場合に
  `TypeError: Object of type set is not JSON serializable` が発生していた問題を修正。
- 専用の `_to_serializable` 関数を導入し、`set` をソート済み `list` に変換することで、
  すべての例外ログおよび集計 JSON を Python 標準の `json` モジュールで安全に
  シリアライズ可能にした。

### Changed
- スクリプト先頭のバージョン表記を `v0.5.3` に更新。
- 例外チェックツール設計書を v3.2 に更新し、JSON シリアライズ仕様を明記。

- Qommons Evaluation Framework v0.1 (Gate-based)

### Added
- Design_Master.md as single design entry point


---

## [Unreleased]
- Add synthetic HTML v0.2 assets (P7–P10), meta templates, and generator v0.1

---

## [Unreleased]
- Add Design_synthetic_html_v0.2 (P1–P10, DOM variation, generator & meta spec)

---

## [Unreleased]
- Add synthetic HTML design doc (Design_synthetic_html_v0.1)
  - 定義パターン P1〜P6 を収録
  - OSS用の安全な synthetic テストセットの設計開始

---

## v2.7.1-doc3 — 2025-12-04

### Added
- `requirements.txt` を追加し、パッケージ依存関係を明確化
- `.gitignore` を更新して `requirements.txt` を追跡対象に修正

### No functional changes

---

## v2.7.1-doc2 — 2025-12-04

### Documentation
- README を **v1.1** に全面改訂
  - TL;DR セクション追加
  - Quick Start 改善
  - Before/After の変換例追加
  - RAG 連携サンプル（LangChain）追加
  - 例規HTMLの著作権注意を追加
  - Contributing ガイドを強化（Golden diff / PR rules）
  - 全体を通して PENTA レビュー内容を反映し文章品質を向上
- ディレクトリ構成説明を最新版に更新
- CI（E2E workflow）に対応した説明を追加

### No functional changes
- コード（validate / convert）の処理内容は変更なし

---

## v2.7.1-doc1 — 2025-12-04

### Documentation
- `docs/test_e2e_design.md` を v1.1 に改訂
  - 異常系テストケース（A01〜A06）を追加
  - Golden diff の方針を明確化
  - CI (GitHub Actions) を前提とした設計へ刷新
  - セキュリティ観点を追加（script混入、chardet、path等）
  - validate → convert の構造整合性チェックを定義

### Added
- `.github/workflows/e2e.yml` を追加
  - Python 3.10/3.11/3.12 の matrix
  - validate → convert → pytest
  - Golden diff による回帰テスト
  - failure 時の artifacts 保存に対応

---

## v2.7.1 — 2025-12-03

### Added
- **convert_reiki_v2.7.py** を追加
  - validate v0.5.2 の構造情報に沿って完全変換を行う改良版
  - 条見出し → 本文の欠落問題を修正
  - `.main` → 条本文抽出ロジックの改善
  - 表（table）を Markdown 表に変換
  - YAML frontmatter（id/title/date/etc.）生成
  - 附則（複数）に完全対応

### Fixed
- 条本文が抜けるバグ
- 「第2条」複数誤検出問題は v0.5.2 側で解消済み

---

## v2.7.0（内部版） — 2025-12-03

### Added
- convert v2.6 の GitHub 移行準備版（非公開）
- ローカルでの動作確認用 scaffolding の整備

---

## v2.6 — 2025-12-01（チャット内完成版）

### Added
- **Design_convert_v2.6.md** を確定
- 表の抽出テスト（k518RG00000080.html）に対応
- 附則の誤結合防止アルゴリズムを実装

### Fixed
- 従来問題だった「本則の途中で附則タイトル判定が誤作動する」問題を解消
- 「同じ class 名のノードが連続する DOM 揺れ」への耐性改善

---

## v0.5.2（validator） — 2025-12-01

### Added
- **validate_reiki_structure_v0.5.2.py** を追加
  - `.eline` 内の `.article` から条を100%正確に抽出
  - 項 = `div.clause`、号 = `div.item`
  - 附則は `.s-head` → meta解析 → 本文抽出
  - E 系（E003/E004/E007 etc.）と S 系のイベント検出
  - `structure_summary.json` / `summary_report.json` / `class_statistics.json` を出力
- サンプル抽出（sample_patterns.json）ロジックを確立
- 例規HTML（12 / 55 / 80）で precision を検証

### Fixed
- 「第2条 検出がループする」バグを完全解消
- 附則の多段構造（最大9本）を正確に解析

---

## v0.5.1 — 2025-11

### Added
- validate v0.5 の初期版を作成
- 本文と項・号の抽出ロジックの基礎構築

---

## v0.5.0 — 2025-11

### Added
- 最初の構造解析パイプライン
- 例規HTMLの class 構造（article/clause/item/s-head）の調査
- サンプル HTML（12/55/80）をベースとした仕様化を開始

---

## v0.1.0 — 2025-11（最初期）

### Added
- プロジェクト立ち上げ
- HTML → テキスト抽出の PoC
- 「条文構造を機械で扱う」コンセプトの実験
- 開発ノート・概念モデルの作成
