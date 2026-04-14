from argparse import Namespace
from importlib.metadata import PackageNotFoundError, version as package_version
import io
import json
from pathlib import Path

import pytest

from src import __version__
from src.main import (
    MorningReport,
    build_html_report,
    build_markdown_report,
    build_report,
    example_payload,
    generate_demo_bundle,
    load_input_data,
    main,
    select_format,
    write_output,
    write_sample_input,
)


def test_build_report_contains_sections():
    report = MorningReport.from_dict(example_payload())
    text = build_report(report)
    assert "Important mail" in text
    assert "News highlights" in text
    assert "Market snapshot" in text
    assert "Cleanup actions" in text
    assert "Follow-ups" in text
    assert "Generated:" in text
    assert "Summary:" in text


def test_select_format_prefers_one_mode():
    assert select_format(Namespace(format="json", json=True, markdown=False, html=False)) == "json"
    assert select_format(Namespace(format="markdown", json=False, markdown=True, html=False)) == "markdown"
    assert select_format(Namespace(format="html", json=False, markdown=False, html=True)) == "html"
    assert select_format(Namespace(format=None, json=False, markdown=False, html=False)) == "text"


def test_version_is_consistent_between_source_and_installed_metadata():
    assert __version__ == "0.2.0"
    try:
        assert package_version("morning-intelligence-butler") == __version__
    except PackageNotFoundError:
        pytest.skip("package metadata is not installed in this environment")


def test_json_mode_returns_normalized_payload():
    report = MorningReport.from_dict(example_payload())
    payload = report.to_dict()
    assert payload["important_mail"]
    assert payload["news_highlights"]
    assert payload["market_snapshot"]
    assert payload["cleanup_actions"]
    assert payload["follow_ups"]
    assert payload["summary"]["important_mail"] == len(payload["important_mail"])


def test_load_input_data_reports_missing_file(tmp_path):
    missing = tmp_path / "nope.json"
    with pytest.raises(ValueError, match="Input file not found"):
        load_input_data(missing)


def test_main_returns_consistent_exit_codes_for_success_and_bad_input(tmp_path, capsys):
    sample = tmp_path / "sample.json"
    demo = tmp_path / "demo"
    missing = tmp_path / "nope.json"

    assert main(["--write-sample", str(sample)]) == 0
    assert sample.exists()

    assert main(["--generate-demo", str(demo)]) == 0
    assert (demo / "report.txt").exists()

    assert main(["--input", str(missing)]) == 2
    captured = capsys.readouterr()
    assert "Input file not found" in captured.err


def test_load_input_data_reports_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_input_data(bad)


def test_write_output_creates_parent_directories(tmp_path):
    target = tmp_path / "nested" / "report.md"
    write_output(target, "hello")
    assert target.read_text(encoding="utf-8") == "hello"


def test_write_sample_input_creates_starter_json(tmp_path):
    target = tmp_path / "starter" / "sample_report.json"
    write_sample_input(target)
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["mail"]["important"]
    assert data["follow_ups"]


def test_generate_demo_bundle_creates_all_demo_files(tmp_path):
    target = tmp_path / "demo"
    generate_demo_bundle(target)
    assert (target / "sample_report.json").exists()
    assert (target / "report.txt").exists()
    assert (target / "report.md").exists()
    assert (target / "report.html").exists()
    assert (target / "report.json").exists()


def test_stdin_input_can_be_used_via_hyphen(tmp_path, monkeypatch):
    sample = example_payload()
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(sample)))
    data = load_input_data(Path("-"))
    assert data["mail"]["important"]


def test_markdown_mode_uses_headings():
    report = MorningReport.from_dict(example_payload())
    text = build_markdown_report(report)
    assert text.startswith("# Morning Intelligence Butler")
    assert "## Important mail" in text
    assert "## Market snapshot" in text
    assert "## Follow-ups" in text
    assert "**Summary:**" in text


def test_html_mode_uses_document_shell():
    report = MorningReport.from_dict(example_payload())
    text = build_html_report(report)
    assert text.startswith("<!doctype html>")
    assert "Morning Intelligence Butler" in text
    assert "<section><h2>Market snapshot</h2>" in text
    assert "<section><h2>Follow-ups</h2>" in text
    assert "\n+<html" not in text
    assert 'class="summary"' in text


def test_build_report_handles_empty_sections():
    report = MorningReport()
    text = build_report(report)
    assert "- None" in text
