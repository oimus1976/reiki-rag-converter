---
title: test_plan
version: v1.0
doc_type: reference
project: reiki-rag-converter
created: 2025-12-02
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - testing
  - reference
  - oss
  - reiki-rag-converter
---

## テスト計画書

reiki-rag-converter（validate v3.1 / convert v2.7.1）

---

## 1. テスト目的

- 条・項・号の抽出精度検証  
- 附則の分割精度  
- 表（table）の変換精度  
- validate → convert の連携正当性  
- 大規模条例群へのスケールテスト  
- 将来拡張（colspan/rowspan）の基盤確認

---

## 2. テスト範囲

- validate（v3.1）  
- convert（v2.7.1）  
- end-to-end テスト（HTML → TXT）  
- サンプル19件（sample.zip）  
- 追加DOMパターン（12/55/80）

---

## 3. テスト項目

### 3.1 validate

| No | テスト項目 | 期待結果 |
|----|------------|-----------|
| V-01 | E001 未知class検出 | 全未知class検出 |
| V-02 | E003 公布日欠落 | 条例番号欠落無し |
| V-03 | S1 表（本則） | 正しい index を出力 |
| V-04 | S2 表（附則） | 正しい index を出力 |
| V-05 | S3 リスト構造 | ul/li を検出 |

### 3.2 convert

| No | テスト項目 | 期待結果 |
|----|------------|-----------|
| C-01 | 条見出し抽出 | `## 第X条（○○）` |
| C-02 | 項本文の抽出 | 条見出し直後に本文 |
| C-03 | 号の bullet 化 | `(1)` → `- (1)` |
| C-04 | 附則見出し | `## 附則（…）` |
| C-05 | 表変換 | Markdown表に変換 |

---

## 4. テストデータ

- k518RG00000012.html  
- k518RG00000055.html  
- k518RG00000080.html  
- sample.zip（19件）

---

## 5. 合否基準

- 条番号抽出：100%  
- 附則誤結合：0件  
- 表の抽出：実データと一致  
- RAG検索の精度：Qommons.AIで正答率が目視確認で80%以上  

---

## 6. 実行手順

```bash

python validate_reiki_structure_v0.5.2.py --source E:/reiki_honbun
python convert_reiki_v2.7.py --source E:/reiki_honbun -o output_md
pytest -q

```

---

## 7. 今後の拡張

- syntheticサンプル（附則10本・表多数）でCI  
- colspan/rowspan対応後の回帰試験  
- 条・項・号の YAML 化後の階層整合チェック  

## 8. Smoke Test に関する運用ルール（必須）

本プロジェクトの CI は `SKIP_E2E` 環境変数により実HTMLの E2E テストが
スキップされる仕様を持っています。

そのため pytest が「テスト 0 件」となると終了コード `5` を返し、
GitHub Actions が失敗扱いとなります。

これを防ぐため、以下のテストファイルは CI 安定運用のための
必須コンポーネントとする。

- tests/test_smoketest.py

このテストは削除・改名してはならず、常に 1 件の pass テストを提供する。

## 7. Qommons.AI 結合テスト計画

### 7.1 テスト環境

- プラットフォーム：Qommons.AI（かつらぎ町テナント）
- モデル：
  - 標準：Claude 4.5 Sonnet（国内リージョン） or PLaMo 2.1 Prime
  - 参考：Chat-GPT 5.1 / Chat-GPT 5 (Reasoning) / Gemini 3.0 Pro
- Web検索：
  - 原則 OFF（条例・規則のQAでは外部情報に依存しない）
- ナレッジスコープ：
  - パターンA：単一ファイルのみ選択（PoC・デバッグ用）
  - パターンB：共有＋所属部署（本番想定）

### 7.2 テストデータ

- TXT＋CSV ハイブリッド用
  - 手数料条例（TXT）
  - 手数料条例_別表（CSV）
  - ノイズ用ダミーファイル（似たような語彙を含むが条例とは無関係）
- HTML比較用
  - reiki_honbun から抽出した代表サンプル（例）：
    - k518RG00000022.html（複雑DOM）  
    - k518RG00000075.html（表を含む条例）  
    - k518RG00000097.html（表構造テスト用） など
- いずれも **TXT/CSV 版と HTML 生ファイル版** を用意し、
  Qommons.AI側でナレッジ差し替えながら比較する。

### 7.3 テストシナリオ（RAG）

| ID | シナリオ | 目的 |
|----|----------|------|
| RAG-01 | 「住民票の写しの手続きと手数料をまとめて教えて」 | TXT＋CSV両方から引用されるか |
| RAG-02 | 「この手数料一覧（CSV）は何の条例に関係していますか？」 | CSV説明行から条例名を特定できるか |
| RAG-03 | 「手数料の一覧を教えて」 | CSVの表を適切に読み取り、一覧化できるか |
| RAG-04 | 「手続きの流れについて教えて」 | 条例本文に無い情報は「無い」と言いつつ、一般的な補足を分離できるか |
| RAG-05 | ノイズ混入時の質問（ダミーファイルを含めた状態） | 関係ないファイルに引きずられず、正しい条例を参照するか |
| RAG-06 | HTML版ナレッジで RAG-01〜05 を再実行 | HTML直接投入時と TXT/CSV 版との差を比較する |

### 7.4 評価方法

- 各シナリオについて、回答を次の3区分で判定する。
  - ○：条例の内容に沿っており、引用元ファイルも妥当
  - △：概ね正しいが、条番号・名称・金額等に軽微な誤差あり
  - ×：条例に反する内容、または完全に的外れ
- モデルごとに集計し、
  - 「○＋△」が80%以上となることを合格条件とする。
- 特に RAG-01〜03 では、
  - 回答中に TXT と CSV の両方が引用されているか  
  - CSV冒頭に埋め込んだ説明行が引用されているか
  をチェックし、TXT＋CSV設計の妥当性を検証する。

### 7.5 回帰テスト

- convert / validate / synthetic 系のバージョンアップ時には、
  - 手数料条例セット（TXT＋CSV＋HTML）を用いた RAG-01〜03 を最低限実施する。
- GOLDEN_POLICY_v1.0 で定義する「Golden質問セット」に、  
  上記シナリオの代表質問を組み込む。

