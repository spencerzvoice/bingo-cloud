# Digest routine patch - 2026-10-07 (NOT YET APPLIED)

Routine: **VO Outreach Pipeline Daily Update - 8am** `trig_01PTnXAXdmvLjyqBCnsgPXVz` (Cowork-scheduled, 07:00 UTC daily, no repo access, so it can't read `memory/followups-queue.md`).

Why: the 2026-10-07 digest listed 9 "follow-ups due today". None were due (verified in live Gmail + ledger, see `memory/2026-10-07.md`). Bingo's API edit of the routine was blocked by the desktop permission classifier, so this block still has to go in.

**How to apply:** open the routine at claude.ai/code/routines, paste the block below on its own lines directly ABOVE the line that starts `Step 1 - Find the correct file`, save. (Or allow `RemoteTrigger` updates for Bingo and say "apply the digest patch".)

```
NEXT-TOUCH DATES + NO SELF-REFERENCE (Bingo, 2026-10-07, after the Oct 7 digest listed 9 "due today" rows when none were due):
- Bingo writes the real follow-up schedule into Next Action as "Next touch: <Day YYYY-MM-DD>", "NOT DUE - ..." or "NOT ON THE CLOCK - ...". These come from Bingo's follow-up ledger and are AUTHORITATIVE. Never list a row as due before its "Next touch" date, and never list a "NOT DUE" or "NOT ON THE CLOCK" row. Never overwrite or remove those Next Action entries; add a dated note in Notes instead.
- Never write "due now", "DUE NOW", "OVERDUE" or "due" into Next Action or Notes. Due-ness is decided fresh every run from Gmail + the cadence; a phrase an earlier run wrote is NOT evidence that anything is due. (Root cause of the Oct 7 error: a Sep 27 run wrote "2nd/final follow-up (NEW HOOK) due now" on warm reconnect rows at 19 days, and later runs trusted their own note.) If a row needs a touch, write "Next touch: <date>" computed from the cadence.
- Days since last contact = today minus THAT row's Last Contact Date, computed per row. Never reuse one number for several rows (the Oct 7 digest printed "26 days" for 9 rows whose real gaps were 21 to 64 days).
- Warm pure check-in window = 28 days minimum. A warm/reconnect row at 26 days is NOT due.
- A row whose Status contains "Responded", where Spencer answered the contact's last reply, is not due unless Next Action gives a Next touch date that has arrived.
- Columns J and K are formulas. If a row's J/K is blank or a typed number, do not type values in; list it once under HEADS UP as "formula missing in row N".
```

The full patched prompt was built from the live prompt on 2026-10-07 (14,520 chars); only this block is new.
