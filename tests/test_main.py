from src.main import (
    MorningReport,
    build_html_report,
    build_markdown_report,
    build_report,
    example_payload,
    main,
)


def test_build_report_contains_sections():
    report = MorningReport.from_dict(example_payload())
    text = build_report(report)
    assert "Important mail" in text
    assert "News highlights" in text
    assert "Cleanup actions" in text
    assert "Follow-ups" in text
    assert "Generated:" in text


def test_json_mode_returns_normalized_payload():
    report = MorningReport.from_dict(example_payload())
    payload = report.to_dict()
    assert payload["important_mail"]
    assert payload["news_highlights"]
    assert payload["cleanup_actions"]
    assert payload["follow_ups"]


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
