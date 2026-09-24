"""Replace Ableton's video export: put an exported WAV mix onto the original picture.

Usage:  python mux_take.py "<client folder>" [take.wav] [source video]
Defaults: newest .wav in "<client>/Ready to Link to Drafted Email/", and the client's
source video (first non-NOVOX mp4/mov in the client folder).
Export the WAV from Ableton with the render range starting at 1.1.1 (bar 1 = video frame 0).
Output: "<Ready to Link>/<wav name>.mp4" - picture stream-copied (no re-encode), AAC 320k audio.
"""
import glob, os, subprocess, sys

FF = r"C:\Users\spenc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin"


def main():
    cdir = sys.argv[1]
    rdir = os.path.join(cdir, "Ready to Link to Drafted Email")
    wav = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else max(glob.glob(os.path.join(glob.escape(rdir), "*.wav")), key=os.path.getmtime)
    if len(sys.argv) > 3:
        src = sys.argv[3]
    else:
        vids = sorted(f for f in os.listdir(cdir) if f.lower().endswith((".mp4", ".mov")) and "NOVOX" not in f and "no_vocals" not in f)
        src = os.path.join(cdir, vids[0])
    out = os.path.join(rdir, os.path.splitext(os.path.basename(wav))[0] + ".mp4")
    subprocess.run([os.path.join(FF, "ffmpeg.exe"), "-y", "-i", src, "-i", wav, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", out], check=True,
                   capture_output=True)
    print(f"{out}\n  picture: {os.path.basename(src)}\n  audio:   {os.path.basename(wav)}")


if __name__ == "__main__":
    main()
