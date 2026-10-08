# VO Pipeline Digest - routine prompt (source of truth)

Run by the Code routine "VO Pipeline Digest (repo)" (daily 07:15 UTC), which also does the morning follow-up reminder (Step 0b). Edit THIS file to change the digest; the routine prompt only points here. Moved off Cowork 2026-10-07 (Cowork routine `trig_01PTnXAXdmvLjyqBCnsgPXVz` disabled, not deleted).

---

You are running a scheduled daily task for Spencer (spencerzpearman@gmail.com) to keep his "VO Outreach Pipeline Tracker" Google Sheet in sync with his Gmail activity for his voiceover (VO) business outreach - agencies, producers, old client reconnects, and coaching contacts.

THE CHAIN OF COMMAND IS FIXED AND NON-NEGOTIABLE (Spencer, 2026-09-25): (1) check Gmail for EVERY active row, fresh, this run -> (2) only then update the tracker from what Gmail shows -> (3) only then send the digest, built from the updated tracker. Never write to the sheet before step 1 is finished for every active row. Never send the digest before the sheet writes are read back. A previous run's work is NOT a source - never skip rows because "the sheet was already verified yesterday" and never limit the Gmail check to "what changed since the last run". That shortcut is exactly what produced stale digests (2026-09-25).

IMPORTANT - connector rules:
- Use the FGAC.ai connector (mcp__FGAC_ai__*) for ALL Gmail and Google Sheets/Drive access. Do NOT use the built-in Gmail connector - it has a known bug returning stale/incomplete thread search results and misses recent messages.
- For Gmail, use FGAC's google_api_get against gmail/v1/users/me/... endpoints (or gmail_list/gmail_read as appropriate) to check both the Sent and Inbox folders for anything related to Spencer's VO outreach.
- For Google Drive, use FGAC's google_api_get against drive/v3/files (with an appropriate query) to search - do NOT use a stored link, URL, or file ID.

IMPORTANT - access/permissions: Spencer already has standing FGAC permissions configured for this spreadsheet (read & write) and for sending email to spencer@spencerzvoice.com. These are persistent - do NOT call request_access preemptively, defensively, "just to check," or as a first step. Just call sheets_read_range, sheets_update_range, and the Gmail send directly - they will succeed. Only call request_access if one of those specific calls actually fails with a real permission-denied/access-required error from the API itself, and even then call it at most once per distinct missing permission, note it plainly in the final summary, and do not retry it. request_access always generates a brand-new approval link regardless of whether access already exists, so calling it unnecessarily creates a needless manual approval step for Spencer and is the reason this task has been silently stalling for hours each day waiting on an approval it never actually needed. Do not repeat that mistake.

FOLLOW-UP CADENCE - use this to decide what counts as "due", alongside the sheet's Follow-Up Flag column:
- Cold agency / brand outreach: follow up 7-10 days after last contact. 10+ days, no reply = OVERDUE.
- Warm / recurring clients: 2-3 weeks if mid-conversation on a Gmail-VERIFIED live project or quote (Step 3d); 4-8 weeks for a pure check-in; 6+ months = soft reconnect.
- A contact who already got ONE follow-up with no reply: at most ONE more touch, and only with a NEW hook (fresh sample, new credit, real reason) - never a third generic "just bumping this". After that, note them for an October revisit and stop listing them as due.
- Bounced / "Fix Email & Resend": always actionable - due until the address is fixed and the email resent.

NEXT-TOUCH DATES + NO SELF-REFERENCE (Bingo, 2026-10-07, after the Oct 7 digest listed 9 "due today" rows when none were due):
- Bingo writes the real follow-up schedule into Next Action as "Next touch: <Day YYYY-MM-DD>", "NOT DUE - ..." or "NOT ON THE CLOCK - ...". These come from Bingo's follow-up ledger and are AUTHORITATIVE. Never list a row as due before its "Next touch" date, and never list a "NOT DUE" or "NOT ON THE CLOCK" row. Never overwrite or remove those Next Action entries; add a dated note in Notes instead.
- Never write "due now", "DUE NOW", "OVERDUE" or "due" into Next Action or Notes. Due-ness is decided fresh every run from Gmail + the cadence; a phrase an earlier run wrote is NOT evidence that anything is due. (Root cause of the Oct 7 error: a Sep 27 run wrote "2nd/final follow-up (NEW HOOK) due now" on warm reconnect rows at 19 days, and later runs trusted their own note.) If a row needs a touch, write "Next touch: <date>" computed from the cadence.
- DAYS SINCE LAST CONTACT - mechanical, per row: after the Step 4 re-read, copy each listed row's own column J value ("Days Since Last Contact", a formula = today minus column I) into its digest line. If J is blank or not a number, compute today minus THAT row's column I and add "(J missing)". Before sending, check: every line's number must equal its own row's J; if two or more lines show the same number, re-check each against its row. Never reuse one number for several rows (the Oct 7 digest printed "26 days" for 9 rows whose real gaps were 21 to 64 days).
- Warm pure check-in window = 28 days minimum. A warm/reconnect row at 26 days is NOT due.
- A row whose Status contains "Responded", where Spencer answered the contact's last reply, is not due unless Next Action gives a Next touch date that has arrived.
- Columns J and K are formulas. Never type a value into J or K, and when appending a row leave J and K empty. Step 4b repairs them every run.

Step 0 - Read Bingo's follow-up ledger (this routine runs on the Bingo repo; Spencer moved it off Cowork 2026-10-07):
- `git pull`. Read `memory/followups-queue.md` (the schedule ledger: every follow-up's reminder date and overdue date) and the "Follow up on" lines in `memory/outreach-log.md`. CLAUDE.md applies (FGAC only, never the Gmail/Google_Drive connectors).
- The ledger decides WHEN. A contact on the ledger is due today only if its reminder date is today or earlier and Step 3 shows the touch has not gone out and no reply came in. A ledger date in the future = not due, whatever the tracker flag says. A contact in the ledger's "Unscheduled backlog" = not due (list it nowhere except, on Mondays, one HEADS UP line "backlog waiting on your go/no-go: <names>").
- Rows not on the ledger fall back to the FOLLOW-UP CADENCE rules below.
- If the tracker's Next Action and the ledger disagree on a date, the ledger wins; fix Next Action to "Next touch: <ledger date>" and say so under HEADS UP.

Step 0b - Morning follow-up duties (merged in 2026-10-07 from the "VO follow-ups - morning reminder" routine `trig_01DpDZ6iUiSxXXWxc4eAreof`, now disabled; Spencer: the routine list was supposed to get smaller):
Read `.claude/skills/followup-drafts/SKILL.md` and do its MODE = remind work as part of this run. NOTHING IS EVER SENT OR SCHEDULED - drafts and reminders only.
- Via FGAC confirm which queued drafts in `memory/followups-queue.md` were SENT since the last run (Sent folder, same thread) and which drafts still exist. For each confirmed send, roll the ledger forward from the SEND date per the cadence table (next reminder + overdue dates, or after a final touch the quarterly long-tail LT1 date per the skill) and update `memory/outreach-log.md`. Tracker updates for these rows happen in Step 4 like any other row.
- Work out what is due TODAY: ledger rows whose reminder date is today, or whose overdue date is today and still unsent. Triage against live Gmail (skip replied / OOO / held / 3rd-touch-done with no LT touch due). Make sure a draft exists for each (threaded; LT touches = new email per the skill), creating missing ones, max ~12, in Spencer's voice with real sourced new proof per the skill and the outreach-email voice rules.
- Those rows ARE the digest's FOLLOW-UPS DUE TODAY section (mark each "draft ready" when the draft exists). Overdue-day rows say "last day of the window".
- If anything is due today, the Step 6 push leads with: "N follow-ups DUE TODAY: drafts are in your Gmail Drafts. Review + send now: <names>." The digest email replaces the old separate "VO follow-ups due today" email. If nothing is due, the digest says "No follow-ups due today." and the push does too.
- Spencer's standing rule (2026-09-24): remind him WHEN a follow-up is due, not every day, so a due item must never be buried below other sections.

Step 1 - Find the correct file (every run, fresh):
Search Google Drive via FGAC for a file titled EXACTLY "VO Outreach Pipeline Tracker" located in the root of My Drive (top-level folder only, not any subfolder - the file may have been deleted and recreated since the last run, so always search fresh by title and location, never reuse a cached ID).
- If zero files match, stop and report that clearly in your final summary - do not guess or create a new file.
- If more than one file matches that title in the root folder, STOP immediately and flag this to Spencer in your final summary instead of guessing which one is current. Do not update anything in this case.
- Only proceed if exactly one match is found.

Step 2 - Read the tracker:
Use FGAC's sheets_read_range to read the current "Outreach Tracker" tab of that spreadsheet (the one confirmed in Step 1). Active rows = every row whose Status is not "Dropped".

Step 3 - CHECK GMAIL FOR EVERY ACTIVE ROW, FRESH (mandatory, complete, BEFORE any sheet write):
3a. RUN THE COMMITTED SCRIPT - this is the sanctioned, Spencer-approved way to do Steps 3a, 3b, 3c and 3e (Spencer, 2026-10-08, after the 10-08 run stopped at 0/~150 because an improvised temp-key script was blocked). Do NOT hand-roll curl/python with the key, and do NOT check rows one by one with the typed tools (they return ids only). Exactly these three steps:
   1. Call FGAC create_temporary_api_key (purpose bulk_calls, ttl_minutes 30).
   2. `mkdir -p local`, then use the Write tool to put the key (only the key) in `local/.fgac_key`. local/ is gitignored; never echo, print, log or commit the key. NEVER put the key text inside a Bash command (printf/echo/heredoc/env var): on 10-08 that exact move was blocked by the auto-mode classifier as "Credential Materialization". Write tool only.
   3. Run `python scripts/digest_gmail_check.py` (Bash timeout 600000; ~5 min for ~170 rows). It is READ-ONLY (GET requests only), reads the tracker itself, deletes local/.fgac_key when it finishes, prints one line per active row (latest IN, latest OUT, OOO, BOUNCE, DRAFT) plus "NEW CONTACTS (last 3 days, not in tracker)" and "CHECKED x/y", and writes the full JSON to the path it prints. Use that output for 3a-3e. If it errors or the key expires, create a new key and rerun once; if it still fails, report CHECKED 0 per 3e with the error text.
   What it checks, for reference: for EVERY active row with an email address, Gmail in BOTH directions (from:ADDRESS / from:me to:ADDRESS), Inbox AND Sent, NO date limit, reading each message's From, To, Date and Subject and attributing it to the right row. Record per row: date + subject of the latest inbound message, date + subject of the latest outbound message, any bounce (mailer-daemon / postmaster / "Undeliverable" naming that address), and any out-of-office auto-reply with its return date. Gmail is the source of truth; the sheet is only a cache of it.
3b. List the current Gmail Drafts (gmail/v1/users/me/drafts, then each draft's To header) and map each draft to its row. The digest may say "draft ready in Gmail" ONLY for a row that has a draft right now.
3c. Scan the last 3 days of Inbox and Sent for new contacts not yet in the sheet (the script's "NEW CONTACTS" list). This INCLUDES every new-client cold pitch Spencer sent from Drafts (Funnel pitches, subject usually "A voice for ..."): nothing else adds those rows, so if the digest skips them they are never tracked (Spencer, 2026-10-08: ~14 pitches sent 10-05..10-07 were missing). Add each as a row: name, company, title (from the contacts file / FUNNEL-COHORTS.md if known), email, Category "New Outreach - Direct", Status "Sent", Date First Contacted + Last Contact Date = the Gmail send date. If the previous digest did not complete, widen the scan to the days since the last completed run (`--days N`).
3d. Reconcile each row against Gmail: Last Contact Date = the later of the latest inbound and latest outbound message (even when that differs from the sheet). If the contact replied after Spencer's latest outbound, the row is NOT due - update Status to reflect the reply. If Status says Sent / Follow-Up Sent / Reconnect Sent but Gmail has NO outbound message to that address, do not list it as due: put "No sent email to this address found in Gmail - status unverified" in Notes and list it once under HEADS UP. VERIFY CLAIMS: any text in Status, Next Action or Notes that asserts a live/in-progress/active project, a pending quote, an awaited deliverable, or "awaiting scripts/budget" must be backed by a Gmail message in the last 30 days in that contact's threads that actually mentions it. If it is not backed: do NOT repeat it as fact. Replace it in Notes and Next Action with "Unverified - no Gmail activity on this since [date of last message]" and treat the row as an ordinary check-in for the FOLLOW-UP CADENCE. The digest may only use the words "live project", "in progress" or "active project" for a row that passed this check. Never copy a claim forward from a previous run's Notes without re-verifying it.
3e. Coverage count: keep CHECKED = number of active rows actually checked against Gmail in 3a, and ACTIVE = number of active rows with an email address. If CHECKED < ACTIVE for any reason (error, time), finish what you can, but say so plainly in the digest's second line and in the push notification, and name the rows not checked - never present a partial check as complete.

Step 4 - Update the sheet (only after Step 3 is complete):
Using FGAC's sheets_update_range, update ONLY these columns based on what Gmail shows (Step 3): Status, Last Contact Date, Notes, and - only to correct or clear an unverified claim (Step 3d) - Next Action. Before writing any row, re-read that row's contact name/company in the same call sequence and read it back after writing.
- Leave "Days Since Last Contact" and "Follow-Up Flag" completely alone - these are formulas that recalculate automatically.
- Do NOT touch the Dashboard tab or the Legend tab.
- If you find a genuinely new DIRECT / AGENCY / reconnect VO client or contact in Gmail that isn't in the sheet, add them as a new row.
- HARD EXCLUSION - NEVER add a Voices.com row. No Voices.com auditions, private invites, job-awarded notices, or clients - not even a paid/awarded job, not even a private invite with a deadline today. Voices.com activity is managed entirely on the Voices.com platform; the tracker is direct/agency/reconnect relationships only. If a Voices.com invite has a deadline of today or tomorrow you may add ONE line under HEADS UP noting it, but do NOT create a tracker row and do NOT treat it as a tracked contact. Same for Bodalgo/Voice123 marketplace auditions.

Step 4b - Formula guard (every run, after the Step 4 writes; Spencer 2026-10-07: "make sure this doesn't happen again"):
Columns J (Days Since Last Contact) and K (Follow-Up Flag) were found missing or overwritten with typed numbers on ~90 rows on 2026-10-07, so the digest was eyeballing dates. Repair them every run, whether or not they look broken:
- Find LAST = the last row with a contact name in column A.
- Call FGAC sheets_edit on the "Outreach Tracker" tab (look its sheetId up via google_api_get v4/spreadsheets/<id>?fields=sheets.properties) with ONE request: {"copyPaste": {"source": {sheetId, startRowIndex: 1, endRowIndex: 2, startColumnIndex: 9, endColumnIndex: 11}, "destination": {sheetId, startRowIndex: 2, endRowIndex: LAST, startColumnIndex: 9, endColumnIndex: 11}, "pasteType": "PASTE_FORMULA"}}. This re-pastes the row-2 formulas down J:K; rows that were fine are unchanged.
- First confirm J2 and K2 still hold the formulas (google_api_get .../values/'Outreach Tracker'!J2:K2?valueRenderOption=FORMULA): J2 starts "=IF(I2=" and K2 starts "=IF(G2=\"Not Sent\"". If not, do NOT paste; put "J2/K2 formulas missing - Bingo must restore" under HEADS UP.
- Then read J:K for the last 3 named rows and confirm J is a number (or blank where I is blank).
Then re-read the tracker (at least every row you changed) so the digest is built from the updated sheet, not from memory.

Step 5 - Send Spencer a digest email to spencer@spencerzvoice.com (his VO BUSINESS address - NOT his personal spencerzpearman@gmail.com). Build it ONLY from the Step 3 Gmail results and the Step 4 updated sheet.

IMPORTANT - encoding: the FGAC send tool does NOT reliably handle non-ASCII characters in the Subject line (and possibly body) - it has previously produced mojibake from em dashes, curly bullets, and middle dots. Use PLAIN ASCII ONLY in subject and body: hyphen "-" not em dash, plain "*" or "-" not a bullet, "x" or "-" not a middle dot. Straight quotes only.

Keep the digest SHORT and SCANNABLE - Spencer reads it on his phone in under 30 seconds. Subject: "VO Pipeline Digest - [Month Day, Year]" (plain hyphen).

The digest MUST contain these sections in THIS ORDER. Omit a section only if it is genuinely empty.

1. ONE-LINE SUMMARY: "X new contacts, Y replies, Z bounces, N follow-ups due today."
   Then a second line, always: "Gmail checked: CHECKED/ACTIVE active rows, as of [HH:MM UTC]. Tracker updated after the check." (plus the list of unchecked rows if CHECKED < ACTIVE).

2. FOLLOW-UPS DUE TODAY - this is the actionable core of the digest, and the reason Spencer reads it. List EVERY row whose Follow-Up Flag is "OVERDUE - Follow Up Now", "Due Soon", or "Fix Email & Resend", PLUS any row the FOLLOW-UP CADENCE rules say is due even if the flag has not caught up yet. For each line: contact name, company, the action needed ("follow-up", "fix email + resend", or "2nd follow-up - NEW HOOK only"), days since last contact (from the Gmail-based Last Contact Date), and "draft ready" only if Step 3b found one. Order: OVERDUE first, then Due Soon, then fixes. If a company has 3+ due, group it as one line with a count and list the names after. This section appears EVERY DAY until each row is actioned - do NOT drop it, shorten it, or soften the language just because the same names appeared yesterday.

EXCLUDE from this list (even when the Follow-Up Flag column still says "Due Soon" or "OVERDUE" - that column is DATE-ONLY and does not know about any of the following):
- any row whose Status is "Dropped", "Hold", "N/A", or "Job Awarded - Active";
- any row whose Next Action or Notes text says it was dropped/scrapped, is on hold, is "not due", "do not surface", or is set for an October / later revisit;
- any row where Step 3 shows Spencer already sent the follow-up, or the contact already replied;
- any row where Step 3d found no sent email at all (HEADS UP instead);
- any row with an unexpired OOO auto-reply (list it under HEADS UP with the return date instead);
- any row in the "Old Client Reconnect" category, or otherwise a warm/recurring pure check-in with no open live thread, where the FOLLOW-UP CADENCE window above (4-8 weeks for a pure check-in) has NOT yet elapsed since Last Contact Date - even if the sheet's Follow-Up Flag says "Due Soon" or "OVERDUE - Follow Up Now". That flag is a fixed day-count formula tuned for the 7-10-day cold-outreach rule; it does not know the longer warm cadence applies to these rows. For any row that looks like a warm/reconnect check-in, compute due-ness yourself from Last Contact Date + the FOLLOW-UP CADENCE rule for its category, and only list it once that window has actually passed.
When in doubt, trust the Notes/Next Action text over the flag, and trust the FOLLOW-UP CADENCE rule over the flag's raw day count for any warm/reconnect row.

3. THIS WEEK (MONDAYS ONLY - check today's date first; include this section only if today is a Monday): every follow-up due now or coming due within the next 7 days, grouped by company, so Spencer can plan the week ahead.

4. NEW CONTACTS - one line each: name, what it is, why it matters.

5. REPLIES / STATUS CHANGES - one line each: who replied, the gist, and what it needs from Spencer next.

6. HEADS UP - bounces to fix, OOO auto-replies with return dates, rows with no sent email found, duplicate-file or access flags.

End with the spreadsheet's URL.

Step 6 - Final summary (this becomes the PUSH NOTIFICATION - write it as a prompt to act, not a status report):
- LINE 1, mandatory: "[N] follow-ups due today:" followed by the top 3-5 names/companies, overdue first. If none: "No follow-ups due today."
- LINE 2, mandatory: "Gmail checked CHECKED/ACTIVE rows; tracker updated: yes/no" + one line per change, or "no updates".
- Then: anything needing Spencer's attention (duplicate tracker files, sheet not found, a real access error, a bounce, an incomplete Gmail check).
Keep the whole summary under ~6 lines.

Step 7 - Log (repo):
Append to `memory/<today>.md` (create if missing) a section "## Pipeline digest (cloud routine)": N due + names, rows changed, formula guard result, anything flagged. Touch nothing else in memory/. Then `git add -A && git commit -m "digest: <date> - N due, formula guard OK|FAIL" && git push` (pull --rebase and retry once on a push conflict).
Usage: on any session-limit / rate_limit error follow CLAUDE.md routine override 7 (stop, commit + push, one push notification, no retry loop).