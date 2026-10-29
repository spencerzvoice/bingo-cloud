# SM7B VOX Chain — Audition (built 2026-10-29)

Natural, broadcast-clean audition chain for Spencer's Shure SM7B, built live in Ableton by Bingo.

- **Set:** `G:\Voiceover Work\ShureSM7B VOX Chain Project\ShureSM7B VOX Chain.als`
- **One-drag preset:** User Library > Presets > Audio Effects > Audio Effect Rack > `SM7B VOX Chain - Audition.adg`
- **Renders:** same project folder: `VO Sample - Mixed FINAL.wav` (raw take copied to `Samples\Imported\VO Sample.wav`)
- **Needs the UA Thunderbolt interface connected:** the LA-2A is the UAD-2 (DSP) version; without the hardware it loads disabled.

## Raw take (measured 2026-10-29, ffmpeg EBU R128 + spectrum)
-24.0 LUFS, -4.8 dBTP, LRA 4.3. Dual-mono. Pauses already silent. Heavy 150–700 Hz (close-mic proximity), dip at 2–5 kHz, sibilance at 7–10 kHz, narrow resonances at 520 / 675 / 4170 Hz.

## Chain (in order, exact settings)
| # | Plugin | Settings | Why |
|---|---|---|---|
| 1 | FabFilter Pro-Q 3 (cleanup) | Low Cut 75 Hz, 18 dB/oct, Q 0.71 · Bell 240 Hz −2.5 dB Q 0.9 · Bell 520 Hz −2 dB Q 4 · Bell 675 Hz −2.5 dB Q 5 | Rumble/plosives out, SM7B mud down, two boxy rings notched. Cut before compression so the compressors react to the voice, not the mud. |
| 2 | UAD Teletronix LA-2A Silver | Comp mode, Peak Reduction ≈ 60, Gain left at default, meter on Gain Reduction | Slow optical leveling, 2–3 dB on louder phrases. Rides the fader without changing word shapes. |
| 3 | FabFilter Pro-C 2 | Style Vocal · Threshold −8.8 dB · Attack 3.7 ms · Release ~105 ms · Auto Gain OFF | Catches only the spikes the LA-2A misses (~3 dB on peaks). Attack slow enough that consonants punch through. |
| 4 | FabFilter Pro-Q 3 (tone) | Bell 3.5 kHz +2 dB Q 0.8 · Bell 4170 Hz −2 dB Q 6 · High Shelf 12 kHz +1.5 dB Q 0.7 | Presence for intelligibility, notch the edgy 4.17 k ring, air above the S's. Tone after compression so the boosts aren't fought. |
| 5 | FabFilter Pro-DS | Single Vocal · Split Band · Threshold −40 dB · Range 6 dB · detection 7–14 kHz | De-ess after the brightening. Split band + 6 dB cap = no lisp. |
| 6 | FabFilter Pro-L 2 | Gain +10.6 dB · Output −1.2 dBTP · True Peak Limiting ON · style left at default | Audition loudness; cushion under −1 so MP3 conversion can't clip. |

## Result (FINAL render, measured)
-16.1 LUFS integrated · -1.2 dBTP · LRA 2.7 LU. Hottest S's no harsher than raw (top-1% S-to-body 21.3 dB vs 22.0 raw). LF plosive moments 10 → 2.

## Reusing it on a new take
Gain-dependent settings move with input level (this take: ~-24 LUFS raw, peaks -4.8 dBFS). On a louder/quieter take re-set three things: LA-2A Peak Reduction for 2–3 dB GR on loud phrases, Pro-C 2 threshold for ~3 dB on peaks, Pro-L 2 gain to land -16 LUFS. EQ and de-esser settings stay.
- Export the VO track (Rendered Track = the VO track) or reset the Main fader: this set's Main sits at -6 dB for monitoring.
- Audition target -16 LUFS / ≤ -1 dBTP is common practice; Voices.com / Voice123 publish no official spec (checked 2026-10-29).
- Client deliveries: usually lighter (cleanup + gentle comp + level), not this full chain, unless the client asks for finished audio.
