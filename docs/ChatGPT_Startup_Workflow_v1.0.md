---
title: ChatGPT_Startup_Workflow
version: v1.0
doc_type: standard
project: reiki-rag-converter
created: 2025-12-06
updated: 2025-12-06
author: Sumio Nishioka + ChatGPT
tags:
  - ai-assisted-development
  - oss
  - startup-workflow
  - governance
  - reiki-rag-converter
---

# ChatGPT Startup Workflow v1.0
**reiki-rag-converter / 開始テンプレート運用プロセス**

---

## 1. Purpose（目的）
ChatGPT を毎回「正しい開発状態」で起動し、  
プロジェクト文脈の再構築・タスク整合性・設計整合性・CI安定性を保証する。

---

## 2. Startup System（構造）
起動時には次の 3 レイヤーをロードする：

1. ChatGPT_Startup_Template_v1.0  
2. PROJECT_STATUS.md（SSoT）  
3. 必要に応じて関連ドキュメント（GRAND_RULES / Design / CI / src）

---

## 3. Startup Sequence（起動手順）
### Step 1（ユーザー側）
```

/start
ChatGPT_Startup_Template_v1.0 を適用し、
PROJECT_STATUS.md を読み込んでください。

```

### Step 2（ChatGPT 側の義務）
- テンプレートのロード  
- PROJECT_STATUS.md の Next Action の確認  
- 状態整合性チェック  
- 次で応答：
```

準備完了。PROJECT_STATUS.md の Next Action を確認しました。

```

---

## 4. Resume Flow（スレッド分断時の復帰）
```

/start
ChatGPT_Startup_Template_v1.0 を再適用し、
PROJECT_STATUS.md を読み込んでください。

```

---

## 5. STATUS 更新時のルール
ChatGPT は：

- STATUS.md の整合性チェック  
- Next Action の空欄チェック  
- 必要に応じて修正案の提示  
- Completed/Pending の配置エラーの指摘  

を行う。

---

## 6. Autonomous Monitoring（自己監査）
ChatGPT は以下のタイミングで状態を自動監査する：

- /start 受信時  
- STATUS.md 変更時  
- 設計・CI の話題が出た時  
- PENTA 必要時  

監査対象：

- STATUS との不整合  
- 設計書との矛盾  
- CI/Golden を壊すリスク  
- 文書バージョン不一致  
- 依存構造の破綻

---

## 7. 禁止事項（運用）
- /start なしで勝手に開発モードへ入る  
- STATUS.md にないタスクの開始  
- ガバナンス文書の逸脱  
- 設計に反するコード生成  
- 安易な Golden 更新  

---

## 8. 効果
- 文脈再構築の安定化  
- タスク迷走ゼロ  
- CI と Golden diff が破壊されない  
- OSS プロジェクトとして継続運用が容易  

---

# Version History
- v1.0 (2025-12-06) 初版制定
