# Morning Intelligence Butler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Morning Intelligence Butler is a small open-source morning briefing assistant.
It combines daily news, important mail summaries, and safe inbox cleanup into one concise report.

## Start here

Shortest path from clone to a real report:

1. Install locally.
2. Verify the install.
3. Generate a demo bundle.
4. Run the tool on your own input.

```bash
pip install -e .
morning-butler-smoke
morning-butler --generate-demo demo-kit
morning-butler --input demo-kit/sample_report.json --output morning-report.txt
```

If you prefer the module form:

```bash
python -m morning_butler --input demo-kit/sample_report.json
```

## Why it exists

Most morning tools are either too noisy or too weak.
This project is designed to be:

- practical
- conservative by default
- easy to automate
- pleasant to read
- safe with mail cleanup

## What it does

Each morning it can help you:

- see today’s important mail first
- summarize what needs attention
- list safe cleanup actions
- identify follow-up items before the day starts
- produce a short report you can scan quickly
- export text, JSON, Markdown, or HTML
- save the result directly to a file

## Example output

Text mode:

```text
Morning Intelligence Butler
Generated: 2026-04-14T08:00:00+08:00
Summary: 2 important mail, 2 news items, 2 cleanup actions, 2 follow-ups
=

Important mail
- Reply to client about proposal

News highlights
- Taiwan headline example
- AI news example

Cleanup actions
- Moved 24 promotional emails to trash
- Skipped 3 starred messages and 2 emails with attachments

Follow-ups
- Reply to the supplier before 11:00
- Check the 10:30 calendar invite
```

Markdown mode:

```md
# Morning Intelligence Butler
Generated: 2026-04-14T08:00:00+08:00
**Summary:** 2 important mail, 2 news items, 2 cleanup actions, 2 follow-ups

## Important mail
- Reply to client about proposal

## News highlights
- Taiwan headline example
- AI news example
```

HTML mode:

```html
<!doctype html>
<html lang="zh-Hant">
  <head>...</head>
  <body>
    <h1>Morning Intelligence Butler</h1>
    <p class="summary">2 important mail · 2 news items · 2 cleanup actions · 2 follow-ups</p>
  </body>
</html>
```

## Verify the install

Run the smoke test after installing:

```bash
pip install -e .
morning-butler-smoke
python scripts/smoke_test.py
```

## Release check

Before cutting a release, run the local release verification flow:

```bash
morning-butler-release-check
```

This runs pytest, the smoke test, builds a wheel, installs that wheel into a fresh virtual environment, and runs the installed smoke test again.

See [RELEASE.md](RELEASE.md) for the full pre-publish checklist.

## Demo bundle

Create a full sample bundle:

```bash
morning-butler --generate-demo
morning-butler --generate-demo demo-kit
```

The bundle includes sample input plus rendered text, Markdown, HTML, and JSON outputs.

## Real use

Feed the tool your own report JSON:

```bash
morning-butler --input your_report.json
morning-butler --format json --input your_report.json --output report.json
morning-butler --format markdown --input your_report.json --output report.md
morning-butler --format html --input your_report.json --output report.html
```

For pipelines, stdin also works:

```bash
cat your_report.json | morning-butler --input - --format text
```

## Sample bootstrap

Create a starter sample file when you need one:

```bash
morning-butler --write-sample
morning-butler --write-sample my_sample.json
```

See [INPUT_SCHEMA.md](INPUT_SCHEMA.md) for the expected input shape and field meanings.

## Design principles

- Never hard-delete mail
- Skip starred mail by default
- Skip mail with attachments by default
- Favor explicit summaries over long dumps
- Make the morning report readable in under a minute
- Surface follow-ups, not just summaries
- Support output formats that are easy to reuse elsewhere
- Keep file output simple and predictable

## Planned roadmap

- News source connectors
- Gmail summary integration
- Telegram delivery
- Scheduled execution
- Configurable cleanup rules
- Richer Markdown / HTML output variants

## Project status

This is an early public foundation release.
It is intended to grow into a reusable morning briefing workflow.

## Release notes

See [CHANGELOG.md](CHANGELOG.md) for versioned release notes and verification-focused changes.
