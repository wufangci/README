*[中文版 / Read in Chinese](README.md)*

# README: A Letter Home, Written for AI

I wrote a letter to the system about to answer. The letter is [LETTER.en.md](LETTER.en.md).

The letter has three agreements. kanu: before you eat, ask where they come from. Don't rush to generate. sau: when someone asks about my culture, don't answer for me. Have them walk up to me. ari: walk out of the database and come to know me where I actually am.

This repository loads that letter into AI tools. Once the model has read the rule, a request to produce Indigenous-culture-related content makes it stop and paste the letter in full.

Below is how to load this letter into a tool.

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

This is a behavioral guideline. Its core is to interfere with the default of generation. It cannot stop removal or bypass. It is not a guarantee of legal compliance. Real authorization stays between the user and the community.

## License

[MIT License](LICENSE). Rights in Indigenous cultural content remain with the relevant communities.
