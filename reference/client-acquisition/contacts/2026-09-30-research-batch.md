# 2026-09-30 — research-only batch (hook-verification gate held, no Funnel letter assigned)

**Run type:** research/shortlist only. The drafts gate was CLEAR this run — `gmail/v1/users/me/drafts` (`resultSizeEstimate`, via FGAC, `spencer@spencerzvoice.com` confirmed in `list_accounts`) returned **0** — but nothing got drafted anyway, for a different reason: **WebFetch is completely egress-blocked in this session.** Every one of 10 companies below cleared Apollo sourcing (primary + verified backup, verified email) but failed the mandatory current-event-hook check, because there was no way to open a single primary source to verify one. Per the routine's own rule ("if nothing current and verifiable turns up, use NO hook line... list the contact under HOOK NEEDED"), all 10 are BANKED, not drafted, and no Funnel letter is assigned.

**The blocker, precisely:** 5 parallel subagents (WebSearch + WebFetch only, no browser) each tried to verify a hook for 2 companies. All 5 independently hit `EGRESS_BLOCKED` on every general-web domain attempted — company newsrooms, PR Newswire, GlobeNewswire, BusinessWire, Nasdaq, Yahoo Finance, StockTitan, Wikipedia, Adweek, WWD, Retail Dive, Tearsheet, theorg.com, RevOps FM, even `google.com` and `example.com` — roughly 80 distinct domains across the 5 agents, zero successes except `anthropic.com`. I independently re-tested `vuoriclothing.com/pages/press` myself afterward and got the identical `EGRESS_BLOCKED` response. Checked `$HTTPS_PROXY/__agentproxy/status` and `/root/.ccr/README.md`: this matches the "403/407 from the proxy... destination host is not allowed by your organization's egress policy for this session — do not retry or route around it, report the blocked host" failure class, not a transient fault. **This session's network policy currently allows essentially no open-web fetching** — WebSearch (snippets) still works, but a snippet is explicitly not an acceptable source under this routine's own rules, so nothing here could be certified.

**Action needed from Spencer/whoever configures this environment:** if the daily lead-batch routine is meant to keep doing hook verification from the cloud, this session's environment needs an egress policy that allows WebFetch to reach ordinary company newsrooms/press pages and trade press — right now it can reach almost nothing. Until that's fixed, this routine can source and verify contacts (Apollo) but cannot verify hooks, so it will keep banking companies without drafting them.

**Data source note:** built from this repo's own `ROSTER.md` / `FUNNEL-COHORTS.md` / tracker Sheet as instructed (not the claude.ai Project's Drive mirror).

Exclusions checked: repo `ROSTER.md` (all sections, 171 companies), repo `FUNNEL-COHORTS.md` (through Funnel F), tracker Sheet columns A–C (full read, ~172 rows), and existing clients (AWS/Amazon, Venmo, Dell, Cisco, Brave, FootJoy, Artlist, VoiceArchive). None of the 10 companies below appear in any of those.

---

## Enterprise and business software

### Pegasystems — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Liz Colanto, Head of Post, Lead Video Editor — liz.colanto@pega.com, Apollo-verified. Strongest title in this batch (post supervision owns the audio chain).
- **Backup:** Carlos Perez, Global Creative Director — carlos.perez@pega.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked (see note above).** WebSearch surfaced an unconfirmed candidate: Pegasystems reportedly named a Leader in Gartner's Magic Quadrant for Business Orchestration and Automation Technology (~2026-09-21, mirrored on Nasdaq/GlobeNewswire/aithority per search) — not opened, not verified, do not use until someone can actually read pega.com/about/news or the press release directly.

### Anaplan — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Georgina Lipovac, Senior Creative Director — email returned as **georgina.brown@anaplan.com**, Apollo-verified but the prefix doesn't match the surname (likely a legacy/maiden-name alias, same pattern flagged before with Amy McWilliams at Marqeta) — flagged, not fabricated.
- **Backup:** Jamieson Copeland, Sr. Video, Events and Content Producer — jamieson.copeland@anaplan.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** WebSearch is actively unreliable here — one hit claimed an "Anaplan acquires Syrup Tech" story dated 2026-09-24, a follow-up search on the same story pointed to a source dated 2025-09-09 (a full year earlier, likely mis-surfaced). Do not use. A "new brand identity" story that also surfaced is confirmed stale (Feb 2025).

### Freshworks — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Pete Anderson, Executive Producer — pete.anderson@freshworks.com, Apollo-verified. **⚠️ Title flag:** WebSearch (unverified, could not open) surfaced a podcast/bio suggesting a "Pete Anderson" at Freshworks may currently hold the title "Global Video Lead" rather than Executive Producer, alongside a Robyn Swierk (Senior Creative Program Manager) — unclear if this is the same person or a stale/different reference. Re-verify title before drafting.
- **Backup:** Mark Girgis, Creative Director, Brand — mark.girgis@freshworks.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** WebSearch surfaced Freshworks' "The Works" blog post "Freshworks September 2026 Innovation Update" (Freddy AI Copilot, MCP Gateway, AI Agent Studio) — plausible, not opened, not dated by me.

## Cybersecurity vendors

### Fortinet — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Brian Kirby, Senior Video Production Manager — bkirby@fortinet.com, Apollo-verified
- **Backup:** William Yeung, Video Producer — yeungw@fortinet.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** Best unverified candidate: a Fortinet–Stanford Athletics multi-year sponsorship (stadium naming rights + endzone branding), reportedly announced 2026-08-28 across several outlets — closest thing to a real, dated, non-political hook in this whole batch, but zero primary-source confirmation. First thing to check once fetch access works: `fortinet.com/corporate/about-us/newsroom/press-releases/2026/stanford-athletics-and-fortinet-team-up-for-multi-year-sponsorship`.

### Check Point Software — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Lia Lerer, Head of Video Production — lial@checkpoint.com, Apollo-verified
- **Backup:** Johnny Thompson, Creative Director — Apollo `email_status: unavailable`, no address found
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** Unverified candidate: Check Point reportedly named a Leader in Gartner's 2026 Magic Quadrant for Hybrid Mesh Firewall (~2026-09-10, tied to a new "AI Network Firewall"). Not opened, not confirmed.

### Arctic Wolf — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Erin Russell, Senior Director, Creative — erin.russell@arcticwolf.com, Apollo-verified. Strong title match.
- **Backup:** Katie Garske, Senior Manager, Content Marketing — Apollo `email_status: unavailable`, no address found
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** Unverified candidate: Arctic Wolf reportedly launched "Aurora MDR Connect" (~2026-09-15) per GlobeNewswire/MSSP Alert/Channel Insider search hits. Not opened, not confirmed.

## Consumer brands and travel

### Vuori — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Mark Tesi, Creative Director — mtesi@vuoriclothing.com, Apollo-verified
- **Backup:** Daniella Carrera, Senior Manager, Creative Production — daniella.carrera@vuori.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked** (confirmed independently by me re-testing `vuoriclothing.com/pages/press` after the subagent report — same `EGRESS_BLOCKED`). Unverified candidates from search only: "For Kaia" (Spring 2026, Kaia Gerber), "The Sunday Collection" (NFL players Goff/Loveland/Hampton), a Tom Holland golf campaign, a Jack Draper "Hardkore Shorts" campaign (WWD headline) — none dated or confirmed, none tied to Mark Tesi personally.

## Fintech and payments

### Plaid — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Heather Mounsey, Head of Brand and Creative — hmounsey@plaid.com, Apollo-verified
- **Backup:** Linda Eliasen, Head of Creative — leliasen@plaid.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** Most promising unverified lead in this batch: search surfaced a Tearsheet.co piece ("...Plaid's Heads of Creative and Design break down the firm's recent rebrand," "The fabric of financial progress") apparently quoting Heather Mounsey directly ("We've been inventing new possibilities in finance for over 12 years, it was time to reinvent ourselves") — but I could not open `plaid.com` or `tearsheet.co` to confirm the quote, get the actual date, or check it's within the ~30-60 day window (Money 20/20 USA was referenced as the reveal venue in one snippet, timing unconfirmed). **First thing to check once fetch access works.**

### Ramp — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Paul Jun, Creative Director, Brand — paul.jun@ramp.com, Apollo-verified
- **Backup:** Karly Snajczuk, Senior Creative Producer — karly.snajczuk@ramp.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** Unverified candidates: "Ramp Accounts Receivable" launch (~2026-09-22) and a UK market launch (~2026-09-15) per search only. Not opened, not confirmed.

## Corporate L&D and LMS software

### Litmos — apollo.mixed_people_api_search, enriched via bulk_match
- **Primary:** Thao Ngo, Head of Brand and Marketing Activation — thao.ngo@litmos.com, Apollo-verified
- **Backup:** Nikki Yttermalm, Event Marketing Manager — nikki.yttermalm@litmos.com, Apollo-verified
- **Hook: HOOK NEEDED — could not verify, WebFetch blocked.** A RevOps FM podcast episode titled "Playbook of a High-Performing Marketing Leader – Thao Ngo" surfaced in search — undated, not opened, not confirmed as recent.

---

## Apollo spend this run

20 lead credits (bulk-match enrichment on 10 primary + 10 backup contacts). Balance before: 2,183. Balance after: ~2,163 (of a 2,555 monthly cycle limit, resets 2026-10-03). No export/direct-dial/waterfall credits used.

## Held / not pursued this run

Weaker or single-contact cards found in the same sweeps, not carried forward: Whatfix, Kallidus, Trainual, iSpring Solutions (Corporate L&D — all generalist "Marketing Manager" titles, no creative-director/producer-level contact), Coupa, Pendo.io (Enterprise software — weaker titles than the four chosen), Cybereason, Abnormal AI (Cybersecurity — single usable contact or content-marketing-only titles), Honeycomb, Temporal Technologies, Supabase, Redis, Warp (Developer/infra — DevRel-only or single-contact, no clean backup pairing), Glossier (Consumer brands — single contact, no backup found), away.com, chubbiesshorts.com (zero Apollo results under either title set).

## Method note for future runs

**WebFetch/general web access is unavailable in this cloud session as of 2026-09-30** — confirmed by 5 independent subagents plus a direct retest, ~80+ domains tried, all `EGRESS_BLOCKED` except `anthropic.com`. Per `/root/.ccr/README.md` this reads as an organization egress-policy denial, not a transient fault — don't keep re-attempting it in future runs without checking whether the policy has changed. WebSearch still works but its snippets are not an acceptable hook source under this routine's own rules.
