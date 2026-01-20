---
schema_version: "0.1"
document_type: design_spec
record_type: evaluation_judgment
status: FIX
---

# Evaluation Judgment フェーズ設計 v0.1

---

## 本文書の位置づけ

本ドキュメントは、**Evaluation Judgment フェーズの設計正本**である。

Evaluation Judgment は、Evaluation プロセス全体において  
**良否・妥当性・結論を明示的に記述してよい唯一のフェーズ**であり、  
それ以前の Observation / AUTO / HUMAN フェーズとは明確に責務を分離する。

---

## フェーズ全体における位置づけ

Evaluation プロセスは以下の順序で構成される。

```

Observation
↓（事実観測）
Evaluation AUTO
↓（集計事実）
Evaluation HUMAN
↓（判断保留理由・比較観点）
Evaluation Judgment

````

Evaluation Judgment は、  
**複数の Evaluation Run を比較した上で判断を下す最終工程**である。

---

## Evaluation Judgment の責務

Evaluation Judgment フェーズの責務は以下に限定される。

- AUTO JSON および HUMAN 記録を根拠として判断を行う
- 判断結果とその射程を明示する
- 判断の限界・留保条件を明文化する
- 次のアクション（再評価・追加観測等）を決定する

---

## 明示的に行わないこと

Evaluation Judgment フェーズでは以下を行わない。

- Observation の再計算・再解釈
- AUTO JSON の再集計
- HUMAN 記録の改変
- 単独 run に基づく判断

---

## Judgment フェーズへの入場条件（Gate）

以下の条件を **すべて満たした場合のみ** Evaluation Judgment を実施する。

- [ ] observation_result.json が存在する
- [ ] evaluation_auto.json（v0.2 以上）が存在する
- [ ] Evaluation HUMAN Record（v0.2 以上）が 1 本以上存在する
- [ ] 対象 run_id が一致している
- [ ] 比較対象となる run が 2 本以上存在する

---

## Judgment の成果物

### 正本成果物

```text
docs/eval/Evaluation_Judgment_<judgment_id>.md
````

※ v0.1 では Markdown を正本とする

---

## Evaluation Judgment Record（v0.1）構造

### YAML Frontmatter（必須）

```yaml
schema_version: "0.1"
record_type: evaluation_judgment
judgment_id: <judgment_id>
target_runs:
  - <evaluation_run_id_1>
  - <evaluation_run_id_2>
created_at: <YYYY-MM-DD>
author: <human_identifier>
```

---

### 本文構造

```md
# Evaluation Judgment Record

## 0. Judgment 前提確認
- [ ] AUTO JSON を参照している
- [ ] HUMAN Record を参照している
- [ ] 単独 run で判断していない
- [ ] 本 Judgment は再評価ではない

## 1. 比較対象
- 対象 run 一覧
- 比較条件（モデル、設定、入力条件など）

## 2. Judgment Scope
本 Judgment が対象とする差分種別：

- [ ] Reference Diff
- [ ] Volume Diff
- [ ] Structural Diff

## 3. 判断根拠

### 3.1 AUTO 由来の事実
- 参照した evaluation_auto.json
- 判断に用いた分布・傾向（再集計しない）

### 3.2 HUMAN 記録からの補足
- 判断保留理由がどのように解消されたか
- 比較により明らかになった差異

## 4. Judgment（結論）
- 判断結果を明示的に記載する
- 判断の射程（どこまで言えるか）を明示する

## 5. 判断の限界・留保
- 今回の Judgment では言えないこと
- 今後の比較・評価に委ねる事項

## 6. 次アクション
- 再 Evaluation の要否
- 追加 Observation の要否
- フレームワーク修正の検討要否
```

---

## Judgment フェーズで使用可能な語彙

Evaluation Judgment フェーズでは、以下の語彙の使用を許可する。

* 妥当である / 妥当でない
* 改善している / 悪化している
* 評価できる / 評価できない
* 判断する / 結論づける

※ これらは他フェーズでは使用してはならない。

---

## Judgment フェーズの性格（v0.1）

* 人間による判断を前提とする
* 再現性はリンク・Gate 条件により担保する
* JSON 正本化は v0.2 以降で検討する

---

## まとめ

Evaluation Judgment フェーズは、

* Evaluation の最終判断を担う唯一の工程であり
* それ以前のフェーズを破壊せず
* 次の意思決定に接続する

ための **判断専用フェーズ**である。

---
