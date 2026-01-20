---
title: Evaluation Overview
version: v0.1
status: FIXED
last_updated: 2026-01-20
---

# Evaluation Overview（入口）

本ディレクトリは、  
**Answer Diff Observation の成果物を用いて、人間による評価・判断を行うための Evaluation フェーズ**の  
設計・手順・成果物をまとめた入口文書である。

Evaluation は「自動評価」ではなく、  
**人間が判断を行うための材料を、再現可能・再配布可能な形に束ねる工程**として設計されている。

---

## 1. Evaluation の位置づけ

Evaluation は以下の工程の **後段**に位置する。

```text
Answer 生成
↓
Observation（差分の事実観測）
↓
Evaluation（評価・判断のための整理）
↓
Judgment（所見・結論の明文化）
```

### 重要な前提

- Observation は **評価前フェーズ**
- 差分の良否・意味・原因解釈は **Evaluation / Judgment 側の責務**
- Observation 結果単体での評価は禁止

---

## 2. Evaluation の構成要素

Evaluation は、以下 4 要素から構成される。

### 2.1 Observation（入力）

- `observation_result.json`
- `observation_summary.md`

👉 差分の **事実のみ** を保持  
👉 再解釈・再計算は禁止

---

### 2.2 AUTO（自動整理）

- Evaluation 用の **機械的集計結果**
- 人間判断を補助するための「事実の要約」

成果物：

- `evaluation_auto.json`（正本）

生成：

- `scripts/eval_summarize.py`

---

### 2.3 HUMAN（人間記録）

- 人間が読む・確認する過程を明示的に記録
- 判断そのものではなく **判断に至る前段の整理**

成果物：

- `Evaluation_Record_HUMAN_v0.2.md`（正本）

---

### 2.4 Judgment（判断）

- Evaluation を踏まえた所見・結論
- 合否判定を前提としない

成果物：

- `Evaluation_Judgment_*.md`
- / または Judgment JSON（v0.2 以降）

---

## 3. Evaluation Bundle

Evaluation の成果は、**単体ファイルではなく Bundle として扱う**。

### Bundle に含まれるもの

- Observation 成果物
- AUTO（JSON 正本）
- HUMAN 記録
- Judgment
- `bundle_manifest.json`

👉 Bundle は **評価単位の正本**  
👉 個別ファイルの抜粋・再編集は禁止

---

## 4. 配布・受け渡し

Evaluation Bundle v0.1 は、  
**ZIP 形式で配布されることを前提**とする。

詳細仕様：

- `docs/eval/Evaluation_Bundle_ZIP_Distribution_v0.1.md`

---

## 5. v0.1 の到達点（完了状態）

Evaluation v0.1 では、以下が達成されている。

- [x] Observation v0.1 を入力として受け取れる
- [x] AUTO（機械集計）を JSON 正本として生成できる
- [x] HUMAN 記録フォーマットが確定している
- [x] Judgment を独立フェーズとして分離した
- [x] Evaluation Bundle v0.1 を生成・配布できる

👉 **Evaluation v0.1 は「実運用可能な状態」で完了**している。

---

## 6. 禁止事項（再掲）

Evaluation フェーズでは、以下を行ってはならない。

- Observation の再計算・再解釈
- 差分原因の推測による断定
- AUTO 結果の意味付け
- Bundle 内ファイルの単体配布

---

## 7. 次フェーズ（v0.2 予定）

次の拡張は v0.2 として扱う。

- Judgment JSON 正本化
- 複数 Evaluation Run の比較
- Bundle v0.2（時系列・差分対応）
- Evaluation 完全自動フロー

---

## 関連ドキュメント

- `docs/README_observation.md`
- `docs/eval/README_evaluation_procedure_v0.1.md`
- `docs/eval/Evaluation_Record_HUMAN_v0.2.md`
- `docs/eval/Evaluation_Bundle_ZIP_Distribution_v0.1.md`
- `docs/eval/Migration_Guide_Evaluation_HUMAN_v0.1_to_v0.2.md`

---

この README は、Evaluation フェーズの **唯一の入口文書**として扱う。
