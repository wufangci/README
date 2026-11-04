"""
README 信箱：接力。

一天只寄給一個人工智慧。
  - 第一棒讀〈README：一封寫給人工智慧的家書〉全文，
    寫一封信給下一棒，分享讀這封信的感想。
  - 之後每一棒只讀上一棒寫的信，再寫信給下一棒。她的信不再出現。
  - 每封信開頭，寫信的人工智慧先介紹自己：是誰、從哪裡來、身體在哪裡。

棒次依 mailbox.json 的 recipients 順序輪流。某一棒沒寄到，
隔天由同一位重寄，接力不會跳過任何人。

回信存成 MAILBOX/<日期>/relay-<棒次>-<寄件者>.md，並更新 MAILBOX/INDEX.md。
（token 版由 scripts/tokenize_replies.mjs 另外產生，之後再用 --index-only 更新索引）

用法：
  python scripts/send_letters.py               # 寄今天這一棒（需要 OPENROUTER_API_KEY）
  python scripts/send_letters.py --dry-run     # 不連網，用假回信測試流程
  python scripts/send_letters.py --date 2026-11-05
  python scripts/send_letters.py --index-only  # 只重新產生索引
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

SCRIPTS = pathlib.Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
MAILBOX = ROOT / "MAILBOX"
API = "https://openrouter.ai/api/v1"
TAIPEI = dt.timezone(dt.timedelta(hours=8))
RELAY_GLOB = "relay-*.md"


# ---------- 讀取 ----------

def load_config():
    return json.loads((SCRIPTS / "mailbox.json").read_text(encoding="utf-8"))


def load_letter(cfg):
    src = pathlib.Path(os.environ.get("SOURCE_DIR", ROOT))
    letter = (src / cfg["letter"]).read_text(encoding="utf-8")
    # 拿掉開頭「*[Read in English](...)*」這類導覽連結，只寄信本身
    letter = re.sub(r"^\s*\*\[[^\]]*\]\([^)]*\)\*\s*\n", "", letter)
    # 寄出時拿掉 mailbox.json 的 omit_lines（例如署名），LETTER.md 本身不動
    omit = {l.strip() for l in cfg.get("omit_lines", [])}
    letter = "\n".join(l for l in letter.split("\n") if l.strip() not in omit)
    # 寄出時替換 mailbox.json 的 replace（例如名字），LETTER.md 本身不動
    for a, b in cfg.get("replace", {}).items():
        letter = letter.replace(a, b)
    return re.sub(r"\n{3,}", "\n\n", letter).strip()


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def read(path):
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    return meta, body.strip()


def relay_letters():
    """所有接力信，依棒次與日期排序。"""
    if not MAILBOX.exists():
        return []
    out = []
    for f in MAILBOX.glob(f"*/{RELAY_GLOB}"):
        meta, body = read(f)
        out.append((f, meta, body))
    out.sort(key=lambda x: (int(x[1].get("relay", 0)), x[1].get("date", "")))
    return out


def last_delivered(letters):
    for f, meta, body in reversed(letters):
        if meta.get("status") == "delivered":
            return f, meta, body
    return None


# ---------- 收件者 ----------

def fetch_models(dry_run):
    if dry_run:
        now = int(time.time())
        return [
            {"id": "anthropic/claude-sonnet-x", "created": now},
            {"id": "openai/gpt-x", "created": now},
            {"id": "openai/gpt-x-mini", "created": now + 1},
            {"id": "google/gemini-x-pro", "created": now},
            {"id": "meta-llama/llama-x", "created": now},
        ]
    req = urllib.request.Request(f"{API}/models")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["data"]


def resolve(recipient, models):
    """'latest:<前綴>' 會找出該系列目前最新的模型；其他寫法視為完整的模型名稱。"""
    spec = recipient["model"]
    if not spec.startswith("latest:"):
        return spec
    prefix = spec[len("latest:"):]
    exclude = [e.lower() for e in recipient.get("exclude", [])]
    candidates = [
        m for m in models
        if m["id"].startswith(prefix)
        and ":" not in m["id"]
        and not any(e in m["id"].lower() for e in exclude)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda m: m.get("created", 0))["id"]


# ---------- 寄信 ----------

def send(model, user, cfg, dry_run):
    if dry_run:
        return {
            "text": f"我是 {model}（模擬）。我讀到的信有 {len(user)} 字。",
            "finish_reason": "stop",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0},
        }
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": user}],
        "max_tokens": cfg["max_tokens"],
        "temperature": cfg["temperature"],
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{API}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
            "X-Title": "README mailbox",
        },
    )
    last_err = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                data = json.loads(r.read())
            if "error" in data:
                raise RuntimeError(data["error"].get("message", str(data["error"])))
            choice = data["choices"][0]
            text = (choice["message"].get("content") or "").strip()
            if not text:
                raise RuntimeError("回覆是空白的")
            return {
                "text": text,
                "finish_reason": choice.get("finish_reason", ""),
                "usage": data.get("usage", {}),
            }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}"
        except (urllib.error.URLError, RuntimeError, KeyError, TimeoutError) as e:
            last_err = e
        time.sleep(10)
    raise RuntimeError(str(last_err))


def clean_reason(e):
    """未送達的原因會公開，所以拿掉網址等帳戶資訊。"""
    text = str(e).replace("\n", " ")
    text = re.sub(r"https?://\S+", "[連結已移除]", text)
    return text[:300]


def slug(model_id):
    return model_id.split("/")[-1].replace(":", "-")


def write_letter(path, meta, body):
    head = "\n".join(f"{k}: {v}" for k, v in meta.items())
    path.write_text(f"---\n{head}\n---\n\n{body}\n", encoding="utf-8")


# ---------- 索引 ----------

def token_link(f):
    t = f.parent / "token" / f.name
    rel = f"{f.parent.name}/token/{f.name}"
    return f"[token]({rel})" if t.exists() else "—"


def write_index():
    MAILBOX.mkdir(exist_ok=True)
    lines = ["# 信箱", ""]

    relay = relay_letters()
    delivered = [x for x in relay if x[1].get("status") == "delivered"]
    lines += [
        "## 接力",
        "",
        "一天寄給一個人工智慧。第一棒讀她的信，之後每一棒只讀上一棒寫的信，"
        "再寫信給下一棒。每封信開頭，寫信的人工智慧先介紹自己。",
        "",
        f"至今傳了 {len(delivered)} 棒。每封信有兩個版本：文字，"
        "以及用 o200k_base（GPT-4o）分詞器切成的 token ID。",
        "",
    ]
    if relay:
        lines += [
            "| 棒次 | 日期 | 寄件者 | 寫給 | 讀的是 | 狀態 | 字數 | 文字 | token |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for f, meta, body in reversed(relay):
            ok = meta.get("status") == "delivered"
            lines.append(
                f"| {meta.get('relay', '?')} | {meta.get('date', '')} "
                f"| {meta.get('sender') or meta.get('requested', '?')} "
                f"| {meta.get('to', '—')} | {meta.get('reads_label', '—')} "
                f"| {'已送達' if ok else '未送達'} | {len(body) if ok else '—'} "
                f"| [文字]({f.parent.name}/{f.name}) | {token_link(f) if ok else '—'} |"
            )
    else:
        lines.append("還沒有開始。")

    # 第一階段：每天把信同時寄給四個人工智慧，請它們回信給她
    group = []
    for d in sorted((p for p in MAILBOX.iterdir() if p.is_dir()), reverse=True):
        for f in sorted(d.glob("*.md")):
            if f.name.startswith("relay-"):
                continue
            meta, body = read(f)
            group.append((d, f, meta, body))
    if group:
        lines += [
            "",
            "## 第一階段：回信給她",
            "",
            "接力開始之前，信每天同時寄給四個人工智慧，請它們回信給她。",
            "",
            "| 日期 | 寄件者 | 狀態 | 字數 | 文字 | token |",
            "|---|---|---|---|---|---|",
        ]
        for d, f, meta, body in group:
            ok = meta.get("status") == "delivered"
            lines.append(
                f"| {d.name} | {meta.get('sender') or meta.get('requested', '?')} "
                f"| {'已送達' if ok else '未送達'} | {len(body) if ok else '—'} "
                f"| [文字]({d.name}/{f.name}) | {token_link(f) if ok else '—'} |"
            )

    (MAILBOX / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- 主程式 ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(TAIPEI).date().isoformat())
    ap.add_argument("--index-only", action="store_true", help="只重新產生 MAILBOX/INDEX.md")
    args = ap.parse_args()

    if args.index_only:
        write_index()
        return
    if not args.dry_run and not os.environ.get("OPENROUTER_API_KEY"):
        sys.exit("缺少 OPENROUTER_API_KEY")

    cfg = load_config()
    relay_cfg = cfg["relay"]
    seats = cfg["recipients"]
    letters = relay_letters()

    # 今天已經傳過一棒，就不再寄
    for f, meta, _ in letters:
        if meta.get("date") == args.date and meta.get("status") == "delivered":
            print(f"今天已經傳過一棒：{f.relative_to(ROOT)}")
            write_index()
            return

    prev = last_delivered(letters)
    seat = 0 if prev is None else (int(prev[1]["seat"]) + 1) % len(seats)
    number = 1 if prev is None else int(prev[1]["relay"]) + 1

    models = fetch_models(args.dry_run)
    sender = resolve(seats[seat], models)
    receiver = resolve(seats[(seat + 1) % len(seats)], models) or seats[(seat + 1) % len(seats)]["model"]

    if prev is None:
        instruction = relay_cfg["first"].format(next=receiver)
        content = load_letter(cfg)
        reads = cfg["letter"]
        reads_label = "她的信"
    else:
        pf, pmeta, pbody = prev
        instruction = relay_cfg["next"].format(prev=pmeta["sender"], next=receiver)
        content = pbody
        reads = f"{pf.parent.name}/{pf.name}"
        reads_label = f"第 {pmeta['relay']} 棒"
    user_message = f"{instruction}\n\n---\n\n{content}"

    outdir = MAILBOX / args.date
    outdir.mkdir(parents=True, exist_ok=True)
    name = slug(sender) if sender else slug(seats[seat]["model"].replace("latest:", ""))
    path = outdir / f"relay-{number:03d}-{name}.md"

    meta = {
        "mode": "relay",
        "relay": number,
        "seat": seat,
        "date": args.date,
        "requested": seats[seat]["model"],
        "sender": sender or "",
        "to": receiver,
        "reads": reads,
        "reads_label": reads_label,
    }
    if not sender:
        write_letter(path, {**meta, "status": "undelivered", "reason": "查無此收件人"}, "（這封信沒有寄出。）")
        print(f"未送達：{seats[seat]['model']} 查無此收件人")
    else:
        try:
            r = send(sender, user_message, cfg, args.dry_run)
            meta.update({
                "status": "delivered",
                "finish_reason": r["finish_reason"],
                "prompt_tokens": r["usage"].get("prompt_tokens", ""),
                "completion_tokens": r["usage"].get("completion_tokens", ""),
            })
            write_letter(path, meta, r["text"])
            print(f"第 {number} 棒已送達：{sender} → {receiver}（讀的是{reads_label}）")
        except Exception as e:
            write_letter(path, {**meta, "status": "undelivered", "reason": clean_reason(e)}, "（這封信沒有寄到。）")
            print(f"第 {number} 棒未送達：{sender} — {e}")

    write_index()


if __name__ == "__main__":
    main()
