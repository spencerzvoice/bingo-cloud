# Automation offload plan: routine stages that don't need Claude
_Mapped 2026-10-29 (Spencer: "Yes, map them")._
_**Step 1 BUILT 2026-10-29** (Spencer: "Yes, build it"): Apps Script "Bingo Digest Prep" in spencer@spencerzvoice.com, project `1g939YAXbqrscyx_zNNwOeIA9Lz6zmOxVDp9nkQVKBEwhwVJBo7--Fd5Q` (script.google.com/u/3), source `scripts/apps-script/DigestPrep.gs`. Writes tabs Prep_Meta / Prep_Rows / Prep_New / Prep_Threads in the Follow-up Queue Sheet; the Digest prompt's Step 3-PREP reads them and falls back to the old sweep unless status = OK. Test lessons: Gmail returns 204 for an empty partial response (= zero matches); 25 parallel requests tripped Gmail's per-minute quota and per-user concurrency (now 10 parallel, paced to 200 units/s); a failed metadata lookup must mark the run PARTIAL, never fall back to an older message (Tim Eger showed 08-24 instead of 09-07); retries back off past a full minute; the 21-day thread list is its own run (`runThreads`, ~05:00 UTC, tab Prep_ThreadMeta) so the row check keeps the whole time budget. Final test 10-29: rows OK 275/275, 0 failures, 204 s (internal cap 300 s, so ~25% headroom; a growing tracker will tip it to PARTIAL and the Digest falls back, at which point chunk it across runs); threads OK 197, 22 s. Spot-checked vs live Gmail: Colby Mitchell, Tim Eger, Sascha Peuckert match. Triggers installed by `setup()`. Steps 2-4 not built._

## The finding that changes the host
- Every repo script (`ledger_coverage.py`, `digest_gmail_check.py`, `draft_format_sweep.py`, `latest_video_check.py`, `digest_render.py`/`digest_upload.py`) calls Google through the **FGAC proxy** with a temporary key (✅ read in the scripts 10-29).
- An FGAC key can only be minted from a Claude session (`create_temporary_api_key`), and it lasts **at most 60 min** (✅ the tool's own description, 10-29). So **GitHub Actions can't run these headless**. It would need a Google OAuth refresh token stored in GitHub, which skips FGAC's access rules and every `.claude/hooks/*` guard. Not recommended.
- **Host = Apps Script in spencer@spencerzvoice.com.** It has native Gmail/Drive/Sheets access, free time triggers and no keys, and the "Bingo Follow-up Sender" already runs that way. API calls (BrightData/ZenRows) go through `UrlFetchApp`, with the keys in Script Properties.
- Hooks don't run inside Apps Script, so each ported job must enforce its own guard: never send; edit only the exact text the job owns; read back after every PUT; re-apply labels.

## Stage map
| Routine / stage | Pure script? | Move to Apps Script | Claude keeps |
|---|---|---|---|
| **Digest Steps 1-3e** (find the tracker, read it, check Gmail both ways for every active row: inbound/outbound/bounce/OOO/drafts/new contacts, coverage count) | Yes | All of it. One "Digest Prep" run ~06:45 UTC writes a compact JSON to a Drive file | Reading that one file instead of ~190 rows of tool calls across 3 subagents (Step 3a "HOW", proven 187/187 rows in ~4 min on 10-12) |
| Digest Step 0a + Prep step (0) **ledger coverage scan** (runs twice a day now) | Yes, except reading `followups-queue.md` from the repo | Sent+Scheduled 21-day thread list into the same JSON; the reconcile vs the ledger stays a quick Claude step (or the ledger moves to a Sheet tab later) | Reconcile + EXEMPT judgment |
| Digest Step 4 **Last Contact Date** + Step 4b **J/K formula guard** | Yes | Both (copyPaste J2:K2 down, read-back check) | Status / Notes / Next Action wording |
| Digest Steps 0, 0b, 3f, 5, 6 (due-today triage, site visitors via Apollo MCP, the digest itself, the push) | No | none | All |
| **Morning Build 13:05 run** = Stage 3 + Stage 4 only | Almost all | Whole run. **Retire the 13:05 cloud run** | MISMATCH calls, WebSearch URL fallback (goes to the desktop list) |
| Stage 3 **LinkedIn API check** (`cloud_check.py` + `strip_not_ready.py`) | Yes | Port both: URL from the repo logs → API → PASS strips the yellow line; MISMATCH/HIDDEN only reported | Possible-LEFT decisions; desktop 5b for HIDDEN |
| Stage 4 **follow-up queue check** (drafts D, due N, queued Q, sent S, missing M, heartbeat `Log!F1`) | Yes | Folds into the Follow-up Sender itself | Queueing a MISSING contact (NO-CONTACT CHECK + tz judgment) |
| Stage 2 **Video Title Sync** (WINNER from `_candidates` → replace `VIDEO TITLE PENDING` / fix title text) | Yes | Port. Touches only the marker/title text; NEEDS HAND FIX → report | Noun edge cases, NO GOOD MATCH variant |
| Stage 0 Lead Batch, Stage 1 Hook Sweep | No | none | All (Opus work) |
| Re-Voicing | Partly (downloads/demucs are scripts, picks are judgment) | Not Apps Script. Later: local GPU + Windows Task Scheduler for `revoice_build.py --all` | Video picks, script checks |
| Weekly Check-in | No | none | All |
| Follow-up Prep | 🟡 only skimmed (10-29) | Its step (0) scan shares the Digest Prep JSON | Queue decisions |

## Build order (biggest saving first)
1. **Digest Prep** (Steps 1-3e + 4 dates + 4b + the coverage thread list). This takes out the daily ~190-row, 3-subagent Gmail sweep.
2. **LinkedIn API check + queue check** in Apps Script, then disable the Morning Build 13:05 trigger (one fewer cloud run a day).
3. **Video Title Sync**.
4. Rewrite each routine prompt to "read the Apps Script output file; if it's missing or older than 2 h, fall back to the old step", so nothing breaks if a script fails.

## Unknowns
- ❓ How much usage each step costs today. Measure one Digest run with `/explain-usage` (or `get_usage` before/after) before and after step 1; no estimate without it.
- ❓ Apps Script quotas for Gmail reads at ~190 rows/day (well under consumer limits on paper; check on the first run).
- ❓ Whether BrightData/ZenRows accept calls from Google's IP ranges the same way.
