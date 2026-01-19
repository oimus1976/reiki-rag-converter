# Answer Diff Observation Summary（v0.1）

## 本ドキュメントの位置づけ

本ドキュメントは、Answer Diff Observation フェーズにおいて生成される  
`observation_result.json` を **正しく解釈するための仕様サマリ**である。

本フェーズの目的は、HTML 版 answer.md と Markdown 版 answer.md の差分を  
**評価・判断・適否判定を行わず、観測事実として固定すること**にある。

したがって、本ドキュメントおよび Observation 成果物には、  
差分の良否・適切性・意味付けは一切含まれない。  
それらは Evaluation Framework 側の責務とする。

---

## 観測フェーズの責務範囲

Observation フェーズでは、以下のみを行う。

- 差分の有無・量・構造を、機械的かつ再現可能な方法で算出する
- 観測結果を JSON および Markdown として固定する

以下は **本フェーズの責務外**である。

- 差分の評価・解釈
- 品質判断・優劣判定
- 改善提案や推奨の提示

---

## 観測対象と Diff の種類（v0.1）

本フェーズでは、以下 3 種類の Diff を観測対象とする。

### Reference Diff（参照差）

- 条（第○条）
- 項（第○項）
- 附則

について、**出現有無のみ**を観測する。

文章内容の言い換え、要約、説明粒度の違いは対象外とする。

---

### Volume Diff（情報量差）

HTML 版と Markdown 版の間で、  
**文章量の差を定量的に観測**する。

観測指標は以下のとおり。

- **chars**  
  回答全文の文字数（Unicode コードポイント数）

- **lines**  
  改行（`\n`）で区切った行数

- **paragraphs**  
  空行で区切られた、1 行以上の非空行ブロック数  
  （見出し・本文・箇条書き等の構文的区別は行わない）

---

### Structural Diff（構造差）

回答中に含まれる以下の構造要素について、  
HTML 版と Markdown 版の **一致／不一致のみ**を観測する。

- 見出し行
- 箇条書き項目
- 附則の有無

v0.1 では、構造要素の個数や内訳は記録せず、  
構造が同一かどうかの boolean 値のみを観測結果として出力する。

---

## 観測仕様に関する重要な前提（v0.1）

### diff_flags の分布について

diff_flags（Reference / Volume / Structural）は、  
分布を前提とした指標ではない。

観測対象データの性質によっては、  
特定の Diff が **全 AnswerPair で true となる run が存在し得る**。

これは観測結果としての事実を示すものであり、  
実装不備や異常を意味するものではない。

---

### observations 配列の並び順について

`observation_result.json` に含まれる observations 配列の並び順は、  
**意味を持たない**。

各観測結果は、`ordinance_id` および `question_id` により識別される。  
配列の順序に基づく比較や差分解釈は行わないこと。

---

### 正規化・構文解釈を行わない方針について

本 Observation フェーズでは、以下を **意図的に行わない**。

- HTML の正規化
- DOM 構造の解釈
- Markdown 構文（見出し・リスト等）の意味的解釈

これは差分を減らすためではなく、  
**形式差を歪めずに観測するための設計判断**である。

正規化や構文解釈を前提とした分析は、  
v0.2 以降、または Evaluation フェーズで扱う課題とする。

---

## 利用上の注意

- `observation_result.json` は、単体での比較・評価を意図していない
- run 間比較や時系列評価は、Evaluation Framework を通して行うこと
- 観測結果の再解釈・再計算・補正は行わないこと

---

## 本フェーズの完了条件（v0.1）

以下を満たした時点で、  
Answer Diff Observation フェーズ（v0.1）は完了とする。

- 全 AnswerPair について ObservationResult が生成されている
- Reference / Volume / Structural の各 Diff が算出されている
- 観測結果が JSON および Markdown の成果物として固定されている
- 成果物に評価・判断を含む記述が存在しない
