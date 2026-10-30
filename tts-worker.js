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

function b64ToBytes(b64) {
  const bin = atob(b64);
  const u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
  return u;
}

// 火山豆包：key 走 X-Api-Key，浏览器预检不放行这个头，所以只能在中转里做
// 返回是 NDJSON，每行一条，audio 在 data 字段里，base64
async function volc({ key, model, voice, speed, text }) {
  const r = await fetch('https://openspeech.bytedance.com/api/v3/tts/unidirectional', {
    method: 'POST',
    headers: {
      'X-Api-Key': key,
      'X-Api-Resource-Id': model || 'seed-tts-2.0',
      'X-Api-Request-Id': crypto.randomUUID(),
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      req_params: {
        text,
        speaker: voice || 'zh_female_vv_uranus_bigtts',
        audio_params: { format: 'mp3', speech_rate: Math.round((Number(speed || 1) - 1) * 100) },
      },
    }),
  });
  if (!r.ok) {
    return new Response(await r.text(), { status: r.status, headers: { ...CORS, 'content-type': 'application/json' } });
  }
  const txt = await r.text();
  const parts = [];
  for (const line of txt.split('\n')) {
    const s = line.trim();
    if (!s) continue;
    let j;
    try { j = JSON.parse(s); } catch { continue; }
    if (j.code && j.code !== 0 && j.code !== 20000000) {
      return json({ error: j.message || ('volc code ' + j.code) }, 400);
    }
    if (j.data) parts.push(j.data);
  }
  if (!parts.length) return json({ error: 'volc returned no audio' }, 400);
  return new Response(b64ToBytes(parts.join('')), { headers: { ...CORS, 'content-type': 'audio/mpeg' } });
}

// ElevenLabs：本来就能浏览器直连，走中转也行
async function eleven({ key, model, voice, text }) {
  const u = `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voice || '21m00Tcm4TlvDq8ikWAM')}?output_format=mp3_44100_128`;
  const r = await fetch(u, {
    method: 'POST',
    headers: { 'xi-api-key': key, 'content-type': 'application/json' },
    body: JSON.stringify({ text, model_id: model || 'eleven_multilingual_v2', voice_settings: { stability: 0.5, similarity_boost: 0.75 } }),
  });
  if (!r.ok) return new Response(await r.text(), { status: r.status, headers: { ...CORS, 'content-type': 'application/json' } });
  return new Response(r.body, { headers: { ...CORS, 'content-type': 'audio/mpeg' } });
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
    if (p.provider === 'volc') return volc({ ...p, key });
    if (p.provider === 'eleven') return eleven({ ...p, key });
    return json({ error: 'unknown provider: ' + p.provider }, 400);
  },
};
