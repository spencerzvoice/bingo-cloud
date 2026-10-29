"""Score each instrumental bed: ghost words Whisper can still hear, voice-envelope bleed, and bed level."""
import sys, glob, os
import numpy as np, soundfile as sf, whisper
from scipy.signal import butter, sosfilt

d = sys.argv[1]
beds = {"demucs (current)": os.path.join(d, "demucs_current.wav")}
for p in glob.glob(os.path.join(d, "*", "*.wav")):
    n = os.path.basename(p).lower()
    if "instrumental" in n or "no_vocals" in n or ("vocals" not in n and "instrumental" not in n):
        beds[os.path.basename(os.path.dirname(p))] = p
voc = [p for p in glob.glob(os.path.join(d, "model_bs_roformer*", "*.wav")) if "(vocals)" in p.lower()][0]

def mono(p):
    x, sr = sf.read(p, always_2d=True)
    return x.mean(1), sr

v, sr = mono(voc)
sos = butter(4, [1000, 4000], "bandpass", fs=sr, output="sos")
hop = sr // 20
def env(x):
    y = sosfilt(sos, x)
    n = len(y) // hop
    return np.sqrt((y[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
ve = env(v)
model = whisper.load_model("base")
for name, p in beds.items():
    x, _ = mono(p)
    e = env(x)
    n = min(len(e), len(ve))
    corr = np.corrcoef(np.log(e[:n]), np.log(ve[:n]))[0, 1]
    rms = 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
    r = model.transcribe(p, language="en", condition_on_previous_text=False, fp16=False)
    words = [w for s in r["segments"] if s["no_speech_prob"] < 0.6 for w in s["text"].split()]
    print(f"{name:45s} bed {rms:6.1f} dBFS | voice-envelope bleed {corr:5.2f} | ghost words {len(words):3d} | {' '.join(words)[:90]}")
