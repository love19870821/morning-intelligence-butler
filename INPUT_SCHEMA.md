# Input schema

This project accepts a simple JSON document describing the morning briefing.

## Canonical sample

The repository includes `sample_report.json` as a ready-to-run example.

```json
{
  "meta": {
    "generated_at": "2026-04-14T08:00:00+08:00"
  },
  "news": [
    "Taiwan market opens higher",
    "AI tooling continues to accelerate"
  ],
  "follow_ups": [
    "Reply to the supplier before 11:00",
    "Check the 10:30 calendar invite"
  ],
  "mail": {
    "important": [
      "Reply to supplier about invoice",
      "Check calendar invite for 10:30 meeting"
    ],
    "cleanup": [
      "Moved 24 promotional emails to trash",
      "Skipped 3 starred messages and 2 emails with attachments"
    ]
  }
}
```

## Fields

### `meta.generated_at`

- Optional string timestamp.
- If present, the renderer prints it as the report time.
- If omitted, the tool uses the current local time.

### `news`

- Optional array of strings.
- Each item becomes one news highlight.

### Market snapshot

- Fetched automatically at runtime from live sources.
- It is not part of the input JSON.
- The tool retrieves international gold, Brent oil, and USD/TWD prices automatically.

### `follow_ups`

- Optional array of strings.
- Each item becomes one follow-up item in the final report.

### `mail.important`

- Optional array of strings.
- Each item becomes one important-mail entry.

### `mail.cleanup`

- Optional array of strings.
- Each item becomes one safe cleanup action.

## Notes

- Missing sections are treated as empty lists.
- Invalid JSON is rejected with a clear error.
- `--input -` reads the same structure from stdin.
