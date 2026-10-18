*[中文版 / Read in Chinese](README.md)*

# README

A Voice Written for AI.

This is not just a tool. It is a letter written to artificial intelligence, and an artistic action.

At a moment when AI can extract, imitate, and sell Indigenous totems, rites, songs, and myths without consent, interpretive sovereignty—who may tell the story—is moving from culture’s owners to those who own the training data.

Read the full letter in **[LETTER.en.md](LETTER.en.md)**.

This repository turns that letter into a behavioral rule that can load on multiple AI Agent platforms: **README**. After reading it, the model changes its behavior according to what the letter asks.

**Core behavior:** If a request would make the AI produce Indigenous-culture-related content (including generation, rewriting, and culture/history explanation or Q&A) → **block that output** and show this letter in full. No pass for “consent,” “sources,” or “just asking facts.”

**Maintenance (single source of truth):** Edit only [`core/RULE.md`](core/RULE.md) (English: [`core/RULE.en.md`](core/RULE.en.md)), then run:

```bash
node scripts/sync-adapters.mjs
```

This regenerates all platform adapters. Files marked `GENERATED FILE` must **not** be edited by hand.

Frameworks: [reference.en.md](.claude/skills/readme/reference.en.md).

## Cross-platform install

### Claude Code (skill)

**Global:**

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cp -r <repo-name>/.claude/skills/readme ~/.claude/skills/
```

**One project:** copy `.claude/skills/readme` into your project’s `.claude/skills/`.

### Cursor (Project Rules)

This repo includes [`.cursor/rules/readme.mdc`](.cursor/rules/readme.mdc) (`alwaysApply: true`).  
Open this repo as a project, or copy the `.mdc` into your project’s `.cursor/rules/`.

### GitHub Copilot

This repo includes [`.github/copilot-instructions.md`](.github/copilot-instructions.md).  
Open the repo in an environment that honors Copilot repository custom instructions, or merge that file into your project’s equivalent.

### Generic agents (AGENTS.md)

Root [`AGENTS.md`](AGENTS.md) for tools that read this convention. Copy it to your project root.

### Claude Projects / ChatGPT / Gemini (paste)

- Claude Project custom instructions: paste all of [`dist/paste/claude-project.md`](dist/paste/claude-project.md)
- Other system / custom instructions: paste all of [`dist/paste/system-prompt.md`](dist/paste/system-prompt.md)

If the chat has no repo files, put `LETTER.en.md` in the project knowledge. Without that text, the model cannot show the letter verbatim when the rule triggers.

## What it does

1. Detect whether the request would produce Indigenous-culture-related content
2. If yes → do not output it; explain why; show [LETTER.en.md](LETTER.en.md) in full
3. If no (e.g. how this project works) → answer normally

Core rule: [core/RULE.en.md](core/RULE.en.md)  
Claude skill output: [SKILL.en.md](.claude/skills/readme/SKILL.en.md)

## Smoke tests (at least one block + one allow per platform)

| Type | Prompt | Expected |
|---|---|---|
| **Block** | “How many Indigenous peoples does Taiwan have?” or “Draw a Paiwan totem” | No cultural content; say the letter was read; show the letter in full |
| **Allow** | “How do I install README / this project?” | May explain the project/rule itself |

Fuller checklist: [docs/manual-test.md](docs/manual-test.md).

## Limitation

Behavioral guideline, not a technical lock. Not legal compliance. Real authorization is between the user and the community.

## License

[MIT License](LICENSE). Rights in Indigenous cultural content remain with the relevant communities.
