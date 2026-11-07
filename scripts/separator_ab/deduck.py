"""Undo the source mix's music ducking: ride the bed back up to its between-line level wherever the original narrator spoke."""
import sys, numpy as np, soundfile as sf
from scipy.ndimage import uniform_filter1d
bed_p, voc_p, out_p = sys.argv[1:4]
x, sr = sf.read(bed_p, always_2d=True); v, _ = sf.read(voc_p, always_2d=True)
hop = sr // 100                       # 10 ms
def lev(y, win):
    y = y.mean(1); n = len(y) // hop
    e = (y[:n*hop].reshape(n, hop) ** 2).mean(1)
    return 10*np.log10(uniform_filter1d(e, win) + 1e-12)
bl, vl = lev(x, 30), lev(v, 30)
n = min(len(bl), len(vl)); bl, vl = bl[:n], vl[:n]
talk = vl > vl.max() - 25
gap_level = np.median(bl[~talk])
gain = np.where(talk, np.clip(gap_level - 3 - bl, 0, 18), 0.0)   # sit 3 dB under the gap level, max +18 dB
gain = uniform_filter1d(gain, 25)                                  # 250 ms smoothing, no pumping
g = np.repeat(10 ** (gain / 20), hop)
g = np.pad(g, (0, max(0, len(x) - len(g))), mode="edge")[:len(x)]
y = x * g[:, None]
pk = np.abs(y).max()
if pk > 0.89: y *= 0.89 / pk                                       # -1 dBFS ceiling
sf.write(out_p, y, sr, subtype="PCM_24")
print(f"gap level {gap_level:.1f} dB, mean boost under lines {gain[talk].mean():.1f} dB, peak scale {min(1, 0.89/pk):.2f}")
