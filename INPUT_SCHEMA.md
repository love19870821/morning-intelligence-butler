# Input schema

This project accepts a simple JSON document describing the morning briefing.

## 範例樣本

倉庫內附有 `sample_report.json`，可直接拿來執行。

```json
{
  "meta": {
    "generated_at": "2026-04-14T08:00:00+08:00"
  },
  "news": [
    "台灣市場開盤走高",
    "AI 工具持續加速"
  ],
  "follow_ups": [
    "在 11:00 前回覆供應商",
    "確認 10:30 的行事曆邀請"
  ],
  "mail": {
    "important": [
      "回覆供應商發票事宜",
      "確認 10:30 會議的行事曆邀請"
    ],
    "cleanup": [
      "已將 24 封促銷信移到垃圾桶",
      "略過 3 封已加星號郵件與 2 封含附件郵件"
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
