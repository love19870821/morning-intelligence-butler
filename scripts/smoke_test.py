#!/usr/bin/env python3
"""Smoke test for morning-intelligence-butler.

This verifies the most important first-run flows:
- create a sample input file
- render text/markdown/html/json outputs
- write outputs to files
- read input from stdin
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(
    cmd: list[str], *, cwd: Path, input_text: str | None = None, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def assert_file(path: Path, startswith: str) -> None:
    content = path.read_text(encoding="utf-8")
    if not content.startswith(startswith):
        raise AssertionError(f"{path.name} did not start with {startswith!r}")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    cli = shutil.which("morning-butler")
    if cli is None:
        cli_cmd = [sys.executable, str(repo_root / "src" / "main.py")]
    else:
        cli_cmd = [cli]

    env = os.environ.copy()
    env["MORNING_BUTLER_MARKET_FIXTURE"] = json.dumps(
        {
            "gold": "USD 4,796.65/oz",
            "oil": "USD 97.79/bbl",
            "usd_twd": "31.623",
        }
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        sample = tmp / "sample.json"
        text_out = tmp / "report.txt"
        md_out = tmp / "report.md"
        html_out = tmp / "report.html"
        json_out = tmp / "report.json"
        demo_dir = tmp / "demo"

        run(cli_cmd + ["--write-sample", str(sample)], cwd=repo_root, env=env)
        sample_data = json.loads(sample.read_text(encoding="utf-8"))
        if not sample_data.get("mail", {}).get("important"):
            raise AssertionError("sample JSON missing important mail")

        run(cli_cmd + ["--format", "text", "--input", str(sample), "--output", str(text_out)], cwd=repo_root, env=env)
        run(cli_cmd + ["--format", "markdown", "--input", str(sample), "--output", str(md_out)], cwd=repo_root, env=env)
        run(cli_cmd + ["--format", "html", "--input", str(sample), "--output", str(html_out)], cwd=repo_root, env=env)
        run(cli_cmd + ["--format", "json", "--input", str(sample), "--output", str(json_out)], cwd=repo_root, env=env)

        assert_file(text_out, "Morning Intelligence Butler")
        assert_file(md_out, "# Morning Intelligence Butler")
        assert_file(html_out, "<!doctype html>")
        json.loads(json_out.read_text(encoding="utf-8"))

        stdin_payload = sample.read_text(encoding="utf-8")
        result = run(cli_cmd + ["--format", "json", "--input", "-"], cwd=repo_root, input_text=stdin_payload, env=env)
        stdin_data = json.loads(result.stdout)
        if "important_mail" not in stdin_data:
            raise AssertionError("stdin JSON missing important_mail")

        run(cli_cmd + ["--generate-demo", str(demo_dir)], cwd=repo_root, env=env)
        expected = {
            "sample_report.json",
            "report.txt",
            "report.md",
            "report.html",
            "report.json",
        }
        actual = {p.name for p in demo_dir.iterdir()}
        if expected != actual:
            raise AssertionError(f"demo bundle mismatch: expected {sorted(expected)}, got {sorted(actual)}")

    print("Smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
