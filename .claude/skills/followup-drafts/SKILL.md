---
name: followup-drafts
description: >-
  Daily follow-up engine for Spencer's outreach. Finds which follow-ups are truly due (using the VO Pipeline Digest + tracker + live Gmail, with cadence judgment). Cold touches 2 and 3 are NEVER Gmail drafts: they go as rows into the Follow-up Queue Sheet, and the Apps Script "Bingo Follow-up Sender" in Spencer's account sends them offline at 09:04 (touch 2) / 10:13 (touch 3) contact-local after a last no-contact check (Spencer, 2026-10-20). Warm and long-tail follow-ups stay Gmail drafts for Spencer. Ledger in memory/followups-queue.md. Use when Spencer says "what's due", "draft my follow-ups", or when the follow-up routines fire.
---

# Follow-up drafts + reminders

Spencer's goal (2026-09-24): he falls behind on follow-ups. Whenever a follow-up is due by the cadence rules it is handled before the due day and he gets told who is being followed up. Not daily: only when something is due. **Cold touches 2 and 3 are SENT automatically, no review, and never sit in his Drafts (Spencer, 2026-10-15: "I don't have to touch them at all. I don't have to read them at all ... They should already be scheduled or out"; "you have full permission to use whatever tools you need").** See "Send queue" below (Spencer, 2026-10-20: "They should not even hit my draft box"). Warm-client follow-ups, quarterly LT touches and anything flagged stay drafts for Spencer to send.

## Schedule-driven, not daily (Spencer, 2026-09-24)
Reminders fire **only when a follow-up is due by the cadence rules**, not every day. The single source of dates is the **schedule ledger** in `memory/followups-queue.md` (rules table + per-cohort reminder / overdue dates, clock starts at the verified Gmail SEND date). Each due follow-up gets exactly three touchpoints: **prep** (drafts written the evening before), **remind** (once, ON the reminder date: "due today, send"), and **one overdue nudge** on the last day of the window if still unsent. Then stop. On days with nothing due: stay silent.

## Modes
- **prep** (Follow-up Prep routine, 08:40 Pacific Sun-Fri): find ledger rows whose reminder date (or overdue-nudge date) is the NEXT business day, plus anything overdue and not yet queued; QUEUE every cold touch 2/3 (no cap, "Send queue" below) and draft only warm/LT ones; notify "Tomorrow: N follow-ups go out automatically: <names>".
- **remind** (inside the Daily Digest): catch-up first: any cold touch 2/3 due today or overdue that is neither SENT nor QUEUED in the queue Sheet gets queued now (send date = today if its send time is still ahead locally, else the next weekday). Then read the queue: SENT rows since yesterday roll the ledger forward + tracker + outreach-log; HELD / ERROR rows go at the top of the digest with the reason; a stale heartbeat (Log!F1 older than 15 min) = "sender down" at the top. Notify only for rows whose reminder date is TODAY and need Spencer (warm/LT/flagged). The ledger is the authority; the digest only supplements it.
- **interactive**: Spencer asks; do prep+remind in one pass.

## Step 0 — Ledger coverage scan (every prep run; every Digest run as a cross-check)
**Why (Spencer, 2026-10-15/16):** ~28 Funnel G/G2 pitches sent 10-02..10-08 never got a touch 2. This engine only acts on ledger rows, and nothing added a pitch to the ledger when it was sent. Match on **thread origin, never subject**: pitches go out under subjects other than "A voice for".
1. **List.** FGAC `google_api_get` (read-only), account spencer@spencerzvoice.com: ALL of Sent for the last 21 days, `gmail/v1/users/me/messages?q=in:sent newer_than:21d&maxResults=500&fields=messages(id,threadId),nextPageToken`, following `nextPageToken` until none is left; plus every Scheduled message (`q=in:scheduled`, same paging). For each distinct threadId: `threads/<id>?format=metadata&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Cc&metadataHeaders=Subject&fields=messages(id,labelIds,internalDate,payload/headers)`.
2. **Candidates.** Keep a thread when its FIRST message (lowest internalDate) is from spencer@spencerzvoice.com and To/Cc holds at least one address that is not spencer@spencerzvoice.com or spencerzpearman@gmail.com. Every one is a candidate, whatever the subject.
3. **Reconcile.** Each candidate ends in exactly ONE state in `memory/followups-queue.md`:
   - **IN LEDGER:** its address or threadId is on a ledger row with touch dates (Reminder + Overdue). A cold pitch with no row gets one: touch 1 = Gmail send date, touch 2 reminder day 7, overdue day 10 (cadence table); already past = overdue, drafted this run.
   - **EXEMPT:** one line in the ledger's `## Ledger coverage: EXEMPT` section (create it under the schedule ledger if missing): `EXEMPT: <addr> | thread <id> | <reason> | <date>`. Reasons allowed: invoice/payment, active job thread, Voices.com/marketplace, personal, admin/vendor, warm client on its own cadence (name the ledger row or tracker row that carries it).
   - **Unclear** = add a ledger row and flag it in the run summary. Never exempt by guess, never skip silently.
4. **Tracker cross-check.** Every tracker row whose Status is Sent / Sent - Awaiting Reply / Follow-Up Sent and that has no ledger row (match on email) is missing too; add it.
5. **Loud output.** Print `Ledger coverage: X outbound threads, Y in ledger, Z exempt, N missing` (X = candidates; tracker-only misses count in N). **N > 0:** prep adds every missing one before Step 1 and re-counts until N = 0; the Digest makes it a priority item at the top (DIGEST-ROUTINE-PROMPT.md Step 0a). The line goes in the run log and final message every run.

## Step 1 — Find what's due (digest is INPUT, not gospel)
0. Read the ledger in `memory/followups-queue.md` FIRST; it decides what is due today/tomorrow. Everything below is triage + supplement.
1. Read the newest "VO Pipeline Digest" email in spencer@spencerzvoice.com (FGAC `google_api_get`, never the generic Gmail connector) and the tracker (`Outreach Tracker`, spreadsheetId in AGENTS.md). Also `memory/followups-queue.md` and `memory/outreach-log.md` "Follow up on" dates.
2. **Triage every digest item against live Gmail** before drafting. The tracker flag is date-only and over-flags. Known false positives (2026-09-24): contacts who already replied (Mackenzie Prokos), contacts on their 3rd touch (Michael MacMillan = initial + 8/24 + 9/1 = done), the "data gap" on Nancy Loud (email was nancyloud@untoldstudios.tv, sent 9/7). For each candidate: search `to:<addr>` in Sent and `from:<domain>` in inbox; read the last sent message; confirm no reply, no bounce, no existing draft for that thread (list drafts).
3. **Cadence rules** (from outreach-email Step 5): cold agency 7-10d, 3 touches in the sequence, then the **quarterly long-tail touch** (section below) instead of stopping. A contact whose sequence is done is NOT "skip, 3rd touch done" when its ledger row shows an LT touch due. Warm past client, no open thread: 4-8 weeks, and the nudge must bring something new. Skip: OOO holds (Krista Hansen, Lucas Bertoli, Geminesse Johnson), "Hold" Next Actions, anyone who said "no current need / we'll reach out", Miro/Drew Jaz (never pitch), dropped rows, Voices.com/marketplace items (never in tracker).
   **"They'll reach out" = PARKED (Spencer, 2026-10-07: "She said she would keep me posted, so I don't want to keep tapping her").** Before drafting ANY touch to a warm contact, read every inbox message `from:<company domain>` since the last job, not just the ledger thread. If the contact OR a colleague at that company said "I'll keep you posted / keep you in mind / will reach out when something comes up", the whole company is PARKED: no cadence touch, no "new reel" nudge, no favor or review ask, until they write first or Spencer says otherwise. Record it in the PARKED list at the top of `memory/followups-queue.md`. (Misses on 10-07: Dan Shaw drafted though Neil Housley at Noah wrote "will defo keep you in mind" 09-04; a review ask to Xpedition after Becca Winkler said she'd reach out, 07-31 + 09-28.)
4. Anything that can't be drafted honestly (no thread history, unknown context, first-ever reconnect with no prior email found, e.g. Luke Mellows, Jamie Pearson on 2026-09-24) goes in a **"flagged, not drafted"** list with the reason. Do not guess.
5. **No cap that pushes anything past its due date (Spencer, 2026-10-15).** The old ~12-per-run cap deferred Funnel C's finals twice and four Funnel H touch-2s to the evening AFTER they were due (10-13/10-14 prep). Draft everything due tomorrow and everything overdue, oldest first. If a run genuinely can't finish (usage limit), the leftovers are drafted by the next run that fires, the morning Digest included, never "the next evening prep".
6. **NO-CONTACT CHECK before every touch 2/3, at draft time AND again right before sending (Spencer, 2026-10-15: "ROUTINE MUST BE CHECKING EMAIL THREAD/LINKEDIN MESSAGES TO MAKE SURE EVERY CLIENT THAT IS GETTING A 2ND/3RD TOUCH HASNT BEEN CONTACTED YET").** "Contacted" since the last ledger touch = any of:
   - Email: any SENT message to the contact's address in ANY thread (`in:sent to:<addr> after:<last touch date>`), any message in Scheduled to them (`in:scheduled to:<addr>`), an existing draft to them other than this one, any inbound from them or `from:<their domain>` (reply, OOO, bounce: `"<addr>"` also catches mailer-daemon).
   - Same company, same day: a colleague at the same domain already got a touch today (no double-tap, Ramp rule).
   - LinkedIn: (a) Gmail notification mail from LinkedIn naming the contact since the last touch (`from:linkedin.com "<First Last>"`: "messaged you", "replied", "sent you a message"); (b) any LinkedIn message logged in the repo (`grep -ri "<Last name>"` across memory/*.md, memory/outreach-log.md, reference/client-acquisition/LINKEDIN-CHECKS.md, contacts/*.md, then read the hit for "DM", "messaged", "LinkedIn message"). A connection request with no note is NOT contact. (c) Desktop sessions also open linkedin.com/messaging in Spencer's Chrome and search the name.
   - Anything found = do NOT queue (or set the queue row's status to HELD with the reason). Roll that contact's ledger clock from the contact date, log why, and list it in the digest/notification. The Apps Script re-runs the email + LinkedIn-notification part of this check itself right before it sends. A reply = warm track, tell Spencer. If the LinkedIn side can't be checked at all (cloud, no notification mail, nothing logged) that counts as clean; the desktop does (c) when it runs.

## Quarterly long-tail touch (Spencer, 2026-10-05: replaces "stop after the final touch")
**Why:** final VO gets cast in days, from a 1-5 voice shortlist of people the producer already knows, and buyers start ~83% of vendor contacts themselves (6sense). A cold sequence can't hit the job. It gets him into the pool, and the long tail keeps him there. VO coaches say quarterly, indefinitely, 6-12 touches (Paul Schmidt/VO Pro, Such A Voice), and follow-ups bring 42% of replies (Instantly). Source: `reports/Campaign budgets and VO timing.md`.

**Who:** every cold contact whose sequence is done (final touch sent) with no reply, no "no", no bounce. Warm past clients keep their own 4-8 week cadence; this rule isn't for them.

**When:** every ~90 days from the last SENT touch (window day 85-105). Ledger touch labels: `LT1`, `LT2`, ...; reminder = day 90, overdue = day 105, both after the shifts below.
- Lands **Nov 23 - Jan 4** → move to Tue-Thu **Jan 5-15** (Thanksgiving week + holiday blackout; December is the worst reply month, Belkins). Thanksgiving 2026 = Thu Nov 26.
- UK/EU contact landing in **August** → move to Sep 1-11.
- Normal send-date rules (US holidays and the day before/after, Friday afternoon ET).
- Inside the window, prefer the company's best pitch window from its row in `reference/client-acquisition/BUDGET-CALENDAR.md` (FY end, new-money month, archetype). No row → add one (rules in that file) before picking the date.
- A real trigger (product launch, new video, new role, funding, rebrand) can pull a touch forward, but never sooner than 45 days after the last touch.
- Revisit dates already in the ledger (Spencer's earlier calls) count as LT1; quarterly runs from their send.
- Big waves: stagger the cohort across the window, oldest final first (LT touches are drafts for Spencer, not auto-sent).

**Form:** a **NEW email, not a thread reply** (three unanswered messages underneath reads needy). Fresh subject naming the new thing. One line placing him ("I reached out earlier this year about voiceover for <company>'s videos"), then the new thing, a short close, the standard sign-off. **It must carry something new and true:** a new verified credit or job, a fresh re-voice of one of their recent videos, or a hook on their recent launch (hook rules: event line + `[YOUR TAKE]`, watch any video it references). Nothing new = flagged, not drafted. Never "just checking in."

**Exits:** reply → warm track · "no" / "we'll reach out" → stop for good (a "not now, try <month>" → one dated touch then) · bounce / left the company → flag for re-sourcing (a new contact there starts a fresh cold sequence) · asked not to be contacted → stop. **After LT4 (≈1 year) with zero response → flag for Spencer's go/no-go**, don't keep going on autopilot.

## Step 2 — Draft (Spencer's voice)
- Read `outreach-email` SKILL Step 4 + `.claude/skills/outreach-email/voice.md`. Casual, contractions, short, no em dashes in the body, sign-off exactly `Best,\nSpencer\nspencerzvoice.com`. NO voice descriptor at all (the "warm bass/baritone" line was cut 2026-10-05; never "American"). Formal opener (Hello) for women / older men.
- **New proof, never "just bumping."** Only true, sourced hooks: verified credits (FIFA World Cup 2026 Preview Series, EuroLeague basketball, etc. per MEMORY.md), the audition offer (if not already made in that thread), a current-event hook for cold emails (LinkedIn/company post read this session). Bracket anything unverified. Cite sources in the run summary (AGENTS.md RULE 0 footer: Verified / Bracketed / Unknown).
- **Touch 2 after a re-voice pitch = this text word for word (Spencer, 2026-10-05, his Sprout Social draft; overrides the "new proof" bullet above for this touch, no FIFA/EuroLeague line, no hook):**
  ```
  Hello <First>,

  Following up on the re-voice I sent last week. I hope you like what you hear! I'd love to chat about working with you all as your go-to Voiceover Artist, and I'd love to offer an audition for any of the videos you have coming up.

  Best,
  Spencer
  spencerzvoice.com
  ```
- **Never offer free work (Spencer, 2026-10-14: "That's offering free work").** No "free", "custom read", "no obligation", "no strings" in any follow-up. The offer is an audition: touch 2 = one paragraph, Spencer's exact wording above (the audition offer joined to the go-to line with ", and", never a stand-alone line); touch 3 = Spencer's sent Funnel B final (below). `pitch_draft_qc.py` blocks any reply draft that offers free work.
- 3rd touch = this text word for word (Spencer's Funnel B finals, sent 2026-10-14):
  ```
  Hey <First>,   (Hello <First>, for women / older men)

  Last note from me for now. I'm happy to offer an audition for any of the videos you have coming up. Hope to hear from you soon.

  I'll leave it here and check back later in the year.

  Best,
  Spencer
  spencerzvoice.com
  ```
- Send-date sanity (outreach-email Step 5): no US holidays / day before-after, no Friday afternoon ET.

## Send queue: cold touches 2 and 3 never touch Drafts (Spencer, 2026-10-20: "They should not even hit my draft box" / "This needs to be done offline")
Applies to cold touch 2 and touch 3 (final) only, with Spencer's exact text from Step 2. Warm, LT, re-worded or flagged = Gmail draft for Spencer (Step 3).
- **Why:** Gmail has no API for scheduled send, and cloud routines have no browser, so every earlier fix (routine runs as the scheduler, send_later, Stage 4) left drafts sitting in his Drafts box. Fixed 10-20 with an Apps Script that lives in his own Google account and runs on Google's servers with the PC off.
- **Queue Sheet:** "Follow-up Queue (Bingo auto-send)" `1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao`, tab `Queue`. Columns A:P = status | touch | name | company | to | tz | send_date_local | send_time_local | thread_id | draft_id | body | last_touch_utc | queued_by | sent_at_utc | sent_msg_id | note.
- **Sender:** Apps Script project "Bingo Follow-up Sender" in spencer@spencerzvoice.com (script.google.com/u/3/home/projects/10aNY35EDHyh1dd5B__8_Nk44x9PTdPrfH2YZamcsqqOk8nqasIRDbJMM). Source of truth = `scripts/apps-script/FollowupSender.gs`; after editing it, paste it into the project and save (desktop). `tick()` runs every minute; `eveningPreview()` emails Spencer the queued list at 19:00 Lisbon. **Format (10-21):** the sender now sends `multipart/alternative` (plain + `<div dir="ltr">` HTML, links auto-linked) instead of text/plain only, so follow-ups render like Spencer's own Gmail mail; queue the body as plain text with a blank line between paragraphs and the sign-off last.
- **Send times (Spencer, 2026-10-20):** touch 1 (pitch) 08:32 local = Spencer's, scheduled by the desktop after he vets/records; **touch 2 = 09:04 local; touch 3 = 10:13 local.** Weekdays only. The script also refuses anything outside 08:32-15:00 local (for tz "US" it must be inside the window in BOTH New York and Los Angeles, so "US" rows send at 09:04 / 10:13 Pacific).
1. **Queue it, never draft it.** For each due cold touch 2/3 that passes the NO-CONTACT CHECK, append ONE row with FGAC `google_api_modify` POST `v4/spreadsheets/1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao/values/Queue!A:P:append?valueInputOption=RAW&insertDataOption=INSERT_ROWS`, body `{"values":[["QUEUED","2","<First Last>","<Company>","<email>","<tz>","<YYYY-MM-DD reminder date>","09:04","<threadId>","","<exact Step 2 text, 
 line breaks>","","<routine> <date>","","",""]]}` (touch 3: "3" and "10:13"). `tz` = the contact's CONTACT-TZ.json value (IANA zone or "US"); missing = look it up on their live LinkedIn location and add it to CONTACT-TZ.json first, never guess. Before appending, read the Queue tab and skip any contact already QUEUED/SENT for that touch (never queue twice).
2. **The script sends it:** at the row's local send time it re-checks the thread, inbound mail from the contact's domain (auto-replies ignored), other sent/scheduled mail to them and LinkedIn notification mail naming them; clear = sends a threaded reply ("Re: <subject>", In-Reply-To/References set) and marks the row SENT with the message id; contact found = HELD + alert email; failure = ERROR + alert email.
3. **A Gmail draft of a cold touch 2/3 is a bug.** `.claude/hooks/followup_queue_guard.py` blocks creating one. If one exists anyway (old run, manual), put its id in a QUEUED row's `draft_id` (leave `body` empty): the script copies the text into the row and deletes the draft on its next tick.
4. **After sending (Digest / next Prep):** every SENT row since the last run: ledger rolled forward from the send date, tracker row (Status "Follow-Up Sent", Last Contact Date, Notes; never J/K), outreach-log, commit + push. HELD/ERROR rows and a stale heartbeat (`Log!F1` older than 15 min) go to the top of the digest and get a push.
5. **End-of-run check (every Prep, Digest and Morning Build run, and any desktop session that touched follow-ups):** count live Gmail drafts that are cold touch 2/3 replies (`q=in:drafts subject:"Re: A voice for"` and the touch-2/3 wording) = must be 0, and every ledger touch 2/3 due today or tomorrow must be QUEUED or SENT in the Sheet. Print `Follow-up queue check: drafts D, due N, queued Q, sent S, missing M`. D > 0 or M > 0 = queue them now; if that fails, push Spencer with the names. A run never ends quietly with M > 0.

## Step 3 — Create the draft (warm / LT / flagged ONLY; FGAC, threaded; LT touches = new email)
- Never for cold touch 2/3: those go to the Send queue above.
- **LT touch exception:** POST the draft with no `threadId`, no `In-Reply-To`/`References`, and a fresh subject (not "Re:"). Everything else in this step applies.
- `google_api_modify` POST `gmail/v1/users/me/drafts` with `{"message":{"threadId":..., "raw": <base64url RFC822>}}`, account spencer@spencerzvoice.com.
- Build the raw with Python `email.message.EmailMessage(policy=SMTP)` so a non-ASCII subject (the original subjects contain an em dash) is MIME-encoded. **Subject must match the thread ("Re: <original>")**, plus `In-Reply-To` = last Message-ID in the thread and `References` = earlier + last, or Gmail won't thread it. Get Message-IDs with `threads/<id>?format=metadata&metadataHeaders=Message-ID&metadataHeaders=Subject&metadataHeaders=To`.
- Updating an existing draft = **PUT**, not PATCH. Read one back with `gmail_read` (draft message id) to verify subject/body/thread.

## Step 4 — Queue, log, notify
1. Append each draft to the draft queue in `memory/followups-queue.md` (contact, company, thread id, draft id, due date, touch #, status `drafted`). When a later run sees the draft gone from Drafts and a matching message in Sent, mark `sent <date>`, set the ledger's next reminder/overdue dates from the SEND date per the cadence table (never leave a sent contact without a next date or an explicit 'no further touch'), and update the tracker (Status, Last Contact Date, Notes) + `memory/outreach-log.md` in the same turn. Tracker edit rules: re-read the row's Name/Company first, write, read back; never write cols J/K.
2. Log in `memory/outreach-log.md` and `memory/<today>.md`; commit + push (`git add -A && git commit -m "memory: follow-up drafts <date>" && git push`).
3. **Notify Spencer** (both):
   - `PushNotification` (status "proactive", <200 chars): prep → "Tomorrow: N follow-ups go out automatically (<names>). Nothing for you to do. M drafts need you: <names>." · Digest → "Sent N follow-ups yesterday (<names>); held M (<why>)." · remind → only for drafts Spencer must send himself (warm/LT/flagged). Cold touches 2/3 never ask him to review or send.
   - Also email him at spencer@spencerzvoice.com from himself via FGAC (same as the digest does), subject `VO follow-ups due today: N drafts ready` / `...due tomorrow...`, body = table of contact | company | touch # | one-line angle | anything to double-check before sending. If the send is blocked by FGAC's whitelist, say so in the run summary.
4. If nothing is due today per the ledger, send NOTHING and stay quiet (no "all clear", no daily pings), but still update the queue for anything sent.

## Standing don'ts
Never send anything from a Claude session except through the Send queue (cold touches 2/3), never send without the NO-CONTACT CHECK, and never drop a contact silently. A "drop this" decision must be enacted in Gmail itself (delete the draft), not just written in memory (Kyle Osher lesson, 2026-09-23). Never add marketplace jobs to the tracker.
