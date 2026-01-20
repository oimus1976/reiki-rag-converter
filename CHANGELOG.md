# Changelog
このプロジェクトにおける全変更履歴をまとめた公式 CHANGELOG です。
バージョンは [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) に準拠しています。

---

## v1.10 (2026-01-20)

### Added

- Evaluation v0.1 を **正式に完了**
  - Observation / Evaluation AUTO / Evaluation HUMAN / Judgment の全フェーズを定義・実行
  - 各フェーズ成果物の責務境界と不変性を FIX
- Evaluation Bundle v0.1 を設計正本として確定
  - Observation / AUTO / HUMAN / Judgment を束ねる評価単位を定義
  - bundle_manifest.json による機械可読な完全性保証を導入
- Evaluation Bundle ZIP 配布仕様 v0.1 を追加
  - 単一 Bundle = 単一 ZIP の配布単位を固定
  - ZIP 内ディレクトリ構成・命名規則・不変性ルールを明文化
- bundle_pack.py を追加
  - Evaluation Bundle v0.1 を ZIP として自動生成する CLI
  - pytest により ZIP 内容・構造を検証
- Evaluation Judgment 設計 v0.1 を追加
  - AUTO / HUMAN を前提とした最終判断フェーズの責務を定義
  - 合否判断・留保・差戻しの記録形式を固定

### Changed

- Evaluation 成果物のライフサイクルを明確化
  - docs/ は設計・テンプレ・仕様のみ
  - 実行生成物は artifacts/ を正とする運用に統一
- Evaluation を「実行可能・配布可能な成果物単位」として再定義

### Notes

- 本バージョン以降、Evaluation v0.1 は再実行・再解釈の対象としない
- 差分比較・複数 run 対応は Bundle v0.2 で扱う

---

## v1.9 (2026-01-20)

### Added

- Evaluation AUTO Result（JSON 正本）v0.2 を設計・実装として追加
  - Observation v0.1 成果物を入力とし、差分の「事実のみ」を自動集約
  - diff_flags 分布および Reference Diff の事実集計を JSON として固定
  - 評価・解釈・合否判断を含まない AUTO フェーズとして明確化
- eval_summarize.py を追加
  - Observation Result（JSON）から Evaluation AUTO Result（JSON）を生成
  - CLI v0.2（--out-dir）を正式 I/F として確定
- Evaluation AUTO Result v0.2 に対する pytest を追加
  - JSON スキーマおよび集計事実をテストで拘束

### Changed

- Evaluation フェーズの内部構成を明確化
  - AUTO（事実集約）/ HUMAN（判断・所見）を明示的に分離
  - Markdown は JSON 正本の派生 view として位置づけ
- Evaluation 成果物の配置方針を整理
  - 実行生成物は artifacts 配下を正とし、docs/ は設計・テンプレのみとする方針を明文化

### Notes

- 本バージョンでは Observation v0.1 の仕様・算出ロジックに変更はない
- Evaluation の人手判断（HUMAN フェーズ）は未実施
- 本更新は **Evaluation 実行基盤の確定**を目的とする

---

## v1.8 (2026-01-xx)

### Added

- Evaluation 実行手順 v0.1 を正式文書として確定
  - Observation v0.1 成果物を前提とした入力条件・読む順・判断ルールを固定
  - Observation の再解釈・再計算・品質判断を行わない方針を明文化
  - 合否ではなく Gate 判定（OK / △ / NG）による評価出口を定義
- 初回 Evaluation Run チェックリスト v0.1 を追加
  - 手順逸脱・責務越境を防止するための初回専用ガードとして位置づけ

### Changed

- Evaluation フェーズの位置づけを整理
  - Observation 完了後に人手で実行する判断フェーズとして明確化
  - Observation / Evaluation / Framework の責務境界を文書レベルで固定

### Notes

- 本バージョンでは Observation / convert / validate / diff 算出ロジックの変更は行っていない
- Evaluation は未実行であり、本更新は **実行手順の確定**のみを対象とする

---

## v1.7 (2026-01-19)

### Added

- Answer Diff Observation 実行フェーズを正式に完了
  - compare_answers.py による差分観測（Reference / Volume / Structural）を全条例で実行
  - ObservationResult（JSON / Markdown）を run 単位の成果物として固定
- Observation Summary v0.1 を正式テンプレとして確定
  - diff_flags が全件 true となり得ることを仕様として明文化
  - observations 配列の並び順が意味を持たないことを明示
  - 正規化・DOM 解釈・Markdown 構文解釈を行わない設計判断を固定
  - observation_result.json 単体での比較・評価を禁止

### Changed

- Observation Summary の生成方式を整理
  - 固定テンプレ（docs/observation/Observation_Summary_v0.1.md）を正本とし
  - run 固有情報（schema_version / generated_at / 件数）を
    compare_answers.py が自動追記する方式に変更
- PROJECT_STATUS を更新し
  - Answer Diff Observation フェーズを「完了」としてクローズ
  - 次フェーズを Evaluation 実行準備に移行

### Notes

- 本バージョンでは HTML / Markdown 変換ロジックの変更は行っていない
- 差分観測は評価や品質判定を目的としない前段工程として固定されている

---

## v1.6 (2026-01-18)

### Changed

- HTML版 / Markdown版 answer.md の差分を「評価前観測」として扱う設計を確定
  - 差分を不具合・品質判定に直結させない方針を明文化
  - 評価（Gate判定）とは独立した Observation フェーズとして位置づけ
  - Evaluation Framework との責務境界を整理
- 上記設計確定に伴い、PROJECT_STATUS を更新
  - 次フェーズを「answer.md 差分観測」に明示的に移行

※ 実装ロジックの変更はなし  
※ reiki-rag-converter の責務・出力契約に変更なし（設計・位置づけの明確化のみ）

### Added

- Answer Diff Observation 設計（v0.1）を正式FIX
  - HTML版 / Markdown版 answer.md の差分を「評価前観測」として整理する仕様を確定
  - 観測と評価の責務境界を明文化（判定・優劣判断を含めない）
  - Structural / Volume / Reference の3観測軸を v0.1 として固定
  - compare_answers.py の責務・CLI I/F・JSON 出力仕様を設計として拘束

### Notes

- 本更新は設計仕様の確定のみを対象とし、変換・生成ロジックの変更は行っていない

---

## v1.5 (2026-01-18)

### Changed

- README を実運用（本番条例HTML）前提に再設計
  - validate / convert / Customized Question Set 生成をフォルダ単位処理として明確化
  - 実在しない data/ パス参照を削除
  - synthetic_html を開発・テスト用途に限定
  - PowerShell / bash の実行例を正しい記法に修正

※ 実装ロジックの変更はなし（利用者向け契約・説明の是正）

---

## v1.4r (2026-01-12)

### Fixed

- refactor: rename customized_question_set to reiki_rag_customized_question_set to fix import reproducibility across environments
- docs: fix README to remove synthetic/test-only assumptions

---

## v1.4 (2026-01-04)

### Added

- Execution Input Contract v0.2 の設計書を追加（Design_Execution_Input_Contract_v0.2.md）
- Core / Extension Fields 区分および Consumer Rules を明文化

### Changed

- PROJECT_STATUS を更新し、Epic 7（Execution Input Contract v0.2 設計）を Close
- Execution Input Contract の位置づけを「成果物」から「長期運用可能な入力契約」として明確化

### Fixed

- Epic 6 までに確立された Invariants を v0.2 設計に正式に継承

---

## v1.3 (2026-01-02)

### Changed

- Refactored OrdinanceStructure into Facts / Summary to clarify responsibilities
- Re-verified determinism of ordinance_structure, concretizer, and writer after type refactor

### Fixed

- Eliminated ambiguous type usage that could cause partial-optimal design issues

### Notes

- Epic 4 base logic is now considered stable and re-tested
- Generator implementation remains as the final pending task for Epic 4 completion

---

## v1.2 (2026-01-02)

### Added

- Epic 4: 条例別カスタマイズ質問セット生成ロジックの中核実装
  - ordinance_structure: 条・項・附則の存在判定および DOM 順事実抽出
  - concretizer: Coverage Policy v0.1.1 に基づく質問具体化ロジックを実装
- Coverage Policy v0.1.1 を正式文書として確定
  - 条・項プレースホルダの機械的展開規則を FIX
  - 除外による検証不足リスクを回避する設計を明文化

### Fixed

- 条・項の選択基準を「意味」ではなく「DOM 順事実」に統一
- HTML / Markdown ナレッジ差分比較における入力決定性を担保

### Notes

- 本バージョンでは generator / サンプル成果物の生成は未実施
- Epic 4 は「生成ロジック基盤完成」段階として位置づける

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
