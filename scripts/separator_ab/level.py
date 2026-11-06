"""Two-way bed leveler: lift the ducked stretches under the old narrator AND pull the gap swells down, so the bed sits
flat and the Ableton sidechain under Spencer's read does the only ducking.
usage: level.py bed.wav vocals.wav out.wav [target_offset_db] [max_boost] [max_cut]"""
import sys, numpy as np, soundfile as sf
from scipy.ndimage import uniform_filter1d, minimum_filter1d
bed_p, voc_p, out_p = sys.argv[1:4]
off = float(sys.argv[4]) if len(sys.argv) > 4 else -3.0
mb = float(sys.argv[5]) if len(sys.argv) > 5 else 20.0
mc = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0
win = int(float(sys.argv[7]) * 200) if len(sys.argv) > 7 else 40   # level window, seconds
ratio = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0           # 1 = flat, <1 keeps some movement
x, sr = sf.read(bed_p, always_2d=True); v, _ = sf.read(voc_p, always_2d=True)
hop = sr // 200                                         # 5 ms
def lev(y, win):
    y = y.mean(1); n = len(y) // hop
    e = (y[:n*hop].reshape(n, hop) ** 2).mean(1)
    return 10*np.log10(uniform_filter1d(e, win) + 1e-12)
bl = lev(x, win)
vl = lev(v, 20)
n = min(len(bl), len(vl)); bl, vl = bl[:n], vl[:n]
talk = vl > vl.max() - 25
gap_lv = np.median(bl[~talk]); target = gap_lv + off
gain = np.clip((target - bl) * ratio, -mc, mb)
gain = np.where(bl < target - 40, 0, gain)               # never pump up true silence
gain = minimum_filter1d(gain, 30)                         # 150 ms: take the lower gain nearby -> no overshoot on swell attacks
gain = uniform_filter1d(gain, max(50, win // 2))
g = np.repeat(10 ** (gain / 20), hop)
g = np.pad(g, (0, max(0, len(x) - len(g))), mode="edge")[:len(x)]
y = x * g[:, None]
pk = np.abs(y).max()
if pk > 0.89: y *= 0.89 / pk
sf.write(out_p, y, sr, subtype="PCM_24")
o = y.mean(1); h = sr // 2; m = len(o) // h
l = 20*np.log10(np.sqrt((o[:m*h].reshape(m, h)**2).mean(1)) + 1e-9)
print(f"target {target:.1f} dB | 0.5 s levels: min {l.min():.1f} max {l.max():.1f} std {l.std():.1f} dB")
print(" ".join(f"{a:.0f}" for a in l))
