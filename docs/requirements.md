---
title: 要件定義書
version: 1.0
project: reiki-rag-converter
updated: 2025-12-02
---

# 要件定義書  
reiki-rag-converter（例規HTML → AI/RAG 向けテキスト変換ツール）

---

# 1. 背景

地方自治体の条例（例規集）は HTML 形式で公開されているが：

- DOM構造が不統一（HTML揺れ）
- 附則の扱いが自治体間で異なる
- 表は読み込みが難しい（colspan/rowspan）
- RAG向けの前処理が未整備

これらの課題により、AI検索やQ&Aシステムで  
「第3条の表を教えて」「附則の施行日を教えて」  
といった精度の高い回答が困難であった。

---

# 2. ユースケース（必須）

## 2.1 職員向け

- AI に条例の特定条文を尋ねる  
- 条・項・号の説明を生成  
- 附則の構造化・施行日抽出

## 2.2 研究・開発向け

- 条例データをRAGに投入  
- 例規集の自動解析  
- 表形式データの構造化

---

# 3. 機能要件

## 3.1 validate（構造検証）

- E001/E003/E004/E007 の検出
- S1/S2/S3 の構造イベント記録
- 詳細ログ（条例単位JSON）
- 総合ログ（summary_report / class_statistics / structure_summary）

## 3.2 convert（変換）

- 条・項・号を Markdown/TXT 化  
- 附則ヘッダ（s-head）の解析  
- 表（table）のMarkdown化  
- YAML frontmatter の付加  
- HTML → TXT の一括変換

---

# 4. 非機能要件

- **速度**：条例1000件を数分以内  
- **精度**：条番号抽出100%（v2.6で達成済）  
- **拡張性**：colspan/rowspan対応など将来の改善に耐える設計  
- **公開性**：著作権を侵害しない構造データのみをGitHub公開

---

# 5. 制約

- HTML本文そのものは著作物 → GitHub公開不可  
- DVD内のHTML構造に依存（自治体差に注意）  
- Python 3.10 以上

---

# 6. 今後の拡張要件（v3以降）

- colspan/rowspan  
- 附則モデル v0.6（改正文抽出）  
- 条・項・号の YAML 構造化  
- 別記様式の抽出  
- RAG向けチャンク分割と座標情報付加（v4）
