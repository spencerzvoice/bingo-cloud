---
name: followup-drafts
description: >-
  Daily follow-up engine for Spencer's outreach. Finds which follow-ups are truly due (using the VO Pipeline Digest + tracker + live Gmail, with cadence judgment), writes the drafts into spencer@spencerzvoice.com Drafts as threaded replies, queues them in memory/followups-queue.md, and reminds Spencer to review + send. Never sends. Use when Spencer says "what's due", "draft my follow-ups", or when the followup-drafts scheduled tasks fire.
---

# Follow-up drafts + reminders

Spencer's goal (2026-09-24): he falls behind on follow-ups. Every day he has any due, the drafts must already be sitting in his Gmail Drafts and he gets a reminder; on the due day the reminder says "due today, be proactive." **Drafts only. Nothing is ever sent or scheduled by Bingo** (CLAUDE.md hard rule; the Gmail API can't schedule-send anyway).

## Modes
- **prep** (evening, Sun-Thu 18:00): find follow-ups due *tomorrow (next business day) or already overdue and undrafted*, draft the missing ones, notify "N drafts ready for tomorrow".
- **remind** (weekday 09:00, after the ~08:27 Lisbon digest lands): pick up anything newly due in that morning's digest (draft it), then remind on everything in the queue still unsent: "due today".
- **interactive**: Spencer asks; do prep+remind in one pass.

## Step 1 — Find what's due (digest is INPUT, not gospel)
1. Read the newest "VO Pipeline Digest" email in spencer@spencerzvoice.com (FGAC `google_api_get`, never the generic Gmail connector) and the tracker (`Outreach Tracker`, spreadsheetId in AGENTS.md). Also `memory/followups-queue.md` and `memory/outreach-log.md` "Follow up on" dates.
2. **Triage every digest item against live Gmail** before drafting. The tracker flag is date-only and over-flags. Known false positives (2026-09-24): contacts who already replied (Mackenzie Prokos), contacts on their 3rd touch (Michael MacMillan = initial + 8/24 + 9/1 = done), the "data gap" on Nancy Loud (email was nancyloud@untoldstudios.tv, sent 9/7). For each candidate: search `to:<addr>` in Sent and `from:<domain>` in inbox; read the last sent message; confirm no reply, no bounce, no existing draft for that thread (list drafts).
3. **Cadence rules** (from outreach-email Step 5): cold agency 7-10d, max 3 touches then October revisit (NO 4th touch). Warm past client, no open thread: 4-8 weeks, and the nudge must bring something new. Skip: OOO holds (Krista Hansen, Lucas Bertoli, Becca Winkler, Geminesse Johnson), "Hold" Next Actions, anyone who said "no current need / we'll reach out", Miro/Drew Jaz (never pitch), dropped rows, Voices.com/marketplace items (never in tracker).
4. Anything that can't be drafted honestly (no thread history, unknown context, first-ever reconnect with no prior email found, e.g. Luke Mellows, Jamie Pearson on 2026-09-24) goes in a **"flagged, not drafted"** list with the reason. Do not guess.
5. Cap: max ~12 drafts per run. If more are due, draft the highest-value/oldest and say what was left.

## Step 2 — Draft (Spencer's voice)
- Read `outreach-email` SKILL Step 4 + `.claude/skills/outreach-email/voice.md`. Casual, contractions, short, no em dashes in the body, sign-off exactly `Best,\nSpencer\nspencerzvoice.com`. "warm bass/baritone" (never "American"). Formal opener (Hello) for women / older men.
- **New proof, never "just bumping."** Only true, sourced hooks: verified credits (FIFA World Cup 2026 Preview Series, EuroLeague basketball, etc. per MEMORY.md), the free custom-read offer (if not already made in that thread), a current-event hook for cold emails (LinkedIn/company post read this session). Bracket anything unverified. Cite sources in the run summary (AGENTS.md RULE 0 footer: Verified / Bracketed / Unknown).
- 3rd touch = closes as last touch ("I'll leave it here and check back later in the year").
- Send-date sanity (outreach-email Step 5): no US holidays / day before-after, no Friday afternoon ET.

## Step 3 — Create the draft (FGAC, threaded)
- `google_api_modify` POST `gmail/v1/users/me/drafts` with `{"message":{"threadId":..., "raw": <base64url RFC822>}}`, account spencer@spencerzvoice.com.
- Build the raw with Python `email.message.EmailMessage(policy=SMTP)` so a non-ASCII subject (the original subjects contain an em dash) is MIME-encoded. **Subject must match the thread ("Re: <original>")**, plus `In-Reply-To` = last Message-ID in the thread and `References` = earlier + last, or Gmail won't thread it. Get Message-IDs with `threads/<id>?format=metadata&metadataHeaders=Message-ID&metadataHeaders=Subject&metadataHeaders=To`.
- Updating an existing draft = **PUT**, not PATCH. Read one back with `gmail_read` (draft message id) to verify subject/body/thread.

## Step 4 — Queue, log, notify
1. Append each draft to `memory/followups-queue.md` (contact, company, thread id, draft id, due date, touch #, status `drafted`). When a later run sees the draft gone from Drafts and a matching message in Sent, mark `sent <date>` and update the tracker (Status, Last Contact Date, Notes) + `memory/outreach-log.md` in the same turn. Tracker edit rules: re-read the row's Name/Company first, write, read back; never write cols J/K.
2. Log in `memory/outreach-log.md` and `memory/<today>.md`; commit + push (`git add -A && git commit -m "memory: follow-up drafts <date>" && git push`).
3. **Notify Spencer** (both):
   - `PushNotification` (status "proactive", <200 chars): prep → "N follow-up drafts are in your Gmail Drafts for tomorrow. Quick look, then send." · remind → "N follow-ups are DUE TODAY, drafts ready in Gmail. Review + send now: <names>."
   - Also email him at spencer@spencerzvoice.com from himself via FGAC (same as the digest does), subject `VO follow-ups due today: N drafts ready` / `...due tomorrow...`, body = table of contact | company | touch # | one-line angle | anything to double-check before sending. If the send is blocked by FGAC's whitelist, say so in the run summary.
4. If nothing is due, send nothing and stay quiet (no "all clear" noise), but still update the queue for anything sent.

## Standing don'ts
Never send, schedule, or drop a contact silently. A "drop this" decision must be enacted in Gmail itself (delete the draft), not just written in memory (Kyle Osher lesson, 2026-09-23). Never add marketplace jobs to the tracker.
