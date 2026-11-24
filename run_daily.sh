#!/bin/bash
# 730pm 每日出报 —— 服务器侧兜底（GitHub 的 schedule 靠不住）
set -uo pipefail
cd /home/admin/newspaper
mkdir -p logs

if [ -f .env ]; then set -a; . ./.env; set +a; fi
if [ -z "${DEEPSEEK_API_KEY:-}" ]; then
  echo "[$(date '+%F %T')] 缺 DEEPSEEK_API_KEY，未出报" >> logs/cron.log
  exit 1
fi

TODAY=$(TZ=Asia/Shanghai date '+%Y年%-m月%-d日')

if python3 - "$TODAY" <<'PY'
import json, sys
d = json.load(open("data.json", encoding="utf-8"))
sys.exit(0 if (d.get("date") or "").strip() == sys.argv[1] else 1)
PY
then
  echo "[$(date '+%F %T')] 今天已出（$TODAY），跳过" >> logs/cron.log
  exit 0
fi

echo "[$(date '+%F %T')] 开始出报 $TODAY" >> logs/cron.log
python3 scripts/build_daily.py --no-push >> logs/cron.log 2>&1 || { echo "[$(date '+%F %T')] build_daily 失败" >> logs/cron.log; exit 1; }
python3 archive.py --no-prune >> logs/cron.log 2>&1
python3 build.py >> logs/cron.log 2>&1

git add -A
if git diff --staged --quiet; then
  echo "[$(date '+%F %T')] 无改动" >> logs/cron.log
else
  git commit -q -m "daily: $(TZ=Asia/Shanghai date +%F)"
  git push -q && echo "[$(date '+%F %T')] 已推送" >> logs/cron.log
fi
