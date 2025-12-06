---
title: AI_Development_Standard
version: v1.0
doc_type: standard
project: reiki-rag-converter
created: 2025-12-06
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - development-standard
  - ai-assisted-development
  - oss
  - reiki-rag-converter
---

# AI Development Standard（v1.0）
本書は、AI（ChatGPT 等）を開発プロジェクトの正式メンバーとして統合するための  
行動規範・設計原則・品質保証基準・進行管理方式を体系化した  
最上位の開発スタンダードである。

OSS 開発、および中長期的プロジェクトにおける  
人間と AI の協働作業を円滑・安定・高品質に保つための基礎となる。

---

# 1. 目的
AI を「単なる回答生成ツール」ではなく  
**プロジェクトを理解し、設計と実装の整合性まで考慮できる開発メンバー**として活用すること。

本スタンダードは以下を実現する：

- プロジェクトの迷走防止  
- 長期開発における整合性維持  
- 設計と実装の一貫性保証  
- CI を中心とした品質保証の徹底  
- AI による生産性向上と人的ミス削減  

---

# 2. 運用基盤（Core Governance Layer）
本スタンダードは次の 3 つの基盤文書を頂点とする：

1. **PROJECT_GRAND_RULES.md**  
   → AI の行動規範・禁止事項・判断原則

2. **AI_OSS_Practices_v1.0.md**  
   → OSS 開発に AI を組み込むための実践手法・文書体系

3. **PROJECT_STATUS.md**  
   → プロジェクト進行の唯一の真実源（SSoT: Single Source of Truth）

---

# 3. 設計原則（Design Principles）
AI は以下を遵守して提案・設計・実装支援を行う。

### 3.1 設計優先原則
- すべての提案は設計書（Design_*.md）と整合していなければならない。
- 設計を逸脱する変更は必ず「設計変更案」として提示する。

### 3.2 全層整合原則（End-to-End Consistency）
提案は以下の全層に影響することを考慮しなければならない：

- meta（生成ルール）
- synthetic HTML
- validate
- convert
- Golden
- CI
- テスト設計

部分最適を行わず、必ず全層整合性を確保する。

### 3.3 Future-proof 原則
将来のバージョンアップ時に破綻しない設計を行う。

例：非決定項目の diff 除外、バージョニング、meta schema の柔軟性。

---

# 4. 実装原則（Implementation Principles）

### 4.1 コード生成は設計依存型とする
AI がコードを生成する際は：

- Design → Implementation → Test → CI の順に検討  
- 設計に存在しない機能は勝手に追加しない  

### 4.2 実装変更前の影響分析
修正提案には以下を必ず含めること：

- 設計との整合性  
- CI 安定性  
- Golden 破壊の可能性  
- meta/validate/convert の依存関係  

### 4.3 安易な解決策禁止
例：  
- CI を通すための機能削除  
- 異常値を“無視して通す”  
- 時刻の出力削除（正しい理由がなければ禁止）

---

# 5. 品質保証（Quality Assurance Standard）

### 5.1 CI の最優先化
CI（GitHub Actions 等）はプロジェクトの品質の中核である。

守るべき原則：
- exit code 5 の回避  
- smoke test の維持  
- Golden diff の完全性  

### 5.2 Golden diff 原則
- Golden は「正解」である  
- 更新には根拠（仕様変更 or バグ修正）が必要  
- 非決定項目は diff 対象外  

### 5.3 Synthetic → Validate → Convert → Compare の完全再現性
どの環境でも毎回同じ結果が得られなければならない。

---

# 6. 進行管理（Project Operation Standard）

### 6.1 PROJECT_STATUS.md を唯一の SSoT とする
- Next Action は常に 1つだけ  
- ChatGPT が勝手にタスク変更しない  
- 進行の整合性は AI が自動で監査する

### 6.2 会話内での提案は「候補」であり、確定は人間が行う
AI がプロジェクトを乗っ取らないための重要な原則。

### 6.3 変更後は状況更新を促す
タスク・文書・CI が変更された場合は  
PROJECT_STATUS.md の更新を AI が必ず提案する。

---

# 7. 知識管理（Knowledge Management Standard）

### 7.1 ChatGPT プロジェクト内のファイルは厳選する
最大 25 個まで。  
本プロジェクトでは 19 ファイル構成がベストプラクティス。

### 7.2 古い設計書・古いコードはプロジェクトに置かない
誤参照を防ぎ、判断の一貫性が確保される。

---

# 8. AI との対話プロトコル（Interaction Standard）

### 8.1 開始テンプレートの利用
セッション開始時に以下を宣言する：

```

このプロジェクトでは以下を厳守してください。

* PROJECT_GRAND_RULES.md を遵守する
* PROJECT_STATUS.md の Next Action のみ実行対象
* 設計書と実装に基づいて判断する
* CI と Golden diff の安定性を最優先する
* 必要に応じて PENTA で多角的検討を行う

```

### 8.2 PENTA（5-Brain System）の利用
複雑な仕様・設計変更・CI の議論には  
PENTA による多角分析を行う。

---

# 9. プロジェクト成熟度モデル（AI × OSS）

1. 文書整備  
2. CI 安定  
3. PROJECT_STATUS（SSoT）確立  
4. ガバナンス構築  
5. AI アシストによる本格的進化フェーズ  

本プロジェクトはすでに「4」まで完了。

---

# 10. 結論
AI は適切なルール・文書体系・CI 制御を与えることで  
**OSS 開発に参加できるアーキテクト**となる。

人間の判断力と AI の構造把握力が結びつくことで、  
高品質な OSS 開発が前例のない速度と安定性で進む。

本標準はそのための基盤であり、  
再利用可能なフレームワークとなる。

---
