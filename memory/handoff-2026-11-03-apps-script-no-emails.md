# Handoff: stop the "[Bingo]" follow-up emails (2026-11-03, cloud chat → desktop)

**Why desktop:** the two Apps Scripts live in spencer@spencerzvoice.com's Google account. Updating them means pasting code into the Apps Script editor in Spencer's Chrome. Cloud sessions have no browser, and FGAC can't write Apps Script projects.

**Task (Spencer, 2026-11-02):** "I don't need six different emails telling me that there are follow-ups going out ... Everything should be in the digest. I shouldn't be receiving multiple emails a day from myself on different schedules or tasks ... Nothing else." On 11-03 he asked for this handoff "so we can finally fix this".

**Done looks like:** both Apps Script projects run the repo versions. The Follow-up Sender has ONE trigger (`tick`, every minute) and no `eveningPreview` trigger. No "[Bingo] ..." email reaches Spencer after that. Report back to Spencer in one or two lines.

## Already done (don't redo)
- ✅ Repo side merged to main as `4270ad6` (11-03). The new code is in:
  - `scripts/apps-script/FollowupSender.gs`: the 19:00 `eveningPreview` email is retired (the function stays as a no-op stub). `setup()` installs only `tick`. `alert_()` no longer emails; it writes a `Log` line. HELD/ERROR were already recorded in the Queue row.
  - `scripts/apps-script/DigestPrep.gs`: `watchdog()` no longer emails. It appends each problem once a day to a new tab `Watchdog_Log` in the Queue Sheet.
  - The Follow-up Prep routine prompt (no email, no push), the Digest prompt (new `autosend` block that reads Queue / Log / Watchdog_Log / Prep notes) and `scripts/digest_render.py` ("Automatic follow-ups" section) are all live from main.
- ✅ Gmail check, 11-03: the old scripts are still sending. Examples: "[Bingo] 7 follow-ups queued to send automatically" (11-03 19:01 Lisbon) and "[Bingo] Follow-up HELD: Patrick Nadjarians (Acclaim Lighting)" (11-02).
- FGAC refuses Gmail settings writes, so a filter isn't an option. Fixing the scripts is the only fix.

## Steps
1. `git pull`. Confirm `git log --oneline -1 -- scripts/apps-script/` shows `4270ad6` or later.
2. **Follow-up Sender.** Chrome, account u/3: `https://script.google.com/u/3/home/projects/10aNY35EDHyh1dd5B__8_Nk44x9PTdPrfH2YZamcsqqOk8nqasIRDbJMM/edit`
   - Check the file list on the left. If the project has more than one `.gs` file, search the others for `ALERT_TO` and `sendEmail` first: the new code removed the `ALERT_TO` constant.
   - Replace the main file's whole contents with `scripts/apps-script/FollowupSender.gs`. Easiest route: `Get-Content -Raw scripts\apps-script\FollowupSender.gs | Set-Clipboard` in PowerShell, then click into the editor, Ctrl+A, Ctrl+V. Fallback: in Chrome JS, `monaco.editor.getModels()[0].setValue(<file text as a JSON string>)`. Save with Ctrl+S.
   - Read back: the editor must contain `RETIRED 2026-11-02` and must NOT contain `ALERT_TO`.
   - Pick **`setup`** in the function dropdown and **check the picker shows `setup`** before you click Run (on 10-21 the wrong function ran because the picker hadn't changed). Run it. It deletes all triggers and reinstalls only `tick`.
   - Open the Triggers page (clock icon) and confirm exactly ONE trigger: `tick`, time-based, every minute. No `eveningPreview`.
3. **Digest Prep.** `https://script.google.com/u/3/home/projects/1g939YAXbqrscyx_zNNwOeIA9Lz6zmOxVDp9nkQVKBEwhwVJBo7--Fd5Q/edit`
   - Replace the file with `scripts/apps-script/DigestPrep.gs` the same way and save.
   - Read back: the file must contain `Watchdog_Log` and no `MailApp`.
   - Do NOT run `setup()` here: the trigger function names (`run`, `runThreads`, `watchdog`) didn't change.
   - Optional check: run `watchdogDryRun` (it sends nothing and writes tab `Prep_Watchdog`).
4. **Verify.**
   - In the Queue Sheet `1YVJbPnETd3gkX8dAwdHsiqijojgMlyCL_4Jaskk9aao`, tab `Log`: there is a new `setup` line ("no evening preview email since 2026-11-02"), and `Log!F1` (heartbeat) is under 2 minutes old. If the heartbeat is stale, the sender is broken: fix it before leaving.
   - After 19:05 Lisbon the same day, check FGAC `gmail/v1/users/me/messages?q=from:spencer@spencerzvoice.com subject:"[Bingo]" newer_than:1d`: there should be no new one.
5. **Close out.** Delete the `**PENDING desktop (11-02)...` line from MEMORY.md under "Tools & known issues". Append a dated line to `memory/<today>.md`. Commit + push.

## Rules that apply
- AGENTS hard rule 0: do it in Spencer's Chrome yourself; don't hand him click steps.
- Don't touch the queued follow-up rows. The sender must keep sending through all of this; a few minutes without ticks while you save is fine.
- If an auth prompt appears when running `setup`, it's Spencer's own account and he has already granted this project. Click Allow on his behalf only if it's the standard Apps Script consent for this same project, and say so in the report.

## Report back
One line to Spencer, for example: "Apps Scripts updated: sender has 1 trigger (tick), no evening email, alerts and watchdog now go to the digest only. Heartbeat OK." Plus anything that failed.
