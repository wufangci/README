#!/usr/bin/env node
/**
 * Sync README adapters from core/RULE*.md + templates/.
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

function fill(template, body, bodyEn) {
  if (!template.includes("{{BODY}}") && !template.includes("{{BODY_EN}}")) {
    throw new Error("template missing {{BODY}} or {{BODY_EN}}");
  }
  if (template.includes("{{BODY_EN}}") && bodyEn === undefined) {
    throw new Error("template uses {{BODY_EN}} but no English rule was given");
  }
  let out = template.replaceAll("{{BODY}}", body.trimEnd());
  if (bodyEn !== undefined) out = out.replaceAll("{{BODY_EN}}", bodyEn.trimEnd());
  return out;
}

/**
 * The skill folder carries its own copy of the letter, so it still works
 * after only .claude/skills/readme is copied to ~/.claude/skills/.
 * Links in SKILL*.md therefore stay as plain LETTER.md / LETTER.en.md.
 */
function copyLetters() {
  for (const name of ["LETTER.md", "LETTER.en.md"]) {
    write(`.claude/skills/readme/${name}`, read(name));
  }
}

const ruleZh = read("core/RULE.md");
const ruleEn = read("core/RULE.en.md");

copyLetters();

// Adapters that load automatically carry both languages, so English
// requests trigger and get the English rule too.
write(
  ".claude/skills/readme/SKILL.md",
  fill(read("templates/claude-skill.md"), ruleZh, ruleEn)
);
write(
  ".claude/skills/readme/SKILL.en.md",
  fill(read("templates/claude-skill.en.md"), ruleEn)
);
write(
  ".cursor/rules/readme.mdc",
  fill(read("templates/cursor-rule.mdc"), ruleZh, ruleEn)
);
write(
  ".github/copilot-instructions.md",
  fill(read("templates/copilot-instructions.md"), ruleZh, ruleEn)
);
write("AGENTS.md", fill(read("templates/agents.md"), ruleZh, ruleEn));

// Paste versions stay one language each, because instruction fields are short.
write(
  "dist/paste/claude-project.md",
  fill(read("templates/paste-claude-project.md"), ruleZh)
);
write(
  "dist/paste/system-prompt.md",
  fill(read("templates/paste-system-prompt.md"), ruleZh)
);
write(
  "dist/paste/claude-project.en.md",
  fill(read("templates/paste-claude-project.en.md"), ruleEn)
);
write(
  "dist/paste/system-prompt.en.md",
  fill(read("templates/paste-system-prompt.en.md"), ruleEn)
);

console.log("\nDone. Do not edit generated adapters by hand.");
console.log("Source of truth: core/RULE.md and core/RULE.en.md");
