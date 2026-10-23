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
"Link shares" (Spencer, 2026-10-23): when someone pastes the site into LinkedIn, Slack, Teams, iMessage, WhatsApp etc.,
that app's preview bot fetches the page to build the card. Those rows are listed on their own: a share, not a visit.
"""
import json
import re
import sys
from collections import OrderedDict

HOME_NETS = ("PT Comunicacoes", "NOS", "Vodafone", "NOWO", "MEO")
# Preview bot -> the app the link was pasted into. Order matters: iMessage's UA also carries facebookexternalhit/Twitterbot.
PREVIEWS = [("Facebot Twitterbot", "iMessage"), ("LinkedInBot", "LinkedIn"), ("Slackbot", "Slack"),
            ("SkypeUriPreview", "Teams/Skype"), ("MicrosoftPreview", "Teams/Outlook"), ("WhatsApp", "WhatsApp"),
            ("TelegramBot", "Telegram"), ("Discordbot", "Discord"), ("facebookexternalhit", "Facebook/Instagram/Messenger"),
            ("Twitterbot", "X"), ("Pinterestbot", "Pinterest"), ("redditbot", "Reddit"), ("Snap URL Preview", "Snapchat"),
            ("Viber", "Viber"), ("Embedly", "Embedly (Notion/Medium etc.)"), ("Iframely", "Iframely (Notion etc.)")]


def share_app(ua):
    return next((app for key, app in PREVIEWS if key.lower() in (ua or "").lower()), None)


# Cloud/hosting networks: scanners and crawlers that send a normal browser UA (first real day, 10-22: Tencent, Oracle,
# Google LLC page tours, Vultr = "The Constant Company", Alibaba = "COLLYER QUAY", an AWS-credential probe from TECHOFF).
# People don't browse from a datacenter, so these are hidden like bots. Corporate proxies (Zscaler etc.) stay visible.
HOSTING = re.compile(r"cloud|hosting|host\b|server|data ?cent|colo|vps|tencent|alibaba|amazon|google llc|microsoft|oracle|"
                     r"fastly|cloudflare|akamai|digitalocean|linode|ovh|hetzner|constant company|vultr|choopa|collyer quay|"
                     r"m247|leaseweb|contabo|palo alto|censys|shodan|techoff|virtualine|aceville|techties|limited network|"
                     r"global business consulting|truview|unmanaged ltd|internet invest|atlas network", re.I)

sys.stdout.reconfigure(encoding="utf-8")  # python -I ignores PYTHONIOENCODING; city names carry accents

days = int(next((a for a in sys.argv[1:] if a.isdigit()), 7))
bots = "--bots" in sys.argv
raw = sys.stdin.buffer.read().decode("utf-8", "replace")
try:
    rows = json.loads(raw)[0]["results"]
except (ValueError, IndexError, KeyError, TypeError):
    sys.exit(f"wrangler failed:\n{raw[-1500:]}")

shares, visitors, hidden = [], OrderedDict(), 0
for r in rows:
    # Checked on the UA, not the bot flag: the Worker's bot regex misses facebookexternalhit and WhatsApp.
    app = share_app(r["ua"])
    if app:
        shares.append((r, app))
        continue
    if HOSTING.search(r["as_org"] or ""):
        r = {**r, "bot": 1}
    if r["bot"] and not bots:
        hidden += 1
        continue
    key = (r["ts"][:10], r["visitor"])
    v = visitors.setdefault(key, {**r, "pages": []})
    v["pages"].append(r["path"] + (r["query"] or ""))
    if not v["referer"] and r["referer"] and "spencerzvoice.com" not in r["referer"]:
        v["referer"] = r["referer"]

views = sum(len(v["pages"]) for v in visitors.values())
print(f"spencerzvoice.com, last {days} days: {len(visitors)} visitors, {views} page views{' (bots included)' if bots else ''}, "
      f"{len(shares)} link shares{'' if bots else f'; {hidden} bot/cloud-server hits hidden (--bots shows them)'}")
for v in visitors.values():
    place = ", ".join(x for x in (v["city"], v["region"], v["country"]) if x)
    net = v["as_org"] or "unknown network"
    you = "  (probably you)" if v["city"] == "Lisbon" and net.startswith(HOME_NETS) else ""
    ref = v["referer"] if v["referer"] and "spencerzvoice.com" not in v["referer"] else "direct/email"
    print(f"{v['ts'][:16].replace('T', ' ')}  {net}  |  {place}  |  from {ref}  |  {len(v['pages'])}p: {' '.join(v['pages'][:6])}"
          f"{'  [BOT]' if v['bot'] else ''}{you}")
if shares:
    print("\nLink shares (someone pasted your link into an app; the network is the app's server, not the person):")
    for r, app in shares:
        print(f"{r['ts'][:16].replace('T', ' ')}  {app}  |  {r['path']}{r['query'] or ''}")
