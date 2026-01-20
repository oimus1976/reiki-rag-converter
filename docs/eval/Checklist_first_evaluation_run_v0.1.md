---
title: 初回 Evaluation Run チェックリスト
version: v0.1
status: FIX
phase: evaluation
usage: first-run-only
related:
  - README_evaluation_procedure_v0.1.md
  - Observation_Summary_v0.1.md
  - Qommons_Evaluation_Framework_v0.1.md
---

# 初回 Evaluation Run チェックリスト（v0.1）

## 0. 本チェックリストの位置づけ

本チェックリストは、
**Evaluation 実行手順 v0.1 を初めて適用する際の事故防止用ガード**である。

* 評価品質を高めるためのものではない
* 手順逸脱・責務越境を防ぐことのみを目的とする
* 2回目以降の Evaluation Run では必須ではない（参考扱い）

---

## 1. 実行前チェック（開始条件）

Evaluation を開始する前に、以下をすべて満たしていることを確認する。

* [ ] `observation_summary.md` が存在する
* [ ] `observation_result.json` が存在する
* [ ] 両ファイルの `run_id` が一致している
* [ ] 成果物は zip 展開直後で、加工されていない
* [ ] `observation_result.json` を**まだ開いていない**

※ 1つでも未達の場合、Evaluation を開始してはならない。

---

## 2. 読み順遵守チェック

Evaluation 実行中、以下の順序を守っていることを確認する。

* [ ] 最初に `observation_summary.md` を読んだ
* [ ] Summary を読んだ後に diff_flags の分布を確認した
* [ ] diff_flags を「異常検知」として扱っていない
* [ ] Reference / Volume / Structural を分離して確認している

---

## 3. 差分解釈チェック（最重要）

Evaluation 中、次の禁止事項を侵していないことを確認する。

* [ ] 差分事実を要約・抽象化していない
* [ ] 差分に良否・品質評価を付与していない
* [ ] Observation の不足を Evaluation 側で補完していない
* [ ] Structural Diff v0.1 を詳細解釈していない
* [ ] run 間の直接比較を行っていない

> 原則：**写像は OK、再構成は NG**

---

## 4. judgment（判断）チェック

Gate 判定を行う際、以下を確認する。

* [ ] Gate 判定（OK / △ / NG）は Evaluation Framework に基づいている
* [ ] 判定理由は Observation の事実にのみ依拠している
* [ ] 判定結果は「合否」ではなく「要調査有無」として扱っている
* [ ] 判断留保点を明示的に言語化している

---

## 5. 成果物整理チェック

Evaluation 終了時、以下が整理されていることを確認する。

* [ ] Gate 判定結果が明示されている
* [ ] 主な論点・傾向が記録されている
* [ ] 次回 Evaluation で再確認すべき観点が整理されている
* [ ] Observation 成果物自体は改変していない

---

## 6. 初回専用 最終確認

初回 Evaluation Run に限り、以下を必ず確認する。

* [ ] Observation と Evaluation の責務境界を越えていない
* [ ] 「Observation を評価していない」
* [ ] 「差分の正しさ」を判断していない
* [ ] Framework を判断基準の唯一の拠り所としている

---

## 7. チェックリストの扱い

* 本チェックリストは **v0.1 固定**とする
* 手順に不備が見つかった場合は
  Evaluation 実行後に **v0.2 として改訂を検討**する
* 個別 Run の事情に合わせた改変は禁止する

---
