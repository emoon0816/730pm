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
.wrap {{ max-width: 720px; margin: 0 auto; padding: 0 16px 70px; position: relative; }}

/* 报头 */
header {{ padding: 22px 0 12px; position: relative; }}
.masthead {{ display:flex; align-items:baseline; justify-content:space-between; gap:10px; }}
h1 {{ font-size: 34px; margin:0; letter-spacing:.5px; font-weight:700;
     font-family:'BarlowCond','ChillRound',sans-serif; line-height:1; }}
h1 .dot {{ color: var(--accent); }}
.dateline {{ font-size: 11.5px; color: var(--muted); letter-spacing:.4px; margin-top:7px;
  display: inline-flex; align-items: center; gap: 5px; cursor: pointer; }}
.dateline .pick {{ border-bottom: 1px dotted var(--line); padding-bottom: 1px; }}
.dateline .cv {{ font-size: 9px; opacity:.75; }}
.dateline.act {{ color: var(--accent); }}
.dateline.act .cv, .dateline.act .pick {{ color: var(--accent); }}
.dateline.act .pick {{ border-bottom: 1px solid var(--accent); }}
#themeBtn {{
  background:transparent; border:1px solid var(--line); color:var(--muted);
  border-radius:999px; padding:4px 11px; font-size:12px; font-family:inherit; cursor:pointer;
  align-self:center;
}}
#themeBtn:active {{ opacity:.6; }}

/* 顶部一行：两个栏目 + 全部 + 搜索 */
.navrow {{
  position: sticky; top: 0; z-index: 20;
  display: flex; gap: 7px; align-items: center;
  margin: 0 -16px; padding: 9px 16px;
  background: var(--tabbar);
  -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
}}
.chip {{
  flex: 0 0 auto; border: 1px solid var(--line); background: transparent;
  color: var(--muted); font-family: inherit; font-size: 13px;
  padding: 6px 13px; border-radius: 999px; cursor: pointer;
  transition: all .16s ease; white-space: nowrap;
}}
.chip.on {{ background: var(--accent); border-color: var(--accent); color: var(--bg); }}
.chip.act {{ border-color: var(--accent); color: var(--accent); }}
.searchbx {{
  flex: 1; min-width: 0; display: flex; align-items: center; gap: 6px;
  border: 1px solid var(--line); border-radius: 999px; padding: 5px 11px;
  transition: border-color .16s ease;
}}
.searchbx input {{
  flex: 1; min-width: 0; border: none; background: transparent; outline: none;
  font-family: inherit; font-size: 12.5px; color: var(--ink);
}}
.searchbx input::placeholder {{ color: var(--muted); opacity: .85; }}
.searchbx .mag {{ font-size: 12px; color: var(--muted); }}
.searchbx .clr {{
  display: none; border: none; background: transparent; color: var(--muted);
  font-size: 13px; line-height: 1; cursor: pointer; padding: 0 1px;
}}
.searchbx.has .clr {{ display: block; }}
body.searching .navrow .chip {{ display: none; }}
body.searching .searchbx {{ border-color: var(--accent); }}

/* 下拉：只包住触发物，圆角小 */
.dd {{
  display: none; position: absolute; z-index: 40;
  background: var(--card); border: 1px solid var(--line);
  border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,.045); overflow: hidden;
}}
.dd.on {{ display: block; }}
#allPanel {{ left: 0; top: 0; width: 262px; }}
#allPanel .grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 5px; padding: 9px; }}
.cell {{
  text-align: center; font-size: 12px; padding: 8px 0; border-radius: 6px;
  background: transparent; border: 1px solid var(--line); color: var(--ink);
  font-family: inherit; cursor: pointer;
}}
.cell.on {{ background: var(--accent); color: var(--bg); border-color: var(--accent); }}
.cell.fn {{ color: var(--muted); border-style: dashed; }}

#datePanel {{ left: 0; top: 0; width: 236px; }}
#datePanel .dh {{ padding: 5px 12px 6px; border-bottom: 1px solid var(--line); }}
#datePanel .dh .l1 {{ display: flex; align-items: center; justify-content: space-between; gap: 6px; }}
#datePanel .dh .d {{ font-size: 12px; color: var(--accent); }}
#datePanel .dh .l2 {{ font-size: 10.5px; color: var(--muted); margin-top: 1px; }}
#datePanel .cv {{ font-size: 9px; color: var(--accent); }}
.srow {{
  display: flex; align-items: center; gap: 7px; padding: 8px 12px;
  font-size: 12.5px; border-bottom: 1px solid var(--line); cursor: pointer;
}}
.srow:last-child {{ border-bottom: none; }}
.srow .no {{ color: var(--accent); font-size: 11.5px; min-width: 24px; }}
.srow .dt {{ flex: 1; }}
.srow .ct {{ font-size: 10.5px; color: var(--muted); }}
.srow.cur {{ background: rgba(108,47,54,.05); }}
.smore {{ font-size: 10.5px; color: var(--muted); text-align: center; padding: 7px; }}

/* 搜索结果 */
.scount {{ font-size: 11.5px; color: var(--muted); letter-spacing: .5px; margin: 14px 0 2px; }}
.scount b {{ color: var(--accent); font-weight: 500; }}
.sitem {{ padding: 12px 0 13px; border-bottom: 1px dashed var(--line); }}
.sitem .where {{ font-size: 10.5px; letter-spacing: 1.2px; color: var(--muted); margin-bottom: 3px; }}
.sitem h3 {{ font-size: 16.5px; margin: 0 0 5px; font-weight: 500; line-height: 1.55; }}
.sitem p {{ margin: 0; font-size: 14px; line-height: 1.78; opacity: .88;
  display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden; }}
mark {{ background: rgba(108,47,54,.14); color: var(--accent); font-weight: 500; border-radius:2px; padding:0 1.5px; }}
html[data-theme="night"] mark {{ background: rgba(198,172,220,.20); }}

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
    <div class="dateline" id="dateBtn"><span class="pick">{date} · {weekday} · {issue}</span><span class="cv">▾</span></div>
  </header>

  <nav class="navrow" id="navrow">
    <button class="chip" type="button" data-id="head">头条</button>
    <button class="chip" type="button" data-id="reading">今日阅读</button>
    <button class="chip" type="button" id="allBtn">全部 <span class="cv">▾</span></button>
    <label class="searchbx" id="searchbx"><span class="mag">⌕</span><input id="q" type="search" placeholder="搜索本期" autocomplete="off"><button class="clr" id="qclr" type="button">✕</button></label>
  </nav>

  <div class="dd" id="allPanel"></div>
  <div class="dd" id="datePanel"></div>

  <main id="main">
{panels}
      <section class="panel" data-id="search"><div id="searchResults"></div></section>
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
var TODAY="{date}", WEEKDAY="{weekday}", ISSUE="{issue}", TODAY_ISO="{today_iso}";
var ALL_TABS={all_tabs};
var ISSUE_ITEMS={issue_json};
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

  var tabs=[].slice.call(document.querySelectorAll('.chip[data-id]'));
  var panels=[].slice.call(document.querySelectorAll('.panel'));
  var lastTab='head';

  function activate(id){{
    lastTab=id;
    tabs.forEach(function(b){{ b.classList.toggle('on', b.dataset.id===id); }});
    panels.forEach(function(p){{ p.classList.toggle('on', p.dataset.id===id); }});
    if(id==='saved') renderSaved();
    window.scrollTo({{top:0,behavior:'smooth'}});
  }}

  /* ---- 下拉：同时只开一个 ---- */
  var allPanel=document.getElementById('allPanel'), datePanel=document.getElementById('datePanel');
  var allBtn=document.getElementById('allBtn'), dateBtn=document.getElementById('dateBtn');
  function closeDD(){{
    allPanel.classList.remove('on'); datePanel.classList.remove('on');
    allBtn.classList.remove('act'); dateBtn.classList.remove('act');
  }}
  function place(panel, anchor, cover){{
    var host=panel.parentNode.getBoundingClientRect();
    var a=anchor.getBoundingClientRect();
    var w=panel.offsetWidth || 240;
    var left=a.left-host.left;
    var maxLeft=host.width-w-8;
    if(left<8) left=8;
    if(left>maxLeft) left=maxLeft;
    panel.style.left=left+'px';
    panel.style.top=(cover ? a.top-host.top : a.bottom-host.top+6)+'px';
  }}
  function openDD(which){{
    var wasOpen = (which==='all' ? allPanel.classList.contains('on') : datePanel.classList.contains('on'));
    closeDD();
    if(wasOpen) return;                    // 再点一次就收
    if(which==='all'){{
      allPanel.classList.add('on'); allBtn.classList.add('act');
      [].forEach.call(allPanel.querySelectorAll('.cell'), function(c){{
        c.classList.toggle('on', c.getAttribute('data-id')===lastTab);
      }});
      place(allPanel, allBtn);
    }}
    else {{
      datePanel.classList.add('on'); dateBtn.classList.add('act');
      loadArchive(); place(datePanel, dateBtn, true);   // 盖住日期本身，由条头替代
    }}
  }}
  window.addEventListener('resize', function(){{
    if(allPanel.classList.contains('on')) place(allPanel, allBtn);
    if(datePanel.classList.contains('on')) place(datePanel, dateBtn, true);
  }});
  allBtn.addEventListener('click', function(e){{ e.stopPropagation(); openDD('all'); }});
  dateBtn.addEventListener('click', function(e){{ e.stopPropagation(); openDD('date'); }});
  allPanel.addEventListener('click', function(e){{ e.stopPropagation(); }});
  datePanel.addEventListener('click', function(e){{ e.stopPropagation(); }});
  document.addEventListener('click', function(){{ closeDD(); }});

  /* ---- 全部栏目 ---- */
  allPanel.innerHTML = '<div class="grid">' + ALL_TABS.map(function(t){{
    return '<button class="cell'+(t.fn?' fn':'')+'" type="button" data-id="'+t.id+'">'+t.name+'</button>';
  }}).join('') + '</div>';
  allPanel.addEventListener('click', function(e){{
    var b=e.target.closest('.cell'); if(!b) return;
    var id=b.getAttribute('data-id');
    closeDD();
    if(id==='archive'){{ location.href='issues.html'; return; }}
    document.getElementById('q').value='';
    document.getElementById('searchbx').classList.remove('has');
    document.body.classList.remove('searching');
    activate(id);
  }});

  /* ---- 往期窄条 ---- */
  var archLoaded=false;
  function pad(n){{ return (n<10?'0':'')+n; }}
  function loadArchive(){{
    if(archLoaded) return;
    archLoaded=true;
    fetch('issues/index.json',{{cache:'no-store'}}).then(function(r){{ return r.json(); }}).then(function(d){{
      var list=d.issues||[];
      var head='<div class="dh"><div class="l1"><span class="d">'+esc(TODAY)+'</span><span class="cv">▴</span></div>'
             + '<div class="l2">'+esc(WEEKDAY)+' · '+esc(ISSUE)+'</div></div>';
      if(!list.length){{ datePanel.innerHTML=head+'<div class="smore">还没有往期</div>'; return; }}
      datePanel.innerHTML = head + list.map(function(it){{
        var no=(it.issue||'').replace(/[^0-9]/g,'');
        var cur=(it.date===TODAY_ISO);
        var label=(it.label||it.date);
        if(label.length>4 && label.charAt(4)==='年') label=label.slice(5);
        if(cur) label += ' · 今天';
        return '<div class="srow'+(cur?' cur':'')+'" data-d="'+esc(it.date)+'">'
             + '<span class="no">'+esc(no)+'</span><span class="dt">'+esc(label)+'</span>'
             + '<span class="ct">'+esc(it.count)+'</span></div>';
      }}).join('') + '<div class="smore">点任意一期翻看</div>';
    }}).catch(function(){{
      datePanel.innerHTML='<div class="smore">往期索引还没生成</div>';
    }});
  }}
  datePanel.addEventListener('click', function(e){{
    var r=e.target.closest('.srow'); if(!r) return;
    var d=r.getAttribute('data-d');
    closeDD();
    if(d===TODAY_ISO) return;
    location.href='issues.html#'+d;
  }});

  /* ---- 搜索本期 ---- */
  var q=document.getElementById('q'), clr=document.getElementById('qclr');
  var sres=document.getElementById('searchResults'), sbx=document.getElementById('searchbx');
  function hl(safe, kws){{
    var out=safe;
    kws.forEach(function(k){{
      if(!k) return;
      var lower=out.toLowerCase(), kl=k.toLowerCase();
      var pos=0, res='', found=false;
      while(true){{
        var i=lower.indexOf(kl,pos);
        if(i<0) break;
        res += out.slice(pos,i) + '<mark>' + out.slice(i,i+k.length) + '</mark>';
        pos = i + k.length; found = true;
      }}
      if(found) out = res + out.slice(pos);
    }});
    return out;
  }}
  function score(kw,text){{
    var k=kw.toLowerCase(), t=(text||'').toLowerCase();
    if(!k||!t) return 0;
    if(t.indexOf(k)>=0) return 1;
    if(k.length<2) return 0;
    var hit=0, total=k.length-1;
    for(var i=0;i<total;i++){{ if(t.indexOf(k.substr(i,2))>=0) hit++; }}
    return hit/total;
  }}
  function runSearch(){{
    var raw=q.value.trim();
    sbx.classList.toggle('has', raw.length>0);
    if(!raw){{
      document.body.classList.remove('searching');
      activate(lastTab||'head');
      return;
    }}
    document.body.classList.add('searching');
    closeDD();
    var kws=raw.split(' ').filter(Boolean).slice(0,12);
    var hits=[];
    ISSUE_ITEMS.forEach(function(it){{
      var best=0;
      kws.forEach(function(k){{
        var s=Math.max(score(k,it.t), score(k,it.d)*0.95);
        if(s>best) best=s;
      }});
      if(best>=0.6) hits.push({{it:it,s:best}});
    }});
    hits.sort(function(a,b){{ return b.s-a.s; }});
    if(!hits.length){{
      sres.innerHTML='<div class="empty">本期没找到「'+esc(raw)+'」。<br>换个词，或者点日期翻往期。</div>';
    }} else {{
      sres.innerHTML='<div class="scount">本期匹配 <b>'+hits.length+'</b> 条 · 关键字 <b>'+esc(kws.join(' '))+'</b></div>'
        + hits.map(function(h){{
            var it=h.it;
            var link=it.u?'<a class="more" href="'+esc(it.u)+'" target="_blank" rel="noopener">原文 ↗</a>':'';
            return '<div class="sitem"><div class="where">'+esc(it.tab)+'</div>'
              + '<h3>'+hl(esc(it.t),kws)+'</h3>'
              + (it.d?'<p>'+hl(esc(it.d),kws)+'</p>':'')
              + (link?'<div class="irow">'+link+'</div>':'') + '</div>';
          }}).join('');
    }}
    tabs.forEach(function(b){{ b.classList.remove('on'); }});
    panels.forEach(function(p){{ p.classList.toggle('on', p.dataset.id==='search'); }});
  }}
  var qtimer=null;
  q.addEventListener('input', function(){{
    clearTimeout(qtimer);
    qtimer=setTimeout(runSearch,120);
  }});
  q.addEventListener('focus', function(){{ closeDD(); }});
  clr.addEventListener('click', function(e){{
    e.preventDefault(); e.stopPropagation();
    q.value=''; q.focus(); runSearch();
  }});

  tabs.forEach(function(b){{ b.addEventListener('click',function(){{
    q.value=''; sbx.classList.remove('has'); document.body.classList.remove('searching');
    activate(b.dataset.id);
  }}); }});

  var start=localStorage.getItem('np-tab');
  if(!start || !document.querySelector('.panel[data-id="'+start+'"]')) start='head';
  activate(start);
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

    # 全部面板的格子：内容栏目（今日阅读挪到第二位）+ 书报架 + 往期
    rest = [t for t in tabs if t["id"] != "reading"]
    reading = [t for t in tabs if t["id"] == "reading"]
    if reading:
        rest.insert(1, reading[0])
    all_tabs = [{"id": t["id"], "name": ("今日阅读" if t["id"] == "reading" else t["name"])} for t in rest]
    all_tabs.append({"id": "saved", "name": "书报架", "fn": True})
    all_tabs.append({"id": "archive", "name": "往期", "fn": True})

    # 搜索用的本期索引
    searchable = []
    for t in tabs:
        if t["id"] == "head":
            l = d["lead"]
            searchable.append({"tab": t["name"], "t": l["title"], "d": l.get("body", ""), "u": l.get("u", "")})
        if "reading" in t:
            r = t["reading"]
            searchable.append({"tab": "今日阅读", "t": r["title"],
                               "d": " ".join(r.get("body", []))[:500], "u": ""})
        for g in t.get("groups", []):
            for i in g["items"]:
                searchable.append({"tab": t["name"], "t": i["t"], "d": i.get("d", ""), "u": i.get("u", "")})

    import re as _re
    m = _re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", d["date"])
    today_iso = "%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3))) if m else ""

    html = TEMPLATE.format(
        date=d["date"], weekday=d["weekday"], issue=d.get("issue", ""),
        tab_buttons=tab_buttons, panels="\n".join(panels),
        today_iso=today_iso,
        all_tabs=json.dumps(all_tabs, ensure_ascii=False, separators=(",", ":")),
        issue_json=json.dumps(searchable, ensure_ascii=False, separators=(",", ":")),
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


if __name__ == "__main__":
    p = build()
    print("built:", p, os.path.getsize(p), "bytes")
