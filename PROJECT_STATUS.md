---
title: PROJECT_STATUS
version: v1.5
doc_type: status
project: reiki-rag-converter
created: 2025-12-06
updated: 2026-01-09
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
**再現可能に観測するための入力資産（Execution Input Contract）を提供する**  
ことを目的とする。

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

---

### Epic 4（条例別カスタマイズ質問セット生成基盤）

- ordinance_structure による条例構造（条・項・附則）の事実抽出
- Coverage Policy v0.1.2 に基づく concretizer 実装
- 決定性・再現性を担保した質問具体化ロジックの確立
- OrdinanceStructure における **条（article）／項（clause）／附則（supplementary）の語彙正規化**
- paragraph（本文段落）と clause（項）の意味分離を完了
- **Q4（条＋項質問）が clause ベースで正しく生成されることを確認**
- **Q8（附則質問）が supplementary 抽出に基づき正しく生成されることを確認**

- pytest / スナップショット / 実データ（Golden Ordinance 10本）での検証完了
- 同一入力 → 同一出力（決定性）を確認

---

### Epic 5（CLI 再現導線整備）

- customized_question_set CLI の安定化
- ordinance ID 明示指定による再現実行の確立
- 実行 manifest 出力による再現性担保

---

### Epic 6（Invariant 保証・回帰テスト）

- Execution Input Contract v0.1 / v0.2 の不変条件（Invariant）確定
- fail-fast 実装（質問集合空禁止）
- pytest / E2E / 実データ（10条例）による検証完了
- Execution Input Contract を「運用可能な契約」として確定

---

### Epic 7（Execution Input Contract v0.2 運用確立）

- Execution Input Contract v0.2 の設計原則・意味論を確定
- Core / Extension Fields の区分と責務定義
- question_set_id / schema_version の意味論確定
- extensions.skipped_questions による **非生成理由の可視化**
- Coverage Policy v0.1.2 を前提とした実装・生成結果の整合確認
- **Q4 / Q8 を含む本番データ生成が可能な状態で完了**

---

## 3. Pending（保留中タスク）

- convert_v2.8（表構造の高度化：colspan / rowspan / 別記様式対応）
- validate_v0.6（編・章・節の階層認識）
- synthetic_generator_v0.3（meta schema 拡張：P16〜P20）

※ 本フェーズは Execution Input Contract の安定運用完了後に再開する

---

## 4. Known Issue / Observation（未解決のみ）

- 現時点では **重大な既知不具合なし**
- 複数附則（改正履歴を含む）の詳細分解・質問分割は将来拡張として保留

---

## 5. Next Action（次に唯一実施すべきタスク）

Execution Input Contract v0.2 を前提とした  
**評価フェーズ成果の整理・知見抽出（生成AIテスト自動化プロジェクト側への受け渡し）**

※ 本リポジトリでは新規仕様追加は行わず、  
　入力資産は凍結状態を維持する。

---

## 6. 外部依存／連携プロジェクト

### External Dependency: gov-llm-e2e-testkit

生成AI 上での RAG 応答挙動を観測するため、  
別プロジェクト「gov-llm-e2e-testkit」を利用する。

同プロジェクトは、  
HTML / Markdown ナレッジ差分が RAG 応答に与える影響を  
再現可能に観測・記録することを目的とし、  
採否判断・優劣判定は行わない。

Golden Question Pool A および Golden Ordinance Set は  
凍結資産として扱い、評価フェーズでは消費のみ行う。

---

## 7. References

- PROJECT_GRAND_RULES.md
- AI_Development_Standard_v1.0.md
- ChatGPT_Startup_Template_v1.0.md
- ChatGPT_Startup_Workflow_v1.0.md
- Design_Execution_Input_Contract_v0.2.md
- Design_convert_v2.6.md
- Design_synthetic_html_v0.2.md
- Design_synthetic_generator_v0.2.md
- Design_interface_customized_question_set_delivery.md
- docs/policy/Coverage_Policy_v0.1.2.md
- docs/design/customized_question_set/Design_Concretizer_v0.1.md
- test_plan.md / test_e2e_design.md
- CI: .github/workflows/e2e.yml

---

【運用ルール】  
本ファイルは唯一の進行基準点（SSoT）であり、  
Next Action のみを次タスクとして扱う。

【運用ルール（追加）】  
commit 前には、PROJECT_STATUS / CHANGELOG の更新有無を必ず確認する。
