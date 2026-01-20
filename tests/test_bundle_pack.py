# tests/test_bundle_pack.py
import json
import subprocess
import sys
from pathlib import Path
import zipfile


def _create_minimal_bundle(bundle_dir: Path):
    """
    Evaluation Bundle v0.1 の最小成立セットを作る
    """
    (bundle_dir / "observation").mkdir(parents=True)
    (bundle_dir / "auto").mkdir()
    (bundle_dir / "human").mkdir()
    (bundle_dir / "judgment").mkdir()

    # dummy files
    (bundle_dir / "observation" / "observation_result.json").write_text("{}", encoding="utf-8")
    (bundle_dir / "observation" / "observation_summary.md").write_text("# summary", encoding="utf-8")
    (bundle_dir / "auto" / "evaluation_auto.json").write_text("{}", encoding="utf-8")
    (bundle_dir / "human" / "Evaluation_Record_HUMAN_test.md").write_text("# human", encoding="utf-8")
    (bundle_dir / "judgment" / "Evaluation_Judgment_test.md").write_text("# judgment", encoding="utf-8")

    manifest = {
        "schema_version": "0.1",
        "bundle_id": "bundle_test_001",
        "created_at": "2026-01-20",
        "observation": {
            "result": "observation/observation_result.json",
            "summary": "observation/observation_summary.md",
            "version": "v0.1"
        },
        "evaluation_auto": {
            "result": "auto/evaluation_auto.json",
            "schema_version": "0.2"
        },
        "evaluation_human": [
            {
                "record": "human/Evaluation_Record_HUMAN_test.md",
                "schema_version": "0.2"
            }
        ],
        "evaluation_judgment": {
            "record": "judgment/Evaluation_Judgment_test.md",
            "schema_version": "0.1"
        }
    }

    (bundle_dir / "bundle_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8"
    )


def test_bundle_pack_dry_run(tmp_path):
    bundle_dir = tmp_path / "bundle_test"
    _create_minimal_bundle(bundle_dir)

    cmd = [
        sys.executable,
        "-m",
        "scripts.bundle_pack",
        "--bundle-dir",
        str(bundle_dir),
        "--dry-run",
    ]

    completed = subprocess.run(cmd, capture_output=True, text=True)

    assert completed.returncode == 0
    assert "DRY-RUN" in completed.stdout


def test_bundle_pack_creates_zip(tmp_path):
    bundle_dir = tmp_path / "bundle_test"
    _create_minimal_bundle(bundle_dir)

    out_dir = tmp_path / "out"

    cmd = [
        sys.executable,
        "-m",
        "scripts.bundle_pack",
        "--bundle-dir",
        str(bundle_dir),
        "--out-dir",
        str(out_dir),
    ]

    completed = subprocess.run(cmd, capture_output=True, text=True)

    assert completed.returncode == 0

    zip_path = out_dir / "evaluation_bundle_bundle_test_001.zip"
    assert zip_path.exists()

    # ZIP の中身確認（最低限）
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        assert "evaluation_bundle_bundle_test_001/bundle_manifest.json" in names
        assert "evaluation_bundle_bundle_test_001/auto/evaluation_auto.json" in names
