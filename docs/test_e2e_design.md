---
title: E2Eテスト設計書（validate → convert）
version: 1.1
project: reiki-rag-converter
updated: 2025-12-04
status: active
---

# E2Eテスト設計書 v1.1  
（validate v3.1 → convert v2.7.1）

本書は、例規HTMLを入力として  
**validate（構造検証） → convert（Markdown/TXT変換）**  
の一連の流れが、実運用に耐えうる品質で動作するかを確認する  
**End-to-End（E2E）テスト** の設計文書である。

v1.1 では、v1.0 のレビュー結果を踏まえ、

- 異常系E2E追加  
- 期待結果の検証方法の明確化  
- バージョン進化時の扱い  
- セキュリティ観点追加  
- CI（GitHub Actions）での前提整理  

など、品質保証の観点を強化した。

---

# 1. 目的

E2Eテストの目的：

1. **validate の結果が convert に悪影響を与えないことを保証する**
2. **条例本文・表・附則を欠落なく変換できることを確認する**
3. **RAG投入に耐える構造（Markdown + YAML）の整合性を担保する**
4. **サンプル19件（sample.zip）＋代表3件（12/55/80）で回帰テスト可能とする**
5. **CI（GitHub Actions）での自動化を前提に設計する**
6. **異常系データへの耐性（堅牢性）を確認する**

---

# 2. テスト対象範囲

E2E 対象の “入口 → 出口”：

```

HTML
↓
validate_reiki_structure_v0.5.2
↓（E系/S系 JSON）
convert_reiki_v2.7.1
↓
RAG-ready TXT

```

## 2.1 validate（v3.1）の対象
- 条・項・号・附則の DOM 認識
- 表（table）、リスト（ul）検出
- E001/E003/E004/E007
- structure_summary JSON 生成

## 2.2 convert（v2.7.1）の対象
- 条本文の抽出
- 項・号の bullet 化
- 附則（s-head）の判断
- 表の Markdown 変換
- YAML frontmatter

## 2.3 出力TXTの品質
- 欠落なし
- 誤結合なし
- 文字化けなし
- 表記揺れなし

---

# 3. 成功基準（正常系の定義）

以下のすべてを満たすこと。

## ✔ 3.1 validate

| 観点 | 成功条件 |
|------|----------|
| E系例外 | E003/E004/E007 が 0 |
| E001 | 未知classは許容（例規HTML特性） |
| Sイベント | S1/S2/S3 が DOM通りに出現 |
| JSON | exceptions・structure_summary が正常 |

## ✔ 3.2 convert

| 観点 | 成功条件 |
|------|----------|
| 条見出し | `## 第X条（○○）` が正確 |
| 条本文 | 条タイトル直後に本文が抽出される（欠落0） |
| 項・号 | `(1)` → `- (1)` |
| 附則 | `## 附則（…）` が DOM順に一致 |
| 表 | `<table>` → Markdown表 |
| YAML | id/title/date が正確 |

## ✔ 3.3 validate → convert 整合性

- validate の S1/S2（検出表数） == convert の Markdown表数  
- validate の条番号一覧 == convert の条見出し数  
- validate の附則数 == convert の附則見出し数  

---

# 4. 入力データ

## 4.1 代表サンプル（必須）
- k518RG00000012.html  
- k518RG00000055.html  
- k518RG00000080.html（表あり）

## 4.2 sample.zip（19件）
DOM揺れ・附則構造・表の多様性を網羅したセット。  
E2Eテストの主力データとする。

---

# 5. テストケース

## 5.1 正常系

| ID | テスト項目 | 入力 | 出力期待 |
|----|------------|------|-----------|
| E2E-01 | 条見出し + 本文 | 12.html | 第1条〜最終条まで完全抽出 |
| E2E-02 | 項・号抽出 | 12.html | `(1)` → `- (1)` |
| E2E-03 | 表変換 | 80.html | 表がMarkdown表として出現 |
| E2E-04 | 附則分割 | 55.html | 附則が誤結合なし |
| E2E-05 | YAML | 全件 | id/title/date が正しい |
| E2E-06 | validate整合 | 全件 | Sイベント数とMarkdown内容一致 |
| E2E-07 | 19件変換 | sample.zip | 全TXT生成 |

---

# 6. 異常系 E2E（v1.1 追加）

異常HTMLに対する堅牢性テスト。

| ID | 異常条件 | 期待結果 |
|----|-----------|-----------|
| E2E-A01 | #primaryInner2 欠落 | validate: E007 / convert: スキップ or 安全停止 |
| E2E-A02 | 条番号なし（articleのみ） | validate: OK（class検出） / convert: 条見出し除外されても落ちない |
| E2E-A03 | <table> のみ存在 | validate: S1/S2 検出 / convert: 表のみ出力、クラッシュなし |
| E2E-A04 | HTML破損（タグ未閉じ） | validate: 解析は継続 / convert: 落ちない |
| E2E-A05 | 想定外の大量class | validate: E001多数 / convert: 出力は破綻しない |
| E2E-A06 | 文字化け文字混入 | convert: UTF-8出力、� や ? を含まない |

異常系は **CI の nightly** で実行してもよい。

---

# 7. 期待結果の検証方法（v1.1 追加）

E2Eテストは以下の2方式を併用する。

## 7.1 ゴールデンファイル比較方式（推奨）
- 代表3件（12/55/80）について  
  `tests/golden/*.txt` を保存  
- convert の出力と diff  
- 条文の改訂やコード仕様が変わらない限り一致することが成功条件

メリット：  
出力の「劣化」を即検出（最強の回帰テスト）

## 7.2 構造レベル比較
sample.zip など件数が多い場合は：

- 見出し数  
- 表の数  
- YAML項目  
- 附則数  

などの **構造だけ**比較して成功/失敗を判定する。

---

# 8. バージョン進化時の扱い（v1.1追加）

v2.7.1 → v2.8 → v3.0 で出力形式が変わる場合：

- **後方互換の仕様変更**  
  → ゴールデンファイルとの差分が 0 であるべき  
- **非互換の仕様変更（v3.0 など）**  
  → ゴールデンファイルを更新し、PRで説明を必須化

E2Eテストは「互換か非互換か」を判断するための基準としても利用する。

---

# 9. セキュリティ観点（v1.1 追加）

本ツールはローカル実行を前提とするが、以下を保証する。

1. **HTML内の <script> や <iframe> は決して実行しない**  
   → BeautifulSoup がテキスト処理であることを前提に確認  
2. **パス・トラバーサル防止**  
   → law_id は DVD データ基準で安全である前提  
3. **外部ネットワークアクセスは行わない**  
4. **文字コード崩壊時に例外を投げない（chardet使用）**

E2Eテストでは必要に応じて script混入HTMLを用意して安全性を確認する。

---

# 10. CI（GitHub Actions）前提（v1.1拡張）

## 10.1 実行条件
- Python 3.10 / 3.11 / 3.12 の matrix 実行  
- OS は ubuntu-latest  
- sample.zip を `samples/html/` に展開する

## 10.2 成功条件
- `pytest tests/test_e2e.py` が PASS  
- validate → convert がすべて成功  
- diff（ゴールデンファイル）が 0  
- 全出力TXTが存在  
- E003/E004/E007 が 0

## 10.3 artifacts（任意）
- E2E失敗時のみ  
  - JSON（validate）  
  - TXT（convert）  
  を artifacts としてアップロード

---

# 11. 今後の拡張

- colspan/rowspan 対応後のE2E  
- 別記様式（画像/iframe）抽出のE2E  
- 附則モデル v0.6 の回帰テスト  
- synthetic HTML（長大条文10章）の CIテスト  
- 差分検知ツール（diffview）との連携

---

# 付録：概念図（再掲）

```

```
            +-------------------------------+
```

HTML ----------> |      validate (v3.1)         |
|  E/S検出 + JSON出力          |
+-------------------------------+
|
v
+-------------------------------+
|     convert (v2.7.1)          |
| 条文/項/号/附則/表 → TXT化     |
+-------------------------------+
|
v
RAG-ready TXT

```
```

---
