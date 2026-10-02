"""Narrator gate: is this spot safe for Spencer (male bass/baritone) to re-voice?

Spencer's rule (2026-10-02): a female ANNOUNCER VO is fine. Reject (a) a woman on camera as the
talking head / presenter / speaking lead, and (b) a female VO that is the on-screen woman's own voice
(her inner monologue, first-person "I/my" thoughts while she's the character we follow). A male voice
replacing a woman's own voice is awkward. Talking heads of any gender are already rejected (lip-sync).

Two checks, both required before a spot can be the winner:
  1. VOICE  - pitch (F0) of the narration: >=60% of voiced frames <155 Hz = MALE, >=60% in 170-300 Hz
              = FEMALE, else UNCLEAR. A screen, not proof: SFX (e.g. gong hits) leak into the vocal stem.
              Uses the demucs vocals stem if given (--vocals), else src minus NOVOX audio.
  2. PICTURE - writes a contact sheet (8 evenly spaced frames). LOOK AT IT: reject if a woman is on
              camera talking/presenting, or anyone is lip-synced to the narration.
  If VOICE is FEMALE/UNCLEAR and a woman is the on-screen lead, read the script: first-person /
  her-thoughts VO = reject. Off-screen announcer = OK.

Usage:
  python narrator_check.py --src "<Client> - SOURCE - <title>.mp4" [--vocals vocals.wav | --novox <Client>_NOVOX.mp4] [--sheet out.jpg]
Prints VOICE: MALE/FEMALE/UNCLEAR and the sheet path. Exit 0 = MALE, 1 = FEMALE, 2 = UNCLEAR/no voice.
MALE = voice is fine (still check the picture). FEMALE/UNCLEAR = apply the on-screen-lead + first-person test.
"""
import argparse, os, subprocess, sys
import numpy as np

SR = 16000


def pcm(path):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.int16).astype(np.float32) / 32768


def voice_track(src, vocals=None, novox=None):
    if vocals:
        return pcm(vocals)
    a = pcm(src)
    if novox:
        b = pcm(novox)
        n = min(len(a), len(b))
        return a[:n] - b[:n]
    return a


def f0_track(x):
    win, hop = int(0.05 * SR), int(0.01 * SR)
    lo, hi = int(SR / 400), int(SR / 60)
    frames = [x[i:i + win] for i in range(0, len(x) - win, hop)]
    if not frames:
        return None
    rms = np.array([np.sqrt(np.mean(f ** 2)) for f in frames])
    gate = np.percentile(rms, 60)
    f0s = []
    for f, r in zip(frames, rms):
        if r < gate or r < 1e-3:
            continue
        f = f - f.mean()
        ac = np.correlate(f, f, "full")[win - 1:]
        if ac[0] <= 0:
            continue
        ac = ac / ac[0]
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.7:
            f0s.append(SR / lag)
    return np.array(f0s)


def contact_sheet(src, out):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "csv=p=0", src], capture_output=True, text=True, check=True).stdout)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf",
                    f"fps={8 / max(dur, 1):.4f},scale=320:-2,tile=4x2", "-frames:v", "1", out], check=True)
    return out


def verdict(f0s):
    """Share of clearly voiced frames in each range. SFX (gongs, synths) leak into the vocal stem
    and fake a voice, so a call needs a clear majority, not just a median."""
    if len(f0s) < 50:
        return "UNCLEAR", 2, None, 0, 0
    hz = float(np.median(f0s))
    male, fem = float(np.mean(f0s < 155)), float(np.mean((f0s > 170) & (f0s < 300)))
    if male >= 0.6:
        return "MALE", 0, hz, male, fem
    if fem >= 0.6:
        return "FEMALE", 1, hz, male, fem
    return "UNCLEAR", 2, hz, male, fem


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--src", required=True)
    a.add_argument("--vocals")
    a.add_argument("--novox")
    a.add_argument("--sheet")
    p = a.parse_args()
    v, code, hz, male, fem = verdict(f0_track(voice_track(p.src, p.vocals, p.novox)))
    sheet = contact_sheet(p.src, p.sheet or os.path.splitext(p.src)[0] + "_frames.jpg")
    print(f"VOICE: {v} (median {hz:.0f} Hz, male-range {male:.0%}, female-range {fem:.0%})" if hz
          else f"VOICE: {v} (no clear voice)")
    print(f"PICTURE: look at {sheet} - reject if a woman is on camera talking/presenting, or anyone lip-syncs the VO")
    if code:
        print("CHECK: female/unclear voice - if a woman is the on-screen lead AND the VO is first-person/her thoughts, REJECT")
    sys.exit(code)
