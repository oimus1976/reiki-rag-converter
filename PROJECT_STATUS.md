---
title: PROJECT_STATUS
version: v1.10
doc_type: status
project: reiki-rag-converter
created: 2025-12-06
updated: 2026-01-20
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

評価工程は以下の責務分離に基づく。

- Observation：差分の事実を観測する前段フェーズ
- Evaluation AUTO：観測結果を事実として集約する自動フェーズ
- Evaluation HUMAN：Framework に基づき人手で判断するフェーズ

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

- ordinance_structure による **条・項・附則の正規抽出**
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
- 実条例での手動検証（Q4 / Q8 含む）
- pytest / E2E / CI による再現性確認

---

### Answer Diff Observation（v0.1）【完了】

- HTML版 / Markdown版 answer.md の差分を  
  **評価前に観測・整理する設計および実装を v0.1 として確定**
- 観測と評価の責務境界を明確化
  - 差分の良否・適切性・意味付けを行わない
- Reference / Volume / Structural の3観測軸を固定
- compare_answers.py による
  - 全条例・全質問ペアの差分観測を実行
  - ObservationResult（JSON / Markdown）を run 単位で生成
- Observation Summary v0.1 を正式テンプレとして確定
  - diff_flags が全件 true となり得ることを仕様として明文化
  - observations 配列の並び順が意味を持たないことを明示
  - 正規化・DOM 解釈・Markdown 構文解釈を行わない設計判断を固定
  - observation_result.json 単体での比較・評価を禁止

※ 詳細は  
`docs/observation/Design_Answer_Diff_Observation_Spec_v0.1.md`  
`docs/observation/Observation_Summary_v0.1.md`  
に記録

---

### 再現性事故と復旧（2026-01）【重要な知見として固定】

- パッケージ名衝突により新端末 / CI 環境で import が破綻
- 原因：
  - `customized_question_set` が他リポジトリと衝突
- 対応：
  - パッケージ名を `reiki_rag_customized_question_set` に rename
  - pyproject.toml / tests / CLI / README を一括更新
- 結果：
  - ローカル / 新端末 / GitHub Actions すべてで再現性回復

※ 詳細は  
`docs/dev/Reproducibility_Break_and_Recovery_2026-01.md` に記録

---

### Evaluation 実行手順（v0.1）【完了】

- Observation v0.1 成果物を前提とした
  - Evaluation 実行手順（読む順・判断ルール）を正式文書として確定
- Observation / Evaluation の責務境界を明確化
- 初回 Evaluation Run チェックリスト v0.1 を整備

---

### Evaluation AUTO Result（v0.2）【完了】

- Evaluation AUTO Result（JSON 正本）v0.2 を設計・実装として確定
- Observation Result（JSON）を入力とし
  - diff_flags 分布の集計
  - Reference Diff に関する事実集約を自動生成
- 評価・解釈・合否判断を含まないことを明示
- eval_summarize.py により CLI 実行可能
- pytest により JSON スキーマと集計事実を拘束

※ 詳細は  
`docs/eval/Design_Evaluation_Auto_Result_v0.2.md`  
に記録

---

### Evaluation v0.1（完了）【正式完了】

- Evaluation v0.1 を **設計・実行・配布可能な単位として正式に完了**
- 以下の全フェーズを FIX
  - Observation（差分の事実観測）
  - Evaluation AUTO（事実集約・JSON 正本）
  - Evaluation HUMAN（Framework に基づく人手判断）
  - Evaluation Judgment（最終判断・結論記録）
- 各フェーズの責務境界を明確化
  - 評価前観測と判断の混線を禁止
  - AUTO フェーズでは解釈・合否判断を行わない
- Evaluation Bundle v0.1 を正式成果物単位として確定
  - Observation / AUTO / HUMAN / Judgment を束ねる構造を固定
  - bundle_manifest.json による完全性検証を導入
- Evaluation Bundle ZIP 配布仕様 v0.1 を確定
  - 単一 Bundle = 単一 ZIP
  - ZIP 内構造・命名規則・不変性ルールを設計として拘束
- bundle_pack.py により
  - Bundle v0.1 の ZIP 自動生成を実装
  - pytest による内容検証を実施

※ Evaluation v0.1 は「完了済み成果物」として固定し、
　再生成・差替えは行わない

---

## 3. Pending（保留中タスク）

- Bundle v0.2 設計
  - 複数 Evaluation run の束ね
  - Bundle 間差分比較
- Reference Diff false 内容分析フェーズの別プロジェクト化
- Evaluation Bundle 受領側検証 CLI（bundle_validate.py）
- Evaluation 完全自動フロー（Observation → ZIP）設計
- convert_v2.8（表構造高度化）
- validate_v0.6（編・章・節認識）
- synthetic_generator_v0.3
  - P16–P20 拡張

---

## 4. Next Action（次に唯一実施すべきタスク）

**Bundle v0.2（差分比較・複数 run 対応）の設計開始**

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
- Design_Answer_Diff_Observation_Spec_v0.1.md
- Observation_Summary_v0.1.md
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
