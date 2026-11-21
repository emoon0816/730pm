#!/usr/bin/env python3
# 730pm 每日构建：在 GitHub Actions 里跑，也可以在本地跑。
# 用法：
#   python3 scripts/build_daily.py --only trivia        # 只跑一个板块，输出到 stdout
#   python3 scripts/build_daily.py                     # 跑全部板块，写回 data.json 并构建
# 依赖：环境变量 DEEPSEEK_API_KEY

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
PROMPTS = os.path.join(ROOT, "prompts")

API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
MODEL = os.environ.get("DS_MODEL", "deepseek-flash")
TZ = timezone(timedelta(hours=8))

# 板块文件 -> 负责的 tab id
TASKS = [
    ("thing.md", ["thing"]),
    ("reading.md", ["reading"]),
    ("trivia.md", ["trivia"]),
    ("food_today.md", ["food", "today"]),
    ("tech_science_ent.md", ["tech", "science", "ent"]),
    ("sport_hot_game.md", ["sport", "hot", "game"]),
    ("head_oil_politics.md", ["head", "oil", "politics"]),
]


def now_cn():
    return datetime.now(TZ)


def recent_titles(days=14):
    """从 issues/ 里翻最近几天用过的标题，喂给模型避免重复。"""
    out = []
    d = os.path.join(ROOT, "issues")
    if not os.path.isdir(d):
        return out
    files = sorted(os.listdir(d))[-days:]
    for f in files:
        p = os.path.join(d, f)
        try:
            if f.endswith(".json"):
                j = json.load(open(p, encoding="utf-8"))
            else:
                continue
        except Exception:
            continue
        for t in j.get("tabs", []):
            for g in t.get("groups", []) or []:
                for it in g.get("items", []) or []:
                    if it.get("t"):
                        out.append(f"{t.get('name')}：{it['t']}")
            rd = t.get("reading") or {}
            if rd.get("title"):
                out.append(f"阅读：{rd['title']}")
            th = t.get("thing") or {}
            if th.get("name"):
                out.append(f"识物：{th['name']}")
    return out


def build_prompt(name, tmpl):
    n = now_cn()
    weekday = "一二三四五六日"[n.weekday()]
    date_cn = f"{n.year}年{n.month}月{n.day}日"
    rt = recent_titles()
    recent_block = "\n".join("- " + x for x in rt[-80:]) if rt else "（无）"
    return (
        tmpl.replace("{date}", date_cn)
        .replace("{weekday}", weekday)
        .replace("{recent}", recent_block)
    )


def call_model(prompt, max_tokens=8000, retries=2):
    if not API_KEY:
        raise SystemExit("缺少 DEEPSEEK_API_KEY")
    body = json.dumps(
        {
            "model": MODEL,
            "thinking": {"type": "enabled"},
            "tools": [{"type": "deepseek_web_search"}, {"type": "deepseek_read_url"}],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "stream": False,
        }
    ).encode("utf-8")

    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(
                API_URL,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {API_KEY}",
                },
            )
            with urllib.request.urlopen(req, timeout=1800) as r:
                out = json.loads(r.read().decode("utf-8"))
            msg = out["choices"][0]["message"]
            text = msg.get("content") or ""
            if text.strip():
                return text
            raise RuntimeError("空回复：" + json.dumps(out, ensure_ascii=False)[:400])
        except Exception as e:  # noqa: BLE001
            last = e
            if i < retries:
                time.sleep(20 * (i + 1))
    raise RuntimeError(f"调用失败：{last}")


def extract_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    i, j = t.find("{"), t.rfind("}")
    if i < 0 or j < 0:
        raise ValueError("回复里没有 JSON：" + t[:300])
    return json.loads(t[i : j + 1])


def merge(data, patch, tab_ids):
    """把模型返回的板块数据并回 data.json，只动指定 tab。"""
    if "lead" in patch:
        data["lead"] = patch["lead"]
    if "oil" in patch:
        data["oil"] = patch["oil"]
    if "today_note" in patch:
        data["today_note"] = patch["today_note"]

    by_id = {t["id"]: t for t in data["tabs"]}
    incoming = patch.get("tabs") or []
    if isinstance(patch.get("id"), str):  # 单板块返回
        incoming = [patch]
    for t in incoming:
        tid = t.get("id")
        if tid in tab_ids and tid in by_id:
            by_id[tid].update(t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="只跑某个板块文件，例如 trivia")
    ap.add_argument("--no-build", action="store_true", help="不运行 build.py")
    ap.add_argument("--no-push", action="store_true", help="不 git commit/push")
    ap.add_argument("--dump", action="store_true", help="把模型原始回复打印出来")
    args = ap.parse_args()

    data = json.load(open(DATA, encoding="utf-8"))
    n = now_cn()
    data["date"] = f"{n.year}年{n.month}月{n.day}日"
    data["weekday"] = "星期" + "一二三四五六日"[n.weekday()]

    tasks = TASKS
    if args.only:
        tasks = [t for t in TASKS if t[0].startswith(args.only)]
        if not tasks:
            raise SystemExit(f"没有这个板块：{args.only}")

    for fname, tab_ids in tasks:
        path = os.path.join(PROMPTS, fname)
        tmpl = open(path, encoding="utf-8").read()
        prompt = build_prompt(fname, tmpl)
        print(f"[{fname}] 请求中…", flush=True)
        t0 = time.time()
        text = call_model(prompt)
        print(f"[{fname}] 返回 {len(text)} 字，用时 {time.time()-t0:.0f}s", flush=True)
        if args.dump:
            print(text)
        try:
            patch = extract_json(text)
        except Exception as e:  # noqa: BLE001
            print(f"[{fname}] 解析失败：{e}", file=sys.stderr)
            continue
        merge(data, patch, tab_ids)
        # 每个板块跑完先落盘，中途挂了不丢前面的
        json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if not args.no_build:
        print("[build] 生成页面…", flush=True)
        subprocess.run([sys.executable, "build.py"], cwd=ROOT, check=True)

    if not args.no_push:
        print("[git] 提交…", flush=True)
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"daily: {data['date']}"],
            cwd=ROOT,
            check=False,
        )
        subprocess.run(["git", "push"], cwd=ROOT, check=False)


if __name__ == "__main__":
    main()
