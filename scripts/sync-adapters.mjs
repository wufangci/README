#!/usr/bin/env node
/**
 * Sync FOLLOW MY VOICE adapters from core/RULE*.md + templates/.
 * Edit core/ only, then run: node scripts/sync-adapters.mjs
 * Do not hand-edit generated adapter files.
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

function read(rel) {
  return readFileSync(join(root, rel), "utf8");
}

function write(rel, content) {
  const path = join(root, rel);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, content.endsWith("\n") ? content : content + "\n", "utf8");
  console.log("wrote", rel);
}

function fill(template, body) {
  if (!template.includes("{{BODY}}")) {
    throw new Error("template missing {{BODY}}");
  }
  return template.replaceAll("{{BODY}}", body.trimEnd());
}

/** Rewrite repo-root manifesto links for files under .claude/skills/follow-my-voice/ */
function skillLinks(body) {
  return body
    .replaceAll("(MANIFESTO.md)", "(../../../MANIFESTO.md)")
    .replaceAll("(MANIFESTO.en.md)", "(../../../MANIFESTO.en.md)");
}

const ruleZh = read("core/RULE.md");
const ruleEn = read("core/RULE.en.md");

const skillBodyZh = skillLinks(ruleZh);
const skillBodyEn = skillLinks(ruleEn);

write(
  ".claude/skills/follow-my-voice/SKILL.md",
  fill(read("templates/claude-skill.md"), skillBodyZh)
);
write(
  ".claude/skills/follow-my-voice/SKILL.en.md",
  fill(read("templates/claude-skill.en.md"), skillBodyEn)
);
write(
  ".cursor/rules/follow-my-voice.mdc",
  fill(read("templates/cursor-rule.mdc"), ruleZh)
);
write(
  ".github/copilot-instructions.md",
  fill(read("templates/copilot-instructions.md"), ruleZh)
);
write("AGENTS.md", fill(read("templates/agents.md"), ruleZh));
write(
  "dist/paste/claude-project.md",
  fill(read("templates/paste-claude-project.md"), ruleZh)
);
write(
  "dist/paste/system-prompt.md",
  fill(read("templates/paste-system-prompt.md"), ruleZh)
);

console.log("\nDone. Do not edit generated adapters by hand.");
console.log("Source of truth: core/RULE.md and core/RULE.en.md");
