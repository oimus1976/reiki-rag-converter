---
schema_version: "0.2"
document_type: evaluation_record_template
record_type: evaluation_human
status: FIX
---

# Evaluation HUMAN Record v0.2

---

## 本文書の位置づけ

本ドキュメントは、**Evaluation HUMAN 記録 v0.2 の正本テンプレート**である。

Evaluation HUMAN 記録は以下の責務を持つ。

- Observation / AUTO Evaluation の**再解釈を行わない**
- 良否・合否・結論を**記載しない**
- Evaluation Judgment を行うための  
  **判断保留理由・比較観点を人間が記録する**

---

## 0. 前提確認（必須）

以下を確認し、チェックを入れること。

- [ ] 本記録は Observation の再計算・再解釈を行っていない
- [ ] 本記録は AUTO JSON に含まれる事実を再記述していない
- [ ] 本記録は 良否・評価・結論を含まない
- [ ] 本記録は Evaluation Judgment のための補助情報である

---

## 1. メタ情報（必須）

```yaml
run_id: <evaluation_run_id>
linked_auto_result: <path/to/evaluation_auto.json>
created_at: <YYYY-MM-DD>
author: <human_identifier>
````

---

## 2. 注目した差分の種類（選択）

本記録で注目した差分にチェックを入れる。

* [ ] Reference Diff
* [ ] Volume Diff
* [ ] Structural Diff

※ 複数選択可
※ 理由は次章で記載する

---

## 3. 注目理由（事実ベース）

AUTO JSON を参照した結果、
**注目した差分が「どこに現れているか」**を記載する。

* 条例・質問・分布などの位置関係
* 件数や割合は記載しない（AUTO JSON に委譲）

（自由記述・短文）

---

## 4. 判断を保留した理由

現時点で判断を行わない理由を記載する。

* 不足している比較軸
* 単独 run では判断できない理由
* 他 run / 他条件との比較が必要な理由

（自由記述）

---

## 5. 次に必要な比較・観点

Evaluation Judgment に進むために
**次に確認すべき観点・比較条件**を列挙する。

* 他 run との比較
* 評価軸候補（※評価は行わない）
* 追加 Observation が必要か否か

（箇条書き）

---

## 6. メモ（任意）

* 自動化可能だと感じた箇所
* 運用・設計上の気づき
* 次フェーズへの引き継ぎメモ

---

## 禁止事項（再掲）

以下を本記録に含めてはならない。

* 正しい／間違っている
* 良い／悪い
* 想定どおり／想定外
* 改善すべき／問題がある

※ これらは **Evaluation Judgment フェーズ専用語彙**である。

---

## まとめ

Evaluation HUMAN 記録 v0.2 は、

* 判断を行わない
* 事実を再集計しない
* 次の判断を可能にするための「余白」を残す

ための **人間専用メタログ**である。

---
