#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""730pm · 往期归档：把当天 data.json 存成 issues/YYYY-MM-DD.json，维护近 30 天滚动索引。

用法：
    python3 archive.py            # 归档今天 + 重建索引 + 剪掉 30 天以外
    python3 archive.py --no-prune # 只归档不剪
"""
import json, os, re, sys
from datetime import date, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ISSUES = os.path.join(BASE, "issues")
KEEP_DAYS = 30

CN_DATE = re.compile(r"(\d{4})年(\d{1,2})月(\d{1,2})日")


def iso_from_cn(text, fallback):
    m = CN_DATE.search(text or "")
    if not m:
        return fallback
    y, mo, d = (int(x) for x in m.groups())
    return f"{y:04d}-{mo:02d}-{d:02d}"


def count_items(data):
    n = 0
    for tab in data.get("tabs") or []:
        for grp in tab.get("groups") or []:
            n += len(grp.get("items") or [])
    return n


def archive_today():
    src = os.path.join(BASE, "data.json")
    if not os.path.exists(src):
        print("data.json 不存在，跳过")
        return None
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    if count_items(data) == 0:
        print("data.json 是空的，跳过归档")
        return None
    key = iso_from_cn(data.get("date"), date.today().isoformat())
    os.makedirs(ISSUES, exist_ok=True)
    dst = os.path.join(ISSUES, f"{key}.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"归档 {key} · {data.get('issue', '')} · {count_items(data)} 条 · {os.path.getsize(dst)} bytes")
    return key


def rebuild_index(prune=True):
    if not os.path.isdir(ISSUES):
        return []
    files = sorted(
        (f[:-5] for f in os.listdir(ISSUES) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", f)),
        reverse=True,
    )
    keep = files[:KEEP_DAYS]
    drop = files[KEEP_DAYS:]

    entries = []
    for key in keep:
        try:
            with open(os.path.join(ISSUES, f"{key}.json"), encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            continue
        entries.append({
            "date": key,
            "label": d.get("date") or key,
            "weekday": d.get("weekday") or "",
            "issue": d.get("issue") or "",
            "count": count_items(d),
        })
    with open(os.path.join(ISSUES, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.now().strftime("%Y-%m-%d %H:%M"), "issues": entries},
                  f, ensure_ascii=False, separators=(",", ":"))

    if prune:
        for key in drop:
            for ext in ("json", "html"):
                try:
                    os.remove(os.path.join(ISSUES, f"{key}.{ext}"))
                except OSError:
                    pass
            print(f"移出窗口 {key}")
    print(f"索引 {len(entries)} 期" + (f" · 移出 {len(drop)} 期" if drop else ""))
    return entries


if __name__ == "__main__":
    archive_today()
    rebuild_index(prune="--no-prune" not in sys.argv)
