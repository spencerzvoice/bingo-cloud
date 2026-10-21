"""Who visited spencerzvoice.com (Spencer, 2026-10-22: "add free visitor logging to the site Worker so we can see company
networks going forward").

Why: Cloudflare's free plan shows visit counts but not who; its GraphQL refuses the network (ASN) and referrer fields.
Since 2026-10-22 the site Worker (spencerzvoice-site/builds/spencerzvoice/worker.js) writes one row per page view to the
D1 database "spencerzvoice-visitors": path, referrer, city, country, network (cf.asOrganization) and browser. No raw IP.
On an office connection the network IS the company (e.g. "Hitachi Rail"); at home it's an ISP (Comcast, MEO...).

Usage (desktop, wrangler signed in to the personal Cloudflare account), always through the shell wrapper:
    bash scripts/site_visitors.sh            # last 7 days, people only
    bash scripts/site_visitors.sh 30         # last 30 days
    bash scripts/site_visitors.sh 7 --bots   # include crawlers
The wrapper runs wrangler and pipes the JSON here: this machine's Python (install-manager build) runs with a virtualized
AppData and can't see wrangler's login, so wrangler can't be called from Python (found 2026-10-22).
One line per visitor per day: first time (UTC), pages, city/country, network, where they came from.
Lisbon on PT Comunicacoes/NOS/Vodafone/NOWO is flagged "(probably you)": Spencer's own visits land there too.
"""
import json
import sys
from collections import OrderedDict

HOME_NETS = ("PT Comunicacoes", "NOS", "Vodafone", "NOWO", "MEO")

days = int(next((a for a in sys.argv[1:] if a.isdigit()), 7))
bots = "--bots" in sys.argv
raw = sys.stdin.buffer.read().decode("utf-8", "replace")
try:
    rows = json.loads(raw)[0]["results"]
except (ValueError, IndexError, KeyError, TypeError):
    sys.exit(f"wrangler failed:\n{raw[-1500:]}")

visitors = OrderedDict()
for r in rows:
    key = (r["ts"][:10], r["visitor"])
    v = visitors.setdefault(key, {**r, "pages": []})
    v["pages"].append(r["path"] + (r["query"] or ""))
    if not v["referer"] and r["referer"] and "spencerzvoice.com" not in r["referer"]:
        v["referer"] = r["referer"]

print(f"spencerzvoice.com, last {days} days: {len(visitors)} visitors, {len(rows)} page views{' (bots included)' if bots else ''}")
for v in visitors.values():
    place = ", ".join(x for x in (v["city"], v["region"], v["country"]) if x)
    net = v["as_org"] or "unknown network"
    you = "  (probably you)" if v["city"] == "Lisbon" and net.startswith(HOME_NETS) else ""
    ref = v["referer"] if v["referer"] and "spencerzvoice.com" not in v["referer"] else "direct/email"
    print(f"{v['ts'][:16].replace('T', ' ')}  {net}  |  {place}  |  from {ref}  |  {len(v['pages'])}p: {' '.join(v['pages'][:6])}"
          f"{'  [BOT]' if v['bot'] else ''}{you}")
