#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""730pm · 生成器：读 data.json -> index.html（分 tab 版）"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="day">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>730pm · {date}</title>
<link rel="manifest" href="{up}manifest.json">
<link rel="icon" href="{up}favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png?v=3">
<link rel="icon" type="image/png" sizes="512x512" href="icon-512.png?v=3">
<link rel="apple-touch-icon" href="apple-touch-icon.png?v=3">
<meta name="theme-color" content="#F4EFE6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="robots" content="noindex, nofollow">
<style>
@font-face {{
  font-family: 'ChillRound';
  src: url('{up}fonts/ChillRoundGothic_Medium.ttf') format('truetype');
  font-weight: 500;
  font-display: swap;
}}
@font-face {{
  font-family: 'BarlowCond';
  src: url('{up}fonts/BarlowCondensed-Bold.ttf') format('truetype');
  font-weight: 700;
  font-display: swap;
}}
@font-face {{
  font-family: 'JinghuaSong';
  src: url('{up}fonts/KingHwa_OldSong.woff2') format('woff2');
  font-weight: 400;
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
  --soft: rgba(108,47,54,.10);
  --body-font: 'ChillRound';
  --fs: 15px;
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
  font-family: var(--body-font, 'ChillRound'), -apple-system, 'PingFang SC', 'Noto Sans CJK SC', sans-serif;
  font-size: var(--fs, 15px); line-height: 1.72;
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
#setBtn {{
  background:transparent; border:1px solid var(--line); color:var(--muted);
  border-radius:999px; padding:4px 12px; font-size:12px; font-family:inherit; cursor:pointer;
  align-self:center;
}}
#setBtn:active {{ opacity:.6; }}

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
.searchbx input::-webkit-search-cancel-button,
.searchbx input::-webkit-search-decoration {{ -webkit-appearance: none; appearance: none; display: none; }}
.searchbx .mag {{ flex: 0 0 auto; color: var(--muted); display: block; }}
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
.sitem h3 {{ font-size: calc(var(--fs) * 1.1); margin: 0 0 5px; font-weight: 500; line-height: 1.55; }}
.sitem p {{ margin: 0; font-size: calc(var(--fs) * .93); line-height: 1.78; opacity: .88;
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
.lead h2 {{ font-size: calc(var(--fs) * 1.27); margin:0 0 8px; line-height:1.5; font-weight:500; }}
.lead p {{ margin:0; font-size: calc(var(--fs) * .93); }}
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
.item h3 {{ font-size: var(--fs); margin:0 0 5px; font-weight:500; line-height:1.55; }}
.item p {{ margin:0; font-size: calc(var(--fs) * .9); opacity:.86; }}
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
.rtitle {{ font-size: calc(var(--fs) * 1.67); margin:0 0 5px; font-weight:500; letter-spacing:1px; line-height:1.4; }}
.rby {{ font-size: 11.5px; color: var(--accent); letter-spacing:2px; margin-bottom: 20px; }}
.rwhy {{ margin:0 0 26px; padding:12px 15px; background:var(--card); border-left:2px solid var(--accent); }}
.rwhy p {{ margin:0 0 9px; font-size: calc(var(--fs) * .85); line-height:1.88; opacity:.92; }}
.rwhy p:last-child {{ margin-bottom:0; }}
.rwhy b {{ color:var(--accent); font-weight:500; margin-right:7px; letter-spacing:1px; }}
.rbody p {{ margin:0 0 15px; font-size: calc(var(--fs) * 1.03); line-height:2.05; text-indent:2em; }}
.rtrans {{ margin:24px 0 0; padding:14px 16px; background:var(--card); border-left:2px solid var(--line); }}
.rlabel {{ font-size:10.5px; letter-spacing:2.4px; color:var(--accent); margin-bottom:9px; }}
.rtrans p {{ margin:0 0 11px; font-size: calc(var(--fs) * .87); line-height:1.95; color:var(--muted); text-indent:2em; }}
.rtrans p:last-child {{ margin-bottom:0; }}
.rfoot {{ margin-top:26px; padding-top:15px; border-top:1px solid var(--line);
  font-size:12px; color:var(--muted); line-height:1.9; }}
.rfoot p {{ margin:0 0 6px; }}
.rfoot b {{ color:var(--accent); font-weight:500; margin-right:7px; letter-spacing:1px; }}

footer {{
  margin-top: 40px; padding-top: 13px; border-top: 1px solid var(--line);
  font-size: 11px; color: var(--muted); text-align:center; letter-spacing:.4px;
}}

/* ===== 设置抽屉 ===== */
.scrim {{
  position:fixed; inset:0; z-index:60; background:rgba(20,16,12,.30);
  opacity:0; pointer-events:none; transition:opacity .22s ease;
}}
.scrim.on {{ opacity:1; pointer-events:auto; }}
.drawer {{
  position:fixed; top:0; right:0; bottom:0; z-index:61; width:320px; max-width:88vw;
  background:var(--card); border-left:1px solid var(--line);
  box-shadow:-6px 0 24px rgba(40,30,20,.12);
  display:flex; flex-direction:column;
  transform:translateX(102%); transition:transform .26s cubic-bezier(.3,.8,.3,1);
}}
.drawer.on {{ transform:translateX(0); }}
.drawer .dh {{ display:flex; align-items:center; justify-content:space-between;
  padding:16px 18px 13px; border-bottom:1px solid var(--line); }}
.drawer .dh b {{ font-size:15px; font-weight:500; letter-spacing:.5px; }}
.drawer .dh .x {{ width:26px; height:26px; border:1px solid var(--line); background:transparent;
  color:var(--muted); border-radius:999px; font-size:12px; line-height:1; font-family:inherit; cursor:pointer; }}
.drawer .dbody {{ flex:1; overflow-y:auto; padding:4px 18px 22px; display:flex; flex-direction:column; }}
.drawer section {{ padding:16px 0; border-bottom:1px solid var(--line); }}
.drawer section:last-of-type {{ border-bottom:none; }}
.drawer .cap {{ display:flex; justify-content:space-between; align-items:baseline;
  font-size:10.5px; letter-spacing:1.6px; color:var(--muted); margin-bottom:9px; }}
.drawer .cap .r {{ letter-spacing:.4px; font-family:'BarlowCond',ui-monospace,monospace; font-size:11px; color:var(--accent); }}

.drawer .sel {{ width:100%; display:flex; align-items:center; justify-content:space-between; gap:8px;
  border:1px solid var(--line); background:transparent; color:var(--ink);
  font-family:inherit; font-size:13px; padding:9px 11px; border-radius:6px; cursor:pointer; text-align:left; }}
.drawer .sel.open {{ border-color:var(--accent); }}
.drawer .sel .cv {{ font-size:9px; color:var(--muted); transition:transform .15s; }}
.drawer .sel.open .cv {{ transform:rotate(180deg); }}
.drawer .menu {{ display:none; margin-top:7px; border:1px solid var(--line); border-radius:6px; overflow:hidden; }}
.drawer .menu.show {{ display:block; }}
.drawer .fi {{ width:100%; display:flex; align-items:center; gap:9px; border:none;
  border-bottom:1px solid var(--line); background:transparent; color:var(--ink);
  font-family:inherit; font-size:12.5px; padding:8px 11px; cursor:pointer; text-align:left; }}
.drawer .fi:last-child {{ border-bottom:none; }}
.drawer .fi .g {{ font-size:16px; line-height:1; width:18px; text-align:center; opacity:.9; }}
.drawer .fi .nm {{ flex:1; }}
.drawer .fi .ck {{ display:none; font-size:12px; color:var(--accent); }}
.drawer .fi.on .ck {{ display:inline; }}
.drawer .fi .tag {{ font-size:9.5px; color:var(--muted); border:1px solid var(--line);
  border-radius:999px; padding:1px 6px; letter-spacing:.3px; }}
.drawer .fi.on {{ background:var(--soft); color:var(--accent); }}
.drawer .fi.on .tag {{ border-color:var(--accent); color:var(--accent); }}
.drawer .now {{ font-size:11px; color:var(--muted); margin-top:8px; }}
.drawer .now em {{ font-style:normal; color:var(--accent); }}
.drawer .prev {{ margin-top:10px; border:1px solid var(--line); border-radius:6px;
  background:var(--bg); padding:10px 12px; white-space:pre-wrap; word-break:break-word;
  line-height:1.9; font-size:15px; }}

.drawer .sizerow {{ display:flex; align-items:center; gap:10px; }}
.drawer .pm {{ width:30px; height:30px; flex:0 0 auto; border:1px solid var(--line); background:transparent;
  color:var(--ink); border-radius:6px; font-family:inherit; font-size:15px; line-height:1; cursor:pointer; }}
.drawer .pm:active {{ background:var(--soft); }}
.drawer input[type=range] {{ -webkit-appearance:none; appearance:none; flex:1; height:2px;
  background:var(--line); border-radius:2px; outline:none; margin:0; }}
.drawer input[type=range]::-webkit-slider-thumb {{ -webkit-appearance:none; width:16px; height:16px;
  border-radius:50%; background:var(--accent); box-shadow:0 1px 3px rgba(0,0,0,.22); cursor:pointer; }}
.drawer .sizes {{ display:flex; gap:6px; margin-top:11px; }}
.drawer .sz {{ flex:1; border:1px solid var(--line); background:transparent; color:var(--muted);
  font-family:inherit; border-radius:6px; padding:6px 0 5px; font-size:12.5px; cursor:pointer; line-height:1.35; }}
.drawer .sz .px {{ display:block; font-size:9.5px; opacity:.75;
  font-family:'BarlowCond',monospace; letter-spacing:.3px; }}
.drawer .sz.on {{ border-color:var(--accent); color:var(--accent); background:var(--soft); }}

.drawer .choc {{ display:grid; grid-template-columns:repeat(4,1fr); gap:7px; }}
.drawer .ch {{ border:none; padding:0; background:transparent; cursor:pointer; }}
.drawer .ch .sq {{ height:50px; border-radius:5px; border:1px solid rgba(0,0,0,.10);
  overflow:hidden; display:flex; flex-direction:column; }}
.drawer .ch .sq .b {{ flex:1; background:var(--b); }}
.drawer .ch .sq .a {{ height:13px; background:var(--a); }}
.drawer .ch .nm {{ display:block; font-size:10.5px; color:var(--muted); margin-top:4px; letter-spacing:.3px; }}
.drawer .ch.on .sq {{ outline:1.5px solid var(--accent); outline-offset:1.5px; }}
.drawer .ch.on .nm {{ color:var(--accent); }}
html[data-theme="night"] .drawer .ch .sq .b {{ background:var(--nb); }}
html[data-theme="night"] .drawer .ch .sq .a {{ background:var(--na); }}
.drawer .detail {{ margin-top:10px; display:flex; align-items:center; gap:7px;
  font-size:11px; color:var(--muted); font-family:'BarlowCond',ui-monospace,monospace; letter-spacing:.4px; }}
.drawer .detail .sw2 {{ width:11px; height:11px; border-radius:2px; border:1px solid rgba(0,0,0,.12); }}

.drawer .row {{ display:flex; align-items:center; justify-content:space-between; padding:9px 0; font-size:13.5px; }}
.drawer .sw {{ position:relative; width:40px; height:23px; border-radius:999px; background:var(--line);
  flex:0 0 auto; cursor:pointer; transition:background .2s; }}
.drawer .sw i {{ position:absolute; top:2.5px; left:2.5px; width:18px; height:18px; border-radius:999px;
  background:#fff; box-shadow:0 1px 2px rgba(0,0,0,.18); transition:.2s; }}
.drawer .sw.on {{ background:var(--accent); }}
.drawer .sw.on i {{ left:19.5px; }}
.drawer .row.dis {{ opacity:.4; }}
.drawer .row.dis .sw {{ cursor:default; }}
.drawer .note {{ font-size:11px; color:var(--muted); opacity:.9; padding-top:2px; }}
.drawer .foot {{ margin-top:auto; font-size:10.5px; color:var(--muted); opacity:.75;
  letter-spacing:.4px; border-top:1px solid var(--line); padding:13px 0 2px; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="masthead">
      <h1>730pm<span class="dot">.</span></h1>
      <button id="setBtn" aria-label="设置">设置</button>
    </div>
    <div class="dateline" id="dateBtn"><span class="pick">{date} · {weekday} · {issue}</span><span class="cv">▾</span></div>
  </header>

  <nav class="navrow" id="navrow">
    <button class="chip" type="button" data-id="head">头条</button>
    <button class="chip" type="button" data-id="reading">今日阅读</button>
    <button class="chip" type="button" id="allBtn">全部 <span class="cv">▾</span></button>
    <label class="searchbx" id="searchbx"><svg class="mag" width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="7" cy="7" r="4.6"></circle><path d="M10.5 10.5 L14 14"></path></svg><input id="q" type="text" inputmode="search" placeholder="搜索本期" autocomplete="off"><button class="clr" id="qclr" type="button">✕</button></label>
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

<div class="scrim" id="scrim"></div>

<aside class="drawer" id="drawer" aria-hidden="true">
  <div class="dh"><b>设置</b><button class="x" id="drawerX" aria-label="关闭">✕</button></div>
  <div class="dbody">

    <section>
      <div class="cap">字体</div>
      <button class="sel" id="fontSel"><span id="fontNow">寒蝉圆黑体</span><span class="cv">▾</span></button>
      <div class="menu" id="fontMenu">
        <button class="fi on" data-f="chill"><span class="g" style="font-family:'ChillRound'">永</span><span class="nm">寒蝉圆黑体</span><span class="ck">✓</span><span class="tag">内置</span></button>
        <button class="fi" data-f="jinghua"><span class="g" style="font-family:'JinghuaSong',serif">永</span><span class="nm">京华老宋体</span><span class="ck">✓</span><span class="tag">内置</span></button>
        <button class="fi" data-f="hei"><span class="g" style="font-family:-apple-system,'PingFang SC',sans-serif">永</span><span class="nm">系统黑体</span><span class="ck">✓</span><span class="tag">系统</span></button>
        <button class="fi" data-f="song"><span class="g" style="font-family:'Songti SC',serif">永</span><span class="nm">系统宋体</span><span class="ck">✓</span><span class="tag">系统</span></button>
      </div>
      <div class="now">当前字体：<em id="fontTxt">寒蝉圆黑体</em></div>
      <div class="prev" id="prev">ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
1234567890

%+-/:=*#￥_，。？！“”……、：；~（）～

世界之心是以我为中心的。</div>
    </section>

    <section>
      <div class="cap"><span>字号</span><span class="r" id="pxNow">15 px</span></div>
      <div class="sizerow">
        <button class="pm" id="minus" aria-label="减小">−</button>
        <input type="range" id="rng" min="12" max="46" step="1" value="15">
        <button class="pm" id="plus" aria-label="增大">＋</button>
      </div>
      <div class="sizes" id="quick">
        <button class="sz" data-v="13">小<span class="px">13px</span></button>
        <button class="sz on" data-v="15">标准<span class="px">15px</span></button>
        <button class="sz" data-v="18">大<span class="px">18px</span></button>
        <button class="sz" data-v="22">特大<span class="px">22px</span></button>
      </div>
    </section>

    <section>
      <div class="cap"><span>配色</span><span class="r" id="palHint">白天这套</span></div>
      <div class="choc" id="choc"></div>
      <div class="detail"><span class="sw2" id="swB"></span><span id="hexB"></span><span class="sw2" id="swA" style="margin-left:5px"></span><span id="hexA"></span></div>
    </section>

    <section>
      <div class="row" id="rowNight"><span>夜间模式</span><span class="sw" id="swNight"><i></i></span></div>
      <div class="row" id="rowAuto"><span>夜间模式跟随系统</span><span class="sw" id="swAuto"><i></i></span></div>
      <div class="note" id="note">跟着系统走时，上面那个手动开关就不作数了。</div>
    </section>

    <div class="foot">改动即时生效 · 只存在这台设备上</div>
  </div>
</aside>


<script>
var TODAY="{date}", WEEKDAY="{weekday}", ISSUE="{issue}", TODAY_ISO="{today_iso}";
var ALL_TABS={all_tabs};
var ISSUE_ITEMS={issue_json};
var ARCHIVE={archive_json};
(function(){{
  var root=document.documentElement, meta=document.querySelector('meta[name=theme-color]');

  var SCHEMES=[
    {{id:'baokan', name:'旧报', day:['#F4EFE6','#2A2521','#6C2F36'], night:['#17140F','#C8BFB2','#C6ACDC']}},
    {{id:'shuang', name:'霜白', day:['#F1F2EF','#20241F','#3C5A4E'], night:['#121815','#C2CBBF','#7FBF9F']}},
    {{id:'shazhi', name:'砂纸', day:['#EFE5D4','#2B241C','#8A4B2A'], night:['#1A1410','#D5C4AE','#D08A5A']}},
    {{id:'dianlan',name:'靛蓝', day:['#EDF1F6','#1E2833','#2B4A70'], night:['#10161F','#BFCBDA','#8FB6D9']}},
    {{id:'ouhe',   name:'藕荷', day:['#F6F0F3','#2A2129','#7C4B6E'], night:['#17121A','#D2C3D0','#D3A8C6']}},
    {{id:'chahe',  name:'茶褐', day:['#F2EDE3','#2A231A','#6B5334'], night:['#181410','#D2C3AC','#C9A87C']}},
    {{id:'zhuqing',name:'竹青', day:['#EDF0EA','#1F2620','#4A6350'], night:['#121714','#C3CFC4','#9BC0A5']}},
    {{id:'qiangui',name:'铅灰', day:['#E9E9E7','#232322','#4A4A48'], night:['#141414','#C7C7C5','#B8B8B6']}}
  ];
  var FONTS={{
    chill:  {{name:'寒蝉圆黑体', css:"'ChillRound'"}},
    jinghua:{{name:'京华老宋体', css:"'JinghuaSong'"}},
    hei:    {{name:'系统黑体',   css:"-apple-system,'PingFang SC','Noto Sans CJK SC',sans-serif"}},
    song:   {{name:'系统宋体',   css:"'Songti SC','Noto Serif CJK SC',serif"}}
  }};
  var SET={{font:'chill', size:15, scheme:'baokan', night:false, auto:false}};
  try{{
    var s=JSON.parse(localStorage.getItem('np-set')||'null');
    if(s) for(var k in SET) if(s[k]!==undefined) SET[k]=s[k];
  }}catch(e){{}}
  if(!FONTS[SET.font]) SET.font='chill';
  if(SET.size<12||SET.size>46) SET.size=15;

  function hex2rgb(h){{h=h.replace('#','');return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)];}}
  function rgb2hex(r){{return '#'+r.map(function(v){{return ('0'+Math.round(v).toString(16)).slice(-2);}}).join('');}}
  function mix(a,b,t){{var A=hex2rgb(a),B=hex2rgb(b);return rgb2hex(A.map(function(v,i){{return v+(B[i]-v)*t;}}));}}
  function scheme(){{for(var i=0;i<SCHEMES.length;i++) if(SCHEMES[i].id===SET.scheme) return SCHEMES[i]; return SCHEMES[0];}}
  function save(){{try{{localStorage.setItem('np-set',JSON.stringify(SET));}}catch(e){{}}}}

  var mql = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function wantNight(){{ return SET.auto ? !!(mql && mql.matches) : SET.night; }}

  var el = {{
    scrim:document.getElementById('scrim'), drawer:document.getElementById('drawer'),
    setBtn:document.getElementById('setBtn'), x:document.getElementById('drawerX'),
    fontSel:document.getElementById('fontSel'), fontMenu:document.getElementById('fontMenu'),
    fontNow:document.getElementById('fontNow'), fontTxt:document.getElementById('fontTxt'),
    prev:document.getElementById('prev'), rng:document.getElementById('rng'),
    pxNow:document.getElementById('pxNow'), quick:document.getElementById('quick'),
    choc:document.getElementById('choc'), swB:document.getElementById('swB'), swA:document.getElementById('swA'),
    hexB:document.getElementById('hexB'), hexA:document.getElementById('hexA'), palHint:document.getElementById('palHint'),
    rowNight:document.getElementById('rowNight'), rowAuto:document.getElementById('rowAuto'),
    swNight:document.getElementById('swNight'), swAuto:document.getElementById('swAuto'), note:document.getElementById('note')
  }};

  /* 巧克力格 */
  el.choc.innerHTML = SCHEMES.map(function(x){{
    return '<button class="ch" data-id="'+x.id+'" style="--b:'+x.day[0]+';--a:'+x.day[2]+';--nb:'+x.night[0]+';--na:'+x.night[2]+'">'
      + '<span class="sq"><span class="b"></span><span class="a"></span></span>'
      + '<span class="nm">'+x.name+'</span></button>';
  }}).join('');

  function paint(){{
    var sc=scheme(), night=wantNight(), p = night ? sc.night : sc.day;
    root.style.setProperty('--bg', p[0]);
    root.style.setProperty('--ink', p[1]);
    root.style.setProperty('--accent', p[2]);
    root.style.setProperty('--muted', mix(p[1],p[0],.42));
    root.style.setProperty('--line', mix(p[0],p[1],.16));
    root.style.setProperty('--card', night ? mix(p[0],'#ffffff',.05) : mix(p[0],'#ffffff',.45));
    root.style.setProperty('--tabbar', 'rgba('+hex2rgb(p[0]).join(',')+',.93)');
    root.style.setProperty('--soft', 'rgba('+hex2rgb(p[2]).join(',')+',.10)');
    root.style.setProperty('--body-font', FONTS[SET.font].css);
    root.style.setProperty('--fs', SET.size+'px');
    root.setAttribute('data-theme', night ? 'night' : 'day');
    if(meta) meta.setAttribute('content', p[0]);

    el.swB.style.background = p[0];
    el.swA.style.background = p[2];
    el.hexB.textContent = p[0].toUpperCase();
    el.hexA.textContent = p[2].toUpperCase();
    el.palHint.textContent = night ? '夜里这套' : '白天这套';
    el.fontNow.textContent = FONTS[SET.font].name;
    el.fontTxt.textContent = FONTS[SET.font].name;
    el.prev.style.fontFamily = FONTS[SET.font].css + ',sans-serif';
    el.prev.style.fontSize = SET.size + 'px';
    el.rng.value = SET.size;
    el.pxNow.textContent = SET.size + ' px';
    el.swNight.classList.toggle('on', night);
    el.swAuto.classList.toggle('on', SET.auto);
    el.rowNight.classList.toggle('dis', SET.auto);
    el.note.textContent = SET.auto ? '现在跟着系统走，手动开关先不管用。' : '跟着系统走时，上面那个手动开关就不作数了。';

    var list = el.choc.querySelectorAll('.ch');
    for(var i=0;i<list.length;i++) list[i].classList.toggle('on', list[i].getAttribute('data-id')===SET.scheme);
    var fl = el.fontMenu.querySelectorAll('.fi');
    for(var j=0;j<fl.length;j++) fl[j].classList.toggle('on', fl[j].getAttribute('data-f')===SET.font);
    var ql = el.quick.querySelectorAll('.sz');
    for(var m=0;m<ql.length;m++) ql[m].classList.toggle('on', +ql[m].getAttribute('data-v')===SET.size);
  }}

  function openDrawer(){{
    el.drawer.classList.add('on'); el.scrim.classList.add('on');
    el.drawer.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden';
  }}
  function closeDrawer(){{
    el.drawer.classList.remove('on'); el.scrim.classList.remove('on');
    el.drawer.setAttribute('aria-hidden','true'); document.body.style.overflow='';
    el.fontMenu.classList.remove('show'); el.fontSel.classList.remove('open');
  }}

  el.setBtn.addEventListener('click', openDrawer);
  el.x.addEventListener('click', closeDrawer);
  el.scrim.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function(e){{ if(e.key==='Escape') closeDrawer(); }});

  el.fontSel.addEventListener('click', function(){{
    el.fontSel.classList.toggle('open'); el.fontMenu.classList.toggle('show');
  }});
  el.fontMenu.addEventListener('click', function(e){{
    var b=e.target.closest('.fi'); if(!b) return;
    SET.font=b.getAttribute('data-f');
    el.fontMenu.classList.remove('show'); el.fontSel.classList.remove('open');
    paint(); save();
  }});

  function setSize(v){{
    v=Math.round(v); if(v<12) v=12; if(v>46) v=46;
    SET.size=v; paint(); save();
  }}
  el.rng.addEventListener('input', function(){{ setSize(+el.rng.value); }});
  document.getElementById('minus').addEventListener('click', function(){{ setSize(SET.size-1); }});
  document.getElementById('plus').addEventListener('click', function(){{ setSize(SET.size+1); }});
  el.quick.addEventListener('click', function(e){{
    var b=e.target.closest('.sz'); if(!b) return; setSize(+b.getAttribute('data-v'));
  }});

  el.choc.addEventListener('click', function(e){{
    var b=e.target.closest('.ch'); if(!b) return;
    SET.scheme=b.getAttribute('data-id'); paint(); save();
  }});

  el.swNight.addEventListener('click', function(){{
    if(SET.auto) return;
    SET.night=!SET.night; paint(); save();
  }});
  el.swAuto.addEventListener('click', function(){{
    SET.auto=!SET.auto; paint(); save();
  }});
  if(mql) {{
    var onSys=function(){{ if(SET.auto) paint(); }};
    if(mql.addEventListener) mql.addEventListener('change', onSys);
    else if(mql.addListener) mql.addListener(onSys);
  }}

  paint();

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
    document.getElementById('q').value='';
    document.getElementById('searchbx').classList.remove('has');
    document.body.classList.remove('searching');
    activate(id);
  }});

  /* ---- 往期窄条（整份索引已内嵌，不用再请求）---- */
  function loadArchive(){{
    var head='<div class="dh"><div class="l1"><span class="d">'+esc(TODAY)+'</span><span class="cv">▴</span></div>'
           + '<div class="l2">'+esc(WEEKDAY)+' · '+esc(ISSUE)+'</div></div>';
    if(!ARCHIVE.length){{ datePanel.innerHTML=head+'<div class="smore">还没有往期</div>'; return; }}
    datePanel.innerHTML = head + ARCHIVE.map(function(it){{
      return '<div class="srow'+(it.cur?' cur':'')+'" data-href="'+esc(it.href)+'">'
           + '<span class="no">'+esc(it.no)+'</span><span class="dt">'+esc(it.label)+'</span>'
           + '<span class="ct">'+esc(it.count)+'</span></div>';
    }}).join('') + '<div class="smore">点任意一期翻看</div>';
  }}
  datePanel.addEventListener('click', function(e){{
    var r=e.target.closest('.srow'); if(!r) return;
    var h=r.getAttribute('data-href');
    closeDD();
    if(h) location.href=h;
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
    navigator.serviceWorker.register('{up}sw.js',{{scope:'{up}'}}).catch(function(){{}});
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


def load_index():
    p = os.path.join(BASE, "issues", "index.json")
    if not os.path.exists(p):
        return {"issues": []}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def iso_of(d):
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", d.get("date", ""))
    return "%s-%02d-%02d" % (m.group(1), int(m.group(2)), int(m.group(3))) if m else ""


def short_label(label):
    return label[5:] if len(label) > 5 and label[4] == "年" else label


def archive_rows(page_iso, in_issues_dir, today_iso):
    """窄条里的一行一行。href 为空 = 当前页。"""
    rows = []
    for it in load_index().get("issues", []):
        dt = it.get("date", "")
        if dt == page_iso:
            href = ""
        elif dt == today_iso and not in_issues_dir:
            href = ""
        elif dt == today_iso:
            href = "../index.html"
        elif in_issues_dir:
            href = dt + ".html"
        else:
            href = "issues/" + dt + ".html"
        label = short_label(it.get("label", dt))
        if dt == today_iso:
            label += " · 今天"
        rows.append({"no": re.sub(r"\D", "", it.get("issue", "")), "label": label,
                     "count": str(it.get("count", "")), "href": href, "cur": dt == page_iso})
    return rows


def render_html(d, page_iso, in_issues_dir):

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
    skip = {"head", "reading"}
    all_tabs = [{"id": t["id"], "name": t["name"]} for t in tabs if t["id"] not in skip]
    all_tabs.append({"id": "saved", "name": "书报架", "fn": True})

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

    today_iso = iso_of(json.load(open(os.path.join(BASE, "data.json"), encoding="utf-8"))) \
        if os.path.exists(os.path.join(BASE, "data.json")) else ""
    rows = archive_rows(page_iso, in_issues_dir, today_iso)

    return TEMPLATE.format(
        up=("../" if in_issues_dir else ""),
        date=d["date"], weekday=d["weekday"], issue=d.get("issue", ""),
        tab_buttons=tab_buttons, panels="\n".join(panels),
        today_iso=page_iso,
        all_tabs=json.dumps(all_tabs, ensure_ascii=False, separators=(",", ":")),
        issue_json=json.dumps(searchable, ensure_ascii=False, separators=(",", ":")),
        archive_json=json.dumps(rows, ensure_ascii=False, separators=(",", ":")),
    )


def build():
    with open(os.path.join(BASE, "data.json"), encoding="utf-8") as f:
        d = json.load(f)
    html = render_html(d, iso_of(d), False)
    out = os.path.join(BASE, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out


def build_archives():
    """每一期生成一张独立页面，和今天那页结构完全一样。"""
    idx = load_index()
    out_dir = os.path.join(BASE, "issues")
    made = []
    for it in idx.get("issues", []):
        dt = it.get("date")
        src = os.path.join(out_dir, dt + ".json")
        if not dt or not os.path.exists(src):
            continue
        with open(src, encoding="utf-8") as f:
            d = json.load(f)
        out = os.path.join(out_dir, dt + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render_html(d, dt, True))
        made.append(out)
    return made


if __name__ == "__main__":
    p = build()
    print("built:", p, os.path.getsize(p), "bytes")
    for q in build_archives():
        print("built:", q, os.path.getsize(q), "bytes")
