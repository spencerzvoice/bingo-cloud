"""Score instrumental beds for Epic History.
- dip: bed level in the voice band (300 Hz-4 kHz) while he speaks minus in pauses. Strongly negative = music carved
  out under every line (pumping). Positive = voice leaking.
- bleed: correlation of the bed's 1-4 kHz envelope with the narrator's. ~0 = clean.
- pause SNR: in pauses the bed should equal the mix. src vs bed residual, higher = more faithful.
- air: energy above 10 kHz, bed vs its own source (dB). Strongly negative = dull / underwater.
"""
import sys, glob, os
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

W = sys.argv[1]
voc = glob.glob(os.path.join(W, "model_bs_roformer_ep_317*", "*(Vocals)*.wav"))[0]
beds = {"A current NOVOX (AAC src, ep_317)": (os.path.join(W, "A_current_novox.wav"), os.path.join(W, "src_aac.wav"))}
for p in sorted(glob.glob(os.path.join(W, "*", "*(Instrumental)*.wav")) + glob.glob(os.path.join(W, "*", "*(other)*.wav"))):
    beds[os.path.basename(os.path.dirname(p)) + " (Opus src)"] = (p, os.path.join(W, "src_opus.wav"))


def load(p):
    x, sr = sf.read(p, always_2d=True)
    return x.mean(1), sr


def frames(y, sr):
    hop = sr // 20
    n = len(y) // hop
    return y[: n * hop].reshape(n, hop)


def band(y, sr, lo, hi):
    sos = butter(4, [lo, hi], "bandpass", fs=sr, output="sos") if hi else butter(4, lo, "highpass", fs=sr, output="sos")
    return sosfilt(sos, y)


v, sr = load(voc)
vdb = 10 * np.log10((frames(band(v, sr, 300, 4000), sr) ** 2).mean(1) + 1e-12)
speech = vdb > vdb.max() - 30
venv = np.log(np.sqrt((frames(band(v, sr, 1000, 4000), sr) ** 2).mean(1) + 1e-12))
print(f"speech frames {speech.mean():.0%}")
for name, (bp, sp) in beds.items():
    b, _ = load(bp)
    s, _ = load(sp)
    n = min(len(b), len(s))
    b, s = b[:n], s[:n]
    bdb = 10 * np.log10((frames(band(b, sr, 300, 4000), sr) ** 2).mean(1) + 1e-12)
    m = min(len(bdb), len(speech))
    sp_, pa = speech[:m], ~speech[:m]
    dip = bdb[:m][sp_].mean() - bdb[:m][pa].mean()
    benv = np.log(np.sqrt((frames(band(b, sr, 1000, 4000), sr) ** 2).mean(1) + 1e-12))
    k = min(len(benv), len(venv))
    bleed = np.corrcoef(benv[:k], venv[:k])[0, 1]
    fb, fs_ = frames(b, sr)[:m], frames(s, sr)[:m]
    res = ((fs_[pa] - fb[pa]) ** 2).sum()
    snr = 10 * np.log10((fs_[pa] ** 2).sum() / (res + 1e-12))
    air = 10 * np.log10((band(b, sr, 10000, None) ** 2).mean() / ((band(s, sr, 10000, None) ** 2).mean() + 1e-20))
    rms = 20 * np.log10(np.sqrt((b ** 2).mean()) + 1e-12)
    print(f"{name:62s} bed {rms:6.1f} dBFS | dip {dip:+5.1f} dB | bleed {bleed:5.2f} | pause SNR {snr:5.1f} dB | air {air:+5.1f} dB")
