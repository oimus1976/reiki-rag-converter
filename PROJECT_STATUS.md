---
title: PROJECT_STATUS
version: v1.6
doc_type: status
project: reiki-rag-converter
created: 2025-12-06
updated: 2026-01-18
author: Sumio Nishioka + ChatGPT
tags:
  - project-management
  - oss
  - reiki-rag-converter
---

# PROJECT STATUS（reiki-rag-converter）

## 1. Purpose

条例 HTML を **再現性高く・決定的に** TXT / Markdown へ変換し、  
生成 AI / RAG 評価に投入可能な入力資産を生成する OSS を提供する。

本プロジェクトはあわせて、

- 入力構造の差異が RAG 応答に与える影響を
- **評価前に歪めず**
- **再現可能な Execution Input Contract として固定する**

ことを目的とする。

また、生成された answer.md については、

- HTML版 / Markdown版の違いを
- **評価や是非判断に先立つ観測対象として整理・固定する**

という方針を採る。

本プロジェクトにおける評価は、

- 観測結果（Answer Diff Observation）を含む入力資産を前提として
- **本プロジェクトの設計思想・評価工程に基づき**
- 人手により実施される

ものであり、  
差分観測はその評価を歪めないための **必須前段工程**として位置づけられる。

---

## 2. Completed（完了済みタスク）

### 基盤・運用

- PROJECT_GRAND_RULES / Startup Workflow / frontmatter 運用の確立
- CI（pytest + E2E）の恒常運用
- synthetic_html / synthetic_generator の安定化（v0.2）
- Golden TXT / HTML（P11–P15）の確定
- README を **実利用者向け手順書**として再定義
  - 実データ前提
  - synthetic_html は dev/test 限定と明示

---

### Epic 4（条例別カスタマイズ質問セット生成基盤）【完了】

- ordinance_structure による **条・項（clause）・附則の正規抽出**
- paragraph ≠ clause の語彙正規化完了
- Coverage Policy v0.1.2 に準拠した concretizer 実装
- Q4（条＋項）/ Q8（附則）質問の **全条例生成保証**
- skip 判定は Extension Fields に理由付きで記録
- 同一入力 → 同一出力の決定性を pytest / 実条例で確認

---

### Epic 5（CLI・再現導線）【完了】

- customized question set CLI の安定化
- 実パス前提の validate / convert / generate 導線確立
- 実行結果の再生成・差分確認が可能な設計を固定

---

### Epic 6（Invariant / 回帰保証）【完了】

- Execution Input Contract v0.2 の確定
- Invariant（質問集合空禁止・構造逸脱防止）実装
- 実条例 10 本での手動検証（Q4/Q8 含む）
- pytest / E2E / CI すべてで再現性確認

---

### Answer Diff Observation 設計【完了】

- HTML版 / Markdown版 answer.md の差分を  
  **評価前に観測・整理する設計を v0.1 として確定**
- 観測と評価の責務境界を明確化（判定・優劣判断を含めない）
- Structural / Volume / Reference の3観測軸を固定
- compare_answers.py の責務・I/F・出力仕様を設計として拘束

※ 詳細は  
`docs/observation/Design_Answer_Diff_Observation_Spec_v0.1.md` に記録

---

### 再現性事故と復旧（2026-01）【重要な知見として固定】

- パッケージ名衝突により
  - 新端末 / CI 環境で import が破綻
- 原因：
  - `customized_question_set` が他リポジトリと衝突
- 対応：
  - パッケージを `reiki_rag_customized_question_set` に rename
  - pyproject.toml / tests / CLI / README を一括更新
- 結果：
  - ローカル / 新端末 / GitHub Actions すべてで再現性回復

※ 詳細は  
`docs/dev/Reproducibility_Break_and_Recovery_2026-01.md` に記録

---

## 3. Pending（保留中タスク）

- convert_v2.8
  - 表構造（rowspan / colspan / 別記様式）の高度化
- validate_v0.6
  - 編・章・節レベルの階層認識
- synthetic_generator_v0.3
  - P16–P20 拡張

---

## 4. Next Action（次に唯一実施すべきタスク）

**Answer Diff Observation の実行フェーズ**

- compare_answers.py による差分観測の実行
- ObservationResult（JSON / Markdown）の生成
- 評価工程に投入可能な観測データの固定

※ convert / validate の拡張は  
　本フェーズ完了後に再開する

---

## 5. 外部連携

### gov-llm-e2e-testkit

- 本プロジェクトは **入力資産・観測資産の提供側**
- 評価は本プロジェクトの設計思想に基づき実施される
- answer.md の差分は **評価前観測データ**として扱う

---

## 6. References

- PROJECT_GRAND_RULES.md
- AI_Development_Standard_v1.0.md
- ChatGPT_Startup_Template_v1.0.md
- ChatGPT_Startup_Workflow_v1.0.md
- Design_Execution_Input_Contract_v0.2.md
- Design_Answer_Diff_Observation_v0.1.md
- Design_convert_v2.6.md
- Design_synthetic_html_v0.2.md
- Design_synthetic_generator_v0.2.md
- Design_interface_customized_question_set_delivery.md
- Coverage_Policy_v0.1.2.md
- Design_Concretizer_v0.1.md
- Design_synthetic_html_v0.2.md
- Reproducibility_Break_and_Recovery_2026-01.md
- test_plan.md / test_e2e_design.md
- CI: .github/workflows/*.yml

---

【運用ルール】

- 本ファイルは唯一の進行基準点（SSoT）
- Next Action 以外の作業は原則行わない
- commit 前に PROJECT_STATUS / CHANGELOG を必ず確認する
