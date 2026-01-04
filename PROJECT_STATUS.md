---
title: PROJECT_STATUS
version: v1.4
doc_type: status
project: reiki-rag-converter
created: 2025-12-06
updated: 2026-01-04
author: Sumio Nishioka + ChatGPT
tags:
  - project-management
  - oss
  - reiki-rag-converter
---

# PROJECT STATUS（reiki-rag-converter）

## 1. Purpose

条例HTMLを安定的・再現性高く TXT / Markdown に変換する OSS を進化・保守する。

加えて本プロジェクトは、生成AIテスト自動化プロジェクトと連携し、  
条例ナレッジ入力差分が RAG 応答に与える影響を  
**再現可能に観測するための入力資産を提供する**ことを目的とする。

---

## 2. Completed（完了済みタスク）

- ChatGPT_Startup_Template_v1.0 の制定
- ChatGPT_Startup_Workflow_v1.0 の制定
- PROJECT_GRAND_RULES.md の更新（Startup Workflow 連携）
- frontmatter 運用ルールの確立（docs 配下）
- CI（smoke + Golden diff）の安定運用
- Golden_v1（P11〜P15）の確定
- synthetic_html_meta v0.2 の整備
- synthetic_generator_v0.2 の安定稼働
- **条例別カスタマイズ質問セットの JSON 最終構造・versioning 方針の確定**
- **customized_question_set.json を Execution Input Contract として凍結**
- **外部連携プロジェクト（gov-llm-e2e-testkit）との責務境界の確定**

### Epic 4（条例別カスタマイズ質問セット生成基盤）

- ordinance_structure による条例構造（条・項・附則）の事実抽出
- Coverage Policy v0.1.1 に基づく concretizer 実装
- 決定性・再現性を担保した質問具体化ロジックの確立
- **OrdinanceStructure の型名分離（Facts / Summary）による責務明確化**
- **型名分離後の再テスト完了**
  - ordinance_structure / concretizer / writer の ad-hoc 検証
  - 同一入力 → 同一出力（決定性）を確認

※ Epic 4 は Epic 6 にて実データ検証まで完了済み

### Epic 5（CLI 再現導線整備）

- customized_question_set CLI の安定化
- ordinance ID 自動検出・逐次実行スクリプトの整備
- 実行 manifest 出力による再現性担保

### Epic 6（Invariant 保証・回帰テスト）

- Execution Input Contract v0.1 の不変条件（Invariant）確定
- fail-fast 実装（質問集合空禁止）
- pytest / E2E / 実データ（10条例）による検証完了
- Execution Input Contract v0.1 を「運用可能な契約」として確定

### Epic 7（Execution Input Contract v0.2 設計）

- Execution Input Contract v0.2 の設計原則・意味論を確定
- Core / Extension Fields の区分と責務定義
- question_set_id / schema_version の意味論確定
- Invariants / Consumer Interpretation Rules の集約
- **Design_Execution_Input_Contract_v0.2.md を freeze 可能な状態で完成**
- v0.1 Consumer との完全後方互換を保証

---

## 3. Pending（保留中タスク）

- convert_v2.8（表構造の高度化：colspan / rowspan / 別記様式対応）
- validate_v0.6（編・章・節の階層認識）
- synthetic_generator_v0.3（meta schema 拡張：P16〜P20）

### Epic 4（残作業）

- generator 実装（接続層）
  - Golden Question Pool A 読み込み
  - ordinance_structure → concretizer → writer の接続
- customized_question_set.json の実生成（最小1条例）

---

## 4. Next Action（次に唯一実施すべきタスク）

Execution Input Contract v0.2 を前提として、
generator / CLI の非破壊対応（schema_version=0.2, Extension Fields 出力）を行う

---

## 5. 外部依存／連携プロジェクト

### External Dependency: gov-llm-e2e-testkit

生成AI 上での RAG 応答挙動を観測するため、  
別プロジェクト「gov-llm-e2e-testkit」を利用する。

同プロジェクトは、  
HTML / Markdown ナレッジ差分が RAG 応答に与える影響を  
再現可能に観測・記録することを目的とし、  
採否判断・優劣判定は行わない。

Golden Question Pool A および Golden Ordinance Set は  
凍結資産として扱い、同プロジェクトの評価フェーズでは消費しない。

---

## 6. References

- PROJECT_GRAND_RULES.md
- AI_Development_Standard_v1.0.md
- ChatGPT_Startup_Template_v1.0.md
- ChatGPT_Startup_Workflow_v1.0.md
- Design_Execution_Input_Contract_v0.2.md
- Design_convert_v2.6.md
- Design_synthetic_html_v0.2.md
- Design_synthetic_generator_v0.2.md
- Design_interface_customized_question_set_delivery.md
- docs/policy/Coverage_Policy_v0.1.1.md
- docs/design/customized_question_set/Design_Concretizer_v0.1.md
- test_plan.md / test_e2e_design.md
- CI: .github/workflows/e2e.yml

---

【運用ルール】  
本ファイルは唯一の進行基準点（SSoT）であり、  
Next Action のみを次タスクとして扱う。

【運用ルール（追加）】  
commit 前には、プロジェクト管理ファイルの更新有無を必ず確認する。
