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

## 信箱 Mailbox

[`scripts/send_letters.py`](scripts/send_letters.py) 由 [`.github/workflows/send-letters.yml`](.github/workflows/send-letters.yml) 每天執行，回信寫入 `MAILBOX/`。收件者與設定在 [`scripts/mailbox.json`](scripts/mailbox.json)：

- `latest:<前綴>` 自動選該系列最新的模型；寫完整名稱則固定版本
- 接力：一天一棒，依 `recipients` 順序輪流；第一棒讀 `LETTER.md`，之後讀上一棒的信。給人工智慧的說明在 `relay.first`、`relay.next`（`{prev}`、`{next}` 會換成模型名稱）。某一棒沒寄到，隔天由同一位重寄
- `MAILBOX/` 裡沒有 `relay-` 開頭的檔案，是接力開始前（2026-11-02 至 11-04）每天同時寄給四個人工智慧的回信
- 需要 repository secret `OPENROUTER_API_KEY`
- 每封送達的回信，[`scripts/tokenize_replies.mjs`](scripts/tokenize_replies.mjs) 會另存一份 token ID 版本在同一天的 `token/` 資料夾，分詞器與 readme-folded-letters 相同（o200k_base，gpt-tokenizer 2.9.0）。重做全部：`npm install --no-save gpt-tokenizer@2.9.0 && node scripts/tokenize_replies.mjs --force && python scripts/send_letters.py --index-only`
- 本機測試：`python scripts/send_letters.py --dry-run`（不連網、不花費；測完刪掉產生的日期資料夾）
