---
title: PROJECT_STATUS
version: v1.1
doc_type: status
project: reiki-rag-converter
created: 2025-12-06
updated: 2026-01-02
author: Sumio Nishioka + ChatGPT
tags:
  - project-management
  - oss
  - reiki-rag-converter
---

## PROJECT STATUS（reiki-rag-converter）

## 1. Purpose

条例HTMLを安定的・再現性高く TXT/Markdown に変換する OSS を進化・保守する。

加えて、本プロジェクトは、
生成AIテスト自動化プロジェクトと連携し、
条例ナレッジ入力差分が RAG 応答に与える影響を
**再現可能に観測するための入力資産を提供する**。

---

## 2. Completed（完了済みタスク）

- ChatGPT_Startup_Template_v1.0 の制定
- ChatGPT_Startup_Workflow_v1.0 の制定
- PROJECT_GRAND_RULES.md の更新（Startup Workflow との連携を追加）
- docs フォルダ内の frontmatter 統一（拡張版 C案）
- CI（smoke + Golden diff）の安定運用
- Golden_v1（P11〜P15）の確定
- synthetic_html_meta v0.2 の整備
- synthetic_generator_v0.2 の安定稼働
- **条例別カスタマイズ質問セットの JSON 最終構造・versioning 方針の確定**
- **customized_question_set.json を Execution Input Contract として凍結**
- **外部連携プロジェクト（gov-llm-e2e-testkit）との責務境界の確定**

---

## 3. Pending（保留中タスク）

- convert_v2.8（表構造の高度化：colspan/rowspan・別記様式対応）
- validate_v0.6（編・章・節の階層認識）
- synthetic_generator_v0.3（meta schema 拡張：P16〜P20）

---

## 4. Next Action（次に唯一実施すべきタスク）

- **GOLDEN_POLICY_v1.0（Golden 更新制度の文書化）を正式に作成する**

---

## 5. 外部依存／連携プロジェクト

### External Dependency: gov-llm-e2e-testkit

生成AI 上での RAG 応答挙動を観測するため、
別プロジェクト「gov-llm-e2e-testkit」を利用する。

同プロジェクトは、
HTMLナレッジと Markdownナレッジの入力差分が
RAG 応答に与える影響を再現可能に観測・記録するための
試験データ（試金石）を提供することを目的とし、
採否判断や優劣判定は行わない。

Golden Question Pool A および Golden Ordinance Set は
凍結資産として扱い、同プロジェクトの F4 フェーズでは消費しない。

---

## 6. References

- PROJECT_GRAND_RULES.md
- AI_Development_Standard_v1.0.md
- ChatGPT_Startup_Template_v1.0.md
- ChatGPT_Startup_Workflow_v1.0.md
- Design_convert_v2.6.md
- Design_synthetic_html_v0.2.md
- Design_synthetic_generator_v0.2.md
- Design_interface_customized_question_set_delivery.md
- test_plan.md / test_e2e_design.md
- CI: .github/workflows/e2e.yml

---

【運用ルール】  
本ファイルは唯一の進行基準点（SSoT）であり、
ChatGPT は Next Action のみをタスクとして実行する。

【運用ルール（追加）】  
commit 前には、ChatGPT がプロジェクトファイルの更新有無を自動チェックし、
必要に応じて git add 対象をリマインドする。
