---
title: Design_Document_Directory_Policy
version: v0.1
status: proposal
scope:
  - documentation
  - repository_structure
  - design_process
related_docs:
  - Design_Master.md
  - Design_Issue_to_Doc_Promotion_Workflow.md
last_updated: 2026-01-02
---

# docs/ 配下ドキュメント整理方針

本書は、本プロジェクトにおける  
**docs/ 配下のディレクトリ構成と運用ルール**を定義する。

現時点では docs/ 直下に文書を配置しているが、  
今後の設計書・仕様書・運用メモの増加を見据え、  
**役割別ディレクトリに段階的に整理する**。

---

## 1. 基本方針

### 1.1 段階的整理を前提とする

- 既存文書は **無理に即時移動しない**
- 新規文書から **適切なディレクトリに配置**
- 必要性が生じたタイミングでのみフォルダを追加する

👉 **最初から完成形を作らない**

---

### 1.2 「用途」で分け、「粒度」で分けない

- 設計・仕様・運用・メモを混在させない
- 技術領域（convert / validate 等）で細分化しすぎない
- **人が探すときの思考単位**を優先する

---

## 2. docs/ 配下の基本構成（現時点）

```text
docs/
├─ design/
│   ├─ Design_Master.md
│   ├─ Design_Issue_to_Doc_Promotion_Workflow_v0.1.md
│   └─ Design_*.md
│
├─ spec/              （将来）
├─ operation/         （将来）
├─ reference/         （将来）
└─ README.md          （必要に応じて）
```

※ 存在しないディレクトリは **必要になった時点で作成する**。

---

## 3. docs/design/ の位置づけ（今回の起点）

### 3.1 docs/design/ に置くもの

- 設計書（凍結された正本）
- Epic Issue から昇格した文書
- 設計プロセス・設計原則を定義する文書

例：

- `Design_Customized_Question_Set_v0.1.md`
- `Design_Issue_to_Doc_Promotion_Workflow_v0.1.md`
- `Design_Document_Directory_Policy_v0.1.md`

---

### 3.2 docs/design/ に置かないもの

- 実装手順の詳細メモ
- 実行ログ・検証ログ
- 一時的な検討メモ（Issue / PR コメントで十分なもの）

---

## 4. 将来ディレクトリの想定（拘束しない）

### 4.1 docs/spec/（仕様）

- 外部連携I/F仕様
- Execution Input Contract
- JSON / CSV / YAML の形式仕様

👉 **設計思想ではなく「守るべき契約」**

---

### 4.2 docs/operation/（運用）

- 実行手順
- 再生成手順
- CI / 手動検証フロー

👉 **人が手を動かすための文書**

---

### 4.3 docs/reference/（参照）

- 用語集
- 判断基準まとめ
- 過去バージョンの参考資料

👉 **読まなくても動くが、読むと理解が深まるもの**

---

## 5. Design_Master.md との関係

- `Design_Master.md` は **設計書群の入口（SSoT）**
- 新しい設計書を `docs/design/` に追加した場合：

  - **必ず Design_Master.md に参照を追加**
- ディレクトリ構成そのものは
  Design_Master.md ではなく **本書で定義**する

---

## 6. 既存 docs/ 直下ファイルの扱い

- 当面は **現状維持**
- 以下のタイミングで移動を検討する：

  - 内容が設計として凍結された
  - 参照頻度が高い
  - 同種文書が増えてきた

👉 **「増えてから整理」** を原則とする。

---

## 7. 運用ルールまとめ（短文）

- 新規設計書 → `docs/design/`
- 迷ったら直下ではなく **Issueで検討**
- フォルダは「必要になった瞬間」に作る
- ディレクトリ構成も設計対象として文書化する

---

## 8. 状態

本書は **proposal（提案）** とする。
実運用で問題がなければ **status: fixed** に昇格する。

---
