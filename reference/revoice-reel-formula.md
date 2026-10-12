# Re-voice reel formula (Spencer's Samsung S26 Ultra reel)

Source: `G:\Videos\1. VO Instagram\Samsung S26 Ultra\FINAL\Samsung S26 Ultra Commercial.mov` (IG @spencerzvoiceovers, 2026-07-08, one of his best posts). Measured by Bingo 2026-10-12 against the source clips. Spencer: "this is the formula and the editing style that I want", so every re-voice reel copies it. Built in HyperFrames, always.

## Structure (Samsung timings, 34.9 s, 1080x1920, timeline fps = the ad's native fps)
1. **Cold open, 0-2.4 s:** the ORIGINAL ad with its own narrator, first line only ("This is it."). Ad full width, centered on black (1096x616 at y=652, a hair wider than the frame), no captions. Starts at the ad's first visible frame (Samsung: 1.88 s in). Ad audio fades in ~0.5 s, sits ~-6 dB.
2. **Hook, 2.4-7.0 s:** hard cut. Ad jumps to the top (y=2) and keeps rolling (no restart). Spencer talks to camera in the panel below (from y=542), punched in ~1.27x: "How would I record this <Brand> commercial, you ask? Let's see..." His voice J-cuts in ~0.3-0.4 s before the picture. Original ad audio keeps playing under him at ~-23.5 dB.
3. **Re-voice, 7.0-32.9 s:** hard cut. Ad restarts from the same opening frame, now with his VO mix at unity. Booth panel from y=617 (ad band fully visible), booth footage unzoomed (1080 wide), slid up so his face sits right under the ad; synced to the VO. Samsung's 3.5-min ad was cut down to ~26 s (one jump to the end slate).
4. **Breath, ~0.5 s:** ad over, booth goes full screen (unzoomed), no caption, music tail.
5. **Ask, last ~1.5 s:** full-screen talk-to-camera, punched in ~1.15x: "Get at me, <Brand>." Voice J-cuts slightly ahead. Ends ~0.4 s after the last word. No end card (Samsung).

## Captions (only on Spencer's voice, never on the original narrator)
- Short phrase chunks, often single words for rhythm ("easy", "and", "S26", "Ultra."); punctuation kept ("Let's see...", "processor,").
- Hard cut on/off, no animation. Disappear during pauses; with no pause the next chunk replaces the last.
- Centered x=540, text band y~1500-1585, ~85 px cap-top-to-descender, no outline.
- Samsung used Niagara Solid in yellow #F8D63B. **From 2026-10-12 on: brand fonts and colours instead** (Spencer: "use one from my brand book... start branding from here on out"). Brand book v2: Lexend Exa = wordmark/headlines, Lexend = body, Lamp Amber #F0B13C, Booth Navy #0B0F15, Paper #F1ECE3, Steel #A9B2BE.

## Finish
No stylised grade (footage ~10% brighter than raw). Reel loudness ~-18 LUFS; his mix untouched.

## Mix, cuts and motion rules (Spencer, 2026-10-12, after the Premier Padel v1)
- **Couch / talk-to-camera VO is mixed and mastered:** mono, dead centre (use the unclipped channel if the camera split them), light denoise, rumble cut, mud cut, gentle compression, clarity, air.
- **No level jumps:** every section (original-ad open, hook, re-voice, outro) level-matched within ~1 LU; ad bed ~20 dB under the hook voice; master to about -16 LUFS, true peak <= -1.5 dBTP. Measure the render per section, don't guess.
- **As few cuts as possible:** one ad jump at most, cut on the ad's own shot change. Booth stays one continuous shot: slow the camera through silent breaths instead of cutting; cut only where the comp switches takes.
- **Slow, tasteful push-ins** on every shot (about 5-16% over the shot), no snap punch-ins, no flash, no layout switching.
- **HyperFrames lip-sync:** shift camera clips' data-media-start +0.040 s (HF shows frames ~40 ms early); verify by frame-matching a zoom-free test render.
