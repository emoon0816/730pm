import json, hashlib, os, sys

DP = '/home/admin/newspaper/data.json'
PP = '/home/admin/newspaper/.thing_payload.json'

raw = open(DP, 'rb').read()
h = hashlib.md5(raw).hexdigest()
d = json.loads(raw.decode('utf-8'))
new = json.load(open(PP, encoding='utf-8'))

tabs = d['tabs']
idx = [i for i, t in enumerate(tabs) if t.get('id') == 'thing']
assert len(idx) == 1, idx
tab = tabs[idx[0]]
assert tab.get('name') == '每日识物' and 'thing' in tab and 'groups' not in tab, list(tab.keys())
old_title = tab['thing'].get('title')

print('标题字数', len(new['title']), '｜kicker字数', len(new['kicker']))
print('段数', len(new['body']), '段长', [len(p) for p in new['body']])
print('facts数', len(new['facts']), 'k长', [len(f['k']) for f in new['facts']], 'v长', [len(f['v']) for f in new['facts']])
print('u', new['u'])
for k in ('title', 'kicker', 'body', 'facts', 'u'):
    assert new.get(k), 'missing ' + k

tab['thing'] = new
out = json.dumps(d, ensure_ascii=False, indent=1)

cur = open(DP, 'rb').read()
if hashlib.md5(cur).hexdigest() != h:
    print('ABORT: data.json 在读写之间被别的任务改过')
    sys.exit(2)

tmp = DP + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(out)
os.replace(tmp, DP)
print('写回完成，旧标题：', old_title)
