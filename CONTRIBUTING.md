# CONTRIBUTING

*給維護這個 repository 的人。To maintainers of this repository.*

## 單一真相來源

只編輯 [`core/RULE.md`](core/RULE.md)（英文 [`core/RULE.en.md`](core/RULE.en.md)），然後執行：

```bash
node scripts/sync-adapters.mjs
```

會同步產生各平台適配檔。標有 `GENERATED FILE` 的檔案**請勿手改**。

- 自動載入的適配檔（`SKILL.md`、Cursor、Copilot、`AGENTS.md`）中英並列，英文請求也能穩定觸發。
- 貼上版本分成中文（`dist/paste/*.md`）與英文（`dist/paste/*.en.md`），因為指示欄位有長度限制。
- 信（`LETTER.md`、`LETTER.en.md`）由同一支腳本複製到 skill 資料夾，不要直接改副本。

改規則後，用 [docs/manual-test.md](docs/manual-test.md) 跑一次煙霧測試。

## Single source of truth

Edit only [`core/RULE.md`](core/RULE.md) (English: [`core/RULE.en.md`](core/RULE.en.md)), then run:

```bash
node scripts/sync-adapters.mjs
```

This regenerates every platform adapter. Do **not** hand-edit files marked `GENERATED FILE`.

- Adapters that load automatically (`SKILL.md`, Cursor, Copilot, `AGENTS.md`) carry both languages, so English requests trigger reliably.
- Paste versions come in Chinese (`dist/paste/*.md`) and English (`dist/paste/*.en.md`), because instruction fields are short.
- The letters (`LETTER.md`, `LETTER.en.md`) are copied into the skill folder by the same script; do not edit the copies.

After changing the rule, run the smoke tests in [docs/manual-test.md](docs/manual-test.md).
