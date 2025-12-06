---
title: PROJECT_STATUS
version: v1.0
doc_type: status
project: reiki-rag-converter
created: 2025-12-06
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - project-management
  - oss
  - reiki-rag-converter
---

# PROJECT STATUS（reiki-rag-converter）

## 1. Purpose
条例HTMLを安定的・再現性高く TXT/Markdown に変換する OSS を進化・保守する。

## 2. Completed（完了済みタスク）
- ChatGPT_Startup_Template_v1.0 の制定  
- ChatGPT_Startup_Workflow_v1.0 の制定  
- PROJECT_GRAND_RULES.md の更新（Startup Workflow との連携を追加）  
- docs フォルダ内の frontmatter 統一（拡張版 C案）  
- CI（smoke + Golden diff）の安定運用  
- Golden_v1（P11〜P15）の確定  
- synthetic_html_meta v0.2 の整備  
- synthetic_generator_v0.2 の安定稼働  

## 3. Pending（保留中タスク）
※ 次スレッドでこの中から Next Action を正式に決定する。

- convert_v2.8（表構造の高度化：colspan/rowspan・別記様式対応）  
- validate_v0.6（編・章・節の階層認識）  
- synthetic_generator_v0.3（meta schema 拡張：P16〜P20）  
- GOLDEN_POLICY_v1.0（Golden 更新制度の文書化）  

## 4. Next Action（次に唯一実施すべきタスク）
※ 次スレッド開始時に決定する。

（空欄：未決定）

## 5. References
- PROJECT_GRAND_RULES.md  
- AI_Development_Standard_v1.0.md  
- ChatGPT_Startup_Template_v1.0.md  
- ChatGPT_Startup_Workflow_v1.0.md  
- Design_convert_v2.6.md  
- Design_synthetic_html_v0.2.md  
- Design_synthetic_generator_v0.2.md  
- test_plan.md / test_e2e_design.md  
- CI: .github/workflows/e2e.yml  

---

【運用ルール】  
本ファイルは唯一の進行基準点（SSoT）であり、  
ChatGPT は Next Action のみをタスクとして実行する。
