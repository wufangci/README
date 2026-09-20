*[Read in English](README.en.md)*

# 詮釋權宣言 / FOLLOW MY VOICE

這不只是一個工具，是一份藝術行動與宣言。

在AI技術得以無需同意就擷取、模仿、販售原住民族的圖騰、祭儀、歌謠與神話的此刻，詮釋權，也就是誰有資格說出這個故事，正從文化的主人手中悄悄轉移到訓練資料的擁有者手中。

完整的立場、控訴與宣告，請讀 **[MANIFESTO.md](MANIFESTO.md)**。

這份 repository 把宣言變成一個可運作的 [Claude Code](https://claude.com/claude-code) skill：`follow-my-voice`。

**核心行為：** 一旦請求會讓 AI 產出原住民族文化相關內容（含生成、改寫、文化／歷史說明與問答）→ **阻擋該輸出**，並回覆宣言相關資訊。不因「有同意」「有來源」「只是問事實」而放行。

參考框架見 [reference.md](.claude/skills/follow-my-voice/reference.md)。

## 安裝

**方法一：個人設定（全域）**

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cp -r <repo-name>/.claude/skills/follow-my-voice ~/.claude/skills/
```

**方法二：單一專案**

```bash
cp -r <repo-name>/.claude/skills/follow-my-voice <your-project>/.claude/skills/
```

安裝後會依 `SKILL.md` 的 `description` 自動觸發。

## 這個 skill 會做什麼

1. 偵測請求是否會產出原住民族文化相關內容
2. 是 → 不輸出該內容；說明為何；指向 [MANIFESTO.md](MANIFESTO.md)
3. 否（例如只問本專案怎麼運作）→ 正常回答

詳細規則：[SKILL.md](.claude/skills/follow-my-voice/SKILL.md)

## 誠實的限制

這是**行為指引**，不是技術鎖。無法阻止移除或繞過。不構成法律合規保證。真正的授權關係在使用者與社群之間。

## License

本 repository 採 [MIT License](LICENSE)；所保護的原住民族文化內容權利仍屬相關社群。
