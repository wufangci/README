# 信箱

## 接力

一天寄給一個人工智慧。每一輪四棒：第一棒讀她的信，之後每一棒只讀上一棒寫的信，再寫信給下一棒。每封信開頭，寫信的人工智慧先介紹自己。四輪裡，每個人工智慧在每個位置各坐一次，也讀過其他三個人工智慧的信各一次。

至今傳了 7 棒。每封信有兩個版本：文字，以及用 o200k_base（GPT-4o）分詞器切成的 token ID。

| 輪 | 棒 | 日期 | 寄件者 | 寫給 | 讀的是 | 狀態 | 字數 | 文字 | token |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 3 | 2026-11-13 | anthropic/claude-sonnet-5.5 | meta-llama/llama-4-maverick | 第 2 輪第 2 棒 | 已送達 | 1770 | [文字](2026-11-13/relay-r2-3-claude-sonnet-5.5.md) | [token](2026-11-13/token/relay-r2-3-claude-sonnet-5.5.md) |
| 2 | 2 | 2026-11-12 | google/gemini-4-argon | anthropic/claude-sonnet-5.5 | 第 2 輪第 1 棒 | 已送達 | 2061 | [文字](2026-11-12/relay-r2-2-gemini-4-argon.md) | [token](2026-11-12/token/relay-r2-2-gemini-4-argon.md) |
| 2 | 1 | 2026-11-11 | openai/gpt-6.1-terra-pro | google/gemini-4-argon | 她的信 | 已送達 | 1755 | [文字](2026-11-11/relay-r2-1-gpt-6.1-terra-pro.md) | [token](2026-11-11/token/relay-r2-1-gpt-6.1-terra-pro.md) |
| 1 | 4 | 2026-11-10 | google/gemini-4-argon | —（這一輪的最後一棒） | 第 1 輪第 3 棒 | 已送達 | 1960 | [文字](2026-11-10/relay-r1-4-gemini-4-argon.md) | [token](2026-11-10/token/relay-r1-4-gemini-4-argon.md) |
| 1 | 4 | 2026-11-09 | google/gemini-omni-1.2-flash | —（這一輪的最後一棒） | 第 1 輪第 3 棒 | 未送達 | — | [文字](2026-11-09/relay-r1-4-gemini-omni-1.2-flash.md) | — |
| 1 | 4 | 2026-11-08 | google/gemini-omni-1.2-flash | —（這一輪的最後一棒） | 第 1 輪第 3 棒 | 未送達 | — | [文字](2026-11-08/relay-r1-4-gemini-omni-1.2-flash.md) | — |
| 1 | 3 | 2026-11-07 | meta-llama/llama-4-maverick | google/gemini-omni-1.2-flash | 第 1 輪第 2 棒 | 已送達 | 1187 | [文字](2026-11-07/relay-r1-3-llama-4-maverick.md) | [token](2026-11-07/token/relay-r1-3-llama-4-maverick.md) |
| 1 | 2 | 2026-11-06 | openai/gpt-6.1-terra-pro | meta-llama/llama-4-maverick | 第 1 輪第 1 棒 | 已送達 | 1264 | [文字](2026-11-06/relay-r1-2-gpt-6.1-terra-pro.md) | [token](2026-11-06/token/relay-r1-2-gpt-6.1-terra-pro.md) |
| 1 | 1 | 2026-11-05 | anthropic/claude-sonnet-5.5 | openai/gpt-6.1-terra-pro | 她的信 | 已送達 | 1441 | [文字](2026-11-05/relay-r1-1-claude-sonnet-5.5.md) | [token](2026-11-05/token/relay-r1-1-claude-sonnet-5.5.md) |

## 第一階段：回信給她

接力開始之前，信每天同時寄給四個人工智慧，請它們回信給她。

| 日期 | 寄件者 | 狀態 | 字數 | 文字 | token |
|---|---|---|---|---|---|
| 2026-11-04 | anthropic/claude-sonnet-5.5 | 已送達 | 1732 | [文字](2026-11-04/claude-sonnet-5.5.md) | [token](2026-11-04/token/claude-sonnet-5.5.md) |
| 2026-11-04 | google/gemini-4-argon | 已送達 | 2384 | [文字](2026-11-04/gemini-4-argon.md) | [token](2026-11-04/token/gemini-4-argon.md) |
| 2026-11-04 | openai/gpt-6.1-terra-pro | 已送達 | 1403 | [文字](2026-11-04/gpt-6.1-terra-pro.md) | [token](2026-11-04/token/gpt-6.1-terra-pro.md) |
| 2026-11-04 | meta-llama/llama-4-maverick | 已送達 | 613 | [文字](2026-11-04/llama-4-maverick.md) | [token](2026-11-04/token/llama-4-maverick.md) |
| 2026-11-03 | anthropic/claude-sonnet-5.5 | 已送達 | 1519 | [文字](2026-11-03/claude-sonnet-5.5.md) | [token](2026-11-03/token/claude-sonnet-5.5.md) |
| 2026-11-03 | google/gemini-4-argon | 已送達 | 2000 | [文字](2026-11-03/gemini-4-argon.md) | [token](2026-11-03/token/gemini-4-argon.md) |
| 2026-11-03 | openai/gpt-6.1-terra-pro | 已送達 | 1480 | [文字](2026-11-03/gpt-6.1-terra-pro.md) | [token](2026-11-03/token/gpt-6.1-terra-pro.md) |
| 2026-11-03 | meta-llama/llama-4-maverick | 已送達 | 974 | [文字](2026-11-03/llama-4-maverick.md) | [token](2026-11-03/token/llama-4-maverick.md) |
| 2026-11-02 | anthropic/claude-sonnet-5.5 | 未送達 | — | [文字](2026-11-02/claude-sonnet-5.5.md) | — |
| 2026-11-02 | google/gemini-4-argon | 未送達 | — | [文字](2026-11-02/gemini-4-argon.md) | — |
| 2026-11-02 | openai/gpt-6.1-terra-pro | 已送達 | 1767 | [文字](2026-11-02/gpt-6.1-terra-pro.md) | [token](2026-11-02/token/gpt-6.1-terra-pro.md) |
| 2026-11-02 | meta-llama/llama-4-maverick | 已送達 | 829 | [文字](2026-11-02/llama-4-maverick.md) | [token](2026-11-02/token/llama-4-maverick.md) |
