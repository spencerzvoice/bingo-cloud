---
name: revoice-material
description: How Spencer's re-voicing sample assets get built — source commercial → download → vocal-stripped NOVOX → script → per-video Ableton project → Client Outreach/<Funnel>/<Client>/. Use when asked how the assets were made, to rebuild/extend them for a new funnel/client, or when a client folder is missing its pieces.
---

# Re-voicing material pipeline

Purpose: for each prospect, one real **scripted single-narrator commercial** the client already made → Spencer re-voices it → the sample goes in the pitch email. Built 2026-09-10/11 (Funnel B/C/D); documented 2026-09-23 so it isn't lost again.

## Where everything lives
- **`D:\My Drive\Client Outreach\`** — Google-Drive-synced local folder (Desktop shortcut "Client Outreach"). Drive folder id `1zZ9owoCgehA-p68i30sC-1u7zPGQtuOh` (My Drive root). NOT in this repo.
- Layout: `Client Outreach/<Funnel X>/<Client>/` holds: source `.mp4`, `<Client>_NOVOX.mp4`, `<Client>_script.docx`, `sources.txt` (URL per line), `<Client> Project/` (Ableton), and `Ready to Link to Drafted Email/` (finished take goes here).
- Multi-video clients: one Ableton project **per video** — `<Client> Project`, `<Client> 2 Project`.
- Separate from `New Client Acquisition` (Spencer's finished deliverables) — never write there.
- Ableton template: `Client Outreach/Ableton Template Project/Ableton Template.als` (Live 12.4.2).

## Tooling (Windows; `python -m`, not bare exes — Scripts dir isn't on PATH)
- `python -m yt_dlp` (download + captions). Harmless warning: "No supported JavaScript runtime".
- ffmpeg/ffprobe: `C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\` (winget `Gyan.FFmpeg`; prepend to PATH).
- `python -m pip install --user demucs numpy openai-whisper` (CPU-only torch; no CUDA). numpy must be installed separately.
- Run ffprobe/ffmpeg via **Python `subprocess` with Windows paths** — Git Bash mangles paths containing `[brackets]`, `’` and spaces.

- **Download fixes learned 2026-09-24 (Funnel D):** `height=1080` misses widescreen crops (1920x1012) — use `height<=1080`. YouTube needs a JS runtime: `pip install --user deno` and put `%APPDATA%\Python\Python314\Scripts` on PATH. Vimeo "only works when logged-in" → use the `player.vimeo.com/video/<id>` embed URL with `--referer <site> --impersonate chrome` (`pip install --user curl_cffi`). Agency sites often embed the full spots from Vimeo — scrape the project page for `player.vimeo.com/video/` ids. Claude Code's Bash sandbox blocks network — downloads need the sandbox off. YouTube "Please sign in" on some videos = bot gate; skip to another candidate rather than using browser cookies.
- **Builder script:** `.claude/skills/revoice-material/scripts/revoice_build.py "<Funnel dir>" [Client ...]` — idempotent: downloads from `sources.txt` if no video, Demucs NOVOX, Ableton project. Multi-video clients: name NOVOX/script `<Client>_<Title>_NOVOX.mp4` and pass n=2 for `<Client> 2 Project`.

## Step 1 — Pick the video (per client)
Real commercial/brand spot, **scripted, single narrator, ~8–125 s**. Reject tutorials, webinars, product overviews/walkthroughs, interviews/panels/podcasts, keynotes, testimonial montages, talking-head, music-only sizzles, anything ≳2 min. Website-embedded marketing videos outrank generic channel uploads. Spencer hand-picked the Funnel B/C sources; the routine (below) scrapes for new funnels.

## Step 2 — Download
```
python -m yt_dlp -f "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]/best" --merge-output-format mp4 --restrict-filenames -o "<dest>/%(title)s [%(id)s].%(ext)s" "<url>"
```
Unlisted playlists need their `&si=` token. Route by the video's YouTube **channel name → client folder** (matched every client). Write the URL to `sources.txt`.

## Step 3 — Strip the vocals → `<Client>_NOVOX.mp4`
Offline via **Demucs** (replaces lalal.ai; Funnel B was originally split with lalal.ai — those files are `*_no_vocals_split_by_lalalai.mp4`).
```
ffmpeg -i src.mp4 -vn -ac 2 -ar 44100 audio.wav
python -m demucs --two-stems=vocals -o stems audio.wav        # -> stems/htdemucs/audio/no_vocals.wav
ffmpeg -i src.mp4 -i stems/htdemucs/audio/no_vocals.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest "<Client>_NOVOX.mp4"
```
Picture untouched (`-c:v copy`); audio = music/SFX bed only. ~15–60 s/clip on CPU after the one-time ~80 MB model download. Spot-check for ghosting on dense mixes. Skip files that are already music-only (e.g. `MasterClass_Background_Music.mp4`).

## Step 4 — Script → `<Client>_script.docx` (**.docx, not .txt** — Spencer, 2026-09-24; python-docx, one paragraph per block)
- YouTube: `python -m yt_dlp --write-subs --write-auto-subs --sub-langs "en.*" --sub-format vtt --skip-download -o "%(id)s.%(ext)s" <url>` → strip timestamps/tags/dupes → punctuate and paragraph. Prefer human subs over auto.
- No captions (e.g. iSpot download): `whisper audio.wav --model small --output_format txt` (16 kHz mono wav; ffmpeg must be on PATH).
- First line of the file: `Original copy - from captions, verify against the video.` (or `... Whisper transcription ...`).
- Spencer also gets one `.docx` per spot emailed to himself ("Funnel B Copy" / "Funnel C Copy") — minimal hand-rolled OOXML zips (~1.5 KB each; python-docx output is ~35 KB and too big to inline as base64 attachments).
- Don't script multi-speaker documentary/interview pieces (Big Think dropped for this reason) — not re-voiceable.

## Step 5 — Ableton project per video (fully automated, verified 2026-09-11)
`.als` = **gzip-compressed XML**. Copy the template folder to `<Client>/<Client> Project/`, rename the `.als` to `<Client> Project.als`, then patch the two clips named `ORIGINAL VIDEO` and `VIDEO WITHOUT VOX`. Inside each `<AudioClip>` → `<SampleRef>`:
- `<FileRef>`: `RelativePath` = `../<filename>`, `Path` = absolute path with forward slashes, `OriginalFileSize` = real bytes.
- `DefaultDuration` = duration_s × sample_rate; `DefaultSampleRate` from `ffprobe -select_streams a:0 -show_entries stream=sample_rate`.
- Beat-length fields `CurrentEnd`, `LoopEnd`, `OutMarker`, `HiddenLoopEnd`, `ScrollerTimePreserver/RightTime` = **duration_s × 2** (template tempo is fixed 120 BPM manual → 1 beat = 0.5 s).
- Leave `WarpMarkers` alone (template's 2-point linear 120 bpm map is file-independent).
- ORIGINAL VIDEO ← source mp4; VIDEO WITHOUT VOX ← NOVOX mp4. (`Duration` from `ffprobe -show_entries format=duration`.)
- Re-gzip with `gzip.GzipFile(path,"wb",mtime=0)`; `ET.fromstring()` the XML before and after round-trip.
Live Ableton needs nothing else to treat an mp4 as video+audio; a bare `VO` track "Sample Offline" and a "Media files are missing" banner on first open come from template leftovers, not the patched clips. Verified: project opened, Video Window played real frames, status bar showed the exact file path.
Template tracks: `VO Chain` > `VO` (full mix chain), `~VAL/~SHORT/~LMS` refs, `ORIGINAL VIDEO`, `VIDEO WITHOUT VOX`, returns, `Main`.

## Step 6 — Hand-off
Spencer opens the project, records over NOVOX, exports the take into `Ready to Link to Drafted Email/`, links it in the drafted email. Every Drive client folder gets that subfolder at creation.

## Automation (cloud routines)
- **Daily VO Lead Batch — 8am** (`trig_0169PRDf1iYUFDAXaMMaDDf4`, weekdays 07:00 UTC): finds companies + drafts outreach **only if the business Drafts folder is clear**; assigns the next `Funnel <letter>` per *drafted* cohort and creates `Client Outreach/Funnel X/<Company>/` + `Ready to Link to Drafted Email/`. Uses FGAC + `spencer@spencerzvoice.com` explicitly; the generic `Gmail` connector (personal account) was removed 2026-09-11 after it drafted 9 emails into the personal inbox.
- **Re-Voicing Material Retrieval — daily** (`trig_01L7j1hN3yToMTFnbBkSTAg2`, weekdays 10:00 UTC): READY = has a Funnel folder + an unsent Gmail draft to that company + folder has no video yet. Scrapes site/YouTube for the spot, downloads, Demucs-strips, extracts script, uploads to Drive (base64; 720p re-encode fallback if too big). **Stage 2 (download→Demucs→upload) was never proven end-to-end** — assets to date were built locally. Funnel membership comes from the Drive folder tree, never the tracker sheet.
- Manage via the `RemoteTrigger` tool. `job_config.ccr` is full-replace on update; connector `tool_policy_overrides` = `always_allow` prevents headless permission stalls (WebFetch domain prompts can't be pre-approved this way — `auto_mode_allow` was tried 2026-09-11, unverified).

## Gotchas
- Always verify the real contact/draft state live (Gmail via FGAC) before touching outreach — see CLAUDE.md 2a.
- Funnel letters: A/B hand-built, C = e-learning, D = Shell/Experian/Shelter UK/Purdue/Snowflake/Sarofsky/Tendril/Goalhanger/iAM Learning/Skillsoft (all 10 packages built 2026-09-24); next drafted cohort = next letter.
- Big files (>~20 MB) may fail the Drive API base64 upload; Drive-for-Desktop local copy avoids it.
