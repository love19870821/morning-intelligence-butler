# Morning Intelligence Butler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Morning Intelligence Butler is a small open-source morning briefing assistant.
It combines Traditional Chinese news summaries, Gmail triage, live market prices, and follow-up items into one concise report.

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

## Deterministic market fixture

For demos, tests, or offline runs, set `MORNING_BUTLER_MARKET_FIXTURE` to a JSON object with `gold`, `oil`, and `usd_twd` values.

```bash
export MORNING_BUTLER_MARKET_FIXTURE='{"gold":"USD 4,796.65/oz","oil":"USD 97.79/bbl","usd_twd":"31.623"}'
morning-butler --input demo-kit/sample_report.json
```

This keeps the market section stable without touching the live fetch flow.

## Example output

Text mode:

```text
晨報
產生時間：2026-04-14T08:00:00+08:00
摘要：2 封重要信件、2 則新聞、3 筆市場行情、2 項清理動作、2 項靈感與待解鎖事項
=

重要信件
- 回覆供應商發票事宜
- 確認 10:30 會議的行事曆邀請

新聞重點
- 台灣市場開盤走高
- AI 工具持續加速

市場行情
- 國際黃金：即時價格
- 布蘭特原油：即時價格
- 美元／台幣：即時匯率

清理動作
- 已將 24 封促銷信移到垃圾桶
- 略過 3 封已加星號郵件與 2 封含附件郵件

靈感與待解鎖事項
- 在 11:00 前回覆供應商
- 確認 10:30 的行事曆邀請
```

Markdown mode:

```md
# 晨報
產生時間：2026-04-14T08:00:00+08:00
**摘要：**2 封重要信件、2 則新聞、3 筆市場行情、2 項清理動作、2 項靈感與待解鎖事項

## 重要信件
- 回覆供應商發票事宜
- 確認 10:30 會議的行事曆邀請

## 新聞重點
- 台灣市場開盤走高
- AI 工具持續加速

## 市場行情
- 國際黃金：USD 2,350/oz
- 布蘭特原油：USD 84.20/bbl
- 美元／台幣：32.12

## 清理動作
- 已將 24 封促銷信移到垃圾桶
- 略過 3 封已加星號郵件與 2 封含附件郵件

## 靈感與待解鎖事項
- 在 11:00 前回覆供應商
- 確認 10:30 的行事曆邀請
```

HTML mode:

```html
<!doctype html>
<html lang="zh-Hant">
  <head>...</head>
  <body>
    <h1>晨報</h1>
    <p class="summary">2 封重要信件 · 2 則新聞 · 3 筆市場行情 · 2 項清理動作 · 2 項靈感與待解鎖事項</p>
    <section><h2>市場行情</h2><ul>...</ul></section>
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

## 實際使用

把你自己的晨報 JSON 丟進去即可。
工具會自動抓取即時的國際黃金、布蘭特原油與美元／台幣。

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

For common errors and fixes, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

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
