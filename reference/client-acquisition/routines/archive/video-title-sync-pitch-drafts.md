# Video Title Sync - pitch drafts

Archived 2026-10-07 before deletion. id `trig_01MEKNw1RisQBJax4WELao1z`, cron `50 6 * * 1-5`, env `env_01VPYwj9nwzjzGqdxm4fRQFY`, connectors: FGAC-ai, Carly.

## Prompt (verbatim)

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

5. REPORT. PushNotification (status "proactive"), short:
   - If any pitch draft is still VIDEO TITLE PENDING / NEEDS HAND FIX: lead with '<N> pitch drafts still missing their video title: <company - reason>' where reason comes from _candidates (NO GOOD MATCH - needs your pick / SCRIPT FAILED / no package yet).
   - Then 'Title sync: <n> patched (<companies>)'. If nothing was patched and nothing is pending, push nothing.
   Also note in the push, for companies newly patched: the link is still the REPLACE-WITH-SAMPLE-LINK placeholder until Spencer records the take.

6. LOG (only if the bingo-cloud repo is in the working directory): append a dated line to memory/<today>.md ('Title sync: patched ..., pending ...'), git add -A, commit 'title-sync: <date>', git push origin HEAD:main (if rejected: git pull --rebase origin main, push once more). If the repo is not there, skip logging - the push notification is the record.
