---
title: Roadmap
version: v1.3
doc_type: roadmap
project: reiki-rag-converter
status: active
created: 2025-12-06
updated: 2026-01-04
author: Sumio Nishioka + ChatGPT
related_docs:
  - PROJECT_STATUS.md
  - Design_Master.md
  - Design_Execution_Input_Contract_v0.2.md
tags:
  - roadmap
  - planning
  - reiki-html-converter
  - execution-input-contract
---

# 例規HTML変換プロジェクト Roadmap v1.3

最終更新：2026-01-04  
適用対象：reiki-rag-converter（例規HTML変換エンジン）

---

# 0. 位置づけの更新（重要）

本プロジェクトは、  
**条例HTMLを入力として、RAG・評価・運用に耐える構造化テキストを
決定的・再現可能に生成する例規HTML変換エンジン**
（reiki-rag-converter）を主成果物とする。

その上で本プロジェクトは、  
当該変換エンジンの出力を前提として、

> **生成AIテスト自動化と連携し、  
> RAG 応答挙動を再現可能に観測するための  
> 入力資産（質問セット）を安定供給する**

という **二次的責務**を担う。

2026年Q1において、  
条例別カスタマイズ質問セット  
（customized_question_set.json）が  
**Execution Input Contract v0.2 として設計凍結**されたことにより、

- 変換エンジン（一次成果物）
- 構造化HTML / TXT（一次成果物）
- 評価観測入力（質問セット：二次成果物）

が、**同一ロードマップ上で明確に役割分離された状態で管理される**
フェーズに移行した。

---

# 1. 現在位置（2026年1月）

※ 本ロードマップにおける v2.x / v3.0 は、  
   すべて **reiki-rag-converter（例規HTML変換エンジン本体）**
   のバージョン番号を指す。

- convert_v2.6 → 安定版（DOM例外処理がほぼ飽和）
- validate_v0.5.3 → 安定（set混入・自己参照問題を根本対処）
- synthetic_html_v0.2 → P1〜P15 生成成功
- exception_check_v3.2 → 想定例外パターン全通過
- CI（ci.yml / e2e.yml） → 完全安定（exit code 5 リスク解消）
- **Execution Input Contract v0.2 設計凍結（Epic 7 完了）**
- 条例別カスタマイズ質問セット生成基盤 実装済み
- 設計書体系（Design_*）は概ね出揃い、最終整理フェーズ

プロジェクトは現在、  

> **「例規HTML変換エンジン v2.7 を
> 実務レベルで完成させる最終安定化フェーズ」**

に位置している。

---

# 2. 2026年 Q1〜Q2（短期：v2.7 目標）

## ゴール：v2.7  

**例規HTML変換エンジンとしての完成（実務最終安定版）**

### ゴール定義（1文）

条例HTMLを入力として、  
**条・項・号・附則・表を含む構造を
決定的・再現可能に解釈し、  
RAG・検索・評価用途に耐える構造化テキストを
安定生成できる例規HTML変換エンジンを完成させる。**

---

### 必須タスク（変換エンジン軸：一次成果物）

- convert_v2.6 → v2.7 微調整  
  - 章・節・款を跨ぐ深階層構造の最終確認  
  - 複雑表組み（P14 / P15）の確定処理  
- validate 仕様の最終明文化
- synthetic_html P16〜P20 追加
- v2.7 設計書（Design_convert_v2.7）確定
- Exception Catalog（例外体系表）作成

---

### 付随タスク（評価観測入力軸：二次成果物）

※ 以下は **変換エンジン完成を前提とした副次目標**である。

- customized_question_set 生成ロジックの安定化
- 条例構造抽出（条・項・附則）の確定
- Golden Question Pool A を起点とした
  条例別カスタマイズ質問セットの自動生成
- gov-llm-e2e-testkit への入力供給安定化

---

### 完了基準

- 全 synthetic_html が CI を通過
- DOM 例外の取りこぼしゼロ
- 大規模条例（附則20以上）で安定変換
- 変換結果の決定性（diff 安定）確認
- customized_question_set が
  **Execution Input Contract v0.2 として
  継続生成・消費可能**

---

# 3. 2026年 Q3（中期：v2.8 目標）

## ゴール：v2.8  

**変換耐性・観測精度を高める機能強化版**

### 主眼

- HTML レイアウト変化への耐性向上
- 変換結果と評価観測の結びつき強化

### 新規開発案

- 自動 DOM 差分検知（HTML → Diff → Warning）
- メタデータ自動修復（制定番号・附則名など）
- convert モジュール簡易 Linter（lint_reiki.py）
- Synthetic HTML Generator v0.3
- 「条例100本テスト」の実施
- HTML差分 × 質問セットの相関観測

---

# 4. 2026年 Q4〜2027年 Q1（長期：v3.0 LTS 目標）

## ゴール：v3.0  

**正式版・長期保守（LTS）対応コンバーター**

### ゴール定義

- 長期運用・環境差・条例形式変化に耐える
  **例規HTML変換エンジンの完成形**

### 必須項目

- パーサ基盤の再設計（v3.0）
  - BeautifulSoup 依存の見直し（lxml 等）
- LGWAN 展開を前提としたモジュール分離
  - convert_core / io 層の完全分離
- 役場環境での Python 実行保証
- 条例形式変化を吸収する差分耐性アーキテクチャ
- LTS 用 CHANGELOG / 保守ポリシー策定
- 評価観測入力（質問・HTML）の長期凍結運用確立

---

# 5. リスクと対策（更新）

- **HTML レイアウト変更**
  → DOM 差分検知（v2.8）
- **生成AI挙動変化**
  → Execution Input Contract を凍結して観測
- **Python バージョン変更**
  → v3.0 で convert_core 抽象化
- **LGWAN 環境制約**
  → IO 層と Core 層の完全分離
- **属人化リスク**
  → 設計書・契約・Issue 駆動の標準化

---

# 6. まとめ

- 本プロジェクトの一次成果物は
  **例規HTML変換エンジン（reiki-rag-converter）である**
- Execution Input Contract / 質問セットは
  **変換エンジンを前提とした二次成果物**
- v2.7 は「変換エンジン完成」
- v2.8 は「耐変化・観測精度向上」
- v3.0 は「LTS・運用耐性の確立」

以上を、  
例規HTML変換プロジェクトの最新ロードマップ v1.3 とする。
