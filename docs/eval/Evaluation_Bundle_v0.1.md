---
schema_version: "0.1"
document_type: design_spec
record_type: evaluation_bundle
status: FIX
---

# Evaluation Bundle 設計 v0.1  

（Observation + AUTO + HUMAN + Judgment）

---

## 本文書の位置づけ

本ドキュメントは、**Evaluation Bundle v0.1 の設計正本**である。

Evaluation Bundle とは、  
**1 回以上の Evaluation Run に関する成果物一式を、評価・判断・再検証可能な単位として束ねるための論理構造**である。

Bundle は以下を目的とする。

- Evaluation の再現性を担保する
- 各フェーズ成果物の責務境界を保持する
- 将来の比較・再評価・監査に耐える単位を定義する

---

## Bundle が扱う対象範囲

Evaluation Bundle v0.1 は、以下のフェーズ成果物を対象とする。

```text
Observation
Evaluation AUTO
Evaluation HUMAN
Evaluation Judgment
```

※ 生成モデル・改善検討・修正案は Bundle の対象外とする。

---

## Bundle の基本原則

### 原則 1：Bundle は「評価の単位」であり「判断の単位」ではない

- 判断は Judgment フェーズにのみ存在する
- Bundle 自体は判断内容を持たない

---

### 原則 2：Bundle 内の成果物は改変されない

- Observation / AUTO / HUMAN / Judgment はすべて **immutable**
- 修正・追記が必要な場合は **新しい Bundle を作成**する

---

### 原則 3：Bundle は run_id / judgment_id により一意に識別される

- 暗黙の「最新版」は存在しない
- 常に ID 指定で参照する

---

## ディレクトリ構成（v0.1）

### 基本構成

```text
artifacts/evaluation/
└─ bundle_<bundle_id>/
   ├─ observation/
   │  ├─ observation_result.json
   │  └─ observation_summary.md
   │
   ├─ auto/
   │  └─ evaluation_auto.json
   │
   ├─ human/
   │  └─ Evaluation_Record_HUMAN_<run_id>.md
   │
   ├─ judgment/
   │  └─ Evaluation_Judgment_<judgment_id>.md
   │
   └─ bundle_manifest.json
```

---

## 各要素の責務（再掲）

### Observation

- 差分の **観測のみ**
- 良否・意味・評価を含まない

---

### Evaluation AUTO

- Observation 結果の **事実集計**
- JSON 正本
- 解釈・評価を含まない

---

### Evaluation HUMAN

- 判断を行わない
- 判断を保留した理由
- 次に必要な比較・観点の提示

---

### Evaluation Judgment

- 良否・妥当性・結論を **唯一記述可能**
- 複数 run を比較した上での判断
- 判断の射程と限界を明示

---

## bundle_manifest.json（v0.1）

### 目的

Bundle 内の成果物を **機械的に参照可能**にするための索引。

---

### スキーマ（v0.1）

```json
{
  "schema_version": "0.1",
  "bundle_id": "bundle_2026-01-20_01",
  "created_at": "2026-01-20",
  "observation": {
    "path": "observation/observation_result.json",
    "version": "v0.1"
  },
  "evaluation_auto": {
    "path": "auto/evaluation_auto.json",
    "version": "v0.2"
  },
  "evaluation_human": [
    {
      "path": "human/Evaluation_Record_HUMAN_eval_auto_2026-01-20_02.md",
      "schema_version": "0.2"
    }
  ],
  "evaluation_judgment": {
    "path": "judgment/Evaluation_Judgment_judgment_2026-01-20_01.md",
    "schema_version": "0.1"
  }
}
```

---

## Bundle v0.1 で「やらないこと」

- Bundle 自体への評価コメント付与
- Bundle 間の比較ロジック定義
- Bundle 内成果物の正規化・再解釈
- 自動 ZIP 化仕様の定義

※ これらは v0.2 以降で検討する。

---

## Bundle v0.1 の性格

- **人間が読める**
- **機械が追える**
- **判断の正本を含む**
- **再評価に耐える**

---

## まとめ

Evaluation Bundle v0.1 は、

- Observation から Judgment までの流れを
- 責務分離を保ったまま
- 再現可能な単位として束ねる

ための **評価成果物の最小完全単位**である。

---
