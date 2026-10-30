/* 730pm · 朗读：点击才生成，生成完才播，音频缓存在本机 IndexedDB */
(function () {
  var CKEY = 'np-tts';
  var cfg = { mode: 'minimax', key: '', group: '', voice: '', model: '', speed: 1, proxy: '' };
  var DEF_MODEL = { minimax: 'speech-02-hd', fish: 's1', volc: 'volc_tts' };
  function modelId() { return (cfg.model || '').trim() || DEF_MODEL[cfg.mode] || ''; }
  try { var s = JSON.parse(localStorage.getItem(CKEY) || 'null'); if (s) for (var k in s) if (k in cfg) cfg[k] = s[k]; } catch (e) {}
  function saveCfg() { try { localStorage.setItem(CKEY, JSON.stringify(cfg)); } catch (e) {} }

  var toastEl = document.getElementById('ttoast'), toastT = null;
  function toast(m) {
    if (!toastEl) return;
    toastEl.textContent = m; toastEl.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 1900);
  }

  function fmt(t) { t = Math.max(0, Math.floor(t || 0)); var m = Math.floor(t / 60), s = t % 60; return m + ':' + (s < 10 ? '0' : '') + s; }

  /* ---------- 本机缓存 ---------- */
  var DBp = null;
  function db() {
    if (DBp) return DBp;
    DBp = new Promise(function (res, rej) {
      try {
        var r = indexedDB.open('730pm-tts', 1);
        r.onupgradeneeded = function () { r.result.createObjectStore('a'); };
        r.onsuccess = function () { res(r.result); };
        r.onerror = function () { rej(r.error); };
      } catch (e) { rej(e); }
    });
    return DBp;
  }
  function idbGet(k) {
    return db().then(function (d) {
      return new Promise(function (res, rej) {
        var q = d.transaction('a', 'readonly').objectStore('a').get(k);
        q.onsuccess = function () { res(q.result || null); };
        q.onerror = function () { rej(q.error); };
      });
    });
  }
  function idbSet(k, v) {
    return db().then(function (d) {
      return new Promise(function (res, rej) {
        var q = d.transaction('a', 'readwrite').objectStore('a').put(v, k);
        q.onsuccess = function () { res(); };
        q.onerror = function () { rej(q.error); };
      });
    });
  }

  /* ---------- 合成 ---------- */
  function split(text, max) {
    var out = [], cur = '';
    String(text || '').split(/\n+/).forEach(function (p) {
      p = p.trim(); if (!p) return;
      if (!cur) { cur = p; return; }
      if ((cur + '\n' + p).length <= max) { cur += '\n' + p; return; }
      out.push(cur); cur = p;
    });
    if (cur) out.push(cur);
    var res = [];
    out.forEach(function (p) {
      while (p.length > max) { res.push(p.slice(0, max)); p = p.slice(max); }
      if (p) res.push(p);
    });
    return res;
  }

  function hexBytes(h) {
    var n = h.length >> 1, u = new Uint8Array(n);
    for (var i = 0; i < n; i++) u[i] = parseInt(h.substr(i * 2, 2), 16);
    return u;
  }

  function one(text) {
    if (cfg.proxy) {
      return fetch(cfg.proxy, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ provider: cfg.mode, model: modelId(), key: cfg.key, group: cfg.group, voice: cfg.voice, speed: cfg.speed, text: text })
      }).then(function (r) {
        if (!r.ok) return r.text().then(function (t) { throw new Error('HTTP ' + r.status + (t ? ' ' + t.slice(0, 60) : '')); });
        return r.blob();
      });
    }
    if (cfg.mode !== 'minimax') throw new Error('这个供应商要走中转，先填中转地址');
    var u = 'https://api.minimaxi.com/v1/t2a_v2' + (cfg.group ? ('?GroupId=' + encodeURIComponent(cfg.group)) : '');
    return fetch(u, {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'authorization': 'Bearer ' + cfg.key },
      body: JSON.stringify({
        model: modelId(), text: text, stream: false,
        voice_setting: { voice_id: cfg.voice, speed: cfg.speed, vol: 1, pitch: 0 },
        audio_setting: { sample_rate: 32000, bitrate: 128000, format: 'mp3' }
      })
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (!j || !j.data || !j.data.audio) {
        var m = (j && j.base_resp && j.base_resp.status_msg) || '合成失败';
        throw new Error(m);
      }
      return hexBytes(j.data.audio);
    });
  }

  function synth(text) {
    var parts = split(text, 1200), bufs = [], i = 0;
    function step() {
      if (i >= parts.length) return Promise.resolve(new Blob(bufs, { type: 'audio/mpeg' }));
      return one(parts[i++]).then(function (b) { bufs.push(b); return step(); });
    }
    return step();
  }

  /* ---------- 播放器 ---------- */
  var ICO_PLAY = '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.6 2.6v10.8L13.4 8z"/></svg>';
  var ICO_PAUSE = '<svg viewBox="0 0 16 16" fill="currentColor"><rect x="4" y="2.8" width="3" height="10.4" rx="0.8"/><rect x="9" y="2.8" width="3" height="10.4" rx="0.8"/></svg>';
  var ICO_WAIT = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M8 2.2a5.8 5.8 0 1 1-4.1 1.7"/></svg>';

  var el = document.querySelector('.tts');
  var audio = new Audio(), url = null, st = 'idle';

  function paint() {
    if (!el) return;
    el.setAttribute('data-st', st);
    var play = el.querySelector('.tplay'), redo = el.querySelector('.tredo'), dl = el.querySelector('.tdl');
    if (st === 'gen') {
      play.innerHTML = ICO_WAIT; play.classList.add('gen'); play.disabled = true;
      redo.disabled = true; dl.disabled = true;
      el.querySelector('.ttime').textContent = '生成中…';
    } else {
      play.classList.remove('gen');
      play.innerHTML = (st === 'ready' && !audio.paused) ? ICO_PAUSE : ICO_PLAY;
      play.disabled = false;
      redo.disabled = (st !== 'ready');
      dl.disabled = (st !== 'ready');
      if (st === 'idle') el.querySelector('.ttime').textContent = '0:00 / 0:00';
    }
  }

  function drawTime() {
    if (!el) return;
    var dur = audio.duration || 0, cur = audio.currentTime || 0;
    var pct = dur ? (cur / dur) : 0;
    el.querySelector('.tfill').style.width = (pct * 100) + '%';
    el.querySelector('.knot').style.left = (pct * 100) + '%';
    el.querySelector('.ttime').textContent = fmt(cur) + ' / ' + fmt(dur);
  }

  function ready(b) {
    if (url) URL.revokeObjectURL(url);
    url = URL.createObjectURL(b);
    audio.src = url;
    st = 'ready';
    paint();
    audio.play().catch(function () {});
  }

  function need() {
    return !!(cfg.proxy || (cfg.mode === 'minimax' && cfg.key && cfg.voice));
  }

  function ensure(force) {
    if (!need()) { toast('先去设置里填朗读的 key 和音色'); return Promise.resolve(); }
    var data = (typeof READTTS !== 'undefined' && READTTS[+el.getAttribute('data-tts')]) || { id: 'read', text: '' };
    var key = 'tts:' + data.id + '|' + cfg.mode + '|' + modelId() + '|' + cfg.voice + '|' + cfg.speed;
    st = 'gen'; paint();
    var p = force ? Promise.resolve(null) : idbGet(key);
    return p.then(function (b) { return b || synth(data.text).then(function (nb) { return idbSet(key, nb).then(function () { return nb; }); }); })
      .then(function (b) { ready(b); })
      .catch(function (e) { st = url ? 'ready' : 'idle'; paint(); toast('没生成成：' + (e && e.message ? e.message : e)); });
  }

  if (el) {
    paint();
    el.querySelector('.tplay').addEventListener('click', function () {
      if (st === 'gen') return;
      if (st === 'ready') { if (audio.paused) audio.play(); else audio.pause(); return; }
      ensure(false);
    });

    var dlg = document.getElementById('ttsDlg');
    el.querySelector('.tredo').addEventListener('click', function () {
      if (st === 'gen') return;
      if (!need()) { toast('先去设置里填朗读的 key 和音色'); return; }
      dlg.classList.add('on'); dlg.setAttribute('aria-hidden', 'false');
    });
    document.getElementById('ttsNo').addEventListener('click', function () {
      dlg.classList.remove('on'); dlg.setAttribute('aria-hidden', 'true'); toast('已取消重新生成');
    });
    document.getElementById('ttsYes').addEventListener('click', function () {
      dlg.classList.remove('on'); dlg.setAttribute('aria-hidden', 'true');
      toast('正在重新生成，请稍候'); ensure(true);
    });
    document.getElementById('ttsDlgMask').addEventListener('click', function () {
      dlg.classList.remove('on'); dlg.setAttribute('aria-hidden', 'true');
    });

    el.querySelector('.tdl').addEventListener('click', function () {
      if (st !== 'ready' || !url) return;
      var a = document.createElement('a');
      var t = (READTTS[+el.getAttribute('data-tts')] || {}).title || '730pm';
      a.href = url; a.download = t.replace(/[\\/:*?"<>|]/g, '') + '.mp3';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      toast('已下载');
    });

    var bar = el.querySelector('.tbar');
    function seek(ev) {
      if (st !== 'ready' || !audio.duration) return;
      var r = bar.getBoundingClientRect();
      var x = (ev.touches ? ev.touches[0].clientX : ev.clientX) - r.left;
      audio.currentTime = Math.min(1, Math.max(0, x / r.width)) * audio.duration;
    }
    bar.addEventListener('click', seek);
    bar.addEventListener('touchstart', function (e) { seek(e); }, { passive: true });

    audio.addEventListener('timeupdate', drawTime);
    audio.addEventListener('loadedmetadata', drawTime);
    audio.addEventListener('play', paint);
    audio.addEventListener('pause', paint);
    audio.addEventListener('ended', function () { audio.currentTime = 0; paint(); });
  }

  /* ---------- 设置里的朗读段 ---------- */
  var mEl = document.getElementById('ttsMode'), mdEl = document.getElementById('ttsModel'), kEl = document.getElementById('ttsKey'),
      gEl = document.getElementById('ttsGroup'), vEl = document.getElementById('ttsVoice'),
      pEl = document.getElementById('ttsProxy'), sEl = document.getElementById('ttsSpeed'),
      spEl = document.getElementById('ttsSpd');
  function readForm() {
    if (!mEl) return;
    cfg.mode = mEl.value; cfg.model = mdEl.value.trim(); cfg.key = kEl.value.trim(); cfg.group = gEl.value.trim();
    cfg.voice = vEl.value.trim(); cfg.proxy = pEl.value.trim(); cfg.speed = parseFloat(sEl.value) || 1;
    if (spEl) spEl.textContent = cfg.speed.toFixed(2) + '×';
    saveCfg(); if (st === 'ready') paint();
  }
  if (mEl) {
    mEl.value = cfg.mode; mdEl.value = cfg.model; kEl.value = cfg.key; gEl.value = cfg.group;
    vEl.value = cfg.voice; pEl.value = cfg.proxy; sEl.value = cfg.speed;
    if (spEl) spEl.textContent = (+cfg.speed).toFixed(2) + '×';
    [mEl, mdEl, kEl, gEl, vEl, pEl].forEach(function (x) {
      x.addEventListener('change', readForm);
      x.addEventListener('input', readForm);
      x.addEventListener('blur', readForm);
    });
    sEl.addEventListener('input', readForm);
  }
})();
