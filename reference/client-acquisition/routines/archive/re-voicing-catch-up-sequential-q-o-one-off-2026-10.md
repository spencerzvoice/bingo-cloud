# Re-Voicing catch-up, sequential Q-O (one-off 2026-10-06)

Archived 2026-10-07 before deletion. id `trig_01WGyZ74sB6y58KCLDcfhvLt`, cron `0 3 1 1 *`, env `env_01VPYwj9nwzjzGqdxm4fRQFY`, connectors: FGAC_ai, vidIQ, Carly.

## Prompt (verbatim)

SEQUENTIAL RE-VOICING CATCH-UP RUN (set up by Bingo on desktop, 2026-10-06, at Spencer's request). Earlier today 7 parallel runs used up Spencer's whole usage limit and died mid-build, so this run goes ONE FUNNEL AT A TIME and is THROTTLED.

FIRST: `git pull`, then read `reference/client-acquisition/routines/REVOICE-ROUTINE-PROMPT.md`. That is the full Re-Voicing Material Retrieval routine. Follow it exactly (Stage 1 pick, Stage 2 build + upload, every gate incl. AGE GATE, narrator_check, script gate, LINK CHECK OK), together with CLAUDE.md, with ONLY these overrides:

1. ORDER: Funnel Q, then P, then K, then J, then L, then N, then M, then R, then O (Drive `Client Outreach/Funnel <X>/`). Finish every client in one funnel (LINK CHECK OK or a logged reason it failed) before starting the next funnel. Never touch Funnel G2, H or I.
2. RESUME, DON'T REBUILD: many clients are half-built from this morning's runs. Before working a client, list its Drive folder (rclone lsf -R / Carly). If source mp4 + NOVOX + script doc + sources doc + `<Client> Project/<Client> Project.als` + `Ready to Link to Drafted Email/MAKE VIDEO - double-click me.bat` all exist, run `cloud_ableton.py --verify-remote` on it; LINK CHECK OK = done, skip it. Otherwise fill ONLY the missing pieces (a client with source + NOVOX but no Ableton project just needs the script/sources docs checked and the Ableton step). Never re-pick a video that already has a SOURCE file in the folder.
3. THROTTLE (Spencer, 2026-10-06: milk the usage, don't zoom past the limit): at most 3 clients in flight at once (subagents or background jobs combined), at most 2 demucs/whisper jobs at the same time, and space out YouTube requests (sleep 5-10 s between yt-dlp calls; on HTTP 429 back off 60 s and move to another client, don't hammer). Prefer captions over Whisper.
4. USAGE LIMIT: if any tool or reply returns "You've hit your session limit" or a rate_limit rejection, STOP starting new work immediately. Commit + push what's done, send ONE PushNotification to Spencer with: funnels/clients finished, the client you stopped on, and the reset time. Do not retry in a loop.
5. No start cutoff time; keep going funnel by funnel until O is done or rule 4 stops you.
6. Skip priority (1) (unsent drafts without a package); the daily routine owns that. Skip any client already SENT (routine step 0b).
7. Sandbox: every client gets its own dir /tmp/revoice/<Client>/ with a client-unique Demucs input filename and output dir.
8. Repo: other sessions push in parallel. `git pull --rebase` right before every push; on conflict keep both sides' rows.
9. Log every pick in VIDEO-PICKS.md. When each funnel finishes, push a one-line PushNotification ("Funnel Q done: 7 LINK CHECK OK, 2 NO GOOD MATCH (names)"). Final report: one line per client.

