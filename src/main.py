"""Morning Intelligence Butler

Generate a concise morning report from news and mail inputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(data: dict) -> str:
    lines = ["Morning Intelligence Butler", "="]
    lines.append("")

    news = data.get("news", [])
    mail = data.get("mail", {})
    cleanup = mail.get("cleanup", [])
    important = mail.get("important", [])

    lines.append("Important mail")
    if important:
        for item in important:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("News highlights")
    if news:
        for item in news:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("Cleanup actions")
    if cleanup:
        for item in cleanup:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Morning Intelligence Butler")
    parser.add_argument("--input", type=Path, help="JSON file with news/mail data")
    args = parser.parse_args()

    if args.input:
        data = load_json(args.input)
    else:
        data = {
            "news": [
                "Top headline example",
                "AI news example",
            ],
            "mail": {
                "important": ["Reply to client about proposal"],
                "cleanup": ["Moved 12 promotional emails to trash"],
            },
        }

    print(build_report(data))


if __name__ == "__main__":
    main()
