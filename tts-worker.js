// 730pm 朗读中转 · Cloudflare Worker
// 前端 POST JSON -> 这里转发给 Fish / MiniMax -> 回二进制音频
// key 由前端传，Worker 不存、不记日志

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'authorization, content-type',
  'Access-Control-Max-Age': '86400',
};

function json(obj, status = 400) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { ...CORS, 'content-type': 'application/json' },
  });
}

async function fish({ key, model, voice, speed, text }) {
  const h = { authorization: `Bearer ${key}`, 'content-type': 'application/json' };
  // Fish 的模型名走请求头，不在 body 里
  if (model) h.model = model;
  const body = {
    text,
    format: 'mp3',
    mp3_bitrate: 128,
    chunk_length: 200,
    normalize: true,
  };
  if (voice) body.reference_id = voice;
  if (speed && speed !== 1) body.prosody = { speed };

  const r = await fetch('https://api.fish.audio/v1/tts', {
    method: 'POST',
    headers: h,
    body: JSON.stringify(body),
  });
  if (!r.ok) return new Response(await r.text(), { status: r.status, headers: { ...CORS, 'content-type': 'application/json' } });
  return new Response(r.body, { headers: { ...CORS, 'content-type': 'audio/mpeg' } });
}

async function minimax({ key, group, model, voice, speed, text }) {
  const u = `https://api.minimaxi.com/v1/t2a_v2${group ? `?GroupId=${encodeURIComponent(group)}` : ''}`;
  const r = await fetch(u, {
    method: 'POST',
    headers: { authorization: `Bearer ${key}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      model: model || 'speech-2.6-hd',
      text,
      stream: false,
      voice_setting: { voice_id: voice || 'female-shaonv', speed: speed || 1, vol: 1, pitch: 0 },
      audio_setting: { sample_rate: 32000, bitrate: 128000, format: 'mp3' },
    }),
  });
  const j = await r.json();
  if (!j?.data?.audio) return json({ error: j?.base_resp?.status_msg || 'minimax failed' }, 400);
  const bin = Uint8Array.from(j.data.audio.match(/../g).map((x) => parseInt(x, 16)));
  return new Response(bin, { headers: { ...CORS, 'content-type': 'audio/mpeg' } });
}

export default {
  async fetch(req) {
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (req.method !== 'POST') return json({ error: 'POST only' }, 405);

    let p;
    try { p = await req.json(); } catch { return json({ error: 'bad json' }, 400); }

    const auth = req.headers.get('authorization') || '';
    const key = (p.key || auth.replace(/^Bearer\s+/i, '') || '').trim();
    if (!key) return json({ error: 'missing api key' }, 400);
    if (!p.text || !String(p.text).trim()) return json({ error: 'missing text' }, 400);

    if (p.provider === 'fish') return fish({ ...p, key });
    if (p.provider === 'minimax') return minimax({ ...p, key });
    return json({ error: 'unknown provider: ' + p.provider }, 400);
  },
};
