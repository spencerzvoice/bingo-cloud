> **2026-10-05: superseded.** These rules now live in CLAUDE.md, "Routine overrides". Every routine loads that file and it overrides the prompt text, so nothing below needs pasting. Kept for history.

# Routine patch: source link inside [YOUR TAKE] (2026-10-03)

Bingo can't edit these two routines (update_trigger refuses routines created outside an agent). Spencer pastes this in at claude.ai/code/routines. Delete this file once both are done.

## Paste this paragraph into BOTH routines

Daily VO Lead Batch (`trig_01GycTKwkwLwvNhYL6huQQ2w`): put it right after the "HOOK = EVENT LINE ONLY, SPENCER WRITES THE TAKE" bullet.
Hook Sweep (`trig_01FQkrArSyKVS3241Qu8qCcM`): put it right after the "HOOK RULE" paragraph.

```
SOURCE LINK IN [YOUR TAKE] (Spencer, 2026-10-03, HARD RULE; overrides every plain "[YOUR TAKE]" in this prompt). Spencer can't write a take without seeing what the hook refers to, so the placeholder always carries a clickable link to the hook's source:
<span style="background-color:#ffff00">[YOUR TAKE] Source: <a href="URL">Publication, Mon D, YYYY</a></span>
The link is the exact page you opened that the event line is based on. If the line says watched/spot/film, link the video page itself (YouTube/Vimeo/iSpot). Otherwise link the LinkedIn post, press release or article. Two links max (article + video), separated by " · ". No openable URL = no hook: use the [HOOK: nothing current found...] placeholder instead. The event line says only what the linked page shows. On 10-03, "Just watched the Ferrari Hypersail film" was backed by a press release with no film. When you read a draft back, check that the [YOUR TAKE] placeholder contains a working <a href> link.
```

## Hook Sweep only: add to the TAKE PENDING bullet in step 1

```
If the [YOUR TAKE] placeholder has no "Source:" link, add one. Use the source URL logged for that company in FUNNEL-COHORTS.md or the contacts docs, or WebSearch the event and open the page to confirm it backs the event line. If no source backs the line, replace it with a line that is backed, or with the [HOOK: ...] placeholder.
```

## Also replace this example line in both

`"Just watched the Ferrari Hypersail film."` → `"Saw the Toast Fuel launch."` (the ABB line wasn't backed by its source).

## Both routines also need: EMPLOYMENT QC GATE (Spencer, 2026-10-04)

```
EMPLOYMENT QC GATE (Spencer, 2026-10-04, HARD RULE). Before drafting to anyone, and before calling any draft ready, confirm the contact's CURRENT employer from a source opened in this run: an Apollo people match run today (current employer + title must match), plus the LinkedIn profile page if it opens. Apollo email_status "verified", a roster checkmark or an earlier run's check is NOT proof of current employment. If it can't be confirmed (no profile, several same-name profiles, blocked, Apollo error): put <span style="background-color:#ffff00">[VERIFY EMPLOYMENT: couldn't confirm <Name> is still at <Company>. Check before sending]</span> as the first line of the draft body, list the contact under "NOT READY: EMPLOYMENT UNCONFIRMED" at the TOP of the digest and in the push notification, and never count them as send-ready. If they've left: clear the draft's To field and swap to the backup only after the backup passes this same check.
```

## Both routines: FINAL LINKEDIN CHECK (Spencer, 2026-10-04: "no questions or excuses")

```
FINAL LINKEDIN CHECK (Spencer, 2026-10-04, HARD RULE). The only proof a contact still holds the job is their live LinkedIn profile page showing <Company> as the current position. This cloud run cannot open LinkedIn, so EVERY draft you create or touch starts with this as its first line: <span style="background-color:#ffff00">[NOT READY: final LinkedIn check pending for <Name>, <Title>, <Company>. Delete this line once done]</span>. List all NOT READY drafts at the TOP of the digest and in the push notification, with each person's LinkedIn profile URL if search found one, so the check takes Spencer seconds. Never call a draft send-ready, and never remove that line yourself.
```

## Lead Batch: ALWAYS RUN WATERFALL EMAIL (Spencer, 2026-10-05)

```
APOLLO WATERFALL EMAIL, ALWAYS (Spencer, 2026-10-05: "always run it when we're enriching contacts"). Every Apollo people match / bulk match you run for a contact sets run_waterfall_email: true. It's async: take the top-level request_id and poll apollo_webhook_result_show, backing off (~15s, then ~30s, up to ~3 minutes). Use the email it returns only if it comes back verified. Credits vary by provider; log the actual spend per person in APOLLO-LEDGER.md. Standing approval, so don't ask.
```

## Lead Batch: REPLACE the whole "DRAFT FORMAT - HARD RULE" block (Spencer, 2026-10-05)

Delete the old DRAFT FORMAT block and paste this in its place. Until you do, the `pitch_draft_qc.py` hook will reject the routine's drafts, and its error message tells the routine what to fix.

```
DRAFT FORMAT - HARD RULE (Spencer, 2026-10-05: Spencer's own Hitachi Rail email is the template, "copy across all other drafts now and moving forward"). Read reference/client-acquisition/PITCH-TEMPLATE.md and build every pitch from it word for word, filling only the slots: greeting name, optional hook paragraph (event line + [YOUR TAKE] Source link), company, 2-4 credits, exact video title + link (or VIDEO TITLE PENDING), video/spot. First line of every cloud-built draft: the yellow [NOT READY: Bingo's LinkedIn check pending ...] line. The repo hook .claude/hooks/pitch_draft_qc.py blocks any draft write that doesn't match. If it blocks you, rebuild the draft to the template and retry. Never route around it.
```
