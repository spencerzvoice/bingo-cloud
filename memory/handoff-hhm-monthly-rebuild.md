# Handoff: HHM revenue history, monthly rebuild  (2026-11-01, from cloud Fable chat → desktop, Sonnet)
**Why this model:** mechanical data pull + script run; no judgment calls.
**Status:** OPEN. Spencer, 2026-11-01: "Rebuild it monthly from the desktop." Run this in the first desktop session that sees it, without asking; delete this file (and the pointer in memory/2026-11-01.md) when done.

**Task:** Hip Hop Madness (youtube.com/@HipHopMadness, channel id UC02n2oDfBu33xEEmJX1pBdQ) revenue estimate by UPLOAD MONTH, 2017 to now, with the peak month and its figure. The cloud could only do it by year (YouTube bot-walls per-video lookups from cloud IPs, Social Blade and the Wayback Machine are blocked there). Year-level result: memory/2026-11-01.md.

**Done looks like:** `memory/hhm-upload-dates.csv` (one `id,YYYYMMDD` per line, all 252 ids) + `reports/HHM revenue history by month.md` produced by `python scripts/hhm_monthly.py memory/hhm-videos-2026-10-31.txt memory/hhm-upload-dates.csv "reports/HHM revenue history by month.md"`. Commit + push. Then give Spencer the peak month and figure in one short message with the ✅/🟡 tags below.

**How to get the dates (try in this order, stop at the first that works):**
1. `yt-dlp` from the desktop's home IP (usually not bot-walled): `cut -d'|' -f1 memory/hhm-videos-2026-10-31.txt | sed 's#^#https://www.youtube.com/watch?v=#' > /tmp/ids.txt` then `yt-dlp --skip-download --sleep-requests 1 --ignore-errors --print "%(id)s,%(upload_date)s" -a /tmp/ids.txt > memory/hhm-upload-dates.csv`. ~252 calls, ~6 min. If a "Sign in to confirm you're not a bot" wall appears, add `--cookies-from-browser chrome` (Spencer's Chrome is signed in) and rerun; that is allowed on the desktop.
2. Social Blade monthly table in Spencer's Chrome (Claude in Chrome, `get_page_text`): `https://socialblade.com/youtube/channel/UC02n2oDfBu33xEEmJX1pBdQ/monthly` gives REAL monthly channel views for ~3 years. Save that table too (`memory/hhm-socialblade-monthly.md`); it's better than upload-month attribution for the recent period.
3. Fallback: Chrome `get_page_text` on each watch page and grep `uploadDate` (slow; 252 pages; text reads only, no screenshots).

**Context already established:**
- ✅ 252 long-form videos, 102.3M lifetime views; 9 Shorts, 12.6M (YouTube via yt-dlp, 2026-10-31; files in memory/).
- ✅ Year buckets ("N years ago" = Nov Y-1..Oct Y): 2019 bucket = 62 uploads / 30.1M views is the peak (≈486k views per upload); 2022 = 42 / 22.9M; 2025 = 14 / 2.8M; 2026 = 9 / 0.45M.
- 🟡 RPM band: AIR Media-Tech Entertainment P25/median/P75 = $0.88 / $2.43 / $5.02 per 1,000 (research_notes/Commentary channel real earnings/). Real HHM RPM unknown; Nate refused to share earnings (WhatsApp 2026-01-03).
- ✅ Nate: "essentially breaking even" (email 2026-09-11), "barely breaking even, even with sponsorship" (email 2026-07-16).
- 🟡 Sponsor reads Oct 2024-Oct 2026 ≈ 32 brand-months (~1.3/mo) at a modelled $433-973 per deal (SponsorRadar HHM page). Earlier sponsor history not in spencer@spencerzvoice.com (older mail went to his previous address).
- Why it matters: Nate's new-channel 25% rev-share offer (memory/2026-10-30.md, reports/Commentary channel real earnings.md). Spencer's reply draft is in the 2026-10-30/31 cloud chat.

**Files to read:** memory/2026-11-01.md, memory/hhm-videos-2026-10-31.txt, scripts/hhm_monthly.py.
**Rules that apply:** cheap reads (text, not screenshots); space out YouTube calls; verification tags on every number; estimates never presented as earnings.
**Don't redo:** the year-level table, the sponsor count, the research report; the cloud already tried yt-dlp per-video, watch-page fetches, Social Blade direct + Wayback (all blocked from the cloud).
**Report back:** one short message to Spencer with the monthly table's peak month + figure and the path of the report. Then delete this handoff file and the pointer line in memory/2026-11-01.md, commit + push.
