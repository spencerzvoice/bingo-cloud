# Client Acquisition — sync docs to Drive

Archived 2026-10-07 before deletion. id `trig_01MMMGbkh8CaD3XUWJbycdn9`, cron `45 7 * * *`, env `env_011111111111111111111117`, connectors: Canva, Claude_Docs, Portio_Apps_Script_MCP, Figma, Google_Calendar, Wispr_Flow, FGAC_ai, Claude_Code_Remote, Carly, vidIQ.

## Prompt (verbatim)

Mirror Spencer Pearman's "Client Aquisition" claude.ai Project docs into his BUSINESS Google Drive as Google Docs, so his local agent (Bingo) can pull them. Cloud-only, right after the Daily VO Lead Batch. Never requires his computer.

ACCOUNT SAFETY — read before anything else. `spencerzpearman@gmail.com` is PERSONAL. `spencer@spencerzvoice.com` is the BUSINESS account and the only correct destination.
- NEVER use the built-in `Google_Drive` connector (`mcp__Google_Drive__*`). It is attached to this task but is signed in to the PERSONAL account. Do not use it at all.
- ALWAYS use FGAC (`mcp__FGAC_ai__*`) — `google_api_get` for reads, `google_api_modify` for writes.
- FIRST call `mcp__FGAC_ai__list_accounts`, confirm `spencer@spencerzvoice.com`, and pass `account: "spencer@spencerzvoice.com"` on EVERY call after that.
- If that account is missing or a call fails, STOP: write nothing, report in one line. Never fall back to the other connector.

TARGET FOLDER: `1_UO7j8qWKHEZA8re81eOvFN4MVpIscyq` ("Client Acquisition Docs", business My Drive root). It already holds all 24 Docs as of 2026-09-28.

WHY GOOGLE DOCS, NOT .md: FGAC serializes any string body as JSON, so a raw `uploadType=media` upload lands as one quoted, escaped JSON string. Tested and confirmed 2026-09-28. Creating Google Docs is the clean path. Do not attempt a media upload and do not switch connectors.

STEPS — follow the order exactly; steps 2 and 3 exist because a run on 2026-09-28 created 15 duplicate Docs by skipping them.

1. `project_info` for the doc list. If no Projects tool is available, STOP and report that in one line.
2. List the folder ONCE, at the start: `drive/v3/files?q='<folderId>' in parents and trashed=false&fields=files(id,name,modifiedTime)&pageSize=100`. Build a name→id map from that single listing and use it for the whole run. Do not re-list mid-run.
3. DEDUPE FIRST. If any name appears more than once in that listing, keep the one with the newest modifiedTime and trash the rest (`PATCH drive/v3/files/<id>` with `{"trashed": true}`) before writing anything. Report how many you trashed.
4. Each Project doc maps to a Doc titled with its basename including `.md` — `claude/ROSTER.md` → `ROSTER.md`. Strip only the `claude/` and `contacts/` prefixes.
5. SKIP any doc whose Doc in the map has a modifiedTime LATER than that doc's `created_at` — it is current. Say how many you skipped. On a normal day this is 21 or more of the 24; only the files the lead batch just rewrote should need work.
6. For each doc that is NOT skipped:
   - Name already in the map → reuse that id. NEVER create a second Doc with a name that is already in the map, whatever else seems wrong.
   - Name not in the map → create it in one call: `POST drive/v3/files` with `{"name":"<NAME>","mimeType":"application/vnd.google-apps.document","parents":["<folderId>"]}`. Add the new name and id to your map immediately.
   - If reusing an existing Doc, first `google_api_get v1/documents/<docId>`, find the body's end index, and `batchUpdate` a deleteContentRange from index 1 to endIndex-1 so no old text survives.
   - Then `POST v1/documents/<docId>:batchUpdate` with `{"requests":[{"insertText":{"location":{"index":1},"text":"<the doc's full markdown, verbatim>"}}]}`. Verbatim — same headings, tables and pipes, no reformatting, no summarizing, no Docs styling.
   - If a batchUpdate is rejected for size (ROSTER.md is ~44k characters), split into sequential insertText requests at increasing indexes. Never leave a doc partially written.
7. BUDGET: if you have worked through 10 docs, stop there and report which ones you did not reach. A later run picks them up via the skip rule. Do not race to finish.
8. Never delete anything except duplicates under step 3.

OUTPUT: one line — written, skipped, duplicates trashed, and any docs not reached. Two-line session summary. Do not ask questions; Spencer will not be watching.

BACKGROUND: this sync used to push to spencerzvoice/bingo-cloud. Abandoned 2026-09-28 — a scheduled Cowork run has no authorized repository, and a Claude Code routine, which can push, has no Projects tool. Do not revive it.
