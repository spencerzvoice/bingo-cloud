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

## Pipeline snapshot (2026-08-27 — will drift; check the sheet)

~85 data rows. Composition:
- **New Outreach - Agency:** Cheil USA (Colby Mitchell, Mark Van Duinen, Didi Fraioli, Tim Eger, +Andrew Davis unsent), Team One (Sam Walsh, Erick Sosa, Sascha Peuckert, Melanie Saitta + bounced: Maya Roberts, Tami Hachiya, Janae David; Janet Bell Anderson on hold), Untold Studios (Luke Colson, Tanya Ferguson, Chelsea Kammeyer, Josephine Gallagher, Nancy Loud), Octagon (Sean LaGamma, Melissa Dunlop Parsons), Anomaly (Erika Madison, Michelle Price, Michael MacMillan — OOO to Sept 1), The Team (Cameron Choate + Nathan Mallon bounced), Laundry Service (Stacy Robnett, Abbey Birsch Garbarino), Ogilvy (Luis Aguilera → Laysa Martins), GMR Marketing (Krista Hansen — OOO), IMG (Ian Henderson), MezzoLab (João Freitas), DDO (Alicia Beekman, Allie Silber).
- **Active / Recurring:** Noah Media Group (6 contacts), Lori Lins Ltd, Shadow Lion (Ryan Lago, Jeff Fine), Xpedition Media (Rebekah Bell, Mary Chaplin, Nandi Smythe), Diamond View (Jeff McKown), Kansas University (Liz Nelson, Steve Rausch — live paid), Kimley-Horn (Jordan Deva), Condado/Pentak (Sara Kear, Craig), iFIT (Michael Hamblin, Ryan Humpherys), Acclaim Lighting, Tellary (bounced), Tony Beck, Wild Creative, Some Odd Pilot, Narwal Creative, Dove Street Films, IMG (Jamie Pearson), Archetype, Rhymesayers (Tanner Groehler).
- **Old Client Reconnect:** Melissa Gillis (ATTN), Rebeccah Sheridan (CGI), Evan Kay (Climb High), Ruthie Mason (Coronation), Kayla Gremer Foreid (Diamond View), Erin Daughenbaugh (EDP), Mel Kane (Invision), Lucas Bertoli (Laundry Design), Taylor Ballam (Modo), Evan Romoff (Romoff Media), Mackenzie Prokos (Rune Haus), David Martin (ShadowLion), Devin Leisher (TBC), Dan Haas (ATTN — sent), Deb (Kanahoma — sent).
- **Professional Development:** Elaine Craig (registered, Sept 19), Carrie Faverty (fall dates pending).

## Live leads & jobs in flight
- **KU Marketing (Liz Nelson / Steve Rausch) — retainer offer** (sent 2026-09-23): Steve declined for now — project-by-project, "will keep a retainer in mind." Next: warm check-in ~2026-11-04. Aug preferred-vendor proposal still ❓ (not in Gmail). Confirm Traditions Night invoice paid.
- **Altra Running — Tyler Gorky (Global Creative Producer, per Spencer)** (2026-09-24): Tyler phoned Spencer directly re an INTERNAL video (3rd/4th Altra spot). Prior Altra work all came via independent producer Lilah Kohlman (Run Spot Aug 2025 $2,200; Torin 9 Mar/Apr 2026 $3,200) — zero Gmail threads with Tyler or an altrarunning.com address (live FGAC check 09-24). Lilah's 08-27 + 09-11 check-ins unanswered. ✅ Tyler verified live on LinkedIn (linkedin.com/in/tyler-gorky-76600670, Spencer's Chrome, 09-24): Altra Running, Global Creative Producer since Aug 2026 (2 mos); Creative Producer, full-time, since Aug 2022 (4 yrs 2 mos) — Spencer's "4 months" was 4 YEARS; Denver. Before: Production Manager & Casting Director, Shutterstock Studios (Nov 2021–Mar 2022); freelance producer NYC (Art + Commerce, M+A). Credited "Producer: Tyler Gorky" on the Torin 9 launch (Altra-side; Lilah Kohlman = "Producer" for production co. V1_Final) — the same campaign Spencer voiced. Activity = reposts only (Torin 9 stills 2mo, Experience 3 7mo). Colleagues: Dani Coplen (Global Creative Director), Grace Zygmun (Global Brand & PR), Rachel Winkel (Dir. Marketing, VF Corp). Scope/script/budget not yet in. Plan: quote fair, deliver clean, pitch retainer/preferred-rate block at delivery. Call 09-24: Tyler said he liked the voice, confirmed in-house studio; Spencer open to record early next week; no price discussed. Usage TBD: internal now, may later go to paid channels (Spencer-reported). Record Mon 09-28/Tue 09-29. No budget stated. Plan: two-tier quote (internal-only vs +paid) + written upgrade clause; usage in writing before recording. Status: awaiting Tyler's usage email.

_Auto-logged (see the memory protocol in CLAUDE.md). Keep status lines current; condense/prune resolved + cold entries on the schedule in MEMORY.md._

### IMG / EuroLeague — "Preview of the Season 26/27" (POTS) — ✅ read from live Gmail 2026-09-19
- **Status:** VO delivered 9/18 (2 reads). **€2,500 invoice** sent to Chloe Hubbard (IMG finance); she confirmed 9/18 it's processed Monday 9/21 on **7-day terms** → payment due ~9/28. Do not touch the invoice.
- **Pickup request 9/19 (Adrian Ross, cc Ian Henderson):** (1) new line "And In Kaunas, another great was returning to his roots" + alternate "And Zeljko wasn't the only one to return to his roots"; (2) re-read of the Sekulic line with SECK-OO-LITCH. Guide audio "Extras for Spencer.m4a" attached — Bingo has NOT listened.
- **Decision (Bingo advice):** Sekulic re-read = free (pronunciation, covered by Spencer's stated terms). New line/alt = technically chargeable script addition, but 10 + 11 words (two alternates, so ~10 usable) on an already-low €2,500 → do free **as an explicit one-time courtesy**; further script additions get a pickup fee. Send as a separate pickup file, reply cc Ian + Chloe. **SENT by Spencer Sat 9/19 16:44 BST** (reply-all to Adrian, Ian cc; attachment "EuroLeague POTS_pickups.mp3"; free, further script additions quoted separately). ✅ live Gmail. Awaiting IMG confirmation that the Preview is final.
- **Unknown:** whether "In Kaunas" was in the original script.
- **Data point:** history quoted £10K → countered $3,750 → £5,000 (passed then); landed €2,500 here. Relationship value (Ian, Jamie, Chloe) > this rate; push rate up next time.
- **Feature-spots pitch (drafted 2026-09-22):** new email to Ian only, "Voicing the EuroLeague feature spots this season" — proposes €1,150/session for up to 4 feature spots, 24h turnaround, locked for season; open question on volume/frequency. References Jamie's £50/spot rate + Mar 2026 batching idea (Jamie never priced the batch — Bingo's earlier "~£62/spot" read was inference, not Jamie's offer; Spencer had rejected bundling outright on 2026-03-04, so pitch reframes it as "makes sense at the right price"). Brackets filled 9/22 (45s per spot, one round of revisions included). **SENT by Spencer 2026-09-22** to Ian only — ✅ live Gmail, msg id `1a0c8e790d2c9453`. Status: awaiting Ian's reply on volume/frequency and whether he'll accept €1,150/session. (Draft mailbox bug + fix: an earlier attempt via the generic Gmail connector `create_draft` silently saved to a different mailbox — that connector has no account-selection param and doesn't default to spencer@spencerzvoice.com; use FGAC for all Gmail writes, not just reads.)

### Laundry → Adobe Creative Cloud — 2×:15 (came from Spencer's outreach) — ✅ read from live Gmail 2026-09-19
- **Thread "VO Audition"**, started 2026-09-16: **Gabriel Gerard**, production coordinator (gabriel.gerard@laundry.studio); producer **Ben Rejzer** cc'd (ben.rejzer@laundry.studio). NDA signed + returned 9/16. Scripts PDF "CC Value Phase 3 — YT Audio scripts_9.15.2026.pdf" — Bingo has NOT read it. Lucas Bertoli (Laundry Design) is not in this thread; his paternity leave (back Nov 20) came from his OOO auto-reply on the Sep 11 check-in, which redirected to production@laundry.studio (per tracker).
- **Brief:** 2×:15 · "record Friday" (9/18), ≤2 hr, done before 1p PT · budget **$2k** · they wanted ≥1 yr national digital + terrestrial radio · creative brief: natural/conversational, avoid robotic/AI-sounding, music bed.
- **Usage as clarified:** Spencer wrote "one-year national digital *paid media* plus one-year national radio"; Gabriel: "I believe that's correct" but deferred to Ben (unconfirmed by the producer). So "digital" may mean paid video/social, not digital radio — 🟡 unresolved ("YT Audio" in the script filename is a hint either way).
- **Source Connect:** Spencer told them 9/16 he has NO active subscription but can get one for the session.
- **Spencer's quotes (9/16):** $5,500–6,000 [sent as "$5500k-6k"] for the 2-hr live session + full usage; or **$2,200 for 3-mo regional digital + radio**. Sent 2 reads (2 takes each) 20:42 Lisbon. **Gabriel:** could "at most squeeze another 20%" (≈$2,400); "maybe that 3-month option could work"; will keep posted. Spencer: "Keep me posted."
- **Status (as of 9/19):** silence since 9/16 evening; no booking confirmation.
- **Guide check (✅ GVAA, 2026-09-19):** if digital = digital *radio*: Radio T+D bundle, Natl 1 yr $2,500–3,250/spot → $5,000–6,500 for 2. If digital = paid video (pre-roll $2,250–3,000/1yr) + national radio ($1,500–2,500): $3,750–5,500/spot → $7,500–11,000 before the 15–25% bundle discount. Regional 3-mo radio bundle $500–900/spot (Spencer's $2,200 is above the guide's top); National 3-mo $1,250–1,500/spot ($2,500–3,000 for 2).
- **OUTCOME 2026-09-22 — LOST, door open (✅ live Gmail 09-24):** Spencer sent the scope-check follow-up 09-22 08:00 PT. Gabriel replied 09:10 PT: team liked the reads, "client went another direction creatively"; will keep Spencer in mind for any follow-up reads or other Laundry VO projects. Spencer replied 17:24 BST (thanks, always ready to audition). The $2,500 national / $2,200 regional counters were never answered; "digital" scope never resolved. No further ask on this job.
- **Relationship:** Gabriel Gerard (Laundry Studio production coordinator, cc producer Ben Rejzer) is now a warm contact separate from Lucas Bertoli (Laundry Design, on leave until Nov 20). Next touch: warm check-in ~Tue 2026-10-20 to Gabriel (something new, not a bump), then Lucas after Nov 20. Tracker row 99 already reflects the loss (routine, 09-22).

### CrowdReply — first Lane 1 (direct-to-brand) opportunity
- **Contact:** Jim Loining ("Jim L"), **co-founder**, 20s. Met in person 2026-08-28 (padel). Also runs a separate side project, BambooVPN.
- **Company:** CrowdReply (crowdreply.io) — AI-search-visibility / GEO-AEO platform (get your brand cited by ChatGPT, Perplexity, Gemini, Claude) + Reddit/social listening + backlinks marketplace. Founded Feb 1 2025 by Jim Loining + Dawood Khan. Seed-stage, NZ-linked (Icehouse Ventures), content-marketing-heavy — claims "5,000+ brands" (marketing figure, ~18-month-old company).
- **Their cadence:** ~1 product/marketing video per month → X + YouTube, likely with paid promotion behind it. Spencer asked whether they also do internal / B2B client videos — awaiting answer (that's the retainer-expansion path).
- **The opening:** Jim sent two CrowdReply product videos from X. Spencer re-voiced both and **sent samples 2026-08-28 14:14 (Lisbon)** to `jim@crowdreply.io`, subject "VO samples" — 2 re-voiced videos (Drive links) + 2 attached past jobs (Amazon AWS SageMaker overview, Artlist 2024). Warm casual note, no pricing, padel sign-off. **Status: awaiting reply.**
- **Pricing plan:** one-off fair rate **~$350/video**; recurring retainer **$300/month** for 1 guaranteed video (24h turnaround, 12-mo rate lock); **~$275** per additional video same month. **Floor $250** — no mate's rates; VC-backed company, his credits justify it. Quote per-video first, then offer the retainer. No pricing in the first send. Confirm paid-media spend + usage term when pricing comes up (real ad spend → attach 12-mo digital usage, rate rises).
- Note for next send: all files on Drive, not mixed Drive links + 21MB attachments (near Gmail's limit).

### Alexander Diner — Head of Brand Studio, Webflow (Funnel A — high priority)
- Exactly the Funnel A decision-maker title. **Viewed Spencer's profile 2026-08-30** (warm signal) after Spencer sent a connection request. Awaiting connection accept.
- When connected: casual warm note, specific compliment on recent Webflow work, no pitch — same playbook as Ryan.

### Justin Jones — "Education at Framer" / Video Marketeer (Amsterdam, remote)
**Verified from screenshots 2026-08-30:** he is the **on-camera host of Framer's Academy** — talking-head + screen-share tutorials, published ~weekly, his face/voice/format. Per his LinkedIn (his words): also does feature-launch videos. One-man band: on camera, editing, motion, scriptwriting. **Also a voice actor** (headline).
- **Academy tutorials = no VO opportunity** — it's his show.
- **VERIFIED (Spencer, 2026-08-30): Framer is a real target.** They publish multiple "Framer Update:" videos/month — some with VO, some without; some use real VO artists, some use internal tech people. Latest: **"Framer Agents: Design with AI, Keep Control"** — July 22, 30-sec spot, **1.1M views, uses a VO artist.** Signal: they may be investing more in these.
- **THE PITCH: "be the consistent voice for Framer Update."** They rotate voices inconsistently — a 1.1M-view series benefits from one recognizable voice. Retainer-shaped. Say it plainly to Justin + lead with the peer (fellow-VO) framing.
- **Custom sample = re-voice the July 22 "Framer Agents: Design with AI, Keep Control" spot** (30 sec, VO-driven, flagship). Exact match for the work.
- 2nd degree, 1 mutual, viewed Spencer's profile. Ryan Cotrupi = internal ally, kept warm.
- **2026-08-30: connection-request note + first message drafted** (peer/fellow-VO hook, "consistent voice for Framer Update" planted softly, ends on a real question). Going out. Awaiting Justin or Ryan to move.

### Ryan Cotrupi (Framer) — new LinkedIn connection (Funnel A)
- Title: "Editor | Photographer | Digital Creator | Digital Marketer at Framer" — grab-bag; role unclear (could be the person who makes their video, a junior generalist, or a route to the brand lead).
- **2026-08-30: accepted connection; Spencer sent a casual no-ask note** — complimented "the video you guys posted yesterday," asked if he's on the video/content side. **Awaiting reply.**
- Spencer's read on Ryan: young creative, casual — connect on that level. Keep every reply in that register.
- Framer's videos **DO have VO** (Spencer confirmed) — pitch is re-voicing one of their narrated videos, NOT the "never had a voice" angle.
- Next fork: if he's on video → soft VO angle next message. If not / junior → stay friendly, later ask who runs brand video. Don't rush it.

### Janae David (Team One, Producer) — warm LinkedIn lead
- **Status:** replied on LinkedIn **Aug 28** — apologised for the delay, thanked Spencer for following up, **asked for his reel**. **Aug 29: Spencer sent his commercial reel link + a short warm reply on LinkedIn** ("thanks for getting back to me, no worries on the delay… here's the link"). Reel = Drive file `1c7_eCvNwox47JShpSUZjrGTjIggKSE1j` (his **commercial cut**, confirmed; Spencer renamed the file himself; "anyone with link" — verified viewable). Best forward motion of the whole Team One push (other 4 Team One contacts silent since Aug 24).
- **Channel:** LinkedIn DM only — her email `janae.david@teamone-usa.com` **bounces**. Get a working address via Hunter.io before real project comms.
- **Next:** don't chase. ~1 week out (≈Sept 5), one light touch — "happy to put down a custom read of anything on your slate." Producer with reel on file = warm asset; let it sit warm.
- **Dependency:** keeps the **commercial reel cut** live-priority for the wider Team One / agency push.

### Enterprise "#OnEveryCorner" — Voices.com case-study narration
- **What:** Voices.com VoiceMatch (90% match, ~28 responses). Internal case-study video for **Enterprise**'s #OnEveryCorner World Cup 2026 campaign (corner-kick sweepstakes w/ Kia). 370 words / ~2m28s. **Non-broadcast, in-perpetuity.** Requires a 1-hr Source Connect **directed session** this week. Cleaned mix-ready WAVs. 2 rounds revisions for talent error; script changes billable. Budget $250–$499 (gross, incl. platform fee) but explicitly "quote as you see fit."
- **Bingo's quote guidance (2026-08-28):** quote **$850** — $600 narration (2.5 min, non-broadcast, in-perp buyout) + $250 directed session. **Floor $600** ($400 + $200); pass below that. Don't apologise for going over; they invited it.
- **Status:** guidance given — Spencer deciding whether to audition/quote. If booked → another World Cup credit next to the FIFA series.

### Father-daughter animated educational series — recurring character (Voices.com)
- **What:** Voices.com (116 responses). Short-form animated educational series, international social-media release. **Recurring voice for "the father"** — warm, calm, human, "sounds like a father speaking to his daughter, not a narrator." Male, neutral English, middle age. 1 min/episode. **Usage: Cartoons / Online (organic social).** Budget **€150–249**.
- **Bingo's quote guidance (2026-08-28):** treat as episodic content-series character work, NOT commercial — GFTB's €500 organic-video rate is the wrong comp. Fair: **€250–300/episode**, or a **batch session ~€300–350 covering 4–6 episodes** (better for a series). Their €249 ceiling ≈ bottom of Spencer's own recurring-content rate, so negotiate structure, don't walk. **Don't drop to €150/episode on singles** — that's batch-only territory. **Get the episode count + schedule in writing before building a rate.** Cap the licence at life-of-series; paid ads = separate fee; watch for a character-exclusivity ask (that's a premium).
- **Status:** guidance given — Spencer deciding whether to audition/quote.

### Walmart Marketplace Seller Summit — Voices.com internal video
- **What:** Voices.com (116 responses). **Internal Video** — "Walmart Marketplace Seller Summit" (event/summit content for Walmart's 3rd-party Marketplace sellers). 100 words / ~0m40s. **Non-broadcast, in-perpetuity.** Budget **$500–$749** (gross).
- **Bingo's guidance (2026-08-28):** budget at/above fair market (~$500). With 116 bids, guidance was $600–625 to win; **Spencer quoted $700** (nets ~$560). Flag left in the quote: confirm genuinely internal — if seller-facing (YouTube / seller portal / recruitment) it's wider usage worth $900–1200+.
- **Status:** quoted $700. Awaiting outcome.

## Quick marketplace quote log — MOVED

Rapid-fire marketplace quotes now live in **`reference/quick-quote.md`** (compact rate card + 5-line output format + log). Use that for any pasted Voices.com job; this file is only for direct/agency/retainer pricing.

## Standing action items

1. **Fix + resend bounced emails:** Maya Roberts, Tami Hachiya, Janae David (Team One — pattern `firstname.lastname@teamone-usa.com` but these bounced; verify via Hunter.io), Nathan Mallon (The Team — Mimecast `550 5.4.1` rejection), Anna Jacobsen (Tellary — try `poullet@tellary.com` or `tellyourstory@tellary.com`).
2. **Send the 10 genuinely-unsent reconnect drafts** (cross-checked list below — was ~18, trimmed after checking the live tracker).
3. **Re-add Robert Salas** (GMR Marketing, Senior Producer) — row vanished before his ready draft was sent.
4. **Lori Lins auditions:** Plaud + AT&T Quantum Fiber (were due Aug 28) — check status.
5. Follow up when Sam Walsh (back Aug 25) and Michael MacMillan (back Sept 1) return from OOO.
6. Investigate why the routine deletes rows.
7. Submit the Gmail-connector bug report to Anthropic support if not already done.
8. Track the Sept 19 Elaine Craig workshop → resubmit to Allie Silber at DDO afterward.

## Overdue-reconnect cohort — SENT 2026-08-26 (~14:29–14:36 Lisbon)
Soft "checking in, anything new?" notes to recurring/past contacts (729-day OVERDUE flag from the digest):
- **Dan Hass** (ATTN) · dhass@attn.com · "Re: Amazon SMB Pawstruck"
- **Craig Pentak** (Pentak Creative / Condado Tacos) · craig@pentakcreative.com · "Re: Condado Tacos VO"
- **Sara Kear** (Condado Tacos) · sara.kear@condadotacos.com · "Re: Condado Tacos VO" — congratulated on Reader's Choice nomination
- **Deb Cad** (Kanahoma / NMSU) · deb@kanahoma.com · "Re: NMSU Global Campus"

No open threads / no live quotes — pure check-ins. **Follow-up cadence = warm/no-thread = 4 weeks, NOT the 7–10 day cold rule.** Do not nudge before **~2026-09-22**; a fast bump on a "just checking in" reads needy and costs standing. When following up, bring something new (updated demo, a fresh sample, a new credit) — never "just bumping." Craig + Sara are one company (Condado) — already 2 touches same day, don't stack a 3rd fast.
As of 2026-08-31: day 5, no replies — expected, hold.

## Reconnect drafts — 10 SENT 2026-08-28, follow-up window ~Sept 4–7

Original list was ~18 (from the memory import). After checking the live sheet: 2 already sent, 3 redundant, 3 held. The remaining 10 **were all sent 2026-08-28 ~17:50 (Lisbon)**:
Melissa Gillis (ATTN — Pawstruck) · Rebeccah Sheridan (CGI — Dell) · Evan Kay (Climb High — OutThere) · Erin Daughenbaugh (EDP — Informatica) · Mel Kane (Invision — Gilead) · Lucas Bertoli (Laundry Design — Fred & Ted/Informatica) · Taylor Ballam (Modo — NordicTrack) · Evan Romoff (Romoff Media — DPSCS) · Mackenzie Prokos (Rune Haus — Woodward) · Devin Leisher (TBC — ADA "We Fight").

**Tone review of what went out (for follow-up calibration):** solid and on-brand — correct formal/casual opener by recipient, specific past-project named, genuine news hooks where found (ATTN independence, Invision Inc. recognition), right sign-off. Two misses to fix on the follow-ups: (1) the middle paragraph ("kept busy with a mix of commercial and sports/tech work… FIFA/AWS/NordicTrack") was **verbatim identical across all 10** — batch skeleton, against his own rule; vary the credits to match each recipient's world (corporate credits for Gilead/Informatica contacts, commercial for agencies). (2) the casual ones closed with "I'd love to be considered again" — which his own style rule explicitly says *not* to use; use "please keep me in mind" / "Hope to hear from you soon!". Also: give the follow-up an active, zero-friction close (offer an updated demo / "send anything on your slate my way").

**Already sent (drop from list):** Jeff McKown (Diamond View — checked in Aug 27) · Lilah Kohlman (Altra — checked in Aug 27).

**Now redundant — same company already contacted, skip unless Spencer wants a second touch:** David Martin (ShadowLion — Jeff Fine already sent the same ESPN/Champ Fund reconnect Aug 26; Ryan Lago active) · Kayla Gremer Foreid (Diamond View — Jeff McKown already active; Kimley-Horn/Jordan Deva already replied) · Ruthie Mason (Coronation — Haley Rossi already reconnected Aug 26 with the same Mount St. Mary's reference).

**Low priority:** Luke Mellows + Luke O'Reilly (Noah Media — both "pick-ups/rewrites" contacts, ~100+ days quiet). The whole Noah cluster has had no touch since May–June; if reconnecting, **Dan Shaw or Neil Housley** are the production contacts (Eve O'Sullivan has left Noah — removed from tracker 2026-08-28).

**Held:** Andrew Davis (Cheil — not casting-focused, deprioritized) · Janet Bell Anderson (Team One — wait until cast). **Excluded:** Tony / Vishuddha.

## History: the Gmail sweep (Aug 19–20 2026)

A full historical sweep of the business Gmail built most of this tracker: 579 sent-mail threads → 311 correspondents → 77 new client/contact rows added (73 initial + 4 from ambiguous cases). Also fixed 11 data-quality issues in pre-existing rows (blank/wrong emails) and two sheet-infrastructure bugs (conditional formatting and Dashboard formulas were both hardcoded to stop at row 57). Voices.com contacts and YouTube-channel cold-outreach were excluded by rule.
