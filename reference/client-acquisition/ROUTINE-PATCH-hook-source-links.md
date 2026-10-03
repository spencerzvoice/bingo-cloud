# Routine patch: source link inside [YOUR TAKE] (2026-10-03)

Bingo can't edit these two routines (update_trigger refuses routines created outside an agent). Spencer pastes this in at claude.ai/code/routines. Delete this file once both are done.

## Paste this paragraph into BOTH routines

Daily VO Lead Batch (`trig_01GycTKwkwLwvNhYL6huQQ2w`): put it right after the "HOOK = EVENT LINE ONLY, SPENCER WRITES THE TAKE" bullet.
Hook Sweep (`trig_01FQkrArSyKVS3241Qu8qCcM`): put it right after the "HOOK RULE" paragraph.

```
SOURCE LINK IN [YOUR TAKE] (Spencer, 2026-10-03, HARD RULE; overrides every plain "[YOUR TAKE]" in this prompt). Spencer can't write a take without seeing what the hook refers to, so the placeholder always carries a clickable link to the hook's source:
<span style="background-color:#ffff00">[YOUR TAKE] Source: <a href="URL">Publication, Mon D, YYYY</a></span>
The link is the exact page you opened that the event line is based on. If the line says watched/spot/film, link the video page itself (YouTube/Vimeo/iSpot). Otherwise link the LinkedIn post, press release or article. Two links max (article + video), separated by " · ". No openable URL = no hook: use the [HOOK: nothing current found...] placeholder instead. The event line says only what the linked page shows. On 10-03, "Just watched the Ferrari Hypersail film" was backed by a press release with no film. When you read a draft back, check that the [YOUR TAKE] placeholder contains a working <a href> link.
```

## Hook Sweep only: add to the TAKE PENDING bullet in step 1

```
If the [YOUR TAKE] placeholder has no "Source:" link, add one. Use the source URL logged for that company in FUNNEL-COHORTS.md or the contacts docs, or WebSearch the event and open the page to confirm it backs the event line. If no source backs the line, replace it with a line that is backed, or with the [HOOK: ...] placeholder.
```

## Also replace this example line in both

`"Just watched the Ferrari Hypersail film."` → `"Saw the Toast Fuel launch."` (the ABB line wasn't backed by its source).
