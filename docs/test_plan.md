---
title: テスト計画書
version: 1.0
project: reiki-rag-converter
updated: 2025-12-02
---

# テスト計画書
reiki-rag-converter（validate v3.1 / convert v2.7.1）

---

# 1. テスト目的

- 条・項・号の抽出精度検証
- 附則の分割精度
- 表（table）の変換精度
- validate → convert の連携正当性
- 大規模条例群へのスケールテスト
- 将来拡張（colspan/rowspan）の基盤確認

---

# 2. テスト範囲

- validate（v3.1）
- convert（v2.7.1）
- end-to-end テスト（HTML → TXT）
- サンプル19件（sample.zip）
- 追加DOMパターン（12/55/80）

---

# 3. テスト項目

## 3.1 validate

| No | テスト項目 | 期待結果 |
|----|------------|-----------|
| V-01 | E001 未知class検出 | 全未知class検出 |
| V-02 | E003 公布日欠落 | 条例番号欠落無し |
| V-03 | S1 表（本則） | 正しい index を出力 |
| V-04 | S2 表（附則） | 正しい index を出力 |
| V-05 | S3 リスト構造 | ul/li を検出 |

## 3.2 convert

| No | テスト項目 | 期待結果 |
|----|------------|-----------|
| C-01 | 条見出し抽出 | `## 第X条（○○）` |
| C-02 | 項本文の抽出 | 条見出し直後に本文 |
| C-03 | 号の bullet 化 | `(1)` → `- (1)` |
| C-04 | 附則見出し | `## 附則（…）` |
| C-05 | 表変換 | Markdown表に変換 |

---

# 4. テストデータ

- k518RG00000012.html
- k518RG00000055.html
- k518RG00000080.html
- sample.zip（19件）

---

# 5. 合否基準

- 条番号抽出：100%
- 附則誤結合：0件
- 表の抽出：実データと一致

- RAGに関する評価は、単純な正答率や点数評価は行わない。
  目視による「正答率80%以上」という従来基準は参考情報とし、
  合否判定の主基準とはしない。

- Qommons.AI を用いた RAG 評価は、
  **Golden_Ordinance_Set × Golden_Question_Pool_A** を対象とし、
  逸脱検知を目的とした **Gate 判定方式**で実施する。

- 評価軸・判定基準・Gate 運用の詳細は、
  以下の公式ドキュメントを参照すること。

  - **Qommons Evaluation Framework v0.1**
    (`docs/Qommons_Evaluation_Framework_v0.1.md`)

※ RAG 応答の観測データ取得には、
外部プロジェクト「gov-llm-e2e-testkit」を利用する。
同プロジェクトは観測データのみを提供し、
評価・採否判断は本プロジェクト側で行う。

---

# 6. 実行手順

```

python validate_reiki_structure_v0.5.2.py --source E:/reiki_honbun
python convert_reiki_v2.7.py --source E:/reiki_honbun -o output_md
pytest -q

```

---

# 7. 今後の拡張

- syntheticサンプル（附則10本・表多数）でCI
- colspan/rowspan対応後の回帰試験
- 条・項・号の YAML 化後の階層整合チェック
