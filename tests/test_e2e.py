import os
import subprocess
from pathlib import Path
import pytest

# ================================================================
#  CI 対策：実条例HTMLは公開できないため、CI では E2E をスキップする
# ================================================================
if os.getenv("SKIP_E2E") == "true":
    pytest.skip(
        "Skipping E2E tests on CI because real HTML data is not available.",
        allow_module_level=True
    )

# ================================================================
#  ローカル実行時：実HTMLで E2E を実施する
# ================================================================
ROOT = Path(__file__).resolve().parent.parent
REIKI_DIR = ROOT / "reiki_honbun"

HTML_FILES = [
    "k518RG00000012.html",
    "k518RG00000055.html",
    "k518RG00000080.html",
]

@pytest.mark.parametrize("filename", HTML_FILES)
def test_e2e(filename):
    """実HTMLを validate → convert できることを確認する E2E テスト"""
    html_path = REIKI_DIR / filename
    assert html_path.exists(), f"HTML file not found: {html_path}"

    # validate
    result_val = subprocess.run(
        ["python", "src/validate_reiki_structure_v0.5.2.py", str(html_path)],
        capture_output=True, text=True
    )
    assert result_val.returncode == 0, f"validate failed: {result_val.stderr}"

    # convert
    result_conv = subprocess.run(
        ["python", "src/convert_reiki_v2.7.py", str(html_path)],
        capture_output=True, text=True
    )
    assert result_conv.returncode == 0, f"convert failed: {result_conv.stderr}"

