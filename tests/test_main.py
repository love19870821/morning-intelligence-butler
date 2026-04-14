from src.main import MorningReport, build_markdown_report, build_report, example_payload


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


def test_build_report_handles_empty_sections():
    report = MorningReport()
    text = build_report(report)
    assert "- None" in text
