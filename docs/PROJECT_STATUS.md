---
title: Project Status
project: reiki-rag-converter
version: 1.0
updated: 2025-12-06
---

# Project Status — reiki-rag-converter

本ファイルは、本プロジェクトの **現在位置（Current Phase）**,  
**未完了タスク（Pending）**,  
**次の最重要アクション（Next Action）** を一元管理し、  
「作業の見失い」を防止するためのステータス文書です。

CHANGELOG が「過去の履歴」を扱うのに対し、  
STATUS.md は **現在・未来を扱う唯一の真実（Single Source of Truth）** として運用します。

---

# 1. Current Phase（現在のフェーズ）

### ✅ CI 強化フェーズ（E2E 直前）
- Step1〜3（generator → validate → convert）の CI 統合が完了  
- synthetic_html_meta v0.2 に基づく P11〜P15 から **Golden_v1** を生成  
- CI パイプラインは安定して稼働中  
- 次は Step4（Golden diff）の導入が可能な状態

---

# 2. Completed Steps（完了した項目）

### ✔ 仕様・設計関連  
- Roadmap_v1.0 を確定  
- synthetic_html（v0.2）設計完了  
- Design_synthetic_generator_v0.2.md 作成  
- exception_check v3.2 設計反映  
- meta.json（P11〜P15）整備

### ✔ 実装関連  
- synthetic_generator_v0.2.py 実装  
- validate_reiki_structure_v0.5.3 安定動作  
- convert_reiki_v2.7 安定動作  
- P3（table）の破損復旧

### ✔ CI関連  
- smoke test の存在保証  
- pytest（unit）稼働  
- Step1: synthetic generator を CI に統合  
- Step2: validate を CI に統合  
- Step3: convert を CI に統合

### ✔ Golden関連  
- P11〜P15 の output_md をレビュー  
- Golden ディレクトリ golden_md/v1 を作成  
- Golden_v1（5ファイル）を GitHub に fix

---

# 3. Pending Items（未完了／今後取り組む項目）

### 🔥 高優先度  
- [ ] Step4: Golden diff の導入  
- [ ] Golden 更新ルール（GOLDEN_POLICY_v1.0.md）を docs に作成  
- [ ] convert_v2.8 の設計開始（colspan / rowspan / 別記様式強化）

### 🟧 中優先度  
- [ ] validate_v0.6 の要件整理（編構造の正規化）  
- [ ] synthetic_generator_v0.3：meta スキーマ拡張  
- [ ] P11〜P15 の「meta スキーマ」リファイン（event depth の追加）

### 🟨 低優先度  
- [ ] CLI 工具化（pip install reiki-rag-converter）  
- [ ] 大規模条例向け chunking 改良  
- [ ] DOM 揺れテンプレート追加（自治体差の吸収）

---

# 4. Risks / Notes（リスク・注意点）

1. **Golden との比較が CI に導入されると、仕様改善時に必ず差分が発生する。  
   → Golden 更新ルールを運用することで制御可能。**

2. synthetic_html_meta v0.2 が今後拡張されると、  
   P11〜P15 の更新が必要になる可能性がある。

3. convert_v2.7 の仕様は現状の synthetic に最適化されており、  
   実HTML の差異（自治体差）までは未吸収。  
   → DOM差吸収テンプレートの追加が必要。

4. CI が躓くとプロジェクト進行が止まるため、  
   **smoke test を削除しないこと**が必須。

---

# 5. Next Action（次の1手）

次の中から 1 つを選択し、作業を進める：

### ▶ **候補 A（推奨））: Step4 Golden diff の導入**  
Golden_v1 と output_md_ci の diff を CI に組み込む。

### ▶ 候補 B: Golden 更新ルールの文書化  
GOLDEN_POLICY_v1.0.md を作成する。

### ▶ 候補 C: convert_v2.8 の仕様策定に着手  
複雑表（colspan/rowspan）と別記様式の扱いを再設計。

---

# 6. 更新方法（STATUS.md の扱い）

- 作業開始前にこのファイルを開き、位置を確認  
- 作業が完了したら **Completed Steps に移動し、Pending を更新する**  
- ネクストステップは常に **1つに絞る**  
- CHANGELOG と併用することで、過去・現在・未来が分離される

---

（End of PROJECT_STATUS.md）
