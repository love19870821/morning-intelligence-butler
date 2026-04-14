"""Morning Intelligence Butler

Generate a concise morning report from news and mail inputs.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class MorningReport:
    important_mail: list[str] = field(default_factory=list)
    news_highlights: list[str] = field(default_factory=list)
    cleanup_actions: list[str] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    generated_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MorningReport":
        mail = data.get("mail", {}) or {}
        meta = data.get("meta", {}) or {}
        return cls(
            important_mail=list(mail.get("important", []) or []),
            news_highlights=list(data.get("news", []) or []),
            cleanup_actions=list(mail.get("cleanup", []) or []),
            follow_ups=list(data.get("follow_ups", []) or []),
            generated_at=meta.get("generated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "important_mail": self.important_mail,
            "news_highlights": self.news_highlights,
            "cleanup_actions": self.cleanup_actions,
            "follow_ups": self.follow_ups,
        }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def format_section(title: str, items: list[str]) -> list[str]:
    lines = [title]
    if items:
        lines.extend(f"- {item}" for item in items)
    else:
        lines.append("- None")
    return lines


def format_markdown_section(title: str, items: list[str]) -> list[str]:
    lines = [f"## {title}"]
    if items:
        lines.extend(f"- {item}" for item in items)
    else:
        lines.append("- None")
    return lines


def format_html_list(items: list[str]) -> str:
    if not items:
        return "<li>None</li>"
    return "".join(f"<li>{html.escape(item)}</li>" for item in items)


def build_report(report: MorningReport) -> str:
    generated = report.generated_at or datetime.now(timezone.utc).astimezone().isoformat(timespec="minutes")
    lines = ["Morning Intelligence Butler", f"Generated: {generated}", "="]
    lines.append("")
    lines.extend(format_section("Important mail", report.important_mail))
    lines.append("")
    lines.extend(format_section("News highlights", report.news_highlights))
    lines.append("")
    lines.extend(format_section("Cleanup actions", report.cleanup_actions))
    lines.append("")
    lines.extend(format_section("Follow-ups", report.follow_ups))
    return "\n".join(lines)


def build_markdown_report(report: MorningReport) -> str:
    generated = report.generated_at or datetime.now(timezone.utc).astimezone().isoformat(timespec="minutes")
    lines = ["# Morning Intelligence Butler", f"Generated: {generated}", ""]
    lines.extend(format_markdown_section("Important mail", report.important_mail))
    lines.append("")
    lines.extend(format_markdown_section("News highlights", report.news_highlights))
    lines.append("")
    lines.extend(format_markdown_section("Cleanup actions", report.cleanup_actions))
    lines.append("")
    lines.extend(format_markdown_section("Follow-ups", report.follow_ups))
    return "\n".join(lines)


def build_html_report(report: MorningReport) -> str:
    generated = report.generated_at or datetime.now(timezone.utc).astimezone().isoformat(timespec="minutes")
    return f"""<!doctype html>
<html lang=\"zh-Hant\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <title>Morning Intelligence Butler</title>\n  <style>body{{font-family:system-ui,sans-serif;max-width:860px;margin:40px auto;padding:0 16px;line-height:1.6}}h1{{margin-bottom:0}}.meta{{color:#666;margin-top:4px}}section{{margin-top:24px}}ul{{padding-left:20px}}</style>\n</head>\n<body>\n  <h1>Morning Intelligence Butler</h1>\n  <div class=\"meta\">Generated: {html.escape(generated)}</div>\n  <section><h2>Important mail</h2><ul>{format_html_list(report.important_mail)}</ul></section>\n  <section><h2>News highlights</h2><ul>{format_html_list(report.news_highlights)}</ul></section>\n  <section><h2>Cleanup actions</h2><ul>{format_html_list(report.cleanup_actions)}</ul></section>\n  <section><h2>Follow-ups</h2><ul>{format_html_list(report.follow_ups)}</ul></section>\n</body>\n</html>"""


def example_payload() -> dict[str, Any]:
    return {
        "meta": {"generated_at": "2026-04-14T08:00:00+08:00"},
        "news": ["Taiwan market opens higher", "AI tooling continues to accelerate"],
        "follow_ups": ["Reply to the supplier before 11:00", "Check the 10:30 calendar invite"],
        "mail": {
            "important": [
                "Reply to supplier about invoice",
                "Check calendar invite for 10:30 meeting",
            ],
            "cleanup": [
                "Moved 24 promotional emails to trash",
                "Skipped 3 starred messages and 2 emails with attachments",
            ],
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Morning Intelligence Butler")
    parser.add_argument("--input", type=Path, help="JSON file with news/mail data")
    parser.add_argument("--output", type=Path, help="Write the rendered report to a file")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    parser.add_argument("--markdown", action="store_true", help="Output Markdown instead of text")
    parser.add_argument("--html", action="store_true", help="Output HTML instead of text")
    return parser.parse_args()


def select_format(args: argparse.Namespace) -> str:
    if args.json:
        return "json"
    if args.markdown:
        return "markdown"
    if args.html:
        return "html"
    return "text"


def render_report(report: MorningReport, output_format: str) -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
    if output_format == "markdown":
        return build_markdown_report(report)
    if output_format == "html":
        return build_html_report(report)
    return build_report(report)


def main() -> None:
    args = parse_args()
    data = load_json(args.input) if args.input else example_payload()
    report = MorningReport.from_dict(data)
    output_format = select_format(args)
    output = render_report(report, output_format)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
