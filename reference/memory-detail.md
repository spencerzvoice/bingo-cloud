# MEMORY detail

Moved verbatim out of MEMORY.md in the 2026-11-03 prune to keep the always-loaded file small. MEMORY.md keeps a one-line pointer for each.

## YouTube-channel lane

**YouTube-channel lane (Spencer 10-26: "highest on the chain"):** faceless/narrated channels, 400k–1M+ subs, long-form at least monthly; goal 3–4 constant channel clients = €500–1,000/week (a Primal-style video + ad read ≈ €500). Funnel S = 10 tech channels, jumps the drafting order; creator pitch variant leads with Primal Space; re-voice = their latest video. Other genres to follow (his list: pop culture, tech, travel, engineering, health). Rate card (per word, EUR/USD/GBP, 3 sub tiers x 3 lengths, never flat per video; live on the site rate desk 10-28/29): `vo-pricing` "YouTube channel narration".

## Cold-pitch wording

**Cold-pitch wording = `reference/client-acquisition/PITCH-TEMPLATE.md` v6 word for word** (Spencer 10-14; intro "...professional Voiceover Artist and Audio Engineer based in Lisbon, Portugal. I'd love to voice the videos that come out of [Company], like those spreading the word about [event] and any other company news."; "like", never "especially", Spencer 10-22; callback = a lowercase event phrase, never a bare title). Enforced by `pitch_draft_qc.py`. Hook rules: CLAUDE.md override 5. Older templates (TVA model, v3, v4) are dead.

## Follow-ups

**Follow-ups:** cadence + ledger in the `followup-drafts` skill and `memory/followups-queue.md`. Cold touches 2/3 never sit in Drafts: queued in the Follow-up Queue Sheet and sent offline by the Apps Script "Bingo Follow-up Sender" (touch 1 = same day if inside 08:32-15:00 local, else next 08:32 (`scripts/send_slot.py`, 10-27); touch 2 09:04, touch 3 10:13 local; Spencer 10-20; CLAUDE.md override 10); warm/LT stay drafts; Spencer gets the list by push + email the evening before. Day-before push + email before anything due (Spencer 09-25).

## AI-search listings

**AI-search listings: free profiles only** (Spencer 10-20, on Gravy for the Brain: "definitely not... if it's only a paid account"). Don't pitch paid memberships/directories as visibility fixes. **No Upwork account** (Spencer 10-23: "won't create an Upwork account"); don't suggest it again. **Exception: Gravy for the Brain** paid by Spencer's own choice (10-27, Community Only €9.98/mo); his Career Profile Website is live at sites.gravyforthebrain.com/website/spencer-pearman/ ([[website-and-brand]]).

## Rank runs

**Rank runs = every engine, every time** (Spencer 10-31: "Claude always needs to be in every run"): ChatGPT, Claude (claude.ai incognito), Perplexity, Gemini, Copilot, Google AI Mode + Google, Bing, Brave; signed out/incognito only, login state labelled per row. 10-31: Claude still names him nowhere; name prompt cites only the dead Carrd page (`memory/2026-10-31.md`).

## AI/search visibility (10-26 run)

**AI/search visibility (re-run 10-26, detail `memory/2026-10-26.md`):** Google jumped (voicerealm flood gone): Lisbon #1-2 US/GB/PT, Europe phrase PT #1 / US #6 / GB #11, 'voice actor based in Europe' GB #3 / US #5, commercial GB #1 / US #2, name US site #6 (page 1 all his profiles); Bing #1 everywhere except 'voice actor based in Europe' US (dropped out); Brave #1 for all four Europe/Lisbon phrases; ChatGPT #1 for Lisbon AND the bare Europe phrase, not named for 'best' or commercial; Claude still names him nowhere; Bing AI mode cites voiceovers.co.uk talent pages (his profile pending). Perplexity/Gemini/Copilot app = sign-in walls. Malt profile live ([[website-and-brand]]).

## Connectors

**Connectors off by default (Spencer 10-29, usage):** Carly, Gmail (personal), Canva, Figma, Descript. Switch one on (composer + → Connectors, or `set_session_connector_enabled`) only when a task needs it, e.g. Canva for banner work. Kept on: FGAC, Apollo, vidIQ, Calendar, personal Drive, Claude Docs. **OpenSEO plugin off for Bingo** (`.claude/settings.json` enabledPlugins `openseo@openseo: false`; still on globally): for an SEO/AI-visibility check, set it true and start a fresh chat for the check, then set it back false.

## Active routines

**Active routines** (Spencer 10-07): Morning Build `trig_01RN6tiRmzaHdq2NJSzmQxVN`, Re-Voicing, Daily Digest `trig_01MNvx5DJ7fG6ivUmJh2Bxj6` (07:15 UTC, styled HTML via `scripts/digest_render.py` since 10-14; reads the Apps Script "Bingo Digest Prep" tabs first since 10-29, plan `reference/automation-offload-plan.md`), Follow-up Prep (08:40 Pacific Sun–Fri, `CRON_TZ=America/Los_Angeles`, so US sends survive clock changes; set 10-19), Weekly Check-in (Mon). To change one, edit its prompt in `reference/client-acquisition/routines/`. Disabled routines stay disabled; only Spencer deletes them. Crons are UTC unless prefixed `CRON_TZ=`; a send-capable run must land 08:32-15:00 local for every CONTACT-TZ zone in summer AND winter time.

## GPU tools

**Anything the GPU speeds up runs on his RTX 2060 (6 GB)** (Spencer 11-01: "Everything that would benefit from my graphics card should use my graphics card"). New desktop tools get set up for it too, with a CPU fallback for the cloud. Live 11-01: NOVOX separation (audio-separator BS-RoFormer, `C:\Users\spenc\sepenv`), Demucs + openai-whisper (system Python torch 2.11.0+cu128), faster-whisper large-v3 (cuda float16), `mux_take.py` encode (h264_nvenc), **HyperFrames renders = always `--gpu`** (NVENC). Claude's own thinking never uses his GPU.
