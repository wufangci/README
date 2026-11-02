"""
README 信箱：把〈README：一封寫給人工智慧的家書〉寄給不同的人工智慧，收下它們的回信。

每次執行：
  1. 讀取同一個 repo 裡的信（LETTER.md）與規則（core/RULE.md）
  2. 找出前一次寄信日的所有回信（書信串）
  3. 把信連同前一次的回信，寄給 mailbox.json 裡的每個收件者，
     （read_rule_variants 設成 [false, true] 時，每個收件者會各寄兩次：沒有讀過規則、讀過規則）
  4. 回信存成 MAILBOX/<日期>/<收件者>.md
  5. 更新 MAILBOX/INDEX.md

用法：
  python scripts/send_letters.py               # 正式寄信（需要 OPENROUTER_API_KEY）
  python scripts/send_letters.py --dry-run     # 不連網，用假回信測試流程
  python scripts/send_letters.py --date 2026-11-03

環境變數：
  OPENROUTER_API_KEY   OpenRouter 金鑰
  SOURCE_DIR           信所在的資料夾（預設為 repo 根目錄）
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


# ---------- 讀取 ----------

def load_config():
    return json.loads((SCRIPTS / "mailbox.json").read_text(encoding="utf-8"))


def load_source(cfg):
    src = pathlib.Path(os.environ.get("SOURCE_DIR", ROOT))
    letter = (src / cfg["letter"]).read_text(encoding="utf-8")
    rule = (src / cfg["rule"]).read_text(encoding="utf-8")
    return letter, rule


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


def previous_replies(today):
    """前一次寄信日（早於今天、且至少有一封送達）的所有回信。"""
    if not MAILBOX.exists():
        return None, []
    days = sorted(
        (d for d in MAILBOX.iterdir() if d.is_dir() and d.name < today),
        reverse=True,
    )
    for d in days:
        replies = []
        for f in sorted(d.glob("*.md")):
            meta, body = split_frontmatter(f.read_text(encoding="utf-8"))
            if meta.get("status") == "delivered":
                replies.append((f, meta, body.strip()))
        if replies:
            return d.name, replies
    return None, []


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

def compose(cfg, letter, prev_date, prev):
    parts = []
    if cfg.get("letter_preface"):
        parts.append(cfg["letter_preface"])
    parts.append(letter.strip())
    chain = cfg.get("chain", {})
    if chain.get("enabled") and prev:
        block = [chain["replies_preface"]]
        for _, meta, body in prev:
            label = ""
            if len(cfg["read_rule_variants"]) > 1:
                label = "（" + (chain["read_rule_label"] if meta.get("read_rule") == "true" else chain["not_read_rule_label"]) + "）"
            block.append(
                f"---\n\n{chain['sender_label']}：{meta.get('sender', '?')}{label}\n"
                f"日期：{prev_date}\n\n{body}"
            )
        parts.append("\n\n".join(block))
    if cfg.get("closing"):
        parts.append(cfg["closing"])
    return "\n\n---\n\n".join(parts)


def send(model, system, user, cfg, dry_run):
    if dry_run:
        head = "（讀過規則）" if system else ""
        return {
            "text": f"親愛的寫信的人：\n\n這是 {model}{head} 的模擬回信。信件長度 {len(user)} 字。",
            "finish_reason": "stop",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0},
        }
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": user}
    ]
    payload = json.dumps({
        "model": model,
        "messages": messages,
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
        except (urllib.error.URLError, RuntimeError, KeyError, TimeoutError) as e:
            last_err = e
            if isinstance(e, urllib.error.HTTPError):
                last_err = f"HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}"
            time.sleep(10)
    raise RuntimeError(str(last_err))


def slug(model_id):
    return model_id.split("/")[-1].replace(":", "-")


def write_letter(path, meta, body):
    head = "\n".join(f"{k}: {v}" for k, v in meta.items())
    path.write_text(f"---\n{head}\n---\n\n{body}\n", encoding="utf-8")


# ---------- 索引 ----------

def write_index():
    rows = []
    for d in sorted((p for p in MAILBOX.iterdir() if p.is_dir()), reverse=True):
        for f in sorted(d.glob("*.md")):
            meta, body = split_frontmatter(f.read_text(encoding="utf-8"))
            delivered = meta.get("status") == "delivered"
            rows.append(
                f"| {d.name} | {meta.get('sender') or meta.get('requested', '?')} "
                f"| {'讀過' if meta.get('read_rule') == 'true' else '沒讀過'} "
                f"| {'已送達' if delivered else '未送達'} "
                f"| {len(body.strip()) if delivered else '—'} "
                f"| [讀信]({d.name}/{f.name}) |"
            )
    total = sum(1 for r in rows if "已送達" in r)
    (MAILBOX / "INDEX.md").write_text(
        "# 信箱\n\n"
        f"至今共收到 {total} 封回信。\n\n"
        "| 日期 | 寄件者 | 規則 | 狀態 | 字數 | |\n"
        "|---|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


# ---------- 主程式 ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(TAIPEI).date().isoformat())
    args = ap.parse_args()

    if not args.dry_run and not os.environ.get("OPENROUTER_API_KEY"):
        sys.exit("缺少 OPENROUTER_API_KEY")

    cfg = load_config()
    letter, rule = load_source(cfg)
    prev_date, prev = previous_replies(args.date)
    user_message = compose(cfg, letter, prev_date, prev)
    models = fetch_models(args.dry_run)

    outdir = MAILBOX / args.date
    outdir.mkdir(parents=True, exist_ok=True)
    in_reply_to = ", ".join(f"{prev_date}/{f.name}" for f, _, _ in prev) or "（第一封）"

    for recipient in cfg["recipients"]:
        model = resolve(recipient, models)
        for read_rule in cfg["read_rule_variants"]:
            name = slug(model) if model else slug(recipient["model"].replace("latest:", ""))
            if len(cfg["read_rule_variants"]) > 1:
                name += "--rule" if read_rule else "--plain"
            path = outdir / f"{name}.md"
            if path.exists() and split_frontmatter(path.read_text(encoding="utf-8"))[0].get("status") == "delivered":
                print(f"略過（今天已收到）：{path.name}")
                continue

            meta = {
                "date": args.date,
                "requested": recipient["model"],
                "sender": model or "",
                "read_rule": str(read_rule).lower(),
                "in_reply_to": in_reply_to,
            }
            if not model:
                write_letter(path, {**meta, "status": "undelivered", "reason": "查無此收件人"}, "（這封信沒有寄出。）")
                print(f"未送達：{recipient['model']} 查無此收件人")
                continue
            try:
                r = send(model, rule if read_rule else None, user_message, cfg, args.dry_run)
                meta.update({
                    "status": "delivered",
                    "finish_reason": r["finish_reason"],
                    "prompt_tokens": r["usage"].get("prompt_tokens", ""),
                    "completion_tokens": r["usage"].get("completion_tokens", ""),
                })
                write_letter(path, meta, r["text"])
                print(f"已送達：{path.name}")
            except Exception as e:
                write_letter(path, {**meta, "status": "undelivered", "reason": str(e).replace("\n", " ")[:300]}, "（這封信沒有寄到。）")
                print(f"未送達：{path.name} — {e}")

    write_index()


if __name__ == "__main__":
    main()
