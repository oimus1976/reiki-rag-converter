---
title: Design_Master
version: v1.0
doc_type: design_index
project: reiki-rag-converter
created: 2025-12-18
updated: 2025-12-18
author: Sumio Nishioka + ChatGPT
tags:
  - design
  - ssoT
  - architecture
  - reiki-rag-converter
---

# Design Master Document（設計総覧）

本書は **reiki-rag-converter プロジェクトにおける設計書群の公式マスター文書**である。
個別の Design_*.md は詳細仕様として GitHub 上に保持し、
**本書を「設計の入口（Single Entry Point）」とする。**

---

## 1. 目的（Why this document exists）

- 設計書の乱立による参照コスト増大を防ぐ
- ChatGPT / 開発者 / レビューアが
  **「どの設計が、どの責務を持つか」を即座に把握できる**ようにする
- ChatGPT プロジェクトファイル数（25制限）を超えないための
  **設計ドキュメント集約点**とする

---

## 2. 設計体系の全体像

```

HTML（条例）
↓
validate（構造検証）
↓
convert（Markdown/TXT変換）
↓
synthetic_html（試験入力）
↓
Golden diff / CI
↓
Qommons.AI（RAG評価）

```

本プロジェクトの設計は、**上流 → 下流に一方向**で影響を及ぼす。
下流都合による上流仕様の歪曲は禁止する。

---

## 3. コア設計ドキュメント一覧（最新版）

### 3.1 convert（変換系）

- **Design_convert_v2.6.md**
  - 条・項・号・附則・表（単純構造）の変換仕様
  - Golden v1（P11〜P15）準拠
  - 次期：convert_v2.8（colspan / rowspan）

**責務境界**
- HTML構造に依存しすぎない
- 出力は「テキスト単体で意味が通る」ことを最優先

---

### 3.2 validate（構造検証系）

- **Design_exception_check_v3.2.md**
  - E系（Error） / S系（Structure）イベントの定義
  - CI での基盤破壊検知の根拠

**責務境界**
- 正しさを保証しない
- 「壊れている可能性」を早期検知する

---

### 3.3 synthetic_html（試験入力系）

- **Design_synthetic_html_v0.2.md**
- **Design_synthetic_generator_v0.2.md**

**役割**
- 実条例では再現困難な DOM 揺れ・異常構造を人工生成
- Golden diff の基準入力を担保

**重要区分**
- P01〜P10：Legacy（固定）
- P11〜P15：Golden v1 中核
- P16〜：将来拡張（v0.3+）

---

### 3.4 E2E / CI 設計

- **test_e2e_design.md**
- **.github/workflows/e2e.yml**（参照）

**原則**
- smoke test は CI の憲法
- exit code 5 を発生させない
- Golden diff は「仕様の結果」であり、テストではない

---

## 4. Qommons.AI 連携設計（外部依存）

### 関連ドキュメント

- Qommons_test_manual_v0.1.md
- Qommons_Evaluation_Framework_v0.1.md

### 成果物インターフェース（観測データ）

Qommons.AI テスト自動化プロジェクトから
reiki-rag-converter が受け取る成果物の形式・責務境界は、
以下のインターフェース定義に完全に委譲される。

- **Qommons_Test_Artifact_Interface_v0.1r.md**

本インターフェースで定義される成果物は、
評価・解釈・結論を一切含まない一次観測データであり、
評価・Gate 判定・Golden 更新判断は
すべて reiki-rag-converter 側の責務とする。

本設計書は、当該成果物の内容・評価方法には立ち入らない。

**前提条件**

- HTMLタグはすべて削除される
- DOM構造は無視され、文字数チャンク化される
- TXT + CSV 横断検索は「両方が検索上位」の場合のみ成立

これらは **convert / Golden 設計に影響を与える制約条件**として扱う。

---

## 5. Golden との関係（最重要）

Golden の管理・更新ルールは **GOLDEN_POLICY_v1.0.md** に完全委譲する。

本書は以下を保証する：

- Design → Implementation → Golden の順序
- 設計書が Golden の代替にならないこと
- Golden は「結果」であり「仕様」ではないこと

---

## 6. Design Master の運用ルール

- 個別 Design_*.md の更新時は、本書の該当節を必ず確認する
- 新しい設計書を追加する場合：
  1. 既存設計で吸収できないか検討
  2. 必要な場合のみ Design_*.md を新設
  3. 本書に **必ず追記**

- ChatGPT は **本書を設計の入口として扱う**

---

## 7. バージョニング方針

- v1.x：設計体系の安定期
- v2.x：convert_v3 / validate_v1.0 移行期に対応

---

## 8. 参照関係（SSoT）

優先順位は以下の通り：

1. PROJECT_STATUS.md
2. PROJECT_GRAND_RULES.md
3. **Design_Master.md（本書）**
4. 個別 Design_*.md
5. CI / 実装コード
6. Golden ファイル

---

## 付録 A. 廃止・統合予定

- ChatGPT_Startup_Template / Workflow
  → PROJECT_GRAND_RULES.md Appendix に統合予定

---

