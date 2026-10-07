# Reference — VO Outreach Pipeline Tracker

The live CRM for Spencer's outreach. **The Google Sheet is ground truth** — Spencer edits it in real time and a daily cloud routine ([[vo-pipeline-routine]]) syncs it from Gmail. This file captures the stable structure, the operational hazards, and the standing action items. Client backgrounds are in [[vo-client-directory]].

## Resource IDs

- Sheet: **"VO Outreach Pipeline Tracker"** — root of My Drive (search by exact title, never a cached link — the file has been deleted/recreated before).
- spreadsheetId: `1SBauz4dCodqnfSVD5yqKETjU-25TY5HEZ7KRGggbgT0`
- Tabs: **Outreach Tracker** (sheetId `1117682425`, the CRM) · **Dashboard** (sheetId `777610067`, formula rollups + chart `445011089`) · **Legend & How To Use** (sheetId `792717929`).
- Gmail account swept: spencer@spencerzvoice.com only.

## Column schema (A–M)

`Contact Name | Company/Agency | Title/Role | Email Address | Category | Priority | Status | Date First Contacted | Last Contact Date | Days Since Last Contact | Follow-Up Flag | Next Action | Notes`

- **Category:** New Outreach - Agency · Active / Recurring Client · Old Client Reconnect · Professional Development
- **Priority:** High (red) · Medium (yellow/orange) · Low (green)
- **Days Since Last Contact** = formula `=IF(I{row}="","",TODAY()-I{row})` — leave alone
- **Follow-Up Flag** = formula. Logic: Bounced→"Fix Email & Resend"; Responded→"Active - Monitor"; Not Sent→"Send Initial Outreach"; Drafted-Not-Sent→"Ready to Send"; else by days: ≥10→"OVERDUE - Follow Up Now", ≥7→"Due Soon", else "Recently Contacted". Leave alone.
- The routine only writes **Status, Last Contact Date, Notes** (and adds rows). Dashboard and Legend tabs are never touched.

## ⚠️ Operational hazards (learned the hard way)

1. **Never write to a row from a remembered row number.** Re-read that row's Name/Company in the same turn before writing, then read it back after to confirm. The sheet grows and shifts; rows have been deleted unexpectedly.
2. **The cloud routine has silently deleted whole rows** (Robert Salas / GMR Marketing, Andy Roth / VO Coach) — not edits, row removal, no error. Root cause unknown. Treat row structure as unstable between sessions.
3. **Real write mistakes that happened:** Erick Sosa's LinkedIn data written into Maya Roberts' row; an OOO note for Michael MacMillan written into Didi Fraioli's row. Both from trusting stale row positions. Hence rule 1.
4. **Standard Gmail connector is buggy** (stale/incomplete thread results — hid 9+ messages of the live KU project once). Use **FGAC.ai** `google_api_get` against `gmail/v1/users/me/...` for anything accuracy-sensitive.
5. **FGAC has blanket permission** — never ask before using it. But FGAC's own `sheets_edit` scope (needed for structural `batchUpdate` / row deletion) can return "No approval received" — a real gate on FGAC's side, not something to retry past. Workaround for row deletion without `sheets_edit`: read the full range, filter rows in memory, rewrite kept rows to the top via `sheets_update_range`, blank the trailing rows.
6. **NEVER put Voices.com / Bodalgo / Voice123 marketplace work in the tracker** — not auditions, not private invites, not even a booked-and-paid job. No exceptions, no manual carve-outs. Spencer manages marketplace work on the platform itself. **Delivered marketplace jobs belong in `vo-client-directory.md` + the invoice log, NOT here.** (History: a "he may still add Zulubot Bravo Inc manually" carve-out here + a "recurring client" line in MEMORY.md let the daily routine re-add Zulubot every morning from the job-award emails in his personal Gmail. Deleted for good 2026-09-02; routine Step 4 now hard-blocks it.)

## Pipeline snapshot
Retired in the 2026-10-06 prune. The Sheet is the roster; don't keep a copy here.

## Live leads & jobs in flight
_Auto-logged (see the memory protocol in CLAUDE.md). Keep status lines current. Pruned 2026-10-06: resolved/cold items are one-liners under "Resolved / cold"; full history is in git (`git log -p reference/outreach-pipeline.md`) and the dated `memory/` logs._

- **Altra Running: Tyler Gorky (Global Creative Producer) + Dani Coplen (Global Creative Director), LIVE.** "15 Year Sizzle VO" internal video, 480 words, booked at **$900** (usage: VF brand 1 yr, Internal + Web + Social organic, Global; exclusivity = the recording only, so no FootJoy/Fabletics conflict; includes the 30-min directed session). Session done Mon 10-05. Takes + Wise pay link sent 10-05; Paul Hartner: "This is great, thank you again!" Payment ❓ not confirmed. Earlier Altra work came through producer Lilah Kohlman (Run Spot Aug 2025 $2,200; Torin 9 2026 $3,200). **Next: retainer email to Tyler + Dani, Thu 10-08 ~9:30am MDT (16:30 Lisbon).** 6-month prepaid credit: Option 1 $750/mo = $900 credit, Option 2 $1,500/mo = $1,800 credit. Floor = Option 1; fallback = preferred-vendor rate sheet with no fee (the KU model). Observed spend ≈ $450/mo, so Option 2 is a stretch. Detail: `memory/2026-10-06.md`. RESEARCH 10-07 (Spencer's goal: build toward ~EUR5,000/mo from Altra/VF): EUR5k = ~$5,589/mo (ECB 1.1177, 10-07) = ~$67k/yr vs observed Altra spend >= ~$6,300 over ~14 mo (~$450/mo), roughly 12x. VF FY26 10-K: advertising + promotion $849.3M = 9% of revenue; Altra revenue NOT broken out (sits in 'All Other'). Search-summary only (unverified): Altra +45% Q4 FY26, >30% FY26, ~$250-270M revenue. No Altra sale news found. No published benchmark for brand-VO monthly retainers. Plan: ladder (start $750/$1,500 options, maybe a $3,000 anchor, 90-day review, cross-VF-brand referrals); EUR5k = 12-24 month goal, not a month-6 ask.
- **IMG / EuroLeague: Ian Henderson.** POTS 26/27 delivered 9/18, €2,500 invoice (Chloe Hubbard, due ~9/28; paid ❓ not re-checked). Pickups sent free 9/19 as a one-time courtesy. **Feature-spots pitch sent 09-22** (€1,150/session, up to 4 spots, season rate lock); awaiting Ian (not re-checked). **May 2027 Review pricing (keep):** open at **€10,000 full buyout** (all media, all territories, perpetuity), pickups €750/round; fallback ~€6,500 for a 3-yr licence; floor ~€5,000 only with rights scoped down. 🟡 Stacked from GFTB ad tables; no published rate exists for this. History: £10K → $3,750 → £5,000 passed; then €2,500.
- **KU Marketing: Liz Nelson / Steve Rausch.** Retainer offer declined 09-23 (project by project, "will keep a retainer in mind"). Warm check-in ~2026-11-04. Confirm the Traditions Night invoice is paid.
- **CrowdReply: Jim (co-founder). BOOKED: now a client; Spencer voiced a job for them in September 2026: one :30 VO, $250, web only in perpetuity (Spencer, 10-06/10-07). Paid/ad use would need a new usage fee; future retainer quotes should cap terms (not in-perp by default).** Samples sent 08-28, check-in on the ledger for 10-14. ❓ Surname: this file said "Loining", `followups-queue.md` says "Levi". Check Gmail before the next send. Pricing plan: ~$350/video one-off; retainer $300/mo for 1 video, ~$275 each extra; floor $250; no pricing in the first reply.
- **Laundry Studio: Gabriel Gerard (production coordinator; producer Ben Rejzer).** Warm. Next: check-in ~Tue 2026-10-20 to Gabriel, with something new. Lucas Bertoli (Laundry Design) is on leave until Nov 20; contact him after that.
- **Framer: Ryan Cotrupi.** Spencer DM'd him 09-24 asking if Framer has a go-to VO; awaiting reply. Funnel A final touches went out 09-29.
- **Shell: Jane Sayers, Global Film Lead.** Replied 10-05 (link blocked by firewall); Spencer sent the re-voice as an attachment 10-05 13:31. Warm, awaiting Jane.
- **Venmo (PayPal): Alisa Lee, Creative Producer.** Warm reconnect scheduled Wed 10-07 (tracker row 166).

## Resolved / cold (one line each)
- Laundry → Adobe CC 2×:15 (Sep 2026): LOST 09-22 ("client went another direction creatively"). Data point: Spencer quoted $5.5–6K national / $2,200 3-mo regional; Gabriel's ceiling ~$2,400.
- Alexander Diner (Webflow Head of Brand Studio): viewed profile 08-30, connection never accepted. Cold.
- Justin Jones (Framer): host of Framer Academy (his own show, no VO opening); DM'd 08-30, no movement. Cold. Pitch idea still stands: "be the consistent voice for Framer Update."
- Janae David (Team One producer): reel sent on LinkedIn 08-29, quiet since. Her email bounces; LinkedIn only.
- Voices.com jobs from 08-28 (Enterprise #OnEveryCorner $850 guidance; father-daughter animated series €250–300/ep guidance; Walmart Seller Summit quoted $700): outcomes ❓, never logged. Marketplace work belongs in `quick-quote.md` anyway.
- Overdue-reconnect cohort sent 08-26 (Dan Hass/ATTN, Craig Pentak + Sara Kear/Condado, Deb Cad/Kanahoma) and 10 reconnects sent 08-28 (Gillis, Sheridan, Kay, Daughenbaugh, Kane, Bertoli, Ballam, Romoff, Prokos, Leisher). Warm follow-ups now run from the `followup-drafts` ledger. Lessons kept: don't reuse one credits paragraph across a batch (match credits to each recipient's world), and never close with "I'd love to be considered again."
- Noah Media: if reconnecting, contact Dan Shaw or Neil Housley (Eve O'Sullivan has left).

## Quick marketplace quote log — MOVED

Rapid-fire marketplace quotes now live in **`reference/quick-quote.md`** (compact rate card + 5-line output format + log). Use that for any pasted Voices.com job; this file is only for direct/agency/retainer pricing.

## Standing action items (re-checked 2026-10-06 against memory, not Gmail)

1. **Bounced addresses still to fix:** Maya Roberts, Tami Hachiya, Janae David (Team One), Nathan Mallon (The Team, Mimecast 550), Anna Jacobsen (Tellary: try `poullet@tellary.com`). Status ❓ since 08-31.
2. **Robert Salas** (GMR Marketing, Senior Producer): re-add to the tracker. Status ❓.
3. **DDO resubmission SENT 2026-10-06 17:05 Lisbon** (Gmail 1a111f646b9cd269, "Hey Allie!" thread, cc Alicia): Elaine workshop, 1:37 commercial reel link, EuroLeague 26/27, offer of fresh reads. Warm nudge Tue 10-20 if silent (window to 10-27). Have 2 fresh reads (main + alternate) ready if she asks.
4. Lori Lins Plaud + AT&T Quantum Fiber auditions (due Aug 28): status ❓, likely stale. Drop at the next prune if nothing turns up.
5. Dead addresses from the 09-29 wave: re-source Thinkific (Eric Smith, Kevin C, Evan Lepage) and Domestika (Valeria).

## History: the Gmail sweep (Aug 19–20 2026)

A full historical sweep of the business Gmail built most of this tracker: 579 sent-mail threads → 311 correspondents → 77 new client/contact rows added (73 initial + 4 from ambiguous cases). Also fixed 11 data-quality issues in pre-existing rows (blank/wrong emails) and two sheet-infrastructure bugs (conditional formatting and Dashboard formulas were both hardcoded to stop at row 57). Voices.com contacts and YouTube-channel cold-outreach were excluded by rule.
