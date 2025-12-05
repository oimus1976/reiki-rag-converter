---
title: "Exception Check Design v3.2"
version: "3.2"
status: "stable"
updated: "2025-12-06"
authors: ["reiki-rag-converter development team"]
---

# Exception Check Design v3.2  
**（validate_reiki_structure_v0.5.3 対応版）**

---

## 1. 目的

本設計書は、条例 HTML の構造解析における  
**例外検知（Exception）および構造イベント（Structural Event）** の仕様を定義する。

v3.2 では、以下の点がアップデートされた：

- validate の JSON 出力が set を含んでも安全にシリアライズされる（v0.5.3 反映）
- synthetic HTML（P1〜P10）に対応した例外・イベントの定義を補強
- 例外・イベントの分類と発生条件を正式版として確定

---

## 2. スコープ

対象：

- validate_reiki_structure_v0.5.3  
- synthetic HTML（P1〜P10）  
- 実 HTML（ぎょうせい系 DOM 揺れを含む）

除外：

- convert の解析ロジック  
- 改正文パーサ（v0.6 以降）

---

## 3. 例外の基本方針（Exception Policy）

### ✔ Exception は「構造が期待と異なる場合の警告」

例外が検出されても **validate は終了コード 0（正常）** を返す。  
これにより、以下が保証される：

- 人手による例外レビューが可能  
- convert への入力が継続できる  
- synthetic の E2E テストを安定的に実行できる  

※ v3.0 以前は validate 終了時に例外件数を評価していたが、v3.2 では保守性向上のため廃止。

---

## 4. 例外分類（Exception Definitions）

### ### E001: `.eline` が見つからない

**説明**  
条例本文のルートノードとなる `.eline` が検出できなかった。

**原因例**  
- DOM 構造が自治体ごとに異なる  
- synthetic P10（壊れた HTML）のテスト用

**payload**
```json
{ "type": "E001", "message": ".eline が見つからない" }
```

---

### ### E002: `div.article`（条）が存在しない

**説明**
`.eline` 内に条ブロックが見つからない。

**発生例**

* 条が 1 条もない条例（稀）
* synthetic P10 のエラーケース

---

### ### E003: 条内に項（clause）が存在しない（警告）

**説明**
条が存在するのに、項（div.clause）がない。

**備考**
正常ケース（条文が短い場合）もあるため、例外ではなく「警告」。

---

### ### E004: 項内に号（item）が存在しない（警告）

**説明**
項（clause）の配下に item が無い場合の警告。

---

### ### E007: `.s-head` が複数存在する（附則の複数構造）

**説明**
附則が 2 個以上検出された。

**備考**
正常な条例でも発生するため、例外ではなくイベント扱い。

---

## 5. 構造イベント（Structural Event）

validate は構造上の「特記事項」を event として収集する。

### S101: 附則が存在

```
{ "event": "found_supplement", "count": n }
```

### S102: 表（table）が存在

```
{ "event": "found_table", "count": n }
```

### S103: 箇条書き（ul/li）

```
{ "event": "found_list", "type": "ul" }
```

### S104: 別記様式（iframe/img）

```
{ "event": "found_form", "type": "iframe" }
```

synthetic P1〜P10 は上記イベントを網羅するよう設計されている。

---

## 6. v0.5.3 での仕様変更（重要）

### 🔧 **変更点：set → JSON シリアライズ安全化**

### Before（v0.5.2）

validate の出力には `classes: set([...])` が含まれ、
JSON 保存時に **TypeError: Object of type set is not JSON serializable** となる。

### After（v0.5.3）

`_to_serializable()` による再帰変換を導入。

* set → sorted list
* dict, list, tuple → 再帰的に JSON 互換へ変換
* validate 全体が JSON 安全化
* synthetic HTML の E2E が安定

---

## 7. 出力 JSON 形式（正式仕様）

```json
{
  "title": "条例タイトル",
  "exceptions": [
    { "type": "E001", "message": ".eline が見つからない" }
  ],
  "events": [
    { "event": "found_supplement", "count": 2 }
  ],
  "classes": [
    "article",
    "clause",
    "item"
  ]
}
```

---

## 8. synthetic HTML との対応

| Synthetic パターン | 想定例外         | 想定イベント |
| -------------- | ------------ | ------ |
| P1（基本）         | なし           | S101   |
| P2（項・号）        | なし           | S101   |
| P3（表）          | なし           | S102   |
| P4（附則複数）       | E007         | S101   |
| P5（画像様式）       | なし           | S104   |
| P6（ul 箇条書き）    | なし           | S103   |
| P7（編構造）        | なし           | あり     |
| P8（PDF iframe） | なし           | S104   |
| P9（長文）         | なし           | S101   |
| P10（壊れた HTML）  | E001/E002 など | ほぼなし   |

---

## 9. 今後の拡張（v3.3〜）

* **編（chapter）構造の詳細分析**
* **別記様式の深度解析（表／PDF／画像差異）**
* **validate の高速化（マルチプロセス対応）**
* **改正文（令和○○年条例第○号）解析の統合**

---

## 10. リファレンス実装

この設計を実装した最新バージョン：

```
src/validate_reiki_structure_v0.5.3.py
```

※ v0.5.2 は後方互換のため残置。

---

## 11. 変更履歴

### v3.2（2025-12-06）

* validate v0.5.3 に対応
* set → list の JSON 互換化を反映
* synthetic_html のイベント仕様を正式文書化
* P10（エラーケース）の例外体系を確立

### v3.1

* E 系例外定義の基礎版
* Synthetic P1〜P6 に対応

---

# 以上
