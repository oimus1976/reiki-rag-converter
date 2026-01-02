---
title: Roadmap
version: v1.2
doc_type: roadmap
project: reiki-rag-converter
status: active
created: 2025-12-06
updated: 2026-01-02
author: Sumio Nishioka + ChatGPT
related_docs:
  - PROJECT_STATUS.md
  - Design_Customized_Question_Set_v0.1.md
tags:
  - roadmap
  - planning
  - execution-input-contract
---

# 例規HTML変換プロジェクト Roadmap v1.2

最終更新：2026-01-02  
適用対象：reiki-rag-converter（例規HTML変換エンジン）

---

# 0. 位置づけの更新（重要）

本プロジェクトは、  
単体の「例規HTML変換ツール」から、

> **生成AIテスト自動化と連携し、  
> RAG 応答挙動を再現可能に観測するための  
> 入力資産生成基盤**

へと役割を拡張した。

2026年Q1において、  
条例別カスタマイズ質問セット  
（customized_question_set.json）が  
**Execution Input Contract として凍結**されたことにより、

- 変換エンジン
- 合成HTML
- 質問入力資産

が **同一ロードマップ上で管理される対象**となった。

---

# 1. 現在位置（2026年1月）

※ 本ロードマップにおける v2.x / v3.0 は、
   すべて reiki-rag-converter（例規HTML変換エンジン本体）の
   バージョン番号を指す。

- convert_v2.6 → 安定版（DOM例外処理がほぼ飽和）
- validate_v0.5.3 → 安定。set混入問題など根本対処完了
- synthetic_html_v0.2 → P1〜P15 まで生成成功
- exception_check_v3.2 → 想定パターンをすべて通過
- CI（ci.yml / e2e.yml） → 完全安定（exit code 5 リスクなし）
- **条例別カスタマイズ質問セットの設計凍結（Epic 0 完了）**
- **Execution Input Contract（customized_question_set.json）確立**
- 全設計書の体系化が9割完了

プロジェクトは  
**reiki-rag-converter 本体 v2.7 安定化フェーズと、  
生成AI評価連携（入力資産供給）フェーズの境界点**  
に到達している。

---

# 2. 2026年 Q1〜Q2（短期：v2.7 目標）

## ゴール：v2.7  

**「実務レベルでの最終安定版」＋「評価観測入力の安定供給」**

### 必須タスク（変換エンジン軸）

- convert_v2.6 → v2.7 微調整  
  - 条→章→節→款の深い階層構造テスト  
  - 複雑表組み（P14/P15）最終調整  
- validate の仕様文書更新  
- synthetic_html の最終追加（P16〜P20）  
- v2.7 設計書（Design_convert_v2.7）を先行作成  
- 例外処理集（Exception Catalog）作成  

### 必須タスク（評価観測入力軸）

- customized_question_set 生成ロジックの実装
- 条例構造抽出（条・項・附則）の安定化
- Golden Question Pool A を起点とした
  条例別カスタマイズ質問セットの自動生成
- gov-llm-e2e-testkit への入力供給安定化

### 完了基準

- 全 synthetic_html が CI 通過  
- DOM 例外の取りこぼしゼロ  
- 大規模条例（附則20個以上）で安定変換  
- customized_question_set が
  Execution Input Contract として
  **継続的に生成・消費可能**

---

# 3. 2026年 Q3（中期：v2.8 目標）

## ゴール：v2.8  

**「機能強化版（観測精度向上ライン）」**

### 新規開発案

- 自動 DOM 差分検知ツール（HTML → Diff → 警告）
- 自動メタデータ修復（制定番号・附則名など）
- convert モジュール簡易 Linter（lint_reiki.py）
- Synthetic HTML Generator v0.3
- “条例100本テスト” の実施
- 質問セット × HTML 差分の相関観測

---

# 4. 2026年 Q4〜2027年 Q1（長期：v3.0 LTS 目標）

## ゴール：v3.0  

**「正式版・長期保守（LTS）＋評価基盤内蔵」**

### 必須項目

- パーサ全面再構築（v3.0）  
  - BeautifulSoup → lxml 等の高速化
- LGWAN 展開に向けたモジュール分離  
  - convert_core / io 層の完全分離
- 役場環境での Python 動作保証
- 将来の条例形式変化への差分吸収アーキテクチャ確立
- LTS 用 CHANGELOG / 長期保守ポリシー作成
- 評価観測入力（質問・HTML）の長期凍結運用確立

---

# 5. リスクと対策（更新）

- **HTML レイアウト変更**  
  → 自動 DOM 差分検知（v2.8）
- **生成AI挙動変化**  
  → 入力契約（Execution Input Contract）を凍結して観測
- **Python バージョン変更**  
  → v3.0 で convert_core 抽象化
- **LGWAN 環境制約**  
  → IO 層と Core 層の完全分離
- **属人化リスク**  
  → 設計書・契約・Issue 昇格スキームの標準化

---

# 6. まとめ

- Epic 0 により  
  **評価観測入力という新しい“正本成果物”が確立**
- v2.7 は  
  「変換エンジンの完成」＋「入力供給の安定」
- v2.8 以降は  
  観測精度・耐変化性の強化フェーズ
- v3.0 は  
  **変換 × 評価 × 運用を内包した LTS**

以上を、  
例規HTML変換プロジェクトの最新ロードマップとする。
