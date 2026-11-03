// 把信箱裡每一封回信切成 token，另外存一份只有 token ID 的版本。
//
//   MAILBOX/<日期>/<寄件者>.md         回信（文字，給人讀的）
//   MAILBOX/<日期>/token/<寄件者>.md   同一封回信的 token ID（給 AI 讀的）
//
// 分詞器：GPT-4o o200k_base（gpt-tokenizer 2.9.0），
// 和 readme-token-animation、readme-folded-letters 相同，ID 對得起來。
//
// ID 面的排法沿用折信 v10：只有數字；換行也是 token，照印它的 ID，
// 段落照樣換行；段落之間多出來的單獨換行 token 接在上一行行尾。
//
// 用法（在 repo 根目錄）：
//   npm install --no-save gpt-tokenizer@2.9.0
//   node scripts/tokenize_replies.mjs            # 只處理還沒有 token 版的回信
//   node scripts/tokenize_replies.mjs --force    # 全部重做

import fs from 'node:fs';
import path from 'node:path';
import { encode, decode } from 'gpt-tokenizer/encoding/o200k_base';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const MAILBOX = path.join(ROOT, 'MAILBOX');
const TOKEN_DIR = 'token';
const TOKENIZER = 'o200k_base（GPT-4o），gpt-tokenizer 2.9.0';
const force = process.argv.includes('--force');

function splitFrontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n\n?([\s\S]*)$/);
  if (!m) return [{}, text];
  const meta = {};
  for (const line of m[1].split('\n')) {
    const i = line.indexOf(':');
    if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return [meta, m[2]];
}

const newlines = (s) => (s.match(/\n/g) || []).length;
const isNewlineOnly = (s) => s.trim() === '' && s.includes('\n');

// token ID 排成 Markdown：ID 之間空一格；行尾用 `\` 強制換行，空一行是段落。
function layout(ids) {
  const strs = ids.map((id) => decode([id]));
  const lines = [];
  let line = [];
  let pending = 0;
  ids.forEach((id, i) => {
    line.push(String(id));
    pending += newlines(strs[i]);
    const next = strs[i + 1];
    if (pending > 0 && !(next !== undefined && isNewlineOnly(next))) {
      lines.push({ text: line.join(' '), paragraph: pending >= 2 });
      line = [];
      pending = 0;
    }
  });
  if (line.length) lines.push({ text: line.join(' '), paragraph: true });

  let out = '';
  lines.forEach((l, i) => {
    const last = i === lines.length - 1;
    out += l.text;
    if (last) out += '\n';
    else out += l.paragraph ? '\n\n' : '\\\n';
  });
  return out;
}

function* replyFiles(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== TOKEN_DIR) yield* replyFiles(p);
    } else if (entry.name.endsWith('.md') && entry.name !== 'INDEX.md') {
      yield p;
    }
  }
}

if (!fs.existsSync(MAILBOX)) process.exit(0);

let made = 0;
for (const file of replyFiles(MAILBOX)) {
  const [meta, body] = splitFrontmatter(fs.readFileSync(file, 'utf8'));
  if (meta.status !== 'delivered') continue;

  const out = path.join(path.dirname(file), TOKEN_DIR, path.basename(file));
  if (fs.existsSync(out) && !force) continue;

  const ids = encode(body.trim());
  const head = [
    `date: ${meta.date ?? ''}`,
    `sender: ${meta.sender ?? ''}`,
    `text: ../${path.basename(file)}`,
    `tokenizer: ${TOKENIZER}`,
    `tokens: ${ids.length}`,
  ].join('\n');

  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, `---\n${head}\n---\n\n${layout(ids)}`, 'utf8');
  console.log(`token 化：${path.relative(ROOT, out)}（${ids.length} tokens）`);
  made++;
}
if (!made) console.log('沒有新的回信需要 token 化');
