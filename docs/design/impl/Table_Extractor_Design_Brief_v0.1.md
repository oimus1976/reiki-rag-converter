---
title: "Table Extractor Design Brief"
doc_type: implementation_brief
component: table_extractor
version: "v0.1"
status: draft
related_spec:
  - Golden_Annex_Extraction_Spec_v1.0.md
scope: annex_table_extraction
authoring_policy:
  html_filename: preserve
  public_api: single_entrypoint
created_at: 2026-01-23
---

# Table Extractor Design Brief（v0.1）

## 1. 目的

本ドキュメントは  
`Golden_Annex_Extraction_Spec_v1.0.md` で確定した **別表抽出仕様**を、

- どのような責務分割で
- どのような関数I/F構造で

Pythonコード（`table_extractor.py`）に落とし込むかを示す  
**実装ブリーフ**である。

本書は **仕様（Spec）ではない**。  
抽出結果の合否基準は Golden Spec にのみ依拠する。

---

## 2. 設計上の基本方針

### 2.1 公開APIは1つだけとする

`table_extractor.py` が外部に公開する関数は、以下の1つのみとする。

```python
extract_annex_tables(html: str, source_html: str) -> List[Annex]
```

#### 理由

- 呼び出し側（converter / pipeline）を固定するため
- 抽出ロジックの変更が外部I/Fに波及するのを防ぐため
- Golden Spec を「入力 → 出力」の黒箱として扱うため

---

### 2.2 HTMLファイル名は入力として必須とする

`source_html`（例：`k518RG00000219.html`）は
**extract_annex_tables の必須引数**とする。

#### 理由

- HTMLファイル名は Golden Set における一次識別子
- table_extractor 内でファイル名を生成・改変しない
- 抽出IRに必ず由来を残すため

---

## 3. 中間概念の導入理由

### 3.1 AnnexHeading

```text
AnnexHeading
  - annex_number
  - annex_caption
  - node (DOM)
```

#### 導入理由

- 「別表第◯」という **意味的見出し**をDOM上で保持するため
- 単なる文字列grepではなく、構造として扱うため
- 後続処理で「どの別表に属するか」を決定する起点にするため

---

### 3.2 AnnexBlock

```text
AnnexBlock
  = AnnexHeading + その論理的配下ノード群
```

#### 導入理由

- 別表の **探索範囲（見出し〜次の見出し）** を明示的に表現するため
- table 抽出ロジックを「範囲処理」として独立させるため
- Golden Spec §4（探索範囲定義）をコード構造に直接反映するため

---

## 4. 処理フェーズの分離

table_extractor は、以下の4段階に責務を分離する。

1. **別表見出し検出**

   - `_find_annex_headings`
2. **別表ブロック生成**

   - `_iter_annex_blocks`
3. **table 抽出**

   - `_extract_tables_from_block`
4. **table → IR 変換**

   - `_table_to_ir`

### 分離する理由

- grep では切れなかった責務境界を明示するため
- 後続フェーズ（rowspan/colspan対応）を局所化するため
- 各段階を単体テスト可能にするため

---

## 5. 非目標（Non-Goals）

本実装ブリーフでは、以下を **意図的に扱わない**。

- rowspan / colspan の正規化
- table の意味解釈（税率計算等）
- 様式抽出
- 画像別表のOCR
- CSV / Markdown 出力仕様

これらは **次フェーズ以降**の責務とする。

---

## 6. Golden Spec との関係

- 抽出対象の定義
  → `Golden_Annex_Extraction_Spec_v1.0.md`
- 抽出「方法」の判断
  → 本ドキュメント
- 合否判定
  → Golden Spec のみを基準とする

本ブリーフは、Golden Spec を **壊さずに実装するための補助線**である。

---

## 7. 状態宣言

本ドキュメントは
**Table Extractor 実装ブリーフ v0.1（ドラフト）**として作成する。

I/F スケルトン実装完了時点で内容を再確認し、
必要に応じて v0.2 へ更新する。
