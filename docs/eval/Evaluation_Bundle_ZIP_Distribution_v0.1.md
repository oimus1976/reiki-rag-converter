---
schema_version: "0.1"
document_type: design_spec
record_type: evaluation_bundle_distribution
status: FIX
---

# Evaluation Bundle ZIP 配布仕様 v0.1

---

## 本文書の位置づけ

本ドキュメントは、**Evaluation Bundle v0.1 を外部に引き渡すための ZIP 配布仕様**を定義する設計正本である。

本仕様は以下を目的とする。

- Evaluation 成果物一式を **改変不能な形**で配布する
- 評価・判断の再現性を担保する
- 受領側が **Bundle 構造を機械的に解釈可能**とする

---

## 対象となる Bundle

本仕様は、以下の条件を満たす Evaluation Bundle に適用する。

- Evaluation Bundle 設計 v0.1 に準拠している
- bundle_manifest.json が存在する
- Observation / AUTO / HUMAN / Judgment がすべて含まれている

---

## 配布単位

### 単一 Bundle = 単一 ZIP

- 1 Bundle は **必ず 1 ZIP ファイル**として配布する
- 複数 Bundle を 1 ZIP にまとめることはしない

---

## ZIP ファイル命名規則

```text
evaluation_bundle_<bundle_id>.zip
```

### 例

```text
evaluation_bundle_bundle_2026-01-20_01.zip
```

---

## ZIP 内ディレクトリ構成（固定）

ZIP を展開した直下は、**Bundle ルート**とする。

```text
evaluation_bundle_<bundle_id>/
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

## bundle_manifest.json の役割（配布時）

ZIP 配布において、`bundle_manifest.json` は以下を満たす必要がある。

- ZIP 内 **相対パスのみ**を記載する
- 外部参照（絶対パス・URL）を含まない
- Bundle の完全性を機械的に検証可能とする

---

## 配布 ZIP に含めてよいもの / 含めないもの

### 含めてよいもの

- Observation 成果物（json / md）
- Evaluation AUTO JSON 正本
- Evaluation HUMAN 記録（md）
- Evaluation Judgment 記録（md）
- bundle_manifest.json

---

### 含めてはならないもの

- 元データ（HTML / Markdown Answer 原本）
- 生成スクリプト・コード
- ログ・デバッグファイル
- ZIP 展開後に生成される中間成果物

---

## 不変性（Immutability）ルール

配布された ZIP は以下の性質を持つ。

- 内容の追記・修正は禁止
- 差し替えが必要な場合は **新しい bundle_id を発行**
- 「最新版 ZIP」という概念は持たない

---

## 受領側の最小確認手順（参考）

ZIP を受領した側は、以下を確認することで Bundle の妥当性を検証できる。

1. ZIP を展開する
2. bundle_manifest.json が存在することを確認
3. manifest に記載された全パスが存在することを確認
4. Observation / AUTO / HUMAN / Judgment が揃っていることを確認

※ 内容の評価・解釈は本仕様の対象外

---

## v0.1 で定義しない事項

本仕様では以下を定義しない。

- ZIP の署名・ハッシュ仕様
- Bundle 間の依存関係
- Bundle を跨いだ比較手法
- 配布後の評価・判断プロセス

※ これらは v0.2 以降で検討する。

---

## v0.1 の性格

Evaluation Bundle ZIP 配布仕様 v0.1 は、

- **人間にとって分かりやすく**
- **機械にとって検証しやすく**
- **改変耐性を持つ**

最小構成の配布仕様である。

---

## まとめ

本仕様により、Evaluation Bundle は、

- 再現可能な評価単位として
- 外部に安全に引き渡され
- 後続の評価・監査・比較に耐える

**正式な成果物**として成立する。

---
