"""Head-to-head: current Demucs NOVOX vs RoFormer models on one source clip."""
import os, subprocess, sys, time, glob

SRC = sys.argv[1]
OUT = sys.argv[2]
MODELS = sys.argv[3:]
SEP = r"C:\Users\spenc\sepenv\Scripts\audio-separator.exe"
MDIR = r"C:\Users\spenc\sepenv\models"
os.makedirs(OUT, exist_ok=True)
wav = os.path.join(OUT, "src.wav")
if not os.path.exists(wav):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-vn", "-ac", "2", "-ar", "44100", wav], check=True)
for spec in MODELS:
    m, _, ov = spec.partition("@")
    d = os.path.join(OUT, spec.replace(".", "_").replace("@", "_ov"))
    if glob.glob(os.path.join(d, "*.wav")):
        continue
    t = time.time()
    args = [SEP, wav, "--model_file_dir", MDIR, "--output_dir", d, "--output_format", "WAV"]
    args += ["--ensemble_preset", m[7:]] if m.startswith("preset:") else ["-m", m]
    if ov:
        args += ["--mdxc_overlap", ov]
    r = subprocess.run(args, capture_output=True, text=True)
    print(spec, f"{time.time() - t:.0f}s", "rc", r.returncode, flush=True)
    if r.returncode:
        print(r.stderr[-1500:])
