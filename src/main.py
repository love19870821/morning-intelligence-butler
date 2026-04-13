"""Morning Intelligence Butler

Generate a concise morning report from news and mail inputs.
"""

from __future__ import annotations

import argparse
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
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_json(args.input) if args.input else example_payload()
    report = MorningReport.from_dict(data)

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(build_report(report))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
