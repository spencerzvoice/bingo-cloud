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
   `[NOT READY:` (any wording, e.g. "Bingo's LinkedIn check pending") or `[VERIFY EMPLOYMENT:`. Also check any new-client pitch
   draft (not a reply, recipient never emailed) whose recipient has no PASS line in
   `reference/client-acquisition/LINKEDIN-CHECKS.md` dated within the last 14 days.

2. **Get the profile URL.** Look it up, in order: `reference/client-acquisition/APOLLO-LEDGER.md`
   (today's lines first), `ROSTER.md`, `contacts/*.md`. If there's none, use LinkedIn's own people
   search in the signed-in browser: `https://www.linkedin.com/search/results/people/?keywords=<Name>%20<Company>`,
   then collect `a[href*="/in/"]` links and the result text with `javascript_tool`. Take the one whose
   name and headline match the company (fallback: DuckDuckGo `<Name> <Company> LinkedIn`). The
   search results page is only a lead. The profile page is the source. Save the URL you found in the
   LINKEDIN-CHECKS line so the next run doesn't search again.

3. **Open the profile in the built-in browser** (signed in as Spencer, one-time sign-in done
   2026-10-05; it persists). Go straight to `https://www.linkedin.com/in/<slug>/details/experience/`,
   because the main profile page lazy-loads Experience and its text often comes back without it. Then run
   `javascript_tool`: `await new Promise(r=>setTimeout(r,2500)); location.href+"
"+document.title+"
"+(document.querySelector('main')||document.body).innerText.slice(0,500)`.
   If the URL comes back as `/authwall` or a login page, the session expired: stop the whole run,
   mark everything UNRESOLVED, and tell Spencer "LinkedIn signed out in the app browser. Sign in once
   (Ctrl+Shift+B) and I'll rerun." Never type his password.
   - **PASS:** the current position (shown as "Present") is at the draft's company, and the title is
     the same role or close to it.
   - **WRONG FIT (still employed, wrong buyer):** the role is current, but the work described is not
     video, content, creative, brand or production for media (e.g. Smithsonian's Ariana Lilligren
     runs exhibit fabrication shops, 2026-10-05). Leave NOT READY, log it, and recommend a video or
     content contact at the same company.
   - **FAIL, LEFT:** the current position is at another company, or the company role has an end date.
   - **UNRESOLVED:** the profile won't load, is private or signed-out, several same-name profiles
     could fit, or the title is a different job at the same company. Never guess. UNRESOLVED stays
     NOT READY.
   Write down exactly what the page shows: headline, current title, company, start date.

4. **Act on the draft.** Re-GET the draft right before any PUT, because Spencer edits drafts himself.
   If it changed since step 1, redo step 1 for that draft.
   - **PASS:** remove only the yellow NOT READY / VERIFY EMPLOYMENT span and the `<br><br>` right
     after it. Change nothing else. Do it with the helper, not by hand: GET
     `messages/<msgId>?format=raw`, put `{"<draftId>": "<raw>"}` for every passing draft into one JSON file
     in the scratchpad, run `python .claude/skills/linkedin-final-check/strip_not_ready.py <file>`.
     It prints `==<draftId>` and the new raw for each, keeping only To/From/Subject/MIME headers. Then PUT each one.
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
