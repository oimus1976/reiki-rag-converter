---
title: Judgment – Primary Format Selection for Private Knowledge
judgment_id: judgment_primary_format_markdown_v0.2
schema_version: judgment.v0.2
decided_at: 2026-01-20
based_on:
  - artifacts/evaluation/bundle_2026-01-20_01/human/HUMAN_Evaluation_Record_2026-01-20_01_v0.2.md
scope:
  target: private_knowledge_primary_format
  candidates:
    - html_converted
    - markdown_converted
decision:
  selected: markdown
---

# Judgment Primary Format Selection for Private Knowledge

## 1. 本 Judgment の位置づけ

本 Judgment は、  
Evaluation v0.2 に基づき、

- 例規データをプライベートナレッジとして格納する際の
- **正本形式（Primary Format）**

を確定するための判断記録である。

本 Judgment は、

- モデル性能の優劣を評価するものではない
- HTML / Markdown の一般的価値を論じるものではない
- 個別回答の正誤を断定するものではない

---

## 2. 判断対象

以下の 2 形式を比較対象とした。

- HTML 変換版例規データ
- Markdown 変換版例規データ

両者は、

- 同一の原条例データ
- 同一の質問セット
- 同一の Evaluation フロー

に基づき生成されている。

---

## 3. 参照した観測事実

本 Judgment は、  
以下の HUMAN Evaluation Record に記載された観測事実を根拠とする。

- HUMAN Evaluation Record v0.2  
  （Run: 2026-01-20_01）  
  :contentReference[oaicite:0]{index=0}

同記録においては、以下の観測軸に基づく複数の Evidence が整理されている。

- 到達性（Retrieval Reach）
- 構造保持（Structural Integrity）
- 補完耐性（Hallucination Control）

---

## 4. 判断の要点（要約）

観測事実から、以下の傾向が確認されている。

- Markdown 変換版は、
  - 条例ID指定
  - 文書全体構成
  - 末尾条文・補則
  に対する到達性が安定している。
- Markdown 変換版は、
  - 章・条・附則といった
    文書構造単位を保持したまま解釈される傾向がある。
- HTML 変換版は、
  - 分かりやすさを目的とした補足説明が付加される傾向があり、
  - 条文外情報の補完が相対的に発生しやすい。

これらは、  
個別事例ではなく、  
複数条例・複数質問において再現的に観測されている。

---

## 5. Judgment（判断）

以上の観測事実を踏まえ、  
本プロジェクトにおいては、

> **プライベートナレッジに格納する例規データの正本形式として  
> Markdown 形式を採用する**

と判断する。

本判断は、

- 到達性の安定性
- 文書構造保持の一貫性
- 条文外補完の抑制傾向

が、  
プライベートナレッジの **再解釈耐性・再利用性**に寄与すると考えられるためである。

---

## 6. 判断の適用範囲と留保

本 Judgment は、以下に限定して適用される。

- 本プロジェクトにおける
  - 例規データ
  - プライベートナレッジ用途
  - RAG / 検索・参照基盤

以下については、本 Judgment の対象外とする。

- 住民向け公開資料としての最適形式
- 視覚的可読性や印刷適性の比較
- 将来のモデル・検索エンジン変更後の再評価

必要に応じて、  
新たな Evaluation を実施した上で、  
Judgment を更新することを妨げない。

---

## 7. 次フェーズへの接続

本 Judgment は、

- Judgment JSON v0.2
- Bundle v0.2 設計
- プライベートナレッジ構築方針

における **判断正本**として参照される。

本 Judgment 自体は、  
Evaluation の代替ではなく、  
Evaluation の結果を閉じるための終端記録である。

---
