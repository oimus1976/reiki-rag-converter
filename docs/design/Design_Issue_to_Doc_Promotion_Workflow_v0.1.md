---
title: Design_Issue_to_Doc_Promotion_Workflow
version: v0.1
status: fixed
scope:
  - github_issue
  - design_process
  - documentation_workflow
related_docs:
  - Design_Master.md
  - PROJECT_GRAND_RULES.md
last_updated: 2026-01-02
---

# Epic Issue → 設計書 昇格スキーム

本書は、本プロジェクトにおける  
**「Epic Issue を最初から設計書型で書き、完了時に docs/ 配下の設計書へ昇格させる」**
ための運用ルールを定義する。

本スキームは、

- 二度書きを防ぐ
- 設計判断の履歴を失わない
- ChatGPT / 人間双方がレビューしやすい

ことを目的とする。

---

## 1. 基本思想

### 1.1 Issue ≒ 設計書（下書き）

本プロジェクトでは、Epic Issue を

> **「設計書の下書き（思考中・可変）」**

として扱う。

設計書との差分は **内容ではなく状態のみ** である。

| 項目 | Epic Issue | Design Doc |
| --- | --- | --- |
| 状態 | 思考中 / 可変 | 凍結 / 正本 |
| 目的 | 設計を詰める | 設計を固定する |
| 記述量 | 多くてよい | ほぼ同じ |
| 判断履歴 | 残る | 要点のみ残す |

---

## 2. Epic Issue の基本構造（設計書型）

Epic Issue は、**最初から以下の章立てで書く**。

```md
# 概要

## 背景 / 問題意識

## 目的

## スコープ
### やる
### やらない

## 設計方針（暫定）

## 決定事項

## 未決事項 / 論点

## Tasks
- [ ] ...
````

### 重要ルール

- 「暫定」「未決」を**明示**する
- この時点では **凍結しない**
- Tasks は **checklist として増減可**

---

## 3. 作業中の運用ルール（Issue = 思考ログ）

### 3.1 本文は「最新の設計状態」

- 決まったことは **本文の「決定事項」へ反映**
- ひっくり返った場合も **上書きして理由を残す**
- 古い案はコメントに追いやる

### 3.2 コメントの役割

Issue コメントは以下を許容する：

- 検討メモ
- 判断理由
- ChatGPT との設計対話ログ
- 差し戻しの理由

👉 **本文は常に最新版、コメントは履歴**

---

## 4. 完了条件（昇格トリガー）

Epic Issue が以下をすべて満たしたとき、
**設計書へ昇格可能**と判断する。

- 未決事項 / 論点 が **空**
- Tasks が **すべて完了**
- 「これ以上変えない」という意思決定ができている

---

## 5. 設計書への昇格手順（実務）

### 5.1 front-matter を追加

Issue本文の先頭に、以下を追加する。

```yaml
---
title: Design_xxx
version: v0.1
status: fixed
origin_issue: <issue番号>
last_updated: YYYY-MM-DD
---
```

### 5.2 ファイル配置

```text
docs/design/Design_xxx_v0.1.md
```

### 5.3 文言の最小調整

- 「暫定」「検討中」などの語を削除
- 時制を現在形に統一
- `Tasks` セクションは削除 or Appendix へ移動

👉 **本文の 8〜9 割はそのまま**

---

## 6. Issue 側のクローズ方法

Issue を close する際は、以下を記載する。

```md
設計が確定したため close。
内容は以下の設計書に昇格。
- docs/design/Design_xxx_v0.1.md
```

これにより：

- Issue = 設計に至る思考の履歴
- Design Doc = 凍結された正本

が両立する。

---

## 7. このスキームの利点（再掲）

- 二度書きしない
- 設計の「なぜ」が消えない
- Issue を貼るだけで設計レビューが可能
- PROJECT_STATUS / CHANGELOG と自然につながる

---

## 8. よくある失敗と回避策

### ❌ Issue をメモにしすぎる

→ **最初から章立てを書く**

### ❌ 設計書で全部書き直す

→ **front-matter を足すだけ**

### ❌ 完了判断が曖昧

→ **未決事項ゼロを条件にする**

---

## 9. 適用範囲

本スキームは以下に適用する：

- Epic Issue（設計を伴うもの）
- 外部連携 I/F
- Execution Input Contract
- Golden / Schema / Interface 設計

軽微な実装Issueには必須ではない。

---
