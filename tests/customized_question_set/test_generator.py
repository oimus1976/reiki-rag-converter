import json
from pathlib import Path

from customized_question_set.generator import generate_customized_question_set


def test_generate_records_skipped_q8_when_supplementary_missing(tmp_path: Path):
    html = """
    <html>
      <body>
        <div class="article" id="a1">
          <h2>第1条</h2>
        </div>
      </body>
    </html>
    """
    output_path = tmp_path / "customized_question_set.json"

    generate_customized_question_set(
        html=html,
        target_ordinance_id="dummy",
        source_golden_question_pool="GQPA:v1.1",
        question_set_id="customized_question_set:dummy:v1",
        schema_version="0.2",
        output_path=output_path,
    )

    data = json.loads(output_path.read_text(encoding="utf-8"))
    template_ids = {q["source_template_id"] for q in data["questions"]}

    assert "Q8" not in template_ids
    assert {
        "source_template_id": "Q8",
        "reason": "supplementary_not_extracted",
    } in data["extensions"]["skipped_questions"]
