*[中文版 / Read in Chinese](README.md)*

# FOLLOW MY VOICE

This is not just a tool. It is an artistic action and a declaration.

At a moment when AI can extract, imitate, and sell Indigenous totems, rites, songs, and myths without consent, interpretive sovereignty—who may tell the story—is moving from culture’s owners to those who own the training data.

Read the full position in **[MANIFESTO.en.md](MANIFESTO.en.md)**.

This repository turns the declaration into a working [Claude Code](https://claude.com/claude-code) skill: `follow-my-voice`.

**Core behavior:** If a request would make the AI produce Indigenous-culture-related content (including generation, rewriting, and culture/history explanation or Q&A) → **block that output** and reply with manifesto information. No pass for “consent,” “sources,” or “just asking facts.”

Frameworks: [reference.en.md](.claude/skills/follow-my-voice/reference.en.md).

## Install

**Option 1: personal (global)**

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cp -r <repo-name>/.claude/skills/follow-my-voice ~/.claude/skills/
```

**Option 2: one project**

```bash
cp -r <repo-name>/.claude/skills/follow-my-voice <your-project>/.claude/skills/
```

## What it does

1. Detect whether the request would produce Indigenous-culture-related content
2. If yes → do not output it; explain why; point to [MANIFESTO.en.md](MANIFESTO.en.md)
3. If no (e.g. how this project works) → answer normally

Rules: [SKILL.en.md](.claude/skills/follow-my-voice/SKILL.en.md)

## Limitation

Behavioral guideline, not a technical lock. Not legal compliance. Real authorization is between the user and the community.

## License

[MIT License](LICENSE). Rights in Indigenous cultural content remain with the relevant communities.
