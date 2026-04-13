"""Morning Intelligence Butler

Generate a concise morning report from news and mail inputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class MorningReport:
    important_mail: list[str] = field(default_factory=list)
    news_highlights: list[str] = field(default_factory=list)
    cleanup_actions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MorningReport":
        mail = data.get("mail", {}) or {}
        return cls(
            important_mail=list(mail.get("important", []) or []),
            news_highlights=list(data.get("news", []) or []),
            cleanup_actions=list(mail.get("cleanup", []) or []),
        )


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def format_section(title: str, items: list[str]) -> list[str]:
    lines = [title]
    if items:
        lines.extend(f"- {item}" for item in items)
    else:
        lines.append("- None")
    return lines


def build_report(report: MorningReport) -> str:
    lines = ["Morning Intelligence Butler", "="]
    lines.append("")
    lines.extend(format_section("Important mail", report.important_mail))
    lines.append("")
    lines.extend(format_section("News highlights", report.news_highlights))
    lines.append("")
    lines.extend(format_section("Cleanup actions", report.cleanup_actions))
    return "\n".join(lines)


def example_payload() -> dict[str, Any]:
    return {
        "news": ["Taiwan headline example", "AI headline example"],
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
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_json(args.input) if args.input else example_payload()
    report = MorningReport.from_dict(data)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(build_report(report))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
