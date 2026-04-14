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

    def counts(self) -> dict[str, int]:
        return {
            "important_mail": len(self.important_mail),
            "news_highlights": len(self.news_highlights),
            "cleanup_actions": len(self.cleanup_actions),
            "follow_ups": len(self.follow_ups),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "summary": self.counts(),
            "important_mail": self.important_mail,
            "news_highlights": self.news_highlights,
            "cleanup_actions": self.cleanup_actions,
            "follow_ups": self.follow_ups,
        }


def load_json(path: Path) -> dict[str, Any]:
    if str(path) == "-":
        return json.loads(sys.stdin.read())
    return json.loads(path.read_text(encoding="utf-8"))


def load_input_data(input_path: Path | None) -> dict[str, Any]:
    if input_path is None:
        return example_payload()
    try:
        return load_json(input_path)
    except FileNotFoundError as exc:
        raise ValueError(f"Input file not found: {input_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in input file {input_path}: {exc.msg}") from exc


def write_output(path: Path, output: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")


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


def format_summary_line(report: MorningReport) -> str:
    counts = report.counts()
    return (
        f"Summary: {counts['important_mail']} important mail, "
        f"{counts['news_highlights']} news items, "
        f"{counts['cleanup_actions']} cleanup actions, "
        f"{counts['follow_ups']} follow-ups"
    )


def format_markdown_summary(report: MorningReport) -> str:
    counts = report.counts()
    return (
        f"**Summary:** {counts['important_mail']} important mail, "
        f"{counts['news_highlights']} news items, "
        f"{counts['cleanup_actions']} cleanup actions, "
        f"{counts['follow_ups']} follow-ups"
    )


def format_html_summary(report: MorningReport) -> str:
    counts = report.counts()
    return (
        "<p class=\"summary\">"
        f"{counts['important_mail']} important mail · "
        f"{counts['news_highlights']} news items · "
        f"{counts['cleanup_actions']} cleanup actions · "
        f"{counts['follow_ups']} follow-ups"
        "</p>"
    )


def build_report(report: MorningReport) -> str:
    generated = report.generated_at or datetime.now(timezone.utc).astimezone().isoformat(timespec="minutes")
    lines = ["Morning Intelligence Butler", f"Generated: {generated}", format_summary_line(report), "="]
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
    lines = ["# Morning Intelligence Butler", f"Generated: {generated}", format_markdown_summary(report), ""]
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
<html lang=\"zh-Hant\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <title>Morning Intelligence Butler</title>\n  <style>body{{font-family:system-ui,sans-serif;max-width:860px;margin:40px auto;padding:0 16px;line-height:1.6}}h1{{margin-bottom:0}}.meta{{color:#666;margin-top:4px}}.summary{{font-weight:600;margin-top:8px}}section{{margin-top:24px}}ul{{padding-left:20px}}</style>\n</head>\n<body>\n  <h1>Morning Intelligence Butler</h1>\n  <div class=\"meta\">Generated: {html.escape(generated)}</div>\n  {format_html_summary(report)}\n  <section><h2>Important mail</h2><ul>{format_html_list(report.important_mail)}</ul></section>\n  <section><h2>News highlights</h2><ul>{format_html_list(report.news_highlights)}</ul></section>\n  <section><h2>Cleanup actions</h2><ul>{format_html_list(report.cleanup_actions)}</ul></section>\n  <section><h2>Follow-ups</h2><ul>{format_html_list(report.follow_ups)}</ul></section>\n</body>\n</html>"""


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
    parser.add_argument(
        "--write-sample",
        nargs="?",
        const=Path("sample_report.json"),
        type=Path,
        help="Write a starter sample JSON file and exit",
    )
    parser.add_argument(
        "--generate-demo",
        nargs="?",
        const=Path("demo-output"),
        type=Path,
        help="Generate a full demo bundle (sample input + rendered outputs) and exit",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "markdown", "html"),
        help="Explicitly choose the output format",
    )
    parser.add_argument("--version", action="version", version="morning-intelligence-butler 0.2.0")
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument("--json", action="store_true", help="Output JSON instead of text")
    format_group.add_argument("--markdown", action="store_true", help="Output Markdown instead of text")
    format_group.add_argument("--html", action="store_true", help="Output HTML instead of text")
    return parser.parse_args()


def select_format(args: argparse.Namespace) -> str:
    if args.format:
        return args.format
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


def write_sample_input(path: Path) -> None:
    write_output(path, json.dumps(example_payload(), ensure_ascii=False, indent=2))


def generate_demo_bundle(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    write_sample_input(directory / "sample_report.json")
    report = MorningReport.from_dict(example_payload())
    write_output(directory / "report.txt", build_report(report))
    write_output(directory / "report.md", build_markdown_report(report))
    write_output(directory / "report.html", build_html_report(report))
    write_output(directory / "report.json", render_report(report, "json"))


def main() -> None:
    args = parse_args()

    if args.generate_demo:
        generate_demo_bundle(args.generate_demo)
        return

    if args.write_sample:
        write_sample_input(args.write_sample)
        return

    try:
        data = load_input_data(args.input)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    report = MorningReport.from_dict(data)
    output_format = select_format(args)
    output = render_report(report, output_format)

    if args.output:
        write_output(args.output, output)
    else:
        print(output)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
