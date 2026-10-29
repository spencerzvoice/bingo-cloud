"""Ghost-voice test: how much louder the bed gets in the voice band (300 Hz-4 kHz) while the narrator speaks
vs in the pauses. Music doesn't care when he talks, ghost voice does. ~0 dB = clean; higher = voice leaking."""
import sys, glob, os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

d = sys.argv[1]
beds = {"demucs (current)": os.path.join(d, "demucs_current.wav")}
for p in glob.glob(os.path.join(d, "*", "*Instrumental*.wav")):
    beds[os.path.basename(os.path.dirname(p))] = p
voc = glob.glob(os.path.join(d, "model_bs_roformer*", "*Vocals*.wav"))[0]

def band(p, sr_lo=300, sr_hi=4000):
    x, sr = sf.read(p, always_2d=True)
    y = sosfilt(butter(4, [sr_lo, sr_hi], "bandpass", fs=sr, output="sos"), x.mean(1))
    hop = sr // 20
    n = len(y) // hop
    return 10 * np.log10((y[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)

v = band(voc)
speech = v > v.max() - 30
for name, p in beds.items():
    b = band(p)
    n = min(len(b), len(v))
    s, g = speech[:n], ~speech[:n]
    print(f"{name:42s} speech {b[:n][s].mean():6.1f} dB  pauses {b[:n][g].mean():6.1f} dB  swell {b[:n][s].mean() - b[:n][g].mean():+5.1f} dB  ({s.mean():.0%} speech)")
