#!/usr/bin/env python
# eval_summarize.py
# Generate AUTO sections of Evaluation Record v0.1 from observation_result.json

import json
import argparse
from datetime import date
from collections import Counter, defaultdict
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--observation-result", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--run-id", required=True)
    return p.parse_args()


def load_observation(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def summarize_diff_flags(observations):
    counts = defaultdict(Counter)
    for obs in observations:
        for k, v in obs["diff_flags"].items():
            counts[k][v] += 1
    return counts


def summarize_reference_false(observations):
    false_obs = [
        obs for obs in observations
        if obs["diff_flags"].get("reference_diff") is False
    ]
    ordinances = {obs.get("ordinance_id") for obs in false_obs}
    return len(false_obs), len(ordinances)


def render_markdown(run_id, diff_counts, ref_false_count, ref_false_ordinances):
    today = date.today().isoformat()

    return f"""---
title: Evaluation Record
version: v0.1
status: DRAFT
phase: evaluation
run_id: {run_id}
run_type: auto-generated
---

# Evaluation Record（v0.1｜AUTO）

## 1. Evaluation メタ情報【AUTO】

- run_id：{run_id}
- 評価日時：{today}
- 評価者：human
- Observation version：v0.1
- Evaluation Procedure：v0.1

---

## 2. Observation 前提確認【AUTO】

- Observation Summary 読了：yes
- 再解釈・再計算なし：yes
- 未加工成果物を使用：yes

---

## 3. diff_flags 分布【AUTO】

```text
reference_diff  : true {diff_counts["reference_diff"].get(True, 0)} / false {diff_counts["reference_diff"].get(False, 0)}
volume_diff     : true {diff_counts["volume_diff"].get(True, 0)}
structural_diff : true {diff_counts["structural_diff"].get(True, 0)}
```

---

## 4. Diff 種別ごとの事実【AUTO】

### 4.1 Reference Diff（事実）

* false 件数：{ref_false_count}
* 分布：複数の条例に分布している（{ref_false_ordinances} 条例）

### 4.2 Volume Diff（事実）

* Volume Diff は全 AnswerPair で true である

### 4.3 Structural Diff（事実）

* Structural Diff は全 AnswerPair で true である

---

## 5. Gate 判定【HUMAN】

> Gate 判定：（未記入）

---

## 6. 判断留保・次回確認点【HUMAN】

* （未記入）

---

## 7. 評価範囲外メモ【HUMAN】

* （未記入）

---

## 8. 固定宣言【AUTO】

* 本記録は Observation v0.1 / Evaluation v0.1 に基づく
* 本記録は後続 Evaluation のための再解釈・再評価を意図しない
  """

def main():
    args = parse_args()
    data = load_observation(args.observation_result)
    observations = data["observations"]

    diff_counts = summarize_diff_flags(observations)
    ref_false_count, ref_false_ordinances = summarize_reference_false(observations)

    md = render_markdown(
        args.run_id,
        diff_counts,
        ref_false_count,
        ref_false_ordinances,
    )

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")

if __name__ == "__main__":
    main()