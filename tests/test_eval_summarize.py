# tests/test_eval_summarize.py

import json
import subprocess
import sys
from pathlib import Path


def test_eval_summarize_generates_evaluation_record(tmp_path):
    """
    eval_summarize.py should generate Evaluation Record (AUTO sections only)
    from observation_result.json without interpreting diffs.
    """

    # --- arrange -------------------------------------------------
    observation_result = {
        "observations": [
            {
                "ordinance_id": "k518RG00000022",
                "question_id": "Q1",
                "diff_flags": {
                    "reference_diff": True,
                    "volume_diff": True,
                    "structural_diff": True,
                },
            },
            {
                "ordinance_id": "k518RG00000022",
                "question_id": "Q2",
                "diff_flags": {
                    "reference_diff": False,
                    "volume_diff": True,
                    "structural_diff": True,
                },
            },
        ]
    }

    obs_path = tmp_path / "observation_result.json"
    obs_path.write_text(json.dumps(observation_result), encoding="utf-8")

    output_md = tmp_path / "Evaluation_Record.md"

    # --- act -----------------------------------------------------
    cmd = [
        sys.executable,
        "-m",
        "scripts.eval_summarize",
        "--observation-result",
        str(obs_path),
        "--run-id",
        "eval_test_run_001",
        "--output",
        str(output_md),
    ]

    completed = subprocess.run(cmd, capture_output=True, text=True)

    # --- assert --------------------------------------------------
    assert completed.returncode == 0
    assert output_md.exists()

    content = output_md.read_text(encoding="utf-8")

    # AUTO sections existence
    assert "## 3. diff_flags 分布【AUTO】" in content
    assert "## 4. Diff 種別ごとの事実【AUTO】" in content

    # diff_flags summary (facts only)
    assert "reference_diff" in content
    assert "false 1" in content

    # Reference Diff facts
    assert "false 件数：1" in content
    assert "複数の条例に分布" in content or "条例" in content

    # HUMAN sections must remain unfilled
    assert "Gate 判定：（未記入）" in content
