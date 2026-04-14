# Morning Intelligence Butler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/love19870821/morning-intelligence-butler/actions/workflows/ci.yml/badge.svg)](https://github.com/love19870821/morning-intelligence-butler/actions/workflows/ci.yml)

Morning Intelligence Butler is a small open-source morning briefing assistant.
It combines daily news, important mail summaries, and safe inbox cleanup into one concise report.

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
  </body>
</html>
```

Write output to a file:

```bash
python src/main.py --markdown --input sample_report.json --output report.md
python src/main.py --html --input sample_report.json --output report.html
python src/main.py --json --input sample_report.json --output report.json
```

Read input from stdin:

```bash
cat sample_report.json | python src/main.py --json --input -
```

Create a starter sample file:

```bash
python src/main.py --write-sample
python src/main.py --write-sample my_sample.json
```

## Quick start

```bash
python src/main.py
python src/main.py --input sample_report.json
python src/main.py --format json
python src/main.py --format markdown
python src/main.py --format html
```

Or install it locally:

```bash
pip install -e .
morning-butler --input sample_report.json
```

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
