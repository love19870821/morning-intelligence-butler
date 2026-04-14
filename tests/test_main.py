from argparse import Namespace
import io
import json
from pathlib import Path

import pytest

from src.main import (
    MorningReport,
    build_html_report,
    build_markdown_report,
    build_report,
    example_payload,
    load_input_data,
    select_format,
    write_output,
)


def test_build_report_contains_sections():
    report = MorningReport.from_dict(example_payload())
    text = build_report(report)
    assert "Important mail" in text
    assert "News highlights" in text
    assert "Cleanup actions" in text
    assert "Follow-ups" in text
    assert "Generated:" in text


def test_select_format_prefers_one_mode():
    assert select_format(Namespace(format="json", json=True, markdown=False, html=False)) == "json"
    assert select_format(Namespace(format="markdown", json=False, markdown=True, html=False)) == "markdown"
    assert select_format(Namespace(format="html", json=False, markdown=False, html=True)) == "html"
    assert select_format(Namespace(format=None, json=False, markdown=False, html=False)) == "text"


def test_json_mode_returns_normalized_payload():
    report = MorningReport.from_dict(example_payload())
    payload = report.to_dict()
    assert payload["important_mail"]
    assert payload["news_highlights"]
    assert payload["cleanup_actions"]
    assert payload["follow_ups"]


def test_load_input_data_reports_missing_file(tmp_path):
    missing = tmp_path / "nope.json"
    with pytest.raises(ValueError, match="Input file not found"):
        load_input_data(missing)


def test_load_input_data_reports_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_input_data(bad)


def test_write_output_creates_parent_directories(tmp_path):
    target = tmp_path / "nested" / "report.md"
    write_output(target, "hello")
    assert target.read_text(encoding="utf-8") == "hello"


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
    assert "## Follow-ups" in text


def test_html_mode_uses_document_shell():
    report = MorningReport.from_dict(example_payload())
    text = build_html_report(report)
    assert text.startswith("<!doctype html>")
    assert "Morning Intelligence Butler" in text
    assert "<section><h2>Follow-ups</h2>" in text
    assert "\n+<html" not in text


def test_build_report_handles_empty_sections():
    report = MorningReport()
    text = build_report(report)
    assert "- None" in text
