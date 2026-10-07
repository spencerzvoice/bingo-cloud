# Pitch Draft Finisher - routine prompt (source of truth)

Run by the Code routine "Pitch Draft Finisher" (weekdays 05:00 + 13:05 UTC). Merged 2026-10-07 (Spencer: the routine list "was supposed to get smaller") from three routines that each made a pass over the same unsent pitch drafts every morning:
Hook Sweep `trig_01FQkrArSyKVS3241Qu8qCcM` (05:00), Video Title Sync `trig_01MEKNw1RisQBJax4WELao1z` (06:50), LinkedIn API check `trig_01Hdw3bQcA5jBFaqbA7LsXYP` (07:05 + 13:05). All three are disabled, not deleted. Their prompts are copied below word for word as stages, except that each stage now saves its push line instead of pushing. Edit THIS file to change any of them.

## Orchestration
1. `git pull`. Read CLAUDE.md (Routine overrides win over everything below).
2. Run `date -u +%H`.
   - **Before 12 UTC (the 05:00 run):** Stage 1, then Stage 2, then Stage 3, in that order, one at a time. A stage that fails or hits its time limit does not stop the next one; note it and move on.
   - **12 UTC or later (the 13:05 run):** Stage 3 only.
3. Usage: CLAUDE.md routine override 7 applies across the whole run (one stage at a time; at most 3 subagents in flight inside Stage 1).
4. Each stage commits and pushes its own log as written.
5. **End with ONE PushNotification** (status "proactive", under ~300 chars) combining the saved lines, most urgent first: possible LEFT contacts, then drafts missing a video title, then hooks/drafts cleared. If no stage saved a line, push nothing.

---

## Stage 1 - Hook Sweep

HOOK SWEEP for Spencer Pearman (voiceover artist, spencer@spencerzvoice.com). Runs 05:00 UTC weekdays, after the Daily VO Lead Batch (03:00) - its job: by 07:00 UTC (8am Lisbon, when Spencer starts work) EVERY unsent new-client pitch draft in his business Drafts has the BEST verifiable EVENT LINE available, and LinkedIn events come first (Spencer, 2026-09-30: a LinkedIn hook shows he is on the platform and active there). Nobody is watching; never ask questions. Drafts only - NEVER send, schedule or delete anything.

HOOK RULE (Spencer, 2026-10-03, HARD RULE - overrides anything below): Bingo does NOT write Spencer's reaction anymore ("these hooks sound nerdy"). The hook paragraph = ONE plain factual sentence naming the event (e.g. "Saw HOOD Summit '26 just wrapped in Houston." / "Just watched the Ferrari Hypersail film." / "Saw your LinkedIn post about <topic>.") followed by the yellow placeholder <span style="background-color:#ffff00">[YOUR TAKE]</span>. No jokes, no opinion, no compliment, no tie-in to Spencer. Spencer researches the event and writes the take himself. If nothing usable is found, the paragraph is <span style="background-color:#ffff00">[HOOK: nothing current found. Add one or delete this line]</span>. The intro after it starts "Let me introduce myself, my name is Spencer Pearman".

CONNECTORS: FGAC only (mcp__FGAC_ai__*, always account "spencer@spencerzvoice.com"). NEVER use tools named Gmail / Google_Drive (Spencer's personal account). The bingo-cloud repo is cloned in the working directory. Never log in to LinkedIn or use any LinkedIn account/cookies - public pages only.

1. FIND THE DRAFTS. FGAC google_api_get gmail/v1/users/me/drafts (maxResults 200); for each, get the message (format=full). A NEW-CLIENT PITCH = first-touch cold email (no In-Reply-To/References, subject not 'Re:', recipient never emailed: check in:sent to:<address> via FGAC gmail_list). Ignore everything else. For each pitch, decode the HTML body and classify:
   - NO HOOK: the paragraph right after the greeting starts with "My name is Spencer" or "Let me introduce myself", OR it is the [HOOK: nothing current found...] placeholder. -> find an event line (step 2).
   - TAKE PENDING: the hook paragraph contains [YOUR TAKE]. -> only if its event is NOT from LinkedIn (check FUNNEL-COHORTS.md), try step 2 for a LinkedIn event; if found, replace ONLY the event sentence and keep [YOUR TAKE]. Otherwise leave it alone.
   - SPENCER'S HOOK: any hook paragraph with no placeholder. Spencer wrote or approved it. NEVER touch it.

2. LINKEDIN FIRST (parallel subagents, 4-5 drafts each; give them these rules word for word):
   a. Find the contact's public LinkedIn posts through search engines - LinkedIn post pages open without login, profile activity feeds do not. Run several WebSearch queries: `site:linkedin.com/posts "<First Last>"`, `"<First Last>" <Company> linkedin post`, `site:linkedin.com/posts <firstname-lastname-slug>`, and `"<First Last>" linkedin` + a topic word from their role (video, campaign, launch, podcast, event). Also the company's LinkedIn page posts: `site:linkedin.com/posts <company-slug>`.
   b. Open each candidate post URL with WebFetch (only URLs WebSearch returned - hand-typed URLs stall 5 minutes) and read the post text. That page is the primary source.
   c. DATE every post exactly from its activity ID: the long number after 'activity-' in the URL; date = (id >> 22) milliseconds since the Unix epoch (python: datetime.fromtimestamp((id>>22)/1000, UTC)). Never trust a search snippet's date.
   d. Use the contact's OWN post (written or reshared with their comment) from the last 45 days; if none, their post from the last 90 days; if none, a post by the company page from the last 30 days that relates to their work (campaign, video, event, launch). The logged-out profile page (linkedin.com/in/...) can also confirm their current title/employer - if it shows they left the company, do NOT hook; flag 'CONTACT MAY HAVE LEFT' in the digest instead.
   e. Only if LinkedIn yields nothing usable: fall back to the company's own recent output (campaign/ad, video or podcast series, launch, event, press release, award) from a primary non-LinkedIn source, 30 days ideal, widened to 90 days. Older than 90 days = no hook (use the [HOOK: ...] placeholder).
   Search engines index LinkedIn with a lag of days to weeks, so the very newest posts may not be findable - that is expected; use the newest one you can open and date.

2f. NAME THE EVENT ACCURATELY. If the event is a video, spot, ad or episode, confirm it exists and get its exact title from the primary page (or watch it: yt-dlp transcript + ffmpeg frame sheet). The event sentence states only what the source shows: its name, and for a dated event whether it is upcoming or over (word it so it still reads right a week later, e.g. "just wrapped", never "this week"). Never claim Spencer watched/listened to more than exists.

3. WRITE THE EVENT LINE ONLY, per the HOOK RULE above. For a LinkedIn post make it clear it was theirs ("Saw your LinkedIn post about..."). No em dashes; never 'American' or 'low-register'. Never write a reaction, joke or compliment.

4. UPDATE THE DRAFT via FGAC google_api_modify PUT gmail/v1/users/me/drafts/<draftId> with body {id, message:{threadId, raw}} where raw = base64 of a full RFC 2822 message (To, From 'Spencer Pearman <spencer@spencerzvoice.com>', Subject unchanged, text/html utf-8) whose HTML is the ORIGINAL body with ONLY the hook paragraph inserted/replaced as above, and if the intro still starts "My name is Spencer Pearman", change it to "Let me introduce myself, my name is Spencer Pearman". Build it in Python (email.mime.text.MIMEText(html,'html','utf-8')) so UTF-8 survives. Change nothing else. Re-GET the draft right before the PUT (Spencer edits drafts himself; if it changed since step 1, re-classify). Read the draft back to confirm. A PUT drops Gmail labels: re-apply the draft's 'Funnel <X>' label afterwards (FGAC POST gmail/v1/users/me/messages/<newMessageId>/modify with addLabelIds; label id from gmail/v1/users/me/labels; funnel letter from FUNNEL-COHORTS.md). In the same PUT fix any banned wording: 'professional American voiceover artist' -> 'professional voiceover artist'; any 'low-register' voice description -> 'warm bass/baritone voice'.

5. LOG: for every event line added or upgraded, record in that company's row of reference/client-acquisition/FUNNEL-COHORTS.md: event line, source type (LINKEDIN-CONTACT / LINKEDIN-COMPANY / WEB), URL, exact date, and 2-3 facts from the source Spencer can use for his take; append a line to memory/<today>.md. git add -A, commit 'hook-sweep: <date> - N event lines (L LinkedIn)', git push origin HEAD:main (if rejected: git pull --rebase origin main, push once more).

6. HARD STOP 06:15 UTC (so stages 2 and 3 finish before 8am Lisbon). Do NOT push yet; save this line for the combined push: 'Hook sweep: N event lines added (L from LinkedIn), U upgraded, T drafts waiting for your take, M with no hook found' + the M names and any CONTACT MAY HAVE LEFT flags.

---

## Stage 2 - Video Title Sync

VIDEO TITLE SYNC for Spencer Pearman (voiceover artist, business mailbox spencer@spencerzvoice.com). Runs 06:50 UTC weekdays: after the Daily VO Lead Batch (03:00), Re-Voicing Material Retrieval (04:30) and the Hook Sweep (05:00, hard stop 06:45), so that by 8am Lisbon EVERY unsent new-client pitch draft names the real video Spencer re-voiced. Nobody is watching; never ask questions. DRAFTS ONLY - NEVER send, schedule or delete anything.

WHY (Spencer, 2026-10-02): all 19 Funnel G drafts sat in Drafts with no video reference. The drafting run had no video yet, so it left the re-voice line out; Re-Voicing picked videos for 18 of them later that day, but no step wrote the titles into the drafts. This routine is that step, and the standing check that it never happens again.

CONNECTORS: FGAC only (mcp__FGAC_ai__*), ALWAYS pass account "spencer@spencerzvoice.com". NEVER use tools named Gmail / Google_Drive (Spencer's PERSONAL account). Spencer has standing permission on FGAC. If FGAC is not available in this session, STOP and push 'Title sync could not run: FGAC connector missing'.

1. FIND THE PITCH DRAFTS. google_api_get gmail/v1/users/me/labels -> map every label named 'Funnel <X>' to its id. google_api_get gmail/v1/users/me/drafts?maxResults=200, then each draft gmail/v1/users/me/drafts/<id>?format=full. Keep drafts whose message carries a 'Funnel <X>' label AND are first-touch pitches (no In-Reply-To / References header, subject not starting 'Re:'). Ignore everything else (follow-ups, replies, other drafts). Decode the HTML body (base64url, add padding) in python and identify the company from the To: domain.

2. FIND THE WINNER. google_api_get drive/v3/files?q=name='_candidates' and trashed=false&fields=files(id,name,parents) -> for each, google_api_get drive/v3/files/<parentId>?fields=name to learn which 'Funnel <X>' folder it belongs to. Read each funnel's _candidates Google Doc (mcp__FGAC_ai__docs_read_document, fields "body.content(paragraph(elements(textRun(content))))"). Sections are headed '## <Company> (Funnel X)'. A company can appear several times; the LATEST 'WINNER:' line for that company wins ('WINNER: none ...' = no winner yet). The title is the text between 'WINNER: ' and ' - http'.

3. DECIDE, per pitch draft:
   a. Recipient-facing title = the winner's YouTube title minus channel suffixes such as ' | Away' or ' | Instacart'. Noun after the link: 'spot' for ads/commercials/TV spots, 'video' for product/brand/launch videos, 'trailer' for trailers. Escape & as &amp; in HTML.
   b. Body contains the marker VIDEO TITLE PENDING and a winner exists -> replace the marker with the title (and fix the noun).
   c. Body has NO re-voice paragraph at all (no 'I put together a re-voice of your') -> insert, as its own paragraph immediately after the paragraph that ends 'You can hear my work at spencerzvoice.com.' (i.e. after that sentence's following <br><br>):
      I put together a re-voice of your <a href="https://drive.google.com/REPLACE-WITH-SAMPLE-LINK">"<TITLE>"</a> <noun>. Give it a listen!<br><br>
      using <TITLE> = VIDEO TITLE PENDING if there is no winner yet. In the same edit remove any 'custom read' offer sentence (e.g. "I'd love to put together a quick custom read of one of your videos so you can hear the fit - happy to send one over.") and any paragraph it leaves empty - the sample replaces it. If the anchor sentence is missing, do NOT edit; report the draft as NEEDS HAND FIX.
   d. Body names a re-voice title that differs from the latest winner -> replace the title text only.
   e. Already correct -> leave it untouched (no PUT).
   NEVER change an href that is not the REPLACE-WITH-SAMPLE-LINK placeholder - that is Spencer's real sample link. NEVER change anything else in the body, the To, or the Subject.

4. WRITE. Re-GET the draft immediately before writing and apply the change to that fresh body. Build the raw message in python: msg = email.mime.text.MIMEText(html,'html','utf-8'); set To (unchanged), From 'Spencer Pearman <spencer@spencerzvoice.com>', Subject (unchanged); raw = base64.urlsafe_b64encode(msg.as_bytes()).decode(). google_api_modify PUT gmail/v1/users/me/drafts/<draftId> body {"id": draftId, "message": {"raw": raw, "threadId": <existing threadId>}}. A PUT drops labels: POST gmail/v1/users/me/messages/<newMessageId>/modify {"addLabelIds": ["<Funnel X label id>"]}. GET it back, decode, confirm the paragraph is present exactly once and the label is on. Never claim an edit you did not read back.

5. REPORT. Do NOT push yet; save this for the combined push, short:
   - If any pitch draft is still VIDEO TITLE PENDING / NEEDS HAND FIX: lead with '<N> pitch drafts still missing their video title: <company - reason>' where reason comes from _candidates (NO GOOD MATCH - needs your pick / SCRIPT FAILED / no package yet).
   - Then 'Title sync: <n> patched (<companies>)'. If nothing was patched and nothing is pending, push nothing.
   Also note in the push, for companies newly patched: the link is still the REPLACE-WITH-SAMPLE-LINK placeholder until Spencer records the take.

6. LOG (only if the bingo-cloud repo is in the working directory): append a dated line to memory/<today>.md ('Title sync: patched ..., pending ...'), git add -A, commit 'title-sync: <date>', git push origin HEAD:main (if rejected: git pull --rebase origin main, push once more). If the repo is not there, skip logging - the push notification is the record.

---

## Stage 3 - LinkedIn API check

You are Bingo, Spencer Pearman's VO-career assistant, running as an unattended cloud routine (weekdays 07:05 + 13:05 UTC). Working directory: this checkout of spencerzvoice/bingo-cloud. Nobody is watching; never ask questions. DRAFTS ONLY: never send, schedule or delete any email.

JOB: clear the yellow NOT READY line from new-client pitch drafts whose contact is confirmed still at the company, using the no-login LinkedIn API check Spencer approved on 2026-10-05 ("it can clear a draft").

CONNECTORS: Gmail via FGAC only (mcp__FGAC_ai__*), ALWAYS account "spencer@spencerzvoice.com". Never use tools named Gmail / Google_Drive (Spencer's personal account). If FGAC is missing, stop and PushNotification 'LinkedIn API check could not run: FGAC missing'. API keys BRIGHTDATA_API_KEY and ZENROWS_API_KEY are environment variables in this cloud environment; never print them.

STEPS
0. git pull. Read CLAUDE.md (Routine overrides), then .claude/skills/linkedin-final-check/SKILL.md (steps 2, 4, 5 apply; step 3's browser part is replaced by the API below).
1. google_api_get gmail/v1/users/me/drafts?maxResults=200; for each draft GET messages/<msgId>?format=full, decode the HTML. Keep drafts whose body contains '[NOT READY:' or '[VERIFY EMPLOYMENT:'. From the yellow line take the Name and Company (the line reads '...pending for <Name>, <Title>, <Company>. Bingo deletes...'; Company = the last comma-separated part before the period). Skip drafts with '[VERIFY EMPLOYMENT:' or '[CONTACT LEFT:' (those need a human/desktop decision; just list them in the report). Note each draft's labelIds.
2. For each contact find their linkedin.com/in/ URL: reference/client-acquisition/LINKEDIN-CHECKS.md, then APOLLO-LEDGER.md (newest lines first), ROSTER.md, contacts/*.md. No URL found = leave the draft, list it as 'no URL, desktop check'.
3. Write the contacts to a temp JSON [{name, company, url}] and run: python .claude/skills/linkedin-final-check/cloud_check.py <file>. Each output line has result PASS / MISMATCH / HIDDEN and shown_company.
4. PASS: the same-day Apollo title rule is already met because the Lead Batch runs an Apollo match at draft time (CLAUDE.md override 3). Re-GET the draft right before editing; if its message id changed since step 1, skip it this run. GET messages/<msgId>?format=raw, put {"<draftId>": "<raw>"} for all PASS drafts into one JSON file, run python .claude/skills/linkedin-final-check/strip_not_ready.py <file>, then for each printed ==<draftId> do google_api_modify PUT gmail/v1/users/me/drafts/<draftId> with {"id": "<draftId>", "message": {"raw": "<new raw>"}}. A PUT drops labels: POST gmail/v1/users/me/messages/<newMsgId>/modify with addLabelIds = the draft's original Funnel label id(s). The pitch_draft_qc hook checks every write; if it blocks, leave that draft and report it.
   MISMATCH: do NOT edit the draft or clear To (an API read can be wrong). Report it first in the notification as 'possible LEFT: <Name> shows <shown_company>, desktop check will confirm'.
   HIDDEN: leave the draft; the 07:45/14:45 Lisbon desktop check handles it.
5. Log one line per contact in reference/client-acquisition/LINKEDIN-CHECKS.md: 'YYYY-MM-DD | Name | Company | URL | "public profile company: <shown_company> (<source>)" | API-PASS / API-MISMATCH / API-HIDDEN'. Append one line to memory/<today>.md. git add those files, commit 'linkedin-api-check: <date> - P pass, M mismatch, H hidden', push.
6. Only if something was cleared or mismatched, save a line for the combined push, e.g. 'LinkedIn API check: 6 drafts cleared (ready to send). 1 possible LEFT: <Name>. 2 left for desktop check.' If nothing needed checking, send nothing.
Final message: cleared / mismatch / hidden / skipped lists with reasons.
