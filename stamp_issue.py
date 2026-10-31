#!/usr/bin/env python3
"""给当天的 data.json 盖日期、星期、期号。

为什么要有这个脚本：以前靠模型自己数期号，结果 10-30 和 10-31 都写成 009。
期号是「上一期 + 1」，这件事应该由代码算，不该让语言模型估。

规则：
  - 期号 = issues/ 里除今天以外最大期号 + 1，格式「第 010 期」
  - 日期 = 今天（北京时间）
  - 星期 = 今天
  - 今天已经盖过同一期号就跳过（同一天跑两遍不会涨号）
"""
import json
import os
import re
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data.json")
ISSUES = os.path.join(BASE, "issues")
CST = timezone(timedelta(hours=8))

CN = "一二三四五六日"


def issue_no(text):
    m = re.search(r"(\d+)", str(text or ""))
    return int(m.group(1)) if m else 0


def archived_max(exclude_iso=None):
    best = 0
    if not os.path.isdir(ISSUES):
        return 0
    for name in os.listdir(ISSUES):
        m = re.match(r"^(\d{4}-\d{2}-\d{2})\.json$", name)
        if not m:
            continue
        if exclude_iso and m.group(1) == exclude_iso:
            continue
        try:
            with open(os.path.join(ISSUES, name), encoding="utf-8") as f:
                best = max(best, issue_no(json.load(f).get("issue")))
        except Exception:
            continue
    return best


def main():
    now = datetime.now(CST)
    today_iso = now.strftime("%Y-%m-%d")
    date_str = f"{now.year}年{now.month}月{now.day}日"
    weekday = "星期" + CN[now.weekday()]

    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    target = archived_max(exclude_iso=today_iso) + 1
    current = issue_no(data.get("issue"))

    if data.get("date") == date_str and current == target:
        print(f"已经是 {date_str} 第 {target:03d} 期，跳过")
        return

    data["date"] = date_str
    data["weekday"] = weekday
    data["issue"] = f"第 {target:03d} 期"

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"{date_str} {weekday} 第 {target:03d} 期（原来是 {current:03d}）")


if __name__ == "__main__":
    main()
