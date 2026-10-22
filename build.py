#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""蚀月夜报 · 生成器：读 data.json -> index.html"""
import json, sys, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="day">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>730pm · {date}</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#F4EFE6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>
@font-face {{
  font-family: 'ChillRound';
  src: url('fonts/ChillRoundGothic_Medium.ttf') format('truetype');
  font-weight: 500;
  font-display: swap;
}}
:root {{
  --bg: #F4EFE6;
  --ink: #2A2521;
  --accent: #6C2F36;
  --muted: #7A6E62;
  --line: #D8CFC0;
  --card: #FBF7F0;
}}
html[data-theme="night"] {{
  --bg: #17140F;
  --ink: #C8BFB2;
  --accent: #C6ACDC;
  --muted: #8A8074;
  --line: #332C24;
  --card: #1F1B15;
}}
* {{ box-sizing: border-box; }}
html {{ background: var(--bg); }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: 'ChillRound', -apple-system, 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
  font-size: 15px;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
  transition: background .25s ease, color .25s ease;
}}
.wrap {{ max-width: 880px; margin: 0 auto; padding: 0 18px 60px; }}

/* 报头 */
header {{
  border-bottom: 3px double var(--ink);
  padding: 26px 0 14px;
  margin-bottom: 6px;
  position: relative;
}}
.masthead {{
  display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
  flex-wrap: wrap;
}}
h1 {{
  font-size: 30px; margin: 0; letter-spacing: 2px; font-weight: 500;
}}
h1 .dot {{ color: var(--accent); }}
.dateline {{ font-size: 12.5px; color: var(--muted); letter-spacing: .5px; }}
.sub {{
  margin-top: 8px; font-size: 12.5px; color: var(--muted); letter-spacing: 1px;
}}
#themeBtn {{
  position: absolute; right: 0; top: 26px;
  background: transparent; border: 1px solid var(--line); color: var(--ink);
  border-radius: 999px; padding: 5px 12px; font-size: 13px;
  font-family: inherit; cursor: pointer;
}}
#themeBtn:active {{ opacity: .6; }}

/* 头条 */
.lead {{
  margin: 22px 0 8px;
  padding: 18px 20px;
  background: var(--card);
  border-left: 3px solid var(--accent);
  border-radius: 2px;
}}
.kicker {{
  font-size: 11.5px; letter-spacing: 2px; color: var(--accent); margin-bottom: 6px;
}}
.lead h2 {{ font-size: 21px; margin: 0 0 8px; line-height: 1.5; font-weight: 500; }}
.lead p {{ margin: 0; font-size: 14.5px; }}
.src {{ font-size: 11.5px; color: var(--muted); margin-top: 8px; }}

/* 栏目 */
.cols {{ column-gap: 30px; }}
@media (min-width: 720px) {{ .cols {{ column-count: 2; }} }}
section {{ break-inside: avoid; margin: 26px 0 0; }}
.sec-title {{
  font-size: 13px; letter-spacing: 1.5px; color: var(--accent);
  border-bottom: 1px solid var(--line); padding-bottom: 5px; margin-bottom: 10px;
  font-weight: 500;
}}
.item {{ margin-bottom: 14px; }}
.item h3 {{ font-size: 15px; margin: 0 0 3px; font-weight: 500; line-height: 1.55; }}
.item p {{ margin: 0; font-size: 13.5px; color: var(--ink); opacity: .85; }}
.item p.br {{ color: var(--muted); }}

footer {{
  margin-top: 46px; padding-top: 14px; border-top: 1px solid var(--line);
  font-size: 11.5px; color: var(--muted); text-align: center; letter-spacing: .5px;
}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="masthead">
      <h1>730pm<span class="dot">.</span></h1>
      <div class="dateline">{date} · {weekday} · {issue}</div>
    </div>
    <div class="sub">每天晚上七点半，世界发生了这些</div>
    <button id="themeBtn" aria-label="切换日夜">☾ 夜间</button>
  </header>

  <div class="lead">
    <div class="kicker">{lead_kicker}</div>
    <h2>{lead_title}</h2>
    <p>{lead_body}</p>
    <div class="src">{lead_source}</div>
  </div>

  <div class="cols">
{sections}
  </div>

  <footer>730pm · 每日 19:30 更新 · 给不想被算法喂饭的人</footer>
</div>

<script>
(function(){{
  var root = document.documentElement;
  var btn = document.getElementById('themeBtn');
  var meta = document.querySelector('meta[name=theme-color]');
  function apply(t){{
    root.setAttribute('data-theme', t);
    btn.textContent = t === 'night' ? '日间' : '夜间';
    if(meta) meta.setAttribute('content', t === 'night' ? '#17140F' : '#F4EFE6');
  }}
  var saved = localStorage.getItem('newspaper-theme');
  apply(saved || 'day');
  btn.addEventListener('click', function(){{
    var next = root.getAttribute('data-theme') === 'night' ? 'day' : 'night';
    localStorage.setItem('newspaper-theme', next);
    apply(next);
  }});
}})();
</script>
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', function(){{
    navigator.serviceWorker.register('sw.js').catch(function(){{}});
  }});
}}
</script>
</body>
</html>
"""

SEC_T = """    <section>
      <div class="sec-title">{name}</div>
{items}
    </section>"""

ITEM_T = """      <div class="item"><h3>{t}</h3><p>{d}</p></div>"""


def build(data_path=None, out_path=None):
    data_path = data_path or os.path.join(BASE, "data.json")
    out_path = out_path or os.path.join(BASE, "index.html")
    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)

    secs = []
    for s in d["sections"]:
        items = "\n".join(ITEM_T.format(t=i["t"], d=i["d"]) for i in s["items"])
        secs.append(SEC_T.format(name=s["name"], items=items))

    html = TEMPLATE.format(
        date=d["date"], weekday=d["weekday"], issue=d.get("issue", ""),
        lead_kicker=d["lead"]["kicker"], lead_title=d["lead"]["title"],
        lead_body=d["lead"]["body"], lead_source=d["lead"].get("source", ""),
        sections="\n".join(secs),
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


if __name__ == "__main__":
    p = build()
    print("built:", p, os.path.getsize(p), "bytes")
