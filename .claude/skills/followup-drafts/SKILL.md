---
name: followup-drafts
description: >-
  Daily follow-up engine for Spencer's outreach. Finds which follow-ups are truly due (using the VO Pipeline Digest + tracker + live Gmail, with cadence judgment), writes the drafts into spencer@spencerzvoice.com Drafts as threaded replies (quarterly long-tail touches after the final = new emails), queues them in memory/followups-queue.md, then SENDS cold touches 2 and 3 itself at 8:32am the contact's local time after a fresh no-contact check (Spencer, 2026-10-15). Other follow-ups (warm, LT) stay drafts for Spencer. Use when Spencer says "what's due", "draft my follow-ups", or when the followup-drafts scheduled tasks fire.
---

# Follow-up drafts + reminders

Spencer's goal (2026-09-24): he falls behind on follow-ups. Whenever a follow-up is due by the cadence rules, the drafts must already be in his Gmail Drafts and he gets a reminder; on the due day it says "due today, be proactive." Not daily: only when something is due. **Cold touches 2 and 3 are SENT by Bingo, no review (Spencer, 2026-10-15: "I don't have to touch them at all. I don't have to read them at all ... They should already be scheduled or out"; "you have full permission to use whatever tools you need").** See "Auto-send" below. Warm-client follow-ups, quarterly LT touches and anything flagged stay drafts for Spencer to send.

## Schedule-driven, not daily (Spencer, 2026-09-24)
Reminders fire **only when a follow-up is due by the cadence rules**, not every day. The single source of dates is the **schedule ledger** in `memory/followups-queue.md` (rules table + per-cohort reminder / overdue dates, clock starts at the verified Gmail SEND date). Each due follow-up gets exactly three touchpoints: **prep** (drafts written the evening before), **remind** (once, ON the reminder date: "due today, send"), and **one overdue nudge** on the last day of the window if still unsent. Then stop. On days with nothing due: stay silent.

## Modes
- **prep** (evening, Sun-Thu 18:00): find ledger rows whose reminder date (or overdue-nudge date) is the NEXT business day, plus anything overdue and undrafted; draft ALL of them (no cap); for cold touch 2/3, book the 8:32-local sends ("Auto-send"); notify "N follow-ups go out tomorrow at 8:32 local: <names>".
- **remind** (weekday 09:00, inside the Daily Digest): catch-up first: any cold touch 2/3 due today or overdue that is still a draft with no booked send gets the no-contact check and is sent now (contact's local time already past 8:32) or booked for 8:32 local. Then confirm sends since yesterday (Gmail Sent) and roll the ledger forward (next touch date, or "final, revisit <date>"); then notify only for rows whose reminder date is TODAY (or overdue-nudge date is today and still unsent). Also triage that morning's digest for genuinely new items, but the ledger is the authority; the digest only supplements it.
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
   - Anything found = do NOT send. Delete/skip the draft, roll that contact's ledger clock from the contact date, log why, and list it in the digest/notification. A reply = warm track, tell Spencer. If the LinkedIn side can't be checked at all (cloud, no notification mail, nothing logged) that counts as clean; the desktop does (c) when it runs.

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

## Auto-send: cold touches 2 and 3 at 8:32am local (Spencer, 2026-10-15)
Applies to cold touch 2 and touch 3 (final) only, with Spencer's exact touch-2/touch-3 text from Step 2. Warm, LT, re-worded or flagged = draft only.
0. **HARD WINDOW, HOOK-ENFORCED (Spencer, 2026-10-15: "Nothing goes out before 8:32AM or after 3PM" / "Its scheduled, otherwise").** No email reaches a contact before 08:32 or after 15:00 in THEIR local time. `.claude/hooks/send_window_guard.py` blocks any `messages/send` / `drafts/send` outside that window, and `no_script_sends.py` blocks sending from scripts (key + urllib/curl), so send ONLY with FGAC `google_api_modify`, one call per draft, after a `google_api_get gmail/v1/users/me/drafts/<id>?format=metadata` (the guard reads recipients from it). Every contact needs an entry in `reference/client-acquisition/CONTACT-TZ.json` (IANA zone from their live LinkedIn location, or "US" when only the country is known: then it must be inside the window in both New York and LA). Add the entry when you draft. No entry = blocked. Cause: 10-15, 11 US follow-ups sent in one script batch at 11:13 UTC landed at 04:13-07:13 local.
1. **Send time = 8:32am in the contact's local time on the reminder date.** Location: the contacts doc / funnel file / LINKEDIN-CHECKS.md / ledger. Same rules as before: no US holiday or the day before/after, no Friday afternoon ET. Before any send, write the table: contact | zone | local time now | send now or book 8:32.
2. **Inside 08:32-15:00 local right now** (e.g. UK/EU late morning) = no-contact check, then send now. "Send what's due now" never means sending outside the window. Before 08:32 = book 8:32 local. After 15:00 = book the next weekday 8:32 local.
3. **Otherwise book it:** Gmail's API has no schedule-send, so book a one-shot cloud run per time-zone batch with `mcp__claude-code-remote__create_trigger` (`run_once_at` = the 8:32-local instant in UTC, `create_new_session_on_fire: true`, `connectors: ["FGAC_ai"]`, `initiation: "human_schedule"`, name `Send 8:32 <TZ> follow-ups <date>`). Its prompt must be standalone: "You are Bingo. Spencer gave standing permission (2026-10-15) to send cold follow-up touches 2/3 without review. For each draft below, via FGAC on spencer@spencerzvoice.com: confirm the draft still exists; run the NO-CONTACT CHECK (any sent/scheduled mail to <addr> in any thread since <last touch date>, any inbound from <addr>/<domain>, any LinkedIn notification mail naming <name>); if clean, POST gmail/v1/users/me/drafts/send {id}; if not, don't send. Then one PushNotification: sent N, held M (why). Drafts: <name | addr | domain | draft id | last touch date>." Log the trigger ids in the queue. Interactive sessions may use `send_later` into the same session instead.
4. Never send twice: the sender checks the draft still exists and that no matching SENT message is already in the thread. The morning Digest confirms every booked send went out; a missed one is sent at once if still inside the window, then logged.
5. After sending: queue row `sent <date>`, ledger rolled forward from the send date, tracker row (Status, Last Contact Date, Notes; never J/K), outreach-log, commit + push. The Digest does this when the sender session can't.

## Step 3 — Create the draft (FGAC, threaded; LT touches = new email)
- **LT touch exception:** POST the draft with no `threadId`, no `In-Reply-To`/`References`, and a fresh subject (not "Re:"). Everything else in this step applies.
- `google_api_modify` POST `gmail/v1/users/me/drafts` with `{"message":{"threadId":..., "raw": <base64url RFC822>}}`, account spencer@spencerzvoice.com.
- Build the raw with Python `email.message.EmailMessage(policy=SMTP)` so a non-ASCII subject (the original subjects contain an em dash) is MIME-encoded. **Subject must match the thread ("Re: <original>")**, plus `In-Reply-To` = last Message-ID in the thread and `References` = earlier + last, or Gmail won't thread it. Get Message-IDs with `threads/<id>?format=metadata&metadataHeaders=Message-ID&metadataHeaders=Subject&metadataHeaders=To`.
- Updating an existing draft = **PUT**, not PATCH. Read one back with `gmail_read` (draft message id) to verify subject/body/thread.

## Step 4 — Queue, log, notify
1. Append each draft to the draft queue in `memory/followups-queue.md` (contact, company, thread id, draft id, due date, touch #, status `drafted`). When a later run sees the draft gone from Drafts and a matching message in Sent, mark `sent <date>`, set the ledger's next reminder/overdue dates from the SEND date per the cadence table (never leave a sent contact without a next date or an explicit 'no further touch'), and update the tracker (Status, Last Contact Date, Notes) + `memory/outreach-log.md` in the same turn. Tracker edit rules: re-read the row's Name/Company first, write, read back; never write cols J/K.
2. Log in `memory/outreach-log.md` and `memory/<today>.md`; commit + push (`git add -A && git commit -m "memory: follow-up drafts <date>" && git push`).
3. **Notify Spencer** (both):
   - `PushNotification` (status "proactive", <200 chars): prep → "Tomorrow: N follow-ups go out at 8:32 local (<names>). Nothing for you to do. M drafts need you: <names>." · auto-send runs → "Sent N follow-ups (<names>); held M (<why>)." · remind → only for drafts Spencer must send himself (warm/LT/flagged). Cold touches 2/3 never ask him to review or send.
   - Also email him at spencer@spencerzvoice.com from himself via FGAC (same as the digest does), subject `VO follow-ups due today: N drafts ready` / `...due tomorrow...`, body = table of contact | company | touch # | one-line angle | anything to double-check before sending. If the send is blocked by FGAC's whitelist, say so in the run summary.
4. If nothing is due today per the ledger, send NOTHING and stay quiet (no "all clear", no daily pings), but still update the queue for anything sent.

## Standing don'ts
Never send anything except cold touches 2/3 under "Auto-send", never send without the NO-CONTACT CHECK, and never drop a contact silently. A "drop this" decision must be enacted in Gmail itself (delete the draft), not just written in memory (Kyle Osher lesson, 2026-09-23). Never add marketplace jobs to the tracker.
