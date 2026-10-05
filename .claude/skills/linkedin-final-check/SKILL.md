---
name: linkedin-final-check
description: >-
  Final job verification for outreach contacts on their live LinkedIn profile, done by Bingo in the
  Claude Desktop app's built-in browser. Clears the yellow [NOT READY: final LinkedIn check pending]
  line from pitch drafts that pass, and pulls the recipient from any draft whose contact has left.
  Use for "LinkedIn-check the drafts", "run the LinkedIn check", or when the daily desktop scheduled
  task fires. Desktop only. Cloud sessions can't load LinkedIn.
---

# LinkedIn final check (Spencer, 2026-10-05: "this is your job")

The LinkedIn profile page is the final word on whether someone still holds the job (Spencer, 2026-10-04,
"no questions or excuses"). Apollo, company pages and search results only find people. This skill
is where the final check actually happens. It runs on Spencer's computer, because only a session
with a real browser can open LinkedIn.

**Hard limits:** drafts only. Never send, schedule or delete an email. Never touch the hook, the
`[YOUR TAKE]`, or anything Spencer wrote. Gmail goes through FGAC only (`mcp__FGAC_ai__*`, account
`spencer@spencerzvoice.com`). Never use the `Gmail` / `Google_Drive` connectors, which are his personal account.

## Steps

0. `git pull`. Load the `anthropic-skills:built-in-browser` skill before the first browser call.
   If no built-in browser (`mcp__Claude_Browser__*`) is available, stop and report:
   "LinkedIn check didn't run: no browser in this session." Never fall back to WebFetch, search
   snippets or Apollo. None of those count as the final check.

1. **Find the drafts to check.** FGAC `google_api_get gmail/v1/users/me/drafts?maxResults=200`, then
   each draft with `format=full`. Decode the HTML body. Check a draft if its body contains
   `[NOT READY: final LinkedIn check pending` or `[VERIFY EMPLOYMENT:`. Also check any new-client pitch
   draft (not a reply, recipient never emailed) whose recipient has no PASS line in
   `reference/client-acquisition/LINKEDIN-CHECKS.md` dated within the last 14 days.

2. **Get the profile URL.** Look it up, in order: `reference/client-acquisition/APOLLO-LEDGER.md`
   (today's lines first), `ROSTER.md`, `contacts/*.md`. If there's none, search DuckDuckGo in the
   browser for `<Name> <Company> LinkedIn` and take the `linkedin.com/in/...` result whose name and
   company match. The search results page is only a lead. The profile page is the source.

3. **Open the profile in the built-in browser** (signed in as Spencer) and read the top
   Experience entry plus the headline.
   - **PASS:** the current position (shown as "Present") is at the draft's company, and the title is
     the same role or close to it.
   - **FAIL, LEFT:** the current position is at another company, or the company role has an end date.
   - **UNRESOLVED:** the profile won't load, is private or signed-out, several same-name profiles
     could fit, or the title is a different job at the same company. Never guess. UNRESOLVED stays
     NOT READY.
   Write down exactly what the page shows: headline, current title, company, start date.

4. **Act on the draft.** Re-GET the draft right before any PUT, because Spencer edits drafts himself.
   If it changed since step 1, redo step 1 for that draft.
   - **PASS:** remove only the yellow NOT READY / VERIFY EMPLOYMENT span and the `<br><br>` right
     after it. Change nothing else.
   - **FAIL, LEFT:** clear the `To` header (the body stays). Replace the yellow line with
     `<span style="background-color:#ffff00">[CONTACT LEFT: <Name> now at <New company> per LinkedIn <date>. Needs a new contact]</span>`.
     In `ROSTER.md`, mark the row LEFT with the date.
   - **UNRESOLVED:** leave the draft alone.
   Build the PUT the house way: `google_api_modify PUT gmail/v1/users/me/drafts/<id>` with
   `{id, message:{raw}}`. The raw message is base64url RFC 2822 with To, From
   `Spencer Pearman <spencer@spencerzvoice.com>`, the Subject unchanged, and text/html utf-8.
   A PUT drops labels, so re-apply the draft's `Funnel <X>` label afterwards: look up the label id
   via `gmail/v1/users/me/labels`, then POST `messages/<newId>/modify` with `addLabelIds`. Read the
   draft back to confirm.

5. **Log every check**, PASS or not, in `reference/client-acquisition/LINKEDIN-CHECKS.md`
   (create it with a header if missing):
   `YYYY-MM-DD | Name | Company | linkedin.com/in/... | "<headline / current title as shown>" | PASS / LEFT / UNRESOLVED (+why)`.
   Append one line per run to `memory/<today>.md`. Then
   `git add -A && git commit -m "linkedin-check: <date> - P pass, L left, U unresolved" && git push`.

6. **Tell Spencer** (a desktop notification, plus the session summary): "LinkedIn check: P cleared,
   L left (names + new company), U unresolved (names + why)." List the drafts that are now ready
   to schedule. If anyone LEFT, recommend the next step: an Apollo match on the ROSTER backup (with
   waterfall email, per the 10-05 rule), then this check again.
