#!/usr/bin/env python
# eval_summarize.py
# Generate AUTO sections of Evaluation Record v0.1 from observation_result.json

import json
import argparse
from datetime import date
from collections import Counter, defaultdict
from pathlib import Path

def render_auto_json(run_id, diff_counts, ref_false_count, ref_false_ordinances, total):
    return {
        "schema_version": "0.2",
        "run_id": run_id,
        "generated_at": date.today().isoformat(),
        "source": {
            "observation_version": "v0.1",
            "evaluation_procedure_version": "v0.1",
        },
        "summary": {
            "total_observations": total
        },
        "diff_flags_summary": {
            k: {
                "true": v.get(True, 0),
                "false": v.get(False, 0),
            }
            for k, v in diff_counts.items()
        },
        "reference_diff_facts": {
            "false_count": ref_false_count,
            "ordinance_count": ref_false_ordinances,
        },
        "notes": {
            "interpretation": "prohibited"
        },
    }

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--observation-result", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument(
        "--out-dir",
        required=True,
        help="Output directory for evaluation auto result and derived artifacts",
    )
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


def render_markdown_from_auto(auto):
    return f"""---
title: Evaluation Record
version: v0.1
status: DRAFT
phase: evaluation
run_id: {auto["run_id"]}
run_type: auto-generated
---

# Evaluation Record（v0.1｜AUTO）

## 1. Evaluation メタ情報【AUTO】

- run_id：{auto["run_id"]}
- 評価日時：{auto["generated_at"]}
- 評価者：human
- Observation version：{auto["source"]["observation_version"]}
- Evaluation Procedure：{auto["source"]["evaluation_procedure_version"]}

---

## 3. diff_flags 分布【AUTO】

```text
reference_diff  : true {auto["diff_flags_summary"]["reference_diff"]["true"]} / false {auto["diff_flags_summary"]["reference_diff"]["false"]}
volume_diff     : true {auto["diff_flags_summary"]["volume_diff"]["true"]}
structural_diff : true {auto["diff_flags_summary"]["structural_diff"]["true"]}

```

---

## 4. Diff 種別ごとの事実【AUTO】

### 4.1 Reference Diff（事実）

* false 件数：{auto["reference_diff_facts"]["false_count"]}
* 分布：複数の条例に分布している（{auto["reference_diff_facts"]["ordinance_count"]} 条例）

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

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- AUTO JSON (正本) ---
    auto_json = render_auto_json(
        run_id=args.run_id,
        diff_counts=diff_counts,
        ref_false_count=ref_false_count,
        ref_false_ordinances=ref_false_ordinances,
        total=len(observations),
    )

    auto_json_path = out_dir / "evaluation_auto.json"
    auto_json_path.write_text(
        json.dumps(auto_json, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # --- Derived Markdown ---
    md = render_markdown_from_auto(auto_json)

    md_path = out_dir / "Evaluation_Record.md"
    md_path.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()