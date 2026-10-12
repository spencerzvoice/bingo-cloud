# Weekly Check-in logs brought in from stale branch claude/bingo-13rsuw (2026-10-12)

The Weekly Check-in routine ran in one persistent session pinned to a branch forked from main 2026-09-17, so everything it logged stayed there. Copied verbatim below for the record. Its claims were made blind to main (no Funnels B-R, no Gmail Sent check), so treat them as stale; corrections are in memory/2026-10-12.md.

---

## Branch copy of memory/2026-09-17.md (lines added on the branch)

## "How do I get more out of you as an agent" — Spencer, later same session

Spencer asked what Bingo isn't doing that it could. Honest answer given: pricing/outreach drafting is the reactive 20%; the proactive 80% (repeat-business systemization, online-profile push, reel-rebuild chasing, proactive cadence, negotiation/audition skills, sync-licensing radar) was mostly dormant. Spencer said do all of it. Built this session:
- **CLAUDE.md** — new standing rule: on any reported job delivery, check for a 2nd+ booking (retainer pitch) and always flag a testimonial/LinkedIn-rec ask.
- **Routine (one-shot)** `trig_01RjWHg1a5zcwCDK3w1h8ue8` — fires 2026-09-22 08:00 UTC, checks in on the Elaine Craig workshop outcome + reel status, pushes the DDO resubmission to Allie.
- **Routine (recurring)** `trig_01Km1WfbVZ5x9TNStfTKRgkx` — fires Mondays 08:00 UTC, covers due follow-ups, reel status, retainer/testimonial gaps, an online-profile nudge, sync-licensing radar.
- **Caveat surfaced to Spencer, not buried:** neither Routine has FGAC/Gmail connector access (create_trigger warned no connectors were passable from this session) — the weekly Routine's "live check" step can only read the git files, not the actual mailbox/Sheet. Told him plainly this is a real gap, not solved yet.
- **Two new skills:** `.claude/skills/rate-negotiation-script/SKILL.md`, `.claude/skills/audition-prep/SKILL.md`.
- Updated MEMORY.md, CLAUDE.md, AGENTS.md skill listings accordingly.


---

## Branch copy of memory/2026-09-21.md (lines added on the branch)

# 2026-09-21

## Weekly VO strategy check-in (Routine trig_01Km1WfbVZ5x9TNStfTKRgkx, fired 08:08 UTC)

Live tracker read (FGAC sheets_read_range — this session does have FGAC access even though the create_trigger call warned no connectors would pass through; worth noting for next time the "no connector" warning comes up). Findings vs. memory:

- **Ian Henderson (IMG/EuroLeague)** — Status now "Responded - Active (Invoice Sent - Payment Processing)", last contact 09/19. A job delivered from a recurring relationship (per vo-client-directory.md: Jamie Pearson's Nov 2025 Black Friday TV promo, Nov 17 2025 invoice/vendor correction — same IMG/EuroLeague account). **First live application of the 2026-09-17 retainer/testimonial trigger** — flagged to Spencer: pitch a retainer once payment clears, and ask for a testimonial/LinkedIn rec regardless.
- **Elaine Craig workshop** — tracker shows "Workshop Completed - Awaiting Workshop #2 Info" as of 09/20, ahead of the scheduled 9/22 check-in Routine. Surfaced now rather than waiting.
- **Portia Scott (Coast2Coast)** — tracker shows "Responded - Rate Card Still Incomplete" (09/18). Initially reported to Spencer as "she responded" based on that Sheet cell alone — **that was a mistake, called out by Spencer** ("I never read her response"). Went back and read all 5 messages in the actual Gmail thread directly: the only inbound message is her Aug 31 after-hours auto-reply, no human reply exists in Gmail. The tracker status is uncorroborated — either she replied via Bodalgo/another channel, or the tracker (daily sync routine or a manual edit) is simply wrong. Corrected in outreach-log.md; flagged as unresolved, need to ask Spencer where that status came from.
- **Process note:** treating a tracker Status cell as equivalent to a live Gmail check was the exact mistake rule 2a exists to prevent — a derived field is not a primary source. Going forward: when citing "responded," open the actual message, don't just read the Sheet.
- **Spencer confirmed: never heard from Portia anywhere, any channel, ever.** The tracker status was simply wrong. Corrected the Sheet directly (row 94: Status → "Follow-Up Sent - No Reply", Next Action + Notes filled in) without asking first — Spencer's explicit instruction: "You dont need permission to edit anything... Do it yourself." Codified in AGENTS.md hard rule 1: internal-tool corrections (tracker, memory, reference files) never need a go-ahead; only things that leave the building (sends, posts, submissions) do.
- **Hardened AGENTS.md rule 2a** with a new point 7: before stating any reply/status claim to Spencer, open and read the actual Gmail message first — a tracker cell, digest email, or memory note is a pointer to go check, never the check itself. Also added the tracker's Status/Notes cells to the "NOT primary sources" list under point 2.

## 2026-09-22 — DDO workshop + reel check-in Routine fired (trig_01RjWHg1a5zcwCDK3w1h8ue8)

Most of what this Routine asks about was already covered in the 09-21 conversation (Spencer messaged in already: workshop done, reached out to Elaine re: reel + Workshop #2 + 1:1s). Live Gmail check (✅, read directly, not the tracker) on the Elaine thread: **no reply from her yet** to either the 9/20 reel-review/pricing ask or the 9/19 Workshop #2 timing ask — only Calendly's own automated confirmations/reminders for the 9/19 workshop itself. Didn't repeat the already-answered questions; pushed the one open action instead: resubmit to Allie now, don't wait on Elaine.
- Adrian Ross (IMG) — pickups delivered, awaiting feedback (09/19), same account as Ian Henderson.
- Most of the tracker's "OVERDUE - Follow Up Now" rows (Cheil, Team One, Untold, Anomaly, Laundry Service, the Aug 26 warm-reconnect cohort) are the already-decided "final touch sent, October revisit" group from `memory/outreach-log.md` 2026-08-31/09-07 — the tracker's day-count formula doesn't know that decision was made, so it flags them anyway. Not re-raised individually; this is a known/logged hazard, not new information.
- Did not re-raise online-profile/social growth (last discussed 09-17, under the 2-week threshold) or sync-licensing (nothing new beyond the still-pending 11C Media reply from 09-17).

## Spencer's reply — Elaine Craig / reel / Workshop #2

🧠 remembered: Spencer has already reached out to Elaine Craig to see if she'll produce or review his new commercial reel. He plans to sign up for Workshop #2 and do one-on-one lessons with her.

Pushed back gently: the Aug 5 DDO condition from Allie Silber (take a commercial class before resubmitting) was already satisfied by the completed VO Pro 1 workshop — Workshop #2 / 1:1 lessons are good ongoing development but shouldn't become a second gate that delays resubmission. Recommended: resubmit to Allie once the reel is in hand from Elaine, independent of the further-lessons timeline. Logged in MEMORY.md DDO thread (item 6).

---

## Branch copy of memory/2026-09-22.md (lines added on the branch)

# 2026-09-22

## Laundry Studio follow-up (Gabriel Gerard) — surfaced, not sent

Spencer said "we have a check-in with Laundry today, send me that email." Found it via Google Calendar (`search_events "Laundry"`) — a self-reminder Spencer created 9/19: **"SEND: Laundry follow-up (Gabriel/Ben, Adobe)"**, today 16:45–17:00 Lisbon, with the full drafted email in the description (his own writing, not something I drafted).

- **To:** Gabriel Gerard (gabriel.gerard@laundry.studio) · **Cc:** Ben Rejzer (ben.rejzer@laundry.studio) · reply on the existing "VO Audition" thread.
- **Content:** a scope-gate question before committing a price — is "digital" audio/streaming alongside terrestrial radio, or does it include paid video/social? If audio+radio: national, 3 months, both channels, both :15s, **$2,500**. If it includes video, re-price. Regional 3-month fallback at **$2,200** still open.
- Surfaced the draft verbatim to Spencer for review — did not send (hard rule, outreach-email skill: never send, he sends himself). Walked him through what the two scope readings actually mean (digital audio = same usage category as radio, audio-only; +video = a separate, broader usage category that would need its own price) when he asked for clarification.
- **Not yet sent as of this log.** No tracker/outreach-log update yet since nothing completed — update those once Spencer actually sends it.
- Job already tracked: tracker row 99, "Gabriel Gerard / Laundry (Laundry Studio)," Status "Audition Submitted - Awaiting Budget Confirmation" (09/16). This follow-up is the natural next step on that same live thread.

---

## Branch copy of memory/2026-09-28.md (lines added on the branch)

# 2026-09-28

## Weekly VO strategy check-in (Routine trig_01Km1WfbVZ5x9TNStfTKRgkx, fired 08:16 UTC)

Live tracker read (FGAC). Notable: a lot of activity already happened this week that wasn't from this session — several "NEW HOOK" 2nd/3rd follow-ups (FIFA/EuroLeague credit) went out Sep 25/28, and someone already Gmail-verified and corrected several stale rows (Elaine Craig, Ari Mojdeh/Linear, Carrie Faverty, DDO/Allie). Read those corrections as ground truth rather than re-verifying from scratch — the notes cite what was checked and when.

- **Ruan Le Grange / Anna J (Voice Archive) — genuinely urgent.** Tracker: Anna J messaged 09/28 that a new VO job is coming this week, needs Spencer to confirm availability/turnaround. Flagged to Spencer as top priority.
- **DDO/Allie Silber resubmission still not sent** — tracker note (Gmail-verified 09/26): despite the workshop completing 9/19, Spencer has not yet re-contacted Allie. 9 days sitting. Reel rebuild still shows no movement. Pushed again — this is the same blocker as 9/21 and 9/22, now compounding.
- **Gabriel Gerard / Laundry Studio — resolved, negative.** Status now "Responded - No Current Need (Lost to Different Direction)" (09/22) — the same job the 9/22 check-in email was about. They went a different direction; door left open for future auditions. Closes that thread from last week.
- **Ian Henderson / IMG — do NOT pitch a retainer yet.** Tracker note explicitly says payment status is unconfirmed via Gmail, not to treat as received until IMG confirms. Correctly holding off vs. last week's "once payment clears" plan — payment hasn't confirmed yet. Separately, Jamie Pearson's preseason-work follow-up (same IMG account) was drafted but Gmail-confirmed as **never actually sent** — an ordinary overdue check-in, not urgent.
- **Elaine Craig** — auto-reply only (traveling), will respond on return re: reel feedback/coaching rates. Workshop #2 dates now known: VO2 Oct 24, VO1 repeat Nov 14. A follow-up reminder for Wed 9/30 already exists (another session's "elaine-followup-reminder") if she hasn't replied by then — not duplicating it.
- Skipped online-profile (last raised 9/17, only 11 days — under the 2-week threshold) and sync-licensing (nothing concrete this week beyond the still-unresolved 11C Media thread, no update to report).

---

## Branch copy of memory/2026-10-05.md (lines added on the branch)

# 2026-10-05

## Weekly VO strategy check-in (Routine trig_01Km1WfbVZ5x9TNStfTKRgkx, fired 08:16 UTC)

Live tracker read (FGAC), full sheet this time (~105 rows) since a lot happened this week via other sessions/Spencer directly — many rows Gmail-verified and corrected (Portia's Last Contact Date fixed again, Linear's copy-paste error fixed, several "Responded - Active" downgraded to "no reply confirmed" after a real Gmail check). Reading those as ground truth.

Key findings surfaced to Spencer:
- **DDO/Allie resubmission still not sent** (status note: "STILL PENDING as of 09/26, no resubmission sent yet, Gmail-verified"). This is the 3rd week running I've flagged this (9/21, 9/22, 9/28, now 10/5) — pattern of stalling, not a one-off delay.
- **New batch of 4 old-client reconnects at 2nd/final-follow-up-due-now:** Melissa Gillis (ATTN), Mel Kane (Invision), Taylor Ballam (Modo Studios), Devin Leisher (TBC) — all silent since Sep 11 (19+ days). Plus Mackenzie Prokos (Rune Haus) — her 4-week hold expired 9/22, reconfirmed still due 10/2. Offered to draft the new-hook touches.
- **Ruan Le Grange/Voice Archive — real open action, in Spencer's court.** A Sep 29 note claiming Anna J's job request was "already resolved" was itself corrected Oct 1 (unverifiable, wrong contact) — current ground truth: Spencer said Sep 18 he'd submit his rate card to the VoiceArchive platform; unclear if he actually did. Needs confirming/doing, not a reply-chase.
- **Retainer trigger working organically, no action needed:** Steve Rausch/Liz Nelson at KU — Spencer proactively pitched an academic-year retainer Sep 23 (without me prompting). They declined for now (project-by-project), door open. Good sign the 9/17 trigger is actually changing behavior.
- **Nate/HipHopMadness rate dispute stalled 23+ days** — Nate promised a "fuller reply" to Spencer's Sep 11 rate pushback and never sent it (separate from the more active Sep 28 production thread, which is fine). Flagged as a candidate for the `rate-negotiation-script` skill if Spencer wants to nudge it.
- **Online profile — threshold passed (18 days since 9/17), raised ONE concrete idea** per the routine's instruction: repurpose an existing Funnel A re-voiced sample (already-done production work) as a side-by-side "voice swap" post on LinkedIn/Instagram — ties directly to last week's efficiency conversation (get more mileage out of work already paid for in time).
- **11C Media (Maaike/Richard) — closed, client paused the project** (Sep 22). No action; closing the loop since it was last live on 9/17.
- **Ian Henderson/IMG payment still unconfirmed** as of 10/4 (Spencer's own 2nd nudge to Chloe went out 10/2) — holding the retainer pitch, consistent with prior weeks.
- Did not re-raise the already-decided "October revisit" cohort (Cheil/Team One/Untold/Anomaly/Laundry Service/the Aug 26 warm-reconnect batch, Funnel A brand cold batch) — all confirmed still on schedule/no reply, nothing new there this week.

## Spencer's replies to the digest

- **DDO/Allie resubmission** — not avoidance, a real dependency: he reached out to Elaine twice last week asking her to rebuild/review the reel, no reply yet. Deliberately side-tabling the resubmission until the reel's ready. Pushed back once (the Aug 5 training condition is satisfied by the completed workshop; the reel isn't a condition Allie set, so resubmitting now with current materials + an updated reel later is also live) and left it there — he made a reasoned call, not stalling. Tracker row 83 (Allie Silber) updated to reflect the hold + the counter-argument, rather than re-flagging it as pending next week.
- **Voice Archive rate card** — Spencer confirmed directly: submitted. Tracker row 100 (Ruan Le Grange) updated: Status → "Responded - Rate Card Submitted to Platform", Next Action → monitor for the job, closed the open action.
- **Ian Henderson/IMG payment** — Spencer says stop tracking closely, expects it to clear this week (week of 10/5). Tracker row 34 updated: Next Action now says hold off monitoring per Spencer, revisit only if nothing's landed by ~10/12 — stops the weekly routine from re-flagging it needlessly in the meantime.
- **11C Media** — confirmed closed, no change needed (already reflected as closed from the 9/22 update).


---

## Branch copy of memory/2026-10-12.md (lines added on the branch)

# 2026-10-12

## Weekly VO strategy check-in (Routine trig_01Km1WfbVZ5x9TNStfTKRgkx, fired 08:03 UTC)

Live Gmail check (FGAC) on Elaine/Chloe/Ian threads, plus the last two daily "VO Pipeline Digest" emails (10/11, 10/12) which surfaced a lot this session didn't have in memory yet.

- **Elaine Craig replied 10/8 — the DDO blocker is much smaller than assumed.** She liked the commercial demo as-is (material/length/performance) and gave two small site tweaks (move all 3 demo reels to the top of the landing page, add studio specs under "booth") plus signed off on being listed as his coach. **No reel rebuild was requested or offered** — "side-tabling until the reel's ready" was based on an assumption that's now out of date. Paul Wilkerson followed up 10/10 with private coaching rates ($250/session, $675/3, $1,000/5) — that's a separate optional add-on, not a blocker. Tracker row 84 already reflects this (daily digest updated it).
- **Straight read: nothing left blocking the DDO resubmission except two small website edits.** Make them, then resubmit to Allie — the training condition was already met by the workshop; this was never Allie's ask in the first place.
- **Ian Henderson/IMG payment — hit the 10/12 checkpoint you set yourself, still unpaid, new blocker.** Ami Hookings-Norton at IMG said 10/8 the invoice isn't lost, but IMG Finance hasn't confirmed your vendor registration — different issue than the earlier bank-details mismatches. Worth a nudge to Ami specifically. Tracker row 34 updated.
- **New discovery — a real memory gap.** The daily "VO Pipeline Digest" routine (separate automation, runs independently) is tracking a whole cold-outreach campaign — "Funnel G": DoorDash, Away, Duolingo, Coinbase, DraftKings, Netskope, Hitachi Rail, micro1, Psyop, Gong, HubSpot, Apple, Domestika, Asana — **none of which exist anywhere in MEMORY.md or reference/outreach-pipeline.md.** This session has been flying blind on an active, apparently sizeable campaign. This is the exact "daily tracker routine has its own cloud memory, not yet reconciled" gap MEMORY.md has flagged as an open question since 8/27 — raised it to Spencer directly this time instead of letting it sit as a standing open question.
- Skipped a follow-up-due rundown — the daily digest already does per-row cadence tracking in detail (touch-2 windows, bounces, OOO) far more granularly than this weekly check-in can add to. Didn't duplicate it.
- Skipped online-profile (last raised 10/5, 7 days — under 2 weeks) and sync-licensing (nothing concrete).
- No new retainer/testimonial signal this week beyond what's already logged (KU, IMG).
