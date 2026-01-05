import subprocess
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SYN_DIR = ROOT / "synthetic_html"
GOLDEN_DIR = ROOT / "tests" / "golden_synthetic"

VALIDATE = ROOT / "src" / "validate_reiki_structure_v0.5.2.py"
CONVERT = ROOT / "src" / "convert_reiki_v2.7.py"

HTML_FILES = sorted([p for p in SYN_DIR.glob("*.html")])


# ---------------------------------------------------------
# 1) validate：synthetic_html ディレクトリを丸ごと検証
# ---------------------------------------------------------
def test_validate_synthetic_directory():
    """validate はディレクトリしか受け付けないため、synthetic_html を一括検証する。"""
    result = subprocess.run(
        ["python", str(VALIDATE), "--source", str(SYN_DIR)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"validate failed:\n{result.stderr}"


# ---------------------------------------------------------
# 2) convert → Golden 一致（ファイル個別）
# ---------------------------------------------------------
@pytest.mark.parametrize("html", HTML_FILES)
def test_convert_matches_golden(html):
    """convert が Golden TXT と一致することを確認"""

    golden = GOLDEN_DIR / html.name.replace(".html", ".txt")
    assert golden.exists(), f"Golden file missing:\n{golden}"

    # convert 実行
    result = subprocess.run(
        ["python", str(CONVERT), "--source", str(html), "--output", str(GOLDEN_DIR)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"convert failed:\n{result.stderr}"

    # convert の出力を読み込み
    out_path = GOLDEN_DIR / golden.name
    assert out_path.exists(), f"convert did not generate output:\n{out_path}"

    out_text = out_path.read_text(encoding="utf-8").strip()
    golden_text = golden.read_text(encoding="utf-8").strip()

    assert out_text == golden_text, (
        f"Golden diff detected in {html.name}\n\n"
        f"------ expected (Golden) ------\n{golden_text}\n\n"
        f"------ got (convert) ----------\n{out_text}\n"
    )


# ---------------------------------------------------------
# 3) P10：異常 DOM synthetic（validate が落ちないことのみ確認）
# ---------------------------------------------------------
def test_p10_validate():
    p10 = SYN_DIR / "synRG00000010_P10_error_cases.html"
    assert p10.exists()

    result = subprocess.run(
        ["python", str(VALIDATE), "--source", str(SYN_DIR)],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"P10 synthetic validate failed:\n{result.stderr}"
