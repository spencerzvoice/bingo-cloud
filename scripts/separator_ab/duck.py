import sys, glob, os, numpy as np, soundfile as sf
W = sys.argv[1]
def lv(p, hop_s=0.5):
    x, sr = sf.read(p, always_2d=True); x = x.mean(1); h = int(sr*hop_s); n = len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
v = lv(glob.glob(os.path.join(W,"mel_band*","*(Vocals)*.wav"))[0])
b = lv(glob.glob(os.path.join(W,"mel_band*","*(Instrumental)*.wav"))[0])
first = np.argmax(v > v.max()-25)
print("first speech at", first*0.5, "s")
sp = v > v.max()-25
body = np.arange(len(v)) >= first
print("body: bed in speech %.1f dB, bed in gaps %.1f dB, gaps n=%d" % (b[body&sp].mean(), b[body&~sp].mean(), (body&~sp).sum()))
print("intro bed (before speech) %.1f dB" % b[:first].mean() if first else "no intro")
print(" t   voice  bed")
for i in range(0, len(v), 2): print(f"{i*0.5:4.0f} {v[i]:6.1f} {b[i]:6.1f}")
