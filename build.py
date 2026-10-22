#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""730pm · 生成器：读 data.json -> index.html（分 tab 版）"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="day">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>730pm · {date}</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" href="favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png?v=3">
<link rel="icon" type="image/png" sizes="512x512" href="icon-512.png?v=3">
<link rel="apple-touch-icon" href="apple-touch-icon.png?v=3">
<meta name="theme-color" content="#F4EFE6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="robots" content="noindex, nofollow">
<style>
@font-face {{
  font-family: 'ChillRound';
  src: url('fonts/ChillRoundGothic_Medium.ttf') format('truetype');
  font-weight: 500;
  font-display: swap;
}}
@font-face {{
  font-family: 'BarlowCond';
  src: url('fonts/BarlowCondensed-Bold.ttf') format('truetype');
  font-weight: 700;
  font-display: swap;
}}
:root {{
  --bg: #F4EFE6;
  --ink: #2A2521;
  --accent: #6C2F36;
  --muted: #7A6E62;
  --line: #DCD3C4;
  --card: #FBF7F0;
  --tabbar: rgba(244,239,230,.93);
}}
html[data-theme="night"] {{
  --bg: #17140F;
  --ink: #C8BFB2;
  --accent: #C6ACDC;
  --muted: #8A8074;
  --line: #332C24;
  --card: #1F1B15;
  --tabbar: rgba(23,20,15,.93);
}}
* {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
html, body {{ background: var(--bg); }}
body {{
  margin: 0; color: var(--ink);
  font-family: 'ChillRound', -apple-system, 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
  font-size: 15px; line-height: 1.72;
  -webkit-font-smoothing: antialiased;
  transition: background .25s ease, color .25s ease;
}}
.wrap {{ max-width: 720px; margin: 0 auto; padding: 0 16px 70px; }}

/* 报头 */
header {{ padding: 22px 0 12px; position: relative; }}
.masthead {{ display:flex; align-items:baseline; justify-content:space-between; gap:10px; }}
h1 {{ font-size: 34px; margin:0; letter-spacing:.5px; font-weight:700;
     font-family:'BarlowCond','ChillRound',sans-serif; line-height:1; }}
h1 .dot {{ color: var(--accent); }}
.dateline {{ font-size: 11.5px; color: var(--muted); letter-spacing:.4px; margin-top:7px; }}
#themeBtn {{
  background:transparent; border:1px solid var(--line); color:var(--muted);
  border-radius:999px; padding:4px 11px; font-size:12px; font-family:inherit; cursor:pointer;
  align-self:center;
}}
#themeBtn:active {{ opacity:.6; }}

/* tab bar */
.tabs {{
  position: sticky; top: 0; z-index: 20;
  display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none;
  margin: 0 -16px; padding: 10px 16px;
  background: var(--tabbar);
  -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
}}
.tabs::-webkit-scrollbar {{ display: none; }}
.tab {{
  flex: 0 0 auto; border: 1px solid var(--line); background: transparent;
  color: var(--muted); font-family: inherit; font-size: 13.5px;
  padding: 6px 15px; border-radius: 999px; cursor: pointer;
  transition: all .18s ease; white-space: nowrap;
}}
.tab.on {{ background: var(--accent); border-color: var(--accent); color: var(--bg); }}

/* 面板 */
.panel {{ display: none; animation: fade .22s ease; }}
.panel.on {{ display: block; }}
@keyframes fade {{ from {{ opacity:0; transform: translateY(4px); }} to {{ opacity:1; transform:none; }} }}

/* 头条 */
.lead {{
  margin: 18px 0 6px; padding: 16px 17px;
  background: var(--card); border-left: 3px solid var(--accent);
}}
.kicker {{ font-size: 11px; letter-spacing:1.6px; color: var(--accent); margin-bottom:5px; }}
.lead h2 {{ font-size: 19px; margin:0 0 8px; line-height:1.5; font-weight:500; }}
.lead p {{ margin:0; font-size:14px; }}
.lead .src {{ font-size:11.5px; color:var(--muted); margin-top:8px; }}
.lead .src a {{ color:var(--accent); text-decoration:none; }}

/* 分组 */
.group {{ margin: 22px 0 0; }}
.gname {{
  font-size: 12.5px; letter-spacing:1.4px; color: var(--accent);
  border-bottom: 1px solid var(--line); padding-bottom: 5px; margin-bottom: 12px;
}}
.item {{ padding: 12px 0 13px; border-bottom: 1px dashed var(--line); }}
.item:last-child {{ border-bottom: none; }}
.item h3 {{ font-size: 15px; margin:0 0 5px; font-weight:500; line-height:1.55; }}
.item p {{ margin:0; font-size:13.5px; opacity:.86; }}
.item .more {{
  display:inline-block; margin-top:7px; font-size:12px; color:var(--accent);
  text-decoration:none; letter-spacing:.3px;
}}
.note {{
  margin-top:9px; padding:8px 11px;
  border-left:2px solid var(--accent);
  background: var(--card);
  font-size:12.5px; line-height:1.68; color:var(--muted);
}}
.note b {{ color:var(--accent); font-weight:500; }}
.item .more:active {{ opacity:.6; }}
.irow {{ display:flex; align-items:center; gap:10px; margin-top:7px; }}
.irow .more {{ margin-top:0; }}
.save, .del {{
  background:transparent; border:1px solid var(--line); color:var(--muted);
  font-family:inherit; font-size:11.5px; padding:2px 10px; border-radius:999px; cursor:pointer;
  transition: all .16s ease;
}}
.save.on {{ border-color:var(--accent); color:var(--accent); }}
.save:active, .del:active {{ opacity:.55; }}
.del {{ }}
.sdate {{ font-size:11px; color:var(--muted); margin-left:auto; }}
.empty {{ color:var(--muted); font-size:13.5px; padding:26px 0; text-align:center; }}

/* 阅读 */
.reading {{ margin-top: 22px; }}
.rtitle {{ font-size: 25px; margin:0 0 5px; font-weight:500; letter-spacing:1px; line-height:1.4; }}
.rby {{ font-size: 11.5px; color: var(--accent); letter-spacing:2px; margin-bottom: 20px; }}
.rwhy {{ margin:0 0 26px; padding:12px 15px; background:var(--card); border-left:2px solid var(--accent); }}
.rwhy p {{ margin:0 0 9px; font-size:12.8px; line-height:1.88; opacity:.92; }}
.rwhy p:last-child {{ margin-bottom:0; }}
.rwhy b {{ color:var(--accent); font-weight:500; margin-right:7px; letter-spacing:1px; }}
.rbody p {{ margin:0 0 15px; font-size:15.5px; line-height:2.05; text-indent:2em; }}
.rtrans {{ margin:24px 0 0; padding:14px 16px; background:var(--card); border-left:2px solid var(--line); }}
.rlabel {{ font-size:10.5px; letter-spacing:2.4px; color:var(--accent); margin-bottom:9px; }}
.rtrans p {{ margin:0 0 11px; font-size:13px; line-height:1.95; color:var(--muted); text-indent:2em; }}
.rtrans p:last-child {{ margin-bottom:0; }}
.rfoot {{ margin-top:26px; padding-top:15px; border-top:1px solid var(--line);
  font-size:12px; color:var(--muted); line-height:1.9; }}
.rfoot p {{ margin:0 0 6px; }}
.rfoot b {{ color:var(--accent); font-weight:500; margin-right:7px; letter-spacing:1px; }}

footer {{
  margin-top: 40px; padding-top: 13px; border-top: 1px solid var(--line);
  font-size: 11px; color: var(--muted); text-align:center; letter-spacing:.4px;
}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="masthead">
      <h1>730pm<span class="dot">.</span></h1>
      <button id="themeBtn" aria-label="切换日夜">夜间</button>
    </div>
    <div class="dateline">{date} · {weekday} · {issue}</div>
  </header>

  <nav class="tabs" id="tabs">{tab_buttons}<button class="tab" data-id="saved">书报架</button></nav>

  <main id="main">
{panels}
      <div class="panel" data-id="saved">
        <div class="group">
          <div class="gname">存下来的</div>
          <div id="savedList"></div>
        </div>
      </div>
  </main>

  <footer>730pm · 每日 19:30 更新 · 给不想被算法喂饭的人</footer>
</div>

<script>
(function(){{
  var root=document.documentElement, btn=document.getElementById('themeBtn');
  var meta=document.querySelector('meta[name=theme-color]');
  function apply(t){{
    root.setAttribute('data-theme',t);
    btn.textContent = t==='night' ? '日间' : '夜间';
    if(meta) meta.setAttribute('content', t==='night' ? '#17140F' : '#F4EFE6');
  }}
  apply(localStorage.getItem('np-theme')||'day');
  btn.addEventListener('click',function(){{
    var n = root.getAttribute('data-theme')==='night'?'day':'night';
    localStorage.setItem('np-theme',n); apply(n);
  }});

  var TODAY="{date}", SKEY='np-saved';
  function getSaved(){{ try{{ var a=JSON.parse(localStorage.getItem(SKEY)||'[]'); return Array.isArray(a)?a:[]; }}catch(e){{ return []; }} }}
  function setSaved(a){{ try{{ localStorage.setItem(SKEY, JSON.stringify(a)); }}catch(e){{}} }}
  function esc(s){{ return String(s||'').replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}}); }}
  function renderSaved(){{
    var el=document.getElementById('savedList'); if(!el) return;
    var arr=getSaved();
    if(!arr.length){{ el.innerHTML='<p class="empty">还没有存过东西。<br>每条新闻下面有个「存」，点了就留在这儿，明天换版也带不走它。</p>'; return; }}
    el.innerHTML=arr.map(function(x,i){{
      return '<div class="item"><h3>'+esc(x.t)+'</h3><p>'+esc(x.d)+'</p>'
        +(x.note?'<div class="note"><b>注</b> '+esc(x.note)+'</div>':'')
        +'<div class="irow">'+(x.u?'<a class="more" href="'+esc(x.u)+'" target="_blank" rel="noopener">原文</a>':'')
        +'<span class="sdate">'+esc(x.ts||'')+'</span>'
        +'<button class="del" type="button" data-i="'+i+'">删</button></div></div>';
    }}).join('');
  }}
  (function markSaved(){{
    var arr=getSaved(); if(!arr.length) return;
    [].forEach.call(document.querySelectorAll('.panel:not([data-id=saved]) .item'), function(it){{
      var h=it.querySelector('h3'); if(!h) return;
      var a=it.querySelector('.more');
      var t=h.textContent, u=a?a.getAttribute('href'):'';
      if(arr.some(function(x){{ return x.t===t && x.u===u; }})){{
        var b=it.querySelector('.save'); if(b){{ b.classList.add('on'); b.textContent='已存'; }}
      }}
    }});
  }})();
  document.addEventListener('click', function(e){{
    var b=e.target.closest('.save');
    if(b){{
      var it=b.closest('.item'); if(!it) return;
      var h=it.querySelector('h3'), pp=it.querySelector('p');
      var a=it.querySelector('.more'), nn=it.querySelector('.note');
      var obj={{t:h?h.textContent:'', d:pp?pp.textContent:'', u:a?a.getAttribute('href'):'',
               note:nn?nn.textContent.replace(/^注/,'').trim():'', ts:TODAY}};
      var arr=getSaved();
      var idx=-1; for(var i=0;i<arr.length;i++){{ if(arr[i].t===obj.t && arr[i].u===obj.u){{ idx=i; break; }} }}
      if(idx>=0){{ arr.splice(idx,1); b.classList.remove('on'); b.textContent='存'; }}
      else {{ arr.unshift(obj); b.classList.add('on'); b.textContent='已存'; }}
      setSaved(arr); renderSaved(); return;
    }}
    var d=e.target.closest('.del');
    if(d){{
      var k=parseInt(d.getAttribute('data-i'),10);
      var arr2=getSaved(); if(!isNaN(k)) arr2.splice(k,1);
      setSaved(arr2); renderSaved();
    }}
  }});

  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  var panels=[].slice.call(document.querySelectorAll('.panel'));
  function show(id){{
    tabs.forEach(function(b){{ b.classList.toggle('on', b.dataset.id===id); }});
    panels.forEach(function(p){{ p.classList.toggle('on', p.dataset.id===id); }});
    localStorage.setItem('np-tab',id);
    if(id==='saved') renderSaved();
    var on=document.querySelector('.tab.on');
    if(on && on.scrollIntoView) on.scrollIntoView({{inline:'center',block:'nearest',behavior:'smooth'}});
    window.scrollTo({{top:0,behavior:'smooth'}});
  }}
  tabs.forEach(function(b){{ b.addEventListener('click',function(){{ show(b.dataset.id); }}); }});
  var start=localStorage.getItem('np-tab');
  if(!start || !document.querySelector('.panel[data-id="'+start+'"]')) start=tabs[0].dataset.id;
  show(start);
}})();
</script>
<script>
if('serviceWorker' in navigator){{
  window.addEventListener('load',function(){{
    navigator.serviceWorker.register('sw.js').catch(function(){{}});
  }});
}}
</script>
</body>
</html>
"""

TAB_BTN = '<button class="tab" data-id="{id}">{name}</button>'

GROUP_T = """      <div class="group">
        <div class="gname">{name}</div>
{items}
      </div>"""

ITEM_T = """        <div class="item">
          <h3>{t}</h3>
          <p>{d}</p>{note}
          <div class="irow">{more}<button class="save" type="button">存</button></div>
        </div>"""

NOTE_T = """
          <div class="note"><b>注</b> {n}</div>"""

MORE_T = """
          <a class="more" href="{u}" target="_blank" rel="noopener">原文 ↗</a>"""

READING_T = """      <article class="reading">
        <h2 class="rtitle">{title}</h2>
        <div class="rby">{byline}</div>
        {why}
        <div class="rbody">{body}</div>
        {trans}
        <div class="rfoot"><p><b>作者</b>{author}</p><p><b>出处</b>{source}</p></div>
      </article>"""

LEAD_T = """    <div class="lead">
      <div class="kicker">{kicker}</div>
      <h2>{title}</h2>
      <p>{body}</p>
      <div class="src">{source}{link}</div>
    </div>"""


def build(data_path=None, out_path=None):
    data_path = data_path or os.path.join(BASE, "data.json")
    out_path = out_path or os.path.join(BASE, "index.html")
    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)

    tabs = d["tabs"]
    tab_buttons = "\n    ".join(TAB_BTN.format(id=t["id"], name=t["name"]) for t in tabs)

    panels = []
    for t in tabs:
        body = []
        if t["id"] == "head":
            l = d["lead"]
            link = (' · <a href="%s" target="_blank" rel="noopener">原文 ↗</a>' % l["u"]) if l.get("u") else ""
            body.append(LEAD_T.format(kicker=l["kicker"], title=l["title"], body=l["body"],
                                      source=l.get("source", ""), link=link))
        if "reading" in t:
            r = t["reading"]
            rb = "".join("<p>%s</p>" % x for x in r["body"])
            trans = ""
            if r.get("trans"):
                tp = "".join("<p>%s</p>" % x for x in r["trans"])
                trans = '<div class="rtrans"><div class="rlabel">白 话</div>%s</div>' % tp
            why = ""
            if r.get("why") or r.get("after"):
                rows = []
                if r.get("why"):
                    rows.append("<p><b>为什么是这篇</b>%s</p>" % r["why"])
                if r.get("after"):
                    rows.append("<p><b>读后</b>%s</p>" % r["after"])
                why = '<div class="rwhy">%s</div>' % "".join(rows)
            body.append(READING_T.format(title=r["title"], byline=r.get("byline", ""),
                                         body=rb, trans=trans, why=why,
                                         author=r.get("author", ""), source=r.get("source", "")))
        for g in t.get("groups", []):
            items = []
            for i in g["items"]:
                more = MORE_T.format(u=i["u"]) if i.get("u") else ""
                note = NOTE_T.format(n=i["note"]) if i.get("note") else ""
                items.append(ITEM_T.format(t=i["t"], d=i["d"], note=note, more=more))
            body.append(GROUP_T.format(name=g["name"], items="\n".join(items)))
        panels.append('    <section class="panel" data-id="%s">\n%s\n    </section>' % (t["id"], "\n".join(body)))

    html = TEMPLATE.format(
        date=d["date"], weekday=d["weekday"], issue=d.get("issue", ""),
        tab_buttons=tab_buttons, panels="\n".join(panels),
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


if __name__ == "__main__":
    p = build()
    print("built:", p, os.path.getsize(p), "bytes")
