# tests/e2e/test_generate_customized_question_set_snapshot.py
import json
from pathlib import Path

from reiki_rag_customized_question_set.generator import generate_customized_question_set


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def normalize(payload: dict) -> dict:
    payload = dict(payload)
    payload.pop("generated_at", None)
    return payload


def test_generate_customized_question_set_snapshot(tmp_path: Path):
    html = Path(
        "tests/fixtures/synthetic_html/synRG00000015_P15_supplements.html"
    ).read_text(encoding="utf-8")
    output_dir = tmp_path / "out"

    generate_customized_question_set(
        html=html,
        target_ordinance_id="synRG00000015",
        source_golden_question_pool="GQPA:v1.1",
        question_set_id="customized_question_set:synRG00000015:v1",
        schema_version="0.2",
        output_path=output_dir / "customized_question_set.json",
    )

    actual = load_json(output_dir / "customized_question_set.json")
    expected = load_json(
        Path(
            "tests/fixtures/customized_question_set/"
            "synRG00000015_P15_supplements.expected.json"
        )
    )

    assert normalize(actual) == normalize(expected)
