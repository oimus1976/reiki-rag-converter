import json
import subprocess
import sys
from pathlib import Path


def test_eval_summarize_v0_2_generates_auto_json(tmp_path):
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

    out_dir = tmp_path / "evaluation_out"

    # --- act -----------------------------------------------------
    cmd = [
        sys.executable,
        "-m",
        "scripts.eval_summarize",
        "--observation-result",
        str(obs_path),
        "--run-id",
        "eval_test_run_002",
        "--out-dir",
        str(out_dir),
    ]

    completed = subprocess.run(cmd, capture_output=True, text=True)

    # --- assert --------------------------------------------------
    assert completed.returncode == 0
    assert out_dir.exists()

    auto_json = out_dir / "evaluation_auto.json"
    assert auto_json.exists()

    data = json.loads(auto_json.read_text(encoding="utf-8"))

    # diff_flags 分布（事実のみ）
    assert data["diff_flags_summary"]["reference_diff"]["false"] == 1
    assert data["diff_flags_summary"]["reference_diff"]["true"] == 1

    # Reference Diff facts（解釈なし）
    ref = data["reference_diff_facts"]
    assert ref["false_count"] == 1
    assert ref["ordinance_count"] == 1
