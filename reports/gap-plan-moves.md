# Gap plan moves (Search Visibility Report)

The report's "Go ahead" buttons write `goahead/<move>` rows to the artifact database (slug `a17732d1-2436-427e-bf44-545afa53a917`, https://claude.ai/artifact/LwRzPzVr19dC1fKuL7aSKQ). The desktop scheduled task "Bingo go-ahead pickup" reads rows with `status: "requested"` and runs the move below. Source page: `reports/visibility-report.html`. Created 2026-11-08 (Spencer: "Have the site be interactive where I can click a link that says 'Waiting on your go-ahead' and we start that task").

Row statuses: `requested` (button clicked) → `started` (pickup set it, with a short `note`) → `done` (note = one-line result) or `blocked` (note = what Spencer must do).

Hard limits for every move (CLAUDE.md, AGENTS.md hard rule 1): nothing sent, submitted, posted, applied to, purchased or signed without Spencer's explicit OK in chat. A move that reaches that point builds the drafts/submissions, sets `blocked` with a note like "5 submissions drafted, waiting on your OK", and stops. Free listings only; paid ones go to Spencer as a yes/no with the price.

## A. European agency rosters + UK voice directories
Targets: The Voice Realm, Voice Squad, QVoice, Voice Fox, Great British Voices, The Voiceover Gallery, London Voiceover, Nordling's Talent, Damn Good Voices, Soho Voices, Speaker-Search, Voicfy, Native Voiceover, Voquent (already a profile: check it).
Do: for each, open the live site and record (✅ with URL) whether it is a free listing, a paid listing (price) or an agency taking submissions, and what it asks for (demo format, rate card, bio). Write the result to `reference/client-acquisition/EU-ROSTERS.md`. Draft each free submission/application (bio, demo links from spencerzvoice.com) in that file. Then `blocked`: "N free / N paid / N agencies researched, submissions drafted, waiting on your OK".

## B. Third-party proof
Do: (1) build review-ask EMAIL DRAFTS (Gmail drafts via FGAC, never sent, HTML via scripts/gmail_compose.py) to 3-5 past direct clients from `reference/vo-client-directory.md` who were happy, asking for a Google Business Profile review (link https://g.page/r/CaLN8IP90nZ7EBM/review); (2) look up One Voice Awards 2027 entry dates, categories and fees on the official site (✅ source). Then `blocked`: "N review drafts in Gmail + One Voice Awards: <dates, fee>, your call".

## C. Earned links
Do: (1) Qwoted: list open requests that fit (VO, audio, remote work, expat, travel-work), draft 2-3 pitches on the working-traveller story (MEMORY.md "Media/PR angle"; ask before printing dates/amounts); (2) list 5 podcasts that take guests in VO/audio/remote-work/expat with their guest-application route; (3) draft credit-link asks to Noah Media and clients with portfolio/credits pages (Gmail drafts). Then `blocked`: "N pitches + N drafts ready, waiting on your OK".

## D. Site fixes (push live, per MEMORY.md site rule)
Do: (1) Search Console (OpenSEO `get_search_console_performance` by page for query "spencer pearman") to see which pages get the name impressions; strengthen the homepage as the page about him; (2) add UK-facing proof on /american-voice-over-europe/ (Lisbon = London time zone, live sessions in UK office hours; credits only for clients verified UK-based); (3) link the GFTB profile from the site. Build, screenshot every section, wrangler deploy, push main, IndexNow. `done` with the commit hash.

## E. Profiles
Audit 2026-11-08 (signed out; LinkedIn/YouTube/Voices.com read in Spencer's Chrome): LINK = Voice123, Bodalgo (nofollow), Instagram (bio), IMDb, Wikidata, Qwoted, LinkedIn, YouTube. TEXT only = TikTok (bio links need 1k followers). NO LINK = GFTB (only the mailto: add the website field, his own career profile), Malt, Twine, VoiceBros, Voquent (marketplaces: check each one's terms on off-platform links before asking Spencer; never risk a ban). Follow-up 11-08 (Spencer: "Yes, check and add"): GFTB and VoiceBros ALREADY have https://spencerzvoice.com/ in their Website field (editor read in his Chrome); their public templates don't render it, nothing to fix. Malt, Twine, Voquent: signed out in his Chrome, need his login, then check each editor for a platform-provided website/link field (rules unconfirmed: Malt help pages 404/403, Twine terms 4.2 keep engagements on platform, VoiceBros reportedly closes accounts for sharing contact info, Voquent T&C 403). Rule: add a link only where the editor itself offers the field. Voices.com = NO link on purpose (MEMORY: never hint off-platform there). Site JSON-LD sameAs lacks VoiceBros + Qwoted: add them under move D.
Do: signed-out check that every profile in the site's JSON-LD sameAs (plus VoiceBros, Qwoted) links to spencerzvoice.com and that its headline says American male voice over, Lisbon, Europe. Fix what Bingo may edit itself; list marketplace profile edits for Spencer's OK. `done`/`blocked` accordingly.

## F. Google Analytics (HHM credits stay queued until Nate agrees the terms)
Do: create a GA4 property for spencerzvoice.com in spencer@spencerzvoice.com's Google account (Chrome, his own account; no password typing), add the tag to the site build, deploy, connect it in OpenSEO (`set_google_analytics_property`). `done` with the measurement ID, or `blocked` if a sign-in is needed.

After any move: update the step's status in `reports/visibility-report.html` run log, republish the artifact (publish_files with base_version from get_artifact), log in `memory/<today>.md`, commit + push (bare git commands, AGENTS.md 0c).
