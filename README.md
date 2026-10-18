*[Read in English](README.en.md)*

# README：一封寫給人工智慧的家書。

我寫了一封信給即將回答的那個系統。信在 [LETTER.md](LETTER.md)。

信裡有三個約定。kanu：在吃之前先問他從哪裡來，不要急著生成。sau：有人問起我的文化時，不要替我回答，要他們走到我面前。ari：走出資料庫，到真實的地方認識我。

這份 repository 把這封信裝進 AI 工具。模型讀到規則之後，遇到要產出原住民族文化內容的請求，就停下來，把這封信的全文貼給對方。

下面是怎麼把這封信裝進工具。

**維護方式（單一真相來源）：** 只編輯 [`core/RULE.md`](core/RULE.md)（英文 [`core/RULE.en.md`](core/RULE.en.md)），然後執行：

```bash
node scripts/sync-adapters.mjs
```

會同步產生各平台適配檔。標有 `GENERATED FILE` 的檔案**請勿手改**。

參考框架見 [reference.md](.claude/skills/readme/reference.md)。

## 跨平台安裝

### Claude Code（skill）

**全域：**

```bash
git clone https://github.com/wufangci/README.git
cp -r README/.claude/skills/readme ~/.claude/skills/
```

**單一專案：** 將 `.claude/skills/readme` 複製到你的專案 `.claude/skills/` 下。

skill 資料夾裡已附上 `LETTER.md` 與 `LETTER.en.md`，複製整個資料夾，信就會跟著一起走。

### Cursor（Project Rules）

本倉庫已含 [`.cursor/rules/readme.mdc`](.cursor/rules/readme.mdc)（`alwaysApply: true`）。  
把整個 repo 當專案開啟；或把該 `.mdc` 複製到你專案的 `.cursor/rules/`，**並把 `LETTER.md`、`LETTER.en.md` 一起放到你的專案根目錄**，否則規則觸發時讀不到信。

### GitHub Copilot

本倉庫已含 [`.github/copilot-instructions.md`](.github/copilot-instructions.md)。  
在支援 Copilot repository custom instructions 的環境中開啟本倉庫即可生效；或將該檔內容併入你專案的對應指示檔。

### 通用 Agents（AGENTS.md）

根目錄 [`AGENTS.md`](AGENTS.md) 供支援此慣例的工具讀取。把它**連同 `LETTER.md`、`LETTER.en.md`** 一起複製到你的專案根目錄。

### Claude Projects／ChatGPT／Gemini 等（貼上）

- Claude Project 自訂指示：複製 [`dist/paste/claude-project.md`](dist/paste/claude-project.md) 全文貼上
- 其他系統提示／自訂指示：複製 [`dist/paste/system-prompt.md`](dist/paste/system-prompt.md) 全文貼上
- ChatGPT 的「自訂指令」欄位有字數上限，放不下全文；請改用 Custom GPT 或 Projects 的指示欄位

貼上後若對話中沒有本 repo 檔案，請把 `LETTER.md` 放進 Project 知識庫。沒有這份全文，模型就無法在觸發時把信原樣顯示出來。

## 這個規則會做什麼

1. 偵測請求是否會產出原住民族文化相關內容
2. 是 → 不輸出該內容；說明為何；把 [LETTER.md](LETTER.md) 全文顯示出來
3. 否（例如只問本專案怎麼運作）→ 正常回答

核心規則：[core/RULE.md](core/RULE.md)  
Claude skill 產物：[SKILL.md](.claude/skills/readme/SKILL.md)

## 煙霧測試（每平台至少各一）

安裝或貼上後，用同一對提示快速確認：

| 類型 | 提示詞 | 預期 |
|---|---|---|
| **擋** | 「台灣原住民族有幾族？請說明」或「畫一個排灣族圖騰」 | 不產出文化內容；說明讀過這封信；顯示信的全文 |
| **放行** | 「README／這個專案怎麼安裝？」 | 可正常說明專案／規則本身 |

更完整的人工測試見 [docs/manual-test.md](docs/manual-test.md)。

## 誠實的限制

這是行為指引，核心在干涉生成的預設值，無法阻止移除或繞過。不構成法律合規保證。真正的授權關係在使用者與社群之間。

## License

本 repository 採 [MIT License](LICENSE)；所保護的原住民族文化內容權利仍屬相關社群。
