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
- **Follow-Up Flag** = formula. Logic: Dropped or Left Company→"N/A" (added 2026-10-08, Spencer); Bounced→"Fix Email & Resend"; Responded→"Active - Monitor"; Not Sent→"Send Initial Outreach"; Drafted-Not-Sent→"Ready to Send"; else by days: ≥10→"OVERDUE - Follow Up Now", ≥7→"Due Soon", else "Recently Contacted". Leave alone.
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
_Auto-logged (see the memory protocol in CLAUDE.md). Keep status lines current. Pruned 2026-10-06 and 2026-11-03: resolved/cold items are one-liners under "Resolved / cold"; full history is in git (`git log -p reference/outreach-pipeline.md`) and the dated `memory/` logs._
- **Hip Hop Madness / Nate: new general-topics channel, rev-share offer (LIVE 2026-10-29).** WhatsApp 2025-12-10: keep flat rate ($100/script, $250 sponsors) OR 25% of all channel revenue in exchange for free VOs, no guarantee. Nate's estimate $10-30k+/mo (12-11-25; based on ~14 yrs on YouTube + a previous channel that "outperformed HHM", unverified), traction hoped by video 20; refused to share HHM earnings (01-03-26), OK sharing the new channel's. Genre (10-29): Patrick Cc / Internet Anarchist style (Kevin Hart, Dave Chappelle vs Key & Peele, Sony). 10-29 Nate asked what % terms Spencer wants. Bingo's advice: hybrid (flat fee + %), or 25% only with read-only YouTube Studio access, sponsors included, monthly payout, sunset back to flat fee at video 20. Source: WhatsApp export emailed 10-29 (Gmail 1a189a85f2297e17).
- **11C Media / Easy Tiger Voices: TV series dubbing (inbound 2026-10-27, LIVE).** Camila Feres (Studio & Casting Coordinator, camila@11cmedia.com; Maaike cc'd), thread 1a17dfec289908f3; tracker row 101. 33 eps x ~42 min, dubbed into English for broadcast, neutral American, ~12 characters. Spencer QUOTED 10-27 16:19 UK: $175/hr, 2-hr min, TV broadcast incl. (floor $125/hr, GVAA CODA non-union). Nudged 11-02; Camila replied 11-02: "still finalizing a few details on our end", will be back in touch (Gmail-checked 11-03). Next: wait; one check-in ~11-16 if silent. Open Qs for them if it moves: territories + streaming + term, characters + est. hours, sync, remote direction tool (no Source Connect sub), payment terms, Easy Tiger commission.
- **Matinée Multilingual (UK agency, Reading): roster application SENT 2026-10-20 13:11 Lisbon** to voices@matinee.co.uk (thread 1a15933e833e4541; tracker row 236). Bio + rates ($250/hr live, eLearning $45/min) + 3 dry demos (F:/0. Spencer Z Voice/Voiceover Work/3. Demos/Matinee Submission). No reply and no nudge sent as of 11-03 (Gmail-checked). Nudge was due ~11-03.
- **Voices&Co (The Irish Voiceover Agency Ltd, Dublin; ex-Voicebank): roster submission SENT 2026-10-23 15:29 Lisbon** (Gmail 1a1692ab21e3dea7; tracker row 253) to talent@voicesandco.ie; commercial, corporate and narration demos attached. Only an auto-reply (10-23) as of 11-03. Their rule: reply only if interested within ~2 months, don't chase. Silent by ~2026-12-23 = not taken.
- **PT agencies via Kyla Nelson referral (WhatsApp, not email; found 2026-10-12):** VOX ARTIST / Ana (+351 960 285 967): 7/15 'welcome... I'll ask for the info needed to join VOX ARTIST portfolio', nothing since. ZOV / Vera (+351 937 981 560): 7/16 asked email + photo 'for our voicebook', Spencer sent both, nothing since. Both ~3 months silent: nudge on WhatsApp. Tracker rows 200-201 (10-12).
- **Altra Running: Tyler Gorky (Global Creative Producer) + Dani Coplen (Global Creative Director), LIVE.** Sizzle $900 (NL-2026-007) PAID 10-26 via Stripe after nudges; Tyler 10-26: "I think I have another project for you", scripts pending (thread 1a0ee3f820e20281, Gmail-checked 11-03). **NEW JOB 11-03 "Altra BC"** (msg 1a1a24ca5c75b6c0, cc Matt Mackenzie): :30 + :15 cutdown + maybe :06, 1.5 yr, All Media ex-broadcast (OOH, Industrial, Internal, Web + Social paid/organic, OTT + Pre-Roll), Worldwide, exclusive on the recording / talent non-exclusive; Tyler offered **$1,500**. Bingo quote 11-03: counter **$4,500** (:30 $2,200 + :15 $1,650 + :06 $660, lift %s), floor $3,500; as-briefed industry math ~$38k+. Reply not sent yet (Spencer to decide). Retainer email NOT sent (nothing to vfc.com since 10-26); per tracker row 155 a "retainer Phase 1" email sits in Gmail Drafts for Spencer to send ~a week after payment (🟡 draft not opened 11-03). Retainer options: $750/mo = $900 credit or $1,500/mo = $1,800 credit; floor Option 1. Booking, research and invoice history: `reference/altra-vf-account.md`.
- **IMG / EuroLeague: Ian Henderson.** POTS 26/27 delivered 9/18, €2,500 invoice. Payout stalled on IMG vendor/W-9/Trustpair checks (Chloe Hubbard, then Tom Roberts, Production Assistant); bank details approved 10-28/29 (IMG Vendor MasterData #10005238); Tom 10-30: invoice posted for approval, "hopefully you will have the money next week" (thread 1a10b5ec8a48881a). No payment email seen as of 11-03. Feature-spots pitch 09-22 (€1,150/session, up to 4 spots, season rate lock): Ian replied 09-23 citing budget; Spencer nudged 10-05 and 10-28, no reply (thread 1a0c8e241ce0a3c8). **May 2027 Review pricing (keep):** open at **€10,000 full buyout** (all media, all territories, perpetuity), pickups €750/round; fallback ~€6,500 for a 3-yr licence; floor ~€5,000 only with rights scoped down. 🟡 Stacked from GFTB ad tables; no published rate exists for this. History: £10K → $3,750 → £5,000 passed; then €2,500.
- **KU Marketing: Liz Nelson / Steve Rausch.** Retainer declined 09-23 (project by project). Steve left a Google review 10-20; Liz out of office 10-20 (Gmail-checked 11-03). Warm check-in ~2026-11-04. Traditions Night ($400, Aug 2026) payment ❓ not confirmed in Gmail.
- **CrowdReply: Jim Levi (co-founder, jim@crowdreply.io; surname confirmed from his 08-28 email header). BOOKED: Spencer voiced one :30 for them in September 2026, $250, web only in perpetuity (Spencer, 10-06/10-07). Paid/ad use would need a new usage fee; future quotes cap terms (not in-perp by default).** No email from crowdreply.io since 08-28 (Gmail-checked 11-03). Pricing plan: ~$350/video one-off; retainer $300/mo for 1 video, ~$275 each extra; floor $250.
- **Laundry Studio: Gabriel Gerard (production coordinator; producer Ben Rejzer).** Warm. The planned 10-20 check-in did NOT go out: no email to or from laundry.studio since 10-01 (Gmail-checked 11-03). Lucas Bertoli (Laundry Design) is on leave until Nov 20; contact him after that.
- **Framer: Ryan Cotrupi.** Spencer DM'd him 09-24 asking if Framer has a go-to VO; awaiting reply. Funnel A final touches went out 09-29.
- **Shell: Jane Sayers, Global Film Lead.** Replied 10-05 (link blocked by firewall); re-voice sent as an attachment 10-05; nudge sent 10-27 11:10 UK; no reply as of 11-03 (thread 1a0d51f505a4ffa7). Next: last check-in ~11-17, then long-tail (Jan budget).
- **Venmo (PayPal): Alisa Lee, Creative Producer.** Reconnect sent 10-06; she replied 10-08 (passing it to the team); Spencer asked for the spot link 10-08; nothing since (Gmail-checked 11-03). Warm check-in ~11/19-12/03 (tracker row 166).
  - **HELD (Spencer, 10-08): Howie Howell, Director, Global Brand & Creative Production, PayPal-Venmo** (the production lead; likely above Alisa, 🟡). LinkedIn linkedin.com/in/howiehowell (live 10-08: headline "Global Brand Production & Innovation Leader | PayPal-Venmo", San Francisco; Spencer's connect request PENDING). Apollo id 5ae46540a6da98d3fbfcd4f7. **No usable email:** Apollo's only result, howie.howell@venmo.com, is extrapolated + ZeroBounce INVALID (twice, 10-08). Do not send there. Apollo has no paypal.com record for him (searched 10-08). howiehowell.com (10-08): contact FORM only, no address shown; resume PDF at /s/howiehowell_executiveproducer_resume_2020-mf6c.pdf not read (it downloads rather than opening). Not contacted. Plan: LinkedIn after he accepts, naming Venmo Days/Alisa; don't go around Alisa this week.

## Resolved / cold (one line each)
- Laundry → Adobe CC 2×:15 (Sep 2026): LOST 09-22 ("client went another direction creatively"). Data point: Spencer quoted $5.5–6K national / $2,200 3-mo regional; Gabriel's ceiling ~$2,400.
- Alexander Diner (Webflow Head of Brand Studio): viewed profile 08-30, connection never accepted. Cold.
- Justin Jones (Framer): host of Framer Academy (his own show, no VO opening); DM'd 08-30, no movement. Cold. Pitch idea still stands: "be the consistent voice for Framer Update."
- Janae David (Team One producer): reel sent on LinkedIn 08-29, quiet since. Her email bounces; LinkedIn only.
- Voices.com jobs from 08-28 (Enterprise #OnEveryCorner $850 guidance; father-daughter animated series €250–300/ep guidance; Walmart Seller Summit quoted $700): outcomes ❓, never logged. Marketplace work belongs in `quick-quote.md` anyway.
- Overdue-reconnect cohort sent 08-26 (Dan Hass/ATTN, Craig Pentak + Sara Kear/Condado, Deb Cad/Kanahoma) and 10 reconnects sent 08-28 (Gillis, Sheridan, Kay, Daughenbaugh, Kane, Bertoli, Ballam, Romoff, Prokos, Leisher). Warm follow-ups now run from the `followup-drafts` ledger. Lessons kept: don't reuse one credits paragraph across a batch (match credits to each recipient's world), and never close with "I'd love to be considered again."
- Lori Lins Plaud + AT&T Quantum Fiber auditions (due Aug 28): never resolved, dropped at the 2026-11-03 prune.
- Noah Media: if reconnecting, contact Dan Shaw or Neil Housley (Eve O'Sullivan has left).

## Quick marketplace quote log — MOVED

Rapid-fire marketplace quotes now live in **`reference/quick-quote.md`** (compact rate card + 5-line output format + log). Use that for any pasted Voices.com job; this file is only for direct/agency/retainer pricing.

## Standing action items (pruned 2026-11-03 against memory, not Gmail)

1. **Bounced addresses still to fix:** Maya Roberts, Tami Hachiya, Janae David (Team One), Nathan Mallon (The Team, Mimecast 550), Anna Jacobsen (Tellary: try `poullet@tellary.com`). Status ❓ since 08-31.
2. **Robert Salas** (GMR Marketing, Senior Producer): re-add to the tracker. Status ❓.
3. **DDO:** parked. Allie replied 10-20: resubmit after 6 months of training; resubmit Wed 2027-04-21 (MEMORY.md "Representation").
4. Dead addresses from the 09-29 wave: re-source Thinkific (Eric Smith, Kevin C, Evan Lepage) and Domestika (Valeria).

## History: the Gmail sweep (Aug 19–20 2026)

A full historical sweep of the business Gmail built most of this tracker: 579 sent-mail threads → 311 correspondents → 77 new client/contact rows added (73 initial + 4 from ambiguous cases). Also fixed 11 data-quality issues in pre-existing rows (blank/wrong emails) and two sheet-infrastructure bugs (conditional formatting and Dashboard formulas were both hardcoded to stop at row 57). Voices.com contacts and YouTube-channel cold-outreach were excluded by rule.
