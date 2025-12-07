---
title: GOLDEN_POLICY
version: v1.0
doc_type: policy
project: reiki-rag-converter
created: 2025-12-07
updated: 2025-12-07
author: Sumio Nishioka + ChatGPT
tags:
  - oss
  - CI
  - golden-diff
  - governance
  - reiki-rag-converter
---

## GOLDEN POLICY v1.0

本書は、reiki-rag-converter プロジェクトにおける  
**Golden diff（Golden ファイル）管理ポリシーの公式規範**である。

Golden は「常に理想の出力」という意味ではなく、  
**“現在の設計仕様を固定化した境界線（Specification Freeze Point）”** であり、  
回帰性・再現性・品質保証の中核となる。

---

## Chapter 1. Overview（総論）

### 1.1 目的

- convert / validate / synthetic の出力差分の扱いを統一する。
- Golden diff を基準点とし、CI の安定運用と劣化検出を保証する。
- OSS プロジェクトとして透明性のある差分管理を行う。

### 1.2 適用範囲

本ポリシーは以下に適用する：

- convert_reiki_v2.x  
- validate_reiki_structure_v0.x  
- synthetic_html（特に P11〜P15）  
- CI（e2e.yml / smoke test）  
- Golden diff を利用する pytest

### 1.3 Golden の定義

Golden は次の特徴をもつ：

- **設計仕様に一致した出力の固定点（Expected Output）**  
- 仕様変更がない限り、内容を変更してはならない  
- CI が比較する対象であり、回帰テストの基準点である  

### 1.4 関連文書との関係（SSoT）

SSoT（Single Source of Truth）は以下の優先順序に従う：

1. PROJECT_STATUS.md  
2. PROJECT_GRAND_RULES.md  
3. Design 文書（Design_convert / Design_validate / synthetic 系）  
4. CI（e2e.yml）  
5. 実装コード（src/*.py）  
6. Golden ファイル  

Golden は “仕様の結果” を保存する最下層の位置づけ。

### 1.5 Qommons.AI 仕様との整合性（補足）

本プロジェクトの Golden は、外部RAG（特に Qommons.AI）の前処理仕様を考慮して評価される。

Qommons.AI は以下の特徴を持つ：

- HTMLタグはすべて削除される（DOM構造は利用されない）
- チャンクは文字数ベースで分割される（セマンティック分割なし）
- 表（table）はタグ除去後、行列構造が失われる可能性がある
- CSV はヘッダー行を検索精度の主要手がかりとする
- TXT と CSV の横断検索は「類似度上位に両方が入る場合のみ発火」する
- ナレッジ選択が単一ファイルの場合、横断検索は行われない

これらは Golden 出力の評価基準に直接影響するため、  
RAG 最適化テストは **Qommons_test_manual_v0.1.md** に基づき実施し、  
結果を Golden 更新可否判断の入力とする。

---

## Chapter 2. Golden diff の基本思想

### 2.1 Golden は「仕様の凍結点」である

Golden は正しさの絶対性を表すのではなく、  
現在の設計通りに実装が動いていることを保証するための「凍結点」である。

### 2.2 役割

- 回帰テストの基準  
- 劣化検出  
- OSS の透明性保持  
- 出力仕様の固定

### 2.3 Golden と設計書

- 設計書（Design_*.md）が仕様であり、Golden はその結果である。  
- Golden は仕様の代替にはならない。

### 2.4 Golden が更新される唯一の理由

**仕様が変更されたときのみ** Golden を更新する。

---

## Chapter 3. diff が揺れる要因分類

### 3.1 揮発性差分（無視対象）

- converted_at（日時）  
- JSON key 順序揺れ  
- 改行コード（LF/CRLF）  
- 空白・インデント揺れ  

### 3.2 構造的差分（実装修正により解決すべき）

DOM 構造解釈の揺れや内部不具合による差分。

### 3.3 仕様変更差分（Golden 更新が必要）

Design 文書の改訂によって出力仕様が変更された場合。

### 3.4 Bug による差分

実装バグの結果生じた差分。  
Golden は更新せず、実装を修正する。

---

## Chapter 4. Golden 更新可否判定フロー  

（Design → Implementation → Golden の順序を保証）

### 4.1 判定基準

1. 揮発性差分 → 無視  
2. Bug → 実装修正  
3. 仕様変更 → Design 文書改訂  
4. Design 文書更新後に Golden を更新

### 4.2 フローチャート

```planetext
差分発生
├─ 揮発性？ → 無視
├─ Bug？ → 修正（Golden 更新なし）
├─ 仕様変更？ → Design 文書改訂
└─ Golden 更新
```

### 4.3 Design 文書改訂が最優先

Golden 更新は **Design → 実装 → Golden** の順序で行う。

### 4.4 PR 説明項目

- 差分の種類  
- 仕様変更の有無  
- 該当 Design セクション  
- CI 影響  
- 後方互換性  

---

## Chapter 5. Golden 更新手順

### 5.1 更新前チェック

- PROJECT_STATUS.md  
- Design 文書  
- CI 設定  
- 実装依存関係

### 5.2 非破壊的変更では Golden 更新禁止

空白調整・インデント修正などの非仕様変更による差分では  
Golden を変更してはならない。

### 5.3 正式更新手順（仕様変更あり）

1. Design 文書更新  
2. 実装更新  
3. E2E 実行  
4. Golden 差分の確認  
5. Golden 更新  
6. CI グリーン確認  
7. PR マージ

### 5.4 コミットメッセージ例

```bash
Update Golden for convert_v2.8 spec change (colspan/rowspan support)
```

### 5.5 バージョン管理

- Golden v1：P11〜P15（永久固定）  
- Golden v2：将来の仕様変更に応じて導入

---

## Chapter 6. Breaking Change（破壊的変更）

### 6.1 定義

仕様の変更を伴い、出力結果が必ず変わる変更。

### 6.2 例

- convert_v2.8（colspan/rowspan）  
- validate_v0.6（章・節構造）  
- synthetic generator v0.3（meta schema 拡張）

### 6.3 必要な対応

- Design 文書改訂  
- Golden 更新  
- CHANGELOG への記録  
- STATUS.md 更新

---

## Chapter 7. Non-breaking Change（非破壊）

### 7.1 定義

出力仕様を変更しない微調整。

### 7.2 例

- 空白整形  
- コメント変更  
- ログ改善

### 7.3 Golden 更新禁止

非破壊的変更では Golden に触れてはならない。

---

## Chapter 8. Golden diff 比較方法（標準化）

### 8.1 比較ルール

- converted_at 比較除外  
- 改行コード LF 統一  
- 空白正規化  
- JSON key ソート比較

### 8.2 使用ツール

- pytest  
- diff  
- 正規表現 ignore patterns

### 8.3 差分の意味付け

- 等価差分 → 無視  
- 構造差分 → 要調査  
- 意味差分 → Golden または実装の更新

---

## Chapter 9. Synthetic HTML と Golden

### 9.1 Legacy（P01〜P10）

変更禁止。

### 9.2 Golden の中核（P11〜P15）

Golden v1 の基礎であり、変更は Breaking Change。

### 9.3 P16 以降

generator v0.3 以降の対象。Golden v1 には含めない。

### 9.4 meta schema 変更時

schema 変更は必ず Golden 更新とセットで扱う。

---

## Chapter 10. CI（e2e.yml）との整合

### 10.1 smoke test

削除不可。CI の憲法。

### 10.2 SKIP_E2E と exit code

0 件テスト → exit code 5 を回避する構造を維持。

### 10.3 Golden diff セクション

E2E 判定の最重要箇所。

---

## Chapter 11. Governance（権限・レビュー）

### 11.1 関係文書

- GRAND_RULES  
- Startup_Workflow  
- STATUS.md

### 11.2 役割と責任

- Golden 更新承認者（Reviewer）  
- 実装者（Developer）  
- ChatGPT アーキテクト（整合性監査）  

### 11.3 透明性

Golden 更新は理由・影響範囲・設計書更新をセットで記録。

---

## Chapter 12. 将来拡張

### 12.1 convert_v2.8 の Golden 影響

表構造（colspan/rowspan）により大幅な差分発生。

### 12.2 validate_v0.6

章・節イベント追加により JSON 出力が変化。

### 12.3 synthetic_generator v0.3

P16〜が増えることで Golden v1 → v2 移行の必要性。

### 12.4 Qommons.AI 仕様との連携強化

convert / validate / synthetic の出力は、  
Qommons.AI が実際に行う前処理（HTMLタグ除去・文字列化・CSVヘッダー依存検索）  
を踏まえて Golden として設計・維持される。

特に以下を Golden 評価項目として扱う：

- 表構造（colspan / rowspan）がタグ除去後にどのように失われるか
- TXT と CSV の横断検索が成立するか（検索上位に両方が出るか）
- HTML が混在した際の検索ノイズ耐性
- 生HTMLを Golden と比較する際の情報消失率

これにより、Golden は「RAGに投入した際に期待されるふるまい」を  
正確に反映する基準点として運用される。

---

## 付録 A. 用語集

Golden / Breaking Change / Non-breaking Change / Legacy / meta schema など。

## 付録 B. 更新履歴

v1.0（2025-12-07）初版制定。
