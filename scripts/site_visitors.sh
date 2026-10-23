#!/bin/bash
# Who visited spencerzvoice.com: reads the Worker's D1 visitor log and prints one line per visitor. Details: site_visitors.py.
# Usage: bash scripts/site_visitors.sh [days=7] [--bots]
days=${1:-7}
[[ "$days" =~ ^[0-9]+$ ]] || days=7
here=$(cd "$(dirname "$0")" && pwd)
cd /c/Users/spenc/spencerzvoice-site/builds/spencerzvoice || exit 1
npx wrangler d1 execute spencerzvoice-visitors --remote --json --command \
  "SELECT ts, path, query, referer, country, region, city, as_org, ua, bot, visitor FROM visits WHERE ts >= datetime('now', '-$days days') ORDER BY ts" 2>/dev/null \
  | PYTHONIOENCODING=utf-8 python -I "$here/site_visitors.py" "$@"
