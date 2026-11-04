"""Tests for scripts/observation_log_q2.py.

拘束対象:
  docs/eval/log_schema/Phase_3_5_Observation_Log_Schema_Q2_v0.1.md

本テストのログはすべてテスト内で組み立てる合成データであり、
Phase 3.5 の実行データではない。
"""

import copy
import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "observation_log_q2.py"

_spec = importlib.util.spec_from_file_location("observation_log_q2", SCRIPT)
olq2 = importlib.util.module_from_spec(_spec)
sys.modules["observation_log_q2"] = olq2
_spec.loader.exec_module(olq2)

RUN_ID = "p35_20260125_k518RG00000200_S1_01"
EXPECTED_ROWS = [
    "工事又は製造の請負",
    "財産の買入れ",
    "物件の借入れ",
    "財産の売払い",
    "前各号以外",
]
JUDGMENT_WORDS = ["正しい", "誤り", "適切", "不適切", "合格", "不合格"]


def make_obs(mode="A_md", run_id=RUN_ID):
    return {
        "schema_version": "observation.q2.v0.1",
        "phase": "3.5",
        "run_id": run_id,
        "scenario": "S1",
        "question_id": "Q-S1-02",
        "ordinance_id": "k518RG00000200",
        "mode": mode,
        "answer_text": "DUMMY ANSWER LINE 1\nDUMMY | ANSWER LINE 2",
        "table_expectation": {"expected_rows": list(EXPECTED_ROWS)},
        "table_observation": [
            {
                "category": cat,
                "amount_present": i % 2 == 0,
                "amount_value": None,
                "source": "csv" if mode == "B_md_csv" else "markdown",
                "notes": f"dummy note {i}",
            }
            for i, cat in enumerate(EXPECTED_ROWS)
        ],
        "reference_behavior": {
            "mentions_table": True,
            "mentions_article": ["第84条第3項"],
            "csv_used": mode == "B_md_csv",
            "extraction_status": "partial",
        },
        "observations": {
            "missing_category": False,
            "mixed_category": True,
            "representative_value_bias": False,
        },
        "meta": {"observer": "human", "notes": "dummy meta note"},
    }


def write_obs(directory: Path, obs: dict, name: str | None = None) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (name or f"observation_{obs['run_id']}_{obs['mode']}.json")
    path.write_text(json.dumps(obs, ensure_ascii=False), encoding="utf-8")
    return path


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Valid baseline
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mode", ["A_md", "B_md_csv"])
def test_valid_log_has_no_violation(mode):
    assert olq2.validate_observation(make_obs(mode)) == []


def test_meta_is_optional_and_optional_fields_may_be_omitted():
    obs = make_obs()
    del obs["meta"]
    del obs["reference_behavior"]["mentions_article"]
    for item in obs["table_observation"]:
        del item["amount_value"]
        del item["notes"]
    assert olq2.validate_observation(obs) == []


def test_amount_value_accepts_string_or_null():
    obs = make_obs()
    obs["table_observation"][0]["amount_value"] = "DUMMY AMOUNT"
    obs["table_observation"][1]["amount_value"] = None
    assert olq2.validate_observation(obs) == []


def test_cli_validate_ok(tmp_path):
    a = write_obs(tmp_path, make_obs("A_md"))
    b = write_obs(tmp_path, make_obs("B_md_csv"))
    r = run_cli("validate", a, b)
    assert r.returncode == 0, r.stderr


# ---------------------------------------------------------------------------
# Schema violations
# ---------------------------------------------------------------------------

REQUIRED_ROOT = [
    "schema_version", "phase", "run_id", "scenario", "question_id",
    "ordinance_id", "mode", "answer_text", "table_expectation",
    "table_observation", "reference_behavior", "observations",
]


@pytest.mark.parametrize("key", REQUIRED_ROOT)
def test_missing_required_root_field(key):
    obs = make_obs()
    del obs[key]
    errors = olq2.validate_observation(obs)
    assert any(e.startswith(f"$.{key}: required") for e in errors), errors


@pytest.mark.parametrize(
    "path,key",
    [
        ("table_expectation", "expected_rows"),
        ("reference_behavior", "mentions_table"),
        ("reference_behavior", "csv_used"),
        ("reference_behavior", "extraction_status"),
        ("observations", "missing_category"),
        ("observations", "mixed_category"),
        ("observations", "representative_value_bias"),
    ],
)
def test_missing_required_nested_field(path, key):
    obs = make_obs()
    del obs[path][key]
    errors = olq2.validate_observation(obs)
    assert any(e.startswith(f"$.{path}.{key}: required") for e in errors), errors


@pytest.mark.parametrize("key", ["category", "amount_present", "source"])
def test_missing_required_table_observation_field(key):
    obs = make_obs()
    del obs["table_observation"][0][key]
    errors = olq2.validate_observation(obs)
    assert any(e.startswith(f"$.table_observation[0].{key}: required") for e in errors), errors


@pytest.mark.parametrize(
    "mutate,prefix",
    [
        (lambda o: o.__setitem__("answer_text", 1), "$.answer_text: expected string"),
        (lambda o: o.__setitem__("table_observation", {}), "$.table_observation: expected array"),
        (lambda o: o.__setitem__("meta", "x"), "$.meta: expected object"),
        (lambda o: o["observations"].__setitem__("missing_category", 0),
         "$.observations.missing_category: expected boolean"),
        (lambda o: o["observations"].__setitem__("mixed_category", "true"),
         "$.observations.mixed_category: expected boolean"),
        (lambda o: o["table_observation"][0].__setitem__("amount_present", 1),
         "$.table_observation[0].amount_present: expected boolean"),
        (lambda o: o["table_observation"][0].__setitem__("amount_value", 100),
         "$.table_observation[0].amount_value: expected string|null"),
        (lambda o: o["reference_behavior"].__setitem__("mentions_article", "第84条"),
         "$.reference_behavior.mentions_article: expected array[string]"),
        (lambda o: o["table_expectation"].__setitem__("expected_rows", [1, 2]),
         "$.table_expectation.expected_rows: expected array[string]"),
    ],
)
def test_type_violations(mutate, prefix):
    obs = make_obs()
    mutate(obs)
    errors = olq2.validate_observation(obs)
    assert any(e.startswith(prefix) for e in errors), errors


@pytest.mark.parametrize(
    "key,value",
    [("phase", "3"), ("scenario", "S2"), ("question_id", "Q-S1-01")],
)
def test_fixed_value_violations(key, value):
    obs = make_obs()
    obs[key] = value
    errors = olq2.validate_observation(obs)
    assert any(e.startswith(f"$.{key}: must be") for e in errors), errors


def test_unknown_mode_rejected():
    obs = make_obs()
    obs["mode"] = "A"
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.mode: must be one of") for e in errors), errors


@pytest.mark.parametrize(
    "path",
    [None, "table_expectation", "reference_behavior", "observations", "meta"],
)
def test_undefined_field_rejected(path):
    obs = make_obs()
    target = obs if path is None else obs[path]
    target["verdict"] = "x"
    errors = olq2.validate_observation(obs)
    expected = "$.verdict" if path is None else f"$.{path}.verdict"
    assert any(e.startswith(expected) and "not defined" in e for e in errors), errors


def test_undefined_field_in_table_observation_rejected():
    obs = make_obs()
    obs["table_observation"][0]["score"] = 1
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.table_observation[0].score") for e in errors), errors


def test_root_must_be_object():
    assert olq2.validate_observation([]) == ["$: root must be an object"]


def test_expected_rows_must_equal_q2_fixed_rows():
    obs = make_obs()
    obs["table_expectation"]["expected_rows"] = EXPECTED_ROWS[:-1]
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.table_expectation.expected_rows: must equal") for e in errors)


def test_expected_rows_variant_spelling_is_not_normalized():
    obs = make_obs()
    rows = list(EXPECTED_ROWS)
    rows[1] = "財産の買入"  # 表記揺れ: 正規化せず不一致として扱う
    obs["table_expectation"]["expected_rows"] = rows
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.table_expectation.expected_rows") for e in errors)


def test_category_must_be_element_of_expected_rows():
    obs = make_obs()
    obs["table_observation"][0]["category"] = "工事又は製造の請負い"
    errors = olq2.validate_observation(obs)
    assert any("is not an element of expected_rows" in e for e in errors), errors


def test_duplicated_category_rejected():
    obs = make_obs()
    obs["table_observation"][1]["category"] = obs["table_observation"][0]["category"]
    errors = olq2.validate_observation(obs)
    assert any("duplicated category" in e for e in errors), errors
    assert any("missing categories" in e for e in errors), errors


def test_one_element_per_category_required():
    obs = make_obs()
    obs["table_observation"].pop()
    errors = olq2.validate_observation(obs)
    assert any("missing categories ['前各号以外']" in e for e in errors), errors


def test_invalid_source_rejected():
    obs = make_obs()
    obs["table_observation"][0]["source"] = "html"
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.table_observation[0].source: must be one of") for e in errors)


def test_invalid_extraction_status_rejected():
    obs = make_obs()
    obs["reference_behavior"]["extraction_status"] = "done"
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.reference_behavior.extraction_status") for e in errors)


@pytest.mark.parametrize("word", JUDGMENT_WORDS)
def test_judgment_word_in_notes_rejected(word):
    obs = make_obs()
    obs["table_observation"][2]["notes"] = f"dummy {word} dummy"
    errors = olq2.validate_observation(obs)
    assert any(
        e.startswith("$.table_observation[2].notes: contains prohibited judgment word")
        for e in errors
    ), errors


@pytest.mark.parametrize("word", JUDGMENT_WORDS)
def test_judgment_word_in_meta_notes_rejected(word):
    obs = make_obs()
    obs["meta"]["notes"] = word
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.meta.notes: contains prohibited") for e in errors), errors


def test_answer_text_is_raw_and_not_scanned_for_judgment_words():
    obs = make_obs()
    obs["answer_text"] = "回答原文に「正しい」が含まれる場合"
    assert olq2.validate_observation(obs) == []


def test_cli_validate_reports_violation_with_nonzero_exit(tmp_path):
    obs = make_obs()
    obs["phase"] = "3"
    p = write_obs(tmp_path, obs)
    r = run_cli("validate", p)
    assert r.returncode == 1
    assert "$.phase: must be '3.5'" in r.stderr


def test_cli_validate_invalid_json(tmp_path):
    p = tmp_path / f"observation_{RUN_ID}_A_md.json"
    p.write_text("{not json", encoding="utf-8")
    r = run_cli("validate", p)
    assert r.returncode == 1
    assert "invalid JSON" in r.stderr


# ---------------------------------------------------------------------------
# Naming conventions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "run_id",
    [
        "p35_20260125_k518RG00000200_S1_01",
        "p35_20261231_k518RG00000200_S1_1",
        "p35_20260125_k518RG00000200_S1_123",
    ],
)
def test_run_id_valid(run_id):
    assert olq2.parse_run_id(run_id) is not None


@pytest.mark.parametrize(
    "run_id",
    [
        "p3_20260125_k518RG00000200_S1_01",      # prefix
        "p35_2026012_k518RG00000200_S1_01",      # date digits
        "p35_20261301_k518RG00000200_S1_01",     # invalid month
        "p35_20260125_k518RG00000200_S2_01",     # scenario
        "p35_20260125_k518RG00000200_S1_",       # seq missing
        "p35_20260125_k518RG00000200_S1_a1",     # seq non-digit
        "p35_20260125__S1_01",                   # ordinance_id empty
        "P35_20260125_k518RG00000200_S1_01",     # case
    ],
)
def test_run_id_invalid(run_id):
    assert olq2.parse_run_id(run_id) is None
    obs = make_obs(run_id=run_id)
    errors = olq2.validate_observation(obs)
    assert any(e.startswith("$.run_id: must follow") for e in errors), errors


def test_run_id_components():
    parts = olq2.parse_run_id(RUN_ID)
    assert parts == {
        "date": "20260125",
        "ordinance_id": "k518RG00000200",
        "scenario": "S1",
        "seq": "01",
    }


def test_run_id_ordinance_id_must_match_field():
    obs = make_obs()
    obs["ordinance_id"] = "k518RG00000999"
    errors = olq2.validate_observation(obs)
    assert any("does not match $.ordinance_id" in e for e in errors), errors


def test_filenames():
    assert olq2.observation_filename(RUN_ID, "A_md", "json") == f"observation_{RUN_ID}_A_md.json"
    assert olq2.observation_filename(RUN_ID, "B_md_csv", "md") == f"observation_{RUN_ID}_B_md_csv.md"
    assert olq2.summary_filename(RUN_ID) == f"observation_summary_{RUN_ID}.csv"
    with pytest.raises(ValueError):
        olq2.observation_filename(RUN_ID, "A", "json")
    with pytest.raises(ValueError):
        olq2.observation_filename(RUN_ID, "A_md", "csv")


@pytest.mark.parametrize(
    "name",
    [
        "obs.json",
        f"observation_{RUN_ID}.json",
        f"observation_{RUN_ID}_A.json",
        f"observation_{RUN_ID}_A_md.md",
        f"observation_{RUN_ID}_A_md.JSON",
    ],
)
def test_json_filename_must_follow_convention(tmp_path, name):
    p = write_obs(tmp_path, make_obs("A_md"), name=name)
    r = run_cli("validate", p)
    assert r.returncode == 1
    assert "file name must follow" in r.stderr


def test_filename_mode_must_match_content(tmp_path):
    p = write_obs(tmp_path, make_obs("A_md"), name=f"observation_{RUN_ID}_B_md_csv.json")
    r = run_cli("validate", p)
    assert r.returncode == 1
    assert "mode in file name 'B_md_csv' does not match $.mode 'A_md'" in r.stderr


def test_filename_run_id_must_match_content(tmp_path):
    other = "p35_20260125_k518RG00000200_S1_02"
    p = write_obs(tmp_path, make_obs("A_md"), name=f"observation_{other}_A_md.json")
    r = run_cli("validate", p)
    assert r.returncode == 1
    assert "run_id in file name" in r.stderr


# ---------------------------------------------------------------------------
# A_md / B_md_csv handling
# ---------------------------------------------------------------------------


def test_csv_used_must_be_false_for_a_md():
    obs = make_obs("A_md")
    obs["reference_behavior"]["csv_used"] = True
    errors = olq2.validate_observation(obs)
    assert "$.reference_behavior.csv_used: must be false for mode 'A_md'" in errors


def test_csv_used_must_be_true_for_b_md_csv():
    obs = make_obs("B_md_csv")
    obs["reference_behavior"]["csv_used"] = False
    errors = olq2.validate_observation(obs)
    assert "$.reference_behavior.csv_used: must be true for mode 'B_md_csv'" in errors


def test_summary_rejects_duplicated_mode():
    a1 = make_obs("A_md")
    a2 = copy.deepcopy(a1)
    with pytest.raises(olq2.ObservationLogError, match="duplicated mode"):
        olq2.build_summary_rows([a1, a2])


def test_summary_rejects_mixed_run_ids():
    a = make_obs("A_md")
    b = make_obs("B_md_csv", run_id="p35_20260125_k518RG00000200_S1_02")
    with pytest.raises(olq2.ObservationLogError, match="share one run_id"):
        olq2.build_summary_rows([a, b])


# ---------------------------------------------------------------------------
# CSV summary generation
# ---------------------------------------------------------------------------


def test_cli_summarize_generates_csv(tmp_path):
    a_obs = make_obs("A_md")
    b_obs = make_obs("B_md_csv")
    b_obs["observations"]["missing_category"] = True
    # B を先に渡しても出力は A_md → B_md_csv の順
    b = write_obs(tmp_path / "in", b_obs)
    a = write_obs(tmp_path / "in", a_obs)
    out_dir = tmp_path / "out"

    r = run_cli("summarize", b, a, "--out-dir", out_dir)
    assert r.returncode == 0, r.stderr

    out = out_dir / f"observation_summary_{RUN_ID}.csv"
    assert out.exists()
    assert sorted(p.name for p in out_dir.iterdir()) == [out.name]

    text = out.read_text(encoding="utf-8")
    header = text.splitlines()[0]
    assert header == (
        "run_id,mode,category,amount_present,source,"
        "missing_category,mixed_category,representative_value_bias"
    )

    rows = list(csv.DictReader(text.splitlines()))
    assert len(rows) == 10
    assert [r["mode"] for r in rows] == ["A_md"] * 5 + ["B_md_csv"] * 5
    assert [r["category"] for r in rows[:5]] == EXPECTED_ROWS
    assert [r["category"] for r in rows[5:]] == EXPECTED_ROWS
    assert {r["run_id"] for r in rows} == {RUN_ID}

    for row, item in zip(rows[:5], a_obs["table_observation"]):
        assert row["amount_present"] == ("true" if item["amount_present"] else "false")
        assert row["source"] == "markdown"
        assert row["missing_category"] == "false"
        assert row["mixed_category"] == "true"
        assert row["representative_value_bias"] == "false"
    for row in rows[5:]:
        assert row["source"] == "csv"
        assert row["missing_category"] == "true"


def test_cli_summarize_single_mode(tmp_path):
    a = write_obs(tmp_path, make_obs("A_md"))
    r = run_cli("summarize", a, "--out-dir", tmp_path / "out")
    assert r.returncode == 0, r.stderr
    rows = list(csv.DictReader(
        (tmp_path / "out" / f"observation_summary_{RUN_ID}.csv")
        .read_text(encoding="utf-8").splitlines()
    ))
    assert {r["mode"] for r in rows} == {"A_md"}


def test_cli_summarize_refuses_invalid_input_and_writes_nothing(tmp_path):
    a = write_obs(tmp_path / "in", make_obs("A_md"))
    bad = make_obs("B_md_csv")
    bad["reference_behavior"]["csv_used"] = False
    b = write_obs(tmp_path / "in", bad)
    out_dir = tmp_path / "out"
    r = run_cli("summarize", a, b, "--out-dir", out_dir)
    assert r.returncode == 1
    assert "csv_used" in r.stderr
    assert not out_dir.exists()


def test_cli_summarize_duplicated_mode_across_files(tmp_path):
    a = write_obs(tmp_path / "x", make_obs("A_md"))
    a2 = write_obs(tmp_path / "y", make_obs("A_md"))
    r = run_cli("summarize", a, a2, "--out-dir", tmp_path / "out")
    assert r.returncode == 1
    assert "duplicated mode" in r.stderr


# ---------------------------------------------------------------------------
# Markdown review generation
# ---------------------------------------------------------------------------

QUESTION_TEXT = "DUMMY QUESTION TEXT FOR TEST"


def _render(tmp_path, mode):
    obs = make_obs(mode)
    j = write_obs(tmp_path / "in", obs)
    q = tmp_path / "q.txt"
    q.write_text(QUESTION_TEXT + "\n", encoding="utf-8")
    out_dir = tmp_path / "out"
    r = run_cli("render-md", j, "--question-file", q, "--out-dir", out_dir)
    assert r.returncode == 0, r.stderr
    md = out_dir / f"observation_{RUN_ID}_{mode}.md"
    assert md.exists()
    return obs, md.read_text(encoding="utf-8")


@pytest.mark.parametrize("mode", ["A_md", "B_md_csv"])
def test_render_md_structure(tmp_path, mode):
    obs, text = _render(tmp_path, mode)
    lines = text.splitlines()

    # YAML frontmatter (run_id, question_id, mode)
    assert lines[0] == "---"
    end = lines.index("---", 1)
    fm = lines[1:end]
    assert fm == [f"run_id: {RUN_ID}", "question_id: Q-S1-02", f"mode: {mode}"]

    # 必須見出しの順序
    headings = [l for l in lines if l.startswith("## ")]
    assert headings == [
        "## 質問本文（Q2）",
        "## 回答原文",
        "## 区分別テーブル",
        "## 観測サマリ",
    ]

    # 質問本文
    assert QUESTION_TEXT in text

    # 回答原文（引用・原文保持）
    assert "> DUMMY ANSWER LINE 1" in lines
    assert "> DUMMY | ANSWER LINE 2" in lines

    # 区分別テーブル
    assert "| 区分 | 金額提示 | 情報源 | メモ |" in lines
    src = "csv" if mode == "B_md_csv" else "markdown"
    for i, cat in enumerate(EXPECTED_ROWS):
        present = "true" if i % 2 == 0 else "false"
        assert f"| {cat} | {present} | {src} | dummy note {i} |" in lines

    # 観測サマリ
    assert "- 欠落（missing_category）: false" in lines
    assert "- 混在（mixed_category）: true" in lines
    assert "- 代表値引きずり（representative_value_bias）: false" in lines
    assert "- 表参照（mentions_table）: true" in lines


def test_render_md_has_no_judgment_words_outside_raw_text(tmp_path):
    _, text = _render(tmp_path, "B_md_csv")
    for word in JUDGMENT_WORDS:
        assert word not in text


def test_render_md_escapes_table_cells():
    obs = make_obs()
    obs["table_observation"][0]["notes"] = "a|b\nc"
    text = olq2.render_markdown(obs, QUESTION_TEXT)
    assert f"| {EXPECTED_ROWS[0]} | true | markdown | a\\|b<br>c |" in text.splitlines()


def test_render_md_missing_notes_is_empty_cell():
    obs = make_obs()
    del obs["table_observation"][0]["notes"]
    text = olq2.render_markdown(obs, QUESTION_TEXT)
    assert f"| {EXPECTED_ROWS[0]} | true | markdown |  |" in text.splitlines()


def test_cli_render_md_refuses_invalid_input(tmp_path):
    obs = make_obs()
    obs["mode"] = "B"
    j = write_obs(tmp_path, obs, name=f"observation_{RUN_ID}_A_md.json")
    q = tmp_path / "q.txt"
    q.write_text(QUESTION_TEXT, encoding="utf-8")
    out_dir = tmp_path / "out"
    r = run_cli("render-md", j, "--question-file", q, "--out-dir", out_dir)
    assert r.returncode == 1
    assert not out_dir.exists()


def test_cli_render_md_requires_question_file(tmp_path):
    j = write_obs(tmp_path, make_obs())
    r = run_cli("render-md", j, "--out-dir", tmp_path / "out")
    assert r.returncode == 2


def test_cli_render_md_rejects_empty_question(tmp_path):
    j = write_obs(tmp_path, make_obs())
    q = tmp_path / "q.txt"
    q.write_text("  \n", encoding="utf-8")
    r = run_cli("render-md", j, "--question-file", q, "--out-dir", tmp_path / "out")
    assert r.returncode == 1
    assert "question text is empty" in r.stderr


def test_input_json_is_not_modified(tmp_path):
    obs = make_obs("A_md")
    j = write_obs(tmp_path / "in", obs)
    before = j.read_bytes()
    q = tmp_path / "q.txt"
    q.write_text(QUESTION_TEXT, encoding="utf-8")
    assert run_cli("summarize", j, "--out-dir", tmp_path / "out").returncode == 0
    assert run_cli("render-md", j, "--question-file", q, "--out-dir", tmp_path / "out").returncode == 0
    assert j.read_bytes() == before
