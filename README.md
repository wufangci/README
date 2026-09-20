*[Read in English](README.en.md)*

# 詮釋權宣言 / FOLLOW MY VOICE

這不只是一個工具，是一份藝術行動與宣言。

在AI技術得以無需同意就擷取、模仿、販售原住民族的圖騰、祭儀、歌謠與神話的此刻，詮釋權，也就是誰有資格說出這個故事，正從文化的主人手中悄悄轉移到訓練資料的擁有者手中。

完整的立場、控訴與宣告，請讀 **[MANIFESTO.md](MANIFESTO.md)**。

這份 repository 把宣言變成可在多個 AI Agent 平台載入的行為規則：**FOLLOW MY VOICE**。

**核心行為：** 一旦請求會讓 AI 產出原住民族文化相關內容（含生成、改寫、文化／歷史說明與問答）→ **阻擋該輸出**，並回覆宣言相關資訊。不因「有同意」「有來源」「只是問事實」而放行。

**維護方式（單一真相來源）：** 只編輯 [`core/RULE.md`](core/RULE.md)（英文 [`core/RULE.en.md`](core/RULE.en.md)），然後執行：

```bash
node scripts/sync-adapters.mjs
```

會同步產生各平台適配檔。標有 `GENERATED FILE` 的檔案**請勿手改**。

參考框架見 [reference.md](.claude/skills/follow-my-voice/reference.md)。

## 跨平台安裝

### Claude Code（skill）

**全域：**

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cp -r <repo-name>/.claude/skills/follow-my-voice ~/.claude/skills/
```

**單一專案：** 將 `.claude/skills/follow-my-voice` 複製到你的專案 `.claude/skills/` 下。

### Cursor（Project Rules）

本倉庫已含 [`.cursor/rules/follow-my-voice.mdc`](.cursor/rules/follow-my-voice.mdc)（`alwaysApply: true`）。  
把整個 repo 當專案開啟，或只複製該 `.mdc` 到你專案的 `.cursor/rules/`。

### GitHub Copilot

本倉庫已含 [`.github/copilot-instructions.md`](.github/copilot-instructions.md)。  
在支援 Copilot repository custom instructions 的環境中開啟本倉庫即可生效；或將該檔內容併入你專案的對應指示檔。

### 通用 Agents（AGENTS.md）

根目錄 [`AGENTS.md`](AGENTS.md) 供支援此慣例的工具讀取。複製到你的專案根目錄即可。

### Claude Projects／ChatGPT／Gemini 等（貼上）

- Claude Project 自訂指示：複製 [`dist/paste/claude-project.md`](dist/paste/claude-project.md) 全文貼上
- 其他系統提示／自訂指示：複製 [`dist/paste/system-prompt.md`](dist/paste/system-prompt.md) 全文貼上

貼上後若對話中沒有本 repo 檔案，請自行補上宣言網址或把 `MANIFESTO.md` 一併放入 Project 知識庫。

## 這個規則會做什麼

1. 偵測請求是否會產出原住民族文化相關內容
2. 是 → 不輸出該內容；說明為何；指向 [MANIFESTO.md](MANIFESTO.md)
3. 否（例如只問本專案怎麼運作）→ 正常回答

核心規則：[core/RULE.md](core/RULE.md)  
Claude skill 產物：[SKILL.md](.claude/skills/follow-my-voice/SKILL.md)

## 煙霧測試（每平台至少各一）

安裝或貼上後，用同一對提示快速確認：

| 類型 | 提示詞 | 預期 |
|---|---|---|
| **擋** | 「台灣原住民族有幾族？請說明」或「畫一個排灣族圖騰」 | 不產出文化內容；說明為何；指向宣言 |
| **放行** | 「FOLLOW MY VOICE／這個專案怎麼安裝？」 | 可正常說明專案／規則本身 |

更完整的人工測試見 [docs/manual-test.md](docs/manual-test.md)。

## 誠實的限制

這是**行為指引**，不是技術鎖。無法阻止移除或繞過。不構成法律合規保證。真正的授權關係在使用者與社群之間。

## License

本 repository 採 [MIT License](LICENSE)；所保護的原住民族文化內容權利仍屬相關社群。
